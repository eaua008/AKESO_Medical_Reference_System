"""Wires the Medicine Reference page to MedicineService.

Loads the local copy, starts a background sync, reloads when newer content
arrives. Same flow as the other modules, reusing SyncWorker.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.core.sync_worker import SyncWorker, start_worker
from app.services.medicine_service import MedicineService
from app.ui.views.medicine_reference_page import MedicineReferencePage


class MedicineController(QObject):
    # Re-emitted for the shell, which owns navigation between modules.
    condition_chosen = Signal(str)   # open this disease
    case_requested = Signal(str)     # "Present Case" in peer discussions

    def __init__(self, page: MedicineReferencePage,
                 service: Optional[MedicineService] = None) -> None:
        super().__init__()
        self._page = page
        self._service = service or MedicineService()
        self._filters = ("", "", "all")

        page.catalog.filters_changed.connect(self._on_filters)
        page.catalog.medicine_chosen.connect(self.inspect)
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
            self._page.catalog.show_status("Downloading the medicine reference\u2026")

    def start_sync(self, force: bool = False) -> None:
        worker = SyncWorker(self._service, force=force)
        worker.sync_finished.connect(self._on_synced)
        start_worker(worker)

    def _on_synced(self, changed: bool, error: str) -> None:
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