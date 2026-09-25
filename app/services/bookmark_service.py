"""Business rules for bookmarks.

The store knows ids; the encyclopedias know content. This class joins the
two, so the Bookmarks page can show a title and a description without
storing a copy of either.

It takes the three services rather than importing repositories directly, so
it reads exactly what the rest of the app reads, cache included.
"""

from typing import Callable, Optional

from app.models.bookmark import (
    DISEASE,
    KIND_ORDER,
    MEDICINE,
    SYMPTOM,
    Bookmark,
    BookmarkEntry,
)
from app.repositories.local_bookmark_store import LocalBookmarkStore


class BookmarkService:
    def __init__(
            self,
            owner: str,
            store: Optional[LocalBookmarkStore] = None,
            disease_lookup: Optional[Callable[[str], object]] = None,
            symptom_lookup: Optional[Callable[[str], object]] = None,
            medicine_lookup: Optional[Callable[[str], object]] = None,
    ) -> None:
        # owner: the signed-in account. Two people sharing a machine keep
        # separate bookmarks, and signing out hides them.
        self._owner = owner
        self._store = store or LocalBookmarkStore()
        self._lookups = {
            DISEASE: disease_lookup,
            SYMPTOM: symptom_lookup,
            MEDICINE: medicine_lookup,
        }

    # ------------------------------------------------------------- state

    def is_bookmarked(self, entity_type: str, entity_id: str) -> bool:
        return self._store.is_bookmarked(self._owner, entity_type, entity_id)

    def ids(self, entity_type: str) -> set[str]:
        """For painting stars across a whole directory in one query."""
        return self._store.ids_for(self._owner, entity_type)

    def set_bookmarked(self, entity_type: str, entity_id: str, state: bool) -> None:
        if state:
            self._store.add(self._owner, entity_type, entity_id)
        else:
            self._store.remove(self._owner, entity_type, entity_id)

    def toggle(self, entity_type: str, entity_id: str) -> bool:
        return self._store.toggle(self._owner, entity_type, entity_id)

    def counts(self) -> dict[str, int]:
        """How many of each kind, for the tab labels."""
        tally = {kind: 0 for kind in KIND_ORDER}
        for bookmark in self._store.list_for(self._owner):
            if bookmark.entity_type in tally:
                tally[bookmark.entity_type] += 1
        return tally

    # ------------------------------------------------------------ joined

    def entries(self, entity_type: str = "") -> list[BookmarkEntry]:
        """Bookmarks with their current content, newest first."""
        return [
            self._resolve(bookmark)
            for bookmark in self._store.list_for(self._owner)
            if not entity_type or bookmark.entity_type == entity_type
        ]

    def _resolve(self, bookmark: Bookmark) -> BookmarkEntry:
        lookup = self._lookups.get(bookmark.entity_type)
        entry = lookup(bookmark.entity_id) if lookup else None
        if entry is None:
            # Starred, then the entry was unpublished or deleted upstream.
            # Say so rather than dropping it silently, so the user can unstar it.
            return BookmarkEntry(
                bookmark=bookmark,
                title="Entry no longer available",
                subtitle="",
                description="This entry has been removed from the encyclopedia "
                            "since you bookmarked it.",
                missing=True,
            )
        if bookmark.entity_type == DISEASE:
            return BookmarkEntry(
                bookmark=bookmark,
                title=entry.name,
                subtitle=entry.scientific_name,
                description=entry.description,
                meta=f"Severity: {entry.severity}" if entry.severity else "",
            )
        if bookmark.entity_type == SYMPTOM:
            return BookmarkEntry(
                bookmark=bookmark,
                title=entry.name,
                subtitle=entry.scientific_name,
                description=entry.description,
                meta=f"{entry.tier_label} \u00b7 {entry.diagnostic_weight}/10",
            )
        return BookmarkEntry(
            bookmark=bookmark,
            title=entry.name,
            subtitle=entry.generic_label,
            description=", ".join(entry.indications[:3]),
            # category_display avoids .title() turning "OTC" into "Otc".
            meta=getattr(entry, "category_display", "") or entry.category_label,
        )