"""Offline copy of the body part descriptions.

Two classes, like the drug-safety cache:

    LocalBodyPartCache          the SQLite file on disk (akeso_body_parts.db)
    CachedBodyPartRepository    what the service reads; syncs from Supabase

The whole set is ONE row: the Explorer needs all of it at once to look a
clicked part up by FMA id, and it is small (a few hundred entries at most).
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator, Optional

from app.models.body_part import BodyPartInfo, parts_from_json, parts_to_json
from app.repositories.local_disease_cache import default_cache_path
from app.repositories.supabase_body_part_repository import SupabaseBodyPartRepository

SCHEMA_VERSION = 1


def default_body_part_cache_path() -> Path:
    return default_cache_path().with_name("akeso_body_parts.db")


class LocalBodyPartCache:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_body_part_cache_path()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        # Explicit close (Windows file locks) and autocommit, as in the other caches.
        connection = sqlite3.connect(self._path, timeout=10, isolation_level=None)
        try:
            connection.execute("PRAGMA journal_mode=WAL")
            yield connection
        finally:
            connection.close()

    def _ensure_schema(self) -> None:
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS meta ("
                       "key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            stored = self._get(db, "schema_version")
            if stored is not None and int(stored) != SCHEMA_VERSION:
                db.execute("DELETE FROM meta")
            self._set(db, "schema_version", str(SCHEMA_VERSION))

    @staticmethod
    def _get(db: sqlite3.Connection, key: str) -> Optional[str]:
        row = db.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None

    @staticmethod
    def _set(db: sqlite3.Connection, key: str, value: str) -> None:
        db.execute("INSERT INTO meta (key, value) VALUES (?, ?) "
                   "ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, value))

    def version(self) -> int:
        with self._connect() as db:
            value = self._get(db, "content_version")
        return int(value) if value else 0

    def has_copy(self) -> bool:
        with self._connect() as db:
            return self._get(db, "parts") is not None

    def load(self) -> list[BodyPartInfo]:
        with self._connect() as db:
            text = self._get(db, "parts")
        return parts_from_json(text) if text else []

    def replace(self, parts: list[BodyPartInfo], version: int) -> None:
        """Both values in one transaction: never new text with an old version."""
        with self._connect() as db:
            db.execute("BEGIN")
            try:
                self._set(db, "parts", parts_to_json(parts))
                self._set(db, "content_version", str(version))
                db.execute("COMMIT")
            except Exception:
                db.execute("ROLLBACK")
                raise


class CachedBodyPartRepository:
    """Reads the local copy; sync() refreshes it from Supabase."""

    def __init__(
            self,
            cache: Optional[LocalBodyPartCache] = None,
            remote_factory: Callable[[], SupabaseBodyPartRepository] = SupabaseBodyPartRepository,
    ) -> None:
        self._cache = cache
        # A factory, not an instance: the network client is only created on
        # the background thread when a sync actually runs.
        self._remote_factory = remote_factory

    def _local(self) -> LocalBodyPartCache:
        if self._cache is None:
            self._cache = LocalBodyPartCache()
        return self._cache

    def load(self) -> list[BodyPartInfo]:
        return self._local().load()

    def sync(self, force: bool = False) -> bool:
        """Background thread: write a newer copy to disk if there is one.

        Raises BodyPartRepositoryError when offline (or before migration 052).
        """
        remote = self._remote_factory()
        remote_version = remote.content_version()
        cache = self._local()
        if not force and remote_version == cache.version() and cache.has_copy():
            return False
        parts = [BodyPartInfo.from_row(row) for row in remote.fetch_published()]
        cache.replace(parts, remote_version)
        return True
