"""80% / 90% for all of Akeso except the Body System Explorer's 3D view.

Why not Qt's own QT_SCALE_FACTOR: it shrinks EVERYTHING, including the
built-in browser engine that draws the 3D body, and that engine cannot draw
below 1 (it squeezed the 3D view and lagged in 1.0.2).

So for sizes under 100% Akeso shrinks its own widgets instead and leaves the
browser engine at its normal size (1):

    * every px in the style sheets (fonts, padding, radii, min sizes),
    * the sizes the code sets: margins, spacing, fixed / minimum / maximum
      widths and heights, icon sizes, fonts set in code,
    * pictures put in labels (icons, avatars, the logo).

The 3D page is a web page, not widgets, so none of this reaches it: it stays
at 100% while the sidebar, header and side panels around it are 80%.

install(0.8) must run right after QApplication exists and before any window
is built (main.py does it). With 1.0 (100% and up) nothing is changed.
"""

import math
import re
from typing import Optional

from PySide6.QtCore import QMargins, QSize, Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QBoxLayout,
    QFormLayout,
    QGridLayout,
    QLabel,
    QLayout,
    QWidget,
)

FACTOR = 1.0
_PX = re.compile(r"(?<![\w.#-])(\d+(?:\.\d+)?)px")
_HUGE = 10_000          # QWIDGETSIZE_MAX and other "no limit" values stay as they are
SNAPSHOT = 600          # px: pictures this big are widget snapshots, never shrunk
_ORIGINAL = {}          # (class, setter name) -> the unpatched Qt setter


def factor() -> float:
    return FACTOR


def px(value) -> int:
    """A size in px at the current factor (1 and 2 px lines stay crisp)."""
    if FACTOR == 1.0 or not isinstance(value, (int, float)):
        return value
    if abs(value) <= 2 or abs(value) >= _HUGE:
        return int(value)
    # Half rounds up (Python's round() sends 4.5 to 4): padding 5px at 90%
    # stays 5, so buttons keep their height relative to their corners.
    return int(math.floor(value * FACTOR + 0.5))


def _radius(value: float) -> int:
    """Corner radii round DOWN. Qt draws a box square when its radius is
    more than half its height, and text/padding don't shrink exactly by the
    factor, so a pill (radius = half its height at 100%) could lose its
    round corners at 90%. One px less keeps it a pill."""
    if value <= 2 or value >= _HUGE:
        return int(value)
    return max(1, int(math.floor(value * FACTOR)) - (1 if value >= 8 else 0))


_DECL = re.compile(r"([\w-]+)(\s*:\s*)([^;{}]*)")


def css(sheet: str) -> str:
    if FACTOR == 1.0 or not sheet or "px" not in sheet:
        return sheet

    def declaration(m):
        prop, colon, value = m.group(1), m.group(2), m.group(3)
        if "px" not in value:
            return m.group(0)
        size = _radius if "radius" in prop else px
        return prop + colon + _PX.sub(lambda n: f"{size(float(n.group(1)))}px", value)
    return _DECL.sub(declaration, sheet)


def _size_args(args):
    if len(args) == 1 and isinstance(args[0], QSize):
        size = args[0]
        return (QSize(px(size.width()), px(size.height())),)
    return tuple(px(a) for a in args)


def exact(obj, name: str, *args):
    """Call a setter WITHOUT the 80% shrink, for sizes the code measured from
    real widgets (already at the current size), e.g. a table's real height.
    Same as obj.<name>(*args) at 100%."""
    for cls in type(obj).__mro__:
        original = _ORIGINAL.get((cls, name))
        if original is not None:
            return original(obj, *args)
    return getattr(obj, name)(*args)


def _wrap(cls, name: str, convert) -> None:
    original = getattr(cls, name)
    _ORIGINAL[(cls, name)] = original

    def patched(self, *args):
        return original(self, *convert(args))
    patched.__name__ = name
    setattr(cls, name, patched)


