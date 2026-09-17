"""Vector icons drawn with QPainter.

Why not emoji? Because "\U0001F512" and friends are emoji codepoints, and
Windows renders them with a colour emoji font — which is why the padlock kept
showing up orange against a purple theme. The text variation selector (U+FE0E)
only sometimes overrides that, and never reliably across machines.

Drawing the shapes ourselves removes the font from the equation entirely:
one code path, correct colour every time, crisp at any size, and the icon
recolours with the theme instead of being stuck as whatever the emoji font
decided.

Everything uses QImage rather than QPixmap so icons can also be generated
before a QApplication exists (needed for the checkbox tick, which has to be
written to disk before the stylesheet string is built).
"""

from pathlib import Path
import tempfile

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPen, QPixmap

# All shapes are described on a 24x24 grid, then scaled to the requested size.
_GRID = 24.0
_SCALE = 2  # render at 2x so edges stay crisp on high-DPI screens


def _new_image(size: int) -> QImage:
    image = QImage(size * _SCALE, size * _SCALE, QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    return image


def _painter_for(image: QImage, size: int, color: str, width: float) -> QPainter:
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    factor = (size * _SCALE) / _GRID
    painter.scale(factor, factor)

    pen = QPen(QColor(color))
    pen.setWidthF(width)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    return painter


def _finish(image: QImage) -> QImage:
    image.setDevicePixelRatio(_SCALE)
    return image


# ---------------------------------------------------------- form field icons


def mail(size: int = 16, color: str = "#6B7280", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.drawRoundedRect(QRectF(2.5, 5, 19, 14), 2.5, 2.5)
    flap = QPainterPath()
    flap.moveTo(3, 6.5)
    flap.lineTo(12, 13)
    flap.lineTo(21, 6.5)
    p.drawPath(flap)
    p.end()
    return _finish(image)


def lock(size: int = 16, color: str = "#6B7280", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.drawRoundedRect(QRectF(4, 10.5, 16, 10.5), 2.5, 2.5)
    # Qt angles are 1/16th degree, counter-clockwise from 3 o'clock.
    p.drawArc(QRectF(7.5, 4, 9, 11), 0 * 16, 180 * 16)
    p.end()
    return _finish(image)


def user(size: int = 16, color: str = "#6B7280", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.drawEllipse(QPointF(12, 8), 4, 4)
    p.drawArc(QRectF(4.5, 13.5, 15, 15), 0 * 16, 180 * 16)
    p.end()
    return _finish(image)


def eye(size: int = 16, color: str = "#6B7280", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    path = QPainterPath()
    path.moveTo(2, 12)
    path.quadTo(12, 3.5, 22, 12)
    path.quadTo(12, 20.5, 2, 12)
    p.drawPath(path)
    p.drawEllipse(QPointF(12, 12), 3, 3)
    p.end()
    return _finish(image)


def check(size: int = 12, color: str = "#FFFFFF", width: float = 3.0) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    tick = QPainterPath()
    tick.moveTo(4.5, 12.5)
    tick.lineTo(9.5, 17.5)
    tick.lineTo(19.5, 6.5)
    p.drawPath(tick)
    p.end()
    return _finish(image)


# ------------------------------------------------------------- nav + header


def pulse(size: int = 20, color: str = "#FFFFFF", width: float = 2.0) -> QImage:
    """Heartbeat line — used for symptom checker."""
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    line = QPainterPath()
    line.moveTo(2, 12)
    line.lineTo(7, 12)
    line.lineTo(9.5, 5)
    line.lineTo(14.5, 19)
    line.lineTo(17, 12)
    line.lineTo(22, 12)
    p.drawPath(line)
    p.end()
    return _finish(image)


def grid(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    """Four panes — dashboard."""
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    for x, y in ((3, 3), (13, 3), (3, 13), (13, 13)):
        p.drawRoundedRect(QRectF(x, y, 8, 8), 1.5, 1.5)
    p.end()
    return _finish(image)


def book(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    """Open book — encyclopedia."""
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    path = QPainterPath()
    path.moveTo(12, 6.5)
    path.quadTo(7, 3.5, 3, 5)
    path.lineTo(3, 19)
    path.quadTo(7, 17.5, 12, 20.5)
    path.quadTo(17, 17.5, 21, 19)
    path.lineTo(21, 5)
    path.quadTo(17, 3.5, 12, 6.5)
    p.drawPath(path)
    p.drawLine(QPointF(12, 6.5), QPointF(12, 20.5))
    p.end()
    return _finish(image)


def search(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.drawEllipse(QPointF(10.5, 10.5), 6.5, 6.5)
    p.drawLine(QPointF(15.5, 15.5), QPointF(20.5, 20.5))
    p.end()
    return _finish(image)


def pill(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.save()
    p.translate(12, 12)
    p.rotate(-45)
    p.translate(-12, -12)
    p.drawRoundedRect(QRectF(4, 8.5, 16, 7), 3.5, 3.5)
    p.drawLine(QPointF(12, 8.5), QPointF(12, 15.5))
    p.restore()
    p.end()
    return _finish(image)


def heart(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    path = QPainterPath()
    path.moveTo(12, 20)
    path.cubicTo(2, 13.5, 4, 5, 8.5, 5)
    path.cubicTo(10.8, 5, 12, 7, 12, 8.2)
    path.cubicTo(12, 7, 13.2, 5, 15.5, 5)
    path.cubicTo(20, 5, 22, 13.5, 12, 20)
    p.drawPath(path)
    p.end()
    return _finish(image)


def notebook(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.drawRoundedRect(QRectF(5.5, 3, 14, 18), 2, 2)
    p.drawLine(QPointF(9.5, 3), QPointF(9.5, 21))
    for y in (8, 12, 16):
        p.drawLine(QPointF(12.5, y), QPointF(16.5, y))
    p.end()
    return _finish(image)


def clock(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.drawEllipse(QPointF(12, 12), 8.5, 8.5)
    p.drawLine(QPointF(12, 7), QPointF(12, 12))
    p.drawLine(QPointF(12, 12), QPointF(15.5, 14))
    p.end()
    return _finish(image)


def leaf(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    path = QPainterPath()
    path.moveTo(4, 20)
    path.quadTo(4, 5, 20, 4)
    path.quadTo(21, 18, 7, 18.5)
    path.quadTo(6, 18.5, 4, 20)
    p.drawPath(path)
    p.drawLine(QPointF(7, 18), QPointF(18, 7))
    p.end()
    return _finish(image)


def alert(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    tri = QPainterPath()
    tri.moveTo(12, 3.5)
    tri.lineTo(22, 20)
    tri.lineTo(2, 20)
    tri.closeSubpath()
    p.drawPath(tri)
    p.drawLine(QPointF(12, 10), QPointF(12, 14.5))
    p.drawPoint(QPointF(12, 17.3))
    p.end()
    return _finish(image)


def stack(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    """Stacked sheets — articles."""
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.drawRoundedRect(QRectF(3, 13, 18, 7), 1.5, 1.5)
    p.drawLine(QPointF(5, 10), QPointF(19, 10))
    p.drawLine(QPointF(7, 6.5), QPointF(17, 6.5))
    p.end()
    return _finish(image)


def star(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    path = QPainterPath()
    pts = [
        (12, 3), (14.6, 9.2), (21, 9.7), (16.2, 14.1),
        (17.7, 20.5), (12, 17.1), (6.3, 20.5), (7.8, 14.1),
        (3, 9.7), (9.4, 9.2),
    ]
    path.moveTo(*pts[0])
    for pt in pts[1:]:
        path.lineTo(*pt)
    path.closeSubpath()
    p.drawPath(path)
    p.end()
    return _finish(image)


def bell(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    path = QPainterPath()
    path.moveTo(5.5, 17)
    path.lineTo(5.5, 11)
    path.quadTo(5.5, 4.5, 12, 4.5)
    path.quadTo(18.5, 4.5, 18.5, 11)
    path.lineTo(18.5, 17)
    path.closeSubpath()
    p.drawPath(path)
    p.drawArc(QRectF(9.5, 17, 5, 4), 180 * 16, 180 * 16)
    p.end()
    return _finish(image)


def gear(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.drawEllipse(QPointF(12, 12), 3.5, 3.5)
    p.drawEllipse(QPointF(12, 12), 7.5, 7.5)
    import math
    for i in range(8):
        angle = math.radians(i * 45)
        x1 = 12 + 7.5 * math.cos(angle)
        y1 = 12 + 7.5 * math.sin(angle)
        x2 = 12 + 10 * math.cos(angle)
        y2 = 12 + 10 * math.sin(angle)
        p.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    p.end()
    return _finish(image)


def shield(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    path = QPainterPath()
    path.moveTo(12, 3)
    path.lineTo(20, 6.5)
    path.lineTo(20, 12)
    path.quadTo(20, 18.5, 12, 21.5)
    path.quadTo(4, 18.5, 4, 12)
    path.lineTo(4, 6.5)
    path.closeSubpath()
    p.drawPath(path)
    p.end()
    return _finish(image)


def moon(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    path = QPainterPath()
    path.moveTo(19, 14.5)
    path.quadTo(11, 18, 8, 11)
    path.quadTo(6.5, 6, 11.5, 3.5)
    path.quadTo(3, 5, 4.5, 13.5)
    path.quadTo(6.5, 22, 15, 20.5)
    path.quadTo(18, 19.5, 19, 14.5)
    p.drawPath(path)
    p.end()
    return _finish(image)


def sun(size: int = 18, color: str = "#9CA3AF", width: float = 1.8) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    p.drawEllipse(QPointF(12, 12), 4.5, 4.5)
    import math
    for i in range(8):
        angle = math.radians(i * 45)
        x1 = 12 + 7 * math.cos(angle)
        y1 = 12 + 7 * math.sin(angle)
        x2 = 12 + 9.8 * math.cos(angle)
        y2 = 12 + 9.8 * math.sin(angle)
        p.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    p.end()
    return _finish(image)


def chevron_right(size: int = 14, color: str = "#9CA3AF", width: float = 2.0) -> QImage:
    image = _new_image(size)
    p = _painter_for(image, size, color, width)
    path = QPainterPath()
    path.moveTo(9, 5)
    path.lineTo(16, 12)
    path.lineTo(9, 19)
    p.drawPath(path)
    p.end()
    return _finish(image)


def pin(size: int = 14, color: str = "#9CA3AF", width: float = 1.7) -> QImage:
    """Pushpin, pointing down — the pinned state."""
    image = _new_image(size)
    p = _painter_for(image, size, color, width)

    head = QPainterPath()
    head.moveTo(9, 3.5)
    head.lineTo(15, 3.5)
    head.lineTo(14, 9)
    head.lineTo(17.5, 12.5)
    head.lineTo(6.5, 12.5)
    head.lineTo(10, 9)
    head.closeSubpath()
    p.drawPath(head)
    p.drawLine(QPointF(12, 12.5), QPointF(12, 20.5))

    p.end()
    return _finish(image)


def pin_off(size: int = 14, color: str = "#9CA3AF", width: float = 1.7) -> QImage:
    """Pushpin with a slash — the unpinned state."""
    image = _new_image(size)
    p = _painter_for(image, size, color, width)

    head = QPainterPath()
    head.moveTo(9, 3.5)
    head.lineTo(15, 3.5)
    head.lineTo(14, 9)
    head.lineTo(17.5, 12.5)
    head.lineTo(6.5, 12.5)
    head.lineTo(10, 9)
    head.closeSubpath()
    p.drawPath(head)
    p.drawLine(QPointF(12, 12.5), QPointF(12, 20.5))
    p.drawLine(QPointF(3.5, 3.5), QPointF(20.5, 20.5))

    p.end()
    return _finish(image)


# Lookup used by the sidebar so nav config can stay pure data.
NAV_ICONS = {
    "grid": grid,
    "pulse": pulse,
    "book": book,
    "search": search,
    "pill": pill,
    "heart": heart,
    "notebook": notebook,
    "clock": clock,
    "leaf": leaf,
    "alert": alert,
    "stack": stack,
    "star": star,
    "bell": bell,
    "gear": gear,
    "shield": shield,
    "user": user,
}


def draw(name: str, size: int = 18, color: str = "#9CA3AF") -> QImage:
    """Render an icon by name; falls back to a dot if the name is unknown."""
    fn = NAV_ICONS.get(name)
    if fn is None:
        image = _new_image(size)
        p = _painter_for(image, size, color, 2.0)
        p.drawPoint(QPointF(12, 12))
        p.end()
        return _finish(image)
    return fn(size=size, color=color)


# ------------------------------------------------------- helpers for widgets


def to_pixmap(image: QImage) -> QPixmap:
    """QLabel.setPixmap needs a QPixmap; keeps the 2x scaling intact."""
    pixmap = QPixmap.fromImage(image)
    pixmap.setDevicePixelRatio(_SCALE)
    return pixmap


_CACHE_DIR = Path(tempfile.gettempdir()) / "akeso_icons"


def checkmark_file(color: str = "#FFFFFF") -> str:
    """Write the tick to disk and return its path.

    Qt stylesheets can only reference images by file path — there is no
    support for inline or data-URI images — so the checkbox tick has to
    exist as a real file before the stylesheet is assembled.
    """
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _CACHE_DIR / f"check_{color.lstrip('#')}.png"
    if not path.exists():
        check(color=color).save(str(path))
    # Qt stylesheets want forward slashes, even on Windows.
    return str(path).replace("\\", "/")