"""How small Akeso may be drawn on this screen (Settings > Display > Size).

Qt can draw the whole app smaller than normal (QT_SCALE_FACTOR below 1), but
the built-in browser engine cannot: below 1 it prints "Unsupported scale
factor" and draws its pages at the wrong size. Those pages include the Body
System Explorer's 3D view and the reference browser, so the 3D body ended up
squeezed into a corner and clicks landed in the wrong place.

Version 1.0.2 still allowed 80% on screens with Windows scaling at 125%
(125% × 80% = 100% in the end), but the browser engine checks Akeso's own
size, not the final one, so the 3D view broke there too and every redraw got
slower. So Akeso is never drawn below 100% now, on any screen; Settings only
offers 100%, 110% and 125%.
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
    """The size Akeso actually uses for a chosen one: never below 100%."""
    return max(chosen, 100)


def qt_scale_factor(chosen: int) -> float:
    return effective_percent(chosen) / 100
