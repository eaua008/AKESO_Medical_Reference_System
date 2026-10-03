"""Wires the Wellness Calculators view to WellnessService.

Every panel follows the same contract: `changed` fires, the controller reads
values(), passes them to the matching calculator, and hands the result back
with show_result(). Adding a sixth calculator means one more line in _routes.
"""

from typing import Optional

from PySide6.QtCore import QObject

from app.services.wellness_calculators import WellnessService
from app.ui.views.wellness_view import WellnessView


class WellnessController(QObject):
    def __init__(self, view: WellnessView, service: Optional[WellnessService] = None) -> None:
        super().__init__()
        self._view = view
        self._service = service or WellnessService()

        view.converter.set_conversions(self._service.converter.conversions)

        # panel -> function that turns its values() into a result
        self._routes = (
            (view.bmi, lambda v: self._service.bmi.calculate(**v)),
            (view.hydration, lambda v: self._service.hydration.calculate(**v)),
            (view.sleep, lambda v: self._service.sleep.recommend(**v)),
            (view.energy, lambda v: self._service.energy.calculate(**v)),
            (view.converter, lambda v: self._service.converter.convert(**v)),
        )
        for panel, calculate in self._routes:
            panel.changed.connect(lambda p=panel, c=calculate: self._recalculate(p, c))
            self._recalculate(panel, calculate)   # fill every panel on first show

    @staticmethod
    def _recalculate(panel, calculate) -> None:
        panel.show_result(calculate(panel.values()))