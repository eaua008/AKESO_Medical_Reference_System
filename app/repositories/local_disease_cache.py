"""The local copy of the encyclopedia, in SQLite.

Why denormalized, when the Supabase schema is fully normalized:

Normalization protects a SOURCE OF TRUTH from update anomalies — two copies
of one fact drifting apart when only one gets edited. This cache is never
edited. It is replaced wholesale from Supabase, so there is nothing to drift.
What it needs is fast reads, and storing each condition as one JSON document
means opening a monograph is a single row lookup rather than a fourteen-table
join. Normalized source of truth, denormalized read cache.

Why no encryption: everything here is public reference data, readable by
anyone through the public-read row-level security policies. Encrypting it
would protect nothing. The rule that matters is the converse — no session
tokens, credentials or personal data ever go in this file.

Threading: every method opens its own short-lived connection. sqlite3
connections cannot be shared across threads, and the background sync writes
while the UI reads. WAL mode lets those happen at the same time — a reader
mid-sync sees the previous complete copy, never a half-written one.
"""

import json
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Iterator, Optional

from app.models.disease import (
    BodySystem,
    ClinicalReference,
    Differential,
    Disease,
    Medicine,
    SymptomLink,
)

SCHEMA_VERSION = 1


def default_cache_path() -> Path:
    """%LOCALAPPDATA%\\Akeso\\akeso_cache.db on Windows.

    LOCALAPPDATA rather than the project folder: the cache belongs to this
    machine and user, is rebuilt from Supabase whenever needed, and must
    never be committed to git alongside the code.
    """
    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / ".local" / "share")
    return Path(base) / "Akeso" / "akeso_cache.db"


# ------------------------------------------------------------ serialisation

def disease_to_json(disease: Disease) -> str:
    return json.dumps(asdict(disease), ensure_ascii=False)


def disease_from_json(text: str) -> Disease:
    """Rebuild a Disease, including every nested dataclass.

    asdict() flattens nested dataclasses into plain dicts. Those have to be
    turned back into SymptomLink, Medicine and so on, or code expecting
    `link.is_primary` would get a dict and fail.
    """
    data = json.loads(text)
    data["symptoms"] = [SymptomLink(**s) for s in data.get("symptoms", [])]
    data["differential_diagnosis"] = [
        Differential(**d) for d in data.get("differential_diagnosis", [])
    ]
    data["clinical_references"] = [
        ClinicalReference(**r) for r in data.get("clinical_references", [])
    ]
    data["medicines"] = [Medicine(**m) for m in data.get("medicines", [])]

    # Tolerate cache files written by an older model: drop keys the current
    # Disease no longer has instead of crashing on an unexpected argument.
    known = set(Disease.__dataclass_fields__)
    return Disease(**{k: v for k, v in data.items() if k in known})


# -------------------------------------------------------------------- store

class LocalDiseaseCache:
    """Reads and writes the local SQLite copy."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_cache_path()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    @property
    def path(self) -> Path:
        return self._path

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        """A connection that is always closed.

        `with sqlite3.connect(...) as db` commits on exit but does NOT close
        the connection. On Windows a leaked handle can hold the file locked,
        so closing is explicit here.

        isolation_level=None puts sqlite3 in autocommit mode, so transactions
        happen only where replace_all opens one with BEGIN. That keeps the
        all-or-nothing swap explicit instead of relying on implicit
        transaction rules.
        """
        connection = sqlite3.connect(self._path, timeout=10, isolation_level=None)
        try:
            connection.execute("PRAGMA journal_mode=WAL")
            yield connection
        finally:
            connection.close()

    def _ensure_schema(self) -> None:
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS meta (
                                                    key   TEXT PRIMARY KEY,
                                                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS body_systems (
                                                            id   TEXT PRIMARY KEY,
                                                            data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS diseases (
                                                        id   TEXT PRIMARY KEY,
                                                        name TEXT NOT NULL,
                                                        data TEXT NOT NULL
                );
                """
            )
            stored = self._get_meta(db, "schema_version")
            if stored is not None and int(stored) != SCHEMA_VERSION:
                # The cache layout changed between app versions. Rather than
                # migrate a disposable copy, empty it and let sync refill it.
                db.executescript(
                    "DELETE FROM diseases; DELETE FROM body_systems; DELETE FROM meta;"
                )
            self._set_meta(db, "schema_version", str(SCHEMA_VERSION))

    # ------------------------------------------------------------- meta

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
        """Content version the local copy was made from. 0 means empty."""
        with self._connect() as db:
            value = self._get_meta(db, "content_version")
        return int(value) if value else 0

    def stats(self) -> Optional[dict[str, int]]:
        with self._connect() as db:
            value = self._get_meta(db, "stats")
        return json.loads(value) if value else None

    # ------------------------------------------------------------ reads

    def load_diseases(self) -> list[Disease]:
        with self._connect() as db:
            rows = db.execute("SELECT data FROM diseases ORDER BY name").fetchall()
        return [disease_from_json(row[0]) for row in rows]

    def load_body_systems(self) -> list[BodySystem]:
        with self._connect() as db:
            rows = db.execute("SELECT data FROM body_systems").fetchall()
        return [BodySystem(**json.loads(row[0])) for row in rows]

    def is_empty(self) -> bool:
        with self._connect() as db:
            row = db.execute("SELECT COUNT(*) FROM diseases").fetchone()
        return row[0] == 0

    # ----------------------------------------------------------- writes

    def replace_all(
            self,
            diseases: list[Disease],
            body_systems: list[BodySystem],
            version: int,
            stats: dict[str, int],
    ) -> None:
        """Swap the entire local copy in one transaction.

        All or nothing. If anything fails partway, the transaction rolls
        back and the previous complete copy stays in place — the app never
        ends up reading half an encyclopedia.
        """
        with self._connect() as db:
            db.execute("BEGIN")
            try:
                db.execute("DELETE FROM diseases")
                db.execute("DELETE FROM body_systems")
                db.executemany(
                    "INSERT INTO diseases (id, name, data) VALUES (?, ?, ?)",
                    [(d.id, d.name, disease_to_json(d)) for d in diseases],
                )
                db.executemany(
                    "INSERT INTO body_systems (id, data) VALUES (?, ?)",
                    [(s.id, json.dumps(asdict(s))) for s in body_systems],
                )
                self._set_meta(db, "content_version", str(version))
                self._set_meta(db, "stats", json.dumps(stats))
                db.execute("COMMIT")
            except Exception:
                db.execute("ROLLBACK")
                raise

    def clear(self) -> None:
        """Delete the local copy. The next sync downloads everything again."""
        with self._connect() as db:
            db.executescript(
                "DELETE FROM diseases; DELETE FROM body_systems; "
                "DELETE FROM meta WHERE key != 'schema_version';"
            )