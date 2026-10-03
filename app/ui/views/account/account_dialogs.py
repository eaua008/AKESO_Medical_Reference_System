"""Dialogs for the Account module.

Display only, like every other view: they collect input and emit it. The
account controller does the work (on a background thread) and then calls
show_error() or accept() on the dialog.
"""

from typing import Optional

from PySide6.QtCore import QByteArray, QRectF, Qt, Signal
from PySide6.QtGui import QGuiApplication, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QCheckBox, QDialog, QHBoxLayout, QLabel, QLayout, QLineEdit, QPushButton, QStackedWidget,
    QTextBrowser, QVBoxLayout, QWidget,
)

from app.core.legal_text import PRIVACY_HTML, PRIVACY_TITLE, TERMS_HTML, TERMS_TITLE
from app.core.theme import Theme
from app.models.account import DELETION_GRACE_DAYS, MfaEnrollment, friendly_time
from app.services.security_service import PASSWORD_RULES
from app.ui.theme_scope import app_mode, stylesheet
from app.ui.views.account.account_widgets import (
    button, field_block, icon_label, label, refresh_icons, repolish, set_text,
)


def match_theme(window: QWidget) -> None:
    """New windows get the app-level stylesheet, which may still be the old
    theme after a light/dark switch (see theme_scope.py). Give this window
    the current one."""
    if Theme.mode() != app_mode():
        window.setStyleSheet(stylesheet(Theme.mode()))


class AccountDialog(QDialog):
    """Common frame: icon, title, message, body, error line, buttons."""

    def __init__(self, title: str, message: str = "", icon: str = "",
                 parent: Optional[QWidget] = None, width: int = 440,
                 danger: bool = False) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setObjectName("acDialog")
        match_theme(self)

        root = QVBoxLayout(self)
        # Never smaller than the content: without this Qt may squeeze the
        # dialog and let the QR code or the text box overlap their neighbours.
        root.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        root.setContentsMargins(24, 22, 24, 20)
        root.setSpacing(12)
        head = QHBoxLayout()
        head.setSpacing(10)
        if icon:
            head.addWidget(icon_label(icon, 22, Theme.token("DANGER") if danger else None),
                           0, Qt.AlignmentFlag.AlignTop)
        head.addWidget(label(title, "acDangerTitle" if danger else "acCardTitle"), 1)
        root.addLayout(head)
        if message:
            self.message = label(message, "acMuted")
            root.addWidget(self.message)
        self.body = QVBoxLayout()
        self.body.setSpacing(10)
        root.addLayout(self.body)
        self.error = label("", "acError")
        self.error.hide()
        root.addWidget(self.error)
        self.buttons = QHBoxLayout()
        self.buttons.setSpacing(8)
        self.buttons.addStretch(1)
        root.addLayout(self.buttons)
        # The dialog's width. (A size constraint on the layout overrides
        # setMinimumWidth, so an invisible strut sets it instead.)
        strut = QWidget()
        strut.setObjectName("panel")
        strut.setFixedSize(width - 48, 0)
        root.addWidget(strut)
        self._busy_widgets: list[QWidget] = []

    def showEvent(self, event) -> None:  # noqa: N802
        # Wrapped text is taller the narrower the dialog is, and a plain
        # minimum size does not account for that. Make room for all of it.
        super().showEvent(event)
        layout = self.layout()
        if layout is not None and layout.hasHeightForWidth():
            need = layout.totalHeightForWidth(self.width())
            if need > self.height():
                self.setMinimumHeight(need)
                self.resize(self.width(), need)

    def add_button(self, text: str, name: str = "acGhost", icon: str = "",
                   on_click=None, default: bool = False) -> QPushButton:
        widget = button(text, name, icon, on_click)
        if default:
            widget.setDefault(True)
        self.buttons.addWidget(widget)
        self._busy_widgets.append(widget)
        return widget

    def show_error(self, message: str) -> None:
        self.set_busy(False)
        self.error.setObjectName("acError")
        repolish(self.error)
        self.error.setText(message)
        self.error.setVisible(bool(message))

    def show_info(self, message: str) -> None:
        self.error.setObjectName("acOk")
        repolish(self.error)
        self.error.setText(message)
        self.error.setVisible(bool(message))

    def set_busy(self, busy: bool) -> None:
        for widget in self._busy_widgets:
            widget.setEnabled(not busy)
        self.setCursor(Qt.CursorShape.WaitCursor if busy else Qt.CursorShape.ArrowCursor)


