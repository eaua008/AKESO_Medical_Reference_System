"""Business rules for the Study Notebook. No widgets and no SQL here.

    what the home page lists     filtered(), counts()
    subjects                     create / rename / delete
    items                        new note, details, pin, duplicate, delete
    the workspace                layout per item, saved as the student works
    the open-items bar           which items are open, remembered per owner
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from app.models.case_study import new_id, now_iso
from app.models.notebook import (
    INTERACTION_CASE,
    ITEM_KINDS,
    NOTE,
    SYMPTOM_CASE,
    NotebookItem,
    Subject,
    WorkspaceState,
)
from app.repositories.local_notebook_store import LocalNotebookStore

HYPOTHETICAL_NOTE = ("Cases are hypothetical study scenarios. Do not enter real patient "
                     "names or identifiers.")

RECENT_DAYS = 14
SORTS = {"edited": "Recently edited", "title": "Title", "subject": "Subject"}
LIBRARIES = ("all", "pinned", "recent")


@dataclass
class Filters:
    """What the home page is currently showing."""

    library: str = "all"            # all | pinned | recent
    subject_id: str = ""            # "" = every subject
    kind: str = ""                  # "" = every type
    tags: set[str] = field(default_factory=set)
    query: str = ""
    sort: str = "edited"


@dataclass
class Counts:
    library: dict[str, int]
    subjects: dict[str, int]
    kinds: dict[str, int]
    tags: list[tuple[str, int]]     # most used first
    total: int


class NotebookService:
    def __init__(self, owner: str, store: Optional[LocalNotebookStore] = None) -> None:
        self._owner = owner
        self._store = store or LocalNotebookStore()

    @property
    def store(self) -> LocalNotebookStore:
        return self._store

    def import_legacy(self, legacy_path: Path) -> int:
        return self._store.import_legacy_cases(self._owner, legacy_path)

    # ----------------------------------------------------------- reading

    def items(self) -> list[NotebookItem]:
        return self._store.list_items(self._owner)

    def get(self, item_id: str) -> Optional[NotebookItem]:
        return self._store.get_item(self._owner, item_id)

    def subjects(self) -> list[Subject]:
        return self._store.list_subjects(self._owner)

    def subject_name(self, subject_id: str) -> str:
        return next((s.name for s in self.subjects() if s.id == subject_id), "")

    @staticmethod
    def _is_recent(item: NotebookItem) -> bool:
        if not item.opened_at:
            return False
        try:
            opened = datetime.fromisoformat(item.opened_at)
        except ValueError:
            return False
        return datetime.now() - opened <= timedelta(days=RECENT_DAYS)

    @staticmethod
    def _is_kind(item: NotebookItem, kind: str) -> bool:
        """The type filter. A note with a Symptom Checker run saved in it
        also counts as a symptom case (and likewise for interactions)."""
        if kind == SYMPTOM_CASE:
            return item.kind == SYMPTOM_CASE or bool(item.symptom_data.get("symptoms"))
        if kind == INTERACTION_CASE:
            return item.kind == INTERACTION_CASE or \
                bool(item.interaction_data.get("candidate_id"))
        return item.kind == kind

    def filtered(self, f: Filters) -> list[NotebookItem]:
        subjects = {s.id: s.name for s in self.subjects()}
        words = f.query.lower().split()
        out = []
        for item in self.items():
            if f.library == "pinned" and not item.pinned:
                continue
            if f.library == "recent" and not self._is_recent(item):
                continue
            if f.subject_id and item.subject_id != f.subject_id:
                continue
            if f.kind and not self._is_kind(item, f.kind):
                continue
            if f.tags and not f.tags.issubset(set(item.tags)):
                continue
            if words:
                haystack = " ".join((item.title, subjects.get(item.subject_id, ""),
                                     " ".join(item.tags), item.plain_text)).lower()
                if not all(w in haystack for w in words):
                    continue
            out.append(item)

        if f.library == "recent":
            out.sort(key=lambda i: i.opened_at, reverse=True)
        elif f.sort == "title":
            out.sort(key=lambda i: i.title.lower())
        elif f.sort == "subject":
            # Items without a subject go last.
            out.sort(key=lambda i: (subjects.get(i.subject_id, "￿").lower(),
                                    i.title.lower()))
        # "edited" is the store's own order (updated_at, newest first)
        return out

    def counts(self) -> Counts:
        items = self.items()
        subject_ids = {s.id for s in self.subjects()}
        tags: dict[str, int] = {}
        for item in items:
            for tag in item.tags:
                tags[tag] = tags.get(tag, 0) + 1
        return Counts(
            library={"all": len(items),
                     "pinned": sum(1 for i in items if i.pinned),
                     "recent": sum(1 for i in items if self._is_recent(i))},
            subjects={sid: sum(1 for i in items if i.subject_id == sid) for sid in subject_ids},
            kinds={k: sum(1 for i in items if self._is_kind(i, k)) for k in ITEM_KINDS},
            tags=sorted(tags.items(), key=lambda t: (-t[1], t[0].lower())),
            total=len(items))

    # ---------------------------------------------------------- subjects

    def create_subject(self, name: str) -> tuple[Optional[Subject], str]:
        """Returns (subject, "") or (None, error message)."""
        name = " ".join(name.split())
        if not name:
            return None, "Enter a subject name."
        if len(name) > 40:
            return None, "Keep subject names under 40 characters."
        if any(s.name.lower() == name.lower() for s in self.subjects()):
            return None, f"You already have a subject called “{name}”."
        subject = Subject(id=new_id(), name=name, created_at=now_iso())
        self._store.add_subject(self._owner, subject)
        return subject, ""

    def rename_subject(self, subject_id: str, name: str) -> str:
        name = " ".join(name.split())
        if not name:
            return "Enter a subject name."
        if any(s.name.lower() == name.lower() and s.id != subject_id for s in self.subjects()):
            return f"You already have a subject called “{name}”."
        self._store.rename_subject(self._owner, subject_id, name)
        return ""

    def delete_subject(self, subject_id: str) -> None:
        self._store.delete_subject(self._owner, subject_id)

    # ------------------------------------------------------------- items

    def create_note(self, subject_id: str = "", base: str = "Untitled note") -> NotebookItem:
        titles = {i.title for i in self.items()}
        title, n = base, 1
        while title in titles:
            n += 1
            title = f"{base} {n}"
        item = NotebookItem(id=new_id(), kind=NOTE, title=title, subject_id=subject_id,
                            created_at=now_iso())
        self._store.save_item(self._owner, item)
        return item

    def create_case(self, kind: str, title: str, subject_id: str, tags: list[str],
                    case: dict, body: str = "") -> tuple[Optional[NotebookItem], str]:
        """A case saved from one of the checkers. Returns (item, "") or
        (None, error message). body: optional starting notes, e.g. the
        case summary."""
        title = " ".join(title.split())
        if not title:
            return None, "Enter a case title."
        if kind not in ITEM_KINDS or kind == NOTE:
            return None, "Unknown case type."
        item = NotebookItem(id=new_id(), kind=kind, title=title, subject_id=subject_id,
                            tags=self._clean_tags(tags), case=dict(case), body=body,
                            created_at=now_iso())
        self._store.save_item(self._owner, item)
        return item, ""

    def update_case(self, item_id: str, title: str, subject_id: str, tags: list[str],
                    changes: dict) -> str:
        """Edit case details (vignette, setting, answer key...)."""
        item = self.get(item_id)
        if item is None:
            return "This case no longer exists."
        title = " ".join(title.split())
        if not title:
            return "Enter a case title."
        item.title, item.subject_id, item.tags = title, subject_id, self._clean_tags(tags)
        item.case.update(changes)
        self._store.save_item(self._owner, item)
        return ""

    def attach(self, item_id: str, part: str, data: dict, summary_html: str = "",
               title: str = "", subject_id: Optional[str] = None,
               tags: Optional[list[str]] = None) -> str:
        """Save a checker run INTO an existing note or case (part is
        "symptom" or "interaction"). Opening it in the checker again and
        saving replaces it, so the run stays editable. summary_html, when
        given, is added to the end of the notes."""
        item = self.get(item_id)
        if item is None:
            return "This note no longer exists."
        if (part == "symptom" and item.kind == SYMPTOM_CASE) or \
                (part == "interaction" and item.kind == INTERACTION_CASE):
            item.case.update(data)
        else:
            item.case[part] = dict(data)
        if title.strip():
            item.title = " ".join(title.split())
        if subject_id is not None:
            item.subject_id = subject_id
        if tags is not None:
            item.tags = self._clean_tags(tags)
        if summary_html:
            body = item.body
            if "</body>" in body:
                body = body.replace("</body>", summary_html + "</body>", 1)
            else:
                body += summary_html
            item.body = body
        self._store.save_item(self._owner, item)
        return ""

    def attach_summary(self, item_id: str, summary_html: str) -> None:
        """Add the case summary to the end of the notes."""
        item = self.get(item_id)
        if item is None or not summary_html:
            return
        body = item.body
        item.body = body.replace("</body>", summary_html + "</body>", 1) \
            if "</body>" in body else body + summary_html
        self._store.save_item(self._owner, item)

    @staticmethod
    def _clean_tags(tags: list[str]) -> list[str]:
        clean: list[str] = []
        for tag in tags:
            tag = " ".join(tag.split())
            if tag and tag.lower() not in (t.lower() for t in clean):
                clean.append(tag)
        return clean

    def notes(self) -> list[NotebookItem]:
        return [i for i in self.items() if i.kind == NOTE]

    def cases(self) -> list[NotebookItem]:
        return [i for i in self.items() if i.kind != NOTE]

    def update_details(self, item_id: str, title: str, subject_id: str,
                       tags: list[str]) -> str:
        """Returns an error message, or "" when saved."""
        item = self.get(item_id)
        if item is None:
            return "This item no longer exists."
        title = " ".join(title.split())
        if not title:
            return "The title can't be empty."
        clean = self._clean_tags(tags)
        if (title, subject_id, clean) == (item.title, item.subject_id, item.tags):
            return ""
        item.title, item.subject_id, item.tags = title, subject_id, clean
        self._store.save_item(self._owner, item)
        return ""

    def set_pinned(self, item_id: str, pinned: bool) -> None:
        item = self.get(item_id)
        if item is not None and item.pinned != pinned:
            item.pinned = pinned
            self._store.save_item(self._owner, item, touch=False)

    def mark_opened(self, item_id: str) -> None:
        item = self.get(item_id)
        if item is not None:
            item.opened_at = now_iso()
            self._store.save_item(self._owner, item, touch=False)

    def duplicate(self, item_id: str) -> Optional[NotebookItem]:
        item = self.get(item_id)
        if item is None:
            return None
        copy = NotebookItem(id=new_id(), kind=item.kind, title=f"{item.title} (Copy)",
                            subject_id=item.subject_id, tags=list(item.tags),
                            body=item.body, case=dict(item.case), created_at=now_iso())
        self._store.save_item(self._owner, copy)
        return copy

    def delete(self, item_id: str) -> None:
        self._store.delete_item(self._owner, item_id)

    def save_body(self, item_id: str, body: str) -> None:
        item = self.get(item_id)
        if item is not None and item.body != body:
            item.body = body
            self._store.save_item(self._owner, item)

    # --------------------------------------------------------- workspace

    def workspace_for(self, item: NotebookItem) -> WorkspaceState:
        return item.workspace or WorkspaceState.default_for(item.kind, item.id)

    def save_workspace(self, item_id: str, workspace: WorkspaceState) -> None:
        self._store.save_workspace(self._owner, item_id, workspace)

    # ------------------------------------------------------ open-items bar

    def open_items(self) -> tuple[list[str], str]:
        """Ids of the items open in the top bar (still existing), and the
        active one."""
        data = self._store.get_setting(self._owner, "open_items", {}) or {}
        existing = {i.id for i in self.items()}
        ids = [i for i in data.get("ids", []) if i in existing]
        active = data.get("active", "")
        return ids, active if active in ids else (ids[0] if ids else "")

    def save_open_items(self, ids: list[str], active: str) -> None:
        self._store.set_setting(self._owner, "open_items", {"ids": ids, "active": active})

    def last_view(self) -> dict:
        return self._store.get_setting(self._owner, "home_view", {}) or {}

    def save_last_view(self, view: dict) -> None:
        self._store.set_setting(self._owner, "home_view", view)
