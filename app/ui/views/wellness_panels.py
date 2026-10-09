"""The five calculator panels and the small widgets they share.

Panels are display only. Each one:
    - emits `changed` whenever any input moves,
    - returns its inputs from values() as a plain dict,
    - draws whatever result object it's handed in show_result().

WellnessController connects the two ends. No arithmetic happens in this file
apart from converting slider positions, which are integers.
"""

from typing import Optional

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPolygonF
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from app.core.theme import Theme
from app.services.wellness_calculators import (
    ACTIVITY_LEVELS,
    BmiResult,
    Conversion,
    ConversionResult,
    EnergyResult,
    HydrationResult,
    SleepResult,
)
from app.ui.views.compare_view import FlowLayout

AMBER = "#F59E0B"


def _label(text: str, name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(name)
    label.setWordWrap(wrap)
    return label


def _repolish(widget: QWidget) -> None:
    """Re-read property selectors such as [tone="good"] after a change."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def _panel_widget() -> QWidget:
    widget = QWidget()
    widget.setObjectName("panel")
    return widget


# ============================================================ shared inputs

class NumberField(QWidget):
    """A labelled number box, optionally with a slider kept in sync.

    The box allows exact typing; the slider allows quick exploration. The
    slider is integer-only, so it stores value x 10^decimals.
    """

    valueChanged = Signal(float)

    def __init__(
            self,
            title: str,
            minimum: float,
            maximum: float,
            value: float,
            unit: str = "",
            decimals: int = 0,
            step: float = 1,
            slider: bool = True,
    ) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._scale = 10 ** decimals
        self._syncing = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        row = QHBoxLayout()
        row.setSpacing(10)
        row.addWidget(_label(title, "wlFieldLabel", wrap=False))
        row.addStretch(1)

        self.spin = QDoubleSpinBox()
        self.spin.setObjectName("wlSpin")
        self.spin.setRange(minimum, maximum)
        self.spin.setDecimals(decimals)
        self.spin.setSingleStep(step)
        self.spin.setValue(value)
        self.spin.setSuffix(f" {unit}" if unit else "")
        self.spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spin.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spin.setFixedWidth(120)
        self.spin.setKeyboardTracking(False)   # recalc on Enter/focus-out, not per digit
        row.addWidget(self.spin)
        layout.addLayout(row)

        self.slider: Optional[QSlider] = None
        if slider:
            self.slider = QSlider(Qt.Orientation.Horizontal)
            self.slider.setObjectName("wlSlider")
            self.slider.setRange(round(minimum * self._scale), round(maximum * self._scale))
            self.slider.setSingleStep(round(step * self._scale))
            self.slider.setValue(round(value * self._scale))
            self.slider.valueChanged.connect(self._from_slider)
            layout.addWidget(self.slider)

        self.spin.valueChanged.connect(self._from_spin)

    def value(self) -> float:
        return self.spin.value()

    def set_value(self, value: float) -> None:
        self.spin.setValue(value)

    def _from_slider(self, position: int) -> None:
        if self._syncing:
            return
        self._syncing = True
        self.spin.setValue(position / self._scale)
        self._syncing = False
        self.valueChanged.emit(self.spin.value())

    def _from_spin(self, value: float) -> None:
        if self._syncing:
            return
        self._syncing = True
        if self.slider is not None:
            self.slider.setValue(round(value * self._scale))
        self._syncing = False
        self.valueChanged.emit(value)


class Segmented(QWidget):
    """A row of mutually exclusive buttons (sex, BMI standard, ...)."""

    changed = Signal(str)

    def __init__(self, options: list[tuple[str, str]], selected: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._ids: dict[QPushButton, str] = {}
        for option_id, text in options:
            button = QPushButton(text)
            button.setObjectName("wlSegment")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setChecked(option_id == selected)
            self._group.addButton(button)
            self._ids[button] = option_id
            layout.addWidget(button)
        layout.addStretch(1)
        self._group.buttonClicked.connect(lambda b: self.changed.emit(self._ids[b]))

    def value(self) -> str:
        return self._ids[self._group.checkedButton()]


class ChoiceField(QWidget):
    """A labelled drop-down."""

    changed = Signal(str)

    def __init__(self, title: str, options: list[tuple[str, str]], selected: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(_label(title, "wlFieldLabel", wrap=False))

        self.combo = QComboBox()
        self.combo.setObjectName("wlCombo")
        for option_id, text in options:
            self.combo.addItem(text, option_id)
        self.combo.setCurrentIndex(max(self.combo.findData(selected), 0))
        self.combo.currentIndexChanged.connect(lambda _i: self.changed.emit(self.value()))
        layout.addWidget(self.combo)

    def value(self) -> str:
        return self.combo.currentData()


# =========================================================== shared output

class ResultCard(QFrame):
    """The coloured card on the right of every panel."""

    def __init__(self, accent: str) -> None:
        super().__init__()
        self.setObjectName("wlResult")
        self.setProperty("accent", accent)
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(22, 20, 22, 20)
        self.body.setSpacing(8)

    def big_number(self, number: str = "", unit: str = "") -> tuple[QLabel, QLabel]:
        row = QHBoxLayout()
        row.setSpacing(8)
        number_label = _label(number, "wlBigNumber", wrap=False)
        unit_label = _label(unit, "wlBigUnit", wrap=False)
        row.addWidget(number_label, 0, Qt.AlignmentFlag.AlignBottom)
        row.addWidget(unit_label, 0, Qt.AlignmentFlag.AlignBottom)
        row.addStretch(1)
        self.body.addLayout(row)
        return number_label, unit_label

    def divider(self) -> None:
        line = QFrame()
        line.setObjectName("wlDivider")
        line.setFixedHeight(1)
        self.body.addWidget(line)


class Badge(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("wlBadge")
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

    def show_tone(self, text: Optional[str], tone: str) -> None:
        self.setVisible(bool(text))
        self.setText(text or "")
        self.setProperty("tone", tone)
        _repolish(self)


class BmiGauge(QWidget):
    """A coloured scale of the BMI bands with a marker for the result."""

    LOW, HIGH = 15.0, 40.0

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.setFixedHeight(46)
        self._bands: list[tuple[float, Optional[float], str]] = []
        self._value: Optional[float] = None

    def set_data(self, result: BmiResult) -> None:
        lower = self.LOW
        self._bands = []
        for band in result.standard.bands:
            self._bands.append((lower, band.upper, band.tone))
            lower = band.upper or self.HIGH
        self._value = result.bmi
        self.update()

    def _x(self, bmi: float, width: float) -> float:
        bmi = min(max(bmi, self.LOW), self.HIGH)
        return (bmi - self.LOW) / (self.HIGH - self.LOW) * width

    def paintEvent(self, _event) -> None:
        if not self._bands:
            return
        colours = {"good": Theme.token("SUCCESS"), "warn": AMBER, "bad": Theme.token("DANGER")}
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width() - 2
        bar_top, bar_h = 14.0, 8.0

        font = QFont(self.font())
        font.setPointSizeF(7.5)
        painter.setFont(font)

        for low, high, tone in self._bands:
            x1 = self._x(low, width) + 1
            x2 = self._x(high or self.HIGH, width) + 1
            if x2 <= x1:
                continue
            colour = QColor(colours.get(tone, Theme.token("BORDER")))
            colour.setAlphaF(0.85)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(colour)
            painter.drawRect(QRectF(x1, bar_top, x2 - x1 - 1.5, bar_h))
            if high is not None and high < self.HIGH:
                painter.setPen(QColor(Theme.token("TEXT_MUTED")))
                painter.drawText(QRectF(x2 - 20, bar_top + bar_h + 3, 40, 14),
                                 Qt.AlignmentFlag.AlignHCenter, f"{high:g}")

        if self._value is not None:
            x = self._x(self._value, width) + 1
            marker = QPolygonF([QPointF(x - 6, 2), QPointF(x + 6, 2), QPointF(x, bar_top - 1)])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(Theme.token("TEXT")))
            painter.drawPolygon(marker)
        painter.end()


class _Panel(QFrame):
    """Outer card: inputs on the left, result on the right."""

    changed = Signal()

    def __init__(self, heading: str, accent: str) -> None:
        super().__init__()
        self.setObjectName("wlPanel")
        outer = QHBoxLayout(self)
        outer.setContentsMargins(24, 22, 24, 22)
        outer.setSpacing(24)

        left = _panel_widget()
        self.inputs = QVBoxLayout(left)
        self.inputs.setContentsMargins(0, 0, 0, 0)
        self.inputs.setSpacing(16)
        self.inputs.addWidget(_label(heading, "wlPanelHeading", wrap=False))
        outer.addWidget(left, 1)

        self.card = ResultCard(accent)
        outer.addWidget(self.card, 1)

    def _finish_inputs(self) -> None:
        self.inputs.addStretch(1)

    def _watch(self, *signals) -> None:
        for signal in signals:
            signal.connect(lambda *_a: self.changed.emit())


# ===================================================================== BMI

class BmiPanel(_Panel):
    def __init__(self) -> None:
        super().__init__("BODY MEASUREMENTS", "bmi")

        self.height = NumberField("Height", 50, 230, 170, "cm", decimals=1, step=0.5)
        self.weight = NumberField("Weight", 10, 250, 68, "kg", decimals=1, step=0.5)
        self.age = NumberField("Age", 2, 100, 28, "years")
        self.standard = Segmented(
            [("asia_pacific", "Asia-Pacific (DOH)"), ("who", "WHO International")],
            "asia_pacific",
        )
        for widget in (self.height, self.weight, self.age):
            self.inputs.addWidget(widget)
        self.inputs.addWidget(_label("Classification", "wlFieldLabel", wrap=False))
        self.inputs.addWidget(self.standard)
        self.inputs.addWidget(_label(
            "DOH uses the Asia-Pacific cutoffs for Filipino adults: weight-related "
            "risk starts at a lower BMI in Asian populations.", "wlHint"))
        self._finish_inputs()
        self._watch(self.height.valueChanged, self.weight.valueChanged,
                    self.age.valueChanged, self.standard.changed)

        c = self.card
        c.body.addWidget(_label("BODY MASS INDEX", "wlKicker", wrap=False))
        self.number, _unit = c.big_number("", "kg/m\u00b2")
        self.badge = Badge()
        c.body.addWidget(self.badge)
        # Age never changes the BMI number (weight / height squared); it
        # decides how that number is judged. Say so, so changing the age
        # visibly does something even when the number stays the same.
        self.age_group = _label("", "wlHint")
        c.body.addWidget(self.age_group)
        self.gauge = BmiGauge()
        c.body.addWidget(self.gauge)
        self.healthy = _label("", "wlStrong")
        c.body.addWidget(self.healthy)
        self.message = _label("", "wlBody")
        c.body.addWidget(self.message)
        c.divider()
        c.body.addWidget(_label(
            "BMI doesn't measure body fat directly: it misreads muscular people and "
            "doesn't apply in pregnancy. Pair it with waist circumference; Asian risk "
            "cutoffs are 90 cm for men and 80 cm for women.", "wlNote"))
        self.source = _label("", "wlSource")
        c.body.addWidget(self.source)
        c.body.addStretch(1)

    def values(self) -> dict:
        return {
            "height_cm": self.height.value(),
            "weight_kg": self.weight.value(),
            "age": int(self.age.value()),
            "standard_id": self.standard.value(),
        }

    def show_result(self, r: BmiResult) -> None:
        self.number.setText(f"{r.bmi:.1f}")
        self.badge.show_tone(r.category or "No adult category", r.tone)
        self.gauge.setVisible(r.category is not None)
        if r.category is not None:
            self.gauge.set_data(r)
        if r.healthy_weight_kg:
            low, high = r.healthy_weight_kg
            self.healthy.setText(
                f"Healthy weight at {self.height.value():g} cm: {low:g}\u2013{high:g} kg"
            )
        self.healthy.setVisible(bool(r.healthy_weight_kg))
        self.message.setText(r.message)
        self.source.setText(f"Cutoffs: {r.standard.source}")
        age = int(self.age.value())
        if age < 5:
            group = "Age under 5: judged on the WHO Child Growth Standards"
        elif age < 20:
            group = f"Age {age}: judged by BMI-for-age percentile (5\u201319 years)"
        elif age < 65:
            group = f"Age {age}: adult categories (20\u201364 years)"
        else:
            group = f"Age {age}: adult categories, with the older-adult note below"
        self.age_group.setText(group + ". Age doesn't change the BMI number itself, "
                               "only how it is read.")


# =============================================================== hydration

class HydrationPanel(_Panel):
    def __init__(self) -> None:
        super().__init__("HYDRATION FACTORS", "hydration")

        self.sex = Segmented([("male", "Male"), ("female", "Female")], "male")
        self.age = NumberField("Age", 1, 100, 28, "years")
        self.exercise = NumberField("Exercise per day", 0, 240, 45, "min", step=5)
        self.hot = QCheckBox("Hot or humid conditions, or working outdoors (+0.5 L)")
        self.hot.setChecked(True)   # the Philippine default
        self.status = ChoiceField(
            "Pregnancy / breastfeeding",
            [("none", "Neither"), ("pregnant", "Pregnant"), ("breastfeeding", "Breastfeeding")],
            "none",
        )

        self.inputs.addWidget(_label("Sex", "wlFieldLabel", wrap=False))
        self.inputs.addWidget(self.sex)
        for widget in (self.age, self.exercise, self.status, self.hot):
            self.inputs.addWidget(widget)
        self.inputs.addWidget(_label(
            "Water needs are set by age and sex, not body weight, so weight "
            "isn't asked for.", "wlHint"))
        self._finish_inputs()
        self._watch(self.sex.changed, self.age.valueChanged, self.exercise.valueChanged,
                    self.hot.toggled, self.status.changed)
        self.sex.changed.connect(lambda _s: self._update_status_visibility())
        self.age.valueChanged.connect(lambda _v: self._update_status_visibility())
        self._update_status_visibility()

        c = self.card
        c.body.addWidget(_label("DAILY WATER TO DRINK", "wlKicker", wrap=False))
        self.number, _unit = c.big_number("", "L / day")
        self.glasses = _label("", "wlStrong")
        c.body.addWidget(self.glasses)
        c.divider()
        self.breakdown = _label("", "wlBody")
        c.body.addWidget(self.breakdown)
        self.caution = _label("", "wlNote")
        c.body.addWidget(self.caution)
        c.body.addWidget(_label(
            "Source: U.S. National Academies Adequate Intake for water (2004); "
            "exercise and heat adjustments are estimates.", "wlSource"))
        c.body.addStretch(1)

    def _status_applies(self) -> bool:
        return self.sex.value() == "female" and self.age.value() >= 14

    def _update_status_visibility(self) -> None:
        self.status.setVisible(self._status_applies())

    def values(self) -> dict:
        # Not isVisible(): that is False whenever this tab isn't on screen.
        status = self.status.value() if self._status_applies() else "none"
        return {
            "sex": self.sex.value(),
            "age": int(self.age.value()),
            "exercise_minutes": int(self.exercise.value()),
            "hot_climate": self.hot.isChecked(),
            "status": status,
        }

    def show_result(self, r: HydrationResult) -> None:
        self.number.setText(f"{r.drinks_litres:.1f}")
        self.glasses.setText(
            f"About {r.glasses} glasses (250 mL). Total including water from "
            f"food: {r.total_litres:.1f} L."
        )
        self.breakdown.setText("\n".join(r.breakdown))
        self.caution.setText(r.caution)


# =================================================================== sleep

class SleepPanel(_Panel):
    TIPS = (
        "Keep the same sleep and wake times, weekends included.",
        "Avoid caffeine in the 6 hours before bed.",
        "Keep the bedroom dark, quiet and cool.",
        "Put screens away 30\u201360 minutes before sleeping.",
        "Avoid heavy meals close to bedtime.",
    )

    def __init__(self) -> None:
        super().__init__("SLEEP INPUTS", "sleep")

        self.age = NumberField("Age", 0, 100, 28, "years")
        self.inputs.addWidget(self.age)
        self.inputs.addWidget(_label(
            "Recommendations depend on age only. Physical workload doesn't change "
            "them, so it isn't asked for. Enter 0 for babies under 1 year.", "wlHint"))
        self._finish_inputs()
        self._watch(self.age.valueChanged)

        c = self.card
        self.group = _label("", "wlKicker", wrap=False)
        c.body.addWidget(self.group)
        self.number, _unit = c.big_number("", "hours / day")
        self.note = _label("", "wlStrong")
        c.body.addWidget(self.note)
        c.divider()
        c.body.addWidget(_label("Sleep habits that help", "wlStrong", wrap=False))
        c.body.addWidget(_label("\n".join(f"\u2022  {t}" for t in self.TIPS), "wlBody"))
        c.body.addWidget(_label(
            "Regularly sleeping less than 7 hours as an adult is linked to "
            "higher risk of obesity, hypertension and depression.", "wlNote"))
        c.body.addWidget(_label("Source: National Sleep Foundation (2015)", "wlSource"))
        c.body.addStretch(1)

    def values(self) -> dict:
        return {"age": int(self.age.value())}

    def show_result(self, r: SleepResult) -> None:
        self.group.setText(r.group.upper())
        self.number.setText(f"{r.low:g}\u2013{r.high:g}")
        self.note.setText(r.note)
        self.note.setVisible(bool(r.note))


# ================================================================== energy

class EnergyPanel(_Panel):
    def __init__(self) -> None:
        super().__init__("ENERGY INPUTS", "energy")

        self.sex = Segmented([("male", "Male"), ("female", "Female")], "female")
        self.age = NumberField("Age", 10, 100, 28, "years", slider=False)
        self.height = NumberField("Height", 100, 230, 165, "cm", decimals=1, slider=False)
        self.weight = NumberField("Weight", 25, 250, 60, "kg", decimals=1, slider=False)
        self.activity = ChoiceField(
            "Activity level",
            [(key, text) for key, (text, _f) in ACTIVITY_LEVELS.items()],
            "light",
        )

        self.inputs.addWidget(_label("Sex", "wlFieldLabel", wrap=False))
        self.inputs.addWidget(self.sex)
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(14)
        grid.addWidget(self.age, 0, 0)
        grid.addWidget(self.height, 0, 1)
        grid.addWidget(self.weight, 1, 0)
        self.inputs.addLayout(grid)
        self.inputs.addWidget(self.activity)
        self._finish_inputs()
        self._watch(self.sex.changed, self.age.valueChanged, self.height.valueChanged,
                    self.weight.valueChanged, self.activity.changed)

        c = self.card
        c.body.addWidget(_label("BASAL METABOLIC RATE (MIFFLIN-ST JEOR)", "wlKicker", wrap=False))
        self.bmr, _u = c.big_number("", "kcal / day at rest")
        c.divider()
        c.body.addWidget(_label("TOTAL DAILY ENERGY EXPENDITURE", "wlKicker", wrap=False))
        self.tdee, _u2 = c.big_number("", "kcal / day with activity")
        self.tdee.setObjectName("wlMidNumber")
        self.compare = _label("", "wlBody")
        c.body.addWidget(self.compare)
        self.message = _label("", "wlNote")
        c.body.addWidget(self.message)
        c.body.addWidget(_label(
            "Source: Mifflin et al. (1990); Harris-Benedict revised by Roza & "
            "Shizgal (1984).", "wlSource"))
        c.body.addStretch(1)

    def values(self) -> dict:
        return {
            "sex": self.sex.value(),
            "age": int(self.age.value()),
            "height_cm": self.height.value(),
            "weight_kg": self.weight.value(),
            "activity": self.activity.value(),
        }

    def show_result(self, r: EnergyResult) -> None:
        self.bmr.setText(f"{r.bmr:,}" if r.valid else "\u2014")
        self.tdee.setText(f"{r.tdee:,}" if r.valid else "\u2014")
        self.compare.setText(
            f"Harris-Benedict BMR for comparison: {r.harris_benedict_bmr:,} kcal/day."
            if r.valid else ""
        )
        self.compare.setVisible(r.valid)
        self.message.setText(r.message)


# =============================================================== converter

class ConverterPanel(QFrame):
    """Unit converter. Swap flips direction and carries the result across."""

    changed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("wlPanel")
        self._conversions: dict[str, Conversion] = {}
        self._current = ""
        self._reverse = False
        self._last: Optional[ConversionResult] = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)
        layout.addWidget(_label("CLINICAL UNIT CONVERTER", "wlPanelHeading", wrap=False))

        self._chip_host = _panel_widget()
        self._chips = FlowLayout()
        self._chip_host.setLayout(self._chips)
        self._chip_group = QButtonGroup(self)
        self._chip_group.setExclusive(True)
        layout.addWidget(self._chip_host)

        row = QHBoxLayout()
        row.setSpacing(18)

        box = QFrame()
        box.setObjectName("wlInputBox")
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(16, 14, 16, 14)
        box_layout.setSpacing(8)
        self.input_label = _label("", "wlKickerMuted", wrap=False)
        self.input = QDoubleSpinBox()
        self.input.setObjectName("wlConvInput")
        self.input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.input.setRange(-100, 100000)
        self.input.valueChanged.connect(lambda _v: self.changed.emit())
        box_layout.addWidget(self.input_label)
        box_layout.addWidget(self.input)
        row.addWidget(box, 1)

        self.swap = QPushButton("\u21c4")
        self.swap.setObjectName("wlSwap")
        self.swap.setFixedSize(46, 46)
        self.swap.setCursor(Qt.CursorShape.PointingHandCursor)
        self.swap.setToolTip("Swap direction")
        self.swap.clicked.connect(self._swap)
        row.addWidget(self.swap, 0, Qt.AlignmentFlag.AlignVCenter)

        self.card = ResultCard("converter")
        head = QHBoxLayout()
        self.result_label = _label("", "wlKicker", wrap=False)
        head.addWidget(self.result_label)
        head.addStretch(1)
        self.copy = QPushButton("Copy")
        self.copy.setObjectName("wlCopy")
        self.copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy.clicked.connect(self._copy)
        head.addWidget(self.copy)
        self.card.body.addLayout(head)
        self.number, self.unit = self.card.big_number()
        self.extra = _label("", "wlStrong", wrap=False)
        self.card.body.addWidget(self.extra)
        self.badge = Badge()
        self.card.body.addWidget(self.badge)
        row.addWidget(self.card, 1)
        layout.addLayout(row)

        note_box = QFrame()
        note_box.setObjectName("wlInputBox")
        note_layout = QVBoxLayout(note_box)
        note_layout.setContentsMargins(16, 10, 16, 10)
        self.note = _label("", "wlBody")
        note_layout.addWidget(self.note)
        layout.addWidget(note_box)
        layout.addStretch(1)

    def set_conversions(self, conversions: tuple[Conversion, ...]) -> None:
        for index, conv in enumerate(conversions):
            self._conversions[conv.id] = conv
            chip = QPushButton(conv.label)
            chip.setObjectName("wlConvChip")
            chip.setCheckable(True)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.clicked.connect(lambda _c=False, cid=conv.id: self._select(cid))
            self._chip_group.addButton(chip)
            self._chips.addWidget(chip)
            chip.setChecked(index == 0)
        if conversions:
            self._select(conversions[0].id)

    def _select(self, conversion_id: str) -> None:
        self._current = conversion_id
        self._reverse = False
        defaults = {
            "temperature": 37.0, "glucose": 100, "hba1c": 5.5, "cholesterol": 190,
            "triglycerides": 150, "creatinine": 1.0, "weight": 70, "height": 170,
            "pressure": 120,
        }
        self._apply_labels()
        self.input.setValue(defaults.get(conversion_id, 1))
        self.changed.emit()

    def _apply_labels(self) -> None:
        conv = self._conversions[self._current]
        src, dst = (conv.other_unit, conv.base_unit) if self._reverse else (conv.base_unit, conv.other_unit)
        self.input.blockSignals(True)
        self.input.setDecimals(conv.decimals[1] if self._reverse else conv.decimals[0])
        self.input.setDecimals(max(self.input.decimals(), 1))
        self.input.setRange(-100 if conv.id == "temperature" else 0, 100000)
        self.input.setSuffix(f" {src}")
        self.input.blockSignals(False)
        self.input_label.setText(f"INPUT ({src.upper()})")
        self.result_label.setText(f"RESULT ({dst.upper()})")
        self.note.setText(conv.note)

    def _swap(self) -> None:
        carry = self._last.value if self._last else self.input.value()
        self._reverse = not self._reverse
        self._apply_labels()
        self.input.setValue(carry)
        self.changed.emit()

    def _copy(self) -> None:
        if self._last:
            QApplication.clipboard().setText(f"{self._last.text} {self._last.unit}")
            self.copy.setText("Copied")

    def values(self) -> dict:
        return {"conversion_id": self._current, "value": self.input.value(), "reverse": self._reverse}

    def show_result(self, r: ConversionResult) -> None:
        self._last = r
        self.copy.setText("Copy")
        self.number.setText(r.text)
        self.unit.setText(r.unit)
        self.extra.setText(r.extra)
        self.extra.setVisible(bool(r.extra))
        self.badge.show_tone(r.badge, r.tone)