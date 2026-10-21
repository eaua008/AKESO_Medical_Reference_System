"""The review screen (inside a PageSheet): one card at a time.

    Space / Enter or click     show the answer
    H                          show the hint under the question
    1 2 3 4                    Again, Hard, Good, Easy (each shows when the
                               card comes back: "1 min", "1 d", "4 d")
    Ctrl+Z                     undo the last rating
    E                          edit (your own cards)
    R                          report (official and auto cards)
    Esc                        end the session

The card is as tall as its content (at least 260 px, then it scrolls inside).
The front sits in the middle, at most ~760 px wide. The back is in sections:
Answer (large), Why, Don't confuse with, then a footer with the source,
"Open {entry}" and Report. Badges in the top corner: subject, body system,
difficulty and Updated.

Multiple choice: click a choice; right and wrong are coloured, every choice's
explanation appears, and Good (right) or Again (wrong) is preselected for you
to confirm or change. Fill-in-the-blank: "[ ... ]" on the front, the full
sentence with the blanks in bold on the back. Type your answer (Study
settings): a box before flipping; the typed words that match the answer are
highlighted and Good or Again is preselected the same way.
"""

import html
import re
from typing import Optional

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QPoint, QSize, Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget,
)

from app.models.study import Card, CardType, DISCLAIMER, Rating
from app.services.study import answer_match, cloze
from app.ui.views.account.account_widgets import button, label, repolish
from app.ui.views.study.motion import ProgressRing, count_up, fade_in, stagger
from app.ui.views.study.widgets import SUBJECT_NAMES, clear_layout

RATING_TEXT = {Rating.AGAIN: "Again", Rating.HARD: "Hard", Rating.GOOD: "Good", Rating.EASY: "Easy"}
ENTRY_WORD = {"disease": "condition", "symptom": "symptom", "medicine": "medicine",
              "article": "article", "body_part": "body part"}
SOURCE_FIELD = {"differential_diagnosis": "differential diagnosis", "emergency_warning_signs": "warning signs",
                "symptoms": "symptoms", "pathophysiology": "how it develops", "medicines": "treatment",
                "doses": "dosing", "drug_class": "drug class", "adverse": "side effects",
                "contraindication": "contraindications", "interaction": "interactions", "causes": "causes",
                "dose_notes": "kidney / liver dosing"}
CARD_MIN = 260
TEXT_WIDTH = 760
_NUMBER = re.compile(r"(\d+(?:[.,]\d+)*(?:\s?(?:mg|mcg|g|kg|mL|ml|L|%))?)")


def _rich(text: str) -> str:
    return html.escape(text or "").replace("\n", "<br>")


def _mono_numbers(text: str) -> str:
    return _NUMBER.sub(r"<span style='font-family: Consolas, \"Cascadia Mono\", monospace;'>\1</span>",
                       html.escape(text or ""))


def answer_text(card: Card) -> str:
    """The words a typed answer is compared with."""
    if card.type == CardType.CLOZE:
        return " ".join(b.answer for b in cloze.blanks(card.cloze_text))
    return card.answer_short or card.back


def _marked(text: str, other: str) -> str:
    out = []
    for word, hit in answer_match.marks(text, other):
        w = html.escape(word)
        out.append(f"<b><u>{w}</u></b>" if hit else w)
    return " ".join(out) or "<i>(nothing typed)</i>"


