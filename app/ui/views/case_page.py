"""Step 7: the Case column (left) — a saved case, read-only.

Symptom case:
    chips (age range, sex, setting, difficulty) · chief complaint ·
    case presentation · reported symptoms · recorded vitals ·
    hallmark correlation (Matrix | Cards) · answer key (hidden) ·
    learning objectives
Interaction case:
    candidate, regimen, comorbidities · verdict · every finding as a table

The findings are worked out again from today's reference data each time
the page is built (see CaseReference); nothing here is stored.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.interaction_styles import tone_color
from app.models.checker import DURATIONS, ONSETS, PATTERNS, TRENDS, CheckerResult
from app.models.notebook import NotebookItem
from app.services.case_reference import correlation_table, label_lists, vitals_flags
from app.services.notebook_service import HYPOTHETICAL_NOTE
from app.services.reference_library import URGENCY_LABELS
from app.models.checker import Vitals
from app.ui.views.interaction_widgets import FlowLayout

MAX_CONDITIONS = 8


def _label(text: str, name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text, objectName=name)
    label.setWordWrap(wrap)
    return label


def _repolish(widget: QWidget) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)


class CasePage(QWidget):
    insert_table = Signal(str, list, list)            # caption, headers, rows
    summary_requested = Signal()                      # "Add case summary to my notes"
    open_reference = Signal(str, str, str)            # kind, id, name
    edit_requested = Signal()
    open_checker = Signal()                           # edit in Drug Interaction Checker
    open_symptom_checker = Signal()                   # edit in Symptom Checker

    def __init__(self, item: NotebookItem, symptom_result: Optional[CheckerResult] = None,
                 interaction: Optional[dict] = None, answer_name: str = "") -> None:
        super().__init__()
        self.setObjectName("panel")
        self.item = item
        self._result = symptom_result
        self._mode = "matrix"
        self._revealed = False
        self._answer_name = answer_name

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        host = QWidget()
        host.setObjectName("panel")
        self._col = QVBoxLayout(host)
        self._col.setContentsMargins(14, 12, 14, 18)
        self._col.setSpacing(12)
        scroll.setWidget(host)
        outer.addWidget(scroll)

        self._col.addWidget(self._disclaimer())
        summary = QPushButton("  Add case summary to my notes")
        summary.setObjectName("nbInsertButton")
        summary.setCursor(Qt.CursorShape.PointingHandCursor)
        summary.setIcon(lucide.icon("arrow-down-to-line", 13, tone_color("primary")))
        summary.setToolTip("Writes the case (presentation, symptoms, vitals, findings) into "
                           "the open note, without the answer key")
        summary.clicked.connect(self.summary_requested.emit)
        self._col.addWidget(summary, 0, Qt.AlignmentFlag.AlignLeft)
        # A note can carry both runs; a case carries its own.
        if item.symptom_data.get("symptoms"):
            self._build_symptom()
        if item.interaction_data.get("candidate_id"):
            self._build_interaction(interaction)
        self._col.addStretch(1)

    # ------------------------------------------------------------- helpers

    @staticmethod
    def _disclaimer() -> QWidget:
        box = QFrame()
        box.setObjectName("nbNoteBox")
        row = QHBoxLayout(box)
        row.setContentsMargins(10, 7, 10, 7)
        row.setSpacing(8)
        icon = QLabel()
        icon.setPixmap(lucide.pixmap("info", 13, tone_color("primary")))
        row.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)
        row.addWidget(_label(HYPOTHETICAL_NOTE, "nbSmallMuted"), 1)
        return box

    def _section(self, icon: str, title: str, reference: bool = False) -> QVBoxLayout:
        frame = QFrame()
        frame.setObjectName("nbSection")
        col = QVBoxLayout(frame)
        col.setContentsMargins(12, 10, 12, 12)
        col.setSpacing(8)
        head = QHBoxLayout()
        head.setSpacing(7)
        glyph = QLabel()
        glyph.setPixmap(lucide.pixmap(icon, 14, tone_color("primary")))
        head.addWidget(glyph)
        head.addWidget(_label(title, "nbSectionTitle", wrap=False))
        head.addStretch(1)
        if reference:
            lock = QLabel()
            lock.setPixmap(lucide.pixmap("lock", 11, tone_color("muted")))
            head.addWidget(lock)
            head.addWidget(_label("Reference", "nbLockLabel", wrap=False))
        col.addLayout(head)
        self._col.addWidget(frame)
        return col

    @staticmethod
    def _chips(values: list[str], name: str = "nbChip") -> QWidget:
        host = QWidget()
        host.setObjectName("panel")
        flow = FlowLayout(host, spacing=6)
        for value in values:
            flow.addWidget(QLabel(value, objectName=name))
        return host

    def _link(self, text: str, kind: str, item_id: str) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("nbLinkChip")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setToolTip("Open in the Reference column")
        button.clicked.connect(lambda: self.open_reference.emit(kind, item_id, text))
        return button

    def _insert_button(self, action) -> QPushButton:
        button = QPushButton("  Insert as table into notes")
        button.setObjectName("nbInsertButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setIcon(lucide.icon("arrow-down-to-line", 13, tone_color("primary")))
        button.clicked.connect(action)
        return button

    # ======================================================== symptom case

    def _build_symptom(self) -> None:
        case = self.item.symptom_data
        sexes = {"female": "Female", "male": "Male"}
        chips = [f"{case.get('age_range', '?')} y/o", sexes.get(case.get("sex", ""), "Sex not set")]
        if case.get("setting"):
            chips.append(case["setting"])
        if case.get("difficulty"):
            chips.append(case["difficulty"])
        self._col.addWidget(self._chips(chips))

        if case.get("chief_complaint"):
            col = self._section("text-quote", "Chief complaint")
            col.addWidget(_label(f"“{case['chief_complaint']}”", "nbQuote"))

        col = self._section("file-text", "Case presentation & history")
        if case.get("vignette"):
            col.addWidget(_label(case["vignette"], "nbBody"))
        else:
            col.addWidget(_label("No vignette yet. Use Edit case details to write one.",
                                 "nbSmallMuted"))

        self._symptoms_table()
        self._vitals()

        lists = label_lists(case)
        extra = [(title, values) for title, values in (
            ("Exposures", lists["exposures"]), ("Comorbidities", lists["comorbidities"]),
            ("Family history", lists["family_history"])) if values]
        if extra:
            col = self._section("layers", "Context")
            for title, values in extra:
                col.addWidget(_label(title, "nbFieldLabel"))
                col.addWidget(self._chips(values))

        self._correlation()
        self._answer_key()

        objectives = [o for o in case.get("objectives", []) if o.strip()]
        col = self._section("target", "Learning objectives")
        if objectives:
            for objective in objectives:
                col.addWidget(_label(f"•  {objective}", "nbBody"))
        else:
            col.addWidget(_label("None set yet.", "nbSmallMuted"))

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        edit = QPushButton("  Edit case details")
        edit.setObjectName("nbButton")
        edit.setCursor(Qt.CursorShape.PointingHandCursor)
        edit.setIcon(lucide.icon("pencil", 14, tone_color("text")))
        edit.clicked.connect(self.edit_requested.emit)
        buttons.addWidget(edit)
        rerun = QPushButton("  Edit in Symptom Checker")
        rerun.setObjectName("nbButton")
        rerun.setCursor(Qt.CursorShape.PointingHandCursor)
        rerun.setIcon(lucide.icon("activity", 14, tone_color("text")))
        rerun.setToolTip("Change the symptoms, vitals or history; saving updates this case")
        rerun.clicked.connect(self.open_symptom_checker.emit)
        buttons.addWidget(rerun)
        buttons.addStretch(1)
        self._col.addLayout(buttons)

    def _symptoms_table(self) -> None:
        symptoms = self.item.symptom_data.get("symptoms", [])
        col = self._section("activity", "Reported symptoms")
        if not symptoms:
            col.addWidget(_label("No symptoms were recorded.", "nbSmallMuted"))
            return
        names = {"onset": dict(ONSETS), "pattern": dict(PATTERNS), "trend": dict(TRENDS),
                 "duration": dict(DURATIONS)}
        # One line per symptom rather than a wide table: the column is narrow.
        for s in symptoms:
            row = QHBoxLayout()
            row.setSpacing(8)
            row.addWidget(self._link(s.get("name", ""), "symptom", s.get("symptom_id", "")),
                          0, Qt.AlignmentFlag.AlignTop)
            detail = " · ".join(x for x in (
                f"{s.get('intensity', 0)}/10",
                names["onset"].get(s.get("onset"), ""),
                names["pattern"].get(s.get("pattern"), ""),
                names["trend"].get(s.get("trend"), ""),
                names["duration"].get(s.get("duration"), "")) if x)
            row.addWidget(_label(detail, "nbSmallMuted"), 1)
            col.addLayout(row)

    def _vitals(self) -> None:
        raw = self.item.symptom_data.get("vitals")
        if not raw:
            return
        v = Vitals(**{k: val for k, val in raw.items() if k in Vitals.__dataclass_fields__})
        flags = vitals_flags(v)
        col = self._section("heart-pulse", "Recorded vitals")
        host = QWidget()
        host.setObjectName("panel")
        flow = FlowLayout(host, spacing=6)       # wraps in a narrow column
        tiles = (("Temp", f"{v.temperature:.1f} °C", "temperature"),
                 ("HR", f"{v.heart_rate} bpm", "heart_rate"),
                 ("BP", f"{v.bp_systolic}/{v.bp_diastolic}", "blood_pressure"),
                 ("RR", f"{v.resp_rate} /min", "resp_rate"),
                 ("SpO₂", f"{v.spo2}%", "spo2"))
        for name, value, key in tiles:
            tile = QFrame()
            tile.setObjectName("nbVitalTile")
            tile.setProperty("flag", "true" if flags[key] else "false")
            t = QVBoxLayout(tile)
            t.setContentsMargins(8, 6, 8, 6)
            t.setSpacing(1)
            t.addWidget(_label(name.upper(), "nbFieldLabel", False))
            t.addWidget(_label(value, "nbMono", False))
            if flags[key]:
                t.addWidget(_label("Outside typical range", "nbFlagText"))
            tile.setFixedWidth(132)
            flow.addWidget(tile)
        col.addWidget(host)

    # --------------------------------------------------------- correlation

    def _matrix_rows(self) -> tuple[list[str], list[list[str]]]:
        return correlation_table(self.item.symptom_data, self._result, MAX_CONDITIONS)

    def _correlation(self) -> None:
        col = self._section("layers", "Hallmark correlation", reference=True)
        if self._result is None or not self._result.matches:
            col.addWidget(_label("No condition in the reference data matches these symptoms, "
                                 "or the data hasn't loaded yet.", "nbSmallMuted"))
            return
        col.addWidget(_label("Worked out again from today's reference data. Counts, not a "
                             "probability: how much of each condition's picture was "
                             "reported, and how many of the reported symptoms it explains.",
                             "nbSmallMuted"))
        switch = QHBoxLayout()
        switch.setSpacing(4)
        self._mode_buttons = {}
        for mode, text in (("matrix", "Matrix"), ("cards", "Cards")):
            button = QPushButton(text)
            button.setObjectName("nbFilterChip")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, m=mode: self._set_mode(m))
            self._mode_buttons[mode] = button
            switch.addWidget(button)
        switch.addStretch(1)
        col.addLayout(switch)
        self._corr_host = QVBoxLayout()
        self._corr_host.setSpacing(8)
        col.addLayout(self._corr_host)
        headers, rows = self._matrix_rows()
        col.addWidget(self._insert_button(lambda: self.insert_table.emit(
            f"Hallmark correlation: {self.item.title}", headers, rows)))
        self._set_mode("matrix")

    def _set_mode(self, mode: str) -> None:
        self._mode = mode
        for key, button in self._mode_buttons.items():
            button.setProperty("on", "true" if key == mode else "false")
            _repolish(button)
        while self._corr_host.count():
            widget = self._corr_host.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        if mode == "matrix":
            self._corr_host.addWidget(self._matrix())
        else:
            for match in self._result.matches[:MAX_CONDITIONS]:
                self._corr_host.addWidget(self._card(match))

    def _matrix(self) -> QWidget:
        """The matrix scrolls sideways on its own when the column is narrow,
        so it never pushes the rest of the page wider."""
        headers, rows = self._matrix_rows()
        area = QScrollArea()
        area.setObjectName("nbMatrixScroll")
        area.setFrameShape(QFrame.Shape.NoFrame)
        area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        area.setWidgetResizable(True)
        host = QWidget()
        host.setObjectName("panel")
        grid = QGridLayout(host)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(6)
        for c, head in enumerate(headers):
            grid.addWidget(_label(head.upper(), "nbFieldLabel", wrap=False), 0, c)
        styles = {"●": "nbCellGood", "✕": "nbCellBad"}
        for r, (row, match) in enumerate(zip(rows, self._result.matches), start=1):
            grid.addWidget(self._link(row[0], "disease", match.disease_id), r, 0,
                           Qt.AlignmentFlag.AlignLeft)
            for c, text in enumerate(row[1:], start=1):
                grid.addWidget(_label(text, styles.get(text[:1], "nbCellMuted"), wrap=False), r, c)
        grid.setColumnStretch(0, 1)
        area.setWidget(host)
        area.setFixedHeight(host.sizeHint().height() + 14)
        return area

    def _card(self, match) -> QWidget:
        card = QFrame()
        card.setObjectName("nbMatchCard")
        col = QVBoxLayout(card)
        col.setContentsMargins(10, 8, 10, 10)
        col.setSpacing(6)
        head = QHBoxLayout()
        head.addWidget(self._link(match.name, "disease", match.disease_id))
        head.addStretch(1)
        head.addWidget(_label(URGENCY_LABELS.get(match.urgency, "Urgency not specified"),
                              "nbSmallMuted", False))
        col.addLayout(head)
        bar_row = QHBoxLayout()
        bar = QProgressBar()
        bar.setObjectName("nbMatchBar")
        bar.setTextVisible(False)
        bar.setFixedHeight(5)
        # Same numbers the Symptom Checker ranks by; hover for the working.
        why = "\n".join(match.why())
        bar.setRange(0, 100)
        bar.setValue(int(match.score))
        bar.setToolTip(why)
        bar_row.addWidget(bar, 1)
        score = _label(f"covers {match.coverage:.0%} \u00b7 explains {match.explained:.0%}  "
                       f"({match.matched_count}/{match.total_hallmarks} of its, "
                       f"{match.explained_count}/{match.reported_count} of yours)",
                       "nbFieldLabel", False)
        score.setToolTip(why)
        bar_row.addWidget(score)
        col.addLayout(bar_row)
        groups = (("Matched", [m.name for m in match.matched], "nbChipGood"),
                  ("Missing hallmarks", list(match.missing), "nbChip"),
                  ("Not linked to this condition", list(match.inconsistent), "nbChip"))
        for title, values, style in groups:
            if values:
                col.addWidget(_label(title, "nbFieldLabel", False))
                col.addWidget(self._chips(values, style))
        return card

    # ---------------------------------------------------------- answer key

    def _answer_key(self) -> None:
        case = self.item.symptom_data
        self._answer_col = self._section("eye-off", "Teaching diagnosis (answer key)")
        self._answer_body = QVBoxLayout()
        self._answer_col.addLayout(self._answer_body)
        if not case.get("answer_key") and not case.get("answer_note"):
            self._answer_body.addWidget(_label("No answer key set. Choose one in Edit case "
                                               "details.", "nbSmallMuted"))
            return
        self._draw_answer()

    def _draw_answer(self) -> None:
        while self._answer_body.count():
            widget = self._answer_body.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        case = self.item.symptom_data
        if not self._revealed:
            hidden = QLabel("██████████  ████████", objectName="nbHidden")
            self._answer_body.addWidget(hidden)
            reveal = QPushButton("  Reveal answer")
            reveal.setObjectName("nbButton")
            reveal.setCursor(Qt.CursorShape.PointingHandCursor)
            reveal.setIcon(lucide.icon("eye", 14, tone_color("text")))
            reveal.clicked.connect(self._reveal)
            self._answer_body.addWidget(reveal, 0, Qt.AlignmentFlag.AlignLeft)
            return
        if case.get("answer_key"):
            self._answer_body.addWidget(self._link(self._answer_name or "Open diagnosis",
                                                   "disease", case["answer_key"]),
                                        0, Qt.AlignmentFlag.AlignLeft)
        if case.get("answer_note"):
            self._answer_body.addWidget(_label(case["answer_note"], "nbBody"))

    def _reveal(self) -> None:
        self._revealed = True
        self._draw_answer()

    # ==================================================== interaction case

    def _build_interaction(self, data: Optional[dict]) -> None:
        case = self.item.interaction_data
        if data is None:
            col = self._section("shield-check", "Case summary", reference=True)
            col.addWidget(_label("The drug-safety reference data isn't loaded yet.",
                                 "nbSmallMuted"))
            return
        col = self._section("shield-check", "Case summary", reference=True)
        text, tone = data.get("verdict", ("", "muted"))
        if text:
            badge = QLabel(f"  {text}  ", objectName="nbVerdict")
            badge.setProperty("tone", tone)
            col.addWidget(badge, 0, Qt.AlignmentFlag.AlignLeft)
        col.addWidget(_label("Candidate drug", "nbFieldLabel"))
        if case.get("candidate_id"):
            col.addWidget(self._link(data.get("candidate") or "Not in reference data",
                                     "medicine", case["candidate_id"]),
                          0, Qt.AlignmentFlag.AlignLeft)
        col.addWidget(_label("Case regimen", "nbFieldLabel"))
        regimen = list(zip(case.get("regimen_ids", []), data.get("regimen", [])))
        if regimen:
            host = QWidget()
            host.setObjectName("panel")
            flow = FlowLayout(host, spacing=6)
            for medicine_id, name in regimen:
                flow.addWidget(self._link(name, "medicine", medicine_id))
            col.addWidget(host)
        else:
            col.addWidget(_label("No other drugs.", "nbSmallMuted"))
        col.addWidget(_label("Case comorbidities", "nbFieldLabel"))
        col.addWidget(self._chips(data.get("conditions", [])) if data.get("conditions")
                      else _label("None.", "nbSmallMuted"))
        if case.get("notes"):
            col.addWidget(_label("Notes saved with the case", "nbFieldLabel"))
            col.addWidget(_label(case["notes"], "nbBody"))
        checker = QPushButton("  Edit in Drug Interaction Checker")
        checker.setObjectName("nbButton")
        checker.setCursor(Qt.CursorShape.PointingHandCursor)
        checker.setIcon(lucide.icon("external-link", 14, tone_color("text")))
        checker.clicked.connect(self.open_checker.emit)
        col.addWidget(checker, 0, Qt.AlignmentFlag.AlignLeft)

        col = self._section("layers", "Findings on record", reference=True)
        headers, rows = data.get("headers", []), data.get("rows", [])
        if not rows:
            col.addWidget(_label("No findings: nothing in this case is on record.",
                                 "nbSmallMuted"))
            return
        for layer, combination, severity, note in rows:
            row = QFrame()
            row.setObjectName("nbMatchCard")
            r = QVBoxLayout(row)
            r.setContentsMargins(10, 7, 10, 8)
            r.setSpacing(3)
            top = QHBoxLayout()
            top.addWidget(_label(combination, "nbBodyStrong"), 1)
            top.addWidget(_label(severity.upper(), "nbFieldLabel", False))
            r.addLayout(top)
            r.addWidget(_label(layer, "nbSmallMuted", False))
            if note:
                r.addWidget(_label(note, "nbBody"))
            col.addWidget(row)
        col.addWidget(self._insert_button(lambda: self.insert_table.emit(
            f"Drug interaction findings: {self.item.title}", headers, rows)))
