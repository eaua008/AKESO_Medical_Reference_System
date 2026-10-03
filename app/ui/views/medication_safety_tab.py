"""Tab 2: Interaction & Safety Check.

Left column, three numbered steps:
    1  Candidate drug      search your medicine database, or a quick chip
    2  Patient Health      the conditions from patient_conditions
       Profile
    3  Active Regimen      the patient's current meds, each can be ticked off

Right column: the verdict card, condition results, drug-pair results,
combination risks, and the Past Safety Checks Log.

Like the rest of the app, this only draws and emits. SafetyCheckController
runs the check and hands back a SafetyReport to draw.
"""

from datetime import datetime
from typing import Optional

from PySide6.QtCore import QPoint, QRect, QSize, QStringListModel, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QCompleter,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.medication_styles import tone_color
from app.models.drug_safety import PatientCondition
from app.models.medication import SafetyCheckLog
from app.services.drug_safety_service import (
    UNKNOWN,
    VERDICT_AVOID,
    VERDICT_CAUTION,
    VERDICT_COMPATIBLE,
    VERDICT_NO_FLAGS,
    ConditionFinding,
    PairFinding,
    RuleFinding,
    SafetyReport,
)
from app.services.medication_service import MedicineOption, RegimenItem

# verdict -> (badge text, tone, icon, summary)
VERDICTS = {
    VERDICT_COMPATIBLE: ("COMPATIBLE PROFILE", "success", "shield-check",
                         "No known major interactions or condition contraindications found in "
                         "structured reference data."),
    VERDICT_NO_FLAGS: ("NO FLAGGED RISKS", "primary", "shield",
                       "Nothing was flagged, but {unknown} of these checks have no entry in the "
                       "reference database yet. Treat those as unverified, not as safe."),
    VERDICT_CAUTION: ("CAUTION ADVISED", "amber", "triangle-alert",
                      "Moderate interactions or precautions noted. Monitor symptoms, consider "
                      "dosage timing, and consult your healthcare provider."),
    VERDICT_AVOID: ("CAUTION STRONGLY ADVISED", "danger", "octagon-alert",
                    "Significant interactions or condition contraindications identified. "
                    "Consult your physician or pharmacist prior to combining."),
}
# finding severity -> (badge text for a condition, badge text for a pair, tone)
SEVERITIES = {
    "safe": ("COMPATIBLE PROFILE", "COMPATIBLE", "success"),
    "caution": ("CAUTION / PRECAUTIONS ADVISED", "CAUTION", "amber"),
    "avoid": ("AVOID / CONTRAINDICATED", "SIGNIFICANT INTERACTION / AVOID", "danger"),
    UNKNOWN: ("NOT ON RECORD", "NOT ON RECORD", "muted"),
}
DISCLAIMER = ("This check is based on structured reference data and does not replace "
              "professional medical advice. Results are advisory indications designed to "
              "highlight potential pharmacological interactions and condition precautions. "
              "Always consult your prescribing physician or dispensing pharmacist before "
              "starting, changing, or combining medications.")


