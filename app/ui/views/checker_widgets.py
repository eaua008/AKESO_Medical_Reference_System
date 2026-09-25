"""Widgets for the Symptom Correlation Engine.

Two things worth knowing:

* The severity control changes with the symptom. A 0-10 NRS rating is a pain
  instrument, so it only appears for symptoms that really are a pain (joint
  stiffness, chest pain, cramping). Fever, cough or a rash get a plain
  intensity slider instead: asking someone to rate a temperature on a pain
  scale means nothing.

* The parameter cards sit in their own scroll area in the view, so adding a
  fifth symptom scrolls that column instead of stretching the whole page.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.models.checker import (
    DURATIONS,
    ONSETS,
    PATTERNS,
    TRENDS,
    SelectedSymptom,
)
from app.models.symptom import Symptom

PAIN_WORDS = {
    0: "No pain", 1: "Barely noticeable", 2: "Mild", 3: "Mild",
    4: "Uncomfortable", 5: "Moderate", 6: "Moderate",
    7: "Severe", 8: "Severe pain", 9: "Very severe", 10: "Worst imaginable",
}
PAIN_PRESENTATION = {
    0: "No pain reported.",
    3: "Noticeable but does not interfere with activity.",
    5: "Interferes with some activity; still tolerable.",
    7: "Limits most activity and concentration.",
    8: "Intense, dominating pain that limits movement or posture.",
    10: "Incapacitating; unable to move or speak through it.",
}
INTENSITY_WORDS = {
    0: "Absent", 1: "Trace", 2: "Very mild", 3: "Mild", 4: "Mild to moderate",
    5: "Moderate", 6: "Moderate", 7: "Marked", 8: "Severe", 9: "Very severe",
    10: "Extreme",
}


def _label(text: str, name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(name)
    label.setWordWrap(wrap)
    return label


def _card(title: str = "", icon_name: str = "", danger: bool = False,
          trailing: str = "") -> tuple[QFrame, QVBoxLayout]:
    card = QFrame()
    card.setObjectName("ccRedCard" if danger else "ccCard")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 12, 16, 14)
    layout.setSpacing(9)
    if title:
        row = QHBoxLayout()
        row.setSpacing(8)
        if icon_name:
            badge = QLabel()
            badge.setObjectName("panel")
            badge.setFixedSize(15, 15)
            badge.setPixmap(icons.to_pixmap(icons.draw(
                icon_name, 15, Theme.token("DANGER" if danger else "BADGE_TEXT"))))
            row.addWidget(badge)
        row.addWidget(_label(title.upper(), "ccRedHeading" if danger else "ccHeading",
                             wrap=False))
        row.addStretch(1)
        if trailing:
            row.addWidget(_label(trailing, "ccCardNote", wrap=False))
        layout.addLayout(row)
    return card, layout


def _combo(options, current: str = "") -> QComboBox:
    combo = QComboBox()
    combo.setObjectName("ccCombo")
    for key, text in options:
        combo.addItem(text, key)
    if current:
        combo.setCurrentIndex(max(combo.findData(current), 0))
    return combo


class SymptomRow(QFrame):
    """One selectable symptom in the left-hand list."""

    toggled_symptom = Signal(str, bool)

    def __init__(self, symptom: Symptom, selected: bool) -> None:
        super().__init__()
        self.setObjectName("ccSymptomRow")
        self.setProperty("selected", selected)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = symptom.id

        row = QHBoxLayout(self)
        row.setContentsMargins(12, 8, 12, 8)
        row.setSpacing(10)

        text = QVBoxLayout()
        text.setSpacing(1)
        text.addWidget(_label(symptom.name, "ccSymptomName", wrap=False))
        tags = ", ".join(symptom.tags[:2]) if symptom.tags else symptom.system_label
        text.addWidget(_label(f"Weight {symptom.diagnostic_weight}/10 \u00b7 {tags}",
                              "ccSymptomMeta", wrap=False))
        row.addLayout(text, 1)

        self.box = QCheckBox()
        self.box.setChecked(selected)
        self.box.toggled.connect(lambda state: self.toggled_symptom.emit(self._id, state))
        row.addWidget(self.box)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.box.toggle()
        super().mouseReleaseEvent(event)


class SuggestionChip(QPushButton):
    """An associated symptom worth adding, with how many conditions want it."""

    def __init__(self, symptom_id: str, name: str, conditions: int) -> None:
        super().__init__()
        self.setObjectName("ccSuggestChip")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.symptom_id = symptom_id
        self.setText(f"+   {name}    {conditions} condition"
                     f"{'s' if conditions != 1 else ''}")
        self.setToolTip(f"Also reported in {conditions} of the conditions "
                        "matching so far")


class SymptomParameters(QFrame):
    """Severity, onset, pattern, trend and duration for one chosen symptom."""

    changed = Signal()
    removed = Signal(str)

    def __init__(self, entry: SelectedSymptom, is_pain: bool) -> None:
        super().__init__()
        self.setObjectName("ccParamCard")
        self.symptom_id = entry.symptom_id
        self.name = entry.name
        self._is_pain = is_pain
        self._intensity = entry.intensity
        self._slider: Optional[QSlider] = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 14)
        layout.setSpacing(10)

        head = QHBoxLayout()
        head.setSpacing(8)
        head.addWidget(_label("\u25cf", "ccDot", wrap=False))
        head.addWidget(_label(entry.name, "ccParamTitle", wrap=False))
        head.addStretch(1)
        remove = QPushButton("Remove")
        remove.setObjectName("ccRemove")
        remove.setCursor(Qt.CursorShape.PointingHandCursor)
        remove.clicked.connect(lambda: self.removed.emit(self.symptom_id))
        head.addWidget(remove)
        layout.addLayout(head)

        layout.addWidget(self._build_pain_scale() if is_pain else self._build_slider())

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(4)
        self.onset = _combo(ONSETS, entry.onset)
        self.pattern = _combo(PATTERNS, entry.pattern)
        self.trend = _combo(TRENDS, entry.trend)
        self.duration = _combo(DURATIONS, entry.duration)
        for column, (caption, widget) in enumerate((
                ("Onset", self.onset), ("Pattern", self.pattern),
                ("Trend", self.trend), ("Duration", self.duration))):
            grid.addWidget(_label(caption.upper(), "ccFieldLabel", wrap=False), 0, column)
            grid.addWidget(widget, 1, column)
            grid.setColumnStretch(column, 1)
            widget.currentIndexChanged.connect(lambda _i: self.changed.emit())
        layout.addLayout(grid)

    # --------------------------------------------------- severity controls

    def _build_slider(self) -> QWidget:
        box = QFrame()
        box.setObjectName("ccIntensityBox")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 9, 12, 10)
        layout.setSpacing(6)

        head = QHBoxLayout()
        head.addWidget(_label("SYMPTOM INTENSITY LEVEL", "ccFieldLabel", wrap=False))
        head.addStretch(1)
        self._reading = _label("", "ccIntensityValue", wrap=False)
        head.addWidget(self._reading)
        layout.addLayout(head)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setObjectName("ccSlider")
        self._slider.setRange(0, 10)
        self._slider.setValue(self._intensity)
        self._slider.valueChanged.connect(self._set_intensity)
        layout.addWidget(self._slider)
        self._update_reading()
        return box

    def _build_pain_scale(self) -> QWidget:
        box = QFrame()
        box.setObjectName("ccPainBox")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 9, 12, 10)
        layout.setSpacing(8)

        head = QHBoxLayout()
        head.addWidget(_label("PAIN / SEVERITY SCALE: NRS (0\u201310 RATING BOXES)",
                              "ccPainLabel", wrap=False))
        head.addStretch(1)
        self._reading = _label("", "ccPainBadge", wrap=False)
        head.addWidget(self._reading)
        layout.addLayout(head)

        scale = QHBoxLayout()
        scale.setSpacing(4)
        self._scale_group = QButtonGroup(self)
        self._scale_group.setExclusive(True)
        for value in range(11):
            button = QPushButton(str(value))
            button.setObjectName("ccScaleButton")
            button.setCheckable(True)
            button.setChecked(value == self._intensity)
            button.setFixedHeight(30)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _c=False, v=value: self._set_intensity(v))
            self._scale_group.addButton(button, value)
            scale.addWidget(button)
        layout.addLayout(scale)

        self._presentation = _label("", "ccPresentation")
        layout.addWidget(self._presentation)
        self._update_reading()
        return box

    def _set_intensity(self, value: int) -> None:
        self._intensity = value
        if self._is_pain:
            button = self._scale_group.button(value)
            if button is not None and not button.isChecked():
                button.setChecked(True)
        elif self._slider is not None and self._slider.value() != value:
            self._slider.setValue(value)
        self._update_reading()
        self.changed.emit()

    def _update_reading(self) -> None:
        value = self._intensity
        if self._is_pain:
            self._reading.setText(f"{value}/10 \u2014 {PAIN_WORDS[value]}")
            closest = max(k for k in PAIN_PRESENTATION if k <= value)
            self._presentation.setText(
                f"Clinical presentation: {PAIN_PRESENTATION[closest]}")
        else:
            self._reading.setText(f"{value} / 10 ({INTENSITY_WORDS[value]})")
        level = "high" if value >= 8 else "mid" if value >= 5 else "low"
        self._reading.setProperty("level", level)
        self._reading.style().unpolish(self._reading)
        self._reading.style().polish(self._reading)

    def value(self) -> SelectedSymptom:
        return SelectedSymptom(
            symptom_id=self.symptom_id, name=self.name, intensity=self._intensity,
            onset=self.onset.currentData(), pattern=self.pattern.currentData(),
            trend=self.trend.currentData(), duration=self.duration.currentData())