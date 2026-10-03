"""Visible-first light/dark switching.

Why: QApplication.setStyleSheet() re-applies the whole ~140 KB stylesheet to
every widget in the app, including pages nobody is looking at (thousands of
widgets), which is what made the theme button lag.

How it works now:
    * The app-level stylesheet is set once (at startup, or on the login
      screen) and then left alone while the dashboard is open.
    * The dashboard registers "areas": the header, the sidebar and each page.
    * On a switch, only the areas you can SEE get the new stylesheet (a
      widget's own stylesheet beats the app-level one), so the click responds
      almost at once.
    * Every other area is restyled the moment it is shown (before it is
      painted, so the old theme never flashes), and quietly in the
      background, one area at a time, while the app is idle.
    * Small top-level windows (tooltips, popups) are refreshed too.

Both stylesheets come from the same Theme.stylesheet() template, so every
rule in the old one has a matching rule in the new one that overrides it.
"""

from typing import Callable, Optional

from PySide6.QtCore import QEvent, QObject, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QWidget

from app.core.theme import Theme

MODE_PROPERTY = "akesoThemeMode"
CATCH_UP_DELAY_MS = 600      # let the visible switch finish painting first
CATCH_UP_STEP_MS = 180       # then one hidden page per step

_css_cache: dict[str, str] = {}
_app_mode: Optional[str] = None     # the mode the app-level stylesheet is in


def stylesheet(mode: Optional[str] = None) -> str:
    """Theme.stylesheet() for a mode, built once and reused."""
    mode = mode or Theme.mode()
    if mode not in _css_cache:
        current = Theme.mode()
        Theme.set_mode(mode)
        try:
            _css_cache[mode] = Theme.stylesheet()
        finally:
            Theme.set_mode(current)
    return _css_cache[mode]


def apply_app_stylesheet() -> None:
    """Set the app-level stylesheet to the current mode (full restyle).

    Cheap while only the login screen exists; the dashboard uses ThemeScope
    instead. Always go through here so ThemeScope knows the app-level mode.
    """
    global _app_mode
    app = QApplication.instance()
    if app is not None:
        app.setStyleSheet(stylesheet())
        _app_mode = Theme.mode()


def app_mode() -> str:
    return _app_mode or Theme.mode()


class ThemeScope(QObject):
    """Restyles the dashboard area by area, visible parts first."""

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        global _app_mode
        if _app_mode is None:           # app stylesheet was set elsewhere
            _app_mode = Theme.mode()
        self._areas: dict[QWidget, Optional[Callable[[], None]]] = {}
        self._queue: list[QWidget] = []
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._catch_up_one)
        self._backdrops: list[QWidget] = []

    # ------------------------------------------------------------- areas

    def add(self, widget: QWidget, on_restyle: Optional[Callable[[], None]] = None) -> None:
        """Register an area. on_restyle runs after it gets a new theme
        (for icons drawn in code, which a stylesheet cannot recolour)."""
        self._areas[widget] = on_restyle
        widget.installEventFilter(self)
        widget.destroyed.connect(lambda _obj=None, w=widget: self._forget(w))
        if not self._current(widget) and widget.isVisible():
            self._restyle(widget)

    def add_backdrop(self, *widgets: QWidget) -> None:
        """Containers that hold the areas (window root, body, page stack).

        They show through wherever a page is transparent, but restyling them
        would restyle every page inside them. So they paint the theme's page
        colour themselves instead, which costs nothing on a switch.
        """
        for widget in widgets:
            widget.setAutoFillBackground(False)
            widget.installEventFilter(self)
            self._backdrops.append(widget)

    def remove(self, widget: QWidget) -> None:
        self._forget(widget)

    def _forget(self, widget: QWidget) -> None:
        self._areas.pop(widget, None)
        if widget in self._queue:
            self._queue.remove(widget)

    # ------------------------------------------------------------ switch

    def switch(self) -> None:
        """Call after Theme.toggle_mode()."""
        for backdrop in self._backdrops:
            backdrop.update()
        for widget in list(self._areas):
            if widget.isVisible():
                self._restyle(widget)
        self._restyle_windows()
        self._queue = [w for w in self._areas if not self._current(w)]
        if self._queue:
            self._timer.start(CATCH_UP_DELAY_MS)

    def pending(self) -> int:
        """Areas still in the old theme (for tests)."""
        return sum(1 for w in self._areas if not self._current(w))

    # ---------------------------------------------------------- internals

    @staticmethod
    def _current(widget: QWidget) -> bool:
        return (widget.property(MODE_PROPERTY) or app_mode()) == Theme.mode()

    def _restyle(self, widget: QWidget) -> None:
        if self._current(widget):
            return
        mode = Theme.mode()
        # Back in the app-level mode: drop the widget's own copy, so it goes
        # back to one stylesheet (cheaper for every widget built later).
        widget.setStyleSheet("" if mode == app_mode() else stylesheet(mode))
        widget.setProperty(MODE_PROPERTY, None if mode == app_mode() else mode)
        callback = self._areas.get(widget)
        if callback is not None:
            callback()

    def _catch_up_one(self) -> None:
        while self._queue and self._current(self._queue[0]):
            self._queue.pop(0)
        if self._queue:
            self._restyle(self._queue.pop(0))
        if self._queue:
            self._timer.start(CATCH_UP_STEP_MS)
        else:
            self._restyle_windows()

    def _restyle_windows(self) -> None:
        """Tooltips, menus and other small top-level windows that are not
        inside an area. The main window itself is skipped (its areas are
        handled above; restyling it would restyle everything)."""
        for window in QApplication.topLevelWidgets():
            if any(window is area or window.isAncestorOf(area) for area in self._areas):
                continue
            if not self._current(window):
                mode = Theme.mode()
                window.setStyleSheet("" if mode == app_mode() else stylesheet(mode))
                window.setProperty(MODE_PROPERTY, None if mode == app_mode() else mode)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        # Show arrives before the first paint, so a page is recoloured before
        # anyone can see the old theme on it.
        if event.type() == QEvent.Type.Show and watched in self._areas:
            self._restyle(watched)
        elif event.type() == QEvent.Type.Paint and watched in self._backdrops:
            painter = QPainter(watched)
            painter.fillRect(watched.rect(), QColor(Theme.token("BG")))
            painter.end()
        return False
