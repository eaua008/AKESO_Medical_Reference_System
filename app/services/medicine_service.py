"""Business rules for the Medicine Reference: lookups and filtering.

No widgets and no database here, so the filter logic can be tested alone.
"""

from typing import Optional

from app.models.medicine import REGULATORY_CLASSES, MedicineMonograph
from app.repositories.cached_medicine_repository import CachedMedicineRepository

# Which fields the search box looks at. Matches the scope toggle in the UI.
SCOPES = (("all", "All Fields"), ("generic", "Generic"), ("brand", "Brands (PH/Intl)"))


class MedicineService:
    def __init__(self, repository: Optional[object] = None) -> None:
        self._repository = repository or CachedMedicineRepository()

    # ------------------------------------------------------------- reads

    def all_medicines(self) -> list[MedicineMonograph]:
        return self._repository.all()

    def get(self, medicine_id: str) -> Optional[MedicineMonograph]:
        return next((m for m in self.all_medicines() if m.id == medicine_id), None)

    def regulatory_classes(self) -> list[tuple[str, str]]:
        """Only the classes that actually appear, so the filter can't come up empty."""
        present = {m.category for m in self.all_medicines()}
        return [(key, label) for key, label in REGULATORY_CLASSES
                if any(c.lower().startswith(key.lower()) for c in present)]

    def search(self, query: str = "", regulatory_class: str = "",
               scope: str = "all") -> list[MedicineMonograph]:
        """Medicines matching every word of the query, within the chosen scope."""
        words = query.lower().split()
        results = []
        for medicine in self.all_medicines():
            if regulatory_class and not medicine.category.lower().startswith(
                    regulatory_class.lower()):
                continue
            if words and not all(w in self._haystack(medicine, scope) for w in words):
                continue
            results.append(medicine)
        # Black-box drugs are not "more important", so plain alphabetical.
        return sorted(results, key=lambda m: m.name.lower())

    @staticmethod
    def _haystack(m: MedicineMonograph, scope: str) -> str:
        if scope == "generic":
            parts = (m.name, m.generic_name, m.international_generic_name, m.drug_class)
        elif scope == "brand":
            parts = (*m.ph_brands, *m.intl_brands)
        else:
            parts = (m.name, m.generic_name, m.international_generic_name, m.drug_class,
                     *m.ph_brands, *m.intl_brands, *m.indications, *m.contraindications)
        return " ".join(parts).lower()

    # -------------------------------------------------------------- sync

    def reload(self) -> None:
        self._repository.reload()

    def has_local_copy(self) -> bool:
        return self._repository.has_local_copy()

    def sync(self, force: bool = False) -> bool:
        """Called by SyncWorker on a background thread."""
        return self._repository.sync(force=force)