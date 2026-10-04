import os
import sys

# First, before anything that could fail: errors get a message box and a log
# file instead of silently closing the packaged .exe (it has no console).
from app.core import crash_report
crash_report.install()

from PySide6.QtCore import QCoreApplication, Qt, qInstallMessageHandler  # noqa: E402
from PySide6.QtGui import QIcon  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from app.core.paths import resource  # noqa: E402
from app.core.preferences import PreferenceStore  # noqa: E402
from app.core.theme import Theme  # noqa: E402
from app.repositories.local_account_data import apply_pending_cache_clear  # noqa: E402
from app.ui.main_window import MainWindow  # noqa: E402
from app.ui.theme_scope import apply_app_stylesheet  # noqa: E402


_previous_handler = None


def _qt_messages(mode, context, message) -> None:
    """Drop one harmless Qt-on-Windows warning, pass everything else on.

    Our stylesheets size text in pixels (font-size: 13px). On Windows, Qt
    then sometimes asks such a font for its point size, gets -1 ("no point
    size, it's a pixel font") and prints this line. Nothing is wrong with
    the text, so the line is only noise in the terminal.
    """
    if "QFont::setPointSize: Point size <= 0" in message:
        return
    if _previous_handler is not None:
        _previous_handler(mode, context, message)
    else:
        print(message, file=sys.stderr)


def main() -> None:
    """Application entry point.

    A QApplication must exist before any widget is created. exec() starts
    the event loop that keeps the window alive until the user closes it.
    """
    # "Clear downloaded reference data" (Account > Privacy & data) runs
    # here, before anything has the cache files open.
    apply_pending_cache_clear()

    global _previous_handler
    _previous_handler = qInstallMessageHandler(_qt_messages)

    # Light or dark, as chosen last time (Settings or the sun/moon button).
    prefs = PreferenceStore().load()
    Theme.set_mode(prefs.theme)
    Theme.set_color_theme(prefs.color_theme)      # Dracula, Catppuccin... (Settings)

    # Display size (Settings > Display). Qt reads this once, before the
    # application exists, and scales everything by it. A QT_SCALE_FACTOR
    # already set outside Akeso (for testing, say) wins.
    if prefs.ui_scale != 100 and "QT_SCALE_FACTOR" not in os.environ:
        os.environ["QT_SCALE_FACTOR"] = f"{prefs.ui_scale / 100:g}"
    # Cards per row in the encyclopedias (Settings > Display).
    from app.ui.components.fluid import ResponsiveGrid
    ResponsiveGrid.set_user_columns(prefs.cards_per_row)

    # The built-in reference browser (QtWebEngine) loads on the first link
    # click; Qt needs this set before the application exists for that.
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    # Only fatal errors from the browser engine itself in the terminal
    # (not every website's blocked request). Must be set before it starts.
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--log-level=3")

    # The Body System Explorer's 3D page is served from akeso://anatomy/;
    # the browser engine must learn that address before the app exists.
    from app.ui.components.anatomy_scheme import register_scheme
    register_scheme()

    if sys.platform == "win32":
        # Its own taskbar entry and icon, even when started as python main.py.
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Akeso.Desktop")
        except (AttributeError, OSError):
            pass
    app = QApplication(sys.argv)
    app.setApplicationName("Akeso")
    icon = resource("assets", "akeso.ico")
    if icon.exists():
        app.setWindowIcon(QIcon(str(icon)))      # title bar, taskbar, Alt+Tab
    # No hover box when it would only repeat the label you can already see.
    from app.core import tooltip_filter
    tooltip_filter.install()
    apply_app_stylesheet()      # records which theme the app-level sheet is in

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
