"""Wires the encyclopedia module to DiseaseService.

The only class that knows both the views and the service exist. It now owns
navigation between the grid and the detail page, since deciding which screen
to show after an action is coordination, not display.

Network calls run on the UI thread, so the window pauses briefly while a
monograph loads. Fine against a small table on a desktop app; worth moving
to a worker thread if it becomes noticeable.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.repositories.supabase_disease_repository import DiseaseRepositoryError
from app.services.disease_service import DiseaseService
from app.ui.views.encyclopedia_page import EncyclopediaPage


class DiseaseController(QObject):
    """Feeds the encyclopedia screens and handles what the user clicks."""

    check_symptoms_requested = Signal(str)

    def __init__(
            self,
            page: EncyclopediaPage,
            service: Optional[DiseaseService] = None,
    ) -> None:
        super().__init__()
        self._page = page
        self._grid = page.grid_view
        self._detail = page.detail_view
        self._service = service or DiseaseService()

        self._grid.filters_changed.connect(self._apply_filters)
        self._grid.refresh_requested.connect(self.refresh)
        self._grid.inspect_requested.connect(self.inspect)

        self._detail.back_requested.connect(self._page.show_grid)
        self._detail.check_symptoms_requested.connect(
            self.check_symptoms_requested.emit
        )

        self.load()

    # ---------------------------------------------------------------- load

    def load(self) -> None:
        """Populate the filters, then draw the full list."""
        try:
            self._grid.set_body_systems(self._service.body_systems())
            self._grid.set_severities(self._service.severities())
            self._grid.set_urgencies(self._service.urgencies())
            self._apply_filters()
        except DiseaseRepositoryError as exc:
            self._grid.show_error(str(exc))

    def refresh(self) -> None:
        """Re-read from the database, picking up newly added conditions."""
        try:
            self._service.reload()
        except DiseaseRepositoryError as exc:
            self._grid.show_error(str(exc))
            return
        self.load()

    # ------------------------------------------------------------- filters

    def _apply_filters(self) -> None:
        state = self._grid.filter_state()
        try:
            results = self._service.search(**state)
            self._grid.set_diseases(results, total=self._service.count())
        except DiseaseRepositoryError as exc:
            self._grid.show_error(str(exc))

    # -------------------------------------------------------------- detail

    def inspect(self, disease_id: str) -> None:
        """Load the full monograph and switch to the detail page.

        The grid holds light objects — scalar fields only — so this fetches
        the child tables before rendering. Switching screens first would
        show an empty page during the round trip.
        """
        try:
            disease = self._service.get(disease_id)
        except DiseaseRepositoryError as exc:
            self._page.show_detail()
            self._detail.show_error(str(exc))
            return

        if disease is None:
            self._page.show_detail()
            self._detail.show_error(
                f"No monograph found for '{disease_id}'."
            )
            return

        self._detail.show_disease(disease)
        self._page.show_detail()