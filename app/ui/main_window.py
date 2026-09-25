"""Top-level window: auth screen, then the application shell.

Owns routing between the two — where the user goes after logging in or out
is a whole-application concern, not something either screen decides.

The shell is built AFTER login, not up front: it needs the user's name,
email and role, and building it early would fire the encyclopedia's queries
before anyone has signed in.
"""

from typing import Optional

from PySide6.QtWidgets import QMainWindow, QStackedWidget

from app.controllers.auth_controller import AuthController
from app.models.user import User
from app.repositories.supabase_disease_repository import DiseaseRepositoryError
from app.services.disease_service import DiseaseService
from app.ui.dashboard_shell import DashboardShell
from app.ui.views.auth_view import AuthView

# Where every successful login and signup lands.
LANDING_TAB = "dashboard"


class MainWindow(QMainWindow):
    """Routes between the auth screen and the dashboard."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akeso")
        self.resize(1480, 920)

        self._screens = QStackedWidget()
        self.setCentralWidget(self._screens)

        self.auth_view = AuthView()
        self._screens.addWidget(self.auth_view)
        self.shell: Optional[DashboardShell] = None

        self._auth_controller = AuthController(self.auth_view)
        self._auth_controller.authenticated.connect(self._on_authenticated)

        self._load_stats()

    # ------------------------------------------------------------- stats

    def _load_stats(self) -> None:
        """Fill the auth screen's counts from the live database.

        Works before login because reference tables are public-read under
        row-level security. On failure the counts stay as dashes rather than
        showing numbers that were never read.
        """
        try:
            stats = DiseaseService().stats()
        except DiseaseRepositoryError:
            return
        self.auth_view.set_stats(
            body_systems=stats["body_systems"],
            diseases=stats["diseases"],
            symptoms=stats["symptoms"],
        )

    # ----------------------------------------------------------- routing

    def _on_authenticated(self, user: User) -> None:
        """Build the shell for this user and switch to it.

        Password login, OTP-verified signup, and Google sign-in all arrive
        here, so they all land on the same tab.
        """
        self._discard_shell()

        self.shell = DashboardShell(
            user_name=user.label,
            user_email=user.email,
            role=self._role_for(user),
            start_tab=LANDING_TAB,
        )
        self.shell.sign_out_requested.connect(self.log_out)
        self._screens.addWidget(self.shell)
        self._screens.setCurrentWidget(self.shell)
        self.setWindowTitle(f"Akeso \u2014 {user.label}")

    @staticmethod
    def _role_for(user: User) -> str:
        """Which nav items this user sees.

        Hardcoded to "user" for now, and a UI convenience only — it decides
        which buttons get built. Real authorisation must live in Postgres
        row-level security, since anyone who can run this app can edit this.
        """
        return "user"

    def _discard_shell(self) -> None:
        # Rebuilt per login rather than reused: a different user may have a
        # different role, and the sidebar decides its items at build time.
        if self.shell is not None:
            self._screens.removeWidget(self.shell)
            self.shell.deleteLater()
            self.shell = None

    def log_out(self) -> None:
        """Sign out and return to the login screen."""
        self._auth_controller.log_out()
        self._discard_shell()
        self._screens.setCurrentWidget(self.auth_view)
        self.setWindowTitle("Akeso")
        self._load_stats()

    def closeEvent(self, event) -> None:  # noqa: N802
        # A Google sign-in in progress holds port 8123 on a background
        # thread. Release it, or the next launch cannot bind the port.
        self._auth_controller.cancel_google()
        super().closeEvent(event)