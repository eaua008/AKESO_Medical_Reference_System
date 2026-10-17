"""Getting a picture ready for a study group chat (migration 045).

What happens to a picture before it leaves the computer:

  * it must really decode as PNG or JPEG (the file name doesn't count);
  * camera rotation is applied, then the picture is RE-ENCODED from its
    pixels. That drops every kind of metadata: GPS location, camera and
    phone model, date, thumbnails, comments;
  * it is scaled down to at most 2048 pixels on its long side;
  * it must come out at 5 MB or less (it is compressed harder, then
    scaled further, before giving up).

No Qt widgets here, so it can run on a worker thread.
"""

import uuid
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PySide6.QtGui import QImage, QImageReader

from app.models.social import IMAGE_MAX_BYTES

MAX_SIDE = 2048
MAX_SOURCE_BYTES = 40 * 1024 * 1024          # don't even try to open something huge
FORMATS = {b"png": ("png", "image/png"), b"jpeg": ("jpg", "image/jpeg"), b"jpg": ("jpg", "image/jpeg")}


class PictureError(ValueError):
    """Something to tell the user instead of sending."""


@dataclass
class Prepared:
    data: bytes
    ext: str                 # png | jpg
    mime: str
    width: int
    height: int

    def new_path(self, group_id: str, user_id: str) -> str:
        """<group>/<sender>/<random>.<ext>, the shape the database accepts."""
        return f"{group_id}/{user_id}/{uuid.uuid4().hex}.{self.ext}"


def _encode(image: QImage, fmt: str, quality: int) -> bytes:
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, fmt.upper(), quality)
    buffer.close()
    return bytes(data)


def prepare(file_path: str) -> Prepared:
    path = Path(file_path)
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise PictureError("Couldn't open that file.") from exc
    if size == 0:
        raise PictureError("That file is empty.")
    if size > MAX_SOURCE_BYTES:
        raise PictureError("That picture is far too large. Choose one under 40 MB.")
    reader = QImageReader(str(path))
    reader.setAutoTransform(True)                    # honour the camera's rotation
    fmt = bytes(reader.format()).lower()
    if fmt not in FORMATS:
        raise PictureError("Only PNG and JPEG pictures can be sent.")
    image = reader.read()
    if image.isNull():
        raise PictureError("That picture couldn't be read. Is the file damaged?")

    ext, mime = FORMATS[fmt]
    side = MAX_SIDE
    for attempt in range(4):
        scaled = image
        if max(image.width(), image.height()) > side:
            from PySide6.QtCore import Qt
            scaled = image.scaled(side, side, Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation)
        if ext == "png":
            data = _encode(scaled, "png", -1)
            if len(data) > IMAGE_MAX_BYTES:             # too big as PNG: send it as JPEG
                flat = QImage(scaled.size(), QImage.Format.Format_RGB32)
                flat.fill(0xFFFFFFFF)
                from PySide6.QtGui import QPainter
                painter = QPainter(flat)
                painter.drawImage(0, 0, scaled)
                painter.end()
                data, ext, mime = _encode(flat, "jpeg", 85), "jpg", "image/jpeg"
        else:
            data = _encode(scaled, "jpeg", 85 if attempt < 2 else 70)
        if data and len(data) <= IMAGE_MAX_BYTES:
            return Prepared(data, ext, mime, scaled.width(), scaled.height())
        side = int(side * 0.75)
    raise PictureError("That picture is still over 5 MB after shrinking it. Choose a smaller one.")
