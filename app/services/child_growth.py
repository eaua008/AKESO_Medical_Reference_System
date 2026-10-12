"""Children's growth z-scores with the WHO growth charts.

Data: data/who_growth.json (built from WHO's published LMS tables; see
scripts/build_who_growth.py):

    0-60 months    WHO Child Growth Standards (2006)
    61-228 months  WHO Growth Reference for 5-19 years (2007)

Each table row is (L, M, S) for one month of age (or one 0.5 cm step of
length/height for weight-for-length/height). The z-score is the LMS formula

    z = ((X / M) ** L - 1) / (L * S)

and, for weight-based indicators beyond +/-3 SD, WHO's restricted
adjustment (the distance between 2 and 3 SD is used as the unit past 3 SD),
as in WHO Anthro and the WHO technical report (2006, chapter 7).

Interpretation cut-offs (WHO Training Course on Child Growth Assessment,
2008; WHO 2007 reference for 5-19 years):

    under 5   weight-for-length/height and BMI-for-age:
              > +3 obese, > +2 overweight, > +1 possible risk of overweight,
              < -2 wasted, < -3 severely wasted
    5-19      BMI-for-age: > +2 obesity, > +1 overweight,
              < -2 thinness, < -3 severe thinness
    all       height-for-age: < -2 stunted, < -3 severely stunted
              weight-for-age (to 10 y): < -2 underweight, < -3 severely underweight
"""

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from app.core.paths import resource

MAX_MONTHS = 228                     # 19 years


@dataclass(frozen=True)
class Indicator:
    key: str                         # "bfa", "hfa", "wfa", "wfh"
    name: str                        # "BMI-for-age"
    z: float
    percentile: float
    label: str                       # "Normal", "Stunted", ...
    tone: str                        # good | warn | bad | info


@dataclass(frozen=True)
class ChildGrowth:
    age_months: float
    sex: str
    reference: str                   # which WHO chart was used
    bmi: Indicator
    others: tuple[Indicator, ...]
    healthy_weight_kg: Optional[tuple[float, float]]
    healthy_note: str


@lru_cache(maxsize=1)
def _tables() -> dict:
    return json.loads(resource("data", "who_growth.json").read_text("utf-8"))


def _by_age(rows: list, months: float) -> tuple[float, float, float]:
    """LMS for an age in months, interpolated between whole months."""
    months = max(0.0, min(len(rows) - 1.0, months))
    low = int(math.floor(months))
    high = min(low + 1, len(rows) - 1)
    k = months - low
    return tuple(a + (b - a) * k for a, b in zip(rows[low], rows[high]))   # type: ignore


def _by_size(table: dict, cm: float) -> Optional[tuple[float, float, float]]:
    rows, start, step = table["rows"], table["start"], table["step"]
    pos = (cm - start) / step
    if pos < 0 or pos > len(rows) - 1:
        return None
    low = int(math.floor(pos))
    high = min(low + 1, len(rows) - 1)
    k = pos - low
    return tuple(a + (b - a) * k for a, b in zip(rows[low], rows[high]))   # type: ignore


def _value_at(lms: tuple[float, float, float], z: float) -> float:
    L, M, S = lms
    if abs(L) < 1e-9:
        return M * math.exp(S * z)
    return M * (1 + L * S * z) ** (1 / L)


def z_score(x: float, lms: tuple[float, float, float], restricted: bool = True) -> float:
    L, M, S = lms
    if abs(L) < 1e-9:
        z = math.log(x / M) / S
    else:
        z = ((x / M) ** L - 1) / (L * S)
    if restricted and abs(z) > 3:
        # WHO: beyond 3 SD, measure in units of the 2-3 SD distance.
        if z > 3:
            sd3, sd2 = _value_at(lms, 3), _value_at(lms, 2)
            z = 3 + (x - sd3) / (sd3 - sd2)
        else:
            sd3, sd2 = _value_at(lms, -3), _value_at(lms, -2)
            z = -3 + (x - sd3) / (sd2 - sd3)
    return z


