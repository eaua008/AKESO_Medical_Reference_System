"""Wires the Account Settings page to the account and security services.

Every Supabase request runs on a background thread (core/background.py), so
the window never freezes on a slow connection. Results come back on the UI
thread and are drawn from one AccountSnapshot, which is reloaded after
anything that changes it.
"""

import threading
from datetime import date
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QObject, QStandardPaths, QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog

from app.core.avatar_image import AvatarImageError, circle_pixmap, prepare_avatar
from app.core.background import call_in_background
from app.core.theme import Theme
from app.models.account import (
    TERMS_VERSION, AccountSnapshot, ActivitySummary, Device, SecurityEvent,
    friendly_time,
)
from app.repositories.local_account_data import LocalAccountData
from app.services.account_service import AccountService
from app.services.activity_tracker import ActivityTracker
from app.services.security_service import SecurityService
from app.ui.views.account.account_dialogs import (
    ChangeEmailDialog, ChangePasswordDialog, CodeDialog, ConfirmDialog, DeleteAccountDialog,
    LegalDialog, SchoolEmailDialog, TwoFactorSetupDialog,
)
from app.ui.views.account.account_view import AccountView

FLUSH_INTERVAL_MS = 60_000
EVENTS_PAGE = 30
SESSION_ENDED = "session has ended"


