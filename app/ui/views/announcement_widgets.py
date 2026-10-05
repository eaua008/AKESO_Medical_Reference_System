"""How announcements look: the pop-up and the dashboard list.

    AnnouncementDialog   the pop-up after signing in (also the admin preview)
    AnnouncementList     "Announcements" card on the dashboard, while any are live
"""

from typing import Optional

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from app.core.theme import Theme
from app.models.account import friendly_time
from app.models.announcement import (
    LEVEL_ICONS, LEVEL_LABELS, LEVEL_PILLS, Announcement,
)
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import Card, icon_label, label, pill


def level_colour(level: str) -> Optional[str]:
    if level == "critical":
        return Theme.token("DANGER")
    if level == "important":
        return "#FBBF24" if Theme.mode() == "dark" else "#B45309"
    return None                                     # the theme's accent


class AnnouncementDialog(AccountDialog):
    """One announcement. Closing it in any way counts as "seen"."""

    def __init__(self, item: Announcement, parent: Optional[QWidget] = None,
                 position: str = "", preview: bool = False) -> None:
        super().__init__(item.title, "", LEVEL_ICONS.get(item.level, "info"), parent,
                         width=540, danger=item.level == "critical")
        self.setWindowTitle("Preview" if preview else "Announcement")
        meta = QHBoxLayout()
        meta.setSpacing(8)
        meta.addWidget(pill(LEVEL_LABELS[item.level].upper(), LEVEL_PILLS[item.level]))
        meta.addWidget(label("From the Akeso team"
                             + (f"  ·  {friendly_time(item.starts_at, False)}"
                                if item.starts_at else ""), "acSmall", wrap=False))
        meta.addStretch(1)
        if position:
            meta.addWidget(label(position, "acSmall", wrap=False))   # "1 of 3"
        self.body.addLayout(meta)

        text = label(item.body, "acValue")
        text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text.setTextFormat(Qt.TextFormat.PlainText)                  # never HTML from the server
        if len(item.body) > 600:
            # Long messages scroll inside the pop-up instead of growing past the screen.
            box = QScrollArea()
            box.setWidgetResizable(True)
            box.setFrameShape(QFrame.Shape.NoFrame)
            box.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            holder = QWidget()
            holder.setObjectName("panel")
            inner = QVBoxLayout(holder)
            inner.setContentsMargins(0, 0, 8, 0)
            inner.addWidget(text)
            box.setWidget(holder)
            box.setFixedHeight(320)
            self.body.addWidget(box)
        else:
            self.body.addWidget(text)
        if preview:
            self.body.addWidget(label("Preview: this is how users will see it. Nothing is "
                                      "published yet.", "acSmall"))

        if item.link_url:
            url = item.link_url
            self.add_button(item.button_text, "acGhost", "external-link",
                            lambda: QDesktopServices.openUrl(QUrl(url)))
        self.add_button("Close preview" if preview else "Got it", "acPrimary", "check",
                        self.accept, default=True)


class _Row(QFrame):
    clicked = Signal(object)

    def __init__(self, item: Announcement) -> None:
        super().__init__()
        self.setObjectName("acRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._item = item
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 10, 12, 10)
        row.setSpacing(10)
        row.addWidget(icon_label(LEVEL_ICONS[item.level], 16, level_colour(item.level)),
                      0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(label(item.title, "acRowTitle"))
        preview = " ".join(item.body.split())
        text.addWidget(label(preview[:140] + ("…" if len(preview) > 140 else ""),
                             "acSmall"))
        row.addLayout(text, 1)
        if not item.dismissed:
            row.addWidget(pill("NEW", "acPillGood"), 0, Qt.AlignmentFlag.AlignTop)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._item)
        super().mouseReleaseEvent(event)


class AnnouncementList(Card):
    """The dashboard's "Announcements" card. Hidden when nothing is live."""

    opened = Signal(object)          # Announcement

    def __init__(self) -> None:
        super().__init__("Announcements", "From the Akeso team. Click one to read it.",
                         "megaphone")
        self._rows = QVBoxLayout()
        self._rows.setSpacing(6)
        self.body.addLayout(self._rows)
        self.hide()

    def set_items(self, items: list[Announcement]) -> None:
        while self._rows.count():
            widget = self._rows.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()
        for item in items:
            row = _Row(item)
            row.clicked.connect(self.opened.emit)
            self._rows.addWidget(row)
        self.setVisible(bool(items))
