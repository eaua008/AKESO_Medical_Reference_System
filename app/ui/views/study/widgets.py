"""Small pieces shared by the Study Hub screens: the origin badge, a deck
tile (the whole tile is clickable), a clickable row, and a sync chip."""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.models.study import Deck, Origin
from app.services.study.study_service import DeckCounts
from app.ui.views.account.account_widgets import button, icon_label, label, repolish

ORIGIN_ICONS = {Origin.OFFICIAL: "badge-check", Origin.AUTO: "refresh-cw",
                Origin.PERSONAL: "user", Origin.SHARED: "users"}
SUBJECT_NAMES = {"anatomy": "Anatomy", "pathology": "Pathology", "pharmacology": "Pharmacology",
                 "microbiology": "Microbiology"}


def family_groups() -> list[tuple[str, list[str]]]:
    """The card kinds students filter by ("Dose calculation", "Tell them apart"),
    each with the template ids behind it (both red-flag templates are one kind)."""
    from app.services.study.auto_cards import TEMPLATE_NAMES
    groups: dict[str, list[str]] = {}
    for family, name in TEMPLATE_NAMES.items():
        groups.setdefault(name, []).append(family)
    return list(groups.items())


def origin_badge(deck: Deck) -> QWidget:
    """Official (check), Auto (sync), Student-made (author), Shared (people)."""
    holder = QFrame()
    holder.setObjectName("stBadge")
    holder.setProperty("origin", deck.origin.value)
    row = QHBoxLayout(holder)
    row.setContentsMargins(6, 1, 8, 1)
    row.setSpacing(4)
    row.addWidget(icon_label(ORIGIN_ICONS[deck.origin], 12))
    text = deck.label
    if deck.origin == Origin.PERSONAL and deck.owner_name:
        text += f" · {deck.owner_name}"
    caption = QLabel(text)
    caption.setObjectName("panel")
    caption.setStyleSheet("background: transparent; font-size: 11px; font-weight: 700;")
    row.addWidget(caption)
    return holder


class Clickable(QFrame):
    """A frame that acts like a button (the whole tile or row)."""

    clicked = Signal()

    def __init__(self, name: str) -> None:
        super().__init__()
        self.setObjectName(name)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.position().toPoint()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.clicked.emit()
            return
        super().keyPressEvent(event)


def counts_text(counts: DeckCounts) -> str:
    return f"{counts.new} new · {counts.due} due · {counts.learned} learned"


class DeckTile(Clickable):
    """A deck in the Decks tab. The whole tile opens it; Study starts at once.

    A coloured edge says the subject, the bar says how much is learned
    (green) and in progress, and the line under it says what is waiting."""

    open_requested = Signal(str)
    study_requested = Signal(str)

    def __init__(self, deck: Deck, counts: DeckCounts) -> None:
        super().__init__("stDeck")
        from app.ui.views.study.motion import HoverLift, MasteryBar, subject_colour
        self.deck = deck
        colour = subject_colour(deck.subject_id)
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        edge = QWidget()
        edge.setFixedWidth(5)
        edge.setStyleSheet(f"background-color: {colour}; border-top-left-radius: 12px; "
                           "border-bottom-left-radius: 12px;")
        outer.addWidget(edge)
        column = QVBoxLayout()
        column.setContentsMargins(14, 13, 14, 13)
        column.setSpacing(8)
        outer.addLayout(column, 1)
        top = QHBoxLayout()
        top.setSpacing(6)
        top.addWidget(origin_badge(deck))
        top.addStretch(1)
        top.addWidget(label(f"{counts.total} cards", "stCount", wrap=False))
        column.addLayout(top)
        shown = deck.title.replace(" (Auto)", "")
        for prefix in ("Pathology · ", "Pharmacology · "):
            if shown.startswith(prefix):
                shown = shown[len(prefix):]      # the shelf already says the subject
        title = label(shown, "stDeckTitle")
        title.setMinimumHeight(38)
        title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        column.addWidget(title)
        column.addWidget(MasteryBar(counts.learned, counts.learning, counts.total, colour))
        percent = round(100 * counts.learned / counts.total) if counts.total else 0
        bottom = QHBoxLayout()
        bottom.setSpacing(8)
        if counts.due:
            bottom.addWidget(label(f"{counts.due} due", "stCountDue", wrap=False))
        bottom.addWidget(label(f"{counts.new} new · {percent}% learned", "stCount", wrap=False))
        bottom.addStretch(1)
        study = button("Study" if counts.due or counts.new else "Review", "acPrimary" if counts.due else "acGhost",
                       "play", lambda: self.study_requested.emit(deck.id))
        study.setEnabled(counts.total > 0)
        study.setToolTip("Study this deck now")
        bottom.addWidget(study)
        column.addLayout(bottom)
        self.setToolTip(f"{deck.title}: click to see its cards")
        self.clicked.connect(lambda: self.open_requested.emit(deck.id))
        self._lift = HoverLift(self)


class RowItem(Clickable):
    """A list row: icon, title, a muted line, something on the right."""

    def __init__(self, icon: str, title: str, subtitle: str = "", right: str = "",
                 right_name: str = "stCount") -> None:
        super().__init__("stRow")
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 9, 12, 9)
        row.setSpacing(10)
        row.addWidget(icon_label(icon, 16), 0, Qt.AlignmentFlag.AlignVCenter)
        text = QVBoxLayout()
        text.setSpacing(1)
        head = label(title, "acRowTitle")
        head.setMinimumWidth(40)
        text.addWidget(head)
        if subtitle:
            sub = label(subtitle, "acSmall")
            sub.setMinimumWidth(40)
            text.addWidget(sub)
        row.addLayout(text, 1)
        if right:
            row.addWidget(label(right, right_name, wrap=False), 0, Qt.AlignmentFlag.AlignVCenter)


class SyncChip(QLabel):
    """Synced · Offline · Syncing · Sync error, like the notebook's line."""

    def __init__(self) -> None:
        super().__init__("Not synced yet")
        self.setObjectName("stSync")

    def set_status(self, text: str, tone: str = "") -> None:
        self.setText(text)
        self.setProperty("tone", tone)
        repolish(self)


def clear_layout(layout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        widget: Optional[QWidget] = item.widget()
        if widget is not None:
            widget.hide()                    # gone now, deleted when Qt is idle
            widget.deleteLater()
        elif item.layout() is not None:
            clear_layout(item.layout())
