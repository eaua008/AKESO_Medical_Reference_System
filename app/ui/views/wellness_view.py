"""Wellness Calculators page: header, tab row, and one panel per calculator.

Like the Emergency Guide, the page lives in its own QScrollArea, so only the
main content scrolls and the shell's header and sidebar stay fixed.
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.ui.views.wellness_panels import (
    BmiPanel,
    ConverterPanel,
    EnergyPanel,
    HydrationPanel,
    SleepPanel,
)


class WellnessView(QWidget):
    """Hosts the five calculator panels."""

    TABS = (
        ("bmi", "Body Mass Index"),
        ("hydration", "Hydration"),
        ("sleep", "Sleep"),
        ("energy", "BMR && Energy"),   # "&&" shows one "&"; a single "&" marks a shortcut key
        ("converter", "Unit Converter"),
    )

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")

        # Public so the controller can connect to each one.
        self.bmi = BmiPanel()
        self.hydration = HydrationPanel()
        self.sleep = SleepPanel()
        self.energy = EnergyPanel()
        self.converter = ConverterPanel()
        panels = {
            "bmi": self.bmi, "hydration": self.hydration, "sleep": self.sleep,
            "energy": self.energy, "converter": self.converter,
        }

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        page = QWidget()
        page.setObjectName("panel")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 22, 30, 30)
        layout.setSpacing(18)

        layout.addWidget(self._build_header())

        tab_row = QWidget()
        tab_row.setObjectName("wlTabRow")
        tabs = QHBoxLayout(tab_row)
        tabs.setContentsMargins(0, 0, 0, 0)
        tabs.setSpacing(4)
        self._tab_group = QButtonGroup(self)
        self._tab_group.setExclusive(True)

        self.stack = QStackedWidget()
        self.stack.setObjectName("panel")
        for tab_id, text in self.TABS:
            button = QPushButton(text)
            button.setObjectName("wlTab")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self._tab_group.addButton(button)
            tabs.addWidget(button)
            index = self.stack.addWidget(panels[tab_id])
            button.clicked.connect(lambda _c=False, i=index: self.stack.setCurrentIndex(i))
            if index == 0:
                button.setChecked(True)
        tabs.addStretch(1)

        layout.addWidget(tab_row)
        layout.addWidget(self.stack)
        layout.addWidget(QLabel(
            "Screening estimates for study and self-checks, not a diagnosis.",
            objectName="wlSource",
        ))
        layout.addStretch(1)

        scroll.setWidget(page)
        root.addWidget(scroll)

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("panel")
        layout = QVBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        row = QHBoxLayout()
        row.setSpacing(10)
        self._icon = QLabel()
        self._icon.setObjectName("panel")
        self._icon.setFixedSize(24, 24)
        row.addWidget(self._icon)
        title = QLabel("Wellness Calculators")
        title.setObjectName("pageTitle")
        row.addWidget(title)
        row.addStretch(1)
        layout.addLayout(row)

        subtitle = QLabel(
            "BMI with Philippine cutoffs, daily water, sleep, energy needs, and "
            "clinical unit conversion."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        self.refresh_theme()
        return header

    def refresh_theme(self) -> None:
        self._icon.setPixmap(icons.to_pixmap(icons.draw("calculator", 24, Theme.token("PRIMARY"))))
        # The BMI gauge paints with theme colours, so it needs a repaint.
        self.bmi.gauge.update()