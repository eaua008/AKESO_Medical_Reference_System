"""Dashboard Overview: gathers a little from every module for the landing page.

Everything on this computer (notes, searches, bookmarks, reference counts,
body systems, the daily tip) is read straight away. What needs the server
(study activity, profile completeness, newest Clinical Exchange posts)
loads in the background, at most once a minute, so returning to the
dashboard is instant.

The controller only takes small callables and services, never other
screens; the shell decides what a click opens.
"""

import time
from datetime import datetime
from typing import Callable, Optional

from PySide6.QtCore import QObject

from app.core.background import call_in_background
from app.models.notebook import ITEM_KINDS
from app.repositories.health_tip_repository import HealthTipRepository
from app.services.bookmark_service import BookmarkService
from app.services.notebook_service import NotebookService
from app.services.search_history_service import SearchHistoryService
from app.ui.views.dashboard_view import DashboardView, DashRow

LIST_LENGTH = 5
REMOTE_EVERY_S = 60
BOOKMARK_ICONS = {"disease": "book-open", "symptom": "activity", "medicine": "pill",
                  "exchange": "message-circle", "article": "file-text"}
HISTORY_ICONS = {"disease": "book-open", "symptom": "activity", "medicine": "pill",
                 "protocol": "heart-pulse", "article": "file-text", "module": "layout-grid"}


def greeting_for(hour: int) -> str:
    if hour < 12:
        return "Good morning"
    if hour < 18:
        return "Good afternoon"
    return "Good evening"


