"""Study Hub in Supabase (migrations 050 and 051).

Row-level security decides what each person may read and write: published
official decks for everyone signed in, and only their own personal decks,
cards, states, history and settings. Official decks are written through the
admin_* functions, never through the tables.

Raw server text never reaches the screen: errors become AccountError with a
friendly message, or StudyNotInstalled when migration 050 is missing.
"""

from typing import Optional

from app.core.supabase_session import SessionClient
from app.repositories.account_errors import AccountError, friendly

PAGE = 500
DECK_COLUMNS = ("id, title, description, subject_id, origin, owner_id, status, visibility, "
                "updated_at, deleted_at, server_updated_at")
CARD_COLUMNS = ("id, deck_id, type, front, back, choices, cloze_text, part_ids, source_kind, "
                "source_id, tags, position, updated_at, deleted_at, server_updated_at")
TEACHING = ("answer_short", "explanation", "distinguish", "hint", "difficulty")      # migration 051
STATE_COLUMNS = ("card_key, state, due, interval_days, ease, reps, lapses, step, last_rating, "
                 "last_review, reset_at, updated_at, server_updated_at")
LOG_COLUMNS = ("client_id, card_key, rating, reviewed_at, elapsed_ms, state_before, interval_before, "
               "interval_after, ease_after, server_received_at")


class _NoColumn(Exception):
    """A column from migration 051 is missing on the server."""


class StudyNotInstalled(AccountError):
    """Migration 050 has not been run on this Supabase project yet."""


class SupabaseStudyRepository:
    def __init__(self, session: SessionClient) -> None:
        self._s = session
        self._has_051: Optional[bool] = None             # None until the server has answered

    def _teaching(self, call_new, call_old):
        """Use migration 051's columns, or 050's when the server doesn't have them yet."""
        if self._has_051 is not False:
            try:
                result = call_new()
                self._has_051 = True
                return result
            except _NoColumn:
                self._has_051 = False
        return call_old()

    def _do(self, call):
        try:
            return self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            text = (getattr(exc, "message", None) or str(exc)).lower()
            if any(c in text for c in TEACHING + ("hinted",)) and (
                    "does not exist" in text or "could not find" in text):
                raise _NoColumn() from exc
            if ("schema cache" in text or "could not find the function" in text
                    or ('relation "public.decks"' in text) or "study_" in text and "does not exist" in text):
                raise StudyNotInstalled(
                    "Study Hub isn't installed on the server yet. Run "
                    "database/migrations/050_study_hub_flashcards.sql.") from exc
            raise AccountError(friendly(exc)) from exc

    def user_id(self) -> str:
        return self._s.user_id()

    # ------------------------------------------------------------- reading

    def _since(self, table: str, columns: str, stamp: str, since: Optional[str]) -> list[dict]:
        rows: list[dict] = []
        start = 0
        while True:
            def call(start=start):
                query = self._s.table(table).select(columns)
                if since:
                    query = query.gt(stamp, since)
                return (query.order(stamp).range(start, start + PAGE - 1).execute().data) or []
            page = self._do(call)
            rows.extend(page)
            if len(page) < PAGE:
                return rows
            start += PAGE

    def subjects(self) -> list[dict]:
        return self._do(lambda: self._s.table("study_subjects").select("*").order("position")
                        .execute().data) or []

    def decks_since(self, since: Optional[str]) -> list[dict]:
        return self._since("decks", DECK_COLUMNS, "server_updated_at", since)

    def official_deck_ids(self) -> set[str]:
        rows = self._do(lambda: self._s.table("decks").select("id").eq("origin", "official")
                        .execute().data) or []
        return {str(r["id"]) for r in rows}

    def cards_since(self, since: Optional[str]) -> list[dict]:
        return self._teaching(
            lambda: self._since("cards", CARD_COLUMNS + ", " + ", ".join(TEACHING), "server_updated_at", since),
            lambda: self._since("cards", CARD_COLUMNS, "server_updated_at", since))

    def states_since(self, since: Optional[str]) -> list[dict]:
        return self._since("card_states", STATE_COLUMNS, "server_updated_at", since)

    def reviews_since(self, since: Optional[str]) -> list[dict]:
        return self._teaching(
            lambda: self._since("review_log", LOG_COLUMNS + ", hinted", "server_received_at", since),
            lambda: self._since("review_log", LOG_COLUMNS, "server_received_at", since))

    def settings(self) -> Optional[dict]:
        rows = self._do(lambda: self._s.table("study_settings").select("*").execute().data) or []
        return rows[0] if rows else None

    # ------------------------------------------------------------- writing

    def _upsert(self, table: str, rows: list[dict], conflict: str, ignore: bool = False) -> None:
        for i in range(0, len(rows), 100):
            chunk = rows[i:i + 100]
            self._do(lambda chunk=chunk: self._s.table(table)
                     .upsert(chunk, on_conflict=conflict, ignore_duplicates=ignore).execute())

    def upsert_decks(self, rows: list[dict]) -> None:
        self._upsert("decks", rows, "id")

    def upsert_cards(self, rows: list[dict]) -> None:
        self._teaching(lambda: self._upsert("cards", rows, "id"),
                       lambda: self._upsert("cards", [{k: v for k, v in r.items() if k not in TEACHING}
                                                      for r in rows], "id"))

    def upsert_states(self, rows: list[dict]) -> None:
        self._upsert("card_states", rows, "user_id,card_key")

    def push_reviews(self, rows: list[dict]) -> None:
        """Idempotent: a review already uploaded (same client_id) is skipped."""
        self._teaching(lambda: self._upsert("review_log", rows, "client_id", ignore=True),
                       lambda: self._upsert("review_log", [{k: v for k, v in r.items() if k != "hinted"}
                                                           for r in rows], "client_id", ignore=True))

    def upsert_settings(self, row: dict) -> None:
        self._upsert("study_settings", [row], "user_id")

    # ----------------------------------------------------- reports, staff

    def report_card(self, card_ref: str, reason: str, note: str) -> None:
        self._do(lambda: self._s.rpc("report_card", {"p_card_ref": card_ref, "p_reason": reason,
                                                     "p_note": note}).execute())

    def admin_list_decks(self) -> list[dict]:
        return self._do(lambda: self._s.rpc("admin_list_decks", {}).execute().data) or []

    def admin_get_deck(self, deck_id: str) -> dict:
        return self._do(lambda: self._s.rpc("admin_get_deck", {"p_id": deck_id}).execute().data) or {}

    def admin_save_deck(self, payload: dict) -> str:
        return str(self._do(lambda: self._s.rpc("admin_save_deck", {"p": payload}).execute().data))

    def admin_set_deck_status(self, deck_id: str, status: str) -> None:
        self._do(lambda: self._s.rpc("admin_set_deck_status",
                                     {"p_id": deck_id, "p_status": status}).execute())

    def admin_delete_deck(self, deck_id: str) -> None:
        self._do(lambda: self._s.rpc("admin_delete_deck", {"p_id": deck_id}).execute())

    def admin_list_card_reports(self) -> list[dict]:
        return self._do(lambda: self._s.rpc("admin_list_card_reports", {}).execute().data) or []

    def admin_resolve_card_report(self, report_id: str) -> None:
        self._do(lambda: self._s.rpc("admin_resolve_card_report", {"p_id": report_id}).execute())
