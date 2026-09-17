"""Akeso left navigation rail.

Collapsed to icon width, expands on hover, pinnable so it stops moving while
you work.

Nav items can declare a required role. Anything listing "roles" is only built
for users holding one of them — the widget is never created, not merely
hidden. This is a UI convenience only: real enforcement belongs in row level
security and the service layer, since anyone who can run the app can edit its
Python.
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
from app.core.theme import Theme

COLLAPSED_WIDTH = 70
EXPANDED_WIDTH = 250
ANIMATION_MS = 180

ROW_HEIGHT = 34
ROW_SPACING = 2
HEADER_HEIGHT = 30

# Pure data. Adding a screen means adding one dict — no layout code.
#   roles    optional; absent means visible to everyone
#   accent   "danger" or "primary" tints the row
#   featured renders as a solid primary pill with a chevron
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
        ],
    },
    {
        "header": "CLINICAL MODULES",
        "items": [
            {"id": "dashboard", "label": "Dashboard Overview", "icon": "grid"},
            {"id": "diseases", "label": "Disease Encyclopedia", "icon": "book"},
            {"id": "symptoms", "label": "Symptom Encyclopedia", "icon": "pulse"},
            {"id": "medicines", "label": "Medicine Reference", "icon": "pill"},
            # Ampersands are escaped by NavButton, not here — keep labels
            # written the way they should read.
            {
                "id": "medications",
                "label": "Medication & Drug Safety",
                "icon": "clock",
            },
            {"id": "body-systems", "label": "Body System Explorer", "icon": "heart"},
            {
                "id": "journal",
                "label": "Personal Health Journal",
                "icon": "notebook",
            },
            {"id": "wellness", "label": "Wellness Calculators", "icon": "leaf"},
            {
                "id": "emergency",
                "label": "Emergency Guide",
                "icon": "alert",
                "accent": "danger",
            },
            {"id": "articles", "label": "Health Articles", "icon": "stack"},
        ],
    },
    {
        "header": "USER WORKSPACE",
        "items": [
            {"id": "account", "label": "Account Settings", "icon": "user"},
            {"id": "favorites", "label": "Bookmarks", "icon": "star"},
            {"id": "history", "label": "Search History", "icon": "clock"},
            {"id": "notifications", "label": "Notifications", "icon": "bell"},
            {"id": "settings", "label": "Settings", "icon": "gear"},
            {
                "id": "admin",
                "label": "Admin Control Panel",
                "icon": "shield",
                "roles": ["admin"],
            },
        ],
    },
]


def visible_items(role: str = "user") -> List[Dict]:
    """Flatten NAV_SECTIONS to the items this role may see."""
    allowed = []
    for section in NAV_SECTIONS:
        for item in section["items"]:
            roles = item.get("roles")
            if roles is None or role in roles:
                allowed.append(item)
    return allowed


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
        """Qt reads '&' in button text as a mnemonic marker and swallows it.

        "Medication & Drug Safety" renders as "Medication  Drug Safety" with
        the D underlined. Doubling the ampersand escapes it.
        """
        return text.replace("&", "&&")

    def _icon_color(self) -> str:
        if self._item.get("featured"):
            return "#FFFFFF"
        accent = self._item.get("accent")
        if accent == "danger":
            return Theme.token("DANGER")
        if accent == "primary":
            return Theme.token("PRIMARY_TEXT_ON_NAV")
        if self._active:
            return Theme.token("PRIMARY_TEXT_ON_NAV")
        return Theme.token("TEXT_MUTED")

    def refresh_icon(self) -> None:
        image = icons.draw(self._item["icon"], size=17, color=self._icon_color())
        self.setIcon(QIcon(icons.to_pixmap(image)))

    def set_active(self, active: bool) -> None:
        self._active = active
        self.setChecked(active)
        self.refresh_icon()

    def set_expanded(self, expanded: bool) -> None:
        # Blank the text rather than let it clip — half-drawn glyphs read as
        # a rendering bug.
        self.setText(self._escape(f"  {self._item['label']}") if expanded else "")


class AkesoSidebarNav(QFrame):
    """Collapsible navigation rail. Expands on hover unless pinned open."""

    tabChanged = Signal(str)

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
        self._section_rows: List[QWidget] = []
        self._chevrons: List[QLabel] = []
        self.pin_btn: Optional[QPushButton] = None

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
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        content = QWidget()
        content.setObjectName("panel")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 8, 12, 14)
        layout.setSpacing(ROW_SPACING)

        for index, section in enumerate(NAV_SECTIONS):
            items = [
                item
                for item in section["items"]
                if item.get("roles") is None or self.role in item["roles"]
            ]
            # A fully filtered section would leave a dangling header with
            # nothing beneath it.
            if not items:
                continue

            row = self._build_section_header(
                section["header"], with_pin=(index == 0)
            )
            layout.addWidget(row)
            self._section_rows.append(row)

            for item in items:
                layout.addWidget(self._build_row(item))

        layout.addStretch(1)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        if self.active_tab in self.nav_buttons:
            self.nav_buttons[self.active_tab].set_active(True)

    def _build_row(self, item: Dict) -> QWidget:
        button = NavButton(item)
        button.clicked.connect(
            lambda _=False, tid=item["id"]: self.select_tab(tid)
        )
        self.nav_buttons[item["id"]] = button

        if not item.get("featured"):
            return button

        # The featured pill carries a trailing chevron, overlaid on the
        # button so the button's own icon and text stay where they are.
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

    def _build_section_header(self, text: str, with_pin: bool) -> QWidget:
        row = QWidget()
        row.setObjectName("panel")
        row.setFixedHeight(HEADER_HEIGHT)

        layout = QHBoxLayout(row)
        # Vertical margins are 0 deliberately, and the stylesheet must not
        # add padding to #navSectionHeader either — padding stacked on top
        # of a fixed row height is what clipped these labels.
        layout.setContentsMargins(4, 0, 2, 0)
        layout.setSpacing(0)

        label = QLabel(text)
        label.setObjectName("navSectionHeader")
        label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(label)
        layout.addStretch(1)

        if with_pin:
            self.pin_btn = QPushButton()
            self.pin_btn.setObjectName("pinButton")
            self.pin_btn.setCheckable(True)
            self.pin_btn.setChecked(self.is_pinned)
            self.pin_btn.setFixedSize(22, 22)
            self.pin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.pin_btn.setIconSize(QSize(14, 14))
            self.pin_btn.clicked.connect(self._toggle_pin)
            self._refresh_pin_icon()
            layout.addWidget(self.pin_btn)

        return row

    def _build_animation(self) -> None:
        self._anim = QParallelAnimationGroup(self)
        for prop in (b"minimumWidth", b"maximumWidth"):
            animation = QPropertyAnimation(self, prop)
            animation.setDuration(ANIMATION_MS)
            animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self._anim.addAnimation(animation)

    # ------------------------------------------------------------ behaviour

    def enterEvent(self, event: QEvent) -> None:
        if not self.is_pinned:
            self._animate_to(EXPANDED_WIDTH)
            self._apply_expansion(True)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
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
        for row in self._section_rows:
            row.setVisible(expanded)
        for button in self.nav_buttons.values():
            button.set_expanded(expanded)
        for chevron in self._chevrons:
            chevron.setVisible(expanded)

    def _toggle_pin(self) -> None:
        self.is_pinned = self.pin_btn.isChecked()
        self._refresh_pin_icon()
        if self.is_pinned:
            self._animate_to(EXPANDED_WIDTH)
            self._apply_expansion(True)

    def _refresh_pin_icon(self) -> None:
        if self.pin_btn is None:
            return
        if self.is_pinned:
            image = icons.pin(14, Theme.token("PRIMARY"))
        else:
            image = icons.pin_off(14, Theme.token("TEXT_MUTED"))
        self.pin_btn.setIcon(QIcon(icons.to_pixmap(image)))
        self.pin_btn.setToolTip(
            "Unpin sidebar" if self.is_pinned else "Keep sidebar open"
        )

    # ----------------------------------------------------------------- api

    def select_tab(self, tab_id: str) -> None:
        if tab_id not in self.nav_buttons:
            return
        self.active_tab = tab_id
        for tid, button in self.nav_buttons.items():
            button.set_active(tid == tab_id)
        self.tabChanged.emit(tab_id)

    def refresh_theme(self) -> None:
        """Redraw icons after a palette switch.

        Stylesheets reapply themselves; these icons are pixmaps baked with
        the old colours.
        """
        for button in self.nav_buttons.values():
            button.refresh_icon()
        self._refresh_pin_icon()