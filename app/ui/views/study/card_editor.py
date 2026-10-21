"""Add or edit a flashcard: pick the type, fill its fields, see problems
before saving. Also used by "Make a flashcard" (text selected on a page),
where a deck picker is shown too.

"Teach it" (optional): a short answer shown big, Why, Don't confuse with
(one "Name: how it differs" per line), a hint and a difficulty. The live
preview shows the front and back as the review screen lays them out."""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QCheckBox, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QVBoxLayout, QWidget,
)

from app.models.study import CHOICES_MAX, DIFFICULTIES, Card, CardType, Choice, Deck, TYPE_LABELS
from app.services.study import cloze
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import button, field_block, label
from app.ui.views.study.review_view import preview_html

TYPES = [CardType.BASIC, CardType.MCQ, CardType.CLOZE, CardType.LABEL3D]
NEW_DECK = "__new__"


def _text_box(placeholder: str, height: int = 80) -> QPlainTextEdit:
    box = QPlainTextEdit()
    box.setObjectName("acInput")
    box.setPlaceholderText(placeholder)
    box.setFixedHeight(height)
    return box


class _ChoiceRow(QFrame):
    removed = Signal(object)

    def __init__(self, choice: Choice) -> None:
        super().__init__()
        self.setObjectName("stEditorChoice")
        column = QVBoxLayout(self)
        column.setContentsMargins(10, 8, 10, 8)
        column.setSpacing(6)
        top = QHBoxLayout()
        top.setSpacing(6)
        self.correct = QCheckBox("Correct")
        self.correct.setChecked(choice.correct)
        top.addWidget(self.correct)
        self.text = QLineEdit(choice.text)
        self.text.setObjectName("acInput")
        self.text.setPlaceholderText("Choice")
        top.addWidget(self.text, 1)
        remove = button("", "acGhost", "x", lambda: self.removed.emit(self))
        remove.setToolTip("Remove this choice")
        top.addWidget(remove)
        column.addLayout(top)
        self.rationale = QLineEdit(choice.rationale)
        self.rationale.setObjectName("acInput")
        self.rationale.setMaxLength(600)
        self.rationale.setPlaceholderText("Why it is right or wrong (shown after answering)")
        column.addWidget(self.rationale)

    def value(self) -> Choice:
        return Choice(self.text.text().strip(), self.correct.isChecked(), self.rationale.text().strip())