def percentile(z: float) -> float:
    return 50 * (1 + math.erf(z / math.sqrt(2)))


def _weight_status(z: float, under_five: bool) -> tuple[str, str]:
    if under_five:
        if z > 3:
            return "Obese", "bad"
        if z > 2:
            return "Overweight", "bad"
        if z > 1:
            return "Possible risk of overweight", "warn"
        if z < -3:
            return "Severely wasted", "bad"
        if z < -2:
            return "Wasted", "bad"
        return "Normal", "good"
    if z > 2:
        return "Obesity", "bad"
    if z > 1:
        return "Overweight", "warn"
    if z < -3:
        return "Severe thinness", "bad"
    if z < -2:
        return "Thinness", "bad"
    return "Normal", "good"


def _height_status(z: float) -> tuple[str, str]:
    if z < -3:
        return "Severely stunted", "bad"
    if z < -2:
        return "Stunted", "bad"
    if z > 3:
        return "Very tall", "info"
    return "Normal", "good"


def _weight_for_age_status(z: float) -> tuple[str, str]:
    if z < -3:
        return "Severely underweight", "bad"
    if z < -2:
        return "Underweight", "bad"
    if z > 1:
        return "Check weight-for-height or BMI", "info"
    return "Normal", "good"


def _indicator(key: str, name: str, z: float, status: tuple[str, str]) -> Indicator:
    return Indicator(key, name, round(z, 2), round(percentile(z), 1), status[0], status[1])


def assess(sex: str, age_months: float, height_cm: float, weight_kg: float) -> ChildGrowth:
    """Every WHO indicator that applies at this age."""
    if not 0 <= age_months <= MAX_MONTHS:
        raise ValueError("WHO growth charts cover 0 to 19 years.")
    sex = "female" if sex == "female" else "male"
    data = _tables()
    under_five = age_months <= 60
    bmi = weight_kg / (height_cm / 100) ** 2

    bfa_lms = _by_age(data["bfa"][sex], age_months)
    bmi_ind = _indicator("bfa", "BMI-for-age", z_score(bmi, bfa_lms),
                         _weight_status(z_score(bmi, bfa_lms), under_five))
    others = []
    hfa = z_score(height_cm, _by_age(data["hfa"][sex], age_months), restricted=False)
    others.append(_indicator("hfa", "Length-for-age" if age_months < 24 else "Height-for-age",
                             hfa, _height_status(hfa)))
    if age_months <= 120:                         # WHO weight-for-age stops at 10 years
        wfa = z_score(weight_kg, _by_age(data["wfa"][sex], age_months))
        others.append(_indicator("wfa", "Weight-for-age", wfa, _weight_for_age_status(wfa)))
    healthy: Optional[tuple[float, float]] = None
    note = ""
    if under_five:
        table = data["wfl"][sex] if age_months < 24 else data["wfh"][sex]
        name = "Weight-for-length" if age_months < 24 else "Weight-for-height"
        lms = _by_size(table, height_cm)
        if lms is not None:
            wfh = z_score(weight_kg, lms)
            others.insert(0, _indicator("wfh", name, wfh, _weight_status(wfh, True)))
            healthy = (round(_value_at(lms, -2), 1), round(_value_at(lms, 2), 1))
            note = f"{name} between -2 and +2 SD"
    else:
        h2 = (height_cm / 100) ** 2
        healthy = (round(_value_at(bfa_lms, -2) * h2, 1), round(_value_at(bfa_lms, 1) * h2, 1))
        note = "BMI-for-age between -2 and +1 SD"
    reference = ("WHO Child Growth Standards (2006)" if under_five
                 else "WHO Growth Reference 5–19 years (2007)")
    return ChildGrowth(age_months, sex, reference, bmi_ind, tuple(others), healthy, note)
