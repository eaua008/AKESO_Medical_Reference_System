"""Wires the encyclopedia module to DiseaseService.

Loading follows a pattern called stale-while-revalidate:

    1. Show the local copy immediately — no network, so it is instant.
    2. Check Supabase for changes on a background thread.
    3. Only if something changed, reload and redraw.

On a normal startup with nothing new, step 2 is one tiny request and the
screen never redraws. The very first run on a machine has no local copy, so
it shows a download message until the first sync lands.

The encyclopedia keeps working offline: a failed sync leaves the last
downloaded copy serving every screen.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.core.sync_worker import SyncWorker, start_worker
from app.repositories.supabase_disease_repository import DiseaseRepositoryError
from app.services import comparison as comparison_service
from app.services.disease_service import DiseaseService
from app.ui.views.encyclopedia_page import EncyclopediaPage


class DiseaseController(QObject):
    """Feeds the encyclopedia screens and keeps their data current."""

    check_symptoms_requested = Signal(str)
    opened = Signal(str)       # a monograph was shown (study activity)

    def __init__(
            self,
            page: EncyclopediaPage,
            service: Optional[DiseaseService] = None,
    ) -> None:
        super().__init__()
        self._page = page
        self._grid = page.grid_view
        self._compare = page.compare_view
        self._detail = page.detail_view
        self._service = service or DiseaseService()
        self._syncing = False

        self._grid.filters_changed.connect(self._apply_filters)
        self._grid.refresh_requested.connect(self.refresh)
        self._grid.inspect_requested.connect(self.inspect)

        self._compare.selection_changed.connect(self._run_comparison)
        self._compare.monograph_requested.connect(self.inspect)

        self._detail.back_requested.connect(self._page.close_detail)
        self._detail.check_symptoms_requested.connect(
            self.check_symptoms_requested.emit
        )

        self.load()        # step 1: local copy, instant
        self.start_sync()  # step 2: check for changes in the background

    # ---------------------------------------------------------------- load

    def load(self) -> None:
        """Draw everything from the local copy."""
        if not self._service.has_local_copy():
            message = (
                "Downloading the encyclopedia for offline use\u2026 This only "
                "happens the first time on this machine."
            )
            self._grid.show_error(message)
            self._compare.show_message(message)
            return

        try:
            self._grid.set_body_systems(self._service.body_systems())
            self._grid.set_severities(self._service.severities())
            self._grid.set_urgencies(self._service.urgencies())
            self._compare.set_conditions(self._service.all_diseases())
            self._apply_filters()
        except DiseaseRepositoryError as exc:
            self._grid.show_error(str(exc))
            self._compare.show_message(str(exc))

    # ---------------------------------------------------------------- sync

    def start_sync(self, force: bool = False) -> None:
        """Check Supabase for changes without blocking the window."""
        if self._syncing:
            return  # one sync at a time; a second click does nothing
        self._syncing = True

        worker = SyncWorker(self._service, force=force)
        worker.sync_finished.connect(self._on_synced)
        start_worker(worker)

    def _on_synced(self, changed: bool, error: str) -> None:
        self._syncing = False

        if changed:
            # A newer copy is on disk. Pull it into memory and redraw. Search
            # shares this service, so it sees the new data automatically.
            self._service.reload()
            self.load()
            return

        if error and not self._service.has_local_copy():
            # First run AND offline: nothing downloaded, nothing to show.
            # With a local copy, a failed sync is silent — the app simply
            # keeps using what it has.
            message = (
                "Could not download the encyclopedia. Check your internet "
                "connection, then press Refresh."
            )
            self._grid.show_error(message)
            self._compare.show_message(message)

    def refresh(self) -> None:
        """The Refresh button: force a full download.

        Forced rather than version-checked. When someone explicitly asks for
        fresh data, one full pull (about 11 requests) is a fair price, and it
        also recovers from any edit made to a table the version triggers do
        not cover.
        """
        self.start_sync(force=True)

    # ------------------------------------------------------------- filters

    def _apply_filters(self) -> None:
        state = self._grid.filter_state()
        results = self._service.search(**state)
        total = self._service.count()
        self._grid.set_diseases(results, total=total)
        self._page.set_count(len(results), total)

    # -------------------------------------------------------------- detail

    def inspect(self, disease_id: str) -> None:
        """Open a monograph. Already fully hydrated locally, so it is instant."""
        disease = self._service.get(disease_id)

        if disease is None:
            self._page.show_detail()
            self._detail.show_error(f"No monograph found for '{disease_id}'.")
            return

        self._detail.show_disease(disease)
        self._page.show_detail()
        self.opened.emit(disease_id)

    # ----------------------------------------------------------- comparison

    def _run_comparison(self) -> None:
        ids = self._compare.selected_ids()
        if len(ids) < 2:
            self._compare.show_message("Select two conditions to compare.")
            return

        diseases = [d for d in (self._service.get(i) for i in ids) if d is not None]
        if len(diseases) < 2:
            self._compare.show_message("Could not load enough conditions to compare.")
            return

        self._compare.show_comparison(comparison_service.compare(diseases))