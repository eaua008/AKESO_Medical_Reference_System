"""Inputs and results for the Symptom Correlation Engine.

Plain dataclasses: the engine takes these, returns these, and never touches a
widget or the database. That is what makes the scoring testable on its own.
"""

from dataclasses import dataclass, field
from typing import Optional

# Per-symptom clinical parameters, as offered in the UI.
ONSETS = (("sudden", "Sudden"), ("gradual", "Gradual"))
PATTERNS = (("constant", "Constant"), ("intermittent", "Intermittent"),
            ("migratory", "Migratory"), ("exertional", "On exertion"))
TRENDS = (("worsening", "Worsening"), ("stable", "Stable"), ("improving", "Improving"))
DURATIONS = (("today", "Today"), ("few_days", "2 - 5 days"),
             ("week", "About a week"), ("weeks", "2 - 4 weeks"),
             ("month_plus", "Over a month"))

# Exposure and history toggles. keywords are matched against the condition's
# own text, so a new disease gets the right boosters without code changes.
EXPOSURES = (
    ("mosquito", "Mosquito / insect bite",
     ("mosquito", "aedes", "vector", "dengue", "malaria", "chikungunya")),
    ("sick_contact", "Contact with a sick person", ("contagious",)),
    ("outbreak", "Fever in the community", ("outbreak", "epidemic", "contagious")),
    ("new_medication", "New medication in the last 14 days",
     ("drug", "medication", "adverse")),
)
# Symptoms whose severity is genuinely a pain rating get the NRS 0-10 boxes.
# Everything else (fever, cough, rash) gets a plain intensity slider: a
# "pain scale" for a temperature reading is meaningless.
PAIN_KEYWORDS = ("pain", "ache", "aching", "stiff", "cramp", "sore", "tender",
                 "headache", "colic", "burning", "arthralgia", "myalgia")

# First-degree family history. The multiplier is applied when the condition's
# own text matches the keywords, so it stays data-driven.
FAMILY_RISKS = (
    ("fh_diabetes", "Diabetes Mellitus", "Endocrine", 1.18,
     ("diabet", "glycemic", "insulin")),
    ("fh_hypertension", "Essential Hypertension", "Cardiovascular", 1.15,
     ("hypertension", "blood pressure")),
    ("fh_cad", "Early Coronary Artery Disease", "Cardiovascular", 1.25,
     ("coronary", "myocardial", "ischemi", "angina")),
    ("fh_autoimmune", "Autoimmune Disease (SLE/RA)", "Immunological", 1.22,
     ("autoimmune", "lupus", "rheumatoid")),
    ("fh_asthma", "Atopic Triad / Asthma", "Respiratory", 1.15,
     ("asthma", "atopic", "allerg")),
    ("fh_malignancy", "Familial Malignancy", "Oncology", 1.20,
     ("cancer", "malignan", "carcinoma", "lymphoma")),
)

COMORBIDITIES = (
    ("hypertension", "Hypertension", ("hypertension", "blood pressure")),
    ("diabetes", "Diabetes mellitus", ("diabetes", "glycemic", "glucose")),
    ("asthma", "Asthma or COPD", ("asthma", "copd", "bronch")),
    ("autoimmune", "Autoimmune condition", ("autoimmune", "immune", "lupus")),
    ("pregnant", "Currently pregnant", ("pregnan",)),
)


def is_pain_symptom(name: str, tags=()) -> bool:
    """Does a 0-10 pain rating make sense for this symptom?"""
    text = " ".join((name, *tags)).lower()
    return any(word in text for word in PAIN_KEYWORDS)


@dataclass
class SelectedSymptom:
    """One symptom the user reported, with its clinical parameters."""

    symptom_id: str
    name: str
    intensity: int = 5          # NRS 0 - 10
    onset: str = "sudden"
    pattern: str = "constant"
    trend: str = "worsening"
    duration: str = "few_days"


@dataclass
class Vitals:
    temperature: float = 37.0   # °C
    heart_rate: int = 75
    bp_systolic: int = 120
    bp_diastolic: int = 80
    spo2: int = 98
    resp_rate: int = 18


@dataclass
class CheckerInput:
    symptoms: list[SelectedSymptom] = field(default_factory=list)
    vitals: Vitals = field(default_factory=Vitals)
    age: int = 30
    sex: str = "female"
    exposures: set[str] = field(default_factory=set)
    comorbidities: set[str] = field(default_factory=set)
    family_history: set[str] = field(default_factory=set)


@dataclass
class MatchedSymptom:
    """One hallmark the user reported, next to what the condition expects."""

    name: str
    user_intensity: int
    typical_intensity: int
    is_primary: bool
    onset: str
    pattern: str
    trend: str


@dataclass
class MatchResult:
    disease_id: str
    name: str
    scientific_name: str
    score: float                        # 0 - 98, the correlation percentage
    urgency: str
    severity: str
    # Uncapped, so two conditions that both hit the cap still order correctly.
    rank_value: float = 0.0
    matched: list[MatchedSymptom] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    inconsistent: list[str] = field(default_factory=list)
    boosters: list[str] = field(default_factory=list)   # why the score was raised
    matched_count: int = 0
    total_hallmarks: int = 0
    weighted_sum: int = 0
    weighted_max: int = 0
    alignment: int = 0                  # how closely intensities matched, %
    emergency_signs: list[str] = field(default_factory=list)

    @property
    def has_primary(self) -> bool:
        return any(m.is_primary for m in self.matched)


@dataclass
class CheckerResult:
    matches: list[MatchResult] = field(default_factory=list)
    triage_level: str = "ROUTINE"
    triage_label: str = ""
    triage_action: str = ""
    triage_rationale: str = ""
    specificity: int = 0
    specificity_label: str = ""
    specificity_guidance: str = ""
    vital_alerts: list[str] = field(default_factory=list)
    emergency_warnings: list[str] = field(default_factory=list)
    suggested_symptoms: list[tuple[str, str, int]] = field(default_factory=list)

    @property
    def top(self) -> Optional[MatchResult]:
        return self.matches[0] if self.matches else None