class AccountController(QObject):
    # name, header caption, photo (PNG bytes or None): for the header chip
    identity_changed = Signal(str, str, object)
    sign_out_requested = Signal()

    def __init__(self, view: AccountView, account: AccountService,
                 security: SecurityService, tracker: ActivityTracker,
                 local: LocalAccountData,
                 snapshot: Optional[AccountSnapshot] = None) -> None:
        super().__init__(view)
        self._view = view
        self._account = account
        self._security = security
        self._tracker = tracker
        self._local = local
        self._snapshot = snapshot
        self._devices: list[Device] = []
        self._events: list[SecurityEvent] = []
        self._avatar: Optional[bytes] = None
        self._notice_action = ""

        self._wire()
        self._flush_timer = QTimer(self)
        self._flush_timer.setInterval(FLUSH_INTERVAL_MS)
        self._flush_timer.timeout.connect(self.flush_activity)
        self._flush_timer.start()
        self.load()

    # ----------------------------------------------------------- wiring

    def _wire(self) -> None:
        v = self._view
        v.retry_requested.connect(self.load)
        v.banner_action.connect(self._on_banner)
        v.tab_changed.connect(self._on_tab)

        p = v.profile
        p.save_requested.connect(self._save_profile)
        p.photo_chosen.connect(self._set_photo)
        p.photo_remove_requested.connect(self._remove_photo)
        p.verify_school_requested.connect(self._verify_school)

        s = v.security
        s.change_email_requested.connect(self._change_email)
        s.change_password_requested.connect(self._change_password)
        s.enable_mfa_requested.connect(self._enable_mfa)
        s.disable_mfa_requested.connect(self._disable_mfa)
        s.sign_out_others_requested.connect(self._sign_out_others)
        s.forget_device_requested.connect(self._forget_device)
        s.more_events_requested.connect(self._more_events)
        s.refresh_requested.connect(self._reload_security)

        pr = v.privacy
        pr.accept_requested.connect(self._accept_documents)
        pr.read_terms_requested.connect(lambda: LegalDialog("terms", parent=self._view).exec())
        pr.read_privacy_requested.connect(
            lambda: LegalDialog("privacy", parent=self._view).exec())
        pr.tracking_toggled.connect(self._set_tracking)
        pr.clear_cache_requested.connect(self._clear_cache)
        pr.export_requested.connect(self._export)
        pr.delete_requested.connect(self._delete)
        pr.cancel_deletion_requested.connect(self._cancel_deletion)

    def _run(self, call: Callable, on_done: Optional[Callable] = None,
             on_error: Optional[Callable[[str], None]] = None) -> None:
        def failed(message: str) -> None:
            if SESSION_ENDED in message.lower():
                self._notice(message, "danger", "Sign in again", "signin")
            if on_error is not None:
                on_error(message)
            elif SESSION_ENDED not in message.lower():
                self._notice(message, "danger")
        call_in_background(call, on_done, failed, owner=self._view)

    def _notice(self, text: str, tone: str = "info", action: str = "",
                key: str = "dismiss") -> None:
        self._notice_action = key
        self._view.notice_banner.show_message(text, tone, action or "Dismiss")

    def _on_banner(self, which: str) -> None:
        if which == "deletion":
            self._cancel_deletion()
        elif self._notice_action == "signin":
            self.sign_out_requested.emit()
        else:
            self._view.notice_banner.hide()

    def _on_tab(self, key: str) -> None:
        if key == "overview" and self._snapshot is not None:
            self._load_activity()

    # ----------------------------------------------------------- loading

    def load(self) -> None:
        self._view.show_loading()

        def fetch():
            snapshot = self._account.snapshot()
            devices = self._security.devices()
            events = self._security.events(EVENTS_PAGE)
            avatar = self._account.avatar_bytes(snapshot.profile)
            activity = (self._account.activity()
                        if snapshot.profile.track_study_activity else ActivitySummary())
            return snapshot, devices, events, avatar, activity

        def done(result) -> None:
            snapshot, devices, events, avatar, activity = result
            self._snapshot, self._devices, self._events, self._avatar = (
                snapshot, devices, events, avatar)
            self._tracker.enabled = snapshot.profile.track_study_activity
            self._render()
            self._view.overview.show_activity(activity)
            self._view.loaded()

        self._run(fetch, done, self._view.show_load_error)

    def _reload_snapshot(self, then: Optional[Callable[[], None]] = None) -> None:
        def done(snapshot: AccountSnapshot) -> None:
            self._snapshot = snapshot
            self._render()
            if then:
                then()
        self._run(self._account.snapshot, done)

    def _reload_security(self) -> None:
        def fetch():
            return self._security.devices(), self._security.events(EVENTS_PAGE)

        def done(result) -> None:
            self._devices, self._events = result
            self._view.security.show_devices(self._devices)
            self._view.security.show_events(self._events, False,
                                            len(self._events) >= EVENTS_PAGE)
            self._render_overview()
        self._run(fetch, done)

    def _load_activity(self) -> None:
        if not self._snapshot.profile.track_study_activity:
            return
        self.flush_activity()
        self._run(self._account.activity, self._view.overview.show_activity,
                  on_error=lambda _m: None)

    # --------------------------------------------------------- rendering

    def _pixmap(self, size: int) -> QPixmap:
        name = self._snapshot.profile.display_name or self._snapshot.email
        return circle_pixmap(self._avatar, size, name, Theme.token("PRIMARY"), "#FFFFFF")

    def _render(self) -> None:
        s = self._snapshot
        if s is None:
            return
        percent, _items = self._account.completeness(s)
        self._view.show_header(s, self._pixmap(72), percent)
        self._view.profile.show_profile(s.profile, self._pixmap(84))
        self._view.security.show_snapshot(s)
        self._view.security.show_devices(self._devices)
        self._view.security.show_events(self._events, False, len(self._events) >= EVENTS_PAGE)
        self._view.privacy.show_snapshot(s, self._local.cache_size(),
                                         self._local.cache_clear_pending())
        self._render_overview()
        self._render_banners()
        self._emit_identity()

    def _render_overview(self) -> None:
        percent, items = self._account.completeness(self._snapshot)
        self._view.overview.show_snapshot(self._snapshot, percent, items, self._devices)

    def _render_banners(self) -> None:
        profile = self._snapshot.profile
        if profile.deletion_pending:
            self._view.deletion_banner.show_message(
                "Your account is scheduled for deletion on "
                f"{friendly_time(profile.deletion_scheduled_for, with_time=False)}.",
                "danger", "Keep my account")
        else:
            self._view.deletion_banner.hide()
        if self._snapshot.pending_email and self._notice_action in ("", "dismiss"):
            self._notice(f"Email change to {self._snapshot.pending_email} is waiting for "
                         "you to open the confirmation link.", "warn")

    def _emit_identity(self) -> None:
        s = self._snapshot
        name = s.profile.display_name or s.email.split("@")[0]
        self.identity_changed.emit(name, self._account.header_role_label(s.role, s.profile),
                                   self._avatar)

    # ----------------------------------------------------------- profile

    def _save_profile(self, changes: dict) -> None:
        self._view.profile.set_busy(True, "Saving…")

        def done(profile) -> None:
            self._snapshot.profile = profile
            self._render()
            self._view.profile.show_saved("Profile saved.")
        self._run(lambda: self._account.save_profile(self._snapshot.profile, changes),
                  done, self._view.profile.show_error)

    def _set_photo(self, path: str) -> None:
        try:
            png = prepare_avatar(path)
        except AvatarImageError as exc:
            self._view.profile.show_error(str(exc))
            return
        self._view.profile.set_busy(True, "Uploading photo…")

        def done(profile) -> None:
            self._snapshot.profile = profile
            self._avatar = png
            self._render()
            self._view.profile.show_saved("Photo updated.")
        self._run(lambda: self._account.set_avatar(png), done, self._view.profile.show_error)

    def _remove_photo(self) -> None:
        dialog = ConfirmDialog("Remove your photo?", "Your initial will be shown instead.",
                               "Remove", "camera", parent=self._view)
        if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
            return

        def done(profile) -> None:
            self._snapshot.profile = profile
            self._avatar = None
            self._render()
            self._view.profile.show_saved("Photo removed.")
        self._run(lambda: self._account.remove_avatar(self._snapshot.profile), done,
                  self._view.profile.show_error)

    def _verify_school(self) -> None:
        dialog = SchoolEmailDialog(parent=self._view)
        dialog.send_requested.connect(lambda email: self._run(
            lambda: self._account.send_school_code(email), dialog.code_sent, dialog.show_error))

        def verified(profile) -> None:
            self._snapshot.profile = profile
            dialog.accept()
            self._render()
            self._notice(f"Verified: you're now shown as a student at "
                         f"{profile.school_email_domain}.", "good")
        dialog.verify_requested.connect(lambda code: self._run(
            lambda: self._account.verify_school_code(code), verified, dialog.show_error))
        dialog.exec()

    # ---------------------------------------------------------- security

    def _change_email(self) -> None:
        s = self._snapshot
        dialog = ChangeEmailDialog(s.email, s.has_password, parent=self._view)

        def done(new_email: str) -> None:
            dialog.accept()
            self._notice(f"Confirmation sent. Open the link emailed to {new_email} "
                         "(and to your current address, if Supabase asks for both).", "good")
            self._reload_snapshot()
        dialog.submitted.connect(lambda email, password: self._run(
            lambda: self._security.request_email_change(email, password), done,
            dialog.show_error))
        dialog.exec()

    def _change_password(self) -> None:
        dialog = ChangePasswordDialog(self._snapshot.has_password, parent=self._view)

        def done(_result) -> None:
            dialog.accept()
            self._notice("Password saved.", "good")
            self._reload_snapshot(self._reload_security)
        dialog.submitted.connect(lambda current, new, confirm: self._run(
            lambda: self._security.change_password(current, new, confirm), done,
            dialog.show_error))
        dialog.exec()

    def _enable_mfa(self) -> None:
        def opened(enrollment) -> None:
            dialog = TwoFactorSetupDialog(enrollment, parent=self._view)
            finished = [False]

            def done(_result) -> None:
                finished[0] = True
                dialog.accept()
                self._notice("Two-factor sign-in is on. Your other devices were signed out.",
                             "good")
                self._reload_snapshot(self._reload_security)
            dialog.submitted.connect(lambda code: self._run(
                lambda: self._security.finish_mfa_setup(enrollment.factor_id, code), done,
                dialog.show_error))
            dialog.exec()
            if not finished[0]:
                self._run(lambda: self._security.cancel_mfa_setup(enrollment.factor_id),
                          on_error=lambda _m: None)
        self._run(self._security.start_mfa_setup, opened)

    def _disable_mfa(self) -> None:
        dialog = CodeDialog("Turn off two-factor sign-in?",
                            "Enter a current code from your authenticator app to confirm. "
                            "Your account will then be protected by your password only.",
                            "Turn off", danger=True, parent=self._view)

        def done(_result) -> None:
            dialog.accept()
            self._notice("Two-factor sign-in is off.", "warn")
            self._reload_snapshot(self._reload_security)
        dialog.submitted.connect(lambda code: self._run(
            lambda: self._security.disable_mfa(code), done, dialog.show_error))
        dialog.exec()

    def _sign_out_others(self) -> None:
        dialog = ConfirmDialog(
            "Sign out all other devices?",
            "Every other computer signed in to this account will have to sign in again "
            "(within the hour, when its current access expires). This computer stays "
            "signed in.", "Sign them out", "log-out", danger=True, parent=self._view)
        if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
            return

        def done(_result) -> None:
            self._notice("Other devices were signed out.", "good")
            self._reload_security()
        self._run(self._security.sign_out_other_devices, done)

    def _forget_device(self, device: Device) -> None:
        dialog = ConfirmDialog(
            f"Remove {device.device_name}?",
            "It is taken off this list. If it is still signed in, use “Sign out all "
            "other devices” to end that session too.", "Remove", "monitor",
            parent=self._view)
        if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
            return
        self._run(lambda: self._security.forget_device(device),
                  lambda _r: self._reload_security())

    def _more_events(self) -> None:
        if not self._events:
            return
        last = self._events[-1].id

        def done(events) -> None:
            self._events.extend(events)
            self._view.security.show_events(events, True, len(events) >= EVENTS_PAGE)
        self._run(lambda: self._security.events(EVENTS_PAGE, before_id=last), done)

    # ----------------------------------------------------------- privacy

    def _accept_documents(self) -> None:
        dialog = LegalDialog(accept=True, version=TERMS_VERSION, parent=self._view)

        def done(_r) -> None:
            dialog.accept()
            self._reload_snapshot()
        dialog.accepted_documents.connect(lambda: self._run(
            self._account.accept_documents, done, dialog.show_error))
        dialog.sign_out.connect(dialog.reject)
        dialog.exec()

    def _set_tracking(self, on: bool) -> None:
        def done(profile) -> None:
            self._snapshot.profile = profile
            self._tracker.enabled = on
            if not on:
                self._tracker.take()        # drop anything not yet sent
            self._render()
            if on:
                self._load_activity()

        def failed(message: str) -> None:
            self._view.privacy.tracking.set_checked(not on)
            self._notice(message, "danger")
        self._run(lambda: self._account.set_tracking(self._snapshot.profile, on), done, failed)

    def _clear_cache(self) -> None:
        dialog = ConfirmDialog(
            "Clear downloaded reference data?",
            "The downloaded disease, symptom and medicine entries are removed the next time "
            "Akeso starts, then downloaded fresh. Your notes, bookmarks and saved cases stay.",
            "Clear at next start", "refresh-cw", parent=self._view)
        if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
            return
        try:
            self._local.schedule_cache_clear()
        except OSError as exc:
            self._notice(f"Could not schedule it: {exc}", "danger")
            return
        self._view.privacy.set_clear_pending(True)
        self._notice("Done. The reference data will re-download the next time you open "
                     "Akeso.", "good")

    def _export(self) -> None:
        folder = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation)
        default = str(Path(folder) / f"akeso-export-{date.today().isoformat()}.zip")
        path, _ = QFileDialog.getSaveFileName(self._view, "Save your Akeso data", default,
                                              "ZIP archive (*.zip)")
        if not path:
            return
        self.flush_activity()
        self._view.privacy.set_export_busy(True, "Collecting your data…")

        def done(target) -> None:
            self._view.privacy.set_export_busy(False, f"Saved to {target}")
            self._notice(f"Your data was exported to {target}. Keep that file private.",
                         "good")
            self._reload_security()
        self._run(lambda: self._account.export(Path(path)), done,
                  lambda m: self._view.privacy.set_export_busy(False, m))

    def _delete(self) -> None:
        dialog = DeleteAccountDialog(parent=self._view)

        def done(_due) -> None:
            dialog.accept()
            self._reload_snapshot(self._reload_security)
        dialog.submitted.connect(lambda text, erase: self._run(
            lambda: self._account.request_deletion(text, erase), done, dialog.show_error))
        dialog.exec()

    def _cancel_deletion(self) -> None:
        def done(profile) -> None:
            self._snapshot.profile = profile
            self._render()
            self._notice("Your account will not be deleted.", "good")
        self._run(self._account.cancel_deletion, done)

    # ---------------------------------------------------------- activity

    def flush_activity(self) -> None:
        if not self._tracker.pending():
            return
        counts = self._tracker.take()
        self._run(lambda: self._account.record_activity(counts),
                  on_error=lambda _m: self._tracker.restore(counts))

    def shutdown(self, timeout: float = 3.0) -> None:
        """Before signing out: send the last counts and log the sign-out.

        Runs on a plain thread with a time limit, so an offline computer
        waits at most a few seconds instead of hanging the sign-out.
        """
        self._flush_timer.stop()
        counts = self._tracker.take()

        def last_calls() -> None:
            try:
                if counts:
                    self._account.record_activity(counts)
                self._security.record_sign_out()
            except Exception:  # noqa: BLE001 - best effort on the way out
                pass
        worker = threading.Thread(target=last_calls, daemon=True)
        worker.start()
        worker.join(timeout)
