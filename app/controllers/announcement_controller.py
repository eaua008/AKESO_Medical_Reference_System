"""Announcements for the signed-in user: Notifications, the red badge on
the bell, the dashboard's "Announcements" card, and the sheet that opens
by itself for Critical ones.

Loads my_announcements() in the background shortly after the dashboard
appears, and again at most every few minutes (returning to the dashboard,
opening Notifications, or the bell's regular check), so one published
mid-session still arrives.

    unread   live announcements this account has not opened yet: they count
             on the bell's badge and show as unread in Notifications
    Critical ones open by themselves as a sheet, one after another; Info
             and Important ones wait in Notifications.
Opening one (or "Mark all read") tells the server, so it never counts as
unread again for this account; it stays listed until it ends.
"""

import time
from typing import Optional

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtWidgets import QApplication, QDialog

from app.core.background import call_in_background
from app.models.announcement import Announcement
from app.repositories.announcement_repository import AnnouncementRepository
from app.ui.views.announcement_widgets import AnnouncementDialog, AnnouncementList

FIRST_CHECK_MS = 1500
RECHECK_SECONDS = 5 * 60


class AnnouncementController(QObject):
    unread_changed = Signal(int)          # for the bell's badge
    items_changed = Signal(list)          # for the Notifications page

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

    def refresh_if_stale(self) -> None:
        """Notifications opened / the bell's regular check."""
        if not self._loaded_at or time.monotonic() - self._loaded_at >= RECHECK_SECONDS:
            self.refresh()

    @property
    def items(self) -> list[Announcement]:
        return list(self._items)

    @property
    def unread(self) -> int:
        return sum(1 for i in self._items if not i.dismissed)

    def open(self, item: Announcement) -> None:
        """Read one (from Notifications or the dashboard card)."""
        self._open(item)

    def hide(self, item: Announcement) -> None:
        """Delete from Notifications (and the dashboard card) for this account."""
        self._items = [i for i in self._items if i.id != item.id]
        self._queue = [i for i in self._queue if i.id != item.id]
        self._publish()
        call_in_background(lambda: self._repo.hide(item.id), None, lambda _m: None,
                           owner=self._card)

    def clear_read(self) -> None:
        """Notifications' "Clear read": drop every announcement already opened."""
        if not any(i.dismissed for i in self._items):
            return
        self._items = [i for i in self._items if not i.dismissed]
        self._publish()
        call_in_background(self._repo.hide_read, None, lambda _m: None, owner=self._card)

    def mark_all_read(self) -> None:
        for item in self._items:
            if not item.dismissed:
                self._dismiss(item, publish=False)
        self._publish()

    def refresh(self) -> None:
        self._loaded_at = time.monotonic()
        # Failures stay quiet: announcements are never worth an error box.
        call_in_background(self._repo.mine, self._loaded, lambda _m: None, owner=self._card)

    # ------------------------------------------------------------ private

    def _loaded(self, items: list[Announcement]) -> None:
        self._items = items
        self._publish()
        waiting = {i.id for i in self._queue}
        # Only Critical ones open by themselves; the rest wait in Notifications.
        new = [i for i in items
               if not i.dismissed and i.level == "critical"
               and i.id not in self._popped and i.id not in waiting]
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
        other_open = any(d.isVisible() for d in window.findChildren(QDialog))
        if QApplication.activeModalWidget() is not None or other_open or not window.isVisible():
            QTimer.singleShot(1500, self._pop_next)
            return
        item = self._queue.pop(0)
        self._popped.add(item.id)
        shown, total = self._batch
        self._batch = (shown + 1, total)
        position = f"{shown + 1} of {total}" if total > 1 else ""
        self._showing = True
        try:
            AnnouncementDialog(item, parent=self._card, position=position).exec()
        finally:
            self._showing = False
        self._dismiss(item)
        QTimer.singleShot(250, self._pop_next)

    def _open(self, item: Announcement) -> None:
        """Clicked in Notifications or on the dashboard card."""
        AnnouncementDialog(item, parent=self._card).exec()
        if not item.dismissed:
            self._dismiss(item)

    def _publish(self) -> None:
        self._card.set_items(self._items)
        self.items_changed.emit(self.items)
        self.unread_changed.emit(self.unread)

    def _dismiss(self, item: Announcement, publish: bool = True) -> None:
        item.dismissed = True
        if publish:
            self._publish()
        call_in_background(lambda: self._repo.dismiss(item.id), None, lambda _m: None,
                           owner=self._card)
