"""Vital Signs Checker: is each reading in the usual range for this age?

Plain numbers in, a small result out (no widgets), like the other wellness
calculators. Every range below names its source so it can be checked.

Adults (18+)
    Blood pressure, two standards to choose from:
      Philippines   2020 Philippine CPG for hypertension (Philippine Heart
                    Association / Philippine Society of Hypertension):
                    Normal < 120/80, Borderline 120-139 / 80-89,
                    Hypertension >= 140/90
      AHA/ACC       2025 AHA/ACC guideline (keeps the 2017 categories):
                    Normal < 120 and < 80, Elevated 120-129 and < 80,
                    Stage 1 130-139 or 80-89, Stage 2 >= 140 or >= 90,
                    Severe > 180 and/or > 120
    Low blood pressure  < 90 systolic or < 60 diastolic (AHA)
    Pulse               60-100 per minute (AHA)
    Breathing rate      12-20 per minute (adult normal used by NEWS2, RCP 2017)

Children (under 18)
    Pulse and breathing rate by age group: "Normal Pediatric Vital Signs",
        PALS reference card (American Red Cross, 2025; awake values)
    Blood pressure: AAP 2017 screening table (Flynn et al., Pediatrics
        2017;140:e20171904): at or above these values, recheck and have the
        child's BP percentile worked out. From 13 years the adult cut-offs apply.
    Low blood pressure (hypotension) by age: PALS (AHA): < 60 under 1 month,
        < 70 under 1 year, < 70 + 2 x age for 1-10 years, < 90 over 10 years

Everyone
    Temperature  fever 38.0 C or more (oral, ear, rectal), 37.5 C or more
                 (armpit or forehead, which read lower; WHO IMCI uses 37.5 C
                 axillary); under 35.0 C is hypothermia. Any fever under 3
                 months of age needs a doctor the same day (NICE NG143).
    SpO2         95-100% usual at sea level; under 94% with breathing
                 difficulty or under 90% at any time needs oxygen
                 assessment (WHO, Oxygen therapy for children, 2016)

A screening aid for study and self-checks, never a diagnosis: one reading
can be off (cuff size, movement, a cold finger, just having exercised).
"""

from dataclasses import dataclass
from typing import Optional

TONE_ORDER = {"good": 0, "info": 1, "warn": 2, "bad": 3}

# (upper age in months, exclusive), name, breathing (low, high), pulse (low, high)
CHILD_RANGES = (
    (1, "Newborn (under 1 month)", (35, 55), (100, 205)),
    (12, "Infant (1-12 months)", (30, 53), (100, 180)),
    (36, "Toddler (1-2 years)", (22, 37), (98, 140)),
    (72, "Preschooler (3-5 years)", (20, 29), (80, 120)),
    (156, "School age (6-12 years)", (18, 25), (75, 118)),
    (216, "Adolescent (13-17 years)", (12, 20), (60, 100)),
)
ADULT = ("Adult (18 and over)", (12, 20), (60, 100))

# AAP 2017 screening table: age -> (boys SBP, boys DBP, girls SBP, girls DBP)
AAP_SCREENING = {
    1: (98, 52, 98, 54), 2: (100, 55, 101, 58), 3: (101, 58, 102, 60),
    4: (102, 60, 103, 62), 5: (103, 63, 104, 64), 6: (105, 66, 105, 67),
    7: (106, 68, 106, 68), 8: (107, 69, 107, 69), 9: (107, 70, 108, 71),
    10: (108, 72, 109, 72), 11: (110, 74, 111, 74), 12: (113, 75, 114, 75),
}

SOURCES = {
    "bp_ph": "2020 Philippine CPG for hypertension (PHA / PSH)",
    "bp_aha": "2025 AHA/ACC high blood pressure guideline",
    "bp_child": "AAP 2017 pediatric BP screening table; PALS hypotension limits",
    "rates_child": "PALS reference card, American Red Cross (2025)",
    "rates_adult": "AHA (pulse); RCP NEWS2, 2017 (breathing)",
    "temp": "WHO IMCI (axillary 37.5 °C); NICE NG143 (fever under 5s)",
    "spo2": "WHO, Oxygen therapy for children (2016)",
}


@dataclass(frozen=True)
class Reading:
    key: str              # bp, pulse, breathing, temperature, spo2
    name: str
    value: str            # "128/82 mmHg"
    label: str            # "Borderline"
    tone: str             # good | info | warn | bad
    usual: str            # "Normal is below 120/80"
    note: str = ""
    source: str = ""


