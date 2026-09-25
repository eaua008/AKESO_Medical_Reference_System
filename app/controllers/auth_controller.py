"""Wires the auth screen to the auth service.

The only class that knows both AuthView and AuthService exist.

It owns two detours from the plain login path, since deciding where the user
goes next is coordination rather than display or business rules:

  * email verification, when signup or login comes back needing a code
  * Google sign-in, which leaves the app for the browser and comes back
"""

from typing import Optional

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtGui import QDesktopServices

from app.core.google_oauth import REDIRECT_URL, OAuthCallbackListener
from app.repositories.auth_repository import AuthError, PendingVerification
from app.services.auth_service import AuthService
from app.ui.views.auth_view import AuthView
from app.ui.views.verify_email_dialog import VerifyEmailDialog

# Pause after a cancelled or failed Google sign-in before the button works
# again. Long enough to absorb an accidental double-click, short enough not
# to feel like a penalty.
GOOGLE_COOLDOWN_SECONDS = 5


class AuthController(QObject):
    """Handles login, signup, email verification and Google sign-in."""

    authenticated = Signal(object)  # emits the logged-in User

    def __init__(self, view: AuthView, service: Optional[AuthService] = None) -> None:
        super().__init__()
        self._view = view
        self._service = service or AuthService()
        self._dialog: Optional[VerifyEmailDialog] = None
        self._listener: Optional[OAuthCallbackListener] = None
        # How the current Google attempt ended. Decides whether to cool down
        # afterwards, and whether a "cancelled" message counts as an error.
        self._google_succeeded = False
        self._google_cancelled = False

        view.login_requested.connect(self._handle_login)
        view.signup_requested.connect(self._handle_signup)
        view.google_requested.connect(self._handle_google)

    # --------------------------------------------------------------- login

    def _handle_login(self, email: str, password: str) -> None:
        self._view.clear_error()
        self._view.set_busy(True)
        try:
            user = self._service.log_in(email, password)
        except PendingVerification:
            # The account exists but was never confirmed. Send them to
            # verification rather than a dead-end error.
            self._view.set_busy(False)
            self._open_verification(resend=True)
            return
        except AuthError as exc:
            self._view.show_error(str(exc))
        else:
            self.authenticated.emit(user)
        finally:
            self._view.set_busy(False)

    # -------------------------------------------------------------- signup

    def _handle_signup(
            self, name: str, email: str, password: str, confirm: str
    ) -> None:
        self._view.clear_error()

        # Terms agreement is a UI and legal concern, not an auth rule.
        if not self._view.terms_agreed():
            self._view.show_error(
                "Please agree to the Terms of Service to continue."
            )
            return

        self._view.set_busy(True)
        try:
            user = self._service.register(name, email, password, confirm)
        except PendingVerification:
            self._view.set_busy(False)
            self._open_verification()
            return
        except AuthError as exc:
            self._view.show_error(str(exc))
        else:
            # Only reached if "Confirm email" is switched off in Supabase.
            self.authenticated.emit(user)
        finally:
            self._view.set_busy(False)

    # -------------------------------------------------------------- Google

    def _handle_google(self) -> None:
        """Start Google sign-in — or, if already waiting, cancel it.

        The same button does both. While waiting it reads "Cancel", because
        the app cannot tell the browser tab was closed: it only listens for a
        redirect that may never come. The person who closed the tab is the
        only one who knows, so they get to decide.
        """
        if self._listener is not None and self._listener.isRunning():
            self._google_cancelled = True
            self._listener.requestInterruption()
            return

        self._view.clear_error()
        self._google_succeeded = False
        self._google_cancelled = False

        try:
            url = self._service.google_sign_in_url(REDIRECT_URL)
        except AuthError as exc:
            self._view.show_error(str(exc))
            return

        # Start listening BEFORE opening the browser. The other order races:
        # a fast redirect could arrive before anything is there to catch it.
        self._listener = OAuthCallbackListener()
        self._listener.code_received.connect(self._on_google_code)
        self._listener.failed.connect(self._on_google_failed)
        self._listener.tick.connect(self._view.set_google_countdown)
        self._listener.finished.connect(self._on_google_finished)
        self._listener.start()

        self._view.set_google_waiting(True)

        if not QDesktopServices.openUrl(QUrl(url)):
            self._listener.requestInterruption()
            self._view.show_error(
                "Could not open your browser for Google sign-in."
            )

    def _on_google_code(self, code: str) -> None:
        try:
            user = self._service.complete_google_sign_in(code)
        except AuthError as exc:
            self._view.show_error(str(exc))
            return
        self._google_succeeded = True
        self.authenticated.emit(user)

    def _on_google_failed(self, message: str) -> None:
        # A cancel the user asked for is not an error, so it gets no red
        # message. The cooldown text already says what is happening.
        if self._google_cancelled:
            return
        self._view.show_error(message)

    def _on_google_finished(self) -> None:
        self._listener = None
        if self._google_succeeded:
            # The screen is switching to the dashboard; nothing to cool down.
            self._view.set_google_waiting(False)
        else:
            # Cancelled, timed out, or failed. A short pause before the
            # button re-arms stops a double-click from firing two sign-ins
            # back to back.
            self._view.start_google_cooldown(GOOGLE_COOLDOWN_SECONDS)

    def cancel_google(self) -> None:
        """Stop waiting for the browser. Safe to call when not waiting."""
        if self._listener is not None:
            self._google_cancelled = True
            self._listener.requestInterruption()

    # -------------------------------------------------------- verification

    def _open_verification(self, resend: bool = False) -> None:
        email = self._service.pending_email
        if not email:
            self._view.show_error("Could not start verification.")
            return

        self._dialog = VerifyEmailDialog(email, parent=self._view)
        self._dialog.code_submitted.connect(self._handle_code)
        self._dialog.resend_requested.connect(self._handle_resend)

        if resend:
            # Reached from a login attempt, so no fresh code was just sent.
            try:
                self._service.resend_code()
                self._dialog.show_info("We sent you a new code.")
                self._dialog.start_cooldown()
            except AuthError as exc:
                self._dialog.show_error(str(exc))

        if self._dialog.exec() == VerifyEmailDialog.DialogCode.Rejected:
            self._service.cancel_verification()
            self._view.show_error(
                "Account created but not yet verified. Log in again to "
                "finish verifying."
            )

    def _handle_code(self, code: str) -> None:
        if not self._dialog:
            return

        self._dialog.set_busy(True)
        try:
            user = self._service.verify_code(code)
        except AuthError as exc:
            self._dialog.show_error(str(exc))
            self._dialog.set_busy(False)
            return

        self._dialog.accept()
        self._dialog = None
        self.authenticated.emit(user)

    def _handle_resend(self) -> None:
        if not self._dialog:
            return
        try:
            self._service.resend_code()
            self._dialog.show_info("A new code is on its way.")
        except AuthError as exc:
            self._dialog.show_error(str(exc))

    # -------------------------------------------------------------- logout

    def log_out(self) -> None:
        """End the session and clear the form.

        Clearing matters: on a shared machine, leaving the previous user's
        email in the field tells the next person who was here.
        """
        self.cancel_google()
        try:
            self._service.log_out()
        except AuthError:
            pass  # the local session is discarded regardless
        self._view.reset()