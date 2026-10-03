"""Medicine Reference page: the catalogue, and the monograph, which slides
in over it in the shell's sheet (stacked if there is none)."""

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
        self._sheet = None

    def attach_sheet(self, sheet) -> None:
        self._sheet = sheet
        self.removeWidget(self.monograph)
        sheet.adopt(self.monograph, self.monograph.back_requested)

    def show_catalog(self) -> None:
        if self._sheet is not None:
            self._sheet.close_sheet()
        self.setCurrentWidget(self.catalog)

    def show_detail(self, medicine: MedicineMonograph) -> None:
        self._current = medicine
        self.monograph.show_medicine(medicine)
        if self._sheet is not None:
            self._sheet.open_sheet()
        else:
            self.setCurrentWidget(self.monograph)

    def refresh_theme(self) -> None:
        """Called by the shell on theme change: redraw painted icons."""
        self.catalog.refresh_theme()
        if self._current is not None:
            self.monograph.show_medicine(self._current)