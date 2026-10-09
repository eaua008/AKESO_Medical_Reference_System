"""Email verification dialog.

Shown after signup, or after a login attempt on an unconfirmed account.

A dialog rather than another page in the auth card: verification is a modal
step. The user cannot usefully do anything else until it is finished or
abandoned, and a dialog says that without extra state to manage.

Display only, like every other view here. It emits what the user did; the
controller talks to the service.
"""

from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.ui.components.sheet_dialog import SheetPresenter

CODE_LENGTH = 6
RESEND_COOLDOWN_SECONDS = 45


class VerifyEmailDialog(QDialog):
    """Collects the six-digit code sent to the user's inbox."""

    code_submitted = Signal(str)
    resend_requested = Signal()

    def __init__(self, email: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._email = email
        self._cooldown = 0

        self.setWindowTitle("Verify your email")
        self.setModal(True)
        self.setFixedWidth(420)
        self.setObjectName("panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("authCard")
        layout.addWidget(card)

        inner = QVBoxLayout(card)
        inner.setContentsMargins(28, 26, 28, 24)
        inner.setSpacing(13)

        inner.addLayout(self._build_icon_row())
        inner.addWidget(self._build_title())
        inner.addWidget(self._build_subtitle())
        inner.addSpacing(4)
        inner.addWidget(self._build_code_field())
        inner.addWidget(self._build_status())
        inner.addSpacing(4)
        inner.addWidget(self._build_verify_button())
        inner.addLayout(self._build_footer())

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        # Drops down over the sign-in screen like Akeso's other pop-ups.
        self._sheet = SheetPresenter(self, compact=True, chrome=False)

    def setVisible(self, visible: bool) -> None:  # noqa: N802
        if visible and not self.isVisible():
            self._sheet.prepare()
        super().setVisible(visible)
        if visible:
            self._sheet.shown()

    # -------------------------------------------------------------- pieces

    def _build_icon_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        glyph = QLabel()
        glyph.setObjectName("logoBox")
        glyph.setFixedSize(44, 44)
        glyph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        glyph.setPixmap(icons.to_pixmap(icons.mail(22, "#FFFFFF", 2.0)))

        row.addStretch(1)
        row.addWidget(glyph)
        row.addStretch(1)
        return row

    def _build_title(self) -> QLabel:
        label = QLabel("Check your email")
        label.setObjectName("cardTitle")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _build_subtitle(self) -> QLabel:
        label = QLabel(
            f"We sent a {CODE_LENGTH}-digit code to <b>{self._email}</b>. "
            "Enter it below to activate your account."
        )
        label.setObjectName("cardSubtitle")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setTextFormat(Qt.TextFormat.RichText)
        return label

    def _build_code_field(self) -> QWidget:
        holder = QFrame()
        holder.setObjectName("iconField")
        holder.setFixedHeight(52)

        layout = QHBoxLayout(holder)
        layout.setContentsMargins(14, 0, 14, 0)

        self._code_input = QLineEdit()
        self._code_input.setObjectName("otpInput")
        self._code_input.setPlaceholderText("000000")
        self._code_input.setMaxLength(CODE_LENGTH)
        self._code_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Digits only, so a pasted code with stray characters is rejected at
        # the keyboard rather than burning a rate-limited API attempt.
        self._code_input.setValidator(QIntValidator(0, 999999, self))
        self._code_input.textChanged.connect(self._on_code_changed)
        self._code_input.returnPressed.connect(self._submit)

        layout.addWidget(self._code_input)
        return holder

    def _build_status(self) -> QLabel:
        self._status = QLabel("")
        self._status.setObjectName("statusLabel")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status.setWordWrap(True)
        return self._status

    def _build_verify_button(self) -> QPushButton:
        self._verify_btn = QPushButton("Verify & Continue")
        self._verify_btn.setObjectName("primaryButton")
        self._verify_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._verify_btn.setEnabled(False)
        self._verify_btn.clicked.connect(lambda _checked: self._submit())
        return self._verify_btn

    def _build_footer(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setContentsMargins(0, 4, 0, 0)

        self._resend_btn = QPushButton("Resend code")
        self._resend_btn.setObjectName("inspectLink")
        self._resend_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._resend_btn.clicked.connect(lambda _checked: self._on_resend())

        cancel = QPushButton("Cancel")
        cancel.setObjectName("inspectLink")
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.reject)

        row.addWidget(cancel)
        row.addStretch(1)
        row.addWidget(self._resend_btn)
        return row

    # ----------------------------------------------------------- behaviour

    def _on_code_changed(self, text: str) -> None:
        self._verify_btn.setEnabled(len(text) == CODE_LENGTH)
        self.clear_error()

        # Submit automatically on the sixth digit. Codes are transcribed from
        # an email, so the moment it is complete is the moment the user wants
        # it checked.
        if len(text) == CODE_LENGTH:
            self._submit()

    def _submit(self) -> None:
        code = self._code_input.text()
        if len(code) == CODE_LENGTH:
            self.code_submitted.emit(code)

    def _on_resend(self) -> None:
        self.resend_requested.emit()
        self.start_cooldown()

    def start_cooldown(self) -> None:
        """Disable resend for a while.

        Supabase rate-limits server-side, but that returns an error. A local
        cooldown means the user sees a countdown instead of a failure.
        """
        self._cooldown = RESEND_COOLDOWN_SECONDS
        self._resend_btn.setEnabled(False)
        self._tick()
        self._timer.start(1000)

    def _tick(self) -> None:
        if self._cooldown <= 0:
            self._timer.stop()
            self._resend_btn.setEnabled(True)
            self._resend_btn.setText("Resend code")
            return
        self._resend_btn.setText(f"Resend in {self._cooldown}s")
        self._cooldown -= 1

    # ---------------------------------------------------------- public api

    def show_error(self, message: str) -> None:
        self._status.setObjectName("statusLabel")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        self._status.setText(message)
        self._code_input.selectAll()
        self._code_input.setFocus()

    def show_info(self, message: str) -> None:
        self._status.setObjectName("infoLabel")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        self._status.setText(message)

    def clear_error(self) -> None:
        self._status.setText("")

    def set_busy(self, busy: bool) -> None:
        self._verify_btn.setEnabled(not busy and len(self._code_input.text()) == CODE_LENGTH)
        self._code_input.setEnabled(not busy)
        self._verify_btn.setText("Verifying\u2026" if busy else "Verify & Continue")