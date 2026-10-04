"""The login / sign-up screen.

Display only. It shows things and announces that a button was pressed. It
never imports AuthService or talks to Supabase — AuthController listens to
these signals and does that work.

Layout matches the redesigned mockup: header bar with logo, platform badge
and theme toggle; hero on the left with live database counts; auth card on
the right with password and Google sign-in; footer bar.
"""

import re
import sys

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QIcon, QImage, QPainter, QPen, QPixmap
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

from app.core import icons
from app.core.assets import logo_mark_pixmap, logo_pixmap
from app.core.device_identity import APP_VERSION   # one version for the whole app
from app.core.theme import Theme


def _google_g(size: int = 18) -> QPixmap:
    """The four-colour Google "G", drawn rather than loaded.

    Drawn with QPainter so there is no image file to ship and it stays crisp
    at any size.
    """
    scale = 2
    image = QImage(size * scale, size * scale, QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    s = size * scale
    stroke = s * 0.19
    inset = stroke / 2 + s * 0.06
    rect = QRectF(inset, inset, s - 2 * inset, s - 2 * inset)

    # Qt angles: 1/16th degree, counter-clockwise from 3 o'clock.
    segments = [
        ("#EA4335", 45, 90),    # red, top
        ("#FBBC05", 135, 90),   # yellow, left
        ("#34A853", 225, 90),   # green, bottom
        ("#4285F4", 315, 45),   # blue, lower right
    ]
    for color, start, span in segments:
        pen = QPen(QColor(color))
        pen.setWidthF(stroke)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(pen)
        painter.drawArc(rect, start * 16, span * 16)

    # The horizontal bar of the G.
    pen = QPen(QColor("#4285F4"))
    pen.setWidthF(stroke)
    pen.setCapStyle(Qt.PenCapStyle.FlatCap)
    painter.setPen(pen)
    mid = s / 2
    painter.drawLine(QPointF(mid, mid), QPointF(s - inset + stroke / 2, mid))
    painter.end()

    pixmap = QPixmap.fromImage(image)
    pixmap.setDevicePixelRatio(scale)
    return pixmap


class FeatureCard(QFrame):
    """Small bordered card used in the hero panel."""

    def __init__(self, icon_name: str, title: str, body: str) -> None:
        super().__init__()
        self.setObjectName("featureCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 13, 14, 13)
        layout.setSpacing(6)

        heading = QHBoxLayout()
        heading.setSpacing(7)

        self._icon = QLabel()
        self._icon.setObjectName("panel")
        self._icon.setFixedSize(14, 14)
        self._icon_name = icon_name
        self.refresh_icon()

        title_label = QLabel(title)
        title_label.setObjectName("featureTitle")

        heading.addWidget(self._icon)
        heading.addWidget(title_label)
        heading.addStretch(1)

        body_label = QLabel(body)
        body_label.setObjectName("featureBody")
        body_label.setWordWrap(True)

        layout.addLayout(heading)
        layout.addWidget(body_label)

    def refresh_icon(self) -> None:
        self._icon.setPixmap(
            icons.to_pixmap(
                icons.draw(self._icon_name, 14, Theme.token("BADGE_TEXT"))
            )
        )


class IconField(QFrame):
    """A line edit with a leading icon, styled as one pill control.

    Optionally adds a trailing eye button that toggles password visibility.
    """

    def __init__(
            self, icon_name: str, placeholder: str, password: bool = False
    ) -> None:
        super().__init__()
        self.setObjectName("iconField")
        self.setFixedHeight(40)
        self._icon_name = icon_name
        self._password = password
        self._shown = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 8, 0)
        layout.setSpacing(9)

        self._icon = QLabel()
        self._icon.setObjectName("panel")
        self._icon.setFixedSize(15, 15)

        self._edit = QLineEdit()
        self._edit.setObjectName("iconFieldEdit")
        self._edit.setPlaceholderText(placeholder)
        if password:
            self._edit.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self._icon)
        layout.addWidget(self._edit, 1)

        self._eye: QPushButton | None = None
        if password:
            self._eye = QPushButton()
            self._eye.setObjectName("eyeToggle")
            self._eye.setFixedSize(26, 26)
            self._eye.setCursor(Qt.CursorShape.PointingHandCursor)
            self._eye.setToolTip("Show password")
            self._eye.setIconSize(QSize(15, 15))
            self._eye.clicked.connect(lambda _checked: self._toggle())
            layout.addWidget(self._eye)

        self.refresh_icon()

    def _toggle(self) -> None:
        self._shown = not self._shown
        self._edit.setEchoMode(
            QLineEdit.EchoMode.Normal if self._shown
            else QLineEdit.EchoMode.Password
        )
        if self._eye is not None:
            self._eye.setToolTip(
                "Hide password" if self._shown else "Show password"
            )

    def refresh_icon(self) -> None:
        muted = Theme.token("ICON_MUTED")
        self._icon.setPixmap(
            icons.to_pixmap(icons.draw(self._icon_name, 15, muted))
        )
        if self._eye is not None:
            self._eye.setIcon(QIcon(icons.to_pixmap(icons.eye(15, muted))))

    def text(self) -> str:
        return self._edit.text()

    def clear(self) -> None:
        self._edit.clear()
        if self._shown:
            self._toggle()

    def line_edit(self) -> QLineEdit:
        return self._edit


