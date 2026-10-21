"""Body part descriptions, read from Supabase (migration 052).

Two requests: the content version, then every published row. Like the
other reference repositories, the app reads the local copy during normal
use and only the background sync calls this.

BodyPartDraftRepository is the admins' preview (migration 054): all rows,
drafts included, through the signed-in session.
"""

from typing import Optional

from supabase import Client, create_client

from app.core.config import config
from app.repositories.account_errors import AccountError, friendly
from app.repositories.supabase_disease_repository import DiseaseRepositoryError


class BodyPartRepositoryError(DiseaseRepositoryError):
    """Subclass, so SyncWorker and the callers treat it like the other syncs."""


class SupabaseBodyPartRepository:
    def __init__(self, client: Optional[Client] = None) -> None:
        self._client = client or create_client(config.supabase_url, config.supabase_key)

    def content_version(self) -> int:
        try:
            rows = (self._client.table("content_version")
                    .select("version").eq("id", 1).limit(1).execute().data or [])
        except Exception as exc:
            raise BodyPartRepositoryError(f"Could not check for updates: {exc}") from exc
        return int(rows[0]["version"]) if rows else 0

    def fetch_published(self) -> list[dict]:
        """Every published row. Row-level security returns only those anyway."""
        try:
            return (self._client.table("body_part_info").select("*")
                    .eq("status", "published").order("key").execute().data or [])
        except Exception as exc:
            raise BodyPartRepositoryError(f"Could not download body part descriptions: {exc}") \
                from exc


class BodyPartDraftRepository:
    """Admins only: every row, drafts included (admin_body_parts_preview)."""

    def __init__(self, session) -> None:
        self._s = session

    def all_rows(self) -> list[dict]:
        def call():
            return self._s.rpc("admin_body_parts_preview", {}).execute().data
        try:
            return self._s.run(call) or []
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise AccountError(friendly(exc)) from exc
