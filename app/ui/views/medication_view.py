"""Medication Tracker & Drug Safety Center: the page.

    MedicationView     header, 4 stat cards, tab row, tab content
    CoursesTab         "My Medication Courses": filters on the left, cards right
    CourseCard         one course with its countdown and actions

Scrolling: the page sits in its own QScrollArea, like the Wellness and
Emergency pages, so only this content area scrolls. The app's header and
sidebar never move.

The view never touches data. It emits what the user asked for and draws
whatever the controller hands it.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.medication_styles import tone_color
from app.core.theme import Theme
from app.models.medication import (
    ABANDONED,
    COMPLETED,
    STATE_MISSED,
    MedicationCourse,
)
from app.ui.views.medication_safety_tab import SafetyTab
from app.services.medication_service import (
    CATEGORY_FILTERS,
    STATUS_FILTERS,
    CourseStats,
    Preset,
)

CARD_MIN_WIDTH = 270     # below this the grid drops a column


class MedicationView(QWidget):
    track_requested = Signal()
    add_med_requested = Signal()
    theme_changed = Signal()     # cards and results are rebuilt with new icon colours

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        # Icons are painted in one colour, so each static one registers how to
        # repaint itself; refresh_theme() replays them after a theme switch.
        self._icon_jobs: list = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        page = QWidget()
        page.setObjectName("panel")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 20, 24, 28)
        layout.setSpacing(16)

        layout.addWidget(self._build_header())
        layout.addLayout(self._build_stats())
        layout.addWidget(self._build_tabs())

        self.courses = CoursesTab()
        self.courses.track_requested.connect(self.track_requested.emit)
        self.safety = SafetyTab()
        self.stack = QStackedWidget()
        self.stack.setObjectName("panel")
        self.stack.addWidget(self.courses)
        self.stack.addWidget(self.safety)
        layout.addWidget(self.stack)
        layout.addStretch(1)

        scroll.setWidget(page)
        root.addWidget(scroll)

    # ------------------------------------------------------------ builders

    def _build_header(self) -> QWidget:
        card = QFrame()
        card.setObjectName("mdHeaderCard")
        row = QHBoxLayout(card)
        row.setContentsMargins(18, 16, 18, 16)
        row.setSpacing(14)

        tile = QFrame()
        tile.setObjectName("mdIconTile")
        tile.setFixedSize(40, 40)
        tile_layout = QVBoxLayout(tile)
        tile_layout.setContentsMargins(0, 0, 0, 0)
        header_icon = QLabel()
        header_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._paint(header_icon, "pill", 20, "white")
        tile_layout.addWidget(header_icon)
        row.addWidget(tile)

        titles = QVBoxLayout()
        titles.setSpacing(2)
        titles.addWidget(QLabel("Medication Tracker && Drug Safety Center".replace("&&", "&"),
                                objectName="mdTitle"))
        subtitle = QLabel("Patient-side course adherence, decrementing intake countdowns, "
                          "and rule-based pairwise drug interaction safety.",
                          objectName="mdSubtitle")
        subtitle.setWordWrap(True)
        titles.addWidget(subtitle)
        row.addLayout(titles, 1)

        track = QPushButton(" Track New Course")
        track.setObjectName("mdPrimary")
        self._paint(track, "plus", 15, "white")
        track.setCursor(Qt.CursorShape.PointingHandCursor)
        track.clicked.connect(self.track_requested.emit)
        add = QPushButton(" Add to Current Meds")
        add.setObjectName("mdSecondary")
        self._paint(add, "plus", 15, "text")
        add.setCursor(Qt.CursorShape.PointingHandCursor)
        add.clicked.connect(self.add_med_requested.emit)
        row.addWidget(track)
        row.addWidget(add)
        return card

    def _build_stats(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(12)
        self.stat_active = _StatCard("ACTIVE COURSES")
        self.stat_adherence = _StatCard("ADHERENCE SCORE")
        self.stat_regimen = _StatCard("ACTIVE REGIMEN")
        self.stat_safety = _StatCard("DRUG SAFETY CHECK")
        for card, name, tone in ((self.stat_active, "clock", "primary"),
                                 (self.stat_adherence, "trending-up", "success"),
                                 (self.stat_regimen, "activity", "primary"),
                                 (self.stat_safety, "shield-check", "success")):
            self._paint(card.icon, name, 16, tone)
        for card in (self.stat_active, self.stat_adherence, self.stat_regimen,
                     self.stat_safety):
            row.addWidget(card, 1)
        self.stat_safety.set("Not checked", "Run a check in the Interaction & Safety "
                             "Check tab")
        return row

    def _build_tabs(self) -> QWidget:
        row_widget = QWidget()
        row_widget.setObjectName("mdTabRow")
        row = QHBoxLayout(row_widget)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)
        group = QButtonGroup(self)
        group.setExclusive(True)

        self.tab_courses = QPushButton(" My Medication Courses")
        self.tab_safety = QPushButton(" Interaction && Safety Check")
        self._paint(self.tab_courses, "clock", 15, "muted")
        self._paint(self.tab_safety, "shield", 15, "muted")
        for index, button in enumerate((self.tab_courses, self.tab_safety)):
            button.setObjectName("mdTab")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            group.addButton(button)
            button.clicked.connect(lambda _c=False, i=index: self.stack.setCurrentIndex(i))
            row.addWidget(button)
            if index == 0:
                self.tab_count = QLabel("0", objectName="mdTabCount")
                self.tab_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tab_count.setFixedHeight(18)
                self.tab_count.setMinimumWidth(20)
                row.addWidget(self.tab_count, 0, Qt.AlignmentFlag.AlignVCenter)
                row.addSpacing(10)
        self.tab_courses.setChecked(True)
        row.addStretch(1)
        return row_widget

    # ------------------------------------------------------------- drawing

    def show_stats(self, stats: CourseStats, course_count: int) -> None:
        self.stat_active.set(str(stats.active_courses),
                             f"{stats.doses_remaining} total doses remaining to complete")
        self.stat_adherence.set(f"{stats.adherence}%",
                                f"{stats.completed_courses} completed courses on record",
                                badge="Review Missed Doses" if stats.has_missed else "")
        self.stat_regimen.set(str(stats.regimen_count),
                              "Current prescription & OTC therapies")
        self.tab_count.setText(str(course_count))

    def _paint(self, widget: QWidget, name: str, size: int, tone: str) -> None:
        def job() -> None:
            if isinstance(widget, QPushButton):
                widget.setIcon(lucide.icon(name, size, tone_color(tone)))
            else:
                widget.setPixmap(lucide.pixmap(name, size, tone_color(tone)))
        job()
        self._icon_jobs.append(job)

    def refresh_theme(self) -> None:
        """Called by the shell after a theme switch."""
        for job in self._icon_jobs:
            job()
        self.courses.repaint_icons()
        self.theme_changed.emit()


class _StatCard(QFrame):
    def __init__(self, label: str) -> None:
        super().__init__()
        self.setObjectName("mdStat")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        head = QHBoxLayout()
        head.addWidget(QLabel(label, objectName="mdStatLabel"))
        head.addStretch(1)
        self.icon = QLabel()
        head.addWidget(self.icon)
        layout.addLayout(head)
        value_row = QHBoxLayout()
        value_row.setSpacing(8)
        self.value = QLabel("0", objectName="mdStatValue")
        value_row.addWidget(self.value)
        self.badge = _badge("", "amber")
        self.badge.hide()
        value_row.addWidget(self.badge, 0, Qt.AlignmentFlag.AlignVCenter)
        value_row.addStretch(1)
        layout.addLayout(value_row)
        self.note = QLabel("", objectName="mdSmallMuted")
        self.note.setWordWrap(True)
        layout.addWidget(self.note)

    def set(self, value: str, note: str, badge: str = "", tone: str = "") -> None:
        self.value.setText(value)
        self.note.setText(note)
        self.badge.setText(badge)
        self.badge.setVisible(bool(badge))
        self.setProperty("tone", tone)
        _repolish(self)


# ======================================================================
# Tab 1: My Medication Courses
# ======================================================================

class CoursesTab(QWidget):
    filters_changed = Signal(str, str, str)     # query, status, category
    track_requested = Signal()
    preset_chosen = Signal(str)                 # course id to copy from
    log_requested = Signal(str)
    abandon_requested = Signal(str)
    details_requested = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._status = "all"
        self._category = "all"
        self._cards: list[CourseCard] = []
        self._icon_jobs: list = []

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(16)
        row.addWidget(self._build_filters(), 0, Qt.AlignmentFlag.AlignTop)

        right = QVBoxLayout()
        right.setSpacing(10)
        self.showing = QLabel("", objectName="mdSmallMuted")
        right.addWidget(self.showing)
        self.grid_host = QWidget()
        self.grid_host.setObjectName("panel")
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(14)
        right.addWidget(self.grid_host)
        self.empty = self._build_empty()
        right.addWidget(self.empty)
        right.addStretch(1)
        row.addLayout(right, 1)
        self.repaint_icons()

    def repaint_icons(self) -> None:
        for job in self._icon_jobs:
            job()

    # ------------------------------------------------------------ filters

    def _build_filters(self) -> QWidget:
        column = QWidget()
        column.setObjectName("panel")
        column.setFixedWidth(270)
        layout = QVBoxLayout(column)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        search_panel, search_body = _panel()
        search_body.addWidget(QLabel("Search Courses", objectName="mdMetaKey"))
        self.search = QLineEdit()
        self.search.setObjectName("mdInput")
        self.search.setPlaceholderText("Filter by medicine or doctor...")
        self.search.textChanged.connect(self._emit_filters)
        search_body.addWidget(self.search)
        layout.addWidget(search_panel)

        status_panel, status_body = _panel()
        status_head = QHBoxLayout()
        status_head.addWidget(QLabel("COURSE STATUS", objectName="mdPanelHeading"))
        status_head.addStretch(1)
        funnel = QLabel()
        self._icon_jobs.append(lambda: funnel.setPixmap(
            lucide.pixmap("funnel", 13, tone_color("muted"))))
        status_head.addWidget(funnel)
        status_body.addLayout(status_head)
        self._status_group = QButtonGroup(self)
        self._status_counts: dict[str, QLabel] = {}
        for key, text in STATUS_FILTERS:
            button, count = _filter_button(text, with_count=True)
            self._status_group.addButton(button)
            self._status_counts[key] = count
            button.clicked.connect(lambda _c=False, k=key: self._set_status(k))
            status_body.addWidget(button)
            if key == "all":
                button.setChecked(True)
        layout.addWidget(status_panel)

        category_panel, category_body = _panel()
        category_body.addWidget(QLabel("CATEGORY", objectName="mdPanelHeading"))
        self._category_group = QButtonGroup(self)
        for key, text in CATEGORY_FILTERS:
            button, _ = _filter_button(text, soft=True)
            self._category_group.addButton(button)
            button.clicked.connect(lambda _c=False, k=key: self._set_category(k))
            category_body.addWidget(button)
            if key == "all":
                button.setChecked(True)
        layout.addWidget(category_panel)

        preset_panel, self._preset_body = _panel()
        preset_head = QHBoxLayout()
        preset_head.setSpacing(6)
        sparkle = QLabel()
        self._icon_jobs.append(lambda: sparkle.setPixmap(
            lucide.pixmap("sparkles", 13, tone_color("primary"))))
        preset_head.addWidget(sparkle)
        preset_head.addWidget(QLabel("QUICK REGIMEN PRESETS", objectName="mdPanelHeading"))
        preset_head.addStretch(1)
        self._preset_body.addLayout(preset_head)
        self._preset_buttons: list[QWidget] = []
        layout.addWidget(preset_panel)

        track = QPushButton(" Track New Course")
        track.setObjectName("mdPrimaryWide")
        self._icon_jobs.append(lambda: track.setIcon(lucide.icon("plus", 15, "#FFFFFF")))
        track.setCursor(Qt.CursorShape.PointingHandCursor)
        track.clicked.connect(self.track_requested.emit)
        layout.addWidget(track)
        return column

    def _set_status(self, key: str) -> None:
        self._status = key
        self._emit_filters()

    def _set_category(self, key: str) -> None:
        self._category = key
        self._emit_filters()

    def _emit_filters(self) -> None:
        self.filters_changed.emit(self.search.text(), self._status, self._category)

    def filters(self) -> tuple[str, str, str]:
        return self.search.text(), self._status, self._category

    def _build_empty(self) -> QWidget:
        box = QFrame()
        box.setObjectName("mdPanel")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(24, 36, 24, 36)
        layout.setSpacing(6)
        self.empty_title = QLabel("No courses yet", objectName="mdEmptyTitle")
        self.empty_note = QLabel("Track a prescribed course to start its countdown.",
                                 objectName="mdMuted")
        layout.addWidget(self.empty_title, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.empty_note, 0, Qt.AlignmentFlag.AlignHCenter)
        box.hide()
        return box

    # ------------------------------------------------------------- drawing

    def show_counts(self, counts: dict[str, int]) -> None:
        for key, label in self._status_counts.items():
            label.setText(str(counts.get(key, 0)))

    def show_presets(self, presets: list[Preset]) -> None:
        for widget in self._preset_buttons:
            widget.setParent(None)
            widget.deleteLater()
        self._preset_buttons = []
        if not presets:
            note = QLabel("Courses you track appear here for one-click reuse.",
                          objectName="mdSmallMuted")
            note.setWordWrap(True)
            self._preset_body.addWidget(note)
            self._preset_buttons.append(note)
            return
        for preset in presets:
            button = QPushButton(_elide(preset.title, 30))
            button.setToolTip(preset.title)
            button.setObjectName("mdPreset")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, cid=preset.course.id:
                                   self.preset_chosen.emit(cid))
            self._preset_body.addWidget(button)
            self._preset_buttons.append(button)

    def show_courses(self, courses: list[MedicationCourse], total: int) -> None:
        for card in self._cards:
            card.setParent(None)
            card.deleteLater()
        self._cards = [CourseCard(c) for c in courses]
        for card in self._cards:
            card.log_requested.connect(self.log_requested.emit)
            card.abandon_requested.connect(self.abandon_requested.emit)
            card.details_requested.connect(self.details_requested.emit)

        self.showing.setText(f"Showing <b>{len(courses)}</b> of {total} courses")
        self.empty.setVisible(not courses)
        if not courses:
            filtered = total > 0
            self.empty_title.setText("No matching courses" if filtered else "No courses yet")
            self.empty_note.setText("Try another filter or search." if filtered
                                    else "Track a prescribed course to start its countdown.")
        self._reflow()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._reflow()

    def _reflow(self) -> None:
        """Lay the cards out in as many columns as fit (1 to 3)."""
        # The tab's own width minus the 270px filter column and its gap:
        # grid_host.width() lags one resize behind and gave wrong counts.
        width = max(self.width() - 270 - 16, 1)
        columns = max(1, min(3, (width + 14) // (CARD_MIN_WIDTH + 14)))
        for card in self._cards:
            self.grid.removeWidget(card)
        for index, card in enumerate(self._cards):
            self.grid.addWidget(card, index // columns, index % columns,
                                Qt.AlignmentFlag.AlignTop)
        for col in range(3):
            self.grid.setColumnStretch(col, 1 if col < columns else 0)


class CourseCard(QFrame):
    log_requested = Signal(str)
    abandon_requested = Signal(str)
    details_requested = Signal(str)

    def __init__(self, course: MedicationCourse) -> None:
        super().__init__()
        self.setObjectName("mdCard")
        # Never squeeze a card below its content height.
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        state = course.state()
        self.setProperty("state", state)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        top = QHBoxLayout()
        title = QLabel(course.medicine_name, objectName="mdCardTitle")
        title.setWordWrap(True)
        top.addWidget(title, 1)
        top.addWidget(_state_badge(state), 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(top)

        if course.is_protected:
            layout.addWidget(QLabel("FULL-COURSE CRITICAL", objectName="mdChip"), 0,
                             Qt.AlignmentFlag.AlignLeft)
        if course.dosage_schedule:
            schedule = QLabel(course.dosage_schedule, objectName="mdSubtitle")
            schedule.setWordWrap(True)
            layout.addWidget(schedule)

        layout.addWidget(self._countdown(course, state))

        if state == STATE_MISSED and course.is_protected:
            layout.addWidget(_note_box(
                "mdWarnBox", "mdWarnTitle", "triangle-alert", "amber",
                "Do Not Stop Early — Antimicrobial Stewardship",
                f"Finish all {course.total_units} {course.unit_label} even if symptoms "
                "resolve to prevent bacterial resistance."))
        elif state == ABANDONED:
            reason = f" | Abandoned: {course.abandon_reason}" if course.abandon_reason else ""
            body = ("Complete the full course. Do not stop early even if fever resolves "
                    "to prevent antibiotic resistance." if course.is_protected
                    else "This course was stopped before the last dose.")
            layout.addWidget(_note_box("mdDangerBox", "mdDangerTitle", "circle-alert",
                                       "danger", "Course Abandoned Early", body + reason))

        meta = QVBoxLayout()
        meta.setSpacing(2)
        if course.prescriber:
            meta.addWidget(_meta_line("Prescriber:", course.prescriber))
        meta.addWidget(_meta_line("Started:",
                                  f"{_short_date(course.started_on)} • Duration: "
                                  f"{course.duration_days} Days"))
        layout.addLayout(meta)
        layout.addStretch(1)

        # Finished courses keep View Details, so their history stays reachable.
        layout.addWidget(_divider())
        actions = QHBoxLayout()
        actions.setSpacing(8)
        active = course.status not in (COMPLETED, ABANDONED)
        if active:
            log = QPushButton(" Log Intake Now")
            log.setObjectName("mdPrimary")
            log.setIcon(lucide.icon("check", 15, "#FFFFFF"))
            log.setCursor(Qt.CursorShape.PointingHandCursor)
            log.clicked.connect(lambda: self.log_requested.emit(course.id))
            actions.addWidget(log)
        details = QPushButton(" View Details")
        details.setObjectName("mdGhost")
        details.setIcon(lucide.icon("eye", 15, tone_color("text")))
        details.setCursor(Qt.CursorShape.PointingHandCursor)
        details.clicked.connect(lambda: self.details_requested.emit(course.id))
        actions.addWidget(details)
        actions.addStretch(1)
        if active:
            abandon = QPushButton("Abandon")
            abandon.setObjectName("mdDangerLink")
            abandon.setCursor(Qt.CursorShape.PointingHandCursor)
            abandon.clicked.connect(lambda: self.abandon_requested.emit(course.id))
            actions.addWidget(abandon)
        layout.addLayout(actions)

    @staticmethod
    def _countdown(course: MedicationCourse, state: str) -> QFrame:
        box = QFrame()
        box.setObjectName("mdCountdown")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        head = QHBoxLayout()
        clock = QLabel()
        clock.setPixmap(lucide.pixmap("clock", 14, tone_color("primary")))
        head.addWidget(clock)
        head.addWidget(QLabel("Remaining:", objectName="mdMuted"))
        head.addStretch(1)
        remaining = QLabel(f"<span style='color:{Theme.token('PRIMARY_TEXT_ON_NAV')}'>"
                           f"{course.remaining}</span> / {course.total_units} "
                           f"{course.unit_label}", objectName="mdRemaining")
        head.addWidget(remaining)
        layout.addLayout(head)

        bar = QProgressBar()
        bar.setObjectName("mdProgress")
        bar.setTextVisible(False)
        bar.setRange(0, 100)
        bar.setValue(course.percent_complete)
        bar.setProperty("tone", "danger" if state == ABANDONED
                        else "success" if state == COMPLETED else "")
        layout.addWidget(bar)

        foot = QHBoxLayout()
        foot.addWidget(QLabel(f"{course.percent_complete}% Completed",
                              objectName="mdSmallMuted"))
        foot.addStretch(1)
        foot.addWidget(QLabel(f"Adherence: {course.adherence()}%",
                              objectName="mdSmallMuted"))
        layout.addLayout(foot)
        return box


# --------------------------------------------------------------- helpers

def _panel() -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setObjectName("mdPanel")
    body = QVBoxLayout(frame)
    body.setContentsMargins(12, 12, 12, 12)
    body.setSpacing(6)
    return frame, body


def _filter_button(text: str, with_count: bool = False,
                   soft: bool = False) -> tuple[QPushButton, Optional[QLabel]]:
    button = QPushButton()
    button.setObjectName("mdFilter")
    button.setCheckable(True)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    if soft:
        button.setProperty("soft", "true")
    row = QHBoxLayout(button)
    row.setContentsMargins(10, 0, 8, 0)
    label = QLabel(text, objectName="mdFilterText")
    # Clicks pass through to the button underneath.
    label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    if soft:
        label.setProperty("soft", "true")
    row.addWidget(label)

    # A QLabel can't inherit the button's :checked colour, so the button
    # tells the label with a property and the stylesheet does the rest.
    def mark(checked: bool) -> None:
        label.setProperty("on", "true" if checked else "false")
        _repolish(label)
    button.toggled.connect(mark)
    mark(False)
    row.addStretch(1)
    count = None
    if with_count:
        count = QLabel("0", objectName="mdCount")
        count.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Only as big as the number: a fixed small height, centred in the
        # row, instead of stretching to the button's full height.
        count.setFixedHeight(18)
        count.setMinimumWidth(20)
        row.addWidget(count, 0, Qt.AlignmentFlag.AlignVCenter)
    button.setFixedHeight(34)
    return button, count


def _badge(text: str, tone: str) -> QLabel:
    badge = QLabel(text, objectName="mdBadge")
    badge.setProperty("tone", tone)
    return badge


def _state_badge(state: str) -> QLabel:
    text, tone = {
        "on_track": ("On Track", "primary"),
        "missed": ("Missed Dose", "amber"),
        "completed": ("Completed", "success"),
        "abandoned": ("Abandoned", "danger"),
    }[state]
    return _badge(text, tone)


def _note_box(frame_name: str, title_name: str, icon_name: str, tone: str,
              title: str, body: str) -> QFrame:
    box = QFrame()
    box.setObjectName(frame_name)
    layout = QVBoxLayout(box)
    layout.setContentsMargins(10, 8, 10, 8)
    layout.setSpacing(3)
    head = QHBoxLayout()
    head.setSpacing(6)
    mark = QLabel()
    mark.setPixmap(lucide.pixmap(icon_name, 14, tone_color(tone)))
    head.addWidget(mark, 0, Qt.AlignmentFlag.AlignTop)
    heading = QLabel(title, objectName=title_name)
    heading.setWordWrap(True)
    head.addWidget(heading, 1)
    layout.addLayout(head)
    text = QLabel(body, objectName="mdBoxBody")
    text.setWordWrap(True)
    layout.addWidget(text)
    return box


def _meta_line(key: str, value: str) -> QLabel:
    label = QLabel(f"<b>{key}</b> <span>{value}</span>", objectName="mdMetaValue")
    label.setWordWrap(True)
    return label


def _short_date(iso: str) -> str:
    """"2026-09-14" -> "9/14/2026", as in the design."""
    year, month, day = iso.split("-")
    return f"{int(month)}/{int(day)}/{year}"


def _elide(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "\u2026"


def _divider() -> QFrame:
    line = QFrame()
    line.setObjectName("mdDivider")
    line.setFixedHeight(1)
    return line


def _repolish(widget: QWidget) -> None:
    """Re-apply the stylesheet after a dynamic property changed."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)
