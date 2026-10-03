"""Wires the Medication & Drug Safety page to MedicationService.

The view emits what the user asked for, the service applies the rules and
saves, and this class redraws the page afterwards. Dialogs are opened here
too, so the view never has to know the service exists.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QDialog

from app.controllers.safety_check_controller import SafetyCheckController
from app.services.drug_safety_service import DrugSafetyService
from app.services.medication_service import MedicationService
from app.ui.views.medication_detail_dialog import CourseDetailDialog
from app.ui.views.medication_dialogs import (
    AbandonCourseDialog,
    AddCurrentMedDialog,
    ConfirmDialog,
    LogIntakeDialog,
    TrackCourseDialog,
)
from app.ui.views.medication_view import MedicationView


class MedicationController(QObject):
    # "View Monograph" in the safety check: the shell opens Medicine Reference.
    monograph_requested = Signal(str)

    def __init__(self, view: MedicationView, service: MedicationService,
                 safety: Optional[DrugSafetyService] = None) -> None:
        super().__init__()
        self._view = view
        self._service = service
        self._safety_ctl: Optional[SafetyCheckController] = None

        view.track_requested.connect(self.open_track_dialog)
        view.add_med_requested.connect(self.open_add_med_dialog)
        tab = view.courses
        tab.filters_changed.connect(lambda *_: self.refresh())
        tab.preset_chosen.connect(self.open_track_dialog)
        tab.log_requested.connect(self.open_log_dialog)
        tab.abandon_requested.connect(self.open_abandon_dialog)
        tab.details_requested.connect(self.open_details)
        view.theme_changed.connect(self.refresh)

        self.refresh()
        # Created after the first refresh so the stat cards exist; it draws
        # the safety tab and the Drug Safety Check card itself.
        self._safety_ctl = SafetyCheckController(
            view.safety, service, safety or DrugSafetyService(), view.stat_safety,
            add_med=self.open_add_med_dialog, on_changed=self.refresh)
        self._safety_ctl.monograph_requested.connect(self.monograph_requested.emit)

    def refresh(self) -> None:
        tab = self._view.courses
        courses = self._service.filtered(*tab.filters())
        all_courses = self._service.courses()
        tab.show_courses(courses, total=len(all_courses))
        tab.show_counts(self._service.status_counts())
        tab.show_presets(self._service.presets())
        self._view.show_stats(self._service.stats(), course_count=len(all_courses))
        if self._safety_ctl is not None:
            self._safety_ctl.refresh()

    # ------------------------------------------------------------- dialogs

    def open_track_dialog(self, copy_from_id: str = "") -> None:
        dialog = TrackCourseDialog(self._view, self._service.medicine_options(),
                                   self._service.match_medicine, self._service.presets())
        if copy_from_id:
            source = next((c for c in self._service.courses() if c.id == copy_from_id), None)
            if source is not None:
                dialog.fill_from(source)

        # Validate before closing: on an error the dialog stays open with
        # the message, instead of losing everything the user typed.
        def try_save() -> None:
            error = self._service.add_course(**dialog.values())
            if error:
                dialog.show_error(error)
            else:
                QDialog.accept(dialog)

        dialog.confirm.clicked.disconnect()
        dialog.confirm.clicked.connect(try_save)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh()

    def open_add_med_dialog(self) -> None:
        dialog = AddCurrentMedDialog(self._view, self._service.medicine_options(),
                                     self._service.match_medicine)

        def try_save() -> None:
            error = self._service.add_current_med(**dialog.values())
            if error:
                dialog.show_error(error)
            else:
                QDialog.accept(dialog)

        dialog.confirm.clicked.disconnect()
        dialog.confirm.clicked.connect(try_save)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh()

    def open_abandon_dialog(self, course_id: str) -> None:
        course = next((c for c in self._service.courses() if c.id == course_id), None)
        if course is None:
            return
        dialog = AbandonCourseDialog(self._view, course)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._service.abandon(course_id, dialog.reason_text())
            self.refresh()

    def open_log_dialog(self, course_id: str, parent=None) -> bool:
        """Returns True when an entry was saved."""
        course = self._service.get(course_id)
        if course is None:
            return False
        dialog = LogIntakeDialog(parent or self._view, course)

        def try_save() -> None:
            error = self._service.log_intake(course_id, **dialog.values())
            if error:
                dialog.show_error(error)
            else:
                QDialog.accept(dialog)

        dialog.confirm.clicked.disconnect()
        dialog.confirm.clicked.connect(try_save)
        saved = dialog.exec() == QDialog.DialogCode.Accepted
        if saved:
            self.refresh()
        return saved

    def open_edit_dialog(self, course_id: str, parent=None) -> bool:
        course = self._service.get(course_id)
        if course is None:
            return False
        dialog = TrackCourseDialog(parent or self._view, self._service.medicine_options(),
                                   self._service.match_medicine, [], editing=True)
        dialog.fill_from(course, include_notes=True)

        def try_save() -> None:
            error = self._service.update_course(course_id, **dialog.values())
            if error:
                dialog.show_error(error)
            else:
                QDialog.accept(dialog)

        dialog.confirm.clicked.disconnect()
        dialog.confirm.clicked.connect(try_save)
        saved = dialog.exec() == QDialog.DialogCode.Accepted
        if saved:
            self.refresh()
        return saved

    def open_details(self, course_id: str) -> None:
        course = self._service.get(course_id)
        if course is None:
            return
        panel = CourseDetailDialog(self._view, course)

        # Each action opens its own pop-up over the panel, then the panel
        # redraws with the saved result and stays on the same tab.
        def reload() -> None:
            updated = self._service.get(course_id)
            if updated is not None:
                panel.load(updated)

        def on_log(cid: str) -> None:
            if self.open_log_dialog(cid, parent=panel):
                reload()

        def on_edit(cid: str) -> None:
            if self.open_edit_dialog(cid, parent=panel):
                reload()

        def on_delete(cid: str, log_id: int) -> None:
            confirm = ConfirmDialog(panel, "Delete this entry?",
                                    "It is removed from the intake history and the "
                                    "countdown is recalculated.", "Delete Entry")
            if confirm.exec() == QDialog.DialogCode.Accepted:
                self._service.delete_intake(cid, log_id)
                self.refresh()
                reload()

        panel.log_requested.connect(on_log)
        panel.edit_requested.connect(on_edit)
        panel.delete_log_requested.connect(on_delete)
        panel.exec()

    def reload_medicines(self) -> None:
        """Called after the medicine sync, so suggestions include new entries."""
        self.refresh()
