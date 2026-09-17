from PySide6.QtCore import QObject, Signal

from app.repositories.auth_repository import AuthError
from app.services.auth_service import AuthService
from app.ui.views.auth_view import AuthView


class AuthController(QObject):
    """Wires the auth screen to the auth service.

    This is the only class that knows both AuthView and AuthService exist.
    The view never imports the service directly.
    """

    authenticated = Signal(object)  # emits the logged-in User

    def __init__(self, view: AuthView, service: AuthService | None = None) -> None:
        super().__init__()
        self._view = view
        self._service = service or AuthService()

        view.login_requested.connect(self._handle_login)
        view.signup_requested.connect(self._handle_signup)

    def _handle_login(self, email: str, password: str) -> None:
        self._view.clear_error()
        self._view.set_busy(True)
        try:
            user = self._service.log_in(email, password)
        except AuthError as exc:
            self._view.show_error(str(exc))
        else:
            self.authenticated.emit(user)
        finally:
            self._view.set_busy(False)

    def _handle_signup(
            self, name: str, email: str, password: str, confirm: str
    ) -> None:
        self._view.clear_error()

        # Terms agreement is a UI/legal concern, not an auth business rule,
        # so it is checked here rather than inside AuthService.
        if not self._view.terms_agreed():
            self._view.show_error("Please agree to the Terms of Service to continue.")
            return

        self._view.set_busy(True)
        try:
            user = self._service.register(name, email, password, confirm)
        except AuthError as exc:
            self._view.show_error(str(exc))
        else:
            self.authenticated.emit(user)
        finally:
            self._view.set_busy(False)