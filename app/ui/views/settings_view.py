"""Settings: how Akeso looks and behaves on this computer.

Display only. Every control emits what the user picked; SettingsController
applies it and saves it. Built from the Account page's pieces (#acCard,
SwitchRow, #acChip...) so the two pages feel like one workspace.
"""

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QFrame, QGridLayout, QHBoxLayout, QProgressBar, QPushButton,
    QScrollArea, QVBoxLayout, QWidget,
)

from app.core.preferences import CARD_COLUMNS, UI_SCALES
from app.ui.views.account.account_widgets import (
    Banner, Card, SwitchRow, button, divider, label, refresh_icons, repolish, set_text,
)

# The maker's credit (also on the sign-in screen and in THIRD_PARTY_NOTICES.md).
CREDIT_NAME = "Eijkim Maulit  |  @eaua008"
CREDIT_LINE = ("A student of Mapúa Malayan Colleges Mindanao, who built Akeso during "
               "his second year.")

SHORTCUTS = [
    ("Ctrl + K", "Jump to the search bar"),
    ("↑ / ↓", "Move through search suggestions"),
    ("Enter", "Open the highlighted suggestion"),
    ("Esc", "Close a detail page or the suggestions"),
]


def theme_preview(palette: dict, width: int = 150, height: int = 76) -> QPixmap:
    """A tiny picture of Akeso in a palette: sidebar, a card, a button."""
    ratio = 2
    pix = QPixmap(width * ratio, height * ratio)
    pix.setDevicePixelRatio(ratio)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(QColor(palette["BORDER"]))
    p.setBrush(QColor(palette["BG"]))
    p.drawRoundedRect(QRectF(0.5, 0.5, width - 1, height - 1), 8, 8)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(palette["SURFACE"]))                       # sidebar
    p.drawRoundedRect(QRectF(5, 5, 22, height - 10), 5, 5)
    p.setBrush(QColor(palette["BADGE_TEXT"]))
    p.drawRoundedRect(QRectF(9, 11, 14, 5), 2, 2)                # active nav item
    p.setBrush(QColor(palette["ICON_MUTED"]))
    for y in (22, 31, 40):
        p.drawRoundedRect(QRectF(10, y, 12, 3), 1.5, 1.5)
    p.setBrush(QColor(palette["SURFACE_RAISED"]))                # a card
    p.setPen(QColor(palette["BORDER"]))
    p.drawRoundedRect(QRectF(33, 9, width - 40, height - 18), 6, 6)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(palette["TEXT"]))
    p.drawRoundedRect(QRectF(41, 17, 56, 5), 2.5, 2.5)            # title
    p.setBrush(QColor(palette["TEXT_MUTED"]))
    p.drawRoundedRect(QRectF(41, 27, 80, 3), 1.5, 1.5)
    p.drawRoundedRect(QRectF(41, 34, 64, 3), 1.5, 1.5)
    p.setBrush(QColor(palette["PRIMARY"]))
    p.drawRoundedRect(QRectF(41, height - 25, 38, 11), 5, 5)       # button
    p.setBrush(QColor(palette["ACCENT_2"]))
    p.drawEllipse(QRectF(width - 26, height - 24, 9, 9))           # second accent
    p.setBrush(QColor(palette["BADGE_TEXT"]))
    p.drawEllipse(QRectF(width - 38, height - 24, 9, 9))
    p.end()
    return pix


class ThemeTile(QFrame):
    """One colour theme in the gallery: preview, name, one-line description."""

    clicked = Signal(str)

    def __init__(self, theme_id: str, preset: dict, mode: str, selected: bool) -> None:
        super().__init__()
        from app.core.theme import Theme
        self.setObjectName("themeTile")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(preset.get("blurb", ""))
        self._id = theme_id
        p = Theme.palette_for(Theme.color_theme(), Theme.mode())     # the app's colours now
        self.setStyleSheet(
            f"#themeTile {{ background: {p['SURFACE_ALT']}; border-radius: 12px; "
            f"border: {'2px solid ' + p['PRIMARY'] if selected else '1px solid ' + p['BORDER']}; }}"
            f"#themeTile:hover {{ border-color: {p['PRIMARY_HOVER']}; }}")
        column = QVBoxLayout(self)
        column.setContentsMargins(8, 8, 8, 8)
        column.setSpacing(6)
        preview = label("", "panel", wrap=False)
        preview.setPixmap(theme_preview(Theme.palette_for(theme_id, mode)))
        preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        column.addWidget(preview)
        name = QHBoxLayout()
        name.setSpacing(6)
        name.addWidget(label(preset.get("name", theme_id), "acRowTitle", wrap=False), 1)
        if selected:
            name.addWidget(label("✓ In use", "acOk", wrap=False))
        column.addLayout(name)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._id)
        super().mouseReleaseEvent(event)


