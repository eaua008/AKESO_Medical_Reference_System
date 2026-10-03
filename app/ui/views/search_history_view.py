"""Search History: everything opened from the search box, newest first.

Display only. It emits what the user did; SearchHistoryController does it.
Reuses the Account page's building blocks (#acCard, #acRow, #acTab...), so
it looks like the rest of the workspace without a new stylesheet.
"""

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QButtonGroup, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea,
    QVBoxLayout, QWidget,
)

from app.core import icons, lucide
from app.core.theme import Theme
from app.models.search_history import FILTERS, HistoryEntry
from app.ui.views.account.account_widgets import (
    Banner, Card, button, icon_label, label, refresh_icons, repolish,
)


class HistoryRow(QFrame):
    """One remembered search. Click to open it again; X forgets it."""

    open_requested = Signal(object)        # HistoryEntry
    remove_requested = Signal(object)

    def __init__(self, entry: HistoryEntry) -> None:
        super().__init__()
        self.setObjectName("acRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Open {entry.title}")
        self._entry = entry

        row = QHBoxLayout(self)
        row.setContentsMargins(12, 9, 8, 9)
        row.setSpacing(12)

        self._icon = QLabel()
        self._icon.setObjectName("panel")
        self._icon.setFixedSize(18, 18)
        row.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignVCenter)

        text = QVBoxLayout()
        text.setSpacing(1)
        text.addWidget(label(entry.title, "acRowTitle"))
        parts = [entry.kind_label]
        if entry.subtitle and entry.subtitle.lower() != entry.kind_label.lower():
            parts.append(entry.subtitle)
        if entry.query:
            parts.append(f"searched “{entry.query}”")
        if entry.times > 1:
            parts.append(f"{entry.times} times")
        text.addWidget(label(" · ".join(parts), "acSmall"))
        row.addLayout(text, 1)

        row.addWidget(label(entry.time_text(), "acSmall", wrap=False), 0,
                      Qt.AlignmentFlag.AlignVCenter)

        self._remove = QPushButton()
        self._remove.setObjectName("acLink")
        self._remove.setFixedSize(28, 28)
        self._remove.setCursor(Qt.CursorShape.PointingHandCursor)
        self._remove.setToolTip("Remove from history")
        self._remove.setAccessibleName("Remove from history")
        self._remove.clicked.connect(lambda _c=False: self.remove_requested.emit(self._entry))
        row.addWidget(self._remove, 0, Qt.AlignmentFlag.AlignVCenter)
        self.refresh_icons()

    def refresh_icons(self) -> None:
        image = icons.draw(self._entry.icon or "search", 18, Theme.token("BADGE_TEXT"))
        self._icon.setPixmap(icons.to_pixmap(image))
        self._remove.setIcon(lucide.icon("x", 15, Theme.token("TEXT_MUTED")))
        self._remove.setIconSize(QSize(15, 15))

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.open_requested.emit(self._entry)
        super().mouseReleaseEvent(event)


