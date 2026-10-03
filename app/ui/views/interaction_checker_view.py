"""Drug Interaction Checker: the page and its three tabs.

    InteractionCheckerView   title, stat cards, tab row, disclaimer, content
    CheckerTab               build a hypothetical case and cross-reference it
    CasesTab                 saved case studies
    BrowserTab               one medicine's complete interaction profile

Akeso is a reference platform, so everything here is about a CASE (a
teaching scenario), never about the person using the app.

The page only draws and emits. InteractionCheckerController does the work.
Only the page content scrolls; the app's header and sidebar stay fixed.
"""

from typing import Optional

from PySide6.QtCore import QStringListModel, Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QCompleter,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.interaction_styles import tone_color
from app.models.case_study import CaseStudy
from app.models.drug_safety import PatientCondition
from app.services.case_study_service import MedicineOption
from app.services.drug_safety_service import SafetyReport
from app.ui.views.interaction_widgets import (
    SEVERITIES,
    VERDICTS,
    ClickFrame,
    FlowLayout,
    badge,
    chip,
    clear,
    condition_card,
    divider,
    icon_label,
    message_card,
    note_card,
    pair_card,
    rule_card,
    section_panel,
    two_column,
    wrapped,
)

DISCLAIMER = ("<b>EDUCATIONAL REFERENCE NOTICE.</b> Results summarise structured reference "
              "data for study purposes. They are not clinical advice and do not replace "
              "professional judgement, current prescribing information, or a pharmacist's "
              "review.")


def _repaintable(jobs: list, widget: QWidget, name: str, size: int, tone: str) -> None:
    """Paint an icon now and remember how, so a theme switch can repaint it."""
    def job() -> None:
        colour = tone_color(tone)
        if isinstance(widget, QPushButton):
            widget.setIcon(lucide.icon(name, size, colour))
        else:
            widget.setPixmap(lucide.pixmap(name, size, colour))
    job()
    jobs.append(job)


# ======================================================================
# Page
# ======================================================================

