"""Offline copy of the drug-safety reference.

Two classes, mirroring the medicine side:

    LocalSafetyCache          the SQLite file on disk (akeso_safety.db)
    CachedSafetyRepository    what the service reads; syncs from Supabase

Why the whole bundle is ONE row: the safety check always needs all of it at
once (every condition, pair and rule), and the data is small. One JSON
document means one read, and replacing it is naturally all-or-nothing.
The medicine cache stores one row per medicine because the monograph page
opens medicines one at a time; here nothing is ever read piecemeal.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator, Optional

from app.models.drug_safety import SafetyReference, reference_from_json, reference_to_json
from app.repositories.local_disease_cache import default_cache_path
from app.repositories.supabase_safety_repository import SupabaseSafetyRepository

SCHEMA_VERSION = 1


def default_safety_cache_path() -> Path:
    return default_cache_path().with_name("akeso_safety.db")


class LocalSafetyCache:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_safety_cache_path()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        # Explicit close (Windows file locks) and autocommit, as in the
        # other caches.
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
        """True once any download has succeeded, even an empty one.

        Different from "has data": after you wipe Supabase, an empty
        reference is still a valid, current copy.
        """
        with self._connect() as db:
            return self._get(db, "reference") is not None

    def load(self) -> SafetyReference:
        with self._connect() as db:
            text = self._get(db, "reference")
        return reference_from_json(text) if text else SafetyReference()

    def replace(self, reference: SafetyReference, version: int) -> None:
        """Both values in one transaction: never a new bundle with an old version."""
        with self._connect() as db:
            db.execute("BEGIN")
            try:
                self._set(db, "reference", reference_to_json(reference))
                self._set(db, "content_version", str(version))
                db.execute("COMMIT")
            except Exception:
                db.execute("ROLLBACK")
                raise


class CachedSafetyRepository:
    """Reads the local copy; sync() refreshes it from Supabase."""

    def __init__(
            self,
            cache: Optional[LocalSafetyCache] = None,
            remote_factory: Callable[[], SupabaseSafetyRepository] = SupabaseSafetyRepository,
    ) -> None:
        self._cache = cache or LocalSafetyCache()
        # A factory, not an instance: the network client is only created on
        # the background thread when a sync actually runs.
        self._remote_factory = remote_factory
        self._reference = SafetyReference()
        self._loaded = False

    def reference(self) -> SafetyReference:
        if not self._loaded:
            self.reload()
        return self._reference

    def reload(self) -> None:
        """UI thread only: re-read the local copy into memory."""
        self._reference = self._cache.load()
        self._loaded = True

    def has_local_copy(self) -> bool:
        return self._cache.has_copy()

    def sync(self, force: bool = False) -> bool:
        """Background thread: write a newer copy to disk if there is one.

        Never touches self._reference; call reload() on the UI thread after.
        Raises SafetyRepositoryError when offline.
        """
        remote = self._remote_factory()
        remote_version = remote.content_version()
        if not force and remote_version == self._cache.version() and self._cache.has_copy():
            return False
        self._cache.replace(remote.fetch_all(), remote_version)
        return True
