"""Where bookmarks live: a SQLite file on this machine.

Local-first, like the reference caches, so starring works instantly and
offline. The schema is already shaped for a later cloud sync:

    deleted_at   soft delete, so an unstar can be sent to the server too.
                 A hard delete would be invisible to the other device.
    synced       0 until the row has been pushed. pending() returns exactly
                 the rows a sync would need to send.

Until that sync exists nothing reads those two columns except pending(),
which is the point: adding sync later changes this file, not the ones above.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from app.models.bookmark import Bookmark, now_iso
from app.repositories.local_disease_cache import default_cache_path

SCHEMA_VERSION = 1


def default_bookmark_path() -> Path:
    return default_cache_path().with_name("akeso_bookmarks.db")


class LocalBookmarkStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_bookmark_path()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self._path, timeout=10, isolation_level=None)
        try:
            connection.execute("PRAGMA journal_mode=WAL")
            yield connection
        finally:
            connection.close()

    def _ensure_schema(self) -> None:
        with self._connect() as db:
            db.executescript("""
                             CREATE TABLE IF NOT EXISTS meta (
                                                                 key   TEXT PRIMARY KEY,
                                                                 value TEXT NOT NULL
                             );
                             CREATE TABLE IF NOT EXISTS bookmarks (
                                                                      owner       TEXT NOT NULL,
                                                                      entity_type TEXT NOT NULL,
                                                                      entity_id   TEXT NOT NULL,
                                                                      created_at  TEXT NOT NULL,
                                                                      deleted_at  TEXT,
                                                                      synced      INTEGER NOT NULL DEFAULT 0,
                                                                      PRIMARY KEY (owner, entity_type, entity_id)
                                 );
                             CREATE INDEX IF NOT EXISTS bookmarks_owner_idx
                                 ON bookmarks (owner, deleted_at, created_at DESC);
                             """)
            db.execute(
                "INSERT INTO meta (key, value) VALUES ('schema_version', ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (str(SCHEMA_VERSION),),
            )

    # ------------------------------------------------------------- reads

    def list_for(self, owner: str) -> list[Bookmark]:
        """Newest first. Soft-deleted rows are skipped."""
        with self._connect() as db:
            rows = db.execute(
                "SELECT owner, entity_type, entity_id, created_at FROM bookmarks "
                "WHERE owner = ? AND deleted_at IS NULL ORDER BY created_at DESC",
                (owner,),
            ).fetchall()
        return [Bookmark(*row) for row in rows]

    def ids_for(self, owner: str, entity_type: str) -> set[str]:
        """Just the ids, for painting stars on a directory of cards."""
        with self._connect() as db:
            rows = db.execute(
                "SELECT entity_id FROM bookmarks WHERE owner = ? AND entity_type = ? "
                "AND deleted_at IS NULL",
                (owner, entity_type),
            ).fetchall()
        return {row[0] for row in rows}

    def is_bookmarked(self, owner: str, entity_type: str, entity_id: str) -> bool:
        with self._connect() as db:
            row = db.execute(
                "SELECT 1 FROM bookmarks WHERE owner = ? AND entity_type = ? "
                "AND entity_id = ? AND deleted_at IS NULL",
                (owner, entity_type, entity_id),
            ).fetchone()
        return row is not None

    # ------------------------------------------------------------ writes

    def add(self, owner: str, entity_type: str, entity_id: str) -> None:
        """Star it. Re-starting something previously unstarred revives the row."""
        with self._connect() as db:
            db.execute(
                "INSERT INTO bookmarks (owner, entity_type, entity_id, created_at, "
                "deleted_at, synced) VALUES (?, ?, ?, ?, NULL, 0) "
                "ON CONFLICT(owner, entity_type, entity_id) DO UPDATE SET "
                "created_at = excluded.created_at, deleted_at = NULL, synced = 0",
                (owner, entity_type, entity_id, now_iso()),
            )

    def remove(self, owner: str, entity_type: str, entity_id: str) -> None:
        """Unstar it: a soft delete, so a later sync can carry the removal."""
        with self._connect() as db:
            db.execute(
                "UPDATE bookmarks SET deleted_at = ?, synced = 0 "
                "WHERE owner = ? AND entity_type = ? AND entity_id = ?",
                (now_iso(), owner, entity_type, entity_id),
            )

    def toggle(self, owner: str, entity_type: str, entity_id: str) -> bool:
        """Flip the star; returns the new state."""
        if self.is_bookmarked(owner, entity_type, entity_id):
            self.remove(owner, entity_type, entity_id)
            return False
        self.add(owner, entity_type, entity_id)
        return True

    # -------------------------------------------------- for a future sync

    def pending(self, owner: str) -> list[tuple]:
        """Rows not yet pushed, additions and removals alike."""
        with self._connect() as db:
            return db.execute(
                "SELECT owner, entity_type, entity_id, created_at, deleted_at "
                "FROM bookmarks WHERE owner = ? AND synced = 0",
                (owner,),
            ).fetchall()

    def mark_synced(self, owner: str, entity_type: str, entity_id: str) -> None:
        with self._connect() as db:
            db.execute(
                "UPDATE bookmarks SET synced = 1 WHERE owner = ? AND entity_type = ? "
                "AND entity_id = ?",
                (owner, entity_type, entity_id),
            )