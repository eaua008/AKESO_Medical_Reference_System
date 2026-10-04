"""Top-level window: auth screen, then the application shell.

Owns routing between the two — where the user goes after logging in or out
is a whole-application concern, not something either screen decides.

The shell is built AFTER login, not up front: it needs the user's name,
email and role, and building it early would fire the encyclopedia's queries
before anyone has signed in.
"""

from typing import Optional

from PySide6.QtCore import QEventLoop, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from app.controllers.account_gate import AccountGate
from app.controllers.auth_controller import AuthController
from app.core.preferences import PreferenceStore
from app.core.theme import Theme
from app.models.user import User
from app.repositories.supabase_disease_repository import DiseaseRepositoryError
from app.services.disease_service import DiseaseService
from app.ui.dashboard_shell import DashboardShell
from app.ui import window_frame
from app.ui.theme_scope import app_mode, apply_app_stylesheet
from app.ui.views.auth_view import AuthView

# Where a login lands when Settings has no (usable) choice saved.
LANDING_TAB = "dashboard"


class MainWindow(QMainWindow):
    """Routes between the auth screen and the dashboard."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akeso")
        self.resize(1480, 920)

        self._screens = QStackedWidget()
        # On Windows, Akeso's own title strip (logo + minimise / maximise /
        # close in the app's colours) replaces the grey Windows one.
        title_bar = window_frame.install(self)
        if title_bar is None:
            self.setCentralWidget(self._screens)
        else:
            frame = QWidget()
            column = QVBoxLayout(frame)
            column.setContentsMargins(0, 0, 0, 0)
            column.setSpacing(0)
            column.addWidget(title_bar)
            column.addWidget(self._screens, 1)
            self.setCentralWidget(frame)
            self.title_bar = title_bar
            # The header's logo, bigger, filling the strip + header height.
            self.brand_logo = window_frame.BrandLogo(frame, title_bar, self._screens)

        self.auth_view = AuthView()
        self._screens.addWidget(self.auth_view)
        self.shell: Optional[DashboardShell] = None

        self._auth_controller = AuthController(self.auth_view)
        self._auth_controller.authenticated.connect(self._on_authenticated)
        # Two-factor, Terms, a pending deletion: checked between login and
        # the dashboard (see account_gate.py).
        self._gate = AccountGate(self)

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
        # Everything below used to run in one go on the UI thread. With the
        # server round trips and ~50 screens to build, Windows marked the
        # window "Not Responding" before the dashboard appeared. Now the
        # server calls run on worker threads and the build pauses between
        # screens to let the window breathe (see _breathe).
        self.auth_view.set_signing_in("Checking your account\u2026")

        account = self._gate.open(
            user, self._auth_controller.session_client(),
            signup_consent=self._auth_controller.take_signup_consent(user.email))
        if account is None:
            # The user chose "Sign out" at the two-factor, Terms or
            # deletion step.
            self.auth_view.set_signing_in(None)
            self.log_out()
            return

        self.auth_view.set_signing_in("Setting up your dashboard\u2026")
        self._breathe()
        self.shell = DashboardShell(
            user_name=account.display_name,
            user_email=user.email,
            role=self._role_for(account.role),
            start_tab=self._start_tab(self._role_for(account.role)),
            account=account,
            progress=self._breathe,
        )
        self.auth_view.set_signing_in(None)
        self.shell.sign_out_requested.connect(self.log_out)
        self.shell.identity_changed.connect(
            lambda name: self.setWindowTitle(f"Akeso \u2014 {name}"))
        self._screens.addWidget(self.shell)
        self._screens.setCurrentWidget(self.shell)
        self.setWindowTitle(f"Akeso \u2014 {account.display_name}")

    @staticmethod
    def _breathe(_step: str = "") -> None:
        """Let the window repaint and answer Windows between build steps.
        Clicks and key presses wait until the dashboard is ready."""
        QApplication.processEvents(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)

    @staticmethod
    def _start_tab(role: str) -> str:
        """Settings > Open on start, if this role can see that screen."""
        from app.ui.components.sidebar import visible_items
        chosen = PreferenceStore().load().start_tab
        allowed = {item["id"] for item in visible_items(role)}
        return chosen if chosen in allowed else LANDING_TAB

    @staticmethod
    def _role_for(role: str) -> str:
        """Which nav items this user sees: "student", "educator" or "admin".

        Read from public.user_roles, which only an admin can change. It is
        still a UI convenience only (it decides which buttons get built):
        the real protection is row-level security in the database, since
        anyone who can run this app can edit this file.
        """
        return role if role in ("student", "educator", "admin") else "student"

    def _discard_shell(self) -> None:
        # Rebuilt per login rather than reused: a different user may have a
        # different role, and the sidebar decides its items at build time.
        if self.shell is not None:
            self._screens.removeWidget(self.shell)
            self.shell.deleteLater()
            self.shell = None

    def log_out(self) -> None:
        """Sign out and return to the login screen."""
        if self.shell is not None:
            # Last study counts and the "signed out" log line, while the
            # session still exists (waits a few seconds at most).
            self.shell.shutdown()
        self._auth_controller.log_out()
        self._discard_shell()
        self._screens.setCurrentWidget(self.auth_view)
        # The dashboard switched themes area by area; bring the app-level
        # stylesheet (used by the login screen) in line once it is gone.
        QTimer.singleShot(50, self._sync_app_theme)
        self.setWindowTitle("Akeso")
        self._load_stats()

    @staticmethod
    def _sync_app_theme() -> None:
        if app_mode() != Theme.key():
            apply_app_stylesheet()

    def closeEvent(self, event) -> None:  # noqa: N802
        # A Google sign-in in progress holds port 8123 on a background
        # thread. Release it, or the next launch cannot bind the port.
        self._auth_controller.cancel_google()
        super().closeEvent(event)