@dataclass(frozen=True)
class VitalsResult:
    group: str                     # "Adult (18 and over)"
    readings: tuple[Reading, ...]
    overall: str                   # badge text
    tone: str
    advice: str


def _group(age_months: int):
    if age_months >= 216:
        return ADULT
    for limit, name, breathing, pulse in CHILD_RANGES:
        if age_months < limit:
            return name, breathing, pulse
    return ADULT


def _rate(key: str, name: str, value: float, unit: str, usual: tuple[int, int],
          low_word: str, high_word: str, source: str, note_low: str = "") -> Reading:
    low, high = usual
    text = f"{value:g} {unit}"
    span = f"Usual for this age: {low}–{high} {unit}"
    if value < low:
        return Reading(key, name, text, low_word, "warn", span, note_low, source)
    if value > high:
        return Reading(key, name, text, high_word, "warn", span, "", source)
    return Reading(key, name, text, "Normal", "good", span, "", source)


def _adult_bp(sbp: float, dbp: float, standard: str) -> tuple[str, str, str, str]:
    """label, tone, usual, note"""
    if sbp < 90 or dbp < 60:
        return ("Low", "warn", "Usual: 90/60 up to 119/79 mmHg",
                "Low readings matter if you feel dizzy, faint or weak.")
    if standard == "aha":
        if sbp > 180 or dbp > 120:
            return ("Severe", "bad", "Normal: below 120 and below 80 mmHg",
                    "Rest 5 minutes and measure again. With chest pain, shortness of "
                    "breath, weakness, or trouble seeing or speaking, get emergency care.")
        if sbp >= 140 or dbp >= 90:
            return "Stage 2 hypertension", "bad", "Normal: below 120 and below 80 mmHg", ""
        if sbp >= 130 or dbp >= 80:
            return "Stage 1 hypertension", "warn", "Normal: below 120 and below 80 mmHg", ""
        if sbp >= 120:
            return "Elevated", "warn", "Normal: below 120 and below 80 mmHg", ""
        return "Normal", "good", "Normal: below 120 and below 80 mmHg", ""
    severe = ("Very high. Rest 5 minutes and measure again; with chest pain, shortness of "
              "breath, weakness, or trouble seeing or speaking, get emergency care."
              if sbp > 180 or dbp > 120 else "")
    if sbp >= 140 or dbp >= 90:
        return ("Hypertension", "bad", "Normal: below 120/80 mmHg",
                severe or "Hypertension is confirmed by raised readings on two separate days.")
    if sbp >= 120 or dbp >= 80:
        return "Borderline", "warn", "Normal: below 120/80 mmHg", ""
    return "Normal", "good", "Normal: below 120/80 mmHg", ""


def _child_bp(sbp: float, dbp: float, age_months: int, sex: str) -> tuple[str, str, str, str]:
    years = age_months // 12
    if age_months < 1:
        low = 60
    elif age_months < 12:
        low = 70
    elif years <= 10:
        low = 70 + 2 * years
    else:
        low = 90
    if sbp < low:
        return ("Low", "bad", f"Low (hypotension) for this age: systolic below {low} mmHg",
                "A low reading in an unwell child needs a doctor now.")
    if years < 1:
        return ("No screening value", "info", f"Hypotension limit for this age: {low} mmHg",
                "AAP screening values start at 1 year.")
    if years >= 13:
        # Low pressure was already judged above (PALS: under 90 systolic), so a
        # low diastolic alone is not called "Low" here.
        label, tone, usual, note = _adult_bp(max(sbp, 90), max(dbp, 60), "aha")
        return label, tone, usual + " (adult cut-offs from 13 years)", note
    boys_s, boys_d, girls_s, girls_d = AAP_SCREENING[min(years, 12)]
    s_cut, d_cut = (girls_s, girls_d) if sex == "female" else (boys_s, boys_d)
    usual = f"Screening value at {years} years: below {s_cut}/{d_cut} mmHg"
    if sbp >= s_cut or dbp >= d_cut:
        return ("Above screening value", "warn", usual,
                "Recheck at rest. If still high, a doctor works out the BP percentile "
                "for the child's age, sex and height.")
    return "Normal", "good", usual, ""


