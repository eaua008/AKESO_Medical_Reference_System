"""Akeso's own title bar.

Windows draws a grey strip above every app with an icon, the window title
("Akeso — Phrixus Orion") and minimise / maximise / close. Akeso replaces
it with its own strip in the same place, in the app's colours, holding
just the three buttons on the right. The header's Akeso logo is drawn
bigger, centred on strip + header together, so it fills the space where
the title text used to be (BrandLogo below).

Everything else is Windows' own, exactly as in any other app:

  * drag the strip (or empty header space) to move the window; drag it to
    the top of the screen to maximise, or to an edge / corner to snap,
  * double-click the strip to maximise / restore,
  * drag the window edges or corners to resize,
  * rest the mouse on maximise for the Windows 11 snap-layouts panel
    (Windows 10 has none, so Akeso shows its own copy there),
  * restore-down after a snap + maximise goes back to the normal size the
    window had before snapping, not to the snapped half.

How: the window keeps its real Windows styles (sizing border, caption,
min / max boxes), and Akeso only tells Windows where its "title bar",
"edges" and "maximise button" are (see "Windows glue" further down). The
maximise button asks Windows whether the window is maximised (IsZoomed),
so its icon always matches what you see.

Only on Windows; on macOS / Linux the normal title bar stays. Setting the
environment variable AKESO_SYSTEM_TITLEBAR=1 brings back the Windows title
bar too.
"""

import os
import sys
from typing import Optional

from PySide6.QtCore import QEvent, QObject, QPoint, QPointF, QRect, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QGuiApplication, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QAbstractButton, QApplication, QHBoxLayout, QLabel, QStackedWidget, QWidget,
)

from app.core.theme import Theme

TITLE_HEIGHT = 34          # the strip
BUTTON_WIDTH = 46          # Windows' own caption-button width
BRAND_HEIGHT = 50          # the big logo spanning the strip and the header
MIN_WIDTH, MIN_HEIGHT = 900, 600   # smallest the window can be dragged to
RESIZE_BORDER = 6          # logical px along each edge that resize the window
CLOSE_HOVER = "#C42B1C"    # Windows 11 close-button red

_active = False


def enabled() -> bool:
    """True when Akeso should try to draw its own title bar."""
    return sys.platform == "win32" and not os.environ.get("AKESO_SYSTEM_TITLEBAR")


def active() -> bool:
    """True once install() succeeded."""
    return _active


def native_snap_layouts() -> bool:
    """Windows 11 shows its own snap-layouts panel over the maximise button
    (build 22000+). Windows 10 does not, so Akeso shows its own there."""
    if sys.platform != "win32":
        return False
    try:
        return sys.getwindowsversion().build >= 22000
    except AttributeError:
        return False


# ------------------------------------------------------- window state (native)

def _hwnd(window: QWidget) -> int:
    return int(window.winId())


def is_maximized(window: QWidget) -> bool:
    """Ask Windows, not Qt: Qt's idea of the state can lag behind for a
    frameless window (that is what made the button need two presses)."""
    if sys.platform == "win32":
        try:
            import ctypes
            return bool(ctypes.windll.user32.IsZoomed(_hwnd(window)))
        except Exception:  # noqa: BLE001
            pass
    return window.isMaximized()


def toggle_maximized(window: QWidget) -> None:
    if sys.platform == "win32":
        try:
            import ctypes
            sw_maximize, sw_restore = 3, 9
            ctypes.windll.user32.ShowWindow(
                _hwnd(window), sw_restore if is_maximized(window) else sw_maximize)
            return
        except Exception:  # noqa: BLE001
            pass
    if window.isMaximized():
        window.showNormal()
    else:
        window.showMaximized()


def minimize(window: QWidget) -> None:
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(_hwnd(window), 6)     # SW_MINIMIZE
            return
        except Exception:  # noqa: BLE001
            pass
    window.showMinimized()


# ------------------------------------------------------------------ buttons

