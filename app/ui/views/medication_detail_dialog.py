"""View Details: one course, with two tabs.

    Course Information     countdown, regimen, prescriber, stewardship
                           status, clinical notes, "Edit Course Details"
    Intake Log History     logged / on-time / late / adherence tiles,
                           next dose, and every entry with a delete button

The panel only displays and asks. The controller does the saving, then
calls load() with the updated course so the panel redraws in place and the
user stays on the tab they were on.
"""

from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.medication_styles import tone_color
from app.models.medication import (
    ABANDONED,
    ACTIVE,
    COMPLETED,
    INTAKE_DELAYED,
    INTAKE_MISSED,
    STATE_MISSED,
    MedicationCourse,
)
from app.ui.views.medication_dialogs import OverlayDialog

_INTAKE_BADGE = {
    "taken": ("On Time", "success", "check"),
    INTAKE_DELAYED: ("Late Intake", "amber", "clock"),
    INTAKE_MISSED: ("Missed / Skipped", "danger", "x"),
}
_STATE_BADGE = {
    "on_track": ("On Track", "primary"),
    STATE_MISSED: ("Missed Dose Flagged", "amber"),
    COMPLETED: ("Completed", "success"),
    ABANDONED: ("Abandoned", "danger"),
}


class CourseDetailDialog(OverlayDialog):
    log_requested = Signal(str)          # course id
    edit_requested = Signal(str)         # course id
    delete_log_requested = Signal(str, int)   # course id, log id

    def __init__(self, parent: QWidget, course: MedicationCourse) -> None:
        # The base class builds its own title row; this panel has a richer
        # header, so it starts from an empty title and hides that row.
        super().__init__(parent, "", "", width=780)
        self._clear_base_header()
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(0)
        self._tab = 0
        self._course = course

        # Tall content scrolls inside the card, never past the window.
        self.card.setMaximumHeight(max(parent.window().height() - 60, 400))
        self._content = QWidget()
        self._content.setObjectName("panel")
        self.body.addWidget(self._content)
        self.load(course)

    def _clear_base_header(self) -> None:
        while self.body.count():
            item = self.body.takeAt(0)
            if item.widget() is not None:
                item.widget().hide()
            elif item.layout() is not None:
                _hide_layout(item.layout())

    # ------------------------------------------------------------ public

    def load(self, course: MedicationCourse) -> None:
        """(Re)draw everything for this version of the course."""
        self._course = course
        old = self._content
        self._content = QWidget()
        self._content.setObjectName("panel")
        self.body.replaceWidget(old, self._content)
        old.setParent(None)
        old.deleteLater()

        layout = QVBoxLayout(self._content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._header(course))
        layout.addWidget(self._tabs(course))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._stack = QStackedWidget()
        self._stack.setObjectName("panel")
        self._stack.addWidget(self._info_tab(course))
        self._stack.addWidget(self._history_tab(course))
        self._stack.setCurrentIndex(self._tab)
        scroll.setWidget(self._stack)
        # Use the room the window has, so most courses need no scrolling.
        scroll.setMinimumHeight(max(min(560, self.height() - 300), 260))
        layout.addWidget(scroll, 1)
        layout.addWidget(self._footer(course))

    # ----------------------------------------------------------- header

    def _header(self, c: MedicationCourse) -> QWidget:
        box = QWidget()
        box.setObjectName("panel")
        row = QHBoxLayout(box)
        row.setContentsMargins(18, 16, 14, 12)
        row.setSpacing(12)

        tile = QFrame()
        tile.setObjectName("mdIconTileAmber" if c.is_protected else "mdIconTileSoft")
        tile.setFixedSize(38, 38)
        tile_layout = QVBoxLayout(tile)
        tile_layout.setContentsMargins(0, 0, 0, 0)
        icon = QLabel()
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setPixmap(lucide.pixmap("pill", 20, tone_color("amber" if c.is_protected
                                                            else "primary")))
        tile_layout.addWidget(icon)
        row.addWidget(tile, 0, Qt.AlignmentFlag.AlignTop)

        text = QVBoxLayout()
        text.setSpacing(4)
        title = QLabel(c.medicine_name, objectName="mdDialogTitle")
        title.setWordWrap(True)
        text.addWidget(title)
        badges = QHBoxLayout()
        badges.setSpacing(6)
        label, tone = _STATE_BADGE[c.state()]
        badges.addWidget(_badge(label, tone))
        if c.is_protected:
            badges.addWidget(QLabel("FULL-COURSE CRITICAL", objectName="mdChip"))
        badges.addStretch(1)
        text.addLayout(badges)
        meta = QHBoxLayout()
        meta.setSpacing(6)
        if c.dosage_schedule:
            meta.addWidget(QLabel(c.dosage_schedule, objectName="mdSmallMuted"))
        if c.prescriber:
            if c.dosage_schedule:
                meta.addWidget(QLabel("•", objectName="mdSmallMuted"))
            meta.addWidget(_icon("user", 12, "muted"))
            meta.addWidget(QLabel(c.prescriber, objectName="mdSmallMuted"))
        meta.addStretch(1)
        text.addLayout(meta)
        row.addLayout(text, 1)

        if c.status == ACTIVE:
            log = QPushButton(" Log Intake Now")
            log.setObjectName("mdPrimary")
            log.setIcon(lucide.icon("check", 15, "#FFFFFF"))
            log.setCursor(Qt.CursorShape.PointingHandCursor)
            log.clicked.connect(lambda: self.log_requested.emit(c.id))
            row.addWidget(log, 0, Qt.AlignmentFlag.AlignTop)
        close = QPushButton()
        close.setObjectName("mdClose")
        close.setIcon(lucide.icon("x", 16, tone_color("muted")))
        close.setCursor(Qt.CursorShape.PointingHandCursor)
        close.clicked.connect(self.reject)
        row.addWidget(close, 0, Qt.AlignmentFlag.AlignTop)
        return box

    def _tabs(self, c: MedicationCourse) -> QWidget:
        bar = QWidget()
        bar.setObjectName("mdDialogTabRow")
        row = QHBoxLayout(bar)
        row.setContentsMargins(18, 0, 18, 0)
        row.setSpacing(4)
        group = QButtonGroup(bar)
        group.setExclusive(True)
        for index, (text, icon_name) in enumerate((("Course Information", "file-text"),
                                                   ("Intake Log History", "history"))):
            button = QPushButton(" " + text)
            button.setIcon(lucide.icon(icon_name, 14, tone_color("muted")))
            button.setObjectName("mdTab")
            button.setCheckable(True)
            button.setChecked(index == self._tab)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, i=index: self._switch(i))
            group.addButton(button)
            row.addWidget(button)
            if index == 1:
                row.addWidget(_pill(str(len(c.intakes))), 0, Qt.AlignmentFlag.AlignVCenter)
        row.addStretch(1)
        if c.status == ACTIVE:
            edit = QPushButton(" Edit Course Details")
            edit.setObjectName("mdSecondarySmall")
            edit.setIcon(lucide.icon("pencil", 13, tone_color("primary")))
            edit.setCursor(Qt.CursorShape.PointingHandCursor)
            edit.clicked.connect(lambda: self.edit_requested.emit(c.id))
            row.addWidget(edit)
        return bar

    def _switch(self, index: int) -> None:
        self._tab = index
        self._stack.setCurrentIndex(index)

    # ------------------------------------------------------ information

    def _info_tab(self, c: MedicationCourse) -> QWidget:
        page = QWidget()
        page.setObjectName("panel")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        status = _box()
        s = QVBoxLayout(status)
        s.setContentsMargins(16, 14, 16, 14)
        s.setSpacing(8)
        head = QHBoxLayout()
        head.addWidget(_icon("clock", 15, "primary"))
        head.addWidget(QLabel("Course Countdown Status", objectName="mdMetaKey"))
        head.addStretch(1)
        head.addWidget(QLabel(f"<span style='color:{tone_color('primary')}'>{c.remaining}"
                              f"</span> / "
                              f"{c.total_units} {c.unit_label} remaining",
                              objectName="mdRemaining"))
        s.addLayout(head)
        s.addWidget(_progress(c))
        foot = QHBoxLayout()
        foot.addWidget(QLabel(f"{c.percent_complete}% of course completed",
                              objectName="mdSmallMuted"))
        foot.addStretch(1)
        foot.addWidget(_icon("trending-up", 13, "success"))
        foot.addWidget(QLabel(f"Adherence Score: {c.adherence()}%", objectName="mdMetaKey"))
        s.addLayout(foot)
        layout.addWidget(status)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(_tile("pill", "primary", "MEDICINE & STRENGTH", c.medicine_name), 0, 0)
        grid.addWidget(_tile("tag", "primary", "PRESCRIBED UNITS & FORM",
                             f"{c.total_units} {c.unit_label} (Total Count)"), 0, 1)
        grid.addWidget(_tile("clock", "success", "DOSAGE SCHEDULE",
                             c.dosage_schedule or "Not specified"), 1, 0)
        grid.addWidget(_tile("calendar", "primary", "DURATION & TIMELINE",
                             f"{c.duration_days} Days • Started {_date(c.started_on)}"),
                       1, 1)
        grid.addWidget(_tile("user", "amber", "PRESCRIBING CLINICIAN / CLINIC",
                             c.prescriber or "Not specified"), 2, 0, 1, 2)
        layout.addLayout(grid)

        if c.is_protected:
            box = _box()
            b = QVBoxLayout(box)
            b.setContentsMargins(16, 12, 16, 12)
            b.setSpacing(6)
            b.addLayout(_icon_heading("shield-alert", "danger",
                                      "ANTIMICROBIAL STEWARDSHIP PROTECTION STATUS"))
            b.addWidget(_badge("Protected Regimen: Strict Full-Course Completion Enforced",
                               "amber"), 0, Qt.AlignmentFlag.AlignLeft)
            note = QLabel("Premature discontinuation or missed intervals increase the risk "
                          "of resistance or rebound.", objectName="mdSmallMuted")
            note.setWordWrap(True)
            b.addWidget(note)
            layout.addWidget(box)

        if c.status == ABANDONED:
            box = _box()
            b = QVBoxLayout(box)
            b.setContentsMargins(16, 12, 16, 12)
            b.addWidget(QLabel("ABANDONED", objectName="mdTileLabel"))
            b.addWidget(QLabel(f"Stopped on {_date(c.ended_on)}"
                               + (f" — {c.abandon_reason}" if c.abandon_reason else ""),
                               objectName="mdTileValue"))
            layout.addWidget(box)

        notes = _box()
        n = QVBoxLayout(notes)
        n.setContentsMargins(16, 12, 16, 12)
        n.setSpacing(8)
        n.addLayout(_icon_heading("file-text", "primary", "ORIGINAL CLINICAL NOTES"))
        inner = QFrame()
        inner.setObjectName("mdCountdown")
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(12, 10, 12, 10)
        text = QLabel(c.notes or "No clinical notes were added.",
                      objectName="mdBoxBody" if c.notes else "mdSmallMuted")
        text.setWordWrap(True)
        inner_layout.addWidget(text)
        n.addWidget(inner)
        layout.addWidget(notes)
        layout.addStretch(1)
        return page

    # ---------------------------------------------------------- history

    def _history_tab(self, c: MedicationCourse) -> QWidget:
        page = QWidget()
        page.setObjectName("panel")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        tiles = QHBoxLayout()
        tiles.setSpacing(10)
        tiles.addWidget(_stat("TOTAL TAKEN", f"{c.taken}", f" / {c.total_units}", ""))
        tiles.addWidget(_stat("ON-TIME DOSES", str(c.on_time_count), "", "success"))
        tiles.addWidget(_stat("LATE DOSES", str(c.late_count), "", "amber"))
        tiles.addWidget(_stat("COURSE ADHERENCE", f"{c.adherence()}%", "", "primary"))
        layout.addLayout(tiles)

        if c.status == ACTIVE:
            bar = QFrame()
            bar.setObjectName("mdNextDose")
            row = QHBoxLayout(bar)
            row.setContentsMargins(14, 8, 10, 8)
            row.addWidget(_icon("clock", 15, "primary"))
            row.addWidget(QLabel(f"Next Dose: <b>Dose {c.next_dose_number} of "
                                 f"{c.total_units}</b>", objectName="mdBoxBody"))
            row.addStretch(1)
            log = QPushButton(" Log Dose Now")
            log.setObjectName("mdPrimary")
            log.setIcon(lucide.icon("plus", 15, "#FFFFFF"))
            log.setCursor(Qt.CursorShape.PointingHandCursor)
            log.clicked.connect(lambda: self.log_requested.emit(c.id))
            row.addWidget(log)
            layout.addWidget(bar)

        table = QFrame()
        table.setObjectName("mdTable")
        grid = QGridLayout(table)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        for col, text in enumerate(("DOSE #", "DATE & TIME", "INTAKE STATUS",
                                    "PER-DOSE CLINICAL NOTE", "ACTION")):
            head = QLabel(text, objectName="mdTableHead")
            grid.addWidget(head, 0, col)

        # Numbered in the order they were logged; shown newest first.
        numbered = list(enumerate(c.intakes, start=1))
        for row_index, (number, log) in enumerate(reversed(numbered), start=1):
            when = datetime.fromisoformat(log.taken_at)
            units = f" ×{log.units}" if log.units > 1 else ""
            cells = [
                _cell(QLabel(f"Dose {number} of {c.total_units}{units}",
                             objectName="mdDoseChip")),
                _cell(_when(when)),
                _cell(_status_badge(*_INTAKE_BADGE.get(log.status,
                                                       ("Logged", "primary", "check")))),
                _cell(_wrapped(f"“{log.note}”" if log.note else "No per-dose note",
                               "mdNote" if log.note else "mdNoteEmpty")),
            ]
            delete = QPushButton()
            delete.setObjectName("mdIconButton")
            delete.setIcon(lucide.icon("trash-2", 15, tone_color("muted")))
            delete.setCursor(Qt.CursorShape.PointingHandCursor)
            delete.setToolTip("Delete this entry")
            delete.clicked.connect(lambda _c=False, lid=log.id:
                                   self.delete_log_requested.emit(c.id, lid))
            cells.append(_cell(delete))
            for col, cell in enumerate(cells):
                grid.addWidget(cell, row_index, col)
        grid.setColumnStretch(3, 1)
        layout.addWidget(table)

        if not c.intakes:
            empty = QLabel("No doses logged yet.", objectName="mdSmallMuted")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(empty)
        layout.addStretch(1)
        return page

    # ----------------------------------------------------------- footer

    def _footer(self, c: MedicationCourse) -> QWidget:
        bar = QWidget()
        bar.setObjectName("mdDialogFooter")
        row = QHBoxLayout(bar)
        row.setContentsMargins(18, 12, 18, 14)
        registered = _date(c.created_at[:10]) if c.created_at else _date(c.started_on)
        row.addWidget(QLabel(f"Course ID: <code>{c.id[:12]}</code>  •  "
                             f"Registered: {registered}", objectName="mdSmallMuted"))
        row.addStretch(1)
        close = QPushButton("Close Panel")
        close.setObjectName("mdSecondary")
        close.setCursor(Qt.CursorShape.PointingHandCursor)
        close.clicked.connect(self.reject)
        row.addWidget(close)
        return bar


