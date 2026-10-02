"""Reference data for the Medication & Drug Safety module.

Everything here is PUBLIC reference data, read from Supabase and cached
offline like the medicine monographs. Nothing about a patient lives here:
their courses, current meds and past checks are a separate, encrypted store.

    PatientCondition        one health-profile checkbox (Hypertension, ...)
    ConditionSafety         medicine X in condition Y: safe / caution / avoid
    DrugInteraction         one drug PAIR, stored once in alphabetical order
    InteractionRule         a risk needing 3+ drugs, a drug class, or a
    RuleMember                drug plus a condition
    SafetyReference         the whole bundle, synced and cached as one unit

Severity values match the Postgres enum condition_safety exactly.
"""

import json
from dataclasses import asdict, dataclass, field
from typing import Optional

SAFE, CAUTION, AVOID = "safe", "caution", "avoid"

# Worst wins when findings are combined: one "avoid" makes the whole check
# "avoid". Higher number = more serious.
SEVERITY_RANK = {SAFE: 0, CAUTION: 1, AVOID: 2}


def pair_key(medicine_id_1: str, medicine_id_2: str) -> tuple[str, str]:
    """The two ids in alphabetical order, the way drug_interactions stores them.

    The table's CHECK constraint forces medicine_a_id < medicine_b_id, so
    every lookup must sort first or it would miss half the pairs.
    """
    return (medicine_id_1, medicine_id_2) if medicine_id_1 < medicine_id_2 \
        else (medicine_id_2, medicine_id_1)


@dataclass
class PatientCondition:
    id: str
    label: str
    description: str = ""
    match_keywords: list[str] = field(default_factory=list)
    sort_order: int = 0


@dataclass
class ConditionSafety:
    medicine_id: str
    condition_id: str
    safety: str
    summary: str = ""
    guidance: str = ""
    source_attribution: str = ""


@dataclass
class DrugInteraction:
    medicine_a_id: str
    medicine_b_id: str
    severity: str
    description: str
    clinical_significance: str = ""
    recommendation: str = ""
    source_attribution: str = ""

    @property
    def key(self) -> tuple[str, str]:
        return (self.medicine_a_id, self.medicine_b_id)


@dataclass
class RuleMember:
    """Exactly one of the two is set (the table's CHECK constraint)."""

    medicine_id: str = ""
    drug_class_keyword: str = ""

    def matches(self, medicine_id: str, drug_class: str) -> bool:
        if self.medicine_id:
            return self.medicine_id == medicine_id
        return self.drug_class_keyword.lower() in (drug_class or "").lower()


@dataclass
class InteractionRule:
    id: str
    name: str
    severity: str
    description: str
    clinical_significance: str = ""
    recommendation: str = ""
    required_condition_id: str = ""
    source_attribution: str = ""
    members: list[RuleMember] = field(default_factory=list)


@dataclass
class SafetyReference:
    """Everything the safety check reads, as one cached bundle."""

    conditions: list[PatientCondition] = field(default_factory=list)
    condition_safety: list[ConditionSafety] = field(default_factory=list)
    interactions: list[DrugInteraction] = field(default_factory=list)
    rules: list[InteractionRule] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.conditions or self.condition_safety
                    or self.interactions or self.rules)

    def interaction_for(self, medicine_id_1: str,
                        medicine_id_2: str) -> Optional[DrugInteraction]:
        key = pair_key(medicine_id_1, medicine_id_2)
        return next((i for i in self.interactions if i.key == key), None)

    def safety_for(self, medicine_id: str,
                   condition_id: str) -> Optional[ConditionSafety]:
        return next((s for s in self.condition_safety
                     if s.medicine_id == medicine_id
                     and s.condition_id == condition_id), None)


# ---------------------------------------------------- cache serialisation

def reference_to_json(reference: SafetyReference) -> str:
    return json.dumps(asdict(reference), ensure_ascii=False)


def reference_from_json(text: str) -> SafetyReference:
    data = json.loads(text)
    return SafetyReference(
        conditions=[PatientCondition(**c) for c in data.get("conditions", [])],
        condition_safety=[ConditionSafety(**s) for s in data.get("condition_safety", [])],
        interactions=[DrugInteraction(**i) for i in data.get("interactions", [])],
        rules=[
            InteractionRule(**{**r, "members": [RuleMember(**m) for m in r.get("members", [])]})
            for r in data.get("rules", [])
        ],
    )
