"""Business rules for the disease encyclopedia.

Search, filtering and sorting live here rather than in the view, so the same
rules apply whether the caller is the desktop grid, a test, or the global
search box in the header.

The repository is injected. Point it at a different repository — local JSON,
a cache, anything with the same method names — and nothing here changes.
"""

from typing import Optional

from app.models.disease import BodySystem, Disease
from app.repositories.supabase_disease_repository import (
    SupabaseDiseaseRepository,
)

# Ordered by clinical urgency, not alphabetically, so "sort by severity"
# means something sensible.
SEVERITY_ORDER = {"Mild": 0, "Moderate": 1, "Severe": 2, "Critical": 3}

# These are the values that actually exist in the data. Note SEEK_URGENT_CARE
# rather than URGENT.
URGENCY_ORDER = {
    "SELF_CARE": 0,
    "SEE_DOCTOR_SOON": 1,
    "SEEK_URGENT_CARE": 2,
    "EMERGENCY": 3,
}


class DiseaseService:
    """Query and filter the disease reference set."""

    def __init__(self, repository: Optional[object] = None) -> None:
        self._repository = repository or SupabaseDiseaseRepository()

    # --------------------------------------------------------------- reads

    def all_diseases(self) -> list[Disease]:
        """Every published condition, sorted by name.

        Sorted so this and search() agree on ordering — an unsorted variant
        here would silently differ from what the grid shows.
        """
        return sorted(
            self._repository.all_diseases(), key=lambda d: d.name.lower()
        )

    def get(self, disease_id: str) -> Optional[Disease]:
        """One condition, fully hydrated with its child tables."""
        return self._repository.get_disease(disease_id)

    def body_systems(self) -> list[BodySystem]:
        return sorted(self._repository.all_body_systems(), key=lambda s: s.name)

    def body_system_name(self, system_id: str) -> str:
        system = self._repository.get_body_system(system_id)
        return system.name if system else "Unclassified"

    def count(self) -> int:
        return self._repository.count()

    def reload(self) -> None:
        """Re-read from the database so newly added rows appear."""
        self._repository.reload()

    # ------------------------------------------------------------ querying

    def search(
            self,
            query: str = "",
            body_system_id: Optional[str] = None,
            severity: Optional[str] = None,
            urgency: Optional[str] = None,
            sort_by: str = "name",
    ) -> list[Disease]:
        """Filter the full set down to what the user asked for.

        Filters combine with AND. Empty or None means "no constraint", so
        calling this with no arguments returns everything sorted by name.
        """
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
            # Descending: most severe first, which is what gets scanned for.
            return sorted(
                diseases,
                key=lambda d: SEVERITY_ORDER.get(d.severity, 0),
                reverse=True,
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
        """Severity values actually present, in clinical order."""
        present = {d.severity for d in self._repository.all_diseases()}
        return sorted(present, key=lambda s: SEVERITY_ORDER.get(s, 0))

    def urgencies(self) -> list[str]:
        """Urgency values actually present, in clinical order.

        Conditions with no authored urgency are simply absent — there is no
        filter option for "unassessed", because that is a gap in the data
        rather than a category.
        """
        present = {
            d.urgency for d in self._repository.all_diseases() if d.urgency
        }
        return sorted(present, key=lambda u: URGENCY_ORDER.get(u, 0))

    # -------------------------------------------------------- cross-links

    def related_diseases(self, disease: Disease) -> list[Disease]:
        """Resolve related IDs into real Disease objects.

        Missing IDs are skipped rather than raising: reference data is
        hand-authored, and one bad cross-link should not break a monograph.
        """
        found = []
        for related_id in disease.related_disease_ids:
            for candidate in self._repository.all_diseases():
                if candidate.id == related_id:
                    found.append(candidate)
                    break
        return found

    def group_by_body_system(self) -> dict[str, list[Disease]]:
        """Conditions bucketed under their body system name."""
        grouped: dict[str, list[Disease]] = {}
        for disease in self._repository.all_diseases():
            key = self.body_system_name(disease.body_system_id)
            grouped.setdefault(key, []).append(disease)

        for diseases in grouped.values():
            diseases.sort(key=lambda d: d.name.lower())
        return dict(sorted(grouped.items()))