"""Admin Control Panel, in Supabase.

Every call is one of the admin_* database functions from migration 004.
They check that the caller is an admin themselves, so this class is only
a thin, typed wrapper; it never decides who may do what.
"""

from typing import Optional

from app.core.supabase_session import SessionClient
from app.repositories.account_errors import AccountError, friendly


class AdminRepository:
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
                raise AccountError("The Admin Control Panel isn't installed yet. Run "
                                   "database/migrations/004_admin.sql.") from exc
            raise AccountError(friendly(exc)) from exc

    # ------------------------------------------------------------ accounts

    def users(self) -> list[dict]:
        return self._rpc("admin_users") or []

    def user_detail(self, user_id: str) -> dict:
        return self._rpc("admin_user_detail", {"p_user": user_id})

    def set_role(self, user_id: str, role: str) -> None:
        self._rpc("admin_set_role", {"p_user": user_id, "p_role": role})

    def set_suspended(self, user_id: str, suspend: bool, reason: str) -> None:
        self._rpc("admin_set_suspended",
                  {"p_user": user_id, "p_suspend": suspend, "p_reason": reason})

    def delete_user(self, user_id: str, confirm: str) -> str:
        return self._rpc("admin_delete_user", {"p_user": user_id, "p_confirm": confirm})

    # ------------------------------------------------------------- content

    def body_systems(self) -> list[dict]:
        return self._rpc("admin_body_systems") or []

    def list_content(self, kind: str) -> list[dict]:
        return self._rpc(f"admin_list_{kind}s") or []

    def get_content(self, kind: str, entry_id: str) -> dict:
        return self._rpc(f"admin_get_{kind}", {"p_id": entry_id})

    def save_content(self, kind: str, data: dict, is_new: bool) -> str:
        return self._rpc(f"admin_save_{kind}", {"p": data, "p_new": is_new})

    def set_published(self, kind: str, entry_id: str, published: bool) -> None:
        self._rpc("admin_set_published",
                  {"p_kind": kind, "p_id": entry_id, "p_published": published})

    def audit(self, limit: int = 200, before: Optional[int] = None) -> dict:
        return self._rpc("admin_audit", {"p_limit": limit, "p_before": before}) or {}
