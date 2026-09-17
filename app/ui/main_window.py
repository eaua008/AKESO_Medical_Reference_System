from PySide6.QtWidgets import QMainWindow, QStackedWidget

from app.controllers.auth_controller import AuthController
from app.ui.views.auth_view import AuthView
from app.ui.views.dashboard_view import DashboardView


class MainWindow(QMainWindow):
    """Top-level window. Holds every screen in one stack and swaps between
    them. The window does no business logic itself — that lives in the
    controllers.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akeso")
        self.resize(1920, 1080)

        self._screens = QStackedWidget()
        self.setCentralWidget(self._screens)

        self.auth_view = AuthView()
        self.dashboard_view = DashboardView()

        self._screens.addWidget(self.auth_view)        # index 0
        self._screens.addWidget(self.dashboard_view)   # index 1

        # Guest mode was removed, so AuthView no longer emits guest_requested.
        # The only route to the dashboard now is a successful authentication.
        self._auth_controller = AuthController(self.auth_view)
        self._auth_controller.authenticated.connect(self._on_authenticated)

    def _on_authenticated(self, user) -> None:
        self._screens.setCurrentWidget(self.dashboard_view)