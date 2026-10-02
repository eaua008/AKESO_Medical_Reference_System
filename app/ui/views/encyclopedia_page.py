"""Container for the encyclopedia tab.

Owns the page header and the Directory / Compare toggle, and holds the three
screens behind this one nav item: the condition grid, the differential
comparison, and the detail monograph.

It exists so the shell does not need to know that one nav tab has three
screens behind it. From the shell's side, "diseases" is a single widget.

The detail page is reached from the grid rather than the toggle, so opening a
monograph hides the tab bar — the toggle is for the two browse modes, and
showing it on a detail page would suggest the tabs switch between views of
the same monograph.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.components.fluid import contain
from app.ui.views.compare_view import CompareView
from app.ui.views.disease_detail_view import DiseaseDetailView
from app.ui.views.disease_encyclopedia_view import DiseaseEncyclopediaView

GRID_INDEX = 0
COMPARE_INDEX = 1
DETAIL_INDEX = 2


class EncyclopediaPage(QWidget):
    """Header, mode toggle, and the three encyclopedia screens."""

    mode_changed = Signal(int)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self._root = root
        self._header_in_grid = False

        # Views first: the header's toggle talks to grid_view, and the mode
        # handler asks the stack which screen is showing.
        self.grid_view = DiseaseEncyclopediaView()
        self.compare_view = CompareView()
        self.detail_view = DiseaseDetailView()

        self._stack = QStackedWidget()
        self._stack.addWidget(self.grid_view)
        self._stack.addWidget(self.compare_view)
        self._stack.addWidget(self.detail_view)

        self._header = self._build_header()
        # The long title and subtitle wrap on narrow windows instead of
        # forcing the window wider than the screen.
        contain(self._header, buttons=False)
        root.addWidget(self._header)
        root.addWidget(self._stack, 1)

        self._sheet = None
        self.show_grid()

    def attach_sheet(self, sheet) -> None:
        """The shell's slide-in sheet (app/ui/components/page_sheet.py):
        monographs open in it, over the directory, instead of replacing it."""
        self._sheet = sheet
        self._stack.removeWidget(self.detail_view)
        sheet.adopt(self.detail_view, self.detail_view.back_requested)

    # -------------------------------------------------------------- header

    def _build_header(self) -> QWidget:
        holder = QFrame()
        holder.setObjectName("pageHeader")

        layout = QVBoxLayout(holder)
        layout.setContentsMargins(30, 22, 30, 0)
        layout.setSpacing(14)

        title_row = QHBoxLayout()
        text_col = QVBoxLayout()
        text_col.setSpacing(4)

        title = QLabel("Disease & Medical Condition Encyclopedia")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Browse peer-reviewed clinical summaries, pathophysiology, "
            "differential diagnoses, treatments, and prevention tiers"
        )
        subtitle.setObjectName("pageSubtitle")

        text_col.addWidget(title)
        text_col.addWidget(subtitle)

        self._count_badge = QLabel("0 conditions indexed")
        self._count_badge.setObjectName("countBadge")

        title_row.addLayout(text_col)
        title_row.addStretch(1)
        title_row.addWidget(self._build_view_toggle(), 0, Qt.AlignmentFlag.AlignTop)
        title_row.addWidget(self._count_badge, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(title_row)

        layout.addWidget(self._build_scope_note())
        layout.addWidget(self._build_tab_bar())
        return holder

    def _build_view_toggle(self) -> QWidget:
        """Cards vs the numbered 8-part entry list, as in the other modules.

        Object names are borrowed from the medicine stylesheet so the three
        directories look identical without a fourth copy of the same rules.
        """
        toggle = QFrame()
        toggle.setObjectName("mdToggle")
        layout = QHBoxLayout(toggle)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        self._view_group = QButtonGroup(self)
        self._view_group.setExclusive(True)
        for label, is_cards in (("Cards", True), ("8-Part Entries", False)):
            button = QPushButton(label)
            button.setObjectName("mdToggleButton")
            button.setCheckable(True)
            button.setChecked(is_cards)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda _c=False, cards=is_cards: self._on_display_mode(cards)
            )
            self._view_group.addButton(button)
            layout.addWidget(button)
        return toggle

    def _on_display_mode(self, cards: bool) -> None:
        self.grid_view.set_display_mode(cards)
        # A mode switch only makes sense on the directory.
        if self._stack.currentIndex() != GRID_INDEX:
            self.show_grid()

    @staticmethod
    def _build_scope_note() -> QWidget:
        box = QFrame()
        box.setObjectName("syScopeNote")
        layout = QHBoxLayout(box)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)

        title = QLabel("Clinical Scope Note:")
        title.setObjectName("syScopeTitle")
        body = QLabel(
            "An educational reference. Entries follow WHO, CDC and standard "
            "textbook clinical documentation and do not replace professional "
            "medical evaluation."
        )
        body.setObjectName("syScopeText")
        body.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(body, 1)
        return box

    def _build_tab_bar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("panel")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(22)

        self._directory_tab = QPushButton("  Condition Directory")
        self._compare_tab = QPushButton("  Compare Conditions (Differential Analysis)")

        for index, button in enumerate((self._directory_tab, self._compare_tab)):
            button.setObjectName("pageTab")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFixedHeight(38)
            button.clicked.connect(
                lambda _=False, i=index: self._on_tab_clicked(i)
            )
            layout.addWidget(button)

        layout.addStretch(1)
        self._directory_tab.setChecked(True)

        underline = QFrame()
        underline.setObjectName("separator")
        underline.setFixedHeight(1)

        holder = QWidget()
        holder.setObjectName("panel")
        holder_layout = QVBoxLayout(holder)
        holder_layout.setContentsMargins(0, 0, 0, 0)
        holder_layout.setSpacing(0)
        holder_layout.addWidget(bar)
        holder_layout.addWidget(underline)
        return holder

    def _on_tab_clicked(self, index: int) -> None:
        if index == GRID_INDEX:
            self.show_grid()
        else:
            self.show_compare()
        self.mode_changed.emit(index)

    # ---------------------------------------------------------------- modes

    def _set_tabs(self, active: Optional[int]) -> None:
        self._directory_tab.setChecked(active == GRID_INDEX)
        self._compare_tab.setChecked(active == COMPARE_INDEX)

    def _place_header(self, in_grid: bool) -> None:
        """On the directory the header lives INSIDE the grid's scroll area,
        so it scrolls away with the cards (like the Symptom and Medicine
        pages); elsewhere it sits above the view as before."""
        if in_grid == self._header_in_grid:
            return
        margins = self._header.layout()
        if in_grid:
            self._root.removeWidget(self._header)
            margins.setContentsMargins(0, 4, 0, 0)     # the grid page has its own
            self.grid_view.set_page_header(self._header)
        else:
            self.grid_view.take_page_header(self._header)
            margins.setContentsMargins(30, 22, 30, 0)
            self._root.insertWidget(0, self._header)
        self._header_in_grid = in_grid

    def show_grid(self) -> None:
        self._close_sheet()
        self._stack.setCurrentIndex(GRID_INDEX)
        self._place_header(True)
        self._header.show()
        self._set_tabs(GRID_INDEX)

    def show_compare(self) -> None:
        self._close_sheet()
        self._stack.setCurrentIndex(COMPARE_INDEX)
        self._place_header(False)
        self._header.show()
        self._set_tabs(COMPARE_INDEX)

    def _close_sheet(self) -> None:
        if self._sheet is not None:
            self._sheet.close_sheet()

    def close_detail(self) -> None:
        """Back / X / Esc on a monograph: back to whichever screen opened it."""
        if self._sheet is not None:
            self._sheet.close_sheet()
        else:
            self.show_grid()

    def show_detail(self) -> None:
        if self._sheet is not None:
            # Slides in over the directory (or the comparison) it came from,
            # which is still there when the sheet closes.
            self._sheet.open_sheet()
            return
        self._stack.setCurrentIndex(DETAIL_INDEX)
        # The monograph carries its own top bar with a back button; keeping
        # the browse header above it would stack two navigation rows.
        self._header.hide()

    def set_count(self, shown: int, total: int) -> None:
        self._count_badge.setText(f"{shown} of {total} conditions indexed")