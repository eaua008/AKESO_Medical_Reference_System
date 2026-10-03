"""Save to Notebook (from the Symptom Checker), and Edit case details.

One dialog for both: saving a new symptom case, and later editing it from
the case column. It only collects input; the controller validates and
saves through NotebookService.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.interaction_styles import tone_color
from app.models.notebook import Subject
from app.services.case_reference import (
    AGE_RANGES,
    DIFFICULTIES,
    SETTINGS,
    SEXES,
    vignette_template,
)
from app.services.notebook_service import HYPOTHETICAL_NOTE
from app.ui.views.interaction_dialogs import OverlayDialog


def _combo(options: list[tuple[str, str]], current: str) -> QComboBox:
    box = QComboBox()
    box.setObjectName("ixCombo")
    for value, label in options:
        box.addItem(label, value)
    box.setCurrentIndex(max(0, box.findData(current)))
    return box


class SymptomCaseDialog(OverlayDialog):
    def __init__(self, parent: QWidget, case: dict, subjects: list[Subject],
                 diagnoses: list[tuple[str, str]], *, title: str = "", subject_id: str = "",
                 tags: list[str] = (), editing: bool = False, linked: bool = False) -> None:
        heading = ("Edit case details" if editing else
                   f"Save to “{title}”" if linked else "Save to Notebook")
        subtitle = ("Change how this case is presented" if editing else
                    "Replaces the Symptom Checker case saved in this note" if linked else
                    "A hypothetical study case built from this Symptom Checker run")
        super().__init__(parent, heading, subtitle, width=640)
        self._case = dict(case)

        def label(text: str) -> QLabel:
            return QLabel(text, objectName="ixFieldLabel")

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(4)
        self.title = QLineEdit(title)
        self.title.setObjectName("ixInput")
        self.title.setPlaceholderText("e.g. Acute pleuritic chest pain with fever")
        grid.addWidget(label("Case title *"), 0, 0, 1, 2)
        grid.addWidget(self.title, 1, 0, 1, 2)
        self.subject = _combo([("", "No subject"), *[(s.id, s.name) for s in subjects]],
                              subject_id)
        grid.addWidget(label("Subject"), 2, 0)
        grid.addWidget(self.subject, 3, 0)
        self.tags = QLineEdit(", ".join(tags))
        self.tags.setObjectName("ixInput")
        self.tags.setPlaceholderText("Comma separated")
        grid.addWidget(label("Tags"), 2, 1)
        grid.addWidget(self.tags, 3, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        self.body.addLayout(grid)

        row = QHBoxLayout()
        row.setSpacing(8)
        self.age = _combo([(r[0], f"{r[0]} y/o") for r in AGE_RANGES], case.get("age_range", ""))
        self.sex = _combo(list(SEXES), case.get("sex", "female"))
        self.setting = _combo([(s, s) for s in SETTINGS], case.get("setting", SETTINGS[0]))
        self.difficulty = _combo([(d, d) for d in DIFFICULTIES],
                                 case.get("difficulty", DIFFICULTIES[1]))
        for caption, box in (("Age range", self.age), ("Sex", self.sex),
                             ("Setting", self.setting), ("Difficulty", self.difficulty)):
            col = QVBoxLayout()
            col.setSpacing(4)
            col.addWidget(label(caption))
            col.addWidget(box)
            row.addLayout(col, 1)
        self.body.addLayout(row)

        self.body.addWidget(label("Chief complaint"))
        self.complaint = QLineEdit(case.get("chief_complaint", ""))
        self.complaint.setObjectName("ixInput")
        self.complaint.setPlaceholderText("In the patient's words, e.g. “My chest hurts when I "
                                          "breathe in”")
        self.body.addWidget(self.complaint)

        head = QHBoxLayout()
        head.addWidget(label("Case presentation & history"))
        head.addStretch(1)
        starter = QPushButton("  Start a vignette for me")
        starter.setObjectName("ixLinkButton")
        starter.setCursor(Qt.CursorShape.PointingHandCursor)
        starter.setIcon(lucide.icon("pencil", 13, tone_color("primary")))
        starter.setToolTip("Fills in a plain template sentence from the inputs, for you to "
                           "rewrite. Not AI.")
        starter.clicked.connect(self._start_vignette)
        head.addWidget(starter)
        self.body.addLayout(head)
        self.vignette = QPlainTextEdit(case.get("vignette", ""))
        self.vignette.setObjectName("ixText")
        self.vignette.setPlaceholderText("A 45–54 y/o male presents with...")
        self.vignette.setFixedHeight(96)
        self.body.addWidget(self.vignette)

        answer = QHBoxLayout()
        answer.setSpacing(8)
        left = QVBoxLayout()
        left.setSpacing(4)
        left.addWidget(label("Teaching diagnosis (answer key)"))
        self.answer = _combo([("", "Not set"), *diagnoses], case.get("answer_key", ""))
        left.addWidget(self.answer)
        answer.addLayout(left, 1)
        right = QVBoxLayout()
        right.setSpacing(4)
        right.addWidget(label("Teaching point"))
        self.answer_note = QLineEdit(case.get("answer_note", ""))
        self.answer_note.setObjectName("ixInput")
        self.answer_note.setPlaceholderText("Key discriminating feature")
        right.addWidget(self.answer_note)
        answer.addLayout(right, 1)
        self.body.addLayout(answer)

        self.body.addWidget(label("Learning objectives (one per line)"))
        self.objectives = QPlainTextEdit("\n".join(case.get("objectives", [])))
        self.objectives.setObjectName("ixText")
        self.objectives.setFixedHeight(64)
        self.body.addWidget(self.objectives)

        self.add_summary = QCheckBox("Add a case summary to my notes")
        self.add_summary.setToolTip("Starts your notes with the presentation, symptoms, vitals "
                                    "and hallmark correlation as tables, ready to annotate. "
                                    "The answer key is left out.")
        self.add_summary.setChecked(not editing)
        self.add_summary.setVisible(not editing)
        self.body.addWidget(self.add_summary)

        note = QFrame()
        note.setObjectName("ixNoteBox")
        note_row = QHBoxLayout(note)
        note_row.setContentsMargins(10, 8, 10, 8)
        icon = QLabel()
        icon.setPixmap(lucide.pixmap("info", 14, tone_color("primary")))
        note_row.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)
        text = QLabel(HYPOTHETICAL_NOTE, objectName="ixNoteText")
        text.setWordWrap(True)
        note_row.addWidget(text, 1)
        self.body.addWidget(note)

        self.confirm = self.add_buttons("Save changes" if editing else
                                        "Save to this note" if linked else "Save to Notebook")
        self.title.setFocus()

    def _start_vignette(self) -> None:
        if self.vignette.toPlainText().strip():
            return          # never overwrite what the student wrote
        case = dict(self._case)
        case["age_range"] = self.age.currentData()
        case["sex"] = self.sex.currentData()
        self.vignette.setPlainText(vignette_template(case, self.setting.currentData()))

    def values(self) -> dict:
        return {
            "add_summary": self.add_summary.isChecked(),
            "title": self.title.text(),
            "subject_id": self.subject.currentData() or "",
            "tags": [t for t in self.tags.text().split(",") if t.strip()],
            "changes": {
                "age_range": self.age.currentData(),
                "sex": self.sex.currentData(),
                "setting": self.setting.currentData(),
                "difficulty": self.difficulty.currentData(),
                "chief_complaint": self.complaint.text().strip(),
                "vignette": self.vignette.toPlainText().strip(),
                "answer_key": self.answer.currentData() or "",
                "answer_note": self.answer_note.text().strip(),
                "objectives": [line.strip() for line in
                               self.objectives.toPlainText().splitlines() if line.strip()],
            },
        }