class CardEditorDialog(AccountDialog):
    """Returns the card through saved (the caller stores it)."""

    saved = Signal(object)                          # Card

    def __init__(self, card: Card, entries: list[tuple[str, tuple[str, str]]] = (),
                 decks: Optional[list[Deck]] = None, parent: Optional[QWidget] = None) -> None:
        editing = bool(card.id)
        super().__init__("Edit card" if editing else "New card",
                         "Short questions are easier to remember. One fact per card.",
                         "layers", parent, width=640)
        self._card = card
        self._choice_rows: list[_ChoiceRow] = []

        # deck (only for "Make a flashcard")
        self.deck_pick = None
        if decks is not None:
            self.deck_pick = QComboBox()
            self.deck_pick.setObjectName("acInput")
            for deck in decks:
                self.deck_pick.addItem(deck.title, deck.id)
            self.deck_pick.addItem("New deck…", NEW_DECK)
            index = self.deck_pick.findData(card.deck_id)
            self.deck_pick.setCurrentIndex(max(0, index))
            self.new_deck_name = QLineEdit()
            self.new_deck_name.setObjectName("acInput")
            self.new_deck_name.setPlaceholderText("Name of the new deck")
            self.new_deck_name.hide()
            self.deck_pick.currentIndexChanged.connect(
                lambda _i: self.new_deck_name.setVisible(self.deck_pick.currentData() == NEW_DECK))
            self.body.addWidget(field_block("Deck", self.deck_pick))
            self.body.addWidget(self.new_deck_name)

        # type
        types = QHBoxLayout()
        types.setSpacing(6)
        self._type_group = QButtonGroup(self)
        self._type_group.setExclusive(True)
        self._type_buttons: dict[CardType, QPushButton] = {}
        for kind in TYPES:
            chip = QPushButton(TYPE_LABELS[kind] + (" (coming soon)" if kind == CardType.LABEL3D else ""))
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.setEnabled(kind != CardType.LABEL3D)
            chip.clicked.connect(lambda _c=False, k=kind: self._set_type(k))
            self._type_group.addButton(chip)
            self._type_buttons[kind] = chip
            types.addWidget(chip)
        types.addStretch(1)
        self.body.addWidget(field_block("Card type", self._row(types)))

        # basic + mcq question
        self.front = _text_box("Front: the question", 70)
        self.front.setPlainText(card.front)
        self.front_block = field_block("Front", self.front)
        self.body.addWidget(self.front_block)
        self.back = _text_box("Back: the answer", 90)
        self.back.setPlainText(card.back)
        self.back_block = field_block("Back", self.back)
        self.body.addWidget(self.back_block)

        # mcq choices
        self.choices_host = QWidget()
        self.choices_host.setObjectName("panel")
        choices = QVBoxLayout(self.choices_host)
        choices.setContentsMargins(0, 0, 0, 0)
        choices.setSpacing(6)
        choices.addWidget(label("CHOICES (UP TO 6, TICK EVERY CORRECT ONE)", "acFieldLabel"))
        self._choices = QVBoxLayout()
        self._choices.setSpacing(6)
        choices.addLayout(self._choices)
        self.add_choice = button("Add choice", "acGhost", "plus", lambda: self._add_choice(Choice("")))
        choices.addWidget(self.add_choice, 0, Qt.AlignmentFlag.AlignLeft)
        self.body.addWidget(self.choices_host)
        for choice in card.choices or [Choice(""), Choice(""), Choice("")]:
            self._add_choice(choice)

        # cloze
        self.cloze_host = QWidget()
        self.cloze_host.setObjectName("panel")
        cloze_col = QVBoxLayout(self.cloze_host)
        cloze_col.setContentsMargins(0, 0, 0, 0)
        cloze_col.setSpacing(6)
        self.cloze_text = _text_box("Write the sentence, select a word or phrase, press Make blank.", 90)
        self.cloze_text.setPlainText(card.cloze_text)
        self.cloze_text.textChanged.connect(self._update_preview)
        cloze_col.addWidget(field_block("Sentence", self.cloze_text))
        cloze_col.addWidget(button("Make blank", "acGhost", "plus", self._make_blank), 0, Qt.AlignmentFlag.AlignLeft)
        self.preview = QLabel()
        self.preview.setObjectName("acMuted")
        self.preview.setWordWrap(True)
        self.preview.setTextFormat(Qt.TextFormat.RichText)
        cloze_col.addWidget(field_block("Preview", self.preview))
        self.body.addWidget(self.cloze_host)

        # teach it: the sections on the back, a hint, a difficulty
        self.teach_toggle = button("Teach it: short answer, why, hint (optional)", "acLink", "chevron-down",
                                   self._toggle_teach)
        self.body.addWidget(self.teach_toggle, 0, Qt.AlignmentFlag.AlignLeft)
        self.teach_host = QWidget()
        self.teach_host.setObjectName("panel")
        teach = QVBoxLayout(self.teach_host)
        teach.setContentsMargins(0, 0, 0, 0)
        teach.setSpacing(8)
        self.answer_short = QLineEdit(card.answer_short)
        self.answer_short.setObjectName("acInput")
        self.answer_short.setMaxLength(300)
        self.answer_short.setPlaceholderText("e.g. Penicillin (beta-lactam)")
        teach.addWidget(field_block("Short answer", self.answer_short, "Shown big on the back."))
        self.explanation = _text_box("Why it is so, in a sentence or two", 64)
        self.explanation.setPlainText(card.explanation)
        teach.addWidget(field_block("Why", self.explanation))
        self.distinguish = _text_box("One per line, e.g. Septic arthritis: one hot joint, does not migrate", 64)
        self.distinguish.setPlainText(card.distinguish)
        teach.addWidget(field_block("Don't confuse with", self.distinguish))
        row = QHBoxLayout()
        row.setSpacing(8)
        self.hint = QLineEdit(card.hint)
        self.hint.setObjectName("acInput")
        self.hint.setMaxLength(200)
        self.hint.setPlaceholderText("e.g. Think: post-infectious")
        row.addWidget(field_block("Hint (H)", self.hint), 2)
        self.difficulty = QComboBox()
        self.difficulty.setObjectName("acInput")
        self.difficulty.addItem("Not set", "")
        for level in DIFFICULTIES:
            self.difficulty.addItem(level.capitalize(), level)
        self.difficulty.setCurrentIndex(max(0, self.difficulty.findData(card.difficulty)))
        row.addWidget(field_block("Difficulty", self.difficulty), 1)
        teach.addLayout(row)
        self.body.addWidget(self.teach_host)
        self.teach_host.setVisible(any((card.answer_short, card.explanation, card.distinguish,
                                        card.hint, card.difficulty)))

        # live preview, as the review screen shows it
        self.card_preview = QFrame()
        self.card_preview.setObjectName("stReviewCard")
        preview_col = QVBoxLayout(self.card_preview)
        preview_col.setContentsMargins(18, 14, 18, 14)
        preview_col.setSpacing(6)
        self.preview_front = QLabel()
        self.preview_back = QLabel()
        for part, name in ((self.preview_front, "stWhy"), (self.preview_back, "stWhy")):
            part.setObjectName(name)
            part.setWordWrap(True)
            part.setTextFormat(Qt.TextFormat.RichText)
            preview_col.addWidget(part)
        self.preview_front.setStyleSheet("font-weight: 700;")
        self.body.addWidget(field_block("Preview", self.card_preview))
        for box in (self.front, self.back, self.cloze_text, self.explanation, self.distinguish):
            box.textChanged.connect(self._update_card_preview)
        for line in (self.answer_short, self.hint):
            line.textChanged.connect(self._update_card_preview)

        # tags + linked entry
        self.tags = QLineEdit(", ".join(card.tags))
        self.tags.setObjectName("acInput")
        self.tags.setPlaceholderText("e.g. finals, antibiotics")
        self.body.addWidget(field_block("Tags", self.tags, "Separate with commas."))
        self.link = QComboBox()
        self.link.setObjectName("acInput")
        self.link.setEditable(True)
        self.link.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.link.addItem("No linked entry", None)
        for text, ref in entries:
            self.link.addItem(text, ref)
        if card.source_kind and card.source_id:
            index = next((i for i in range(self.link.count())
                          if self.link.itemData(i) == (card.source_kind, card.source_id)), 0)
            self.link.setCurrentIndex(index)
        completer = self.link.completer()
        if completer is not None:
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(completer.CompletionMode.PopupCompletion)
        self.body.addWidget(field_block("Linked entry", self.link,
                                        "Optional: a disease, symptom or medicine this card is about."))

        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Save card", "acPrimary", "check", self._save, default=True)
        self._set_type(card.type if card.type != CardType.LABEL3D else CardType.BASIC)
        self._type_buttons[self._type].setChecked(True)
        self._update_preview()
        self._update_card_preview()

    @staticmethod
    def _row(layout) -> QWidget:
        host = QWidget()
        host.setObjectName("panel")
        host.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        return host

    # ----------------------------------------------------------- choices

    def _add_choice(self, choice: Choice) -> None:
        if len(self._choice_rows) >= CHOICES_MAX:
            return
        row = _ChoiceRow(choice)
        row.removed.connect(self._remove_choice)
        self._choice_rows.append(row)
        self._choices.addWidget(row)
        self.add_choice.setEnabled(len(self._choice_rows) < CHOICES_MAX)

        row.text.textChanged.connect(self._update_card_preview)
        row.correct.toggled.connect(self._update_card_preview)

    def _remove_choice(self, row: _ChoiceRow) -> None:
        if row in self._choice_rows:
            self._choice_rows.remove(row)
            row.deleteLater()
        self.add_choice.setEnabled(len(self._choice_rows) < CHOICES_MAX)
        self._update_card_preview()

    # ------------------------------------------------------------ teach it

    def _toggle_teach(self) -> None:
        self.teach_host.setVisible(not self.teach_host.isVisible())

    def _update_card_preview(self, *_args) -> None:
        if not hasattr(self, "preview_back"):
            return                                  # still building the dialog
        front, back = preview_html(self.value())
        self.preview_front.setText(front or "<i>The front shows here.</i>")
        self.preview_back.setText(back or "<i>The back shows here.</i>")

    # -------------------------------------------------------------- cloze

    def _make_blank(self) -> None:
        cursor = self.cloze_text.textCursor()
        if not cursor.hasSelection():
            self.show_error("Select the word or phrase to hide first.")
            return
        text = self.cloze_text.toPlainText()
        self.cloze_text.setPlainText(cloze.make_blank(text, cursor.selectionStart(), cursor.selectionEnd()))
        self.show_error("")

    def _update_preview(self) -> None:
        text = self.cloze_text.toPlainText()
        if not cloze.blanks(text):
            self.preview.setText("No blanks yet.")
            return
        self.preview.setText(f"<b>Question:</b> {cloze.question_html(text)}<br>"
                             f"<b>Answer:</b> {cloze.answer_html(text)}")

    # --------------------------------------------------------------- type

    def _set_type(self, kind: CardType) -> None:
        self._type = kind
        self.front_block.setVisible(kind in (CardType.BASIC, CardType.MCQ))
        self.back_block.setVisible(kind == CardType.BASIC)
        self.choices_host.setVisible(kind == CardType.MCQ)
        self.cloze_host.setVisible(kind == CardType.CLOZE)
        self.front.setPlaceholderText("The question" if kind == CardType.MCQ else "Front: the question")
        self._update_card_preview()

    # --------------------------------------------------------------- save

    def value(self) -> Card:
        card = Card(id=self._card.id, deck_id=self._card.deck_id, type=self._type,
                    position=self._card.position)
        if self._type in (CardType.BASIC, CardType.MCQ):
            card.front = self.front.toPlainText().strip()
        if self._type == CardType.BASIC:
            card.back = self.back.toPlainText().strip()
        if self._type == CardType.MCQ:
            card.choices = [row.value() for row in self._choice_rows if row.value().text]
        if self._type == CardType.CLOZE:
            card.cloze_text = self.cloze_text.toPlainText().strip()
        card.answer_short = self.answer_short.text().strip()
        card.explanation = self.explanation.toPlainText().strip()
        card.distinguish = self.distinguish.toPlainText().strip()
        card.hint = self.hint.text().strip()
        card.difficulty = self.difficulty.currentData() or ""
        if not hasattr(self, "tags"):
            return card                             # still building the dialog
        card.tags = [t.strip() for t in self.tags.text().split(",") if t.strip()][:20]
        ref = self.link.currentData()
        if isinstance(ref, tuple) and self.link.currentText() == self.link.itemText(self.link.currentIndex()):
            card.source_kind, card.source_id = ref
        return card

    def chosen_deck(self) -> tuple[Optional[str], str]:
        """(deck id, or None for a new deck; new deck name)."""
        if self.deck_pick is None:
            return self._card.deck_id, ""
        data = self.deck_pick.currentData()
        if data == NEW_DECK:
            return None, self.new_deck_name.text().strip()
        return data, ""

    def _save(self) -> None:
        card = self.value()
        problems = card.problems()
        if self.deck_pick is not None:
            deck_id, name = self.chosen_deck()
            if deck_id is None and not name:
                problems.insert(0, "Name the new deck.")
        if problems:
            self.show_error(problems[0])
            return
        self.saved.emit(card)
