"""Medicine data access backed by Supabase.

Four requests for the whole catalogue, whatever its size: the medicines, the
facts, the references, and the disease links. Grouping happens in Python, as
in SupabaseDiseaseRepository.fetch_all_hydrated().

The app doesn't read this during normal use: it reads the local copy, and
the background sync uses this to refresh it.
"""

from collections import defaultdict
from typing import Optional

from supabase import Client, create_client

from app.core.config import config
from app.models.medicine import (
    ADVERSE,
    BRAND_INTL,
    BRAND_PH,
    CONTRAINDICATION,
    INDICATION,
    INTERACTION,
    LinkedCondition,
    MedicineMonograph,
    MedicineReference,
)
from app.repositories.supabase_disease_repository import DiseaseRepositoryError


class MedicineRepositoryError(DiseaseRepositoryError):
    """Subclass, so the existing SyncWorker already handles it."""


class SupabaseMedicineRepository:
    def __init__(self, client: Optional[Client] = None) -> None:
        self._client = client or create_client(config.supabase_url, config.supabase_key)

    def content_version(self) -> int:
        try:
            response = (
                self._client.table("content_version")
                .select("version").eq("id", 1).limit(1).execute()
            )
        except Exception as exc:
            raise MedicineRepositoryError(f"Could not check for updates: {exc}") from exc
        rows = response.data or []
        return int(rows[0]["version"]) if rows else 0

    def fetch_all(self) -> list[MedicineMonograph]:
        try:
            rows = (
                    self._client.table("medicines")
                    .select("*")
                    .eq("is_published", True)
                    .order("name")
                    .execute()
                    .data or []
            )
            ids = [str(row["id"]) for row in rows]
            if not ids:
                return []

            facts = self._rows("medicine_facts", ids,
                               select="medicine_id, kind, content, position",
                               order="position")
            references = self._rows("medicine_references", ids, order="position")
            links = self._rows(
                "disease_medicines", ids,
                select="medicine_id, safety, note, diseases(id, name, severity, is_published)",
            )
        except MedicineRepositoryError:
            raise
        except Exception as exc:
            raise MedicineRepositoryError(f"Could not download medicines: {exc}") from exc

        # kind -> medicine id -> ordered lines
        grouped: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
        for row in facts:
            grouped[row["kind"]][str(row["medicine_id"])].append(row["content"])

        refs: dict[str, list[MedicineReference]] = defaultdict(list)
        for row in references:
            refs[str(row["medicine_id"])].append(MedicineReference(
                source_name=row.get("source_name", ""),
                citation_text=row.get("citation_text") or "",
                url=row.get("url") or "",
                is_mother_book=bool(row.get("is_mother_book")),
            ))

        conditions: dict[str, list[LinkedCondition]] = defaultdict(list)
        for row in links:
            disease = row.get("diseases") or {}
            if not disease or disease.get("is_published") is False:
                continue
            conditions[str(row["medicine_id"])].append(LinkedCondition(
                disease_id=str(disease["id"]),
                name=disease.get("name", ""),
                severity=disease.get("severity") or "",
                safety=row.get("safety") or "",
                note=row.get("note") or "",
            ))

        medicines = []
        for row in rows:
            mid = str(row["id"])
            medicines.append(MedicineMonograph(
                id=mid,
                name=row.get("name", ""),
                generic_name=row.get("generic_name") or "",
                international_generic_name=row.get("international_generic_name") or "",
                drug_class=row.get("drug_class") or "",
                category=row.get("category") or "Prescription",
                dosage_text=row.get("dosage_text") or "",
                storage=row.get("storage") or "",
                black_box_warning=row.get("black_box_warning") or "",
                source_attribution=row.get("source_attribution") or "",
                ph_brands=grouped[BRAND_PH].get(mid, []),
                intl_brands=grouped[BRAND_INTL].get(mid, []),
                indications=grouped[INDICATION].get(mid, []),
                adverse_reactions=grouped[ADVERSE].get(mid, []),
                contraindications=grouped[CONTRAINDICATION].get(mid, []),
                interactions=grouped[INTERACTION].get(mid, []),
                references=refs.get(mid, []),
                conditions=sorted(conditions.get(mid, []), key=lambda c: c.name.lower()),
            ))
        return medicines

    def _rows(self, table: str, ids: list[str], select: str = "*",
              order: Optional[str] = None) -> list[dict]:
        query = self._client.table(table).select(select).in_("medicine_id", ids)
        if order:
            query = query.order(order)
        return query.execute().data or []