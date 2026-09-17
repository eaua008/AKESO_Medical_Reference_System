"""Disease data access backed by Supabase.

Drop-in replacement for DiseaseRepository: same method names, same return
types. DiseaseService does not change, which is the whole point of having a
repository layer.

Two-speed loading, on purpose:

  all_diseases()  returns LIGHT objects — scalar columns plus tags. That is
                  everything the grid card shows, in three queries total.
  get_disease()   returns a FULLY hydrated object, pulling every child table.
                  Costs about nine queries, but only runs when someone opens
                  one monograph.

Fetching every child table for all sixteen conditions just to draw a grid of
cards would be a lot of wasted round trips.

Not yet handled: offline caching. This repository needs the network. The
local cache layer wraps this one later.
"""

from typing import Optional

from supabase import Client, create_client

from app.core.config import config
from app.models.disease import (
    BodySystem,
    ClinicalReference,
    Differential,
    Disease,
    SymptomLink,
)


class DiseaseRepositoryError(Exception):
    """Raised when the reference data cannot be read."""


class SupabaseDiseaseRepository:
    """Reads the encyclopedia from Supabase."""

    def __init__(self, client: Optional[Client] = None) -> None:
        self._client = client or create_client(
            config.supabase_url, config.supabase_key
        )
        self._diseases: list[Disease] = []
        self._body_systems: list[BodySystem] = []
        self._loaded = False

    # ------------------------------------------------------------- loading

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.reload()

    def reload(self) -> None:
        """Re-fetch the light disease list and body systems.

        Call this to pick up rows added to Supabase since the app started —
        it is what makes a newly inserted disease appear in the grid.
        """
        try:
            systems = self._client.table("body_systems").select("*").execute()
            diseases = (
                self._client.table("diseases")
                .select("*")
                .eq("is_published", True)
                .execute()
            )
            tags = self._client.table("disease_tags").select("*").execute()
        except Exception as exc:
            raise DiseaseRepositoryError(
                f"Could not load the encyclopedia from Supabase: {exc}"
            ) from exc

        self._body_systems = [
            self._to_body_system(row) for row in (systems.data or [])
        ]

        # Group tags by disease in one pass rather than querying per disease.
        tags_by_disease: dict[str, list[str]] = {}
        for row in tags.data or []:
            tags_by_disease.setdefault(row["disease_id"], []).append(row["tag"])

        self._diseases = []
        for row in diseases.data or []:
            disease = self._to_disease(row)
            disease.tags = tags_by_disease.get(disease.id, [])
            self._diseases.append(disease)

        self._loaded = True

    # ---------------------------------------------------------- converters

    @staticmethod
    def _to_body_system(row: dict) -> BodySystem:
        return BodySystem(
            id=row["id"],
            name=row["name"],
            description=row.get("description") or "",
            icon_name=row.get("icon_name") or "",
        )

    @staticmethod
    def _to_disease(row: dict) -> Disease:
        """Map one `diseases` row onto the model.

        Columns are snake_case in Postgres and snake_case on the model, so
        this is mostly one-to-one — unlike the JSON repository, which had to
        translate camelCase.
        """
        return Disease(
            id=row["id"],
            name=row["name"],
            scientific_name=row.get("scientific_name") or "",
            description=row.get("description") or "",
            body_system_id=row.get("body_system_id") or "",
            severity=row.get("severity") or "Moderate",
            # Left as None when the column is NULL. Do not substitute a
            # default — an unauthored triage level must not be invented.
            urgency=row.get("urgency"),
            urgency_criteria=row.get("urgency_criteria") or "",
            contagious=row.get("contagious", False),
            views_count=row.get("views_count", 0),
            pathophysiology=row.get("pathophysiology") or "",
            clinicopathologic_correlation=row.get(
                "clinicopathologic_correlation"
            ) or "",
            follow_up_monitoring=row.get("follow_up_monitoring") or "",
            source_attribution=row.get("source_attribution") or "",
        )

    # --------------------------------------------------------------- reads

    def all_diseases(self) -> list[Disease]:
        self._ensure_loaded()
        return list(self._diseases)

    def all_body_systems(self) -> list[BodySystem]:
        self._ensure_loaded()
        return list(self._body_systems)

    def get_body_system(self, system_id: str) -> Optional[BodySystem]:
        self._ensure_loaded()
        for system in self._body_systems:
            if system.id == system_id:
                return system
        return None

    def count(self) -> int:
        self._ensure_loaded()
        return len(self._diseases)

    def get_disease(self, disease_id: str) -> Optional[Disease]:
        """Fetch one disease with every child table attached."""
        self._ensure_loaded()

        base = next((d for d in self._diseases if d.id == disease_id), None)
        if base is None:
            return None

        try:
            disease = self._hydrate(base)
        except Exception as exc:
            raise DiseaseRepositoryError(
                f"Could not load the full monograph for {disease_id}: {exc}"
            ) from exc
        return disease

    def _hydrate(self, disease: Disease) -> Disease:
        """Pull the child tables for one disease."""
        did = disease.id

        disease.causes = self._ordered_list("disease_causes", did)
        disease.risk_factors = self._ordered_list("disease_risk_factors", did)
        disease.recommended_tests = self._ordered_list(
            "disease_recommended_tests", did
        )
        disease.treatments = self._ordered_list("disease_treatments", did)
        disease.home_care = self._ordered_list("disease_home_care", did)
        disease.emergency_warning_signs = self._ordered_list(
            "disease_emergency_signs", did
        )

        # Prevention carries a tier: NULL rows are the flat list, tiered rows
        # are grouped into prevention_tiers.
        prevention = (
            self._client.table("disease_prevention")
            .select("*")
            .eq("disease_id", did)
            .order("position")
            .execute()
        )
        flat: list[str] = []
        tiers: dict[str, list[str]] = {}
        for row in prevention.data or []:
            if row.get("tier"):
                tiers.setdefault(row["tier"], []).append(row["content"])
            else:
                flat.append(row["content"])
        disease.prevention = flat
        disease.prevention_tiers = tiers

        differentials = (
            self._client.table("disease_differentials")
            .select("*")
            .eq("disease_id", did)
            .order("position")
            .execute()
        )
        disease.differential_diagnosis = [
            Differential(
                condition=row["condition"],
                distinguishing_feature=row["distinguishing_feature"],
            )
            for row in differentials.data or []
        ]

        references = (
            self._client.table("clinical_references")
            .select("*")
            .eq("disease_id", did)
            .order("position")
            .execute()
        )
        disease.clinical_references = [
            ClinicalReference(
                id=row["id"],
                source_name=row["source_name"],
                citation_text=row["citation_text"],
            )
            for row in references.data or []
        ]

        symptoms = (
            self._client.table("disease_symptoms")
            .select("*")
            .eq("disease_id", did)
            .execute()
        )
        disease.symptoms = [
            SymptomLink(
                symptom_id=row["symptom_id"],
                typical_intensity=row.get("typical_intensity", 0),
                is_primary=row.get("is_primary", False),
                weight_multiplier=float(row.get("weight_multiplier", 1.0)),
            )
            for row in symptoms.data or []
        ]

        related = (
            self._client.table("disease_related")
            .select("related_disease_id")
            .eq("disease_id", did)
            .execute()
        )
        disease.related_disease_ids = [
            row["related_disease_id"] for row in related.data or []
        ]

        return disease

    def _ordered_list(self, table: str, disease_id: str) -> list[str]:
        """Read one ordered text list, preserving the author's ordering."""
        result = (
            self._client.table(table)
            .select("content, position")
            .eq("disease_id", disease_id)
            .order("position")
            .execute()
        )
        return [row["content"] for row in result.data or []]