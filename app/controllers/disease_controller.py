"""Wires the encyclopedia grid to DiseaseService.

The only class that knows both DiseaseEncyclopediaView and DiseaseService
exist. Same shape as AuthController.

Note the network calls run on the UI thread, so the window will freeze
briefly during a refresh. Acceptable for a local desktop app against a small
table; worth moving to a worker thread if it becomes noticeable.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.repositories.supabase_disease_repository import DiseaseRepositoryError
from app.services.disease_service import DiseaseService
from app.ui.views.disease_encyclopedia_view import DiseaseEncyclopediaView


class DiseaseController(QObject):
    """Feeds the encyclopedia grid and handles what the user clicks."""

    inspect_requested = Signal(str)

    def __init__(
            self,
            view: DiseaseEncyclopediaView,
            service: Optional[DiseaseService] = None,
    ) -> None:
        super().__init__()
        self._view = view
        self._service = service or DiseaseService()

        view.filters_changed.connect(self._apply_filters)
        view.refresh_requested.connect(self.refresh)
        view.inspect_requested.connect(self.inspect_requested.emit)

        self.load()

    # ---------------------------------------------------------------- load

    def load(self) -> None:
        """Populate the filters, then draw the full list."""
        try:
            self._view.set_body_systems(self._service.body_systems())
            self._view.set_severities(self._service.severities())
            self._view.set_urgencies(self._service.urgencies())
            self._apply_filters()
        except DiseaseRepositoryError as exc:
            self._view.show_error(str(exc))

    def refresh(self) -> None:
        """Re-read from the database, picking up newly added conditions."""
        try:
            self._service.reload()
        except DiseaseRepositoryError as exc:
            self._view.show_error(str(exc))
            return
        self.load()

    # ------------------------------------------------------------- filters

    def _apply_filters(self) -> None:
        state = self._view.filter_state()
        try:
            results = self._service.search(**state)
            self._view.set_diseases(results, total=self._service.count())
        except DiseaseRepositoryError as exc:
            self._view.show_error(str(exc))