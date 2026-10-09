"""How announcements look: the pop-up and the dashboard list.

    AnnouncementDialog   the pop-up after signing in (also the admin preview)
    AnnouncementList     "Announcements" card on the dashboard, while any are live
"""

from typing import Optional

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.core.theme import Theme
from app.models.account import friendly_time
from app.models.announcement import (
    LEVEL_ICONS, LEVEL_LABELS, Announcement,
)
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import Card, icon_label, label, pill


def level_colour(level: str) -> Optional[str]:
    if level == "critical":
        return Theme.token("DANGER")
    if level == "important":
        return "#FBBF24" if Theme.mode() == "dark" else "#B45309"
    return None                                     # the theme's accent


# The announcement page is white with dark text in every theme.
INK = "#111827"
INK_SOFT = "#4B5563"
RULE = "#D1D5DB"
PAPER_BADGES = {                                   # background, text
    "info": ("#E0E7FF", "#3730A3"),
    "important": ("#FEF3C7", "#92400E"),
    "critical": ("#FEE2E2", "#991B1B"),
}


def _ink(text: str, size: int, colour: str = INK, weight: int = 400) -> QLabel:
    widget = QLabel(text)
    widget.setWordWrap(True)
    widget.setStyleSheet(f"color: {colour}; font-size: {size}px; font-weight: {weight}; "
                         "background: transparent;")
    return widget


class AnnouncementDialog(AccountDialog):
    """One announcement, as a white page over the module:

        TITLE
        FROM: AKESO TEAM  [IMPORTANT]  ·  Oct 6, 2026
        ─────────────────────────────────────────────
        the message

    Closing it in any way counts as "seen"."""

    def __init__(self, item: Announcement, parent: Optional[QWidget] = None,
                 position: str = "", preview: bool = False) -> None:
        super().__init__(item.title, "", LEVEL_ICONS.get(item.level, "info"), parent,
                         width=760, danger=item.level == "critical")
        self.setWindowTitle("Preview" if preview else "Announcement")
        self.make_paper()

        title = _ink(item.title, 34, INK, 600)
        title.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.body.addWidget(title)
        self.body.addSpacing(6)

        meta = QHBoxLayout()
        meta.setSpacing(10)
        sender = _ink("FROM: AKESO TEAM", 13, INK_SOFT, 600)
        sender.setWordWrap(False)
        meta.addWidget(sender)
        back, fore = PAPER_BADGES[item.level]
        badge = QLabel(LEVEL_LABELS[item.level].upper())
        badge.setStyleSheet(f"background-color: {back}; color: {fore}; font-size: 11px; "
                            "font-weight: 700; border-radius: 9px; padding: 2px 10px;")
        meta.addWidget(badge)
        if item.starts_at:
            meta.addWidget(_ink(f"\u00b7  {friendly_time(item.starts_at, False)}", 13,
                                INK_SOFT))
        meta.addStretch(1)
        if position:
            meta.addWidget(_ink(position, 13, INK_SOFT))                # "1 of 3"
        self.body.addLayout(meta)
        self.body.addSpacing(10)

        rule = QFrame()
        rule.setFixedHeight(1)
        rule.setStyleSheet(f"background-color: {RULE}; border: none;")
        self.body.addWidget(rule)
        self.body.addSpacing(10)

        text = _ink(item.body, 16, INK)
        text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text.setTextFormat(Qt.TextFormat.PlainText)                  # never HTML from the server
        self.body.addWidget(text)        # long messages scroll with the page
        if preview:
            self.body.addSpacing(16)
            self.body.addWidget(_ink("Preview: this is how users will see it. Nothing is "
                                     "published yet.", 13, INK_SOFT))

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
