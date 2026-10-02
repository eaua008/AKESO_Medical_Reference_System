"""Where search history lives: a SQLite file on this computer.

Local only, like bookmarks. Nothing here is sent to the server. Each row has
an "owner" (the account's email), so LocalAccountData can export it, erase
it when the account is deleted, and move it after an email change, without
knowing this table.

One row per thing opened: searching for Dengue twice moves it to the top
and counts it twice, rather than filling the list with copies.

Whether history is saved at all is a per-account choice, kept in meta under
"save_history:<owner>" (so it is included in that account's data export).
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from app.models.search_history import HistoryEntry, now_iso
from app.repositories.local_disease_cache import default_cache_path

SCHEMA_VERSION = 1
MAX_ROWS = 300          # per account; the oldest are dropped past this


def default_history_path() -> Path:
    return default_cache_path().with_name("akeso_search_history.db")


class LocalHistoryStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_history_path()
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
                CREATE TABLE IF NOT EXISTS searches (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner       TEXT NOT NULL,
                    kind        TEXT NOT NULL,
                    target_id   TEXT NOT NULL,
                    title       TEXT NOT NULL,
                    subtitle    TEXT NOT NULL DEFAULT '',
                    icon        TEXT NOT NULL DEFAULT '',
                    query       TEXT NOT NULL DEFAULT '',
                    searched_at TEXT NOT NULL,
                    times       INTEGER NOT NULL DEFAULT 1,
                    UNIQUE (owner, kind, target_id)
                );
                CREATE INDEX IF NOT EXISTS searches_owner_idx
                    ON searches (owner, searched_at DESC);
            """)
            db.execute(
                "INSERT INTO meta (key, value) VALUES ('schema_version', ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (str(SCHEMA_VERSION),),
            )

    # ------------------------------------------------------------- reads

    def list_for(self, owner: str, limit: int = MAX_ROWS) -> list[HistoryEntry]:
        """Newest first."""
        with self._connect() as db:
            rows = db.execute(
                "SELECT id, kind, target_id, title, subtitle, icon, query, searched_at, "
                "times FROM searches WHERE owner = ? ORDER BY searched_at DESC, id DESC "
                "LIMIT ?", (owner, limit),
            ).fetchall()
        return [HistoryEntry(*row) for row in rows]

    def saving_enabled(self, owner: str) -> bool:
        with self._connect() as db:
            row = db.execute("SELECT value FROM meta WHERE key = ?",
                             (f"save_history:{owner}",)).fetchone()
        return row is None or row[0] != "0"

    # ------------------------------------------------------------ writes

    def add(self, owner: str, kind: str, target_id: str, title: str,
            subtitle: str = "", icon: str = "", query: str = "") -> None:
        with self._connect() as db:
            db.execute(
                "INSERT INTO searches (owner, kind, target_id, title, subtitle, icon, query, "
                "searched_at, times) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1) "
                "ON CONFLICT(owner, kind, target_id) DO UPDATE SET "
                "title = excluded.title, subtitle = excluded.subtitle, icon = excluded.icon, "
                "query = excluded.query, searched_at = excluded.searched_at, "
                "times = searches.times + 1",
                (owner, kind, target_id, title, subtitle, icon, query.strip()[:120], now_iso()),
            )
            db.execute(
                "DELETE FROM searches WHERE owner = ? AND id NOT IN ("
                "SELECT id FROM searches WHERE owner = ? "
                "ORDER BY searched_at DESC, id DESC LIMIT ?)",
                (owner, owner, MAX_ROWS),
            )

    def remove(self, owner: str, entry_id: int) -> None:
        with self._connect() as db:
            db.execute("DELETE FROM searches WHERE owner = ? AND id = ?", (owner, entry_id))

    def clear(self, owner: str) -> int:
        """Delete every entry for this account; returns how many went."""
        with self._connect() as db:
            return db.execute("DELETE FROM searches WHERE owner = ?", (owner,)).rowcount

    def set_saving(self, owner: str, on: bool) -> None:
        with self._connect() as db:
            db.execute(
                "INSERT INTO meta (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (f"save_history:{owner}", "1" if on else "0"),
            )