# --------------------------------------------------------------- helpers

def _pill(text: str) -> QLabel:
    """A count badge only as tall as its number."""
    pill = QLabel(text, objectName="mdTabCount")
    pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pill.setFixedHeight(18)
    pill.setMinimumWidth(20)
    return pill


def _wrapped(text: str, name: str) -> QLabel:
    label = QLabel(text, objectName=name)
    label.setWordWrap(True)
    return label


def _hide_layout(layout) -> None:
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item.widget() is not None:
            item.widget().hide()
        elif item.layout() is not None:
            _hide_layout(item.layout())


def _box() -> QFrame:
    frame = QFrame()
    frame.setObjectName("mdPanel")
    return frame


def _icon(name: str, size: int, tone: str) -> QLabel:
    label = QLabel()
    label.setPixmap(lucide.pixmap(name, size, tone_color(tone)))
    label.setFixedSize(size, size)
    return label


def _icon_heading(name: str, tone: str, text: str) -> QHBoxLayout:
    row = QHBoxLayout()
    row.setSpacing(6)
    row.addWidget(_icon(name, 13, tone))
    row.addWidget(QLabel(text, objectName="mdTileLabel"))
    row.addStretch(1)
    return row


def _status_badge(text: str, tone: str, icon_name: str) -> QFrame:
    """A badge with a leading icon (On Time / Late Intake / Missed)."""
    badge = QFrame()
    badge.setObjectName("mdBadgeFrame")
    badge.setProperty("tone", tone)
    row = QHBoxLayout(badge)
    row.setContentsMargins(7, 2, 8, 2)
    row.setSpacing(4)
    row.addWidget(_icon(icon_name, 11, tone))
    label = QLabel(text, objectName="mdBadgeText")
    label.setProperty("tone", tone)
    row.addWidget(label)
    return badge


