"""Business rules for the disease encyclopedia.

Search, filtering and sorting live here rather than in the view, so the same
rules apply whether the caller is the grid, the global search box, or a test.

The repository is injected. By default it is now CachedDiseaseRepository,
which reads from a local copy and syncs from Supabase in the background.
Nothing in this class changed to make that work beyond the default below —
which is the point of having a repository layer.
"""

from typing import Optional

from app.models.disease import BodySystem, Disease
from app.repositories.cached_disease_repository import CachedDiseaseRepository

SEVERITY_ORDER = {"Mild": 0, "Moderate": 1, "Severe": 2, "Critical": 3}

URGENCY_ORDER = {
    "SELF_CARE": 0,
    "SEE_DOCTOR_SOON": 1,
    "SEEK_URGENT_CARE": 2,
    "EMERGENCY": 3,
}


class DiseaseService:
    """Query and filter the disease reference set."""

    def __init__(self, repository: Optional[object] = None) -> None:
        self._repository = repository or CachedDiseaseRepository()

    # --------------------------------------------------------------- reads

    def all_diseases(self) -> list[Disease]:
        """Every condition, sorted by name, so this agrees with search()."""
        return sorted(self._repository.all_diseases(), key=lambda d: d.name.lower())

    def get(self, disease_id: str) -> Optional[Disease]:
        return self._repository.get_disease(disease_id)

    def body_systems(self) -> list[BodySystem]:
        return sorted(self._repository.all_body_systems(), key=lambda s: s.name)

    def body_system_name(self, system_id: str) -> str:
        system = self._repository.get_body_system(system_id)
        return system.name if system else "Unclassified"

    def count(self) -> int:
        return self._repository.count()

    def stats(self) -> dict[str, int]:
        return self._repository.stats()

    # ---------------------------------------------------------------- sync

    def reload(self) -> None:
        """Re-read the local copy into memory. Fast; no network."""
        self._repository.reload()

    def sync(self, force: bool = False) -> bool:
        """Refresh the local copy from Supabase. Returns True if it changed.

        Blocking — call from SyncWorker, never the UI thread.
        """
        return self._repository.sync(force=force)

    def has_local_copy(self) -> bool:
        is_empty = getattr(self._repository, "is_empty", None)
        return not is_empty() if callable(is_empty) else True

    # ------------------------------------------------------------ querying

    def search(
            self,
            query: str = "",
            body_system_id: Optional[str] = None,
            severity: Optional[str] = None,
            urgency: Optional[str] = None,
            sort_by: str = "name",
    ) -> list[Disease]:
        """Filters combine with AND; empty or None means no constraint."""
        results = self._repository.all_diseases()

        if query:
            results = [d for d in results if d.matches(query)]
        if body_system_id:
            results = [d for d in results if d.body_system_id == body_system_id]
        if severity:
            results = [d for d in results if d.severity == severity]
        if urgency:
            results = [d for d in results if d.urgency == urgency]

        return self._sort(results, sort_by)

    @staticmethod
    def _sort(diseases: list[Disease], sort_by: str) -> list[Disease]:
        if sort_by == "severity":
            return sorted(
                diseases, key=lambda d: SEVERITY_ORDER.get(d.severity, 0), reverse=True
            )
        if sort_by == "urgency":
            return sorted(
                diseases,
                key=lambda d: URGENCY_ORDER.get(d.urgency or "", -1),
                reverse=True,
            )
        if sort_by == "views":
            return sorted(diseases, key=lambda d: d.views_count, reverse=True)
        return sorted(diseases, key=lambda d: d.name.lower())

    # ------------------------------------------------------- filter options

    def severities(self) -> list[str]:
        present = {d.severity for d in self._repository.all_diseases()}
        return sorted(present, key=lambda s: SEVERITY_ORDER.get(s, 0))

    def urgencies(self) -> list[str]:
        """Urgency values actually present. Unassessed conditions are simply
        absent — a gap in the data is not a category to filter by."""
        present = {d.urgency for d in self._repository.all_diseases() if d.urgency}
        return sorted(present, key=lambda u: URGENCY_ORDER.get(u, 0))

    # -------------------------------------------------------- cross-links

    def related_diseases(self, disease: Disease) -> list[Disease]:
        """Resolve related ids; missing ones are skipped, not fatal."""
        by_id = {d.id: d for d in self._repository.all_diseases()}
        return [by_id[i] for i in disease.related_disease_ids if i in by_id]

    def group_by_body_system(self) -> dict[str, list[Disease]]:
        grouped: dict[str, list[Disease]] = {}
        for disease in self._repository.all_diseases():
            key = self.body_system_name(disease.body_system_id)
            grouped.setdefault(key, []).append(disease)
        for diseases in grouped.values():
            diseases.sort(key=lambda d: d.name.lower())
        return dict(sorted(grouped.items()))