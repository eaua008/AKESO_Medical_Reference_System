"""Akeso left navigation rail.

Collapsed to icon width, expands on hover, pinnable open.

When collapsed, two things change so the rail stays readable:

  * icons are centred — the expanded style left-aligns them with padding,
    which in a 70px column put every icon noticeably off-centre
  * section headers are replaced by thin partition lines, so the groups
    stay visually separate without their labels

Nav items can declare a required role. Items listing "roles" are only built
for users holding one of them. That is a UI convenience only — real
enforcement belongs in row-level security, since anyone who can run the app
can edit its Python.
"""

from typing import Dict, List, Optional

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.admin_styles import admin_amber
from app.core.theme import Theme

COLLAPSED_WIDTH = 70
EXPANDED_WIDTH = 250
ANIMATION_MS = 180

ROW_HEIGHT = 34
ROW_SPACING = 2
HEADER_HEIGHT = 30

# Pure data. Adding a screen means adding one dict — no layout code.
#   roles    optional; absent means visible to everyone
#   accent   "danger", "primary" or "admin" (amber) tints the row
#   featured solid primary pill with a chevron
NAV_SECTIONS = [
    {
        "header": "NAVIGATION",
        "items": [
            {
                "id": "symptom-checker",
                "label": "Symptom Checker",
                "icon": "pulse",
                "featured": True,
            },
            {"id": "drug-checker", "label": "Drug Interaction Checker", "icon": "shield"},
        ],
    },
    {
        "header": "CLINICAL MODULES",
        "items": [
            {"id": "dashboard", "label": "Dashboard Overview", "icon": "grid"},
            {"id": "diseases", "label": "Disease Encyclopedia", "icon": "book"},
            {"id": "symptoms", "label": "Symptom Encyclopedia", "icon": "pulse"},
            {"id": "medicines", "label": "Medicine Reference", "icon": "pill"},
            {"id": "body-systems", "label": "Body System Explorer", "icon": "heart"},
            {"id": "wellness", "label": "Wellness Calculators", "icon": "calculator"},
            {
                "id": "emergency",
                "label": "Emergency Guide",
                "icon": "alert",
                "accent": "danger",
            },
            {"id": "articles", "label": "Health Articles", "icon": "stack"},
            {"id": "exchange", "label": "Clinical Exchange", "icon": "chat"},
        ],
    },
    {
        "header": "USER WORKSPACE",
        "items": [
            {"id": "notebook", "label": "Study Notebook", "icon": "notebook"},
            {"id": "account", "label": "Account Settings", "icon": "user"},
            {"id": "favorites", "label": "Bookmarks", "icon": "star"},
            {"id": "history", "label": "Search History", "icon": "clock"},
            {"id": "notifications", "label": "Notifications", "icon": "bell"},
            {"id": "settings", "label": "Settings", "icon": "gear"},
        ],
    },
    {
        # Admin Control Panel (migration 004). Hidden from everyone else; the
        # database refuses non-admins anyway.
        "header": "ADMIN",
        "items": [
            {"id": "admin-users", "label": "User Management", "icon": "users",
             "roles": ["admin"], "accent": "admin"},
            {"id": "admin-content", "label": "Content Management", "icon": "database",
             "roles": ["admin"], "accent": "admin"},
            {"id": "admin-announcements", "label": "Announcements", "icon": "megaphone",
             "roles": ["admin"], "accent": "admin"},
        ],
    },
]


def visible_items(role: str = "user") -> List[Dict]:
    """Flatten NAV_SECTIONS to the items this role may see.

    Also used by search, so a user can never search their way to a module
    their role hides from the sidebar.
    """
    allowed = []
    for section in NAV_SECTIONS:
        for item in section["items"]:
            roles = item.get("roles")
            if roles is None or role in roles:
                allowed.append(item)
    return allowed


def _repolish(widget: QWidget) -> None:
    """Re-apply the stylesheet after a dynamic property changes.

    Qt resolves property selectors like [collapsed="true"] once, when the
    style is applied. Changing the property later does nothing visible
    until the widget is unpolished and polished again.
    """
    widget.style().unpolish(widget)
    widget.style().polish(widget)


