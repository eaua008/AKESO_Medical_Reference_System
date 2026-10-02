"""Account > Privacy & data: consents, tracking, local data, export, delete."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from app.models.account import (
    DELETION_GRACE_DAYS, PRIVACY_VERSION, TERMS_VERSION, AccountSnapshot, friendly_time,
)
from app.ui.components.fluid import ResponsiveGrid
from app.ui.views.account.account_widgets import Card, SwitchRow, button, label, set_text


class PrivacyTab(QWidget):
    accept_requested = Signal()
    read_terms_requested = Signal()
    read_privacy_requested = Signal()
    tracking_toggled = Signal(bool)
    clear_cache_requested = Signal()
    export_requested = Signal()
    delete_requested = Signal()
    cancel_deletion_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)
        self.grid = ResponsiveGrid(400, max_columns=2, spacing=16, steps=(2, 1))
        self.grid.set_cards([self._build_documents(), self._build_tracking(),
                             self._build_export(), self._build_local()])
        root.addWidget(self.grid)
        root.addWidget(self._build_delete())

    # -------------------------------------------------------------- cards

    def _build_documents(self) -> Card:
        card = Card("Terms and Privacy Notice", "What you agreed to, and when.", "file-text")
        self._terms_state = label("", "acValue")
        self._privacy_state = label("", "acValue")
        card.body.addWidget(self._terms_state)
        card.body.addWidget(self._privacy_state)
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(button("Read Terms", "acGhost", on_click=self.read_terms_requested.emit))
        row.addWidget(button("Read Privacy Notice", "acGhost",
                             on_click=self.read_privacy_requested.emit))
        row.addStretch(1)
        card.body.addLayout(row)
        self._accept = button(f"Accept version {TERMS_VERSION}", "acPrimary", "check",
                              self.accept_requested.emit)
        card.body.addWidget(self._accept, 0, Qt.AlignmentFlag.AlignLeft)
        card.body.addStretch(1)
        return card

    def _build_tracking(self) -> Card:
        card = Card("Study activity", "Daily counts behind your streak and weekly totals.",
                    "activity")
        self.tracking = SwitchRow("Track my study activity",
                                  "Counts pages you open and checker runs, per day. Never "
                                  "which entries, never what you type.")
        self.tracking.toggled.connect(self.tracking_toggled.emit)
        card.body.addWidget(self.tracking)
        card.body.addWidget(label("Turning it off stops new counting at once. Past days stay "
                                  "until you delete your account.", "acSmall"))
        card.body.addStretch(1)
        return card

    def _build_export(self) -> Card:
        card = Card("Export my data", "Everything Akeso keeps about you, in one ZIP file "
                    "you can open with any text editor.", "download")
        card.body.addWidget(label("Includes your profile, devices, activity log, consents, "
                                  "study counters, and the notes, cases, bookmarks, "
                                  "medications and search history saved on this computer.", "acSmall"))
        self._export = button("Export my data", "acGhost", "download", self.export_requested.emit)
        card.body.addWidget(self._export, 0, Qt.AlignmentFlag.AlignLeft)
        self._export_status = label("", "acSmall")
        card.body.addWidget(self._export_status)
        card.body.addStretch(1)
        return card

    def _build_local(self) -> Card:
        card = Card("This computer", "Reference entries downloaded so Akeso works "
                    "offline.", "monitor")
        self._cache_size = label("", "acValue")
        card.body.addWidget(self._cache_size)
        self._clear = button("Clear downloaded reference data", "acGhost", "refresh-cw",
                             self.clear_cache_requested.emit)
        card.body.addWidget(self._clear, 0, Qt.AlignmentFlag.AlignLeft)
        self._clear_note = label("Removed the next time Akeso starts, then downloaded fresh. "
                                 "Your notes and saved cases are not touched.", "acSmall")
        card.body.addWidget(self._clear_note)
        card.body.addStretch(1)
        return card

    def _build_delete(self) -> Card:
        card = Card("Delete account", f"Removes your account and everything on Akeso's "
                    f"server. You have {DELETION_GRACE_DAYS} days to change your mind: "
                    "signing in during that time offers to cancel.", "trash-2", danger=True)
        self._delete_state = label("", "acValue")
        card.body.addWidget(self._delete_state)
        row = QHBoxLayout()
        self._delete = button("Delete my account…", "acDanger", "trash-2",
                              self.delete_requested.emit)
        self._cancel_delete = button("Keep my account", "acPrimary", "check",
                                     self.cancel_deletion_requested.emit)
        row.addWidget(self._delete)
        row.addWidget(self._cancel_delete)
        row.addStretch(1)
        card.body.addLayout(row)
        return card

    def watch(self, viewport: QWidget) -> None:
        self.grid.watch(viewport)

    # --------------------------------------------------------------- data

    def show_snapshot(self, snapshot: AccountSnapshot, cache_bytes: int,
                      clear_pending: bool) -> None:
        terms = snapshot.accepted("terms", TERMS_VERSION)
        privacy = snapshot.accepted("privacy", PRIVACY_VERSION)
        self._terms_state.setText(
            f"Terms of Use {TERMS_VERSION}: accepted {friendly_time(terms.accepted_at)}"
            if terms else f"Terms of Use {TERMS_VERSION}: not accepted yet")
        self._privacy_state.setText(
            f"Privacy Notice {PRIVACY_VERSION}: accepted {friendly_time(privacy.accepted_at)}"
            if privacy else f"Privacy Notice {PRIVACY_VERSION}: not accepted yet")
        self._accept.setVisible(not (terms and privacy))

        self.tracking.set_checked(snapshot.profile.track_study_activity)

        size = cache_bytes / (1024 * 1024)
        self._cache_size.setText(f"{size:.1f} MB of reference data on this computer."
                                 if cache_bytes else "No reference data downloaded yet.")
        self.set_clear_pending(clear_pending)

        profile = snapshot.profile
        if profile.deletion_pending:
            self._delete_state.setText(
                f"Scheduled: your account will be deleted on "
                f"{friendly_time(profile.deletion_scheduled_for, with_time=False)}.")
            self._delete_state.setObjectName("acError")
        else:
            self._delete_state.setText("")
            self._delete_state.setObjectName("acValue")
        self._delete_state.style().unpolish(self._delete_state)
        self._delete_state.style().polish(self._delete_state)
        self._delete_state.setVisible(profile.deletion_pending)
        self._delete.setVisible(not profile.deletion_pending)
        self._cancel_delete.setVisible(profile.deletion_pending)

    def set_clear_pending(self, pending: bool) -> None:
        self._clear.setEnabled(not pending)
        if pending:
            set_text(self._clear, "Will clear at next start")

    def set_export_busy(self, busy: bool, message: str = "") -> None:
        self._export.setEnabled(not busy)
        self._export_status.setText(message)
