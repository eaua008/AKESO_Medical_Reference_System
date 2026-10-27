"""Weight-based dose arithmetic for the "Dose calculation" practice cards.

Strict on purpose: a dose string is only used when it is unambiguous.

    "15 mg/kg"            per intake; times per day from the frequency
    "100 mg/kg/day ÷ 3"   per day, split into 3 intakes
    "10–20 mg/kg/day"     per day; only with "Once a day"
    "40–90 mg/kg/day, divided", "20 mg/kg (range 15–25)", "units/kg",
    "micrograms/kg", "100/20 mg/kg" ... are skipped (None)

Maximums: "4 g/day", "500 mg/dose", "1 g", "60 mg/kg/day"; "—" or empty
means none is listed. Anything else makes the row ambiguous (None).
"""

import re
from dataclasses import dataclass, field
from typing import Optional

NUM = r"(\d+(?:\.\d+)?)"
DASH = r"\s*[–—-]\s*"
_DOSE = re.compile(rf"^{NUM}(?:{DASH}{NUM})?\s*mg/kg(/day)?(?:\s*÷\s*(\d+))?$")
_MAX = re.compile(rf"^(\d[\d,]*(?:\.\d+)?)\s*(mg|g)(?:\s*(?:/|per\s+)(day|dose))?$", re.I)
_MAX_KG = re.compile(rf"^{NUM}\s*mg/kg/(day|dose)$", re.I)
_LIQUID = re.compile(r"(\d+(?:\.\d+)?)\s*mg\s*/\s*(\d+(?:\.\d+)?)\s*mL", re.I)
NONE_WORDS = ("", "—", "-", "none")
DISCLAIMER = "Practice calculation: always check the prescriber and product insert."


@dataclass
class DoseRule:
    low: float                    # mg/kg
    high: float
    per_day: bool                 # mg/kg/day (else per intake)
    divide: Optional[int]         # "÷ N"


@dataclass
class MaxRule:
    mg: Optional[float] = None    # absolute
    per_kg: Optional[float] = None
    per: str = "day"              # day | dose


@dataclass
class Worked:
    per_intake_low: float
    per_intake_high: float
    frequency: str
    steps: list[str] = field(default_factory=list)
    capped: bool = False
    ml: Optional[tuple[float, float]] = None
    liquid: str = ""

    @property
    def answer(self) -> str:
        dose = mg_text(self.per_intake_low, self.per_intake_high)
        text = f"{dose} {self.frequency}".strip()
        if self.ml:
            text += f" ({ml_text(*self.ml)})"
        return text


def _num(text: str) -> float:
    return float(text.replace(",", ""))


def fmt(value: float) -> str:
    """1350 -> '1,350'; 7.5 -> '7.5'; 666.67 -> '667' (whole mg from 10 up)."""
    value = round(value) if value >= 10 else round(value, 1)
    if value == int(value):
        return f"{int(value):,}"
    return f"{value:,.1f}"


def mg_text(low: float, high: float) -> str:
    return f"{fmt(low)} mg" if abs(low - high) < 1e-9 else f"{fmt(low)}–{fmt(high)} mg"


def ml_text(low: float, high: float) -> str:
    return f"{fmt(low)} mL" if abs(low - high) < 1e-9 else f"{fmt(low)}–{fmt(high)} mL"


def parse_dose(text: str) -> Optional[DoseRule]:
    m = _DOSE.match((text or "").strip())
    if not m:
        return None
    low = float(m.group(1))
    high = float(m.group(2)) if m.group(2) else low
    if high < low:
        return None
    return DoseRule(low, high, bool(m.group(3)), int(m.group(4)) if m.group(4) else None)


def times_per_day(frequency: str) -> Optional[int]:
    """'Every 8 h' -> 3, '2× a day' -> 2, 'Once a day' / 'Single dose' -> 1; ranges -> None."""
    text = (frequency or "").strip().lower()
    if re.fullmatch(r"once a day|once daily|single dose|daily", text):
        return 1
    m = re.fullmatch(r"every (\d+) ?h(?:ours?)?", text)
    if m and 24 % int(m.group(1)) == 0:
        return 24 // int(m.group(1))
    m = re.fullmatch(r"(\d+) ?(?:×|x|times) a day", text)
    if m:
        return int(m.group(1))
    return None


