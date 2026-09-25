"""Disease data access backed by Supabase — the source of truth.

The app no longer reads from this directly during normal use. It reads a
local copy (CachedDiseaseRepository), and this class is what the background
sync uses to refresh that copy.

Two ways in:

  fetch_all_hydrated()  every condition with every child table attached.
                        Each child table is queried ONCE for all conditions
                        and grouped locally, so it costs about 11 requests
                        whether there are 6 conditions or 600. Hydrating one
                        condition at a time would cost 10 per condition.

  content_version()     one small read. Tells the sync whether anything
                        changed since the local copy was made.

It keeps the older single-condition interface too, so it still works as a
drop-in repository on its own.
"""

from collections import defaultdict
from typing import Optional

from supabase import Client, create_client

from app.core.config import config
from app.models.disease import (
    BodySystem,
    ClinicalReference,
    Differential,
    Disease,
    Medicine,
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

    # ------------------------------------------------------ light loading

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.reload()

    def reload(self) -> None:
        """Fetch the light condition list: scalar columns plus tags."""
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
            BodySystem(
                id=row["id"],
                name=row["name"],
                description=row.get("description") or "",
                icon_name=row.get("icon_name") or "",
            )
            for row in (systems.data or [])
        ]
        system_names = {s.id: s.name for s in self._body_systems}

        tags_by_disease: dict[str, list[str]] = defaultdict(list)
        for row in tags.data or []:
            tags_by_disease[row["disease_id"]].append(row["tag"])

        self._diseases = []
        for row in diseases.data or []:
            disease = Disease.from_dict(row)
            disease.tags = tags_by_disease.get(disease.id, [])
            disease.body_system_name = system_names.get(
                disease.body_system_id, "Unclassified"
            )
            self._diseases.append(disease)

        self._loaded = True

    # ------------------------------------------------------ bulk hydration

    def fetch_all_hydrated(self) -> tuple[list[Disease], list[BodySystem]]:
        """Every published condition, fully populated, in about 11 requests.

        The pattern: fetch a whole child table once, filtered to the
        condition ids, then group rows by disease_id in Python. Request count
        stays constant as the encyclopedia grows.
        """
        self.reload()
        ids = [d.id for d in self._diseases]
        if not ids:
            return [], list(self._body_systems)

        try:
            causes = self._grouped_text("disease_causes", ids)
            risks = self._grouped_text("disease_risk_factors", ids)
            tests = self._grouped_text("disease_recommended_tests", ids)
            treatments = self._grouped_text("disease_treatments", ids)
            home_care = self._grouped_text("disease_home_care", ids)
            red_flags = self._grouped_text("disease_emergency_signs", ids)

            prevention = self._rows("disease_prevention", ids, order="position")
            differentials = self._rows("disease_differentials", ids, order="position")
            references = self._rows("clinical_references", ids, order="position")
            # Embedded joins: the link row plus the joined record's fields, in
            # the same request.
            symptoms = self._rows(
                "disease_symptoms", ids, select="*, symptoms(id, name, is_red_flag)"
            )
            medicines = self._rows(
                "disease_medicines",
                ids,
                select="*, medicines(id, name, generic_name, drug_class, category)",
                order="position",
            )
            related = self._rows(
                "disease_related", ids, select="disease_id, related_disease_id"
            )
        except Exception as exc:
            raise DiseaseRepositoryError(
                f"Could not download the full encyclopedia: {exc}"
            ) from exc

        flat_prev: dict[str, list[str]] = defaultdict(list)
        tiered_prev: dict[str, dict[str, list[str]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for row in prevention:
            if row.get("tier"):
                tiered_prev[row["disease_id"]][row["tier"]].append(row["content"])
            else:
                flat_prev[row["disease_id"]].append(row["content"])

        ddx: dict[str, list[Differential]] = defaultdict(list)
        for row in differentials:
            ddx[row["disease_id"]].append(
                Differential(
                    condition=row["condition"],
                    distinguishing_feature=row["distinguishing_feature"],
                )
            )

        refs: dict[str, list[ClinicalReference]] = defaultdict(list)
        for row in references:
            refs[row["disease_id"]].append(ClinicalReference.from_dict(row))

        links: dict[str, list[SymptomLink]] = defaultdict(list)
        for row in symptoms:
            links[row["disease_id"]].append(SymptomLink.from_dict(row))

        meds: dict[str, list[Medicine]] = defaultdict(list)
        for row in medicines:
            meds[row["disease_id"]].append(Medicine.from_dict(row))

        rel: dict[str, list[str]] = defaultdict(list)
        for row in related:
            rel[row["disease_id"]].append(row["related_disease_id"])

        for disease in self._diseases:
            did = disease.id
            disease.causes = causes.get(did, [])
            disease.risk_factors = risks.get(did, [])
            disease.recommended_tests = tests.get(did, [])
            disease.treatments = treatments.get(did, [])
            disease.home_care = home_care.get(did, [])
            disease.emergency_warning_signs = red_flags.get(did, [])
            disease.prevention = flat_prev.get(did, [])
            disease.prevention_tiers = dict(tiered_prev.get(did, {}))
            disease.differential_diagnosis = ddx.get(did, [])
            disease.clinical_references = refs.get(did, [])
            # Cardinal signs first, then by intensity — scan order.
            disease.symptoms = sorted(
                links.get(did, []),
                key=lambda s: (not s.is_primary, -s.typical_intensity),
            )
            disease.medicines = meds.get(did, [])
            disease.related_disease_ids = rel.get(did, [])

        return list(self._diseases), list(self._body_systems)

    def _rows(
            self,
            table: str,
            ids: list[str],
            select: str = "*",
            order: Optional[str] = None,
    ) -> list[dict]:
        query = self._client.table(table).select(select).in_("disease_id", ids)
        if order:
            query = query.order(order)
        return query.execute().data or []

    def _grouped_text(self, table: str, ids: list[str]) -> dict[str, list[str]]:
        """An ordered text list for every condition, in one request."""
        grouped: dict[str, list[str]] = defaultdict(list)
        for row in self._rows(
                table, ids, select="disease_id, content, position", order="position"
        ):
            grouped[row["disease_id"]].append(row["content"])
        return grouped

    # ----------------------------------------------------- sync metadata

    def content_version(self) -> int:
        """The current content watermark. One tiny request."""
        try:
            response = (
                self._client.table("content_version")
                .select("version")
                .eq("id", 1)
                .limit(1)
                .execute()
            )
        except Exception as exc:
            raise DiseaseRepositoryError(
                f"Could not check for encyclopedia updates: {exc}"
            ) from exc
        rows = response.data or []
        return int(rows[0]["version"]) if rows else 0

    def stats(self) -> dict[str, int]:
        """Row counts. head=True returns the count only, no rows."""
        def count(table: str) -> int:
            response = (
                self._client.table(table)
                .select("id", count="exact", head=True)
                .execute()
            )
            return response.count or 0

        try:
            return {
                "body_systems": count("body_systems"),
                "diseases": count("diseases"),
                "symptoms": count("symptoms"),
            }
        except Exception as exc:
            raise DiseaseRepositoryError(
                f"Could not read encyclopedia counts: {exc}"
            ) from exc

    # ------------------------------------------- single-condition interface

    def all_diseases(self) -> list[Disease]:
        self._ensure_loaded()
        return list(self._diseases)

    def all_body_systems(self) -> list[BodySystem]:
        self._ensure_loaded()
        return list(self._body_systems)

    def get_body_system(self, system_id: str) -> Optional[BodySystem]:
        self._ensure_loaded()
        return next((s for s in self._body_systems if s.id == system_id), None)

    def count(self) -> int:
        self._ensure_loaded()
        return len(self._diseases)

    def get_disease(self, disease_id: str) -> Optional[Disease]:
        """One condition, fully hydrated. Reuses the bulk path."""
        diseases, _ = self.fetch_all_hydrated()
        return next((d for d in diseases if d.id == disease_id), None)