"""Pieces shared by the Friends, sharing and Study Groups screens.

    SocialPage   the page frame: title, banner, tab row, scrolling body
    PersonRow    photo (or initial), name, @handle, role badge, actions
    StatePanel   an empty / not-set-up / error message in a dashed card
"""

from typing import Callable

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from app.models.social import Person
from app.ui.components.avatar_cache import AvatarCache
from app.ui.components.akeso_loader import LoadingLabel
from app.ui.views.account.account_widgets import (
    Banner, button, icon_label, label, pill, refresh_icons, repolish,
)

AVATAR = 34


def clear_layout(layout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        widget, child = item.widget(), item.layout()
        if widget is not None:
            widget.hide()
            widget.deleteLater()
        elif child is not None:
            clear_layout(child)


def short_when(value) -> str:
    from app.models.exchange import time_ago
    return time_ago(value) if value else ""


class PersonRow(QFrame):
    """One person in a list. Actions go on the right (add_action)."""

    profile_requested = Signal(str)          # handle
    clicked = Signal()                       # only when made with clickable=True

    def __init__(self, person: Person, subtitle: str = "", badge: str = "",
                 title: str = "", clickable: bool = False) -> None:
        super().__init__()
        self.setObjectName("scRow")
        self.person = person
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 9, 10, 9)
        row.setSpacing(10)
        self.avatar = QLabel()
        self.avatar.setObjectName("panel")
        self.avatar.setFixedSize(AVATAR, AVATAR)
        AvatarCache.apply(self.avatar, person.avatar_path, person.name, AVATAR)
        row.addWidget(self.avatar, 0, Qt.AlignmentFlag.AlignTop)

        text = QVBoxLayout()
        text.setSpacing(1)
        if title:                              # e.g. a shared note's title above who shared it
            text.addWidget(label(title, "scRowTitle"))
        self._clickable = clickable
        if clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        top = QHBoxLayout()
        top.setSpacing(6)
        shown = person.name + (" (you)" if person.is_me else "")
        target = person.handle or person.mention          # members may know a private handle
        if target:
            name = QPushButton(shown.replace("&", "&&"))
            name.setObjectName("scNameLink")
            name.setCursor(Qt.CursorShape.PointingHandCursor)
            name.setToolTip(f"Open @{target}'s profile")
            name.clicked.connect(lambda _c=False, h=target: self.profile_requested.emit(h))
        else:
            name = label(shown, "acValue" if title else "scRowTitle", wrap=False)
        top.addWidget(name)
        shown_badge = badge or person.badge
        if shown_badge:
            top.addWidget(pill(shown_badge, "acPillGood" if shown_badge in ("Owner", "Moderator")
                               else "acPill"))
        top.addStretch(1)
        text.addLayout(top)
        bits = []
        if person.handle:
            bits.append(f"@{person.handle}")
        if subtitle:
            bits.append(subtitle)
        if bits:
            text.addWidget(label("  ·  ".join(bits), "scHandle"))
        row.addLayout(text, 1)
        self.actions = QHBoxLayout()
        self.actions.setSpacing(4)
        row.addLayout(self.actions)
        if person.handle and not person.is_me:
            self.setToolTip(f"Click the name or double-click to open @{person.handle}'s profile")

    def add_action(self, text: str, on_click: Callable[[], None], name: str = "acGhost",
                   icon: str = "", tip: str = "") -> QPushButton:
        widget = button(text, name, icon, on_click)
        if tip:
            widget.setToolTip(tip)
        self.actions.addWidget(widget)
        return widget

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (self._clickable and event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:  # noqa: N802
        target = self.person.handle or self.person.mention
        if target and not self.person.is_me:
            self.profile_requested.emit(target)
        super().mouseDoubleClickEvent(event)


class StatePanel(QFrame):
    """A friendly message where a list would be: empty, not set up, error."""

    action_clicked = Signal()

    def __init__(self, title: str, text: str, icon: str = "users", action: str = "") -> None:
        super().__init__()
        self.setObjectName("scEmpty")
        col = QVBoxLayout(self)
        col.setContentsMargins(24, 24, 24, 24)
        col.setSpacing(6)
        col.addWidget(icon_label(icon, 26), 0, Qt.AlignmentFlag.AlignHCenter)
        heading = label(title, "scEmptyTitle")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col.addWidget(heading)
        body = label(text, "acMuted")
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col.addWidget(body)
        if action:
            go = button(action, "acPrimary", on_click=self.action_clicked.emit)
            col.addWidget(go, 0, Qt.AlignmentFlag.AlignHCenter)


class SocialPage(QWidget):
    """Title and subtitle, a banner for messages, optional tabs, and a
    scrolling body (self.body). Subclasses fill the body per tab."""

    refresh_requested = Signal()

    def __init__(self, title: str, subtitle: str, icon: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        self.page = QVBoxLayout(page)
        self.page.setContentsMargins(30, 22, 30, 30)
        self.page.setSpacing(14)

        head = QHBoxLayout()
        head.setSpacing(12)
        head.addWidget(icon_label(icon, 24), 0, Qt.AlignmentFlag.AlignTop)
        titles = QVBoxLayout()
        titles.setSpacing(3)
        titles.addWidget(label(title, "acTitle"))
        self.subtitle = label(subtitle, "acSubtitle")
        titles.addWidget(self.subtitle)
        head.addLayout(titles, 1)
        self.head_actions = QHBoxLayout()
        self.head_actions.setSpacing(6)
        head.addLayout(self.head_actions)
        refresh = button("Refresh", "acLink", "refresh-cw", self.refresh_requested.emit)
        self.head_actions.addWidget(refresh, 0, Qt.AlignmentFlag.AlignTop)
        self.page.addLayout(head)

        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        self.page.addWidget(self.banner)

        self.top = QVBoxLayout()               # fixed controls above the tabs
        self.top.setSpacing(10)
        self.page.addLayout(self.top)

        self._tab_row = QWidget()
        self._tab_row.setObjectName("acTabRow")
        tabs = QHBoxLayout(self._tab_row)
        tabs.setContentsMargins(0, 0, 0, 0)
        tabs.setSpacing(0)
        self._tab_layout = tabs
        self._tab_group = QButtonGroup(self)
        self._tab_group.setExclusive(True)
        self.tabs: dict[str, QPushButton] = {}
        tabs.addStretch(1)
        self._tab_row.hide()
        self.page.addWidget(self._tab_row)

        self.body = QVBoxLayout()
        self.body.setSpacing(8)
        self.page.addLayout(self.body)
        self.page.addStretch(1)
        self.scroll.setWidget(page)
        outer.addWidget(self.scroll)
        self.current_tab = ""

    # ------------------------------------------------------------ tabs

    def add_tab(self, key: str, text: str) -> QPushButton:
        tab = QPushButton(text)
        tab.setObjectName("acTab")
        tab.setCheckable(True)
        tab.setCursor(Qt.CursorShape.PointingHandCursor)
        tab.clicked.connect(lambda _c=False, k=key: self.select_tab(k))
        self._tab_group.addButton(tab)
        self._tab_layout.insertWidget(self._tab_layout.count() - 1, tab)
        self.tabs[key] = tab
        self._tab_row.show()
        if not self.current_tab:
            self.current_tab = key
            tab.setChecked(True)
        return tab

    def set_tab_text(self, key: str, text: str) -> None:
        if key in self.tabs:
            self.tabs[key].setText(text)

    def select_tab(self, key: str) -> None:
        self.current_tab = key
        if key in self.tabs:
            self.tabs[key].setChecked(True)
        self.draw()

    def draw(self) -> None:
        """Subclasses redraw self.body for self.current_tab."""

    # ----------------------------------------------------------- states

    def show_loading(self, text: str = "Loading…") -> None:
        clear_layout(self.body)
        loading = LoadingLabel("", "acMuted")
        loading.set_loading(text)
        self.body.addWidget(loading)

    def show_state(self, title: str, text: str, icon: str = "users") -> StatePanel:
        clear_layout(self.body)
        panel = StatePanel(title, text, icon)
        self.body.addWidget(panel)
        return panel

    def show_not_installed(self, message: str) -> None:
        """Before migrations 040-042 run: say so, without an error."""
        self._tab_row.hide()
        self.show_state("Not set up yet", message, "database")

    def section(self, text: str) -> None:
        self.body.addWidget(label(text.upper(), "scSection", wrap=False))

    def refresh_theme(self) -> None:
        refresh_icons(self)
        for tab in self.tabs.values():
            repolish(tab)