class _CaptionButton(QAbstractButton):
    """Minimise / maximise / close, drawn like Windows 11's (thin 1 px lines)."""

    def __init__(self, kind: str) -> None:
        super().__init__()
        self.kind = kind                       # "min" | "max" | "close"
        self.setFixedSize(BUTTON_WIDTH, TITLE_HEIGHT)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setAccessibleName({"min": "Minimize", "max": "Maximize",
                                "close": "Close"}[kind])
        # On Windows 11 the maximise button belongs to Windows while the
        # mouse is on it (that is what brings up snap layouts), so Qt sees
        # no hover / press there; native_event() reports them instead.
        self._native_hover = False
        self._native_down = False
        self._leave_check = QTimer(self)
        self._leave_check.setInterval(120)
        self._leave_check.timeout.connect(self._check_left)

    def sizeHint(self) -> QSize:  # noqa: N802
        return self.size()

    def set_native_state(self, hover: Optional[bool] = None,
                         down: Optional[bool] = None) -> None:
        if hover is not None:
            self._native_hover = hover
        if down is not None:
            self._native_down = down
        if self._native_hover or self._native_down:
            self._leave_check.start()
        self.update()

    def _check_left(self) -> None:
        """Windows does not always say when the mouse left; check."""
        if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
            self._native_hover = False
            self._native_down = False
            self._leave_check.stop()
            self.update()

    def event(self, event) -> bool:
        if event.type() in (QEvent.Type.HoverEnter, QEvent.Type.HoverLeave):
            self.update()
        return super().event(event)

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        hovered = self.underMouse() or self._native_hover
        pressed = self.isDown() or self._native_down
        ink = QColor(Theme.token("TEXT"))
        if self.kind == "close" and (hovered or pressed):
            back = QColor(CLOSE_HOVER)
            p.fillRect(self.rect(), back.darker(115) if pressed else back)
            ink = QColor("#FFFFFF")
        elif hovered or pressed:
            back = QColor(Theme.token("TEXT"))
            back.setAlphaF(0.14 if pressed else 0.08)
            p.fillRect(self.rect(), back)
        if not self.window().isActiveWindow() and not hovered:
            ink.setAlphaF(0.5)

        pen = QPen(ink)
        pen.setWidthF(1.0)
        pen.setCosmetic(True)
        p.setPen(pen)
        cx, cy = round(self.width() / 2) + 0.5, round(self.height() / 2) + 0.5
        s = 5.0                                       # half of a 10 px glyph
        if self.kind == "min":
            p.drawLine(QPointF(cx - s, cy), QPointF(cx + s, cy))
        elif self.kind == "max":
            if is_maximized(self.window()):           # "restore": two squares
                p.drawRect(QRectF(cx - s, cy - s + 2, 2 * s - 2, 2 * s - 2))
                p.drawLine(QPointF(cx - s + 2, cy - s), QPointF(cx + s, cy - s))
                p.drawLine(QPointF(cx + s, cy - s), QPointF(cx + s, cy + s - 2))
            else:
                p.drawRect(QRectF(cx - s, cy - s, 2 * s, 2 * s))
        else:
            p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            p.drawLine(QPointF(cx - s, cy - s), QPointF(cx + s, cy + s))
            p.drawLine(QPointF(cx - s, cy + s), QPointF(cx + s, cy - s))
        p.end()


# ------------------------------------------------- snap layouts (Windows 10)

# Each layout: the zones a window can take, as (x, y, w, h) fractions of the
# screen's free area (without the taskbar). Same set as Windows 11's own.
SNAP_LAYOUTS = (
    ((0, 0, .5, 1), (.5, 0, .5, 1)),
    ((0, 0, 2 / 3, 1), (2 / 3, 0, 1 / 3, 1)),
    ((0, 0, 1 / 3, 1), (1 / 3, 0, 1 / 3, 1), (2 / 3, 0, 1 / 3, 1)),
    ((0, 0, .5, 1), (.5, 0, .5, .5), (.5, .5, .5, .5)),
    ((0, 0, .5, .5), (.5, 0, .5, .5), (0, .5, .5, .5), (.5, .5, .5, .5)),
)
SNAP_TILE = QSize(72, 50)          # one layout preview
SNAP_GAP = 3                       # between zones inside a preview


def snap_to(window: QWidget, zone: tuple) -> None:
    """Put the window in that part of the screen it is on."""
    screen = window.screen() or QGuiApplication.primaryScreen()
    area = screen.availableGeometry()
    if is_maximized(window) or window.isFullScreen():
        toggle_maximized(window)                 # restore first, then place
        QApplication.processEvents()
    x, y, w, h = zone
    left = area.left() + round(x * area.width())
    top = area.top() + round(y * area.height())
    right = area.left() + round((x + w) * area.width())
    bottom = area.top() + round((y + h) * area.height())
    window.setGeometry(left, top, right - left, bottom - top)


