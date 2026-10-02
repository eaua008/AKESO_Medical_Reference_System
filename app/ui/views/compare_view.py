"""Compare Conditions — differential analysis workstation.

Display only. The controller hands it a Comparison and it renders. It does no
set arithmetic and writes no clinical text.

Everything shown is recorded data. Where the page states a contrast, it is
reporting stored values, not generating a clinical claim — which is why the
synthesis banner says what it says.
"""

from typing import Optional

from PySide6.QtCore import QPoint, QRect, QSize, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.models.disease import Disease
from app.services.comparison import Comparison, SharedSymptom

MAX_CONDITIONS = 3


def _card(object_name: str = "detailCard") -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setObjectName(object_name)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(20, 18, 20, 18)
    layout.setSpacing(12)
    return frame, layout


def _label(text: str, object_name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(object_name)
    label.setWordWrap(wrap)
    return label


def _chip(text: str, object_name: str) -> QLabel:
    chip = QLabel(text)
    chip.setObjectName(object_name)
    chip.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
    return chip


def _heading(text: str, icon_name: str, color: Optional[str] = None) -> QWidget:
    row = QWidget()
    row.setObjectName("panel")
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)

    glyph = QLabel()
    glyph.setObjectName("panel")
    glyph.setPixmap(
        icons.to_pixmap(
            icons.draw(icon_name, 14, color or Theme.token("BADGE_TEXT"))
        )
    )
    glyph.setFixedSize(14, 14)

    layout.addWidget(glyph)
    layout.addWidget(_label(text.upper(), "sectionHeading"))
    layout.addStretch(1)
    return row


class WrapChip(QLabel):
    """A chip that sits on one line when it fits, and wraps when it doesn't.

    A plain QLabel chip is one unbreakable line. A single long risk factor
    ("Residence in or travel to endemic tropical regions...") would force its
    whole column wide and push the page off the right edge.

    This reports its natural single-line width as the preferred size, but a
    small minimum, and word-wraps its own text when squeezed below its
    natural width.
    """

    def __init__(self, text: str, object_name: str) -> None:
        super().__init__(text)
        self.setObjectName(object_name)
        # Polish now, so the stylesheet's padding is applied before measuring.
        # The app-level stylesheet reaches a widget on polish even before it
        # has a parent.
        self.ensurePolished()
        self._natural = super().sizeHint()   # one line, padding included
        self.setWordWrap(True)

    def sizeHint(self) -> QSize:
        return QSize(self._natural)

    def minimumSizeHint(self) -> QSize:
        # Small, so the chip never forces its container wider than it is.
        return QSize(min(60, self._natural.width()), self._natural.height())


class FlowLayout(QLayout):
    """Lays widgets out left to right, wrapping to a new line when full.

    Like words in a paragraph. Qt ships no flow layout, so this is the
    standard pattern from Qt's own examples, extended to handle a single
    item wider than the whole line: that item is capped at the line width
    and asked how tall it becomes (height-for-width) — which is what lets a
    long WrapChip break onto two lines instead of overflowing.
    """

    def __init__(self, h_spacing: int = 7, v_spacing: int = 6) -> None:
        super().__init__()
        self._items: list = []
        self._h_spacing = h_spacing
        self._v_spacing = v_spacing
        self.setContentsMargins(0, 0, 0, 0)
        # heightForWidth is asked for again and again during one resize
        # (thousands of times across a page of cards); the answer only
        # changes when the items do, so remember it per width.
        self._hfw: dict[int, int] = {}

    def __del__(self) -> None:
        while self.takeAt(0) is not None:
            pass

    # QLayout's required interface ----------------------------------------

    def addItem(self, item) -> None:  # noqa: N802
        self._items.append(item)
        self.invalidate()

    def invalidate(self) -> None:
        cache = getattr(self, "_hfw", None)    # Qt calls this during __init__ too
        if cache:
            cache.clear()
        super().invalidate()

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int):  # noqa: N802
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int):  # noqa: N802
        if not 0 <= index < len(self._items):
            return None
        self._hfw.clear()
        return self._items.pop(index)

    def expandingDirections(self) -> Qt.Orientation:  # noqa: N802
        return Qt.Orientation(0)

    # Height depends on width: narrower means more lines ---------------------

    def hasHeightForWidth(self) -> bool:  # noqa: N802
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802
        height = self._hfw.get(width)
        if height is None:
            height = self._hfw[width] = self._arrange(QRect(0, 0, width, 0), apply=False)
        return height

    def setGeometry(self, rect: QRect) -> None:  # noqa: N802
        super().setGeometry(rect)
        self._arrange(rect, apply=True)

    def sizeHint(self) -> QSize:  # noqa: N802
        return self.minimumSize()

    def minimumSize(self) -> QSize:  # noqa: N802
        """As narrow as the narrowest-allowed item, never the sum of them.

        This is the whole fix. A grid's minimum width is the sum of a row's
        items; a flow layout's is just the widest single item's minimum,
        because everything else can drop to the next line.
        """
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        return size + QSize(
            margins.left() + margins.right(), margins.top() + margins.bottom()
        )

    def _arrange(self, rect: QRect, apply: bool) -> int:
        margins = self.contentsMargins()
        area = rect.adjusted(
            margins.left(), margins.top(), -margins.right(), -margins.bottom()
        )
        x, y, line_height = area.x(), area.y(), 0

        for item in self._items:
            hint = item.sizeHint()
            # Cap an overlong item at the line width; it wraps its own text.
            width = min(hint.width(), max(area.width(), 1))
            height = (
                item.heightForWidth(width)
                if item.hasHeightForWidth()
                else hint.height()
            )

            # Start a new line if this item would pass the right edge — but
            # never before the first item on a line, or a too-wide item
            # would loop forever.
            if x + width > area.right() + 1 and line_height > 0:
                x = area.x()
                y += line_height + self._v_spacing
                line_height = 0

            if apply:
                item.setGeometry(QRect(QPoint(x, y), QSize(width, height)))

            x += width + self._h_spacing
            line_height = max(line_height, height)

        return y + line_height - rect.y() + margins.bottom()


