"""Dashboard Overview: the landing page after signing in.

Display only. It shows what DashboardController hands it and emits what
the user clicked; it never loads anything itself.

Layout ("clean + charts"):

    greeting, date, role, quick actions
    announcements from the admins (only while any are live)
    daily health tip (only when tips exist in data/health_tips.json)
    Study activity: streak, 14-day chart, this week     | Finish your profile (until 100%)
    Explore by body system: tiles with disease counts
    Continue studying                                   | Clinical Exchange (+ unread)
    Recent searches     |     Bookmarks     |     Reference library
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath
from PySide6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QScrollArea, QSizePolicy, QVBoxLayout, QWidget,
)

from app.core.theme import Theme
from app.models.account import ACTIVITY_FIELDS
from app.ui.components.fluid import ResponsiveGrid
from app.ui.views.account.account_widgets import (
    Card, ProgressRing, button, icon_label, label, pill, refresh_icons, repolish,
)
from app.ui.views.account.overview_tab import STAT_ICONS

QUICK_ACTIONS = [
    ("symptom-checker", "Check symptoms", "stethoscope", "acPrimary"),
    ("drug-checker", "Check interactions", "arrow-left-right", "acGhost"),
    ("new-note", "New note", "notebook-pen", "acGhost"),
    ("emergency", "Emergency Guide", "triangle-alert", "acDanger"),
]
LIBRARY = [
    ("diseases", "Diseases", "book-open"),
    ("symptoms", "Symptoms", "activity"),
    ("medicines", "Medicines", "pill"),
    ("emergency", "First-aid protocols", "heart-pulse"),
]


@dataclass
class DashRow:
    """One line in a dashboard list."""

    key: str              # what to open (meaning depends on the list)
    title: str
    subtitle: str = ""
    right: str = ""       # a short time or count on the right
    icon: str = "circle"  # a lucide name
    extra: str = ""       # e.g. the kind, when the key alone is not enough


# ------------------------------------------------------------------ charts

class ActivityChart(QWidget):
    """The last 14 days as bars: one series, so one colour and no legend.

    Bars start at the baseline with 4px rounded tops and a gap between them;
    today is labelled, and hovering a bar shows its day and count.
    """

    def __init__(self) -> None:
        super().__init__()
        self._days: list[tuple[date, int]] = []
        self._hover = -1
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

    def set_days(self, days: list[tuple[date, int]]) -> None:
        self._days = days
        self.update()

    def _geometry(self) -> tuple[list[QRectF], float, float]:
        count = max(len(self._days), 1)
        gap = 8.0
        left, right = 26.0, 4.0
        top, bottom = 16.0, self.height() - 24.0
        width = max(6.0, (self.width() - left - right - gap * (count - 1)) / count)
        peak = max([n for _d, n in self._days] + [1])
        rects = []
        for i, (_day, total) in enumerate(self._days):
            h = (bottom - top) * total / peak if total else 0.0
            rects.append(QRectF(left + i * (width + gap), bottom - h, width, h))
        return rects, top, bottom

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        x = event.position().x()
        rects, _top, _bottom = self._geometry()
        hover = -1
        for i, rect in enumerate(rects):
            # The hit area is the whole column, wider and taller than the bar.
            if rect.left() - 4 <= x <= rect.right() + 4:
                hover = i
                day, total = self._days[i]
                self.setToolTip(f"{day.strftime('%a, %b %d').replace(' 0', ' ')}\n"
                                f"{total} {'activity' if total == 1 else 'activities'}")
                break
        if hover == -1:
            self.setToolTip("")
        if hover != self._hover:
            self._hover = hover
            self.update()

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._hover = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rects, top, bottom = self._geometry()
        muted = QColor(Theme.token("TEXT_MUTED"))
        grid = QColor(Theme.token("BORDER"))
        font = QFont()
        font.setPixelSize(10)
        painter.setFont(font)

        # Recessive grid: the baseline and the peak, labelled on the left.
        peak = max([n for _d, n in self._days] + [0])
        painter.setPen(grid)
        painter.drawLine(int(26), int(bottom), self.width() - 4, int(bottom))
        if peak:
            painter.drawLine(int(26), int(top), self.width() - 4, int(top))
            painter.setPen(muted)
            painter.drawText(QRectF(0, top - 7, 22, 14), Qt.AlignmentFlag.AlignRight, str(peak))
        painter.setPen(muted)
        painter.drawText(QRectF(0, bottom - 7, 22, 14), Qt.AlignmentFlag.AlignRight, "0")

        primary = QColor(Theme.token("PRIMARY"))
        today = date.today()
        for i, (rect, (day, total)) in enumerate(zip(rects, self._days)):
            if total:
                colour = QColor(primary)
                if self._hover not in (-1, i):
                    colour.setAlpha(150)
                path = QPainterPath()
                radius = min(4.0, rect.width() / 2, rect.height())
                path.addRoundedRect(rect.adjusted(0, 0, 0, radius), radius, radius)
                painter.save()
                painter.setClipRect(QRectF(rect.left(), rect.top(), rect.width(), rect.height()))
                painter.fillPath(path, colour)
                painter.restore()
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(grid)
                painter.drawRoundedRect(QRectF(rect.left(), bottom - 3, rect.width(), 3), 1.5, 1.5)
            # Day initials; today in full ink so the reader finds "now".
            painter.setPen(QColor(Theme.token("TEXT")) if day == today else muted)
            text = "Today" if day == today else day.strftime("%a")[0]
            painter.drawText(QRectF(rect.center().x() - 20, bottom + 5, 40, 14),
                             Qt.AlignmentFlag.AlignHCenter, text)
        painter.end()


class SystemTile(QFrame):
    """One body system: its name, how many diseases it has, and a bar
    showing that count against the largest system (one hue, magnitude)."""

    clicked = Signal(str)

    def __init__(self, system_id: str, name: str, count: int, peak: int) -> None:
        super().__init__()
        self.setObjectName("acRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = system_id
        self._share = count / peak if peak else 0.0
        column = QVBoxLayout(self)
        column.setContentsMargins(12, 10, 12, 10)
        column.setSpacing(6)
        top = QHBoxLayout()
        title = label(name, "acRowTitle", wrap=False)
        title.setMinimumWidth(30)
        top.addWidget(title, 1)
        top.addWidget(label(str(count), "acRowTitle", wrap=False))
        column.addLayout(top)
        self._bar = QWidget()
        self._bar.setFixedHeight(6)
        column.addWidget(self._bar)
        column.addWidget(label(f"{count} disease{'s' if count != 1 else ''}", "acSmall",
                               wrap=False))
        self._bar.paintEvent = self._paint_bar

    def _paint_bar(self, _event) -> None:
        painter = QPainter(self._bar)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(0, 0, self._bar.width(), self._bar.height())
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(Theme.token("BORDER")))
        painter.drawRoundedRect(rect, 3, 3)
        if self._share:
            painter.setBrush(QColor(Theme.token("PRIMARY")))
            painter.drawRoundedRect(QRectF(0, 0, max(6.0, rect.width() * self._share), 6), 3, 3)
        painter.end()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._id)
        super().mouseReleaseEvent(event)


# ------------------------------------------------------------------- lists

class ListRow(QFrame):
    clicked = Signal(object)              # the DashRow

    def __init__(self, row: DashRow) -> None:
        super().__init__()
        self.setObjectName("acRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._row = row
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)
        layout.addWidget(icon_label(row.icon, 16), 0, Qt.AlignmentFlag.AlignVCenter)
        text = QVBoxLayout()
        text.setSpacing(1)
        title = label(row.title, "acRowTitle", wrap=False)
        title.setMinimumWidth(40)
        text.addWidget(title)
        if row.subtitle:
            sub = label(row.subtitle, "acSmall", wrap=False)
            sub.setMinimumWidth(40)
            text.addWidget(sub)
        layout.addLayout(text, 1)
        if row.right:
            layout.addWidget(label(row.right, "acSmall", wrap=False), 0,
                             Qt.AlignmentFlag.AlignVCenter)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._row)
        super().mouseReleaseEvent(event)


class ListCard(Card):
    """A titled card holding a short list, an empty message and a link."""

    row_clicked = Signal(object)
    see_all = Signal()

    def __init__(self, title: str, subtitle: str, icon: str, link_text: str = "See all") -> None:
        super().__init__(title, subtitle, icon)
        self.badge = pill("", "acPill")
        self.badge.hide()
        self.head.addWidget(self.badge, 0, Qt.AlignmentFlag.AlignTop)
        self.head.addWidget(button(link_text, "acLink", on_click=self.see_all.emit), 0,
                            Qt.AlignmentFlag.AlignTop)
        self._list = QVBoxLayout()
        self._list.setSpacing(6)
        self.body.addLayout(self._list)
        self._empty = label("", "acMuted")
        self.body.addWidget(self._empty)

    def set_rows(self, rows: list[DashRow], empty_text: str) -> None:
        while self._list.count():
            item = self._list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for row in rows:
            widget = ListRow(row)
            widget.clicked.connect(self.row_clicked.emit)
            self._list.addWidget(widget)
        self._empty.setText(empty_text)
        self._empty.setVisible(not rows)

    def set_badge(self, text: str) -> None:
        self.badge.setText(text)
        self.badge.setVisible(bool(text))


class MiniStat(QFrame):
    """A compact count: icon badge, number, caption."""

    def __init__(self, caption: str, icon: str) -> None:
        super().__init__()
        self.setObjectName("acRow")
        row = QHBoxLayout(self)
        row.setContentsMargins(10, 8, 12, 8)
        row.setSpacing(10)
        row.addWidget(icon_label(icon, 18), 0, Qt.AlignmentFlag.AlignVCenter)
        text = QVBoxLayout()
        text.setSpacing(0)
        self.number = label("—", "acCardTitle", wrap=False)
        text.addWidget(self.number)
        cap = label(caption, "acSmall", wrap=False)
        cap.setMinimumWidth(30)
        text.addWidget(cap)
        row.addLayout(text, 1)

    def set_number(self, value) -> None:
        self.number.setText(f"{value:,}" if isinstance(value, int) else str(value))


# -------------------------------------------------------------------- page

class DashboardView(QWidget):
    action_requested = Signal(str)        # a QUICK_ACTIONS key or a tab id
    note_opened = Signal(str)             # notebook item id
    search_opened = Signal(object)        # DashRow from Recent searches
    bookmark_opened = Signal(str, str)    # entity type, entity id
    post_opened = Signal(str)             # Clinical Exchange post id
    system_opened = Signal(str)           # body system id
    profile_step = Signal(str)            # the Account tab that fixes a step

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
        column.setSpacing(16)

        column.addWidget(self._build_hero())
        # Live announcements from the admins (migration 015); hidden when none.
        from app.ui.views.announcement_widgets import AnnouncementList
        self.announcements = AnnouncementList()
        column.addWidget(self.announcements)
        self.tip = self._build_tip()
        column.addWidget(self.tip)

        top = QHBoxLayout()
        top.setSpacing(16)
        top.addWidget(self._build_activity(), 3)
        self.profile = self._build_profile()
        top.addWidget(self.profile, 2)
        column.addLayout(top)

        column.addWidget(self._build_systems())

        middle = QHBoxLayout()
        middle.setSpacing(16)
        self.notes = ListCard("Continue studying", "Your most recent notes and cases.",
                              "notebook-pen", "Open notebook")
        self.notes.row_clicked.connect(lambda r: self.note_opened.emit(r.key))
        self.notes.see_all.connect(lambda: self.action_requested.emit("notebook"))
        self.exchange = ListCard("Clinical Exchange", "Newest hypothetical cases.",
                                 "message-circle", "Open board")
        self.exchange.row_clicked.connect(lambda r: self.post_opened.emit(r.key))
        self.exchange.see_all.connect(lambda: self.action_requested.emit("exchange"))
        middle.addWidget(self.notes, 1)
        middle.addWidget(self.exchange, 1)
        column.addLayout(middle)

        bottom = QGridLayout()
        bottom.setHorizontalSpacing(16)
        bottom.setVerticalSpacing(16)
        self.searches = ListCard("Recent searches", "From the search bar.", "history")
        self.searches.row_clicked.connect(self.search_opened.emit)
        self.searches.see_all.connect(lambda: self.action_requested.emit("history"))
        self.bookmarks = ListCard("Bookmarks", "Entries you starred.", "bookmark")
        self.bookmarks.row_clicked.connect(lambda r: self.bookmark_opened.emit(r.extra, r.key))
        self.bookmarks.see_all.connect(lambda: self.action_requested.emit("favorites"))
        bottom.addWidget(self.searches, 0, 0)
        bottom.addWidget(self.bookmarks, 0, 1)
        bottom.addWidget(self._build_library(), 0, 2)
        for i in range(3):
            bottom.setColumnStretch(i, 1)
        column.addLayout(bottom)
        column.addStretch(1)

        self.scroll.setWidget(page)
        outer.addWidget(self.scroll)
        self.stat_grid.watch(self.scroll.viewport())
        self.system_grid.watch(self.scroll.viewport())

    # ------------------------------------------------------------- pieces

    def _build_hero(self) -> QFrame:
        hero = QFrame()
        hero.setObjectName("acHero")
        column = QVBoxLayout(hero)
        column.setContentsMargins(24, 22, 24, 20)
        column.setSpacing(14)
        top = QHBoxLayout()
        text = QVBoxLayout()
        text.setSpacing(4)
        self.greeting = label("", "acTitle")
        self.date_line = label("", "acSubtitle")
        text.addWidget(self.greeting)
        text.addWidget(self.date_line)
        top.addLayout(text, 1)
        self.role = pill("", "acPill")
        top.addWidget(self.role, 0, Qt.AlignmentFlag.AlignTop)
        column.addLayout(top)
        actions = QHBoxLayout()
        actions.setSpacing(8)
        for key, text_, icon, style in QUICK_ACTIONS:
            actions.addWidget(button(text_, style, icon,
                                     lambda k=key: self.action_requested.emit(k)))
        actions.addStretch(1)
        column.addLayout(actions)
        return hero

    def _build_tip(self) -> QFrame:
        tip = QFrame()
        tip.setObjectName("acBanner")
        tip.setProperty("tone", "good")
        row = QHBoxLayout(tip)
        row.setContentsMargins(16, 12, 16, 12)
        row.setSpacing(12)
        row.addWidget(icon_label("sparkles", 18), 0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(label("HEALTH TIP OF THE DAY", "acFieldLabel", wrap=False))
        self.tip_text = label("", "acBannerText")
        self.tip_source = label("", "acSmall")
        text.addWidget(self.tip_text)
        text.addWidget(self.tip_source)
        row.addLayout(text, 1)
        tip.hide()
        return tip

    def _build_activity(self) -> Card:
        card = Card("Study activity", "Last 14 days. Private to you.", "trending-up")
        card.head.addWidget(button("Details", "acLink",
                                   on_click=lambda: self.action_requested.emit("account")),
                            0, Qt.AlignmentFlag.AlignTop)
        line = QHBoxLayout()
        line.setSpacing(10)
        line.addWidget(pill("\U0001F525 Streak", "acPillWarn"))
        self.streak = label("—", "acCardTitle", wrap=False)
        line.addWidget(self.streak)
        self.activity_total = label("", "acSmall")
        line.addWidget(self.activity_total, 1)
        card.body.addLayout(line)
        self.chart = ActivityChart()
        card.body.addWidget(self.chart)
        self.activity_note = label("", "acMuted")
        self.activity_note.hide()
        card.body.addWidget(self.activity_note)
        card.body.addWidget(label("THIS WEEK", "acFieldLabel", wrap=False))
        self._stats: dict[str, MiniStat] = {}
        stats = []
        for key, caption in ACTIVITY_FIELDS:
            stat = MiniStat(caption, STAT_ICONS.get(key, "circle"))
            self._stats[key] = stat
            stats.append(stat)
        self.stat_grid = ResponsiveGrid(170, max_columns=3, spacing=8, steps=(3, 2))
        self.stat_grid.set_cards(stats)
        card.body.addWidget(self.stat_grid)
        return card

    def _build_profile(self) -> Card:
        card = Card("Finish your profile", "A few steps unlock the full workspace.",
                    "user-check")
        row = QHBoxLayout()
        row.setSpacing(16)
        self.ring = ProgressRing(84)
        row.addWidget(self.ring, 0, Qt.AlignmentFlag.AlignTop)
        self._steps = QVBoxLayout()
        self._steps.setSpacing(6)
        row.addLayout(self._steps, 1)
        card.body.addLayout(row)
        card.body.addWidget(button("Open Account Settings", "acGhost", "user",
                                   lambda: self.action_requested.emit("account")),
                            0, Qt.AlignmentFlag.AlignLeft)
        card.hide()
        return card

    def _build_systems(self) -> Card:
        card = Card("Explore by body system", "How many diseases each system has in the "
                    "encyclopedia. Click one to browse it.", "heart-pulse")
        self.system_grid = ResponsiveGrid(200, max_columns=5, spacing=10, steps=(5, 4, 3, 2))
        card.body.addWidget(self.system_grid)
        self.systems_empty = label("", "acMuted")
        card.body.addWidget(self.systems_empty)
        return card

    def _build_library(self) -> Card:
        card = Card("Reference library", "What you can study right now.", "layers")
        self._library: dict[str, QLabel] = {}
        for key, caption, icon in LIBRARY:
            row = ListRow(DashRow(key, caption, icon=icon))
            row.clicked.connect(lambda r: self.action_requested.emit(r.key))
            number = label("—", "acRowTitle", wrap=False)
            row.layout().addWidget(number, 0, Qt.AlignmentFlag.AlignVCenter)
            self._library[key] = number
            card.body.addWidget(row)
        self.library_note = label("", "acSmall")
        self.library_note.hide()
        card.body.addWidget(self.library_note)
        return card

    # ---------------------------------------------------------------- api

    def show_greeting(self, greeting: str, date_text: str, role_text: str) -> None:
        self.greeting.setText(greeting)
        self.date_line.setText(date_text)
        self.role.setText(role_text)
        self.role.setVisible(bool(role_text))

    def show_tip(self, text: str, source: str) -> None:
        self.tip_text.setText(text)
        self.tip_source.setText(f"Source: {source}" if source else "")
        self.tip_source.setVisible(bool(source))
        self.tip.setVisible(bool(text))

    def show_activity(self, streak: Optional[int], days: list[tuple[date, int]],
                      week: dict, note: str = "") -> None:
        """streak None = nothing to show (tracking off, signed out, or failed)."""
        has = streak is not None
        self.streak.setText(f"{streak} day{'s' if streak != 1 else ''}" if has else "—")
        total = sum(n for _d, n in days)
        self.activity_total.setText(
            f"{total} activit{'y' if total == 1 else 'ies'} in the last 14 days" if has else "")
        self.chart.setVisible(has)
        self.chart.set_days(days)
        self.activity_note.setText(note)
        self.activity_note.setVisible(bool(note))
        for key, stat in self._stats.items():
            stat.set_number(int(week.get(key, 0)) if has else "—")

    def show_profile(self, percent: Optional[int], steps: list[tuple[str, str]]) -> None:
        """steps: (label, account tab) still to do. Hidden at 100% or unknown."""
        self.profile.setVisible(percent is not None and percent < 100)
        if percent is None:
            return
        self.ring.set_value(percent)
        while self._steps.count():
            item = self._steps.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for text, tab in steps[:4]:
            self._steps.addWidget(button(f"○  {text}", "acLink",
                                         on_click=lambda t=tab: self.profile_step.emit(t)),
                                  0, Qt.AlignmentFlag.AlignLeft)
        if len(steps) > 4:
            self._steps.addWidget(label(f"+ {len(steps) - 4} more", "acSmall"))

    def show_systems(self, systems: list[tuple[str, str, int]]) -> None:
        """[(id, name, disease count)], largest first."""
        peak = max([n for _i, _n, n in systems] + [0])
        tiles = []
        for system_id, name, count in systems:
            tile = SystemTile(system_id, name, count, peak)
            tile.clicked.connect(self.system_opened.emit)
            tiles.append(tile)
        self.system_grid.set_cards(tiles)
        self.systems_empty.setText("" if systems else
                                   "Body systems appear once the encyclopedia has loaded.")
        self.systems_empty.setVisible(not systems)

    def show_library(self, counts: dict[str, Optional[int]], note: str = "") -> None:
        for key, number in self._library.items():
            value = counts.get(key)
            number.setText("—" if value is None else f"{value:,}")
        self.library_note.setText(note)
        self.library_note.setVisible(bool(note))

    def set_unread(self, count: int) -> None:
        self.exchange.set_badge(f"{count} unread" if count else "")

    def refresh_theme(self) -> None:
        refresh_icons(self)
        repolish(self)
        self.chart.update()
