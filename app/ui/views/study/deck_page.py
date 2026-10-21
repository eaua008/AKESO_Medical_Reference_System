"""One deck, full page (inside a PageSheet): its badge and counts, Study now,
and the cards. Your own decks can be renamed right in the header, and
their cards added, edited and deleted. When a deck mixes difficulties or
kinds of card, two filters pick what Study now asks ("only calculations")."""

from PySide6.QtCore import Qt, Signal
from typing import Optional

from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLineEdit, QScrollArea, QVBoxLayout, QWidget

from app.models.study import Card, CardState, CardStateKind, CardType, DIFFICULTIES, DISCLAIMER, TYPE_LABELS
from app.services.study import cloze
from app.services.study.study_service import DeckSummary
from app.ui.views.account.account_widgets import Card as Panel, button, icon_label, label
from app.ui.views.study.widgets import SUBJECT_NAMES, clear_layout, counts_text, family_groups, origin_badge

TYPE_ICONS = {CardType.BASIC: "layers", CardType.MCQ: "list", CardType.CLOZE: "pencil",
              CardType.LABEL3D: "heart-pulse"}
STATE_TEXT = {CardStateKind.NEW: "New", CardStateKind.LEARNING: "Learning",
              CardStateKind.RELEARNING: "Relearning", CardStateKind.REVIEW: "Learned",
              CardStateKind.SUSPENDED: "Suspended"}


def card_preview(card: Card) -> str:
    if card.type == CardType.CLOZE:
        return cloze.question(card.cloze_text)
    return card.front


