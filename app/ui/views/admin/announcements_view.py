"""Admin > Announcements: write a message that pops up for every user (or
only students / educators) on their dashboard after signing in.

    AnnouncementsAdminView   the list: what is live, scheduled or over
    AnnouncementEditor       write / edit one (with a preview)
"""

from datetime import datetime, timedelta
from typing import Optional

from PySide6.QtCore import QDateTime, Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QCheckBox, QDateTimeEdit, QFrame, QGridLayout, QHBoxLayout, QLineEdit,
    QPlainTextEdit, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from app.core.theme import Theme
from app.models.account import friendly_time
from app.models.announcement import (
    AUDIENCE_LABELS, AUDIENCES, BODY_MAX, LABEL_MAX, LEVEL_LABELS, LEVELS, STATUS_LABELS,
    STATUS_TONES, TITLE_MAX, Announcement,
)
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import Banner, button, label, refresh_icons
from app.ui.views.admin.admin_widgets import (
    AdminStat, DataTable, IconButton, actions_cell, page_header, pill_cell, text_cell,
    title_cell,
)

LEVEL_TONES = {"info": "blue", "important": "amber", "critical": "danger"}
COLUMNS = ["Announcement", "Audience", "Importance", "Schedule", "Status", "Seen by",
           "Actions"]
TITLE, AUDIENCE, LEVEL, SCHEDULE, STATUS, SEEN, ACTIONS = range(7)
DATE_FORMAT = "MMM d, yyyy  h:mm AP"


def _to_qt(value: Optional[datetime]) -> QDateTime:
    if value is None:
        return QDateTime.currentDateTime()
    return QDateTime(value.astimezone().replace(tzinfo=None))   # local wall time


def _from_qt(value: QDateTime) -> datetime:
    return value.toPython().astimezone()           # local wall time -> aware


class _Chips(QWidget):
    """One choice out of a few, as chips (importance, audience)."""

    def __init__(self, options: list[tuple[str, str]], current: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._buttons: dict[str, QPushButton] = {}
        for value, text in options:
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.setChecked(value == current)
            self._group.addButton(chip)
            self._buttons[value] = chip
            row.addWidget(chip)
        row.addStretch(1)

    def value(self) -> str:
        return next((v for v, b in self._buttons.items() if b.isChecked()),
                    next(iter(self._buttons)))


class AnnouncementEditor(AccountDialog):
    submitted = Signal(object, bool)       # Announcement, show again to everyone
    preview_requested = Signal(object)     # Announcement

    def __init__(self, item: Optional[Announcement] = None,
                 parent: Optional[QWidget] = None) -> None:
        self._editing = item is not None
        item = item or Announcement(id="", title="", body="")
        super().__init__("Edit announcement" if self._editing else "New announcement",
                         "Pops up on the dashboard after signing in, once per account. "
                         "It stays listed on the dashboard until it ends.",
                         "megaphone", parent, width=620)
        self._id = item.id

        self.title_input = QLineEdit(item.title)
        self.title_input.setObjectName("acInput")
        self.title_input.setMaxLength(TITLE_MAX)
        self.title_input.setPlaceholderText("Title, e.g. Scheduled maintenance on Saturday")
        self.body.addWidget(label("TITLE", "acFieldLabel", wrap=False))
        self.body.addWidget(self.title_input)

        self.message = QPlainTextEdit(item.body)
        self.message.setObjectName("acInput")
        self.message.setPlaceholderText("The message. Plain text; line breaks are kept.")
        self.message.setFixedHeight(150)
        self._count = label("", "acSmall", wrap=False)
        self.message.textChanged.connect(self._update_count)
        head = QHBoxLayout()
        head.addWidget(label("MESSAGE", "acFieldLabel", wrap=False))
        head.addStretch(1)
        head.addWidget(self._count)
        self.body.addLayout(head)
        self.body.addWidget(self.message)
        self._update_count()

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(6)
        grid.addWidget(label("IMPORTANCE", "acFieldLabel", wrap=False), 0, 0)
        self.level = _Chips([(v, t) for v, t, _ in LEVELS], item.level)
        grid.addWidget(self.level, 1, 0)
        grid.addWidget(label("WHO SEES IT", "acFieldLabel", wrap=False), 0, 1)
        self.audience = _Chips(AUDIENCES, item.audience)
        grid.addWidget(self.audience, 1, 1)
        self.body.addLayout(grid)

        self.body.addWidget(label("LINK BUTTON (OPTIONAL)", "acFieldLabel", wrap=False))
        link = QHBoxLayout()
        link.setSpacing(8)
        self.url = QLineEdit(item.link_url)
        self.url.setObjectName("acInput")
        self.url.setPlaceholderText("https://…")
        link.addWidget(self.url, 3)
        self.link_label = QLineEdit(item.link_label)
        self.link_label.setObjectName("acInput")
        self.link_label.setMaxLength(LABEL_MAX)
        self.link_label.setPlaceholderText("Button text (Learn more)")
        link.addWidget(self.link_label, 2)
        self.body.addLayout(link)

        self.body.addWidget(label("SCHEDULE", "acFieldLabel", wrap=False))
        when = QGridLayout()
        when.setHorizontalSpacing(10)
        when.setVerticalSpacing(6)
        when.addWidget(label("Starts", "acValue", wrap=False), 0, 0)
        self.starts = self._date_field(_to_qt(item.starts_at))
        when.addWidget(self.starts, 0, 1)
        self.has_end = QCheckBox("Ends")
        self.has_end.setChecked(item.ends_at is not None)
        when.addWidget(self.has_end, 1, 0)
        default_end = item.ends_at or ((item.starts_at or datetime.now().astimezone())
                                       + timedelta(days=7))
        self.ends = self._date_field(_to_qt(default_end))
        self.ends.setEnabled(self.has_end.isChecked())
        self.has_end.toggled.connect(self.ends.setEnabled)
        when.addWidget(self.ends, 1, 1)
        when.setColumnStretch(2, 1)
        self.body.addLayout(when)
        self.body.addWidget(label("A start in the future schedules it. With no end it stays "
                                  "until you end it.", "acSmall"))

        self.reshow = QCheckBox("Pop up again for people who already closed it")
        self.reshow.setVisible(self._editing)
        self.body.addWidget(self.reshow)

        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Preview", "acGhost", "eye",
                        lambda: self.preview_requested.emit(self.value()))
        self.add_button("Save changes" if self._editing else "Publish", "acPrimary",
                        "check" if self._editing else "megaphone",
                        lambda: self.submitted.emit(self.value(), self.reshow.isChecked()),
                        default=True)

    @staticmethod
    def _date_field(value: QDateTime) -> QDateTimeEdit:
        field = QDateTimeEdit(value)
        field.setObjectName("acInput")
        field.setCalendarPopup(True)
        field.setDisplayFormat(DATE_FORMAT)
        field.setMinimumWidth(220)
        return field

    def _update_count(self) -> None:
        n = len(self.message.toPlainText().strip())
        self._count.setText(f"{n} / {BODY_MAX}")

    def value(self) -> Announcement:
        return Announcement(
            id=self._id, title=self.title_input.text().strip(),
            body=self.message.toPlainText().strip(), level=self.level.value(),
            audience=self.audience.value(), link_url=self.url.text().strip(),
            link_label=self.link_label.text().strip(),
            starts_at=_from_qt(self.starts.dateTime()),
            ends_at=_from_qt(self.ends.dateTime()) if self.has_end.isChecked() else None)


