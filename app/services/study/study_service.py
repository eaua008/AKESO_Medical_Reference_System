"""Study Hub: what the screens ask for, in one place.

    decks + counts      official (cached), own, and Auto decks made from the
                        encyclopedia on this computer
    the review queue    for one deck, or "Today" across every deck in use
    answering           rate a card (SM-2), undo the last rating
    own content         make, rename, delete decks; add, edit, delete cards
    numbers             due today, streak, weak cards

Everything here reads and writes the local store; StudySync carries it to
the server. No Qt, so it can run on a worker thread and in tests.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable, Iterable, Optional

from app.models.study import (
    RETIRED_PREFIX, Card, CardState, CardStateKind, Deck, Origin, Rating, ReviewLogEntry, StudySettings,
    Subject,
    new_id,
)
from app.repositories.study_local_repository import StudyLocalRepository, now_iso
from app.services.srs.queue import Queue, build_queue, next_card
from app.services.srs.scheduler import day_number, day_start
from app.services.srs.sm2 import Sm2Scheduler
from app.services.study.auto_cards import AutoCardBuilder, AutoSet

SUBJECTS = [Subject("anatomy", "Anatomy", "heart-pulse", 1),
            Subject("pathology", "Pathology", "activity", 2),
            Subject("pharmacology", "Pharmacology", "pill", 3),
            Subject("microbiology", "Microbiology", "microscope", 4)]
MY_CARDS = "My cards"
S = CardStateKind


@dataclass
class DeckCounts:
    total: int = 0
    new: int = 0
    due: int = 0
    learned: int = 0
    learning: int = 0        # started, not yet learned


@dataclass
class DeckSummary:
    deck: Deck
    counts: DeckCounts
    started: bool = False           # has at least one card been studied


@dataclass
class Undo:
    entry: ReviewLogEntry
    before: Optional[CardState]


class StudyService:
    def __init__(self, local: StudyLocalRepository,
                 diseases: Callable[[], Iterable] = list, symptoms: Callable[[], Iterable] = list,
                 medicines: Callable[[], Iterable] = list,
                 clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)) -> None:
        self.local = local
        self._diseases, self._symptoms, self._medicines = diseases, symptoms, medicines
        self._clock = clock
        self._auto: Optional[AutoSet] = None
        self._auto_sig = None
        self._builder: Optional[AutoCardBuilder] = None
        self._entry_decks: dict[str, Deck] = {}

    # -------------------------------------------------------------- basics

    def now(self) -> datetime:
        return self._clock()

    def settings(self) -> StudySettings:
        return self.local.settings()

    def save_settings(self, settings: StudySettings) -> None:
        self.local.save_settings(settings, synced=False)

    def scheduler(self) -> Sm2Scheduler:
        return Sm2Scheduler(self.settings())

    @staticmethod
    def subjects() -> list[Subject]:
        return list(SUBJECTS)

    # ---------------------------------------------------------- auto cards

    def auto(self) -> AutoSet:
        diseases, symptoms, medicines = list(self._diseases()), list(self._symptoms()), list(self._medicines())
        sig = (len(diseases), len(symptoms), len(medicines),
               max((getattr(x, "id", "") for x in diseases), default=""))
        if self._auto is None or sig != self._auto_sig:
            self._builder = AutoCardBuilder(diseases, symptoms, medicines)
            self._auto = self._builder.build()
            self._auto_sig = sig
        return self._auto

    def entry_deck(self, kind: str, entry_id: str, name: str) -> Optional[Deck]:
        auto = self.auto()
        deck = self._builder.entry_deck(auto, kind, entry_id, name) if self._builder else None
        if deck is not None:
            self._entry_decks[deck.id] = deck
        return deck

    # --------------------------------------------------------------- decks

    def decks(self) -> list[Deck]:
        own = self.local.decks()
        return own + list(self.auto().decks)

    def deck(self, deck_id: str) -> Optional[Deck]:
        if deck_id.startswith("auto-deck:"):
            found = next((d for d in self.auto().decks if d.id == deck_id), None)                 or self._entry_decks.get(deck_id)
            if found is None and deck_id.startswith("auto-deck:entry:"):
                _a, _b, kind, entry_id = deck_id.split(":", 3)
                return self.entry_deck(kind, entry_id, entry_id)
            return found
        return self.local.deck(deck_id)

    def cards(self, deck_id: str) -> list[Card]:
        if deck_id.startswith("auto-deck:"):
            return list(self.auto().cards.get(deck_id, []))
        return self.local.cards(deck_id)

    def card(self, key: str) -> Optional[Card]:
        if key.startswith(("auto:", "auto2:")):
            return next((c for c in self.auto().all_cards() if c.card_key == key), None)
        row = self.local.card_row(key)
        if row is None or row.get("deleted_at"):
            return None
        return Card.from_row(row)

    def deck_of(self, card: Card) -> Optional[Deck]:
        return self.deck(card.deck_id)

    def summaries(self) -> list[DeckSummary]:
        states = self.local.states()
        now = self.now()
        out = []
        for deck in self.decks():
            out.append(self._summary(deck, self.cards(deck.id), states, now))
        return out

    def summary(self, deck_id: str) -> Optional[DeckSummary]:
        deck = self.deck(deck_id)
        if deck is None:
            return None
        return self._summary(deck, self.cards(deck_id), self.local.states(), self.now())

    @staticmethod
    def _summary(deck: Deck, cards: list[Card], states: dict, now: datetime) -> DeckSummary:
        # "due" = due today: learning steps coming back later today count too
        until = day_start(now) + timedelta(days=1)
        counts = DeckCounts(total=len(cards))
        started = False
        for card in cards:
            state = states.get(card.card_key)
            if state is None or state.state == S.NEW:
                counts.new += 1
                continue
            started = True
            if state.state == S.SUSPENDED:
                continue
            if state.due is not None and (state.due <= now or (
                    state.state in (S.LEARNING, S.RELEARNING) and state.due < until)):
                counts.due += 1
            if state.state == S.REVIEW:
                counts.learned += 1
            else:
                counts.learning += 1
        return DeckSummary(deck, counts, started)

    # ------------------------------------------------------------- queues

    @staticmethod
    def _wanted(card: Card, difficulties, families) -> bool:
        if difficulties and (card.difficulty or "basic") not in difficulties:
            return False
        if families and card.family not in families:
            return False
        return True

    def queue(self, deck_id: Optional[str] = None, difficulties: Optional[list] = None,
              families: Optional[list] = None) -> Queue:
        """One deck's queue, or Today's: every card already being studied that is
        due, plus new cards from the decks you have started."""
        states = self.local.states()
        settings = self.settings()
        now = self.now()
        log = self.local.reviews(since=day_start(now, settings.day_starts_at_hour))
        difficulties = settings.difficulties if difficulties is None else difficulties
        families = settings.families if families is None else families
        if deck_id is not None:
            keys = [c.card_key for c in self.cards(deck_id) if self._wanted(c, difficulties, families)]
        else:
            keys = []
            seen = set()
            for summary in self.summaries():
                for card in self.cards(summary.deck.id):
                    key = card.card_key
                    if key in seen or not self._wanted(card, difficulties, families):
                        continue
                    state = states.get(key)
                    if (state is not None and state.state != S.NEW) or summary.started:
                        seen.add(key)
                        keys.append(key)
        return build_queue(keys, states, settings, log, now)

    def next_key(self, queue: Queue) -> Optional[str]:
        return next_card(queue, self.local.states(), self.now())

    def due_today(self) -> tuple[int, int]:
        """(cards due, new cards waiting) for Today, the sidebar and the dashboard."""
        q = self.queue()
        return len(q.learning) + len(q.reviews) + len(q.waiting), len(q.new)

    # ------------------------------------------------------------ answering

    def state(self, key: str) -> CardState:
        return self.local.states().get(key) or CardState(key)

    def preview(self, key: str) -> dict[Rating, str]:
        return self.scheduler().preview(self.state(key), self.now())

    def answer(self, key: str, rating: Rating, elapsed_ms: int = 0, hinted: bool = False) -> Undo:
        before_row = self.local.state_row(key)
        before = self.state(key)
        now = self.now()
        after = self.scheduler().answer(before, rating, now)
        entry = ReviewLogEntry(card_key=key, rating=int(rating), reviewed_at=now,
                               elapsed_ms=max(0, int(elapsed_ms)), state_before=before.state.value,
                               interval_before=before.interval_days, interval_after=after.interval_days,
                               ease_after=after.ease, hinted=hinted)
        self.local.add_review(entry)
        card = self.card(key)
        self.local.save_state(after, seen_hash=card.content_hash if card else "")
        return Undo(entry, before if before_row else None)

    def is_updated(self, card) -> bool:
        """The card's content changed since this person last reviewed it ("Updated" badge)."""
        row = self.local.state_row(card.card_key) or {}
        seen = row.get("seen_hash") or ""
        return bool(seen and card.content_hash and seen != card.content_hash)

    def undo(self, token: Undo) -> None:
        self.local.remove_review(token.entry.client_id)
        if token.before is None:
            self.local.delete_state(token.entry.card_key)
        else:
            self.local.save_state(token.before)

    def reset_deck(self, deck_id: str) -> int:
        """Forget the progress of every card in a deck (history before now is ignored)."""
        stamp = now_iso()
        cards = self.cards(deck_id)
        for card in cards:
            self.local.save_state(CardState(card.card_key), synced=False, reset_at=stamp)
        return len(cards)

    # ---------------------------------------------------------------- stats

    def streak(self) -> int:
        """Days in a row (up to today, or yesterday if not studied yet today) with a review."""
        hour = self.settings().day_starts_at_hour
        days = {day_number(e.reviewed_at, hour) for e in self.local.reviews(
            since=self.now() - timedelta(days=400))}
        today = day_number(self.now(), hour)
        start = today if today in days else today - 1
        count = 0
        while start - count in days:
            count += 1
        return count

    def weak_cards(self, limit: int = 10) -> list[tuple[Card, CardState]]:
        out = []
        for key, state in sorted(self.local.states().items(), key=lambda kv: -kv[1].lapses):
            if state.lapses <= 0 or len(out) >= limit:
                break
            card = self.card(key)
            if card is not None:
                out.append((card, state))
        return out

    def reviewed_today(self) -> int:
        start = day_start(self.now(), self.settings().day_starts_at_hour)
        return len(self.local.reviews(since=start))

    def seconds_per_card(self) -> float:
        """How long a card usually takes this person (10 s until there is history)."""
        recent = [e.elapsed_ms for e in self.local.reviews(since=self.now() - timedelta(days=30))
                  if 0 < e.elapsed_ms < 5 * 60_000]
        return sum(recent) / len(recent) / 1000 if len(recent) >= 5 else 10.0

    def forecast(self, days: int = 7) -> list[tuple[str, int]]:
        """Cards that come due on each of the next days ("Today" counts what is due now)."""
        hour = self.settings().day_starts_at_hour
        start = day_start(self.now(), hour)
        counts = [0] * days
        for key, state in self.local.states().items():
            if key.startswith(RETIRED_PREFIX) or state.state in (S.NEW, S.SUSPENDED) or state.due is None:
                continue
            index = 0 if state.due < start + timedelta(days=1) else int((state.due - start).total_seconds() // 86400)
            if 0 <= index < days:
                counts[index] += 1
        labels = ["Today"] + [(start + timedelta(days=i)).strftime("%a") for i in range(1, days)]
        return list(zip(labels, counts))

    def session_stats(self, since: datetime) -> dict:
        log = [e for e in self.local.reviews(since=since)]
        right = sum(1 for e in log if e.rating >= Rating.GOOD)
        return {"reviewed": len(log), "correct": right, "seconds": sum(e.elapsed_ms for e in log) / 1000}

    # ----------------------------------------------------------- own decks

    def create_deck(self, title: str, subject_id: str = "", description: str = "") -> Deck:
        title = title.strip()[:120] or "Untitled deck"
        row = {"id": new_id(), "title": title, "description": description.strip()[:1000],
               "subject_id": subject_id or None, "origin": "personal", "status": "draft",
               "visibility": "private", "updated_at": now_iso()}
        self.local.save_deck_row(row, synced=False)
        return Deck.from_row(row)

    def rename_deck(self, deck_id: str, title: str) -> None:
        row = self.local.deck_row(deck_id)
        if row is None or row.get("origin") != "personal":
            return
        row["title"] = title.strip()[:120] or row["title"]
        row["updated_at"] = now_iso()
        self.local.save_deck_row(row, synced=False)

    def delete_deck(self, deck_id: str) -> None:
        row = self.local.deck_row(deck_id)
        if row is None or row.get("origin") != "personal":
            return
        stamp = now_iso()
        for card in self.local.cards(deck_id):
            card_row = self.local.card_row(card.id)
            card_row.update(deleted_at=stamp, updated_at=stamp)
            self.local.save_card_row(card_row, synced=False)
        row.update(deleted_at=stamp, updated_at=stamp)
        self.local.save_deck_row(row, synced=False)

    def my_cards_deck(self) -> Deck:
        found = next((d for d in self.local.decks() if d.origin == Origin.PERSONAL and d.title == MY_CARDS), None)
        return found or self.create_deck(MY_CARDS)

    def own_decks(self) -> list[Deck]:
        return [d for d in self.local.decks() if d.origin == Origin.PERSONAL]

    def save_card(self, card: Card) -> Card:
        problems = card.problems()
        if problems:
            raise ValueError(problems[0])
        deck = self.local.deck(card.deck_id)
        if deck is None or deck.origin != Origin.PERSONAL:
            raise ValueError("Cards can only be added to your own decks.")
        if not card.id:
            card.id = new_id()
            card.position = len(self.local.cards(card.deck_id)) + 1
        row = card.to_row()
        row["updated_at"] = now_iso()
        self.local.save_card_row(row, synced=False)
        deck_row = self.local.deck_row(card.deck_id)
        deck_row["updated_at"] = now_iso()
        self.local.save_deck_row(deck_row, synced=False)
        return card

    def delete_card(self, card_id: str) -> None:
        row = self.local.card_row(card_id)
        if row is None:
            return
        stamp = now_iso()
        row.update(deleted_at=stamp, updated_at=stamp)
        self.local.save_card_row(row, synced=False)
