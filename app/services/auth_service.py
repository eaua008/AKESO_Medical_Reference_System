"""Business rules for authentication.

Validation lives here rather than in the UI, so any future interface — a
test, a CLI, another window — enforces the same rules.
"""

import re

from app.models.user import User
from app.repositories.auth_repository import (
    AuthError,
    AuthRepository,
    PendingVerification,
)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
MIN_PASSWORD_LENGTH = 8
OTP_LENGTH = 6


class AuthService:
    """Authentication rules and session state."""

    def __init__(self, repository: AuthRepository | None = None) -> None:
        self._repository = repository or AuthRepository()
        self._current_user: User | None = None
        self._pending_email: str | None = None

    @property
    def current_user(self) -> User | None:
        return self._current_user

    @property
    def pending_email(self) -> str | None:
        """Address awaiting a verification code, if any."""
        return self._pending_email

    # ------------------------------------------------------------ password

    def log_in(self, email: str, password: str) -> User:
        email = email.strip().lower()

        if not email or not password:
            raise AuthError("Please fill in both fields.")
        if not EMAIL_PATTERN.match(email):
            raise AuthError("That does not look like a valid email address.")

        try:
            user = self._repository.sign_in(email, password)
        except PendingVerification:
            # Remember who is waiting, so verification does not have to ask
            # for the address again.
            self._pending_email = email
            raise

        self._current_user = user
        self._pending_email = None
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

        try:
            user = self._repository.sign_up(email, password, display_name)
        except PendingVerification:
            self._pending_email = email
            raise

        self._current_user = user
        return user

    # ----------------------------------------------------------------- OTP

    def verify_code(self, code: str) -> User:
        """Confirm the pending signup with a code from the user's email."""
        if not self._pending_email:
            raise AuthError("There is no signup waiting to be verified.")

        code = code.strip().replace(" ", "")

        # A malformed code is certainly wrong, and sending it would spend a
        # rate-limited attempt for nothing.
        if not code.isdigit() or len(code) != OTP_LENGTH:
            raise AuthError(f"Enter the {OTP_LENGTH}-digit code from your email.")

        user = self._repository.verify_signup_code(self._pending_email, code)
        self._current_user = user
        self._pending_email = None
        return user

    def resend_code(self) -> str:
        if not self._pending_email:
            raise AuthError("There is no signup waiting to be verified.")
        self._repository.resend_signup_code(self._pending_email)
        return self._pending_email

    def cancel_verification(self) -> None:
        """Abandon the pending signup.

        The account still exists in Supabase, unconfirmed and unusable.
        """
        self._pending_email = None

    # -------------------------------------------------------------- Google

    def google_sign_in_url(self, redirect_to: str) -> str:
        """The URL to open in the browser to begin Google sign-in."""
        return self._repository.start_google_sign_in(redirect_to)

    def complete_google_sign_in(self, code: str) -> User:
        """Finish Google sign-in with the code from the browser redirect.

        Google accounts arrive already verified by Google, so there is no
        OTP step on this path.
        """
        if not code:
            raise AuthError("Google did not return an authorisation code.")
        user = self._repository.complete_google_sign_in(code)
        self._current_user = user
        self._pending_email = None
        return user

    # ------------------------------------------------------------ session

    def refresh_token(self):
        return self._repository.refresh_token()

    def restore_session(self, refresh_token: str) -> User:
        user = self._repository.restore(refresh_token)
        self._current_user = user
        return user

    def on_session_change(self, callback) -> None:
        self._repository.on_session_change(callback)

    def session_client(self):
        """The Supabase client holding the signed-in session."""
        return self._repository.client

    # -------------------------------------------------------------- logout

    def log_out(self) -> None:
        self._repository.sign_out()
        self._current_user = None
        self._pending_email = None
