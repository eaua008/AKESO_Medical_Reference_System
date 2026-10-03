"""Wellness calculators: the math, with no widgets.

Every calculator here takes plain numbers and returns a small result object.
The view never does arithmetic, so each formula can be checked in a test
against a worked example from its source.

Sources, so anyone reviewing the numbers can check them:

    BMI cutoffs      DOH Philippines (WHO Asia-Pacific, 2000) and WHO global
    Hydration        U.S. National Academies, Dietary Reference Intakes for
                     Water (2004): Adequate Intake by age and sex
    Sleep            National Sleep Foundation recommendations (2015)
    Energy (BMR)     Mifflin-St Jeor (1990); Harris-Benedict revised by
                     Roza & Shizgal (1984) shown for comparison
    Conversions      standard SI factors; interpretation bands from ADA
                     (glucose, HbA1c) and NCEP ATP III (lipids)

"Tone" on a result is only a colour hint for the view: good, warn, bad, info.
"""

from dataclasses import dataclass, field
from typing import Callable, Optional

# ====================================================================== BMI

ADULT_AGE = 20   # WHO adult BMI categories start at 20; 5-19 use BMI-for-age


@dataclass(frozen=True)
class BmiBand:
    label: str
    upper: Optional[float]   # exclusive upper bound; None for the last band
    tone: str


@dataclass(frozen=True)
class BmiStandard:
    id: str
    name: str
    bands: tuple[BmiBand, ...]
    source: str

    def band_for(self, bmi: float) -> BmiBand:
        for band in self.bands:
            if band.upper is None or bmi < band.upper:
                return band
        return self.bands[-1]

    @property
    def healthy(self) -> tuple[float, float]:
        """Lower and upper BMI of the 'Normal' band."""
        lower = 0.0
        for band in self.bands:
            if band.label == "Normal":
                return lower, band.upper
            lower = band.upper
        raise ValueError("Standard has no Normal band")


BMI_STANDARDS = {
    "asia_pacific": BmiStandard(
        id="asia_pacific",
        name="Asia-Pacific (DOH)",
        bands=(
            BmiBand("Underweight", 18.5, "warn"),
            BmiBand("Normal", 23.0, "good"),
            BmiBand("Overweight", 25.0, "warn"),
            BmiBand("Obese I", 30.0, "bad"),
            BmiBand("Obese II", None, "bad"),
        ),
        source="DOH Philippines / WHO Western Pacific (2000)",
    ),
    "who": BmiStandard(
        id="who",
        name="WHO International",
        bands=(
            BmiBand("Underweight", 18.5, "warn"),
            BmiBand("Normal", 25.0, "good"),
            BmiBand("Overweight", 30.0, "warn"),
            BmiBand("Obese I", 35.0, "bad"),
            BmiBand("Obese II", 40.0, "bad"),
            BmiBand("Obese III", None, "bad"),
        ),
        source="World Health Organization",
    ),
}


@dataclass(frozen=True)
class BmiResult:
    bmi: float
    standard: BmiStandard
    category: Optional[str]           # None when adult categories don't apply
    tone: str
    message: str
    healthy_weight_kg: Optional[tuple[float, float]]


class BmiCalculator:
    """BMI = weight (kg) / height (m) squared."""

    def calculate(
            self,
            height_cm: float,
            weight_kg: float,
            age: int,
            standard_id: str = "asia_pacific",
    ) -> BmiResult:
        standard = BMI_STANDARDS[standard_id]
        height_m = height_cm / 100
        # Classify the ROUNDED value, the one on screen. Otherwise 22.96
        # shows as "23.0" but is labelled Normal, which looks like a bug.
        bmi = round(weight_kg / (height_m ** 2), 1)

        if age < ADULT_AGE:
            if age >= 5:
                chart = "WHO BMI-for-age growth reference (5\u201319 years)"
            else:
                chart = "WHO Child Growth Standards (under 5)"
            return BmiResult(
                bmi=bmi,
                standard=standard,
                category=None,
                tone="info",
                message=(
                    f"Adult categories don't apply under {ADULT_AGE}. Children's "
                    f"BMI is judged by percentile for age and sex; use the {chart}."
                ),
                healthy_weight_kg=None,
            )

        band = standard.band_for(bmi)
        low, high = standard.healthy
        healthy = (round(low * height_m ** 2, 1), round((high - 0.1) * height_m ** 2, 1))

        messages = {
            "Underweight": "Below the healthy range. Consider nutritional assessment.",
            "Normal": "Within the range linked to the lowest weight-related risk.",
            "Overweight": "Above the healthy range; weight-related risk starts rising here.",
        }
        message = messages.get(band.label, "In the obese range, with higher risk of diabetes, hypertension and heart disease.")
        if age >= 65:
            message += (
                " In adults over 65, BMI predicts risk less well and a slightly "
                "higher value may be protective; interpret with clinical context."
            )

        return BmiResult(
            bmi=bmi,
            standard=standard,
            category=band.label,
            tone=band.tone,
            message=message,
            healthy_weight_kg=healthy,
        )


