"""Emergency Guide: Philippine hotlines and first-aid protocols.

Display only. The controller hands it an EmergencyGuide and a list of
protocols to show; it announces filter text and does nothing else.

Scrolling: the whole page sits in one QScrollArea, so only the main content
area scrolls. The header and sidebar belong to DashboardShell and never move
or grow with this page, however long it gets.

Filtering hides and shows cards that were built once, instead of rebuilding
widgets on every keystroke.
"""

from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.models.emergency import EmergencyGuide, EmergencyProtocol, Hotline
# Reused rather than copied. If a third screen needs these, move them to
# app/ui/components/ so views stop importing from each other.
from app.ui.views.compare_view import FlowLayout, WrapChip

HOTLINE_COLUMNS = 3

# Shown if the data file fails to load. 911 must always be on screen.
FALLBACK_HOTLINE = Hotline(
    name="National Emergency Hotline",
    number="911",
    description="Police, fire, ambulance and disaster response. Free, nationwide.",
)

BADGE_OBJECTS = {
    "critical": "emBadgeCritical",
    "urgent": "emBadgeUrgent",
    "same_day": "emBadgeSameDay",
}


# ----------------------------------------------------------------- helpers

def _label(text: str, object_name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(object_name)
    label.setWordWrap(wrap)
    return label


def _selectable(label: QLabel) -> QLabel:
    """Phone numbers can be highlighted and copied."""
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    label.setCursor(Qt.CursorShape.IBeamCursor)
    return label


def _chip_flow(items: tuple[str, ...], object_name: str) -> QWidget:
    holder = QWidget()
    holder.setObjectName("panel")
    flow = FlowLayout()
    holder.setLayout(flow)
    for text in items:
        flow.addWidget(WrapChip(text, object_name))
    return holder


class _Icon(QLabel):
    """A drawn icon that knows how to redraw itself for the current theme."""

    def __init__(self, name: str, size: int, token: Optional[str], color: str = "") -> None:
        super().__init__()
        self.setObjectName("panel")
        self._name, self._size, self._token, self._color = name, size, token, color
        self.setFixedSize(size, size)
        self.refresh_theme()

    def refresh_theme(self) -> None:
        color = Theme.token(self._token) if self._token else self._color
        self.setPixmap(icons.to_pixmap(icons.draw(self._name, self._size, color)))


# ------------------------------------------------------------------ pieces

class HotlineCard(QFrame):
    """One secondary hotline in the grid."""

    def __init__(self, hotline: Hotline) -> None:
        super().__init__()
        self.setObjectName("emHotlineCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        layout.addWidget(_label(hotline.name, "emHotlineName"))
        layout.addWidget(_selectable(_label(hotline.number, "emHotlineNumber", wrap=False)))
        if hotline.alt_numbers:
            alt = _label(" \u00b7 ".join(hotline.alt_numbers), "emHotlineAlt")
            layout.addWidget(_selectable(alt))
        layout.addWidget(_label(hotline.description, "emHotlineDesc"))
        layout.addStretch(1)


class ProtocolCard(QFrame):
    """One first-aid protocol."""

    def __init__(self, protocol: EmergencyProtocol) -> None:
        super().__init__()
        self.setObjectName("emProtocolCard")
        self.protocol_id = protocol.id
        self._icons: list[_Icon] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(10)

        layout.addWidget(self._title_row(protocol))

        if protocol.warning_signs:
            layout.addWidget(_label("WARNING SIGNS", "emSectionLabel"))
            layout.addWidget(_chip_flow(protocol.warning_signs, "emWarningChip"))

        layout.addWidget(_label("WHAT TO DO", "emSectionLabel"))
        for number, text in enumerate(protocol.steps, start=1):
            layout.addWidget(self._step_row(number, text))

        if protocol.avoid:
            layout.addWidget(_label("AVOID", "emSectionLabel"))
            layout.addWidget(_chip_flow(protocol.avoid, "emAvoidChip"))

        if protocol.call_when:
            layout.addWidget(self._call_box(protocol.call_when))

        if protocol.source:
            layout.addWidget(_label(f"Source: {protocol.source}", "emSource"))

    def _title_row(self, protocol: EmergencyProtocol) -> QWidget:
        row = QWidget()
        row.setObjectName("panel")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        icon = _Icon("heart", 18, "DANGER")
        self._icons.append(icon)
        layout.addWidget(icon)
        layout.addWidget(_label(protocol.title, "emProtocolTitle", wrap=False))
        if protocol.local_name:
            layout.addWidget(_label(protocol.local_name, "emLocalName", wrap=False))
        layout.addStretch(1)

        badge = QLabel(protocol.urgency_label)
        badge.setObjectName(BADGE_OBJECTS.get(protocol.urgency, "emBadgeUrgent"))
        layout.addWidget(badge)
        return row

    @staticmethod
    def _step_row(number: int, text: str) -> QWidget:
        row = QWidget()
        row.setObjectName("panel")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        bubble = QLabel(str(number))
        bubble.setObjectName("emStepNumber")
        bubble.setFixedSize(24, 24)
        bubble.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body = _label(text, "emStepText")
        body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout.addWidget(bubble, 0, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(body, 1)
        return row

    def _call_box(self, text: str) -> QWidget:
        box = QFrame()
        box.setObjectName("emCallBox")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(3)

        head = QWidget()
        head.setObjectName("panel")
        head_layout = QHBoxLayout(head)
        head_layout.setContentsMargins(0, 0, 0, 0)
        head_layout.setSpacing(6)
        icon = _Icon("alert", 13, "DANGER")
        self._icons.append(icon)
        head_layout.addWidget(icon)
        head_layout.addWidget(_label("WHEN TO CALL 911", "emCallTitle", wrap=False))
        head_layout.addStretch(1)

        layout.addWidget(head)
        layout.addWidget(_label(text, "emCallText"))
        return box

    def set_focused(self, focused: bool) -> None:
        # A dynamic property switches the stylesheet rule; Qt only re-reads
        # property selectors after an unpolish/polish.
        self.setProperty("focused", focused)
        self.style().unpolish(self)
        self.style().polish(self)

    def refresh_theme(self) -> None:
        for icon in self._icons:
            icon.refresh_theme()


# -------------------------------------------------------------------- view

class EmergencyGuideView(QWidget):
    """The Emergency Guide page."""

    filter_changed = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")

        self._icons: list[_Icon] = []
        self._cards: dict[str, ProtocolCard] = {}
        self._total = 0

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll = scroll

        page = QWidget()
        page.setObjectName("panel")
        self._page = page
        self._page_layout = QVBoxLayout(page)
        self._page_layout.setContentsMargins(30, 22, 30, 30)
        self._page_layout.setSpacing(18)

        self._page_layout.addWidget(self._build_page_header())

        self._hero_host = QVBoxLayout()
        self._page_layout.addLayout(self._hero_host)

        self._page_layout.addWidget(self._section_heading("Other Philippine Hotlines", "bell"))
        self._hotline_host = QWidget()
        self._hotline_host.setObjectName("panel")
        self._hotline_grid = QGridLayout(self._hotline_host)
        self._hotline_grid.setContentsMargins(0, 0, 0, 0)
        self._hotline_grid.setSpacing(14)
        for column in range(HOTLINE_COLUMNS):
            self._hotline_grid.setColumnStretch(column, 1)
        self._page_layout.addWidget(self._hotline_host)

        self._local_note = _label("", "emLocalNote")
        self._page_layout.addWidget(self._local_note)

        self._page_layout.addWidget(self._build_protocol_bar())

        self._protocol_layout = QVBoxLayout()
        self._protocol_layout.setSpacing(16)
        self._page_layout.addLayout(self._protocol_layout)

        self._empty_label = _label("", "emEmpty")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.hide()
        self._page_layout.addWidget(self._empty_label)

        self._page_layout.addWidget(self._build_disclaimer())
        self._page_layout.addStretch(1)

        scroll.setWidget(page)
        root.addWidget(scroll)

        # 911 is visible before any data arrives, and stays if loading fails.
        self._set_hero(FALLBACK_HOTLINE, ())

    # ------------------------------------------------------------ builders

    def _build_page_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("panel")
        layout = QVBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        title_row = QWidget()
        title_row.setObjectName("panel")
        row = QHBoxLayout(title_row)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)
        icon = _Icon("alert", 24, "DANGER")
        self._icons.append(icon)
        row.addWidget(icon)
        row.addWidget(_label("Emergency Guide", "pageTitle", wrap=False))
        row.addStretch(1)

        layout.addWidget(title_row)
        layout.addWidget(
            _label(
                "Philippine emergency hotlines and first-aid steps based on "
                "DOH and Philippine Red Cross guidance.",
                "pageSubtitle",
            )
        )
        return header

    def _section_heading(self, text: str, icon_name: str) -> QWidget:
        row = QWidget()
        row.setObjectName("panel")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(8)
        icon = _Icon(icon_name, 16, "BADGE_TEXT")
        self._icons.append(icon)
        layout.addWidget(icon)
        layout.addWidget(_label(text, "emSectionHeading", wrap=False))
        layout.addStretch(1)
        return row

    def _build_protocol_bar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("panel")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(12)

        icon = _Icon("shield", 16, "BADGE_TEXT")
        self._icons.append(icon)
        layout.addWidget(icon)
        layout.addWidget(_label("First-Aid Protocols", "emSectionHeading", wrap=False))

        self._count_badge = QLabel("")
        self._count_badge.setObjectName("countBadge")
        layout.addWidget(self._count_badge)
        layout.addStretch(1)

        self.filter_input = QLineEdit()
        self.filter_input.setObjectName("filterSearch")
        self.filter_input.setPlaceholderText("Filter: CPR, paso, rabies, heat\u2026")
        self.filter_input.setFixedHeight(38)
        self.filter_input.setMinimumWidth(280)
        self.filter_input.setClearButtonEnabled(True)
        self.filter_input.textChanged.connect(self.filter_changed.emit)
        layout.addWidget(self.filter_input)
        return bar

    @staticmethod
    def _build_disclaimer() -> QWidget:
        box = QFrame()
        box.setObjectName("emDisclaimer")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.addWidget(
            _label(
                "Akeso is a study reference, not a substitute for hands-on "
                "training. The Philippine Red Cross runs first-aid and Basic "
                "Life Support courses nationwide.",
                "emDisclaimerText",
            )
        )
        return box

    def _set_hero(self, hotline: Hotline, tips: tuple[str, ...]) -> None:
        self._clear(self._hero_host)

        hero = QFrame()
        hero.setObjectName("emHero")
        layout = QHBoxLayout(hero)
        layout.setContentsMargins(26, 22, 26, 22)
        layout.setSpacing(26)

        left = QWidget()
        left.setObjectName("panel")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(2)
        left_layout.addWidget(_label(hotline.name.upper(), "emHeroKicker"))
        left_layout.addWidget(_selectable(_label(hotline.number, "emHeroNumber", wrap=False)))
        left_layout.addWidget(_label(hotline.description, "emHeroText"))
        left_layout.addStretch(1)
        layout.addWidget(left, 3)

        if tips:
            panel = QFrame()
            panel.setObjectName("emHeroTips")
            tips_layout = QVBoxLayout(panel)
            tips_layout.setContentsMargins(16, 14, 16, 14)
            tips_layout.setSpacing(6)
            tips_layout.addWidget(_label("WHEN YOU CALL", "emHeroKicker"))
            for number, tip in enumerate(tips, start=1):
                tips_layout.addWidget(_label(f"{number}.  {tip}", "emHeroTip"))
            tips_layout.addStretch(1)
            layout.addWidget(panel, 2)

        self._hero_host.addWidget(hero)

    # ---------------------------------------------------------- public API

    def set_guide(self, guide: EmergencyGuide) -> None:
        """Build the hotlines and every protocol card, once."""
        self._set_hero(guide.featured_hotline, guide.call_tips)

        self._clear(self._hotline_grid)
        for index, hotline in enumerate(guide.hotlines):
            row, column = divmod(index, HOTLINE_COLUMNS)
            self._hotline_grid.addWidget(HotlineCard(hotline), row, column)

        self._local_note.setText(guide.local_note)
        self._local_note.setVisible(bool(guide.local_note))

        for card in self._cards.values():
            self._protocol_layout.removeWidget(card)
            card.hide()
            card.deleteLater()
        self._cards = {}
        for protocol in guide.protocols:
            card = ProtocolCard(protocol)
            # Parented now, hidden until show_protocols() places it. Without a
            # parent, a card that never matches would float as its own window
            # if anything ever called show() on it.
            card.setParent(self._page)
            card.hide()
            self._cards[protocol.id] = card
        self._total = len(self._cards)

    def show_protocols(self, protocols: list[EmergencyProtocol]) -> None:
        """Show exactly these protocols, in this order."""
        # Detach every card, then re-add the matching ones in order. Cards are
        # kept alive in self._cards, so nothing is rebuilt.
        for card in self._cards.values():
            self._protocol_layout.removeWidget(card)
            card.hide()

        for protocol in protocols:
            card = self._cards.get(protocol.id)
            if card is not None:
                self._protocol_layout.addWidget(card)
                card.show()

        shown = len(protocols)
        self._count_badge.setText(
            f"{self._total} protocols" if shown == self._total else f"{shown} of {self._total}"
        )

        query = self.filter_input.text().strip()
        self._empty_label.setVisible(shown == 0)
        if shown == 0:
            self._empty_label.setText(
                f"No protocol matches \u201c{query}\u201d. In an emergency, call 911."
            )

    def focus_protocol(self, protocol_id: str) -> None:
        """Scroll to one card and highlight it briefly (used by global search)."""
        card = self._cards.get(protocol_id)
        if card is None:
            return
        # A leftover filter could be hiding the card. Clearing it emits
        # filter_changed, and the controller re-shows every card.
        if self.filter_input.text():
            self.filter_input.clear()

        # Wait one event-loop turn: the layout has to place the re-shown
        # cards before the card's position is known.
        QTimer.singleShot(0, lambda: self._scroll_to(card))

    def _scroll_to(self, card: "ProtocolCard") -> None:
        self._scroll.verticalScrollBar().setValue(max(card.y() - 16, 0))
        card.set_focused(True)
        QTimer.singleShot(1600, lambda: card.set_focused(False))

    def show_error(self, message: str) -> None:
        self._set_hero(FALLBACK_HOTLINE, ())
        self._count_badge.setText("")
        self._empty_label.setText(
            f"First-aid protocols couldn't be loaded ({message}). "
            "In an emergency, call 911."
        )
        self._empty_label.show()

    def refresh_theme(self) -> None:
        """Redraw painted icons; the stylesheet recolours everything else."""
        for icon in self._icons:
            icon.refresh_theme()
        for card in self._cards.values():
            card.refresh_theme()

    # ------------------------------------------------------------ internals

    @staticmethod
    def _clear(layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                # Hide first: deleteLater waits for the event loop, and until
                # then the widget would still be painted at its old spot.
                widget.hide()
                widget.deleteLater()