class SearchHistoryView(QWidget):
    open_requested = Signal(object)        # HistoryEntry
    remove_requested = Signal(object)
    clear_requested = Signal()
    saving_requested = Signal(bool)        # the banner's "Turn on"
    filter_changed = Signal(str, str)      # kind, text

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._kind = "all"
        self._rows: list[HistoryRow] = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        self._page = QVBoxLayout(page)
        self._page.setContentsMargins(30, 22, 30, 30)
        self._page.setSpacing(16)

        self._page.addWidget(self._build_title())
        self.banner = Banner()
        self.banner.action.connect(lambda: self.saving_requested.emit(True))
        self._page.addWidget(self.banner)
        self._page.addWidget(self._build_toolbar())

        self._empty = Card()
        self._empty_icon = icon_label("history", 28, Theme.token("TEXT_MUTED"))
        self._empty_title = label("", "acCardTitle")
        self._empty_text = label("", "acMuted")
        for widget in (self._empty_icon, self._empty_title, self._empty_text):
            self._empty.body.addWidget(widget, 0, Qt.AlignmentFlag.AlignHCenter)
        self._empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._page.addWidget(self._empty)

        self._groups = QVBoxLayout()
        self._groups.setSpacing(16)
        self._page.addLayout(self._groups)
        self._page.addStretch(1)

        scroll.setWidget(page)
        outer.addWidget(scroll)

    # ------------------------------------------------------------- pieces

    def _build_title(self) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        text = QVBoxLayout()
        text.setSpacing(4)
        text.addWidget(label("Search History", "acTitle"))
        text.addWidget(label("What you opened from the search bar. Saved on this computer "
                             "only and never sent to Akeso’s server.", "acSubtitle"))
        row.addLayout(text, 1)
        self.clear_button = button("Clear history", "acDanger", "trash-2",
                                   self.clear_requested.emit)
        row.addWidget(self.clear_button, 0, Qt.AlignmentFlag.AlignTop)
        return holder

    def _build_toolbar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("panel")
        column = QVBoxLayout(bar)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(10)

        self.search = QLineEdit()
        self.search.setObjectName("acInput")
        self.search.setPlaceholderText("Search your history…")
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(
            lambda text: self.filter_changed.emit(self._kind, text))
        column.addWidget(self.search)

        tabs = QWidget()
        tabs.setObjectName("acTabRow")
        tabs.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        row = QHBoxLayout(tabs)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)
        self._tab_group = QButtonGroup(self)
        self._tab_group.setExclusive(True)
        self._tabs: dict[str, QPushButton] = {}
        for key, text in FILTERS:
            tab = QPushButton(text)
            tab.setObjectName("acTab")
            tab.setCheckable(True)
            tab.setCursor(Qt.CursorShape.PointingHandCursor)
            tab.clicked.connect(lambda _c=False, k=key: self._choose_kind(k))
            self._tab_group.addButton(tab)
            self._tabs[key] = tab
            row.addWidget(tab)
        row.addStretch(1)
        self._tabs["all"].setChecked(True)
        column.addWidget(tabs)
        return bar

    def _choose_kind(self, kind: str) -> None:
        self._kind = kind
        self.filter_changed.emit(kind, self.search.text())

    # ---------------------------------------------------------------- api

    def show_entries(self, groups: list[tuple[str, list[HistoryEntry]]],
                     counts: dict[str, int], saving: bool) -> None:
        for key, text in FILTERS:
            n = counts.get(key, 0)
            self._tabs[key].setText(f"{text}  {n}" if n else text)

        if saving:
            self.banner.hide()
        else:
            self.banner.show_message(
                "Search history is off, so new searches aren’t saved. "
                "You can change this in Settings.", "warn", "Turn on")

        while self._groups.count():
            item = self._groups.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._rows = []

        total = counts.get("all", 0)
        self.clear_button.setEnabled(total > 0)
        filtered = self._kind != "all" or bool(self.search.text().strip())
        self._empty.setVisible(not groups)
        if not groups:
            if total and filtered:
                self._empty_title.setText("No matches")
                self._empty_text.setText("Nothing in your history matches this filter.")
            else:
                self._empty_title.setText("No searches yet")
                self._empty_text.setText(
                    "Diseases, symptoms, medicines and first-aid steps you open from the "
                    "search bar (Ctrl+K) will show up here.")
            return

        for day, entries in groups:
            block = QWidget()
            block.setObjectName("panel")
            column = QVBoxLayout(block)
            column.setContentsMargins(0, 0, 0, 0)
            column.setSpacing(6)
            column.addWidget(label(day.upper(), "acFieldLabel"))
            for entry in entries:
                row = HistoryRow(entry)
                row.open_requested.connect(self.open_requested.emit)
                row.remove_requested.connect(self.remove_requested.emit)
                self._rows.append(row)
                column.addWidget(row)
            self._groups.addWidget(block)

    def refresh_theme(self) -> None:
        refresh_icons(self)
        for row in self._rows:
            row.refresh_icons()
        repolish(self)
