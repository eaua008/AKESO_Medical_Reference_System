"""Bookmarks: what a user starred, and how it is shown back to them.

A bookmark stores only a type and an id. The title, description and severity
shown on the Bookmarks page are looked up from the encyclopedias at display
time, so an entry that is edited in Supabase is never stale here, and a
deleted entry can be reported as missing rather than shown as a ghost.
"""

from dataclasses import dataclass
from datetime import datetime, timezone

# What can be bookmarked. The value is what is stored in the database.
DISEASE, SYMPTOM, MEDICINE = "disease", "symptom", "medicine"

KIND_LABELS = {
    DISEASE: "Condition",
    SYMPTOM: "Symptom",
    MEDICINE: "Medicine",
}
# Which tab each kind belongs to, and the order the tabs appear in.
KIND_ORDER = (DISEASE, SYMPTOM, MEDICINE)


def now_iso() -> str:
    """UTC, so bookmarks still sort correctly if the device timezone changes."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Bookmark:
    """One starred entry, as stored."""

    owner: str            # the signed-in account this belongs to
    entity_type: str      # DISEASE | SYMPTOM | MEDICINE
    entity_id: str
    created_at: str


@dataclass(frozen=True)
class BookmarkEntry:
    """A bookmark joined with the entry it points at, ready to draw."""

    bookmark: Bookmark
    title: str
    subtitle: str = ""
    description: str = ""
    meta: str = ""            # severity, weight tier, or regulatory class
    missing: bool = False     # the entry is no longer in the encyclopedia

    @property
    def entity_type(self) -> str:
        return self.bookmark.entity_type

    @property
    def entity_id(self) -> str:
        return self.bookmark.entity_id

    @property
    def kind_label(self) -> str:
        return KIND_LABELS.get(self.entity_type, self.entity_type.title())