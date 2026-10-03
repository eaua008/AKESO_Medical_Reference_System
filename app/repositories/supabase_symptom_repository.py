"""Symptom data access backed by Supabase, the source of truth.

Same approach as SupabaseDiseaseRepository.fetch_all_hydrated(): each child
table is queried ONCE for all symptoms and grouped in Python, so the request
count stays at 5 whether there are 5 symptoms or 500.

The app doesn't read this during normal use. It reads the local copy
(CachedSymptomRepository), and the background sync uses this to refresh it.
"""

from collections import defaultdict
from typing import Optional

from supabase import Client, create_client

from app.core.config import config
from app.models.symptom import AssociatedCondition, Symptom, SymptomReference
from app.repositories.supabase_disease_repository import DiseaseRepositoryError


class SymptomRepositoryError(DiseaseRepositoryError):
    """Subclass, so the existing SyncWorker already knows how to handle it."""


class SupabaseSymptomRepository:
    def __init__(self, client: Optional[Client] = None) -> None:
        self._client = client or create_client(config.supabase_url, config.supabase_key)

    def content_version(self) -> int:
        """Same watermark the disease sync uses. One tiny request."""
        try:
            response = (
                self._client.table("content_version")
                .select("version").eq("id", 1).limit(1).execute()
            )
        except Exception as exc:
            raise SymptomRepositoryError(f"Could not check for symptom updates: {exc}") from exc
        rows = response.data or []
        return int(rows[0]["version"]) if rows else 0

    def fetch_all(self) -> list[Symptom]:
        try:
            rows = (
                    self._client.table("symptoms")
                    # Embedded join through the body_system_id foreign key.
                    .select("*, body_systems(id, name)")
                    .eq("is_published", True)
                    .order("name")
                    .execute()
                    .data or []
            )
            ids = [str(row["id"]) for row in rows]
            if not ids:
                return []

            causes = self._grouped_text("symptom_causes", ids)
            red_flags = self._grouped_text("symptom_red_flags", ids)
            references = self._rows("symptom_references", ids, order="position")
            links = self._rows(
                "disease_symptoms", ids,
                select="symptom_id, is_primary, diseases(id, name, severity, is_published)",
            )
        except SymptomRepositoryError:
            raise
        except Exception as exc:
            raise SymptomRepositoryError(f"Could not download symptoms: {exc}") from exc

        refs_by_symptom: dict[str, list[SymptomReference]] = defaultdict(list)
        for row in references:
            refs_by_symptom[str(row["symptom_id"])].append(SymptomReference(
                source_name=row.get("source_name", ""),
                citation_text=row.get("citation_text") or "",
                url=row.get("url") or "",
                is_mother_book=bool(row.get("is_mother_book")),
            ))

        conditions: dict[str, list[AssociatedCondition]] = defaultdict(list)
        for row in links:
            disease = row.get("diseases") or {}
            # Skip links to diseases that aren't published (or were deleted).
            if not disease or disease.get("is_published") is False:
                continue
            conditions[str(row["symptom_id"])].append(AssociatedCondition(
                disease_id=str(disease["id"]),
                name=disease.get("name", ""),
                severity=disease.get("severity") or "",
                is_primary=bool(row.get("is_primary")),
            ))

        symptoms = []
        for row in rows:
            sid = str(row["id"])
            system = row.get("body_systems") or {}
            symptoms.append(Symptom(
                id=sid,
                name=row.get("name", ""),
                scientific_name=row.get("scientific_name") or "",
                description=row.get("description") or "",
                body_system_id=str(system.get("id") or ""),
                body_system_name=system.get("name") or "",
                is_red_flag=bool(row.get("is_red_flag")),
                diagnostic_weight=int(row.get("diagnostic_weight") or 5),
                weight_rationale=row.get("weight_rationale") or "",
                source_attribution=row.get("source_attribution") or "",
                tags=list(row.get("tags") or []),
                causes=causes.get(sid, []),
                red_flags=red_flags.get(sid, []),
                references=refs_by_symptom.get(sid, []),
                # Primary-symptom conditions first, then alphabetical.
                conditions=sorted(conditions.get(sid, []),
                                  key=lambda c: (not c.is_primary, c.name.lower())),
            ))
        return symptoms

    # ------------------------------------------------------------ helpers

    def _rows(self, table: str, ids: list[str], select: str = "*",
              order: Optional[str] = None) -> list[dict]:
        query = self._client.table(table).select(select).in_("symptom_id", ids)
        if order:
            query = query.order(order)
        return query.execute().data or []

    def _grouped_text(self, table: str, ids: list[str]) -> dict[str, list[str]]:
        grouped: dict[str, list[str]] = defaultdict(list)
        for row in self._rows(table, ids, select="symptom_id, content, position", order="position"):
            grouped[str(row["symptom_id"])].append(row["content"])
        return grouped