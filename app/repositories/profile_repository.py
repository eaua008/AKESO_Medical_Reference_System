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