# ================================================================ hydration

@dataclass(frozen=True)
class HydrationResult:
    total_litres: float        # from food and drinks together
    drinks_litres: float       # the part to actually drink (about 80%)
    glasses: int               # 250 mL glasses of the drinks part
    breakdown: tuple[str, ...]
    caution: str


class HydrationCalculator:
    """Adequate Intake of total water, then adjusted for sweat losses.

    The mockup multiplied body weight by a factor. Adequate Intake is set by
    age and sex instead, so weight isn't an input here.
    """

    # (max age inclusive, male L/day, female L/day), total water from all sources
    _AI_TABLE = (
        (3, 1.3, 1.3),
        (8, 1.7, 1.7),
        (13, 2.4, 2.1),
        (18, 3.3, 2.3),
        (200, 3.7, 2.7),
    )
    _PREGNANT_TOTAL = 3.0
    _BREASTFEEDING_TOTAL = 3.8
    _FROM_DRINKS = 0.8           # roughly 20% of water comes from food
    _EXERCISE_L_PER_HOUR = 0.5   # conservative; real sweat rates vary widely
    _HOT_CLIMATE_L = 0.5

    def calculate(
            self,
            sex: str,
            age: int,
            exercise_minutes: int,
            hot_climate: bool,
            status: str = "none",    # "none" | "pregnant" | "breastfeeding"
    ) -> HydrationResult:
        base = next(
            (male if sex == "male" else female)
            for limit, male, female in self._AI_TABLE
            if age <= limit
        )
        breakdown = [f"Adequate Intake for age and sex: {base:.1f} L"]

        if sex == "female" and age >= 14:
            if status == "pregnant":
                base = self._PREGNANT_TOTAL
                breakdown = [f"Adequate Intake in pregnancy: {base:.1f} L"]
            elif status == "breastfeeding":
                base = self._BREASTFEEDING_TOTAL
                breakdown = [f"Adequate Intake while breastfeeding: {base:.1f} L"]

        total = base
        if exercise_minutes:
            extra = exercise_minutes / 60 * self._EXERCISE_L_PER_HOUR
            total += extra
            breakdown.append(f"Exercise, {exercise_minutes} min: +{extra:.2f} L")
        if hot_climate:
            total += self._HOT_CLIMATE_L
            breakdown.append(f"Hot or humid conditions: +{self._HOT_CLIMATE_L:.1f} L")

        drinks = total * self._FROM_DRINKS
        return HydrationResult(
            total_litres=round(total, 1),
            drinks_litres=round(drinks, 1),
            glasses=round(drinks / 0.25),
            breakdown=tuple(breakdown),
            caution=(
                "People with heart failure, kidney disease, or a prescribed fluid "
                "limit should follow their doctor's target instead."
            ),
        )


# ==================================================================== sleep

@dataclass(frozen=True)
class SleepResult:
    group: str
    low: float
    high: float
    note: str


class SleepCalculator:
    """Recommended hours by age group.

    The mockup also asked for physical workload, but no guideline changes the
    recommendation by workload, so that input is gone.
    """

    # (max age inclusive, group, low, high)
    _TABLE = (
        (0, "Infant (4\u201311 months)", 12, 15),
        (2, "Toddler (1\u20132 years)", 11, 14),
        (5, "Preschool (3\u20135 years)", 10, 13),
        (13, "School age (6\u201313 years)", 9, 11),
        (17, "Teen (14\u201317 years)", 8, 10),
        (25, "Young adult (18\u201325 years)", 7, 9),
        (64, "Adult (26\u201364 years)", 7, 9),
        (200, "Older adult (65+ years)", 7, 8),
    )

    def recommend(self, age: int) -> SleepResult:
        limit, group, low, high = next(row for row in self._TABLE if age <= row[0])
        note = "Includes naps." if age <= 5 else ""
        if age == 0:
            note = "Includes naps. Newborns (0\u20133 months) need 14\u201317 hours."
        return SleepResult(group=group, low=low, high=high, note=note)


