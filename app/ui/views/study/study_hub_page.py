"""Study Hub: Today | Courses | Decks under one header (sync chip, settings).
Only the content scrolls; the sidebar and the header stay put."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QFrame, QHBoxLayout, QPushButton, QScrollArea, QStackedWidget, QVBoxLayout, QWidget,
)

from app.ui.views.account.account_widgets import Card, button, label, refresh_icons, repolish
from app.ui.views.study.decks_view import DecksView
from app.ui.views.study.today_view import TodayView
from app.ui.views.study.widgets import SyncChip

TABS = [("today", "Today"), ("courses", "Courses"), ("decks", "Decks")]


class StudyHubPage(QWidget):
    settings_requested = Signal()
    sync_requested = Signal()
    tab_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        column = QVBoxLayout(page)
        column.setContentsMargins(30, 22, 30, 30)
        column.setSpacing(14)

        head = QHBoxLayout()
        head.setSpacing(10)
        titles = QVBoxLayout()
        titles.setSpacing(2)
        titles.addWidget(label("Study Hub", "pageTitle", wrap=False))
        titles.addWidget(label("Flashcards that come back just before you would forget them.", "pageSubtitle"))
        head.addLayout(titles, 1)
        self.sync_chip = SyncChip()
        self.sync_chip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sync_chip.setToolTip("Click to sync now")
        self.sync_chip.mousePressEvent = lambda _e: self.sync_requested.emit()
        head.addWidget(self.sync_chip, 0, Qt.AlignmentFlag.AlignTop)
        gear = button("", "acGhost", "settings", self.settings_requested.emit)
        gear.setToolTip("Study settings")
        head.addWidget(gear, 0, Qt.AlignmentFlag.AlignTop)
        column.addLayout(head)

        tabs = QHBoxLayout()
        tabs.setSpacing(18)
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._tabs: dict[str, QPushButton] = {}
        for key, text in TABS:
            tab = QPushButton(text)
            tab.setObjectName("stTab")
            tab.setCheckable(True)
            tab.setCursor(Qt.CursorShape.PointingHandCursor)
            tab.clicked.connect(lambda _c=False, k=key: self.open_tab(k))
            self._group.addButton(tab)
            self._tabs[key] = tab
            tabs.addWidget(tab)
        tabs.addStretch(1)
        column.addLayout(tabs)
        rule = QFrame()
        rule.setObjectName("stRule")
        rule.setFixedHeight(1)
        column.addWidget(rule)

        self.stack = QStackedWidget()
        self.today = TodayView()
        self.courses = QWidget()
        self.courses.setObjectName("panel")
        courses = QVBoxLayout(self.courses)
        courses.setContentsMargins(0, 0, 0, 0)
        soon = Card("Courses are coming", "Curated courses (Anatomy, Pathology, Pharmacology, "
                    "Microbiology) with lessons, decks and quizzes arrive in the next update.",
                    "graduation-cap")
        courses.addWidget(soon)
        courses.addStretch(1)
        self.decks = DecksView()
        for widget in (self.today, self.courses, self.decks):
            self.stack.addWidget(widget)
        column.addWidget(self.stack, 1)
        self.scroll.setWidget(page)
        outer.addWidget(self.scroll)
        self.decks.watch(self.scroll.viewport())
        self.open_tab("today")

    def open_tab(self, key: str) -> None:
        self._tabs[key].setChecked(True)
        self.stack.setCurrentWidget({"today": self.today, "courses": self.courses, "decks": self.decks}[key])
        self.scroll.verticalScrollBar().setValue(0)
        self.tab_changed.emit(key)

    def current_tab(self) -> str:
        widget = self.stack.currentWidget()
        return "today" if widget is self.today else "decks" if widget is self.decks else "courses"

    def refresh_theme(self) -> None:
        refresh_icons(self)
        repolish(self)
