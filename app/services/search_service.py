"""Global search: relevance-ranked suggestions across the app.

Pure logic — no widgets, no database client. It takes providers that hand
back things to search, scores every candidate against the query, and returns
the best matches in order. That makes the ranking testable on its own.

Providers are the extension point. Today there are three:

    ModuleProvider     every nav destination, matched by name
    DiseaseProvider    every published condition, matched by content
    EmergencyProvider  every first-aid protocol in the Emergency Guide

Symptoms and medicines exist in the database but have no screens yet, so a
result for them would have nowhere to land. When those screens exist, each
becomes one more provider class — nothing here changes.
"""

import re
from dataclasses import dataclass
from typing import Callable, Iterable, Protocol

from app.models.disease import Disease
from app.models.emergency import EmergencyProtocol


@dataclass
class SearchResult:
    """One suggestion in the dropdown."""

    kind: str          # "module", "disease" or "protocol"
    target_id: str     # tab id, disease id, or protocol id
    title: str
    subtitle: str
    icon: str          # an icons.py name
    score: float


# ------------------------------------------------------------------ scoring

_WORD_SPLIT = re.compile(r"[^\w]+")


def score_text(query: str, text: str) -> float:
    """How well one piece of text matches the query, 0 to 100.

    Ranked by how a person expects a search box to behave:

        100  exact match              "influenza"   -> Influenza
         85  whole text starts with   "influ"       -> Influenza (Seasonal Flu)
         65  a word starts with       "flu"         -> Influenza (Seasonal Flu)
         40  appears anywhere         "luen"        -> Influenza
          0  no match

    Word-prefix beats plain substring because people type the start of the
    word they're thinking of, not the middle of it.
    """
    if not query or not text:
        return 0.0

    q = query.lower().strip()
    t = text.lower()

    if t == q:
        return 100.0
    if t.startswith(q):
        return 85.0
    if any(word.startswith(q) for word in _WORD_SPLIT.split(t) if word):
        return 65.0
    if q in t:
        return 40.0
    return 0.0


# ---------------------------------------------------------------- providers

class Provider(Protocol):
    def search(self, query: str) -> Iterable[SearchResult]: ...


class ModuleProvider:
    """Every sidebar destination, so any module is one search away."""

    def __init__(self, modules: list[dict]) -> None:
        self._modules = modules

    def search(self, query: str) -> Iterable[SearchResult]:
        for module in self._modules:
            score = score_text(query, module["label"])
            if score:
                yield SearchResult(
                    kind="module",
                    target_id=module["id"],
                    title=module["label"],
                    subtitle="Open module",
                    icon=module.get("icon", "grid"),
                    # A small boost, so typing a module's exact name puts the
                    # module above a disease that merely shares a word.
                    score=score + 5,
                )


class DiseaseProvider:
    """Every published condition, matched across several fields."""

    # Weight per field. The name matters most; a hit buried in the
    # description is weak evidence the user meant this condition.
    #
    # The gap between name and the rest is deliberate. A secondary field's
    # best score (a whole-text prefix, 85) times its weight must stay BELOW
    # a word-prefix hit on the name (65). At 0.9, "hyper" ranked Asthma —
    # scientific name "Hyperreactive Airway Disease" — above Essential
    # Hypertension. At 0.7, 85 x 0.7 = 59.5 < 65, and the name wins.
    _WEIGHTS = {
        "name": 1.0,
        "scientific_name": 0.7,
        "tags": 0.7,
        "body_system_name": 0.55,
        "description": 0.35,
    }

    def __init__(self, source: Callable[[], list[Disease]]) -> None:
        # A callable, not a list: the disease set can change after a refresh,
        # and this should always search the current one.
        self._source = source

    def search(self, query: str) -> Iterable[SearchResult]:
        long_enough_for_body = len(query.strip()) >= 3

        for disease in self._source():
            best = max(
                score_text(query, disease.name) * self._WEIGHTS["name"],
                score_text(query, disease.scientific_name)
                * self._WEIGHTS["scientific_name"],
                max(
                    (score_text(query, tag) for tag in disease.tags),
                    default=0.0,
                ) * self._WEIGHTS["tags"],
                score_text(query, disease.body_system_name)
                * self._WEIGHTS["body_system_name"],
                # Description only for 3+ characters. Short fragments match
                # almost every paragraph and flood the list with noise.
                (score_text(query, disease.description)
                 * self._WEIGHTS["description"])
                if long_enough_for_body else 0.0,
                )
            if best:
                yield SearchResult(
                    kind="disease",
                    target_id=disease.id,
                    title=disease.name,
                    subtitle=disease.scientific_name
                             or disease.body_system_name
                             or "Clinical condition",
                    icon="book",
                    score=best,
                )


class EmergencyProvider:
    """Every first-aid protocol, so "cpr" or "kagat" finds its card."""

    # Same reasoning as DiseaseProvider: the title decides. The Filipino name
    # is a real name for the protocol, so it sits just below; keywords are
    # supporting evidence; warning-sign text is weakest.
    _WEIGHTS = {
        "title": 1.0,
        "local_name": 0.9,
        "keywords": 0.7,
        "warning_signs": 0.35,
    }

    def __init__(self, source: Callable[[], list[EmergencyProtocol]]) -> None:
        self._source = source

    def search(self, query: str) -> Iterable[SearchResult]:
        long_enough_for_body = len(query.strip()) >= 3

        for protocol in self._source():
            best = max(
                score_text(query, protocol.title) * self._WEIGHTS["title"],
                score_text(query, protocol.local_name)
                * self._WEIGHTS["local_name"],
                max(
                    (score_text(query, word) for word in protocol.keywords),
                    default=0.0,
                ) * self._WEIGHTS["keywords"],
                max(
                    (score_text(query, sign) for sign in protocol.warning_signs),
                    default=0.0,
                ) * self._WEIGHTS["warning_signs"]
                if long_enough_for_body else 0.0,
                )
            if best:
                subtitle = "First aid \u00b7 " + protocol.urgency_label.capitalize()
                if protocol.local_name:
                    subtitle = f"{protocol.local_name} \u00b7 {subtitle}"
                yield SearchResult(
                    kind="protocol",
                    target_id=protocol.id,
                    title=protocol.title,
                    subtitle=subtitle,
                    icon="alert",
                    score=best,
                )


# ------------------------------------------------------------------ service

class SearchService:
    """Runs every provider and returns the best matches overall."""

    # For a single character, only a strong match is worth showing. Anything
    # weaker would list most of the app.
    _SINGLE_CHAR_MINIMUM = 60.0

    def __init__(self, providers: list[Provider]) -> None:
        self._providers = providers

    def search(self, query: str, limit: int = 8) -> list[SearchResult]:
        query = query.strip()
        if not query:
            return []

        minimum = self._SINGLE_CHAR_MINIMUM if len(query) == 1 else 1.0

        results: list[SearchResult] = []
        for provider in self._providers:
            results.extend(
                r for r in provider.search(query) if r.score >= minimum
            )

        results.sort(key=lambda r: (-r.score, r.title.lower()))
        return results[:limit]