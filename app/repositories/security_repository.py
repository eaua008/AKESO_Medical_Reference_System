"""Password, email, two-factor, devices and the activity log.

Password and email changes and two-factor go through Supabase Auth itself.
Devices and the log go through the SQL functions in migration 002, which
decide what the app is allowed to record.
"""

from datetime import date
from typing import Optional

from app.core.supabase_session import SessionClient
from app.models.account import MfaEnrollment, MfaStatus, parse_time
from app.repositories.account_errors import AccountError, friendly

MFA_ISSUER = "Akeso"


class SecurityRepository:
    def __init__(self, session: SessionClient) -> None:
        self._s = session

    def _do(self, call):
        try:
            return self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise AccountError(friendly(exc)) from exc

    # ------------------------------------------------------------ account

    def current_user(self):
        """The auth user as Supabase has it now (email, pending email, identities)."""
        def call():
            response = self._s.auth.get_user()
            if response is None or response.user is None:
                raise AccountError("Your session has ended. Please sign in again.")
            return response.user
        return self._do(call)

    def has_password(self) -> bool:
        return bool(self._do(lambda: self._s.rpc("has_password").execute().data))

    def verify_current_password(self, password: str) -> bool:
        return bool(self._do(lambda: self._s.rpc(
            "verify_current_password", {"p_password": password}).execute().data))

    def set_password(self, new_password: str) -> None:
        self._do(lambda: self._s.auth.update_user({"password": new_password}))

    def request_email_change(self, new_email: str) -> None:
        """Supabase emails a confirmation link; with "Secure email change" on,
        to both the old and the new address. Nothing changes until then."""
        self._do(lambda: self._s.auth.update_user({"email": new_email}))

    def sign_out_others(self) -> None:
        self._do(lambda: self._s.auth.sign_out({"scope": "others"}))

    def sign_out_here(self) -> None:
        self._do(lambda: self._s.auth.sign_out({"scope": "local"}))

    # --------------------------------------------------------- two-factor

    def mfa_status(self) -> MfaStatus:
        def call():
            factors = self._s.auth.mfa.list_factors()
            verified = factors.totp
            if not verified:
                return MfaStatus(enabled=False)
            first = verified[0]
            return MfaStatus(enabled=True, factor_id=first.id,
                             since=parse_time(getattr(first, "created_at", None)))
        return self._do(call)

    def mfa_needs_code(self) -> bool:
        """True when the account has 2FA but this session has not passed it."""
        def call():
            level = self._s.auth.mfa.get_authenticator_assurance_level()
            return level.current_level == "aal1" and level.next_level == "aal2"
        return self._do(call)

    def mfa_enroll(self) -> MfaEnrollment:
        def call():
            # Leftovers from a setup that was started and abandoned would
            # otherwise pile up (and share a friendly name with the new one).
            for factor in self._s.auth.mfa.list_factors().all:
                if factor.factor_type == "totp" and factor.status != "verified":
                    self._s.auth.mfa.unenroll({"factor_id": factor.id})
            response = self._s.auth.mfa.enroll({
                "factor_type": "totp",
                "issuer": MFA_ISSUER,
                "friendly_name": f"Akeso authenticator {date.today().isoformat()}",
            })
            svg = response.totp.qr_code
            if svg.startswith("data:"):
                svg = svg.split(",", 1)[1]
            return MfaEnrollment(factor_id=response.id, qr_svg=svg,
                                 secret=response.totp.secret, uri=response.totp.uri)
        return self._do(call)

    def mfa_verify(self, factor_id: str, code: str) -> None:
        self._do(lambda: self._s.auth.mfa.challenge_and_verify(
            {"factor_id": factor_id, "code": code}))

    def mfa_cancel_enrollment(self, factor_id: str) -> None:
        self._do(lambda: self._s.auth.mfa.unenroll({"factor_id": factor_id}))

    def mfa_disable(self, factor_id: str) -> None:
        self._do(lambda: self._s.auth.mfa.unenroll({"factor_id": factor_id}))

    # ------------------------------------------------------------ devices

    def touch_device(self, key: str, name: str, platform: str, version: str) -> None:
        self._do(lambda: self._s.rpc("touch_device", {
            "p_device_key": key, "p_device_name": name,
            "p_platform": platform, "p_app_version": version}).execute())

    def devices(self) -> list[dict]:
        return self._do(lambda: self._s.rpc("my_devices").execute().data or [])

    def forget_device(self, device_id: str) -> None:
        self._do(lambda: self._s.table("user_devices").delete().eq("id", device_id).execute())

    # ---------------------------------------------------------- the log

    def events(self, limit: int = 40, before_id: Optional[int] = None) -> list[dict]:
        def call():
            query = (self._s.table("security_events")
                     .select("id, kind, device_name, detail, created_at")
                     .order("id", desc=True).limit(limit))
            if before_id is not None:
                query = query.lt("id", before_id)
            return query.execute().data or []
        return self._do(call)

    def all_events(self) -> list[dict]:
        return self._do(lambda: self._s.table("security_events")
                        .select("kind, device_name, detail, created_at")
                        .order("id").execute().data or [])

    def log(self, kind: str, device_name: str = "", detail: Optional[dict] = None) -> None:
        self._do(lambda: self._s.rpc("log_security_event", {
            "p_kind": kind, "p_device_name": device_name,
            "p_detail": detail or {}}).execute())

    def all_devices(self) -> list[dict]:
        return self._do(lambda: self._s.table("user_devices")
                        .select("device_name, platform, app_version, first_seen, last_seen")
                        .order("first_seen").execute().data or [])
