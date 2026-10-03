"""Where the patient's medication data lives for now: a SQLite file.

Same shape as the bookmark store, and for the same reason:

    owner        every row belongs to one account, so two people signing in
                 on one PC never see each other's courses
    deleted_at   soft delete, so the future cloud sync can send removals too
    synced       0 until pushed; the encrypted vault step will read this

Plain SQLite for now, readable only on this machine. The next security step
encrypts these rows before they ever leave the PC.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

import json

from app.models.medication import (
    ACTIVE,
    CurrentMedication,
    IntakeLog,
    MedicationCourse,
    SafetyCheckLog,
    now_iso,
)
from app.repositories.local_disease_cache import default_cache_path

SCHEMA_VERSION = 3

_COURSE_COLUMNS = (
    "id", "medicine_name", "total_units", "unit_form", "dosage_schedule",
    "duration_days", "started_on", "medicine_id", "prescriber", "is_protected",
    "notes", "status", "ended_on", "abandon_reason",
)
_MED_COLUMNS = ("id", "name", "dosage", "frequency", "is_otc", "notes",
                "medicine_id", "added_at")


def default_medication_path() -> Path:
    return default_cache_path().with_name("akeso_medications.db")


class LocalMedicationStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or default_medication_path()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self._path, timeout=10, isolation_level=None)
        try:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("PRAGMA foreign_keys=ON")
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
                CREATE TABLE IF NOT EXISTS courses (
                    id              TEXT PRIMARY KEY,
                    owner           TEXT NOT NULL,
                    medicine_name   TEXT NOT NULL,
                    total_units     INTEGER NOT NULL CHECK (total_units > 0),
                    unit_form       TEXT NOT NULL,
                    dosage_schedule TEXT NOT NULL DEFAULT '',
                    duration_days   INTEGER NOT NULL CHECK (duration_days > 0),
                    started_on      TEXT NOT NULL,
                    medicine_id     TEXT NOT NULL DEFAULT '',
                    prescriber      TEXT NOT NULL DEFAULT '',
                    is_protected    INTEGER NOT NULL DEFAULT 0,
                    notes           TEXT NOT NULL DEFAULT '',
                    status          TEXT NOT NULL DEFAULT 'active',
                    ended_on        TEXT NOT NULL DEFAULT '',
                    abandon_reason  TEXT NOT NULL DEFAULT '',
                    created_at      TEXT NOT NULL,
                    updated_at      TEXT NOT NULL,
                    deleted_at      TEXT,
                    synced          INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS courses_owner_idx
                    ON courses (owner, deleted_at, started_on DESC);

                CREATE TABLE IF NOT EXISTS intake_logs (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id  TEXT NOT NULL REFERENCES courses (id) ON DELETE CASCADE,
                    taken_at   TEXT NOT NULL,
                    status     TEXT NOT NULL DEFAULT 'taken',
                    units      INTEGER NOT NULL DEFAULT 1 CHECK (units > 0),
                    note       TEXT NOT NULL DEFAULT '',
                    deleted_at TEXT,
                    synced     INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS intake_logs_course_idx
                    ON intake_logs (course_id);

                CREATE TABLE IF NOT EXISTS current_meds (
                    id          TEXT PRIMARY KEY,
                    owner       TEXT NOT NULL,
                    name        TEXT NOT NULL,
                    dosage      TEXT NOT NULL DEFAULT '',
                    frequency   TEXT NOT NULL DEFAULT 'Daily',
                    is_otc      INTEGER NOT NULL DEFAULT 0,
                    notes       TEXT NOT NULL DEFAULT '',
                    medicine_id TEXT NOT NULL DEFAULT '',
                    added_at    TEXT NOT NULL,
                    updated_at  TEXT NOT NULL,
                    deleted_at  TEXT,
                    synced      INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS current_meds_owner_idx
                    ON current_meds (owner, deleted_at);

                -- The ticked Patient Health Profile conditions. Personal
                -- health data, so it lives here with the courses, not in
                -- the public reference cache.
                CREATE TABLE IF NOT EXISTS health_profile (
                    owner        TEXT NOT NULL,
                    condition_id TEXT NOT NULL,
                    added_at     TEXT NOT NULL,
                    PRIMARY KEY (owner, condition_id)
                );

                CREATE TABLE IF NOT EXISTS safety_checks (
                    id             TEXT PRIMARY KEY,
                    owner          TEXT NOT NULL,
                    candidate_name TEXT NOT NULL,
                    candidate_id   TEXT NOT NULL DEFAULT '',
                    verdict        TEXT NOT NULL,
                    condition_ids  TEXT NOT NULL DEFAULT '[]',
                    regimen_ids    TEXT NOT NULL DEFAULT '[]',
                    created_at     TEXT NOT NULL,
                    deleted_at     TEXT,
                    synced         INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS safety_checks_owner_idx
                    ON safety_checks (owner, deleted_at, created_at DESC);
            """)
            self._upgrade(db)
            db.execute(
                "INSERT INTO meta (key, value) VALUES ('schema_version', ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (str(SCHEMA_VERSION),),
            )

    @staticmethod
    def _upgrade(db: sqlite3.Connection) -> None:
        """Bring a version-1 file up to date without losing anyone's courses.

        CREATE TABLE IF NOT EXISTS skips a table that already exists, so
        columns added later must be added here, one ALTER per missing column.
        """
        existing = {row[1] for row in db.execute("PRAGMA table_info(intake_logs)")}
        for column, ddl in (
                ("status", "TEXT NOT NULL DEFAULT 'taken'"),
                ("units", "INTEGER NOT NULL DEFAULT 1"),
                ("note", "TEXT NOT NULL DEFAULT ''"),
                ("deleted_at", "TEXT")):
            if column not in existing:
                db.execute(f"ALTER TABLE intake_logs ADD COLUMN {column} {ddl}")

    # ------------------------------------------------------------ courses

    def courses_for(self, owner: str) -> list[MedicationCourse]:
        """Newest first, each with its intake log attached."""
        cols = ", ".join(_COURSE_COLUMNS)
        with self._connect() as db:
            rows = db.execute(
                f"SELECT {cols}, created_at FROM courses WHERE owner = ? AND deleted_at IS NULL "
                "ORDER BY started_on DESC, created_at DESC", (owner,)).fetchall()
            logs = db.execute(
                "SELECT l.id, l.course_id, l.taken_at, l.status, l.units, l.note "
                "FROM intake_logs l JOIN courses c ON c.id = l.course_id "
                "WHERE c.owner = ? AND c.deleted_at IS NULL AND l.deleted_at IS NULL "
                "ORDER BY l.taken_at, l.id", (owner,)).fetchall()
        by_course: dict[str, list[IntakeLog]] = {}
        for log_id, course_id, taken_at, status, units, note in logs:
            by_course.setdefault(course_id, []).append(
                IntakeLog(course_id, taken_at, status, units, note, log_id))
        courses = []
        for row in rows:
            data = dict(zip((*_COURSE_COLUMNS, "created_at"), row))
            data["is_protected"] = bool(data["is_protected"])
            courses.append(MedicationCourse(**data, intakes=by_course.get(data["id"], [])))
        return courses

    def add_course(self, owner: str, course: MedicationCourse) -> None:
        values = [getattr(course, c) for c in _COURSE_COLUMNS]
        values[_COURSE_COLUMNS.index("is_protected")] = int(course.is_protected)
        stamp = now_iso()
        placeholders = ", ".join("?" for _ in range(len(_COURSE_COLUMNS) + 3))
        with self._connect() as db:
            db.execute(
                f"INSERT INTO courses ({', '.join(_COURSE_COLUMNS)}, owner, created_at, "
                f"updated_at) VALUES ({placeholders})", (*values, owner, stamp, stamp))

    def log_intake(self, owner: str, course_id: str, taken_at: str,
                   status: str, units: int, note: str) -> None:
        """One log entry. The owner check stops writing into someone else's course."""
        with self._connect() as db:
            if not self._owns_active(db, owner, course_id):
                return
            db.execute("INSERT INTO intake_logs (course_id, taken_at, status, units, note) "
                       "VALUES (?, ?, ?, ?, ?)", (course_id, taken_at, status, units, note))
            db.execute("UPDATE courses SET updated_at = ?, synced = 0 WHERE id = ?",
                       (now_iso(), course_id))

    def delete_intake(self, owner: str, course_id: str, log_id: int) -> None:
        """Soft delete one entry, only if it belongs to this owner's course."""
        with self._connect() as db:
            db.execute(
                "UPDATE intake_logs SET deleted_at = ?, synced = 0 WHERE id = ? "
                "AND course_id = (SELECT id FROM courses WHERE id = ? AND owner = ?)",
                (now_iso(), log_id, course_id, owner))

    def update_course(self, owner: str, course_id: str, values: dict) -> None:
        """Edit the regimen fields. Progress and status are never touched here."""
        editable = ("medicine_name", "medicine_id", "total_units", "unit_form",
                    "dosage_schedule", "duration_days", "prescriber", "is_protected", "notes")
        fields = {k: (int(v) if k == "is_protected" else v)
                  for k, v in values.items() if k in editable}
        if not fields:
            return
        assignments = ", ".join(f"{k} = ?" for k in fields)
        with self._connect() as db:
            db.execute(f"UPDATE courses SET {assignments}, updated_at = ?, synced = 0 "
                       "WHERE id = ? AND owner = ?",
                       (*fields.values(), now_iso(), course_id, owner))

    @staticmethod
    def _owns_active(db: sqlite3.Connection, owner: str, course_id: str) -> bool:
        return db.execute(
            "SELECT 1 FROM courses WHERE id = ? AND owner = ? AND deleted_at IS NULL "
            "AND status = ?", (course_id, owner, ACTIVE)).fetchone() is not None

    def set_status(self, owner: str, course_id: str, status: str,
                   ended_on: str, reason: str = "") -> None:
        with self._connect() as db:
            db.execute(
                "UPDATE courses SET status = ?, ended_on = ?, abandon_reason = ?, "
                "updated_at = ?, synced = 0 WHERE id = ? AND owner = ?",
                (status, ended_on, reason, now_iso(), course_id, owner))

    def delete_course(self, owner: str, course_id: str) -> None:
        with self._connect() as db:
            db.execute("UPDATE courses SET deleted_at = ?, synced = 0 "
                       "WHERE id = ? AND owner = ?", (now_iso(), course_id, owner))

    # ------------------------------------------------------- current meds

    def current_meds_for(self, owner: str) -> list[CurrentMedication]:
        cols = ", ".join(_MED_COLUMNS)
        with self._connect() as db:
            rows = db.execute(
                f"SELECT {cols} FROM current_meds WHERE owner = ? AND deleted_at IS NULL "
                "ORDER BY added_at", (owner,)).fetchall()
        meds = []
        for row in rows:
            data = dict(zip(_MED_COLUMNS, row))
            data["is_otc"] = bool(data["is_otc"])
            meds.append(CurrentMedication(**data))
        return meds

    def add_current_med(self, owner: str, med: CurrentMedication) -> None:
        values = [getattr(med, c) for c in _MED_COLUMNS]
        values[_MED_COLUMNS.index("is_otc")] = int(med.is_otc)
        placeholders = ", ".join("?" for _ in range(len(_MED_COLUMNS) + 2))
        with self._connect() as db:
            db.execute(
                f"INSERT INTO current_meds ({', '.join(_MED_COLUMNS)}, owner, updated_at) "
                f"VALUES ({placeholders})", (*values, owner, now_iso()))

    def remove_current_med(self, owner: str, med_id: str) -> None:
        with self._connect() as db:
            db.execute("UPDATE current_meds SET deleted_at = ?, synced = 0 "
                       "WHERE id = ? AND owner = ?", (now_iso(), med_id, owner))

    # ----------------------------------------------------- health profile

    def health_profile(self, owner: str) -> set[str]:
        with self._connect() as db:
            rows = db.execute("SELECT condition_id FROM health_profile WHERE owner = ?",
                              (owner,)).fetchall()
        return {row[0] for row in rows}

    def set_condition(self, owner: str, condition_id: str, on: bool) -> None:
        with self._connect() as db:
            if on:
                db.execute("INSERT OR IGNORE INTO health_profile (owner, condition_id, "
                           "added_at) VALUES (?, ?, ?)", (owner, condition_id, now_iso()))
            else:
                db.execute("DELETE FROM health_profile WHERE owner = ? AND condition_id = ?",
                           (owner, condition_id))

    # ------------------------------------------------------ safety checks

    def safety_checks(self, owner: str) -> list[SafetyCheckLog]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT id, candidate_name, candidate_id, verdict, condition_ids, "
                "regimen_ids, created_at FROM safety_checks WHERE owner = ? AND "
                "deleted_at IS NULL ORDER BY created_at DESC", (owner,)).fetchall()
        return [SafetyCheckLog(r[0], r[1], r[2], r[3], json.loads(r[4]), json.loads(r[5]),
                               r[6]) for r in rows]

    def add_safety_check(self, owner: str, log: SafetyCheckLog) -> None:
        with self._connect() as db:
            db.execute(
                "INSERT INTO safety_checks (id, owner, candidate_name, candidate_id, verdict, "
                "condition_ids, regimen_ids, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (log.id, owner, log.candidate_name, log.candidate_id, log.verdict,
                 json.dumps(log.condition_ids), json.dumps(log.regimen_ids), log.created_at))

    def clear_safety_checks(self, owner: str) -> None:
        with self._connect() as db:
            db.execute("UPDATE safety_checks SET deleted_at = ?, synced = 0 "
                       "WHERE owner = ? AND deleted_at IS NULL", (now_iso(), owner))
