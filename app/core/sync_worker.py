"""Runs the encyclopedia sync on a background thread.

The sync talks to Supabase, and on a slow connection that can take a few
seconds. On the UI thread the whole window would freeze for that time. Here
it runs alongside, and the app keeps serving the local copy while it works.

The worker only writes to disk. It reports back with a signal, and the UI
thread reloads from the local copy — so the in-memory data is only ever
touched by one thread.
"""

from PySide6.QtCore import QCoreApplication, QThread, Signal

from app.repositories.supabase_disease_repository import DiseaseRepositoryError


class SyncWorker(QThread):
    """Calls service.sync() without blocking the interface."""

    # changed: whether a newer copy was written. error: a message, or "".
    sync_finished = Signal(bool, str)

    def __init__(self, service, force: bool = False, parent=None) -> None:
        super().__init__(parent)
        self._service = service
        self._force = force

    def run(self) -> None:
        try:
            changed = self._service.sync(force=self._force)
        except DiseaseRepositoryError as exc:
            # Offline, or Supabase unreachable. Not fatal: the local copy
            # keeps working, and the next sync will try again.
            self.sync_finished.emit(False, str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            # Anything unexpected must still end this thread cleanly and be
            # reported, or the UI would sit on "Syncing…" forever.
            self.sync_finished.emit(False, f"Unexpected sync error: {exc}")
            return
        self.sync_finished.emit(changed, "")


# --------------------------------------------------------------------------
# Worker lifetime
#
# Qt aborts the whole process if a QThread object is destroyed while its
# thread is still running. That can happen here two ways: closing the window
# mid-sync, or signing out mid-sync (which discards the shell, and with it
# the controller that started the worker).
#
# So running workers are held here, independent of any screen, until they
# finish on their own. On quit, the app waits briefly for them.
# --------------------------------------------------------------------------

_live_workers: set = set()
_quit_hook_installed = False


def start_worker(worker: SyncWorker) -> None:
    """Start a worker and keep it alive until its thread has ended."""
    global _quit_hook_installed

    _live_workers.add(worker)
    worker.finished.connect(lambda: _live_workers.discard(worker))

    if not _quit_hook_installed:
        app = QCoreApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(wait_for_workers)
            _quit_hook_installed = True

    worker.start()


def wait_for_workers(timeout_ms: int = 4000) -> None:
    """Let in-flight syncs finish before the process exits.

    A sync is at most a few seconds of network work plus one SQLite
    transaction, and the transaction is atomic — so an interrupted one
    leaves the previous copy intact rather than a corrupt one.
    """
    for worker in list(_live_workers):
        worker.wait(timeout_ms)