"""The Study Workspace: the open-items bar and three resizable columns.

    ┌ open items ─ [Item A][Item B][+] ───────────────────────────────┐
    ├ ← Study Notebook / Item A                    [▤][✎][⌕] [Reset] ┤
    │ Case tabs      ┃ Notes tabs            ┃ Reference tabs          │
    │ [Case][+][≡][«]┃ [My notes][+][≡]      ┃ (Folder▾)[Dengue][+][≡][»]
    │                ┃                       ┃                         │
    │   page         ┃   page                ┃   page                  │
    └────────────────┸───────────────────────┸─────────────────────────┘

The view draws and reports; NotebookController owns the state. Pages are
built lazily: a tab's page is only created the first time it is shown,
so a workspace with 30 tabs only builds the ones you actually look at.

Step 4 fills pages with placeholders. Steps 5 to 7 swap in the notes
editor, the reference browser and the case presentation.
"""

from typing import Callable, Optional

from PySide6.QtCore import QRectF, QSize, Qt, Signal
from PySide6.QtGui import QFont, QPainter, QColor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.theme import Theme
from app.models.notebook import COLUMN_TITLES, COLUMNS, ColumnState, Tab, WorkspaceState
from app.ui.components.tab_strip import TabStrip

RAIL_WIDTH = 36
MIN_COLUMN = 240
QWIDGETSIZE_MAX = 16777215

COLUMN_ICONS = {"left": "stethoscope", "center": "notebook-pen", "right": "book-open"}
# The centre column never collapses: it is where you write.
COLLAPSE_ICONS = {"left": "chevrons-left", "right": "chevrons-right"}

PageFactory = Callable[[Tab, str], QWidget]


# ======================================================================
#   Placeholder page (until steps 5 to 7)
# ======================================================================

PLACEHOLDER_TEXT = {
    "case": "The case presentation, vitals, labs and hallmark correlation "
            "will appear here (step 7).",
    "note": "The Word-like notes editor, with tables, arrives in step 5.",
    "search": "Search diseases, symptoms and medicines here (step 6).",
    "disease": "A compact disease monograph arrives in step 6.",
    "symptom": "A compact symptom monograph arrives in step 6.",
    "medicine": "A compact medicine monograph arrives in step 6.",
}


class PlaceholderPage(QWidget):
    def __init__(self, tab: Tab, column: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._tab = tab
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        card = QFrame()
        card.setObjectName("nbPlaceholder")
        body = QVBoxLayout(card)
        body.setContentsMargins(22, 26, 22, 26)
        body.setSpacing(8)
        self._icon = QLabel()
        self._icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.addWidget(self._icon)
        title = QLabel(tab.title, objectName="nbPlaceholderTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setWordWrap(True)
        body.addWidget(title)
        text = QLabel(PLACEHOLDER_TEXT.get(tab.kind, "Coming in a later step."),
                      objectName="nbPlaceholderText")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text.setWordWrap(True)
        body.addWidget(text)
        where = QLabel(f"Tab type: {tab.kind}", objectName="nbPlaceholderText")
        where.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.addWidget(where)
        outer.addWidget(card)
        outer.addStretch(1)
        self.refresh_theme()

    def refresh_theme(self) -> None:
        self._icon.setPixmap(lucide.pixmap(self._tab.icon, 30,
                                           Theme.token("PRIMARY_TEXT_ON_NAV")))


# ======================================================================
#   Collapsed-column rail
# ======================================================================

class ColumnRail(QFrame):
    """The slim bar a collapsed column turns into. Click to expand."""

    clicked = Signal()

    def __init__(self, icon: str) -> None:
        super().__init__()
        self.setObjectName("nbRail")
        self.setFixedWidth(RAIL_WIDTH)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Expand column")
        self._icon = icon
        self._text = ""

    def set_text(self, text: str) -> None:
        self._text = text
        self.update()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        muted = Theme.token("TEXT_MUTED")
        painter.drawPixmap(10, 12, lucide.pixmap(self._icon, 16, muted))
        # Text reads bottom-to-top, turned 90 degrees like a book spine.
        painter.translate(self.width() / 2 + 5, 42)
        painter.rotate(90)
        font = QFont(self.font())
        font.setPointSizeF(8.5)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(muted))
        painter.drawText(QRectF(0, 0, self.height() - 50, 14),
                         Qt.AlignmentFlag.AlignLeft, self._text)
        painter.end()


# ======================================================================
#   One column
# ======================================================================

class WorkspaceColumn(QFrame):
    def __init__(self, name: str, strip: TabStrip, page_factory: PageFactory) -> None:
        super().__init__()
        self.name = name
        self.strip = strip
        self._factory = page_factory
        self._pages: dict[str, QWidget] = {}
        self.setObjectName("nbColumn")

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self.rail = ColumnRail(COLUMN_ICONS[name])
        outer.addWidget(self.rail)

        self.body = QWidget()
        self.body.setObjectName("panel")
        body = QVBoxLayout(self.body)
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body.addWidget(strip)
        self.stack = QStackedWidget()
        self.empty = QLabel(f"No tabs open in {COLUMN_TITLES[name]}. Press + to open one.",
                            objectName="nbEmpty")
        self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty.setWordWrap(True)
        self.stack.addWidget(self.empty)
        body.addWidget(self.stack, 1)
        outer.addWidget(self.body, 1)

    def show_state(self, state: ColumnState) -> None:
        self.setVisible(state.visible)
        self.rail.setVisible(state.collapsed)
        self.body.setVisible(not state.collapsed)
        if state.collapsed:
            self.setMinimumWidth(RAIL_WIDTH)
            self.setMaximumWidth(RAIL_WIDTH)
            count = len(state.tabs)
            self.rail.set_text(f"{COLUMN_TITLES[self.name]} · {count} "
                               f"tab{'s' if count != 1 else ''}")
        else:
            self.setMinimumWidth(MIN_COLUMN)
            self.setMaximumWidth(QWIDGETSIZE_MAX)
        self.strip.show_state(state)

        active = state.active
        if active is None:
            self.stack.setCurrentWidget(self.empty)
            return
        page = self._pages.get(active.id)
        if page is None:
            page = self._factory(active, self.name)
            self._pages[active.id] = page
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)

    def take_page(self, tab_id: str) -> Optional[QWidget]:
        """Hand a page over, e.g. when its tab is dragged to another column,
        so unsaved work in it survives the move."""
        page = self._pages.pop(tab_id, None)
        if page is not None:
            self.stack.removeWidget(page)
        return page

    def put_page(self, tab_id: str, page: QWidget) -> None:
        self._pages[tab_id] = page
        self.stack.addWidget(page)

    def set_factory(self, page_factory: PageFactory) -> None:
        self._factory = page_factory

    def page_for(self, tab_id: str) -> Optional[QWidget]:
        return self._pages.get(tab_id)

    def pages(self) -> dict[str, QWidget]:
        return dict(self._pages)

    def drop_pages(self, tab_ids: set[str]) -> None:
        for tab_id in tab_ids:
            page = self.take_page(tab_id)
            if page is not None:
                page.setParent(None)
                page.deleteLater()

    def refresh_theme(self) -> None:
        self.strip.refresh_theme()
        self.rail.update()
        for page in self._pages.values():
            refresh = getattr(page, "refresh_theme", None)
            if callable(refresh):
                refresh()


