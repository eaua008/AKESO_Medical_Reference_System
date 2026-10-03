"""Profile photos: crop to a square, shrink, and draw as a circle.

Photos are re-encoded here before upload. That keeps them small (256 px,
well under the bucket's 1 MB limit) and strips whatever else the original
file carried, such as camera and location (EXIF) data.
"""

from typing import Optional

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPainterPath, QPixmap

AVATAR_SIZE = 256


class AvatarImageError(Exception):
    pass


def prepare_avatar(path: str) -> bytes:
    """Load an image file and return a square 256 px PNG."""
    image = QImage(path)
    if image.isNull():
        raise AvatarImageError("That file is not an image Akeso can read.")
    side = min(image.width(), image.height())
    if side < 32:
        raise AvatarImageError("That image is too small. Use one at least 32 pixels wide.")
    left = (image.width() - side) // 2
    top = (image.height() - side) // 2
    square = image.copy(left, top, side, side).scaled(
        AVATAR_SIZE, AVATAR_SIZE, Qt.AspectRatioMode.IgnoreAspectRatio,
        Qt.TransformationMode.SmoothTransformation)
    square = square.convertToFormat(QImage.Format.Format_ARGB32)

    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    square.save(buffer, "PNG")
    buffer.close()
    return bytes(data)


def circle_pixmap(png: Optional[bytes], size: int, initial: str,
                  fill: str, text_color: str) -> QPixmap:
    """The photo in a circle, or the first letter of the name if none."""
    scale = 2
    canvas = QPixmap(size * scale, size * scale)
    canvas.fill(Qt.GlobalColor.transparent)
    painter = QPainter(canvas)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    clip = QPainterPath()
    clip.addEllipse(QRectF(0, 0, size * scale, size * scale))
    painter.setClipPath(clip)

    image = QImage.fromData(png) if png else QImage()
    if not image.isNull():
        painter.drawImage(QRectF(0, 0, size * scale, size * scale), image)
    else:
        painter.fillRect(0, 0, size * scale, size * scale, QColor(fill))
        font = QFont()
        font.setPixelSize(int(size * scale * 0.42))
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(text_color))
        painter.drawText(QRectF(0, 0, size * scale, size * scale),
                         Qt.AlignmentFlag.AlignCenter, (initial[:1] or "?").upper())
    painter.end()
    canvas.setDevicePixelRatio(scale)
    return canvas
