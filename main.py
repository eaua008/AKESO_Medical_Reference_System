import sys

from PySide6.QtWidgets import QApplication

from app.core.preferences import PreferenceStore
from app.core.theme import Theme
from app.repositories.local_account_data import apply_pending_cache_clear
from app.ui.main_window import MainWindow
from app.ui.theme_scope import apply_app_stylesheet


def main() -> None:
    """Application entry point.

    A QApplication must exist before any widget is created. exec() starts
    the event loop that keeps the window alive until the user closes it.
    """
    # "Clear downloaded reference data" (Account > Privacy & data) runs
    # here, before anything has the cache files open.
    apply_pending_cache_clear()

    # Light or dark, as chosen last time (Settings or the sun/moon button).
    Theme.set_mode(PreferenceStore().load().theme)

    app = QApplication(sys.argv)
    apply_app_stylesheet()      # records which theme the app-level sheet is in

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
