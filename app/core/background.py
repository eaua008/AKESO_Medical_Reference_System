"""Run one blocking call (a Supabase request) off the UI thread.

    call_in_background(lambda: service.load(), on_done=show, on_error=warn)

on_done receives the call's return value; on_error receives a message.
Both run on the UI thread, so they may touch widgets: the worker's signals
go to a small receiver object that lives on the UI thread, which makes Qt
queue them there instead of calling back from the worker thread.

    result = wait_for(lambda: service.load())   # same, but returns the answer

wait_for keeps the window responsive while it waits (a local event loop),
for step-by-step code such as signing in.

Workers are kept alive by sync_worker.start_worker until their thread ends,
so closing a screen mid-request cannot crash the app.
"""

from typing import Any, Callable, Optional

from PySide6.QtCore import QEventLoop, QObject, QThread, Signal, Slot

from app.core.sync_worker import start_worker


class CallWorker(QThread):
    done = Signal(object)
    failed = Signal(str)

    def __init__(self, call: Callable[[], Any]) -> None:
        super().__init__()
        self._call = call

    def run(self) -> None:
        try:
            result = self._call()
        except Exception as exc:  # noqa: BLE001 - reported to the UI, never swallowed
            self.failed.emit(str(exc) or exc.__class__.__name__)
            return
        self.done.emit(result)


class _Receiver(QObject):
    """Lives on the UI thread; forwards results to plain Python callables."""

    def __init__(self, on_done, on_error, owner: Optional[QObject]) -> None:
        super().__init__()
        self._on_done = on_done
        self._on_error = on_error
        self._alive = True
        if owner is not None:
            owner.destroyed.connect(self._owner_gone)

    @Slot()
    def _owner_gone(self) -> None:
        self._alive = False

    @Slot(object)
    def deliver(self, result: Any) -> None:
        _receivers.discard(self)        # exactly one of deliver / fail runs
        if self._alive and self._on_done is not None:
            self._on_done(result)

    @Slot(str)
    def fail(self, message: str) -> None:
        _receivers.discard(self)
        if self._alive and self._on_error is not None:
            self._on_error(message)


_receivers: set = set()


class _WaitWorker(QThread):
    """Runs one call and keeps its result or its exception (not just a message)."""

    def __init__(self, call: Callable[[], Any]) -> None:
        super().__init__()
        self._call = call
        self.result: Any = None
        self.error: Optional[BaseException] = None

    def run(self) -> None:
        try:
            self.result = self._call()
        except BaseException as exc:  # noqa: BLE001 - re-raised on the UI thread
            self.error = exc


def wait_for(call: Callable[[], Any]) -> Any:
    """Run a blocking call on a worker thread and wait for it WITHOUT
    freezing the window. Returns its result, or raises the same exception
    the call raised.

    While it waits, a local event loop keeps the window painting and
    answering Windows, so it never shows "Not Responding". Like a dialog's
    exec(), clicks still arrive meanwhile: disable whatever must not be
    pressed twice before calling this.
    """
    worker = _WaitWorker(call)
    loop = QEventLoop()
    worker.finished.connect(loop.quit)
    start_worker(worker)
    if not worker.isFinished():
        loop.exec()
    # Quitting the app ends every event loop early; then wait for the call
    # itself (seconds at most) so the result is real.
    worker.wait()
    if worker.error is not None:
        raise worker.error
    return worker.result


def call_in_background(call: Callable[[], Any],
                       on_done: Optional[Callable[[Any], None]] = None,
                       on_error: Optional[Callable[[str], None]] = None,
                       owner: Optional[QObject] = None) -> CallWorker:
    """Start call on a worker thread.

    owner: when given, results are dropped once it has been deleted (for
    example a screen closed by signing out), instead of reaching a widget
    that no longer exists.
    """
    worker = CallWorker(call)
    receiver = _Receiver(on_done, on_error, owner)
    _receivers.add(receiver)
    worker.done.connect(receiver.deliver)
    worker.failed.connect(receiver.fail)
    start_worker(worker)
    return worker
