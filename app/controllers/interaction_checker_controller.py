"""Wires the Drug Interaction Checker to its two services.

    DrugSafetyService   the reference data and the check itself
    CaseStudyService    medicine pickers and saved case studies

The case being built (candidate, regimen, comorbidities) lives only in this
controller's memory: it is a scratchpad, and nothing about it is stored
until the user chooses Save as Case Study.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QDialog

from app.core.sync_worker import SyncWorker, start_worker
from app.core.theme import Theme
from app.services.case_study_service import CaseStudyService, MedicineOption
from app.services.drug_safety_service import DrugSafetyService, SafetyReport
from app.ui.views.interaction_checker_view import InteractionCheckerView
from app.ui.views.interaction_dialogs import AddDrugDialog, ConfirmDialog, SaveCaseDialog
from app.ui.views.interaction_widgets import VERDICTS


class InteractionCheckerController(QObject):
    # "View Monograph" / "Full Monograph": the shell opens Medicine Reference.
    monograph_requested = Signal(str)

    # A check was saved into a note in the Study Notebook (item id).
    case_saved = Signal(str)

    def __init__(self, view: InteractionCheckerView, cases: CaseStudyService,
                 safety: DrugSafetyService, brands_for=None, notebook=None) -> None:
        super().__init__()
        self._view = view
        self._cases = cases
        self._safety = safety
        self._brands_for = brands_for or (lambda _id: [])
        self._notebook = notebook            # NotebookService, for linked saves
        self._link_id = ""                   # the note this check is saved into

        # The case on screen.
        self._candidate_id = ""
        self._not_found = ""
        self._regimen: list[str] = []          # medicine ids, in the order added
        self._excluded: set[str] = set()       # regimen drugs unticked for this check
        self._conditions: set[str] = set()
        self._report: Optional[SafetyReport] = None

        # The browser.
        self._browse_id = ""
        self._browse_filter = ""

        checker = view.checker
        checker.candidate_chosen.connect(self._choose)
        checker.candidate_typed.connect(self._typed)
        checker.candidate_cleared.connect(self._clear_candidate)
        checker.condition_toggled.connect(self._toggle_condition)
        checker.regimen_toggled.connect(self._toggle_regimen)
        checker.remove_drug_requested.connect(self._remove_drug)
        checker.add_drug_requested.connect(self._add_drug)
        checker.save_requested.connect(self._save_case)
        checker.monograph_requested.connect(self._open_monograph)

        view.cases.filters_changed.connect(lambda *_: self._draw_cases())
        view.cases.open_requested.connect(self._open_case)
        view.cases.duplicate_requested.connect(self._duplicate_case)
        view.cases.delete_requested.connect(self._delete_case)

        view.browser.drug_chosen.connect(self._browse)
        view.browser.filter_changed.connect(self._set_browse_filter)
        view.browser.check_in_case_requested.connect(self._check_in_case)
        view.browser.monograph_requested.connect(self._open_monograph)

        view.new_case_requested.connect(self.new_case)
        view.unlink_requested.connect(self.unlink)
        view.theme_changed.connect(self.refresh)

        self.refresh()
        self._start_sync()

    # --------------------------------------------------------------- sync

    def _start_sync(self) -> None:
        worker = SyncWorker(self._safety)
        worker.sync_finished.connect(self._on_synced)
        start_worker(worker)

    def _on_synced(self, changed: bool, _error: str) -> None:
        # Offline is fine: the last downloaded copy keeps working.
        if changed:
            self._safety.reload()
            self.refresh()

    # ------------------------------------------------------------ drawing

    def _signature(self, options) -> tuple:
        return (Theme.mode(), len(options), tuple(repr(c) for c in self._cases.cases()))

    def refresh_if_stale(self) -> None:
        """Redraw only if the data or the theme changed since the last
        redraw (the shell calls this every time the tab is opened)."""
        if self._signature(self._cases.medicine_options()) != getattr(self, "_drawn", None):
            self.refresh()

    def refresh(self) -> None:
        """Redraw everything from current data (also after a theme switch)."""
        options = self._cases.medicine_options()
        self._drawn = self._signature(options)
        known = {o.medicine_id for o in options}
        # Medicines removed from the database drop out of the case.
        self._regimen = [m for m in self._regimen if m in known]
        if self._candidate_id and self._candidate_id not in known:
            self._candidate_id = ""
        self._view.show_stats(len(options), self._safety.documented_count(),
                              len(self._cases.cases()))
        self._draw_checker(options)
        self._draw_cases()
        self._draw_browser(options)

    def _draw_checker(self, options: Optional[list[MedicineOption]] = None) -> None:
        options = options if options is not None else self._cases.medicine_options()
        by_id = {o.medicine_id: o for o in options}
        tab = self._view.checker
        tab.set_options(options)
        tab.set_quick(self._cases.quick_candidates(), self._candidate_id)
        tab.set_conditions(self._safety.conditions(), self._conditions)
        tab.set_regimen([by_id[m] for m in self._regimen if m in by_id],
                        set(self._regimen) - self._excluded)
        candidate = by_id.get(self._candidate_id)
        tab.set_candidate_text(candidate.name if candidate else self._not_found)

        if self._not_found:
            self._report = None
            tab.show_not_found(self._not_found)
        elif candidate is None:
            self._report = None
            tab.show_prompt()
        else:
            self._report = self._evaluate(self._candidate_id, self._included(),
                                          self._conditions)
            tab.show_report(self._report, candidate)

    def _evaluate(self, candidate_id: str, regimen: list[str],
                  conditions: set[str]) -> SafetyReport:
        candidate = self._safety.drug_for("", candidate_id, is_candidate=True)
        drugs = [self._safety.drug_for("", m) for m in regimen]
        return self._safety.evaluate(candidate, drugs, conditions)

    def _included(self) -> list[str]:
        return [m for m in self._regimen if m not in self._excluded]

    def _draw_cases(self) -> None:
        tab = self._view.cases
        names = {o.medicine_id: o.name for o in self._cases.medicine_options()}
        tab.set_tags(self._cases.all_tags())
        cards = []
        for case in self._cases.search(*tab.filters()):
            # The verdict is recomputed from today's reference data, so a saved
            # case never shows a result the database no longer supports.
            report = self._evaluate(case.candidate_id, case.regimen_ids,
                                    set(case.condition_ids))
            cards.append((case, names.get(case.candidate_id, "Not in reference data"),
                          report.verdict, len(case.regimen_ids), len(case.condition_ids)))
        tab.show_cases(cards, total=len(self._cases.cases()))

    def _draw_browser(self, options: Optional[list[MedicineOption]] = None) -> None:
        options = options if options is not None else self._cases.medicine_options()
        tab = self._view.browser
        option = next((o for o in options if o.medicine_id == self._browse_id), None)
        tab.set_options(options, self._browse_id if option else "")
        if option is None:
            tab.show_empty()
            return
        drug = self._safety.drug_for("", option.medicine_id)
        tab.show_profile(option, self._brands_for(option.medicine_id), self._browse_filter,
                         self._safety.interactions_for(option.medicine_id),
                         self._safety.condition_entries_for(option.medicine_id),
                         self._safety.rules_for(drug))

    # ----------------------------------------------------- checker actions

    def new_case(self) -> None:
        self._candidate_id, self._not_found = "", ""
        self._regimen, self._excluded, self._conditions = [], set(), set()
        self._draw_checker()
        self._view.show_tab(0)

    def _choose(self, medicine_id: str) -> None:
        self._candidate_id, self._not_found = medicine_id, ""
        self._draw_checker()

    def _typed(self, text: str) -> None:
        text = text.strip()
        if not text:
            return
        medicine_id = self._cases.match_medicine(text)
        if medicine_id:
            self._choose(medicine_id)
        else:
            self._candidate_id, self._not_found = "", text
            self._draw_checker()

    def _clear_candidate(self) -> None:
        self._candidate_id, self._not_found = "", ""
        self._draw_checker()

    def _toggle_condition(self, condition_id: str, on: bool) -> None:
        if on:
            self._conditions.add(condition_id)
        else:
            self._conditions.discard(condition_id)
        self._draw_checker()

    def _toggle_regimen(self, medicine_id: str, on: bool) -> None:
        if on:
            self._excluded.discard(medicine_id)
        else:
            self._excluded.add(medicine_id)
        self._draw_checker()

    def _remove_drug(self, medicine_id: str) -> None:
        self._regimen = [m for m in self._regimen if m != medicine_id]
        self._excluded.discard(medicine_id)
        self._draw_checker()

    def _add_drug(self) -> None:
        dialog = AddDrugDialog(self._view, self._cases.medicine_options(), set(self._regimen))
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.chosen is not None:
            self._regimen.append(dialog.chosen.medicine_id)
            self._draw_checker()

    # ------------------------------------------------- linked to a note

    def edit_for_item(self, item_id: str) -> None:
        """Opened from a note ("Add / Edit in Drug Interaction Checker"):
        load that note's saved check, if any, and save back into it."""
        item = self._notebook.get(item_id) if self._notebook else None
        if item is None:
            return
        self._link_id = item_id
        data = item.interaction_data
        self._candidate_id, self._not_found = data.get("candidate_id", ""), ""
        self._regimen = list(data.get("regimen_ids", []))
        self._excluded = set()
        self._conditions = set(data.get("condition_ids", []))
        self._view.set_link(item.title)
        self._draw_checker()
        self._view.show_tab(0)

    def unlink(self) -> None:
        self._link_id = ""
        self._view.set_link("")
        self._draw_checker()

    def _save_to_note(self) -> None:
        item = self._notebook.get(self._link_id)
        if item is None:
            self.unlink()
            return
        data = {"candidate_id": self._candidate_id, "regimen_ids": self._included(),
                "condition_ids": sorted(self._conditions)}
        error = self._notebook.attach(item.id, "interaction", data)
        if error:
            return
        self._view.set_link(item.title, saved=True)
        self._draw_checker()
        self.case_saved.emit(item.id)

    def _save_case(self) -> None:
        if self._report is None:
            return
        if self._link_id and self._notebook is not None:
            self._save_to_note()
            return
        candidate = self._cases.option(self._candidate_id)
        badge_text, tone, _icon, _summary = VERDICTS[self._report.verdict]
        included = self._included()
        dialog = SaveCaseDialog(self._view, candidate.name if candidate else "",
                                len(included), len(self._conditions), badge_text, tone)

        def try_save() -> None:
            error = self._cases.save(candidate_id=self._candidate_id, regimen_ids=included,
                                     condition_ids=sorted(self._conditions),
                                     **dialog.values())
            if error:
                dialog.show_error(error)
            else:
                QDialog.accept(dialog)

        dialog.confirm.clicked.connect(try_save)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh()

    # ------------------------------------------------------- case actions

    def describe(self, candidate_id: str, regimen_ids: list[str],
                 condition_ids: list[str]) -> dict:
        """A case in words, for the Study Notebook's quick view. The verdict
        is worked out from today's reference data, never stored."""
        names = {o.medicine_id: o.name for o in self._cases.medicine_options()}
        labels = {c.id: c.label for c in self._safety.conditions()}
        report = self._evaluate(candidate_id, list(regimen_ids), set(condition_ids))
        text, tone = VERDICTS[report.verdict][:2]
        return {"candidate": names.get(candidate_id, ""),
                "regimen": [names.get(m, "Not in reference data") for m in regimen_ids],
                "conditions": [labels.get(c, c) for c in condition_ids],
                "verdict": (text, tone)}

    def open_case(self, case_id: str) -> None:
        """Load a saved case into the Checker tab (from the notebook)."""
        self._open_case(case_id)

    def _open_case(self, case_id: str) -> None:
        case = self._cases.get(case_id)
        if case is None:
            return
        self._candidate_id, self._not_found = case.candidate_id, ""
        self._regimen = list(case.regimen_ids)
        self._excluded = set()
        self._conditions = set(case.condition_ids)
        self._draw_checker()
        self._view.show_tab(0)

    def _duplicate_case(self, case_id: str) -> None:
        self._cases.duplicate(case_id)
        self.refresh()

    def _delete_case(self, case_id: str) -> None:
        case = self._cases.get(case_id)
        if case is None:
            return
        dialog = ConfirmDialog(self._view, "Delete this case study?",
                               f"“{case.title}” will be removed from your saved "
                               "case studies.", "Delete")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._cases.delete(case_id)
            self.refresh()

    # ---------------------------------------------------- browser actions

    def _browse(self, medicine_id: str) -> None:
        self._browse_id = medicine_id
        self._draw_browser()

    def _set_browse_filter(self, severity: str) -> None:
        self._browse_filter = severity
        self._draw_browser()

    def _check_in_case(self, candidate_id: str, other_id: str) -> None:
        """Start a fresh case: the browsed drug against the other one."""
        self._candidate_id, self._not_found = candidate_id, ""
        self._regimen, self._excluded, self._conditions = [other_id], set(), set()
        self._draw_checker()
        self._view.show_tab(0)

    def _open_monograph(self, medicine_id: str) -> None:
        if medicine_id:
            self.monograph_requested.emit(medicine_id)
