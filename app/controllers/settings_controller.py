"""Settings: applies and saves what the user picks on the Settings page.

The shell owns the header, sidebar and theme switching, so it hands this
class small callbacks rather than letting it reach into those widgets.
"""

import os
import sys
from typing import Callable

from PySide6.QtCore import QObject, QProcess
from PySide6.QtWidgets import QApplication

from app.controllers.search_history_controller import SearchHistoryController
from app.controllers.update_controller import UpdateManager
from app.core.device_identity import APP_VERSION
from app.core.preferences import PreferenceStore
from app.core.theme import Theme
from app.repositories.local_account_data import LocalAccountData
from app.services.search_history_service import SearchHistoryService
from app.ui.views.account.account_dialogs import ConfirmDialog, LegalDialog
from app.ui.components.fluid import ResponsiveGrid
from app.ui.views.settings_view import SettingsView


def running_scale() -> int:
    """The display size this session started with (main.py sets it)."""
    try:
        return round(float(os.environ.get("QT_SCALE_FACTOR", "1")) * 100)
    except ValueError:
        return 100


class SettingsController(QObject):
    def __init__(self, view: SettingsView, prefs: PreferenceStore,
                 history: SearchHistoryService, history_controller: SearchHistoryController,
                 start_options: list[tuple[str, str]],
                 apply_theme: Callable[[str], None],
                 apply_color_theme: Callable[[str], None],
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
        view.color_theme_chosen.connect(apply_color_theme)
        view.pin_toggled.connect(self._pin)
        view.start_tab_chosen.connect(lambda tab: self._prefs.update(start_tab=tab))
        view.history_saving_toggled.connect(self._saving)
        view.open_history_requested.connect(open_history)
        view.clear_history_requested.connect(self._clear_history)
        view.clear_cache_requested.connect(self._clear_cache)
        view.read_terms_requested.connect(lambda: LegalDialog("terms", parent=view).exec())
        view.read_privacy_requested.connect(lambda: LegalDialog("privacy", parent=view).exec())
        view.scale_chosen.connect(self._scale)
        view.columns_chosen.connect(self._columns)
        view.restart_requested.connect(self._restart)

        # Updates (update_controller.py): the shared manager keeps the state,
        # this page shows it.
        self._updates = UpdateManager.instance()
        self._updates.changed.connect(self._show_update)
        view.check_updates_requested.connect(lambda: self._updates.check())
        view.install_update_requested.connect(self._install_update)
        view.open_releases_requested.connect(self._open_releases)
        self._show_update()

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
        self._view.show_display(prefs.ui_scale, running_scale(), prefs.cards_per_row)
        self._view.show_color_themes(Theme.color_theme(), Theme.mode())

    # ------------------------------------------------------------- private

    def _show_update(self) -> None:
        u = self._updates
        release = u.release
        self._view.show_update(
            state=u.state, current=u.current_version,
            latest=release.version if release else "", notes=release.notes if release else "",
            message=u.message, done=u.progress[0], total=u.progress[1],
            can_install=u.can_install)

    def _install_update(self) -> None:
        release = self._updates.release
        if release is None:
            return
        size = release.size / 1048576
        dialog = ConfirmDialog(
            f"Update to Akeso {release.version}?",
            f"Akeso downloads the update ({size:.0f} MB), checks that it is genuine, then "
            "closes, installs it and opens again. Your notes, settings and saved sign-in "
            "are kept.\n\nUnsaved work in an open note is saved first.",
            "Update now", "download", parent=self._view)
        if dialog.exec() == ConfirmDialog.DialogCode.Accepted:
            self._updates.install()

    @staticmethod
    def _open_releases() -> None:
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        from app.services.updater import RELEASES_PAGE
        QDesktopServices.openUrl(QUrl(RELEASES_PAGE))

    def _theme(self, mode: str) -> None:
        if mode != Theme.mode():
            self._apply_theme(mode)        # the shell saves it with the header's toggle

    def _scale(self, percent: int) -> None:
        prefs = self._prefs.update(ui_scale=percent)
        self._view.show_display(prefs.ui_scale, running_scale(), prefs.cards_per_row)

    def _columns(self, columns: int) -> None:
        prefs = self._prefs.update(cards_per_row=columns)
        ResponsiveGrid.set_user_columns(prefs.cards_per_row)      # applies right away
        self._view.banner.show_message(
            "Encyclopedia cards now fit as many as the window allows." if not columns else
            f"Encyclopedias now show up to {columns} cards per row.", "good")

    def _restart(self) -> None:
        """Start a fresh copy of Akeso, then close this one (the new size is
        read at start-up). Sessions are not stored, so the new copy opens on
        the sign-in screen; unsaved notebook edits are flushed on quit."""
        env_scale = os.environ.pop("QT_SCALE_FACTOR", None)   # let main.py read the new one
        # Packaged: sys.executable is Akeso.exe and argv[0] is that same path,
        # so pass only the real arguments. From IntelliJ: python + main.py.
        frozen = getattr(sys, "frozen", False)
        arguments = sys.argv[1:] if frozen else sys.argv
        if not QProcess.startDetached(sys.executable, arguments):
            if env_scale is not None:
                os.environ["QT_SCALE_FACTOR"] = env_scale
            self._view.banner.show_message(
                "Could not restart automatically. Close Akeso and open it again.", "danger")
            return
        QApplication.quit()

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
