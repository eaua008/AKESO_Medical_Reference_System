"""Global search (Ctrl+K) for Study Hub: decks by title, and your own cards
by their text. Opening one shows the deck (the card's deck for a card)."""

from typing import Callable, Iterable, Optional

from app.models.study import Origin
from app.services.search_service import SearchResult, score_text


class StudyProvider:
    def __init__(self, service: Callable[[], Optional[object]]) -> None:
        self._service = service              # -> StudyService, or None before sign-in

    def search(self, query: str) -> Iterable[SearchResult]:
        service = self._service()
        if service is None or len(query.strip()) < 2:
            return
        try:
            decks = service.decks()
        except Exception:  # noqa: BLE001 - search must never break on a bad local file
            return
        for deck in decks:
            score = max(score_text(query, deck.title), score_text(query, deck.description) * 0.5)
            if score > 0:
                yield SearchResult("deck", deck.id, deck.title, f"Study Hub · {deck.label} deck",
                                   "stack", score * 0.9)
        for deck in decks:
            if deck.origin != Origin.PERSONAL:
                continue
            for card in service.cards(deck.id):
                text = card.front or card.cloze_text or card.back
                score = max(score_text(query, card.front), score_text(query, card.back) * 0.6,
                            score_text(query, card.cloze_text) * 0.8)
                if score > 0:
                    yield SearchResult("study_card", card.id, text[:80], f"Card in {deck.title}",
                                       "notebook", score * 0.7)
