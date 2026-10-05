"""Keeps track of Akeso updates for the whole app (one shared object).

    updates = UpdateManager.instance()
    updates.changed.connect(...)      # state / progress changed
    updates.check()                   # ask GitHub (in the background)
    updates.install()                 # download, verify, run the installer

The dashboard checks a few seconds after sign-in (quietly: a failed check
is not worth an error message) and puts a green dot on Settings when a
newer version exists. Settings shows the state and the buttons.
"""

import time
from typing import Optional

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication

from app.core.background import call_in_background
from app.core.device_identity import APP_VERSION
from app.core.paths import is_frozen
from app.core.sync_worker import start_worker
from app.services import updater
from app.services.updater import Release, UpdateError

RECHECK_SECONDS = 6 * 60 * 60        # a quiet re-check at most every 6 hours


class _DownloadWorker(QThread):
    progress = Signal(int, int)
    done = Signal(str)
    failed = Signal(str)

    def __init__(self, release: Release) -> None:
        super().__init__()
        self._release = release

    def run(self) -> None:
        try:
            path = updater.download(self._release, self.progress.emit,
                                    self.isInterruptionRequested)
        except UpdateError as exc:
            self.failed.emit(str(exc))
        except Exception as exc:  # noqa: BLE001 - shown, never a crash
            self.failed.emit(f"The update failed: {exc}")
        else:
            self.done.emit(str(path))


class UpdateManager(QObject):
    # states: idle, checking, current, available, downloading, installing, error
    changed = Signal()

    _instance: Optional["UpdateManager"] = None

    @classmethod
    def instance(cls) -> "UpdateManager":
        if cls._instance is None:
            cls._instance = UpdateManager(QApplication.instance())
            updater.clean_up_downloads()
        return cls._instance

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.state = "idle"
        self.release: Optional[Release] = None
        self.message = ""
        self.progress = (0, 0)
        self._checked_at = 0.0
        self._worker: Optional[_DownloadWorker] = None

    # ---------------------------------------------------------- queries

    @property
    def current_version(self) -> str:
        return APP_VERSION

    @property
    def can_install(self) -> bool:
        """Only the installed app updates itself; a copy run from IntelliJ
        would just install a second Akeso."""
        return is_frozen()

    @property
    def available(self) -> bool:
        return self.state in ("available", "downloading", "installing") \
            or (self.state == "error" and self.release is not None)

    # ---------------------------------------------------------- actions

    def check(self, quiet: bool = False) -> None:
        """Ask GitHub for the latest release. quiet: the automatic check
        (skipped if one ran recently; failures stay silent)."""
        if self.state in ("checking", "downloading", "installing"):
            return
        if quiet and time.monotonic() - self._checked_at < RECHECK_SECONDS \
                and self._checked_at:
            return
        self._set("checking")
        call_in_background(updater.fetch_latest,
                           on_done=self._checked,
                           on_error=lambda m: self._check_failed(m, quiet),
                           owner=self)

    def install(self) -> None:
        if self.release is None or self.state in ("downloading", "installing"):
            return
        if not self.can_install:
            self._set("error", "Updates install from the installed Akeso only. "
                               "This copy is running from the project folder.")
            return
        self.progress = (0, self.release.size)
        self._set("downloading")
        worker = _DownloadWorker(self.release)
        worker.progress.connect(self._on_progress)
        worker.done.connect(self._downloaded)
        worker.failed.connect(lambda m: self._set("error", m))
        self._worker = worker
        start_worker(worker)

    def cancel(self) -> None:
        if self._worker is not None and self._worker.isRunning():
            self._worker.requestInterruption()

    # ---------------------------------------------------------- private

    def _set(self, state: str, message: str = "") -> None:
        self.state = state
        self.message = message
        self.changed.emit()

    def _checked(self, release: Optional[Release]) -> None:
        self._checked_at = time.monotonic()
        if release is not None and updater.is_newer(release.version):
            self.release = release
            self._set("available")
        else:
            self.release = None
            self._set("current")

    def _check_failed(self, message: str, quiet: bool) -> None:
        self._checked_at = time.monotonic()
        if quiet:
            self._set("idle")
        else:
            self._set("error", message)

    def _on_progress(self, done: int, total: int) -> None:
        self.progress = (done, total)
        self.changed.emit()

    def _downloaded(self, path: str) -> None:
        self._worker = None
        try:
            updater.launch_installer(updater.Path(path))
        except UpdateError as exc:
            self._set("error", str(exc))
            return
        self._set("installing")
        # Close the windows normally (saves the window size, "Remember me"
        # and unsaved notes), then quit so the installer can replace files.
        for widget in QApplication.topLevelWidgets():
            if widget.isWindow() and widget.isVisible():
                widget.close()
        QApplication.quit()
