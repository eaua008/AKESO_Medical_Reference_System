"""Image assets: locating them on disk and serving the right one per theme.

Naming warning, because it reads backwards:

    LIGHTLOGO.png  has LIGHT (white/pale) lettering  -> use on the DARK theme
    DARKLOGO.png   has DARK (navy) lettering         -> use on the LIGHT theme

The filename describes the ink, not the background it belongs on. So
logo_for_theme() deliberately returns LIGHTLOGO when the app is in dark mode.
If that ever looks like a bug, it isn't.
"""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from app.core.theme import Theme

# app/core/assets.py -> app/core -> app -> <project root>
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"

LIGHT_INK_LOGO = ASSETS_DIR / "LIGHTLOGO.png"   # for dark backgrounds
DARK_INK_LOGO = ASSETS_DIR / "DARKLOGO.png"     # for light backgrounds

_cache: dict[tuple[str, int], QPixmap] = {}


def logo_path_for_theme() -> Path:
    return LIGHT_INK_LOGO if Theme.mode() == "dark" else DARK_INK_LOGO


def logo_pixmap(height: int = 30) -> QPixmap:
    """Return the themed logo scaled to a target height.

    The source art is 2170x725 (roughly 3:1), so width follows from height
    automatically. Results are cached because this gets called on every
    theme switch and the scaling is not free.

    Returns an empty QPixmap if the file is missing, so a misplaced asset
    degrades to "no logo" instead of crashing the app on startup.
    """
    path = logo_path_for_theme()
    key = (str(path), height)

    if key in _cache:
        return _cache[key]

    if not path.exists():
        print(f"[assets] Logo not found: {path}")
        return QPixmap()

    pixmap = QPixmap(str(path))
    if pixmap.isNull():
        print(f"[assets] Could not decode logo: {path}")
        return QPixmap()

    scaled = pixmap.scaledToHeight(
        height * 2,  # render at 2x, then hand Qt the device pixel ratio
        Qt.TransformationMode.SmoothTransformation,
        )
    scaled.setDevicePixelRatio(2)

    _cache[key] = scaled
    return scaled


def clear_cache() -> None:
    """Drop cached pixmaps. Call if logo files are replaced at runtime."""
    _cache.clear()