def preview_html(card: Card) -> tuple[str, str]:
    """(front, back) of a card as the review screen lays them out, for the
    card editor's live preview."""
    def head(title: str) -> str:
        return f"<p style='margin:10px 0 2px 0; font-size:10px; font-weight:700; letter-spacing:1px;'>{title}</p>"
    if card.type == CardType.CLOZE:
        front = cloze.question_html(card.cloze_text) if cloze.blanks(card.cloze_text) else ""
        answer = cloze.answer_html(card.cloze_text) if front else ""
    else:
        front = _rich(card.front)
        right = ", ".join(c.text for c in card.choices if c.correct and c.text)
        answer = _rich(card.answer_short or (right if card.type == CardType.MCQ else card.back))
    if card.type == CardType.MCQ:
        front += "".join(f"<br>{chr(65 + i)}.&nbsp; {html.escape(c.text)}"
                         for i, c in enumerate(card.choices) if c.text)
    if card.hint.strip():
        front += f"<br><i>Hint: {html.escape(card.hint)}</i>"
    back = ""
    if answer:
        back += head("ANSWER") + f"<p style='margin:0; font-size:16px; font-weight:700;'>{answer}</p>"
    extra = card.back.strip()
    if card.type == CardType.BASIC and card.answer_short.strip() and extra and extra != card.answer_short.strip():
        back += f"<p style='margin:4px 0 0 0;'>{_rich(extra)}</p>"
    why = " ".join(line.strip() for line in card.explanation.split("\n") if line.strip())
    if why:
        back += head("WHY") + f"<p style='margin:0;'>{html.escape(why)}</p>"
    confuse = [line.strip() for line in card.distinguish.split("\n") if line.strip()]
    if confuse:
        back += head("DON'T CONFUSE WITH") + "".join(
            f"<p style='margin:0;'>• {ReviewView._confuse_item(line)}</p>" for line in confuse)
    return front, back


class _FitScroll(QScrollArea):
    """A scroll area that asks for its content's height, so the card is only
    as tall as it needs to be (the layout still shrinks it to fit, and then
    it scrolls inside)."""

    def sizeHint(self) -> QSize:
        inner = self.widget()
        if inner is None:
            return super().sizeHint()
        width = max(200, self.viewport().width())
        lay = inner.layout()
        height = lay.heightForWidth(width) if lay is not None and lay.hasHeightForWidth() else -1
        if height < 0:
            height = inner.sizeHint().height()
        return QSize(super().sizeHint().width(), height + 2)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if event.oldSize().width() != event.size().width():
            self.updateGeometry()


def _column(parent_layout: QVBoxLayout) -> QVBoxLayout:
    """A centred column at most TEXT_WIDTH wide."""
    holder = QWidget()
    holder.setObjectName("panel")
    holder.setStyleSheet("background: transparent;")
    holder.setMaximumWidth(TEXT_WIDTH)
    holder.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
    column = QVBoxLayout(holder)
    column.setContentsMargins(0, 0, 0, 0)
    column.setSpacing(10)
    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    row.addStretch(1)
    row.addWidget(holder, 100)
    row.addStretch(1)
    parent_layout.addLayout(row)
    return column


def _text(text: str, name: str, rich: bool = True) -> QLabel:
    lab = QLabel(text)
    lab.setObjectName(name)
    lab.setWordWrap(True)
    lab.setTextFormat(Qt.TextFormat.RichText if rich else Qt.TextFormat.PlainText)
    lab.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    return lab