class InteractionCheckerView(QWidget):
    new_case_requested = Signal()
    theme_changed = Signal()
    unlink_requested = Signal()         # stop saving into the linked note

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._icon_jobs: list = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll = scroll

        page = QWidget()
        page.setObjectName("panel")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 22, 28, 30)
        layout.setSpacing(16)
        layout.addLayout(self._header())
        layout.addLayout(self._stats())
        layout.addWidget(self._link_bar())
        layout.addWidget(self._tabs())

        banner = QFrame()
        banner.setObjectName("ixNoteBox")
        banner_row = QHBoxLayout(banner)
        banner_row.setContentsMargins(14, 10, 14, 10)
        banner_row.setSpacing(10)
        info = QLabel()
        _repaintable(self._icon_jobs, info, "info", 15, "primary")
        banner_row.addWidget(info, 0, Qt.AlignmentFlag.AlignTop)
        banner_row.addWidget(wrapped(DISCLAIMER, "ixSmallBody"), 1)
        layout.addWidget(banner)

        self.checker = CheckerTab()
        self.cases = CasesTab()
        self.browser = BrowserTab()
        self.stack = QStackedWidget()
        self.stack.setObjectName("panel")
        for tab in (self.checker, self.cases, self.browser):
            self.stack.addWidget(tab)
        layout.addWidget(self.stack)
        layout.addStretch(1)

        scroll.setWidget(page)
        root.addWidget(scroll)

    # ------------------------------------------------- linked to a note

    def _link_bar(self) -> QWidget:
        """Shown when the checker was opened from a note in the Study
        Notebook: saving then updates that note instead of a new case."""
        self._link = QFrame()
        self._link.setObjectName("ixNoteBox")
        row = QHBoxLayout(self._link)
        row.setContentsMargins(14, 10, 14, 10)
        row.setSpacing(10)
        icon = QLabel()
        _repaintable(self._icon_jobs, icon, "notebook-pen", 15, "primary")
        row.addWidget(icon)
        self._link_text = wrapped("", "ixSmallBody")
        row.addWidget(self._link_text, 1)
        unlink = QPushButton("Unlink")
        unlink.setObjectName("ixSecondary")
        unlink.setCursor(Qt.CursorShape.PointingHandCursor)
        unlink.clicked.connect(self.unlink_requested.emit)
        row.addWidget(unlink)
        self._link.hide()
        return self._link

    def set_link(self, title: str, saved: bool = False) -> None:
        if title:
            self._link_text.setText(
                (f"✓ Saved to “{title}”. " if saved else f"Linked to your note “{title}”. ")
                + "Save to Note stores this check in that note; you can edit it again later.")
        self._link.setVisible(bool(title))
        self.checker.save_text = " Save to Note" if title else " Save as Case Study"

    # ------------------------------------------------------------ builders

    def _header(self) -> QHBoxLayout:
        row = QHBoxLayout()
        titles = QVBoxLayout()
        titles.setSpacing(4)
        title_row = QHBoxLayout()
        title_row.setSpacing(10)
        title_row.addWidget(QLabel("Drug Interaction Checker", objectName="ixTitle"))
        title_row.addWidget(QLabel("REFERENCE PLATFORM", objectName="ixRefBadge"), 0,
                            Qt.AlignmentFlag.AlignVCenter)
        title_row.addStretch(1)
        titles.addLayout(title_row)
        titles.addWidget(QLabel("Cross-reference medicines against each other and against "
                                "comorbidities using structured reference data.",
                                objectName="ixSubtitle"))
        row.addLayout(titles, 1)
        new_case = QPushButton(" New Case")
        new_case.setObjectName("ixPrimary")
        new_case.setCursor(Qt.CursorShape.PointingHandCursor)
        _repaintable(self._icon_jobs, new_case, "plus", 15, "white")
        new_case.clicked.connect(self.new_case_requested.emit)
        row.addWidget(new_case, 0, Qt.AlignmentFlag.AlignVCenter)
        return row

    def _stats(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(14)
        self.stat_drugs = self._stat_card("pill", "primary", "Reference Drugs")
        self.stat_interactions = self._stat_card("arrow-left-right", "success",
                                                 "Documented Interactions")
        self.stat_cases = self._stat_card("bookmark", "amber", "Saved Case Studies")
        for card in (self.stat_drugs, self.stat_interactions, self.stat_cases):
            row.addWidget(card, 1)
        return row

    def _stat_card(self, icon_name: str, tone: str, label: str) -> QFrame:
        card = QFrame()
        card.setObjectName("ixStat")
        row = QHBoxLayout(card)
        row.setContentsMargins(16, 14, 16, 14)
        row.setSpacing(14)
        tile = QFrame()
        tile.setObjectName("ixStatTile")
        tile.setProperty("tone", tone)
        tile.setFixedSize(42, 42)
        tile_layout = QVBoxLayout(tile)
        tile_layout.setContentsMargins(0, 0, 0, 0)
        icon = QLabel()
        _repaintable(self._icon_jobs, icon, icon_name, 20, tone)
        tile_layout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        row.addWidget(tile)
        text = QVBoxLayout()
        text.setSpacing(0)
        card.number = QLabel("0", objectName="ixBigNumber")
        text.addWidget(card.number)
        text.addWidget(QLabel(label, objectName="ixSmallMuted"))
        row.addLayout(text, 1)
        return card

    def _tabs(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("ixTabRow")
        row = QHBoxLayout(bar)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)
        group = QButtonGroup(self)
        group.setExclusive(True)
        self.tab_buttons = []
        for index, (text, icon_name) in enumerate((("Interaction Checker", "shield-check"),
                                                  ("Saved Case Studies", "bookmark"),
                                                  ("Interaction Browser", "layers"))):
            button = QPushButton(" " + text)
            button.setObjectName("ixTab")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            _repaintable(self._icon_jobs, button, icon_name, 15, "muted")
            button.clicked.connect(lambda _c=False, i=index: self.show_tab(i))
            group.addButton(button)
            row.addWidget(button)
            self.tab_buttons.append(button)
            if index == 1:
                self.cases_count = QLabel("0", objectName="ixTabCount")
                self.cases_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.cases_count.setFixedHeight(18)
                self.cases_count.setMinimumWidth(20)
                row.addWidget(self.cases_count, 0, Qt.AlignmentFlag.AlignVCenter)
                row.addSpacing(8)
        self.tab_buttons[0].setChecked(True)
        row.addStretch(1)
        return bar

    # ------------------------------------------------------------- public

    def show_tab(self, index: int) -> None:
        self.tab_buttons[index].setChecked(True)
        self.stack.setCurrentIndex(index)
        self.scroll.verticalScrollBar().setValue(0)

    def show_stats(self, drugs: int, interactions: int, cases: int) -> None:
        self.stat_drugs.number.setText(str(drugs))
        self.stat_interactions.number.setText(str(interactions))
        self.stat_cases.number.setText(str(cases))
        self.cases_count.setText(str(cases))

    def refresh_theme(self) -> None:
        """Called by the shell after a theme switch."""
        for job in self._icon_jobs:
            job()
        for tab in (self.checker, self.cases, self.browser):
            tab.repaint_icons()
        self.theme_changed.emit()


# ======================================================================
# Tab 1: Interaction Checker
# ======================================================================

class CheckerTab(QWidget):
    candidate_chosen = Signal(str)          # medicine id
    candidate_typed = Signal(str)           # free text, on Enter
    candidate_cleared = Signal()
    condition_toggled = Signal(str, bool)
    regimen_toggled = Signal(str, bool)     # medicine id, included
    remove_drug_requested = Signal(str)
    add_drug_requested = Signal()
    save_requested = Signal()
    monograph_requested = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._icon_jobs: list = []
        self._by_label: dict[str, MedicineOption] = {}

        columns = QHBoxLayout(self)
        columns.setContentsMargins(0, 0, 0, 0)
        columns.setSpacing(20)

        left = QWidget()
        left.setObjectName("panel")
        left.setFixedWidth(430)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)
        left_layout.addWidget(self._candidate_panel())
        left_layout.addWidget(self._comorbidity_panel())
        left_layout.addWidget(self._regimen_panel())
        left_layout.addStretch(1)
        columns.addWidget(left, 0, Qt.AlignmentFlag.AlignTop)

        self._results_host = QWidget()
        self._results_host.setObjectName("panel")
        self._results = QVBoxLayout(self._results_host)
        self._results.setContentsMargins(0, 0, 0, 0)
        self._results.setSpacing(16)
        columns.addWidget(self._results_host, 1, Qt.AlignmentFlag.AlignTop)

    def repaint_icons(self) -> None:
        for job in self._icon_jobs:
            job()

    # --------------------------------------------------------------- left

    def _step(self, number: str, title: str, subtitle: str) -> tuple[QFrame, QVBoxLayout,
                                                                      QHBoxLayout]:
        panel = QFrame()
        panel.setObjectName("ixPanel")
        body = QVBoxLayout(panel)
        body.setContentsMargins(16, 14, 16, 16)
        body.setSpacing(12)
        head = QHBoxLayout()
        head.setSpacing(10)
        circle = QLabel(number, objectName="ixStepNumber")
        circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        circle.setFixedSize(24, 24)
        head.addWidget(circle, 0, Qt.AlignmentFlag.AlignTop)
        titles = QVBoxLayout()
        titles.setSpacing(1)
        titles.addWidget(QLabel(title, objectName="ixStepTitle"))
        titles.addWidget(wrapped(subtitle, "ixSmallMuted"))
        head.addLayout(titles, 1)
        body.addLayout(head)
        return panel, body, head

    def _candidate_panel(self) -> QFrame:
        panel, body, _head = self._step("1", "Candidate Drug",
                                        "Select a medicine to evaluate against the case")
        field = QFrame()
        field.setObjectName("ixSearchField")
        row = QHBoxLayout(field)
        row.setContentsMargins(10, 0, 4, 0)
        row.setSpacing(6)
        search_icon = QLabel()
        _repaintable(self._icon_jobs, search_icon, "search", 15, "muted")
        row.addWidget(search_icon)
        self.search = QLineEdit()
        self.search.setObjectName("ixSearchInput")
        self.search.setPlaceholderText("Search by name, generic or brand...")
        self.search.returnPressed.connect(lambda: self.candidate_typed.emit(self.search.text()))
        row.addWidget(self.search, 1)
        self.clear_button = QPushButton()
        self.clear_button.setObjectName("ixIconButtonPlain")
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_button.setToolTip("Clear the candidate")
        _repaintable(self._icon_jobs, self.clear_button, "x", 14, "muted")
        self.clear_button.clicked.connect(self.candidate_cleared.emit)
        row.addWidget(self.clear_button)
        field.setFixedHeight(38)
        body.addWidget(field)

        self._model = QStringListModel([], self)
        completer = QCompleter(self._model, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setMaxVisibleItems(7)
        completer.popup().setObjectName("ixSuggest")
        completer.activated[str].connect(self._on_completed)
        self.search.setCompleter(completer)

        body.addWidget(QLabel("Quick candidates", objectName="ixFieldLabel"))
        self._chips_host = QWidget()
        self._chips_host.setObjectName("panel")
        self._chips = FlowLayout(self._chips_host, spacing=6)
        body.addWidget(self._chips_host)
        return panel

    def _comorbidity_panel(self) -> QFrame:
        panel, body, head = self._step("2", "Case Comorbidities",
                                       "Select conditions to cross-check against the candidate")
        self._selected_badge = QLabel("0 SELECTED", objectName="ixActiveBadge")
        head.addWidget(self._selected_badge, 0, Qt.AlignmentFlag.AlignTop)
        self._conditions_host = QWidget()
        self._conditions_host.setObjectName("panel")
        self._conditions = QGridLayout(self._conditions_host)
        self._conditions.setContentsMargins(0, 0, 0, 0)
        self._conditions.setSpacing(8)
        body.addWidget(self._conditions_host)
        return panel

    def _regimen_panel(self) -> QFrame:
        panel, body, head = self._step("3", "Case Regimen", "Medicines the case is already on")
        add = QPushButton(" Add drug")
        add.setObjectName("ixCheckInCase")
        add.setCursor(Qt.CursorShape.PointingHandCursor)
        _repaintable(self._icon_jobs, add, "plus", 13, "primary")
        add.clicked.connect(self.add_drug_requested.emit)
        head.addWidget(add, 0, Qt.AlignmentFlag.AlignTop)
        self._regimen_host = QWidget()
        self._regimen_host.setObjectName("panel")
        self._regimen = QVBoxLayout(self._regimen_host)
        self._regimen.setContentsMargins(0, 0, 0, 0)
        self._regimen.setSpacing(8)
        body.addWidget(self._regimen_host)
        return panel

    # ------------------------------------------------------ left: filling

    def set_options(self, options: list[MedicineOption]) -> None:
        self._by_label = {o.label: o for o in options}
        self._model.setStringList([o.label for o in options])

    def _on_completed(self, label: str) -> None:
        option = self._by_label.get(label)
        if option is not None:
            self.set_candidate_text(option.name)
            self.candidate_chosen.emit(option.medicine_id)

    def set_candidate_text(self, text: str) -> None:
        self.search.blockSignals(True)
        self.search.setText(text)
        self.search.blockSignals(False)
        self.clear_button.setVisible(bool(text))

    def set_quick(self, options: list[MedicineOption], selected_id: str) -> None:
        clear(self._chips)
        if not options:
            self._chips.addWidget(QLabel("Add medicines to your database to see quick "
                                         "candidates here.", objectName="ixSmallMuted"))
            return
        for option in options:
            frame = chip(option.name, option.is_otc, option.medicine_id == selected_id)
            frame.clicked.connect(lambda o=option: self._pick(o))
            self._chips.addWidget(frame)

    def _pick(self, option: MedicineOption) -> None:
        self.set_candidate_text(option.name)
        self.candidate_chosen.emit(option.medicine_id)

    def set_conditions(self, conditions: list[PatientCondition], selected: set[str]) -> None:
        clear(self._conditions)
        self._selected_badge.setText(
            f"{len(selected & {c.id for c in conditions})} SELECTED")
        if not conditions:
            self._conditions.addWidget(wrapped("No comorbidities in the reference data yet.",
                                               "ixSmallMuted"), 0, 0, 1, 2)
            return
        for index, condition in enumerate(conditions):
            on = condition.id in selected
            toggle = ClickFrame("ixConditionToggle", on=on)
            row = QHBoxLayout(toggle)
            row.setContentsMargins(12, 10, 10, 10)
            row.setSpacing(6)
            text = QVBoxLayout()
            text.setSpacing(2)
            # One line each, shortened with "..." to the box width: wrapped
            # labels inside a grid can overlap, and the full text is in the
            # tooltip. Width: half the 430px column, minus padding and icon.
            for value, name in ((condition.label, "ixToggleTitle"),
                                (condition.description, "ixToggleSub")):
                if not value:
                    continue
                label = QLabel(objectName=name)
                label.setText(label.fontMetrics().elidedText(
                    value, Qt.TextElideMode.ElideRight, 150))
                text.addWidget(label)
            toggle.setToolTip(f"{condition.label}\n{condition.description}".strip())
            toggle.setMinimumHeight(56)
            row.addLayout(text, 1)
            if on:
                row.addWidget(icon_label("circle-check", 15, "primary"), 0,
                              Qt.AlignmentFlag.AlignTop)
            toggle.clicked.connect(lambda cid=condition.id, now=on:
                                   self.condition_toggled.emit(cid, not now))
            self._conditions.addWidget(toggle, index // 2, index % 2)

    def set_regimen(self, drugs: list[MedicineOption], included: set[str]) -> None:
        clear(self._regimen)
        if not drugs:
            self._regimen.addWidget(wrapped("No drugs in the case regimen yet. Use Add drug "
                                            "to build the scenario.", "ixSmallMuted"))
            return
        for drug in drugs:
            row_frame = QFrame()
            row_frame.setObjectName("ixRegimenRow")
            row = QHBoxLayout(row_frame)
            row.setContentsMargins(12, 8, 8, 8)
            row.setSpacing(10)
            box = QCheckBox()
            box.setChecked(drug.medicine_id in included)
            box.setToolTip("Include in this check")
            box.toggled.connect(lambda on, mid=drug.medicine_id:
                                self.regimen_toggled.emit(mid, on))
            row.addWidget(box)
            text = QVBoxLayout()
            text.setSpacing(1)
            text.addWidget(wrapped(drug.name, "ixToggleTitle"))
            if drug.drug_class:
                text.addWidget(wrapped(drug.drug_class, "ixToggleSubAccent"))
            row.addLayout(text, 1)
            trash = QPushButton()
            trash.setObjectName("ixIconButton")
            trash.setIcon(lucide.icon("trash-2", 15, tone_color("muted")))
            trash.setToolTip("Remove from the case")
            trash.setCursor(Qt.CursorShape.PointingHandCursor)
            trash.clicked.connect(lambda _c=False, mid=drug.medicine_id:
                                  self.remove_drug_requested.emit(mid))
            row.addWidget(trash)
            self._regimen.addWidget(row_frame)

    # -------------------------------------------------------------- right

    def show_prompt(self) -> None:
        clear(self._results)
        self._results.addWidget(message_card(
            "pill", "Choose a candidate drug to cross-reference",
            "Search the medicine reference on the left or pick a quick candidate. It is "
            "checked against the case comorbidities and every drug in the case regimen."))

    def show_not_found(self, text: str) -> None:
        clear(self._results)
        self._results.addWidget(message_card(
            "circle-help", f"“{text}” isn't in the reference data",
            "Only medicines in the reference data can be evaluated. Pick one from the "
            "suggestions list instead."))

    def show_report(self, report: SafetyReport, option: MedicineOption) -> None:
        clear(self._results)
        self._results.addWidget(self._evaluation_card(report, option))

        if report.rules:
            panel, body = section_panel("layers", "danger",
                                        f"COMBINATION RULES TRIGGERED ({len(report.rules)} "
                                        "MATCHED)", "", panel_tone="danger")
            for finding in report.rules:
                rule = finding.rule
                body.addWidget(rule_card(rule.name, rule.severity, rule.description,
                                         [d.name for d in finding.drugs],
                                         rule.clinical_significance, rule.recommendation))
            self._results.addWidget(panel)

        panel, body = section_panel("heart-pulse", "danger",
                                    f"DRUG × CONDITION ({len(report.conditions)} CHECKED)",
                                    "Cross-referenced against the candidate")
        if report.conditions:
            body.addLayout(two_column([
                condition_card(f.condition.label, f.severity, f.summary, f.guidance,
                               f.drug.name) for f in report.conditions]))
        else:
            body.addWidget(wrapped("No case comorbidities selected.", "ixSmallMuted"))
        self._results.addWidget(panel)

        pairs = report.candidate_pairs
        panel, body = section_panel("activity", "primary",
                                    f"DRUG × DRUG ({len(pairs)} CHECKED)",
                                    "Candidate ⇄ Regimen")
        if pairs:
            for p in pairs:
                body.addWidget(pair_card(p.first.name, p.second.name, p.severity,
                                         p.description, p.clinical_significance,
                                         p.recommendation, p.duplicate))
        else:
            body.addWidget(wrapped("No regimen drugs are included in this check.",
                                   "ixSmallMuted"))
        if report.regimen_pairs:
            body.addWidget(divider())
            count = len(report.regimen_pairs)
            sub = QHBoxLayout()
            sub.addWidget(QLabel(f"Within the case regimen ({count} "
                                 f"pair{'s' if count != 1 else ''})",
                                 objectName="ixSubSection"))
            sub.addStretch(1)
            sub.addWidget(QLabel("Interactions between regimen drugs",
                                 objectName="ixSmallMuted"))
            body.addLayout(sub)
            for p in report.regimen_pairs:
                body.addWidget(pair_card(p.first.name, p.second.name, p.severity,
                                         p.description, p.clinical_significance,
                                         p.recommendation, p.duplicate))
        self._results.addWidget(panel)

        if report.not_in_database:
            names = ", ".join(d.name for d in report.not_in_database)
            self._results.addWidget(note_card(f"Not checked, because they aren't in the "
                                              f"reference data: {names}."))

    def _evaluation_card(self, report: SafetyReport, option: MedicineOption) -> QFrame:
        badge_text, tone, icon_name, summary = VERDICTS[report.verdict]
        card = QFrame()
        card.setObjectName("ixVerdict")
        card.setProperty("tone", tone)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 16)
        layout.setSpacing(12)

        top = QHBoxLayout()
        top.setSpacing(14)
        tile = QFrame()
        tile.setObjectName("ixVerdictTileSoft")
        tile.setProperty("tone", tone)
        tile.setFixedSize(46, 46)
        tile_layout = QVBoxLayout(tile)
        tile_layout.setContentsMargins(0, 0, 0, 0)
        tile_layout.addWidget(icon_label(icon_name, 22, tone), 0, Qt.AlignmentFlag.AlignCenter)
        top.addWidget(tile, 0, Qt.AlignmentFlag.AlignTop)

        titles = QVBoxLayout()
        titles.setSpacing(3)
        titles.addWidget(QLabel("REFERENCE EVALUATION", objectName="ixTileLabel"))
        name_row = QHBoxLayout()
        name_row.setSpacing(10)
        name_row.addWidget(QLabel(option.name, objectName="ixVerdictName"))
        name_row.addWidget(badge(badge_text, tone), 0, Qt.AlignmentFlag.AlignVCenter)
        name_row.addStretch(1)
        titles.addLayout(name_row)
        titles.addWidget(wrapped(summary.format(unknown=report.unknown_count), "ixBoxBody"))
        top.addLayout(titles, 1)

        buttons = QVBoxLayout()
        buttons.setSpacing(8)
        save = QPushButton(getattr(self, "save_text", " Save as Case Study"))
        save.setObjectName("ixPrimary")
        save.setIcon(lucide.icon("bookmark-plus", 14, "#FFFFFF"))
        save.setCursor(Qt.CursorShape.PointingHandCursor)
        save.clicked.connect(self.save_requested.emit)
        monograph = QPushButton(" View Monograph")
        monograph.setObjectName("ixSecondary")
        monograph.setIcon(lucide.icon("external-link", 14, tone_color("text")))
        monograph.setCursor(Qt.CursorShape.PointingHandCursor)
        monograph.clicked.connect(lambda: self.monograph_requested.emit(option.medicine_id))
        buttons.addWidget(save)
        buttons.addWidget(monograph)
        buttons.addStretch(1)
        top.addLayout(buttons)
        layout.addLayout(top)

        layout.addWidget(divider())
        foot = QHBoxLayout()
        facts = [f"<b>{option.drug_class}</b>" if option.drug_class else "",
                 f"Generic: {option.generic_name}" if option.generic_name else ""]
        foot.addWidget(QLabel("  •  ".join(f for f in facts if f)
                              or "No class or generic name on record.",
                              objectName="ixSmallBody"), 1)
        foot.addWidget(QLabel("OTC" if option.is_otc else "RX", objectName="ixRefBadge"))
        layout.addLayout(foot)
        return card


# ======================================================================
# Tab 2: Saved Case Studies
# ======================================================================

class CasesTab(QWidget):
    filters_changed = Signal(str, str)      # query, tag
    open_requested = Signal(str)
    duplicate_requested = Signal(str)
    delete_requested = Signal(str)

    CARD_MIN_WIDTH = 300

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._icon_jobs: list = []
        self._tag = ""
        self._cards: list[QWidget] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        bar = QFrame()
        bar.setObjectName("ixPanel")
        row = QHBoxLayout(bar)
        row.setContentsMargins(14, 10, 14, 10)
        row.setSpacing(12)
        field = QFrame()
        field.setObjectName("ixSearchField")
        field_row = QHBoxLayout(field)
        field_row.setContentsMargins(10, 0, 6, 0)
        icon = QLabel()
        _repaintable(self._icon_jobs, icon, "search", 15, "muted")
        field_row.addWidget(icon)
        self.search = QLineEdit()
        self.search.setObjectName("ixSearchInput")
        self.search.setPlaceholderText("Search saved case title, candidate drug, or tags...")
        self.search.textChanged.connect(self._emit)
        field_row.addWidget(self.search, 1)
        field.setFixedHeight(36)
        field.setMinimumWidth(320)
        row.addWidget(field, 1)
        funnel = QLabel()
        _repaintable(self._icon_jobs, funnel, "funnel", 13, "muted")
        row.addWidget(funnel)
        row.addWidget(QLabel("Tags:", objectName="ixSmallMuted"))
        self._tags_host = QWidget()
        self._tags_host.setObjectName("panel")
        self._tags_row = QHBoxLayout(self._tags_host)
        self._tags_row.setContentsMargins(0, 0, 0, 0)
        self._tags_row.setSpacing(6)
        row.addWidget(self._tags_host)
        layout.addWidget(bar)

        self._grid_host = QWidget()
        self._grid_host.setObjectName("panel")
        self._grid = QGridLayout(self._grid_host)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setSpacing(16)
        layout.addWidget(self._grid_host)
        self._empty = message_card("bookmark", "No case studies yet",
                                   "Run a check in the Interaction Checker and click "
                                   "Save as Case Study.")
        layout.addWidget(self._empty)
        layout.addStretch(1)

    def repaint_icons(self) -> None:
        for job in self._icon_jobs:
            job()

    def _emit(self) -> None:
        self.filters_changed.emit(self.search.text(), self._tag)

    def filters(self) -> tuple[str, str]:
        return self.search.text(), self._tag

    def set_tags(self, tags: list[str]) -> None:
        clear(self._tags_row)
        if self._tag and self._tag not in tags:
            self._tag = ""
        group = QButtonGroup(self._tags_host)
        for tag in ["", *tags]:
            button = QPushButton(tag or "All")
            button.setObjectName("ixFilterChip")
            button.setCheckable(True)
            button.setChecked(tag == self._tag)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, t=tag: self._set_tag(t))
            group.addButton(button)
            self._tags_row.addWidget(button)

    def _set_tag(self, tag: str) -> None:
        self._tag = tag
        self._emit()

    def show_cases(self, cards: list[tuple[CaseStudy, str, str, int, int]],
                   total: int) -> None:
        """cards: (case, candidate name, verdict, regimen count, comorbidity count)."""
        for card in self._cards:
            card.setParent(None)
            card.deleteLater()
        self._cards = [self._case_card(*c) for c in cards]
        self._empty.setVisible(not cards)
        if not cards and total:
            self._empty.findChild(QLabel, "ixEmptyTitle").setText("No matching case studies")
        self._reflow()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._reflow()

    def _reflow(self) -> None:
        width = max(self.width(), 1)
        columns = max(1, min(3, (width + 16) // (self.CARD_MIN_WIDTH + 16)))
        for card in self._cards:
            self._grid.removeWidget(card)
        for index, card in enumerate(self._cards):
            self._grid.addWidget(card, index // columns, index % columns,
                                 Qt.AlignmentFlag.AlignTop)
        for col in range(3):
            self._grid.setColumnStretch(col, 1 if col < columns else 0)

    def _case_card(self, case: CaseStudy, candidate: str, verdict: str,
                   regimen_count: int, condition_count: int) -> QFrame:
        badge_text, tone, _icon, _summary = VERDICTS[verdict]
        card = QFrame()
        card.setObjectName("ixPanel")
        card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        top = QHBoxLayout()
        top.addWidget(badge(badge_text, tone))
        top.addStretch(1)
        top.addWidget(icon_label("calendar", 12, "muted"))
        top.addWidget(QLabel(case.saved_on, objectName="ixSmallMuted"))
        layout.addLayout(top)
        layout.addWidget(wrapped(case.title, "ixCaseTitle"))

        box = QFrame()
        box.setObjectName("ixCountdown")
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(12, 9, 12, 9)
        box_layout.setSpacing(4)
        line = QHBoxLayout()
        line.addWidget(QLabel("Candidate:", objectName="ixSmallMuted"))
        line.addStretch(1)
        line.addWidget(icon_label("pill", 12, "primary"))
        line.addWidget(QLabel(candidate, objectName="ixToggleTitle"))
        box_layout.addLayout(line)
        counts = QHBoxLayout()
        counts.addWidget(QLabel(f"Regimen: <b>{regimen_count}</b> "
                                f"drug{'s' if regimen_count != 1 else ''}",
                                objectName="ixSmallMuted"))
        counts.addStretch(1)
        counts.addWidget(QLabel(f"Comorbidities: <b>{condition_count}</b>",
                                objectName="ixSmallMuted"))
        box_layout.addLayout(counts)
        layout.addWidget(box)

        if case.notes:
            layout.addWidget(wrapped(f"“{case.notes}”", "ixNote"))
        if case.tags:
            tags = QHBoxLayout()
            tags.setSpacing(6)
            for tag in case.tags:
                tags.addWidget(QLabel(f"#{tag}", objectName="ixTag"))
            tags.addStretch(1)
            layout.addLayout(tags)
        layout.addStretch(1)
        layout.addWidget(divider())

        actions = QHBoxLayout()
        actions.setSpacing(8)
        open_button = QPushButton(" Open in Checker")
        open_button.setObjectName("ixPrimary")
        open_button.setIcon(lucide.icon("play", 13, "#FFFFFF"))
        open_button.setCursor(Qt.CursorShape.PointingHandCursor)
        open_button.clicked.connect(lambda: self.open_requested.emit(case.id))
        actions.addWidget(open_button, 1)
        for icon_name, tip, signal in (("copy", "Duplicate", self.duplicate_requested),
                                       ("trash-2", "Delete", self.delete_requested)):
            button = QPushButton()
            button.setObjectName("ixIconBox")
            button.setIcon(lucide.icon(icon_name, 15, tone_color("muted")))
            button.setToolTip(tip)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, s=signal: s.emit(case.id))
            actions.addWidget(button)
        layout.addLayout(actions)
        return card


# ======================================================================
# Tab 3: Interaction Browser
# ======================================================================

class BrowserTab(QWidget):
    drug_chosen = Signal(str)
    filter_changed = Signal(str)            # "", "avoid", "caution", "safe"
    check_in_case_requested = Signal(str, str)   # browsed drug, other drug
    monograph_requested = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._icon_jobs: list = []
        self._options: list[MedicineOption] = []
        self._selected = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        bar = QFrame()
        bar.setObjectName("ixPanel")
        row = QHBoxLayout(bar)
        row.setContentsMargins(16, 12, 16, 12)
        row.setSpacing(12)
        tile = QFrame()
        tile.setObjectName("ixStatTile")
        tile.setProperty("tone", "primary")
        tile.setFixedSize(38, 38)
        tile_layout = QVBoxLayout(tile)
        tile_layout.setContentsMargins(0, 0, 0, 0)
        tile_icon = QLabel()
        _repaintable(self._icon_jobs, tile_icon, "pill", 18, "primary")
        tile_layout.addWidget(tile_icon, 0, Qt.AlignmentFlag.AlignCenter)
        row.addWidget(tile)
        titles = QVBoxLayout()
        titles.setSpacing(1)
        titles.addWidget(QLabel("Digital Reference Browser", objectName="ixStepTitle"))
        titles.addWidget(QLabel("Inspect the documented interaction profile of any medicine "
                                "in the reference data", objectName="ixSmallMuted"))
        row.addLayout(titles, 1)
        field = QFrame()
        field.setObjectName("ixSearchField")
        field_row = QHBoxLayout(field)
        field_row.setContentsMargins(10, 0, 6, 0)
        icon = QLabel()
        _repaintable(self._icon_jobs, icon, "search", 15, "muted")
        field_row.addWidget(icon)
        self.search = QLineEdit()
        self.search.setObjectName("ixSearchInput")
        self.search.setPlaceholderText("Filter medicines...")
        self.search.textChanged.connect(lambda _t: self._draw_chips())
        field_row.addWidget(self.search, 1)
        field.setFixedSize(260, 36)
        row.addWidget(field)
        layout.addWidget(bar)

        self._chips_host = QWidget()
        self._chips_host.setObjectName("panel")
        self._chips = FlowLayout(self._chips_host, spacing=8)
        layout.addWidget(self._chips_host)

        self._content_host = QWidget()
        self._content_host.setObjectName("panel")
        self._content = QVBoxLayout(self._content_host)
        self._content.setContentsMargins(0, 0, 0, 0)
        self._content.setSpacing(16)
        layout.addWidget(self._content_host)
        layout.addStretch(1)

    def repaint_icons(self) -> None:
        for job in self._icon_jobs:
            job()

    def set_options(self, options: list[MedicineOption], selected: str) -> None:
        self._options = options
        self._selected = selected
        self._draw_chips()

    def _draw_chips(self) -> None:
        clear(self._chips)
        words = self.search.text().lower().split()
        shown = 0
        for option in self._options:
            haystack = f"{option.label} {option.drug_class}".lower()
            if words and not all(w in haystack for w in words):
                continue
            frame = chip(option.name, option.is_otc, option.medicine_id == self._selected)
            frame.clicked.connect(lambda mid=option.medicine_id: self.drug_chosen.emit(mid))
            self._chips.addWidget(frame)
            shown += 1
        if not shown:
            self._chips.addWidget(QLabel("No medicine in the reference data matches that "
                                         "filter." if self._options else
                                         "The medicine reference is empty.",
                                         objectName="ixSmallMuted"))

    def show_empty(self) -> None:
        clear(self._content)
        self._content.addWidget(message_card(
            "layers", "Pick a medicine to browse",
            "See every documented drug interaction, condition caution and combination rule "
            "the reference data holds for it."))

    def show_profile(self, option: MedicineOption, brands: list[str], severity_filter: str,
                     interactions: list, conditions: list, rules: list) -> None:
        """interactions: [(Drug, DrugInteraction)], conditions: [(PatientCondition,
        ConditionSafety)], rules: [InteractionRule]."""
        clear(self._content)

        head = QFrame()
        head.setObjectName("ixPanel")
        head_layout = QVBoxLayout(head)
        head_layout.setContentsMargins(20, 18, 20, 18)
        head_layout.setSpacing(6)
        title = QHBoxLayout()
        title.setSpacing(10)
        title.addWidget(QLabel(option.name, objectName="ixDrugTitle"))
        title.addWidget(QLabel("OTC" if option.is_otc else "RX", objectName="ixRefBadge"),
                        0, Qt.AlignmentFlag.AlignVCenter)
        title.addStretch(1)
        monograph = QPushButton(" Full Monograph")
        monograph.setObjectName("ixSecondary")
        monograph.setIcon(lucide.icon("external-link", 14, tone_color("text")))
        monograph.setCursor(Qt.CursorShape.PointingHandCursor)
        monograph.clicked.connect(lambda: self.monograph_requested.emit(option.medicine_id))
        title.addWidget(monograph)
        head_layout.addLayout(title)
        facts = []
        if option.generic_name:
            facts.append(f"Generic: <b>{option.generic_name}</b>")
        if option.drug_class:
            facts.append(f"Class: <span style='color:{tone_color('primary')}'><b>"
                         f"{option.drug_class}</b></span>")
        if facts:
            head_layout.addWidget(QLabel("  •  ".join(facts), objectName="ixSmallBody"))
        if brands:
            head_layout.addWidget(wrapped("Brands: " + ", ".join(brands), "ixSmallMuted"))
        self._content.addWidget(head)

        filters = QHBoxLayout()
        filters.setSpacing(6)
        filters.addWidget(icon_label("funnel", 13, "muted"))
        filters.addWidget(QLabel("Filter severities:", objectName="ixSmallMuted"))
        group = QButtonGroup(self._content_host)
        for key, text, tone in (("", "All", ""), ("avoid", "Avoid", "danger"),
                                ("caution", "Caution", "amber"),
                                ("safe", "Compatible", "success")):
            button = QPushButton(text)
            button.setObjectName("ixFilterChip")
            if tone:
                button.setProperty("tone", tone)
            button.setCheckable(True)
            button.setChecked(key == severity_filter)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, k=key: self.filter_changed.emit(k))
            group.addButton(button)
            filters.addWidget(button)
        filters.addStretch(1)
        self._content.addLayout(filters)

        keep = (lambda s: True) if not severity_filter else (lambda s: s == severity_filter)

        pairs = [(d, row) for d, row in interactions if keep(row.severity)]
        panel, body = section_panel("activity", "primary",
                                    f"Documented Drug Interactions ({len(pairs)})",
                                    "Sorted Avoid → Precaution → Compatible")
        for drug, row in pairs:
            body.addWidget(self._interaction_row(option, drug, row))
        if not pairs:
            body.addWidget(wrapped("No documented drug interactions match this filter.",
                                   "ixSmallMuted"))
        self._content.addWidget(panel)

        cond = [(c, row) for c, row in conditions if keep(row.safety)]
        panel, body = section_panel("heart-pulse", "danger",
                                    f"Condition Cautions & Contraindications ({len(cond)})",
                                    f"Comorbidity entries for {option.name}")
        if cond:
            body.addLayout(two_column([condition_card(c.label, row.safety, row.summary,
                                                      row.guidance, option.name)
                                       for c, row in cond]))
        else:
            body.addWidget(wrapped("No condition entries match this filter.", "ixSmallMuted"))
        self._content.addWidget(panel)

        matched = [r for r in rules if keep(r.severity)]
        panel, body = section_panel("layers", "primary",
                                    f"Combination Rules Involving {option.name} or Its Class "
                                    f"({len(matched)})",
                                    "3+ drug, class, or drug-plus-condition rules")
        for rule in matched:
            body.addWidget(rule_card(rule.name, rule.severity, rule.description, [],
                                     rule.clinical_significance, rule.recommendation))
        if not matched:
            body.addWidget(wrapped("No combination rules match this filter.", "ixSmallMuted"))
        self._content.addWidget(panel)

    def _interaction_row(self, option: MedicineOption, drug, row) -> QFrame:
        badge_text, tone = SEVERITIES.get(row.severity, SEVERITIES["caution"])
        card = QFrame()
        card.setObjectName("ixInnerCard")
        card.setProperty("tone", tone)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(12)
        text = QVBoxLayout()
        text.setSpacing(4)
        head = QHBoxLayout()
        head.setSpacing(8)
        head.addWidget(QLabel(drug.name, objectName="ixFindingTitle"))
        if drug.drug_class:
            head.addWidget(QLabel(f"({drug.drug_class})", objectName="ixSmallAccent"))
        head.addWidget(badge(badge_text, tone))
        head.addStretch(1)
        text.addLayout(head)
        text.addWidget(wrapped(row.description, "ixBoxBody"))
        if row.recommendation:
            text.addWidget(wrapped(f"<span style='color:{tone_color('primary')}; "
                                   f"font-weight:800'>Recommendation:</span> "
                                   f"{row.recommendation}", "ixSmallMuted"))
        layout.addLayout(text, 1)
        check = QPushButton(" Check in case")
        check.setObjectName("ixCheckInCase")
        check.setIcon(lucide.icon("play", 12, tone_color("primary")))
        check.setCursor(Qt.CursorShape.PointingHandCursor)
        check.clicked.connect(lambda: self.check_in_case_requested.emit(option.medicine_id,
                                                                         drug.medicine_id))
        layout.addWidget(check, 0, Qt.AlignmentFlag.AlignVCenter)
        return card
