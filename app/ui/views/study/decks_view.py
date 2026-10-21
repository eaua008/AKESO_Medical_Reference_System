"""Study Hub -> Decks, organised the way a student looks for something:

    Continue studying    the decks you have started (most due first)
    Your decks           the ones you made
    one shelf per subject (Pathology, Pharmacology...), each showing a few
    decks with "Show all" to open the rest

Typing in search, or picking a filter chip or subject, turns the shelves
into one list of matches. Tiles grow a shadow when pointed at and fade in.
"""

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QFrame, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget,
)

from app.models.study import Origin
from app.services.study.study_service import DeckSummary
from app.ui.components.fluid import ResponsiveGrid
from app.ui.views.account.account_widgets import button, label
from app.ui.views.study.motion import fade_in, subject_colour
from app.ui.views.study.widgets import SUBJECT_NAMES, DeckTile, clear_layout

FILTERS = [("all", "All"), ("official", "Official"), ("auto", "Auto"), ("mine", "Mine"), ("shared", "Shared")]
SHELF_SIZE = 4


class _Shelf(QWidget):
    """A titled row of deck tiles with Show all / Show fewer."""

    def __init__(self, title: str, colour: str, summaries: list[DeckSummary], make_tile, viewport,
                 subtitle: str = "") -> None:
        super().__init__()
        self.setObjectName("panel")
        self._summaries, self._make_tile, self._open = summaries, make_tile, False
        column = QVBoxLayout(self)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(10)
        head = QHBoxLayout()
        head.setSpacing(8)
        dot = QWidget()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background-color: {colour}; border-radius: 5px;")
        head.addWidget(dot, 0, Qt.AlignmentFlag.AlignVCenter)
        head.addWidget(label(title, "acCardTitle", wrap=False))
        head.addWidget(label(f"{len(summaries)} deck{'s' if len(summaries) != 1 else ''}", "stCount", wrap=False))
        if subtitle:
            head.addWidget(label(subtitle, "stCount", wrap=False))
        head.addStretch(1)
        self.more = button("", "acLink", on_click=self._toggle)
        self.more.setVisible(len(summaries) > SHELF_SIZE)
        head.addWidget(self.more)
        column.addLayout(head)
        self.grid = ResponsiveGrid(250, max_columns=4, spacing=12, steps=(4, 3, 2, 1))
        self.grid.watch(viewport)
        column.addWidget(self.grid)
        self._fill()

    def _toggle(self) -> None:
        self._open = not self._open
        self._fill()
        fade_in(self.grid, 0, 220)

    def _fill(self) -> None:
        shown = self._summaries if self._open else self._summaries[:SHELF_SIZE]
        self.grid.set_cards([self._make_tile(s) for s in shown])
        self.more.setText("Show fewer" if self._open else f"Show all {len(self._summaries)}")