def install(value: float, app: Optional[QApplication] = None) -> None:
    """Shrink Akeso's widgets by value (0.8 = 80%). Call once, early."""
    global FACTOR
    if value >= 1.0 or FACTOR != 1.0:
        return
    FACTOR = float(value)

    sizes = _size_args

    def margins(args):
        if len(args) == 1 and isinstance(args[0], QMargins):
            m = args[0]
            return (QMargins(px(m.left()), px(m.top()), px(m.right()), px(m.bottom())),)
        return tuple(px(a) for a in args)

    def first(args):
        return (px(args[0]),) + tuple(args[1:]) if args else args

    def second(args):       # (index, size)
        return (args[0], px(args[1])) + tuple(args[2:]) if len(args) >= 2 else args

    _wrap(QLayout, "setContentsMargins", margins)
    for cls in (QLayout, QBoxLayout, QGridLayout, QFormLayout):
        if "setSpacing" in cls.__dict__:
            _wrap(cls, "setSpacing", first)
    for cls in (QGridLayout, QFormLayout):
        _wrap(cls, "setHorizontalSpacing", first)
        _wrap(cls, "setVerticalSpacing", first)
    _wrap(QGridLayout, "setColumnMinimumWidth", second)
    _wrap(QGridLayout, "setRowMinimumHeight", second)
    _wrap(QBoxLayout, "addSpacing", first)
    _wrap(QBoxLayout, "insertSpacing", second)

    for name in ("setFixedSize", "setMinimumSize", "setMaximumSize"):
        _wrap(QWidget, name, sizes)
    for name in ("setFixedWidth", "setFixedHeight", "setMinimumWidth",
                 "setMinimumHeight", "setMaximumWidth", "setMaximumHeight"):
        _wrap(QWidget, name, first)
    _wrap(QAbstractButton, "setIconSize", sizes)

    _wrap(QFont, "setPixelSize", first)
    original_point = QFont.setPointSizeF

    def set_point_size_f(self, size):
        return original_point(self, size * FACTOR if size > 0 else size)
    QFont.setPointSizeF = set_point_size_f
    original_point_int = QFont.setPointSize

    def set_point_size(self, size):
        return original_point_int(self, max(1, int(round(size * FACTOR))) if size > 0 else size)
    QFont.setPointSize = set_point_size

    # Style sheets: every px, both the app-wide sheet and per-widget ones.
    original_widget_sheet = QWidget.setStyleSheet
    QWidget.setStyleSheet = lambda self, sheet: original_widget_sheet(self, css(sheet))
    original_app_sheet = QApplication.setStyleSheet
    QApplication.setStyleSheet = lambda self, sheet: original_app_sheet(self, css(sheet))

    # Pictures in labels (icons are drawn at their 100% size by the code).
    original_pixmap = QLabel.setPixmap

    def set_pixmap(self, pixmap):
        # Icons, avatars and logos are drawn at their 100% size, so they
        # shrink. Pictures of whole widgets (the sliding sheets' "ghost",
        # grab()) are already at the real size: shrinking those again showed
        # the page at 80% of its size while it slid in. Anything bigger than
        # SNAPSHOT px is such a picture and stays as it is.
        if (isinstance(pixmap, QPixmap) and not pixmap.isNull() and pixmap.width() > 2
                and max(pixmap.deviceIndependentSize().width(),
                        pixmap.deviceIndependentSize().height()) < SNAPSHOT):
            ratio = pixmap.devicePixelRatio() or 1.0
            pixmap = pixmap.scaled(
                max(1, round(pixmap.width() * FACTOR)), max(1, round(pixmap.height() * FACTOR)),
                Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            pixmap.setDevicePixelRatio(ratio)
        return original_pixmap(self, pixmap)
    _ORIGINAL[(QLabel, "setPixmap")] = original_pixmap
    QLabel.setPixmap = set_pixmap

    app = app or QApplication.instance()
    if app is not None:
        font = app.font()
        if font.pointSizeF() > 0:
            original_point(font, font.pointSizeF() * FACTOR)
        else:
            font.setPixelSize(font.pixelSize())          # (patched: scales)
        app.setFont(font)
