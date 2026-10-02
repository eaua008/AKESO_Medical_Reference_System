"""Account Settings page: header card, banners, and four tabs.

Display only. The tabs emit what the user did; AccountController does it.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QButtonGroup, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from app.models.account import AccountSnapshot, ROLE_LABELS
from app.ui.components.fluid import contain
from app.ui.views.account.account_widgets import (
    Banner, ProgressRing, button, label, pill, refresh_icons, repolish,
)
from app.ui.views.account.overview_tab import OverviewTab, _clear
from app.ui.views.account.privacy_tab import PrivacyTab
from app.ui.views.account.profile_tab import ProfileTab
from app.ui.views.account.security_tab import SecurityTab

TABS = [("overview", "Overview"), ("profile", "Profile"),
        ("security", "Security"), ("privacy", "Privacy && data")]


class AccountView(QWidget):
    retry_requested = Signal()
    banner_action = Signal(str)          # which banner's button was pressed
    tab_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        self._page = QVBoxLayout(page)
        self._page.setContentsMargins(30, 22, 30, 30)
        self._page.setSpacing(16)

        self._page.addWidget(self._build_title())
        self._page.addWidget(self._build_hero())
        self.deletion_banner = Banner()
        self.deletion_banner.action.connect(lambda: self.banner_action.emit("deletion"))
        self.notice_banner = Banner()
        self.notice_banner.action.connect(lambda: self.banner_action.emit("notice"))
        self._page.addWidget(self.deletion_banner)
        self._page.addWidget(self.notice_banner)
        self._page.addWidget(self._build_tab_row())

        self.overview = OverviewTab()
        self.profile = ProfileTab()
        self.security = SecurityTab()
        self.privacy = PrivacyTab()
        self._tabs = {"overview": self.overview, "profile": self.profile,
                      "security": self.security, "privacy": self.privacy}
        for tab in self._tabs.values():
            self._page.addWidget(tab)
        self.overview.go_to_tab.connect(self.show_tab)
        self._page.addStretch(1)

        self.scroll.setWidget(page)
        outer.addWidget(self.scroll)
        for tab in self._tabs.values():
            tab.watch(self.scroll.viewport())
        self.show_tab("overview")
        self.show_loading()

    # ------------------------------------------------------------- pieces

    def _build_title(self) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        column = QVBoxLayout(holder)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(4)
        column.addWidget(label("Account Settings", "acTitle"))
        column.addWidget(label("Your profile, sign-in security and the data Akeso keeps "
                               "about you.", "acSubtitle"))
        return holder

    def _build_hero(self) -> QFrame:
        hero = QFrame()
        hero.setObjectName("acHero")
        row = QHBoxLayout(hero)
        row.setContentsMargins(20, 18, 20, 18)
        row.setSpacing(18)
        self.avatar = QLabel()
        self.avatar.setObjectName("panel")
        self.avatar.setFixedSize(72, 72)
        row.addWidget(self.avatar, 0, Qt.AlignmentFlag.AlignVCenter)

        text = QVBoxLayout()
        text.setSpacing(4)
        self.name = label("", "acName")
        self.line = label("", "acMuted")
        text.addWidget(self.name)
        text.addWidget(self.line)
        self._badges = QHBoxLayout()
        self._badges.setSpacing(6)
        text.addLayout(self._badges)
        row.addLayout(text, 1)

        ring_box = QVBoxLayout()
        ring_box.setSpacing(4)
        self.ring = ProgressRing(64)
        ring_box.addWidget(self.ring, 0, Qt.AlignmentFlag.AlignHCenter)
        ring_box.addWidget(label("Profile complete", "acSmall", wrap=False), 0,
                           Qt.AlignmentFlag.AlignHCenter)
        row.addLayout(ring_box)
        contain(hero, buttons=False)
        return hero

    def _build_tab_row(self) -> QWidget:
        row_widget = QWidget()
        row_widget.setObjectName("acTabRow")
        row_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        row = QHBoxLayout(row_widget)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)
        self._tab_group = QButtonGroup(self)
        self._tab_group.setExclusive(True)
        self._tab_buttons: dict[str, QPushButton] = {}
        for key, text in TABS:
            tab = QPushButton(text)
            tab.setObjectName("acTab")
            tab.setCheckable(True)
            tab.setCursor(Qt.CursorShape.PointingHandCursor)
            tab.clicked.connect(lambda _c=False, k=key: self.show_tab(k))
            self._tab_group.addButton(tab)
            self._tab_buttons[key] = tab
            row.addWidget(tab)
        row.addStretch(1)
        self._loading = label("", "acSmall", wrap=False)
        row.addWidget(self._loading)
        self._retry = button("Retry", "acLink", on_click=self.retry_requested.emit)
        self._retry.hide()
        row.addWidget(self._retry)
        return row_widget

    # ---------------------------------------------------------------- api

    def show_tab(self, key: str) -> None:
        if key not in self._tabs:
            return
        for name, tab in self._tabs.items():
            tab.setVisible(name == key)
        self._tab_buttons[key].setChecked(True)
        self.current_tab = key
        self.tab_changed.emit(key)

    def show_loading(self, text: str = "Loading your account…") -> None:
        self._loading.setObjectName("acSmall")
        repolish(self._loading)
        self._loading.setText(text)
        self._retry.hide()

    def show_load_error(self, message: str) -> None:
        self._loading.setObjectName("acError")
        repolish(self._loading)
        self._loading.setText(message)
        self._retry.show()

    def loaded(self) -> None:
        self._loading.setText("")
        self._retry.hide()

    def show_header(self, snapshot: AccountSnapshot, avatar: QPixmap, percent: int) -> None:
        profile = snapshot.profile
        self.avatar.setPixmap(avatar)
        self.name.setText(profile.display_name or snapshot.email.split("@")[0])
        parts = [f"@{profile.handle}" if profile.handle else "",
                 profile.program_label, profile.year_label, profile.school or ""]
        self.line.setText(" · ".join(p for p in parts if p) or snapshot.email)
        _clear(self._badges)
        self._badges.addWidget(pill(ROLE_LABELS.get(snapshot.role, snapshot.role.title())))
        if profile.is_verified_student:
            self._badges.addWidget(pill(f"Verified student · {profile.school_email_domain}",
                                        "acPillGood"))
        self._badges.addWidget(pill("2FA on", "acPillGood") if snapshot.mfa.enabled
                               else pill("2FA off", "acPillWarn"))
        if profile.deletion_pending:
            self._badges.addWidget(pill("Deletion scheduled", "acPillDanger"))
        self._badges.addStretch(1)
        self.ring.set_value(percent)

    def set_avatar(self, avatar: QPixmap) -> None:
        self.avatar.setPixmap(avatar)

    def refresh_theme(self) -> None:
        refresh_icons(self)
        for widget in self.findChildren(QWidget):
            if isinstance(widget, ProgressRing):
                widget.update()

