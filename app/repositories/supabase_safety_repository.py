"""Drug-safety reference data, read from Supabase.

Five small requests for the whole reference set, whatever its size. The
rule members come embedded in their rule (PostgREST follows the foreign key
from interaction_rule_members.rule_id), so rules cost one request, not one
per rule.

Like the medicine repository, the app doesn't read this during normal use:
it reads the local copy, and the background sync uses this to refresh it.

Empty tables are fine. You plan to wipe and re-enter the data, so every
list here may legitimately come back empty.
"""

from typing import Optional

from supabase import Client, create_client

from app.core.config import config
from app.models.drug_safety import (
    ConditionSafety,
    DrugInteraction,
    InteractionRule,
    PatientCondition,
    RuleMember,
    SafetyReference,
)
from app.repositories.supabase_disease_repository import DiseaseRepositoryError


class SafetyRepositoryError(DiseaseRepositoryError):
    """Subclass, so the existing SyncWorker already handles it."""


class SupabaseSafetyRepository:
    def __init__(self, client: Optional[Client] = None) -> None:
        self._client = client or create_client(config.supabase_url, config.supabase_key)

    def content_version(self) -> int:
        try:
            rows = (self._client.table("content_version")
                    .select("version").eq("id", 1).limit(1).execute().data or [])
        except Exception as exc:
            raise SafetyRepositoryError(f"Could not check for updates: {exc}") from exc
        return int(rows[0]["version"]) if rows else 0

    def fetch_all(self) -> SafetyReference:
        try:
            conditions = (self._client.table("patient_conditions").select("*")
                          .eq("is_published", True).order("sort_order")
                          .execute().data or [])
            safety = (self._client.table("medicine_condition_safety").select("*")
                      .execute().data or [])
            pairs = (self._client.table("drug_interactions").select("*")
                     .eq("is_published", True).execute().data or [])
            rules = (self._client.table("interaction_rules")
                     .select("*, interaction_rule_members(medicine_id, drug_class_keyword)")
                     .eq("is_published", True).execute().data or [])
        except Exception as exc:
            raise SafetyRepositoryError(
                f"Could not download the drug-safety reference: {exc}") from exc

        return SafetyReference(
            conditions=[
                PatientCondition(
                    id=row["id"],
                    label=row.get("label", ""),
                    description=row.get("description") or "",
                    match_keywords=list(row.get("match_keywords") or []),
                    sort_order=int(row.get("sort_order") or 0),
                )
                for row in conditions
            ],
            condition_safety=[
                ConditionSafety(
                    medicine_id=row["medicine_id"],
                    condition_id=row["condition_id"],
                    safety=row.get("safety") or "caution",
                    summary=row.get("summary") or "",
                    guidance=row.get("guidance") or "",
                    source_attribution=row.get("source_attribution") or "",
                )
                for row in safety
            ],
            interactions=[
                DrugInteraction(
                    medicine_a_id=row["medicine_a_id"],
                    medicine_b_id=row["medicine_b_id"],
                    severity=row.get("severity") or "caution",
                    description=row.get("description") or "",
                    clinical_significance=row.get("clinical_significance") or "",
                    recommendation=row.get("recommendation") or "",
                    source_attribution=row.get("source_attribution") or "",
                )
                for row in pairs
            ],
            rules=[
                InteractionRule(
                    id=row["id"],
                    name=row.get("name", ""),
                    severity=row.get("severity") or "caution",
                    description=row.get("description") or "",
                    clinical_significance=row.get("clinical_significance") or "",
                    recommendation=row.get("recommendation") or "",
                    required_condition_id=row.get("required_condition_id") or "",
                    source_attribution=row.get("source_attribution") or "",
                    members=[
                        RuleMember(medicine_id=m.get("medicine_id") or "",
                                   drug_class_keyword=m.get("drug_class_keyword") or "")
                        for m in (row.get("interaction_rule_members") or [])
                    ],
                )
                for row in rules
            ],
        )
