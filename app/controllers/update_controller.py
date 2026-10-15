"""Keeps track of Akeso updates for the whole app (one shared object).

    updates = UpdateManager.instance()
    updates.changed.connect(...)      # state / progress changed
    updates.check()                   # ask GitHub (in the background)
    updates.install()                 # download, verify, run the installer
    updates.check_files()             # Repair: are all program files there?
    updates.repair()                  # reinstall this version (or update)

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
from app.services import repair as repair_files
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


class _CheckFilesWorker(QThread):
    progress = Signal(int, int)
    done = Signal(object)
    failed = Signal(str)

    def run(self) -> None:
        try:
            report = repair_files.check_files(self.progress.emit, self.isInterruptionRequested)
        except repair_files.RepairError as exc:
            self.failed.emit(str(exc))
        except Exception:  # noqa: BLE001 - shown as a plain message, never a crash
            self.failed.emit("The file check could not finish. Try Repair Akeso anyway.")
        else:
            self.done.emit(report)


class UpdateManager(QObject):
    # states: idle, checking, current, available, downloading, installing, error
    changed = Signal()
    # repair states: idle, scanning, ok, damaged, unknown (no file list), error
    repair_changed = Signal()

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
        self.repair_state = "idle"
        self.repair_message = ""
        self.repair_progress = (0, 0)
        self.repairing = False             # the download running is a repair
        self._scan: Optional[_CheckFilesWorker] = None

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

    def check_files(self) -> None:
        """Settings > Updates > Check files (in the background)."""
        if self.repair_state == "scanning":
            return
        if not self.can_install:
            self._set_repair("error", "The file check works on the installed Akeso only. "
                                      "This copy is running from the project folder.")
            return
        self.repair_progress = (0, 0)
        self._set_repair("scanning")
        worker = _CheckFilesWorker()
        worker.progress.connect(self._on_scan_progress)
        worker.done.connect(self._scanned)
        worker.failed.connect(lambda m: self._set_repair("error", m))
        self._scan = worker
        start_worker(worker)

    def repair(self) -> None:
        """Reinstall every file. If a newer version is out, updating does
        the same job and brings the fixes too."""
        if self.state in ("downloading", "installing"):
            return
        if not self.can_install:
            self._set_repair("error", "Repair works on the installed Akeso only. "
                                      "This copy is running from the project folder.")
            return
        if self.release is not None and updater.is_newer(self.release.version):
            self.repairing = True
            self.install()
            return
        self._set_repair("fetching")
        call_in_background(repair_files.release_for_this_version,
                           on_done=self._repair_release,
                           on_error=self._repair_failed, owner=self)

    def cancel(self) -> None:
        if self._worker is not None and self._worker.isRunning():
            self._worker.requestInterruption()

    # ---------------------------------------------------------- private

    def _set(self, state: str, message: str = "") -> None:
        if state == "error" and self.repairing:
            self.repairing = False
            if self.release is not None and not updater.is_newer(self.release.version):
                self.release = None            # not an update: no "Update to" button
            self._set_repair("error", message)
            state, message = "idle", ""
        self.state = state
        self.message = message
        self.changed.emit()

    def _set_repair(self, state: str, message: str = "") -> None:
        self.repair_state = state
        self.repair_message = message
        self.repair_changed.emit()

    def _on_scan_progress(self, done: int, total: int) -> None:
        self.repair_progress = (done, total)
        self.repair_changed.emit()

    def _scanned(self, report) -> None:
        self._scan = None
        if not report.has_manifest:
            state = "unknown"
        else:
            state = "ok" if report.ok else "damaged"
        self._set_repair(state, repair_files.summary(report))

    def _repair_release(self, release: Release) -> None:
        self.release = release
        self.repairing = True
        self._set_repair("idle")
        self.install()

    def _repair_failed(self, message: str) -> None:
        # RepairError messages are written for users; anything else is not.
        friendly = message if message.endswith(".") and len(message) < 200 else \
            "The repair could not start. Check your internet connection and try again."
        self._set_repair("error", friendly)

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
