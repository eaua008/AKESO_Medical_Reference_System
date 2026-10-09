"""How small Akeso may be drawn on this screen (Settings > Display > Size).

Qt can draw the whole app smaller than normal (QT_SCALE_FACTOR below 1), but
the built-in browser engine cannot: below 1 it prints "Unsupported scale
factor" and draws its pages at the wrong size. Those pages include the Body
System Explorer's 3D view and the reference browser, so the 3D body ended up
squeezed into a corner and clicks landed in the wrong place.

What matters is the final size: Windows display scaling × Akeso's size. On a
screen set to 125%, Akeso at 80% is 125% × 80% = 100%, which is fine. On a
screen at 100%, anything under 100% is not, so Akeso stays at 100% there.
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


def smallest_percent() -> int:
    """The smallest Akeso size that keeps the browser engine working here."""
    return round(100 / windows_scaling())


def effective_percent(chosen: int) -> int:
    """The size Akeso actually uses for a chosen one (never below the floor)."""
    return max(chosen, min(100, smallest_percent()))


def qt_scale_factor(chosen: int) -> float:
    return effective_percent(chosen) / 100
