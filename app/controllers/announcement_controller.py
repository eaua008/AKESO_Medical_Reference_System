"""Announcements for the signed-in user: the pop-ups after signing in and
the dashboard's "Announcements" card.

Loads my_announcements() in the background shortly after the dashboard
appears. Each announcement this account has not closed yet pops up, one
after another (Critical first). Closing one, in any way, tells the server
so it never pops up again for this account; it stays on the dashboard
card until it ends. Returning to the dashboard checks again at most every
few minutes, so one published mid-session still arrives.
"""

import time
from typing import Optional

from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QApplication

from app.core.background import call_in_background
from app.models.announcement import Announcement
from app.repositories.announcement_repository import AnnouncementRepository
from app.ui.views.announcement_widgets import AnnouncementDialog, AnnouncementList

FIRST_CHECK_MS = 1500
RECHECK_SECONDS = 5 * 60


class AnnouncementController(QObject):
    def __init__(self, repository: AnnouncementRepository, card: AnnouncementList,
                 parent: Optional[QObject] = None) -> None:
        super().__init__(parent or card)
        self._repo = repository
        self._card = card
        self._items: list[Announcement] = []
        self._queue: list[Announcement] = []
        self._popped: set[str] = set()        # popped this session (even if dismiss failed)
        self._showing = False
        self._loaded_at = 0.0
        self._batch = (0, 0)                  # (shown, total) for "2 of 3"
        card.opened.connect(self._open)

    def start(self) -> None:
        QTimer.singleShot(FIRST_CHECK_MS, self.refresh)

    def dashboard_shown(self) -> None:
        if self._loaded_at and time.monotonic() - self._loaded_at >= RECHECK_SECONDS:
            self.refresh()

    def refresh(self) -> None:
        self._loaded_at = time.monotonic()
        # Failures stay quiet: announcements are never worth an error box.
        call_in_background(self._repo.mine, self._loaded, lambda _m: None, owner=self._card)

    # ------------------------------------------------------------ private

    def _loaded(self, items: list[Announcement]) -> None:
        self._items = items
        self._card.set_items(items)
        waiting = {i.id for i in self._queue}
        new = [i for i in items
               if not i.dismissed and i.id not in self._popped and i.id not in waiting]
        if new:
            shown, total = self._batch if (self._queue or self._showing) else (0, 0)
            self._batch = (shown, total + len(new))
            self._queue += new
        self._pop_next()

    def _pop_next(self) -> None:
        if self._showing or not self._queue:
            return
        window = self._card.window()
        # Wait for whatever else is on screen (sign-in steps, another dialog).
        if QApplication.activeModalWidget() is not None or not window.isVisible():
            QTimer.singleShot(1500, self._pop_next)
            return
        item = self._queue.pop(0)
        self._popped.add(item.id)
        shown, total = self._batch
        self._batch = (shown + 1, total)
        position = f"{shown + 1} of {total}" if total > 1 else ""
        self._showing = True
        try:
            AnnouncementDialog(item, parent=window, position=position).exec()
        finally:
            self._showing = False
        self._dismiss(item)
        QTimer.singleShot(250, self._pop_next)

    def _open(self, item: Announcement) -> None:
        """Clicked on the dashboard card."""
        AnnouncementDialog(item, parent=self._card.window()).exec()
        if not item.dismissed:
            self._dismiss(item)

    def _dismiss(self, item: Announcement) -> None:
        item.dismissed = True
        self._card.set_items(self._items)
        call_in_background(lambda: self._repo.dismiss(item.id), None, lambda _m: None,
                           owner=self._card)