def _when(moment: datetime) -> QWidget:
    box = QWidget()
    box.setObjectName("panel")
    layout = QVBoxLayout(box)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(2)
    for icon_name, text, name in (("calendar", f"{moment:%b %d, %Y}", "mdSmallBody"),
                                  ("clock", f"{moment:%I:%M %p}", "mdSmallMuted")):
        row = QHBoxLayout()
        row.setSpacing(5)
        row.addWidget(_icon(icon_name, 11, "muted"))
        row.addWidget(QLabel(f"<b>{text}</b>" if name == "mdSmallBody" else text,
                             objectName=name))
        row.addStretch(1)
        layout.addLayout(row)
    return box


def _tile(icon_name: str, tone: str, label: str, value: str) -> QFrame:
    frame = _box()
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(14, 10, 14, 10)
    layout.setSpacing(4)
    layout.addLayout(_icon_heading(icon_name, tone, label))
    text = QLabel(value, objectName="mdTileValue")
    text.setWordWrap(True)
    layout.addWidget(text)
    return frame


def _stat(label: str, value: str, suffix: str, tone: str) -> QFrame:
    frame = QFrame()
    frame.setObjectName("mdStatTile")
    frame.setProperty("tone", tone)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(12, 10, 12, 10)
    layout.setSpacing(2)
    layout.addWidget(QLabel(label, objectName="mdTileLabel"))
    layout.addWidget(QLabel(f"{value}<span style='font-size:11px'>{suffix}</span>",
                            objectName="mdStatTileValue"))
    return frame


def _badge(text: str, tone: str) -> QLabel:
    badge = QLabel(text, objectName="mdBadge")
    badge.setProperty("tone", tone)
    return badge


def _progress(c: MedicationCourse) -> QProgressBar:
    bar = QProgressBar()
    bar.setObjectName("mdProgress")
    bar.setTextVisible(False)
    bar.setRange(0, 100)
    bar.setValue(c.percent_complete)
    bar.setProperty("tone", "danger" if c.status == ABANDONED
                    else "success" if c.status == COMPLETED else "")
    return bar


def _cell(widget: QWidget) -> QFrame:
    """One table cell: fixed padding and the row divider line."""
    frame = QFrame()
    frame.setObjectName("mdTableCell")
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(12, 9, 12, 9)
    layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    return frame


def _date(iso: str) -> str:
    if not iso:
        return ""
    year, month, day = iso[:10].split("-")
    return f"{int(month)}/{int(day)}/{year}"
