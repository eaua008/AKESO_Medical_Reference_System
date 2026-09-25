"""Symptom Correlation Engine: the assessment screen.

Laid out as in the reference build:

    symptom picker          |  onset, pattern and intensity (own scroll)
    associated symptom checklist
    exposure | comorbidity | vitals | family history      (four columns)
    demographics + calculate
    ------------------------------------------------------------------
    differential header, then the matrix and/or the detailed cards

Only this widget scrolls; the shell's sidebar and header sit outside it and
never move. The two inner columns scroll independently, so choosing a fifth
symptom scrolls that column instead of stretching the page.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QLayout,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.models.checker import (
    COMORBIDITIES,
    EXPOSURES,
    FAMILY_RISKS,
    CheckerInput,
    CheckerResult,
    MatchResult,
    SelectedSymptom,
    Vitals,
    is_pain_symptom,
)
from app.models.symptom import Symptom
from app.ui.views.checker_widgets import (
    SuggestionChip,
    SymptomParameters,
    SymptomRow,
    _card,
    _combo,
    _label,
)

URGENCY_LABELS = {
    "EMERGENCY": "Emergency",
    "SEEK_URGENT_CARE": "Seek Urgent Care",
    "SEE_DOCTOR_SOON": "See Doctor Soon",
    "SELF_CARE": "Self-Care",
}
COLUMN_HEIGHT = 330


class MatchCard(QFrame):
    """One condition in the differential, expandable to its reasoning."""

    open_requested = Signal(str)
    toggled = Signal(str)

    def __init__(self, match: MatchResult, rank: int, expanded: bool) -> None:
        super().__init__()
        self.setObjectName("ccMatchCard")
        self.setProperty("top", rank == 1)
        self._id = match.disease_id

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)
        layout.addLayout(self._build_head(match, rank, expanded))
        if expanded:
            self._build_body(layout, match)

    def _build_head(self, match: MatchResult, rank: int, expanded: bool) -> QHBoxLayout:
        head = QHBoxLayout()
        head.setSpacing(10)
        head.addWidget(_label(f"#{rank}", "ccRank", wrap=False))
        head.addWidget(_label("PRIMARY DIFFERENTIAL" if rank == 1 else "DIFFERENTIAL MATCH",
                              "ccMatchTag", wrap=False))
        urgency = _label(URGENCY_LABELS.get(match.urgency, "Not specified"),
                         "ccUrgencyPill", wrap=False)
        urgency.setProperty("urgency", match.urgency.lower() or "none")
        head.addWidget(urgency)

        names = QVBoxLayout()
        names.setSpacing(1)
        names.addWidget(_label(match.name, "ccMatchName", wrap=False))
        if match.scientific_name:
            names.addWidget(_label(match.scientific_name, "ccMatchSci", wrap=False))
        head.addLayout(names, 1)

        score = QVBoxLayout()
        score.setSpacing(2)
        value = QHBoxLayout()
        value.addStretch(1)
        value.addWidget(_label(f"{match.score:.0f}", "ccScore", wrap=False))
        value.addWidget(_label("%", "ccScorePercent", wrap=False))
        score.addLayout(value)
        bar = QProgressBar()
        bar.setObjectName("ccScoreBar")
        bar.setRange(0, 100)
        bar.setValue(int(match.score))
        bar.setTextVisible(False)
        bar.setFixedHeight(3)
        bar.setFixedWidth(110)
        score.addWidget(bar)
        head.addLayout(score)

        chevron = QPushButton("\u25b2" if expanded else "\u25bc")
        chevron.setObjectName("ccChevron")
        chevron.setFixedWidth(26)
        chevron.setCursor(Qt.CursorShape.PointingHandCursor)
        chevron.clicked.connect(lambda: self.toggled.emit(self._id))
        head.addWidget(chevron)
        return head

    def _build_body(self, layout: QVBoxLayout, match: MatchResult) -> None:
        # urgency indicator strip
        urgent = match.urgency in ("EMERGENCY", "SEEK_URGENT_CARE")
        strip, strip_layout = _card(
            f"Urgency indicator: {URGENCY_LABELS.get(match.urgency, 'not specified')}",
            "alert", danger=urgent,
            trailing=("Immediate evaluation (0\u201315 minutes)"
                      if match.urgency == "EMERGENCY" else
                      "Same-day consultation (2\u20136 hours)"
                      if match.urgency == "SEEK_URGENT_CARE" else
                      "Outpatient evaluation (1\u20133 days)"))
        columns = QHBoxLayout()
        columns.setSpacing(14)
        for caption, text in (
                ("Recommended action", self._action_for(match.urgency)),
                ("Triage rationale", f"{match.severity or 'Unclassified'} severity; "
                                     f"{match.matched_count} of {match.total_hallmarks} "
                                     "defined symptoms reported.")):
            cell = QVBoxLayout()
            cell.setSpacing(2)
            cell.addWidget(_label(caption.upper() + ":", "ccFieldLabel", wrap=False))
            cell.addWidget(_label(text, "ccBody"))
            columns.addLayout(cell, 1)
        strip_layout.addLayout(columns)
        layout.addWidget(strip)

        # reasoning
        reasoning, reasoning_layout = _card("Multi-factor algorithmic reasoning", "search")
        reasoning_layout.addWidget(_label(
            f"Matches {match.matched_count} of {match.total_hallmarks} defined symptoms "
            f"for {match.name}. Includes "
            f"{sum(1 for m in match.matched if m.is_primary)} hallmark symptom(s).",
            "ccBody"))
        if match.boosters:
            box = QFrame()
            box.setObjectName("ccBoosterBox")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(12, 8, 12, 9)
            box_layout.setSpacing(3)
            box_layout.addWidget(_label("EXPOSURE & RISK BOOSTERS APPLIED:",
                                        "ccBoosterLabel", wrap=False))
            for booster in match.boosters:
                box_layout.addWidget(_label(f"\u2022 {booster}", "ccBooster"))
            reasoning_layout.addWidget(box)
        reasoning_layout.addWidget(_label(
            f"Intensity alignment: {match.alignment}%     Weighted sum: "
            f"{match.weighted_sum} / {match.weighted_max}", "ccMuted"))
        layout.addWidget(reasoning)

        if match.matched:
            layout.addWidget(_label("MATCHED SYMPTOMS & CLINICAL PATTERNS:",
                                    "ccLabel", wrap=False))
            grid = QGridLayout()
            grid.setSpacing(10)
            for index, symptom in enumerate(match.matched):
                tile = QFrame()
                tile.setObjectName("ccSymptomTile")
                tile_layout = QVBoxLayout(tile)
                tile_layout.setContentsMargins(12, 9, 12, 9)
                tile_layout.setSpacing(4)

                top = QHBoxLayout()
                top.addWidget(_label(symptom.name, "ccTileName", wrap=False))
                top.addStretch(1)
                if symptom.is_primary:
                    top.addWidget(_label("HALLMARK", "ccHallmark", wrap=False))
                tile_layout.addLayout(top)

                compare = QHBoxLayout()
                compare.addWidget(_label(f"Your intensity: {symptom.user_intensity}/10",
                                         "ccTileMeta", wrap=False))
                compare.addStretch(1)
                compare.addWidget(_label(f"Typical: {symptom.typical_intensity}/10",
                                         "ccTileMeta", wrap=False))
                tile_layout.addLayout(compare)

                chips = QHBoxLayout()
                chips.setSpacing(6)
                for text, style in ((symptom.onset.title(), "ccChip"),
                                    (symptom.pattern.title(), "ccChipAccent"),
                                    (symptom.trend.title(),
                                     "ccChipWarn" if symptom.trend == "worsening" else "ccChip")):
                    chips.addWidget(_label(text, style, wrap=False))
                chips.addStretch(1)
                tile_layout.addLayout(chips)
                grid.addWidget(tile, *divmod(index, 2))
            for column in range(2):
                grid.setColumnStretch(column, 1)
            layout.addLayout(grid)

        if match.missing:
            layout.addWidget(_label(f"MISSING INDICATORS FOR {match.name.upper()}:",
                                    "ccLabel", wrap=False))
            row = QHBoxLayout()
            row.setSpacing(6)
            for name in match.missing[:5]:
                row.addWidget(_label(f"\u2022 {name}", "ccChip", wrap=False))
            row.addStretch(1)
            layout.addLayout(row)

        if match.emergency_signs:
            footer, footer_layout = _card("", danger=True)
            row = QHBoxLayout()
            text = QVBoxLayout()
            text.setSpacing(2)
            text.addWidget(_label("WARNING SIGNS TO MONITOR", "ccRedHeading", wrap=False))
            text.addWidget(_label("; ".join(match.emergency_signs[:3]), "ccRedBody"))
            row.addLayout(text, 1)
            read = QPushButton("View protocol  \u2192")
            read.setObjectName("ccPrimaryButton")
            read.setCursor(Qt.CursorShape.PointingHandCursor)
            read.clicked.connect(lambda: self.open_requested.emit(self._id))
            row.addWidget(read)
            footer_layout.addLayout(row)
            layout.addWidget(footer)
        else:
            row = QHBoxLayout()
            row.addStretch(1)
            read = QPushButton("Read full monograph  \u2192")
            read.setObjectName("ccPrimaryButton")
            read.setCursor(Qt.CursorShape.PointingHandCursor)
            read.clicked.connect(lambda: self.open_requested.emit(self._id))
            row.addWidget(read)
            layout.addLayout(row)

    @staticmethod
    def _action_for(urgency: str) -> str:
        return {
            "EMERGENCY": "Call 911 or go to the nearest emergency department now.",
            "SEEK_URGENT_CARE": "Visit an urgent care centre or request a same-day "
                                "clinic evaluation.",
            "SEE_DOCTOR_SOON": "Book an appointment with your primary care doctor.",
            "SELF_CARE": "Rest and monitor; see a doctor if it worsens.",
        }.get(urgency, "Read the monograph and monitor.")


class SymptomCheckerView(QWidget):
    calculate_requested = Signal()
    symptoms_changed = Signal()
    disease_requested = Signal(str)
    reset_requested = Signal()
    suggestion_chosen = Signal(str)
    save_case_requested = Signal()      # Save to Notebook
    open_case_requested = Signal()      # Open the saved case in the notebook

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._symptoms: list[Symptom] = []
        self._selected: dict[str, SelectedSymptom] = {}
        self._param_cards: dict[str, SymptomParameters] = {}
        self._rows: list[SymptomRow] = []
        self._expanded: set[str] = set()
        self._view_mode = "both"
        self._last_result: Optional[CheckerResult] = None
        self._saved_case = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        page = QWidget()
        page.setObjectName("panel")
        self._page = QVBoxLayout(page)
        self._page.setContentsMargins(30, 22, 30, 30)
        self._page.setSpacing(14)

        self._page.addWidget(self._build_header())
        self._page.addWidget(self._build_disclaimer())
        self._page.addWidget(self._build_specificity())
        self._page.addWidget(self._build_selection())
        self._page.addWidget(self._build_suggestions())
        self._page.addWidget(self._build_four_columns())
        self._page.addWidget(self._build_demographics())

        self._results_host = QVBoxLayout()
        self._results_host.setSpacing(14)
        self._page.addLayout(self._results_host)
        self._page.addStretch(1)

        self._scroll.setWidget(page)
        root.addWidget(self._scroll)

    # ----------------------------------------------------------- builders

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
        title = QHBoxLayout()
        title.setSpacing(10)
        title.addWidget(_label("Akeso Symptom Correlation Engine", "pageTitle", wrap=False))
        title.addWidget(_label("ENGINE V2.5", "ccEngineBadge", wrap=False))
        title.addStretch(1)
        text.addLayout(title)
        text.addWidget(_label(
            "Rule-based weighted matching consuming standardized clinical "
            "parameters (onset, pattern, exposures, vitals).", "pageSubtitle"))
        row.addLayout(text, 1)

        reset = QPushButton("\u21ba  Reset")
        reset.setObjectName("ccGhostButton")
        reset.setCursor(Qt.CursorShape.PointingHandCursor)
        reset.clicked.connect(self.reset_requested.emit)
        row.addWidget(reset, 0, Qt.AlignmentFlag.AlignTop)
        self.refresh_theme()
        return header

    @staticmethod
    def _build_disclaimer() -> QWidget:
        box = QFrame()
        box.setObjectName("ccDisclaimer")
        layout = QHBoxLayout(box)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)
        layout.addWidget(_label("Medical disclaimer:", "ccDisclaimerTitle", wrap=False))
        layout.addWidget(_label(
            "This computes statistical differential probabilities for educational "
            "reference. It generates possible conditions, never a certified "
            "diagnosis. In a medical emergency, seek urgent in-person care.",
            "ccDisclaimerText"), 1)
        return box

    def _build_specificity(self) -> QWidget:
        card, layout = _card()
        row = QHBoxLayout()
        row.addWidget(_label("DIAGNOSTIC SPECIFICITY METER", "ccLabel", wrap=False))
        self._spec_badge = _label("\u2014", "ccSpecBadge", wrap=False)
        row.addWidget(self._spec_badge)
        row.addStretch(1)
        self._spec_text = _label("Add symptoms to begin.", "ccMuted", wrap=False)
        row.addWidget(self._spec_text)
        layout.addLayout(row)

        self._spec_bar = QProgressBar()
        self._spec_bar.setObjectName("ccSpecBar")
        self._spec_bar.setRange(0, 100)
        self._spec_bar.setValue(0)
        self._spec_bar.setTextVisible(False)
        self._spec_bar.setFixedHeight(5)
        layout.addWidget(self._spec_bar)
        return card

    def _build_selection(self) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(14)

        picker, picker_layout = _card("Select symptoms", "pulse")
        self._picker_card = picker
        self._search = QLineEdit()
        self._search.setObjectName("filterSearch")
        self._search.setPlaceholderText("Search symptoms (e.g. Fever, Cough, Joint pain)\u2026")
        self._search.setFixedHeight(36)
        self._search.setClearButtonEnabled(True)
        self._search.textChanged.connect(lambda _t: self._render_symptom_list())
        picker_layout.addWidget(self._search)

        self._list_scroll = QScrollArea()
        self._list_scroll.setWidgetResizable(True)
        self._list_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._list_scroll.setFixedHeight(COLUMN_HEIGHT)
        list_host = QWidget()
        list_host.setObjectName("panel")
        self._list_layout = QVBoxLayout(list_host)
        self._list_layout.setContentsMargins(0, 0, 6, 0)
        self._list_layout.setSpacing(6)
        self._list_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self._list_layout.addStretch(1)
        self._list_scroll.setWidget(list_host)
        picker_layout.addWidget(self._list_scroll)
        row.addWidget(picker, 2)

        # Parameters get their own scroll area of the same height, so a fifth
        # symptom scrolls this column instead of stretching the page.
        params, params_layout = _card("Onset, pattern & intensity (per symptom)", "clock",
                                      trailing="Structured parameters")
        self._params_scroll = QScrollArea()
        self._params_scroll.setWidgetResizable(True)
        self._params_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._params_scroll.setFixedHeight(COLUMN_HEIGHT)
        params_host = QWidget()
        params_host.setObjectName("panel")
        self._params_layout = QVBoxLayout(params_host)
        self._params_layout.setContentsMargins(0, 0, 6, 0)
        self._params_layout.setSpacing(10)
        # Without this the scroll area squeezes the cards to fit its height
        # instead of letting them keep their size and scroll.
        self._params_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self._no_params = _label(
            "Choose a symptom on the left to set how it started, how severe it "
            "is and how long it has lasted.", "ccMuted")
        self._params_layout.addWidget(self._no_params)
        self._params_layout.addStretch(1)
        self._params_scroll.setWidget(params_host)
        params_layout.addWidget(self._params_scroll)
        row.addWidget(params, 3)
        return holder

    def _build_suggestions(self) -> QWidget:
        card = QFrame()
        card.setObjectName("ccSuggestCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 13)
        layout.setSpacing(8)

        head = QHBoxLayout()
        title = QVBoxLayout()
        title.setSpacing(2)
        title.addWidget(_label("Associated symptom checklist (auto-suggested co-occurrences)",
                               "ccSuggestTitle", wrap=False))
        self._suggest_sub = _label("Choose symptoms to see what commonly occurs with them.",
                                   "ccSuggestSub")
        title.addWidget(self._suggest_sub)
        head.addLayout(title, 1)
        head.addWidget(_label("RULE-BASED CROSS-DISEASE QUERY", "ccCrossQuery", wrap=False))
        layout.addLayout(head)

        self._suggest_row = QHBoxLayout()
        self._suggest_row.setSpacing(8)
        self._suggest_row.addStretch(1)
        layout.addLayout(self._suggest_row)
        self._suggest_card = card
        return card

    def _build_four_columns(self) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(14)

        # 1. exposure
        exposure, exposure_layout = _card("Exposure / risk toggles", "alert",
                                          trailing="Multipliers")
        self._exposure_boxes = {}
        for key, label, _keywords in EXPOSURES:
            box = QCheckBox(label)
            box.setObjectName("ccCheck")
            self._exposure_boxes[key] = box
            exposure_layout.addWidget(box)
        exposure_layout.addStretch(1)
        row.addWidget(exposure, 1)

        # 2. comorbidity
        history, history_layout = _card("Comorbidity / history", "heart",
                                        trailing="Prior baseline")
        self._comorbidity_boxes = {}
        for key, label, _keywords in COMORBIDITIES:
            box = QCheckBox(label)
            box.setObjectName("ccCheck")
            self._comorbidity_boxes[key] = box
            history_layout.addWidget(box)
        self._no_history = QCheckBox("None / no chronic history")
        self._no_history.setObjectName("ccCheck")
        self._no_history.setChecked(True)
        self._no_history.toggled.connect(self._on_no_history)
        history_layout.addWidget(self._no_history)
        history_layout.addStretch(1)
        row.addWidget(history, 1)

        # 3. vitals
        vitals, vitals_layout = _card("Objective vital signs", "pulse",
                                      trailing="Standardized")
        temp_row = QHBoxLayout()
        temp_row.addWidget(_label("MEASURED TEMP:", "ccFieldLabel", wrap=False))
        temp_row.addStretch(1)
        self._unit_group = QButtonGroup(self)
        self._unit_group.setExclusive(True)
        for unit in ("\u00b0C", "\u00b0F"):
            button = QPushButton(unit)
            button.setObjectName("ccUnitButton")
            button.setCheckable(True)
            button.setChecked(unit == "\u00b0C")
            button.setFixedWidth(30)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, u=unit: self._set_unit(u))
            self._unit_group.addButton(button)
            temp_row.addWidget(button)
        vitals_layout.addLayout(temp_row)

        self.temperature = QDoubleSpinBox()
        self.temperature.setObjectName("ccSpin")
        self.temperature.setRange(30.0, 43.0)
        self.temperature.setDecimals(1)
        self.temperature.setSingleStep(0.1)
        self.temperature.setValue(37.0)
        self.temperature.valueChanged.connect(lambda _v: self._update_temp_status())
        vitals_layout.addWidget(self.temperature)

        self._temp_status = _label("", "ccVitalStatus")
        self._temp_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vitals_layout.addWidget(self._temp_status)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(4)
        self.heart_rate = self._int_field(30, 220, 88)
        self.bp_systolic = self._int_field(60, 250, 120)
        self.bp_diastolic = self._int_field(30, 150, 80)
        grid.addWidget(_label("HEART RATE (BPM)", "ccFieldLabel", wrap=False), 0, 0)
        grid.addWidget(self.heart_rate, 1, 0)
        grid.addWidget(_label("BLOOD PRESSURE", "ccFieldLabel", wrap=False), 0, 1, 1, 2)
        grid.addWidget(self.bp_systolic, 1, 1)
        grid.addWidget(self.bp_diastolic, 1, 2)
        grid.setColumnStretch(0, 2)
        vitals_layout.addLayout(grid)

        extra = QHBoxLayout()
        self.spo2 = self._int_field(70, 100, 98)
        self.resp_rate = self._int_field(6, 60, 18)
        for caption, widget in (("SPO2 (%)", self.spo2), ("RESP RATE", self.resp_rate)):
            cell = QVBoxLayout()
            cell.setSpacing(3)
            cell.addWidget(_label(caption, "ccFieldLabel", wrap=False))
            cell.addWidget(widget)
            extra.addLayout(cell, 1)
        vitals_layout.addLayout(extra)
        vitals_layout.addStretch(1)
        row.addWidget(vitals, 1)

        # 4. family history
        family, family_layout = _card("Family & hereditary risk", "user",
                                      trailing="1st degree")
        family_scroll = QScrollArea()
        family_scroll.setWidgetResizable(True)
        family_scroll.setFrameShape(QFrame.Shape.NoFrame)
        family_scroll.setFixedHeight(170)
        family_host = QWidget()
        family_host.setObjectName("panel")
        family_inner = QVBoxLayout(family_host)
        family_inner.setContentsMargins(0, 0, 6, 0)
        family_inner.setSpacing(6)

        self._family_boxes = {}
        for key, label, domain, factor, _keywords in FAMILY_RISKS:
            item = QFrame()
            item.setObjectName("ccFamilyRow")
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(10, 6, 10, 6)
            text = QVBoxLayout()
            text.setSpacing(1)
            text.addWidget(_label(label, "ccFamilyName", wrap=False))
            text.addWidget(_label(f"{domain}  ({factor:.2f}\u00d7)", "ccFamilyMeta", wrap=False))
            item_layout.addLayout(text, 1)
            box = QCheckBox()
            self._family_boxes[key] = box
            item_layout.addWidget(box)
            family_inner.addWidget(item)
        family_inner.addStretch(1)
        family_scroll.setWidget(family_host)
        family_layout.addWidget(family_scroll)
        row.addWidget(family, 1)

        self._update_temp_status()
        return holder

    def _build_demographics(self) -> QWidget:
        card = QFrame()
        card.setObjectName("ccCard")
        row = QHBoxLayout(card)
        row.setContentsMargins(16, 12, 16, 12)
        row.setSpacing(12)

        row.addWidget(_label("\u2207  Demographics:", "ccLabel", wrap=False))
        row.addWidget(_label("AGE", "ccFieldLabel", wrap=False))
        self.age = self._int_field(0, 120, 29)
        self.age.setFixedWidth(90)
        row.addWidget(self.age)
        row.addWidget(_label("SEX", "ccFieldLabel", wrap=False))
        self.sex = _combo((("female", "Female"), ("male", "Male")), "female")
        self.sex.setFixedWidth(120)
        row.addWidget(self.sex)
        row.addStretch(1)

        self.calculate = QPushButton("\u26a1  Calculate Structured Clinical Matches")
        self.calculate.setObjectName("ccPrimaryButton")
        self.calculate.setFixedHeight(38)
        self.calculate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calculate.clicked.connect(self.calculate_requested.emit)
        row.addWidget(self.calculate)
        return card

    @staticmethod
    def _int_field(low: int, high: int, value: int) -> QSpinBox:
        box = QSpinBox()
        box.setObjectName("ccSpin")
        box.setRange(low, high)
        box.setValue(value)
        box.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        return box

    # --------------------------------------------------------- input state

    def _on_no_history(self, state: bool) -> None:
        """"None" and a named comorbidity cannot both be true."""
        if state:
            for box in self._comorbidity_boxes.values():
                box.setChecked(False)

    def _set_unit(self, unit: str) -> None:
        """Convert in place, so the number keeps its meaning."""
        celsius = unit == "\u00b0C"
        value = self.temperature.value()
        self.temperature.blockSignals(True)
        if celsius and self.temperature.maximum() > 50:      # was Fahrenheit
            self.temperature.setRange(30.0, 43.0)
            self.temperature.setValue((value - 32) * 5 / 9)
        elif not celsius and self.temperature.maximum() <= 50:
            self.temperature.setRange(86.0, 109.0)
            self.temperature.setValue(value * 9 / 5 + 32)
        self.temperature.setSuffix(f" {unit}")
        self.temperature.blockSignals(False)
        self._update_temp_status()

    def _celsius(self) -> float:
        value = self.temperature.value()
        return value if self.temperature.maximum() <= 50 else (value - 32) * 5 / 9

    def _update_temp_status(self) -> None:
        celsius = self._celsius()
        if celsius >= 38.0:
            text, tone = f"Active pyrexia / fever ({celsius:.1f} \u00b0C)", "bad"
        elif celsius <= 35.0:
            text, tone = f"Hypothermia ({celsius:.1f} \u00b0C)", "bad"
        elif celsius >= 37.6:
            text, tone = f"Low-grade elevation ({celsius:.1f} \u00b0C)", "warn"
        else:
            text, tone = f"Afebrile ({celsius:.1f} \u00b0C)", "good"
        self._temp_status.setText(text)
        self._temp_status.setProperty("tone", tone)
        self._temp_status.style().unpolish(self._temp_status)
        self._temp_status.style().polish(self._temp_status)

    # ------------------------------------------------------- symptom list

    def set_symptoms(self, symptoms: list[Symptom]) -> None:
        self._symptoms = sorted(symptoms, key=lambda s: -s.diagnostic_weight)
        self._render_symptom_list()

    def _render_symptom_list(self) -> None:
        while self._list_layout.count() > 1:
            item = self._list_layout.takeAt(0)
            if item.widget():
                item.widget().hide()
                item.widget().deleteLater()
        self._rows.clear()

        query = self._search.text().lower().strip()
        for symptom in self._symptoms:
            haystack = " ".join((symptom.name, symptom.scientific_name,
                                 *symptom.tags)).lower()
            if query and query not in haystack:
                continue
            row = SymptomRow(symptom, symptom.id in self._selected)
            row.toggled_symptom.connect(self._on_symptom_toggled)
            self._list_layout.insertWidget(self._list_layout.count() - 1, row)
            self._rows.append(row)

        if not self._rows:
            message = ("No symptom matches that search." if query else
                       "No symptoms available. The Symptom Encyclopedia has to "
                       "sync at least once first.")
            self._list_layout.insertWidget(0, _label(message, "ccMuted"))

    def _on_symptom_toggled(self, symptom_id: str, state: bool) -> None:
        if state:
            symptom = next((s for s in self._symptoms if s.id == symptom_id), None)
            if symptom is None:
                return
            self._selected[symptom_id] = SelectedSymptom(
                symptom_id=symptom_id, name=symptom.name,
                intensity=min(8, max(3, symptom.diagnostic_weight)))
        else:
            self._selected.pop(symptom_id, None)
        self._render_parameters()
        self.symptoms_changed.emit()

    def _render_parameters(self) -> None:
        while self._params_layout.count():
            item = self._params_layout.takeAt(0)
            if item.widget() and item.widget() is not self._no_params:
                item.widget().hide()
                item.widget().deleteLater()
        self._param_cards.clear()

        for entry in self._selected.values():
            symptom = next((s for s in self._symptoms if s.id == entry.symptom_id), None)
            is_pain = is_pain_symptom(entry.name, symptom.tags if symptom else ())
            card = SymptomParameters(entry, is_pain)
            card.removed.connect(lambda sid: self._on_symptom_toggled(sid, False))
            card.changed.connect(self.symptoms_changed.emit)
            self._params_layout.addWidget(card)
            self._param_cards[entry.symptom_id] = card

        self._params_layout.addWidget(self._no_params)
        self._no_params.setVisible(not self._selected)
        self._params_layout.addStretch(1)

        for row in self._rows:
            row.box.blockSignals(True)
            row.box.setChecked(row._id in self._selected)
            row.box.blockSignals(False)

    def add_symptom(self, symptom_id: str) -> None:
        if symptom_id not in self._selected:
            self._on_symptom_toggled(symptom_id, True)
            self._render_symptom_list()

    def show_suggestions(self, suggestions: list[tuple[str, str, int]]) -> None:
        """Associated symptoms worth adding: (id, name, how many conditions)."""
        while self._suggest_row.count():
            item = self._suggest_row.takeAt(0)
            if item.widget():
                item.widget().hide()
                item.widget().deleteLater()

        chosen = ", ".join(entry.name for entry in self._selected.values())
        if not suggestions:
            self._suggest_sub.setText(
                "Choose symptoms to see what commonly occurs with them."
                if not self._selected else
                "No further co-occurring symptoms found for this combination.")
        else:
            self._suggest_sub.setText(f"People who report {chosen} also commonly report:")
            for symptom_id, name, count in suggestions:
                chip = SuggestionChip(symptom_id, name, count)
                chip.clicked.connect(lambda _c=False, sid=symptom_id:
                                     self.suggestion_chosen.emit(sid))
                self._suggest_row.addWidget(chip)
        self._suggest_row.addStretch(1)

    def clear(self) -> None:
        self._selected.clear()
        self._expanded.clear()
        self._last_result = None
        self._saved_case = False
        self._render_symptom_list()
        self._render_parameters()
        self.show_suggestions([])
        self._clear_results()

    # ------------------------------------------------------------- input

    def gather(self) -> CheckerInput:
        for symptom_id, card in self._param_cards.items():
            self._selected[symptom_id] = card.value()
        return CheckerInput(
            symptoms=list(self._selected.values()),
            vitals=Vitals(
                temperature=self._celsius(),
                heart_rate=self.heart_rate.value(),
                bp_systolic=self.bp_systolic.value(),
                bp_diastolic=self.bp_diastolic.value(),
                spo2=self.spo2.value(),
                resp_rate=self.resp_rate.value()),
            age=self.age.value(),
            sex=self.sex.currentData(),
            exposures={k for k, box in self._exposure_boxes.items() if box.isChecked()},
            comorbidities={k for k, box in self._comorbidity_boxes.items()
                           if box.isChecked()},
            family_history={k for k, box in self._family_boxes.items()
                            if box.isChecked()})

    def selected_names(self) -> list[str]:
        return [entry.name for entry in self._selected.values()]

    # ------------------------------------------------------------ results

    def show_result(self, result: CheckerResult) -> None:
        self._last_result = result
        self._clear_results()

        self._spec_badge.setText(f"{result.specificity_label} ({result.specificity}%)")
        self._spec_badge.setProperty(
            "level", "high" if result.specificity >= 75 else
            "mid" if result.specificity >= 50 else "low")
        self._spec_badge.style().unpolish(self._spec_badge)
        self._spec_badge.style().polish(self._spec_badge)
        self._spec_bar.setValue(result.specificity)
        self._spec_text.setText(result.specificity_guidance)

        if not result.matches:
            empty, empty_layout = _card("No matches", "search")
            empty_layout.addWidget(_label(
                "No condition in the encyclopedia lists the symptoms you chose. "
                "Try another symptom, or browse the Disease Encyclopedia directly.",
                "ccBody"))
            self._results_host.addWidget(empty)
            return

        self._results_host.addWidget(self._build_results_header(result))
        self._results_host.addWidget(self._build_notebook_strip())
        self._results_host.addWidget(self._build_triage(result))
        if result.vital_alerts:
            alerts, alerts_layout = _card("Objective findings", "pulse")
            for alert in result.vital_alerts:
                alerts_layout.addWidget(_label(f"\u2022  {alert}", "ccBody"))
            self._results_host.addWidget(alerts)

        self._results_host.addWidget(self._build_view_switch())
        if self._view_mode in ("both", "matrix"):
            self._results_host.addWidget(self._build_matrix(result))
        if self._view_mode in ("both", "cards"):
            self._results_host.addWidget(_label(
                "2. DETAILED CLINICAL DIFFERENTIAL MONOGRAPHS & CARDS",
                "ccSectionTitle", wrap=False))
            for rank, match in enumerate(result.matches, 1):
                card = MatchCard(match, rank,
                                 expanded=(rank == 1 or match.disease_id in self._expanded))
                card.open_requested.connect(self.disease_requested.emit)
                card.toggled.connect(self._toggle_card)
                self._results_host.addWidget(card)

    def _build_results_header(self, result: CheckerResult) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 4, 0, 0)
        row.setSpacing(10)

        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(_label(
            f"CLINICAL PROBABILITY DIFFERENTIAL ({len(result.matches)} CANDIDATES)",
            "ccSectionTitle", wrap=False))
        text.addWidget(_label("Consuming onset, pattern, risk multipliers and objective "
                              "vitals.", "ccMuted", wrap=False))
        row.addLayout(text, 1)

        edit = QPushButton("\u2191  Edit inputs")
        edit.setObjectName("ccGhostButton")
        edit.setCursor(Qt.CursorShape.PointingHandCursor)
        edit.clicked.connect(lambda: self._scroll.verticalScrollBar().setValue(0))
        row.addWidget(edit)

        if self._saved_case:
            saved = _label("\u2713  Saved to Notebook", "ccSavedBadge", wrap=False)
            row.addWidget(saved)
            view = QPushButton("Open in Notebook  \u2192")
            view.setObjectName("ccGhostButton")
            view.setCursor(Qt.CursorShape.PointingHandCursor)
            view.clicked.connect(self.open_case_requested.emit)
            row.addWidget(view)
        else:
            save = QPushButton("\u25a3  Save to Notebook")
            save.setObjectName("ccPrimaryButton")
            save.setCursor(Qt.CursorShape.PointingHandCursor)
            save.clicked.connect(self.save_case_requested.emit)
            row.addWidget(save)
        return holder

    def _build_notebook_strip(self) -> QWidget:
        card = QFrame()
        card.setObjectName("ccJournalStrip")
        row = QHBoxLayout(card)
        row.setContentsMargins(16, 10, 16, 10)
        row.setSpacing(10)
        badge = QLabel()
        badge.setObjectName("panel")
        badge.setFixedSize(16, 16)
        badge.setPixmap(icons.to_pixmap(icons.draw("notebook", 16, Theme.token("BADGE_TEXT"))))
        row.addWidget(badge)
        row.addWidget(_label("Study Notebook:", "ccJournalTitle", wrap=False))
        row.addWidget(_label(
            "Save this run as a hypothetical case study, with a vignette, the vitals, "
            "the symptoms and the hallmark correlation, to annotate in your notebook.",
            "ccMuted"), 1)
        save = QPushButton("+ Save as case study")
        save.setObjectName("ccLinkButton")
        save.setCursor(Qt.CursorShape.PointingHandCursor)
        save.clicked.connect(self.save_case_requested.emit)
        row.addWidget(save)
        return card

    @property
    def last_result(self) -> Optional[CheckerResult]:
        return self._last_result

    def mark_saved(self) -> None:
        """Show "Saved to Notebook" until the inputs are cleared."""
        self._saved_case = True
        if self._last_result:
            self.show_result(self._last_result)

    def _build_view_switch(self) -> QWidget:
        card = QFrame()
        card.setObjectName("ccCard")
        row = QHBoxLayout(card)
        row.setContentsMargins(16, 10, 16, 10)
        row.setSpacing(10)
        row.addWidget(_label("Differential view:", "ccStrong", wrap=False))
        row.addWidget(_label("Switch between the side-by-side comparison matrix, the "
                             "detailed monographs, or both.", "ccMuted"), 1)

        toggle = QFrame()
        toggle.setObjectName("mdToggle")
        toggle_row = QHBoxLayout(toggle)
        toggle_row.setContentsMargins(4, 4, 4, 4)
        toggle_row.setSpacing(2)
        self._mode_group = QButtonGroup(self)
        self._mode_group.setExclusive(True)
        for key, text in (("both", "Both Views"), ("matrix", "Tabular Matrix"),
                          ("cards", "Detailed Cards")):
            button = QPushButton(text)
            button.setObjectName("mdToggleButton")
            button.setCheckable(True)
            button.setChecked(key == self._view_mode)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, k=key: self._set_mode(k))
            self._mode_group.addButton(button)
            toggle_row.addWidget(button)
        row.addWidget(toggle)
        return card

    def _set_mode(self, mode: str) -> None:
        self._view_mode = mode
        if self._last_result:
            self.show_result(self._last_result)

    def _toggle_card(self, disease_id: str) -> None:
        if disease_id in self._expanded:
            self._expanded.discard(disease_id)
        else:
            self._expanded.add(disease_id)
        if self._last_result:
            self.show_result(self._last_result)

    def _build_triage(self, result: CheckerResult) -> QWidget:
        danger = result.triage_level in ("EMERGENCY", "URGENT")
        card, layout = _card("", "alert", danger=danger)
        card.setProperty("triage", {"EMERGENCY": "bad", "URGENT": "warn",
                                    "PROMPT": "info"}.get(result.triage_level, "good"))

        head = QHBoxLayout()
        head.addWidget(_label("TRIAGE RECOMMENDATION", "ccLabel", wrap=False))
        head.addStretch(1)
        head.addWidget(_label(result.triage_level, "ccTriageTag", wrap=False))
        layout.addLayout(head)
        layout.addWidget(_label(result.triage_label, "ccTriageTitle"))

        detail = QHBoxLayout()
        detail.setSpacing(14)
        for caption, text in (("Recommended action", result.triage_action),
                              ("Why", result.triage_rationale)):
            box = QFrame()
            box.setObjectName("ccInnerBox")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(14, 10, 14, 10)
            box_layout.setSpacing(3)
            box_layout.addWidget(_label(caption.upper(), "ccFieldLabel", wrap=False))
            box_layout.addWidget(_label(text, "ccBody"))
            detail.addWidget(box, 1)
        layout.addLayout(detail)

        if result.emergency_warnings:
            layout.addWidget(_label("WARNING SIGNS TO MONITOR", "ccLabel", wrap=False))
            for sign in result.emergency_warnings[:4]:
                layout.addWidget(_label(f"\u2022  {sign}", "ccRedBody"))
        return card

    def _build_matrix(self, result: CheckerResult) -> QWidget:
        """One column per reported symptom, rule-in / rule-out per condition."""
        card, layout = _card("1. Clinical differential matrix (rule-in / rule-out)",
                             "stack", trailing="Cross-condition comparative evaluation")

        legend = QHBoxLayout()
        legend.setSpacing(14)
        for text, style in (("Expected / hallmark (rule-in)", "ccGood"),
                            ("Inconsistent (rule-out)", "ccBad"),
                            ("Not associated", "ccMuted")):
            legend.addWidget(_label(f"\u25cf  {text}", style, wrap=False))
        legend.addStretch(1)
        layout.addLayout(legend)

        names = self.selected_names()
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(7)
        headers = ["Candidate condition", *[n.upper() for n in names],
                   "Triage urgency", "Correlation score"]
        for column, caption in enumerate(headers):
            grid.addWidget(_label(caption.upper(), "ccFieldLabel", wrap=False), 0, column)

        for row, match in enumerate(result.matches, 1):
            cell = QVBoxLayout()
            cell.setSpacing(1)
            cell.addWidget(_label(f"#{row}  {match.name}", "ccMatrixName", wrap=False))
            if match.scientific_name:
                cell.addWidget(_label(match.scientific_name, "ccMatchSci", wrap=False))
            grid.addLayout(cell, row, 0)

            matched = {m.name: m for m in match.matched}
            for index, name in enumerate(names, start=1):
                entry = matched.get(name)
                if entry is not None:
                    text = "Hallmark" if entry.is_primary else "Present"
                    style = "ccPillGood"
                elif name in match.inconsistent:
                    text, style = "\u2715 Inconsistent", "ccPillBad"
                else:
                    text, style = "\u2014", "ccMuted"
                grid.addWidget(_label(text, style, wrap=False), row, index)

            urgency = _label(URGENCY_LABELS.get(match.urgency, "Not specified"),
                             "ccUrgencyPill", wrap=False)
            urgency.setProperty("urgency", match.urgency.lower() or "none")
            grid.addWidget(urgency, row, len(names) + 1)

            score = QVBoxLayout()
            score.setSpacing(2)
            score.addWidget(_label(f"{match.score:.0f}%", "ccMatrixScore", wrap=False))
            bar = QProgressBar()
            bar.setObjectName("ccScoreBar")
            bar.setRange(0, 100)
            bar.setValue(int(match.score))
            bar.setTextVisible(False)
            bar.setFixedHeight(3)
            bar.setFixedWidth(80)
            score.addWidget(bar)
            grid.addLayout(score, row, len(names) + 2)

        grid.setColumnStretch(0, 3)
        layout.addLayout(grid)
        return card

    def _clear_results(self) -> None:
        while self._results_host.count():
            item = self._results_host.takeAt(0)
            if item.widget():
                item.widget().hide()
                item.widget().deleteLater()

    def refresh_theme(self) -> None:
        self._icon.setPixmap(icons.to_pixmap(
            icons.draw("stethoscope", 26, Theme.token("PRIMARY"))))