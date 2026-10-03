"""The three pop-ups of My Medication Courses.

    TrackCourseDialog     Track New Prescribed Course
    AddCurrentMedDialog   Add to Current Medications
    AbandonCourseDialog   confirm stopping a course early, with a reason

All three sit on OverlayDialog: a frameless window laid over the whole app
that dims everything behind it and centres a card, as in the design.

The dialogs only collect input. They never save anything themselves: the
controller reads the values and hands them to MedicationService.
"""

from typing import Optional

from PySide6.QtCore import QRect, Qt, QStringListModel, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QCompleter,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.medication_styles import tone_color
from app.models.medication import (
    FREQUENCIES,
    INTAKE_DELAYED,
    INTAKE_MISSED,
    INTAKE_STATUSES,
    INTAKE_TAKEN,
    UNIT_FORMS,
    MedicationCourse,
)
from app.services.medication_service import MedicineOption, Preset


class OverlayDialog(QDialog):
    """A modal card over a dimmed copy of the app window."""

    def __init__(self, parent: QWidget, title: str, subtitle: str,
                 width: int = 400) -> None:
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)

        # Cover the whole top-level window, so the dim reaches every edge.
        window = parent.window()
        top_left = window.mapToGlobal(window.rect().topLeft())
        self.setGeometry(QRect(top_left, window.size()))

        outer = QVBoxLayout(self)

        self.card = QFrame()
        self.card.setObjectName("mdDialogCard")
        self.card.setFixedWidth(width)
        # Aligned, so the card keeps its natural height instead of being
        # stretched to the window's height (which spread the fields apart).
        outer.addWidget(self.card, 0, Qt.AlignmentFlag.AlignCenter)

        self.body = QVBoxLayout(self.card)
        self.body.setContentsMargins(18, 16, 18, 16)
        self.body.setSpacing(10)

        head = QHBoxLayout()
        titles = QVBoxLayout()
        titles.setSpacing(1)
        titles.addWidget(QLabel(title, objectName="mdDialogTitle"))
        sub = QLabel(subtitle, objectName="mdSmallMuted")
        sub.setWordWrap(True)
        titles.addWidget(sub)
        head.addLayout(titles, 1)
        close = QPushButton()
        close.setObjectName("mdClose")
        close.setIcon(lucide.icon("x", 16, tone_color("muted")))
        close.setCursor(Qt.CursorShape.PointingHandCursor)
        close.clicked.connect(self.reject)
        head.addWidget(close, 0, Qt.AlignmentFlag.AlignTop)
        self.body.addLayout(head)
        self.body.addWidget(_divider())

        self.error = QLabel("", objectName="mdError")
        self.error.setWordWrap(True)
        self.error.hide()

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt name)
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 170))
        painter.end()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        # A click on the dimmed area outside the card closes the dialog.
        if not self.card.geometry().contains(event.position().toPoint()):
            self.reject()
        else:
            super().mousePressEvent(event)

    def add_buttons(self, confirm_text: str) -> QPushButton:
        self.body.addWidget(self.error)
        self.body.addWidget(_divider())
        row = QHBoxLayout()
        row.addStretch(1)
        cancel = QPushButton("Cancel")
        cancel.setObjectName("mdSecondary")
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.reject)
        confirm = QPushButton(confirm_text)
        confirm.setObjectName("mdPrimary")
        confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm.setDefault(True)
        row.addWidget(cancel)
        row.addWidget(confirm)
        self.body.addLayout(row)
        return confirm

    def show_error(self, message: str) -> None:
        self.error.setText(message)
        self.error.setVisible(bool(message))


