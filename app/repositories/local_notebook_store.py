"""The Study Notebook, in a SQLite file on this machine (akeso_notebook.db).

Same shape as the bookmark and case stores: every row has an owner (the
signed-in account), soft deletes (deleted_at) and a synced flag, so a
later cloud sync can send changes, including deletions.

    subjects          the folders on the notebook home ("Cardiology")
    notebook_items    notes and case studies, one table for all kinds
    meta              schema version, and per-owner settings such as
                      which items are open in the top tab bar

Lists (tags), the case ids and the workspace layout are stored as JSON
text columns: SQLite has no array type, and these are always read and
written whole, never searched with SQL.

Interaction case studies used to live in akeso_cases.db. The first time an
owner opens the app after this update, import_legacy_cases() copies them
in once; the old file is left untouched.
"""

import json
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Iterator, Optional

from app.models.case_study import now_iso
from app.models.notebook import (
    INTERACTION_CASE,
    ITEM_KINDS,
    NotebookItem,
    Subject,
    WorkspaceState,
)
from app.repositories.local_disease_cache import default_cache_path

SCHEMA_VERSION = 1

_ITEM_COLUMNS = ("id, kind, title, subject_id, tags, body, case_data, workspace, pinned, "
                 "created_at, updated_at, opened_at")


def default_notebook_path() -> Path:
    return default_cache_path().with_name("akeso_notebook.db")


class LocalNotebookStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_notebook_path()
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
        kinds = ", ".join(f"'{k}'" for k in ITEM_KINDS)
        with self._connect() as db:
            db.executescript(f"""
                CREATE TABLE IF NOT EXISTS meta (
                    key   TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS subjects (
                    id          TEXT PRIMARY KEY,
                    owner       TEXT NOT NULL,
                    name        TEXT NOT NULL CHECK (length(trim(name)) > 0),
                    created_at  TEXT NOT NULL,
                    updated_at  TEXT NOT NULL,
                    deleted_at  TEXT,
                    synced      INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS notebook_items (
                    id          TEXT PRIMARY KEY,
                    owner       TEXT NOT NULL,
                    kind        TEXT NOT NULL CHECK (kind IN ({kinds})),
                    title       TEXT NOT NULL CHECK (length(trim(title)) > 0),
                    subject_id  TEXT NOT NULL DEFAULT '',
                    tags        TEXT NOT NULL DEFAULT '[]',
                    body        TEXT NOT NULL DEFAULT '',
                    case_data   TEXT NOT NULL DEFAULT '{{}}',
                    workspace   TEXT NOT NULL DEFAULT '',
                    pinned      INTEGER NOT NULL DEFAULT 0,
                    created_at  TEXT NOT NULL,
                    updated_at  TEXT NOT NULL,
                    opened_at   TEXT NOT NULL DEFAULT '',
                    deleted_at  TEXT,
                    synced      INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS notebook_items_owner_idx
                    ON notebook_items (owner, deleted_at, updated_at DESC);
                CREATE INDEX IF NOT EXISTS subjects_owner_idx
                    ON subjects (owner, deleted_at);
            """)
            self._set_meta(db, "schema_version", str(SCHEMA_VERSION))

    # --------------------------------------------------------------- meta

    @staticmethod
    def _set_meta(db: sqlite3.Connection, key: str, value: str) -> None:
        db.execute("INSERT INTO meta (key, value) VALUES (?, ?) "
                   "ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, value))

    def get_setting(self, owner: str, key: str, default=None):
        with self._connect() as db:
            row = db.execute("SELECT value FROM meta WHERE key = ?",
                             (f"{key}:{owner}",)).fetchone()
        return json.loads(row[0]) if row else default

    def set_setting(self, owner: str, key: str, value) -> None:
        with self._connect() as db:
            self._set_meta(db, f"{key}:{owner}", json.dumps(value))

    # ------------------------------------------------------------ subjects

    def list_subjects(self, owner: str) -> list[Subject]:
        with self._connect() as db:
            rows = db.execute("SELECT id, name, created_at FROM subjects "
                              "WHERE owner = ? AND deleted_at IS NULL "
                              "ORDER BY name COLLATE NOCASE", (owner,)).fetchall()
        return [Subject(id=r[0], name=r[1], created_at=r[2]) for r in rows]

    def add_subject(self, owner: str, subject: Subject) -> None:
        stamp = now_iso()
        with self._connect() as db:
            db.execute("INSERT INTO subjects (id, owner, name, created_at, updated_at) "
                       "VALUES (?, ?, ?, ?, ?)",
                       (subject.id, owner, subject.name, subject.created_at or stamp, stamp))

    def rename_subject(self, owner: str, subject_id: str, name: str) -> None:
        with self._connect() as db:
            db.execute("UPDATE subjects SET name = ?, updated_at = ?, synced = 0 "
                       "WHERE id = ? AND owner = ?", (name, now_iso(), subject_id, owner))

    def delete_subject(self, owner: str, subject_id: str) -> None:
        """Soft-delete the subject. Its items stay, with no subject."""
        stamp = now_iso()
        with self._connect() as db:
            db.execute("BEGIN")
            db.execute("UPDATE subjects SET deleted_at = ?, synced = 0 "
                       "WHERE id = ? AND owner = ?", (stamp, subject_id, owner))
            db.execute("UPDATE notebook_items SET subject_id = '', synced = 0 "
                       "WHERE subject_id = ? AND owner = ?", (subject_id, owner))
            db.execute("COMMIT")

    # --------------------------------------------------------------- items

    def list_items(self, owner: str) -> list[NotebookItem]:
        with self._connect() as db:
            rows = db.execute(f"SELECT {_ITEM_COLUMNS} FROM notebook_items "
                              "WHERE owner = ? AND deleted_at IS NULL "
                              "ORDER BY updated_at DESC, rowid DESC", (owner,)).fetchall()
        return [self._item(r) for r in rows]

    def get_item(self, owner: str, item_id: str) -> Optional[NotebookItem]:
        with self._connect() as db:
            row = db.execute(f"SELECT {_ITEM_COLUMNS} FROM notebook_items "
                             "WHERE owner = ? AND id = ? AND deleted_at IS NULL",
                             (owner, item_id)).fetchone()
        return self._item(row) if row else None

    @staticmethod
    def _item(r) -> NotebookItem:
        workspace = None
        if r[7]:
            try:
                workspace = WorkspaceState.from_dict(json.loads(r[7]))
            except (ValueError, TypeError, KeyError):
                workspace = None        # a damaged layout falls back to the default
        return NotebookItem(id=r[0], kind=r[1], title=r[2], subject_id=r[3],
                            tags=json.loads(r[4]), body=r[5], case=json.loads(r[6]),
                            workspace=workspace, pinned=bool(r[8]), created_at=r[9],
                            updated_at=r[10], opened_at=r[11])

    def save_item(self, owner: str, item: NotebookItem, touch: bool = True) -> None:
        """Insert or update the whole item. touch=False keeps updated_at,
        for changes that are not edits (pinning, opening)."""
        stamp = now_iso()
        if touch or not item.updated_at:
            item.updated_at = stamp
        item.created_at = item.created_at or stamp
        workspace = json.dumps(item.workspace.to_dict()) if item.workspace else ""
        with self._connect() as db:
            db.execute(
                f"INSERT INTO notebook_items ({_ITEM_COLUMNS}, owner) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET kind = excluded.kind, title = excluded.title, "
                "subject_id = excluded.subject_id, tags = excluded.tags, body = excluded.body, "
                "case_data = excluded.case_data, workspace = excluded.workspace, "
                "pinned = excluded.pinned, updated_at = excluded.updated_at, "
                "opened_at = excluded.opened_at, synced = 0 "
                "WHERE notebook_items.owner = excluded.owner",
                (item.id, item.kind, item.title, item.subject_id, json.dumps(item.tags),
                 item.body, json.dumps(item.case), workspace, int(item.pinned),
                 item.created_at, item.updated_at, item.opened_at, owner))

    def save_workspace(self, owner: str, item_id: str, workspace: WorkspaceState) -> None:
        """Only the layout. Moving tabs around is not an edit, so
        updated_at stays as it is."""
        with self._connect() as db:
            db.execute("UPDATE notebook_items SET workspace = ?, synced = 0 "
                       "WHERE id = ? AND owner = ?",
                       (json.dumps(workspace.to_dict()), item_id, owner))

    def delete_item(self, owner: str, item_id: str) -> None:
        with self._connect() as db:
            db.execute("UPDATE notebook_items SET deleted_at = ?, synced = 0 "
                       "WHERE id = ? AND owner = ?", (now_iso(), item_id, owner))

    # --------------------------------------------------------- legacy data

    def import_legacy_cases(self, owner: str, legacy_path: Path) -> int:
        """Copy this owner's case studies from akeso_cases.db, once.
        Returns how many were imported."""
        flag = "legacy_cases_imported"
        if self.get_setting(owner, flag, False) or not legacy_path.exists():
            self.set_setting(owner, flag, True)
            return 0
        try:
            with closing(sqlite3.connect(legacy_path)) as old:
                rows = old.execute(
                    "SELECT id, title, candidate_id, regimen_ids, condition_ids, tags, "
                    "notes, created_at, updated_at FROM case_studies "
                    "WHERE owner = ? AND deleted_at IS NULL", (owner,)).fetchall()
        except sqlite3.Error:
            return 0                    # unreadable old file: try again next time
        count = 0
        for r in rows:
            if self.get_item(owner, r[0]) is not None:
                continue
            case = {"candidate_id": r[2], "regimen_ids": json.loads(r[3]),
                    "condition_ids": json.loads(r[4]), "notes": r[6]}
            item = NotebookItem(id=r[0], kind=INTERACTION_CASE, title=r[1],
                                tags=json.loads(r[5]), case=case,
                                created_at=r[7], updated_at=r[8] or r[7])
            self.save_item(owner, item, touch=False)
            count += 1
        self.set_setting(owner, flag, True)
        return count
