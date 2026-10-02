"""The Study Notebook page: three layers in one widget.

    Level 1   NotebookHome          always underneath
    Level 2   SlidePanel (half)     shows the QuickView
    Level 3   SlidePanel (full)     shows the NotebookWorkspace

The panel is the same widget at levels 2 and 3; only its width changes.
Its content is swapped at the right moment so the slide stays smooth:

    half -> full   slide first, then show the workspace (heavy)
    full -> half   show the quick view first (light), then slide
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from app.ui.components.slide_panel import CLOSED, FULL, HALF, SlidePanel
from app.ui.views.notebook_home import NotebookHome
from app.ui.views.notebook_quick_view import QuickView
from app.ui.views.notebook_workspace import NotebookWorkspace


class NotebookPage(QWidget):
    theme_changed = Signal()
    panel_closed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("nbPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.home = NotebookHome()
        layout.addWidget(self.home)

        self.panel = SlidePanel(self)
        self.stack = QStackedWidget()
        self.quick = QuickView()
        self.workspace = NotebookWorkspace()
        self.stack.addWidget(self.quick)
        self.stack.addWidget(self.workspace)
        self.panel.body.addWidget(self.stack)
        self.panel.settled.connect(self._settled)
        self.panel.closed.connect(self.panel_closed.emit)

        escape = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        escape.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        escape.activated.connect(self._escape)

    # --------------------------------------------------------------- layers

    @property
    def level(self) -> str:
        """closed | half | full, where the panel is (or is heading)."""
        return self.panel.target_mode

    def show_half(self) -> None:
        self.stack.setCurrentWidget(self.quick)
        if self.level == FULL:
            self.panel.shrink()
        else:
            self.panel.open_half()

    def show_full(self) -> None:
        if self.level == CLOSED:
            # Straight to the workspace (e.g. New Note): no quick view first.
            self.stack.setCurrentWidget(self.workspace)
        self.panel.expand()

    def close_panel(self) -> None:
        self.panel.close_panel()

    def _settled(self, mode: str) -> None:
        if mode == FULL:
            self.stack.setCurrentWidget(self.workspace)
        elif mode == HALF:
            self.stack.setCurrentWidget(self.quick)

    def _escape(self) -> None:
        if self.level == FULL:
            self.show_half()
        elif self.level == HALF:
            self.close_panel()

    # ---------------------------------------------------------------- theme

    def refresh_theme(self) -> None:
        """Called by the dashboard shell when light/dark mode changes."""
        self.home.refresh_theme()
        self.quick.refresh_theme()
        self.workspace.refresh_theme()     # also emits workspace.theme_changed
        self.theme_changed.emit()
