"""Offline copy of the Symptom Encyclopedia.

Two classes, mirroring the disease side:

    LocalSymptomCache        the SQLite file on disk
    CachedSymptomRepository  what the service reads; syncs from Supabase

It uses its own file (akeso_symptoms.db, next to akeso_cache.db) so the
disease cache's schema and wipe-on-upgrade logic stay untouched.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator, Optional

from app.models.symptom import Symptom, symptom_from_json, symptom_to_json
from app.repositories.local_disease_cache import default_cache_path
from app.repositories.supabase_symptom_repository import SupabaseSymptomRepository

SCHEMA_VERSION = 1


def default_symptom_cache_path() -> Path:
    return default_cache_path().with_name("akeso_symptoms.db")


class LocalSymptomCache:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_symptom_cache_path()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        # Explicit close (Windows file locks) and autocommit, as in the
        # disease cache; replace_all opens its own transaction.
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
                             CREATE TABLE IF NOT EXISTS symptoms (
                                                                     id   TEXT PRIMARY KEY,
                                                                     name TEXT NOT NULL,
                                                                     data TEXT NOT NULL
                             );
                             """)
            stored = self._get_meta(db, "schema_version")
            if stored is not None and int(stored) != SCHEMA_VERSION:
                db.executescript("DELETE FROM symptoms; DELETE FROM meta;")
            self._set_meta(db, "schema_version", str(SCHEMA_VERSION))

    @staticmethod
    def _get_meta(db: sqlite3.Connection, key: str) -> Optional[str]:
        row = db.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None

    @staticmethod
    def _set_meta(db: sqlite3.Connection, key: str, value: str) -> None:
        db.execute(
            "INSERT INTO meta (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )

    def version(self) -> int:
        with self._connect() as db:
            value = self._get_meta(db, "content_version")
        return int(value) if value else 0

    def is_empty(self) -> bool:
        with self._connect() as db:
            return db.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0] == 0

    def load(self) -> list[Symptom]:
        with self._connect() as db:
            rows = db.execute("SELECT data FROM symptoms ORDER BY name").fetchall()
        return [symptom_from_json(row[0]) for row in rows]

    def replace_all(self, symptoms: list[Symptom], version: int) -> None:
        """All or nothing: a failed write leaves the previous copy intact."""
        with self._connect() as db:
            db.execute("BEGIN")
            try:
                db.execute("DELETE FROM symptoms")
                db.executemany(
                    "INSERT INTO symptoms (id, name, data) VALUES (?, ?, ?)",
                    [(s.id, s.name, symptom_to_json(s)) for s in symptoms],
                )
                self._set_meta(db, "content_version", str(version))
                db.execute("COMMIT")
            except Exception:
                db.execute("ROLLBACK")
                raise


class CachedSymptomRepository:
    """Reads the local copy; sync() refreshes it from Supabase."""

    def __init__(
            self,
            cache: Optional[LocalSymptomCache] = None,
            remote_factory: Callable[[], SupabaseSymptomRepository] = SupabaseSymptomRepository,
    ) -> None:
        self._cache = cache or LocalSymptomCache()
        # A factory, not an instance: the network client is only created on
        # the background thread when a sync actually runs.
        self._remote_factory = remote_factory
        self._symptoms: list[Symptom] = []
        self._loaded = False

    def all(self) -> list[Symptom]:
        if not self._loaded:
            self.reload()
        return list(self._symptoms)

    def reload(self) -> None:
        """UI thread only: re-read the local copy into memory."""
        self._symptoms = self._cache.load()
        self._loaded = True

    def has_local_copy(self) -> bool:
        return not self._cache.is_empty()

    def sync(self, force: bool = False) -> bool:
        """Background thread: write a newer copy to disk if there is one.

        Never touches self._symptoms; the controller calls reload() on the
        UI thread afterwards. Raises SymptomRepositoryError when offline.
        """
        remote = self._remote_factory()
        remote_version = remote.content_version()
        if not force and remote_version == self._cache.version() and not self._cache.is_empty():
            return False
        self._cache.replace_all(remote.fetch_all(), remote_version)
        return True