"""The steps between "password accepted" and "dashboard shown".

    1. Two-factor code, if the account has it on
    2. Local data follows an email change (notes are stored per email)
    3. Load the account (profile, role, consents)
    4. Terms and Privacy Notice, if this version was not accepted yet
    5. Offer to cancel a scheduled deletion
    6. Record this computer in the Devices list (in the background)

Each step can end the sign-in (the user chooses Sign out), in which case
open() returns None and MainWindow signs out. If the account tables are
not installed or the server cannot be reached, steps 3 to 5 are skipped
and the app still opens: the Account page then shows the error.
"""

from dataclasses import dataclass
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget

from app.core.background import call_in_background, wait_for
from app.core.device_identity import last_email_for, remember_email
from app.core.supabase_session import SessionClient
from app.models.account import TERMS_VERSION, AccountSnapshot
from app.models.user import User
from app.repositories.account_data_repository import AccountDataRepository
from app.repositories.account_errors import AccountError
from app.repositories.local_account_data import LocalAccountData
from app.repositories.profile_repository import ProfileRepository
from app.repositories.security_repository import SecurityRepository
from app.services.account_service import AccountService
from app.services.activity_tracker import ActivityTracker
from app.services.security_service import SecurityService
from app.ui.views.account.account_dialogs import (
    CodeDialog, ConfirmDialog, DeletionPendingDialog, LegalDialog,
)


@dataclass
class AccountContext:
    """Everything the dashboard needs about the signed-in account."""

    user: User
    session: SessionClient
    account: AccountService
    security: SecurityService
    local: LocalAccountData
    tracker: ActivityTracker
    snapshot: Optional[AccountSnapshot]
    load_error: str = ""

    @property
    def role(self) -> str:
        return self.snapshot.role if self.snapshot else "student"

    @property
    def display_name(self) -> str:
        if self.snapshot and self.snapshot.profile.display_name:
            return self.snapshot.profile.display_name
        return self.user.label


def _busy(call):
    """Run one server call with a wait cursor. The call runs on a worker
    thread (wait_for), so the window keeps responding while it waits."""
    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
    try:
        return wait_for(call)
    finally:
        QApplication.restoreOverrideCursor()


class AccountGate:
    def __init__(self, parent: QWidget) -> None:
        self._parent = parent

    def open(self, user: User, client, signup_consent: bool = False) -> Optional[AccountContext]:
        session = SessionClient(client)
        security_repo = SecurityRepository(session)
        local = LocalAccountData()
        owner = user.email
        account = AccountService(ProfileRepository(session), security_repo,
                                 AccountDataRepository(session), local,
                                 email=user.email, owner=owner)
        security = SecurityService(security_repo, user.email)

        # 1. two-factor
        try:
            needs_code = _busy(security.mfa_needs_code)
        except AccountError:
            needs_code = False      # offline: the database still hides everything until aal2
        if needs_code and not self._ask_for_code(security):
            return None

        # 2. the notes on this computer follow the account to its new email
        try:
            previous = last_email_for(user.id)
            if previous and previous.lower() != owner.lower():
                local.rename_owner(previous, owner)
            remember_email(user.id, owner)
        except OSError:
            pass

        # 3. load
        snapshot, error = None, ""
        try:
            if signup_consent:
                _busy(account.accept_documents)     # ticked on the signup form
            snapshot = _busy(account.snapshot)
        except AccountError as exc:
            error = str(exc)

        if snapshot is not None and snapshot.profile.suspended_at is not None:
            # Suspended by an admin (Supabase Auth normally refuses the sign-in
            # already; this covers a session that was still valid).
            self._tell_suspended(snapshot.profile.suspended_reason)
            return None

        if snapshot is not None:
            # 4. terms
            if account.needs_consent(snapshot):
                if not self._ask_for_consent(account):
                    return None
                snapshot = self._reload(account, snapshot)
            # 5. deletion
            if snapshot.profile.deletion_pending:
                if not self._ask_about_deletion(account, snapshot):
                    return None
                snapshot = self._reload(account, snapshot)

        # 6. this computer
        call_in_background(security.register_this_device, on_error=lambda _m: None)

        tracker = ActivityTracker(
            enabled=bool(snapshot and snapshot.profile.track_study_activity))
        return AccountContext(user=user, session=session, account=account,
                              security=security, local=local, tracker=tracker,
                              snapshot=snapshot, load_error=error)

    # ------------------------------------------------------------- steps

    def _tell_suspended(self, reason: str) -> None:
        message = "An administrator has suspended this account."
        if reason:
            message += f"\n\nReason: {reason}"
        message += "\n\nContact your Akeso administrator if you think this is a mistake."
        dialog = ConfirmDialog("Account suspended", message, "OK", "shield-alert",
                               danger=True, parent=self._parent)
        dialog.exec()

    def _ask_for_code(self, security: SecurityService) -> bool:
        dialog = CodeDialog(
            "Two-factor sign-in",
            "Enter the 6-digit code from your authenticator app to finish signing in.",
            "Verify", secondary="Sign out", parent=self._parent)
        dialog.secondary.connect(dialog.reject)

        def submit(code: str) -> None:
            dialog.set_busy(True)       # the window stays live while it waits
            try:
                _busy(lambda: security.pass_mfa(code))
            except AccountError as exc:
                dialog.show_error(str(exc))
                return
            dialog.accept()
        dialog.submitted.connect(submit)
        return dialog.exec() == CodeDialog.DialogCode.Accepted

    def _ask_for_consent(self, account: AccountService) -> bool:
        dialog = LegalDialog(accept=True, version=TERMS_VERSION, parent=self._parent)
        dialog.sign_out.connect(dialog.reject)

        def accept() -> None:
            dialog.set_busy(True)       # the window stays live while it waits
            try:
                _busy(account.accept_documents)
            except AccountError as exc:
                dialog.show_error(str(exc))
                return
            dialog.accept()
        dialog.accepted_documents.connect(accept)
        return dialog.exec() == LegalDialog.DialogCode.Accepted

    def _ask_about_deletion(self, account: AccountService, snapshot: AccountSnapshot) -> bool:
        dialog = DeletionPendingDialog(snapshot.profile.deletion_scheduled_for,
                                       parent=self._parent)
        dialog.leave.connect(dialog.reject)

        def keep() -> None:
            dialog.set_busy(True)       # the window stays live while it waits
            try:
                _busy(account.cancel_deletion)
            except AccountError as exc:
                dialog.show_error(str(exc))
                return
            dialog.accept()
        dialog.keep.connect(keep)
        return dialog.exec() == DeletionPendingDialog.DialogCode.Accepted

    @staticmethod
    def _reload(account: AccountService, fallback: AccountSnapshot) -> AccountSnapshot:
        try:
            return _busy(account.snapshot)
        except AccountError:
            return fallback