def _temperature(value: float, site: str, age_months: int) -> Reading:
    low_reading = site in ("axillary", "forehead")
    fever_at = 37.5 if low_reading else 38.0
    where = {"oral": "mouth", "ear": "ear", "rectal": "rectal",
             "axillary": "armpit", "forehead": "forehead"}.get(site, site)
    usual = f"Fever ({where}): {fever_at:.1f} °C or higher"
    text = f"{value:.1f} °C ({where})"
    if value < 35.0:
        return Reading("temperature", "Temperature", text, "Hypothermia", "bad",
                       "Below 35.0 °C is too low",
                       "Warm the person and get medical help.", SOURCES["temp"])
    if value >= fever_at:
        if age_months < 3:
            return Reading("temperature", "Temperature", text, "Fever", "bad", usual,
                           "Any fever in a baby under 3 months needs a doctor today.",
                           SOURCES["temp"])
        high = value >= 40.0
        return Reading("temperature", "Temperature", text,
                       "High fever" if high else "Fever", "bad" if high else "warn", usual,
                       "See a doctor if it lasts over 2 days, or with a stiff neck, rash, "
                       "confusion, or trouble breathing." , SOURCES["temp"])
    return Reading("temperature", "Temperature", text, "Normal", "good", usual, "",
                   SOURCES["temp"])


def _spo2(value: float) -> Reading:
    text = f"{value:g}%"
    usual = "Usual at sea level: 95–100%"
    if value < 90:
        return Reading("spo2", "Oxygen saturation", text, "Very low", "bad", usual,
                       "Below 90% needs urgent medical care (oxygen).", SOURCES["spo2"])
    if value < 95:
        return Reading("spo2", "Oxygen saturation", text, "Low", "warn", usual,
                       "Recheck with a warm, still finger. Below 94% with breathing "
                       "difficulty needs a doctor now.", SOURCES["spo2"])
    return Reading("spo2", "Oxygen saturation", text, "Normal", "good", usual, "",
                   SOURCES["spo2"])


class VitalSignsChecker:
    def check(self, age_years: int, age_months: int = 0, sex: str = "male",
              systolic: float = 0, diastolic: float = 0, pulse: float = 0,
              breathing: float = 0, temperature: float = 0, temp_site: str = "oral",
              spo2: float = 0, bp_standard: str = "ph") -> VitalsResult:
        """A value of 0 means "not measured" and is left out."""
        months = max(0, int(age_years) * 12 + int(age_months))
        group, breathing_range, pulse_range = _group(months)
        child = months < 216
        readings: list[Reading] = []

        if systolic and diastolic:
            if child:
                label, tone, usual, note = _child_bp(systolic, diastolic, months, sex)
                source = SOURCES["bp_child"]
            else:
                label, tone, usual, note = _adult_bp(systolic, diastolic, bp_standard)
                source = SOURCES["bp_aha" if bp_standard == "aha" else "bp_ph"]
            readings.append(Reading("bp", "Blood pressure", f"{systolic:g}/{diastolic:g} mmHg",
                                    label, tone, usual, note, source))
        rates_source = SOURCES["rates_child" if child else "rates_adult"]
        if pulse:
            readings.append(_rate("pulse", "Pulse", pulse, "per min", pulse_range,
                                  "Slow", "Fast", rates_source,
                                  "" if child else "A slow pulse can be normal in fit adults."))
        if breathing:
            readings.append(_rate("breathing", "Breathing rate", breathing, "per min",
                                  breathing_range, "Slow", "Fast", rates_source))
        if temperature:
            readings.append(_temperature(temperature, temp_site, months))
        if spo2:
            readings.append(_spo2(spo2))

        if not readings:
            return VitalsResult(group, (), "Enter a reading", "info",
                                "Fill in any of the readings on the left; leave the rest at "
                                "“Not measured”.")
        worst = max(readings, key=lambda r: TONE_ORDER[r.tone])
        flagged = [r for r in readings if r.tone in ("warn", "bad")]
        if worst.tone == "bad":
            overall = "Needs attention"
            advice = ("At least one reading is well outside the usual range. Measure again "
                      "at rest; if it stays there, or the person feels unwell, see a doctor.")
        elif flagged:
            overall = f"{len(flagged)} outside the usual range"
            advice = ("Measure again after 5 minutes of rest. One reading outside the range "
                      "is common; a pattern over several days is what matters.")
        else:
            overall = "All in the usual range"
            advice = "Every reading entered is within the usual range for this age."
        return VitalsResult(group, tuple(readings), overall, worst.tone, advice)