def frequency_words(frequency: str, per_day: Optional[int]) -> str:
    text = (frequency or "").strip()
    if not text and per_day:
        return {1: "once a day"}.get(per_day, f"{per_day}× a day")
    return text[:1].lower() + text[1:]


def parse_max(text: str) -> Optional[MaxRule]:
    """A MaxRule, MaxRule() when none is listed, or None when it can't be read."""
    text = (text or "").strip()
    if text.lower() in NONE_WORDS:
        return MaxRule()
    m = _MAX_KG.match(text)
    if m:
        return MaxRule(per_kg=float(m.group(1)), per=m.group(2).lower())
    m = _MAX.match(text)
    if m:
        mg = _num(m.group(1)) * (1000 if m.group(2).lower() == "g" else 1)
        return MaxRule(mg=mg, per=(m.group(3) or "dose").lower() if m.group(3) else "dose")
    return None


def liquid_strength(form_notes: list[str]) -> Optional[tuple[float, float, str]]:
    """(mg, mL, text) of the first liquid form listed, e.g. 250 mg/5 mL."""
    for note in form_notes:
        m = _LIQUID.search(note or "")
        if m:
            return float(m.group(1)), float(m.group(2)), f"{fmt(float(m.group(1)))} mg/{fmt(float(m.group(2)))} mL"
    return None


def work_out(dose: str, frequency: str, max_dose: str, weight: float,
             form_notes: list[str] = ()) -> Optional[Worked]:
    """The worked answer for one child, or None when the row is ambiguous."""
    rule = parse_dose(dose)
    if rule is None:
        return None
    limit = parse_max(max_dose)
    if limit is None:
        return None
    per_day_count = times_per_day(frequency)
    steps: list[str] = []
    if rule.per_day:
        divide = rule.divide or (per_day_count if per_day_count == 1 else None)
        if divide is None or (rule.divide and per_day_count and per_day_count != rule.divide):
            return None
        day_low, day_high = rule.low * weight, rule.high * weight
        steps.append(f"{mg_text(rule.low, rule.high).replace(' mg', '')} mg/kg/day × {fmt(weight)} kg = "
                     f"{mg_text(day_low, day_high)} a day")
        low, high = day_low / divide, day_high / divide
        if divide > 1:
            steps.append(f"÷ {divide} doses = {mg_text(low, high)} per dose")
        per_day_count = divide
    else:
        low, high = rule.low * weight, rule.high * weight
        steps.append(f"{mg_text(rule.low, rule.high).replace(' mg', '')} mg/kg × {fmt(weight)} kg = "
                     f"{mg_text(low, high)} per dose")
        if per_day_count:
            steps.append(f"{per_day_count} dose{'s' if per_day_count != 1 else ''} a day = "
                         f"{mg_text(low * per_day_count, high * per_day_count)} a day")
    capped = False
    cap_mg = None
    if limit.mg is not None:
        cap_mg = limit.mg
    elif limit.per_kg is not None:
        cap_mg = limit.per_kg * weight
    if cap_mg is not None:
        limit_text = (f"{fmt(limit.per_kg)} mg/kg/{limit.per} = {fmt(cap_mg)} mg/{limit.per}"
                      if limit.per_kg is not None else f"{fmt(cap_mg)} mg/{limit.per}")
        if limit.per == "dose":
            if high > cap_mg:
                capped = True
                low, high = min(low, cap_mg), cap_mg
                steps.append(f"Max {limit_text}: capped to {mg_text(low, high)} per dose")
            else:
                steps.append(f"Max {limit_text}: within the limit")
        else:
            if per_day_count:
                if high * per_day_count > cap_mg:
                    capped = True
                    per_dose_cap = cap_mg / per_day_count
                    low, high = min(low, per_dose_cap), per_dose_cap
                    steps.append(f"Max {limit_text}: capped to {mg_text(low, high)} per dose")
                else:
                    steps.append(f"Max {limit_text}: within the limit")
            else:
                steps.append(f"Max {limit_text}: keep the day's total under it")
    else:
        steps.append("No maximum is listed in Akeso for this row")
    worked = Worked(low, high, frequency_words(frequency, per_day_count), steps, capped)
    strength = liquid_strength(list(form_notes))
    if strength:
        mg, ml, text = strength
        worked.ml = (low * ml / mg, high * ml / mg)
        worked.liquid = text
        worked.steps.append(f"As {text} liquid: {ml_text(*worked.ml)} per dose")
    worked.steps.append(DISCLAIMER)
    return worked