def ago(value: Optional[datetime]) -> str:
    """"just now", "5m ago", "3h ago", "2d ago", or a date, for list rows."""
    if value is None:
        return ""
    now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
    seconds = max(0, int((now - value).total_seconds()))
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{seconds // 60}m ago"
    if seconds < 86400:
        return f"{seconds // 3600}h ago"
    if seconds < 7 * 86400:
        return f"{seconds // 86400}d ago"
    return value.astimezone().strftime("%b %d").replace(" 0", " ")


def _parse(text: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(text) if text else None
    except ValueError:
        return None


class DashboardController(QObject):
    def __init__(self, view: DashboardView, *, first_name: str,
                 notebook: NotebookService, history: SearchHistoryService,
                 bookmarks: BookmarkService,
                 library_counts: Callable[[], dict],
                 body_systems: Callable[[], list],
                 tips: Optional[HealthTipRepository] = None) -> None:
        super().__init__(view)
        self._view = view
        self._first_name = first_name
        self._role_text = ""
        self._notebook = notebook
        self._history = history
        self._bookmarks = bookmarks
        self._library_counts = library_counts
        self._body_systems = body_systems
        self._tips = tips or HealthTipRepository()
        self._load_activity: Optional[Callable[[], dict]] = None
        self._load_profile: Optional[Callable[[], tuple]] = None
        self._load_posts: Optional[Callable[[], list]] = None
        self._last_remote = 0.0
        view.exchange.set_rows([], "Clinical Exchange needs a signed-in account.")
        view.show_activity(None, [], {}, "Sign in to see your study activity.")

    def attach_account(self, role_text: str, load_activity: Callable[[], dict],
                       load_profile: Callable[[], tuple],
                       load_posts: Optional[Callable[[], list]]) -> None:
        """Called once the signed-in account's services exist."""
        self._role_text = role_text
        self._load_activity = load_activity
        self._load_profile = load_profile
        self._load_posts = load_posts
        self._last_remote = 0.0

    def set_name(self, first_name: str) -> None:
        self._first_name = first_name
        self._show_greeting()

    # -------------------------------------------------------------- public

    def refresh(self, force_remote: bool = False) -> None:
        self._show_greeting()
        self._show_tip()
        self._show_library()
        self._show_systems()
        self._show_notes()
        self._show_searches()
        self._show_bookmarks()
        if force_remote or time.monotonic() - self._last_remote > REMOTE_EVERY_S:
            self._last_remote = time.monotonic()
            self._fetch_remote()

    # ------------------------------------------------------------ sections

    def _show_greeting(self) -> None:
        now = datetime.now()
        name = f", {self._first_name}" if self._first_name else ""
        self._view.show_greeting(f"{greeting_for(now.hour)}{name}",
                                 now.strftime("%A, %B %d, %Y").replace(" 0", " "),
                                 self._role_text)

    def _show_tip(self) -> None:
        # A different tip each time the dashboard is shown.
        tip = self._tips.random_tip(getattr(self, "_last_tip", None))
        self._last_tip = tip
        self._view.show_tip(tip.text if tip else "", tip.source if tip else "")

    def _show_library(self) -> None:
        try:
            counts = self._library_counts()
            note = "" if any(counts.values()) else (
                "Nothing downloaded yet. The library fills in once Akeso reaches the server.")
        except Exception:
            counts, note = {}, "Could not read the reference library right now."
        self._view.show_library(counts, note)

    def _show_systems(self) -> None:
        try:
            systems = self._body_systems()
        except Exception:
            systems = []
        self._view.show_systems(systems)

    def _show_notes(self) -> None:
        try:
            items = sorted(self._notebook.items(),
                           key=lambda i: i.opened_at or i.updated_at or i.created_at,
                           reverse=True)[:LIST_LENGTH]
        except Exception:
            items = []
        rows = []
        for item in items:
            kind = ITEM_KINDS.get(item.kind)
            subject = self._notebook.subject_name(item.subject_id) if item.subject_id else ""
            subtitle = " · ".join(x for x in (kind[1] if kind else "", subject) if x)
            rows.append(DashRow(item.id, item.title or "Untitled", subtitle,
                                ago(_parse(item.updated_at)), item.icon))
        self._view.notes.set_rows(rows, "No notes yet. Press New note, or save a case from "
                                        "the Symptom or Drug Interaction Checker.")

    def _show_searches(self) -> None:
        try:
            entries = self._history.entries()[:LIST_LENGTH]
            saving = self._history.saving_enabled()
        except Exception:
            entries, saving = [], True
        rows = [DashRow(e.target_id, e.title, e.kind_label, ago(e.when),
                        HISTORY_ICONS.get(e.kind, "search"), e.kind) for e in entries]
        empty = ("Press Ctrl+K to search diseases, symptoms and medicines." if saving
                 else "Search history is off (Settings).")
        self._view.searches.set_rows(rows, empty)

    def _show_bookmarks(self) -> None:
        try:
            entries = [e for e in self._bookmarks.entries() if not e.missing][:LIST_LENGTH]
        except Exception:
            entries = []
        rows = [DashRow(e.entity_id, e.title, e.kind_label, "",
                        BOOKMARK_ICONS.get(e.entity_type, "bookmark"), e.entity_type)
                for e in entries]
        self._view.bookmarks.set_rows(rows, "Press the star on any entry to keep it here.")

    # -------------------------------------------------------------- remote

    def _fetch_remote(self) -> None:
        view = self._view
        if self._load_activity is not None:
            def shown(result: dict) -> None:
                view.show_activity(result.get("streak"), result.get("days") or [],
                                   result.get("week") or {}, result.get("note", ""))
            call_in_background(self._load_activity, shown,
                               lambda _m: view.show_activity(
                                   None, [], {}, "Could not load your activity right now."),
                               owner=view)
        if self._load_profile is not None:
            call_in_background(self._load_profile, lambda r: view.show_profile(*r),
                               lambda _m: view.show_profile(None, []), owner=view)
        if self._load_posts is not None:
            def posts_shown(posts: list) -> None:
                rows = []
                for post in posts[:LIST_LENGTH - 1]:
                    who = ("Anonymous" if post.author is None or post.author.anonymous
                           else post.author.name)
                    replies = f"{post.reply_count} repl{'y' if post.reply_count == 1 else 'ies'}"
                    rows.append(DashRow(post.id, post.title,
                                        f"{post.kind.title()} · {who} · {replies}",
                                        ago(post.last_activity_at or post.created_at),
                                        "message-circle"))
                view.exchange.set_rows(rows, "No posts yet. Be the first to present a "
                                             "hypothetical case.")
            call_in_background(self._load_posts, posts_shown,
                               lambda _m: view.exchange.set_rows(
                                   [], "Could not load the board right now."),
                               owner=view)