class DecksView(QWidget):
    open_requested = Signal(str)
    study_requested = Signal(str)
    new_requested = Signal()
    staff_requested = Signal()                  # educators/admins: official deck editor

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._summaries: list[DeckSummary] = []
        self._viewport = None
        column = QVBoxLayout(self)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(14)

        bar = QHBoxLayout()
        bar.setSpacing(8)
        self.search = QLineEdit()
        self.search.setObjectName("acInput")
        self.search.setPlaceholderText("Search decks, e.g. antibiotics, cardiovascular…")
        self.search.setClearButtonEnabled(True)
        bar.addWidget(self.search, 1)
        self.subject = QComboBox()
        self.subject.setObjectName("acInput")
        self.subject.addItem("All subjects", "")
        for key, name in SUBJECT_NAMES.items():
            self.subject.addItem(name, key)
        bar.addWidget(self.subject)
        self.staff_button = button("Official decks", "acGhost", "badge-check", self.staff_requested.emit)
        self.staff_button.setToolTip("Write official decks (educators draft, admins publish)")
        self.staff_button.hide()
        bar.addWidget(self.staff_button)
        bar.addWidget(button("New deck", "acPrimary", "plus", self.new_requested.emit))
        column.addLayout(bar)

        chips = QHBoxLayout()
        chips.setSpacing(6)
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._filter = "all"
        self._chips: dict[str, QPushButton] = {}
        for key, text in FILTERS:
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setChecked(key == "all")
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.clicked.connect(lambda _c=False, k=key: self._set_filter(k))
            self._group.addButton(chip)
            self._chips[key] = chip
            chips.addWidget(chip)
        chips.addStretch(1)
        self.count = label("", "stCount", wrap=False)
        chips.addWidget(self.count)
        column.addLayout(chips)

        self.body = QVBoxLayout()
        self.body.setSpacing(22)
        column.addLayout(self.body)
        self.empty = QFrame()
        self.empty.setObjectName("stHero")
        empty = QVBoxLayout(self.empty)
        empty.setContentsMargins(24, 28, 24, 28)
        empty.setSpacing(8)
        self.empty_text = label("", "acMuted")
        self.empty_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty.addWidget(self.empty_text)
        new = button("Make a deck", "acPrimary", "plus", self.new_requested.emit)
        empty.addWidget(new, 0, Qt.AlignmentFlag.AlignHCenter)
        self.empty.hide()
        column.addWidget(self.empty)
        column.addStretch(1)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(160)
        self._timer.timeout.connect(self._render)
        self.search.textChanged.connect(lambda _t: self._timer.start())
        self.subject.currentIndexChanged.connect(lambda _i: self._render())

    def watch(self, viewport) -> None:
        self._viewport = viewport

    def set_staff(self, on: bool) -> None:
        self.staff_button.setVisible(on)

    def set_subject(self, subject: str) -> None:
        index = self.subject.findData(subject or "")
        self.subject.setCurrentIndex(max(0, index))

    def _set_filter(self, key: str) -> None:
        self._filter = key
        self._render()

    def show_decks(self, summaries: list[DeckSummary]) -> None:
        self._summaries = summaries
        self._render()

    # -------------------------------------------------------------- render

    def _tile(self, summary: DeckSummary) -> DeckTile:
        tile = DeckTile(summary.deck, summary.counts)
        tile.open_requested.connect(self.open_requested.emit)
        tile.study_requested.connect(self.study_requested.emit)
        return tile

    def _matches(self) -> list[DeckSummary]:
        query = self.search.text().strip().lower()
        subject = self.subject.currentData()
        wanted = {"official": Origin.OFFICIAL, "auto": Origin.AUTO, "mine": Origin.PERSONAL,
                  "shared": Origin.SHARED}.get(self._filter)
        out = []
        for s in self._summaries:
            if wanted is not None and s.deck.origin != wanted:
                continue
            if subject and s.deck.subject_id != subject:
                continue
            if query and query not in s.deck.title.lower() and query not in s.deck.description.lower():
                continue
            out.append(s)
        return out

    @staticmethod
    def _order(items: list[DeckSummary]) -> list[DeckSummary]:
        rank = {Origin.PERSONAL: 0, Origin.OFFICIAL: 1, Origin.SHARED: 2, Origin.AUTO: 3}
        return sorted(items, key=lambda s: (-s.counts.due, rank[s.deck.origin], s.deck.title.lower()))

    def _render(self) -> None:
        clear_layout(self.body)
        matches = self._matches()
        self.count.setText(f"{len(matches)} deck{'s' if len(matches) != 1 else ''}")
        browsing = not self.search.text().strip() and self._filter == "all" and not self.subject.currentData()
        viewport = self._viewport
        shelves: list[QWidget] = []
        if browsing:
            started = self._order([s for s in matches if s.started])
            mine = self._order([s for s in matches if s.deck.origin == Origin.PERSONAL])
            if started:
                shelves.append(_Shelf("Continue studying", "#F59E0B", started, self._tile, viewport))
            if mine:
                shelves.append(_Shelf("Your decks", "#9CA3AF", mine, self._tile, viewport, "private to you"))
            for key, name in SUBJECT_NAMES.items():
                items = self._order([s for s in matches if s.deck.subject_id == key
                                     and s.deck.origin != Origin.PERSONAL])
                if items:
                    shelves.append(_Shelf(name, subject_colour(key), items, self._tile, viewport))
        elif matches:
            title = "Results" if self.search.text().strip() else "Decks"
            shelf = _Shelf(title, subject_colour(self.subject.currentData() or ""), self._order(matches),
                           self._tile, viewport)
            shelf._open = True
            shelf._fill()
            shelves.append(shelf)
        for i, shelf in enumerate(shelves):
            self.body.addWidget(shelf)
            fade_in(shelf, i * 70)
        if not matches:
            self.empty_text.setText("No shared decks yet: when classmates share decks with you (coming soon), "
                                    "they appear here." if self._filter == "shared" else
                                    "No deck matches. Try another word, or make your own deck.")
        self.empty.setVisible(not matches)
