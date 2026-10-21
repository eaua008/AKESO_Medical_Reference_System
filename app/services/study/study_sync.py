"""Keeps Study Hub the same on every computer (migration 050).

Reviews always happen on this computer first (akeso_study.db), so they work
offline. A sync round:

  1. uploads what changed here: own decks and cards (soft deletes too),
     new reviews (each has a client_id, so sending one twice does nothing),
     suspensions and resets, and the settings;
  2. downloads what changed elsewhere: own decks and cards (the newer edit
     wins), the published official decks (and drops any that were
     unpublished), reviews done on other computers, resets, settings;
  3. rebuilds the schedule of every card that got new reviews by REPLAYING
     its whole review history in time order. Two computers that saw the same
     reviews end in exactly the same state, whatever order they synced in.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional

from app.models.study import CardState, CardStateKind, Rating, ReviewLogEntry
from app.repositories.study_local_repository import (
    StudyLocalRepository, iso, now_iso, parse_time, state_to_json,
)
from app.services.srs.scheduler import Scheduler


@dataclass
class StudySyncResult:
    uploaded: int = 0
    downloaded: int = 0
    rebuilt: int = 0

    @property
    def changed_here(self) -> bool:
        return self.downloaded > 0 or self.rebuilt > 0


def replay(card_key: str, entries: Iterable[ReviewLogEntry], scheduler: Scheduler,
           reset_at: Optional[datetime] = None) -> CardState:
    """The card's state after every review in its history (de-duplicated by
    client_id, in time order, ignoring anything before a reset)."""
    seen, ordered = set(), []
    for entry in sorted(entries, key=lambda e: (e.reviewed_at, e.client_id)):
        if entry.client_id in seen or entry.card_key != card_key:
            continue
        seen.add(entry.client_id)
        if reset_at is not None and entry.reviewed_at <= reset_at:
            continue
        ordered.append(entry)
    state = CardState(card_key)
    for entry in ordered:
        state = scheduler.answer(state, Rating(int(entry.rating)), entry.reviewed_at)
    return state


def _later(a: Optional[str], b: Optional[str]) -> bool:
    """a is later than b (ISO times; None is the earliest)."""
    ta, tb = parse_time(a), parse_time(b)
    if ta is None:
        return False
    return tb is None or ta > tb


class StudySync:
    def __init__(self, local: StudyLocalRepository, remote, scheduler: Scheduler) -> None:
        self.local = local
        self.remote = remote                 # SupabaseStudyRepository (or a fake in tests)
        self.scheduler = scheduler

    def has_local_changes(self) -> bool:
        return bool(self.local.unsynced("decks") or self.local.unsynced("cards")
                    or self.local.unsynced_reviews() or self.local.unsynced_states()
                    or (self.local.settings_row() or {}).get("synced") is False)

    # ---------------------------------------------------------------- round

    def sync(self, push_reviews: bool = True) -> StudySyncResult:
        result = StudySyncResult()
        uid = self.remote.user_id()
        self._push(uid, result, push_reviews)
        touched = self._pull(uid, result)
        for key in touched:
            self._rebuild(key)
            result.rebuilt += 1
        return result

    # ----------------------------------------------------------------- push

    def _push(self, uid: str, result: StudySyncResult, push_reviews: bool) -> None:
        decks = [d for d in self.local.unsynced("decks") if d.get("origin") == "personal"]
        if decks:
            self.remote.upsert_decks([{
                "id": d["id"], "title": d["title"], "description": d.get("description") or "",
                "subject_id": d.get("subject_id") or None, "origin": "personal", "owner_id": uid,
                "visibility": d.get("visibility") or "private", "updated_at": d.get("updated_at") or now_iso(),
                "deleted_at": d.get("deleted_at")} for d in decks])
            self.local.mark_synced("decks", [d["id"] for d in decks])
            result.uploaded += len(decks)
        own_decks = {d.id for d in self.local.decks(include_deleted=True) if d.origin.value == "personal"}
        cards = [c for c in self.local.unsynced("cards") if c.get("deck_id") in own_decks]
        if cards:
            self.remote.upsert_cards([{
                "id": c["id"], "deck_id": c["deck_id"], "type": c["type"], "front": c.get("front") or "",
                "back": c.get("back") or "", "choices": c.get("choices") or [],
                "cloze_text": c.get("cloze_text") or "", "part_ids": c.get("part_ids") or [],
                "source_kind": c.get("source_kind"), "source_id": c.get("source_id"),
                "tags": c.get("tags") or [], "position": c.get("position") or 0,
                "answer_short": c.get("answer_short") or "", "explanation": c.get("explanation") or "",
                "distinguish": c.get("distinguish") or "", "hint": c.get("hint") or "",
                "difficulty": c.get("difficulty") or "",
                "updated_at": c.get("updated_at") or now_iso(), "deleted_at": c.get("deleted_at")}
                for c in cards])
            self.local.mark_synced("cards", [c["id"] for c in cards])
            result.uploaded += len(cards)
        if push_reviews:
            reviews = self.local.unsynced_reviews()
            if reviews:
                self.remote.push_reviews([{
                    "user_id": uid, "client_id": e.client_id, "card_key": e.card_key, "rating": int(e.rating),
                    "reviewed_at": iso(e.reviewed_at), "elapsed_ms": e.elapsed_ms,
                    "state_before": e.state_before, "interval_before": e.interval_before,
                    "interval_after": e.interval_after, "ease_after": e.ease_after,
                    "hinted": e.hinted} for e in reviews])
                self.local.mark_reviews_synced([e.client_id for e in reviews])
                result.uploaded += len(reviews)
        states = self.local.unsynced_states()
        if states:
            # seen_hash stays on this computer (it only drives the "Updated" badge)
            self.remote.upsert_states([dict({k: v for k, v in row.items() if k != "seen_hash"},
                                            user_id=uid, card_key=key, updated_at=updated)
                                       for key, row, updated in states])
            self.local.mark_states_synced([key for key, _r, _u in states])
        settings = self.local.settings_row()
        if settings and not settings.get("synced"):
            self.remote.upsert_settings({
                "user_id": uid, "new_per_day": settings["new_per_day"],
                "max_reviews": settings["max_reviews"], "learning_steps": settings["learning_steps"],
                "relearn_steps": settings["relearn_steps"], "updated_at": settings["updated_at"]})
            self.local.save_settings(self.local.settings(), synced=True, updated_at=settings["updated_at"])

    # ----------------------------------------------------------------- pull

    def _pull(self, uid: str, result: StudySyncResult) -> set[str]:
        touched: set[str] = set()
        # decks
        since = self.local.meta("pull_decks") or None
        newest = since
        for row in self.remote.decks_since(since):
            newest = max(newest or "", str(row.get("server_updated_at") or "")) or newest
            if self._merge_row("deck", row):
                result.downloaded += 1
        if newest:
            self.local.set_meta("pull_decks", newest)
        # official decks that were unpublished or deleted: forget them here
        live = self.remote.official_deck_ids()
        for deck in self.local.decks(include_deleted=True):
            if deck.origin.value == "official" and deck.id not in live:
                self.local.remove_deck_local(deck.id)
                result.downloaded += 1
        # cards
        since = self.local.meta("pull_cards") or None
        newest = since
        known = {d.id for d in self.local.decks(include_deleted=True)}
        for row in self.remote.cards_since(since):
            newest = max(newest or "", str(row.get("server_updated_at") or "")) or newest
            if str(row.get("deck_id")) in known and self._merge_row("card", row):
                result.downloaded += 1
        if newest:
            self.local.set_meta("pull_cards", newest)
        # reviews done elsewhere
        since = self.local.meta("pull_reviews") or None
        newest = since
        for row in self.remote.reviews_since(since):
            newest = max(newest or "", str(row.get("server_received_at") or "")) or newest
            entry = ReviewLogEntry(card_key=row["card_key"], rating=int(row["rating"]),
                                   reviewed_at=parse_time(row["reviewed_at"]), client_id=str(row["client_id"]),
                                   elapsed_ms=int(row.get("elapsed_ms") or 0),
                                   state_before=row.get("state_before") or "new",
                                   interval_before=float(row.get("interval_before") or 0),
                                   interval_after=float(row.get("interval_after") or 0),
                                   ease_after=float(row.get("ease_after") or 2.5),
                                   hinted=bool(row.get("hinted")))
            if self.local.add_review(entry, synced=True):
                touched.add(entry.card_key)
                result.downloaded += 1
        if newest:
            self.local.set_meta("pull_reviews", newest)
        # resets and suspensions done elsewhere
        since = self.local.meta("pull_states") or None
        newest = since
        for row in self.remote.states_since(since):
            newest = max(newest or "", str(row.get("server_updated_at") or "")) or newest
            key = row["card_key"]
            mine = self.local.state_row(key) or {}
            if mine and not mine.get("synced") and not _later(row.get("updated_at"), mine.get("updated_at")):
                continue                                  # my unsent change is newer
            reset = row.get("reset_at") if _later(row.get("reset_at"), mine.get("reset_at")) \
                else mine.get("reset_at")
            current = self.local.states().get(key) or CardState(key)
            if row.get("state") == CardStateKind.SUSPENDED.value:
                current = current.copy(state=CardStateKind.SUSPENDED)
            self.local.save_state(current, synced=True, reset_at=reset, updated_at=row.get("updated_at"))
            touched.add(key)
        if newest:
            self.local.set_meta("pull_states", newest)
        # settings
        remote = self.remote.settings()
        mine = self.local.settings_row()
        if remote and (mine is None or (mine.get("synced") and _later(remote.get("updated_at"), mine.get("updated_at")))):
            from app.models.study import StudySettings
            here = self.local.settings()                  # typing and filters stay on this computer
            self.local.save_settings(StudySettings(
                type_answer=here.type_answer, difficulties=here.difficulties, families=here.families,
                new_per_day=int(remote.get("new_per_day") or 20), max_reviews=int(remote.get("max_reviews") or 200),
                learning_steps=[int(x) for x in (remote.get("learning_steps") or [1, 10])],
                relearn_steps=[int(x) for x in (remote.get("relearn_steps") or [10])]),
                synced=True, updated_at=remote.get("updated_at"))
        return touched

    def _merge_row(self, kind: str, row: dict) -> bool:
        """Save a downloaded deck/card unless my unsent edit is newer."""
        row = dict(row)
        row["id"] = str(row["id"])
        if kind == "card":
            row["deck_id"] = str(row["deck_id"])
        mine = self.local.deck_row(row["id"]) if kind == "deck" else self.local.card_row(row["id"])
        if mine and not mine.get("synced") and not _later(row.get("updated_at"), mine.get("updated_at")):
            return False
        row.pop("server_updated_at", None)
        if kind == "deck":
            self.local.save_deck_row(row, synced=True)
        else:
            self.local.save_card_row(row, synced=True)
        return True

    # -------------------------------------------------------------- rebuild

    def _rebuild(self, key: str) -> None:
        mine = self.local.state_row(key) or {}
        reset = parse_time(mine.get("reset_at"))
        state = replay(key, self.local.reviews(card_key=key), self.scheduler, reset)
        if mine.get("state") == CardStateKind.SUSPENDED.value:
            state = state.copy(state=CardStateKind.SUSPENDED)
        # the rebuilt state is what every computer computes: no need to upload it
        self.local.save_state(state, synced=bool(mine.get("synced", True)) or not mine,
                              reset_at=mine.get("reset_at"), updated_at=mine.get("updated_at"))


__all__ = ["StudySync", "StudySyncResult", "replay", "state_to_json"]