def _chip_flow(items: list[str], object_name: str) -> QWidget:
    """Chips that wrap onto new lines to fit the column they are in."""
    holder = QWidget()
    holder.setObjectName("panel")
    flow = FlowLayout()
    holder.setLayout(flow)
    for text in items:
        flow.addWidget(WrapChip(text, object_name))
    return holder


class IntensityBar(QWidget):
    """Intensity out of ten, drawn as a filled bar."""

    def __init__(self, value: int, cardinal: bool) -> None:
        super().__init__()
        self.setObjectName("panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        top = QHBoxLayout()
        top.setSpacing(8)
        top.addWidget(
            _chip("Cardinal Sign" if cardinal else "Secondary",
                  "cardinalChip" if cardinal else "secondaryChip")
        )
        top.addStretch(1)
        top.addWidget(_label(f"Intensity: {value}/10", "metaLabel", wrap=False))
        layout.addLayout(top)

        bar = QProgressBar()
        bar.setObjectName("intensityBarCardinal" if cardinal else "intensityBar")
        bar.setTextVisible(False)
        bar.setFixedHeight(4)
        bar.setRange(0, 10)
        bar.setValue(value)
        layout.addWidget(bar)


class ConditionColumn(QFrame):
    """One condition's side of the comparison."""

    monograph_requested = Signal(str)

    def __init__(
            self, disease: Disease, position: str, unique_symptoms: list
    ) -> None:
        super().__init__()
        self.setObjectName("compareColumn")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(13)

        header = QHBoxLayout()
        header.addWidget(_chip(position.upper(), "positionChip"))
        header.addStretch(1)
        header.addWidget(_chip(disease.severity, "severityChipModerate"))
        header.addWidget(
            _chip(
                "Contagious" if disease.contagious else "Non-Contagious",
                "contagiousChip" if disease.contagious else "safeChip",
            )
        )
        layout.addLayout(header)

        layout.addWidget(_label(disease.name, "compareTitle"))
        if disease.scientific_name:
            layout.addWidget(
                _label(disease.scientific_name, "cardScientificName")
            )
        layout.addWidget(_label(disease.description, "bodyTextMuted"))

        if disease.pathophysiology:
            block, block_layout = _card("innerCard")
            block_layout.setSpacing(7)
            block_layout.addWidget(_heading("Pathophysiology snapshot", "pulse"))
            block_layout.addWidget(_label(disease.pathophysiology, "bodyText"))
            layout.addWidget(block)

        if disease.onset_progression:
            block, block_layout = _card("innerCard")
            block_layout.setSpacing(7)
            block_layout.addWidget(
                _heading("Onset & progression pattern", "clock")
            )
            block_layout.addWidget(
                _label(disease.onset_progression, "bodyText")
            )
            layout.addWidget(block)

        if unique_symptoms:
            layout.addWidget(
                _label(
                    f"UNIQUE HALLMARK SYMPTOMS ({len(unique_symptoms)})",
                    "subHeading",
                )
            )
            layout.addWidget(
                _chip_flow(
                    [s.name or s.symptom_id for s in unique_symptoms],
                    "relatedPillPrimary",
                )
            )

        if disease.recommended_tests:
            layout.addWidget(
                _heading("Key diagnostic tests (rule-in value)", "search")
            )
            for test in disease.recommended_tests:
                layout.addWidget(_label(f"\u2022  {test}", "bulletText"))

        if disease.risk_factors:
            layout.addWidget(_heading("Risk factors & population", "user"))
            layout.addWidget(
                _chip_flow(disease.risk_factors, "relatedPill")
            )

        if disease.emergency_warning_signs:
            block, block_layout = _card("redflagCard")
            block_layout.setSpacing(7)
            block_layout.addWidget(
                _heading(
                    "Emergency warning signs", "alert", Theme.token("DANGER")
                )
            )
            for sign in disease.emergency_warning_signs:
                block_layout.addWidget(_label(f"\u2022  {sign}", "bulletText"))
            layout.addWidget(block)

        if disease.treatments:
            layout.addWidget(_label("PRIMARY TREATMENTS", "subHeading"))
            layout.addWidget(
                _label(" \u2022 ".join(disease.treatments), "bodyTextMuted")
            )

        layout.addStretch(1)

        monograph = QPushButton("View Full Monograph  \u2192")
        monograph.setObjectName("inspectLink")
        monograph.setCursor(Qt.CursorShape.PointingHandCursor)
        monograph.clicked.connect(
            lambda: self.monograph_requested.emit(disease.id)
        )
        layout.addWidget(monograph, 0, Qt.AlignmentFlag.AlignRight)


class CompareView(QWidget):
    """Differential analysis between two or three conditions."""

    selection_changed = Signal()
    monograph_requested = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")

        self._combos: list[QComboBox] = []
        self._third_visible = False

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
        self._page_layout.setContentsMargins(30, 20, 30, 30)
        self._page_layout.setSpacing(17)

        self._page_layout.addWidget(self._build_selector_card())

        self._results_host = QWidget()
        self._results_host.setObjectName("panel")
        self._results_layout = QVBoxLayout(self._results_host)
        self._results_layout.setContentsMargins(0, 0, 0, 0)
        self._results_layout.setSpacing(17)
        self._page_layout.addWidget(self._results_host)
        self._page_layout.addStretch(1)

        scroll.setWidget(page)
        root.addWidget(scroll)

    # ------------------------------------------------------------ selectors

    def _build_selector_card(self) -> QWidget:
        card, layout = _card()

        header = QHBoxLayout()
        text_col = QVBoxLayout()
        text_col.setSpacing(3)
        text_col.addWidget(
            _heading("Compare medical conditions (differential analysis)", "search")
        )
        text_col.addWidget(
            _label(
                "Differential workstation with mechanism snapshots, onset "
                "trajectories, rule-in tests, and comparative citations.",
                "bodyTextMuted",
            )
        )
        header.addLayout(text_col)
        header.addStretch(1)
        layout.addLayout(header)

        self._selector_row = QHBoxLayout()
        self._selector_row.setSpacing(14)
        for index in range(MAX_CONDITIONS):
            self._selector_row.addWidget(self._build_combo(index), 1)
        layout.addLayout(self._selector_row)

        self._third_btn = QPushButton("+  Add a Third Condition (Triad)")
        self._third_btn.setObjectName("secondaryButton")
        self._third_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._third_btn.clicked.connect(self._toggle_third)
        layout.addWidget(self._third_btn, 0, Qt.AlignmentFlag.AlignRight)

        return card

    def _build_combo(self, index: int) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        layout = QVBoxLayout(holder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        caption = _label(f"CONDITION {chr(65 + index)}", "subHeading")
        combo = QComboBox()
        combo.setObjectName("filterCombo")
        combo.setFixedHeight(38)
        combo.setCursor(Qt.CursorShape.PointingHandCursor)
        # By default a combo box widens itself to fit its longest option.
        # "Community-Acquired Pneumonia (Bacterial/Viral Pneumonitis)" made
        # each one ~560px, and three side by side pushed the page off the
        # right edge. These let it shrink to share the row evenly; the
        # dropdown list itself is widened separately in set_conditions, so
        # long names are still readable when it opens.
        combo.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        combo.setMinimumContentsLength(14)
        combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        combo.addItem("Select a condition\u2026", None)
        # currentIndexChanged carries an int; selection_changed takes none.
        # signal.emit is a plain callable, so Qt does not discard the extra
        # argument the way it would for a real slot.
        combo.currentIndexChanged.connect(
            lambda _index: self.selection_changed.emit()
        )
        # Truncated names stay readable on hover.
        combo.currentIndexChanged.connect(
            lambda _index, c=combo: c.setToolTip(c.currentText())
        )

        layout.addWidget(caption)
        layout.addWidget(combo)

        self._combos.append(combo)
        if index == 2:
            holder.hide()
            self._third_holder = holder
        return holder

    def _toggle_third(self) -> None:
        self._third_visible = not self._third_visible
        self._third_holder.setVisible(self._third_visible)
        self._third_btn.setText(
            "\u2212  Remove Third Condition" if self._third_visible
            else "+  Add a Third Condition (Triad)"
        )
        if not self._third_visible:
            self._combos[2].setCurrentIndex(0)
        self.selection_changed.emit()

    # ---------------------------------------------------------- public api

    def set_conditions(self, diseases: list[Disease]) -> None:
        """Fill every selector. Keeps current choices where still valid."""
        for index, combo in enumerate(self._combos):
            current = combo.currentData()
            combo.blockSignals(True)
            combo.clear()
            combo.addItem("Select a condition\u2026", None)
            for disease in diseases:
                label = disease.name
                if disease.scientific_name:
                    label = f"{disease.name} ({disease.scientific_name})"
                combo.addItem(label, disease.id)

            restored = combo.findData(current)
            if restored >= 0:
                combo.setCurrentIndex(restored)
            elif index < len(diseases):
                # Preselect the first two so the page is not blank on open.
                combo.setCurrentIndex(index + 1 if index < 2 else 0)
            combo.blockSignals(False)

            # The combo itself is now allowed to be narrow, so widen just the
            # dropdown list to fit the longest name. It floats above the
            # page when open, so this cannot affect the layout.
            view = combo.view()
            view.setMinimumWidth(view.sizeHintForColumn(0) + 32)
            # The closed combo shows the full name on hover when truncated.
            combo.setToolTip(combo.currentText())

        self.selection_changed.emit()

    def selected_ids(self) -> list[str]:
        """Chosen condition ids, deduplicated, in selector order.

        Comparing a condition against itself produces a page of empty
        differences, so duplicates are dropped rather than rendered.
        """
        ids: list[str] = []
        for index, combo in enumerate(self._combos):
            if index == 2 and not self._third_visible:
                continue
            value = combo.currentData()
            if value and value not in ids:
                ids.append(value)
        return ids

    def show_comparison(self, comparison: Comparison) -> None:
        self._clear_results()

        if len(comparison.diseases) < 2:
            self._results_layout.addWidget(
                _label(
                    "Select two conditions to compare. At least two published "
                    "conditions must exist in the database.",
                    "bodyTextMuted",
                )
            )
            return

        self._results_layout.addWidget(self._build_columns(comparison))
        self._results_layout.addWidget(self._build_pivot(comparison))

        if comparison.shared:
            self._results_layout.addWidget(self._build_matrix(comparison))
        else:
            note, note_layout = _card()
            note_layout.addWidget(
                _heading("Shared overlapping symptoms", "search")
            )
            note_layout.addWidget(
                _label(
                    "No symptoms are recorded in every selected condition. "
                    "That may be a genuine finding or a gap in the data.",
                    "bodyTextMuted",
                )
            )
            self._results_layout.addWidget(note)

        self._results_layout.addWidget(self._build_references(comparison))

    def show_message(self, message: str) -> None:
        self._clear_results()
        self._results_layout.addWidget(_label(message, "bodyTextMuted"))

    # ------------------------------------------------------------- sections

    def _clear_results(self) -> None:
        while self._results_layout.count():
            item = self._results_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _build_columns(self, comparison: Comparison) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        layout = QHBoxLayout(holder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        for index, disease in enumerate(comparison.diseases):
            column = ConditionColumn(
                disease,
                f"Condition {chr(65 + index)}",
                comparison.unique_for(disease.id),
            )
            column.monograph_requested.connect(self.monograph_requested.emit)
            layout.addWidget(column, 1)
        return holder

    def _build_pivot(self, comparison: Comparison) -> QWidget:
        """The differentiating facts panel.

        Labelled as assembled from stored data, because that is exactly what
        it is — no clinical reasoning is generated here.
        """
        card, layout = _card("pivotCard")

        header = QHBoxLayout()
        header.addWidget(
            _heading("Key differentiating facts (cardinal clinical pivot)", "search")
        )
        header.addStretch(1)
        header.addWidget(
            _chip("Assembled from recorded data \u2022 not clinical advice",
                  "synthesisChip")
        )
        layout.addLayout(header)

        summary = comparison.hallmark_summary()
        if summary:
            layout.addWidget(
                _label(
                    f"Does the presentation match the recorded hallmark signs "
                    f"of {summary}?",
                    "pivotQuestion",
                )
            )
        else:
            layout.addWidget(
                _label(
                    "No cardinal symptoms are recorded for these conditions, "
                    "so no hallmark contrast can be drawn.",
                    "bodyTextMuted",
                )
            )

        facts = comparison.differentiating_facts()
        if facts:
            layout.addWidget(
                _label("DIFFERENTIAL BRANCHING CRITERIA", "subHeading")
            )
            grid = QGridLayout()
            grid.setHorizontalSpacing(14)
            grid.setVerticalSpacing(8)
            for index, fact in enumerate(facts):
                row, column = divmod(index, 2)
                grid.addWidget(_label(f"\u2713  {fact}", "bulletText"), row, column)
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            layout.addLayout(grid)

        layout.addWidget(
            _label(
                "Source: assembled from this database's recorded fields. "
                "Requires faculty review before teaching use.",
                "bodyTextMuted",
            )
        )
        return card

    def _build_matrix(self, comparison: Comparison) -> QWidget:
        card, layout = _card("matrixCard")

        header = QHBoxLayout()
        header.addWidget(
            _heading(
                f"Shared overlapping symptoms ({len(comparison.shared)}) "
                "\u2014 rule-in / rule-out matrix",
                "search",
                Theme.token("SUCCESS"),
            )
        )
        header.addStretch(1)
        layout.addLayout(header)
        layout.addWidget(
            _label(
                "Identical symptoms presenting with distinct recorded "
                "intensity across each condition.",
                "bodyTextMuted",
            )
        )

        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(12)

        grid.addWidget(_label("SHARED SYMPTOM", "matrixHeader"), 0, 0)
        for index, disease in enumerate(comparison.diseases):
            grid.addWidget(
                _label(f"{disease.name.upper()} PRESENTATION", "matrixHeader"),
                0,
                index + 1,
                )
        takeaway_column = len(comparison.diseases) + 1
        grid.addWidget(
            _label("DIFFERENTIAL TAKEAWAY", "matrixHeader"), 0, takeaway_column
        )

        for row, shared in enumerate(comparison.shared, start=1):
            grid.addWidget(
                _label(shared.name or shared.symptom_id, "symptomName"), row, 0
            )
            for index, disease in enumerate(comparison.diseases):
                grid.addWidget(
                    IntensityBar(
                        shared.intensity_for(disease.id),
                        shared.is_cardinal_for(disease.id),
                    ),
                    row,
                    index + 1,
                    )
            grid.addWidget(
                _label(shared.distinction(comparison.diseases), "bodyTextMuted"),
                row,
                takeaway_column,
            )

        grid.setColumnStretch(0, 2)
        for index in range(len(comparison.diseases)):
            grid.setColumnStretch(index + 1, 3)
        grid.setColumnStretch(takeaway_column, 3)

        layout.addLayout(grid)
        return card

    def _build_references(self, comparison: Comparison) -> QWidget:
        card, layout = _card()

        header = QHBoxLayout()
        header.addWidget(
            _heading("References for this differential comparison", "book")
        )
        header.addStretch(1)
        header.addWidget(_chip("Primary mother book citations", "systemChip"))
        layout.addLayout(header)

        columns = QHBoxLayout()
        columns.setSpacing(14)
        any_citation = False

        for disease in comparison.diseases:
            tile, tile_layout = _card("innerCard")
            tile_layout.setSpacing(7)
            tile_layout.addWidget(
                _label(f"{disease.name.upper()} REFERENCE", "subHeading")
            )

            if disease.mother_book_references:
                any_citation = True
                for reference in disease.mother_book_references:
                    tile_layout.addWidget(_label("TIER 1 (MOTHER BOOK)", "tierLabel"))
                    tile_layout.addWidget(
                        _label(reference.source_name, "symptomName")
                    )
            if disease.chapter_references:
                any_citation = True
                for reference in disease.chapter_references:
                    tile_layout.addWidget(
                        _label("TIER 2 (SPECIFIC REFERENCE)", "tierLabel")
                    )
                    tile_layout.addWidget(
                        _label(reference.source_name, "bodyTextMuted")
                    )
            if not disease.clinical_references:
                tile_layout.addWidget(
                    _label("No citation recorded.", "bodyTextMuted")
                )

            tile_layout.addStretch(1)
            columns.addWidget(tile, 1)

        layout.addLayout(columns)

        if any_citation:
            layout.addWidget(
                _label(
                    "No single joint comparative monograph is indexed for this "
                    "pairing. Each condition's own primary citation is shown.",
                    "bodyTextMuted",
                )
            )
        return card