"""Small profile photos next to names (Clinical Exchange posts and replies).

One shared cache: each photo is downloaded once per session, on a
background thread, and every label waiting for it is filled in when it
arrives. Until then (and for people without a photo, or who keep it
hidden) the label shows the first letter of their name in a circle.

The database decides whose photo a viewer may see (ex_author in migration
013 only sends avatar_path when the profile and its "Show my photo"
switch allow it), so this module never decides anything about privacy.
"""

from typing import Callable, Optional

from PySide6.QtWidgets import QLabel

from app.core.avatar_image import circle_pixmap
from app.core.background import call_in_background
from app.core.theme import Theme

try:
    from shiboken6 import isValid as _alive
except ImportError:                                    # pragma: no cover
    def _alive(_obj) -> bool:
        return True


class AvatarCache:
    loader: Optional[Callable[[str], Optional[bytes]]] = None   # set by the shell
    _photos: dict[str, Optional[bytes]] = {}
    _waiting: dict[str, list[tuple[QLabel, str, int]]] = {}

    @classmethod
    def apply(cls, target: QLabel, path: Optional[str], name: str, size: int) -> None:
        """Show name's initial now; swap in the photo once it is here."""
        cls._paint(target, None, name, size)
        if not path or cls.loader is None:
            return
        if path in cls._photos:
            cls._paint(target, cls._photos[path], name, size)
            return
        queue = cls._waiting.setdefault(path, [])
        queue.append((target, name, size))
        if len(queue) > 1:
            return                                     # already downloading
        loader = cls.loader
        call_in_background(lambda: loader(path), lambda data: cls._arrived(path, data),
                           lambda _m: cls._arrived(path, None))

    @classmethod
    def _arrived(cls, path: str, data: Optional[bytes]) -> None:
        cls._photos[path] = data or None
        for target, name, size in cls._waiting.pop(path, []):
            if _alive(target):
                cls._paint(target, data, name, size)

    @staticmethod
    def _paint(target: QLabel, data: Optional[bytes], name: str, size: int) -> None:
        if not _alive(target):
            return
        target.setFixedSize(size, size)
        target.setPixmap(circle_pixmap(data, size, name, Theme.token("PRIMARY"), "#FFFFFF"))

    @classmethod
    def clear(cls) -> None:
        """Signing out: forget the photos and stop loading new ones."""
        cls.loader = None
        cls._photos.clear()
        cls._waiting.clear()
