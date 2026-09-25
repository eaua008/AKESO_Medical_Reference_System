"""The suggestion dropdown under the header search box.

A child widget overlaid on the window, NOT a separate popup window. A real
popup window (Qt.Popup) grabs keyboard focus when it opens, so typing the
next character would go to the popup instead of the search box — you could
only ever type one letter. As a child widget with no focus of its own, the
search field keeps the keyboard the whole time and this just follows along.

Display only: it shows results it is handed and announces which was chosen.
"""

from typing import Optional

from PySide6.QtCore import QPoint, QSize, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.services.search_service import SearchResult

ROW_HEIGHT = 50
MAX_VISIBLE_ROWS = 8

_KIND_LABEL = {"module": "Module", "disease": "Condition"}


class _ResultRow(QWidget):
    """Icon, title, subtitle, and a kind chip."""

    def __init__(self, result: SearchResult) -> None:
        super().__init__()
        self.setObjectName("panel")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(11)

        glyph = QLabel()
        glyph.setObjectName("searchRowIcon")
        glyph.setFixedSize(30, 30)
        glyph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        glyph.setPixmap(
            icons.to_pixmap(
                icons.draw(result.icon, 15, Theme.token("BADGE_TEXT"))
            )
        )

        text = QVBoxLayout()
        text.setSpacing(1)
        title = QLabel(result.title)
        title.setObjectName("searchRowTitle")
        subtitle = QLabel(result.subtitle)
        subtitle.setObjectName("searchRowSub")
        text.addWidget(title)
        text.addWidget(subtitle)

        chip = QLabel(_KIND_LABEL.get(result.kind, result.kind.title()))
        chip.setObjectName(
            "searchKindModule" if result.kind == "module" else "searchKindDisease"
        )

        layout.addWidget(glyph)
        layout.addLayout(text, 1)
        layout.addWidget(chip)


class SearchPopup(QFrame):
    """Relevance-ranked suggestions, driven entirely from the search field."""

    chosen = Signal(object)  # the SearchResult picked

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("searchPopup")
        self._results: list[SearchResult] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(0)

        self._list = QListWidget()
        self._list.setObjectName("searchList")
        # No focus, so clicking a suggestion never pulls the keyboard away
        # from the search field.
        self._list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._list.itemClicked.connect(self._on_clicked)
        layout.addWidget(self._list)

        self.hide()

    # ---------------------------------------------------------- public api

    def set_results(self, results: list[SearchResult], query: str) -> None:
        self._results = results
        self._list.clear()

        if not results:
            item = QListWidgetItem(f"No matches for \u201c{query}\u201d")
            # Not selectable: Enter on an empty list must not "choose" this.
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            item.setSizeHint(QSize(0, 40))
            self._list.addItem(item)
        else:
            for result in results:
                item = QListWidgetItem()
                item.setSizeHint(QSize(0, ROW_HEIGHT))
                self._list.addItem(item)
                self._list.setItemWidget(item, _ResultRow(result))
            self._list.setCurrentRow(0)

        rows = max(1, min(len(results), MAX_VISIBLE_ROWS))
        height = (ROW_HEIGHT if results else 40) * rows
        self._list.setFixedHeight(height + 4)
        self.adjustSize()

    def show_under(self, anchor: QWidget) -> None:
        """Position just below the anchor and bring to the front."""
        window = self.parentWidget()
        if window is None:
            return
        position = anchor.mapTo(window, QPoint(0, anchor.height() + 6))
        self.setFixedWidth(anchor.width())
        self.move(position)
        self.show()
        # Raised above page content, which is laid out later and would
        # otherwise paint over this.
        self.raise_()

    def move_selection(self, delta: int) -> None:
        if not self._results:
            return
        row = self._list.currentRow() + delta
        row = max(0, min(row, len(self._results) - 1))
        self._list.setCurrentRow(row)

    def current(self) -> Optional[SearchResult]:
        row = self._list.currentRow()
        if 0 <= row < len(self._results):
            return self._results[row]
        return None

    def first(self) -> Optional[SearchResult]:
        return self._results[0] if self._results else None

    # ------------------------------------------------------------ internal

    def _on_clicked(self, item: QListWidgetItem) -> None:
        row = self._list.row(item)
        if 0 <= row < len(self._results):
            self.chosen.emit(self._results[row])