"""Akeso top header bar.

Rebuilt from the reference implementation with three changes:

  1. The brand lockup uses the real logo artwork instead of a "✚" glyph.
  2. All styling comes from Theme, not inline setStyleSheet calls, so the
     header follows light/dark mode like everything else.
  3. Icons are vector-drawn rather than emoji — see app/core/icons.py for
     why that matters on Windows.

Like the auth view, this widget only displays things and emits signals. It
does not know what a search does or where navigation goes.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.assets import logo_pixmap
from app.core.theme import Theme

LOGO_HEIGHT = 30


class IconButton(QPushButton):
    """A square button whose face is a vector icon, redrawn on theme change."""

    def __init__(
            self,
            icon_name: str,
            tooltip: str = "",
            size: int = 34,
            icon_size: int = 18,
            object_name: str = "iconButton",
    ) -> None:
        super().__init__()
        self._icon_name = icon_name
        self._icon_size = icon_size

        self.setObjectName(object_name)
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if tooltip:
            self.setToolTip(tooltip)

        self.refresh_icon()

    def refresh_icon(self, color: str | None = None) -> None:
        from PySide6.QtCore import QSize
        from PySide6.QtGui import QIcon

        tint = color or Theme.token("TEXT_MUTED")
        image = icons.draw(self._icon_name, size=self._icon_size, color=tint)
        self.setIcon(QIcon(icons.to_pixmap(image)))
        self.setIconSize(QSize(self._icon_size, self._icon_size))


class AkesoHeader(QFrame):
    """Top bar: brand, omnisearch, quick actions, theme toggle, profile."""

    themeToggled = Signal(bool)          # True when dark mode is active
    emergencyClicked = Signal()
    searchSubmitted = Signal(str)
    searchOpened = Signal()
    navigationRequested = Signal(str)

    def __init__(self, user_name: str = "User", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("headerFrame")
        self.setFixedHeight(64)
        self._user_name = user_name

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 0, 18, 0)
        layout.setSpacing(12)

        layout.addWidget(self._build_brand())
        layout.addSpacing(8)
        layout.addWidget(self._build_search(), 1)
        layout.addSpacing(8)
        layout.addWidget(self._build_actions())

    # ------------------------------------------------------------- sections

    def _build_brand(self) -> QWidget:
        wrapper = QWidget()
        wrapper.setObjectName("panel")

        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)

        self._logo_label = QLabel()
        self._logo_label.setObjectName("brandLogo")
        self._logo_label.setPixmap(logo_pixmap(LOGO_HEIGHT))
        self._logo_label.setFixedHeight(LOGO_HEIGHT + 4)

        layout.addWidget(self._logo_label)
        return wrapper

    def _build_search(self) -> QWidget:
        box = QFrame()
        box.setObjectName("searchField")
        box.setFixedHeight(36)
        box.setMaximumWidth(460)

        layout = QHBoxLayout(box)
        layout.setContentsMargins(12, 0, 8, 0)
        layout.setSpacing(8)

        self._search_icon = QLabel()
        self._search_icon.setObjectName("panel")
        self._search_icon.setFixedWidth(16)
        self._search_icon.setPixmap(
            icons.to_pixmap(icons.search(16, Theme.token("ICON_MUTED")))
        )

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText(
            "Search diseases, symptoms, medicines, articles…"
        )
        self.search_input.returnPressed.connect(
            lambda: self.searchSubmitted.emit(self.search_input.text())
        )

        shortcut = QLabel("Ctrl K")
        shortcut.setObjectName("kbdBadge")

        layout.addWidget(self._search_icon)
        layout.addWidget(self.search_input, 1)
        layout.addWidget(shortcut)
        return box

    def _build_actions(self) -> QWidget:
        wrapper = QWidget()
        wrapper.setObjectName("panel")

        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.emergency_btn = QPushButton("  Emergency Guide")
        self.emergency_btn.setObjectName("emergencyButton")
        self.emergency_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.emergency_btn.clicked.connect(self.emergencyClicked.emit)
        self._apply_button_icon(self.emergency_btn, "alert", Theme.token("DANGER"))

        self.fav_btn = IconButton("star", "Saved bookmarks")
        self.fav_btn.clicked.connect(
            lambda: self.navigationRequested.emit("favorites")
        )

        self.notif_btn = IconButton("bell", "Alerts and reminders")
        self.notif_btn.clicked.connect(
            lambda: self.navigationRequested.emit("notifications")
        )

        self.theme_btn = IconButton(
            "moon" if Theme.mode() == "dark" else "sun", "Switch theme"
        )
        self.theme_btn.clicked.connect(self._toggle_theme)

        layout.addWidget(self.emergency_btn)
        layout.addWidget(self.fav_btn)
        layout.addWidget(self.notif_btn)
        layout.addWidget(self.theme_btn)
        layout.addSpacing(4)
        layout.addWidget(self._build_profile())
        return wrapper

    def _build_profile(self) -> QWidget:
        chip = QFrame()
        chip.setObjectName("profileChip")
        chip.setFixedHeight(38)

        layout = QHBoxLayout(chip)
        layout.setContentsMargins(6, 4, 14, 4)
        layout.setSpacing(9)

        initial = (self._user_name[:1] or "U").upper()
        avatar = QLabel(initial)
        avatar.setObjectName("avatarCircle")
        avatar.setFixedSize(28, 28)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_col = QVBoxLayout()
        text_col.setSpacing(0)
        text_col.setContentsMargins(0, 0, 0, 0)

        name = QLabel(self._user_name)
        name.setObjectName("profileName")
        role = QLabel("MEDICAL STUDENT")
        role.setObjectName("profileRole")

        text_col.addWidget(name)
        text_col.addWidget(role)

        layout.addWidget(avatar)
        layout.addLayout(text_col)
        return chip

    # ------------------------------------------------------------- helpers

    @staticmethod
    def _apply_button_icon(button: QPushButton, name: str, color: str) -> None:
        from PySide6.QtCore import QSize
        from PySide6.QtGui import QIcon

        image = icons.draw(name, size=16, color=color)
        button.setIcon(QIcon(icons.to_pixmap(image)))
        button.setIconSize(QSize(16, 16))

    def set_user_name(self, name: str) -> None:
        self._user_name = name

    def _toggle_theme(self) -> None:
        Theme.toggle_mode()
        self.refresh_theme()
        self.themeToggled.emit(Theme.mode() == "dark")

    def refresh_theme(self) -> None:
        """Re-render every themed image after a palette switch.

        Stylesheets update themselves, but pixmaps were baked with the old
        colours and have to be redrawn by hand.
        """
        self._logo_label.setPixmap(logo_pixmap(LOGO_HEIGHT))
        self._search_icon.setPixmap(
            icons.to_pixmap(icons.search(16, Theme.token("ICON_MUTED")))
        )
        self._apply_button_icon(
            self.emergency_btn, "alert", Theme.token("DANGER")
        )
        for button in (self.fav_btn, self.notif_btn):
            button.refresh_icon()

        self.theme_btn._icon_name = "moon" if Theme.mode() == "dark" else "sun"
        self.theme_btn.refresh_icon()