"""Health Articles: written by the Akeso team, or curated links to trusted sources.

Built from the health_articles tables (migration 005). Two kinds share one
shape so they can sit in one list:

    written    title, summary, body, author, last reviewed date, references
    external   title, summary, source and a link (opens in the built-in browser)

Either kind can be linked to diseases, symptoms and medicines.
"""

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from urllib.parse import urlparse

from app.models.account import parse_time

WRITTEN, EXTERNAL = "written", "external"
KIND_LABELS = {WRITTEN: "Akeso article", EXTERNAL: "External link"}
LINK_KINDS = ("disease", "symptom", "medicine")
WORDS_PER_MINUTE = 200


@dataclass
class ArticleReference:
    source_name: str
    citation_text: str = ""
    url: str = ""
    is_mother_book: bool = False


@dataclass
class ArticleLink:
    kind: str          # disease | symptom | medicine
    ref_id: str


@dataclass
class HealthArticle:
    id: str
    title: str
    kind: str = WRITTEN
    category: str = "General"
    summary: str = ""
    body: str = ""
    url: str = ""
    source_name: str = ""
    author_name: str = ""
    reviewed_on: Optional[date] = None
    updated_at: Optional[object] = None
    references: list[ArticleReference] = field(default_factory=list)
    links: list[ArticleLink] = field(default_factory=list)

    @classmethod
    def from_row(cls, row: dict) -> "HealthArticle":
        reviewed = None
        if row.get("reviewed_on"):
            try:
                reviewed = date.fromisoformat(str(row["reviewed_on"])[:10])
            except ValueError:
                reviewed = None
        refs = sorted(row.get("health_article_references") or row.get("references") or [],
                      key=lambda r: r.get("position", 0))
        return cls(
            id=str(row["id"]), title=row.get("name") or "",
            kind=row.get("kind") or WRITTEN, category=row.get("category") or "General",
            summary=row.get("summary") or "", body=row.get("body") or "",
            url=row.get("url") or "", source_name=row.get("source_name") or "",
            author_name=row.get("author_name") or "", reviewed_on=reviewed,
            updated_at=parse_time(row.get("updated_at")),
            references=[ArticleReference(r.get("source_name") or "", r.get("citation_text") or "",
                                         r.get("url") or "", bool(r.get("is_mother_book")))
                        for r in refs],
            links=[ArticleLink(l.get("kind"), str(l.get("ref_id")))
                   for l in (row.get("health_article_links") or row.get("links") or [])
                   if l.get("kind") in LINK_KINDS and l.get("ref_id")],
        )

    # ------------------------------------------------------------ display

    @property
    def is_external(self) -> bool:
        return self.kind == EXTERNAL

    @property
    def kind_label(self) -> str:
        return KIND_LABELS.get(self.kind, "Article")

    @property
    def domain(self) -> str:
        host = urlparse(self.url).netloc.lower()
        return host[4:] if host.startswith("www.") else host

    @property
    def read_minutes(self) -> int:
        words = len(re.findall(r"\w+", f"{self.summary} {self.body}"))
        return max(1, round(words / WORDS_PER_MINUTE))

    def meta_line(self) -> str:
        """"5 min read · Reviewed Oct 1, 2026" or "WHO · who.int"."""
        if self.is_external:
            return " · ".join(x for x in (self.source_name, self.domain) if x)
        parts = [f"{self.read_minutes} min read"]
        if self.reviewed_on:
            parts.append("Reviewed " + self.reviewed_on.strftime("%b %d, %Y").replace(" 0", " "))
        return " · ".join(parts)

    def links_to(self, kind: str, ref_id: str) -> bool:
        return any(l.kind == kind and l.ref_id == ref_id for l in self.links)

    def matches(self, query: str) -> bool:
        query = query.strip().lower()
        if not query:
            return True
        return any(query in (text or "").lower()
                   for text in (self.title, self.summary, self.category, self.source_name,
                                self.author_name))


def body_blocks(body: str) -> list[tuple[str, str]]:
    """Split article text into ("h", heading) / ("p", paragraph) / ("li", item).

    The editor is plain text: a blank line starts a new paragraph, a line
    starting with "## " is a heading, and "- " or "* " starts a bullet.
    """
    blocks: list[tuple[str, str]] = []
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            blocks.append(("p", " ".join(paragraph)))
            paragraph.clear()

    for raw in (body or "").splitlines():
        line = raw.strip()
        if not line:
            flush()
        elif line.startswith("#"):
            flush()
            blocks.append(("h", line.lstrip("#").strip()))
        elif line[:2] in ("- ", "* ", "• "):
            flush()
            blocks.append(("li", line[2:].strip()))
        else:
            paragraph.append(line)
    flush()
    return blocks