class RequirementRow(QWidget):
    """One line in the password checklist. Lights up when met."""

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


def _panel() -> QWidget:
    widget = QWidget()
    widget.setObjectName("formPanel")
    return widget


def _link_label(html: str) -> QLabel:
    label = QLabel(html)
    label.setObjectName("cardSubtitle")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setTextFormat(Qt.TextFormat.RichText)
    label.setOpenExternalLinks(False)
    return label


class AuthView(QWidget):
    """The login / sign-up screen."""

    login_requested = Signal(str, str)
    signup_requested = Signal(str, str, str, str)
    google_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")

        self._feature_cards: list[FeatureCard] = []
        self._icon_fields: list[IconField] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())

        body = _panel()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(40, 40, 40, 40)
        body_layout.setSpacing(0)
        body_layout.addStretch(1)
        body_layout.addWidget(self._build_hero(), 0, Qt.AlignmentFlag.AlignVCenter)
        body_layout.addSpacing(64)
        body_layout.addWidget(self._build_card(), 0, Qt.AlignmentFlag.AlignVCenter)
        body_layout.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidget(body)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        root.addWidget(scroll, 1)

        root.addWidget(self._build_footer())

    # ---------------------------------------------------------------- header

    def _build_header(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("authHeader")
        bar.setFixedHeight(58)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(28, 0, 28, 0)
        layout.setSpacing(12)

        self._header_logo = QLabel()
        self._header_logo.setObjectName("brandLogo")
        self._header_logo.setPixmap(logo_pixmap(26))

        badge = QLabel("Academic Reference Platform")
        badge.setObjectName("headerBadge")
        # Fixed vertical policy plus vertical centring. Without both, a QLabel
        # in a horizontal layout stretches to the full height of the bar,
        # which is what made this badge fill the header.
        badge.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

        self._theme_btn = QPushButton()
        self._theme_btn.setObjectName("themeToggle")
        self._theme_btn.setFixedSize(32, 32)
        self._theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme_btn.setToolTip("Switch light / dark mode")
        self._theme_btn.setIconSize(QSize(16, 16))
        self._theme_btn.clicked.connect(lambda _checked: self._toggle_theme())
        self._refresh_theme_icon()

        layout.addWidget(self._header_logo, 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch(1)
        layout.addWidget(badge, 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self._theme_btn, 0, Qt.AlignmentFlag.AlignVCenter)
        return bar

    # ------------------------------------------------------------------ hero

    def _build_hero(self) -> QWidget:
        hero = _panel()
        hero.setFixedWidth(440)

        layout = QVBoxLayout(hero)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        badge = QLabel("Weighted Symptom Correlation & Clinical Study Platform")
        badge.setObjectName("heroBadge")
        badge.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

        title = QLabel("Clinical knowledge &\ndifferential study reference.")
        title.setObjectName("heroTitle")
        title.setWordWrap(True)

        body = QLabel(
            "Akeso correlates presenting symptoms against curated textbook "
            "disease monographs using deterministic, weighted clinical "
            "reasoning. Explore differential considerations, track your "
            "study journal, and cross-reference curriculum monographs."
        )
        body.setObjectName("heroBody")
        body.setWordWrap(True)

        cards = QHBoxLayout()
        cards.setSpacing(12)
        for icon_name, card_title, card_body in [
            (
                    "pulse",
                    "Weighted Correlation",
                    "Rule-based symptom weighting with primary and secondary "
                    "correlation scores.",
            ),
            (
                    "shield",
                    "Row-Level Security",
                    "Clinical reference data is read-only to clients, enforced "
                    "by Postgres row-level security.",
            ),
        ]:
            card = FeatureCard(icon_name, card_title, card_body)
            self._feature_cards.append(card)
            cards.addWidget(card, 1)

        line = QFrame()
        line.setObjectName("separator")
        line.setFixedHeight(1)

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(body)
        layout.addSpacing(4)
        layout.addLayout(cards)
        layout.addSpacing(4)
        layout.addWidget(line)
        layout.addLayout(self._build_stats())
        return hero

    def _build_stats(self) -> QHBoxLayout:
        """Counts start as dashes and are filled from the database.

        Placeholder dashes rather than numbers, so nothing on screen claims
        a count that has not actually been read.
        """
        row = QHBoxLayout()
        row.setSpacing(20)

        self._stat_values: dict[str, QLabel] = {}
        for key, label_text in [
            ("body_systems", "Body Systems Represented"),
            ("diseases", "Diseases Indexed"),
            ("symptoms", "Clinical Symptoms"),
        ]:
            group = QHBoxLayout()
            group.setSpacing(6)

            value = QLabel("\u2014")
            value.setObjectName("statNumber")
            text = QLabel(label_text)
            text.setObjectName("statLabel")

            group.addWidget(value)
            group.addWidget(text)
            row.addLayout(group)
            self._stat_values[key] = value

        row.addStretch(1)
        return row

    # ------------------------------------------------------------------ card

    def _build_card(self) -> QWidget:
        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(404)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 26, 28, 24)
        layout.setSpacing(12)

        self._card_logo = QLabel()
        self._card_logo.setObjectName("brandLogo")
        self._card_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._card_logo.setPixmap(logo_mark_pixmap(46))

        self._title_label = QLabel("Sign In to Akeso")
        self._title_label.setObjectName("cardTitle")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._subtitle_label = QLabel(
            "Enter your credentials to access your clinical study workspace"
        )
        self._subtitle_label.setObjectName("cardSubtitle")
        self._subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._subtitle_label.setWordWrap(True)

        layout.addWidget(self._card_logo)
        layout.addWidget(self._title_label)
        layout.addWidget(self._subtitle_label)
        layout.addSpacing(4)
        layout.addWidget(self._build_tab_bar())

        # Plain show/hide rather than QStackedWidget: a stacked widget
        # reserves room for its tallest page, which left an empty gap under
        # the shorter login form.
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
        self._status.hide()
        layout.addWidget(self._status)

        # "Signing you in…" / "Setting up your dashboard…" while the steps
        # after a successful sign-in run (see set_signing_in).
        self._progress = QLabel("")
        self._progress.setObjectName("cardSubtitle")
        self._progress.setWordWrap(True)
        self._progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._progress.hide()
        layout.addWidget(self._progress)

        layout.addLayout(self._build_divider("OR"))
        layout.addWidget(self._build_google_button())

        line = QFrame()
        line.setObjectName("separator")
        line.setFixedHeight(1)
        layout.addSpacing(4)
        layout.addWidget(line)

        self._switch_label = _link_label("")
        self._switch_label.linkActivated.connect(
            lambda _href: self._switch_tab(0 if self._signup_form.isVisible() else 1)
        )
        layout.addWidget(self._switch_label)
        self._refresh_switch_label()
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
            button.clicked.connect(
                lambda _checked, i=index: self._switch_tab(i)
            )
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
        self._login_email = IconField("mail", "user@akeso.org or gmail.com")

        password_row = QHBoxLayout()
        password_label = QLabel("Password")
        password_label.setObjectName("fieldLabel")
        forgot = QLabel("Forgot Password?")
        forgot.setObjectName("linkLabel")
        password_row.addWidget(password_label)
        password_row.addStretch(1)
        password_row.addWidget(forgot)

        self._login_password = IconField(
            "lock", "\u2022" * 8, password=True
        )
        # Enter in the password field submits, as users expect.
        self._login_password.line_edit().returnPressed.connect(self._emit_login)

        self._remember = QCheckBox("Remember me")
        self._remember.setChecked(True)

        self._login_button = QPushButton("Log In to Akeso  \u2192")
        self._login_button.setObjectName("primaryButton")
        self._login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._login_button.clicked.connect(lambda _checked: self._emit_login())

        self._icon_fields += [self._login_email, self._login_password]

        layout.addWidget(email_label)
        layout.addWidget(self._login_email)
        layout.addSpacing(4)
        layout.addLayout(password_row)
        layout.addWidget(self._login_password)
        layout.addSpacing(4)
        layout.addWidget(self._remember)
        layout.addSpacing(6)
        layout.addWidget(self._login_button)
        return form

    def _build_signup_form(self) -> QWidget:
        form = _panel()
        layout = QVBoxLayout(form)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(6)

        self._signup_name = IconField("user", "Alex Rivera")
        self._signup_email = IconField("mail", "user@akeso.org or gmail.com")
        self._signup_password = IconField("lock", "Min 8 characters", password=True)
        self._signup_confirm = IconField("lock", "Re-enter password", password=True)

        self._icon_fields += [
            self._signup_name,
            self._signup_email,
            self._signup_password,
            self._signup_confirm,
        ]

        for text, field in (
                ("Full Name", self._signup_name),
                ("Email Address", self._signup_email),
                ("Password", self._signup_password),
        ):
            label = QLabel(text)
            label.setObjectName("fieldLabel")
            layout.addWidget(label)
            layout.addWidget(field)

        layout.addWidget(self._build_requirements())

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
        self._signup_button.clicked.connect(lambda _checked: self._emit_signup())
        layout.addSpacing(6)
        layout.addWidget(self._signup_button)

        self._signup_password.line_edit().textChanged.connect(
            self._update_requirements
        )
        self._signup_password.line_edit().textChanged.connect(
            lambda _text: self._update_match()
        )
        self._signup_confirm.line_edit().textChanged.connect(
            lambda _text: self._update_match()
        )
        return form

    def _build_requirements(self) -> QWidget:
        box = QFrame()
        box.setObjectName("requirementsBox")

        grid = QGridLayout(box)
        grid.setContentsMargins(10, 8, 10, 8)
        grid.setHorizontalSpacing(14)
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
        return box

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
            f'<a href="#" style="color:{Theme.token("BADGE_TEXT")};">'
            "Terms of Service</a> and acknowledge that this study tool is "
            "for reference and educational use only."
        )
        text.setObjectName("cardSubtitle")
        text.setWordWrap(True)
        text.setTextFormat(Qt.TextFormat.RichText)
        text.setOpenExternalLinks(False)
        text.linkActivated.connect(self._show_terms)

        row.addWidget(self._terms_check, 0, Qt.AlignmentFlag.AlignTop)
        row.addWidget(text, 1)
        return row

    def _show_terms(self, _link: str = "") -> None:
        from app.ui.views.account.account_dialogs import LegalDialog
        LegalDialog("terms", parent=self).exec()

    def _build_divider(self, text: str) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setContentsMargins(0, 4, 0, 4)
        row.setSpacing(12)

        for side in (0, 1):
            line = QFrame()
            line.setObjectName("separator")
            line.setFixedHeight(1)
            if side == 0:
                row.addWidget(line, 1)
                label = QLabel(text)
                label.setObjectName("dividerLabel")
                row.addWidget(label)
            else:
                row.addWidget(line, 1)
        return row

    def _build_google_button(self) -> QPushButton:
        self._google_btn = QPushButton("  Continue with Google")
        self._google_btn.setObjectName("googleButton")
        self._google_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._google_btn.setFixedHeight(42)
        self._google_btn.setIcon(QIcon(_google_g(18)))
        self._google_btn.setIconSize(QSize(18, 18))
        self._google_btn.clicked.connect(lambda _checked: self.google_requested.emit())

        # The button has three states: idle ("Continue with Google"),
        # waiting ("Cancel", with a countdown), and cooldown ("Try again in
        # Ns", disabled). Tracked explicitly so that unrelated code — like
        # a password login finishing — cannot re-enable it mid-cooldown.
        self._google_state = "idle"
        self._cooldown_left = 0
        self._cooldown_timer = QTimer(self)
        self._cooldown_timer.setInterval(1000)
        self._cooldown_timer.timeout.connect(self._tick_cooldown)
        return self._google_btn

    def _build_footer(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("authFooter")
        bar.setFixedHeight(44)

        layout = QHBoxLayout(bar)
        label = QLabel(
            f"Akeso Academic Reference Platform v{APP_VERSION}  \u2022  Clinical "
            "Weighted Symptom Correlation & Health Reference"
        )
        label.setObjectName("footerLabel")
        layout.addWidget(label, 0, Qt.AlignmentFlag.AlignCenter)
        return bar

    # ----------------------------------------------------------- interaction

    def _switch_tab(self, index: int) -> None:
        self._login_tab.setChecked(index == 0)
        self._signup_tab.setChecked(index == 1)
        self._login_form.setVisible(index == 0)
        self._signup_form.setVisible(index == 1)
        self.clear_error()

        if index == 0:
            self._title_label.setText("Sign In to Akeso")
            self._subtitle_label.setText(
                "Enter your credentials to access your clinical study workspace"
            )
        else:
            self._title_label.setText("Create an Account")
            self._subtitle_label.setText(
                "Set up your medical student profile and personal study workspace"
            )
        self._refresh_switch_label()

    def _refresh_switch_label(self) -> None:
        link_color = Theme.token("BADGE_TEXT")
        if self._signup_form.isVisible():
            prompt, action = "Already have an account?", "Log In"
        else:
            prompt, action = "Don't have an account?", "Sign Up"
        self._switch_label.setText(
            f"{prompt}&nbsp; <a href='#' style='color:{link_color}; "
            f"text-decoration:none; font-weight:700;'>{action}</a>"
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

    # ---------------------------------------------------------------- theme

    def _toggle_theme(self) -> None:
        Theme.toggle_mode()
        # Only the login screen exists here, so a full restyle is cheap.
        from app.ui.theme_scope import apply_app_stylesheet
        apply_app_stylesheet()
        self.refresh_theme()
        from app.core.preferences import PreferenceStore
        PreferenceStore().update(theme=Theme.mode())   # remembered for next launch

    def _refresh_theme_icon(self) -> None:
        image = (
            icons.sun(16, Theme.token("TEXT_MUTED")) if Theme.mode() == "light"
            else icons.moon(16, Theme.token("BADGE_TEXT"))
        )
        self._theme_btn.setIcon(QIcon(icons.to_pixmap(image)))

    def refresh_theme(self) -> None:
        """Redraw every pixmap after a palette switch.

        Stylesheets reapply themselves; the logos and icons were baked with
        the old colours and must be regenerated.
        """
        self._header_logo.setPixmap(logo_pixmap(26))
        self._card_logo.setPixmap(logo_mark_pixmap(46))
        self._refresh_theme_icon()
        for card in self._feature_cards:
            card.refresh_icon()
        for field in self._icon_fields:
            field.refresh_icon()
        self._refresh_switch_label()

    # ------------------------------------------------------------ public api

    def set_stats(self, body_systems: int, diseases: int, symptoms: int) -> None:
        """Fill the hero counts from the database."""
        self._stat_values["body_systems"].setText(str(body_systems))
        self._stat_values["diseases"].setText(str(diseases))
        self._stat_values["symptoms"].setText(str(symptoms))

    def terms_agreed(self) -> bool:
        return self._terms_check.isChecked()

    def remember_me(self) -> bool:
        return self._remember.isChecked()

    def show_error(self, message: str) -> None:
        self._status.setText(message)
        self._status.show()

    def clear_error(self) -> None:
        self._status.setText("")
        self._status.hide()

    def set_busy(self, busy: bool) -> None:
        for button in (self._login_button, self._signup_button):
            button.setEnabled(not busy)
        # The Google button follows its own state rather than a blanket
        # enable, so finishing a password login cannot cut a cooldown short.
        self._google_btn.setEnabled(not busy and self._google_state != "cooldown")
        self._login_button.setText(
            "Please wait\u2026" if busy else "Log In to Akeso  \u2192"
        )
        self._signup_button.setText("Please wait\u2026" if busy else "Create Account")

    def set_signing_in(self, text: str | None) -> None:
        """Lock the card and show progress while sign-in finishes (the
        code exchange, the account checks, building the dashboard). The
        window keeps responding meanwhile; this stops a second sign-in
        from starting. None unlocks it again."""
        busy = text is not None
        if busy:
            self.clear_error()
            self._progress.setText(text)
            self._google_btn.setText("  " + text)
        elif self._google_state != "cooldown":
            self._set_google_state("idle", "  Continue with Google")
        self._progress.setVisible(busy)
        for widget in (self._login_form, self._signup_form, self._google_btn,
                       self._switch_label):
            widget.setEnabled(not busy)

    # --------------------------------------------------------- Google button

    def _set_google_state(self, state: str, text: str) -> None:
        self._google_state = state
        self._google_btn.setText(text)
        # Waiting stays clickable — that click is the cancel. Only the
        # cooldown disables it.
        self._google_btn.setEnabled(state != "cooldown")
        self._google_btn.setProperty("googleState", state)
        self._google_btn.style().unpolish(self._google_btn)
        self._google_btn.style().polish(self._google_btn)

    def set_google_waiting(self, waiting: bool) -> None:
        """Browser open and waiting — or back to idle."""
        if waiting:
            self._cooldown_timer.stop()
            self._set_google_state(
                "waiting", "  Waiting for Google\u2026  Cancel"
            )
        else:
            self._cooldown_timer.stop()
            self._set_google_state("idle", "  Continue with Google")

    def set_google_countdown(self, remaining: int) -> None:
        """Show seconds left before the backstop timeout gives up."""
        if self._google_state == "waiting":
            self._google_btn.setText(
                f"  Waiting for Google\u2026  Cancel ({remaining}s)"
            )

    def start_google_cooldown(self, seconds: int) -> None:
        """Disable the button briefly after a cancelled or failed attempt."""
        self._cooldown_left = seconds
        self._set_google_state("cooldown", f"  Try again in {seconds}s")
        self._cooldown_timer.start()

    def _tick_cooldown(self) -> None:
        self._cooldown_left -= 1
        if self._cooldown_left <= 0:
            self._cooldown_timer.stop()
            self._set_google_state("idle", "  Continue with Google")
        else:
            self._google_btn.setText(f"  Try again in {self._cooldown_left}s")

    def reset(self) -> None:
        """Clear every field. Called on logout.

        On a shared machine, leaving the previous user's email in the field
        would tell the next person who was here.
        """
        for field in self._icon_fields:
            field.clear()
        self._terms_check.setChecked(False)
        self._update_requirements("")
        self._match_label.setText("")
        self.clear_error()
        # Stop any cooldown, or it could carry over into the next session.
        self._cooldown_timer.stop()
        self._set_google_state("idle", "  Continue with Google")
        self.set_busy(False)
        self._switch_tab(0)


def main() -> int:
    """Preview on its own: python -m app.ui.views.auth_view"""
    app = QApplication(sys.argv)
    app.setStyleSheet(Theme.stylesheet())
    view = AuthView()
    view.set_stats(10, 6, 15)
    view.resize(1440, 900)
    view.setWindowTitle("Akeso \u2014 auth preview")
    view.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
