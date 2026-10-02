"""Counts study activity in memory and hands it over in batches.

Opening a disease page should not cost a network request, so views only
bump a counter here; the account controller sends the totals once a minute
(and at sign-out) through record_activity(). If the student switched
tracking off, nothing is counted at all.
"""

from app.models.account import ACTIVITY_FIELDS

FIELDS = {key for key, _label in ACTIVITY_FIELDS}


class ActivityTracker:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled
        self._counts: dict[str, int] = {}

    def bump(self, field: str, amount: int = 1) -> None:
        if self.enabled and field in FIELDS and amount > 0:
            self._counts[field] = self._counts.get(field, 0) + amount

    def pending(self) -> bool:
        return bool(self._counts)

    def take(self) -> dict[str, int]:
        """The counts so far, emptied. Put them back with restore() on failure."""
        counts, self._counts = self._counts, {}
        return counts

    def restore(self, counts: dict[str, int]) -> None:
        for key, value in counts.items():
            self.bump(key, value)
