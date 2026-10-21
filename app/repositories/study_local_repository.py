"""Study Hub on this computer: akeso_study.db, next to the other caches.

Reviews work fully offline from here. Every row belongs to an owner (the
signed-in account) so two accounts on one computer never mix, and rows the
server has not seen yet carry synced = 0.

    decks        own decks and the cached official ones (row JSON)
    cards        their cards (row JSON); deleted_at = soft delete
    card_states  where each card is in this person's schedule
    review_log   every rating (client_id is unique worldwide)
    settings     new cards a day etc. (JSON)
    sync_meta    "last pulled at" per table, and other small values
"""

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator, Optional

from app.models.study import (
    Card, CardState, CardStateKind, Deck, ReviewLogEntry, StudySettings,
)
from app.repositories.local_disease_cache import default_cache_path

SCHEMA_VERSION = 1


def default_study_path() -> Path:
    return default_cache_path().with_name("akeso_study.db")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_time(text) -> Optional[datetime]:
    if not text:
        return None
    if isinstance(text, datetime):
        return text if text.tzinfo else text.replace(tzinfo=timezone.utc)
    try:
        value = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    except ValueError:
        return None
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def iso(value: Optional[datetime]) -> Optional[str]:
    return value.astimezone(timezone.utc).isoformat() if value else None


def state_to_json(state: CardState, reset_at: Optional[str] = None, seen_hash: str = "") -> dict:
    return {"seen_hash": seen_hash, "state": state.state.value, "due": iso(state.due), "interval_days": state.interval_days,
            "ease": state.ease, "reps": state.reps, "lapses": state.lapses, "step": state.step,
            "last_rating": state.last_rating, "last_review": iso(state.last_review),
            "reset_at": reset_at}


def state_from_json(key: str, raw: dict) -> CardState:
    try:
        kind = CardStateKind(raw.get("state") or "new")
    except ValueError:
        kind = CardStateKind.NEW
    return CardState(card_key=key, state=kind, due=parse_time(raw.get("due")),
                     interval_days=float(raw.get("interval_days") or 0),
                     ease=float(raw.get("ease") or 2.5), reps=int(raw.get("reps") or 0),
                     lapses=int(raw.get("lapses") or 0), step=int(raw.get("step") or 0),
                     last_rating=raw.get("last_rating"), last_review=parse_time(raw.get("last_review")))


