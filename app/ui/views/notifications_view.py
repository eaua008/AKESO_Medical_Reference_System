"""Notifications page: replies, best answers, reveals, moderation notices."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from app.models.exchange import Notification, time_ago
from app.ui.views.account.account_widgets import (
    Banner, button, icon_label, label, refresh_icons, repolish,
)
from app.ui.views.exchange.exchange_widgets import clear_layout


class NotificationRow(QFrame):
    clicked = Signal(object)

    def __init__(self, notification: Notification) -> None:
        super().__init__()
        self.setObjectName("exNotif")
        self.setProperty("unread", "false" if notification.read else "true")
        self.setCursor(Qt.CursorShape.PointingHandCursor if notification.post_id
                       else Qt.CursorShape.ArrowCursor)
        self._notification = notification
        row = QHBoxLayout(self)
        row.setContentsMargins(14, 10, 14, 10)
        row.setSpacing(12)
        row.addWidget(icon_label(notification.icon, 20), 0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(label(notification.kind_label.upper(), "acFieldLabel", wrap=False))
        text.addWidget(label(notification.message, "acRowTitle"))
        row.addLayout(text, 1)
        row.addWidget(label(time_ago(notification.created_at), "acSmall", wrap=False),
                      0, Qt.AlignmentFlag.AlignTop)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._notification)
        super().mouseReleaseEvent(event)


class NotificationsView(QWidget):
    open_requested = Signal(object)          # Notification
    mark_all_requested = Signal()
    clear_requested = Signal()
    more_requested = Signal()
    refresh_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        self._page = QVBoxLayout(page)
        self._page.setContentsMargins(30, 22, 30, 30)
        self._page.setSpacing(12)
        head = QHBoxLayout()
        text = QVBoxLayout()
        text.setSpacing(4)
        text.addWidget(label("Notifications", "acTitle"))
        self._summary = label("Replies, best answers and reveals on posts you follow.",
                              "acSubtitle")
        text.addWidget(self._summary)
        head.addLayout(text, 1)
        head.addWidget(button("Refresh", "acLink", on_click=self.refresh_requested.emit),
                       0, Qt.AlignmentFlag.AlignTop)
        head.addWidget(button("Mark all read", "acGhost", "check", self.mark_all_requested.emit),
                       0, Qt.AlignmentFlag.AlignTop)
        head.addWidget(button("Clear read", "acGhost", "trash-2", self.clear_requested.emit),
                       0, Qt.AlignmentFlag.AlignTop)
        self._page.addLayout(head)
        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        self._page.addWidget(self.banner)
        self._list = QVBoxLayout()
        self._list.setSpacing(8)
        self._page.addLayout(self._list)
        self._more = button("Show older", "acGhost", on_click=self.more_requested.emit)
        self._more.hide()
        self._page.addWidget(self._more, 0, Qt.AlignmentFlag.AlignHCenter)
        self._page.addStretch(1)
        scroll.setWidget(page)
        outer.addWidget(scroll)

    def show_notifications(self, items: list[Notification], append: bool, has_more: bool,
                           unread: int) -> None:
        if not append:
            clear_layout(self._list)
        if not items and not append:
            empty = label("You're all caught up. Follow a post in Clinical Exchange to hear "
                          "about replies.", "acMuted")
            self._list.addWidget(empty)
        for item in items:
            row = NotificationRow(item)
            row.clicked.connect(self.open_requested.emit)
            self._list.addWidget(row)
        self._more.setVisible(has_more)
        self._summary.setText(f"{unread} unread" if unread else
                              "Replies, best answers and reveals on posts you follow.")

    def mark_row_read(self, notification_id: int) -> None:
        for row in self.findChildren(NotificationRow):
            if row._notification.id == notification_id:
                row.setProperty("unread", "false")
                repolish(row)

    def show_error(self, message: str) -> None:
        clear_layout(self._list)
        self._list.addWidget(label(message, "acError"))

    def refresh_theme(self) -> None:
        refresh_icons(self)


__all__ = ["NotificationsView", "QLabel"]
