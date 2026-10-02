"""Building blocks shared by User Management and Content Management."""

from typing import Callable, Optional

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView, QFrame, QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QTableWidget, QVBoxLayout, QWidget,
)

from app.core import lucide
from app.core.theme import Theme
from app.ui.components.fluid import ElidedLabel
from app.ui.views.account.account_widgets import icon_label, label, repolish

ROW_HEIGHT = 58


def tone_label(text: str, name: str, tone: str = "", wrap: bool = False) -> QLabel:
    widget = label(text, name, wrap=wrap)
    if tone:
        widget.setProperty("tone", tone)
    return widget


def page_header(badge: str, badge_tone: str, crumb: str, icon: str, icon_colour: str,
                title: str, description: str) -> tuple[QWidget, QHBoxLayout]:
    """The ADMIN MODULE header. Returns (widget, right_side_layout)."""
    holder = QWidget()
    holder.setObjectName("panel")
    column = QVBoxLayout(holder)
    column.setContentsMargins(0, 0, 0, 0)
    column.setSpacing(6)
    row = QHBoxLayout()
    text = QVBoxLayout()
    text.setSpacing(6)
    crumbs = QHBoxLayout()
    crumbs.setSpacing(8)
    crumbs.addWidget(tone_label(badge, "adModuleBadge", badge_tone))
    crumbs.addWidget(label("•  " + crumb, "adCrumb", wrap=False))
    crumbs.addStretch(1)
    text.addLayout(crumbs)
    title_row = QHBoxLayout()
    title_row.setSpacing(10)
    title_row.addWidget(icon_label(icon, 30, icon_colour))
    title_row.addWidget(label(title, "adTitle", wrap=False))
    title_row.addStretch(1)
    text.addLayout(title_row)
    text.addWidget(label(description, "adDesc"))
    row.addLayout(text, 1)
    right = QHBoxLayout()
    right.setSpacing(8)
    row.addLayout(right, 0)
    column.addLayout(row)
    rule = QFrame()
    rule.setObjectName("adRule")
    rule.setFixedHeight(1)
    column.addSpacing(8)
    column.addWidget(rule)
    return holder, right


class AdminStat(QFrame):
    def __init__(self, caption: str, tone: str = "") -> None:
        super().__init__()
        self.setObjectName("adStat")
        column = QVBoxLayout(self)
        column.setContentsMargins(14, 12, 14, 12)
        column.setSpacing(6)
        column.addWidget(tone_label(caption.upper(), "adStatCaption", tone))
        self.number = tone_label("0", "adStatNumber", tone)
        column.addWidget(self.number)

    def set_number(self, value: int) -> None:
        self.number.setText(f"{value:,}")


