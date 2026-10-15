"""Wires the Symptom Correlation Engine screen to the matching service.

The view gathers inputs; this asks the engine; the view draws the result.
Symptoms come from the Symptom Encyclopedia and conditions from the Disease
Encyclopedia, so the checker always scores against the same content the
student can go and read.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.models.notebook import SYMPTOM_CASE
from app.services.case_reference import (
    DIFFICULTIES,
    SETTINGS,
    case_to_checker_input,
    checker_input_to_case,
    symptom_summary_html,
)
from app.services.matching_service import MatchingService
from app.ui.views.notebook_dialogs import SymptomCaseDialog
from app.ui.views.symptom_checker_view import SymptomCheckerView


class SymptomCheckerController(QObject):
    # Re-emitted for the shell, which owns navigation between modules.
    disease_requested = Signal(str)
    case_saved = Signal(str)              # notebook item id
    notebook_requested = Signal(str)      # open that case in the Study Notebook

    def __init__(self, view: SymptomCheckerView, symptom_service,
                 disease_service, engine: Optional[MatchingService] = None,
                 notebook=None) -> None:
        super().__init__()
        self._view = view
        self._symptoms = symptom_service
        self._diseases = disease_service
        self._notebook = notebook             # NotebookService, for Save to Notebook
        self._saved_id = ""
        self._link_id = ""                     # a note this run is saved into
        self._engine = engine or MatchingService(
            disease_source=disease_service.all_diseases,
            symptom_source=symptom_service.all_symptoms)

        view.calculate_requested.connect(self.calculate)
        view.reset_requested.connect(self.reset)
        view.disease_requested.connect(self.disease_requested.emit)
        view.suggestion_chosen.connect(self.add_symptom)
        view.symptoms_changed.connect(self.refresh_suggestions)
        view.save_case_requested.connect(self.save_case)
        view.open_case_requested.connect(lambda: self.notebook_requested.emit(self._saved_id))
        view.unlink_requested.connect(self.unlink)
        self.load()

    @property
    def engine(self) -> MatchingService:
        return self._engine

    def load(self) -> None:
        """Refill the picker; cheap enough to call whenever the tab opens."""
        self._view.set_symptoms(self._symptoms.all_symptoms())

    def calculate(self) -> None:
        result = self._engine.evaluate(self._view.gather())
        self._view.show_result(result)
        self._view.show_suggestions(self._suggestions(result))

    def refresh_suggestions(self) -> None:
        """Co-occurring symptoms, updated as the selection changes.

        Cheap: it scores against the same cached encyclopedia the checker
        already reads, so there is no extra query.
        """
        data = self._view.gather()
        if not data.symptoms:
            self._view.show_suggestions([])
            return
        self._view.show_suggestions(self._suggestions(self._engine.evaluate(data)))

    def _suggestions(self, result) -> list[tuple[str, str, int]]:
        """Turn the engine's missing-symptom tally into (id, name, count).

        Only symptoms that exist in the encyclopedia are offered, so every
        chip can actually be added.
        """
        by_name = {s.name.lower(): s.id for s in self._symptoms.all_symptoms()}
        chosen = {s.symptom_id for s in self._view.gather().symptoms}
        out = []
        for name, _key, count in result.suggested_symptoms:
            symptom_id = by_name.get(name.lower())
            if symptom_id and symptom_id not in chosen:
                out.append((symptom_id, name, count))
        return out[:6]

    def reset(self) -> None:
        self._saved_id = ""
        self._view.clear()

    # ------------------------------------------------- Save to Notebook

    def edit_for_item(self, item_id: str) -> None:
        """Opened from a note ("Add / Edit in Symptom Checker"): load that
        note's saved run, if any, and save back into the same note."""
        item = self._notebook.get(item_id) if self._notebook else None
        if item is None:
            return
        self._link_id = item_id
        self.load()
        data = item.symptom_data
        if data.get("symptoms"):
            self._view.load_input(case_to_checker_input(data))
            self.calculate()
        else:
            self._view.clear()
        self._view.set_link(item.title)

    def unlink(self) -> None:
        self._link_id = ""
        self._view.set_link("")

    def save_case(self) -> None:
        """Save to Notebook. Unlinked: a new hypothetical case study.
        Linked to a note: the run is saved into that note (replacing the
        one it had), so it can be edited again later. The exact age is
        stored as a range; nothing identifies a real person."""
        if self._notebook is None:
            return
        data = self._view.gather()
        if not data.symptoms:
            return
        try:
            self._open_save_dialog(data)
        except Exception as error:          # never fail silently
            import traceback
            traceback.print_exc()
            from app.ui.views.account.account_dialogs import NoticeDialog
            NoticeDialog("Save to Notebook", f"The case could not be saved: {error}",
                         "triangle-alert", danger=True, parent=self._view).exec()

    def _open_save_dialog(self, data) -> None:
        result = self._view.last_result or self._engine.evaluate(data)
        linked = self._notebook.get(self._link_id) if self._link_id else None
        case = checker_input_to_case(data)
        case["setting"], case["difficulty"] = SETTINGS[0], DIFFICULTIES[1]
        if linked is not None:
            # Keep what the student wrote last time (vignette, answer key...).
            previous = linked.symptom_data
            for key in ("setting", "difficulty", "chief_complaint", "vignette",
                        "answer_key", "answer_note", "objectives"):
                if previous.get(key):
                    case[key] = previous[key]
        diagnoses = [(m.disease_id, m.name) for m in result.matches[:10]]
        seen = {d for d, _n in diagnoses}
        diagnoses += [(d.id, d.name) for d in self._diseases.all_diseases() if d.id not in seen]
        dialog = SymptomCaseDialog(
            self._view, case, self._notebook.subjects(), diagnoses,
            title=linked.title if linked else "",
            subject_id=linked.subject_id if linked else "",
            tags=linked.tags if linked else (), linked=linked is not None)

        def save() -> None:
            values = dialog.values()
            case.update(values["changes"])
            title = " ".join(values["title"].split())
            # "Add a case summary to my notes": the case written out as
            # tables, ready to annotate (never the answer key).
            summary = symptom_summary_html(title, case, result) if values["add_summary"] else ""
            if linked is not None:
                error = self._notebook.attach(linked.id, "symptom", case, summary, title=title,
                                              subject_id=values["subject_id"],
                                              tags=values["tags"])
                item_id = linked.id
            else:
                item, error = self._notebook.create_case(
                    SYMPTOM_CASE, title, values["subject_id"], values["tags"], case,
                    body=summary)
                item_id = item.id if item else ""
            if error:
                dialog.show_error(error)
                return
            self._saved_id = item_id
            dialog.accept()
        dialog.confirm.clicked.connect(save)
        if dialog.exec():
            self._view.mark_saved()
            self.case_saved.emit(self._saved_id)

    def add_symptom(self, symptom_id: str) -> None:
        """A symptom sent from its monograph, or from a suggestion chip."""
        self.load()
        self._view.add_symptom(symptom_id)
        self.refresh_suggestions()