"""Bookmarks: everything the signed-in user has starred.

Display only. It emits which entry was opened and which was unstarred; the
controller does the work.

Cards reuse the encyclopedia object names (#conditionCard, #systemChip and
friends), so this page inherits the same look without a fourth stylesheet.
"""

from typing import Optional

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.models.bookmark import KIND_LABELS, KIND_ORDER, BookmarkEntry

CARD_MIN_WIDTH = 360
MAX_COLUMNS = 3


def _label(text: str, name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(name)
    label.setWordWrap(wrap)
    return label


def _shorten(text: str, limit: int = 150) -> str:
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "\u2026"


class BookmarkCard(QFrame):
    """One starred entry. The star removes it; the rest of the card opens it."""

    open_requested = Signal(str, str)     # entity_type, entity_id
    remove_requested = Signal(str, str)

    def __init__(self, entry: BookmarkEntry) -> None:
        super().__init__()
        self.setObjectName("conditionCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._entry = entry

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 14)
        layout.setSpacing(8)

        top = QHBoxLayout()
        top.addWidget(_label(entry.kind_label.upper(), "systemChip", wrap=False))
        top.addStretch(1)

        self._star = QPushButton()
        self._star.setObjectName("bookmarkButton")
        self._star.setFixedSize(26, 26)
        self._star.setCursor(Qt.CursorShape.PointingHandCursor)
        self._star.setToolTip("Remove from bookmarks")
        # Everything on this page is saved by definition, so the star is
        # always solid; pressing it removes the bookmark.
        self._star.setIcon(QIcon(icons.to_pixmap(
            icons.star_filled(15, Theme.token("PRIMARY")))))
        self._star.setIconSize(QSize(15, 15))
        self._star.clicked.connect(
            lambda: self.remove_requested.emit(entry.entity_type, entry.entity_id))
        top.addWidget(self._star)
        layout.addLayout(top)

        layout.addWidget(_label(entry.title, "cardConditionName"))
        if entry.subtitle:
            layout.addWidget(_label(entry.subtitle, "cardScientificName"))
        if entry.description:
            layout.addWidget(_label(_shorten(entry.description), "cardDescription"))
        layout.addStretch(1)

        line = QFrame()
        line.setObjectName("separator")
        line.setFixedHeight(1)
        layout.addWidget(line)

        footer = QHBoxLayout()
        footer.addWidget(_label(entry.meta, "cardDescription", wrap=False))
        footer.addStretch(1)
        if not entry.missing:
            footer.addWidget(_label("Open entry  \u203a", "inspectLink", wrap=False))
        layout.addLayout(footer)

    def mouseReleaseEvent(self, event) -> None:
        # A missing entry has nothing to open; only its star still works.
        if (event.button() == Qt.MouseButton.LeftButton
                and not self._entry.missing
                and self.rect().contains(event.position().toPoint())):
            self.open_requested.emit(self._entry.entity_type, self._entry.entity_id)
        super().mouseReleaseEvent(event)


class BookmarksView(QWidget):
    open_requested = Signal(str, str)
    remove_requested = Signal(str, str)
    kind_changed = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._cards: list[QWidget] = []
        self._columns = 0

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        page = QWidget()
        page.setObjectName("panel")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 22, 30, 30)
        layout.setSpacing(16)

        layout.addWidget(self._build_header())
        layout.addWidget(self._build_tabs())

        self._empty = _label("", "syStatus")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.hide()
        layout.addWidget(self._empty)

        self._grid_host = QWidget()
        self._grid_host.setObjectName("panel")
        self._grid = QGridLayout(self._grid_host)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setSpacing(16)
        layout.addWidget(self._grid_host)
        layout.addStretch(1)

        scroll.setWidget(page)
        root.addWidget(scroll)

    # ----------------------------------------------------------- builders

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("panel")
        row = QHBoxLayout(header)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        self._icon = QLabel()
        self._icon.setObjectName("panel")
        self._icon.setFixedSize(26, 26)
        row.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignTop)

        text = QVBoxLayout()
        text.setSpacing(4)
        text.addWidget(_label("Bookmarks", "pageTitle", wrap=False))
        text.addWidget(_label(
            "Conditions, symptoms and medicines you have starred, kept on "
            "this device for your account.", "pageSubtitle"))
        row.addLayout(text, 1)

        self.count_badge = _label("", "countBadge", wrap=False)
        row.addWidget(self.count_badge, 0, Qt.AlignmentFlag.AlignTop)
        self.refresh_theme()
        return header

    def _build_tabs(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("mdToggle")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        self._tab_group = QButtonGroup(self)
        self._tab_group.setExclusive(True)
        self._tabs: dict[str, QPushButton] = {}
        for kind in ("", *KIND_ORDER):
            button = QPushButton("All" if not kind else KIND_LABELS[kind] + "s")
            button.setObjectName("mdToggleButton")
            button.setCheckable(True)
            button.setChecked(kind == "")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, k=kind: self.kind_changed.emit(k))
            self._tab_group.addButton(button)
            self._tabs[kind] = button
            layout.addWidget(button)
        layout.addStretch(1)
        return bar

    # ---------------------------------------------------------- public API

    def set_counts(self, counts: dict[str, int]) -> None:
        total = sum(counts.values())
        self.count_badge.setText(f"{total} saved" if total != 1 else "1 saved")
        self._tabs[""].setText(f"All ({total})")
        for kind in KIND_ORDER:
            self._tabs[kind].setText(f"{KIND_LABELS[kind]}s ({counts.get(kind, 0)})")

    def show_entries(self, entries: list[BookmarkEntry], kind: str = "") -> None:
        self._clear()
        for entry in entries:
            card = BookmarkCard(entry)
            card.open_requested.connect(self.open_requested.emit)
            card.remove_requested.connect(self.remove_requested.emit)
            self._cards.append(card)
        self._columns = 0
        self._relayout()

        self._grid_host.setVisible(bool(entries))
        self._empty.setVisible(not entries)
        if not entries:
            what = "entries" if not kind else KIND_LABELS[kind].lower() + "s"
            self._empty.setText(
                f"No {what} bookmarked yet.\n"
                "Open an entry and press the star to save it here.")

    def refresh_theme(self) -> None:
        self._icon.setPixmap(icons.to_pixmap(icons.draw("star", 26, Theme.token("PRIMARY"))))

    # ------------------------------------------------------------ layout

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._relayout()

    def _relayout(self) -> None:
        # Measure the page, not the grid host: the host has no width until
        # after the first layout pass, which would pin the grid to one column.
        available = max(self.width() - 60, 0)
        columns = max(1, min(MAX_COLUMNS, available // CARD_MIN_WIDTH))
        if columns == self._columns:
            return
        self._columns = columns
        for card in self._cards:
            self._grid.removeWidget(card)
        for index, card in enumerate(self._cards):
            row, column = divmod(index, columns)
            self._grid.addWidget(card, row, column)
            card.show()
        for column in range(MAX_COLUMNS):
            self._grid.setColumnStretch(column, 1 if column < columns else 0)

    def _clear(self) -> None:
        for card in self._cards:
            self._grid.removeWidget(card)
            card.hide()
            card.deleteLater()
        self._cards.clear()