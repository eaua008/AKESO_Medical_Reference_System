"""When the Study Notebook syncs with the account, and what the notebook
home says about it.

  * right after signing in            download + upload
  * every 30 s, if something changed  upload (and download)
  * every 3 min                       download what other computers changed
  * "Sync now" on the notebook home   both, straight away
  * signing out / closing Akeso       a last upload (waits a few seconds at
                                      most, so closing never hangs offline)

Every round runs on a background thread. Offline or signed out, the
notebook keeps working from this computer and tries again later; nothing
is lost, because local changes stay marked until an upload succeeds.
"""

import threading
from datetime import datetime
from typing import Callable, Optional

from PySide6.QtCore import QObject, QTimer

from app.core.background import call_in_background
from app.repositories.notebook_cloud_repository import NotebookNotInstalled
from app.services.notebook_sync import NotebookSync, SyncResult

PUSH_EVERY_MS = 30_000
PULL_EVERY_MS = 180_000
LAST_WAIT_S = 6


class NotebookSyncController(QObject):
    def __init__(self, sync: NotebookSync, home, on_changed: Callable[[], None],
                 before_sync: Optional[Callable[[], None]] = None,
                 parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._sync = sync
        self._home = home                    # NotebookHome: set_sync_status(), sync_requested
        self._on_changed = on_changed        # redraw the notebook after a download
        self._before_sync = before_sync      # save open editors first
        self._running = False
        self._stopped = False
        self._disabled = False               # migration 011 missing
        self._last_ok: Optional[datetime] = None

        self._push_timer = QTimer(self)
        self._push_timer.setInterval(PUSH_EVERY_MS)
        self._push_timer.timeout.connect(self._push_if_needed)
        self._pull_timer = QTimer(self)
        self._pull_timer.setInterval(PULL_EVERY_MS)
        self._pull_timer.timeout.connect(self.sync_now)
        self._clock = QTimer(self)                   # keeps "2 min ago" fresh
        self._clock.setInterval(30_000)
        self._clock.timeout.connect(self._show_ok)
        home.sync_requested.connect(self.sync_now)

    def start(self) -> None:
        self._home.set_sync_status("Syncing your notebook…", "muted")
        QTimer.singleShot(1500, self.sync_now)
        self._push_timer.start()
        self._pull_timer.start()
        self._clock.start()

    # -------------------------------------------------------------- rounds

    def _push_if_needed(self) -> None:
        if self._before_sync is not None:
            self._before_sync()
        if self._sync.has_local_changes():
            self.sync_now()

    def sync_now(self) -> None:
        if self._running or self._stopped or self._disabled:
            return
        if self._before_sync is not None:
            self._before_sync()
        self._running = True
        self._home.set_sync_status("Syncing your notebook…", "muted")
        call_in_background(self._sync.sync, self._done, self._failed, owner=self)

    def _done(self, result: SyncResult) -> None:
        self._running = False
        self._last_ok = datetime.now()
        if result.changed_here:
            self._on_changed()
        self._show_ok()

    def _failed(self, message: str) -> None:
        self._running = False
        if "011_notebook_sync" in message:
            self._disabled = True
            self._home.set_sync_status(
                "Saved on this computer only. Cloud sync needs migration 011.", "warn")
            return
        self._home.set_sync_status(
            "Offline: saved on this computer, will sync when you're back online.", "warn")

    def _show_ok(self) -> None:
        if self._last_ok is None or self._running or self._disabled:
            return
        minutes = int((datetime.now() - self._last_ok).total_seconds() // 60)
        when = "just now" if minutes < 1 else f"{minutes} min ago" if minutes < 60 else \
            self._last_ok.strftime("at %I:%M %p").replace(" 0", " ")
        pending = " · changes waiting" if self._sync.has_local_changes() else ""
        self._home.set_sync_status(f"Synced to your account {when}{pending}", "good")

    # ------------------------------------------------------------- the end

    def shutdown(self) -> None:
        """Last upload before signing out / closing. Waits LAST_WAIT_S at
        most: offline, the changes simply go up next time."""
        if self._stopped:
            return
        self._stopped = True
        for timer in (self._push_timer, self._pull_timer, self._clock):
            timer.stop()
        if self._disabled:
            return
        if self._before_sync is not None:
            try:
                self._before_sync()
            except Exception:  # noqa: BLE001
                pass
        try:
            if not self._sync.has_local_changes():
                return
        except Exception:  # noqa: BLE001
            return

        def last_round() -> None:
            try:
                self._sync.sync()
            except Exception:  # noqa: BLE001 - offline: next time
                pass
        worker = threading.Thread(target=last_round, daemon=True)
        worker.start()
        worker.join(LAST_WAIT_S)

    @staticmethod
    def not_installed(error: Exception) -> bool:
        return isinstance(error, NotebookNotInstalled)
