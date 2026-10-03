"""Wires the Emergency Guide view to EmergencyService.

The view announces "the filter text changed"; the service decides what
matches; this class passes one to the other. Neither side knows the other
exists.
"""

from typing import Optional

from PySide6.QtCore import QObject

from app.repositories.emergency_repository import EmergencyDataError
from app.services.emergency_service import EmergencyService
from app.ui.views.emergency_guide_view import EmergencyGuideView


class EmergencyController(QObject):
    """Feeds the guide into the view and handles filtering."""

    def __init__(
            self,
            view: EmergencyGuideView,
            service: Optional[EmergencyService] = None,
    ) -> None:
        super().__init__()
        self._view = view
        self._service = service or EmergencyService()

        self._view.filter_changed.connect(self._apply_filter)
        self.load()

    def load(self) -> None:
        try:
            guide = self._service.guide()
        except EmergencyDataError as exc:
            # The hotline 911 still has to be reachable, so the view shows
            # it even when the data file is broken.
            self._view.show_error(str(exc))
            return
        self._view.set_guide(guide)
        self._view.show_protocols(self._service.protocols())

    def _apply_filter(self, text: str) -> None:
        try:
            self._view.show_protocols(self._service.filter(text))
        except EmergencyDataError as exc:
            self._view.show_error(str(exc))