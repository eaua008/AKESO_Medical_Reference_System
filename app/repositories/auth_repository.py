from typing import Optional

from supabase import Client, create_client

from app.core.config import config
from app.models.user import User


class AuthError(Exception):
    """Our own error type, so upper layers never catch a Supabase exception."""


class AuthRepository:
    """Data access for authentication.

    Everything that knows Supabase exists lives in this file and nowhere else.
    """

    def __init__(self, client: Optional[Client] = None) -> None:
        self._client = client or create_client(
            config.supabase_url, config.supabase_key
        )

    def sign_in(self, email: str, password: str) -> User:
        try:
            response = self._client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception as exc:
            raise AuthError(self._friendly(exc)) from exc

        if not response.user:
            raise AuthError("Invalid email or password.")
        return User.from_supabase(response.user)

    def sign_up(self, email: str, password: str, display_name: str) -> User:
        try:
            response = self._client.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {"data": {"display_name": display_name}},
                }
            )
        except Exception as exc:
            raise AuthError(self._friendly(exc)) from exc

        if not response.user:
            raise AuthError("Could not create the account.")
        return User.from_supabase(response.user)

    def sign_out(self) -> None:
        self._client.auth.sign_out()

    @staticmethod
    def _friendly(exc: Exception) -> str:
        """Turn Supabase's raw messages into something a user can read."""
        text = str(exc).lower()
        if "invalid login" in text:
            return "Invalid email or password."
        if "already registered" in text:
            return "That email is already registered."
        if "email not confirmed" in text:
            return "Please confirm your email before logging in."
        return f"Unexpected error: {exc}"