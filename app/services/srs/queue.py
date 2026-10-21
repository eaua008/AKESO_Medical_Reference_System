"""Today's review queue: what to study next, in what order.

    1. learning and relearning cards that are due (they are on a timer)
    2. reviews that are due, oldest first, up to the reviews-a-day limit
       (reviews already done today count against it)
    3. new cards, in deck order, up to the new-cards-a-day limit (cards
       first seen today count against it, from the review history)

A learning card due in the next 20 minutes is shown early when nothing else
is left, so a session doesn't stall waiting for a 10-minute step.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Iterable, Optional

from app.models.study import CardState, CardStateKind, ReviewLogEntry, StudySettings
from app.services.srs.scheduler import day_start

LEARN_AHEAD = timedelta(minutes=20)
S = CardStateKind


@dataclass
class Queue:
    learning: list[str] = field(default_factory=list)
    reviews: list[str] = field(default_factory=list)
    new: list[str] = field(default_factory=list)
    waiting: list[str] = field(default_factory=list)     # learning, due later today

    @property
    def order(self) -> list[str]:
        return self.learning + self.reviews + self.new

    @property
    def due_count(self) -> int:
        return len(self.learning) + len(self.reviews) + len(self.waiting)

    @property
    def total(self) -> int:
        return len(self.order) + len(self.waiting)


def _today(log: Iterable[ReviewLogEntry], now: datetime, hour: int):
    start = day_start(now, hour)
    return [e for e in log if e.reviewed_at >= start]


def new_seen_today(log: Iterable[ReviewLogEntry], now: datetime, hour: int = 4) -> int:
    """New cards introduced today (each card counted once)."""
    return len({e.card_key for e in _today(log, now, hour) if e.state_before == S.NEW.value})


def reviews_done_today(log: Iterable[ReviewLogEntry], now: datetime, hour: int = 4) -> int:
    return len({e.card_key for e in _today(log, now, hour) if e.state_before == S.REVIEW.value})


def build_queue(keys: list[str], states: dict[str, CardState], settings: StudySettings,
                log: Iterable[ReviewLogEntry], now: datetime,
                limit_new: Optional[int] = None) -> Queue:
    """keys: the cards to study, in deck order. states: by card_key (missing = new)."""
    log = list(log)
    hour = settings.day_starts_at_hour
    end_of_day = day_start(now, hour) + timedelta(days=1)
    queue = Queue()
    reviews: list[tuple[datetime, str]] = []
    new: list[str] = []
    for key in keys:
        state = states.get(key)
        if state is None or state.state == S.NEW:
            new.append(key)
        elif state.state == S.SUSPENDED:
            continue
        elif state.state in (S.LEARNING, S.RELEARNING):
            due = state.due or now
            if due <= now:
                queue.learning.append(key)
            elif due < end_of_day:
                queue.waiting.append(key)
        elif state.state == S.REVIEW and state.due is not None and state.due <= now:
            reviews.append((state.due, key))
    queue.learning.sort(key=lambda k: states[k].due or now)
    queue.waiting.sort(key=lambda k: states[k].due or now)
    reviews.sort()
    room = max(0, settings.max_reviews - reviews_done_today(log, now, hour))
    queue.reviews = [key for _due, key in reviews[:room]]
    quota = settings.new_per_day if limit_new is None else limit_new
    room_new = max(0, quota - new_seen_today(log, now, hour))
    queue.new = new[:room_new]
    return queue


def next_card(queue: Queue, states: dict[str, CardState], now: datetime) -> Optional[str]:
    """The next card to show, or None when the session is done."""
    order = queue.order
    if order:
        return order[0]
    if queue.waiting:
        key = queue.waiting[0]
        due = states[key].due if key in states else now
        if due is None or due - now <= LEARN_AHEAD:
            return key
    return None
