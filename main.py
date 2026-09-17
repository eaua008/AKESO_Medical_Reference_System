import sys

from PySide6.QtWidgets import QApplication

from app.core.theme import Theme
from app.ui.main_window import MainWindow


def main() -> None:
    """Application entry point.

    A QApplication must exist before any widget is created. exec() starts
    the event loop that keeps the window alive until the user closes it.
    """
    app = QApplication(sys.argv)
    app.setStyleSheet(Theme.stylesheet())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()