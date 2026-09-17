"""Standalone preview for the header and sidebar.

Run from the project root with the venv active:

    python -m app.ui.shell_preview

Shows the chrome with a placeholder content area, so layout, hover
behaviour and theme switching can be checked without booting Supabase or
any of the real views.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from app.core.theme import Theme
from app.ui.components.header import AkesoHeader
from app.ui.components.sidebar import AkesoSidebarNav


class ShellPreview(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akeso — shell preview")
        self.resize(1480, 920)

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.header = AkesoHeader(user_name="Eijkim")
        root_layout.addWidget(self.header)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.sidebar = AkesoSidebarNav(active_tab="dashboard")
        body_layout.addWidget(self.sidebar)

        self.content = QLabel("Dashboard Overview")
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content.setObjectName("heroTitle")
        body_layout.addWidget(self.content, 1)

        root_layout.addWidget(body, 1)
        self.setCentralWidget(root)

        self.sidebar.tabChanged.connect(self._on_tab)
        self.header.themeToggled.connect(self._on_theme)

    def _on_tab(self, tab_id: str) -> None:
        self.content.setText(tab_id.replace("-", " ").title())

    def _on_theme(self, _is_dark: bool) -> None:
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(Theme.stylesheet())
        # Stylesheets reapply themselves; hand-drawn pixmaps do not.
        self.header.refresh_theme()
        self.sidebar.refresh_theme()


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(Theme.stylesheet())
    window = ShellPreview()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())