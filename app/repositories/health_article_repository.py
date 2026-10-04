"""Health Articles in Supabase (migration 005).

Published articles are public-read under row-level security, so this uses
the same anonymous client as the encyclopedias. One request fetches every
published article with its references and linked entries embedded.
"""

from typing import Optional

from supabase import Client, create_client

from app.core.config import config


class ArticleRepositoryError(Exception):
    pass


class HealthArticleRepository:
    def __init__(self, client: Optional[Client] = None) -> None:
        self._client = client
        # Made on first use, so building the dashboard costs nothing.

    def _c(self) -> Client:
        if self._client is None:
            self._client = create_client(config.supabase_url, config.supabase_key)
        return self._client

    def fetch_published(self) -> list[dict]:
        try:
            return (self._c().table("health_articles")
                    .select("*, health_article_references(*), health_article_links(*)")
                    .eq("is_published", True)
                    .order("updated_at", desc=True)
                    .execute().data or [])
        except Exception as exc:  # noqa: BLE001
            text = str(exc).lower()
            if "health_articles" in text and ("does not exist" in text or "schema cache" in text
                                              or "could not find" in text):
                raise ArticleRepositoryError(
                    "Health Articles aren't set up on the server yet. Run "
                    "database/migrations/005_health_articles.sql.") from exc
            raise ArticleRepositoryError(
                "Couldn't load articles. Check your connection and try again.") from exc