# =================================================================== energy

ACTIVITY_LEVELS = {
    "sedentary": ("Sedentary (little or no exercise)", 1.2),
    "light": ("Lightly active (1\u20133 days/week)", 1.375),
    "moderate": ("Moderately active (3\u20135 days/week)", 1.55),
    "very": ("Very active (6\u20137 days/week)", 1.725),
    "extra": ("Extra active (physical job + training)", 1.9),
}


@dataclass(frozen=True)
class EnergyResult:
    valid: bool
    bmr: int = 0
    tdee: int = 0
    harris_benedict_bmr: int = 0
    message: str = ""


class EnergyCalculator:
    """Resting energy (BMR) and total daily energy (TDEE).

    Mifflin-St Jeor is the primary equation: in validation studies it predicts
    measured resting energy more accurately than Harris-Benedict, which the
    mockup used. Harris-Benedict stays visible for comparison, since students
    meet both.
    """

    def calculate(
            self,
            sex: str,
            age: int,
            height_cm: float,
            weight_kg: float,
            activity: str,
    ) -> EnergyResult:
        if age < 18:
            return EnergyResult(
                valid=False,
                message="These equations were derived in adults (18+). "
                        "Children's needs are assessed with pediatric references.",
            )

        mifflin = 10 * weight_kg + 6.25 * height_cm - 5 * age
        mifflin += 5 if sex == "male" else -161

        if sex == "male":
            harris = 88.362 + 13.397 * weight_kg + 4.799 * height_cm - 5.677 * age
        else:
            harris = 447.593 + 9.247 * weight_kg + 3.098 * height_cm - 4.330 * age

        factor = ACTIVITY_LEVELS[activity][1]
        return EnergyResult(
            valid=True,
            bmr=round(mifflin),
            tdee=round(mifflin * factor),
            harris_benedict_bmr=round(harris),
            message=f"TDEE = BMR \u00d7 {factor} activity factor. Equations "
                    "estimate; individual needs can differ by about 10%.",
        )


# =============================================================== converter

@dataclass(frozen=True)
class Band:
    upper: Optional[float]    # exclusive, in the conversion's base unit
    label: str
    tone: str


@dataclass(frozen=True)
class Conversion:
    id: str
    label: str
    icon: str
    base_unit: str            # the "left" unit
    other_unit: str
    to_other: Callable[[float], float]
    to_base: Callable[[float], float]
    decimals: tuple[int, int]  # (base unit, other unit); mg/dL wants 0, mmol/L 2
    note: str
    bands: tuple[Band, ...] = field(default=())
    band_prefix: str = ""     # e.g. "If fasting: "

    def interpret(self, base_value: float) -> Optional[tuple[str, str]]:
        for band in self.bands:
            if band.upper is None or base_value < band.upper:
                return self.band_prefix + band.label, band.tone
        return None


@dataclass(frozen=True)
class ConversionResult:
    value: float
    text: str
    unit: str
    extra: str = ""
    badge: Optional[str] = None
    tone: str = "info"


def _feet_inches(inches: float) -> str:
    feet, rest = divmod(round(inches), 12)
    return f"{feet} ft {rest} in"


