"""The scheduler interface, and the day boundary every scheduler shares.

A scheduler only answers "after this rating, what is the card's next state?"
and "what would each rating do?" (the labels on the rating buttons). It never
touches storage. SM-2 is the one in use (sm2.py); FSRS can be added later as
another Scheduler without changing anything that calls it.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.models.study import CardState, Rating, StudySettings


def local(now: datetime) -> datetime:
    """The same moment in this computer's time zone."""
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return now.astimezone()


def day_start(now: datetime, hour: int = 4) -> datetime:
    """When today's study day began: 04:00 local time, like Anki, so a late
    night session still counts as "today" (aware datetime, local zone)."""
    here = local(now)
    start = here.replace(hour=hour, minute=0, second=0, microsecond=0)
    if here < start:
        start -= timedelta(days=1)
    return start


def day_number(moment: datetime, hour: int = 4) -> int:
    """A whole number that changes once per study day (for streaks and fuzz)."""
    return day_start(moment, hour).date().toordinal()


def interval_label(seconds: float) -> str:
    """'1 min', '10 min', '1 d', '3 d', '1.5 mo', '1.2 y': short, for buttons."""
    if seconds < 60 * 60:
        return f"{max(1, round(seconds / 60))} min"
    if seconds < 24 * 60 * 60:
        return f"{round(seconds / 3600)} h"
    days = seconds / 86400
    if days < 30:
        return f"{round(days)} d"
    if days < 365:
        months = days / 30
        return f"{months:.1f} mo".replace(".0 ", " ")
    return f"{days / 365:.1f} y".replace(".0 ", " ")


class Scheduler(ABC):
    def __init__(self, settings: Optional[StudySettings] = None) -> None:
        self.settings = settings or StudySettings()

    @abstractmethod
    def answer(self, state: CardState, rating: Rating, now: datetime) -> CardState:
        """The card's state after this rating at this moment."""

    def preview(self, state: CardState, now: datetime) -> dict[Rating, str]:
        """What each button would do: {Rating.AGAIN: '1 min', Rating.GOOD: '1 d', ...}."""
        out = {}
        for rating in Rating:
            after = self.answer(state, rating, now)
            seconds = max(0.0, (after.due - now).total_seconds()) if after.due else 0.0
            out[rating] = interval_label(seconds)
        return out
