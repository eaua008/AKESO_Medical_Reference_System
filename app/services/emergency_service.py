"""Business rules for the Emergency Guide.

Right now that's one rule: how the protocol filter matches. It lives here, not
in the view, so a test can check "does 'rabies' find the animal bite card?"
without building any widgets.
"""

from typing import Optional

from app.models.emergency import EmergencyGuide, EmergencyProtocol
from app.repositories.emergency_repository import BundledEmergencyRepository

# Life-threatening protocols first, whatever order the data file uses.
URGENCY_ORDER = {"critical": 0, "urgent": 1, "same_day": 2}


class EmergencyService:
    """Serves the guide and filters its protocols."""

    def __init__(self, repository: Optional[object] = None) -> None:
        self._repository = repository or BundledEmergencyRepository()

    def guide(self) -> EmergencyGuide:
        return self._repository.load()

    def protocols(self) -> list[EmergencyProtocol]:
        # sorted() is stable, so protocols with equal urgency keep file order.
        return sorted(
            self.guide().protocols,
            key=lambda p: URGENCY_ORDER.get(p.urgency, len(URGENCY_ORDER)),
        )

    def filter(self, query: str) -> list[EmergencyProtocol]:
        """Protocols matching every word of the query.

        Searches title, Filipino name, keywords and warning signs, so
        "kagat", "rabies" and "dog bite" all find the same card.
        """
        words = query.lower().split()
        if not words:
            return self.protocols()
        return [p for p in self.protocols() if self._matches(p, words)]

    @staticmethod
    def _matches(protocol: EmergencyProtocol, words: list[str]) -> bool:
        haystack = " ".join(
            (
                protocol.title,
                protocol.local_name,
                *protocol.keywords,
                *protocol.warning_signs,
            )
        ).lower()
        return all(word in haystack for word in words)