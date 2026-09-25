"""Symptom Encyclopedia, directory screen.

Matches the reference build: entries carry an algorithmic weight badge and a
priority tier, and can be read either as cards or as the numbered 7-part
entry list.

Display only. It emits filter changes and clicks; the controller decides
what to show.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.models.symptom import Symptom
from app.ui.views.compare_view import FlowLayout, WrapChip

CARD_MIN_WIDTH = 330
MAX_COLUMNS = 3
CAUSES_ON_CARD = 3

# Tier colours, as in the reference build.
TIER_COLOURS = {
    "critical": "#F43F5E",
    "high": "#F59E0B",
    "moderate": "#6366F1",
    "mild": "#10B981",
}


def _label(text: str, name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(name)
    label.setWordWrap(wrap)
    return label


def _tier_label(text: str, tier_key: str, name: str = "syTierBadge") -> QLabel:
    """A badge coloured by tier. Property selectors keep it in the stylesheet."""
    badge = _label(text, name, wrap=False)
    badge.setProperty("tier", tier_key)
    return badge


def _shorten(text: str, limit: int = 155) -> str:
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "\u2026"


class SymptomCard(QFrame):
    """One entry as a card. The whole card is clickable."""

    clicked = Signal(str)

    def __init__(self, symptom: Symptom) -> None:
        super().__init__()
        self.setObjectName("syCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = symptom.id

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 14)
        layout.setSpacing(8)

        top = QHBoxLayout()
        # "1." is part 1 of the 7-part entry: body system classification.
        top.addWidget(_label(f"1. {symptom.system_label.upper()}", "sySystemChip", wrap=False))
        top.addStretch(1)
        top.addWidget(_tier_label(
            f"\u25cf  Weight: {symptom.diagnostic_weight}/10", symptom.tier_key))
        layout.addLayout(top)

        title = QHBoxLayout()
        title.setSpacing(8)
        title.addWidget(_label(symptom.name, "syCardTitle", wrap=False))
        if symptom.scientific_name:
            title.addWidget(_label(f"({symptom.scientific_name})", "syCardSci", wrap=False))
        title.addStretch(1)
        layout.addLayout(title)

        if symptom.description:
            layout.addWidget(_label(_shorten(symptom.description), "syCardBody"))

        if symptom.causes:
            layout.addWidget(_label("COMMON CAUSES", "sySectionLabel", wrap=False))
            holder = QWidget()
            holder.setObjectName("panel")
            flow = FlowLayout()
            holder.setLayout(flow)
            for cause in symptom.causes[:CAUSES_ON_CARD]:
                flow.addWidget(WrapChip(_shorten(cause, 44), "syChip"))
            extra = len(symptom.causes) - CAUSES_ON_CARD
            if extra > 0:
                flow.addWidget(WrapChip(f"+{extra} more", "syChipMore"))
            layout.addWidget(holder)

        layout.addStretch(1)

        line = QFrame()
        line.setObjectName("syCardDivider")
        line.setFixedHeight(1)
        layout.addWidget(line)

        footer = QHBoxLayout()
        if symptom.red_flags:
            footer.addWidget(_label(
                f"\u26a0  {len(symptom.red_flags)} Red Flags", "syFlagCount", wrap=False))
        footer.addStretch(1)
        footer.addWidget(_label("Inspect Entry  \u203a", "syLink", wrap=False))
        layout.addLayout(footer)

    def mouseReleaseEvent(self, event) -> None:
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._id)
        super().mouseReleaseEvent(event)


class SymptomEntryRow(QFrame):
    """One entry in "7-Part Entries" mode: the numbered parts, at a glance."""

    clicked = Signal(str)

    PARTS = ("Body system", "Nomenclature", "Weight", "Definition",
             "Causes", "Conditions", "Red flags")

    def __init__(self, symptom: Symptom, index: int) -> None:
        super().__init__()
        self.setObjectName("syRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = symptom.id

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        head = QHBoxLayout()
        head.setSpacing(10)
        head.addWidget(_label(f"{index:02d}", "syRowIndex", wrap=False))
        head.addWidget(_label(symptom.name, "syRowTitle", wrap=False))
        if symptom.scientific_name:
            head.addWidget(_label(f"({symptom.scientific_name})", "syCardSci", wrap=False))
        head.addStretch(1)
        head.addWidget(_tier_label(symptom.tier_label.upper(), symptom.tier_key))
        head.addWidget(_tier_label(
            f"{symptom.diagnostic_weight}/10", symptom.tier_key, "syWeightPill"))
        layout.addLayout(head)

        values = (
            symptom.system_label,
            symptom.scientific_name or "\u2014",
            f"{symptom.diagnostic_weight}/10",
            _shorten(symptom.description, 60),
            str(len(symptom.causes)),
            str(len(symptom.conditions)),
            str(len(symptom.red_flags)),
        )
        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(2)
        for column, (part, value) in enumerate(zip(self.PARTS, values)):
            grid.addWidget(_label(f"{column + 1}. {part.upper()}", "syPartLabel", wrap=False), 0, column)
            grid.addWidget(_label(value, "syPartValue"), 1, column)
            grid.setColumnStretch(column, 2 if part == "Definition" else 1)
        layout.addLayout(grid)

    def mouseReleaseEvent(self, event) -> None:
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._id)
        super().mouseReleaseEvent(event)


class CardGrid(QWidget):
    """Lays cards out in as many columns as fit, re-flowing on resize."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setSpacing(16)
        self._cards: list[QWidget] = []
        self._columns = 0

    def set_cards(self, cards: list[QWidget], columns: Optional[int] = None) -> None:
        for card in self._cards:
            self._grid.removeWidget(card)
            card.hide()
            card.deleteLater()
        self._cards = cards
        self._fixed_columns = columns
        self._columns = 0
        self._relayout()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._relayout()

    def _relayout(self) -> None:
        columns = getattr(self, "_fixed_columns", None) or max(
            1, min(MAX_COLUMNS, self.width() // CARD_MIN_WIDTH))
        if columns == self._columns:
            return
        self._columns = columns
        for card in self._cards:
            self._grid.removeWidget(card)
        for index, card in enumerate(self._cards):
            row, column = divmod(index, columns)
            self._grid.addWidget(card, row, column)
            card.show()
        for column in range(MAX_COLUMNS):
            self._grid.setColumnStretch(column, 1 if column < columns else 0)


class SymptomBrowseView(QWidget):
    filters_changed = Signal(str, str, str)   # query, body system id, tier key
    symptom_chosen = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._cards_mode = True
        self._symptoms: list[Symptom] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        page = QWidget()
        page.setObjectName("panel")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 22, 30, 30)
        layout.setSpacing(16)

        layout.addWidget(self._build_header())
        layout.addWidget(self._build_scope_note())
        layout.addWidget(self._build_filters())

        self.status = _label("", "syStatus")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.hide()
        layout.addWidget(self.status)

        self.grid = CardGrid()
        layout.addWidget(self.grid)
        layout.addStretch(1)

        scroll.setWidget(page)
        root.addWidget(scroll)

    # ------------------------------------------------------------ builders

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("panel")
        row = QHBoxLayout(header)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        self._icon = QLabel()
        self._icon.setObjectName("panel")
        self._icon.setFixedSize(26, 26)
        row.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignTop)

        text = QVBoxLayout()
        text.setSpacing(4)
        text.addWidget(_label("Symptom Reference Encyclopedia", "pageTitle", wrap=False))
        text.addWidget(_label(
            "Clinically structured 7-part reference entries: body system, "
            "nomenclature, algorithmic weight, definition, causes, linked "
            "conditions and emergency red flags.", "pageSubtitle"))
        row.addLayout(text, 1)

        # Cards / 7-Part Entries toggle
        toggle = QFrame()
        toggle.setObjectName("syToggle")
        toggle_row = QHBoxLayout(toggle)
        toggle_row.setContentsMargins(4, 4, 4, 4)
        toggle_row.setSpacing(2)
        self._view_group = QButtonGroup(self)
        self._view_group.setExclusive(True)
        for text_label, is_cards in (("Cards", True), ("7-Part Entries", False)):
            button = QPushButton(text_label)
            button.setObjectName("syToggleButton")
            button.setCheckable(True)
            button.setChecked(is_cards)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, cards=is_cards: self._set_mode(cards))
            self._view_group.addButton(button)
            toggle_row.addWidget(button)
        row.addWidget(toggle, 0, Qt.AlignmentFlag.AlignTop)

        self.count_badge = _label("", "countBadge", wrap=False)
        row.addWidget(self.count_badge, 0, Qt.AlignmentFlag.AlignTop)
        self.refresh_theme()
        return header

    @staticmethod
    def _build_scope_note() -> QWidget:
        box = QFrame()
        box.setObjectName("syScopeNote")
        layout = QHBoxLayout(box)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)
        layout.addWidget(_label("Clinical Scope Note:", "syScopeTitle", wrap=False))
        layout.addWidget(_label(
            "An educational reference. Entries follow WHO, CDC and standard "
            "textbook clinical documentation and do not replace professional "
            "medical evaluation.", "syScopeText"), 1)
        return box

    def _build_filters(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("syFilterBar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(14, 12, 14, 12)
        row.setSpacing(12)

        self.search = QLineEdit()
        self.search.setObjectName("filterSearch")
        self.search.setPlaceholderText(
            "Search common name, scientific name (e.g. Pyrexia), causes, or tags\u2026")
        self.search.setClearButtonEnabled(True)
        self.search.setFixedHeight(38)
        row.addWidget(self.search, 1)

        self.system = QComboBox()
        self.system.setObjectName("syCombo")
        self.system.setFixedHeight(38)
        self.system.setMinimumWidth(230)
        row.addWidget(self.system)

        self.tier = QComboBox()
        self.tier.setObjectName("syCombo")
        self.tier.setFixedHeight(38)
        self.tier.setMinimumWidth(230)
        row.addWidget(self.tier)

        self.search.textChanged.connect(self._emit_filters)
        self.system.currentIndexChanged.connect(self._emit_filters)
        self.tier.currentIndexChanged.connect(self._emit_filters)
        return bar

    def _emit_filters(self, *_args) -> None:
        self.filters_changed.emit(
            self.search.text(), self.system.currentData() or "", self.tier.currentData() or "")

    def _set_mode(self, cards: bool) -> None:
        self._cards_mode = cards
        self._render()

    # ---------------------------------------------------------- public API

    def set_body_systems(self, systems: list[tuple[str, str]]) -> None:
        current = self.system.currentData()
        self.system.blockSignals(True)
        self.system.clear()
        self.system.addItem(f"All Body Systems ({len(systems)})", "")
        for system_id, label in systems:
            self.system.addItem(label, system_id)
        index = self.system.findData(current)
        self.system.setCurrentIndex(index if index >= 0 else 0)
        self.system.blockSignals(False)

    def set_tiers(self, tiers: list[tuple[str, str]]) -> None:
        if self.tier.count():
            return
        self.tier.blockSignals(True)
        self.tier.addItem("All Algorithmic Weights", "")
        for key, label in tiers:
            self.tier.addItem(label, key)
        self.tier.blockSignals(False)

    def show_symptoms(self, symptoms: list[Symptom], total: int) -> None:
        self._symptoms = symptoms
        self.count_badge.setText(
            f"{total} Symptoms Cataloged" if len(symptoms) == total
            else f"{len(symptoms)} of {total} Entries")
        self._render()
        if total and not symptoms:
            self.show_status("No entry matches these filters.")
        elif total:
            self.status.hide()

    def _render(self) -> None:
        if self._cards_mode:
            widgets = [SymptomCard(s) for s in self._symptoms]
            columns = None
        else:
            widgets = [SymptomEntryRow(s, i) for i, s in enumerate(self._symptoms, start=1)]
            columns = 1
        for widget in widgets:
            widget.clicked.connect(self.symptom_chosen.emit)
        self.grid.set_cards(widgets, columns)

    def show_status(self, message: str) -> None:
        self.status.setText(message)
        self.status.show()

    def refresh_theme(self) -> None:
        self._icon.setPixmap(icons.to_pixmap(icons.draw("pulse", 26, Theme.token("PRIMARY"))))