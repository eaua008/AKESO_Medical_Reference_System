"""Symptom Correlation Engine: the assessment screen.

Three numbered steps, then a bar pinned to the bottom:

    1  SYMPTOMS   symptom picker | each chosen symptom's onset, pattern, trend,
                  duration and intensity (0-10 pain boxes for a pain, an
                  intensity slider for anything else); both columns have the
                  same fixed height and scroll on their own
                  associated symptoms worth adding
    2  CONTEXT    exposure | comorbidity | vitals | family history, age / sex
    3  RESULTS    triage, then the matrix and/or the detailed cards
    ==================================================================
    pinned bar:   "3 symptoms selected", the specificity meter, Reset, Calculate

Adding a fifth or sixth symptom scrolls its column instead of stretching the
page, and Calculate is always one click away.
"""

from typing import Optional

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QButtonGroup,
    QLayout,
    QCheckBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
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
from app.ui.views.compare_view import FlowLayout
from app.ui.components.fluid import ElidedLabel, HScrollArea, ResponsiveGrid, contain, fit_width
from app.ui.components.akeso_loader import MinimumLoading
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
        contain(self, limit=160, buttons=False)    # long names wrap on narrow windows
        for widget in self._one_line:               # but the score stays on one line
            widget.setWordWrap(False)

    def _build_head(self, match: MatchResult, rank: int, expanded: bool) -> QHBoxLayout:
        head = QHBoxLayout()
        head.setSpacing(10)
        centre = Qt.AlignmentFlag.AlignVCenter       # pills keep their height, not the row's
        head.addWidget(_label(f"#{rank}", "ccRank", wrap=False), 0, centre)
        head.addWidget(_label("PRIMARY DIFFERENTIAL" if rank == 1 else "DIFFERENTIAL MATCH",
                              "ccMatchTag", wrap=False), 0, centre)
        urgency = _label(URGENCY_LABELS.get(match.urgency, "Not specified"),
                         "ccUrgencyPill", wrap=False)
        urgency.setProperty("urgency", match.urgency.lower() or "none")
        head.addWidget(urgency, 0, centre)

        names = QVBoxLayout()
        names.setSpacing(1)
        names.addWidget(_label(match.name, "ccMatchName", wrap=False))
        if match.scientific_name:
            names.addWidget(_label(match.scientific_name, "ccMatchSci", wrap=False))
        head.addLayout(names, 1)

        # The two weighted values the ranking really uses, then the plain
        # counts. Hover for the full breakdown (hallmarks, intensity, boosters).
        # An open card already shows this working in its body, so the hover
        # text only appears on a closed one, and says what it is.
        why = "" if expanded else "Why it ranks here:\n" + "\n".join(match.why())
        score = QVBoxLayout()
        score.setSpacing(2)
        headline = _label(f"covers {match.coverage:.0%} \u00b7 explains {match.explained:.0%}",
                          "ccMatrixScore", wrap=False)
        headline.setToolTip(why)
        self._one_line = [headline]
        score.addWidget(headline, 0, Qt.AlignmentFlag.AlignRight)
        counts = _label(f"{match.matched_count}/{match.total_hallmarks} of its symptoms \u00b7 "
                        f"{match.explained_count}/{match.reported_count} of yours"
                        + ("  \u2191 boosted" if match.boosters else ""),
                        "ccMuted", wrap=False)
        counts.setToolTip(why)
        self._one_line.append(counts)
        score.addWidget(counts, 0, Qt.AlignmentFlag.AlignRight)
        bar = QProgressBar()
        bar.setToolTip(why)
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
        head.addWidget(chevron, 0, centre)
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
        # Why it ranks where it does, in the same numbers the ranking uses.
        for line in match.why():
            if not line.startswith("Boosters:"):      # listed in the box below
                reasoning_layout.addWidget(_label(line, "ccBody"))
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
    unlink_requested = Signal()         # stop saving into the linked note
    sync_requested = Signal()           # "Sync with encyclopedias"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._symptoms: list[Symptom] = []
        self._selected: dict[str, SelectedSymptom] = {}
        self._param_cards: dict[str, SymptomParameters] = {}
        self._rows: list[SymptomRow] = []
        self._expanded: set[str] = set()
        self._collapsed: set[str] = set()       # the #1 card, closed by the user
        self._match_cards: dict = {}
        self._view_mode = "both"
        self._mode_buttons: dict = {}
        self._matrix_view: Optional[QWidget] = None
        self._results_anchor: Optional[QWidget] = None
        self._last_result: Optional[CheckerResult] = None
        self._saved_case = False
        self._link_title = ""

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        page = QWidget()
        page.setObjectName("panel")
        self._page = QVBoxLayout(page)
        self._page.setContentsMargins(30, 22, 30, 24)
        self._page.setSpacing(14)

        self._page.addWidget(self._build_header())
        self._page.addWidget(self._build_link_bar())
        self._page.addWidget(self._build_disclaimer())
        self._page.addWidget(self._step("1", "Symptoms", "Pick what is present, then set how "
                                        "each one started, its pattern and how strong it is."))
        self._page.addWidget(self._build_selection())
        self._page.addWidget(self._build_suggestions())
        self._page.addWidget(self._step("2", "Context", "Optional. Exposures, history, vitals "
                                        "and family risk adjust the ranking."))
        self._page.addWidget(self._build_four_columns())
        self._page.addWidget(self._build_demographics())
        self._page.addWidget(self._step("3", "Results", ""))
        self._results_empty = _label("Press Calculate in the bar below to rank the conditions "
                                     "for these symptoms.", "ccMuted")
        self._page.addWidget(self._results_empty)

        self._results_host = QVBoxLayout()
        self._results_host.setSpacing(14)
        self._page.addLayout(self._results_host)
        self._page.addStretch(1)

        self._scroll.setWidget(page)
        self._four_columns.watch(self._scroll.viewport())
        root.addWidget(self._scroll, 1)
        root.addWidget(self._build_action_bar())
        self._update_count()

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
        title.addStretch(1)
        text.addLayout(title)
        text.addWidget(_label(
            "Rule-based weighted matching consuming standardized clinical "
            "parameters (onset, pattern, exposures, vitals).", "pageSubtitle"))
        row.addLayout(text, 1)
        self.refresh_theme()
        return header

    @staticmethod
    def _step(number: str, title: str, hint: str) -> QWidget:
        """A numbered step heading: "1  SYMPTOMS  Pick what is present..."."""
        holder = QWidget()
        holder.setObjectName("panel")
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 8, 0, 0)
        row.setSpacing(10)
        badge = _label(number, "ccStepNumber", wrap=False)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFixedSize(26, 26)
        row.addWidget(badge, 0, Qt.AlignmentFlag.AlignVCenter)
        row.addWidget(_label(title.upper(), "ccSectionTitle", wrap=False), 0,
                      Qt.AlignmentFlag.AlignVCenter)
        if hint:
            row.addWidget(_label(hint, "ccMuted"), 1, Qt.AlignmentFlag.AlignVCenter)
        else:
            row.addStretch(1)
        return holder

    def _build_action_bar(self) -> QWidget:
        """Pinned under the page: what is selected, the specificity meter,
        Reset and Calculate, so the main action never needs a scroll."""
        bar = QFrame()
        bar.setObjectName("ccActionBar")
        bar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        row = QHBoxLayout(bar)
        row.setContentsMargins(30, 10, 30, 10)
        row.setSpacing(12)
        self._count_text = _label("", "ccStrong", wrap=False)
        row.addWidget(self._count_text)
        row.addSpacing(6)
        row.addWidget(_label("SPECIFICITY", "ccLabel", wrap=False))
        self._spec_badge = _label("\u2014", "ccSpecBadge", wrap=False)
        row.addWidget(self._spec_badge)
        self._spec_bar = QProgressBar()
        self._spec_bar.setObjectName("ccSpecBar")
        self._spec_bar.setRange(0, 100)
        self._spec_bar.setValue(0)
        self._spec_bar.setTextVisible(False)
        self._spec_bar.setFixedSize(120, 5)
        row.addWidget(self._spec_bar, 0, Qt.AlignmentFlag.AlignVCenter)
        self._spec_text = ElidedLabel("Add symptoms to begin.", "ccMuted")
        self._spec_text.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        row.addWidget(self._spec_text, 1)

        reset = QPushButton("\u21ba  Reset")
        reset.setObjectName("ccGhostButton")
        reset.setCursor(Qt.CursorShape.PointingHandCursor)
        reset.clicked.connect(self.reset_requested.emit)
        row.addWidget(reset)
        self.calculate = QPushButton("\u26a1  Calculate matches")
        self.calculate.setObjectName("ccPrimaryButton")
        self.calculate.setFixedHeight(38)
        self.calculate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calculate.setToolTip("Rank the conditions for the symptoms and context above")
        self.calculate.clicked.connect(self.calculate_requested.emit)
        row.addWidget(self.calculate)
        return bar

    def _update_count(self) -> None:
        n = len(self._selected)
        self._count_text.setText("No symptoms selected" if not n else
                                 f"{n} symptom{'s' if n != 1 else ''} selected")

    @staticmethod
    def _build_disclaimer() -> QWidget:
        box = QFrame()
        box.setObjectName("ccDisclaimer")
        layout = QHBoxLayout(box)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)
        layout.addWidget(_label("For study only:", "ccDisclaimerTitle", wrap=False))
        layout.addWidget(_label(
            "Akeso is an educational study tool, not a medical device. The checker "
            "lists conditions to study from the symptoms you enter; it does not "
            "diagnose real patients, and any treatment or medicine it links to is "
            "a study note, not a prescription. For a real person, see a licensed "
            "clinician. In an emergency, call 911 or go to the nearest emergency "
            "department.",
            "ccDisclaimerText"), 1)
        return box

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
        # The checker works from the Symptom and Disease encyclopedias on this
        # computer; Sync downloads the latest of both.
        search_row = QHBoxLayout()
        search_row.setSpacing(8)
        search_row.addWidget(self._search, 1)
        sync = QPushButton("Sync")
        sync.setObjectName("secondaryButton")
        sync.setFixedHeight(36)
        sync.setCursor(Qt.CursorShape.PointingHandCursor)
        sync.setToolTip("Sync with the encyclopedias: download the latest symptoms and "
                        "diseases the checker uses")
        sync.clicked.connect(lambda _c=False: self.sync_requested.emit())
        search_row.addWidget(sync)
        picker_layout.addLayout(search_row)

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
        fit_width(self._list_scroll)       # never wider than its panel
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
        fit_width(self._params_scroll)
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
                               "ccSuggestTitle"))
        self._suggest_sub = _label("Choose symptoms to see what commonly occurs with them.",
                                   "ccSuggestSub")
        title.addWidget(self._suggest_sub)
        head.addLayout(title, 1)
        head.addWidget(_label("RULE-BASED CROSS-DISEASE QUERY", "ccCrossQuery", wrap=False))
        layout.addLayout(head)

        # Chips wrap onto new lines. In a single row, five or six long
        # suggestions pushed the whole page past the right edge.
        holder = QWidget()
        holder.setObjectName("panel")
        self._suggest_row = FlowLayout(8, 8)
        holder.setLayout(self._suggest_row)
        layout.addWidget(holder)
        self._suggest_card = card
        return card

    def _build_four_columns(self) -> QWidget:
        # Four across on a wide window, two by two on a narrower one (four
        # fixed columns needed ~1,330 px and ran off smaller screens).
        holder = ResponsiveGrid(300, 4, spacing=14, steps=(4, 2, 1))
        self._four_columns = holder
        cards: list[QWidget] = []

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
        cards.append(exposure)

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
        cards.append(history)

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
        cards.append(vitals)

        # 4. family history
        family, family_layout = _card("Family & hereditary risk", "user",
                                      trailing="1st degree")
        family_host = QWidget()
        family_host.setObjectName("panel")
        family_inner = QVBoxLayout(family_host)
        family_inner.setContentsMargins(0, 0, 0, 0)
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
        family_layout.addWidget(family_host)
        cards.append(family)

        self._update_temp_status()
        holder.set_cards(cards)
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

    # ------------------------------------------------------------- syncing

    def begin_sync(self) -> None:
        """The Akeso loader over the checker while both encyclopedias sync."""
        if getattr(self, "_sync_gate", None) is None:
            self._sync_gate = MinimumLoading(self, "Syncing with the encyclopedias\u2026")
        self._sync_gate.begin()

    def end_sync(self, message: str = "") -> None:
        gate = getattr(self, "_sync_gate", None)
        if gate is not None:
            gate.finish(message=message)

    def syncing(self) -> bool:
        gate = getattr(self, "_sync_gate", None)
        return gate is not None and gate.active

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
            contain(row, limit=200, buttons=False)     # long names wrap
            self._list_layout.insertWidget(self._list_layout.count() - 1, row)
            self._rows.append(row)

        if not self._rows and query:
            self._list_layout.insertWidget(0, _label("No symptom matches that search.", "ccMuted"))
        elif not self._rows:
            # Nothing downloaded yet on this computer: say why, and offer the fix.
            empty = QWidget()
            empty.setObjectName("panel")
            box = QVBoxLayout(empty)
            box.setContentsMargins(0, 8, 0, 0)
            box.setSpacing(8)
            box.addWidget(_label(
                "The symptom list is not on this computer yet. The Symptom Checker "
                "uses the Symptom and Disease encyclopedias, so it needs one sync "
                "first.", "ccMuted"))
            button = QPushButton("Sync with encyclopedias")
            button.setObjectName("primaryButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False: self.sync_requested.emit())
            box.addWidget(button, 0, Qt.AlignmentFlag.AlignLeft)
            self._list_layout.insertWidget(0, empty)

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
            # A long symptom name wraps instead of pushing the panel wider
            # ("Signs of dehydration (sunken eyes, dry mouth, intense thirst)").
            contain(card, limit=200, buttons=False)
            self._params_layout.addWidget(card)
            self._param_cards[entry.symptom_id] = card

        self._params_layout.addWidget(self._no_params)
        self._no_params.setVisible(not self._selected)
        self._params_layout.addStretch(1)
        if hasattr(self, "_count_text"):
            self._update_count()

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

    def clear(self) -> None:
        """Reset: every input back to its starting value, not only the symptoms
        (history, exposures, vitals, demographics and the specificity meter too)."""
        self._selected.clear()
        self._expanded.clear()
        self._collapsed.clear()
        self._last_result = None
        self._saved_case = False
        self._view_mode = "both"
        self._search.blockSignals(True)
        self._search.clear()
        self._search.blockSignals(False)
        for box in (*self._exposure_boxes.values(), *self._comorbidity_boxes.values(),
                    *self._family_boxes.values()):
            box.setChecked(False)
        self._no_history.setChecked(True)
        for button in self._unit_group.buttons():
            button.setChecked(button.text() == "\u00b0C")
        self._set_unit("\u00b0C")
        self.temperature.setValue(37.0)
        self.heart_rate.setValue(88)
        self.bp_systolic.setValue(120)
        self.bp_diastolic.setValue(80)
        self.spo2.setValue(98)
        self.resp_rate.setValue(18)
        self.age.setValue(29)
        self.sex.setCurrentIndex(max(0, self.sex.findData("female")))
        self._spec_badge.setText("\u2014")
        self._spec_badge.setProperty("level", None)
        self._spec_badge.style().unpolish(self._spec_badge)
        self._spec_badge.style().polish(self._spec_badge)
        self._spec_bar.setValue(0)
        self._spec_text.setText("Add symptoms to begin.")
        self._render_symptom_list()
        self._render_parameters()
        self.show_suggestions([])
        self._clear_results()
        self._scroll.verticalScrollBar().setValue(0)

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
            self._results_empty.hide()
            return

        self._results_anchor = self._build_results_header(result)
        self._results_host.addWidget(self._results_anchor)
        self._results_empty.hide()
        self._results_host.addWidget(self._build_triage(result))
        if result.vital_alerts:
            alerts, alerts_layout = _card("Objective findings", "pulse")
            for alert in result.vital_alerts:
                alerts_layout.addWidget(_label(f"\u2022  {alert}", "ccBody"))
            self._results_host.addWidget(alerts)

        self._results_host.addWidget(self._build_view_switch())
        # Both views are built once; the switch only shows or hides them, so
        # changing view never rebuilds the page or moves the scroll position.
        self._matrix_view = self._build_matrix(result)
        self._results_host.addWidget(self._matrix_view)
        self._cards_title = _label("2. DETAILED CLINICAL DIFFERENTIAL MONOGRAPHS & CARDS",
                                   "ccSectionTitle", wrap=False)
        self._results_host.addWidget(self._cards_title)
        for rank, match in enumerate(result.matches, 1):
            self._results_host.addWidget(self._make_match_card(match, rank))
        self._apply_view_mode()

    def _is_open(self, disease_id: str, rank: int) -> bool:
        if rank == 1:
            return disease_id not in self._collapsed
        return disease_id in self._expanded

    def _make_match_card(self, match: MatchResult, rank: int) -> MatchCard:
        card = MatchCard(match, rank, expanded=self._is_open(match.disease_id, rank))
        card.open_requested.connect(self.disease_requested.emit)
        card.toggled.connect(self._toggle_card)
        self._match_cards[match.disease_id] = (card, match, rank)
        return card

    def _apply_view_mode(self) -> None:
        show_matrix = self._view_mode in ("both", "matrix")
        show_cards = self._view_mode in ("both", "cards")
        if self._matrix_view is not None:
            self._matrix_view.setVisible(show_matrix)
            self._cards_title.setVisible(show_cards)
            for card, _match, _rank in self._match_cards.values():
                card.setVisible(show_cards)
        button = self._mode_buttons.get(self._view_mode)
        if button is not None:
            button.setChecked(True)

    def reveal_results(self) -> None:
        """After Calculate, scroll down to the results (once the new widgets
        have their size), so nobody has to scroll to find them."""
        def scroll() -> None:
            anchor = self._results_anchor
            if anchor is None:
                return
            top = anchor.mapTo(self._scroll.widget(), anchor.rect().topLeft()).y()
            self._scroll.verticalScrollBar().setValue(max(0, top - 12))
        QTimer.singleShot(60, scroll)

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
            save = QPushButton(f"\u25a3  Save to \u201c{self._link_title}\u201d"
                               if self._link_title else "\u25a3  Save to Notebook")
            save.setObjectName("ccPrimaryButton")
            save.setCursor(Qt.CursorShape.PointingHandCursor)
            save.setToolTip("Save this run as a hypothetical case study (vignette, vitals, "
                            "symptoms and the hallmark correlation) to annotate in your notebook")
            save.clicked.connect(self.save_case_requested.emit)
            row.addWidget(save)
        return holder

    # ------------------------------------------------- linked to a note

    def _build_link_bar(self) -> QWidget:
        """Shown when the checker was opened from a note in the Study
        Notebook: saving then updates that note instead of making a new one."""
        self._link_bar = QFrame()
        self._link_bar.setObjectName("ccJournalStrip")
        row = QHBoxLayout(self._link_bar)
        row.setContentsMargins(16, 10, 16, 10)
        row.setSpacing(10)
        row.addWidget(_label("Linked to your notebook:", "ccJournalTitle", wrap=False))
        self._link_text = _label("", "ccMuted")
        row.addWidget(self._link_text, 1)
        unlink = QPushButton("Unlink")
        unlink.setObjectName("ccLinkButton")
        unlink.setCursor(Qt.CursorShape.PointingHandCursor)
        unlink.clicked.connect(self.unlink_requested.emit)
        row.addWidget(unlink)
        self._link_bar.hide()
        return self._link_bar

    def set_link(self, title: str) -> None:
        self._link_title = title
        self._link_text.setText(
            f"\u201c{title}\u201d. Save to Notebook updates that note." if title else "")
        self._link_bar.setVisible(bool(title))
        if self._last_result:
            self.show_result(self._last_result)

    def load_input(self, data: CheckerInput) -> None:
        """Fill the form from a saved case, so it can be edited and re-run."""
        self.clear()
        for entry in data.symptoms:
            self._selected[entry.symptom_id] = entry
        self._render_symptom_list()
        self._render_parameters()
        v = data.vitals
        self.temperature.setValue(v.temperature if self.temperature.maximum() <= 50
                                  else v.temperature * 9 / 5 + 32)
        self.heart_rate.setValue(v.heart_rate)
        self.bp_systolic.setValue(v.bp_systolic)
        self.bp_diastolic.setValue(v.bp_diastolic)
        self.spo2.setValue(v.spo2)
        self.resp_rate.setValue(v.resp_rate)
        self.age.setValue(data.age)
        self.sex.setCurrentIndex(max(0, self.sex.findData(data.sex)))
        for key, box in self._exposure_boxes.items():
            box.setChecked(key in data.exposures)
        self._no_history.setChecked(not data.comorbidities)
        for key, box in self._comorbidity_boxes.items():
            box.setChecked(key in data.comorbidities)
        for key, box in self._family_boxes.items():
            box.setChecked(key in data.family_history)
        self.symptoms_changed.emit()

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
        self._mode_group = QButtonGroup(card)
        self._mode_group.setExclusive(True)
        self._mode_buttons = {}
        for key, text in (("both", "Both Views"), ("matrix", "Tabular Matrix"),
                          ("cards", "Detailed Cards")):
            button = QPushButton(text)
            button.setObjectName("mdToggleButton")
            button.setCheckable(True)
            button.setChecked(key == self._view_mode)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, k=key: self._set_mode(k))
            self._mode_group.addButton(button)
            self._mode_buttons[key] = button
            toggle_row.addWidget(button)
        row.addWidget(toggle)
        return card

    def _set_mode(self, mode: str) -> None:
        self._view_mode = mode
        self._apply_view_mode()

    def _toggle_card(self, disease_id: str) -> None:
        """Open or close one card in place. Only that card is rebuilt, and the
        view stays on its header instead of jumping to the bottom."""
        entry = self._match_cards.get(disease_id)
        if entry is None:
            return
        old, match, rank = entry
        opening = not self._is_open(disease_id, rank)
        if opening:
            self._collapsed.discard(disease_id)
            self._expanded.add(disease_id)
        else:
            self._expanded.discard(disease_id)
            self._collapsed.add(disease_id)

        bar = self._scroll.verticalScrollBar()
        keep = bar.value()
        new = self._make_match_card(match, rank)
        new.setVisible(self._view_mode in ("both", "cards"))
        self._results_host.replaceWidget(old, new)
        old.hide()
        old.deleteLater()
        bar.setValue(keep)

        def settle() -> None:
            top = new.mapTo(self._scroll.widget(), new.rect().topLeft()).y()
            if top < bar.value() or top > bar.value() + self._scroll.viewport().height() - 60:
                bar.setValue(max(0, top - 12))
            else:
                bar.setValue(keep)
        QTimer.singleShot(0, settle)
        self._fade_in(new)

    @staticmethod
    def _fade_in(card: QWidget) -> None:
        """Ease a freshly opened or closed card in instead of snapping."""
        effect = QGraphicsOpacityEffect(card)
        effect.setOpacity(0.0)
        card.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity", card)
        anim.setDuration(220)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.finished.connect(lambda: card.setGraphicsEffect(None))
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

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

    # Matrix geometry. Every row has the same fixed height so the three
    # parts (pinned conditions | scrolling symptoms | pinned triage & match)
    # stay lined up.
    MX_ROW, MX_HEAD = 58, 70
    MX_NAME_W, MX_SYMPTOM_W, MX_TRIAGE_W, MX_MATCH_W = 250, 140, 150, 220

    def _build_matrix(self, result: CheckerResult) -> QWidget:
        """Every ranked condition as a row, every reported symptom as a column.

        All conditions are listed, not just the top few: a low match can still
        be the one that matters. The condition names stay pinned on the left
        and triage + match on the right; only the symptom columns scroll
        sideways (drag the bar under the table, or Shift + mouse wheel).
        """
        matches = result.matches
        card, layout = _card("1. Clinical differential matrix", "stack",
                             trailing=f"All {len(matches)} ranked conditions")

        legend = QHBoxLayout()
        legend.setSpacing(14)
        for text, style in (("\u25cf  Hallmark / present: listed for this condition", "ccGood"),
                            ("\u2014 not linked: this condition's entry does not list it", "ccMuted"),
                            ("\u2191 a risk-factor booster applied", "ccMuted")):
            legend.addWidget(_label(text, style, wrap=False))
        legend.addStretch(1)
        layout.addLayout(legend)

        names = self.selected_names()

        def cell(width: Optional[int], head: bool = False,
                 grow: bool = False) -> tuple[QWidget, QHBoxLayout]:
            box = QWidget()
            box.setObjectName("ccMxHead" if head else "ccMxCell")
            box.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            box.setFixedHeight(self.MX_HEAD if head else self.MX_ROW)
            if width and grow:
                box.setMinimumWidth(width)      # wider when there is room, no empty gap
            elif width:
                box.setFixedWidth(width)
            row = QHBoxLayout(box)
            row.setContentsMargins(8, 4, 8, 4)
            row.setSpacing(6)
            return box, row

        def column(object_name: str, width: int) -> tuple[QWidget, QVBoxLayout]:
            holder = QWidget()
            holder.setObjectName(object_name)
            holder.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            holder.setFixedWidth(width)
            stack = QVBoxLayout(holder)
            stack.setContentsMargins(0, 0, 0, 0)
            stack.setSpacing(0)
            return holder, stack

        # ---- left, pinned: the conditions
        left, left_stack = column("ccMxPinLeft", self.MX_NAME_W)
        box, row = cell(self.MX_NAME_W, head=True)
        row.addWidget(_label("CANDIDATE CONDITION", "ccFieldLabel"), 1, Qt.AlignmentFlag.AlignBottom)
        left_stack.addWidget(box)
        for rank, match in enumerate(matches, 1):
            box, row = cell(self.MX_NAME_W)
            name = _label(f"#{rank}  {match.name}", "ccMatrixName")
            name.setToolTip(match.scientific_name or match.name)
            row.addWidget(name, 1)
            left_stack.addWidget(box)
        left_stack.addStretch(1)

        # ---- middle, scrolls sideways: one column per reported symptom
        grid_host = QWidget()
        grid_host.setObjectName("panel")
        grid = QGridLayout(grid_host)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        for index, symptom_name in enumerate(names):
            box, row = cell(self.MX_SYMPTOM_W, head=True, grow=True)
            head = _label(symptom_name.upper(), "ccFieldLabel")
            head.setToolTip(symptom_name)
            row.addWidget(head, 1, Qt.AlignmentFlag.AlignBottom)
            grid.addWidget(box, 0, index)
        for rank, match in enumerate(matches, 1):
            matched = {m.name: m for m in match.matched}
            for index, symptom_name in enumerate(names):
                box, row = cell(self.MX_SYMPTOM_W, grow=True)
                entry = matched.get(symptom_name)
                if entry is not None:
                    pill = _label("Hallmark" if entry.is_primary else "Present",
                                  "ccPillGood", wrap=False)
                    pill.setToolTip(f"Your intensity {entry.user_intensity}/10, typical "
                                    f"{entry.typical_intensity}/10 in {match.name}")
                    row.addWidget(pill, 0, Qt.AlignmentFlag.AlignVCenter)
                else:
                    dash = _label("\u2014", "ccMuted", wrap=False)
                    dash.setToolTip(f"Not linked: the {match.name} entry does not list "
                                    f"{symptom_name}")
                    row.addWidget(dash, 0, Qt.AlignmentFlag.AlignVCenter)
                row.addStretch(1)
                grid.addWidget(box, rank, index)
        for index in range(len(names)):             # spare width shared by the columns
            grid.setColumnStretch(index, 1)
        # Spare height goes below the last row, never between rows, so every
        # row stays level with its condition name on the left.
        grid.setRowStretch(len(matches) + 1, 1)
        middle = HScrollArea()
        middle.setObjectName("ccMxScroll")
        middle.setWidget(grid_host)
        # Exactly header + one fixed-height row per condition (+ the scroll bar).
        # Asking the grid for its height here came back too short when there
        # were many conditions, which cut off the last rows (#10, #11 showed
        # no cells at all).
        # setFixedHeight itself scales by the 80% / 90% size (soft_scale), so it
        # gets the unscaled height: passing an already-scaled one shrank the
        # table twice and cut off the last rows at 80%.
        import math
        from app.core import soft_scale
        real = (soft_scale.px(self.MX_HEAD) + len(matches) * soft_scale.px(self.MX_ROW)
                + middle.horizontalScrollBar().sizeHint().height() + 4)
        middle.setFixedHeight(math.ceil(real / soft_scale.FACTOR) + 1)

        # ---- right, pinned: triage and match
        right, right_stack = column("ccMxPinRight", self.MX_TRIAGE_W + self.MX_MATCH_W)
        box, row = cell(None, head=True)
        triage_head = _label("TRIAGE URGENCY", "ccFieldLabel")
        triage_head.setFixedWidth(self.MX_TRIAGE_W - 14)
        row.addWidget(triage_head, 0, Qt.AlignmentFlag.AlignBottom)
        row.addWidget(_label("MATCH  (hover for the working)", "ccFieldLabel"), 1,
                      Qt.AlignmentFlag.AlignBottom)
        right_stack.addWidget(box)
        for match in matches:
            box, row = cell(None)
            urgency = _label(URGENCY_LABELS.get(match.urgency, "Not specified"),
                             "ccUrgencyPill", wrap=False)
            urgency.setProperty("urgency", match.urgency.lower() or "none")
            urgency_slot = QWidget()
            urgency_slot.setObjectName("ccMxSlot")
            urgency_slot.setFixedWidth(self.MX_TRIAGE_W - 14)
            slot = QHBoxLayout(urgency_slot)
            slot.setContentsMargins(0, 0, 0, 0)
            slot.addWidget(urgency, 0, Qt.AlignmentFlag.AlignVCenter)
            slot.addStretch(1)
            row.addWidget(urgency_slot)

            why = "Why it ranks here:\n" + "\n".join(match.why())
            score = QVBoxLayout()
            score.setSpacing(1)
            headline = _label(f"covers {match.coverage:.0%} \u00b7 explains {match.explained:.0%}"
                              + ("  \u2191" if match.boosters else ""),
                              "ccMatrixScore", wrap=False)
            counts = _label(f"{match.matched_count}/{match.total_hallmarks} of its \u00b7 "
                            f"{match.explained_count}/{match.reported_count} of yours",
                            "ccMuted", wrap=False)
            bar = QProgressBar()
            bar.setObjectName("ccScoreBar")
            bar.setRange(0, 100)
            bar.setValue(int(match.score))
            bar.setTextVisible(False)
            bar.setFixedHeight(3)
            bar.setMaximumWidth(150)
            for widget in (headline, counts, bar):
                widget.setToolTip(why)
                score.addWidget(widget)
            row.addLayout(score)
            row.addStretch(1)       # keep every row's content left-aligned
            right_stack.addWidget(box)
        right_stack.addStretch(1)

        table = QHBoxLayout()
        table.setSpacing(0)
        table.addWidget(left, 0, Qt.AlignmentFlag.AlignTop)
        table.addWidget(middle, 1, Qt.AlignmentFlag.AlignTop)
        table.addWidget(right, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(table)
        layout.addWidget(_label(
            "Ranked by the weighted values, not the counts: hallmark symptoms, how "
            "specific each symptom is, the intensity you reported and any risk factors "
            "all count. Hover a Match cell for the full working. Scroll the symptom "
            "columns with the bar under the table or Shift + mouse wheel.", "ccMuted"))
        return card

    def _clear_results(self) -> None:
        self._results_empty.show()
        self._matrix_view = None
        self._results_anchor = None
        self._match_cards = {}
        while self._results_host.count():
            item = self._results_host.takeAt(0)
            if item.widget():
                item.widget().hide()
                item.widget().deleteLater()

    def refresh_theme(self) -> None:
        self._icon.setPixmap(icons.to_pixmap(
            icons.draw("stethoscope", 26, Theme.token("PRIMARY"))))