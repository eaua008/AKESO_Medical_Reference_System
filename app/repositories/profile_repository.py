"""Profile, role and profile photo, in Supabase.

Row-level security limits every query here to the signed-in account, so
no method takes a user id from the caller: the id always comes from the
session itself.
"""

from typing import Optional

from app.core.supabase_session import SessionClient
from app.repositories.account_errors import AccountError, friendly

AVATAR_BUCKET = "avatars"


class ProfileRepository:
    def __init__(self, session: SessionClient) -> None:
        self._s = session

    def _do(self, call):
        try:
            return self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise AccountError(friendly(exc)) from exc

    # ------------------------------------------------------------ profile

    def get(self) -> dict:
        def call():
            uid = self._s.user_id()
            rows = self._s.table("profiles").select("*").eq("id", uid).limit(1).execute().data
            if not rows:
                raise AccountError("Your profile was not found. Is migration 002 installed?")
            return rows[0]
        return self._do(call)

    def update(self, changes: dict) -> dict:
        def call():
            uid = self._s.user_id()
            rows = self._s.table("profiles").update(changes).eq("id", uid).execute().data
            if not rows:
                raise AccountError("Your profile could not be saved.")
            return rows[0]
        return self._do(call)

    def role(self) -> str:
        def call():
            uid = self._s.user_id()
            rows = (self._s.table("user_roles").select("role").eq("user_id", uid)
                    .limit(1).execute().data)
            return rows[0]["role"] if rows else "student"
        return self._do(call)

    def handle_available(self, handle: str) -> bool:
        return bool(self._do(lambda: self._s.rpc("handle_available", {"p_handle": handle})
                             .execute().data))

    # Changing the handle (migration 043): only through these functions,
    # which check the format, reserved words, taken handles and the
    # once-every-30-days rule.
    def handle_check(self, handle: str) -> Optional[str]:
        return self._rpc_043("handle_check", {"p_handle": handle})

    def handle_change_info(self) -> dict:
        return self._rpc_043("handle_change_info", {}) or {}

    def change_handle(self, handle: str) -> str:
        return str(self._rpc_043("change_handle", {"p_handle": handle}))

    def _rpc_043(self, function: str, params: dict):
        def call():
            return self._s.rpc(function, params).execute().data
        try:
            return self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            text = (getattr(exc, "message", None) or str(exc)).lower()
            if "could not find the function" in text or "schema cache" in text:
                raise AccountError("Changing your handle isn't set up on Akeso's server yet. "
                                   "The administrator needs to run "
                                   "database/migrations/043_change_handle.sql.") from exc
            raise AccountError(friendly(exc)) from exc

    # ------------------------------------------------------------- avatar

    def upload_avatar(self, png: bytes) -> str:
        """Store the photo at <user id>/avatar.png and return that path."""
        def call():
            path = f"{self._s.user_id()}/avatar.png"
            self._s.bucket(AVATAR_BUCKET).upload(
                path, png, {"content-type": "image/png", "upsert": "true",
                            "cache-control": "60"})
            return path
        return self._do(call)

    def download_avatar(self, path: str) -> Optional[bytes]:
        def call():
            try:
                return self._s.bucket(AVATAR_BUCKET).download(path)
            except Exception as exc:  # noqa: BLE001
                if "not found" in str(exc).lower() or "404" in str(exc):
                    return None
                raise
        return self._do(call)

    def remove_avatar(self, path: str) -> None:
        self._do(lambda: self._s.bucket(AVATAR_BUCKET).remove([path]))
