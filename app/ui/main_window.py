"""Top-level window: auth screen, then the application shell.

Owns routing between the two — where the user goes after logging in or out
is a whole-application concern, not something either screen decides.

The shell is built AFTER login, not up front: it needs the user's name,
email and role, and building it early would fire the encyclopedia's queries
before anyone has signed in.
"""

from typing import Optional

from PySide6.QtCore import QEventLoop, QPoint, QRect, QSize, QTimer
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
# First-launch window size (shrunk to fit smaller screens). After that the
# window reopens at whatever normal size the user left it.
DEFAULT_SIZE = QSize(1480, 920)


class MainWindow(QMainWindow):
    """Routes between the auth screen and the dashboard."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akeso")

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

        # Same size and place as last time (or DEFAULT_SIZE, centred), and
        # maximised again if it was maximised when Akeso closed.
        prefs = PreferenceStore().load()
        window_frame.place(self, prefs.window_rect, DEFAULT_SIZE)
        self._open_maximized = prefs.window_maximized

        self.auth_view = AuthView()
        self._screens.addWidget(self.auth_view)
        self.shell: Optional[DashboardShell] = None

        self._auth_controller = AuthController(self.auth_view)
        self._auth_controller.authenticated.connect(self._on_authenticated)
        # Two-factor, Terms, a pending deletion: checked between login and
        # the dashboard (see account_gate.py).
        self._gate = AccountGate(self)

        self._load_stats()
        # "Remember me" from last time: sign straight in once the window shows.
        QTimer.singleShot(0, self._auth_controller.try_restore)
        self._prepare_gpu_window()

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

    # ------------------------------------------------------------ window

    def _prepare_gpu_window(self) -> None:
        """Make the window GPU-ready before it first appears.

        The Body System Explorer (3D) and the reference browser are web
        views drawn by the graphics card. The first time one appears in a
        window that was drawn the ordinary way, Qt has to destroy and
        rebuild the whole Windows window to switch it over, which looks
        like Akeso closing and opening again. A 1-pixel, invisible web view
        added now, before the window is shown, makes Qt build the window
        GPU-ready from the start, so nothing is rebuilt later.
        OFF by default since 1.0.3: a GPU-ready window redraws every change
        through the graphics card, which made the whole app slow to respond
        on some laptops (1.0.2). The price is one flicker the first time the
        3D body opens. AKESO_GPU_WARMUP=1 turns it back on."""
        import os
        import sys
        if sys.platform != "win32" or not os.environ.get("AKESO_GPU_WARMUP"):
            return
        try:
            from PySide6.QtCore import Qt, QUrl
            from PySide6.QtWebEngineWidgets import QWebEngineView
        except ImportError:
            return
        warm = QWebEngineView(self.centralWidget())
        warm.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        warm.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        warm.setGeometry(0, 0, 1, 1)
        warm.load(QUrl("about:blank"))
        warm.lower()                      # under everything: never seen, never clicked
        warm.show()
        self._gpu_warm = warm             # kept: removing it could switch the window back

    def sheet_area(self) -> tuple:
        """Where pop-ups slide in (app/ui/components/sheet_dialog.py):
        (the widget they live in, the module area in its coordinates, the
        top of the click-blocking layer: below Akeso's title strip so the
        window can still be moved, minimised or closed)."""
        host = self.centralWidget()
        area = self._screens
        if self.shell is not None and self._screens.currentWidget() is self.shell:
            area = self.shell.content
        if area is host:
            rect = QRect(QPoint(0, 0), area.size())
        else:
            rect = QRect(area.mapTo(host, QPoint(0, 0)), area.size())
        if area is self._screens:
            # Sign-in screen: below its logo header, which stays visible.
            header = self.auth_view.findChild(QWidget, "authHeader")
            if header is not None and header.isVisible():
                cut = header.mapTo(host, QPoint(0, header.height())).y()
                rect.setTop(max(rect.top(), cut))
        title_bar = getattr(self, "title_bar", None)
        return host, rect, title_bar.height() if title_bar is not None else 0

    def nativeEvent(self, event_type, message):  # noqa: N802
        """Windows asks where the title bar, edges and maximise button are
        (see window_frame.py); everything else goes to Qt as usual."""
        handled = window_frame.native_event(self, event_type, message)
        if handled is not None:
            return handled
        return super().nativeEvent(event_type, message)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        if self._open_maximized:
            self._open_maximized = False
            QTimer.singleShot(0, self._maximize_if_needed)

    def _maximize_if_needed(self) -> None:
        if not window_frame.is_maximized(self):
            window_frame.toggle_maximized(self)

    def _save_window(self) -> None:
        rect = window_frame.floating_rect(self)
        changes = {"window_maximized": window_frame.is_maximized(self)}
        if rect is not None:
            changes["window_rect"] = [rect.x(), rect.y(), rect.width(), rect.height()]
        PreferenceStore().update(**changes)

    def closeEvent(self, event) -> None:  # noqa: N802
        self._save_window()                           # reopen at this size next time
        # A Google sign-in in progress holds port 8123 on a background
        # thread. Release it, or the next launch cannot bind the port.
        self._auth_controller.cancel_google()
        self._auth_controller.save_session_now()      # newest token for "Remember me"
        super().closeEvent(event)