class ReviewView(QWidget):
    rated = Signal(int)
    undo_requested = Signal()
    edit_requested = Signal()
    report_requested = Signal()
    open_entry = Signal(str, str)
    end_requested = Signal()
    again_requested = Signal()                 # "Study more" on the summary

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._card: Optional[Card] = None
        self._shown = False
        self._can_edit = False
        self._can_report = False
        self._choice_buttons: list[QPushButton] = []
        self.type_answer = False               # set from Study settings by the controller
        self.hinted = False                    # read by the controller when a rating is given
        self._entry_name = ""

        outer = QVBoxLayout(self)
        outer.setContentsMargins(56, 18, 30, 22)
        outer.setSpacing(12)
        top = QHBoxLayout()
        top.setSpacing(10)
        self.deck_name = label("", "acCardTitle", wrap=False)
        top.addWidget(self.deck_name, 1)
        self.position = label("", "stCount", wrap=False)
        top.addWidget(self.position)
        self.undo_button = button("Undo", "acGhost", "undo-2", self.undo_requested.emit)
        self.undo_button.setToolTip("Undo the last rating (Ctrl+Z)")
        top.addWidget(self.undo_button)
        top.addWidget(button("End", "acGhost", "x", self.end_requested.emit))
        outer.addLayout(top)
        self.progress = QProgressBar()
        self.progress.setObjectName("stProgress")
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(6)
        outer.addWidget(self.progress)

        # the card: as tall as its content, from CARD_MIN up to the space there is
        self.card_frame = QFrame()
        self.card_frame.setObjectName("stReviewCard")
        self.card_frame.setMinimumHeight(CARD_MIN)
        self.card_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        frame = QVBoxLayout(self.card_frame)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setSpacing(0)
        self.badges = QHBoxLayout()
        self.badges.setContentsMargins(20, 14, 20, 0)
        self.badges.setSpacing(6)
        frame.addLayout(self.badges)
        self.scroll = _FitScroll()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("background: transparent;")
        self.scroll.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        inner = QWidget()
        inner.setObjectName("panel")
        inner.setStyleSheet("background: transparent;")
        self._body = QVBoxLayout(inner)
        self._body.setContentsMargins(28, 14, 28, 22)
        self._body.setSpacing(12)
        self.scroll.setWidget(inner)
        frame.addWidget(self.scroll, 1)
        outer.addWidget(self.card_frame)

        # under the card: type your answer, hint, show answer, or the four ratings
        self.typed = QLineEdit()
        self.typed.setObjectName("acInput")
        self.typed.setPlaceholderText("Type your answer, then press Enter")
        self.typed.setMaxLength(300)
        self.typed.returnPressed.connect(self.reveal)
        outer.addWidget(self.typed)
        self.flip_row = QWidget()
        self.flip_row.setObjectName("panel")
        flip = QHBoxLayout(self.flip_row)
        flip.setContentsMargins(0, 0, 0, 0)
        flip.setSpacing(8)
        self.hint_button = button("Hint (H)", "acGhost", "lightbulb", self.show_hint)
        self.hint_button.setMinimumHeight(42)
        flip.addWidget(self.hint_button)
        self.show_button = button("Show answer", "acPrimary", "eye", self.reveal)
        self.show_button.setMinimumHeight(42)
        self.show_button.setToolTip("Space or Enter")
        flip.addWidget(self.show_button, 1)
        outer.addWidget(self.flip_row)
        self.rating_host = QWidget()
        self.rating_host.setObjectName("panel")
        ratings = QHBoxLayout(self.rating_host)
        ratings.setContentsMargins(0, 0, 0, 0)
        ratings.setSpacing(8)
        self.rate_buttons: dict[Rating, QPushButton] = {}
        for rating in Rating:
            b = QPushButton()
            b.setObjectName("stRate")
            b.setProperty("rating", str(int(rating)))
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setMinimumHeight(48)
            b.setToolTip(f"Key {int(rating)}")
            b.clicked.connect(lambda _c=False, r=rating: self._rate(r))
            self.rate_buttons[rating] = b
            ratings.addWidget(b, 1)
        outer.addWidget(self.rating_host)

        # the summary at the end
        self.summary = QWidget()
        self.summary.setObjectName("panel")
        self._summary = QVBoxLayout(self.summary)
        self._summary.setContentsMargins(0, 0, 0, 0)
        self._summary.setSpacing(10)
        outer.addWidget(self.summary, 1)
        self.summary.hide()
        self._spacer = QWidget()
        self._spacer.setObjectName("panel")
        outer.addWidget(self._spacer, 1)       # space below a short card
        outer.addWidget(label(DISCLAIMER, "stDisclaimer"))

        for key, slot in (("Space", self._key_reveal), ("Return", self._key_reveal), ("Enter", self._key_reveal),
                          ("H", self._key_hint),
                          ("1", lambda: self._key_rate(Rating.AGAIN)), ("2", lambda: self._key_rate(Rating.HARD)),
                          ("3", lambda: self._key_rate(Rating.GOOD)), ("4", lambda: self._key_rate(Rating.EASY)),
                          ("Ctrl+Z", self.undo_requested.emit), ("E", self._key_edit), ("R", self._key_report)):
            # Esc is the sheet's own shortcut (it ends the session); a second one here would make both silent
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
            shortcut.activated.connect(slot)

    # --------------------------------------------------------------- showing

    def show_card(self, card: Card, deck_title: str, index: int, total: int, previews: dict,
                  can_edit: bool, can_report: bool, can_undo: bool, entry_name: str = "",
                  updated: bool = False, subject_id: str = "") -> None:
        self._card = card
        self._shown = False
        self.hinted = False
        self._can_edit, self._can_report = can_edit, can_report
        self.summary.hide()
        self._spacer.show()
        self.card_frame.show()
        self.deck_name.setText(deck_title)
        self.position.setText(f"{index} / {total}")
        self.progress.setRange(0, max(1, total))
        self.progress.setValue(max(0, index - 1))
        self.undo_button.setEnabled(can_undo)
        self._entry_name = entry_name
        for rating, b in self.rate_buttons.items():
            b.setText(f"{RATING_TEXT[rating]}\n{previews.get(rating, '')}")
            b.setChecked(False)
        self._fill_badges(card, subject_id, updated)

        clear_layout(self._body)
        self._choice_buttons = []
        self._body.addStretch(1)                       # centres a short front
        self._front = _column(self._body)
        if card.type == CardType.CLOZE:
            front = _text(cloze.question_html(card.cloze_text), "stFront")
        else:
            front = _text(_rich(card.front), "stFront")
        front.setAlignment(Qt.AlignmentFlag.AlignHCenter if card.type != CardType.MCQ
                           else Qt.AlignmentFlag.AlignLeft)
        self._front.addWidget(front)
        self._hint_label = _text("", "stHintText")
        self._hint_label.setAlignment(front.alignment())
        self._hint_label.hide()
        self._front.addWidget(self._hint_label)
        if card.type == CardType.MCQ:
            for i, choice in enumerate(card.choices):
                b = QPushButton(f"{chr(65 + i)}.  {choice.text}")
                b.setObjectName("stChoice")
                b.setCursor(Qt.CursorShape.PointingHandCursor)
                b.clicked.connect(lambda _c=False, n=i: self._choose(n))
                self._front.addWidget(b)
                self._choice_buttons.append(b)
                why = _text(_rich(choice.rationale), "stRationale")
                why.hide()
                b.why = why
                self._front.addWidget(why)
        self._back = _column(self._body)
        self._body.addStretch(1)

        has_hint = bool(card.hint.strip())
        self.hint_button.setVisible(has_hint)
        self.hint_button.setEnabled(has_hint)
        typing = self.type_answer and card.type in (CardType.BASIC, CardType.CLOZE) and bool(answer_text(card))
        self.typed.clear()
        self.typed.setVisible(typing)
        self.show_button.setVisible(card.type != CardType.MCQ)
        self.flip_row.setVisible(card.type != CardType.MCQ or has_hint)
        self.rating_host.hide()
        self.scroll.verticalScrollBar().setValue(0)
        self.scroll.updateGeometry()
        self._animate_in()
        if typing:
            self.typed.setFocus()
        else:
            self.setFocus()

    def _fill_badges(self, card: Card, subject_id: str, updated: bool) -> None:
        clear_layout(self.badges)
        self.badges.addStretch(1)
        items = []
        if SUBJECT_NAMES.get(subject_id or ""):
            items.append((SUBJECT_NAMES[subject_id], ""))
        system = (card.source_ref or {}).get("system") or ""
        if system:
            items.append((system, ""))
        if card.difficulty:
            items.append((card.difficulty.capitalize(), card.difficulty))
        for text, level in items:
            badge = label(text, "stBadge", wrap=False)
            if level:
                badge.setProperty("level", level)
                repolish(badge)
            self.badges.addWidget(badge)
        if updated:
            badge = label("Updated", "stBadge", wrap=False)
            badge.setProperty("origin", "official")
            repolish(badge)
            badge.setToolTip("This card's content changed since you last saw it. Your progress on it is kept.")
            self.badges.addWidget(badge)

    def show_hint(self) -> None:
        if self._card is None or self._shown or not self._card.hint.strip() or self._hint_label.isVisible():
            return
        self.hinted = True
        self._hint_label.setText("Hint: " + _rich(self._card.hint))
        self._hint_label.show()
        fade_in(self._hint_label, 0, 220)
        self.hint_button.setEnabled(False)
        self.scroll.updateGeometry()

    def reveal(self) -> None:
        if self._card is None or self._shown or not self.card_frame.isVisible():
            return
        if self._card.type == CardType.MCQ:
            return                                 # answered by picking a choice
        self._shown = True
        card = self._card
        typed = self.typed.text().strip() if self.typed.isVisible() else None
        if card.type == CardType.CLOZE:
            self._section("Answer", _text(cloze.answer_html(card.cloze_text), "stAnswer"), first=True)
        else:
            self._section("Answer", self._answer_label(card), first=True)
            extra = card.back.strip()
            if card.answer_short.strip() and extra and extra != card.answer_short.strip():
                self._back.addWidget(_text(_rich(extra), "stBack"))
        if typed:
            want = answer_text(card)
            self._section("You typed", _text(_marked(typed, want), "stTyped"))
            pick = answer_match.suggested(typed, want)
            if pick is not None:
                self.rate_buttons[Rating(pick)].setChecked(True)
        self._teaching(card)
        self._after_answer()

    def _answer_label(self, card: Card) -> QLabel:
        return _text(_rich(card.answer_short or card.back), "stAnswer")

    def _section(self, title: str, body: QWidget, first: bool = False) -> None:
        if first:
            rule = QFrame()
            rule.setObjectName("stRule")
            rule.setFixedHeight(1)
            self._back.addWidget(rule)
            fade_in(rule, 0, 200)
        head = label(title.upper(), "stSection", wrap=False)
        self._back.addWidget(head)
        self._back.addWidget(body)
        delay = 60 * max(0, self._back.count() // 2 - 1)
        fade_in(head, delay, 260)
        fade_in(body, delay + 40, 320)

    def _teaching(self, card: Card) -> None:
        """Why, Don't confuse with, and the worked steps of a calculation.
        On a multiple-choice card, what the choices' explanations already say
        is not repeated."""
        said = {c.rationale.strip().lower() for c in card.choices if c.rationale.strip()}
        lines = [line.strip() for line in (card.explanation or "").split("\n") if line.strip()]
        if lines and card.family == "rx_calc":
            steps = "".join(f"<tr><td style='padding-right:8px; font-family: Consolas, monospace;'>{i}.</td>"
                            f"<td>{_mono_numbers(line)}</td></tr>" for i, line in enumerate(lines, 1))
            self._section("Steps", _text(f"<table cellspacing='0' cellpadding='2'>{steps}</table>", "stWhy"))
        elif lines and " ".join(lines).lower() not in said:
            self._section("Why", _text(_rich(" ".join(lines)), "stWhy"))
        confuse = [line.strip() for line in (card.distinguish or "").split("\n")
                   if line.strip() and line.partition(":")[2].strip().lower() not in said]
        if confuse:
            items = "".join(f"<li>{self._confuse_item(line)}</li>" for line in confuse)
            self._section("Don't confuse with",
                          _text(f"<ul style='margin-left:-18px'>{items}</ul>", "stWhy"))

    @staticmethod
    def _confuse_item(line: str) -> str:
        name, sep, rest = line.partition(":")
        if sep and rest.strip() and len(name) <= 80:
            return f"<b>{html.escape(name.strip())}</b>: {html.escape(rest.strip())}"
        return html.escape(line)

    def _choose(self, index: int) -> None:
        if self._shown or self._card is None:
            return
        self._shown = True
        card = self._card
        picked = card.choices[index]
        for i, (b, choice) in enumerate(zip(self._choice_buttons, card.choices)):
            if choice.correct:
                b.setProperty("result", "right")
            elif i == index:
                b.setProperty("result", "wrong")
            repolish(b)
            b.setEnabled(False)
            if choice.rationale:
                b.why.show()
                fade_in(b.why, 80 * i, 260)
        right = ", ".join(c.text for c in card.choices if c.correct)
        verdict = "Right." if picked.correct else "Not quite."
        self._section("Answer", _text(f"<span>{html.escape(verdict)}</span> "
                                      f"{_rich(card.answer_short or right)}", "stAnswer"), first=True)
        self._teaching(card)
        self.rate_buttons[Rating.GOOD if picked.correct else Rating.AGAIN].setChecked(True)
        self._after_answer()

    def _after_answer(self) -> None:
        self.flip_row.hide()
        self.typed.hide()
        self.rating_host.show()
        stagger(list(self.rate_buttons.values()), 45)
        self._footer(self._card)
        self.scroll.updateGeometry()
        self.setFocus()

    def _footer(self, card: Card) -> None:
        """Source, Open {entry}, Edit and Report, at the bottom of the back."""
        row = QHBoxLayout()
        row.setSpacing(8)
        ref = card.source_ref or {}
        raw = (ref.get("field") or "").split(":")[0]
        field = SOURCE_FIELD.get(raw, raw.replace("_", " "))
        name = self._entry_name or ENTRY_WORD.get(card.source_kind or "", "entry")
        short = name if len(name) <= 32 else name[:30].rstrip() + "…"
        if card.source_kind and card.source_id and card.source_kind in ENTRY_WORD:
            source = label(f"Source: Akeso, {field}" if field else "Source: Akeso", "stCount", wrap=False)
            source.setToolTip(f"{name}" + (f" · {field}" if field else ""))
            row.addWidget(source)
        row.addStretch(1)
        if card.source_kind and card.source_id and card.source_kind in ("disease", "symptom", "medicine", "article"):
            link = button(f"Open {short}", "acLink", "external-link",
                          lambda: self.open_entry.emit(card.source_kind, card.source_id))
            link.setToolTip(f"Open {name}")
            row.addWidget(link)
        if self._can_edit:
            row.addWidget(button("Edit (E)", "acLink", "pencil", self.edit_requested.emit))
        if self._can_report:
            row.addWidget(button("Report (R)", "acLink", "flag", self.report_requested.emit))
        if row.count() > 1:
            rule = QFrame()
            rule.setObjectName("stRule")
            rule.setFixedHeight(1)
            self._back.addSpacing(4)
            self._back.addWidget(rule)
            self._back.addLayout(row)

    def _rate(self, rating: Rating) -> None:
        if self._shown:
            self.rated.emit(int(rating))

    def _key_reveal(self) -> None:
        if self.typed.hasFocus():
            return                                  # Space types a space; Enter is handled by the box
        self.reveal()

    def _key_hint(self) -> None:
        if not self.typed.hasFocus():
            self.show_hint()

    def _key_rate(self, rating: Rating) -> None:
        if self._shown and self.rating_host.isVisible():
            self.rated.emit(int(rating))

    def _key_edit(self) -> None:
        if self._can_edit and self._card is not None and not self.typed.hasFocus():
            self.edit_requested.emit()

    def _key_report(self) -> None:
        if self._can_report and self._card is not None and not self.typed.hasFocus():
            self.report_requested.emit()

    def _animate_in(self) -> None:
        """A short slide for the next card. (No fade on the whole card: the
        sections inside fade in themselves, and Qt can't draw a fade inside
        a fade.)"""
        start = self.card_frame.pos()
        self._slide = QPropertyAnimation(self.card_frame, b"pos", self)
        self._slide.setDuration(180)
        self._slide.setStartValue(start + QPoint(24, 0))
        self._slide.setEndValue(start)
        self._slide.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._slide.start()

    # -------------------------------------------------------------- summary

    def show_summary(self, reviewed: int, correct: int, seconds: float, next_due: str) -> None:
        self._card = None
        self.card_frame.hide()
        self._spacer.hide()
        self.flip_row.hide()
        self.typed.hide()
        self.rating_host.hide()
        self.progress.setValue(self.progress.maximum())
        self.position.setText("Done")
        self.undo_button.setEnabled(False)
        clear_layout(self._summary)
        percent = round(100 * correct / reviewed) if reviewed else 0
        minutes = int(seconds // 60)
        head = QHBoxLayout()
        head.setSpacing(24)
        ring = ProgressRing(150)
        ring.show_progress(percent / 100 if reviewed else 1.0, f"{percent}%" if reviewed else "✓",
                           "remembered" if reviewed else "nothing due")
        head.addWidget(ring)
        text = QVBoxLayout()
        text.setSpacing(6)
        cheer = ("Great session!" if percent >= 85 else "Good work." if percent >= 60
                 else "Tough set: these will come back sooner.") if reviewed else "All caught up."
        text.addWidget(label(cheer, "pageTitle"))
        number = label("0", "stHeroNumber", wrap=False)
        text.addWidget(number)
        count_up(number, reviewed, "{} card" + ("s" if reviewed != 1 else "") + " reviewed")
        text.addWidget(label(f"{minutes} min {int(seconds % 60)} s · {next_due}", "acMuted"))
        text.addStretch(1)
        head.addLayout(text, 1)
        self._summary.addLayout(head)
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(button("Study more", "acGhost", "play", self.again_requested.emit))
        row.addWidget(button("Close", "acPrimary", "check", self.end_requested.emit))
        row.addStretch(1)
        self._summary.addLayout(row)
        self._summary.addStretch(1)
        self.summary.show()
        fade_in(self.summary, 0, 320)
