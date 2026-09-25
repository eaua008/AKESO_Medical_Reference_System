"""Global-search provider for symptoms.

Kept in its own file so search_service.py doesn't need editing; the shell
just adds SymptomProvider to its provider list. Scoring follows the same
rules as DiseaseProvider: the name decides, other fields support.
"""

from typing import Callable, Iterable

from app.models.symptom import Symptom
from app.services.search_service import SearchResult, score_text


class SymptomProvider:
    _WEIGHTS = {"name": 1.0, "scientific_name": 0.7, "tags": 0.7, "description": 0.35}

    def __init__(self, source: Callable[[], list[Symptom]]) -> None:
        self._source = source

    def search(self, query: str) -> Iterable[SearchResult]:
        long_enough_for_body = len(query.strip()) >= 3

        for s in self._source():
            best = max(
                score_text(query, s.name) * self._WEIGHTS["name"],
                score_text(query, s.scientific_name) * self._WEIGHTS["scientific_name"],
                max((score_text(query, t) for t in s.tags), default=0.0) * self._WEIGHTS["tags"],
                score_text(query, s.description) * self._WEIGHTS["description"]
                if long_enough_for_body else 0.0,
                )
            if best:
                yield SearchResult(
                    kind="symptom",
                    target_id=s.id,
                    title=s.name,
                    subtitle=s.scientific_name or s.system_label,
                    icon="pulse",
                    score=best,
                )