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
    QGridLayout,
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
        self._bookmark_btn.setIcon(
            QIcon(icons.to_pixmap(icons.star(15, color)))
        )
        self._bookmark_btn.setIconSize(QSize(15, 15))


class DiseaseEncyclopediaView(QWidget):
    """The condition directory: filter bar plus a grid of condition cards."""

    filters_changed = Signal()
    inspect_requested = Signal(str)
    bookmark_toggled = Signal(str, bool)
    refresh_requested = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")

        self._cards: list[ConditionCard] = []
        self._system_names: dict[str, str] = {}

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
        self._page_layout.setContentsMargins(32, 26, 32, 32)
        self._page_layout.setSpacing(18)

        self._page_layout.addLayout(self._build_header())
        self._page_layout.addWidget(self._build_filter_bar())
        self._page_layout.addWidget(self._build_grid_container(), 1)

        scroll.setWidget(page)
        root.addWidget(scroll)

    # -------------------------------------------------------------- header

    def _build_header(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(12)

        text_col = QVBoxLayout()
        text_col.setSpacing(4)

        title = QLabel("Clinical Condition Encyclopedia")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Browse peer-reviewed clinical summaries, pathophysiology, "
            "differential diagnoses, treatments, and prevention tiers"
        )
        subtitle.setObjectName("pageSubtitle")

        text_col.addWidget(title)
        text_col.addWidget(subtitle)

        self._count_badge = QLabel("0 conditions indexed")
        self._count_badge.setObjectName("countBadge")

        refresh = QPushButton("Refresh")
        refresh.setObjectName("secondaryButton")
        refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh.setToolTip("Re-read the encyclopedia from Supabase")
        refresh.clicked.connect(self.refresh_requested.emit)

        row.addLayout(text_col)
        row.addStretch(1)
        row.addWidget(refresh)
        row.addWidget(self._count_badge)
        return row

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
        self.search_input.textChanged.connect(self.filters_changed.emit)

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
        combo.currentIndexChanged.connect(self.filters_changed.emit)
        return combo

    # ---------------------------------------------------------------- grid

    def _build_grid_container(self) -> QWidget:
        container = QWidget()
        container.setObjectName("panel")

        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._grid_host = QWidget()
        self._grid_host.setObjectName("panel")
        self._grid = QGridLayout(self._grid_host)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setSpacing(18)
        self._grid.setAlignment(Qt.AlignmentFlag.AlignTop)

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
        """Rebuild the grid from a list of conditions."""
        self._clear_grid()

        for index, disease in enumerate(diseases):
            card = ConditionCard(
                disease,
                self._system_names.get(disease.body_system_id, "Unclassified"),
            )
            card.inspect_requested.connect(self.inspect_requested.emit)
            card.bookmark_toggled.connect(self.bookmark_toggled.emit)

            row, column = divmod(index, CARD_COLUMNS)
            self._grid.addWidget(card, row, column)
            self._cards.append(card)

        self._empty_label.setVisible(not diseases)
        self._grid_host.setVisible(bool(diseases))

        shown = len(diseases)
        overall = total if total is not None else shown
        self._count_badge.setText(
            f"{shown} of {overall} conditions indexed"
        )

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
        for card in self._cards:
            self._grid.removeWidget(card)
            card.deleteLater()
        self._cards.clear()