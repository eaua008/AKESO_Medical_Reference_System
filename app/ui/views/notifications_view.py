"""Notifications page: announcements from the Akeso team, then replies,
best answers, reveals and moderation notices from Clinical Exchange."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from app.models.exchange import Notification, time_ago
from app.ui.views.account.account_widgets import (
    Banner, button, icon_label, label, refresh_icons, repolish,
)
from app.ui.views.exchange.exchange_widgets import clear_layout


def _delete_button(tooltip: str, on_click) -> QWidget:
    from app.ui.views.admin.admin_widgets import IconButton
    return IconButton("trash-2", tooltip, on_click=on_click)


DEFAULT_SUMMARY = ("Announcements from the Akeso team, and replies, best answers and "
                   "reveals on posts you follow.")


class NotificationRow(QFrame):
    clicked = Signal(object)
    delete_clicked = Signal(object)

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
        side = QVBoxLayout()
        side.setSpacing(4)
        side.addWidget(label(time_ago(notification.created_at), "acSmall", wrap=False),
                       0, Qt.AlignmentFlag.AlignRight)
        side.addWidget(_delete_button("Delete notification",
                                      lambda: self.delete_clicked.emit(self._notification)),
                       0, Qt.AlignmentFlag.AlignRight)
        side.addStretch(1)
        row.addLayout(side)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._notification)
        super().mouseReleaseEvent(event)


class AnnouncementRow(QFrame):
    """An announcement in the list (unread until opened)."""

    clicked = Signal(object)
    delete_clicked = Signal(object)

    def __init__(self, item) -> None:
        super().__init__()
        from app.models.announcement import LEVEL_ICONS, LEVEL_LABELS
        from app.ui.views.announcement_widgets import level_colour
        self.setObjectName("exNotif")
        self.setProperty("unread", "false" if item.dismissed else "true")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.item = item
        row = QHBoxLayout(self)
        row.setContentsMargins(14, 10, 14, 10)
        row.setSpacing(12)
        row.addWidget(icon_label(LEVEL_ICONS[item.level], 20, level_colour(item.level)),
                      0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(2)
        kind = "ANNOUNCEMENT" + ("" if item.level == "info"
                                 else f"  \u00b7  {LEVEL_LABELS[item.level].upper()}")
        text.addWidget(label(kind, "acFieldLabel", wrap=False))
        text.addWidget(label(item.title, "acRowTitle"))
        preview = " ".join(item.body.split())
        text.addWidget(label(preview[:160] + ("\u2026" if len(preview) > 160 else ""),
                             "acSmall"))
        row.addLayout(text, 1)
        side = QVBoxLayout()
        side.setSpacing(4)
        side.addWidget(label(time_ago(item.starts_at), "acSmall", wrap=False),
                       0, Qt.AlignmentFlag.AlignRight)
        side.addWidget(_delete_button("Delete from my notifications",
                                      lambda: self.delete_clicked.emit(self.item)),
                       0, Qt.AlignmentFlag.AlignRight)
        side.addStretch(1)
        row.addLayout(side)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.item)
        super().mouseReleaseEvent(event)


class NotificationsView(QWidget):
    open_requested = Signal(object)          # Notification
    delete_requested = Signal(object)        # Notification (trash button)
    announcement_delete_requested = Signal(object)  # Announcement
    announcement_requested = Signal(object)  # Announcement
    mark_all_requested = Signal()
    clear_requested = Signal()
    more_requested = Signal()
    refresh_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._exchange_unread = 0
        self._announce_unread = 0
        self._announcement_rows: list = []
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
        self._summary = label(DEFAULT_SUMMARY, "acSubtitle")
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
        self._announce_title = label("FROM THE AKESO TEAM", "acFieldLabel", wrap=False)
        self._announce_title.hide()
        self._page.addWidget(self._announce_title)
        self._announcements = QVBoxLayout()
        self._announcements.setSpacing(8)
        self._page.addLayout(self._announcements)
        self._list_title = label("CLINICAL EXCHANGE", "acFieldLabel", wrap=False)
        self._list_title.hide()
        self._page.addWidget(self._list_title)
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
            row.delete_clicked.connect(self.delete_requested.emit)
            self._list.addWidget(row)
        self._more.setVisible(has_more)
        self._exchange_unread = unread
        self._list_title.setVisible(bool(self._announcement_rows))
        self._update_summary()

    def show_announcements(self, items: list) -> None:
        clear_layout(self._announcements)
        self._announcement_rows = []
        for item in items:
            row = AnnouncementRow(item)
            row.clicked.connect(self.announcement_requested.emit)
            row.delete_clicked.connect(self.announcement_delete_requested.emit)
            self._announcements.addWidget(row)
            self._announcement_rows.append(row)
        self._announce_title.setVisible(bool(items))
        self._list_title.setVisible(bool(items))
        self._announce_unread = sum(1 for i in items if not i.dismissed)
        self._update_summary()

    def _update_summary(self) -> None:
        unread = self._exchange_unread + self._announce_unread
        self._summary.setText(f"{unread} unread" if unread else DEFAULT_SUMMARY)

    def remove_row(self, notification_id: int) -> None:
        for row in self.findChildren(NotificationRow):
            if row._notification.id == notification_id:
                if not row._notification.read:
                    self._exchange_unread = max(0, self._exchange_unread - 1)
                row.hide()
                row.deleteLater()
        self._update_summary()

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
