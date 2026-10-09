"""Health Articles rules: loading, filtering, and what is related to what.

Articles are read live from the server and kept in memory for a few
minutes, so moving around the app does not refetch them. Everything else
here is pure filtering over that list, testable without a network.
"""

import time
from typing import Iterable, Optional

from app.models.health_article import HealthArticle
from app.repositories.health_article_repository import HealthArticleRepository
from app.services.search_service import SearchResult, score_text

FRESH_FOR_S = 300


class HealthArticleService:
    def __init__(self, repository: Optional[HealthArticleRepository] = None) -> None:
        self._repo = repository or HealthArticleRepository()
        self._articles: list[HealthArticle] = []
        self._loaded_at = 0.0

    # ------------------------------------------------------------ loading

    @property
    def loaded(self) -> bool:
        return self._loaded_at > 0

    def is_fresh(self) -> bool:
        return self.loaded and time.monotonic() - self._loaded_at < FRESH_FOR_S

    def load(self) -> list[HealthArticle]:
        """Fetch from the server (call on a worker thread). Raises
        ArticleRepositoryError with a readable message on failure."""
        articles = [HealthArticle.from_row(row) for row in self._repo.fetch_published()]
        self._articles = articles
        self._loaded_at = time.monotonic()
        return articles

    def invalidate(self) -> None:
        self._loaded_at = 0.0

    # ------------------------------------------------------------ reading

    def all(self) -> list[HealthArticle]:
        return list(self._articles)

    def get(self, article_id: str) -> Optional[HealthArticle]:
        return next((a for a in self._articles if a.id == article_id), None)

    def categories(self) -> list[tuple[str, int]]:
        counts: dict[str, int] = {}
        for article in self._articles:
            counts[article.category] = counts.get(article.category, 0) + 1
        return sorted(counts.items(), key=lambda pair: pair[0].lower())

    def search(self, query: str = "", category: str = "", kind: str = "") -> list[HealthArticle]:
        return [a for a in self._articles
                if a.matches(query)
                and (not category or a.category == category)
                and (not kind or a.kind == kind)]

    def related_to(self, kind: str, ref_id: str) -> list[HealthArticle]:
        return [a for a in self._articles if a.links_to(kind, ref_id)]


class ArticleProvider:
    """Global search (Ctrl+K): articles by title, category and summary."""

    def __init__(self, articles) -> None:
        self._articles = articles            # callable -> list[HealthArticle]

    def search(self, query: str) -> Iterable[SearchResult]:
        for article in self._articles():
            score = max(score_text(query, article.title),
                        score_text(query, article.category) * 0.6,
                        score_text(query, article.summary) * 0.5)
            if score > 0:
                yield SearchResult("article", article.id, article.title,
                                   f"{article.kind_label} · {article.category}",
                                   "stack", score)
