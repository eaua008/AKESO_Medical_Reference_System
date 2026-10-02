"""Settings: how Akeso looks and behaves on this computer.

Display only. Every control emits what the user picked; SettingsController
applies it and saves it. Built from the Account page's pieces (#acCard,
SwitchRow, #acChip...) so the two pages feel like one workspace.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QFrame, QGridLayout, QHBoxLayout, QPushButton, QScrollArea,
    QVBoxLayout, QWidget,
)

from app.ui.views.account.account_widgets import (
    Banner, Card, SwitchRow, button, divider, label, refresh_icons, repolish, set_text,
)

SHORTCUTS = [
    ("Ctrl + K", "Jump to the search bar"),
    ("↑ / ↓", "Move through search suggestions"),
    ("Enter", "Open the highlighted suggestion"),
    ("Esc", "Close a detail page or the suggestions"),
]


class SettingsView(QWidget):
    theme_chosen = Signal(str)             # "light" or "dark"
    pin_toggled = Signal(bool)
    start_tab_chosen = Signal(str)
    history_saving_toggled = Signal(bool)
    open_history_requested = Signal()
    clear_history_requested = Signal()
    clear_cache_requested = Signal()
    read_terms_requested = Signal()
    read_privacy_requested = Signal()

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
        grid.addWidget(self._appearance(), 0, 0)
        grid.addWidget(self._navigation(), 0, 1)
        grid.addWidget(self._search(), 1, 0)
        grid.addWidget(self._offline(), 1, 1)
        grid.addWidget(self._shortcuts(), 2, 0)
        grid.addWidget(self._about(), 2, 1)
        column.addLayout(grid)
        column.addStretch(1)

        scroll.setWidget(page)
        outer.addWidget(scroll)

    # -------------------------------------------------------------- cards

    def _appearance(self) -> Card:
        card = Card("Appearance", "Light or dark. The sun / moon button at the top "
                    "switches it too.", "layout-grid")
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
        card.body.addWidget(label("Remembered the next time Akeso opens, on the sign-in "
                                  "screen too.", "acSmall"))
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
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(button("Read Terms", "acGhost", on_click=self.read_terms_requested.emit))
        row.addWidget(button("Read Privacy Notice", "acGhost",
                             on_click=self.read_privacy_requested.emit))
        row.addStretch(1)
        card.body.addLayout(row)
        return card

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

    def set_clear_pending(self, pending: bool) -> None:
        self._clear_cache.setEnabled(not pending)
        set_text(self._clear_cache, "Will clear at next start" if pending
                 else "Clear downloaded reference data")

    def refresh_theme(self) -> None:
        refresh_icons(self)
        repolish(self)
