"""Saved case studies, in a SQLite file on this machine (akeso_cases.db).

Same shape as the bookmark store: every row has an owner (the signed-in
account), soft deletes, and a synced flag so a later cloud sync can send
changes, including deletions.

No encryption: cases hold hypothetical scenarios made of reference ids,
not anyone's health data. The Save dialog tells users not to enter real
patient names.
"""

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from app.models.case_study import CaseStudy, now_iso
from app.repositories.local_disease_cache import default_cache_path

SCHEMA_VERSION = 1


def default_case_path() -> Path:
    return default_cache_path().with_name("akeso_cases.db")


class LocalCaseStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_case_path()
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
                CREATE TABLE IF NOT EXISTS case_studies (
                    id            TEXT PRIMARY KEY,
                    owner         TEXT NOT NULL,
                    title         TEXT NOT NULL CHECK (length(trim(title)) > 0),
                    candidate_id  TEXT NOT NULL DEFAULT '',
                    regimen_ids   TEXT NOT NULL DEFAULT '[]',
                    condition_ids TEXT NOT NULL DEFAULT '[]',
                    tags          TEXT NOT NULL DEFAULT '[]',
                    notes         TEXT NOT NULL DEFAULT '',
                    created_at    TEXT NOT NULL,
                    updated_at    TEXT NOT NULL,
                    deleted_at    TEXT,
                    synced        INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS case_studies_owner_idx
                    ON case_studies (owner, deleted_at, created_at DESC);
            """)
            db.execute("INSERT INTO meta (key, value) VALUES ('schema_version', ?) "
                       "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                       (str(SCHEMA_VERSION),))

    def list_for(self, owner: str) -> list[CaseStudy]:
        """Newest first (rowid breaks ties within the same second). Deleted
        cases are skipped."""
        with self._connect() as db:
            rows = db.execute(
                "SELECT id, title, candidate_id, regimen_ids, condition_ids, tags, notes, "
                "created_at FROM case_studies WHERE owner = ? AND deleted_at IS NULL "
                "ORDER BY created_at DESC, rowid DESC", (owner,)).fetchall()
        return [CaseStudy(id=r[0], title=r[1], candidate_id=r[2],
                          regimen_ids=json.loads(r[3]), condition_ids=json.loads(r[4]),
                          tags=json.loads(r[5]), notes=r[6], created_at=r[7])
                for r in rows]

    def add(self, owner: str, case: CaseStudy) -> None:
        stamp = now_iso()
        with self._connect() as db:
            db.execute(
                "INSERT INTO case_studies (id, owner, title, candidate_id, regimen_ids, "
                "condition_ids, tags, notes, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (case.id, owner, case.title, case.candidate_id,
                 json.dumps(case.regimen_ids), json.dumps(case.condition_ids),
                 json.dumps(case.tags), case.notes, case.created_at or stamp, stamp))

    def delete(self, owner: str, case_id: str) -> None:
        with self._connect() as db:
            db.execute("UPDATE case_studies SET deleted_at = ?, synced = 0 "
                       "WHERE id = ? AND owner = ?", (now_iso(), case_id, owner))