class IconButton(QPushButton):
    """A small borderless icon button for a table row's actions."""

    def __init__(self, icon: str, tooltip: str, colour: str = "",
                 on_click: Optional[Callable[[], None]] = None) -> None:
        super().__init__()
        self.setObjectName("adIconButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setAccessibleName(tooltip)
        self.setFixedSize(28, 28)
        self._icon, self._colour = icon, colour
        self.refresh_icon()
        if on_click is not None:
            self.clicked.connect(lambda _c=False: on_click())

    def refresh_icon(self) -> None:
        self.setIcon(lucide.icon(self._icon, 15, self._colour or Theme.token("TEXT_MUTED")))
        self.setIconSize(QSize(15, 15))


def _cell(margins=(12, 0, 12, 0)) -> tuple[QWidget, QVBoxLayout]:
    holder = QWidget()
    holder.setObjectName("adCell")
    column = QVBoxLayout(holder)
    column.setContentsMargins(*margins)
    column.setSpacing(2)
    column.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    return holder, column


def title_cell(title: str, subtitle: str = "", name: str = "adCellTitle") -> QWidget:
    """Name and subtitle; both shorten with "…" in a narrow column."""
    holder, column = _cell()
    column.addWidget(ElidedLabel(title, name, min_chars=8))
    if subtitle:
        column.addWidget(ElidedLabel(subtitle, "adCellSub", min_chars=6))
    holder.setToolTip(f"{title}\n{subtitle}" if subtitle else title)
    return holder


def text_cell(text: str, name: str = "adCellText", subtitle: str = "") -> QWidget:
    holder, column = _cell()
    column.addWidget(label(text, name, wrap=False))
    if subtitle:
        column.addWidget(label(subtitle, "adCellMuted", wrap=False))
    return holder


def pill_cell(text: str, tone: str = "", caption: str = "", name: str = "adPill") -> QWidget:
    holder, column = _cell()
    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    row.addWidget(tone_label(text, name, tone))
    row.addStretch(1)
    column.addLayout(row)
    if caption:
        column.addWidget(label(caption, "adSubCaption", wrap=False))
    return holder


def pills_cell(items: list[tuple[str, str]]) -> QWidget:
    holder, column = _cell()
    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(6)
    for text, tone in items:
        row.addWidget(tone_label(text, "adPill", tone))
    row.addStretch(1)
    column.addLayout(row)
    return holder


def avatar_cell(initial: str, title: str, subtitle: str) -> QWidget:
    holder = QWidget()
    holder.setObjectName("adCell")
    row = QHBoxLayout(holder)
    row.setContentsMargins(12, 0, 12, 0)
    row.setSpacing(10)
    avatar = QLabel(initial)
    avatar.setObjectName("adAvatar")
    avatar.setFixedSize(30, 30)
    avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
    row.addWidget(avatar)
    text = QVBoxLayout()
    text.setSpacing(1)
    text.addWidget(label(title, "adCellTitle", wrap=False))
    text.addWidget(label(subtitle, "adSubCaption", wrap=False))
    row.addLayout(text, 1)
    return holder


def actions_cell(buttons: list[QPushButton]) -> QWidget:
    holder = QWidget()
    holder.setObjectName("adCell")
    row = QHBoxLayout(holder)
    row.setContentsMargins(6, 0, 12, 0)
    row.setSpacing(4)
    row.addStretch(1)
    for widget in buttons:
        row.addWidget(widget)
    return holder


class DataTable(QTableWidget):
    """A read-only table whose cells are widgets (names with subtitles,
    pills, action buttons). Clicking a sortable header asks the page to
    re-sort its data (header_clicked); the table only shows what it gets."""

    header_clicked = Signal(int)

    def __init__(self, headers: list[str], stretch: list[int], fixed: dict[int, int],
                 sortable: tuple[int, ...] = ()) -> None:
        super().__init__(0, len(headers))
        self.setObjectName("adTable")
        self._headers = headers
        self._sortable = sortable
        self.setHorizontalHeaderLabels([h.upper() for h in headers])
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalHeader().setDefaultSectionSize(ROW_HEIGHT)
        header = self.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setHighlightSections(False)
        for column in range(len(headers)):
            if column in stretch:
                header.setSectionResizeMode(column, QHeaderView.ResizeMode.Stretch)
            elif column in fixed:
                header.setSectionResizeMode(column, QHeaderView.ResizeMode.Fixed)
                self.setColumnWidth(column, fixed[column])
            else:
                header.setSectionResizeMode(column, QHeaderView.ResizeMode.Interactive)
        header.setSectionsClickable(bool(sortable))
        header.sectionClicked.connect(self._on_header)
        self._sort: tuple[int, bool] = (-1, True)

    def _on_header(self, column: int) -> None:
        if column in self._sortable:
            self.header_clicked.emit(column)

    def show_sort(self, column: int, ascending: bool) -> None:
        """Arrows in the header text (the cells are widgets, so Qt's own
        sort indicator does not apply)."""
        self._sort = (column, ascending)
        for index, text in enumerate(self._headers):
            mark = ""
            if index in self._sortable:
                mark = ("  ↑" if ascending else "  ↓") if index == column else "  ⇅"
            self.horizontalHeaderItem(index).setText(text.upper() + mark)

    def set_rows(self, rows: list[list[QWidget]]) -> None:
        self.setUpdatesEnabled(False)
        self.clearContents()
        self.setRowCount(len(rows))
        for r, cells in enumerate(rows):
            for c, widget in enumerate(cells):
                self.setCellWidget(r, c, widget)
        self._fit_columns(rows)
        self.setUpdatesEnabled(True)

    def _fit_columns(self, rows: list[list[QWidget]]) -> None:
        """Size the content-width columns to their widest cell. (Qt's
        ResizeToContents measures text items, not cell widgets, which cut
        pills like "Published" short.)"""
        header = self.horizontalHeader()
        metrics = header.fontMetrics()
        for column in range(self.columnCount()):
            if header.sectionResizeMode(column) != QHeaderView.ResizeMode.Interactive:
                continue
            title = self.horizontalHeaderItem(column).text()
            width = metrics.horizontalAdvance(title) + 34
            for cells in rows:
                if column < len(cells):
                    cell = cells[column]
                    for child in cell.findChildren(QWidget):
                        child.ensurePolished()      # styled padding counts in the width
                    cell.ensurePolished()
                    cell.layout().invalidate()
                    width = max(width, cell.sizeHint().width() + 8)
            self.setColumnWidth(column, width)

    def fit_height(self) -> None:
        """Grow to show every row, so the page scrolls instead of the table."""
        height = self.horizontalHeader().height() + 2
        height += sum(self.rowHeight(r) for r in range(self.rowCount()))
        self.setFixedHeight(max(height, self.horizontalHeader().height() + ROW_HEIGHT))


def repolish_all(widget: QWidget) -> None:
    repolish(widget)
    for child in widget.findChildren(QWidget):
        repolish(child)