class _SnapTile(QWidget):
    """One layout preview; each zone in it is clickable."""

    def __init__(self, zones: tuple, on_pick) -> None:
        super().__init__()
        self._zones = zones
        self._on_pick = on_pick
        self._hover: Optional[int] = None
        self.setFixedSize(SNAP_TILE)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _rects(self) -> list[QRectF]:
        w, h = self.width() - 1, self.height() - 1
        return [QRectF(x * w + SNAP_GAP / 2, y * h + SNAP_GAP / 2,
                       zw * w - SNAP_GAP, zh * h - SNAP_GAP)
                for x, y, zw, zh in self._zones]

    def _zone_at(self, pos) -> Optional[int]:
        for i, rect in enumerate(self._rects()):
            if rect.contains(QPointF(pos)):
                return i
        return None

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        hover = self._zone_at(event.position().toPoint())
        if hover != self._hover:
            self._hover = hover
            self.update()

    def leaveEvent(self, _event) -> None:  # noqa: N802
        self._hover = None
        self.update()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        zone = self._zone_at(event.position().toPoint())
        if zone is not None and event.button() == Qt.MouseButton.LeftButton:
            self._on_pick(self._zones[zone])

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        border = QColor(Theme.token("TEXT_MUTED"))
        border.setAlphaF(0.55)
        for i, rect in enumerate(self._rects()):
            fill = QColor(Theme.token("PRIMARY")) if i == self._hover else \
                QColor(Theme.token("SURFACE_RAISED"))
            p.setPen(QPen(QColor(Theme.token("PRIMARY")) if i == self._hover else border, 1))
            p.setBrush(fill)
            p.drawRoundedRect(rect, 4, 4)
        p.end()


class SnapLayouts(QWidget):
    """Windows 10 only: the "arrange window" panel that opens under the
    maximise button when you rest the mouse on it (a copy of Windows 11's
    snap layouts). Click a zone to put Akeso in that part of the screen."""

    def __init__(self, button: QWidget) -> None:
        super().__init__(None, Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint
                         | Qt.WindowType.WindowStaysOnTopHint
                         | Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._button = button
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 12, 12, 12)
        row.setSpacing(12)
        for zones in SNAP_LAYOUTS:
            row.addWidget(_SnapTile(zones, self._pick))
        self.adjustSize()
        self._watch = QTimer(self)                 # close when the mouse leaves
        self._watch.setInterval(150)
        self._watch.timeout.connect(self._check_mouse)
        self._outside = 0

    def popup(self) -> None:
        anchor = self._button.mapToGlobal(QPoint(self._button.width(), self._button.height()))
        screen = self._button.screen().availableGeometry()
        x = max(screen.left() + 4, min(anchor.x() - self.width(), screen.right() - self.width() - 4))
        self.move(x, anchor.y() + 4)
        self._outside = 0
        self.show()
        self.raise_()
        self._watch.start()

    def _pick(self, zone: tuple) -> None:
        self.hide()
        snap_to(self._button.window(), zone)

    def _check_mouse(self) -> None:
        cursor = QCursor.pos()
        over_button = self._button.rect().contains(self._button.mapFromGlobal(cursor))
        over_me = self.rect().adjusted(-8, -12, 8, 8).contains(self.mapFromGlobal(cursor))
        self._outside = 0 if (over_button or over_me) else self._outside + 1
        if self._outside >= 3 or not self._button.window().isVisible():
            self.hide()

    def hideEvent(self, event) -> None:  # noqa: N802
        self._watch.stop()
        super().hideEvent(event)

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor(Theme.token("BORDER")), 1))
        p.setBrush(QColor(Theme.token("SURFACE")))
        p.drawRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), 10, 10)
        p.end()


