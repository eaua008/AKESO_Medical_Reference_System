"""Business rules for sign-in security: password, email, two-factor, devices.

Every change here is also recorded in the activity log. The log lines that
matter most (password and email changes, sign-ins) are written by the
database itself; the app only reports what the database cannot see.
"""

import re
from typing import Callable, Optional

from app.core.device_identity import (
    APP_VERSION, device_key, device_name, platform_label,
)
from app.models.account import Device, MfaEnrollment, MfaStatus, SecurityEvent
from app.repositories.account_errors import AccountError
from app.repositories.security_repository import SecurityRepository

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
SPECIALS = "!@#$%^&*"

# Same checklist as the signup form, so both screens ask for the same thing.
PASSWORD_RULES: list[tuple[str, Callable[[str], bool]]] = [
    ("8+ characters", lambda p: len(p) >= 8),
    ("Uppercase letter", lambda p: bool(re.search(r"[A-Z]", p))),
    ("Lowercase letter", lambda p: bool(re.search(r"[a-z]", p))),
    ("At least 1 number", lambda p: bool(re.search(r"\d", p))),
    (f"Special character ({SPECIALS})", lambda p: any(c in SPECIALS for c in p)),
]


def password_problems(password: str) -> list[str]:
    return [label for label, ok in PASSWORD_RULES if not ok(password)]


class SecurityService:
    def __init__(self, repository: SecurityRepository, email: str) -> None:
        self._repo = repository
        self._email = email

    # ----------------------------------------------------------- password

    def has_password(self) -> bool:
        return self._repo.has_password()

    def change_password(self, current: str, new: str, confirm: str) -> None:
        """current may be empty for a Google-only account setting its first one."""
        problems = password_problems(new)
        if problems:
            raise AccountError("The new password needs: " + ", ".join(problems).lower() + ".")
        if new != confirm:
            raise AccountError("The new passwords do not match.")
        if self._repo.has_password():
            if not current:
                raise AccountError("Enter your current password.")
            if current == new:
                raise AccountError("The new password must be different from the current one.")
            if not self._repo.verify_current_password(current):
                raise AccountError("Your current password is not right.")
        self._repo.set_password(new)

    # -------------------------------------------------------------- email

    def request_email_change(self, new_email: str, password: str) -> str:
        new_email = new_email.strip().lower()
        if not EMAIL_PATTERN.match(new_email):
            raise AccountError("That does not look like a valid email address.")
        if new_email == self._email.lower():
            raise AccountError("That is already your email address.")
        # Re-check the password, so someone at an unlocked computer cannot
        # quietly move the account to their own inbox.
        if self._repo.has_password() and not self._repo.verify_current_password(password):
            raise AccountError("Your password is not right.")
        self._repo.request_email_change(new_email)
        return new_email

    # --------------------------------------------------------- two-factor

    def mfa_status(self) -> MfaStatus:
        return self._repo.mfa_status()

    def mfa_needs_code(self) -> bool:
        return self._repo.mfa_needs_code()

    def start_mfa_setup(self) -> MfaEnrollment:
        if self._repo.mfa_status().enabled:
            raise AccountError("Two-factor sign-in is already on.")
        return self._repo.mfa_enroll()

    def finish_mfa_setup(self, factor_id: str, code: str) -> None:
        self._repo.mfa_verify(factor_id, self._clean_code(code))
        self._log("mfa_enabled")

    def cancel_mfa_setup(self, factor_id: str) -> None:
        try:
            self._repo.mfa_cancel_enrollment(factor_id)
        except AccountError:
            pass    # an unverified factor expires on its own anyway

    def disable_mfa(self, code: str) -> None:
        """Turning 2FA off needs a current code: proof the phone is at hand."""
        status = self._repo.mfa_status()
        if not status.enabled or not status.factor_id:
            return
        self._repo.mfa_verify(status.factor_id, self._clean_code(code))
        self._repo.mfa_disable(status.factor_id)
        self._log("mfa_disabled")

    def pass_mfa(self, code: str) -> None:
        """The sign-in step: raise the session from aal1 to aal2."""
        status = self._repo.mfa_status()
        if not status.factor_id:
            return
        try:
            self._repo.mfa_verify(status.factor_id, self._clean_code(code))
        except AccountError:
            self._log("mfa_challenge_failed")
            raise

    @staticmethod
    def _clean_code(code: str) -> str:
        code = code.strip().replace(" ", "")
        if not (code.isdigit() and len(code) == 6):
            raise AccountError("Enter the 6-digit code from your authenticator app.")
        return code

    # ------------------------------------------------------------ devices

    def register_this_device(self) -> None:
        self._repo.touch_device(device_key(), device_name(), platform_label(), APP_VERSION)

    def devices(self) -> list[Device]:
        return [Device.from_row(r) for r in self._repo.devices()]

    def forget_device(self, device: Device) -> None:
        if device.is_current:
            raise AccountError("This is the computer you are using now.")
        self._repo.forget_device(device.id)
        self._log("device_forgotten", {"device": device.device_name})

    def sign_out_other_devices(self) -> None:
        self._repo.sign_out_others()
        self._log("sign_out_others")

    def record_sign_out(self) -> None:
        self._log("sign_out")

    # ---------------------------------------------------------------- log

    def events(self, limit: int = 40, before_id: Optional[int] = None) -> list[SecurityEvent]:
        return [SecurityEvent.from_row(r) for r in self._repo.events(limit, before_id)]

    def _log(self, kind: str, detail: Optional[dict] = None) -> None:
        try:
            self._repo.log(kind, device_name(), detail)
        except AccountError:
            pass
