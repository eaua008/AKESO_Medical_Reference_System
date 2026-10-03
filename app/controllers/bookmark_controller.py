"""Wires the Bookmarks page to BookmarkService.

Also the single place other modules report starring to: the shell connects
each encyclopedia's bookmark signal here, so no module has to know the
Bookmarks page exists.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.services.bookmark_service import BookmarkService
from app.ui.views.bookmarks_view import BookmarksView


class BookmarkController(QObject):
    # Re-emitted for the shell, which owns navigation between modules.
    open_requested = Signal(str, str)     # entity_type, entity_id

    def __init__(self, view: BookmarksView, service: BookmarkService) -> None:
        super().__init__()
        self._view = view
        self._service = service
        self._kind = ""

        view.kind_changed.connect(self._on_kind)
        view.remove_requested.connect(self._on_remove)
        view.open_requested.connect(self.open_requested.emit)
        self.reload()

    def reload(self) -> None:
        """Re-read from the store. Cheap: a single indexed query."""
        self._view.set_counts(self._service.counts())
        self._view.show_entries(self._service.entries(self._kind), self._kind)

    def _on_kind(self, kind: str) -> None:
        self._kind = kind
        self.reload()

    def _on_remove(self, entity_type: str, entity_id: str) -> None:
        self._service.set_bookmarked(entity_type, entity_id, False)
        self.reload()

    def set_bookmarked(self, entity_type: str, entity_id: str, state: bool) -> None:
        """Called when a star is pressed anywhere else in the app."""
        self._service.set_bookmarked(entity_type, entity_id, state)
        self.reload()