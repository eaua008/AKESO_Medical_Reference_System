import re

from app.models.user import User
from app.repositories.auth_repository import AuthRepository, AuthError

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
MIN_PASSWORD_LENGTH = 8


class AuthService:
    """Business rules for authentication.

    Validation lives here rather than in the UI, so any future interface
    enforces the same rules.
    """

    def __init__(self, repository: AuthRepository | None = None) -> None:
        self._repository = repository or AuthRepository()
        self._current_user: User | None = None

    @property
    def current_user(self) -> User | None:
        return self._current_user

    def log_in(self, email: str, password: str) -> User:
        email = email.strip().lower()

        if not email or not password:
            raise AuthError("Please fill in both fields.")
        if not EMAIL_PATTERN.match(email):
            raise AuthError("That does not look like a valid email address.")

        user = self._repository.sign_in(email, password)
        self._current_user = user
        return user

    def register(
            self, display_name: str, email: str, password: str, confirm: str
    ) -> User:
        email = email.strip().lower()
        display_name = display_name.strip()

        if not display_name:
            raise AuthError("Please enter your name.")
        if not EMAIL_PATTERN.match(email):
            raise AuthError("That does not look like a valid email address.")
        if len(password) < MIN_PASSWORD_LENGTH:
            raise AuthError(
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
            )
        if password != confirm:
            raise AuthError("Passwords do not match.")

        user = self._repository.sign_up(email, password, display_name)
        self._current_user = user
        return user

    def log_out(self) -> None:
        self._repository.sign_out()
        self._current_user = None