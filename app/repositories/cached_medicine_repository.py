"""Offline copy of the Medicine Reference.

Two classes, mirroring the disease side:

    LocalMedicineCache        the SQLite file on disk
    CachedMedicineRepository  what the service reads; syncs from Supabase

It uses its own file (akeso_medicines.db, next to akeso_cache.db) so the
disease cache's schema and wipe-on-upgrade logic stay untouched.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator, Optional

from app.models.medicine import MedicineMonograph, medicine_from_json, medicine_to_json
from app.repositories.local_disease_cache import default_cache_path
from app.repositories.supabase_medicine_repository import SupabaseMedicineRepository

SCHEMA_VERSION = 1


def default_medicine_cache_path() -> Path:
    return default_cache_path().with_name("akeso_medicines.db")


class LocalMedicineCache:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_medicine_cache_path()
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
                             CREATE TABLE IF NOT EXISTS medicines (
                                                                      id   TEXT PRIMARY KEY,
                                                                      name TEXT NOT NULL,
                                                                      data TEXT NOT NULL
                             );
                             """)
            stored = self._get_meta(db, "schema_version")
            if stored is not None and int(stored) != SCHEMA_VERSION:
                db.executescript("DELETE FROM medicines; DELETE FROM meta;")
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
            return db.execute("SELECT COUNT(*) FROM medicines").fetchone()[0] == 0

    def load(self) -> list[MedicineMonograph]:
        with self._connect() as db:
            rows = db.execute("SELECT data FROM medicines ORDER BY name").fetchall()
        return [medicine_from_json(row[0]) for row in rows]

    def replace_all(self, medicines: list[MedicineMonograph], version: int) -> None:
        """All or nothing: a failed write leaves the previous copy intact."""
        with self._connect() as db:
            db.execute("BEGIN")
            try:
                db.execute("DELETE FROM medicines")
                db.executemany(
                    "INSERT INTO medicines (id, name, data) VALUES (?, ?, ?)",
                    [(s.id, s.name, medicine_to_json(s)) for s in medicines],
                )
                self._set_meta(db, "content_version", str(version))
                db.execute("COMMIT")
            except Exception:
                db.execute("ROLLBACK")
                raise


class CachedMedicineRepository:
    """Reads the local copy; sync() refreshes it from Supabase."""

    def __init__(
            self,
            cache: Optional[LocalMedicineCache] = None,
            remote_factory: Callable[[], SupabaseMedicineRepository] = SupabaseMedicineRepository,
    ) -> None:
        self._cache = cache or LocalMedicineCache()
        # A factory, not an instance: the network client is only created on
        # the background thread when a sync actually runs.
        self._remote_factory = remote_factory
        self._medicines: list[MedicineMonograph] = []
        self._loaded = False

    def all(self) -> list[MedicineMonograph]:
        if not self._loaded:
            self.reload()
        return list(self._medicines)

    def reload(self) -> None:
        """UI thread only: re-read the local copy into memory."""
        self._medicines = self._cache.load()
        self._loaded = True

    def has_local_copy(self) -> bool:
        return not self._cache.is_empty()

    def sync(self, force: bool = False) -> bool:
        """Background thread: write a newer copy to disk if there is one.

        Never touches self._medicines; the controller calls reload() on the
        UI thread afterwards. Raises MedicineRepositoryError when offline.
        """
        remote = self._remote_factory()
        remote_version = remote.content_version()
        if not force and remote_version == self._cache.version() and not self._cache.is_empty():
            return False
        self._cache.replace_all(remote.fetch_all(), remote_version)
        return True