class TitleBar(QWidget):
    """The strip at the very top: the three buttons on the right, painted in
    the header's colour so it reads as part of the app."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(TITLE_HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addStretch(1)
        self.minimize = _CaptionButton("min")
        self.maximize = _CaptionButton("max")
        self.close_button = _CaptionButton("close")
        self.minimize.clicked.connect(lambda: minimize(self.window()))
        self.maximize.clicked.connect(lambda: toggle_maximized(self.window()))
        self.close_button.clicked.connect(lambda: self.window().close())
        for button in (self.minimize, self.maximize, self.close_button):
            row.addWidget(button)
        # Rest the mouse on maximise -> arrange-window layouts. Windows 11
        # shows its own panel there; only Windows 10 needs Akeso's copy.
        self.snap: Optional[SnapLayouts] = None
        self._snap_timer = QTimer(self)
        self._snap_timer.setSingleShot(True)
        self._snap_timer.setInterval(450)
        self._snap_timer.timeout.connect(self._maybe_snap)
        if not native_snap_layouts():
            self.snap = SnapLayouts(self.maximize)
            self.maximize.installEventFilter(self)
        # Repaint after a light/dark or colour-theme switch.
        self._theme_key = Theme.key()
        self._theme_timer = QTimer(self)
        self._theme_timer.setInterval(400)
        self._theme_timer.timeout.connect(self._check_theme)
        self._theme_timer.start()

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        if watched is self.maximize:
            if event.type() == QEvent.Type.HoverEnter:
                self._snap_timer.start()
            elif event.type() in (QEvent.Type.HoverLeave, QEvent.Type.MouseButtonPress):
                self._snap_timer.stop()
                if event.type() == QEvent.Type.MouseButtonPress and self.snap:
                    self.snap.hide()
        return False

    def _maybe_snap(self) -> None:
        if self.snap and self.maximize.underMouse() and self.window().isActiveWindow():
            self.snap.popup()

    def _check_theme(self) -> None:
        if Theme.key() != self._theme_key:
            self._theme_key = Theme.key()
            self.refresh()

    def refresh(self) -> None:
        for button in (self.minimize, self.maximize, self.close_button):
            button.setDown(False)
            button.update()
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(Theme.token("SURFACE")))
        p.end()


class BrandLogo(QLabel):
    """One big Akeso logo over the strip + the current screen's header.

    The header keeps its own logo label (so its layout and spacing stay as
    they are), but that label is given an empty picture of the big logo's
    size; this label floats on top and draws the real logo, centred on the
    strip and the header together. Clicks go through it to whatever is
    underneath, so dragging the logo area still moves the window.
    """

    def __init__(self, host: QWidget, title_bar: TitleBar, screens: QStackedWidget) -> None:
        super().__init__(host)
        self.setObjectName("panel")
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._title = title_bar
        self._screens = screens
        self._key = None
        self._blank: Optional[QPixmap] = None
        screens.currentChanged.connect(lambda _i: QTimer.singleShot(0, self.sync))
        host.installEventFilter(self)
        # Headers redraw their logo on a theme switch; take it back.
        self._timer = QTimer(self)
        self._timer.setInterval(300)
        self._timer.timeout.connect(self.sync)
        self._timer.start()

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        if event.type() in (QEvent.Type.Resize, QEvent.Type.Show, QEvent.Type.LayoutRequest):
            QTimer.singleShot(0, self.sync)
        return False

    def _header_logo(self) -> Optional[QLabel]:
        screen = self._screens.currentWidget()
        if screen is None:
            return None
        for label in screen.findChildren(QLabel, "brandLogo"):
            parent = label.parentWidget()
            if parent is not None and parent.objectName() in _DRAG_AREAS:
                return label
        return None

    def sync(self) -> None:
        from app.core.assets import logo_pixmap
        label = self._header_logo()
        if label is None or not label.isVisible():
            self.hide()
            return
        key = Theme.key()
        if key != self._key:
            self._key = key
            self.setPixmap(logo_pixmap(BRAND_HEIGHT))
            self.adjustSize()
            blank = QPixmap(self.pixmap().size())
            blank.setDevicePixelRatio(self.pixmap().devicePixelRatio())
            blank.fill(Qt.GlobalColor.transparent)
            self._blank = blank
        if self._blank is not None and label.pixmap().cacheKey() != self._blank.cacheKey():
            label.setPixmap(self._blank)                 # keeps the header's spacing
        header = label.parentWidget()
        band = self._title.height() + header.height()
        x = label.mapTo(self.parentWidget(), QPoint(0, 0)).x()
        top = self._title.mapTo(self.parentWidget(), QPoint(0, 0)).y()
        self.move(x, top + round((band - self.height()) / 2))
        self.show()
        self.raise_()


# ------------------------------------------------------------- hit testing

# The screen headers (dashboard and sign-in): their empty space drags the
# window too, like the space beside the tabs in a browser.
_DRAG_AREAS = ("headerFrame", "authHeader")

HTCLIENT, HTCAPTION, HTMAXBUTTON = 1, 2, 9
HTLEFT, HTRIGHT, HTTOP, HTTOPLEFT, HTTOPRIGHT = 10, 11, 12, 13, 14
HTBOTTOM, HTBOTTOMLEFT, HTBOTTOMRIGHT = 15, 16, 17


def _caption_part(window: QWidget, pos: QPoint) -> str:
    """What is under this point (window coordinates):
    "max" (the maximise button), "caption" (empty part of the strip or
    header, which drags the window) or "client" (anything else; Qt)."""
    widget = window.childAt(pos)
    if isinstance(widget, _CaptionButton):
        # Only Windows 11 has a snap-layouts panel to show over it; on
        # Windows 10 Qt keeps the button (and Akeso's own panel).
        return "max" if widget.kind == "max" and native_snap_layouts() else "client"
    if isinstance(widget, TitleBar):
        return "caption"
    if widget is not None and (
            widget.objectName() in _DRAG_AREAS
            or (widget.objectName() == "brandLogo" and widget.parentWidget() is not None
                and widget.parentWidget().objectName() in _DRAG_AREAS)):
        return "caption"
    return "client"


def _edge_at(window: QWidget, pos: QPoint) -> Optional[int]:
    """The Windows hit-test code for a resize edge here, or None."""
    if is_maximized(window) or window.isFullScreen():
        return None
    b = RESIZE_BORDER
    left, right = pos.x() < b, pos.x() >= window.width() - b
    top, bottom = pos.y() < b, pos.y() >= window.height() - b
    if (left or right or top or bottom) and isinstance(window.childAt(pos), _CaptionButton) \
            and not (top and right):
        return None                       # the buttons keep their clicks
    if top and left:
        return HTTOPLEFT
    if top and right:
        return HTTOPRIGHT
    if bottom and left:
        return HTBOTTOMLEFT
    if bottom and right:
        return HTBOTTOMRIGHT
    if left:
        return HTLEFT
    if right:
        return HTRIGHT
    if top:
        return HTTOP
    if bottom:
        return HTBOTTOM
    return None


# ------------------------------------------------------------ the window

class _FrameController(QObject):
    """Window-level bookkeeping that is not a Windows message: repaint the
    caption buttons on state changes, remember the window's normal
    ("floating") size, and use it when coming back from maximised."""

    def __init__(self, window: QWidget) -> None:
        super().__init__(window)
        self._window = window
        self.floating_rect: Optional[QRect] = None   # last size not snapped / maximised
        self._was_maximized = False

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        window = self._window
        if watched is not window:
            return False
        kind = event.type()
        if kind == QEvent.Type.WinIdChange:
            # Qt rebuilt the Windows window behind Akeso. It does that the
            # first time a 3D / web view appears (the Body System Explorer,
            # the reference browser): the window switches to GPU drawing and
            # is recreated with Qt's plain frameless styles, which drops the
            # sizing border, Aero Snap and snap layouts. Put them back.
            QTimer.singleShot(0, self._restyle)
        if kind in (QEvent.Type.Move, QEvent.Type.Resize):
            self._remember()
        if kind == QEvent.Type.WindowStateChange:
            maximized = is_maximized(window)
            if self._was_maximized and not maximized and not window.isMinimized():
                # Restore-down from maximised: back to the normal size, not
                # to a snapped half (Windows would otherwise reuse that).
                QTimer.singleShot(0, self._restore_floating)
            if not window.isMinimized():
                self._was_maximized = maximized
        if kind in (QEvent.Type.WindowStateChange, QEvent.Type.ActivationChange,
                    QEvent.Type.Resize):
            for bar in window.findChildren(TitleBar):
                bar.refresh()
        return False

    def _restyle(self) -> None:
        if sys.platform != "win32" or not _active:
            return
        try:
            _apply_native_styles(self._window)
        except Exception as error:  # noqa: BLE001 - cosmetics never stop the app
            print(f"[window_frame] Could not restore the window styles: {error}")
        for bar in self._window.findChildren(TitleBar):
            bar.refresh()

    def _remember(self) -> None:
        window = self._window
        if not window.isVisible() or window.isMinimized() or is_maximized(window) \
                or window.isFullScreen():
            return
        rect = window.geometry()
        if rect.x() <= -30000 or _looks_snapped(window, rect):
            return
        self.floating_rect = rect

    def _restore_floating(self) -> None:
        window = self._window
        rect = self.floating_rect
        if rect is None or is_maximized(window) or window.isMinimized():
            return
        if _looks_snapped(window, window.geometry()) or window.geometry() != rect:
            window.setGeometry(_fit_on_screen(window, rect))


def _looks_snapped(window: QWidget, rect) -> bool:
    """A rectangle that fills the free screen area edge to edge on at least
    two opposite sides is a snapped half / third / quarter, not a size the
    person dragged to."""
    screen = window.screen() or QGuiApplication.primaryScreen()
    area = screen.availableGeometry()
    tol = 2
    full_height = abs(rect.top() - area.top()) <= tol and abs(rect.bottom() - area.bottom()) <= tol
    full_width = abs(rect.left() - area.left()) <= tol and abs(rect.right() - area.right()) <= tol
    on_edge_x = abs(rect.left() - area.left()) <= tol or abs(rect.right() - area.right()) <= tol
    on_edge_y = abs(rect.top() - area.top()) <= tol or abs(rect.bottom() - area.bottom()) <= tol
    return (full_height and on_edge_x) or (full_width and on_edge_y) or \
        (on_edge_x and on_edge_y and rect.width() <= area.width() // 2 + tol
         and rect.height() <= area.height() // 2 + tol)


def _fit_on_screen(window: QWidget, rect: QRect) -> QRect:
    """Keep a remembered size on the screen the window is on now."""
    screen = window.screen() or QGuiApplication.primaryScreen()
    return _fit_in(screen.availableGeometry(), rect)


def _fit_in(area: QRect, rect: QRect) -> QRect:
    w = min(rect.width(), area.width())
    h = min(rect.height(), area.height())
    x = min(max(rect.x(), area.left()), area.right() - w + 1)
    y = min(max(rect.y(), area.top()), area.bottom() - h + 1)
    return QRect(x, y, w, h)


# ------------------------------------------------------------ Windows glue
#
# The window keeps real Windows styles (sizing border, caption, min/max
# boxes, system menu), so Windows itself does the moving, resizing, Aero
# Snap (drag to the top / an edge), the Windows 11 snap-layouts panel on the
# maximise button, the minimise / maximise animations and the right-click
# window menu. Akeso only answers three questions Windows asks:
#
#   WM_NCCALCSIZE   "how big is the title bar / border?"  -> nothing: the
#                   whole window is Akeso's (when maximised, the border
#                   Windows pushes off-screen is trimmed off),
#   WM_GETMINMAXINFO "how big may it get?"                -> exactly the free
#                   screen area when maximised, and Akeso's minimum size,
#   WM_NCHITTEST    "what is under the mouse?"            -> a resize edge,
#                   the caption (drag), the maximise button (so Windows 11
#                   shows its snap layouts), or the app itself.
#
# Because Windows treats the maximise button as its own while the mouse is
# on it, its clicks and hover arrive as non-client messages and are handled
# here too.

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    _user32 = ctypes.windll.user32
    _dwmapi = ctypes.windll.dwmapi

    WM_NCCALCSIZE, WM_NCHITTEST, WM_GETMINMAXINFO = 0x0083, 0x0084, 0x0024
    WM_NCMOUSEMOVE, WM_NCLBUTTONDOWN, WM_NCLBUTTONUP = 0x00A0, 0x00A1, 0x00A2
    WM_NCLBUTTONDBLCLK, WM_NCMOUSELEAVE = 0x00A3, 0x02A2
    GWL_STYLE = -16
    WS_CAPTION, WS_THICKFRAME, WS_SYSMENU = 0x00C00000, 0x00040000, 0x00080000
    WS_MINIMIZEBOX, WS_MAXIMIZEBOX = 0x00020000, 0x00010000
    SWP_FRAMECHANGED, SWP_NOMOVE, SWP_NOSIZE = 0x0020, 0x0002, 0x0001
    SWP_NOZORDER, SWP_NOACTIVATE = 0x0004, 0x0010
    SM_CXSIZEFRAME, SM_CYSIZEFRAME, SM_CXPADDEDBORDER = 32, 33, 92
    MONITOR_DEFAULTTONEAREST = 2
    WVR_REDRAW = 0x0300
    ABM_GETSTATE, ABS_AUTOHIDE = 0x00000004, 0x0000001

    class _NCCALCSIZE_PARAMS(ctypes.Structure):
        _fields_ = [("rgrc", wintypes.RECT * 3), ("lppos", ctypes.c_void_p)]

    class _MINMAXINFO(ctypes.Structure):
        _fields_ = [("ptReserved", wintypes.POINT), ("ptMaxSize", wintypes.POINT),
                    ("ptMaxPosition", wintypes.POINT), ("ptMinTrackSize", wintypes.POINT),
                    ("ptMaxTrackSize", wintypes.POINT)]

    class _MONITORINFO(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT),
                    ("rcWork", wintypes.RECT), ("dwFlags", wintypes.DWORD)]

    class _MARGINS(ctypes.Structure):
        _fields_ = [("l", ctypes.c_int), ("r", ctypes.c_int),
                    ("t", ctypes.c_int), ("b", ctypes.c_int)]

    class _APPBARDATA(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("hWnd", wintypes.HWND),
                    ("uCallbackMessage", wintypes.UINT), ("uEdge", wintypes.UINT),
                    ("rc", wintypes.RECT), ("lParam", wintypes.LPARAM)]

    _get_style = getattr(_user32, "GetWindowLongPtrW", _user32.GetWindowLongW)
    _set_style = getattr(_user32, "SetWindowLongPtrW", _user32.SetWindowLongW)
    _get_style.restype = ctypes.c_ssize_t
    _get_style.argtypes = [wintypes.HWND, ctypes.c_int]
    _set_style.restype = ctypes.c_ssize_t
    _set_style.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
    _user32.MonitorFromWindow.restype = wintypes.HANDLE
    _user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
    _user32.GetMonitorInfoW.argtypes = [wintypes.HANDLE, ctypes.POINTER(_MONITORINFO)]

    def _frame_thickness(hwnd) -> tuple[int, int]:
        """The sizing border Windows pushes off-screen when maximised."""
        try:
            dpi = _user32.GetDpiForWindow(hwnd)
            fx = _user32.GetSystemMetricsForDpi(SM_CXSIZEFRAME, dpi)
            fy = _user32.GetSystemMetricsForDpi(SM_CYSIZEFRAME, dpi)
            pad = _user32.GetSystemMetricsForDpi(SM_CXPADDEDBORDER, dpi)
        except AttributeError:
            fx = _user32.GetSystemMetrics(SM_CXSIZEFRAME)
            fy = _user32.GetSystemMetrics(SM_CYSIZEFRAME)
            pad = _user32.GetSystemMetrics(SM_CXPADDEDBORDER)
        return fx + pad, fy + pad

    def _taskbar_autohides() -> bool:
        data = _APPBARDATA()
        data.cbSize = ctypes.sizeof(_APPBARDATA)
        try:
            return bool(ctypes.windll.shell32.SHAppBarMessage(ABM_GETSTATE, ctypes.byref(data))
                        & ABS_AUTOHIDE)
        except OSError:
            return False


def _set_button_state(window: QWidget, hover: Optional[bool] = None,
                      down: Optional[bool] = None) -> None:
    for bar in window.findChildren(TitleBar):
        bar.maximize.set_native_state(hover, down)


def native_event(window: QWidget, event_type, message) -> Optional[tuple[bool, int]]:
    """Answer the Windows messages described above. None = let Qt handle it."""
    if not _active or sys.platform != "win32" or bytes(event_type) != b"windows_generic_MSG":
        return None
    msg = wintypes.MSG.from_address(int(message))
    kind = msg.message

    if kind == WM_NCCALCSIZE:
        rect = (_NCCALCSIZE_PARAMS.from_address(msg.lParam).rgrc[0] if msg.wParam
                else wintypes.RECT.from_address(msg.lParam))
        if _user32.IsZoomed(msg.hWnd) and not window.isFullScreen():
            fx, fy = _frame_thickness(msg.hWnd)
            rect.left += fx
            rect.top += fy
            rect.right -= fx
            rect.bottom -= fy
            if _taskbar_autohides():
                rect.bottom -= 2                # a sliver to reveal the taskbar
        return True, (WVR_REDRAW if msg.wParam else 0)

    if kind == WM_GETMINMAXINFO:
        info = _MINMAXINFO.from_address(msg.lParam)
        monitor = _user32.MonitorFromWindow(msg.hWnd, MONITOR_DEFAULTTONEAREST)
        mi = _MONITORINFO()
        mi.cbSize = ctypes.sizeof(_MONITORINFO)
        if monitor and _user32.GetMonitorInfoW(monitor, ctypes.byref(mi)):
            fx, fy = _frame_thickness(msg.hWnd)
            work, full = mi.rcWork, mi.rcMonitor
            # Maximised = the free screen area exactly, once WM_NCCALCSIZE
            # trims the off-screen border (no gaps, taskbar never covered).
            info.ptMaxPosition.x = work.left - full.left - fx
            info.ptMaxPosition.y = work.top - full.top - fy
            info.ptMaxSize.x = (work.right - work.left) + 2 * fx
            info.ptMaxSize.y = (work.bottom - work.top) + 2 * fy
        ratio = window.devicePixelRatioF() or 1.0
        info.ptMinTrackSize.x = int(max(window.minimumWidth(), MIN_WIDTH) * ratio)
        info.ptMinTrackSize.y = int(max(window.minimumHeight(), MIN_HEIGHT) * ratio)
        return True, 0

    if kind == WM_NCHITTEST:
        pos = window.mapFromGlobal(QCursor.pos())
        edge = _edge_at(window, pos)
        if edge is not None:
            return True, edge
        part = _caption_part(window, pos)
        if part == "max":
            return True, HTMAXBUTTON
        if part == "caption":
            return True, HTCAPTION
        return True, HTCLIENT

    # The maximise button, while Windows treats it as a caption button.
    if kind == WM_NCMOUSEMOVE:
        _set_button_state(window, hover=(msg.wParam == HTMAXBUTTON))
        return None                     # Windows still shows its snap layouts
    if kind == WM_NCMOUSELEAVE:
        _set_button_state(window, hover=False, down=False)
        return None
    if kind == WM_NCLBUTTONDOWN and msg.wParam == HTMAXBUTTON:
        _set_button_state(window, down=True)
        return True, 0
    if kind == WM_NCLBUTTONUP and msg.wParam == HTMAXBUTTON:
        _set_button_state(window, down=False)
        toggle_maximized(window)
        return True, 0
    if kind == WM_NCLBUTTONDBLCLK and msg.wParam == HTMAXBUTTON:
        return True, 0
    if kind in (WM_NCLBUTTONUP, WM_NCLBUTTONDOWN):
        _set_button_state(window, down=False)
    return None


def _apply_native_styles(window: QWidget) -> None:
    hwnd = _hwnd(window)
    style = _get_style(hwnd, GWL_STYLE)
    _set_style(hwnd, GWL_STYLE, style | WS_CAPTION | WS_THICKFRAME | WS_SYSMENU
               | WS_MINIMIZEBOX | WS_MAXIMIZEBOX)
    # A pixel of "glass" gives the usual drop shadow (Windows 10 too).
    margins = _MARGINS(0, 0, 1, 0)
    _dwmapi.DwmExtendFrameIntoClientArea(wintypes.HWND(hwnd), ctypes.byref(margins))
    corner = ctypes.c_int(2)                                 # DWMWCP_ROUND (Windows 11)
    _dwmapi.DwmSetWindowAttribute(wintypes.HWND(hwnd), 33, ctypes.byref(corner),
                                  ctypes.sizeof(corner))
    _user32.SetWindowPos(wintypes.HWND(hwnd), None, 0, 0, 0, 0, SWP_FRAMECHANGED
                         | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE)


def install(window: QWidget) -> Optional[TitleBar]:
    """Swap the Windows title bar of this window for Akeso's. Returns the
    TitleBar to place at the top of the window, or None (normal Windows
    title bar) when not on Windows, switched off, or if anything fails.
    The window must forward nativeEvent() to native_event()."""
    global _active
    if not enabled():
        return None
    try:
        # Qt lays the whole window out as content (no frame of its own)...
        window.setWindowFlags(window.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # ...while Windows still treats it as a normal, resizable window.
        _apply_native_styles(window)
        controller = _FrameController(window)
        window.installEventFilter(controller)
        window._frame_controller = controller        # keep it alive
        _active = True
        return TitleBar()
    except Exception as error:  # noqa: BLE001 - never stop the app over cosmetics
        print(f"[window_frame] Keeping the Windows title bar: {error}")
        window.setWindowFlags(window.windowFlags() & ~Qt.WindowType.FramelessWindowHint)
        return None


def place(window: QWidget, saved: Optional[list], default_size: QSize) -> None:
    """Before the first show: put the window where it was last time
    ([x, y, w, h] from the preferences), kept on a screen that still exists
    and shrunk to fit it, or centred on the main screen at default_size."""
    rect = QRect(*saved) if saved else None
    screen = (QGuiApplication.screenAt(rect.center()) if rect is not None else None) \
        or QGuiApplication.primaryScreen()
    if screen is None:
        window.resize(default_size)
        return
    area = screen.availableGeometry()
    if rect is None:
        w = min(default_size.width(), area.width())
        h = min(default_size.height(), area.height())
        rect = QRect(area.left() + (area.width() - w) // 2,
                     area.top() + (area.height() - h) // 2, w, h)
    rect = _fit_in(area, rect)
    window.setGeometry(rect)
    controller = getattr(window, "_frame_controller", None)
    if controller is not None:
        controller.floating_rect = QRect(rect)


def floating_rect(window: QWidget) -> Optional[QRect]:
    """The window's normal (not snapped, not maximised) size, for saving."""
    controller = getattr(window, "_frame_controller", None)
    if controller is not None and controller.floating_rect is not None:
        return controller.floating_rect
    return None if is_maximized(window) else window.geometry()
