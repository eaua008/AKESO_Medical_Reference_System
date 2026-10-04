"""Akeso's own title bar.

Windows draws a grey strip above every app with an icon, the window title
("Akeso — Phrixus Orion") and minimise / maximise / close. Akeso replaces
it with its own strip in the same place, in the app's colours, holding
just the three buttons on the right. The header's Akeso logo is drawn
bigger, centred on strip + header together, so it fills the space where
the title text used to be (BrandLogo below).

  * drag the strip to move the window (drag a maximised window to pull it
    back to its normal size), double-click it to maximise / restore,
  * drag the window edges or corners to resize,
  * drag to a screen edge to snap.

The window is a Qt frameless window; Qt moves and resizes it
(startSystemMove / startSystemResize). Maximise / restore go straight to
Windows (ShowWindow), and the maximise button asks Windows whether the
window is maximised (IsZoomed), so the button and its icon always match
what you see, however the window got maximised (button, double-click,
Win+Up, snapping, the taskbar).

Only on Windows; on macOS / Linux the normal title bar stays. Setting the
environment variable AKESO_SYSTEM_TITLEBAR=1 brings back the Windows title
bar too.
"""

import os
import sys
from typing import Optional

from PySide6.QtCore import QEvent, QObject, QPoint, QPointF, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QGuiApplication, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QAbstractButton, QApplication, QHBoxLayout, QLabel, QStackedWidget, QWidget,
)

from app.core.theme import Theme

TITLE_HEIGHT = 34          # the strip
BUTTON_WIDTH = 46          # Windows' own caption-button width
BRAND_HEIGHT = 50       # the big logo spanning the strip and the header
RESIZE_BORDER = 5          # logical px along each edge that resize the window
CLOSE_HOVER = "#C42B1C"    # Windows 11 close-button red

_active = False


def enabled() -> bool:
    """True when Akeso should try to draw its own title bar."""
    return sys.platform == "win32" and not os.environ.get("AKESO_SYSTEM_TITLEBAR")


def active() -> bool:
    """True once install() succeeded."""
    return _active


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

    def sizeHint(self) -> QSize:  # noqa: N802
        return self.size()

    def event(self, event) -> bool:
        if event.type() in (QEvent.Type.HoverEnter, QEvent.Type.HoverLeave):
            self.update()
        return super().event(event)

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        hovered = self.underMouse()
        pressed = self.isDown()
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
        # Repaint after a light/dark or colour-theme switch.
        self._theme_key = Theme.key()
        self._theme_timer = QTimer(self)
        self._theme_timer.setInterval(400)
        self._theme_timer.timeout.connect(self._check_theme)
        self._theme_timer.start()

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
            if parent is not None and parent.objectName() in ("headerFrame", "authHeader"):
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

def _edges_at(window: QWidget, pos: QPoint) -> Qt.Edge:
    """Which window edges this point is close enough to resize."""
    edges = Qt.Edge(0)
    if is_maximized(window) or window.isFullScreen():
        return edges
    b = RESIZE_BORDER
    if pos.x() < b:
        edges |= Qt.Edge.LeftEdge
    elif pos.x() >= window.width() - b:
        edges |= Qt.Edge.RightEdge
    if pos.y() < b:
        edges |= Qt.Edge.TopEdge
    elif pos.y() >= window.height() - b:
        edges |= Qt.Edge.BottomEdge
    if edges and isinstance(window.childAt(pos), _CaptionButton):
        return Qt.Edge(0)          # the corner belongs to the close button
    return edges


def _on_title(window: QWidget, pos: QPoint) -> bool:
    """An empty part of the title strip (not one of its buttons)?"""
    widget = window.childAt(pos)
    return isinstance(widget, TitleBar)


_EDGE_CURSORS = {
    Qt.Edge.LeftEdge: Qt.CursorShape.SizeHorCursor,
    Qt.Edge.RightEdge: Qt.CursorShape.SizeHorCursor,
    Qt.Edge.TopEdge: Qt.CursorShape.SizeVerCursor,
    Qt.Edge.BottomEdge: Qt.CursorShape.SizeVerCursor,
    Qt.Edge.TopEdge | Qt.Edge.LeftEdge: Qt.CursorShape.SizeFDiagCursor,
    Qt.Edge.BottomEdge | Qt.Edge.RightEdge: Qt.CursorShape.SizeFDiagCursor,
    Qt.Edge.TopEdge | Qt.Edge.RightEdge: Qt.CursorShape.SizeBDiagCursor,
    Qt.Edge.BottomEdge | Qt.Edge.LeftEdge: Qt.CursorShape.SizeBDiagCursor,
}


