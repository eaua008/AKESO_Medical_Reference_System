"""When Study Hub syncs, and what its status chip says.

    opening Study Hub            a round straight away
    every 5 minutes while open   a round
    after a review session       a round (reviews are held back while you
                                 review, so Undo can still take one back)
    back online                  after a failed round, it tries again every
                                 minute until one works

Offline, Study Hub keeps working from this computer; nothing is lost,
because unsent changes stay marked until an upload succeeds.
"""

from datetime import datetime
from typing import Callable, Optional

from PySide6.QtCore import QObject, QTimer

from app.core.background import call_in_background
from app.repositories.supabase_study_repository import StudyNotInstalled
from app.services.study.study_sync import StudySync, StudySyncResult

EVERY_MS = 5 * 60_000
RETRY_MS = 60_000


class StudySyncController(QObject):
    def __init__(self, sync: StudySync, set_status: Callable[[str, str], None],
                 on_changed: Callable[[], None], parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._sync = sync
        self._set_status = set_status          # (text, tone) for the chip
        self._on_changed = on_changed          # redraw Study Hub after a download
        self._running = False
        self._disabled = False
        self.reviewing = False                 # a session is on: hold reviews back
        self._last_ok: Optional[datetime] = None
        self._timer = QTimer(self)
        self._timer.setInterval(EVERY_MS)
        self._timer.timeout.connect(self.sync_now)
        self._retry = QTimer(self)
        self._retry.setSingleShot(True)
        self._retry.setInterval(RETRY_MS)
        self._retry.timeout.connect(self.sync_now)
        self._clock = QTimer(self)
        self._clock.setInterval(30_000)
        self._clock.timeout.connect(self._show_ok)
        self._clock.start()

    def hub_opened(self) -> None:
        self.sync_now()
        self._timer.start()

    def hub_closed(self) -> None:
        self._timer.stop()

    def sync_now(self) -> None:
        if self._running or self._disabled:
            return
        self._running = True
        self._set_status("Syncing…", "")
        push = not self.reviewing
        call_in_background(lambda: self._sync.sync(push_reviews=push), self._done, self._failed, owner=self)

    def _done(self, result: StudySyncResult) -> None:
        self._running = False
        self._last_ok = datetime.now()
        if result.changed_here:
            self._on_changed()
        self._show_ok()

    def _failed(self, message: str) -> None:
        self._running = False
        if "050_study_hub" in message:
            self._disabled = True
            self._set_status("On this computer only", "warn")
            return
        self._set_status("Offline", "warn")
        self._retry.start()

    def _show_ok(self) -> None:
        if self._last_ok is None or self._running or self._disabled:
            return
        pending = self._sync.has_local_changes()
        self._set_status("Synced · changes waiting" if pending else "Synced", "good")

    def shutdown(self) -> None:
        for timer in (self._timer, self._retry, self._clock):
            timer.stop()

    @staticmethod
    def not_installed(error: Exception) -> bool:
        return isinstance(error, StudyNotInstalled)