class NavButton(QPushButton):
    """One nav row: vector icon plus label, with active and accent states."""

    def __init__(self, item: Dict[str, str]) -> None:
        super().__init__()
        self._item = item
        self._active = False

        if item.get("featured"):
            self.setObjectName("navButtonFeatured")
        elif item.get("accent") == "danger":
            self.setObjectName("navButtonDanger")
        elif item.get("accent") == "primary":
            self.setObjectName("navButtonAccent")
        elif item.get("accent") == "admin":
            self.setObjectName("navButtonAdmin")
        else:
            self.setObjectName("navButton")

        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(item["label"])
        self.setFixedHeight(ROW_HEIGHT)
        self.setIconSize(QSize(17, 17))
        self.set_expanded(True)
        self.refresh_icon()

    @staticmethod
    def _escape(text: str) -> str:
        """Qt reads '&' as a mnemonic marker and swallows it; double it."""
        return text.replace("&", "&&")

    def _icon_color(self) -> str:
        if self._item.get("featured"):
            return "#FFFFFF"
        accent = self._item.get("accent")
        if accent == "danger":
            return Theme.token("DANGER")
        if accent == "admin":
            return admin_amber()
        if accent == "primary" or self._active:
            return Theme.token("PRIMARY_TEXT_ON_NAV")
        return Theme.token("TEXT_MUTED")

    def refresh_icon(self) -> None:
        image = icons.draw(self._item["icon"], 17, self._icon_color())
        self.setIcon(QIcon(icons.to_pixmap(image)))

    def set_active(self, active: bool) -> None:
        # Only the two items whose state changed redraw their icon, not all
        # seventeen on every tab switch.
        changed = active != getattr(self, "_active", None)
        self._active = active
        self.setChecked(active)
        if changed:
            self.refresh_icon()

    def set_dot(self, on: bool) -> None:
        """A small green dot on the icon (Settings: an update is ready)."""
        if on != getattr(self, "_dot", False):
            self._dot = on
            self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        if not getattr(self, "_dot", False):
            return
        from PySide6.QtGui import QColor, QPainter, QPen
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor(Theme.token("SURFACE")), 1.5))
        p.setBrush(QColor(Theme.token("SUCCESS")))
        if self.property("collapsed"):
            # Icons only: on the top-right corner of the centred icon.
            x, y = (self.width() - 17) // 2 + 13, (self.height() - 17) // 2 - 2
        else:
            # Full row: at the end of the row, like a notification badge.
            x, y = self.width() - 22, (self.height() - 8) // 2
        p.drawEllipse(x, y, 8, 8)
        p.end()

    def set_expanded(self, expanded: bool) -> None:
        # Blank the text rather than let it clip — half-drawn glyphs read as
        # a rendering bug. The collapsed property switches the stylesheet to
        # a centred, unpadded layout for the icon.
        self.setText(self._escape(f"  {self._item['label']}") if expanded else "")
        self.setProperty("collapsed", not expanded)
        _repolish(self)