# ======================================================================
#   The workspace
# ======================================================================

class NotebookWorkspace(QWidget):
    theme_changed = Signal()
    column_toggled = Signal(str, bool)       # column, visible
    reset_layout_requested = Signal()
    shrink_requested = Signal()              # back to the half panel
    close_requested = Signal()               # back to the notebook list
    sizes_changed = Signal(list)             # pixel widths of the 3 columns

    def __init__(self, page_factory: Optional[PageFactory] = None) -> None:
        super().__init__()
        self.setObjectName("nbPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        factory = page_factory or (lambda tab, column: PlaceholderPage(tab, column))

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # --- open-items bar: the same TabStrip, without folders
        self.item_strip = TabStrip("items", group="items", title="Open items",
                                   allow_folders=False, allow_duplicate=False,
                                   new_tooltip="New notebook item",
                                   object_name="nbItemBar")
        outer.addWidget(self.item_strip)

        # --- workspace bar
        bar = QFrame()
        bar.setObjectName("nbWsBar")
        bar.setFixedHeight(46)
        row = QHBoxLayout(bar)
        row.setContentsMargins(12, 0, 12, 0)
        row.setSpacing(8)
        self._icon_buttons: list[QPushButton] = []
        self.back_button = self._icon_button("minimize-2", "Back to half view (Esc)")
        self.back_button.clicked.connect(self.shrink_requested.emit)
        row.addWidget(self.back_button)
        self.crumb = QLabel("Study Notebook  /", objectName="nbCrumb")
        row.addWidget(self.crumb)
        self.crumb_title = QLabel("", objectName="nbCrumbStrong")
        row.addWidget(self.crumb_title)
        self.saved = QLabel("", objectName="nbSaved")
        row.addSpacing(6)
        row.addWidget(self.saved)
        row.addStretch(1)

        self.toggles: dict[str, QPushButton] = {}
        for column in COLUMNS:
            toggle = QPushButton()
            toggle.setObjectName("nbToggle")
            toggle.setCheckable(True)
            toggle.setFixedSize(30, 28)
            toggle.setCursor(Qt.CursorShape.PointingHandCursor)
            toggle.setToolTip(f"Show or hide the {COLUMN_TITLES[column]} column")
            toggle.setProperty("lucide", COLUMN_ICONS[column])
            toggle.clicked.connect(lambda checked, c=column: self.column_toggled.emit(c, checked))
            self.toggles[column] = toggle
            row.addWidget(toggle)
        reset = QPushButton("Reset layout")
        reset.setObjectName("nbButton")
        reset.setCursor(Qt.CursorShape.PointingHandCursor)
        reset.clicked.connect(self.reset_layout_requested.emit)
        row.addWidget(reset)
        close = self._icon_button("x", "Close to the notebook list")
        close.clicked.connect(self.close_requested.emit)
        row.addWidget(close)

        # --- body: empty state or the three columns
        self.body = QStackedWidget()
        self.no_items = QLabel("No notebook items open. Press + in the bar above to start one.",
                               objectName="nbEmpty")
        self.no_items.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body.addWidget(self.no_items)

        columns_host = QWidget()
        columns_host.setObjectName("panel")
        host = QVBoxLayout(columns_host)
        host.setContentsMargins(0, 0, 0, 0)
        host.setSpacing(0)
        host.addWidget(bar)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setObjectName("nbSplitter")
        self.splitter.setHandleWidth(3)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.splitterMoved.connect(
            lambda _pos, _index: self.sizes_changed.emit(self.splitter.sizes()))
        targets = [(c, COLUMN_TITLES[c]) for c in COLUMNS]
        self.columns: dict[str, WorkspaceColumn] = {}
        for column in COLUMNS:
            strip = TabStrip(column, title=COLUMN_TITLES[column], move_targets=targets,
                             collapse_icon=COLLAPSE_ICONS.get(column, ""),
                             new_tooltip=f"New {COLUMN_TITLES[column].lower()} tab")
            self.columns[column] = WorkspaceColumn(column, strip, factory)
            self.splitter.addWidget(self.columns[column])
        host.addWidget(self.splitter, 1)
        self.body.addWidget(columns_host)
        self._columns_host = columns_host
        outer.addWidget(self.body, 1)
        self.refresh_icons()

    def _icon_button(self, icon: str, tooltip: str) -> QPushButton:
        button = QPushButton()
        button.setObjectName("nbIconButton")
        button.setFixedSize(28, 28)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setToolTip(tooltip)
        button.setProperty("lucide", icon)
        self._icon_buttons.append(button)
        return button

    # ------------------------------------------------------------- drawing

    def show_items(self, items: ColumnState, subject: str = "") -> None:
        self.item_strip.show_state(items)
        self.body.setCurrentWidget(self._columns_host if items.tabs else self.no_items)
        active = items.active
        self.crumb.setText(f"Study Notebook  /  {subject}  /" if subject
                           else "Study Notebook  /")
        self.crumb_title.setText(active.title if active else "")

    def show_saved(self, text: str) -> None:
        self.saved.setText(text)

    def show_workspace(self, workspace: WorkspaceState) -> None:
        for name, column in self.columns.items():
            state = workspace.column(name)
            column.show_state(state)
            self.toggles[name].setChecked(state.visible)
        self.apply_sizes(workspace)

    def apply_sizes(self, workspace: WorkspaceState) -> None:
        """Turn the saved percentages into pixel widths. Collapsed columns
        get the rail width; hidden ones get nothing."""
        total = max(self.splitter.width(), 900)
        states = [workspace.column(c) for c in COLUMNS]
        fixed = sum(RAIL_WIDTH for s in states if s.visible and s.collapsed)
        flexible = [(i, workspace.sizes[i]) for i, s in enumerate(states)
                    if s.visible and not s.collapsed]
        weight = sum(p for _i, p in flexible) or 1
        sizes = [0, 0, 0]
        for i, s in enumerate(states):
            if s.visible and s.collapsed:
                sizes[i] = RAIL_WIDTH
        for i, pct in flexible:
            sizes[i] = int((total - fixed) * pct / weight)
        self.splitter.setSizes(sizes)

    def set_page_factory(self, page_factory: PageFactory) -> None:
        """Steps 5 to 7 plug the real pages in here (notes, reference, case)."""
        for column in self.columns.values():
            column.set_factory(page_factory)

    def page_owner(self, column: str) -> WorkspaceColumn:
        return self.columns[column]

    # --------------------------------------------------------------- theme

    def refresh_icons(self) -> None:
        muted = Theme.token("TEXT_MUTED")
        accent = Theme.token("PRIMARY_TEXT_ON_NAV")
        for button in self._icon_buttons:
            button.setIcon(lucide.icon(button.property("lucide"), 16, muted))
        for toggle in self.toggles.values():
            toggle.setIcon(lucide.icon(toggle.property("lucide"), 15, accent))
            toggle.setIconSize(QSize(15, 15))

    def refresh_theme(self) -> None:
        """Called by the dashboard shell when light/dark mode changes."""
        self.refresh_icons()
        self.item_strip.refresh_theme()
        for column in self.columns.values():
            column.refresh_theme()
        self.theme_changed.emit()