class DeckPage(QWidget):
    study_requested = Signal(str)
    rename_requested = Signal(str, str)
    delete_requested = Signal(str)
    reset_requested = Signal(str)
    add_card_requested = Signal(str)
    edit_card_requested = Signal(str)               # card id
    delete_card_requested = Signal(str)
    back_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        self._column = QVBoxLayout(page)
        self._column.setContentsMargins(56, 22, 30, 30)
        self._column.setSpacing(14)
        scroll.setWidget(page)
        outer.addWidget(scroll)
        self._deck_id = ""
        self._cards: list[Card] = []
        self.difficulty: Optional[QComboBox] = None
        self.kind: Optional[QComboBox] = None

    def show_deck(self, summary: DeckSummary, cards: list[Card], states: dict[str, CardState]) -> None:
        clear_layout(self._column)
        deck = summary.deck
        self._deck_id = deck.id
        top = QHBoxLayout()
        top.setSpacing(8)
        top.addWidget(origin_badge(deck))
        subject = SUBJECT_NAMES.get(deck.subject_id, "")
        if subject:
            top.addWidget(label(subject, "stCount", wrap=False))
        top.addStretch(1)
        self._column.addLayout(top)
        if deck.editable:
            self.title = QLineEdit(deck.title)
            self.title.setObjectName("exComposerTitle")
            self.title.setMaxLength(120)
            self.title.setToolTip("Click to rename")
            self.title.editingFinished.connect(self._renamed)
            self._column.addWidget(self.title)
        else:
            self._column.addWidget(label(deck.title, "pageTitle"))
        if deck.description:
            self._column.addWidget(label(deck.description, "acMuted"))
        self._column.addWidget(label(f"{summary.counts.total} cards · {counts_text(summary.counts)}",
                                     "stCount"))
        actions = QHBoxLayout()
        actions.setSpacing(8)
        study = button("Study now", "acPrimary", "play", lambda: self.study_requested.emit(deck.id))
        study.setEnabled(bool(cards))
        actions.addWidget(study)
        if deck.editable:
            actions.addWidget(button("Add card", "acGhost", "plus", lambda: self.add_card_requested.emit(deck.id)))
        if summary.started:
            actions.addWidget(button("Reset progress", "acGhost", "rotate-ccw",
                                     lambda: self.reset_requested.emit(deck.id)))
        if deck.editable:
            actions.addWidget(button("Delete deck", "acDanger", "trash-2", lambda: self.delete_requested.emit(deck.id)))
        actions.addStretch(1)
        self._column.addLayout(actions)
        self._cards = cards
        self._study = study
        self._filters(cards)

        panel = Panel(f"Cards ({len(cards)})", "", "layers")
        if not cards:
            panel.body.addWidget(label("No cards yet. Press Add card to make the first one."
                                       if deck.editable else "This deck has no cards.", "acMuted"))
        for card in cards[:400]:
            state = states.get(card.card_key)
            row = QFrame()
            row.setObjectName("stRow")
            line = QHBoxLayout(row)
            line.setContentsMargins(12, 8, 10, 8)
            line.setSpacing(10)
            line.addWidget(icon_label(TYPE_ICONS.get(card.type, "layers"), 15), 0, Qt.AlignmentFlag.AlignTop)
            text = card_preview(card)
            body = QVBoxLayout()
            body.setSpacing(1)
            body.addWidget(label(text[:160] + ("…" if len(text) > 160 else ""), "acRowTitle"))
            kind = next((name for name, fams in family_groups() if card.family in fams), "")
            body.addWidget(label(" · ".join(x for x in (TYPE_LABELS[card.type], kind,
                                                        (card.difficulty or "").capitalize(),
                                                        STATE_TEXT[state.state] if state else "New") if x),
                                 "acSmall"))
            line.addLayout(body, 1)
            if deck.editable:
                line.addWidget(button("", "acGhost", "pencil", lambda _c=False, i=card.id: self.edit_card_requested.emit(i)))
                line.addWidget(button("", "acGhost", "trash-2", lambda _c=False, i=card.id: self.delete_card_requested.emit(i)))
            panel.body.addWidget(row)
        if len(cards) > 400:
            panel.body.addWidget(label(f"+ {len(cards) - 400} more cards", "acSmall"))
        self._column.addWidget(panel)
        self._column.addWidget(label(DISCLAIMER, "stDisclaimer"))
        self._column.addStretch(1)

    def _filters(self, cards: list[Card]) -> None:
        """Difficulty and kind pickers, only when the deck has more than one."""
        self.difficulty = self.kind = None
        levels = [d for d in DIFFICULTIES if any((c.difficulty or "basic") == d for c in cards)]
        present = {c.family for c in cards if c.family}
        kinds = [(name, fams) for name, fams in family_groups() if present & set(fams)]
        if len(levels) < 2 and len(kinds) < 2:
            return
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(label("Study only:", "stCount", wrap=False))
        if len(levels) >= 2:
            self.difficulty = QComboBox()
            self.difficulty.setObjectName("acInput")
            self.difficulty.addItem("Any difficulty", None)
            for level in levels:
                self.difficulty.addItem(level.capitalize(), [level])
            self.difficulty.currentIndexChanged.connect(self._count)
            row.addWidget(self.difficulty)
        if len(kinds) >= 2:
            self.kind = QComboBox()
            self.kind.setObjectName("acInput")
            self.kind.addItem("Any kind of card", None)
            for name, fams in kinds:
                self.kind.addItem(name, fams)
            self.kind.currentIndexChanged.connect(self._count)
            row.addWidget(self.kind)
        self._match = label("", "stCount", wrap=False)
        row.addWidget(self._match)
        row.addStretch(1)
        self._column.addLayout(row)

    def difficulties(self) -> Optional[list]:
        """The picked difficulty, or None (then Study settings decide)."""
        return self.difficulty.currentData() if self.difficulty is not None else None

    def families(self) -> Optional[list]:
        return self.kind.currentData() if self.kind is not None else None

    def _count(self) -> None:
        levels, fams = self.difficulties(), self.families()
        if levels is None and fams is None:
            self._match.setText("")
            self._study.setEnabled(bool(self._cards))
            return
        n = sum(1 for c in self._cards
                if (levels is None or (c.difficulty or "basic") in levels) and (fams is None or c.family in fams))
        self._match.setText("1 card matches" if n == 1 else f"{n} cards match")
        self._study.setEnabled(n > 0)

    def _renamed(self) -> None:
        text = self.title.text().strip()
        if text:
            self.rename_requested.emit(self._deck_id, text)

    @property
    def deck_id(self) -> str:
        return self._deck_id

