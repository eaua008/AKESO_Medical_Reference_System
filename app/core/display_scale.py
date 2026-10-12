"""How big Akeso is drawn (Settings > Display > Size), including 80% and 90%.

The problem with sizes below 100%: Qt can draw the whole app smaller
(QT_SCALE_FACTOR below 1), but the built-in browser engine cannot. Below 1 it
prints "Unsupported scale factor" and draws its pages at the wrong size. That
is the Body System Explorer's 3D view (and the reference browser), which in
1.0.2 ended up squeezed into a corner with clicks landing in the wrong place.

How 80% / 90% work now: Qt stays at its normal size and Akeso shrinks its
own widgets (app/core/soft_scale.py). The sidebar, header, pages and side
panels are 80%, while the Body System Explorer's 3D view (a web page) keeps
its own size of 1, on every screen.
"""

import sys


def windows_scaling() -> float:
    """Windows display scaling of the main screen: 1.0 = 100%, 1.25 = 125%.

    Read from the registry because Qt (which knows the real value) does not
    exist yet when main.py decides the size. Anything unexpected = 100%.
    """
    if sys.platform != "win32":
        return 1.0
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Control Panel\Desktop\WindowMetrics") as key:
            dpi, _kind = winreg.QueryValueEx(key, "AppliedDPI")
        dpi = int(dpi)
    except (OSError, ValueError, TypeError):
        return 1.0
    return dpi / 96 if 96 <= dpi <= 480 else 1.0


def smallest_percent(scaling: float = 0.0) -> int:
    """80% and 90% work on every screen now (soft_scale.py)."""
    return 80


def effective_percent(chosen: int, scaling: float = 0.0) -> int:
    return chosen


def qt_environment(chosen: int, scaling: float = 0.0) -> dict:
    """Qt settings for a chosen size. Under 100% Qt is left at its normal size:
    Akeso shrinks its own widgets instead (app/core/soft_scale.py), so the
    3D explorer's browser engine keeps a factor of exactly 1."""
    if chosen > 100:
        return {"QT_SCALE_FACTOR": f"{chosen / 100:g}"}
    return {}


def soft_factor(chosen: int) -> float:
    """What soft_scale.install() gets: 0.8 for 80%, 1.0 for 100% and up."""
    return chosen / 100 if chosen < 100 else 1.0


def qt_scale_factor(chosen: int) -> float:
    """Kept for older callers."""
    return max(chosen, 100) / 100


# Environment names main.py may set, so a restart can clear them all.
QT_KEYS = ("QT_ENABLE_HIGHDPI_SCALING", "QT_SCALE_FACTOR", "QT_FONT_DPI", "AKESO_UI_SCALE")
