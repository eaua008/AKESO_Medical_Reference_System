"""Notifications page and the unread badge on the header bell.

The count is checked once a minute (a desktop app without a live
connection), and right away after anything that may have changed it.
"""

from typing import Callable, Optional

from PySide6.QtCore import QObject, QTimer, Signal

from app.core.background import call_in_background
from app.models.exchange import Notification
from app.services.exchange_service import NotificationService
from app.ui.views.notifications_view import NotificationsView

POLL_INTERVAL_MS = 60_000
PAGE = 30


class NotificationsController(QObject):
    open_post = Signal(str)
    unread_changed = Signal(int)

    def __init__(self, view: NotificationsView, service: NotificationService) -> None:
        super().__init__(view)
        self._view = view
        self._service = service
        self._items: list[Notification] = []
        self._unread = 0

        view.open_requested.connect(self._open)
        view.delete_requested.connect(self._delete)
        view.mark_all_requested.connect(self._mark_all)
        view.clear_requested.connect(self._clear)
        view.more_requested.connect(self._more)
        view.refresh_requested.connect(self.reload)

        self._timer = QTimer(self)
        self._timer.setInterval(POLL_INTERVAL_MS)
        self._timer.timeout.connect(self.check_count)
        self._timer.start()
        QTimer.singleShot(1500, self.check_count)

    def _run(self, call: Callable, on_done: Optional[Callable] = None, quiet: bool = False) -> None:
        def failed(message: str) -> None:
            if not quiet:
                self._view.banner.show_message(message, "danger", "Dismiss")
        call_in_background(call, on_done, failed, owner=self._view)

    def check_count(self) -> None:
        self._run(self._service.unread_count, self._set_unread, quiet=True)

    def _set_unread(self, count: int) -> None:
        self._unread = int(count or 0)
        self.unread_changed.emit(self._unread)

    def reload(self) -> None:
        def done(items: list[Notification]) -> None:
            self._items = items
            self._view.show_notifications(items, False, len(items) >= PAGE,
                                          sum(1 for i in items if not i.read))
        self._run(self._service.latest, done)
        self.check_count()

    def _more(self) -> None:
        if not self._items:
            return
        before = self._items[-1].id

        def done(items: list[Notification]) -> None:
            self._items.extend(items)
            self._view.show_notifications(items, True, len(items) >= PAGE,
                                          sum(1 for i in self._items if not i.read))
        self._run(lambda: self._service.latest(before), done)

    def _open(self, notification: Notification) -> None:
        if not notification.read:
            self._run(lambda: self._service.mark_read([notification.id]),
                      lambda _r: self.check_count(), quiet=True)
            notification.read = True
            self._view.mark_row_read(notification.id)
        if notification.post_id:
            self.open_post.emit(notification.post_id)

    def _delete(self, notification: Notification) -> None:
        """The row's trash button (migration 016)."""
        self._items = [i for i in self._items if i.id != notification.id]
        self._view.remove_row(notification.id)
        self._run(lambda: self._service.delete([notification.id]),
                  lambda _r: self.check_count())

    def _mark_all(self) -> None:
        self._run(lambda: self._service.mark_read(None), lambda _r: self.reload())

    def _clear(self) -> None:
        self._run(self._service.clear_read, lambda _r: self.reload())

    def shutdown(self) -> None:
        self._timer.stop()
