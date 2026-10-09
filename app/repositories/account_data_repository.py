"""Consents, study activity, deletion and the school-email badge."""

from typing import Optional

from app.core.supabase_session import SessionClient
from app.repositories.account_errors import AccountError, friendly


class AccountDataRepository:
    def __init__(self, session: SessionClient) -> None:
        self._s = session

    def _do(self, call):
        try:
            return self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise AccountError(friendly(exc)) from exc

    # ----------------------------------------------------------- consents

    def consents(self) -> list[dict]:
        return self._do(lambda: self._s.table("consents")
                        .select("document, version, accepted_at")
                        .order("accepted_at", desc=True).execute().data or [])

    def accept(self, terms_version: str, privacy_version: str) -> None:
        self._do(lambda: self._s.rpc("accept_documents", {
            "p_terms_version": terms_version,
            "p_privacy_version": privacy_version}).execute())

    # ----------------------------------------------------------- activity

    def record_activity(self, counts: dict[str, int]) -> None:
        self._do(lambda: self._s.rpc("record_activity", {"p_counts": counts}).execute())

    def activity_summary(self) -> dict:
        return self._do(lambda: self._s.rpc("activity_summary").execute().data or {})

    def all_activity(self) -> list[dict]:
        return self._do(lambda: self._s.table("study_activity").select("*")
                        .order("day").execute().data or [])

    # ----------------------------------------------------------- deletion

    def request_deletion(self, confirm_text: str) -> Optional[str]:
        return self._do(lambda: self._s.rpc("request_account_deletion",
                                            {"p_confirm": confirm_text}).execute().data)

    def cancel_deletion(self) -> None:
        self._do(lambda: self._s.rpc("cancel_account_deletion").execute())

    # ------------------------------------------------ school email (Edge Fn)

    def _school(self, body: dict) -> dict:
        def call():
            try:
                result = self._s.invoke("school-email", body)
            except Exception as exc:  # noqa: BLE001
                text = getattr(exc, "message", None) or str(exc)
                low = text.lower()
                if "404" in text or ("not found" in low and "function" in low):
                    raise AccountError("The school-email Edge Function is not deployed yet "
                                       "(Supabase > Edge Functions).") from exc
                if "invalid jwt" in low or "an error occurred while requesting" in low:
                    # The platform's own JWT check refused it before the
                    # function ran (it does not understand the new API keys).
                    raise AccountError("School email check was refused by Supabase. In Edge "
                                       "Functions > school-email, turn off \"Verify JWT\" "
                                       "and try again.") from exc
                raise AccountError(text if len(text) < 160 else friendly(exc)) from exc
            if not isinstance(result, dict):
                raise AccountError("Unexpected reply from the verification service.")
            if result.get("error"):
                raise AccountError(str(result["error"]))
            return result
        return self._do(call)

    def send_school_code(self, email: str) -> dict:
        return self._school({"action": "send", "email": email})

    def verify_school_code(self, code: str) -> dict:
        return self._school({"action": "verify", "code": code})
