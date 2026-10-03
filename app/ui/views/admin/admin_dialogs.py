"""Dialogs for User Management: role, suspend, delete, account details."""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QPlainTextEdit, QRadioButton, QVBoxLayout, QWidget

from app.models.account import EVENT_LABELS, PROGRAM_LABELS, YEAR_LABELS, friendly_time
from app.models.admin import ROLES, STATUS_LABELS, AdminUser, UserDetail
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import label, repolish


class _RoleCard(QFrame):
    """One choice in the role picker: the whole card is clickable."""

    chosen = Signal(str)

    def __init__(self, value: str, name: str, description: str) -> None:
        super().__init__()
        self.setObjectName("adRoleCard")
        self.setProperty("role", value)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.value = value
        row = QHBoxLayout(self)
        row.setContentsMargins(14, 12, 14, 12)
        row.setSpacing(12)
        self.radio = QRadioButton()
        self.radio.toggled.connect(lambda on: on and self.chosen.emit(self.value))
        row.addWidget(self.radio, 0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(3)
        title = label(name, "adRoleName", wrap=False)
        title.setProperty("role", value)
        text.addWidget(title)
        text.addWidget(label(description, "acSmall"))
        row.addLayout(text, 1)

    def set_selected(self, selected: bool) -> None:
        self.radio.setChecked(selected)
        self.setProperty("selected", "true" if selected else "false")
        repolish(self)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.radio.setChecked(True)
        super().mouseReleaseEvent(event)


class RoleDialog(AccountDialog):
    submitted = Signal(str)

    def __init__(self, user: AdminUser, parent: Optional[QWidget] = None) -> None:
        super().__init__("Modify user role", f"Target: {user.display_name} ({user.email})",
                         "shield", parent, width=520)
        self._role = user.role
        self.body.addWidget(label("SELECT ROLE", "acFieldLabel", wrap=False))
        self._cards: list[_RoleCard] = []
        for value, name, description in ROLES:
            card = _RoleCard(value, name, description)
            card.chosen.connect(self._choose)
            self.body.addWidget(card)
            self._cards.append(card)
        if user.is_me:
            self.body.addWidget(label(
                "This is your own account. If you stop being an admin you lose access to "
                "this panel straight away.", "acError"))
        self.add_button("Cancel", on_click=self.reject)
        self._save = self.add_button("Save role", "acPrimary", "check",
                                     lambda: self.submitted.emit(self._role))
        self._original = user.role
        self._choose(user.role)

    def _choose(self, role: str) -> None:
        self._role = role
        for card in self._cards:
            card.set_selected(card.value == role)
        if hasattr(self, "_save"):
            self._save.setEnabled(role != self._original)


class SuspendDialog(AccountDialog):
    submitted = Signal(str)     # reason

    def __init__(self, user: AdminUser, parent: Optional[QWidget] = None) -> None:
        super().__init__(
            "Suspend account",
            f"{user.display_name} ({user.email}) will be signed out within the hour and "
            "can't sign in until you reactivate the account. Nothing is deleted.",
            "user-x", parent, width=480, danger=True)
        self.reason = QPlainTextEdit()
        self.reason.setObjectName("acInput")
        self.reason.setPlaceholderText("Reason (shown to the user when they try to sign in)")
        self.reason.setFixedHeight(80)
        self.body.addWidget(self.reason)
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Suspend", "acDanger", "user-x",
                        lambda: self.submitted.emit(self.reason.toPlainText().strip()[:300]))


class DeleteUserDialog(AccountDialog):
    submitted = Signal(str)     # what was typed

    def __init__(self, user: AdminUser, parent: Optional[QWidget] = None) -> None:
        super().__init__(
            "Delete account",
            f"This permanently deletes {user.display_name} ({user.email}): their profile, "
            "role, devices, activity log, and their Clinical Exchange posts and replies. "
            "It cannot be undone. Suspending is the reversible option.",
            "trash-2", parent, width=480, danger=True)
        self.confirm = QLineEdit()
        self.confirm.setObjectName("acInput")
        self.confirm.setPlaceholderText("Type DELETE to confirm")
        self.body.addWidget(self.confirm)
        self.add_button("Cancel", on_click=self.reject)
        self._go = self.add_button("Delete account", "acDanger", "trash-2",
                                   lambda: self.submitted.emit(self.confirm.text()))
        self._go.setEnabled(False)
        self.confirm.textChanged.connect(lambda t: self._go.setEnabled(t.strip() == "DELETE"))


class UserDetailDialog(AccountDialog):
    def __init__(self, detail: UserDetail, parent: Optional[QWidget] = None) -> None:
        user = detail.user
        super().__init__(user.display_name, user.email, "user", parent, width=520)
        rows = [
            ("Registry ID", user.registry_id),
            ("Handle", f"@{user.handle}" if user.handle else "Not set"),
            ("Role", user.role_label + (f" (since {friendly_time(detail.role_granted_at, False)}"
                                        + (f", by {detail.role_granted_by}" if detail.role_granted_by else "")
                                        + ")" if detail.role_granted_at else "")),
            ("Status", STATUS_LABELS[user.status]
             + (f": {user.suspended_reason}" if user.suspended and user.suspended_reason else "")),
            ("Program", PROGRAM_LABELS.get(detail.program or "", "") or "Not set"),
            ("School", detail.school or "Not set"),
            ("Year level", YEAR_LABELS.get(detail.year_level or 0, "") or "Not set"),
            ("School email", f"Verified ({detail.school_email_domain})"
             if detail.school_email_verified_at else "Not verified"),
            ("Account created", friendly_time(user.created_at)),
            ("Last sign-in", friendly_time(user.last_sign_in_at) if user.last_sign_in_at else "Never"),
            ("Computers", str(detail.device_count)),
        ]
        grid = QVBoxLayout()
        grid.setSpacing(6)
        for caption, value in rows:
            line = QHBoxLayout()
            name = label(caption, "acMuted", wrap=False)
            name.setFixedWidth(130)
            line.addWidget(name)
            line.addWidget(label(value, "acValue"), 1)
            grid.addLayout(line)
        self.body.addLayout(grid)
        self.body.addWidget(label("RECENT ACCOUNT ACTIVITY", "acFieldLabel", wrap=False))
        if not detail.recent_events:
            self.body.addWidget(label("No activity recorded yet.", "acSmall"))
        for event in detail.recent_events:
            text, _tone = EVENT_LABELS.get(event.get("kind"), (event.get("kind", ""), "info"))
            device = f" · {event['device']}" if event.get("device") else ""
            self.body.addWidget(label(f"{friendly_time(event.get('at'))}  —  {text}{device}",
                                      "acSmall"))
        self.body.addWidget(label("Study and health data are private and not shown here.",
                                  "acSmall"))
        self.add_button("Close", "acPrimary", on_click=self.accept, default=True)
