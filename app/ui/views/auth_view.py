import re
import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core.theme import Theme

# U+FE0E (VARIATION SELECTOR-15) tells Windows to draw the flat, monochrome
# "text" form of a glyph instead of the full-color emoji form. Without it,
# lock/mail/person render as colored emoji that clash with the dark theme.
VS_TEXT = "\uFE0E"
PULSE = "\u223F"


def _panel() -> QWidget:
    """A plain container widget that shows its parent's colour through it.

    Any bare QWidget picks up the global page background from the QWidget
    stylesheet rule, which paints a dark rectangle over the lighter card.
    Naming it lets the #formPanel rule clear that background.
    """
    widget = QWidget()
    widget.setObjectName("formPanel")
    return widget


class FeatureCard(QFrame):
    """Small bordered card used in the hero panel."""

    def __init__(self, title: str, body: str) -> None:
        super().__init__()
        self.setObjectName("featureCard")
        self.setFixedWidth(198)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(7)

        title_label = QLabel(title)
        title_label.setObjectName("featureTitle")

        body_label = QLabel(body)
        body_label.setObjectName("featureBody")
        body_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(body_label)


class IconField(QFrame):
    """A line edit with a leading icon glyph, styled as one pill control.

    Optionally adds a trailing text button that toggles password visibility.
    Qt has no built-in "icon inside a line edit" widget, so this composes
    a label and a borderless QLineEdit inside one bordered frame.
    """

    def __init__(self, icon: str, placeholder: str, password: bool = False) -> None:
        super().__init__()
        self.setObjectName("iconField")
        self.setFixedHeight(42)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(11, 0, 8, 0)
        layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setObjectName("fieldIcon")
        icon_label.setFixedWidth(16)

        self._edit = QLineEdit()
        self._edit.setObjectName("iconFieldEdit")
        self._edit.setPlaceholderText(placeholder)
        if password:
            self._edit.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(icon_label)
        layout.addWidget(self._edit, 1)

        if password:
            toggle = QPushButton("Show")
            toggle.setObjectName("eyeToggle")
            toggle.setFixedWidth(38)
            toggle.setCheckable(True)
            toggle.setCursor(Qt.CursorShape.PointingHandCursor)
            toggle.toggled.connect(
                lambda shown, t=toggle: self._set_visible(shown, t)
            )
            layout.addWidget(toggle)

    def _set_visible(self, shown: bool, button: QPushButton) -> None:
        self._edit.setEchoMode(
            QLineEdit.EchoMode.Normal if shown else QLineEdit.EchoMode.Password
        )
        button.setText("Hide" if shown else "Show")

    def text(self) -> str:
        return self._edit.text()

    def line_edit(self) -> QLineEdit:
        return self._edit


class RequirementRow(QWidget):
    """One line in the password-requirement checklist. Lights up when met."""

    def __init__(self, text: str) -> None:
        super().__init__()
        self.setObjectName("formPanel")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._check = QLabel("\u2713")
        self._check.setObjectName("reqCheckOff")
        self._label = QLabel(text)
        self._label.setObjectName("reqLabelOff")

        layout.addWidget(self._check)
        layout.addWidget(self._label)
        layout.addStretch(1)

    def set_met(self, met: bool) -> None:
        self._check.setObjectName("reqCheckOn" if met else "reqCheckOff")
        self._label.setObjectName("reqLabelOn" if met else "reqLabelOff")
        for widget in (self._check, self._label):
            widget.style().unpolish(widget)
            widget.style().polish(widget)


def _rich_label(html: str) -> QLabel:
    label = QLabel(html)
    label.setObjectName("cardSubtitle")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setTextFormat(Qt.TextFormat.RichText)
    label.setOpenExternalLinks(False)
    return label


