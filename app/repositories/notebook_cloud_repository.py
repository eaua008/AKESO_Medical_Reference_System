"""The account's Study Notebook in Supabase (migration 011).

Plain table access: row-level security limits every query to the signed-in
person's own rows, and a database trigger stamps the owner and the server
time, so nothing here passes a user id for rows. Pictures pasted into notes
live in the private "notebook-images" bucket at <user id>/<file name>.
"""

from typing import Optional

from app.core.supabase_session import SessionClient
from app.repositories.account_errors import AccountError, friendly

IMAGE_BUCKET = "notebook-images"
PAGE = 500

SUBJECT_COLUMNS = "id, name, created_at, updated_at, deleted_at, server_updated_at"
ITEM_COLUMNS = ("id, kind, title, subject_id, tags, body, case_data, workspace, pinned, "
                "created_at, updated_at, deleted_at, server_updated_at")


class NotebookNotInstalled(AccountError):
    """Migration 011 has not been run on this Supabase project yet."""


class NotebookCloudRepository:
    def __init__(self, session: SessionClient) -> None:
        self._s = session

    def _do(self, call):
        try:
            return self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            text = (getattr(exc, "message", None) or str(exc)).lower()
            if "notebook_items" in text or "notebook_subjects" in text or "schema cache" in text:
                raise NotebookNotInstalled(
                    "Notebook sync isn't installed yet. Run "
                    "database/migrations/011_notebook_sync.sql.") from exc
            raise AccountError(friendly(exc)) from exc

    # ------------------------------------------------------------ reading

    def _changed_since(self, table: str, columns: str, since: Optional[str]) -> list[dict]:
        rows: list[dict] = []
        start = 0
        while True:
            def call(start=start):
                query = self._s.table(table).select(columns)
                if since:
                    query = query.gt("server_updated_at", since)
                return (query.order("server_updated_at").order("id")
                        .range(start, start + PAGE - 1).execute().data) or []
            page = self._do(call)
            rows.extend(page)
            if len(page) < PAGE:
                return rows
            start += PAGE

    def subjects_since(self, since: Optional[str]) -> list[dict]:
        return self._changed_since("notebook_subjects", SUBJECT_COLUMNS, since)

    def items_since(self, since: Optional[str]) -> list[dict]:
        return self._changed_since("notebook_items", ITEM_COLUMNS, since)

    # ------------------------------------------------------------ writing

    def upsert(self, table: str, rows: list[dict]) -> None:
        for i in range(0, len(rows), 50):
            chunk = rows[i:i + 50]
            self._do(lambda chunk=chunk: self._s.table(table)
                     .upsert(chunk, on_conflict="owner,id").execute())

    # ----------------------------------------------------------- pictures

    def image_names(self) -> set[str]:
        def call():
            folder = self._s.user_id()
            names: set[str] = set()
            offset = 0
            while True:
                page = self._s.bucket(IMAGE_BUCKET).list(
                    folder, {"limit": 1000, "offset": offset}) or []
                names.update(entry["name"] for entry in page if entry.get("name"))
                if len(page) < 1000:
                    return names
                offset += 1000
        return self._do(call)

    def upload_image(self, name: str, data: bytes, content_type: str) -> None:
        def call():
            path = f"{self._s.user_id()}/{name}"
            self._s.bucket(IMAGE_BUCKET).upload(
                path, data, {"content-type": content_type, "upsert": "true"})
        self._do(call)

    def download_image(self, name: str) -> Optional[bytes]:
        def call():
            try:
                return self._s.bucket(IMAGE_BUCKET).download(f"{self._s.user_id()}/{name}")
            except Exception as exc:  # noqa: BLE001
                if "not found" in str(exc).lower() or "404" in str(exc):
                    return None
                raise
        return self._do(call)