class StudyLocalRepository:
    def __init__(self, owner: str, path: Optional[Path] = None) -> None:
        self.owner = owner or "local"
        self._path = path or default_study_path()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    @property
    def path(self) -> Path:
        return self._path

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
                CREATE TABLE IF NOT EXISTS decks (
                    owner TEXT NOT NULL, id TEXT NOT NULL, row TEXT NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT '', deleted_at TEXT,
                    synced INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (owner, id));
                CREATE TABLE IF NOT EXISTS cards (
                    owner TEXT NOT NULL, id TEXT NOT NULL, deck_id TEXT NOT NULL, row TEXT NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT '', deleted_at TEXT,
                    synced INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (owner, id));
                CREATE INDEX IF NOT EXISTS cards_deck ON cards (owner, deck_id);
                CREATE TABLE IF NOT EXISTS card_states (
                    owner TEXT NOT NULL, card_key TEXT NOT NULL, row TEXT NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT '', synced INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY (owner, card_key));
                CREATE TABLE IF NOT EXISTS review_log (
                    owner TEXT NOT NULL, client_id TEXT NOT NULL, card_key TEXT NOT NULL,
                    rating INTEGER NOT NULL, reviewed_at TEXT NOT NULL, elapsed_ms INTEGER NOT NULL DEFAULT 0,
                    state_before TEXT NOT NULL DEFAULT 'new', interval_before REAL NOT NULL DEFAULT 0,
                    interval_after REAL NOT NULL DEFAULT 0, ease_after REAL NOT NULL DEFAULT 2.5,
                    synced INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (owner, client_id));
                CREATE INDEX IF NOT EXISTS review_log_card ON review_log (owner, card_key, reviewed_at);
                CREATE INDEX IF NOT EXISTS review_log_time ON review_log (owner, reviewed_at);
                CREATE TABLE IF NOT EXISTS settings (
                    owner TEXT PRIMARY KEY, row TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT '',
                    synced INTEGER NOT NULL DEFAULT 0);
                CREATE TABLE IF NOT EXISTS sync_meta (
                    owner TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL,
                    PRIMARY KEY (owner, key));
            """)
            db.execute("INSERT OR IGNORE INTO sync_meta VALUES ('*', 'schema', ?)", (str(SCHEMA_VERSION),))
            columns = {row[1] for row in db.execute("PRAGMA table_info(review_log)")}
            if "hinted" not in columns:                       # migration 051
                db.execute("ALTER TABLE review_log ADD COLUMN hinted INTEGER NOT NULL DEFAULT 0")

    # ---------------------------------------------------------------- meta

    def meta(self, key: str, default: str = "") -> str:
        with self._connect() as db:
            row = db.execute("SELECT value FROM sync_meta WHERE owner = ? AND key = ?",
                             (self.owner, key)).fetchone()
        return row[0] if row else default

    def set_meta(self, key: str, value: str) -> None:
        with self._connect() as db:
            db.execute("INSERT OR REPLACE INTO sync_meta VALUES (?, ?, ?)", (self.owner, key, value))

    # --------------------------------------------------------------- decks

    def decks(self, include_deleted: bool = False) -> list[Deck]:
        with self._connect() as db:
            rows = db.execute("SELECT row, deleted_at FROM decks WHERE owner = ?"
                              + ("" if include_deleted else " AND deleted_at IS NULL"),
                              (self.owner,)).fetchall()
        out = []
        for raw, deleted in rows:
            deck = Deck.from_row(json.loads(raw))
            deck.deleted_at = deleted
            out.append(deck)
        return out

    def deck(self, deck_id: str) -> Optional[Deck]:
        with self._connect() as db:
            row = db.execute("SELECT row FROM decks WHERE owner = ? AND id = ? AND deleted_at IS NULL",
                             (self.owner, deck_id)).fetchone()
        return Deck.from_row(json.loads(row[0])) if row else None

    def deck_row(self, deck_id: str) -> Optional[dict]:
        with self._connect() as db:
            row = db.execute("SELECT row, updated_at, deleted_at, synced FROM decks WHERE owner = ? AND id = ?",
                             (self.owner, deck_id)).fetchone()
        if not row:
            return None
        data = json.loads(row[0])
        data.update(updated_at=row[1], deleted_at=row[2], synced=bool(row[3]))
        return data

    def save_deck_row(self, row: dict, synced: bool) -> None:
        with self._connect() as db:
            db.execute("INSERT OR REPLACE INTO decks VALUES (?, ?, ?, ?, ?, ?)",
                       (self.owner, row["id"], json.dumps(row), row.get("updated_at") or now_iso(),
                        row.get("deleted_at"), int(synced)))

    def remove_deck_local(self, deck_id: str) -> None:
        """Forget a deck here only (an official deck that was unpublished)."""
        with self._connect() as db:
            db.execute("DELETE FROM cards WHERE owner = ? AND deck_id = ?", (self.owner, deck_id))
            db.execute("DELETE FROM decks WHERE owner = ? AND id = ?", (self.owner, deck_id))

    # --------------------------------------------------------------- cards

    def cards(self, deck_id: Optional[str] = None, include_deleted: bool = False) -> list[Card]:
        sql = "SELECT row, deleted_at FROM cards WHERE owner = ?"
        args: list = [self.owner]
        if deck_id is not None:
            sql += " AND deck_id = ?"
            args.append(deck_id)
        if not include_deleted:
            sql += " AND deleted_at IS NULL"
        with self._connect() as db:
            rows = db.execute(sql, args).fetchall()
        out = []
        for raw, deleted in rows:
            card = Card.from_row(json.loads(raw))
            card.deleted_at = deleted
            out.append(card)
        out.sort(key=lambda c: (c.position, c.updated_at))
        return out

    def card_row(self, card_id: str) -> Optional[dict]:
        with self._connect() as db:
            row = db.execute("SELECT row, updated_at, deleted_at, synced FROM cards WHERE owner = ? AND id = ?",
                             (self.owner, card_id)).fetchone()
        if not row:
            return None
        data = json.loads(row[0])
        data.update(updated_at=row[1], deleted_at=row[2], synced=bool(row[3]))
        return data

    def save_card_row(self, row: dict, synced: bool) -> None:
        with self._connect() as db:
            db.execute("INSERT OR REPLACE INTO cards VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (self.owner, row["id"], row["deck_id"], json.dumps(row),
                        row.get("updated_at") or now_iso(), row.get("deleted_at"), int(synced)))

    def unsynced(self, table: str) -> list[dict]:
        assert table in ("decks", "cards")
        with self._connect() as db:
            rows = db.execute(f"SELECT row, updated_at, deleted_at FROM {table} "
                              "WHERE owner = ? AND synced = 0", (self.owner,)).fetchall()
        out = []
        for raw, updated, deleted in rows:
            data = json.loads(raw)
            data.update(updated_at=updated, deleted_at=deleted)
            out.append(data)
        return out

    def mark_synced(self, table: str, ids: Iterable[str]) -> None:
        assert table in ("decks", "cards")
        ids = list(ids)
        if not ids:
            return
        with self._connect() as db:
            db.executemany(f"UPDATE {table} SET synced = 1 WHERE owner = ? AND id = ?",
                           [(self.owner, i) for i in ids])

    # -------------------------------------------------------------- states

    def states(self) -> dict[str, CardState]:
        with self._connect() as db:
            rows = db.execute("SELECT card_key, row FROM card_states WHERE owner = ?", (self.owner,)).fetchall()
        return {key: state_from_json(key, json.loads(raw)) for key, raw in rows}

    def state_row(self, key: str) -> Optional[dict]:
        with self._connect() as db:
            row = db.execute("SELECT row, updated_at, synced FROM card_states WHERE owner = ? AND card_key = ?",
                             (self.owner, key)).fetchone()
        if not row:
            return None
        data = json.loads(row[0])
        data.update(updated_at=row[1], synced=bool(row[2]))
        return data

    def save_state(self, state: CardState, synced: bool = False, reset_at: Optional[str] = None,
                   updated_at: Optional[str] = None, seen_hash: Optional[str] = None) -> None:
        old = self.state_row(state.card_key) or {}
        if reset_at is None:
            reset_at = old.get("reset_at")
        if seen_hash is None:
            seen_hash = old.get("seen_hash") or ""
        with self._connect() as db:
            db.execute("INSERT OR REPLACE INTO card_states VALUES (?, ?, ?, ?, ?)",
                       (self.owner, state.card_key, json.dumps(state_to_json(state, reset_at, seen_hash)),
                        updated_at or now_iso(), int(synced)))

    def delete_state(self, key: str) -> None:
        with self._connect() as db:
            db.execute("DELETE FROM card_states WHERE owner = ? AND card_key = ?", (self.owner, key))

    def unsynced_states(self) -> list[tuple[str, dict, str]]:
        with self._connect() as db:
            rows = db.execute("SELECT card_key, row, updated_at FROM card_states WHERE owner = ? AND synced = 0",
                              (self.owner,)).fetchall()
        return [(k, json.loads(r), u) for k, r, u in rows]

    def mark_states_synced(self, keys: Iterable[str]) -> None:
        with self._connect() as db:
            db.executemany("UPDATE card_states SET synced = 1 WHERE owner = ? AND card_key = ?",
                           [(self.owner, k) for k in keys])

    # ---------------------------------------------------------- review log

    def add_review(self, entry: ReviewLogEntry, synced: bool = False) -> bool:
        """False if this client_id is already here (a duplicate)."""
        with self._connect() as db:
            cur = db.execute(
                "INSERT OR IGNORE INTO review_log (owner, client_id, card_key, rating, reviewed_at, elapsed_ms, "
                "state_before, interval_before, interval_after, ease_after, synced, hinted) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (self.owner, entry.client_id, entry.card_key, int(entry.rating), iso(entry.reviewed_at),
                 entry.elapsed_ms, entry.state_before, entry.interval_before, entry.interval_after,
                 entry.ease_after, int(synced), int(entry.hinted)))
            return cur.rowcount > 0

    def remove_review(self, client_id: str) -> None:
        """Undo: only a review that has not been uploaded yet can be taken back."""
        with self._connect() as db:
            db.execute("DELETE FROM review_log WHERE owner = ? AND client_id = ? AND synced = 0",
                       (self.owner, client_id))

    def reviews(self, card_key: Optional[str] = None, since: Optional[datetime] = None) -> list[ReviewLogEntry]:
        sql = ("SELECT client_id, card_key, rating, reviewed_at, elapsed_ms, state_before, interval_before, "
               "interval_after, ease_after, synced, hinted FROM review_log WHERE owner = ?")
        args: list = [self.owner]
        if card_key is not None:
            sql += " AND card_key = ?"
            args.append(card_key)
        if since is not None:
            sql += " AND reviewed_at >= ?"
            args.append(iso(since))
        sql += " ORDER BY reviewed_at, client_id"
        with self._connect() as db:
            rows = db.execute(sql, args).fetchall()
        return [ReviewLogEntry(card_key=r[1], rating=r[2], reviewed_at=parse_time(r[3]), client_id=r[0],
                               elapsed_ms=r[4], state_before=r[5], interval_before=r[6],
                               interval_after=r[7], ease_after=r[8], synced=bool(r[9]),
                               hinted=bool(r[10])) for r in rows]

    def unsynced_reviews(self) -> list[ReviewLogEntry]:
        return [e for e in self.reviews() if not e.synced]

    def mark_reviews_synced(self, client_ids: Iterable[str]) -> None:
        with self._connect() as db:
            db.executemany("UPDATE review_log SET synced = 1 WHERE owner = ? AND client_id = ?",
                           [(self.owner, c) for c in client_ids])

    # ------------------------------------------------------------ settings

    def settings(self) -> StudySettings:
        with self._connect() as db:
            row = db.execute("SELECT row FROM settings WHERE owner = ?", (self.owner,)).fetchone()
        if not row:
            return StudySettings()
        raw = json.loads(row[0])
        base = StudySettings()
        return StudySettings(new_per_day=int(raw.get("new_per_day", base.new_per_day)),
                             max_reviews=int(raw.get("max_reviews", base.max_reviews)),
                             learning_steps=[int(x) for x in raw.get("learning_steps", base.learning_steps)],
                             relearn_steps=[int(x) for x in raw.get("relearn_steps", base.relearn_steps)],
                             type_answer=bool(raw.get("type_answer", False)),
                             difficulties=list(raw.get("difficulties") or []),
                             families=list(raw.get("families") or []))

    def settings_row(self) -> Optional[dict]:
        with self._connect() as db:
            row = db.execute("SELECT row, updated_at, synced FROM settings WHERE owner = ?",
                             (self.owner,)).fetchone()
        if not row:
            return None
        data = json.loads(row[0])
        data.update(updated_at=row[1], synced=bool(row[2]))
        return data

    def save_settings(self, settings: StudySettings, synced: bool = False,
                      updated_at: Optional[str] = None) -> None:
        row = {"new_per_day": settings.new_per_day, "max_reviews": settings.max_reviews,
               "learning_steps": list(settings.learning_steps), "relearn_steps": list(settings.relearn_steps),
               "type_answer": settings.type_answer, "difficulties": list(settings.difficulties),
               "families": list(settings.families)}
        with self._connect() as db:
            db.execute("INSERT OR REPLACE INTO settings VALUES (?, ?, ?, ?)",
                       (self.owner, json.dumps(row), updated_at or now_iso(), int(synced)))
