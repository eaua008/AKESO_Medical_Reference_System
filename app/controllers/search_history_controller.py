"""Search History: connects the page to SearchHistoryService.

Opening an entry is the shell's job (it knows every module), so this class
takes an open_entry callback instead of importing any other screen.
"""

from typing import Callable

from PySide6.QtCore import QObject

from app.models.search_history import HistoryEntry
from app.services.search_history_service import SearchHistoryService
from app.ui.views.account.account_dialogs import ConfirmDialog
from app.ui.views.search_history_view import SearchHistoryView


class SearchHistoryController(QObject):
    def __init__(self, view: SearchHistoryView, service: SearchHistoryService,
                 open_entry: Callable[[HistoryEntry], None]) -> None:
        super().__init__(view)
        self._view = view
        self._service = service
        self._open_entry = open_entry
        self._kind = "all"
        self._text = ""
        self._stale = True

        view.open_requested.connect(self._open)
        view.remove_requested.connect(self._remove)
        view.clear_requested.connect(self.clear)
        view.saving_requested.connect(self.set_saving)
        view.filter_changed.connect(self._filter)

    # -------------------------------------------------------------- public

    def mark_stale(self) -> None:
        """Something was recorded; redraw on the next visit, not now."""
        self._stale = True

    def refresh_if_stale(self) -> None:
        if self._stale:
            self.refresh()

    def refresh(self) -> None:
        self._stale = False
        rows = self._service.entries(self._kind, self._text)
        self._view.show_entries(self._service.grouped(rows), self._service.counts(),
                                self._service.saving_enabled())

    def clear(self) -> bool:
        """Ask, then forget every saved search. Returns True if cleared."""
        if not self._service.counts().get("all"):
            return False
        dialog = ConfirmDialog(
            "Clear search history?",
            "Every saved search on this computer for this account is removed. "
            "This can’t be undone.",
            "Clear history", "trash-2", danger=True, parent=self._view)
        if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
            return False
        self._service.clear()
        self.refresh()
        return True

    def set_saving(self, on: bool) -> None:
        self._service.set_saving(on)
        self.refresh()

    # ------------------------------------------------------------- private

    def _open(self, entry: HistoryEntry) -> None:
        self._open_entry(entry)

    def _remove(self, entry: HistoryEntry) -> None:
        self._service.remove(entry.id)
        self.refresh()

    def _filter(self, kind: str, text: str) -> None:
        self._kind, self._text = kind, text
        self.refresh()
