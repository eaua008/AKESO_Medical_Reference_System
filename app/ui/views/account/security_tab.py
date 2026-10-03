"""Account > Security: sign-in, two-factor, devices, activity log."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from app.models.account import AccountSnapshot, Device, SecurityEvent, friendly_time
from app.ui.components.fluid import ResponsiveGrid
from app.ui.views.account.account_widgets import (
    Card, DeviceRow, EventRow, button, label, pill, set_text,
)
from app.ui.views.account.overview_tab import _clear

PROVIDER_LABELS = {"email": "Email and password", "google": "Google"}


class SecurityTab(QWidget):
    change_email_requested = Signal()
    change_password_requested = Signal()
    enable_mfa_requested = Signal()
    disable_mfa_requested = Signal()
    sign_out_others_requested = Signal()
    forget_device_requested = Signal(object)
    more_events_requested = Signal()
    refresh_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)
        self.grid = ResponsiveGrid(400, max_columns=2, spacing=16, steps=(2, 1))
        self.grid.set_cards([self._build_sign_in(), self._build_mfa()])
        root.addWidget(self.grid)
        root.addWidget(self._build_devices())
        root.addWidget(self._build_log())

    # -------------------------------------------------------------- cards

    def _build_sign_in(self) -> Card:
        card = Card("Sign-in", "The email and password you sign in with.", "key-round")
        self._email = label("", "acRowTitle")
        self._pending = label("", "acSmall")
        card.body.addWidget(label("EMAIL", "acFieldLabel", wrap=False))
        card.body.addWidget(self._email)
        card.body.addWidget(self._pending)
        card.body.addWidget(button("Change email", "acGhost", "mail",
                                   self.change_email_requested.emit),
                            0, Qt.AlignmentFlag.AlignLeft)
        card.body.addSpacing(4)
        card.body.addWidget(label("PASSWORD", "acFieldLabel", wrap=False))
        self._password_note = label("", "acSmall")
        card.body.addWidget(self._password_note)
        self._password_button = button("Change password", "acGhost", "lock",
                                       self.change_password_requested.emit)
        card.body.addWidget(self._password_button, 0, Qt.AlignmentFlag.AlignLeft)
        card.body.addSpacing(4)
        card.body.addWidget(label("SIGN-IN METHODS", "acFieldLabel", wrap=False))
        self._providers = QHBoxLayout()
        self._providers.setSpacing(6)
        card.body.addLayout(self._providers)
        card.body.addStretch(1)
        return card

    def _build_mfa(self) -> Card:
        card = Card("Two-factor sign-in", "After your password, Akeso also asks for a "
                    "6-digit code from an authenticator app on your phone (Google "
                    "Authenticator, Microsoft Authenticator, Authy…).", "smartphone")
        state = QHBoxLayout()
        self._mfa_pill = pill("Off", "acPillWarn")
        state.addWidget(self._mfa_pill)
        state.addStretch(1)
        card.body.addLayout(state)
        self._mfa_note = label("", "acSmall")
        card.body.addWidget(self._mfa_note)
        self._mfa_on = button("Turn on two-factor", "acPrimary", "shield-check",
                              self.enable_mfa_requested.emit)
        self._mfa_off = button("Turn off two-factor", "acDanger", on_click=self.disable_mfa_requested.emit)
        card.body.addWidget(self._mfa_on, 0, Qt.AlignmentFlag.AlignLeft)
        card.body.addWidget(self._mfa_off, 0, Qt.AlignmentFlag.AlignLeft)
        card.body.addStretch(1)
        return card

    def _build_devices(self) -> Card:
        card = Card("Devices", "Computers where this account has signed in to Akeso.",
                    "monitor")
        self._devices = QVBoxLayout()
        self._devices.setSpacing(8)
        card.body.addLayout(self._devices)
        row = QHBoxLayout()
        row.addWidget(label("Lost a laptop, or used a shared computer? Sign everywhere "
                            "else out. This computer stays signed in.", "acSmall"), 1)
        self._sign_out_others = button("Sign out all other devices", "acDanger", "log-out",
                                       self.sign_out_others_requested.emit)
        row.addWidget(self._sign_out_others, 0, Qt.AlignmentFlag.AlignVCenter)
        card.body.addLayout(row)
        return card

    def _build_log(self) -> Card:
        card = Card("Account activity", "Sign-ins and changes to your account. Recorded by "
                    "Akeso's server; nobody can edit or remove a line.", "history")
        refresh = button("Refresh", "acLink", on_click=self.refresh_requested.emit)
        card.head.addWidget(refresh, 0, Qt.AlignmentFlag.AlignTop)
        self._events = QVBoxLayout()
        self._events.setSpacing(6)
        card.body.addLayout(self._events)
        self._more = button("Show older activity", "acGhost", on_click=self.more_events_requested.emit)
        card.body.addWidget(self._more, 0, Qt.AlignmentFlag.AlignHCenter)
        return card

    def watch(self, viewport: QWidget) -> None:
        self.grid.watch(viewport)

    # --------------------------------------------------------------- data

    def show_snapshot(self, snapshot: AccountSnapshot) -> None:
        self._email.setText(snapshot.email)
        if snapshot.pending_email:
            self._pending.setText(
                f"Waiting for confirmation: {snapshot.pending_email}. Open the link Supabase "
                "emailed you (check both inboxes).")
            self._pending.show()
        else:
            self._pending.hide()
        if snapshot.has_password:
            self._password_note.setText("Set. Akeso never sees it; the server keeps only a "
                                        "one-way hash.")
            set_text(self._password_button, "Change password")
        else:
            self._password_note.setText("You sign in with Google. Add a password to also sign "
                                        "in with your email.")
            set_text(self._password_button, "Add a password")
        _clear(self._providers)
        for provider in snapshot.providers or ["email"]:
            self._providers.addWidget(pill(PROVIDER_LABELS.get(provider, provider.title())))
        self._providers.addStretch(1)

        mfa = snapshot.mfa
        self._mfa_pill.setText("On" if mfa.enabled else "Off")
        self._mfa_pill.setObjectName("acPillGood" if mfa.enabled else "acPillWarn")
        self._mfa_pill.style().unpolish(self._mfa_pill)
        self._mfa_pill.style().polish(self._mfa_pill)
        self._mfa_note.setText(
            f"On since {friendly_time(mfa.since, with_time=False)}. You'll be asked for a code "
            "each time you sign in." if mfa.enabled else
            "Recommended. Even if someone learns your password, they can't sign in "
            "without your phone.")
        self._mfa_on.setVisible(not mfa.enabled)
        self._mfa_off.setVisible(mfa.enabled)

    def show_devices(self, devices: list[Device]) -> None:
        _clear(self._devices)
        if not devices:
            self._devices.addWidget(label("No devices recorded yet.", "acMuted"))
        for device in devices:
            row = DeviceRow(device)
            row.forget.connect(self.forget_device_requested.emit)
            self._devices.addWidget(row)

    def show_events(self, events: list[SecurityEvent], append: bool, has_more: bool) -> None:
        if not append:
            _clear(self._events)
        if not events and not append:
            self._events.addWidget(label("No activity recorded yet.", "acMuted"))
        for event in events:
            self._events.addWidget(EventRow(event))
        self._more.setVisible(has_more)
