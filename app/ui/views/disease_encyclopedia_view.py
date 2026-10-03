"""Disease Encyclopedia — condition directory.

Display only. It renders whatever list of Disease objects it is handed and
announces what the user did. It does not import a service, does not know
Supabase exists, and does not filter anything itself — the controller asks
DiseaseService and calls set_diseases() with the result.

That split is why the same grid works unchanged against the JSON repository,
the Supabase repository, or a local cache.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.models_helpers import urgency_style  # see edits file
from app.core.theme import Theme
from app.ui.components.fluid import ResponsiveGrid, contain
from app.models.disease import BodySystem, Disease

CARD_COLUMNS = 3
CARD_MIN_WIDTH = 330


class ConditionCard(QFrame):
    """One condition tile in the directory grid."""

    inspect_requested = Signal(str)
    bookmark_toggled = Signal(str, bool)

    def __init__(
            self,
            disease: Disease,
            body_system_name: str,
            bookmarked: bool = False,
    ) -> None:
        super().__init__()
        self._disease = disease
        self._bookmarked = bookmarked

        self.setObjectName("conditionCard")
        self.setMinimumWidth(CARD_MIN_WIDTH)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 16)
        layout.setSpacing(10)

        layout.addLayout(self._build_chip_row(body_system_name))
        layout.addWidget(self._build_title())
        layout.addWidget(self._build_scientific_name())
        layout.addWidget(self._build_urgency_pill())
        layout.addWidget(self._build_description())
        layout.addStretch(1)
        layout.addWidget(self._build_divider())
        layout.addLayout(self._build_footer())

    # -------------------------------------------------------------- pieces

    def _build_chip_row(self, body_system_name: str) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(8)

        system_chip = QLabel(body_system_name.upper())
        system_chip.setObjectName("systemChip")

        entry_chip = QLabel("Clinical Entry")
        entry_chip.setObjectName("entryChip")

        self._bookmark_btn = QPushButton()
        self._bookmark_btn.setObjectName("bookmarkButton")
        self._bookmark_btn.setFixedSize(26, 26)
        self._bookmark_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bookmark_btn.clicked.connect(self._toggle_bookmark)
        self._refresh_bookmark_icon()

        row.addWidget(system_chip)
        row.addWidget(entry_chip)
        row.addStretch(1)
        row.addWidget(self._bookmark_btn)
        return row

    def _build_title(self) -> QLabel:
        label = QLabel(self._disease.name)
        label.setObjectName("cardConditionName")
        label.setWordWrap(True)
        return label

    def _build_scientific_name(self) -> QLabel:
        label = QLabel(self._disease.scientific_name or "\u2014")
        label.setObjectName("cardScientificName")
        label.setWordWrap(True)
        return label

    def _build_urgency_pill(self) -> QWidget:
        text, object_name = urgency_style(self._disease.urgency)

        pill = QLabel(text)
        pill.setObjectName(object_name)
        pill.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed
        )

        wrapper = QWidget()
        wrapper.setObjectName("panel")
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(pill)
        layout.addStretch(1)
        return wrapper

    def _build_description(self) -> QLabel:
        label = QLabel(self._disease.description)
        label.setObjectName("cardDescription")
        label.setWordWrap(True)
        label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        return label

    def _build_divider(self) -> QFrame:
        line = QFrame()
        line.setObjectName("separator")
        line.setFixedHeight(1)
        return line

    def _build_footer(self) -> QHBoxLayout:
        row = QHBoxLayout()

        severity = QLabel(self._disease.severity.upper())
        severity.setObjectName(f"severityChip{self._disease.severity}")

        inspect = QPushButton("Inspect Entry  \u203A")
        inspect.setObjectName("inspectLink")
        inspect.setCursor(Qt.CursorShape.PointingHandCursor)
        inspect.clicked.connect(
            lambda: self.inspect_requested.emit(self._disease.id)
        )

        row.addWidget(severity)
        row.addStretch(1)
        row.addWidget(inspect)
        return row

    # ----------------------------------------------------------- behaviour

    def _toggle_bookmark(self) -> None:
        self._bookmarked = not self._bookmarked
        self._refresh_bookmark_icon()
        self.bookmark_toggled.emit(self._disease.id, self._bookmarked)

    def _refresh_bookmark_icon(self) -> None:
        from PySide6.QtCore import QSize
        from PySide6.QtGui import QIcon

        color = (
            Theme.token("PRIMARY") if self._bookmarked
            else Theme.token("TEXT_MUTED")
        )
        # Solid when saved, outline when not: the fill is what reads as
        # "saved" at a glance, not the colour alone.
        glyph = icons.star_filled if self._bookmarked else icons.star
        self._bookmark_btn.setIcon(QIcon(icons.to_pixmap(glyph(15, color))))
        self._bookmark_btn.setIconSize(QSize(15, 15))


class ConditionEntryRow(QFrame):
    """One condition in "8-Part Entries" mode: every part, at a glance.

    The eight parts are the monograph's own sections, so the list is a map
    of what the detail page holds rather than a second design.
    """

    inspect_requested = Signal(str)

    PARTS = ("Body system", "Nomenclature", "Severity", "Urgency",
             "Summary", "Symptoms", "Medicines", "Red flags")

    def __init__(self, disease: Disease, system_name: str, index: int) -> None:
        super().__init__()
        self.setObjectName("conditionCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = disease.id

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        head = QHBoxLayout()
        head.setSpacing(10)

        number = QLabel(f"{index:02d}")
        number.setObjectName("cardScientificName")
        head.addWidget(number)

        name = QLabel(disease.name)
        name.setObjectName("cardConditionName")
        head.addWidget(name)

        if disease.scientific_name:
            scientific = QLabel(f"({disease.scientific_name})")
            scientific.setObjectName("cardScientificName")
            head.addWidget(scientific)

        head.addStretch(1)
        if disease.contagious:
            chip = QLabel("CONTAGIOUS")
            chip.setObjectName("contagiousChip")
            head.addWidget(chip)
        label, style = urgency_style(disease.urgency)
        pill = QLabel(label)
        pill.setObjectName(style)
        head.addWidget(pill)
        layout.addLayout(head)

        summary = disease.description or "No summary recorded yet."
        if len(summary) > 60:
            summary = summary[:60].rsplit(" ", 1)[0] + "\u2026"
        values = (
            system_name,
            disease.scientific_name or "\u2014",
            disease.severity or "\u2014",
            label,
            summary,
            str(len(disease.symptoms)),
            str(len(disease.medicines)),
            str(len(disease.emergency_warning_signs)),
        )

        # The eight parts sit in one row when there is room and reflow to two
        # rows of four on narrow windows (eight fixed columns needed ~960 px).
        # The list view calls self.parts.watch(viewport) once the row is placed.
        cells = []
        for column, (part, value) in enumerate(zip(self.PARTS, values)):
            cell = QWidget()
            cell.setObjectName("panel")
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setSpacing(2)
            caption = QLabel(f"{column + 1}. {part.upper()}")
            caption.setObjectName("subHeading")
            caption.setWordWrap(True)
            body = QLabel(value)
            body.setObjectName("bodyTextMuted")
            body.setWordWrap(True)
            cell_layout.addWidget(caption)
            cell_layout.addWidget(body)
            cell_layout.addStretch(1)
            cells.append(cell)
        self.parts = ResponsiveGrid(105, len(cells), spacing=14, steps=(8, 4, 2))
        self.parts.set_cards(cells)
        layout.addWidget(self.parts)

    def mouseReleaseEvent(self, event) -> None:
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.inspect_requested.emit(self._id)
        super().mouseReleaseEvent(event)


class DiseaseEncyclopediaView(QWidget):
    """The condition directory: filter bar plus a grid of condition cards."""

    filters_changed = Signal()
    inspect_requested = Signal(str)
    bookmark_toggled = Signal(str, bool)
    refresh_requested = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")

        self._cards: list[QWidget] = []
        self._system_names: dict[str, str] = {}
        self._diseases: list[Disease] = []
        self._cards_mode = True
        # Set by the shell: tells each card whether it is already starred.
        self.bookmark_lookup = None

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        page = QWidget()
        page.setObjectName("panel")
        self._page_layout = QVBoxLayout(page)
        self._page_layout.setContentsMargins(30, 18, 30, 30)
        self._page_layout.setSpacing(18)

        self._page_layout.addWidget(self._build_toolbar())
        self._page_layout.addWidget(self._build_filter_bar())
        self._page_layout.addWidget(self._build_grid_container(), 1)

        scroll.setWidget(page)
        self._grid_host.watch(scroll.viewport())
        contain(page, buttons=False)
        root.addWidget(scroll)

    # -------------------------------------------------------------- header

    def set_page_header(self, header: QWidget) -> None:
        """Put the page's title block at the top of this scrollable page."""
        self._page_layout.insertWidget(0, header)
        header.show()

    def take_page_header(self, header: QWidget) -> None:
        self._page_layout.removeWidget(header)

    def _build_toolbar(self) -> QWidget:
        """Just the refresh control now — the title moved to the page
        header so it can sit above the Directory / Compare tabs."""
        bar = QWidget()
        bar.setObjectName("panel")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)

        refresh = QPushButton("Refresh")
        refresh.setObjectName("secondaryButton")
        refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh.setToolTip("Re-read the encyclopedia from Supabase")
        refresh.clicked.connect(lambda _checked: self.refresh_requested.emit())
        layout.addWidget(refresh)
        return bar

    # ---------------------------------------------------------- filter bar

    def _build_filter_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("filterBar")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("filterSearch")
        self.search_input.setPlaceholderText(
            "Search condition, scientific name, or tag\u2026"
        )
        self.search_input.setFixedHeight(38)
        self.search_input.textChanged.connect(
            lambda _text: self.filters_changed.emit()
        )

        self.system_combo = self._combo("All Body Systems")
        self.severity_combo = self._combo("All Severities")
        self.urgency_combo = self._combo("All Urgency Levels")

        layout.addWidget(self.search_input, 2)
        layout.addWidget(self.system_combo, 1)
        layout.addWidget(self.severity_combo, 1)
        layout.addWidget(self.urgency_combo, 1)
        return bar

    def _combo(self, placeholder: str) -> QComboBox:
        combo = QComboBox()
        combo.setObjectName("filterCombo")
        combo.setFixedHeight(38)
        combo.setCursor(Qt.CursorShape.PointingHandCursor)
        # userData None means "no constraint" — the service treats it that way.
        combo.addItem(placeholder, None)
        combo.currentIndexChanged.connect(
            lambda _index: self.filters_changed.emit()
        )
        return combo

    # ---------------------------------------------------------------- grid

    def _build_grid_container(self) -> QWidget:
        container = QWidget()
        container.setObjectName("panel")

        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Up to three columns, fewer when the window is narrow: a fixed three
        # columns of 330 px cards forced the page wider than small screens.
        self._grid_host = ResponsiveGrid(CARD_MIN_WIDTH, CARD_COLUMNS, spacing=18)

        self._empty_label = QLabel("No conditions match those filters.")
        self._empty_label.setObjectName("cardSubtitle")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.hide()

        outer.addWidget(self._grid_host)
        outer.addWidget(self._empty_label)
        outer.addStretch(1)
        return container

    # ---------------------------------------------------------- public api

    def set_body_systems(self, systems: list[BodySystem]) -> None:
        """Fill the body system filter. Keeps the current choice if possible."""
        current = self.system_combo.currentData()

        self.system_combo.blockSignals(True)
        self.system_combo.clear()
        self.system_combo.addItem(f"All Body Systems ({len(systems)})", None)
        for system in systems:
            self.system_combo.addItem(system.name, system.id)
            self._system_names[system.id] = system.name

        index = self.system_combo.findData(current)
        if index >= 0:
            self.system_combo.setCurrentIndex(index)
        self.system_combo.blockSignals(False)

    def set_severities(self, severities: list[str]) -> None:
        self.severity_combo.blockSignals(True)
        self.severity_combo.clear()
        self.severity_combo.addItem("All Severities", None)
        for severity in severities:
            self.severity_combo.addItem(severity, severity)
        self.severity_combo.blockSignals(False)

    def set_urgencies(self, urgencies: list[str]) -> None:
        self.urgency_combo.blockSignals(True)
        self.urgency_combo.clear()
        self.urgency_combo.addItem("All Urgency Levels", None)
        for urgency in urgencies:
            label, _ = urgency_style(urgency)
            self.urgency_combo.addItem(label, urgency)
        self.urgency_combo.blockSignals(False)

    def set_diseases(
            self, diseases: list[Disease], total: Optional[int] = None
    ) -> None:
        """Rebuild the directory from a list of conditions."""
        self._diseases = diseases
        self._render()

    def set_display_mode(self, cards: bool) -> None:
        """Cards, or the numbered 8-part entry list."""
        if cards == self._cards_mode:
            return
        self._cards_mode = cards
        self._render()

    def _render(self) -> None:
        self._clear_grid()
        cards: list[QWidget] = []
        for index, disease in enumerate(self._diseases):
            system_name = self._system_names.get(
                disease.body_system_id, "Unclassified")
            if self._cards_mode:
                starred = bool(self.bookmark_lookup(disease.id)) \
                    if self.bookmark_lookup else False
                card = ConditionCard(disease, system_name, bookmarked=starred)
                card.bookmark_toggled.connect(self.bookmark_toggled.emit)
            else:
                card = ConditionEntryRow(disease, system_name, index + 1)
            card.inspect_requested.connect(self.inspect_requested.emit)
            if hasattr(card, "parts"):
                card.parts.watch(self._grid_host.viewport())
            contain(card, limit=CARD_MIN_WIDTH - 60)
            cards.append(card)
        self._cards = cards
        # Cards mode: as many columns as fit. List mode: always one.
        self._grid_host.set_cards(cards, None if self._cards_mode else 1)

        self._empty_label.setVisible(not self._diseases)
        self._grid_host.setVisible(bool(self._diseases))

    def filter_state(self) -> dict:
        """What the controller passes to DiseaseService.search()."""
        return {
            "query": self.search_input.text().strip(),
            "body_system_id": self.system_combo.currentData(),
            "severity": self.severity_combo.currentData(),
            "urgency": self.urgency_combo.currentData(),
        }

    def show_error(self, message: str) -> None:
        self._clear_grid()
        self._empty_label.setText(message)
        self._empty_label.show()
        self._grid_host.hide()

    # ------------------------------------------------------------ internal

    def _clear_grid(self) -> None:
        # ResponsiveGrid hides the old cards before deleting them, so they
        # are not painted behind the new ones while deleteLater waits.
        self._grid_host.set_cards([])
        self._cards = []