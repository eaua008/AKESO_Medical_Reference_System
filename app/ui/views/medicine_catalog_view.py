"""Medicine Reference, catalogue screen.

Cards carry the regulatory badge, the black-box flag, the drug class, the
Philippine and international brands, and the primary uses. A toggle switches
between the cards and the 8-part structured list.

Display only: it emits filter changes and clicks.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.models.medicine import MedicineMonograph
from app.services.medicine_service import SCOPES

CARD_MIN_WIDTH = 360
MAX_COLUMNS = 3


def _label(text: str, name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(name)
    label.setWordWrap(wrap)
    return label


def _rich(caption: str, value: str, name: str = "mdBody") -> QLabel:
    """A bold caption followed by normal text, in one wrapped line."""
    label = QLabel(f"<b>{caption}</b> {value}")
    label.setObjectName(name)
    label.setWordWrap(True)
    label.setTextFormat(Qt.TextFormat.RichText)
    return label


def _shorten(text: str, limit: int = 150) -> str:
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "\u2026"


class MedicineCard(QFrame):
    """One formulation as a card. Clicking anywhere opens the monograph."""

    clicked = Signal(str)

    def __init__(self, medicine: MedicineMonograph) -> None:
        super().__init__()
        self.setObjectName("mdCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._medicine = medicine

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 14)
        layout.setSpacing(8)

        top = QHBoxLayout()
        badge = _label(medicine.category_label, "mdCategoryBadge", wrap=False)
        badge.setProperty("category", medicine.category_key)
        top.addWidget(badge)
        top.addStretch(1)
        if medicine.has_black_box:
            top.addWidget(_label("\u26a0  BLACK BOX WARNING", "mdBlackBoxBadge", wrap=False))
        layout.addLayout(top)

        layout.addWidget(_label(medicine.name, "mdCardTitle"))
        if medicine.drug_class:
            layout.addWidget(_rich("Class:", medicine.drug_class, "mdCardClass"))
        layout.addWidget(_label(f"Generic: {medicine.generic_label}", "mdCardGeneric"))

        if medicine.ph_brands or medicine.intl_brands:
            brands = QFrame()
            brands.setObjectName("mdBrandBox")
            brand_layout = QVBoxLayout(brands)
            brand_layout.setContentsMargins(14, 10, 14, 10)
            brand_layout.setSpacing(4)
            if medicine.ph_brands:
                brand_layout.addWidget(
                    _rich("Philippine Brands:", ", ".join(medicine.ph_brands), "mdBrandPh"))
            if medicine.intl_brands:
                brand_layout.addWidget(
                    _rich("Int'l Brands:", ", ".join(medicine.intl_brands), "mdBrandIntl"))
            layout.addWidget(brands)

        if medicine.indications:
            layout.addWidget(_rich("Primary Uses:",
                                   _shorten("; ".join(medicine.indications), 170), "mdUses"))
        layout.addStretch(1)

        line = QFrame()
        line.setObjectName("mdCardDivider")
        line.setFixedHeight(1)
        layout.addWidget(line)

        footer = QHBoxLayout()
        self._copy = QPushButton("Copy Entry")
        self._copy.setObjectName("mdCopyLink")
        self._copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self._copy.clicked.connect(self._copy_entry)
        footer.addWidget(self._copy)
        footer.addStretch(1)
        footer.addWidget(_label("Inspect Entry  \u203a", "mdLink", wrap=False))
        layout.addLayout(footer)

    def _copy_entry(self) -> None:
        QApplication.clipboard().setText(self._medicine.as_text())
        self._copy.setText("Copied")

    def mouseReleaseEvent(self, event) -> None:
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._medicine.id)
        super().mouseReleaseEvent(event)


class MedicineEntryRow(QFrame):
    """One formulation in "8-Part Structured View": every part, at a glance."""

    clicked = Signal(str)

    PARTS = ("Class", "Nomenclature", "Indications", "Dosage",
             "Adverse", "Contraindications", "Interactions", "References")

    def __init__(self, medicine: MedicineMonograph, index: int) -> None:
        super().__init__()
        self.setObjectName("mdRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = medicine.id

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        head = QHBoxLayout()
        head.setSpacing(10)
        head.addWidget(_label(f"{index:02d}", "mdRowIndex", wrap=False))
        head.addWidget(_label(medicine.name, "mdRowTitle", wrap=False))
        head.addWidget(_label(f"({medicine.generic_label})", "mdCardGeneric", wrap=False))
        head.addStretch(1)
        if medicine.has_black_box:
            head.addWidget(_label("BLACK BOX", "mdBlackBoxBadge", wrap=False))
        badge = _label(medicine.category_label, "mdCategoryBadge", wrap=False)
        badge.setProperty("category", medicine.category_key)
        head.addWidget(badge)
        layout.addLayout(head)

        values = (
            medicine.drug_class or "\u2014",
            f"{len(medicine.ph_brands)} PH / {len(medicine.intl_brands)} int'l brands",
            str(len(medicine.indications)),
            _shorten(medicine.dosage_text, 40) or "\u2014",
            str(len(medicine.adverse_reactions)),
            str(len(medicine.contraindications)),
            str(len(medicine.interactions)),
            str(len(medicine.references)),
        )
        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(2)
        for column, (part, value) in enumerate(zip(self.PARTS, values)):
            grid.addWidget(_label(f"{column + 1}. {part.upper()}", "mdPartLabel", wrap=False),
                           0, column)
            grid.addWidget(_label(value, "mdPartValue"), 1, column)
            grid.setColumnStretch(column, 2 if part in ("Class", "Dosage") else 1)
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
        self._fixed_columns: Optional[int] = None

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
        columns = self._fixed_columns or max(
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


class MedicineCatalogView(QWidget):
    filters_changed = Signal(str, str, str)   # query, regulatory class, scope
    medicine_chosen = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._cards_mode = True
        self._medicines: list[MedicineMonograph] = []

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
        layout.addWidget(self._build_filters())

        self.status = _label("", "mdStatus")
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
        text.addWidget(_label("Pharmaceutical Medicine Reference", "pageTitle", wrap=False))
        text.addWidget(_label(
            "Structured 8-part clinical monographs for educational reference "
            "and pharmacovigilance.", "pageSubtitle"))
        row.addLayout(text, 1)

        toggle = QFrame()
        toggle.setObjectName("mdToggle")
        toggle_row = QHBoxLayout(toggle)
        toggle_row.setContentsMargins(4, 4, 4, 4)
        toggle_row.setSpacing(2)
        self._view_group = QButtonGroup(self)
        self._view_group.setExclusive(True)
        for text_label, is_cards in (("Catalog Cards", True), ("8-Part Structured View", False)):
            button = QPushButton(text_label)
            button.setObjectName("mdToggleButton")
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

    def _build_filters(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("mdFilterBar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(14, 12, 14, 12)
        row.setSpacing(12)

        self.search = QLineEdit()
        self.search.setObjectName("filterSearch")
        self.search.setPlaceholderText(
            "Search paracetamol, amlodipine, metformin, Ventolin, PPI\u2026")
        self.search.setClearButtonEnabled(True)
        self.search.setFixedHeight(38)
        row.addWidget(self.search, 1)

        self.regulatory = QComboBox()
        self.regulatory.setObjectName("mdCombo")
        self.regulatory.setFixedHeight(38)
        self.regulatory.setMinimumWidth(230)
        row.addWidget(self.regulatory)

        # Which fields the search looks at.
        scope_box = QFrame()
        scope_box.setObjectName("mdToggle")
        scope_layout = QHBoxLayout(scope_box)
        scope_layout.setContentsMargins(4, 4, 4, 4)
        scope_layout.setSpacing(2)
        self._scope_group = QButtonGroup(self)
        self._scope_group.setExclusive(True)
        self._scope = "all"
        for key, label in SCOPES:
            button = QPushButton(label)
            button.setObjectName("mdToggleButton")
            button.setCheckable(True)
            button.setChecked(key == "all")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, k=key: self._set_scope(k))
            self._scope_group.addButton(button)
            scope_layout.addWidget(button)
        row.addWidget(scope_box)

        self.search.textChanged.connect(self._emit_filters)
        self.regulatory.currentIndexChanged.connect(self._emit_filters)
        return bar

    def _set_scope(self, key: str) -> None:
        self._scope = key
        self._emit_filters()

    def _emit_filters(self, *_args) -> None:
        self.filters_changed.emit(
            self.search.text(), self.regulatory.currentData() or "", self._scope)

    def _set_mode(self, cards: bool) -> None:
        self._cards_mode = cards
        self._render()

    # ---------------------------------------------------------- public API

    def set_regulatory_classes(self, classes: list[tuple[str, str]]) -> None:
        current = self.regulatory.currentData()
        self.regulatory.blockSignals(True)
        self.regulatory.clear()
        self.regulatory.addItem("All Regulatory Classes", "")
        for key, label in classes:
            self.regulatory.addItem(label, key)
        index = self.regulatory.findData(current)
        self.regulatory.setCurrentIndex(index if index >= 0 else 0)
        self.regulatory.blockSignals(False)

    def show_medicines(self, medicines: list[MedicineMonograph], total: int) -> None:
        self._medicines = medicines
        self.count_badge.setText(
            f"{total} Formulations" if len(medicines) == total
            else f"{len(medicines)} of {total}")
        self._render()
        if total and not medicines:
            self.show_status("No formulation matches these filters.")
        elif total:
            self.status.hide()

    def _render(self) -> None:
        if self._cards_mode:
            widgets = [MedicineCard(m) for m in self._medicines]
            columns = None
        else:
            widgets = [MedicineEntryRow(m, i) for i, m in enumerate(self._medicines, start=1)]
            columns = 1
        for widget in widgets:
            widget.clicked.connect(self.medicine_chosen.emit)
        self.grid.set_cards(widgets, columns)

    def show_status(self, message: str) -> None:
        self.status.setText(message)
        self.status.show()

    def refresh_theme(self) -> None:
        self._icon.setPixmap(icons.to_pixmap(icons.draw("pill", 26, Theme.token("PRIMARY"))))