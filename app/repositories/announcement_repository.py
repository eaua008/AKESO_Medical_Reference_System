"""Announcements in Supabase (migration 015).

Every call is one of the announcement database functions. They decide who
sees what and refuse non-admins for the admin_* ones, so this class is
only a thin, typed wrapper.
"""

from typing import Optional

from app.core.supabase_session import SessionClient
from app.models.announcement import Announcement
from app.repositories.account_errors import AccountError, friendly


class AnnouncementRepository:
    def __init__(self, session: SessionClient) -> None:
        self._s = session

    def _rpc(self, function: str, params: Optional[dict] = None):
        def call():
            return self._s.rpc(function, params or {}).execute().data
        try:
            return self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            message = (getattr(exc, "message", None) or str(exc)).lower()
            if "could not find the function" in message or "schema cache" in message:
                raise AccountError("Announcements aren't installed yet. Run "
                                   "database/migrations/015_announcements.sql.") from exc
            raise AccountError(friendly(exc)) from exc

    # ------------------------------------------------------------ everyone

    def mine(self) -> list[Announcement]:
        return [Announcement.from_row(r) for r in self._rpc("my_announcements") or []]

    def dismiss(self, announcement_id: str) -> None:
        self._rpc("dismiss_announcement", {"p_id": announcement_id})

    # -------------------------------------------------------------- admins

    def all(self) -> list[Announcement]:
        return [Announcement.from_row(r) for r in self._rpc("admin_list_announcements") or []]

    def save(self, item: Announcement, reshow: bool = False) -> str:
        return str(self._rpc("admin_save_announcement", {"p": item.to_payload(reshow)}))

    def end(self, announcement_id: str) -> None:
        self._rpc("admin_end_announcement", {"p_id": announcement_id})
