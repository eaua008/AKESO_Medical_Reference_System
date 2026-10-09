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

import sys
from typing import Optional

from supabase import Client, ClientOptions, create_client

from app.core.config import config
from app.models.user import User


class AuthError(Exception):
    """Our own error type, so upper layers never catch a Supabase exception."""


class AccountSuspended(AuthError):
    """An admin suspended this account (User Management). The controller
    shows this as a pop-up rather than a red line under the form."""


SUSPENDED_MESSAGE = ("This account has been suspended by an administrator. "
                     "Contact your Akeso administrator if you think this is a mistake.")
GENERIC_MESSAGE = "Something went wrong while signing in. Please try again in a moment."


def auth_error_from_text(text: str) -> AuthError:
    """Turn a raw message from Supabase Auth (an exception, or the error in
    a Google sign-in redirect) into what the user is allowed to see.

    Raw server text never reaches the screen: it can hold database
    internals (column names, SQL errors) that tell an attacker how the
    backend is built. Details go to the console for debugging instead.
    """
    lower = (text or "").lower()
    if "banned" in lower or "user_banned" in lower:
        return AccountSuspended(SUSPENDED_MESSAGE)
    print(f"[auth] {text}", file=sys.stderr)
    return AuthError(GENERIC_MESSAGE)


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
            raise self._error(exc) from exc

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
            raise self._error(exc) from exc

        if not response.user:
            raise AuthError("Could not create the account.")

        # With "Confirm email" on, Supabase returns a user but no session. A
        # user row exists, but nobody is signed in until the code is entered.
        if response.session is None:
            raise PendingVerification(email)

        return User.from_supabase(response.user)

    @property
    def client(self) -> Client:
        """The signed-in client, for the account repositories (their data is
        private, so they need this session rather than a client of their own)."""
        return self._client

    # ------------------------------------------------------- remember me

    def refresh_token(self) -> Optional[str]:
        """The current session's refresh token (for "Remember me")."""
        try:
            session = self._client.auth.get_session()
        except Exception:  # noqa: BLE001
            return None
        return getattr(session, "refresh_token", None) if session else None

    def restore(self, refresh_token: str) -> User:
        """Sign in again with a saved refresh token (next launch)."""
        try:
            response = self._client.auth.refresh_session(refresh_token)
        except Exception as exc:
            raise self._error(exc) from exc
        if not response or not response.user or not response.session:
            raise AuthError("Your saved sign-in has expired. Please sign in again.")
        return User.from_supabase(response.user)

    def on_session_change(self, callback) -> None:
        """callback(event: str, refresh_token) whenever the session changes
        (signed in, token refreshed, signed out)."""
        def relay(event, session):
            callback(str(event), getattr(session, "refresh_token", None) if session else None)
        try:
            self._client.auth.on_auth_state_change(relay)
        except Exception:  # noqa: BLE001 - remember-me just won't update
            pass

    def sign_out(self) -> None:
        # "local" ends the session on THIS computer only. The library's
        # default ("global") signs the account out of every device, which
        # would make the Devices list and "Sign out all other devices"
        # meaningless: every ordinary sign-out would already do that.
        try:
            self._client.auth.sign_out({"scope": "local"})
        except Exception as exc:  # noqa: BLE001 - the local session is dropped regardless
            raise self._error(exc) from exc

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
            print(f"[auth] Google sign-in URL: {exc}", file=sys.stderr)
            raise AuthError("Could not start Google sign-in. Check your internet "
                            "connection and try again.") from exc

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
            if "banned" in str(exc).lower():
                raise AccountSuspended(SUSPENDED_MESSAGE) from exc
            print(f"[auth] Google code exchange: {exc}", file=sys.stderr)
            raise AuthError(
                "Google sign-in could not be completed. Try again."
            ) from exc

        if not response.user:
            raise AuthError("Google did not return an account.")
        return User.from_supabase(response.user)

    # ------------------------------------------------------------- helpers

    @staticmethod
    def _error(exc: Exception) -> AuthError:
        text = str(exc).lower()
        if "invalid login" in text:
            return AuthError("Invalid email or password.")
        if "already registered" in text:
            return AuthError("That email is already registered.")
        if "email not confirmed" in text:
            return AuthError("Please verify your email before logging in.")
        if "rate limit" in text or "too many" in text:
            return AuthError("Too many attempts. Wait a minute before trying again.")
        # Suspended (set by an admin in User Management), or anything else:
        # never the raw server text.
        return auth_error_from_text(str(exc))

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
        print(f"[auth] {exc}", file=sys.stderr)
        return GENERIC_MESSAGE
