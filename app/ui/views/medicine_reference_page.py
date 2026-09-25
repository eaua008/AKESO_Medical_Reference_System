"""Medicine Reference page: catalogue and monograph, stacked."""

from typing import Optional

from PySide6.QtWidgets import QStackedWidget

from app.models.medicine import MedicineMonograph
from app.ui.views.medicine_catalog_view import MedicineCatalogView
from app.ui.views.medicine_monograph_view import MedicineMonographView


class MedicineReferencePage(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.catalog = MedicineCatalogView()
        self.monograph = MedicineMonographView()
        self.addWidget(self.catalog)
        self.addWidget(self.monograph)
        self.monograph.back_requested.connect(self.show_catalog)
        self._current: Optional[MedicineMonograph] = None

    def show_catalog(self) -> None:
        self.setCurrentWidget(self.catalog)

    def show_detail(self, medicine: MedicineMonograph) -> None:
        self._current = medicine
        self.monograph.show_medicine(medicine)
        self.setCurrentWidget(self.monograph)

    def refresh_theme(self) -> None:
        """Called by the shell on theme change: redraw painted icons."""
        self.catalog.refresh_theme()
        if self._current is not None:
            self.monograph.show_medicine(self._current)