class MedicineField(QWidget):
    """A text box with a suggestions list drawn from the medicine database.

    Typing filters the list by any part of the name, generic name or brand.
    Choosing a suggestion fills in the medicine's name. Free text is still
    allowed (not every medicine is in the database yet); the line under the
    box says whether what was typed is linked to a database entry.
    """

    changed = Signal()

    def __init__(self, placeholder: str, options: list[MedicineOption],
                 matcher, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._by_label = {o.label: o for o in options}
        self._matcher = matcher          # MedicationService.match_medicine

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        self.edit = QLineEdit()
        self.edit.setObjectName("mdInput")
        self.edit.setPlaceholderText(placeholder)
        layout.addWidget(self.edit)

        # The model is parented to this widget: without a parent, Python
        # would garbage-collect it and the suggestions list would be empty.
        self._model = QStringListModel([o.label for o in options], self)
        completer = QCompleter(self._model, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setMaxVisibleItems(7)
        completer.popup().setObjectName("mdSuggest")
        # activated gives the chosen label; swap it for the plain name.
        completer.activated[str].connect(self._on_chosen)
        self.edit.setCompleter(completer)

        self.status = QLabel("", objectName="mdUnlinked")
        layout.addWidget(self.status)
        self.edit.textChanged.connect(self._refresh_status)
        self._refresh_status()

    def _on_chosen(self, label: str) -> None:
        option = self._by_label.get(label)
        if option is not None:
            # After the completer has written the label, replace it.
            self.edit.setText(option.name)

    def _refresh_status(self) -> None:
        text = self.edit.text().strip()
        if not text:
            self.status.setText(f"{len(self._by_label)} medicines in the database. "
                                "Start typing for suggestions.")
            self.status.setObjectName("mdUnlinked")
        elif self._matcher(text):
            self.status.setText("Linked to the medicine database")
            self.status.setObjectName("mdLinked")
        else:
            self.status.setText("Not in the database. It will be saved as typed.")
            self.status.setObjectName("mdUnlinked")
        # Object name changed: re-apply the stylesheet to this label.
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        self.changed.emit()

    def text(self) -> str:
        return self.edit.text()

    def set_text(self, text: str) -> None:
        self.edit.setText(text)


class TrackCourseDialog(OverlayDialog):
    """Also the edit form: pass editing=True and fill_from() the course."""

    def __init__(self, parent: QWidget, options: list[MedicineOption], matcher,
                 presets: list[Preset], editing: bool = False) -> None:
        super().__init__(parent,
                         "Edit Course Details" if editing else "Track New Prescribed Course",
                         "Progress and intake history are kept as they are" if editing
                         else "Fixed duration therapy tracking with countdown & adherence "
                              "calculation", width=380)
        if editing:
            presets = []

        if presets:
            self.body.addWidget(QLabel("QUICK REGIMEN PRESETS:", objectName="mdPanelHeading"))
            chips = QHBoxLayout()
            chips.setSpacing(6)
            for preset in presets:
                name = preset.course.medicine_name
                chip = QPushButton(name if len(name) <= 16 else name[:15].rstrip() + "\u2026")
                chip.setToolTip(preset.title)
                chip.setObjectName("mdPresetChip")
                chip.setCursor(Qt.CursorShape.PointingHandCursor)
                chip.clicked.connect(lambda _c=False, c=preset.course: self.fill_from(c))
                chips.addWidget(chip)
            chips.addStretch(1)
            self.body.addLayout(chips)

        self.body.addWidget(_label("Medicine & Strength"))
        self.medicine = MedicineField("e.g. Co-Amoxiclav 625mg, Ciprofloxacin 500mg",
                                      options, matcher)
        self.body.addWidget(self.medicine)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(4)
        self.units = _spin(1, 1000, 14)
        self.form = QComboBox()
        self.form.setObjectName("mdCombo")
        self.form.addItems(UNIT_FORMS)
        self.schedule = _line("e.g. 1 tablet twice daily with food")
        self.duration = _spin(1, 365, 7)
        grid.addWidget(_label("Prescribed Units (Total Count)"), 0, 0)
        grid.addWidget(_label("Unit Form"), 0, 1)
        grid.addWidget(self.units, 1, 0)
        grid.addWidget(self.form, 1, 1)
        grid.addWidget(_label("Dosage Schedule"), 2, 0)
        grid.addWidget(_label("Duration (Days)"), 2, 1)
        grid.addWidget(self.schedule, 3, 0)
        grid.addWidget(self.duration, 3, 1)
        self.body.addLayout(grid)

        self.body.addWidget(_label("Prescribing Clinician / Clinic"))
        self.prescriber = _line("e.g. Dr. Santos, Outpatient Infectious Disease")
        self.body.addWidget(self.prescriber)

        protect_box = QFrame()
        protect_box.setObjectName("mdCheckRow")
        protect_row = QHBoxLayout(protect_box)
        protect_row.setContentsMargins(10, 8, 10, 8)
        self.protected = QCheckBox()
        protect_row.addWidget(self.protected, 0, Qt.AlignmentFlag.AlignTop)
        protect_text = QVBoxLayout()
        protect_text.setSpacing(1)
        protect_title = QLabel("Antibiotic or Tapered Steroid (Stewardship Warning "
                               "Protected)", objectName="mdMetaKey")
        protect_title.setWordWrap(True)
        protect_text.addWidget(protect_title)
        hint = QLabel("Enforces resistance prevention warnings if doses are skipped or "
                      "course abandoned.", objectName="mdSmallMuted")
        hint.setWordWrap(True)
        protect_text.addWidget(hint)
        protect_row.addLayout(protect_text, 1)
        self.body.addWidget(protect_box)

        self.body.addWidget(_label("Clinical Notes"))
        self.notes = QPlainTextEdit()
        self.notes.setObjectName("mdText")
        self.notes.setPlaceholderText("Special instructions, dietary restrictions...")
        self.notes.setFixedHeight(56)
        self.body.addWidget(self.notes)

        self.confirm = self.add_buttons("Save Changes" if editing else "Save && Start Course")
        self.confirm.clicked.connect(self.accept)
        self.medicine.edit.setFocus()

    def fill_from(self, course: MedicationCourse, include_notes: bool = False) -> None:
        """A preset copies a past course's regimen, not its progress."""
        self.medicine.set_text(course.medicine_name)
        self.units.setValue(course.total_units)
        self.form.setCurrentText(course.unit_form)
        self.schedule.setText(course.dosage_schedule)
        self.duration.setValue(course.duration_days)
        self.prescriber.setText(course.prescriber)
        self.protected.setChecked(course.is_protected)
        if include_notes:
            self.notes.setPlainText(course.notes)

    def values(self) -> dict:
        return {
            "medicine_name": self.medicine.text(),
            "total_units": self.units.value(),
            "unit_form": self.form.currentText(),
            "dosage_schedule": self.schedule.text(),
            "duration_days": self.duration.value(),
            "prescriber": self.prescriber.text(),
            "is_protected": self.protected.isChecked(),
            "notes": self.notes.toPlainText(),
        }


class AddCurrentMedDialog(OverlayDialog):
    def __init__(self, parent: QWidget, options: list[MedicineOption], matcher) -> None:
        super().__init__(parent, "Add to Current Medications",
                         "Maintains continuous pairwise interaction surveillance",
                         width=380)
        self._options = {o.name.lower(): o for o in options}

        self.body.addWidget(_label("Medicine Name"))
        self.medicine = MedicineField("e.g. Warfarin, Omeprazole, Metformin, Ibuprofen",
                                      options, matcher)
        self.body.addWidget(self.medicine)

        self.body.addWidget(_label("Dosage / Strength"))
        self.dosage = _line("e.g. 5mg oral tablet, 20mg capsule")
        self.body.addWidget(self.dosage)

        self.body.addWidget(_label("Frequency"))
        self.frequency = QComboBox()
        self.frequency.setObjectName("mdCombo")
        self.frequency.addItems(FREQUENCIES)
        self.body.addWidget(self.frequency)

        otc_row = QHBoxLayout()
        otc_row.setSpacing(8)
        self.otc = QCheckBox()
        otc_row.addWidget(self.otc, 0, Qt.AlignmentFlag.AlignTop)
        otc_text = QLabel("Over-the-counter (OTC) supplement or self-administered "
                          "medication", objectName="mdBoxBody")
        otc_text.setWordWrap(True)
        otc_row.addWidget(otc_text, 1)
        self.body.addLayout(otc_row)
        # Pre-tick OTC when the database says so; the patient can still change it.
        self.medicine.changed.connect(self._suggest_otc)

        self.body.addWidget(_label("Notes / Indication"))
        self.notes = _line("e.g. For acid reflux, for blood pressure...")
        self.body.addWidget(self.notes)

        self.confirm = self.add_buttons("Add to Active List")
        self.confirm.clicked.connect(self.accept)
        self.medicine.edit.setFocus()

    def _suggest_otc(self) -> None:
        option = self._options.get(self.medicine.text().strip().lower())
        if option is not None:
            self.otc.setChecked(option.is_otc)

    def values(self) -> dict:
        return {
            "name": self.medicine.text(),
            "dosage": self.dosage.text(),
            "frequency": self.frequency.currentText(),
            "is_otc": self.otc.isChecked(),
            "notes": self.notes.text(),
        }


class AbandonCourseDialog(OverlayDialog):
    def __init__(self, parent: QWidget, course: MedicationCourse) -> None:
        super().__init__(parent, "Stop This Course Early?",
                         f"{course.medicine_name} · {course.remaining} "
                         f"{course.unit_label} remaining", width=380)
        if course.is_protected:
            box = QFrame()
            box.setObjectName("mdWarnBox")
            inner = QVBoxLayout(box)
            inner.setContentsMargins(10, 8, 10, 8)
            inner.addWidget(_titled("triangle-alert", "Full-course critical medicine"))
            body = QLabel("Stopping an antibiotic or tapered steroid early can cause "
                          "resistance or rebound. Talk to your prescriber first.",
                          objectName="mdBoxBody")
            body.setWordWrap(True)
            inner.addWidget(body)
            self.body.addWidget(box)

        self.body.addWidget(_label("Reason for stopping"))
        self.reason = _line("e.g. Side effects, prescriber advised, felt better")
        self.body.addWidget(self.reason)

        self.confirm = self.add_buttons("Abandon Course")
        self.confirm.clicked.connect(self.accept)

    def reason_text(self) -> str:
        return self.reason.text()


class LogIntakeDialog(OverlayDialog):
    """Taken now / delayed / missed, how many units, and an optional note.

    The hint under the units box says exactly what will happen to the
    countdown, and a protected course (antibiotic or tapered steroid) shows
    the stewardship warning as soon as "Missed / Skipped" is chosen.
    """

    def __init__(self, parent: QWidget, course: MedicationCourse) -> None:
        super().__init__(parent, "Log Medication Intake", course.medicine_name, width=400)
        self._course = course
        self._status = INTAKE_TAKEN

        self.body.addWidget(_label("Intake Status"))
        row = QHBoxLayout()
        row.setSpacing(8)
        group = QButtonGroup(self)
        group.setExclusive(True)
        for key, text in INTAKE_STATUSES:
            button = QPushButton(text)
            button.setObjectName("mdSegment")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setChecked(key == INTAKE_TAKEN)
            button.clicked.connect(lambda _c=False, k=key: self._set_status(k))
            group.addButton(button)
            row.addWidget(button, 1)
        self.body.addLayout(row)

        self.body.addWidget(_label(f"Units Consumed ({course.unit_label})"))
        self.units = _spin(1, max(course.total_units, 1), 1)
        self.units.valueChanged.connect(self._refresh)
        self.body.addWidget(self.units)
        self.hint = QLabel("", objectName="mdSmallMuted")
        self.hint.setWordWrap(True)
        self.body.addWidget(self.hint)

        self.warning = QFrame()
        self.warning.setObjectName("mdWarnBox")
        warn = QVBoxLayout(self.warning)
        warn.setContentsMargins(10, 8, 10, 8)
        warn.setSpacing(3)
        title_row = QHBoxLayout()
        title_row.setSpacing(6)
        self.warning_icon = QLabel()
        title_row.addWidget(self.warning_icon, 0, Qt.AlignmentFlag.AlignTop)
        self.warning_title = QLabel("", objectName="mdWarnTitle")
        self.warning_title.setWordWrap(True)
        title_row.addWidget(self.warning_title, 1)
        self.warning_body = QLabel("", objectName="mdBoxBody")
        self.warning_body.setWordWrap(True)
        warn.addLayout(title_row)
        warn.addWidget(self.warning_body)
        self.body.addWidget(self.warning)

        self.body.addWidget(_label("Optional Intake Notes"))
        self.note = _line("e.g. Taken with light breakfast, mild stomach ache...")
        self.body.addWidget(self.note)

        self.confirm = self.add_buttons("Confirm Intake")
        self.confirm.clicked.connect(self.accept)
        self._refresh()

    def _set_status(self, key: str) -> None:
        self._status = key
        self._refresh()

    def _refresh(self) -> None:
        c = self._course
        units = self.units.value()
        if self._status == INTAKE_MISSED:
            self.hint.setText("Recorded as missed. The remaining countdown stays at "
                              f"{c.remaining}.")
        else:
            after = max(c.remaining - units, 0)
            self.hint.setText(f"Will decrement remaining countdown from {c.remaining} "
                              f"to {after}.")

        # The warning explains the risk; it never blocks the entry.
        if self._status == INTAKE_MISSED and c.is_protected:
            self._show_warning(
                "Do Not Stop Early \u2014 Antimicrobial Stewardship",
                f"Skipping doses of a full-course medicine raises the risk of resistance "
                f"or rebound. Take the next dose as scheduled and finish all "
                f"{c.total_units} {c.unit_label}.")
        elif self._status == INTAKE_MISSED:
            self._show_warning("Missed dose",
                               "Don't double the next dose to make up for it unless your "
                               "prescriber or pharmacist says so.")
        elif self._status == INTAKE_DELAYED:
            self._show_warning("Late intake",
                               "Keep the usual gap before the next dose where possible.")
        elif self._status != INTAKE_MISSED and units > c.remaining:
            self._show_warning("More than remains",
                               f"Only {c.remaining} {c.unit_label} are left in this course.")
        else:
            self.warning.hide()

    def _show_warning(self, title: str, body: str) -> None:
        name = "clock" if title == "Late intake" else "triangle-alert"
        self.warning_icon.setPixmap(lucide.pixmap(name, 14, tone_color("amber")))
        self.warning_title.setText(title)
        self.warning_body.setText(body)
        self.warning.show()

    def values(self) -> dict:
        return {"status": self._status, "units": self.units.value(),
                "note": self.note.text()}


class ConfirmDialog(OverlayDialog):
    """A small yes/no, for actions like deleting a log entry."""

    def __init__(self, parent: QWidget, title: str, message: str, confirm_text: str) -> None:
        super().__init__(parent, title, "", width=360)
        text = QLabel(message, objectName="mdBoxBody")
        text.setWordWrap(True)
        self.body.addWidget(text)
        self.confirm = self.add_buttons(confirm_text)
        self.confirm.clicked.connect(self.accept)


# --------------------------------------------------------------- helpers

def _titled(icon_name: str, text: str) -> QWidget:
    """A warning title with its icon, for the amber boxes."""
    row_widget = QWidget()
    row_widget.setObjectName("panel")
    row = QHBoxLayout(row_widget)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(6)
    mark = QLabel()
    mark.setPixmap(lucide.pixmap(icon_name, 14, tone_color("amber")))
    row.addWidget(mark)
    row.addWidget(QLabel(text, objectName="mdWarnTitle"), 1)
    return row_widget


def _label(text: str) -> QLabel:
    return QLabel(text, objectName="mdFieldLabel")


def _line(placeholder: str) -> QLineEdit:
    edit = QLineEdit()
    edit.setObjectName("mdInput")
    edit.setPlaceholderText(placeholder)
    return edit


def _spin(low: int, high: int, value: int) -> QSpinBox:
    spin = QSpinBox()
    spin.setObjectName("mdSpin")
    spin.setRange(low, high)
    spin.setValue(value)
    spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
    return spin


def _divider() -> QFrame:
    line = QFrame()
    line.setObjectName("mdDivider")
    line.setFixedHeight(1)
    return line