def _password_field(placeholder: str) -> QLineEdit:
    field = QLineEdit()
    field.setObjectName("acInput")
    field.setEchoMode(QLineEdit.EchoMode.Password)
    field.setPlaceholderText(placeholder)
    return field


def _code_field() -> QLineEdit:
    field = QLineEdit()
    field.setObjectName("acCode")
    field.setMaxLength(7)
    field.setPlaceholderText("000000")
    field.setAlignment(Qt.AlignmentFlag.AlignCenter)
    field.setInputMask("")
    return field


# ------------------------------------------------------------------ password

class ChangePasswordDialog(AccountDialog):
    submitted = Signal(str, str, str)

    def __init__(self, has_password: bool, parent: Optional[QWidget] = None) -> None:
        super().__init__(
            "Change password" if has_password else "Add a password",
            "Other devices stay signed in. To sign them out too, use “Sign out all "
            "other devices” afterwards." if has_password else
            "You can then sign in with your email and this password as well as Google.",
            "lock", parent)
        self.current = _password_field("Current password")
        if has_password:
            self.body.addWidget(field_block("Current password", self.current))
        self.new = _password_field("New password")
        self.confirm = _password_field("Type it again")
        self.body.addWidget(field_block("New password", self.new))
        self.body.addWidget(field_block("Confirm new password", self.confirm))
        self._rules: list[QLabel] = []
        for text, _check in PASSWORD_RULES:
            rule = label(f"• {text}", "acSmall")
            self._rules.append(rule)
            self.body.addWidget(rule)
        self.new.textChanged.connect(self._update_rules)
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Save password", "acPrimary", "check", self._submit, default=True)

    def _update_rules(self, text: str) -> None:
        for rule, (_label, check) in zip(self._rules, PASSWORD_RULES):
            rule.setObjectName("acOk" if check(text) else "acSmall")
            repolish(rule)

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self.current.text(), self.new.text(), self.confirm.text())


# --------------------------------------------------------------------- email

class ChangeEmailDialog(AccountDialog):
    submitted = Signal(str, str)

    def __init__(self, current_email: str, has_password: bool,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(
            "Change email",
            f"You sign in as {current_email}. Supabase sends a confirmation link; the "
            "change happens only after you open it (with secure email change on, a link "
            "goes to both addresses).", "mail", parent)
        self.email = QLineEdit()
        self.email.setObjectName("acInput")
        self.email.setPlaceholderText("new.address@example.com")
        self.body.addWidget(field_block("New email", self.email))
        self.password = _password_field("Your password")
        if has_password:
            self.body.addWidget(field_block("Current password", self.password,
                                            "So nobody at an unlocked computer can move "
                                            "your account."))
        self.body.addWidget(label("Your notes and saved cases on this computer move to the "
                                  "new address automatically the next time you sign in.",
                                  "acSmall"))
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Send confirmation", "acPrimary", "mail", self._submit, default=True)

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self.email.text(), self.password.text())


# ------------------------------------------------------------------ 2FA setup

def svg_pixmap(svg: str, size: int) -> QPixmap:
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    scale = 2
    image = QPixmap(size * scale, size * scale)
    image.fill(Qt.GlobalColor.white)       # QR codes need a light background to scan
    painter = QPainter(image)
    renderer.render(painter, QRectF(8, 8, size * scale - 16, size * scale - 16))
    painter.end()
    image.setDevicePixelRatio(scale)
    return image