class AuthView(QWidget):
    """The login / sign-up screen.

    Only knows how to display things and how to announce that a button
    was pressed. It never imports AuthService or talks to Supabase — the
    controller listens to these signals and does that work instead.
    """

    login_requested = Signal(str, str)
    signup_requested = Signal(str, str, str, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # The sign-up card is tall. A scroll area keeps the Create Account
        # button and everything below it reachable on shorter screens rather
        # than silently clipping off the bottom edge.
        body = _panel()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(40, 24, 40, 40)
        body_layout.setSpacing(0)

        # Theme toggle used to live in the header. With the header gone it
        # floats top-right so light/dark mode is still reachable.
        toggle_row = QHBoxLayout()
        toggle_row.addStretch(1)
        self._theme_toggle = QPushButton(
            "\u2600" if Theme.mode() == "light" else "\U0001F319"
        )
        self._theme_toggle.setObjectName("themeToggle")
        self._theme_toggle.setFixedSize(32, 32)
        self._theme_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme_toggle.clicked.connect(self._on_theme_toggle)
        toggle_row.addWidget(self._theme_toggle)
        body_layout.addLayout(toggle_row)
        body_layout.addSpacing(16)

        columns = QHBoxLayout()
        columns.setSpacing(0)
        columns.addStretch(1)
        columns.addWidget(self._build_hero(), 0, Qt.AlignmentFlag.AlignTop)
        columns.addSpacing(80)
        columns.addWidget(self._build_card(), 0, Qt.AlignmentFlag.AlignTop)
        columns.addStretch(1)
        body_layout.addLayout(columns)
        body_layout.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidget(body)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        root.addWidget(scroll, 1)

    def _on_theme_toggle(self) -> None:
        Theme.toggle_mode()
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(Theme.stylesheet())
        self._theme_toggle.setText(
            "\u2600" if Theme.mode() == "light" else "\U0001F319"
        )

    # ------------------------------------------------------------------- hero

    def _build_hero(self) -> QWidget:
        hero = _panel()
        hero.setFixedWidth(420)

        layout = QVBoxLayout(hero)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(16)

        badge = QLabel("Diagnostic Engine v2.5 Architecture")
        badge.setObjectName("heroBadge")
        badge.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

        title = QLabel("Clinical intelligence at your fingertips.")
        title.setObjectName("heroTitle")
        title.setWordWrap(True)

        body = QLabel(
            "Akeso matches reported symptoms against comprehensive clinical "
            "disease monographs using weighted probabilistic logic. Log in to "
            "track physiological vitals, record health journals, and explore "
            "evidence-based monographs."
        )
        body.setObjectName("heroBody")
        body.setWordWrap(True)

        cards = QHBoxLayout()
        cards.setSpacing(12)
        cards.addWidget(
            FeatureCard(
                "Weighted Correlation",
                "Rule-based symptom weighting with primary and secondary "
                "correlation scores.",
            )
        )
        cards.addWidget(
            FeatureCard(
                "Private & Local",
                "Client-side encrypted local storage ensures your personal "
                "health records remain private.",
            )
        )
        cards.addStretch(1)

        line = QFrame()
        line.setObjectName("separator")
        line.setFixedHeight(1)

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(body)
        layout.addSpacing(6)
        layout.addLayout(cards)
        layout.addSpacing(6)
        layout.addWidget(line)
        layout.addLayout(self._build_stats())
        layout.addStretch(1)
        return hero

    def _build_stats(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(24)
        for number, label in [
            ("15+", "Body Systems"),
            ("200+", "Disease Monographs"),
            ("100%", "Rule-Based"),
        ]:
            group = QHBoxLayout()
            group.setSpacing(6)
            num = QLabel(number)
            num.setObjectName("statNumber")
            text = QLabel(label)
            text.setObjectName("statLabel")
            group.addWidget(num)
            group.addWidget(text)
            row.addLayout(group)
        row.addStretch(1)
        return row

    # -------------------------------------------------------------- auth card

    def _build_card(self) -> QWidget:
        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(400)
        card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)

        logo = QLabel(PULSE)
        logo.setObjectName("logoBox")
        logo.setFixedSize(40, 40)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_row = QHBoxLayout()
        logo_row.addStretch(1)
        logo_row.addWidget(logo)
        logo_row.addStretch(1)

        self._title_label = QLabel("Sign In to Akeso")
        self._title_label.setObjectName("cardTitle")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._subtitle_label = QLabel(
            "Enter your credentials to access your diagnostic engine"
        )
        self._subtitle_label.setObjectName("cardSubtitle")
        self._subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._subtitle_label.setWordWrap(True)

        layout.addLayout(logo_row)
        layout.addWidget(self._title_label)
        layout.addWidget(self._subtitle_label)
        layout.addSpacing(4)
        layout.addWidget(self._build_tab_bar())

        # Plain show()/hide() instead of QStackedWidget: a stacked widget
        # always reserves room for its tallest page, so the login card would
        # keep the sign-up form's height. Hidden siblings contribute nothing
        # to layout, so the card genuinely resizes between tabs.
        self._login_form = self._build_login_form()
        self._signup_form = self._build_signup_form()
        self._signup_form.hide()

        forms = _panel()
        forms_layout = QVBoxLayout(forms)
        forms_layout.setContentsMargins(0, 0, 0, 0)
        forms_layout.addWidget(self._login_form)
        forms_layout.addWidget(self._signup_form)
        layout.addWidget(forms)

        self._status = QLabel("")
        self._status.setObjectName("statusLabel")
        self._status.setWordWrap(True)
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)
        return card

    def _build_tab_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("tabBar")
        bar.setFixedHeight(38)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        self._login_tab = QPushButton("Log In")
        self._signup_tab = QPushButton("Sign Up")
        for index, button in enumerate((self._login_tab, self._signup_tab)):
            button.setObjectName("tabButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, i=index: self._switch_tab(i))
            layout.addWidget(button)

        self._login_tab.setChecked(True)
        return bar

    def _build_login_form(self) -> QWidget:
        form = _panel()
        layout = QVBoxLayout(form)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(6)

        email_label = QLabel("Email or Username")
        email_label.setObjectName("fieldLabel")
        self._login_email = IconField("\u2709" + VS_TEXT, "user@akeso.org")

        password_row = QHBoxLayout()
        password_label = QLabel("Password")
        password_label.setObjectName("fieldLabel")
        forgot = QLabel("Forgot Password?")
        forgot.setObjectName("linkLabel")
        password_row.addWidget(password_label)
        password_row.addStretch(1)
        password_row.addWidget(forgot)

        self._login_password = IconField(
            "\U0001F512" + VS_TEXT, "\u2022" * 8, password=True
        )

        self._remember = QCheckBox("Remember me")
        self._remember.setChecked(True)

        self._login_button = QPushButton("Log In to Akeso  \u2192")
        self._login_button.setObjectName("primaryButton")
        self._login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._login_button.clicked.connect(self._emit_login)

        divider = QFrame()
        divider.setObjectName("separator")
        divider.setFixedHeight(1)

        footer = _rich_label(
            "Don't have an account?&nbsp; "
            '<a href="#" style="color:#A29BFE; text-decoration:none; '
            'font-weight:700;">Sign Up</a>'
        )
        footer.linkActivated.connect(lambda _: self._switch_tab(1))

        layout.addWidget(email_label)
        layout.addWidget(self._login_email)
        layout.addSpacing(4)
        layout.addLayout(password_row)
        layout.addWidget(self._login_password)
        layout.addSpacing(4)
        layout.addWidget(self._remember)
        layout.addSpacing(6)
        layout.addWidget(self._login_button)
        layout.addSpacing(12)
        layout.addWidget(divider)
        layout.addSpacing(10)
        layout.addWidget(footer)
        return form

    def _build_signup_form(self) -> QWidget:
        form = _panel()
        layout = QVBoxLayout(form)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(6)

        self._signup_name = IconField("\U0001F464" + VS_TEXT, "Alex Rivera")
        self._signup_email = IconField("\u2709" + VS_TEXT, "user@akeso.org")
        self._signup_password = IconField(
            "\U0001F512" + VS_TEXT, "Min 8 characters", password=True
        )
        self._signup_confirm = IconField(
            "\U0001F512" + VS_TEXT, "Re-enter password", password=True
        )

        for text, field in (
                ("Full Name", self._signup_name),
                ("Email Address", self._signup_email),
                ("Password", self._signup_password),
        ):
            label = QLabel(text)
            label.setObjectName("fieldLabel")
            layout.addWidget(label)
            layout.addWidget(field)

        layout.addLayout(self._build_requirements())

        confirm_row = QHBoxLayout()
        confirm_label = QLabel("Confirm Password")
        confirm_label.setObjectName("fieldLabel")
        self._match_label = QLabel("")
        self._match_label.setObjectName("reqLabelOff")
        confirm_row.addWidget(confirm_label)
        confirm_row.addStretch(1)
        confirm_row.addWidget(self._match_label)
        layout.addLayout(confirm_row)
        layout.addWidget(self._signup_confirm)
        layout.addLayout(self._build_terms_row())

        self._signup_button = QPushButton("Create Account")
        self._signup_button.setObjectName("primaryButton")
        self._signup_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._signup_button.clicked.connect(self._emit_signup)
        layout.addSpacing(6)
        layout.addWidget(self._signup_button)

        divider = QFrame()
        divider.setObjectName("separator")
        divider.setFixedHeight(1)

        footer = _rich_label(
            "Already have an account?&nbsp; "
            '<a href="#" style="color:#A29BFE; text-decoration:none; '
            'font-weight:700;">Log In</a>'
        )
        footer.linkActivated.connect(lambda _: self._switch_tab(0))
        layout.addSpacing(10)
        layout.addWidget(divider)
        layout.addSpacing(8)
        layout.addWidget(footer)

        self._signup_password.line_edit().textChanged.connect(
            self._update_requirements
        )
        self._signup_password.line_edit().textChanged.connect(self._update_match)
        self._signup_confirm.line_edit().textChanged.connect(self._update_match)
        return form

    def _build_requirements(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setContentsMargins(2, 8, 2, 8)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(4)

        self._req_length = RequirementRow("8+ characters")
        self._req_upper = RequirementRow("Uppercase letter")
        self._req_lower = RequirementRow("Lowercase letter")
        self._req_number = RequirementRow("At least 1 number")
        self._req_special = RequirementRow("Special character (!@#$%^&*)")

        grid.addWidget(self._req_length, 0, 0)
        grid.addWidget(self._req_upper, 0, 1)
        grid.addWidget(self._req_lower, 1, 0)
        grid.addWidget(self._req_number, 1, 1)
        grid.addWidget(self._req_special, 2, 0, 1, 2)
        return grid

    def _update_requirements(self, password: str) -> None:
        self._req_length.set_met(len(password) >= 8)
        self._req_upper.set_met(bool(re.search(r"[A-Z]", password)))
        self._req_lower.set_met(bool(re.search(r"[a-z]", password)))
        self._req_number.set_met(bool(re.search(r"\d", password)))
        self._req_special.set_met(any(c in "!@#$%^&*" for c in password))

    def _update_match(self) -> None:
        confirm = self._signup_confirm.text()
        if not confirm:
            self._match_label.setText("")
            return
        matches = confirm == self._signup_password.text()
        self._match_label.setText("Passwords match" if matches else "Does not match")
        self._match_label.setObjectName("reqLabelOn" if matches else "matchBad")
        self._match_label.style().unpolish(self._match_label)
        self._match_label.style().polish(self._match_label)

    def _build_terms_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setContentsMargins(0, 8, 0, 0)
        row.setSpacing(9)

        self._terms_check = QCheckBox()
        text = QLabel(
            "I agree to Akeso's "
            '<a href="#" style="color:#A29BFE; text-decoration:none;">Terms of '
            "Service</a> and acknowledge that this diagnostic tool is for "
            "reference and informational tracking."
        )
        text.setObjectName("cardSubtitle")
        text.setWordWrap(True)
        text.setTextFormat(Qt.TextFormat.RichText)
        text.setOpenExternalLinks(False)

        row.addWidget(self._terms_check, 0, Qt.AlignmentFlag.AlignTop)
        row.addWidget(text, 1)
        return row

    # ----------------------------------------------------------- interactions

    def _switch_tab(self, index: int) -> None:
        self._login_tab.setChecked(index == 0)
        self._signup_tab.setChecked(index == 1)
        self._login_form.setVisible(index == 0)
        self._signup_form.setVisible(index == 1)
        self.clear_error()

        if index == 0:
            self._title_label.setText("Sign In to Akeso")
            self._subtitle_label.setText(
                "Enter your credentials to access your diagnostic engine"
            )
        else:
            self._title_label.setText("Create an Account")
            self._subtitle_label.setText(
                "Set up your diagnostic profile and personal health workspace"
            )

    def _emit_login(self) -> None:
        self.login_requested.emit(
            self._login_email.text(), self._login_password.text()
        )

    def _emit_signup(self) -> None:
        self.signup_requested.emit(
            self._signup_name.text(),
            self._signup_email.text(),
            self._signup_password.text(),
            self._signup_confirm.text(),
        )

    # ------------------------------------------------------------- public API

    def terms_agreed(self) -> bool:
        return self._terms_check.isChecked()

    def remember_me(self) -> bool:
        return self._remember.isChecked()

    def show_error(self, message: str) -> None:
        self._status.setText(message)

    def clear_error(self) -> None:
        self._status.setText("")

    def set_busy(self, busy: bool) -> None:
        self._login_button.setEnabled(not busy)
        self._signup_button.setEnabled(not busy)
        self._login_button.setText(
            "Please wait\u2026" if busy else "Log In to Akeso  \u2192"
        )
        self._signup_button.setText("Please wait\u2026" if busy else "Create Account")


def main() -> int:
    """Standalone preview: run `python -m app.ui.views.auth_view` from the
    project root (with the venv active) to see this screen without booting
    the rest of the app, Supabase included.
    """
    app = QApplication(sys.argv)
    app.setStyleSheet(Theme.stylesheet())

    view = AuthView()
    view.resize(1440, 900)
    view.setWindowTitle("Akeso — Diagnostic Engine (preview)")
    view.login_requested.connect(lambda e, p: print("login:", e, bool(p)))
    view.signup_requested.connect(lambda *a: print("signup:", a[:2]))
    view.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())