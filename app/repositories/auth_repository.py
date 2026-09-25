"""Data access for authentication.

Everything that knows Supabase exists lives in this file and nowhere else.

On passwords: this app never sees, hashes, or stores one. Supabase hashes
them server-side with bcrypt, and credentials travel over TLS. Encrypting a
password in the client before sending would be strictly worse — the
ciphertext just becomes the new password, and the key would have to ship
inside the binary.

One client per repository, deliberately. Google sign-in uses PKCE, and the
PKCE code verifier is stored inside the client object between starting the
flow and finishing it. A fresh client for the second step would have no
verifier and the exchange would fail.
"""

from typing import Optional

from supabase import Client, ClientOptions, create_client

from app.core.config import config
from app.models.user import User


class AuthError(Exception):
    """Our own error type, so upper layers never catch a Supabase exception."""


class PendingVerification(Exception):
    """Signup succeeded but the account is unusable until a code is entered.

    A routing signal rather than a failure. Raised so the controller must
    handle it explicitly instead of quietly treating an unverified account
    as a logged-in one.
    """

    def __init__(self, email: str) -> None:
        super().__init__(f"Verification required for {email}")
        self.email = email


class AuthRepository:
    """Authentication against Supabase."""

    def __init__(self, client: Optional[Client] = None) -> None:
        # flow_type="pkce" is required for desktop OAuth. The implicit flow
        # returns tokens in a URL fragment, which never reaches a local
        # listener. OTP verification is unaffected by this setting.
        self._client = client or create_client(
            config.supabase_url,
            config.supabase_key,
            options=ClientOptions(flow_type="pkce"),
        )

    # ------------------------------------------------------- password auth

    def sign_in(self, email: str, password: str) -> User:
        try:
            response = self._client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception as exc:
            if "not confirmed" in str(exc).lower():
                raise PendingVerification(email) from exc
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

        # With "Confirm email" on, Supabase returns a user but no session. A
        # user row exists, but nobody is signed in until the code is entered.
        if response.session is None:
            raise PendingVerification(email)

        return User.from_supabase(response.user)

    def sign_out(self) -> None:
        self._client.auth.sign_out()

    # ----------------------------------------------------------------- OTP

    def verify_signup_code(self, email: str, code: str) -> User:
        """Exchange a six-digit signup code for a session.

        type="signup" confirms a new account. Password resets and magic links
        use other types and are not interchangeable.
        """
        try:
            response = self._client.auth.verify_otp(
                {"email": email, "token": code, "type": "signup"}
            )
        except Exception as exc:
            raise AuthError(self._friendly_otp(exc)) from exc

        if not response.user:
            raise AuthError("That code was not accepted.")
        return User.from_supabase(response.user)

    def resend_signup_code(self, email: str) -> None:
        """Send a fresh code. Supabase rate-limits this server-side."""
        try:
            self._client.auth.resend({"type": "signup", "email": email})
        except Exception as exc:
            raise AuthError(self._friendly_otp(exc)) from exc

    # -------------------------------------------------------------- Google

    def start_google_sign_in(self, redirect_to: str) -> str:
        """Begin the OAuth flow and return the URL to open in a browser.

        This also generates the PKCE verifier and stores it in this client.
        complete_google_sign_in must run on the same repository instance.
        """
        try:
            response = self._client.auth.sign_in_with_oauth(
                {
                    "provider": "google",
                    "options": {
                        "redirect_to": redirect_to,
                        # Always show the account picker. Without this, a
                        # browser already signed in to one Google account
                        # skips straight through, and a shared machine
                        # signs the next person in as the previous one.
                        "query_params": {"prompt": "select_account"},
                    },
                }
            )
        except Exception as exc:
            raise AuthError(f"Could not start Google sign-in: {exc}") from exc

        if not getattr(response, "url", None):
            raise AuthError("Supabase did not return a Google sign-in URL.")
        return response.url

    def complete_google_sign_in(self, code: str) -> User:
        """Exchange the code from the browser redirect for a session.

        The verifier is read from this client's storage automatically. That
        binding is what makes an intercepted code worthless elsewhere.
        """
        try:
            response = self._client.auth.exchange_code_for_session(
                {"auth_code": code}
            )
        except Exception as exc:
            raise AuthError(
                "Google sign-in could not be completed. Try again."
            ) from exc

        if not response.user:
            raise AuthError("Google did not return an account.")
        return User.from_supabase(response.user)

    # ------------------------------------------------------------- helpers

    @staticmethod
    def _friendly(exc: Exception) -> str:
        text = str(exc).lower()
        if "invalid login" in text:
            return "Invalid email or password."
        if "already registered" in text:
            return "That email is already registered."
        if "email not confirmed" in text:
            return "Please verify your email before logging in."
        return f"Unexpected error: {exc}"

    @staticmethod
    def _friendly_otp(exc: Exception) -> str:
        """Code-specific messages.

        Does not distinguish "wrong code" from "no pending signup for this
        address" — that difference would reveal which emails are registered.
        """
        text = str(exc).lower()
        if "expired" in text:
            return "That code has expired. Request a new one."
        if "invalid" in text or "token" in text:
            return "That code is not valid. Check it and try again."
        if "rate" in text or "too many" in text:
            return "Too many attempts. Wait a minute before trying again."
        return f"Unexpected error: {exc}"