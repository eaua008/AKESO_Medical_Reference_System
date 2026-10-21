"""Study Hub dialogs: settings, reporting a card, naming a deck."""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QCheckBox, QComboBox, QGridLayout, QHBoxLayout, QLineEdit, QPushButton, QSpinBox, QWidget,
)

from app.models.study import DIFFICULTIES, Deck, StudySettings
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import field_block
from app.ui.views.study.widgets import SUBJECT_NAMES, family_groups

REASONS = [("wrong", "Wrong"), ("unclear", "Unclear"), ("outdated", "Outdated"), ("typo", "Typo"),
           ("other", "Other")]


def _steps(text: str) -> Optional[list[int]]:
    try:
        values = [int(x) for x in text.replace(",", " ").split()]
    except ValueError:
        return None
    if not values or any(v < 1 or v > 1440 for v in values) or len(values) > 6:
        return None
    return values


class StudySettingsDialog(AccountDialog):
    saved = Signal(object)                 # StudySettings
    reset_requested = Signal(str)          # deck id

    def __init__(self, settings: StudySettings, started_decks: list[Deck],
                 parent: Optional[QWidget] = None) -> None:
        super().__init__("Study settings", "How many cards a day, and how soon new cards come back.",
                         "settings", parent, width=520)
        self.new = QSpinBox()
        self.new.setObjectName("acInput")
        self.new.setRange(0, 500)
        self.new.setValue(settings.new_per_day)
        self.body.addWidget(field_block("New cards a day", self.new, "Default 20."))
        self.reviews = QSpinBox()
        self.reviews.setObjectName("acInput")
        self.reviews.setRange(0, 5000)
        self.reviews.setValue(settings.max_reviews)
        self.body.addWidget(field_block("Most reviews a day", self.reviews, "Default 200."))
        self.learning = QLineEdit(" ".join(str(s) for s in settings.learning_steps))
        self.learning.setObjectName("acInput")
        self.body.addWidget(field_block("Learning steps (minutes)", self.learning,
                                        "When a new card comes back today. Default: 1 10."))
        self.relearn = QLineEdit(" ".join(str(s) for s in settings.relearn_steps))
        self.relearn.setObjectName("acInput")
        self.body.addWidget(field_block("Relearning steps (minutes)", self.relearn,
                                        "After you forget a card. Default: 10."))
        self.type_answer = QCheckBox("Type my answer before I flip the card")
        self.type_answer.setChecked(settings.type_answer)
        self.body.addWidget(field_block("Answering", self.type_answer,
                                        "The words you typed that match the answer are highlighted."))
        self._difficulty_chips = self._chips([(d.capitalize(), [d]) for d in DIFFICULTIES],
                                             settings.difficulties, "Difficulty",
                                             "Nothing picked = every difficulty.")
        self._family_chips = self._chips(family_groups(), settings.families, "Card kinds",
                                         "Nothing picked = every kind. Your own cards have no kind, "
                                         "so a kind filter skips them.", columns=3)
        if started_decks:
            row = QHBoxLayout()
            row.setSpacing(8)
            self.reset_pick = QComboBox()
            self.reset_pick.setObjectName("acInput")
            for deck in started_decks:
                self.reset_pick.addItem(deck.title, deck.id)
            row.addWidget(self.reset_pick, 1)
            reset = QPushButton("Reset progress")
            reset.setObjectName("acDanger")
            reset.setCursor(Qt.CursorShape.PointingHandCursor)
            reset.clicked.connect(lambda: self.reset_requested.emit(self.reset_pick.currentData()))
            row.addWidget(reset)
            holder = QWidget()
            holder.setObjectName("panel")
            holder.setLayout(row)
            row.setContentsMargins(0, 0, 0, 0)
            self.body.addWidget(field_block("Reset a deck", holder,
                                            "Every card in it becomes new again. Your history stays."))
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Save", "acPrimary", "check", self._save, default=True)

    def _chips(self, options: list[tuple[str, list[str]]], picked: list[str], title: str, note: str,
               columns: int = 4) -> list[tuple[QPushButton, list[str]]]:
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(6)
        grid.setVerticalSpacing(6)
        chips = []
        for i, (text, values) in enumerate(options):
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.setChecked(any(v in picked for v in values))
            grid.addWidget(chip, i // columns, i % columns)
            chips.append((chip, values))
        holder = QWidget()
        holder.setObjectName("panel")
        holder.setLayout(grid)
        self.body.addWidget(field_block(title, holder, note))
        return chips

    @staticmethod
    def _picked(chips) -> list[str]:
        return [v for chip, values in chips if chip.isChecked() for v in values]

    def _save(self) -> None:
        learning, relearn = _steps(self.learning.text()), _steps(self.relearn.text())
        if learning is None or relearn is None:
            self.show_error("Write the steps as minutes between 1 and 1440, e.g. 1 10.")
            return
        self.saved.emit(StudySettings(new_per_day=self.new.value(), max_reviews=self.reviews.value(),
                                      learning_steps=learning, relearn_steps=relearn,
                                      type_answer=self.type_answer.isChecked(),
                                      difficulties=self._picked(self._difficulty_chips),
                                      families=self._picked(self._family_chips)))


class ReportCardDialog(AccountDialog):
    submitted = Signal(str, str)           # reason, note

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__("Report this card", "Tell the Akeso team what's wrong. Thank you!",
                         "flag", parent, width=480)
        row = QHBoxLayout()
        row.setSpacing(6)
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._reason = ""
        for key, text in REASONS:
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.clicked.connect(lambda _c=False, k=key: setattr(self, "_reason", k))
            self._group.addButton(chip)
            row.addWidget(chip)
        row.addStretch(1)
        holder = QWidget()
        holder.setObjectName("panel")
        holder.setLayout(row)
        row.setContentsMargins(0, 0, 0, 0)
        self.body.addWidget(field_block("What's wrong?", holder))
        self.note = QLineEdit()
        self.note.setObjectName("acInput")
        self.note.setMaxLength(500)
        self.note.setPlaceholderText("Optional: what should it say?")
        self.body.addWidget(field_block("Note", self.note))
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Send report", "acPrimary", "flag", self._send, default=True)

    def _send(self) -> None:
        if not self._reason:
            self.show_error("Choose what's wrong with the card.")
            return
        self.set_busy(True)
        self.submitted.emit(self._reason, self.note.text().strip())


class NewDeckDialog(AccountDialog):
    submitted = Signal(str, str, str)       # title, subject id, description

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__("New deck", "Your decks are private: only you see them.", "layers", parent, width=480)
        self.title_edit = QLineEdit()
        self.title_edit.setObjectName("acInput")
        self.title_edit.setMaxLength(120)
        self.title_edit.setPlaceholderText("e.g. Pharmacology finals")
        self.body.addWidget(field_block("Title", self.title_edit))
        self.subject = QComboBox()
        self.subject.setObjectName("acInput")
        self.subject.addItem("No subject", "")
        for key, name in SUBJECT_NAMES.items():
            self.subject.addItem(name, key)
        self.body.addWidget(field_block("Subject", self.subject))
        self.description = QLineEdit()
        self.description.setObjectName("acInput")
        self.description.setMaxLength(1000)
        self.body.addWidget(field_block("Description (optional)", self.description))
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Create deck", "acPrimary", "plus", self._create, default=True)
        self.title_edit.returnPressed.connect(self._create)

    def _create(self) -> None:
        title = self.title_edit.text().strip()
        if not title:
            self.show_error("Give the deck a title.")
            return
        self.submitted.emit(title, self.subject.currentData() or "", self.description.text().strip())

