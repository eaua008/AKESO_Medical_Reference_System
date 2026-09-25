"""Domain model for the Symptom Encyclopedia (7-part clinical entry).

Follows the reference build's SymptomModel: every entry carries a diagnostic
weight from 1 to 10 with its justification, and the weight decides the
priority tier shown on the card and in the monograph.

Associated conditions come from the disease_symptoms join table, so section 5
always agrees with the Disease Encyclopedia instead of being typed twice.
"""

import json
from dataclasses import asdict, dataclass, field

# Weight bands, matching the reference build.
TIERS = (
    ("critical", "Tier 1 Critical", 9, 10),
    ("high", "Tier 2 High", 7, 8),
    ("moderate", "Tier 3 Moderate", 5, 6),
    ("mild", "Tier 4 Mild", 1, 4),
)


@dataclass
class SymptomReference:
    """A citation. is_mother_book marks the Tier 1 primary textbook."""

    source_name: str
    citation_text: str = ""
    url: str = ""
    is_mother_book: bool = False


@dataclass
class AssociatedCondition:
    """A disease in the encyclopedia that presents with this symptom."""

    disease_id: str
    name: str
    severity: str = ""
    is_primary: bool = False


@dataclass
class Symptom:
    id: str
    name: str
    scientific_name: str = ""
    description: str = ""
    body_system_id: str = ""
    body_system_name: str = ""
    is_red_flag: bool = False
    diagnostic_weight: int = 5
    weight_rationale: str = ""
    source_attribution: str = ""
    tags: list[str] = field(default_factory=list)
    causes: list[str] = field(default_factory=list)
    red_flags: list[str] = field(default_factory=list)
    references: list[SymptomReference] = field(default_factory=list)
    conditions: list[AssociatedCondition] = field(default_factory=list)

    @property
    def system_label(self) -> str:
        """Symptoms like fever belong to no single organ system."""
        return self.body_system_name or "Systemic / General"

    @property
    def tier_key(self) -> str:
        return self._tier()[0]

    @property
    def tier_label(self) -> str:
        return self._tier()[1]

    def _tier(self) -> tuple:
        for tier in TIERS:
            if tier[2] <= self.diagnostic_weight <= tier[3]:
                return tier
        return TIERS[-1]

    @property
    def mother_book(self):
        return next((r for r in self.references if r.is_mother_book), None)

    @property
    def supporting_references(self) -> list[SymptomReference]:
        return [r for r in self.references if not r.is_mother_book]


# ---------------------------------------------------- cache serialisation

def symptom_to_json(symptom: Symptom) -> str:
    return json.dumps(asdict(symptom))


def symptom_from_json(text: str) -> Symptom:
    """Rebuild a Symptom, turning nested dicts back into dataclasses."""
    data = json.loads(text)
    data["references"] = [SymptomReference(**r) for r in data.get("references", [])]
    data["conditions"] = [AssociatedCondition(**c) for c in data.get("conditions", [])]
    known = set(Symptom.__dataclass_fields__)
    return Symptom(**{k: v for k, v in data.items() if k in known})