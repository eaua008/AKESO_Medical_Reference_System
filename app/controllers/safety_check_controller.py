"""Wires Tab 2 (Interaction & Safety Check) to its two services.

    DrugSafetyService    public reference data and the check itself
    MedicationService    the patient's own data: current meds, ticked
                         conditions, saved checks

It also keeps the "Drug Safety Check" stat card current: that card checks
the current regimen on its own (every pair of current meds, plus the
ticked conditions), with no candidate drug.
"""

from typing import Callable, Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QDialog

from app.core.sync_worker import SyncWorker, start_worker
from app.services.drug_safety_service import (
    VERDICT_AVOID,
    VERDICT_CAUTION,
    VERDICT_COMPATIBLE,
    Drug,
    DrugSafetyService,
    SafetyReport,
)
from app.services.medication_service import MedicationService
from app.ui.views.medication_dialogs import ConfirmDialog
from app.ui.views.medication_safety_tab import SafetyTab


class SafetyCheckController(QObject):
    monograph_requested = Signal(str)

    def __init__(self, tab: SafetyTab, medications: MedicationService,
                 safety: DrugSafetyService, stat_card,
                 add_med: Callable[[], None], on_changed: Callable[[], None]) -> None:
        super().__init__()
        self._tab = tab
        self._meds = medications
        self._safety = safety
        self._stat = stat_card
        self._add_med = add_med            # opens the Add to Current Meds dialog
        self._on_changed = on_changed      # lets the page refresh its other parts
        self._candidate_id = ""
        self._candidate_name = ""
        self._not_found = ""
        self._excluded: set[str] = set()   # regimen keys unticked for this check
        self._report: Optional[SafetyReport] = None

        tab.candidate_chosen.connect(self.choose)
        tab.candidate_typed.connect(self._typed)
        tab.condition_toggled.connect(self._toggle_condition)
        tab.regimen_toggled.connect(self._toggle_med)
        tab.remove_med_requested.connect(self._remove_med)
        tab.add_med_requested.connect(self._add_med)
        tab.save_requested.connect(self._save)
        tab.monograph_requested.connect(self._open_monograph)
        tab.reload_requested.connect(self._reload_check)
        tab.clear_log_requested.connect(self._clear_log)

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

    def refresh(self) -> None:
        """Redraw every part of the tab from current data."""
        items = self._meds.regimen()
        keys = {i.key for i in items}
        self._excluded &= keys
        included = keys - self._excluded
        selected = self._meds.health_profile()
        conditions = self._safety.conditions()

        self._tab.set_options(self._meds.medicine_options())
        self._tab.set_quick(self._meds.quick_candidates(), self._candidate_id)
        self._tab.set_conditions(conditions, selected, self._candidate_name)
        self._tab.set_regimen(items, included)
        self._show_log()
        self._evaluate()
        self._update_stat_card()

    def _evaluate(self) -> None:
        if self._not_found:
            self._report = None
            self._tab.show_not_found(self._not_found)
            return
        if not self._candidate_id:
            self._report = None
            self._tab.show_prompt()
            return
        candidate = self._safety.drug_for(self._candidate_name, self._candidate_id,
                                          is_candidate=True)
        self._report = self._safety.evaluate(candidate, self._regimen_drugs(),
                                             self._meds.health_profile())
        self._tab.show_report(self._report)

    def _update_stat_card(self) -> None:
        drugs = self._regimen_drugs(include_all=True)
        if not drugs:
            self._stat.set("No regimen", "Add current meds to check them against each other")
            return
        report = self._safety.evaluate(None, drugs, self._meds.health_profile())
        verdict = report.verdict
        if verdict == VERDICT_AVOID:
            self._stat.set("Avoid Combination", "Significant interaction in your current "
                           "regimen", tone="danger")
        elif verdict == VERDICT_CAUTION:
            self._stat.set("Caution", "Precautions flagged in your current regimen",
                           tone="amber")
        elif verdict == VERDICT_COMPATIBLE:
            self._stat.set("Safe Profile", "No pairwise contraindications detected",
                           tone="success")
        else:
            self._stat.set("No Flags", f"{report.unknown_count} checks not on record yet",
                           tone="primary")

    def _regimen_drugs(self, include_all: bool = False) -> list[Drug]:
        return [self._safety.drug_for(i.name, i.medicine_id)
                for i in self._meds.regimen()
                if include_all or i.key not in self._excluded]

    def _show_log(self) -> None:
        names = {c.id: c.label for c in self._safety.conditions()}
        self._tab.show_log(self._meds.safety_checks(), names)

    # ------------------------------------------------------------ actions

    def choose(self, medicine_id: str) -> None:
        option = next((o for o in self._meds.medicine_options()
                       if o.medicine_id == medicine_id), None)
        if option is None:
            return
        self._candidate_id = medicine_id
        self._candidate_name = option.name
        self._not_found = ""
        self._tab.set_candidate_text(option.name)
        self.refresh()

    def _typed(self, text: str) -> None:
        text = text.strip()
        if not text:
            return
        medicine_id = self._meds.match_medicine(text)
        if medicine_id:
            self.choose(medicine_id)
        else:
            self._candidate_id, self._candidate_name, self._not_found = "", "", text
            self.refresh()

    def _toggle_condition(self, condition_id: str, on: bool) -> None:
        self._meds.set_condition(condition_id, on)
        self.refresh()

    def _toggle_med(self, med_id: str, on: bool) -> None:
        if on:
            self._excluded.discard(med_id)
        else:
            self._excluded.add(med_id)
        self._evaluate()

    def _remove_med(self, med_id: str) -> None:
        med = next((m for m in self._meds.current_meds() if m.id == med_id), None)
        if med is None:
            return
        dialog = ConfirmDialog(self._tab, "Remove from current medications?",
                               f"{med.name} will no longer be part of your active regimen "
                               "or the safety checks.", "Remove")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._meds.remove_current_med(med_id)
            self._on_changed()

    def _save(self) -> None:
        if self._report is None:
            return
        items = self._meds.regimen()
        self._meds.save_safety_check(
            candidate_name=self._candidate_name, candidate_id=self._candidate_id,
            verdict=self._report.verdict,
            condition_ids=sorted(self._meds.health_profile()),
            regimen_ids=[i.key for i in items if i.key not in self._excluded])
        self._tab.open_log()
        self._show_log()

    def _reload_check(self, log_id: str) -> None:
        """Put a saved check back on screen: its drug, conditions and regimen."""
        log = next((l for l in self._meds.safety_checks() if l.id == log_id), None)
        if log is None:
            return
        wanted = set(log.condition_ids)
        for condition in self._safety.conditions():
            self._meds.set_condition(condition.id, condition.id in wanted)
        self._excluded = {i.key for i in self._meds.regimen()} - set(log.regimen_ids)
        if log.candidate_id:
            self.choose(log.candidate_id)
        else:
            self.refresh()

    def _clear_log(self) -> None:
        dialog = ConfirmDialog(self._tab, "Clear safety check history?",
                               "All saved checks are removed from the log.", "Clear History")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._meds.clear_safety_checks()
            self._show_log()

    def _open_monograph(self, medicine_id: str) -> None:
        if medicine_id:
            self.monograph_requested.emit(medicine_id)