class SettingsView(QWidget):
    theme_chosen = Signal(str)             # "light" or "dark"
    color_theme_chosen = Signal(str)       # "dracula", "nord"... (theme_presets.py)
    pin_toggled = Signal(bool)
    start_tab_chosen = Signal(str)
    history_saving_toggled = Signal(bool)
    open_history_requested = Signal()
    clear_history_requested = Signal()
    clear_cache_requested = Signal()
    read_terms_requested = Signal()
    read_privacy_requested = Signal()
    scale_chosen = Signal(int)             # percent
    columns_chosen = Signal(int)           # 0 = auto
    restart_requested = Signal()
    check_updates_requested = Signal()
    install_update_requested = Signal()
    open_releases_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
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

        title = QVBoxLayout()
        title.setSpacing(4)
        title.addWidget(label("Settings", "acTitle"))
        title.addWidget(label("How Akeso looks and behaves on this computer. Your profile and "
                              "sign-in security are in Account Settings.", "acSubtitle"))
        column.addLayout(title)

        self.banner = Banner()
        column.addWidget(self.banner)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.addWidget(self._appearance(), 0, 0, 1, 2)
        grid.addWidget(self._navigation(), 1, 0)
        grid.addWidget(self._display(), 1, 1, 2, 1)
        grid.addWidget(self._search(), 2, 0)
        grid.addWidget(self._offline(), 3, 0)
        grid.addWidget(self._shortcuts(), 3, 1)
        grid.addWidget(self._about(), 4, 0)
        grid.addWidget(self._updates(), 4, 1)
        column.addLayout(grid)
        column.addStretch(1)

        scroll.setWidget(page)
        outer.addWidget(scroll)

    # -------------------------------------------------------------- cards

    def _appearance(self) -> Card:
        card = Card("Appearance", "A colour theme, in light or dark. The sun / moon button "
                    "at the top switches light and dark within the theme.", "layout-grid")
        row = QHBoxLayout()
        row.setSpacing(8)
        self._theme_group = QButtonGroup(self)
        self._theme_group.setExclusive(True)
        self._theme_buttons: dict[str, QPushButton] = {}
        for key, text in (("light", "Light"), ("dark", "Dark")):
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.clicked.connect(lambda _c=False, k=key: self.theme_chosen.emit(k))
            self._theme_group.addButton(chip)
            self._theme_buttons[key] = chip
            row.addWidget(chip)
        row.addStretch(1)
        card.body.addLayout(row)
        card.body.addWidget(label("THEME", "acFieldLabel"))
        self._theme_grid = QGridLayout()
        self._theme_grid.setHorizontalSpacing(10)
        self._theme_grid.setVerticalSpacing(10)
        card.body.addLayout(self._theme_grid)
        self._theme_tiles: dict[str, ThemeTile] = {}
        card.body.addWidget(label("Both choices are remembered the next time Akeso opens, on "
                                  "the sign-in screen too.", "acSmall"))
        return card

    def show_color_themes(self, current: str, mode: str) -> None:
        """(Re)draw the theme tiles: previews follow the current light/dark."""
        from app.core.theme_presets import ORDER, PRESETS
        for tile in self._theme_tiles.values():
            self._theme_grid.removeWidget(tile)
            tile.deleteLater()
        self._theme_tiles = {}
        for i, theme_id in enumerate(ORDER):
            tile = ThemeTile(theme_id, PRESETS[theme_id], mode, theme_id == current)
            tile.clicked.connect(self.color_theme_chosen.emit)
            self._theme_grid.addWidget(tile, i // 5, i % 5)
            self._theme_tiles[theme_id] = tile
        for column in range(5):
            self._theme_grid.setColumnStretch(column, 1)

    def _chip_row(self, options: list[tuple[int, str]], signal) -> tuple[QHBoxLayout, dict]:
        row = QHBoxLayout()
        row.setSpacing(6)
        group = QButtonGroup(self)
        group.setExclusive(True)
        chips: dict[int, QPushButton] = {}
        for value, text in options:
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.clicked.connect(lambda _c=False, v=value: signal.emit(v))
            group.addButton(chip)
            chips[value] = chip
            row.addWidget(chip)
        row.addStretch(1)
        return row, chips

    def _display(self) -> Card:
        card = Card("Display", "How big things are, and how many cards fit in a row.",
                    "search")
        card.body.addWidget(label("SIZE", "acFieldLabel"))
        row, self._scale_chips = self._chip_row(
            [(s, f"{s}%") for s in UI_SCALES], self.scale_chosen)
        card.body.addLayout(row)
        card.body.addWidget(label("Text, buttons, cards and the sidebar all scale together. "
                                  "90% is the default; pick a bigger size if text is hard "
                                  "to read.", "acSmall"))
        self._scale_floor_note = label("", "acSmall")
        self._scale_floor_note.hide()
        card.body.addWidget(self._scale_floor_note)
        self._restart_row = QWidget()
        self._restart_row.setObjectName("panel")
        rr = QHBoxLayout(self._restart_row)
        rr.setContentsMargins(0, 2, 0, 0)
        rr.setSpacing(10)
        self._restart_note = label("", "acValue")
        rr.addWidget(self._restart_note, 1)
        rr.addWidget(button("Restart now", "acPrimary", "refresh-cw",
                            self.restart_requested.emit))
        self._restart_row.hide()
        card.body.addWidget(self._restart_row)
        card.body.addWidget(divider())
        card.body.addWidget(label("CARDS PER ROW", "acFieldLabel"))
        row, self._column_chips = self._chip_row(
            [(c, "Auto" if c == 0 else str(c)) for c in CARD_COLUMNS], self.columns_chosen)
        card.body.addLayout(row)
        card.body.addWidget(label("In the Disease, Symptom and Medicine encyclopedias. Auto "
                                  "fits as many as the window allows; fewer show when the "
                                  "window is too narrow for your choice.", "acSmall"))
        return card

    def _navigation(self) -> Card:
        card = Card("Navigation", "The sidebar and where Akeso opens.", "panel-left")
        self.pin = SwitchRow("Keep the sidebar open",
                             "Off: the sidebar shrinks to icons and opens when you point at "
                             "it. Same as the pin at the top of the sidebar.")
        self.pin.toggled.connect(self.pin_toggled.emit)
        card.body.addWidget(self.pin)
        card.body.addWidget(divider())
        card.body.addWidget(label("OPEN ON START", "acFieldLabel"))
        self.start_tab = QComboBox()
        self.start_tab.setObjectName("acInput")
        self.start_tab.activated.connect(
            lambda i: self.start_tab_chosen.emit(self.start_tab.itemData(i)))
        card.body.addWidget(self.start_tab)
        card.body.addWidget(label("The screen you see right after signing in.", "acSmall"))
        return card

    def _search(self) -> Card:
        card = Card("Search history", "Kept on this computer only, for this account.",
                    "history")
        self.saving = SwitchRow("Save my search history",
                                "Remembers what you open from the search bar. Off: nothing "
                                "new is saved; what is already there stays until you clear "
                                "it.")
        self.saving.toggled.connect(self.history_saving_toggled.emit)
        card.body.addWidget(self.saving)
        self._history_count = label("", "acValue")
        card.body.addWidget(self._history_count)
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(button("Open Search History", "acGhost", "history",
                             self.open_history_requested.emit))
        self._clear_history = button("Clear search history", "acDanger", "trash-2",
                                     self.clear_history_requested.emit)
        row.addWidget(self._clear_history)
        row.addStretch(1)
        card.body.addLayout(row)
        return card

    def _offline(self) -> Card:
        card = Card("Offline reference data", "Entries downloaded so Akeso works without "
                    "internet.", "database")
        self._cache_size = label("", "acValue")
        card.body.addWidget(self._cache_size)
        self._clear_cache = button("Clear downloaded reference data", "acGhost", "refresh-cw",
                                   self.clear_cache_requested.emit)
        card.body.addWidget(self._clear_cache, 0, Qt.AlignmentFlag.AlignLeft)
        card.body.addWidget(label("Removed the next time Akeso starts, then downloaded fresh. "
                                  "Your notes, bookmarks and saved cases are not touched.",
                                  "acSmall"))
        return card

    def _shortcuts(self) -> Card:
        card = Card("Keyboard shortcuts", "Work faster without the mouse.", "layers")
        for keys, action in SHORTCUTS:
            row = QHBoxLayout()
            row.setSpacing(12)
            row.addWidget(label(action, "acValue"), 1)
            row.addWidget(label(keys, "acPill", wrap=False), 0, Qt.AlignmentFlag.AlignRight)
            card.body.addLayout(row)
        return card

    def _about(self) -> Card:
        card = Card("About Akeso", "", "info")
        self._version = label("", "acValue")
        card.body.addWidget(self._version)
        card.body.addWidget(label("A study reference for students. Results are educational, "
                                  "not a diagnosis or medical advice.", "acSmall"))
        card.body.addWidget(divider())
        card.body.addWidget(label("CREATED BY", "acFieldLabel"))
        card.body.addWidget(label(CREDIT_NAME, "acValue"))
        card.body.addWidget(label(CREDIT_LINE, "acSmall"))
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(button("Read Terms", "acGhost", on_click=self.read_terms_requested.emit))
        row.addWidget(button("Read Privacy Notice", "acGhost",
                             on_click=self.read_privacy_requested.emit))
        row.addStretch(1)
        card.body.addLayout(row)
        return card

    def _updates(self) -> Card:
        card = Card("Updates", "New versions of Akeso, installed in one click.",
                    "refresh-cw")
        self._update_status = label("", "acValue")
        card.body.addWidget(self._update_status)
        self._update_notes = label("", "acSmall")
        self._update_notes.hide()
        card.body.addWidget(self._update_notes)
        self._update_bar = QProgressBar()
        self._update_bar.setTextVisible(False)
        self._update_bar.setFixedHeight(6)
        self._update_bar.hide()
        card.body.addWidget(self._update_bar)
        row = QHBoxLayout()
        row.setSpacing(8)
        self._install_update = button("Update now", "acPrimary", "download",
                                      self.install_update_requested.emit)
        self._install_update.hide()
        row.addWidget(self._install_update)
        self._check_updates = button("Check for updates", "acGhost", "refresh-cw",
                                     self.check_updates_requested.emit)
        row.addWidget(self._check_updates)
        row.addStretch(1)
        card.body.addLayout(row)
        self._releases_link = button("See all releases", "acGhost", "external-link",
                                     self.open_releases_requested.emit)
        card.body.addWidget(self._releases_link, 0, Qt.AlignmentFlag.AlignLeft)
        card.body.addWidget(label("Your notes, settings and saved sign-in are kept. Akeso "
                                  "closes, updates and opens again by itself.", "acSmall"))
        return card

    def show_update(self, *, state: str, current: str, latest: str, notes: str,
                    message: str, done: int, total: int, can_install: bool) -> None:
        """state: idle | checking | current | available | downloading |
        installing | error (see update_controller.py)."""
        texts = {
            "idle": f"Akeso {current}.",
            "checking": "Checking for updates\u2026",
            "current": f"Akeso {current} is the latest version.",
            "available": f"Akeso {latest} is available. You have {current}.",
            "downloading": f"Downloading Akeso {latest}\u2026",
            "installing": f"Installing Akeso {latest}. Akeso will open again in a moment.",
            "error": message or "Something went wrong.",
        }
        self._update_status.setText(texts.get(state, ""))
        self._update_status.setObjectName("acError" if state == "error" else "acValue")
        repolish(self._update_status)
        show_notes = bool(latest) and state in ("available", "downloading") and bool(notes)
        self._update_notes.setText(notes[:600] + ("\u2026" if len(notes) > 600 else ""))
        self._update_notes.setVisible(show_notes)
        busy = state in ("downloading", "installing")
        self._update_bar.setVisible(busy)
        if state == "downloading" and total:
            self._update_bar.setRange(0, 1000)
            self._update_bar.setValue(int(done * 1000 / total))
            self._update_status.setText(
                f"Downloading Akeso {latest}\u2026  {done / 1048576:.0f} of "
                f"{total / 1048576:.0f} MB")
        elif busy:
            self._update_bar.setRange(0, 0)               # moving bar
        offer = bool(latest) and state in ("available", "error") and can_install
        self._install_update.setVisible(offer)
        if offer:
            set_text(self._install_update, f"Update to {latest}")
            self._paint_update_button()
        self._check_updates.setEnabled(state not in ("checking", "downloading", "installing"))
        self._check_updates.setVisible(not busy)

    def _paint_update_button(self) -> None:
        """The green "there is an update" button."""
        from app.core.theme import Theme
        green = Theme.token("SUCCESS")
        self._install_update.setStyleSheet(
            f"QPushButton {{ background-color: {green}; color: #FFFFFF; border: none; }}"
            f"QPushButton:hover {{ background-color: {green}; border: 1px solid #FFFFFF; }}")

    # ---------------------------------------------------------------- api

    def set_start_options(self, options: list[tuple[str, str]]) -> None:
        self.start_tab.blockSignals(True)
        self.start_tab.clear()
        for tab_id, text in options:
            self.start_tab.addItem(text, tab_id)
        self.start_tab.blockSignals(False)

    def show_state(self, *, theme: str, pinned: bool, start_tab: str, saving: bool,
                   history_count: int, cache_bytes: int, clear_pending: bool,
                   version: str) -> None:
        self._theme_buttons.get(theme, self._theme_buttons["light"]).setChecked(True)
        self.pin.set_checked(pinned)
        index = self.start_tab.findData(start_tab)
        self.start_tab.setCurrentIndex(max(index, 0))
        self.saving.set_checked(saving)
        self._history_count.setText(
            f"{history_count} saved search{'es' if history_count != 1 else ''}."
            if history_count else "No saved searches.")
        self._clear_history.setEnabled(history_count > 0)
        size = cache_bytes / (1024 * 1024)
        self._cache_size.setText(f"{size:.1f} MB of reference data on this computer."
                                 if cache_bytes else "No reference data downloaded yet.")
        self.set_clear_pending(clear_pending)
        self._version.setText(f"Akeso {version}")

    def show_display(self, scale: int, running_scale: int, columns: int,
                     effective: int = 0, floor: int = 0) -> None:
        """scale: saved choice; running_scale: what this session started with;
        effective: the size the choice really gives on this screen; floor:
        the smallest size this screen allows (app/core/display_scale.py)."""
        effective = effective or scale
        chip = self._scale_chips.get(scale)
        if chip is not None:
            chip.setChecked(True)
        chip = self._column_chips.get(columns)
        if chip is not None:
            chip.setChecked(True)
        limited = effective != scale
        self._scale_floor_note.setText(
            f"On this screen Akeso can't go below {floor}%, so it uses {effective}%. Smaller "
            "sizes break the 3D body and the built-in browser (with Windows display scaling "
            "at 100%, the browser engine can't draw smaller than normal)." if limited else "")
        self._scale_floor_note.setVisible(limited)
        pending = effective != running_scale
        self._restart_note.setText(f"Akeso is showing {running_scale}%. Restart to use "
                                   f"{effective}% (you will sign in again). Or it applies the "
                                   "next time you open Akeso." if pending else "")
        self._restart_row.setVisible(pending)

    def set_clear_pending(self, pending: bool) -> None:
        self._clear_cache.setEnabled(not pending)
        set_text(self._clear_cache, "Will clear at next start" if pending
                 else "Clear downloaded reference data")

    def refresh_theme(self) -> None:
        refresh_icons(self)
        repolish(self)
        if self._install_update.isVisible():
            self._paint_update_button()
