"""PageSheet: a full-page panel that slides in from the right.

It covers the content area (everything right of the sidebar) and leaves
the header and the sidebar where they are. A square close tab sticks out of
its left edge and overlaps the sidebar, so it is always easy to find:

    +--------+------------------------------------------+
    | header                                            |
    +--------+--+---------------------------------------+
    | side  [X] |  sheet content                        |
    | bar    |  |                                       |
    +--------+------------------------------------------+

The sheet does not decide whether it may close. The X tab and Escape emit
close_requested; the owner checks for unsaved work and then calls
close_sheet(). Content goes in with set_content().

    opened()            the slide-in has finished
    closed()            the slide-out has finished (content is removed)
    close_requested()   the user pressed X or Escape

suspend() / resume() hide and restore the sheet instantly, keeping its
content, for when the user switches to another tab and comes back. The
shell does this for every sheet (DashboardShell.add_sheet).

Two kinds of content:
    keep_content=False   a form made for one use (the Exchange composer):
                         deleted when the sheet closes
    keep_content=True    a page that stays (a disease monograph): only
                         hidden, and shown again on the next open

adopt(widget, back_signal) turns a page's detail screen into a sheet in
one call: the screen moves into the sheet, its own Back button is hidden,
and X / Esc go through back_signal, so the controller's existing "back"
path runs and nothing else has to change.
"""

import itertools

from typing import Optional

from PySide6.QtCore import QEasingCurve, QEvent, QObject, QPoint, QPropertyAnimation, QRect, QSize, Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from app.core import lucide

TAB_SIZE = 44          # the square close tab
TAB_TOP = 14           # its distance from the top of the sheet


