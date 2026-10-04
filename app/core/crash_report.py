"""Show a readable message, and keep a log, when Akeso hits an unexpected error.

The packaged Akeso.exe has no console window, so an error that would print
a traceback in IntelliJ would otherwise close the app (or do nothing) with
no explanation. Installed first thing in main.py, this:

  * writes the full error to %LOCALAPPDATA%\\Akeso\\akeso_crash.log
    (newest at the bottom, trimmed so it never grows past ~200 KB),
  * shows a short message box with where that log is,
  * keeps the app running when the error happened inside a button click
    or similar (Qt keeps going after the hook returns).

It never sends anything anywhere.
"""

import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

MAX_LOG_BYTES = 200_000
_showing = False
_apps: list = []                 # keeps an emergency QApplication alive


def log_path() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / ".local" / "share")
    return Path(base) / "Akeso" / "akeso_crash.log"


def _write(text: str) -> None:
    try:
        path = log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        old = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        combined = (old + text)[-MAX_LOG_BYTES:]
        path.write_text(combined, encoding="utf-8")
    except OSError:
        pass


def _message(summary: str) -> None:
    global _showing
    if _showing:                     # one box at a time, never a cascade
        return
    _showing = True
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        if QApplication.instance() is None:        # failed before the app existed
            _apps.append(QApplication(sys.argv))
        QMessageBox.critical(
            None, "Akeso ran into a problem",
            f"{summary}\n\nDetails were saved to:\n{log_path()}\n\n"
            "If Akeso stops working, close it and open it again.")
    except Exception:  # noqa: BLE001 - a broken Qt must not hide the log
        pass
    finally:
        _showing = False


def _hook(kind, value, tb) -> None:
    if issubclass(kind, KeyboardInterrupt):
        sys.__excepthook__(kind, value, tb)
        return
    details = "".join(traceback.format_exception(kind, value, tb))
    _write(f"\n===== {datetime.now():%Y-%m-%d %H:%M:%S} =====\n{details}")
    if sys.stderr is not None:                 # IntelliJ console still shows it
        try:
            sys.stderr.write(details)
        except Exception:  # noqa: BLE001
            pass
    _message(f"{kind.__name__}: {value}"[:400])


def install() -> None:
    sys.excepthook = _hook