class _FrameController(QObject):
    """Edge -> resize, title strip -> move, double-click strip -> maximise."""

    def __init__(self, window: QWidget) -> None:
        super().__init__(window)
        self._window = window
        self._edge_cursor = False
        # Resize cursor near the edges. Polled, because most widgets don't
        # report plain mouse moves.
        self._timer = QTimer(self)
        self._timer.setInterval(60)
        self._timer.timeout.connect(self._update_edge_cursor)
        self._timer.start()

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        window = self._window
        kind = event.type()
        if watched is window and kind in (QEvent.Type.WindowStateChange,
                                          QEvent.Type.ActivationChange, QEvent.Type.Resize):
            for bar in window.findChildren(TitleBar):
                bar.refresh()
            return False
        if kind not in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonDblClick):
            return False
        if not isinstance(watched, QWidget) or watched.window() is not window:
            return False
        if event.button() != Qt.MouseButton.LeftButton:
            return False
        pos = window.mapFromGlobal(event.globalPosition().toPoint())

        if kind == QEvent.Type.MouseButtonDblClick:
            if _on_title(window, pos):
                toggle_maximized(window)
                return True
            return False

        handle = window.windowHandle()
        edges = _edges_at(window, pos)
        if edges and handle is not None:
            handle.startSystemResize(edges)
            return True
        if _on_title(window, pos) and handle is not None:
            if is_maximized(window):
                self._restore_under_cursor(pos)
            handle.startSystemMove()
            return True
        return False

    def _restore_under_cursor(self, pos: QPoint) -> None:
        """Dragging a maximised window: restore it, keeping the cursor at the
        same relative spot of the strip (like any Windows app)."""
        window = self._window
        ratio = pos.x() / max(1, window.width())
        toggle_maximized(window)
        QApplication.processEvents()
        cursor = QCursor.pos()
        window.move(int(cursor.x() - ratio * window.width()), int(cursor.y() - pos.y()))

    def _update_edge_cursor(self) -> None:
        window = self._window
        shape = None
        if window.isVisible() and window.isActiveWindow() \
                and QApplication.mouseButtons() == Qt.MouseButton.NoButton \
                and QApplication.activePopupWidget() is None:
            pos = window.mapFromGlobal(QCursor.pos())
            if window.rect().contains(pos):
                edges = _edges_at(window, pos)
                shape = _EDGE_CURSORS.get(edges) if edges else None
        self._set_edge_cursor(shape)

    def _set_edge_cursor(self, shape) -> None:
        if shape is None:
            if self._edge_cursor:
                QGuiApplication.restoreOverrideCursor()
                self._edge_cursor = False
            return
        if self._edge_cursor:
            QGuiApplication.changeOverrideCursor(shape)
        else:
            QGuiApplication.setOverrideCursor(shape)
            self._edge_cursor = True


# ------------------------------------------------------------ Windows glue

def _polish_native(window: QWidget) -> None:
    """Minimise/restore by clicking the taskbar button, Win+Arrow, rounded
    corners on Windows 11. Best effort: failures leave a plain window."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        user32, dwmapi = ctypes.windll.user32, ctypes.windll.dwmapi
        hwnd = _hwnd(window)
        gwl_style = -16
        ws_sysmenu, ws_minimizebox, ws_maximizebox = 0x00080000, 0x00020000, 0x00010000
        get = getattr(user32, "GetWindowLongPtrW", user32.GetWindowLongW)
        put = getattr(user32, "SetWindowLongPtrW", user32.SetWindowLongW)
        get.restype = put.restype = ctypes.c_ssize_t
        get.argtypes = [ctypes.c_void_p, ctypes.c_int]
        put.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_ssize_t]
        put(hwnd, gwl_style, get(hwnd, gwl_style) | ws_sysmenu | ws_minimizebox | ws_maximizebox)
        corner = ctypes.c_int(2)                     # DWMWCP_ROUND
        dwmapi.DwmSetWindowAttribute(ctypes.c_void_p(hwnd), 33, ctypes.byref(corner),
                                     ctypes.sizeof(corner))
    except Exception as error:  # noqa: BLE001 - cosmetics only
        print(f"[window_frame] Windows extras skipped: {error}")


def install(window: QWidget) -> Optional[TitleBar]:
    """Swap the Windows title bar of this window for Akeso's. Returns the
    TitleBar to place at the top of the window, or None (normal Windows
    title bar) when not on Windows, switched off, or if anything fails."""
    global _active
    if not enabled():
        return None
    try:
        window.setWindowFlags(window.windowFlags() | Qt.WindowType.FramelessWindowHint)
        controller = _FrameController(window)
        QApplication.instance().installEventFilter(controller)
        window._frame_controller = controller        # keep it alive
        _polish_native(window)
        _active = True
        return TitleBar()
    except Exception as error:  # noqa: BLE001 - never stop the app over cosmetics
        print(f"[window_frame] Keeping the Windows title bar: {error}")
        window.setWindowFlags(window.windowFlags() & ~Qt.WindowType.FramelessWindowHint)
        return None
