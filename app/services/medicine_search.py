"""Global-search provider for medicines.

Kept in its own file so search_service.py needs no edits; the shell adds
MedicineProvider to its provider list. Brand names score high because in the
Philippines people search "Biogesic" far more often than "paracetamol".
"""

from typing import Callable, Iterable

from app.models.medicine import MedicineMonograph
from app.services.search_service import SearchResult, score_text


class MedicineProvider:
    _WEIGHTS = {"name": 1.0, "generic": 0.85, "brand": 0.8, "drug_class": 0.5,
                "indication": 0.35}

    def __init__(self, source: Callable[[], list[MedicineMonograph]]) -> None:
        self._source = source

    def search(self, query: str) -> Iterable[SearchResult]:
        long_enough_for_body = len(query.strip()) >= 3

        for m in self._source():
            brands = (*m.ph_brands, *m.intl_brands)
            best = max(
                score_text(query, m.name) * self._WEIGHTS["name"],
                max((score_text(query, g) for g in
                     (m.generic_name, m.international_generic_name)), default=0.0)
                * self._WEIGHTS["generic"],
                max((score_text(query, b) for b in brands), default=0.0)
                * self._WEIGHTS["brand"],
                score_text(query, m.drug_class) * self._WEIGHTS["drug_class"],
                max((score_text(query, i) for i in m.indications), default=0.0)
                * self._WEIGHTS["indication"] if long_enough_for_body else 0.0,
                )
            if best:
                subtitle = m.drug_class or m.generic_label
                yield SearchResult(
                    kind="medicine",
                    target_id=m.id,
                    title=m.name,
                    subtitle=subtitle,
                    icon="pill",
                    score=best,
                )