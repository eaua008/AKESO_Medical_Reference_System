"""User Management: every account, its role and status.

Shows account facts only (name, email, role, sign-in times). Health and
study data are never loaded here: the database functions behind this page
cannot read them.
"""

from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox, QFrame, QGridLayout, QHBoxLayout, QLineEdit, QScrollArea, QVBoxLayout, QWidget,
)

from app.core.theme import Theme
from app.models.account import friendly_time
from app.models.admin import ROLES, STATUS_LABELS, AdminUser, UserStats
from app.ui.views.account.account_widgets import Banner, button, icon_label, label, refresh_icons
from app.ui.views.admin.admin_widgets import (
    AdminStat, DataTable, IconButton, actions_cell, avatar_cell, page_header, pill_cell,
    text_cell,
)

ROLE_TONES = {"admin": "amber", "educator": "teal", "student": "blue"}
STATUS_TONES = {"active": "good", "suspended": "danger", "deleting": "amber"}

COLUMNS = ["User / Name", "Email", "Role", "Account created", "Last active", "Status", "Actions"]
NAME, EMAIL, ROLE, CREATED, LAST, STATUS, ACTIONS = range(7)


class UserManagementView(QWidget):
    refresh_requested = Signal()
    view_requested = Signal(object)        # AdminUser
    role_requested = Signal(object)
    suspend_requested = Signal(object)     # suspend or reactivate, by its status
    delete_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._users: list[AdminUser] = []
        self._sort = (CREATED, True)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        column = QVBoxLayout(page)
        column.setContentsMargins(30, 22, 30, 30)
        column.setSpacing(16)

        header, right = page_header(
            "ADMIN MODULE", "", "RBAC & Identity Governance", "users", Theme.token("BADGE_TEXT"),
            "User Management",
            "Manage account access, assign roles, monitor sign-in activity, and suspend "
            "or remove accounts.")
        right.addWidget(button("Refresh", "acGhost", "refresh-cw", self.refresh_requested.emit),
                        0, Qt.AlignmentFlag.AlignTop)
        column.addWidget(header)

        column.addWidget(self._privacy_note())
        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        column.addWidget(self.banner)

        stats = QGridLayout()
        stats.setSpacing(12)
        self._stats = {
            "total": AdminStat("Total accounts"),
            "active": AdminStat("Active", "good"),
            "suspended": AdminStat("Suspended", "danger"),
            "admins": AdminStat("Admins", "amber"),
            "educators": AdminStat("Educators", "teal"),
            "students": AdminStat("Students", "blue"),
        }
        for index, tile in enumerate(self._stats.values()):
            stats.addWidget(tile, 0, index)
        column.addLayout(stats)

        column.addWidget(self._filter_bar())

        self.table = DataTable(COLUMNS, stretch=[NAME, EMAIL], fixed={ACTIONS: 150},
                               sortable=(NAME, EMAIL, ROLE, CREATED, LAST, STATUS))
        self.table.header_clicked.connect(self._sort_by)
        self.table.show_sort(*self._sort)
        column.addWidget(self.table)
        self._empty = label("No account matches these filters.", "adEmpty")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.hide()
        column.addWidget(self._empty)
        column.addStretch(1)

        scroll.setWidget(page)
        outer.addWidget(scroll)

    # ------------------------------------------------------------- pieces

    @staticmethod
    def _privacy_note() -> QWidget:
        box = QFrame()
        box.setObjectName("adPrivacy")
        row = QHBoxLayout(box)
        row.setContentsMargins(16, 14, 16, 14)
        row.setSpacing(12)
        amber = "#FBBF24" if Theme.mode() == "dark" else "#B45309"
        row.addWidget(icon_label("lock", 20, amber), 0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(4)
        title = QHBoxLayout()
        title.setSpacing(8)
        title.addWidget(label("Clinical Confidentiality & Privacy Boundary", "adPrivacyTitle",
                              wrap=False))
        title.addWidget(label("ACCOUNT DATA ONLY", "adPrivacyTag", wrap=False))
        title.addStretch(1)
        text.addLayout(title)
        text.addWidget(label(
            "This page shows account details only: names, emails, roles and sign-in times. "
            "Users' private study and health data (saved symptom cases, medication schedules, "
            "notebook entries and wellness results) cannot be read from the admin console.",
            "adPrivacyText"))
        row.addLayout(text, 1)
        return box

    def _filter_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("adFilterBar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(14, 12, 14, 12)
        row.setSpacing(10)
        self.search = QLineEdit()
        self.search.setObjectName("acInput")
        self.search.setPlaceholderText("Search users by name, email, handle or registry ID…")
        self.search.setClearButtonEnabled(True)
        row.addWidget(self.search, 1)
        row.addWidget(icon_label("funnel", 16))
        row.addWidget(label("Role:", "adFilterLabel", wrap=False))
        self.role = QComboBox()
        self.role.setObjectName("acInput")
        self.role.addItem("All roles", "")
        for value, name, _ in ROLES:
            self.role.addItem(name, value)
        row.addWidget(self.role)
        row.addWidget(label("Status:", "adFilterLabel", wrap=False))
        self.status = QComboBox()
        self.status.setObjectName("acInput")
        self.status.addItem("All statuses", "")
        for value, name in STATUS_LABELS.items():
            self.status.addItem(name, value)
        row.addWidget(self.status)
        self._search_timer = QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(150)
        self._search_timer.timeout.connect(self._render)
        self.search.textChanged.connect(lambda _t: self._search_timer.start())
        self.role.currentIndexChanged.connect(lambda _i: self._render())
        self.status.currentIndexChanged.connect(lambda _i: self._render())
        return bar

    # ------------------------------------------------------------ showing

    def show_users(self, users: list[AdminUser]) -> None:
        self._users = users
        stats = UserStats.of(users)
        for key, value in (("total", stats.total), ("active", stats.active),
                           ("suspended", stats.suspended), ("admins", stats.admins),
                           ("educators", stats.educators), ("students", stats.students)):
            self._stats[key].set_number(value)
        self._render()

    def _visible(self) -> list[AdminUser]:
        query, role, status = self.search.text(), self.role.currentData(), self.status.currentData()
        users = [u for u in self._users if u.matches(query)
                 and (not role or u.role == role) and (not status or u.status == status)]
        column, ascending = self._sort
        key = {
            NAME: lambda u: u.display_name.lower(),
            EMAIL: lambda u: u.email.lower(),
            ROLE: lambda u: [r[0] for r in ROLES].index(u.role) if u.role in ROLE_TONES else 9,
            CREATED: lambda u: u.created_at.timestamp() if u.created_at else 0,
            LAST: lambda u: u.last_sign_in_at.timestamp() if u.last_sign_in_at else 0,
            STATUS: lambda u: u.status,
        }[column]
        return sorted(users, key=key, reverse=not ascending)

    def _sort_by(self, column: int) -> None:
        current, ascending = self._sort
        self._sort = (column, not ascending if column == current else True)
        self.table.show_sort(*self._sort)
        self._render()

    def _render(self) -> None:
        users = self._visible()
        self.table.set_rows([self._row(u) for u in users])
        self.table.fit_height()
        self.table.setVisible(bool(users))
        self._empty.setVisible(not users)

    def _row(self, user: AdminUser) -> list[QWidget]:
        danger = Theme.token("DANGER")
        good = Theme.token("SUCCESS")
        amber = "#FBBF24" if Theme.mode() == "dark" else "#B45309"
        name = user.display_name + ("  (you)" if user.is_me else "")
        suspend = (IconButton("user-check", "Reactivate account", good,
                              lambda u=user: self.suspend_requested.emit(u))
                   if user.suspended else
                   IconButton("user-x", "Suspend account", amber,
                              lambda u=user: self.suspend_requested.emit(u)))
        delete = IconButton("trash-2", "Delete account", danger,
                            lambda u=user: self.delete_requested.emit(u))
        if user.is_me:
            # Your own account: no suspending or deleting from here.
            for widget in (suspend, delete):
                widget.setEnabled(False)
                widget.setToolTip("Not available for your own account")
        last = friendly_time(user.last_sign_in_at) if user.last_sign_in_at else "Never"
        return [
            avatar_cell(user.initial, name, f"ID: {user.registry_id}"),
            text_cell(user.email, "adMono"),
            pill_cell(("◆  " if user.role == "admin" else "") + user.role_label,
                      ROLE_TONES.get(user.role, "")),
            text_cell(friendly_time(user.created_at, with_time=False)),
            text_cell("◷  " + last),
            pill_cell("●  " + STATUS_LABELS[user.status], STATUS_TONES[user.status]),
            actions_cell([
                IconButton("eye", "View account details",
                           on_click=lambda u=user: self.view_requested.emit(u)),
                IconButton("pencil", "Modify role",
                           on_click=lambda u=user: self.role_requested.emit(u)),
                suspend, delete]),
        ]

    def show_error(self, message: str) -> None:
        self.banner.show_message(message, "danger", "Dismiss")

    def show_notice(self, message: str) -> None:
        self.banner.show_message(message, "good", "Dismiss")

    def refresh_theme(self) -> None:
        refresh_icons(self)
        self._render()


