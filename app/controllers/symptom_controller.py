"""Wires the Symptom Encyclopedia page to SymptomService.

Load the local copy right away, start a background sync, and reload when the
sync reports newer content. The same flow as DiseaseController, reusing its
SyncWorker.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.core.sync_worker import SyncWorker, start_worker
from app.services.symptom_service import SymptomService
from app.ui.components.akeso_loader import MinimumLoading
from app.ui.views.symptom_encyclopedia_page import SymptomEncyclopediaPage


class SymptomController(QObject):
    # Re-emitted for the shell, which owns navigation between modules.
    condition_chosen = Signal(str)     # open this disease
    session_requested = Signal(str)    # "Add to Active Session" / correlation
    matching_requested = Signal(str)   # "Find Matching Diseases"
    case_requested = Signal(str)       # "Present Case"
    opened = Signal(str)               # an entry was shown (study activity)
    synced = Signal(bool, str)         # a sync ended: (changed, error); the checker listens

    def __init__(self, page: SymptomEncyclopediaPage,
                 service: Optional[SymptomService] = None) -> None:
        super().__init__()
        self._page = page
        self._service = service or SymptomService()
        self._filters = ("", "", False)
        self._syncing = False
        self._refresh = MinimumLoading(page.browse, "Refreshing the symptom encyclopedia\u2026")

        page.browse.filters_changed.connect(self._on_filters)
        page.browse.symptom_chosen.connect(self.inspect)
        page.browse.refresh_requested.connect(self.refresh)
        page.detail.condition_chosen.connect(self.condition_chosen.emit)
        page.detail.session_requested.connect(self.session_requested.emit)
        page.detail.matching_requested.connect(self.matching_requested.emit)
        page.detail.case_requested.connect(self.case_requested.emit)

        self.load()
        self.start_sync()

    def load(self) -> None:
        """Show whatever the local copy holds (may be empty on first run)."""
        self._service.reload()
        self._page.browse.set_body_systems(self._service.body_systems())
        self._page.browse.set_tiers(self._service.tiers())
        self._apply()
        if not self._service.has_local_copy():
            self._page.browse.show_loading("Downloading the symptom encyclopedia\u2026")

    def refresh(self) -> None:
        """The Refresh button: download everything again, with the Akeso
        loader over the page for at least 10 seconds."""
        if self._syncing:
            return
        self._refresh.begin()
        self.start_sync(force=True)

    def start_sync(self, force: bool = False) -> None:
        if self._syncing:
            return
        self._syncing = True
        worker = SyncWorker(self._service, force=force)
        worker.sync_finished.connect(self._on_synced)
        start_worker(worker)

    def _on_synced(self, changed: bool, error: str) -> None:
        self._syncing = False
        def done() -> None:
            if changed:
                self.load()
            self.synced.emit(changed, error)

        if self._refresh.active:
            note = ("Couldn't reach the server. Showing the copy saved on this computer."
                    if error and not changed else "")
            self._refresh.finish(then=done, message=note)
            return
        done()
        if not changed and error and not self._service.has_local_copy():
            self._page.browse.show_status(
                "Couldn't download the symptom encyclopedia. Check your "
                f"connection and reopen the app.\n({error})")

    def _on_filters(self, query: str, system_id: str, tier_key: str) -> None:
        self._filters = (query, system_id, tier_key)
        self._apply()

    def _apply(self) -> None:
        results = self._service.search(*self._filters)
        self._page.browse.show_symptoms(results, total=len(self._service.all_symptoms()))

    def inspect(self, symptom_id: str) -> None:
        """Open one entry. Also used by global search."""
        symptom = self._service.get(symptom_id)
        if symptom is not None:
            self._page.show_detail(symptom)
            self.opened.emit(symptom_id)
