"""Health Articles: loads them, filters the list, opens what was clicked.

    written article   -> the reader, in a full-page sheet (like inspect)
    external link     -> the built-in reference browser (app/core/links.py)

Bookmarks and "Save to notebook" go through the same services the
encyclopedias use. Opening a linked disease, symptom or medicine is the
shell's job (open_entry callback), so this never imports another screen.
"""

from html import escape
from typing import Callable, Optional

from PySide6.QtCore import QObject, Signal

from app.core.background import call_in_background
from app.core.links import open_link
from app.models.bookmark import ARTICLE
from app.models.health_article import HealthArticle, body_blocks
from app.services.bookmark_service import BookmarkService
from app.services.health_article_service import HealthArticleService
from app.services.notebook_service import NotebookService
from app.ui.components.page_sheet import PageSheet
from app.ui.views.health_articles_view import ArticleReader, HealthArticlesView


class HealthArticlesController(QObject):
    loaded = Signal()                   # the article list arrived (or changed)
    opened = Signal(str)                # an article was opened (search history, activity)
    bookmark_changed = Signal(str, str, bool)   # type, id, starred
    notebook_saved = Signal(str)        # notebook item id

    def __init__(self, view: HealthArticlesView, service: HealthArticleService,
                 bookmarks: BookmarkService, notebook: NotebookService,
                 entry_name: Callable[[str, str], Optional[str]],
                 open_entry: Callable[[str, str], None]) -> None:
        super().__init__(view)
        self._view = view
        self._service = service
        self._bookmarks = bookmarks
        self._notebook = notebook
        self._entry_name = entry_name
        self._open_entry = open_entry
        self._filters = ("", "", "")
        self._loading = False
        self._sheet: Optional[PageSheet] = None
        self.reader = ArticleReader()
        self._waiting_for: Optional[str] = None      # opened before the list loaded

        view.filters_changed.connect(self._on_filters)
        view.open_requested.connect(self.open_article)
        view.star_requested.connect(self._toggle_star)
        view.retry_requested.connect(lambda: self.refresh(force=True))
        self.reader.star_requested.connect(self._toggle_star)
        self.reader.notebook_requested.connect(self._save_to_notebook)
        self.reader.entry_requested.connect(self._open_linked)
        self.reader.link_requested.connect(open_link)

    def attach_sheet(self, sheet: PageSheet) -> None:
        self._sheet = sheet
        sheet.set_content(self.reader)
        sheet.close_requested.connect(sheet.close_sheet)

    # -------------------------------------------------------------- loading

    def refresh(self, force: bool = False) -> None:
        """Called when the tab is shown; fetches only if the copy is stale."""
        if self._loading or (self._service.is_fresh() and not force):
            self._render()
            return
        self._loading = True
        if not self._service.loaded:
            self._view.show_loading()

        def done(_articles) -> None:
            self._loading = False
            self._render()
            self.loaded.emit()
            if self._waiting_for:
                article_id, self._waiting_for = self._waiting_for, None
                self.open_article(article_id)

        def failed(message: str) -> None:
            self._loading = False
            self._view.show_error(message)
            self._render()

        call_in_background(self._service.load, done, failed, owner=self._view)

    def _on_filters(self, query: str, category: str, kind: str) -> None:
        self._filters = (query, category, kind)
        self._render()

    def _render(self) -> None:
        total = len(self._service.all())
        self._view.set_categories(self._service.categories(), total)
        self._view.show_articles(self._service.search(*self._filters),
                                 self._bookmarks.ids(ARTICLE), total)

    # -------------------------------------------------------------- opening

    def open_article(self, article_id: str) -> None:
        article = self._service.get(article_id)
        if article is None:
            if not self._service.loaded:
                self._waiting_for = article_id
                self.refresh()
            return
        self.opened.emit(article_id)
        if article.is_external:
            open_link(article.url, article.title)
            return
        links = []
        for link in article.links:
            name = self._entry_name(link.kind, link.ref_id)
            if name:
                links.append((link.kind, link.ref_id, name))
        self.reader.show_article(article, self._bookmarks.is_bookmarked(ARTICLE, article.id),
                                 links)
        self.reader.show_notice("")
        if self._sheet is not None:
            self._sheet.open_sheet()
            self._sheet.raise_()
            self._sheet.tab.raise_()

    def _open_linked(self, kind: str, ref_id: str) -> None:
        # The entry opens on top of the article; closing it returns here.
        self._open_entry(kind, ref_id)

    # ------------------------------------------------------------- actions

    def _toggle_star(self, article_id: str) -> None:
        on = self._bookmarks.toggle(ARTICLE, article_id)
        self.bookmark_changed.emit(ARTICLE, article_id, on)
        self.reader.set_starred(on)
        self._render()

    def set_bookmarked(self, article_id: str, on: bool) -> None:
        """A star changed elsewhere (the Bookmarks page)."""
        self.reader.set_starred(on)
        self._render()

    def _save_to_notebook(self, article_id: str) -> None:
        article = self._service.get(article_id)
        if article is None:
            return
        item = self._notebook.create_note(base=article.title)
        self._notebook.save_body(item.id, article_note_html(article))
        self.notebook_saved.emit(item.id)
        self.reader.show_notice("Saved to your Study Notebook as a new note.")


def article_note_html(article: HealthArticle) -> str:
    """The article as a notebook note: a source line, the summary, the text."""
    parts = [f'<p><i>Source: Akeso Health Articles · {escape(article.title)}'
             + (f" · by {escape(article.author_name)}" if article.author_name else "")
             + "</i></p>"]
    if article.summary:
        parts.append(f"<p><b>{escape(article.summary)}</b></p>")
    bullets: list[str] = []
    for kind, text in body_blocks(article.body):
        if kind == "li":
            bullets.append(f"<li>{escape(text)}</li>")
            continue
        if bullets:
            parts.append("<ul>" + "".join(bullets) + "</ul>")
            bullets = []
        parts.append(f"<h3>{escape(text)}</h3>" if kind == "h" else f"<p>{escape(text)}</p>")
    if bullets:
        parts.append("<ul>" + "".join(bullets) + "</ul>")
    if article.references:
        parts.append("<p><b>References</b></p><ul>" + "".join(
            f"<li>{escape(r.source_name)}"
            + (f' — <a href="{escape(r.url, quote=True)}">{escape(r.url)}</a>' if r.url else "")
            + "</li>" for r in article.references) + "</ul>")
    return "".join(parts)