class SafetyTab(QWidget):
    candidate_chosen = Signal(str)          # medicine id
    candidate_typed = Signal(str)           # free text, on Enter
    condition_toggled = Signal(str, bool)
    regimen_toggled = Signal(str, bool)     # RegimenItem.key
    remove_med_requested = Signal(str)
    add_med_requested = Signal()
    save_requested = Signal()
    monograph_requested = Signal(str)
    reload_requested = Signal(str)          # safety-check log id
    clear_log_requested = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._by_label: dict[str, MedicineOption] = {}
        self._log_open = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)
        root.addWidget(self._disclaimer())

        columns = QHBoxLayout()
        columns.setSpacing(18)
        left = QWidget()
        left.setObjectName("panel")
        left.setFixedWidth(430)
        self._left = QVBoxLayout(left)
        self._left.setContentsMargins(0, 0, 0, 0)
        self._left.setSpacing(14)
        self._left.addWidget(self._candidate_panel())
        self._left.addWidget(self._profile_panel())
        self._left.addWidget(self._regimen_panel())
        self._left.addStretch(1)
        columns.addWidget(left, 0, Qt.AlignmentFlag.AlignTop)

        right = QWidget()
        right.setObjectName("panel")
        self._right = QVBoxLayout(right)
        self._right.setContentsMargins(0, 0, 0, 0)
        self._right.setSpacing(14)
        self._results = QWidget()
        self._results.setObjectName("panel")
        self._right.addWidget(self._results)
        self._log_panel = QFrame()
        self._log_panel.setObjectName("mdPanel")
        self._right.addWidget(self._log_panel)
        self._right.addStretch(1)
        columns.addWidget(right, 1, Qt.AlignmentFlag.AlignTop)
        root.addLayout(columns)

    # ================================================================ left

    def _disclaimer(self) -> QFrame:
        box = QFrame()
        box.setObjectName("mdPanel")
        row = QHBoxLayout(box)
        row.setContentsMargins(16, 12, 16, 12)
        row.setSpacing(12)
        row.addWidget(_icon("info", 18, "primary"), 0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(3)
        text.addWidget(QLabel("MEDICAL DISCLAIMER & CLINICAL ADVISORY NOTICE",
                              objectName="mdPanelHeading"))
        body = QLabel(DISCLAIMER, objectName="mdMuted")
        body.setWordWrap(True)
        text.addWidget(body)
        row.addLayout(text, 1)
        return box

    def _candidate_panel(self) -> QFrame:
        panel, body, _head = _step_panel("1", "Candidate Drug to Evaluate", "SEARCH OR PRESET")
        field = QFrame()
        field.setObjectName("mdSearchField")
        row = QHBoxLayout(field)
        row.setContentsMargins(10, 0, 6, 0)
        row.setSpacing(6)
        row.addWidget(_icon("search", 15, "muted"))
        self.search = QLineEdit()
        self.search.setObjectName("mdSearchInput")
        self.search.setPlaceholderText("Search a medicine by name, generic or brand...")
        self.search.returnPressed.connect(lambda: self.candidate_typed.emit(self.search.text()))
        row.addWidget(self.search, 1)
        field.setFixedHeight(38)
        body.addWidget(field)

        self._model = QStringListModel([], self)
        completer = QCompleter(self._model, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setMaxVisibleItems(7)
        completer.popup().setObjectName("mdSuggest")
        completer.activated[str].connect(self._on_completed)
        self.search.setCompleter(completer)

        head = QHBoxLayout()
        head.addWidget(QLabel("Quick Test Candidates:", objectName="mdSmallMuted"))
        head.addStretch(1)
        head.addWidget(QLabel("From your database", objectName="mdSmallAccent"))
        body.addLayout(head)
        self._chips_host = QWidget()
        self._chips_host.setObjectName("panel")
        self._chips = FlowLayout(self._chips_host, spacing=6)
        body.addWidget(self._chips_host)
        return panel

    def _profile_panel(self) -> QFrame:
        panel, body, head = _step_panel("2", "Patient Health Profile", "")
        self._active_badge = QLabel("0 Active", objectName="mdActiveBadge")
        head.addWidget(self._active_badge)
        self._profile_hint = QLabel("Select any medical conditions or comorbidities to "
                                    "cross-check:", objectName="mdMuted")
        self._profile_hint.setWordWrap(True)
        body.addWidget(self._profile_hint)
        self._conditions_host = QWidget()
        self._conditions_host.setObjectName("panel")
        self._conditions = QGridLayout(self._conditions_host)
        self._conditions.setContentsMargins(0, 0, 0, 0)
        self._conditions.setSpacing(8)
        body.addWidget(self._conditions_host)
        return panel

    def _regimen_panel(self) -> QFrame:
        panel, body, head = _step_panel("3", "Active Regimen to Cross-Check", "")
        add = QPushButton(" Add Med")
        add.setObjectName("mdLinkButton")
        add.setIcon(lucide.icon("plus", 14, tone_color("primary")))
        add.setCursor(Qt.CursorShape.PointingHandCursor)
        add.clicked.connect(self.add_med_requested.emit)
        head.addWidget(add)
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
            self.search.setText(option.name)
            self.candidate_chosen.emit(option.medicine_id)

    def set_candidate_text(self, text: str) -> None:
        self.search.blockSignals(True)
        self.search.setText(text)
        self.search.blockSignals(False)

    def set_quick(self, options: list[MedicineOption], selected_id: str) -> None:
        _clear(self._chips)
        if not options:
            self._chips.addWidget(QLabel("Add medicines to your database to see quick "
                                         "candidates here.", objectName="mdSmallMuted"))
            return
        for option in options:
            chip = ClickFrame("mdChipButton", on=option.medicine_id == selected_id)
            row = QHBoxLayout(chip)
            row.setContentsMargins(10, 5, 6, 5)
            row.setSpacing(6)
            name = QLabel(option.name, objectName="mdChipText")
            name.setProperty("on", chip.property("on"))
            row.addWidget(name)
            row.addWidget(QLabel("OTC" if option.is_otc else "Rx", objectName="mdChipTag"))
            chip.clicked.connect(lambda o=option: self._pick(o))
            self._chips.addWidget(chip)

    def _pick(self, option: MedicineOption) -> None:
        self.set_candidate_text(option.name)
        self.candidate_chosen.emit(option.medicine_id)

    def set_conditions(self, conditions: list[PatientCondition], selected: set[str],
                       candidate_name: str) -> None:
        _clear(self._conditions)
        self._active_badge.setText(f"{len(selected & {c.id for c in conditions})} Active")
        target = candidate_name or "the chosen medicine"
        self._profile_hint.setText("Select any medical conditions or comorbidities to "
                                   f"cross-check against {target}:")
        if not conditions:
            note = QLabel("No health-profile conditions in the reference database yet.",
                          objectName="mdSmallMuted")
            note.setWordWrap(True)
            self._conditions.addWidget(note, 0, 0, 1, 2)
            return
        for index, condition in enumerate(conditions):
            on = condition.id in selected
            button = ClickFrame("mdConditionToggle", on=on)
            row = QHBoxLayout(button)
            row.setContentsMargins(10, 8, 10, 8)
            row.setSpacing(8)
            mark = _icon("circle-check" if on else "circle", 15,
                         "primary" if on else "muted")
            row.addWidget(mark, 0, Qt.AlignmentFlag.AlignTop)
            text = QVBoxLayout()
            text.setSpacing(1)
            for value, name in ((condition.label, "mdToggleTitle"),
                                (condition.description, "mdToggleSub")):
                label = QLabel(value, objectName=name)
                label.setWordWrap(True)
                text.addWidget(label)
            row.addLayout(text, 1)
            button.clicked.connect(lambda cid=condition.id, now=on:
                                   self.condition_toggled.emit(cid, not now))
            self._conditions.addWidget(button, index // 2, index % 2)

    def set_regimen(self, items: list[RegimenItem], included: set[str]) -> None:
        _clear(self._regimen)
        if not items:
            note = QLabel("Nothing to cross-check yet. Use Add Med for medicines you take "
                          "regularly; active courses appear here automatically.",
                          objectName="mdSmallMuted")
            note.setWordWrap(True)
            self._regimen.addWidget(note)
            return
        for item in items:
            row_frame = QFrame()
            row_frame.setObjectName("mdRegimenRow")
            row = QHBoxLayout(row_frame)
            row.setContentsMargins(12, 8, 8, 8)
            row.setSpacing(10)
            box = QCheckBox()
            box.setChecked(item.key in included)
            box.toggled.connect(lambda on, key=item.key: self.regimen_toggled.emit(key, on))
            row.addWidget(box)
            text = QVBoxLayout()
            text.setSpacing(1)
            name = QLabel(item.name, objectName="mdToggleTitle")
            name.setWordWrap(True)
            text.addWidget(name)
            # Tags on their own line, so a long name keeps the full width.
            if item.is_course or not item.medicine_id:
                tags = QHBoxLayout()
                tags.setSpacing(6)
                if item.is_course:
                    tags.addWidget(_badge("COURSE", "primary"))
                if not item.medicine_id:
                    tags.addWidget(_badge("NOT IN DATABASE", "muted"))
                tags.addStretch(1)
                text.addLayout(tags)
            if item.detail:
                detail = QLabel(item.detail, objectName="mdToggleSubAccent")
                detail.setWordWrap(True)
                text.addWidget(detail)
            row.addLayout(text, 1)
            if item.is_course:
                # Courses leave the regimen on their own when completed or
                # abandoned, so they have no remove button here.
                row.addSpacing(30)
            else:
                trash = QPushButton()
                trash.setObjectName("mdIconButton")
                trash.setIcon(lucide.icon("trash-2", 15, tone_color("muted")))
                trash.setToolTip("Remove from current medications")
                trash.setCursor(Qt.CursorShape.PointingHandCursor)
                trash.clicked.connect(lambda _c=False, key=item.key:
                                      self.remove_med_requested.emit(key))
                row.addWidget(trash)
            self._regimen.addWidget(row_frame)

    # =============================================================== right

    def _reset_results(self) -> QVBoxLayout:
        old = self._results
        self._results = QWidget()
        self._results.setObjectName("panel")
        self._right.replaceWidget(old, self._results)
        old.setParent(None)
        old.deleteLater()
        layout = QVBoxLayout(self._results)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        return layout

    def show_prompt(self) -> None:
        layout = self._reset_results()
        layout.addWidget(_message_card("pill", "Choose a candidate drug",
                                       "Search your medicine database on the left, or pick "
                                       "a quick candidate, to check it against your health "
                                       "profile and current regimen."))

    def show_not_found(self, text: str) -> None:
        layout = self._reset_results()
        layout.addWidget(_message_card(
            "circle-help", f"“{text}” isn't in the medicine database",
            "The check only uses verified reference data, so a medicine that isn't in the "
            "database can't be evaluated. Pick one from the suggestions list instead."))

    def show_report(self, report: SafetyReport) -> None:
        layout = self._reset_results()
        layout.addWidget(self._verdict_card(report))

        layout.addLayout(_section("heart-pulse", "danger",
                                  f"CONDITION-TO-DRUG COMPATIBILITY ({len(report.conditions)} "
                                  "CHECKED)", "Evaluated against your active health profile"))
        if report.conditions:
            for finding in report.conditions:
                layout.addWidget(_condition_card(finding))
        else:
            layout.addWidget(_note_card("No conditions are ticked in your health profile."))

        pairs = report.candidate_pairs
        layout.addLayout(_section("activity", "primary",
                                  f"DRUG-TO-DRUG INTERACTIONS ({len(pairs)} CHECKED)",
                                  "Pairwise check against your active medication regimen"))
        if pairs:
            for finding in pairs:
                layout.addWidget(_pair_card(finding))
        else:
            layout.addWidget(_note_card("No current medications are ticked for "
                                        "cross-checking."))

        if report.regimen_pairs:
            count = len(report.regimen_pairs)
            layout.addWidget(QLabel(f"WITHIN YOUR CURRENT REGIMEN ({count} "
                                    f"PAIR{'S' if count != 1 else ''})",
                                    objectName="mdSubSection"))
            for finding in report.regimen_pairs:
                layout.addWidget(_pair_card(finding))

        if report.rules:
            layout.addLayout(_section("layers", "danger",
                                      f"COMBINATION RISKS ({len(report.rules)} FOUND)",
                                      "Three or more drugs, or a drug plus a condition"))
            for finding in report.rules:
                layout.addWidget(_rule_card(finding))

        if report.not_in_database:
            names = ", ".join(d.name for d in report.not_in_database)
            layout.addWidget(_note_card(f"Not checked, because they aren't in the medicine "
                                        f"database: {names}."))

    def _verdict_card(self, report: SafetyReport) -> QFrame:
        badge_text, tone, icon_name, summary = VERDICTS[report.verdict]
        card = QFrame()
        card.setObjectName("mdVerdict")
        card.setProperty("tone", tone)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 16)
        layout.setSpacing(12)

        top = QHBoxLayout()
        top.setSpacing(14)
        tile = QFrame()
        tile.setObjectName("mdVerdictTile")
        tile.setProperty("tone", tone)
        tile.setFixedSize(44, 44)
        tile_layout = QVBoxLayout(tile)
        tile_layout.setContentsMargins(0, 0, 0, 0)
        tile_layout.addWidget(_icon(icon_name, 22, "white"), 0, Qt.AlignmentFlag.AlignCenter)
        top.addWidget(tile, 0, Qt.AlignmentFlag.AlignTop)

        titles = QVBoxLayout()
        titles.setSpacing(2)
        titles.addWidget(QLabel("SAFETY EVALUATION PROFILE", objectName="mdTileLabel"))
        name_row = QHBoxLayout()
        name_row.setSpacing(8)
        name_row.addWidget(QLabel(report.candidate.name, objectName="mdVerdictName"))
        name_row.addWidget(_badge(badge_text, tone), 0, Qt.AlignmentFlag.AlignVCenter)
        name_row.addStretch(1)
        titles.addLayout(name_row)
        top.addLayout(titles, 1)

        save = QPushButton(" Save Check")
        save.setObjectName("mdSecondary")
        save.setIcon(lucide.icon("bookmark-plus", 14, tone_color("text")))
        save.setCursor(Qt.CursorShape.PointingHandCursor)
        save.clicked.connect(self.save_requested.emit)
        top.addWidget(save, 0, Qt.AlignmentFlag.AlignTop)
        monograph = QPushButton("View Monograph ")
        monograph.setObjectName("mdPrimary")
        monograph.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        monograph.setIcon(lucide.icon("external-link", 14, "#FFFFFF"))
        monograph.setCursor(Qt.CursorShape.PointingHandCursor)
        monograph.clicked.connect(
            lambda: self.monograph_requested.emit(report.candidate.medicine_id))
        top.addWidget(monograph, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(top)

        text = QLabel(summary.format(unknown=report.unknown_count), objectName="mdBoxBody")
        text.setWordWrap(True)
        layout.addWidget(text)
        layout.addWidget(_divider())
        facts = []
        if report.candidate.drug_class:
            facts.append(f"<b>Drug Class:</b> {report.candidate.drug_class}")
        if report.candidate.generic_name:
            facts.append(f"<b>Generic Name:</b> {report.candidate.generic_name}")
        meta = QLabel("  •  ".join(facts) or "No class or generic name on record.",
                      objectName="mdSmallBody")
        meta.setWordWrap(True)
        layout.addWidget(meta)
        return card

    # ----------------------------------------------------------------- log

    def show_log(self, logs: list[SafetyCheckLog], condition_names: dict[str, str]) -> None:
        old_layout = self._log_panel.layout()
        if old_layout is not None:
            _clear(old_layout)
            QWidget().setLayout(old_layout)     # detach the old layout
        layout = QVBoxLayout(self._log_panel)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        head = QPushButton()
        head.setObjectName("mdLogHeader")
        head.setCursor(Qt.CursorShape.PointingHandCursor)
        row = QHBoxLayout(head)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        row.addWidget(_icon("history", 16, "primary"))
        title = QLabel(f"PAST SAFETY CHECKS LOG ({len(logs)})", objectName="mdPanelHeading")
        title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        row.addWidget(title)
        row.addWidget(_icon("chevron-up" if self._log_open else "chevron-down", 14, "muted"))
        row.addStretch(1)
        head.setFixedHeight(28)
        head.clicked.connect(lambda: self._toggle_log(logs, condition_names))
        top = QHBoxLayout()
        top.addWidget(head, 1)
        if self._log_open and logs:
            clear = QPushButton("Clear History")
            clear.setObjectName("mdDangerLink")
            clear.setCursor(Qt.CursorShape.PointingHandCursor)
            clear.clicked.connect(self.clear_log_requested.emit)
            top.addWidget(clear)
        layout.addLayout(top)

        if not self._log_open:
            return
        layout.addWidget(_divider())
        if not logs:
            empty = QLabel("No safety checks recorded yet. Click “Save Check” on "
                           "any evaluation to keep a log.", objectName="mdSmallMuted")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(empty)
            return
        for log in logs:
            entry = QFrame()
            entry.setObjectName("mdRegimenRow")
            line = QHBoxLayout(entry)
            line.setContentsMargins(12, 8, 10, 8)
            text = QVBoxLayout()
            text.setSpacing(2)
            name_row = QHBoxLayout()
            name_row.setSpacing(8)
            name_row.addWidget(QLabel(log.candidate_name, objectName="mdToggleTitle"))
            label, tone = _log_badge(log.verdict)
            name_row.addWidget(_badge(label, tone))
            name_row.addStretch(1)
            text.addLayout(name_row)
            when = datetime.fromisoformat(log.created_at)
            conditions = ", ".join(condition_names.get(c, c) for c in log.condition_ids)
            text.addWidget(QLabel(
                f"{when:%m/%d/%Y, %I:%M %p} • {len(log.condition_ids)} Conditions"
                + (f" ({conditions})" if conditions else "")
                + f" • {len(log.regimen_ids)} Regimen Meds", objectName="mdSmallMuted"))
            line.addLayout(text, 1)
            again = QPushButton("Reload Check")
            again.setObjectName("mdLinkButton")
            again.setCursor(Qt.CursorShape.PointingHandCursor)
            again.clicked.connect(lambda _c=False, lid=log.id: self.reload_requested.emit(lid))
            line.addWidget(again)
            layout.addWidget(entry)

    def _toggle_log(self, logs, condition_names) -> None:
        self._log_open = not self._log_open
        self.show_log(logs, condition_names)

    def open_log(self) -> None:
        self._log_open = True


# ======================================================================
# cards
# ======================================================================

def _condition_card(finding: ConditionFinding) -> QFrame:
    badge_text, _pair_text, tone = SEVERITIES[finding.severity]
    card = QFrame()
    card.setObjectName("mdFinding")
    card.setProperty("tone", tone)
    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(8)
    head = QHBoxLayout()
    title = finding.condition.label
    if not finding.drug.is_candidate:
        title += f" • {finding.drug.name}"
    head.addWidget(QLabel(title, objectName="mdFindingTitle"))
    head.addStretch(1)
    head.addWidget(_badge(badge_text, tone))
    layout.addLayout(head)
    if finding.severity == UNKNOWN:
        body = (f"No entry in the reference database for {finding.drug.name} in "
                f"{finding.condition.label.lower()}. This is not confirmation that it is "
                "safe; ask your pharmacist.")
    else:
        body = finding.summary or "No summary on record."
    text = QLabel(body, objectName="mdBoxBody")
    text.setWordWrap(True)
    layout.addWidget(text)
    if finding.guidance:
        layout.addWidget(_inner_box(f"<b>Advisory guidance:</b> {finding.guidance}"))
    return card


def _pair_card(finding: PairFinding) -> QFrame:
    _cond_text, badge_text, tone = SEVERITIES[finding.severity]
    if finding.duplicate:
        badge_text = "DUPLICATE THERAPY"
    card = QFrame()
    card.setObjectName("mdFinding")
    card.setProperty("tone", tone)
    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(8)
    head = QHBoxLayout()
    head.setSpacing(6)
    head.addWidget(QLabel(finding.first.name, objectName="mdFindingTitle"))
    head.addWidget(_icon("arrow-left-right", 13, "muted"))
    head.addWidget(QLabel(finding.second.name, objectName="mdFindingAccent"))
    head.addStretch(1)
    head.addWidget(_badge(badge_text, tone))
    layout.addLayout(head)
    if finding.severity == UNKNOWN:
        body = (f"No entry for {finding.first.name} with {finding.second.name} in the "
                "reference database. This is not confirmation that they are safe together.")
    else:
        body = finding.description or "No description on record."
    text = QLabel(body, objectName="mdBoxBody")
    text.setWordWrap(True)
    layout.addWidget(text)
    lines = []
    if finding.clinical_significance:
        lines.append(f"<b>Clinical Significance:</b> {finding.clinical_significance}")
    if finding.recommendation:
        lines.append(f"<span style='color:{tone_color('primary')}'>"
                     f"{finding.recommendation}</span>")
    if lines:
        layout.addWidget(_inner_box("<br>".join(lines)))
    return card


def _rule_card(finding: RuleFinding) -> QFrame:
    rule = finding.rule
    _cond_text, badge_text, tone = SEVERITIES.get(rule.severity, SEVERITIES["caution"])
    card = QFrame()
    card.setObjectName("mdFinding")
    card.setProperty("tone", tone)
    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(8)
    head = QHBoxLayout()
    head.addWidget(QLabel(rule.name, objectName="mdFindingTitle"))
    head.addStretch(1)
    head.addWidget(_badge(badge_text, tone))
    layout.addLayout(head)
    layout.addWidget(QLabel("Involves: " + ", ".join(d.name for d in finding.drugs),
                            objectName="mdSmallMuted"))
    text = QLabel(rule.description, objectName="mdBoxBody")
    text.setWordWrap(True)
    layout.addWidget(text)
    lines = []
    if rule.clinical_significance:
        lines.append(f"<b>Clinical Significance:</b> {rule.clinical_significance}")
    if rule.recommendation:
        lines.append(f"<span style='color:{tone_color('primary')}'>{rule.recommendation}</span>")
    if lines:
        layout.addWidget(_inner_box("<br>".join(lines)))
    return card


def _message_card(icon_name: str, title: str, body: str) -> QFrame:
    card = QFrame()
    card.setObjectName("mdPanel")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(24, 30, 24, 30)
    layout.setSpacing(8)
    layout.addWidget(_icon(icon_name, 28, "primary"), 0, Qt.AlignmentFlag.AlignHCenter)
    heading = QLabel(title, objectName="mdEmptyTitle")
    heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
    heading.setWordWrap(True)
    layout.addWidget(heading)
    text = QLabel(body, objectName="mdMuted")
    text.setAlignment(Qt.AlignmentFlag.AlignCenter)
    text.setWordWrap(True)
    layout.addWidget(text)
    return card


def _note_card(text: str) -> QFrame:
    card = QFrame()
    card.setObjectName("mdPanel")
    layout = QHBoxLayout(card)
    layout.setContentsMargins(16, 12, 16, 12)
    layout.setSpacing(10)
    layout.addWidget(_icon("info", 15, "muted"), 0, Qt.AlignmentFlag.AlignTop)
    label = QLabel(text, objectName="mdMuted")
    label.setWordWrap(True)
    layout.addWidget(label, 1)
    return card


# ======================================================================
# small helpers
# ======================================================================

def _step_panel(number: str, title: str,
                hint: str) -> tuple[QFrame, QVBoxLayout, QHBoxLayout]:
    panel = QFrame()
    panel.setObjectName("mdPanel")
    body = QVBoxLayout(panel)
    body.setContentsMargins(16, 14, 16, 16)
    body.setSpacing(10)
    head = QHBoxLayout()
    head.setSpacing(10)
    circle = QLabel(number, objectName="mdStepNumber")
    circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
    circle.setFixedSize(22, 22)
    head.addWidget(circle)
    head.addWidget(QLabel(title, objectName="mdStepTitle"))
    head.addStretch(1)
    if hint:
        head.addWidget(QLabel(hint, objectName="mdStepHint"))
    body.addLayout(head)
    return panel, body, head


def _section(icon_name: str, tone: str, title: str, note: str) -> QHBoxLayout:
    row = QHBoxLayout()
    row.setSpacing(8)
    row.addWidget(_icon(icon_name, 16, tone))
    row.addWidget(QLabel(title, objectName="mdSectionTitle"))
    row.addStretch(1)
    row.addWidget(QLabel(note, objectName="mdSmallAccent"))
    return row


def _inner_box(html: str) -> QFrame:
    box = QFrame()
    box.setObjectName("mdCountdown")
    layout = QVBoxLayout(box)
    layout.setContentsMargins(12, 9, 12, 9)
    label = QLabel(html, objectName="mdSmallBody")
    label.setWordWrap(True)
    layout.addWidget(label)
    return box


def _icon(name: str, size: int, tone: str) -> QLabel:
    label = QLabel()
    label.setPixmap(lucide.pixmap(name, size, tone_color(tone)))
    label.setFixedSize(size, size)
    return label


def _badge(text: str, tone: str) -> QLabel:
    badge = QLabel(text, objectName="mdBadge")
    badge.setProperty("tone", tone)
    return badge


def _log_badge(verdict: str) -> tuple[str, str]:
    return {
        VERDICT_COMPATIBLE: ("COMPATIBLE", "success"),
        VERDICT_NO_FLAGS: ("NO FLAGS", "primary"),
        VERDICT_CAUTION: ("CAUTION", "amber"),
        VERDICT_AVOID: ("AVOID", "danger"),
    }.get(verdict, ("CHECKED", "muted"))


def _divider() -> QFrame:
    line = QFrame()
    line.setObjectName("mdDivider")
    line.setFixedHeight(1)
    return line


def _clear(layout: QLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()
        elif item.layout() is not None:
            _clear(item.layout())


class ClickFrame(QFrame):
    """A clickable card. Unlike a QPushButton, a frame grows to fit the
    labels inside it, so wrapped text never overlaps. The "on" property
    drives the selected look in the stylesheet."""

    clicked = Signal()

    def __init__(self, object_name: str, on: bool = False) -> None:
        super().__init__()
        self.setObjectName(object_name)
        self.setProperty("on", "true" if on else "false")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
                event.position().toPoint()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class FlowLayout(QLayout):
    """Lays chips left to right and wraps to a new line when full."""

    def __init__(self, parent: QWidget, spacing: int = 6) -> None:
        super().__init__(parent)
        self._items = []
        self._spacing = spacing
        self.setContentsMargins(0, 0, 0, 0)

    def addItem(self, item) -> None:  # noqa: N802
        self._items.append(item)

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int):  # noqa: N802
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int):  # noqa: N802
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def expandingDirections(self):  # noqa: N802
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:  # noqa: N802
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802
        return self._arrange(QRect(0, 0, width, 0), apply=False)

    def setGeometry(self, rect: QRect) -> None:  # noqa: N802
        super().setGeometry(rect)
        self._arrange(rect, apply=True)

    def sizeHint(self) -> QSize:  # noqa: N802
        return self.minimumSize()

    def minimumSize(self) -> QSize:  # noqa: N802
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        return size

    def _arrange(self, rect: QRect, apply: bool) -> int:
        x, y, line_height = rect.x(), rect.y(), 0
        for item in self._items:
            hint = item.sizeHint().expandedTo(item.minimumSize())
            if x + hint.width() > rect.right() + 1 and line_height > 0:
                x, y = rect.x(), y + line_height + self._spacing
                line_height = 0
            if apply:
                item.setGeometry(QRect(QPoint(x, y), hint))
            x += hint.width() + self._spacing
            line_height = max(line_height, hint.height())
        return y + line_height - rect.y()