class TwoFactorSetupDialog(AccountDialog):
    submitted = Signal(str)

    def __init__(self, enrollment: MfaEnrollment, parent: Optional[QWidget] = None) -> None:
        super().__init__(
            "Turn on two-factor sign-in",
            "1. Open an authenticator app on your phone and scan this code.", "smartphone",
            parent, width=460)
        qr = QLabel()
        qr.setObjectName("panel")
        qr.setFixedSize(200, 200)
        qr.setPixmap(svg_pixmap(enrollment.qr_svg, 200))
        self.body.addWidget(qr, 0, Qt.AlignmentFlag.AlignHCenter)
        self.body.addWidget(label("Can't scan it? Type this key into the app instead:",
                                  "acSmall"))
        secret_row = QHBoxLayout()
        secret = QLineEdit(" ".join(enrollment.secret[i:i + 4]
                                    for i in range(0, len(enrollment.secret), 4)))
        secret.setObjectName("acSecret")
        secret.setReadOnly(True)
        secret_row.addWidget(secret, 1)
        copy = button("Copy", "acGhost", "copy",
                      lambda: QGuiApplication.clipboard().setText(enrollment.secret))
        secret_row.addWidget(copy)
        self.body.addLayout(secret_row)
        self.body.addWidget(label("2. Enter the 6-digit code the app shows.", "acMuted"))
        self.code = _code_field()
        self.body.addWidget(self.code)
        self.body.addWidget(label("Turning this on signs out your other devices; they will "
                                  "need a code next time.", "acSmall"))
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Turn on", "acPrimary", "shield-check", self._submit, default=True)
        self.code.returnPressed.connect(self._submit)

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self.code.text())


class CodeDialog(AccountDialog):
    """Ask for a current authenticator code (sign-in, or turning 2FA off)."""

    submitted = Signal(str)
    secondary = Signal()

    def __init__(self, title: str, message: str, action: str, secondary: str = "",
                 danger: bool = False, parent: Optional[QWidget] = None) -> None:
        super().__init__(title, message, "smartphone", parent, danger=danger)
        self.code = _code_field()
        self.body.addWidget(self.code)
        self.code.returnPressed.connect(self._submit)
        if secondary:
            self.add_button(secondary, on_click=self.secondary.emit)
        else:
            self.add_button("Cancel", on_click=self.reject)
        self.add_button(action, "acDanger" if danger else "acPrimary", "", self._submit,
                        default=True)

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self.code.text())

    def show_error(self, message: str) -> None:
        super().show_error(message)
        self.code.selectAll()
        self.code.setFocus()


# -------------------------------------------------------------- school email

class SchoolEmailDialog(AccountDialog):
    send_requested = Signal(str)
    verify_requested = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__("Verify your school email",
                         "We email a 6-digit code to your school address. Only the "
                         "school's domain is saved on your profile.", "graduation-cap", parent)
        self.pages = QStackedWidget()
        self.body.addWidget(self.pages)

        first = QWidget()
        first.setObjectName("panel")
        column = QVBoxLayout(first)
        column.setContentsMargins(0, 0, 0, 0)
        self.email = QLineEdit()
        self.email.setObjectName("acInput")
        self.email.setPlaceholderText("juan.delacruz@school.edu.ph")
        column.addWidget(field_block("School email", self.email,
                                     "Must end in .edu.ph or .edu."))
        self.pages.addWidget(first)

        second = QWidget()
        second.setObjectName("panel")
        column = QVBoxLayout(second)
        column.setContentsMargins(0, 0, 0, 0)
        self._sent_to = label("", "acMuted")
        column.addWidget(self._sent_to)
        self.code = _code_field()
        column.addWidget(self.code)
        self._resend = button("Send a new code", "acLink", on_click=self._send)
        column.addWidget(self._resend, 0, Qt.AlignmentFlag.AlignLeft)
        self.pages.addWidget(second)

        self.add_button("Cancel", on_click=self.reject)
        self._main = self.add_button("Send code", "acPrimary", "mail", self._primary,
                                     default=True)
        self.email.returnPressed.connect(self._primary)
        self.code.returnPressed.connect(self._primary)

    def _primary(self) -> None:
        if self.pages.currentIndex() == 0:
            self._send()
        else:
            self.set_busy(True)
            self.verify_requested.emit(self.code.text())

    def _send(self) -> None:
        self.set_busy(True)
        self.send_requested.emit(self.email.text())

    def code_sent(self, domain: str) -> None:
        self.set_busy(False)
        self.pages.setCurrentIndex(1)
        self._sent_to.setText(f"Code sent to your address at {domain}. It expires in 15 "
                              "minutes. Check spam if it's not there.")
        set_text(self._main, "Verify")
        self.show_info("")
        self.code.setFocus()


# ------------------------------------------------------------------- delete

