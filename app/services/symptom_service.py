"""Business rules for the Symptom Encyclopedia: lookups and filtering.

No widgets and no database here, so filtering can be tested on its own.
"""

from typing import Optional

from app.models.symptom import TIERS, Symptom
from app.repositories.cached_symptom_repository import CachedSymptomRepository


class SymptomService:
    def __init__(self, repository: Optional[object] = None) -> None:
        self._repository = repository or CachedSymptomRepository()

    # ------------------------------------------------------------- reads

    def all_symptoms(self) -> list[Symptom]:
        return self._repository.all()

    def get(self, symptom_id: str) -> Optional[Symptom]:
        return next((s for s in self.all_symptoms() if s.id == symptom_id), None)

    def body_systems(self) -> list[tuple[str, str]]:
        """(id, label) pairs for the filter, only systems that have symptoms.

        "General" (no system) uses the id "general".
        """
        systems = {}
        for s in self.all_symptoms():
            systems[s.body_system_id or "general"] = s.system_label
        return sorted(systems.items(), key=lambda item: item[1].lower())

    def tiers(self) -> list[tuple[str, str]]:
        """(key, label) for the algorithmic-weight filter."""
        return [(key, f"{label} ({low}\u2013{high}/10)") for key, label, low, high in TIERS]

    def search(self, query: str = "", system_id: str = "",
               tier_key: str = "") -> list[Symptom]:
        """Symptoms matching every word of the query, plus the filters.

        Results are ordered by diagnostic weight, so the entries that matter
        most clinically are read first.
        """
        words = query.lower().split()
        results = []
        for s in self.all_symptoms():
            if system_id and (s.body_system_id or "general") != system_id:
                continue
            if tier_key and s.tier_key != tier_key:
                continue
            if words and not all(w in self._haystack(s) for w in words):
                continue
            results.append(s)
        return sorted(results, key=lambda s: (-s.diagnostic_weight, s.name.lower()))

    @staticmethod
    def _haystack(s: Symptom) -> str:
        return " ".join((
            s.name, s.scientific_name, s.description, s.system_label,
            *s.tags, *s.causes, *s.red_flags,
        )).lower()

    # -------------------------------------------------------------- sync

    def reload(self) -> None:
        self._repository.reload()

    def has_local_copy(self) -> bool:
        return self._repository.has_local_copy()

    def sync(self, force: bool = False) -> bool:
        """Called by SyncWorker on a background thread."""
        return self._repository.sync(force=force)