class AkesoSidebarNav(QFrame):
    """Collapsible navigation rail. Expands on hover unless pinned open."""

    tabChanged = Signal(str)
    pinChanged = Signal(bool)              # the user pressed the pin

    def __init__(
            self,
            active_tab: str = "dashboard",
            role: str = "user",
            pinned: bool = False,
            parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("sidebarFrame")

        self.active_tab = active_tab
        self.role = role
        self.is_pinned = pinned
        self.is_expanded = pinned
        self.nav_buttons: Dict[str, NavButton] = {}
        self._section_headers: List[QWidget] = []
        self._partitions: List[QWidget] = []
        self._chevrons: List[QLabel] = []
        self.pin_btn: Optional[QPushButton] = None
        self._pin_row_layout: Optional[QHBoxLayout] = None
        self._nav_label: Optional[QLabel] = None

        self.setFixedWidth(EXPANDED_WIDTH if pinned else COLLAPSED_WIDTH)

        self._build_ui()
        self._build_animation()
        self._apply_expansion(self.is_expanded)

    # --------------------------------------------------------------- build

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content.setObjectName("panel")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 8, 12, 14)
        layout.setSpacing(ROW_SPACING)

        first = True
        for section in NAV_SECTIONS:
            items = [
                item for item in section["items"]
                if item.get("roles") is None or self.role in item["roles"]
            ]
            # A fully filtered section would leave a dangling header.
            if not items:
                continue

            if first:
                # The first header also carries the pin, and stays visible
                # when collapsed so the pin remains reachable.
                layout.addWidget(self._build_pin_row(section["header"]))
                first = False
            else:
                partition = self._build_partition()
                layout.addWidget(partition)
                self._partitions.append(partition)

                header = self._build_section_header(
                    section["header"], admin=section["header"] == "ADMIN")
                layout.addWidget(header)
                self._section_headers.append(header)

            for item in items:
                layout.addWidget(self._build_row(item))

        layout.addStretch(1)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        if self.active_tab in self.nav_buttons:
            self.nav_buttons[self.active_tab].set_active(True)

    def _build_pin_row(self, text: str) -> QWidget:
        row = QWidget()
        row.setObjectName("panel")
        row.setFixedHeight(HEADER_HEIGHT + 6)

        self._pin_row_layout = QHBoxLayout(row)
        self._pin_row_layout.setContentsMargins(4, 0, 2, 0)
        self._pin_row_layout.setSpacing(0)

        self._nav_label = QLabel(text)
        self._nav_label.setObjectName("navSectionHeader")
        self._nav_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # Stretch 1: when visible it takes the free space and pushes the pin
        # right. When hidden, the pin has the row to itself and centres.
        self._pin_row_layout.addWidget(self._nav_label, 1)

        self.pin_btn = QPushButton()
        self.pin_btn.setObjectName("pinButton")
        self.pin_btn.setCheckable(True)
        self.pin_btn.setChecked(self.is_pinned)
        self.pin_btn.setFixedSize(26, 26)
        self.pin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pin_btn.setIconSize(QSize(14, 14))
        self.pin_btn.clicked.connect(lambda _c: self._toggle_pin())
        self._refresh_pin_icon()
        self._pin_row_layout.addWidget(self.pin_btn)
        return row

    def _build_section_header(self, text: str, admin: bool = False) -> QWidget:
        row = QWidget()
        row.setObjectName("panel")
        row.setFixedHeight(HEADER_HEIGHT)
        layout = QHBoxLayout(row)
        # No vertical margins, and #navSectionHeader has no padding either:
        # padding stacked on a fixed row height is what clipped these before.
        layout.setContentsMargins(4, 0, 2, 0)
        label = QLabel(text)
        label.setObjectName("navSectionHeader")
        if admin:
            label.setProperty("tone", "admin")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(label)
        return row

    @staticmethod
    def _build_partition() -> QWidget:
        """A short divider shown only when collapsed, in place of headers."""
        holder = QWidget()
        holder.setObjectName("panel")
        holder.setFixedHeight(17)
        layout = QVBoxLayout(holder)
        layout.setContentsMargins(10, 8, 10, 8)
        line = QFrame()
        line.setObjectName("navPartition")
        line.setFixedHeight(1)
        layout.addWidget(line)
        return holder

    def _build_row(self, item: Dict) -> QWidget:
        button = NavButton(item)
        button.clicked.connect(lambda _c=False, tid=item["id"]: self.select_tab(tid))
        self.nav_buttons[item["id"]] = button

        if not item.get("featured"):
            return button

        # The featured pill carries a trailing chevron, overlaid on the
        # button so the button's own icon and text stay put.
        wrapper = QWidget()
        wrapper.setObjectName("panel")
        wrapper.setFixedHeight(ROW_HEIGHT)
        stack = QHBoxLayout(wrapper)
        stack.setContentsMargins(0, 0, 0, 0)
        stack.addWidget(button)

        chevron = QLabel(wrapper)
        chevron.setObjectName("navChevron")
        chevron.setPixmap(icons.to_pixmap(icons.chevron_right(12, "#FFFFFF")))
        chevron.setFixedSize(14, 14)
        chevron.move(EXPANDED_WIDTH - 24 - 26, (ROW_HEIGHT - 14) // 2)
        chevron.raise_()
        self._chevrons.append(chevron)
        return wrapper

    def _build_animation(self) -> None:
        self._anim = QParallelAnimationGroup(self)
        for prop in (b"minimumWidth", b"maximumWidth"):
            animation = QPropertyAnimation(self, prop)
            animation.setDuration(ANIMATION_MS)
            animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self._anim.addAnimation(animation)

    # ------------------------------------------------------------ behaviour

    def enterEvent(self, event: QEvent) -> None:  # noqa: N802
        if not self.is_pinned:
            self._animate_to(EXPANDED_WIDTH)
            self._apply_expansion(True)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:  # noqa: N802
        if not self.is_pinned:
            self._animate_to(COLLAPSED_WIDTH)
            self._apply_expansion(False)
        super().leaveEvent(event)

    def _animate_to(self, width: int) -> None:
        self._anim.stop()
        for i in range(self._anim.animationCount()):
            animation = self._anim.animationAt(i)
            animation.setStartValue(self.width())
            animation.setEndValue(width)
        self._anim.start()

    def _apply_expansion(self, expanded: bool) -> None:
        self.is_expanded = expanded

        for header in self._section_headers:
            header.setVisible(expanded)
        for partition in self._partitions:
            partition.setVisible(not expanded)
        for button in self.nav_buttons.values():
            button.set_expanded(expanded)
        for chevron in self._chevrons:
            chevron.setVisible(expanded)

        if self._nav_label is not None and self._pin_row_layout is not None:
            self._nav_label.setVisible(expanded)
            self._pin_row_layout.setAlignment(
                self.pin_btn,
                (Qt.AlignmentFlag.AlignRight if expanded else Qt.AlignmentFlag.AlignHCenter)
                | Qt.AlignmentFlag.AlignVCenter,
                )

    def _toggle_pin(self) -> None:
        self.is_pinned = self.pin_btn.isChecked()
        self._refresh_pin_icon()
        if self.is_pinned:
            self._animate_to(EXPANDED_WIDTH)
            self._apply_expansion(True)
        self.pinChanged.emit(self.is_pinned)

    def set_pinned(self, pinned: bool) -> None:
        """Pin or unpin from elsewhere (Settings), without echoing pinChanged."""
        if self.pin_btn is None or pinned == self.is_pinned:
            return
        self.pin_btn.blockSignals(True)
        self.pin_btn.setChecked(pinned)
        self.pin_btn.blockSignals(False)
        self.is_pinned = pinned
        self._refresh_pin_icon()
        if pinned:
            self._animate_to(EXPANDED_WIDTH)
            self._apply_expansion(True)
        elif not self.underMouse():
            self._animate_to(COLLAPSED_WIDTH)
            self._apply_expansion(False)

    def _refresh_pin_icon(self) -> None:
        if self.pin_btn is None:
            return
        image = (
            icons.pin(14, Theme.token("PRIMARY")) if self.is_pinned
            else icons.pin_off(14, Theme.token("TEXT_MUTED"))
        )
        self.pin_btn.setIcon(QIcon(icons.to_pixmap(image)))
        self.pin_btn.setToolTip("Unpin sidebar" if self.is_pinned else "Keep sidebar open")

    # ----------------------------------------------------------------- api

    def select_tab(self, tab_id: str) -> None:
        if tab_id not in self.nav_buttons:
            return
        self.active_tab = tab_id
        for tid, button in self.nav_buttons.items():
            button.set_active(tid == tab_id)
        self.tabChanged.emit(tab_id)

    def set_dot(self, tab_id: str, on: bool) -> None:
        button = self.nav_buttons.get(tab_id)
        if button is not None:
            button.set_dot(on)

    def refresh_theme(self) -> None:
        """Redraw icons after a palette switch — they are baked pixmaps."""
        for button in self.nav_buttons.values():
            button.refresh_icon()
        self._refresh_pin_icon()