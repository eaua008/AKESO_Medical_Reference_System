"""Akeso top header bar.

Display only. It shows the brand, search, quick actions and the account menu,
and emits signals. It does not know what a search does, where navigation
goes, or how to sign out — DashboardShell decides all of that.

Search is split deliberately: this widget emits what was typed and renders
the results it is given. It never runs a search itself. The ranking lives in
SearchService, where it can be tested without a window.
"""

from typing import Optional

from PySide6.QtCore import QEvent, QObject, QPoint, QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QIcon, QImage, QPainter, QPainterPath, QPen, QPixmap
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
from app.services.search_service import SearchResult
from app.ui.components.search_popup import SearchPopup

LOGO_HEIGHT = 30


# ------------------------------------------------------------- local icons

def _draw(size: int, color: str, width: float, paint) -> QPixmap:
    """Render a small vector icon. Kept local: only this header uses these."""
    scale = 2
    image = QImage(size * scale, size * scale, QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.scale(size * scale / 24.0, size * scale / 24.0)
    pen = QPen(QColor(color))
    pen.setWidthF(width)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    paint(painter)
    painter.end()
    pixmap = QPixmap.fromImage(image)
    pixmap.setDevicePixelRatio(scale)
    return pixmap


def _chevron_down(size: int, color: str) -> QPixmap:
    def paint(p: QPainter) -> None:
        path = QPainterPath()
        path.moveTo(6, 9)
        path.lineTo(12, 15)
        path.lineTo(18, 9)
        p.drawPath(path)
    return _draw(size, color, 2.2, paint)


def _log_out(size: int, color: str) -> QPixmap:
    def paint(p: QPainter) -> None:
        door = QPainterPath()
        door.moveTo(10, 4)
        door.lineTo(5, 4)
        door.lineTo(5, 20)
        door.lineTo(10, 20)
        p.drawPath(door)
        p.drawLine(QPointF(10, 12), QPointF(20, 12))
        arrow = QPainterPath()
        arrow.moveTo(16, 8)
        arrow.lineTo(20, 12)
        arrow.lineTo(16, 16)
        p.drawPath(arrow)
    return _draw(size, color, 2.0, paint)


def _user_cog(size: int, color: str) -> QPixmap:
    def paint(p: QPainter) -> None:
        p.drawEllipse(QPointF(10, 8), 4, 4)
        p.drawArc(QRectF(3, 13, 14, 14), 30 * 16, 120 * 16)
        p.drawEllipse(QPointF(18, 17), 2.4, 2.4)
    return _draw(size, color, 1.9, paint)


# --------------------------------------------------------------- pieces

class IconButton(QPushButton):
    """A square button whose face is a vector icon, redrawn on theme change."""

    def __init__(
            self, icon_name: str, tooltip: str = "", size: int = 34, icon_size: int = 18
    ) -> None:
        super().__init__()
        self._icon_name = icon_name
        self._icon_size = icon_size
        self.setObjectName("iconButton")
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if tooltip:
            self.setToolTip(tooltip)
        self.refresh_icon()

    def set_icon_name(self, name: str) -> None:
        self._icon_name = name
        self.refresh_icon()

    def refresh_icon(self) -> None:
        image = icons.draw(self._icon_name, self._icon_size, Theme.token("TEXT_MUTED"))
        self.setIcon(QIcon(icons.to_pixmap(image)))
        self.setIconSize(QSize(self._icon_size, self._icon_size))


class _ClickableFrame(QFrame):
    """A QFrame that reports clicks — used for the profile chip."""

    clicked = Signal()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ProfileMenu(QFrame):
    """The dropdown under the profile chip.

    A true popup window (Qt.Popup) is right here, unlike the search dropdown:
    a menu should take focus and close itself when you click anywhere else,
    which Qt.Popup does automatically.
    """

    account_requested = Signal()
    history_requested = Signal()
    sign_out_requested = Signal()

    def __init__(self, name: str, email: str, parent: QWidget) -> None:
        super().__init__(parent, Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        # Transparent outer shell so the inner card's rounded corners show,
        # instead of square black corners from the window behind them.
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setObjectName("profileMenuShell")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("profileMenuCard")
        outer.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 12, 8, 8)
        layout.setSpacing(2)

        name_label = QLabel(name)
        name_label.setObjectName("menuName")
        email_label = QLabel(email or "Signed in")
        email_label.setObjectName("menuEmail")

        header = QVBoxLayout()
        header.setContentsMargins(8, 0, 8, 8)
        header.setSpacing(2)
        header.addWidget(name_label)
        header.addWidget(email_label)
        layout.addLayout(header)
        layout.addWidget(self._separator())

        self._account_btn = self._item(
            "Account Settings", _user_cog(16, Theme.token("BADGE_TEXT")), "menuItemAccent"
        )
        self._account_btn.clicked.connect(lambda _c: self._fire(self.account_requested))

        self._history_btn = self._item(
            "Search History", icons.to_pixmap(icons.clock(16, Theme.token("BADGE_TEXT"))), "menuItem"
        )
        self._history_btn.clicked.connect(lambda _c: self._fire(self.history_requested))

        self._sign_out_btn = self._item(
            "Sign Out", _log_out(16, Theme.token("DANGER")), "menuItemDanger"
        )
        self._sign_out_btn.clicked.connect(lambda _c: self._fire(self.sign_out_requested))

        layout.addWidget(self._account_btn)
        layout.addWidget(self._history_btn)
        layout.addWidget(self._separator())
        layout.addWidget(self._sign_out_btn)

        self.setFixedWidth(232)

    @staticmethod
    def _separator() -> QFrame:
        line = QFrame()
        line.setObjectName("menuSeparator")
        line.setFixedHeight(1)
        return line

    @staticmethod
    def _item(text: str, pixmap: QPixmap, object_name: str) -> QPushButton:
        button = QPushButton(f"  {text}")
        button.setObjectName(object_name)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFixedHeight(36)
        button.setIcon(QIcon(pixmap))
        button.setIconSize(QSize(16, 16))
        return button

    def _fire(self, signal) -> None:
        # Close first, then emit. Emitting first would let the receiver swap
        # screens while this popup is still open over the old one.
        self.hide()
        signal.emit()

    def open_under(self, anchor: QWidget) -> None:
        # Right edges aligned, so the menu never runs off the window edge.
        position = anchor.mapToGlobal(
            QPoint(anchor.width() - self.width(), anchor.height() + 6)
        )
        self.move(position)
        self.show()


# ------------------------------------------------------------------ header

class AkesoHeader(QFrame):
    """Top bar: brand, search, quick actions, theme toggle, account menu."""

    themeToggled = Signal(bool)            # True when dark mode is active
    emergencyClicked = Signal()
    navigationRequested = Signal(str)
    searchTextChanged = Signal(str)
    searchResultChosen = Signal(object)    # a SearchResult
    accountRequested = Signal()
    historyRequested = Signal()
    signOutRequested = Signal()

    def __init__(
            self,
            user_name: str = "User",
            user_email: str = "",
            parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("headerFrame")
        self.setFixedHeight(64)
        self._user_name = user_name
        self._user_email = user_email
        self._popup: Optional[SearchPopup] = None
        self._menu: Optional[ProfileMenu] = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 0, 18, 0)
        layout.setSpacing(12)

        layout.addWidget(self._build_brand(), 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addSpacing(8)
        layout.addStretch(1)
        layout.addWidget(self._build_search(), 3)
        layout.addStretch(1)
        layout.addSpacing(8)
        layout.addWidget(self._build_actions(), 0, Qt.AlignmentFlag.AlignVCenter)

    # -------------------------------------------------------------- brand

    def _build_brand(self) -> QWidget:
        self._logo_label = QLabel()
        self._logo_label.setObjectName("brandLogo")
        self._logo_label.setPixmap(logo_pixmap(LOGO_HEIGHT))
        return self._logo_label

    # ------------------------------------------------------------- search

    def _build_search(self) -> QWidget:
        self._search_box = QFrame()
        self._search_box.setObjectName("searchField")
        self._search_box.setFixedHeight(38)
        self._search_box.setMaximumWidth(560)

        layout = QHBoxLayout(self._search_box)
        layout.setContentsMargins(12, 0, 6, 0)
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
            "Search diseases, symptoms, medicines, articles\u2026"
        )
        self.search_input.textChanged.connect(self._on_text_changed)
        # Arrow keys, Enter and Escape are intercepted here so the search
        # field keeps focus while the user steers the dropdown.
        self.search_input.installEventFilter(self)

        shortcut = QLabel("Ctrl K")
        shortcut.setObjectName("kbdBadge")

        layout.addWidget(self._search_icon)
        layout.addWidget(self.search_input, 1)
        layout.addWidget(shortcut)
        return self._search_box

    def _ensure_popup(self) -> SearchPopup:
        if self._popup is None:
            # Parented to the top-level window so it can overlay page content
            # below the header. Created lazily: at construction time this
            # header may not have a window yet.
            self._popup = SearchPopup(self.window())
            self._popup.chosen.connect(self._choose)
        return self._popup

    def _on_text_changed(self, text: str) -> None:
        if not text.strip():
            self.hide_suggestions()
            return
        self.searchTextChanged.emit(text)

    def show_suggestions(self, results: list[SearchResult]) -> None:
        """Render results the shell computed for the current query."""
        query = self.search_input.text().strip()
        if not query:
            return
        popup = self._ensure_popup()
        popup.set_results(results, query)
        popup.show_under(self._search_box)

    def hide_suggestions(self) -> None:
        if self._popup is not None:
            self._popup.hide()

    def _choose(self, result: SearchResult) -> None:
        self.hide_suggestions()
        self.search_input.blockSignals(True)
        self.search_input.clear()
        self.search_input.blockSignals(False)
        self.search_input.clearFocus()
        self.searchResultChosen.emit(result)

    def focus_search(self) -> None:
        """Ctrl+K target: put the cursor in search, ready to type."""
        self.search_input.setFocus(Qt.FocusReason.ShortcutFocusReason)
        self.search_input.selectAll()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if watched is self.search_input:
            if event.type() == QEvent.Type.KeyPress:
                return self._handle_search_key(event.key())
            if event.type() == QEvent.Type.FocusOut:
                self.hide_suggestions()
        return super().eventFilter(watched, event)

    def _handle_search_key(self, key: int) -> bool:
        popup = self._popup
        visible = popup is not None and popup.isVisible()

        if key == Qt.Key.Key_Down and visible:
            popup.move_selection(1)
            return True
        if key == Qt.Key.Key_Up and visible:
            popup.move_selection(-1)
            return True
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if visible:
                chosen = popup.current() or popup.first()
                if chosen:
                    self._choose(chosen)
            return True
        if key == Qt.Key.Key_Escape:
            self.hide_suggestions()
            self.search_input.clearFocus()
            return True
        return False

    # ------------------------------------------------------------ actions

    def _build_actions(self) -> QWidget:
        wrapper = QWidget()
        wrapper.setObjectName("panel")

        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.emergency_btn = QPushButton("  Emergency Guide")
        self.emergency_btn.setObjectName("emergencyButton")
        self.emergency_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # Lambda, not .connect(self.emergencyClicked.emit): clicked carries a
        # bool, and signal.emit forwards it — which crashes a zero-argument
        # signal. The old wiring would have thrown on the first click.
        self.emergency_btn.clicked.connect(lambda _c: self.emergencyClicked.emit())
        self._set_emergency_icon()

        self.fav_btn = IconButton("star", "Saved bookmarks")
        self.fav_btn.clicked.connect(lambda _c: self.navigationRequested.emit("favorites"))

        self.notif_btn = IconButton("bell", "Alerts and reminders")
        self.notif_btn.clicked.connect(lambda _c: self.navigationRequested.emit("notifications"))

        self.theme_btn = IconButton(
            "moon" if Theme.mode() == "dark" else "sun", "Switch theme"
        )
        self.theme_btn.clicked.connect(lambda _c: self._toggle_theme())

        layout.addWidget(self.emergency_btn)
        layout.addWidget(self.fav_btn)
        layout.addWidget(self.notif_btn)
        layout.addWidget(self.theme_btn)
        layout.addSpacing(4)
        layout.addWidget(self._build_profile())
        return wrapper

    def _set_emergency_icon(self) -> None:
        image = icons.draw("alert", 16, Theme.token("DANGER"))
        self.emergency_btn.setIcon(QIcon(icons.to_pixmap(image)))
        self.emergency_btn.setIconSize(QSize(16, 16))

    def _build_profile(self) -> QWidget:
        self._chip = _ClickableFrame()
        self._chip.setObjectName("profileChip")
        self._chip.setFixedHeight(40)
        self._chip.setCursor(Qt.CursorShape.PointingHandCursor)
        self._chip.clicked.connect(self._open_menu)

        layout = QHBoxLayout(self._chip)
        layout.setContentsMargins(6, 4, 10, 4)
        layout.setSpacing(9)

        avatar = QLabel((self._user_name[:1] or "U").upper())
        avatar.setObjectName("avatarCircle")
        avatar.setFixedSize(28, 28)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_col = QVBoxLayout()
        text_col.setSpacing(0)
        name = QLabel(self._user_name)
        name.setObjectName("profileName")
        role = QLabel("MEDICAL STUDENT")
        role.setObjectName("profileRole")
        text_col.addWidget(name)
        text_col.addWidget(role)

        self._chevron = QLabel()
        self._chevron.setObjectName("panel")
        self._chevron.setPixmap(_chevron_down(14, Theme.token("TEXT_MUTED")))

        layout.addWidget(avatar)
        layout.addLayout(text_col)
        layout.addWidget(self._chevron)
        return self._chip

    def _open_menu(self) -> None:
        # Built fresh each time, so it always reflects the current theme and
        # never holds stale colours from before a light/dark switch.
        self._menu = ProfileMenu(self._user_name, self._user_email, self.window())
        self._menu.account_requested.connect(self.accountRequested.emit)
        self._menu.history_requested.connect(self.historyRequested.emit)
        self._menu.sign_out_requested.connect(self.signOutRequested.emit)
        self._menu.open_under(self._chip)

    # -------------------------------------------------------------- theme

    def _toggle_theme(self) -> None:
        Theme.toggle_mode()
        self.refresh_theme()
        self.themeToggled.emit(Theme.mode() == "dark")

    def refresh_theme(self) -> None:
        """Redraw every baked pixmap after a palette switch."""
        self._logo_label.setPixmap(logo_pixmap(LOGO_HEIGHT))
        self._search_icon.setPixmap(
            icons.to_pixmap(icons.search(16, Theme.token("ICON_MUTED")))
        )
        self._set_emergency_icon()
        self._chevron.setPixmap(_chevron_down(14, Theme.token("TEXT_MUTED")))
        for button in (self.fav_btn, self.notif_btn):
            button.refresh_icon()
        self.theme_btn.set_icon_name("moon" if Theme.mode() == "dark" else "sun")