class DeleteAccountDialog(AccountDialog):
    submitted = Signal(str, bool)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(
            "Delete your account?",
            f"Your account will be deleted in {DELETION_GRACE_DAYS} days, together with your "
            "profile, photo, devices, activity log and study counters. Sign in before then "
            "to cancel. After that it cannot be undone.", "trash-2", parent, danger=True)
        self.body.addWidget(label("Tip: export your data first (Privacy & data > Export).",
                                  "acSmall"))
        self.erase_local = QCheckBox("Also remove my data from this computer now")
        self.body.addWidget(self.erase_local)
        self.body.addWidget(label("Your notes, saved cases, bookmarks and medications on this "
                                  "computer. This part happens at once and can't be undone.",
                                  "acSmall"))
        self.confirm = QLineEdit()
        self.confirm.setObjectName("acInput")
        self.confirm.setPlaceholderText("DELETE")
        self.body.addWidget(field_block("Type DELETE to confirm", self.confirm))
        self.add_button("Cancel", on_click=self.reject)
        self._go = self.add_button("Schedule deletion", "acDanger", "trash-2", self._submit)
        self._go.setEnabled(False)
        self.confirm.textChanged.connect(lambda t: self._go.setEnabled(t.strip() == "DELETE"))

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self.confirm.text(), self.erase_local.isChecked())


# ------------------------------------------------------------------- legal

class LegalDialog(AccountDialog):
    """Read the Terms or the Privacy Notice; or, with accept=True, both,
    with Accept and Sign out (the sign-in consent step)."""

    accepted_documents = Signal()
    sign_out = Signal()

    def __init__(self, which: str = "terms", accept: bool = False,
                 version: str = "", parent: Optional[QWidget] = None) -> None:
        if accept:
            title = "Please review and accept"
            message = (f"Akeso's Terms of Use and Privacy Notice (version {version}). "
                       "You'll be asked again only if they change.")
            html = f"<h2>{TERMS_TITLE}</h2>{TERMS_HTML}<hr><h2>{PRIVACY_TITLE}</h2>{PRIVACY_HTML}"
        elif which == "privacy":
            title, message, html = PRIVACY_TITLE, "", PRIVACY_HTML
        else:
            title, message, html = TERMS_TITLE, "", TERMS_HTML
        super().__init__(title, message, "file-text", parent, width=560)
        text = QTextBrowser()
        text.setObjectName("acLegal")
        text.setOpenExternalLinks(False)
        text.setHtml(html)
        text.setMinimumHeight(360)
        self.body.addWidget(text)
        if accept:
            self._agree = QCheckBox("I have read and accept both documents.")
            self.body.addWidget(self._agree)
            self.add_button("Sign out", on_click=self.sign_out.emit)
            go = self.add_button("Accept and continue", "acPrimary", "check",
                                 self._accept, default=True)
            go.setEnabled(False)
            self._agree.toggled.connect(go.setEnabled)
        else:
            self.add_button("Close", "acPrimary", on_click=self.accept, default=True)

    def _accept(self) -> None:
        self.set_busy(True)
        self.accepted_documents.emit()


class DeletionPendingDialog(AccountDialog):
    keep = Signal()
    leave = Signal()

    def __init__(self, scheduled_for, parent: Optional[QWidget] = None) -> None:
        super().__init__(
            "Your account is scheduled for deletion",
            f"It will be deleted on {friendly_time(scheduled_for, with_time=False)}. "
            "Do you want to keep it?", "triangle-alert", parent, danger=True)
        self.add_button("Sign out", on_click=self.leave.emit)
        self.add_button("Keep my account", "acPrimary", "check", self._keep, default=True)

    def _keep(self) -> None:
        self.set_busy(True)
        self.keep.emit()


class ConfirmDialog(AccountDialog):
    def __init__(self, title: str, message: str, action: str, icon: str = "circle-alert",
                 danger: bool = False, parent: Optional[QWidget] = None) -> None:
        super().__init__(title, message, icon, parent, danger=danger)
        self.add_button("Cancel", on_click=self.reject)
        self.add_button(action, "acDanger" if danger else "acPrimary", "", self.accept,
                        default=True)


def refresh_dialog_icons(dialog: QWidget) -> None:
    refresh_icons(dialog)