class PageSheet(QFrame):
    opened = Signal()
    closed = Signal()
    close_requested = Signal()

    DURATION = 280
    animations_enabled = True
    _order = itertools.count(1)        # which sheet was opened last

    def __init__(self, host: QWidget, cover: QWidget, keep_content: bool = False) -> None:
        """host: the widget holding both the sidebar and the content area.
        cover: the content area (a direct child of host) the sheet covers."""
        super().__init__(host)
        self._host = host
        self._cover = cover
        self._content: Optional[QWidget] = None
        self._open = False          # open (or opening), even while suspended
        self._suspended = False
        self._keep = keep_content
        self.opened_at = 0
        self.setObjectName("pageSheet")
        # Focus goes to the sheet when it opens, so Esc reaches it.
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.hide()

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # The tab is the host's child, not the sheet's, so it can stick out
        # past the sheet's left edge over the sidebar.
        self.tab = QPushButton(host)
        self.tab.setObjectName("pageSheetClose")
        self.tab.setFixedSize(TAB_SIZE, TAB_SIZE)
        self.tab.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tab.setToolTip("Close (Esc)")
        self.tab.setAccessibleName("Close")
        self.tab.clicked.connect(lambda _c=False: self.close_requested.emit())
        self.tab.hide()
        self.refresh_theme()

        escape = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        escape.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        escape.activated.connect(self.close_requested.emit)

        # What actually slides: a picture of the sheet, not the sheet. Moving
        # the real page repaints every card and paragraph on every frame,
        # which stutters on a long monograph; moving one picture is a single
        # copy per frame. The real page takes its place when the slide ends.
        self._ghost = QLabel(host)
        self._ghost.setObjectName("panel")
        self._ghost.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._ghost.hide()
        self._slide = QPropertyAnimation(self._ghost, b"pos", self)
        self._slide.setDuration(self.DURATION)
        self._slide.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._slide.valueChanged.connect(lambda pos: self._place_tab(pos))
        self._slide.finished.connect(self._finished)
        host.installEventFilter(self)

    # ------------------------------------------------------------- state

    @property
    def is_open(self) -> bool:
        return self._open

    @property
    def content(self) -> Optional[QWidget]:
        return self._content

    def set_content(self, widget: QWidget) -> None:
        self._drop_content(force=True)
        self._content = widget
        self._layout.addWidget(widget)
        widget.show()

    def adopt(self, widget: QWidget, back_signal) -> None:
        """Make a page's detail screen live in this sheet (keep_content)."""
        back = getattr(widget, "back_button", None)
        if back is not None:
            back.hide()                 # the X tab replaces it
        self.set_content(widget)
        self.close_requested.connect(back_signal.emit)

    def _drop_content(self, force: bool = False) -> None:
        if self._keep and not force:
            return
        if self._content is not None:
            self._layout.removeWidget(self._content)
            self._content.hide()
            self._content.deleteLater()
            self._content = None

    # ---------------------------------------------------------- geometry

    def _full(self) -> QRect:
        return QRect(self._cover.geometry())

    def _off(self) -> QPoint:
        area = self._full()
        return QPoint(self._host.width(), area.y())

    def moveEvent(self, event) -> None:  # noqa: N802
        super().moveEvent(event)
        if self.isVisible():
            self._place_tab(self.pos())

    def _place_tab(self, pos: QPoint) -> None:
        self.tab.move(pos.x() - TAB_SIZE, pos.y() + TAB_TOP)

    def _sliding(self) -> bool:
        return self._slide.state() == QPropertyAnimation.State.Running

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if watched is self._host and event.type() == QEvent.Type.Resize and self.isVisible():
            self.setGeometry(self._full())
        return False

    # ------------------------------------------------------------ moving

    def open_sheet(self) -> None:
        area = self._full()
        self.opened_at = self.opened_at if self._open else next(self._order)
        self._open = True
        self._suspended = False
        if self.isVisible():
            # Already open (another entry was inspected): the page has
            # redrawn itself in place, nothing to slide.
            self.setGeometry(area)
            self.setFocus()
            return
        start = self._ghost.pos() if self._sliding() else self._off()
        if not self._sliding():
            # Lay the page out at its final size while hidden, and take its
            # picture for the slide.
            self.setGeometry(area)
            self._snapshot()
        self._run(start, area.topLeft())

    def close_sheet(self) -> None:
        if not self._open:
            return
        self._open = False
        if self._suspended or not (self.isVisible() or self._sliding()):
            self._suspended = False
            self._slide.stop()
            self._finished()
            return
        start = self._ghost.pos() if self._sliding() else self.pos()
        if not self._sliding():
            self._snapshot()
        self.hide()
        self._run(start, self._off())

    def suspend(self) -> None:
        """Hide at once, keeping the content (another tab was opened)."""
        if self._sliding():
            self._slide.stop()
            self._ghost.hide()
            if not self._open:             # was closing: finish now
                self._finished()
                return
        if self._open and not self._suspended:
            self._suspended = True
            self.hide()
            self.tab.hide()

    def resume(self) -> None:
        if self._open and self._suspended:
            self._suspended = False
            self.setGeometry(self._full())
            self._show_live()

    def _snapshot(self) -> None:
        layout = self.layout()
        if layout is not None:
            layout.activate()
        self._ghost.setPixmap(self.grab())
        self._ghost.resize(self.size())

    def _show_live(self) -> None:
        self.show()
        self.raise_()
        self.tab.show()
        self.tab.raise_()
        self._place_tab(self.pos())
        self.setFocus()

    def _run(self, start: QPoint, end: QPoint) -> None:
        self._slide.stop()
        if not self.animations_enabled:
            self._finished()
            return
        self._ghost.move(start)
        self._ghost.show()
        self._ghost.raise_()
        self.tab.show()
        self.tab.raise_()
        self._place_tab(start)
        self._slide.setStartValue(start)
        self._slide.setEndValue(end)
        self._slide.start()

    def _finished(self) -> None:
        self._ghost.hide()
        self._ghost.clear()                # free the picture
        if self._open:
            self.setGeometry(self._full())
            self._show_live()
            self.opened.emit()
            return
        self.hide()
        self.tab.hide()
        self._drop_content()
        self.closed.emit()

    # ------------------------------------------------------------- theme

    def refresh_theme(self) -> None:
        self.tab.setIcon(lucide.icon("x", 22, "#FFFFFF"))
        self.tab.setIconSize(QSize(22, 22))
        refresh = getattr(self._content, "refresh_theme", None)
        if refresh is not None:
            refresh()
