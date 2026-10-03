"""Symptom Encyclopedia page: the browse screen, and the detail screen,
which slides in over it in the shell's sheet (stacked if there is none)."""

from typing import Optional

from PySide6.QtWidgets import QStackedWidget

from app.models.symptom import Symptom
from app.ui.views.symptom_browse_view import SymptomBrowseView
from app.ui.views.symptom_detail_view import SymptomDetailView


class SymptomEncyclopediaPage(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.browse = SymptomBrowseView()
        self.detail = SymptomDetailView()
        self.addWidget(self.browse)
        self.addWidget(self.detail)
        self.detail.back_requested.connect(self.show_browse)
        self._current: Optional[Symptom] = None
        self._sheet = None

    def attach_sheet(self, sheet) -> None:
        self._sheet = sheet
        self.removeWidget(self.detail)
        sheet.adopt(self.detail, self.detail.back_requested)

    def show_browse(self) -> None:
        if self._sheet is not None:
            self._sheet.close_sheet()
        self.setCurrentWidget(self.browse)

    def show_detail(self, symptom: Symptom) -> None:
        self._current = symptom
        self.detail.show_symptom(symptom)
        if self._sheet is not None:
            self._sheet.open_sheet()
        else:
            self.setCurrentWidget(self.detail)

    def refresh_theme(self) -> None:
        """Called by the shell on theme change: redraw painted icons."""
        self.browse.refresh_theme()
        if self._current is not None:
            self.detail.show_symptom(self._current)