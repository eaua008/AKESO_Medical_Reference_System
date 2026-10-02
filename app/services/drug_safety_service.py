"""The Interaction & Safety Check engine.

Three layers, all read from your Supabase reference tables (via the offline
cache). Nothing about any drug is written in this file.

    1. drug + condition    medicine_condition_safety
    2. drug pairs          drug_interactions: the candidate against every
                           ticked current med, AND the current meds against
                           each other (4 drugs = 6 pairs, not 3)
    3. combinations        interaction_rules: 3+ drugs, a drug class, or a
                           drug together with a condition

The overall verdict is the worst finding: one "avoid" makes the whole
check "avoid".

Honesty rule: a pair with no row in the database is NOT reported as safe.
It is "not on record", and if anything was not on record the verdict says
"no flagged risks" instead of "compatible". A missing entry means nobody
has checked it yet, not that it was checked and found safe.
"""

from dataclasses import dataclass, field
from itertools import combinations
from typing import Callable, Iterable, Optional

from app.models.drug_safety import (
    AVOID,
    CAUTION,
    SAFE,
    SEVERITY_RANK,
    ConditionSafety,
    DrugInteraction,
    InteractionRule,
    PatientCondition,
    SafetyReference,
)
from app.repositories.cached_safety_repository import CachedSafetyRepository

UNKNOWN = "unknown"          # no reference row for this pair

# Verdict keys the view draws.
VERDICT_COMPATIBLE = "compatible"      # everything checked and on record as safe
VERDICT_NO_FLAGS = "no_flags"          # nothing flagged, but some pairs not on record
VERDICT_CAUTION = CAUTION
VERDICT_AVOID = AVOID


@dataclass
class Drug:
    """One drug in a check: the candidate or a current med."""

    name: str
    medicine_id: str = ""          # "" when typed freely and not in the database
    drug_class: str = ""
    generic_name: str = ""
    is_candidate: bool = False


@dataclass
class ConditionFinding:
    condition: PatientCondition
    drug: Drug
    severity: str                  # safe / caution / avoid / unknown
    summary: str = ""
    guidance: str = ""


@dataclass
class PairFinding:
    first: Drug
    second: Drug
    severity: str                  # safe / caution / avoid / unknown
    description: str = ""
    clinical_significance: str = ""
    recommendation: str = ""
    duplicate: bool = False        # the same medicine twice

    @property
    def involves_candidate(self) -> bool:
        return self.first.is_candidate or self.second.is_candidate


@dataclass
class RuleFinding:
    rule: InteractionRule
    drugs: list[Drug]


@dataclass
class SafetyReport:
    candidate: Drug
    in_database: bool
    conditions: list[ConditionFinding] = field(default_factory=list)
    pairs: list[PairFinding] = field(default_factory=list)
    rules: list[RuleFinding] = field(default_factory=list)
    not_in_database: list[Drug] = field(default_factory=list)   # current meds we can't check

    @property
    def worst(self) -> str:
        severities = ([c.severity for c in self.conditions] + [p.severity for p in self.pairs]
                      + [r.rule.severity for r in self.rules])
        known = [s for s in severities if s in SEVERITY_RANK]
        return max(known, key=SEVERITY_RANK.get) if known else SAFE

    @property
    def unknown_count(self) -> int:
        return (sum(c.severity == UNKNOWN for c in self.conditions)
                + sum(p.severity == UNKNOWN for p in self.pairs)
                + len(self.not_in_database))

    @property
    def verdict(self) -> str:
        worst = self.worst
        if worst in (AVOID, CAUTION):
            return worst
        return VERDICT_NO_FLAGS if self.unknown_count else VERDICT_COMPATIBLE

    @property
    def candidate_pairs(self) -> list[PairFinding]:
        return [p for p in self.pairs if p.involves_candidate]

    @property
    def regimen_pairs(self) -> list[PairFinding]:
        return [p for p in self.pairs if not p.involves_candidate]


