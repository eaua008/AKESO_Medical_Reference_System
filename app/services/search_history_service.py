"""Search History rules: what gets remembered, and how the list is shown.

Pure logic over LocalHistoryStore, so it can be tested without widgets.
"""

from typing import Optional

from app.models.search_history import KIND_LABELS, HistoryEntry
from app.repositories.local_history_store import LocalHistoryStore


class SearchHistoryService:
    def __init__(self, owner: str, store: Optional[LocalHistoryStore] = None) -> None:
        self._owner = owner
        self._store = store or LocalHistoryStore()

    # ------------------------------------------------------------- record

    def record(self, kind: str, target_id: str, title: str, subtitle: str = "",
               icon: str = "", query: str = "") -> bool:
        """Remember one opened result. Returns False when saving is off
        (or the kind is unknown), so nothing was written."""
        if kind not in KIND_LABELS or not target_id or not self.saving_enabled():
            return False
        self._store.add(self._owner, kind, target_id, title, subtitle, icon, query)
        return True

    # --------------------------------------------------------------- read

    def entries(self, kind: str = "all", text: str = "") -> list[HistoryEntry]:
        """Newest first, filtered by kind and by words in the title,
        subtitle or the words typed."""
        rows = self._store.list_for(self._owner)
        if kind != "all":
            rows = [r for r in rows if r.kind == kind]
        needle = text.strip().lower()
        if needle:
            rows = [r for r in rows
                    if needle in r.title.lower() or needle in r.subtitle.lower()
                    or needle in r.query.lower()]
        return rows

    def counts(self) -> dict[str, int]:
        rows = self._store.list_for(self._owner)
        counts = {"all": len(rows)}
        for row in rows:
            counts[row.kind] = counts.get(row.kind, 0) + 1
        return counts

    @staticmethod
    def grouped(rows: list[HistoryEntry]) -> list[tuple[str, list[HistoryEntry]]]:
        """[(day label, entries)] in the order given (newest first)."""
        groups: list[tuple[str, list[HistoryEntry]]] = []
        for row in rows:
            label = row.day_label()
            if groups and groups[-1][0] == label:
                groups[-1][1].append(row)
            else:
                groups.append((label, [row]))
        return groups

    # -------------------------------------------------------------- write

    def remove(self, entry_id: int) -> None:
        self._store.remove(self._owner, entry_id)

    def clear(self) -> int:
        return self._store.clear(self._owner)

    def saving_enabled(self) -> bool:
        return self._store.saving_enabled(self._owner)

    def set_saving(self, on: bool) -> None:
        self._store.set_saving(self._owner, on)
