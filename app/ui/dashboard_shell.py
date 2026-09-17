"""The application shell: header, sidebar, and a swappable content area.

Screens are plugged in with register_view(). Anything not yet built shows a
placeholder, so every nav item leads somewhere instead of nothing.

Run it on its own:

    python -m app.ui.dashboard_shell
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.controllers.disease_controller import DiseaseController
from app.core.theme import Theme
from app.ui.components.header import AkesoHeader
from app.ui.components.sidebar import NAV_SECTIONS, AkesoSidebarNav
from app.ui.views.disease_encyclopedia_view import DiseaseEncyclopediaView


class PlaceholderView(QWidget):
    """Stand-in for a screen that has not been built yet."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.setObjectName("panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(8)
        layout.addStretch(1)

        heading = QLabel(title)
        heading.setObjectName("cardTitle")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        note = QLabel("Not built yet")
        note.setObjectName("cardSubtitle")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(heading)
        layout.addWidget(note)
        layout.addStretch(1)


class DashboardShell(QWidget):
    """Header + sidebar + swappable content area."""

    def __init__(
            self,
            user_name: str = "User",
            role: str = "user",
            start_tab: str = "dashboard",
    ) -> None:
        super().__init__()
        self.setObjectName("panel")

        self._pages: dict[str, QWidget] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.header = AkesoHeader(user_name=user_name)
        root.addWidget(self.header)

        body = QWidget()
        body.setObjectName("panel")
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.sidebar = AkesoSidebarNav(active_tab=start_tab, role=role)
        body_layout.addWidget(self.sidebar)

        self.content = QStackedWidget()
        body_layout.addWidget(self.content, 1)

        root.addWidget(body, 1)

        self._build_placeholders()
        self.sidebar.tabChanged.connect(self.show_tab)
        self.header.themeToggled.connect(self._on_theme_changed)
        self.header.navigationRequested.connect(self.show_tab)

        self._register_real_views()
        self.show_tab(start_tab)

    # -------------------------------------------------------------- pages

    def _build_placeholders(self) -> None:
        """One placeholder per nav item, read from the same NAV_SECTIONS the
        sidebar uses, so a new nav entry automatically leads somewhere.
        """
        for section in NAV_SECTIONS:
            for item in section["items"]:
                page = PlaceholderView(item["label"])
                self._pages[item["id"]] = page
                self.content.addWidget(page)

    def _register_real_views(self) -> None:
        """Swap built screens in for their placeholders.

        Each new screen adds three lines here and nothing else.
        """
        self.encyclopedia_view = DiseaseEncyclopediaView()
        self.disease_controller = DiseaseController(self.encyclopedia_view)
        self.register_view("diseases", self.encyclopedia_view)

    def register_view(self, tab_id: str, widget: QWidget) -> None:
        old = self._pages.get(tab_id)
        if old is not None:
            self.content.removeWidget(old)
            old.deleteLater()

        self._pages[tab_id] = widget
        self.content.addWidget(widget)

        if self.sidebar.active_tab == tab_id:
            self.content.setCurrentWidget(widget)

    def show_tab(self, tab_id: str) -> None:
        page = self._pages.get(tab_id)
        if page is None:
            return

        self.content.setCurrentWidget(page)

        # The sidebar's select_tab emits tabChanged, which is wired back to
        # this method — calling it directly would recurse forever. Blocking
        # signals moves the highlight (needed when navigation comes from the
        # header) without the echo.
        self.sidebar.blockSignals(True)
        self.sidebar.select_tab(tab_id)
        self.sidebar.blockSignals(False)

    # -------------------------------------------------------------- theme

    def _on_theme_changed(self, _is_dark: bool) -> None:
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(Theme.stylesheet())
        # Stylesheets reapply themselves; hand-drawn icons and the logo were
        # baked with the old colours and must be redrawn.
        self.header.refresh_theme()
        self.sidebar.refresh_theme()


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(Theme.stylesheet())

    shell = DashboardShell(user_name="Eijkim", start_tab="diseases")
    shell.resize(1480, 920)
    shell.setWindowTitle("Akeso")
    shell.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())