class DrugSafetyService:
    def __init__(self, medicines: Callable[[], Iterable] = list,
                 repository: Optional[CachedSafetyRepository] = None) -> None:
        self._medicines = medicines                  # MedicineService.all_medicines
        self._repository = repository or CachedSafetyRepository()

    # --------------------------------------------------------------- data

    def reference(self) -> SafetyReference:
        return self._repository.reference()

    def conditions(self) -> list[PatientCondition]:
        return sorted(self.reference().conditions, key=lambda c: c.sort_order)

    def drug_for(self, name: str, medicine_id: str = "", is_candidate: bool = False) -> Drug:
        medicine = next((m for m in self._medicines() if m.id == medicine_id), None) \
            if medicine_id else None
        if medicine is None:
            return Drug(name=name, is_candidate=is_candidate)
        return Drug(name=name or medicine.name, medicine_id=medicine.id,
                    drug_class=medicine.drug_class,
                    generic_name=medicine.international_generic_name or medicine.generic_name,
                    is_candidate=is_candidate)

    # ------------------------------------------------------------- engine

    def evaluate(self, candidate: Optional[Drug], regimen: list[Drug],
                 condition_ids: Iterable[str]) -> SafetyReport:
        """Run all three layers. candidate=None checks the regimen on its own
        (that is what the "Drug Safety Check" stat card shows)."""
        ref = self.reference()
        chosen = [c for c in self.conditions() if c.id in set(condition_ids)]
        checkable = [d for d in regimen if d.medicine_id]
        report = SafetyReport(
            candidate=candidate or Drug(name="Current regimen"),
            in_database=bool(candidate and candidate.medicine_id) or candidate is None,
            not_in_database=[d for d in regimen if not d.medicine_id],
        )
        drugs = ([candidate] if candidate and candidate.medicine_id else []) + checkable

        # 1. conditions: every drug in the check, against every ticked condition
        condition_targets = [candidate] if candidate and candidate.medicine_id else checkable
        for condition in chosen:
            for drug in condition_targets:
                row = ref.safety_for(drug.medicine_id, condition.id)
                report.conditions.append(ConditionFinding(
                    condition=condition,
                    drug=drug,
                    severity=row.safety if row else UNKNOWN,
                    summary=row.summary if row else "",
                    guidance=row.guidance if row else "",
                ))

        # 2. every pair among all the drugs in the check
        for first, second in combinations(drugs, 2):
            if first.medicine_id == second.medicine_id:
                report.pairs.append(PairFinding(
                    first, second, CAUTION, duplicate=True,
                    description=f"{second.name} is already in your current regimen.",
                    clinical_significance="Taking the same medicine from two sources can "
                                          "double the dose.",
                    recommendation="Check with your pharmacist before combining."))
                continue
            row = ref.interaction_for(first.medicine_id, second.medicine_id)
            report.pairs.append(PairFinding(
                first, second,
                severity=row.severity if row else UNKNOWN,
                description=row.description if row else "",
                clinical_significance=row.clinical_significance if row else "",
                recommendation=row.recommendation if row else "",
            ))

        # 3. combination rules
        condition_set = {c.id for c in chosen}
        for rule in ref.rules:
            if rule.required_condition_id and rule.required_condition_id not in condition_set:
                continue
            matched = _match_members(rule, drugs)
            if matched is not None:
                report.rules.append(RuleFinding(rule, matched))
        return report

    # ------------------------------------------------ Interaction Browser

    def interactions_for(self, medicine_id: str) -> list[tuple[Drug, DrugInteraction]]:
        """Every documented pair involving this medicine, worst first."""
        out = []
        for row in self.reference().interactions:
            if medicine_id not in row.key:
                continue
            other_id = row.medicine_b_id if row.medicine_a_id == medicine_id \
                else row.medicine_a_id
            other = self.drug_for("", other_id)
            if other.medicine_id:          # skip medicines no longer published
                out.append((other, row))
        return sorted(out, key=lambda p: (-SEVERITY_RANK.get(p[1].severity, 0),
                                          p[0].name.lower()))

    def condition_entries_for(self, medicine_id: str) -> list[tuple[PatientCondition,
                                                                      ConditionSafety]]:
        conditions = {c.id: c for c in self.conditions()}
        out = [(conditions[row.condition_id], row)
               for row in self.reference().condition_safety
               if row.medicine_id == medicine_id and row.condition_id in conditions]
        return sorted(out, key=lambda p: (-SEVERITY_RANK.get(p[1].safety, 0),
                                          p[0].sort_order))

    def rules_for(self, drug: Drug) -> list[InteractionRule]:
        """Rules with at least one member this medicine or its class satisfies."""
        return [rule for rule in self.reference().rules
                if any(m.matches(drug.medicine_id, drug.drug_class) for m in rule.members)]

    def documented_count(self) -> int:
        ref = self.reference()
        return len(ref.interactions) + len(ref.rules)

    # --------------------------------------------------------------- sync

    def reload(self) -> None:
        self._repository.reload()

    def sync(self, force: bool = False) -> bool:
        """Called by SyncWorker on a background thread."""
        return self._repository.sync(force=force)


def _match_members(rule: InteractionRule, drugs: list[Drug]) -> Optional[list[Drug]]:
    """Give every member of the rule its own, different drug, or None.

    A small backtracking search: with two NSAIDs and a rule needing "NSAID +
    ARB", the first NSAID must not be used up by one member while another
    member could only have matched it. Regimens are a handful of drugs, so
    this is instant.
    """
    if not rule.members:
        return None
    used: list[Drug] = []

    def assign(index: int) -> bool:
        if index == len(rule.members):
            return True
        member = rule.members[index]
        for drug in drugs:
            if any(d is drug for d in used) or not member.matches(drug.medicine_id, drug.drug_class):
                continue
            used.append(drug)
            if assign(index + 1):
                return True
            used.pop()
        return False

    return list(used) if assign(0) else None