CONVERSIONS = (
    Conversion(
        "temperature", "Temperature", "heart", "\u00b0C", "\u00b0F",
        lambda c: c * 9 / 5 + 32, lambda f: (f - 32) * 5 / 9, (1, 1),
        "Normal core temperature is about 36.5\u201337.5 \u00b0C. Fever is 38.0 \u00b0C or higher.",
        (
            Band(35.0, "Hypothermia", "bad"),
            Band(36.5, "Below normal", "warn"),
            Band(37.6, "Normal", "good"),
            Band(38.0, "Slightly elevated", "warn"),
            Band(40.0, "Fever", "bad"),
            Band(None, "High fever", "bad"),
        ),
    ),
    Conversion(
        "glucose", "Glucose", "pulse", "mg/dL", "mmol/L",
        lambda v: v / 18.016, lambda v: v * 18.016, (0, 2),
        "Fasting: 70\u201399 mg/dL normal, 100\u2013125 prediabetes, 126+ diabetes range "
        "(ADA). Bands apply only to a fasting sample.",
        (
            Band(70, "Low (hypoglycemia)", "bad"),
            Band(100, "Normal", "good"),
            Band(126, "Prediabetes range", "warn"),
            Band(None, "Diabetes range", "bad"),
        ),
        band_prefix="If fasting: ",
    ),
    Conversion(
        "hba1c", "HbA1c", "pulse", "%", "mmol/mol",
        lambda v: (v - 2.15) * 10.929, lambda v: v / 10.929 + 2.15, (1, 0),
        "NGSP % to IFCC mmol/mol. Below 5.7% normal, 5.7\u20136.4% prediabetes, "
        "6.5%+ diabetes range (ADA).",
        (
            Band(5.7, "Normal", "good"),
            Band(6.5, "Prediabetes range", "warn"),
            Band(None, "Diabetes range", "bad"),
        ),
    ),
    Conversion(
        "cholesterol", "Cholesterol", "heart", "mg/dL", "mmol/L",
        lambda v: v / 38.67, lambda v: v * 38.67, (0, 2),
        "Total cholesterol: below 200 mg/dL desirable, 200\u2013239 borderline high, "
        "240+ high (NCEP ATP III). The same factor converts LDL and HDL.",
        (
            Band(200, "Desirable (total)", "good"),
            Band(240, "Borderline high (total)", "warn"),
            Band(None, "High (total)", "bad"),
        ),
    ),
    Conversion(
        "triglycerides", "Triglycerides", "heart", "mg/dL", "mmol/L",
        lambda v: v / 88.57, lambda v: v * 88.57, (0, 2),
        "Below 150 mg/dL normal, 150\u2013199 borderline, 200\u2013499 high, "
        "500+ very high (NCEP ATP III).",
        (
            Band(150, "Normal", "good"),
            Band(200, "Borderline high", "warn"),
            Band(500, "High", "bad"),
            Band(None, "Very high", "bad"),
        ),
    ),
    Conversion(
        "creatinine", "Creatinine", "pulse", "mg/dL", "\u00b5mol/L",
        lambda v: v * 88.4, lambda v: v / 88.4, (2, 0),
        "1 mg/dL = 88.4 \u00b5mol/L. Reference ranges depend on sex, age and muscle "
        "mass, so no band is shown; kidney function is judged by eGFR.",
    ),
    Conversion(
        "weight", "Weight", "user", "kg", "lb",
        lambda v: v * 2.20462, lambda v: v / 2.20462, (1, 1),
        "1 kg = 2.20462 lb.",
    ),
    Conversion(
        "height", "Height", "user", "cm", "in",
        lambda v: v / 2.54, lambda v: v * 2.54, (1, 1),
        "1 in = 2.54 cm; 1 ft = 30.48 cm.",
    ),
    Conversion(
        "pressure", "BP (mmHg/kPa)", "pulse", "mmHg", "kPa",
        lambda v: v * 0.133322, lambda v: v / 0.133322, (0, 2),
        "1 mmHg = 0.1333 kPa. 120/80 mmHg is about 16.0/10.7 kPa. Convert "
        "systolic and diastolic separately.",
    ),
)


class UnitConverter:
    """Converts in either direction and interprets in the base unit."""

    def __init__(self) -> None:
        self._by_id = {c.id: c for c in CONVERSIONS}

    @property
    def conversions(self) -> tuple[Conversion, ...]:
        return CONVERSIONS

    def get(self, conversion_id: str) -> Conversion:
        return self._by_id[conversion_id]

    def convert(self, conversion_id: str, value: float, reverse: bool) -> ConversionResult:
        conv = self._by_id[conversion_id]
        if reverse:
            out = conv.to_base(value)
            # Interpret the value as displayed, like BMI: otherwise 99.99
            # shows as "100 mg/dL" but is labelled Normal instead of Prediabetes.
            unit, base_value = conv.base_unit, round(out, conv.decimals[0])
        else:
            out, unit, base_value = conv.to_other(value), conv.other_unit, value

        extra = ""
        if conv.id == "height":
            inches = value if reverse else out
            extra = _feet_inches(inches)

        badge = conv.interpret(base_value) if conv.bands else None
        return ConversionResult(
            value=out,
            text=f"{out:.{conv.decimals[0 if reverse else 1]}f}",
            unit=unit,
            extra=extra,
            badge=badge[0] if badge else None,
            tone=badge[1] if badge else "info",
        )


# ================================================================ facade

class WellnessService:
    """One object the controller holds, instead of five."""

    def __init__(self) -> None:
        self.bmi = BmiCalculator()
        self.hydration = HydrationCalculator()
        self.sleep = SleepCalculator()
        self.energy = EnergyCalculator()
        self.converter = UnitConverter()