class AnnouncementsAdminView(QWidget):
    refresh_requested = Signal()
    new_requested = Signal()
    edit_requested = Signal(object)        # Announcement
    preview_requested = Signal(object)
    end_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._items: list[Announcement] = []
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        column = QVBoxLayout(page)
        column.setContentsMargins(30, 22, 30, 30)
        column.setSpacing(16)

        header, right = page_header(
            "ADMIN MODULE", "", "Broadcast", "megaphone", Theme.token("BADGE_TEXT"),
            "Announcements",
            "Publish a message to everyone, or only students or educators. It pops up on "
            "their dashboard after signing in, once per account.")
        right.addWidget(button("Refresh", "acGhost", "refresh-cw", self.refresh_requested.emit),
                        0, Qt.AlignmentFlag.AlignTop)
        right.addWidget(button("New announcement", "acPrimary", "plus",
                               self.new_requested.emit), 0, Qt.AlignmentFlag.AlignTop)
        column.addWidget(header)

        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        column.addWidget(self.banner)

        stats = QGridLayout()
        stats.setSpacing(12)
        self._stats = {"live": AdminStat("Live", "good"),
                       "scheduled": AdminStat("Scheduled", "blue"),
                       "over": AdminStat("Ended or expired")}
        for index, tile in enumerate(self._stats.values()):
            stats.addWidget(tile, 0, index)
        column.addLayout(stats)

        self.table = DataTable(COLUMNS, stretch=[TITLE], fixed={ACTIONS: 120})
        column.addWidget(self.table)
        self._empty = label("No announcements yet. Click New announcement to write one.",
                            "adEmpty")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.hide()
        column.addWidget(self._empty)
        column.addStretch(1)
        scroll.setWidget(page)
        outer.addWidget(scroll)

    def show_items(self, items: list[Announcement]) -> None:
        self._items = items
        self._render()

    def _render(self) -> None:
        counts = {"live": 0, "scheduled": 0, "over": 0}
        rows = []
        for item in self._items:
            status = item.status()
            counts["over" if status in ("ended", "expired") else status] += 1
            snippet = " ".join(item.body.split())
            schedule_sub = (f"until {friendly_time(item.ends_at)}" if item.ends_at
                            else "no end date")
            if item.ended_at:
                schedule_sub = f"ended {friendly_time(item.ended_at)}"
            buttons = [IconButton("eye", "Preview",
                                  on_click=lambda i=item: self.preview_requested.emit(i)),
                       IconButton("pencil", "Edit",
                                  on_click=lambda i=item: self.edit_requested.emit(i))]
            if status in ("live", "scheduled"):
                buttons.append(IconButton("x", "End now", Theme.token("DANGER"),
                                          lambda i=item: self.end_requested.emit(i)))
            rows.append([
                title_cell(item.title, snippet[:120]),
                text_cell(AUDIENCE_LABELS[item.audience], subtitle=f"by {item.author}"
                          if item.author else ""),
                pill_cell(LEVEL_LABELS[item.level], LEVEL_TONES[item.level]),
                text_cell(friendly_time(item.starts_at), subtitle=schedule_sub),
                pill_cell(STATUS_LABELS[status], STATUS_TONES[status]),
                text_cell(f"{item.dismiss_count:,}", subtitle="closed it"),
                actions_cell(buttons),
            ])
        for key, tile in self._stats.items():
            tile.set_number(counts[key])
        self.table.set_rows(rows)
        self.table.fit_height()
        self.table.setVisible(bool(rows))
        self._empty.setVisible(not rows)

    def show_error(self, message: str) -> None:
        self.banner.show_message(message, "danger", "Dismiss")

    def show_notice(self, message: str) -> None:
        self.banner.show_message(message, "good", "Dismiss")

    def refresh_theme(self) -> None:
        refresh_icons(self)
        self._render()
