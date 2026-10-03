"""A case study: a hypothetical scenario built for studying interactions.

This is deliberately NOT a patient record. Akeso is a reference platform,
so a case is a teaching scenario ("Elderly patient on an anticoagulant with
liver disease"): which drug is being evaluated, which drugs the scenario is
already on, and which comorbidities it has. Only medicine and condition ids
from the reference data are stored, never a real person's details.

The verdict is not stored. It is worked out again from the current reference
data whenever a case is shown, so a saved case never shows an outdated result
after the database is corrected or extended.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime

# Tag suggestions offered in the Save dialog. UI labels only; any tag can
# be typed.
SUGGESTED_TAGS = ("Pharmacology", "Cardiology", "Nephrology", "Geriatrics",
                  "Gastroenterology", "Primary Care", "Pediatrics", "Infectious Disease")


def new_id() -> str:
    return uuid.uuid4().hex


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class CaseStudy:
    id: str
    title: str
    candidate_id: str = ""
    regimen_ids: list[str] = field(default_factory=list)     # medicine ids
    condition_ids: list[str] = field(default_factory=list)   # patient_conditions ids
    tags: list[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = ""

    @property
    def saved_on(self) -> str:
        return self.created_at[:10]
