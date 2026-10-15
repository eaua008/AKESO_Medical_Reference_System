"""Wires the Medicine Reference page to MedicineService.

Loads the local copy, starts a background sync, reloads when newer content
arrives. Same flow as the other modules, reusing SyncWorker.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.core.sync_worker import SyncWorker, start_worker
from app.services.medicine_service import MedicineService
from app.ui.components.akeso_loader import MinimumLoading
from app.ui.views.medicine_reference_page import MedicineReferencePage


class MedicineController(QObject):
    # Re-emitted for the shell, which owns navigation between modules.
    condition_chosen = Signal(str)   # open this disease
    case_requested = Signal(str)     # "Present Case" in peer discussions
    opened = Signal(str)             # a monograph was shown (study activity)

    def __init__(self, page: MedicineReferencePage,
                 service: Optional[MedicineService] = None) -> None:
        super().__init__()
        self._page = page
        self._service = service or MedicineService()
        self._filters = ("", "", "all")
        self._syncing = False
        self._refresh = MinimumLoading(page.catalog, "Refreshing the medicine reference\u2026")

        page.catalog.filters_changed.connect(self._on_filters)
        page.catalog.medicine_chosen.connect(self.inspect)
        page.catalog.refresh_requested.connect(self.refresh)
        page.monograph.condition_chosen.connect(self.condition_chosen.emit)
        page.monograph.case_requested.connect(self.case_requested.emit)

        self.load()
        self.start_sync()

    def load(self) -> None:
        """Show whatever the local copy holds (may be empty on first run)."""
        self._service.reload()
        self._page.catalog.set_regulatory_classes(self._service.regulatory_classes())
        self._apply()
        if not self._service.has_local_copy():
            self._page.catalog.show_loading("Downloading the medicine reference\u2026")

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
        if self._refresh.active:
            note = ("Couldn't reach the server. Showing the copy saved on this computer."
                    if error and not changed else "")
            self._refresh.finish(then=self.load if changed else None, message=note)
            return
        if changed:
            self.load()
        elif error and not self._service.has_local_copy():
            self._page.catalog.show_status(
                "Couldn't download the medicine reference. Check your connection "
                f"and reopen the app.\n({error})")

    def _on_filters(self, query: str, regulatory_class: str, scope: str) -> None:
        self._filters = (query, regulatory_class, scope)
        self._apply()

    def _apply(self) -> None:
        results = self._service.search(*self._filters)
        self._page.catalog.show_medicines(results, total=len(self._service.all_medicines()))

    def inspect(self, medicine_id: str) -> None:
        """Open one monograph. Also used by global search."""
        medicine = self._service.get(medicine_id)
        if medicine is not None:
            self._page.show_detail(medicine)
            self.opened.emit(medicine_id)
