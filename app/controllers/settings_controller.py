"""Settings: applies and saves what the user picks on the Settings page.

The shell owns the header, sidebar and theme switching, so it hands this
class small callbacks rather than letting it reach into those widgets.
"""

from typing import Callable

from PySide6.QtCore import QObject

from app.controllers.search_history_controller import SearchHistoryController
from app.core.device_identity import APP_VERSION
from app.core.preferences import PreferenceStore
from app.core.theme import Theme
from app.repositories.local_account_data import LocalAccountData
from app.services.search_history_service import SearchHistoryService
from app.ui.views.account.account_dialogs import ConfirmDialog, LegalDialog
from app.ui.views.settings_view import SettingsView


class SettingsController(QObject):
    def __init__(self, view: SettingsView, prefs: PreferenceStore,
                 history: SearchHistoryService, history_controller: SearchHistoryController,
                 start_options: list[tuple[str, str]],
                 apply_theme: Callable[[str], None],
                 apply_pinned: Callable[[bool], None],
                 open_history: Callable[[], None]) -> None:
        super().__init__(view)
        self._view = view
        self._prefs = prefs
        self._history = history
        self._history_controller = history_controller
        self._apply_theme = apply_theme
        self._apply_pinned = apply_pinned

        view.set_start_options(start_options)
        view.theme_chosen.connect(self._theme)
        view.pin_toggled.connect(self._pin)
        view.start_tab_chosen.connect(lambda tab: self._prefs.update(start_tab=tab))
        view.history_saving_toggled.connect(self._saving)
        view.open_history_requested.connect(open_history)
        view.clear_history_requested.connect(self._clear_history)
        view.clear_cache_requested.connect(self._clear_cache)
        view.read_terms_requested.connect(lambda: LegalDialog("terms", parent=view).exec())
        view.read_privacy_requested.connect(lambda: LegalDialog("privacy", parent=view).exec())

    def refresh(self) -> None:
        prefs = self._prefs.load()
        self._view.show_state(
            theme=Theme.mode(),
            pinned=prefs.sidebar_pinned,
            start_tab=prefs.start_tab,
            saving=self._history.saving_enabled(),
            history_count=self._history.counts().get("all", 0),
            cache_bytes=LocalAccountData.cache_size(),
            clear_pending=LocalAccountData.cache_clear_pending(),
            version=APP_VERSION,
        )

    # ------------------------------------------------------------- private

    def _theme(self, mode: str) -> None:
        if mode != Theme.mode():
            self._apply_theme(mode)        # the shell saves it with the header's toggle

    def _pin(self, on: bool) -> None:
        self._prefs.update(sidebar_pinned=on)
        self._apply_pinned(on)

    def _saving(self, on: bool) -> None:
        self._history.set_saving(on)
        self._history_controller.mark_stale()
        self._view.banner.show_message(
            "Search history is on." if on else
            "Search history is off. Searches you already made stay until you clear them.",
            "good" if on else "info")

    def _clear_history(self) -> None:
        if self._history_controller.clear():
            self._view.banner.show_message("Search history cleared.", "good")
            self.refresh()

    def _clear_cache(self) -> None:
        dialog = ConfirmDialog(
            "Clear downloaded reference data?",
            "The downloaded disease, symptom and medicine entries are removed the next time "
            "Akeso starts, then downloaded fresh. Your notes, bookmarks and saved cases stay.",
            "Clear at next start", "refresh-cw", parent=self._view)
        if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
            return
        try:
            LocalAccountData.schedule_cache_clear()
        except OSError as exc:
            self._view.banner.show_message(f"Could not schedule it: {exc}", "danger")
            return
        self._view.set_clear_pending(True)
        self._view.banner.show_message(
            "Done. The reference data will re-download the next time you open Akeso.", "good")
