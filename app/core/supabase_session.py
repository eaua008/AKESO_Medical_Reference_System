"""The signed-in Supabase connection, shared by the account repositories.

Why this wrapper exists
-----------------------
Only AuthRepository's client holds the signed-in session; every other
repository uses its own client with the publishable key, which is fine for
public reference data. Account data is private (row-level security), so
those requests must carry the user's access token.

supabase-py keeps the token in its request headers, but only updates them
on some auth events. After a password/email change (USER_UPDATED) or a
two-factor check (MFA_CHALLENGE_VERIFIED) the headers can fall back to the
publishable key, and the database would then treat the user as signed out.
So this class never trusts the stored headers: every request asks the auth
client for the current token first (refreshing it if it expired) and sets
it explicitly.

It also serialises requests with a lock. Account calls run on background
threads, and one httpx client should not be used by two threads at once.
"""

import threading
from contextlib import contextmanager
from typing import Any, Callable, Iterator, Optional, TypeVar

from storage3 import SyncStorageClient
from supabase import Client
from supabase_functions import SyncFunctionsClient

T = TypeVar("T")


class SessionExpired(Exception):
    """The session is gone (signed out elsewhere, or the refresh failed)."""


class SessionClient:
    """Authenticated access to PostgREST, RPC, Storage and Edge Functions."""

    def __init__(self, client: Client) -> None:
        self._client = client
        self._lock = threading.RLock()

    # ----------------------------------------------------------- plumbing

    @property
    def auth(self):
        """The Supabase auth client (password, email, two-factor, sign-out)."""
        return self._client.auth

    @contextmanager
    def locked(self) -> Iterator[None]:
        with self._lock:
            yield

    def run(self, call: Callable[[], T]) -> T:
        """Run one request (or a few that belong together) under the lock."""
        with self._lock:
            return call()

    def access_token(self) -> str:
        session = self._client.auth.get_session()   # refreshes when expired
        if session is None or not session.access_token:
            raise SessionExpired("Your session has ended. Please sign in again.")
        return session.access_token

    def user_id(self) -> str:
        session = self._client.auth.get_session()
        if session is None or session.user is None:
            raise SessionExpired("Your session has ended. Please sign in again.")
        return session.user.id

    def _headers(self) -> dict[str, str]:
        return {
            "apiKey": self._client.supabase_key,
            "Authorization": f"Bearer {self.access_token()}",
        }

    # ----------------------------------------------------------- services

    def table(self, name: str):
        rest = self._client.postgrest
        rest.auth(self.access_token())
        return rest.from_(name)

    def rpc(self, function: str, params: Optional[dict[str, Any]] = None):
        rest = self._client.postgrest
        rest.auth(self.access_token())
        return rest.rpc(function, params or {})

    def bucket(self, name: str):
        storage = SyncStorageClient(str(self._client.storage_url), self._headers())
        return storage.from_(name)

    def invoke(self, function: str, body: dict[str, Any]) -> Any:
        """Call an Edge Function as the signed-in user; returns parsed JSON.

        The functions client lets its own headers win over per-call ones,
        so the token has to go in when the client is built, not per call.
        """
        functions = SyncFunctionsClient(str(self._client.functions_url), self._headers())
        return functions.invoke(function, {"body": body, "responseType": "json"})
