"""Study Hub -> Today, built around the three questions a student has when
they open it: how much is left, how long will it take, and what next.

    hero          a ring that fills as today's cards get done, "24 due ·
                  8 new · about 5 min", Start review, the streak
    next 7 days   how many cards come back each day (plan the week)
    continue      the decks you are studying, with how far along you are
    weak cards    the ones you keep forgetting
    explore       the subjects, for picking something new
    how to rate   what Again / Hard / Good / Easy mean

First-timers see three steps and the subjects instead of empty numbers.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from app.models.study import DISCLAIMER
from app.services.study.study_service import DeckSummary
from app.ui.views.account.account_widgets import Card, button, icon_label, label
from app.ui.views.study.motion import (
    ForecastBars, MasteryBar, ProgressRing, count_up, fade_in, stagger, subject_colour,
)
from app.ui.views.study.widgets import SUBJECT_NAMES, Clickable, clear_layout

RATING_HELP = [("Again", "I forgot it. It comes back in a minute."),
               ("Hard", "I got it, but it was a struggle."),
               ("Good", "I remembered it. The usual choice."),
               ("Easy", "Too easy. Show it much later.")]


def _greeting(hour: int) -> str:
    return "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"


class _DeckRow(Clickable):
    def __init__(self, summary: DeckSummary) -> None:
        super().__init__("stRow")
        deck, counts = summary.deck, summary.counts
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 10, 12, 10)
        row.setSpacing(12)
        dot = QWidget()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background-color: {subject_colour(deck.subject_id)}; border-radius: 5px;")
        row.addWidget(dot, 0, Qt.AlignmentFlag.AlignVCenter)
        text = QVBoxLayout()
        text.setSpacing(5)
        head = label(deck.title, "acRowTitle")
        head.setMinimumWidth(40)
        text.addWidget(head)
        text.addWidget(MasteryBar(counts.learned, counts.learning, counts.total, subject_colour(deck.subject_id)))
        row.addLayout(text, 1)
        right = QVBoxLayout()
        right.setSpacing(0)
        due = label(f"{counts.due} due" if counts.due else "Up to date", "stCountDue" if counts.due else "stCount",
                    wrap=False)
        due.setAlignment(Qt.AlignmentFlag.AlignRight)
        right.addWidget(due)
        percent = round(100 * counts.learned / counts.total) if counts.total else 0
        sub = label(f"{percent}% learned", "stCount", wrap=False)
        sub.setAlignment(Qt.AlignmentFlag.AlignRight)
        right.addWidget(sub)
        row.addLayout(right)


class TodayView(QWidget):
    start_requested = Signal()                 # review everything due today
    deck_requested = Signal(str)               # study one deck
    weak_requested = Signal(list)              # card keys
    browse_requested = Signal()                # go to the Decks tab
    subject_requested = Signal(str)            # Decks tab, one subject

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        column = QVBoxLayout(self)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(16)

        # ---- hero
        self.hero = QFrame()
        self.hero.setObjectName("stHero")
        hero = QHBoxLayout(self.hero)
        hero.setContentsMargins(24, 22, 24, 22)
        hero.setSpacing(24)
        self.ring = ProgressRing(150)
        hero.addWidget(self.ring, 0, Qt.AlignmentFlag.AlignVCenter)
        middle = QVBoxLayout()
        middle.setSpacing(6)
        self.greeting = label("", "stHeroCaption", wrap=False)
        middle.addWidget(self.greeting)
        self.headline = label("", "stHeroNumber")
        middle.addWidget(self.headline)
        self.caption = label("", "stHeroCaption")
        middle.addWidget(self.caption)
        actions = QHBoxLayout()
        actions.setSpacing(8)
        self.start = button("Start review", "acPrimary", "play", self.start_requested.emit)
        self.start.setMinimumHeight(42)
        self.start.setMinimumWidth(170)
        actions.addWidget(self.start)
        actions.addWidget(button("Browse decks", "acGhost", "layers", self.browse_requested.emit))
        actions.addStretch(1)
        middle.addSpacing(6)
        middle.addLayout(actions)
        hero.addLayout(middle, 1)
        streak = QFrame()
        streak.setObjectName("stStreak")
        sc = QVBoxLayout(streak)
        sc.setContentsMargins(18, 14, 18, 14)
        sc.setSpacing(0)
        sc.addWidget(icon_label("flame", 22, "#F59E0B"), 0, Qt.AlignmentFlag.AlignHCenter)
        self.streak = label("0", "stHeroNumber", wrap=False)
        self.streak.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sc.addWidget(self.streak)
        self.streak_caption = label("day streak", "stHeroCaption", wrap=False)
        self.streak_caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sc.addWidget(self.streak_caption)
        hero.addWidget(streak, 0, Qt.AlignmentFlag.AlignVCenter)
        column.addWidget(self.hero)

        # ---- first time
        self.guide = Card("Start studying in three steps", "Flashcards work best a little every day.",
                          "graduation-cap")
        steps = QHBoxLayout()
        steps.setSpacing(12)
        for number, title, text in (
                ("1", "Pick a deck", "An Auto deck made from the encyclopedia, an Official deck, or your own."),
                ("2", "Review", "Think of the answer, show it, then rate how well you knew it."),
                ("3", "Come back tomorrow", "Each card returns just before you would forget it.")):
            step = QFrame()
            step.setObjectName("stRow")
            box = QVBoxLayout(step)
            box.setContentsMargins(14, 12, 14, 12)
            box.setSpacing(4)
            box.addWidget(label(number, "stHeroNumber", wrap=False))
            box.addWidget(label(title, "acRowTitle"))
            box.addWidget(label(text, "acSmall"))
            steps.addWidget(step, 1)
        self.guide.body.addLayout(steps)
        column.addWidget(self.guide)

        # ---- two columns
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)
        self.forecast_card = Card("Next 7 days", "Cards coming back each day. Plan around busy days.",
                                  "calendar")
        self.forecast = ForecastBars()
        self.forecast_card.body.addWidget(self.forecast)
        grid.addWidget(self.forecast_card, 0, 0)

        self.continue_card = Card("Continue studying", "Decks you have started.", "layers")
        self._continue = QVBoxLayout()
        self._continue.setSpacing(6)
        self.continue_card.body.addLayout(self._continue)
        grid.addWidget(self.continue_card, 0, 1)

        self.weak_card = Card("Weak cards", "The ones you keep forgetting. A quick extra pass helps.", "flag")
        self._weak = QVBoxLayout()
        self._weak.setSpacing(6)
        self.weak_card.body.addLayout(self._weak)
        self._weak_keys: list[str] = []
        self.weak_card.head.addWidget(button("Review these", "acLink",
                                             on_click=lambda: self.weak_requested.emit(self._weak_keys)),
                                      0, Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.weak_card, 1, 0)

        self.explore_card = Card("Explore subjects", "Pick something new to learn.", "graduation-cap")
        self._explore = QGridLayout()
        self._explore.setSpacing(8)
        self.explore_card.body.addLayout(self._explore)
        grid.addWidget(self.explore_card, 1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        column.addLayout(grid)

        help_card = Card("How to rate a card", "Be honest: the schedule is only as good as your ratings.",
                         "circle-help")
        help_row = QHBoxLayout()
        help_row.setSpacing(8)
        for i, (name, text) in enumerate(RATING_HELP, start=1):
            box = QFrame()
            box.setObjectName("stRate")
            box.setProperty("rating", str(i))
            inner = QVBoxLayout(box)
            inner.setContentsMargins(12, 10, 12, 10)
            inner.setSpacing(2)
            inner.addWidget(label(f"{i} · {name}", "acRowTitle", wrap=False))
            inner.addWidget(label(text, "acSmall"))
            help_row.addWidget(box, 1)
        help_card.body.addLayout(help_row)
        column.addWidget(help_card)
        column.addWidget(label(DISCLAIMER, "stDisclaimer"))
        column.addStretch(1)

    def show_today(self, due: int, new: int, streak: int, summaries: list[DeckSummary],
                   weak: list, first_time: bool, reviewed: int = 0, seconds_per_card: float = 10.0,
                   forecast: list = (), hour: int = 12) -> None:
        self.greeting.setText(_greeting(hour))
        todo = due + new
        if todo:
            self.headline.setText(f"{due} due · {new} new")
            minutes = max(1, round(todo * seconds_per_card / 60))
            self.caption.setText(f"About {minutes} min. Reviews first, then new cards.")
            self.start.setText("  Start review")
            self.start.setEnabled(True)
        else:
            self.headline.setText("All done for today")
            self.caption.setText("Nice work. Come back tomorrow, or start a new deck.")
            self.start.setText("  All done")
            self.start.setEnabled(False)
        total = reviewed + todo
        self.ring.show_progress(reviewed / total if total else 1.0,
                                f"{todo}" if todo else "✓", "left today" if todo else "done")
        count_up(self.streak, streak)
        self.streak_caption.setText("day streak" if streak != 1 else "day streak")
        self.guide.setVisible(first_time)
        self.hero.setVisible(True)
        self.forecast_card.setVisible(not first_time)
        self.forecast.set_days(list(forecast))

        clear_layout(self._continue)
        started = sorted((s for s in summaries if s.started), key=lambda s: (-s.counts.due, s.deck.title.lower()))
        rows = []
        for summary in started[:6]:
            row = _DeckRow(summary)
            row.clicked.connect(lambda d=summary.deck.id: self.deck_requested.emit(d))
            self._continue.addWidget(row)
            rows.append(row)
        if not started:
            self._continue.addWidget(label("Nothing started yet. Open a deck and press Study.", "acMuted"))
        self.continue_card.setVisible(True)

        clear_layout(self._weak)
        self._weak_keys = [card.card_key for card, _state in weak]
        for card, state in weak[:6]:
            text = card.front or card.cloze_text
            row = Clickable("stRow")
            line = QHBoxLayout(row)
            line.setContentsMargins(12, 8, 12, 8)
            line.addWidget(label(text[:80] + ("…" if len(text) > 80 else ""), "acRowTitle"), 1)
            line.addWidget(label(f"forgot {state.lapses}×", "stCountDue", wrap=False))
            row.clicked.connect(lambda k=card.card_key: self.weak_requested.emit([k]))
            self._weak.addWidget(row)
            rows.append(row)
        self.weak_card.setVisible(bool(weak))

        clear_layout(self._explore)
        per_subject: dict[str, int] = {}
        for s in summaries:
            per_subject[s.deck.subject_id or ""] = per_subject.get(s.deck.subject_id or "", 0) + s.counts.total
        for i, (key, name) in enumerate(SUBJECT_NAMES.items()):
            tile = QPushButton(f"  {name}\n  {per_subject.get(key, 0)} cards" if per_subject.get(key)
                               else f"  {name}\n  Coming soon")
            tile.setObjectName("stSubject")
            tile.setStyleSheet(f"border-left: 4px solid {subject_colour(key)};")
            tile.setCursor(Qt.CursorShape.PointingHandCursor)
            tile.setEnabled(bool(per_subject.get(key)))
            tile.clicked.connect(lambda _c=False, k=key: self.subject_requested.emit(k))
            self._explore.addWidget(tile, i // 2, i % 2)
        stagger([self.hero] + rows, 40)
        fade_in(self.guide if first_time else self.forecast_card, 120)
