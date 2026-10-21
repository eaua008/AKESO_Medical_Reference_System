"""Body System Explorer: from a clicked part to what Akeso knows about it.

Each part in the 3D model carries the body system it belongs to (an
anatomical grouping from BodyParts3D / the Foundational Model of Anatomy:
brain -> nervous, heart -> cardiovascular...). This matches it to Akeso's
own body systems by name and lists that system's conditions, symptoms,
articles and Clinical Exchange posts. It also finds the part's description
(BodyPartService, looked up by FMA id) and keeps that data in sync in the
background. No medical text is generated here.
"""

from typing import Callable, Optional

from PySide6.QtCore import QObject, QTimer

from app.core.background import call_in_background
from app.ui.views.body_explorer_view import BodyExplorerView

# part system key -> words to look for in Akeso's body system names
SYSTEM_WORDS = {
    "nervous": "nervous", "cardiovascular": "cardiovascular", "respiratory": "respiratory",
    "digestive": "digestive", "urinary": "urinary", "endocrine": "endocrine",
    "reproductive": "reproductive",
    "musculoskeletal": "musculoskeletal", "integumentary": "integumentary",
}


class BodyExplorerController(QObject):
    def __init__(self, view: BodyExplorerView, diseases, symptoms, articles,
                 discussions_for: Optional[Callable[[str], object]] = None,
                 body_parts=None) -> None:
        """diseases / symptoms / articles: the shared services.
        discussions_for(body_system_id) -> widget listing tagged posts.
        body_parts: BodyPartService (descriptions), or None."""
        super().__init__(view)
        self._view = view
        self._diseases = diseases
        self._symptoms = symptoms
        self._articles = articles
        self._discussions_for = discussions_for
        self._parts = body_parts
        self._shown: Optional[dict] = None
        self._syncing = False
        view.part_selected.connect(self.show_part)
        if body_parts is not None:
            QTimer.singleShot(2500, self.sync_descriptions)   # after the app has settled

    # ---------------------------------------------------------- descriptions

    def sync_descriptions(self, force: bool = False) -> None:
        """Refresh the description copy on a worker thread; offline keeps the old one."""
        if self._parts is None or self._syncing:
            return
        self._syncing = True
        call_in_background(lambda: self._parts.sync(force=force), self._synced,
                           lambda _message: self._sync_ended(), owner=self)

    def _synced(self, changed) -> None:
        self._syncing = False
        if changed:
            self._parts.reload()
            self._redraw()

    def _sync_ended(self) -> None:
        self._syncing = False

    def enable_drafts(self, load_rows: Callable[[], list]) -> None:
        """Admins: also show unpublished descriptions, marked Draft.
        load_rows runs on a worker thread (the admin preview, migration 054)."""
        if self._parts is None:
            return
        call_in_background(load_rows, self._drafts_loaded, lambda _message: None, owner=self)

    def _drafts_loaded(self, rows) -> None:
        self._parts.set_drafts(rows or [])
        self._redraw()

    def _redraw(self) -> None:
        if self._shown is not None:
            self.show_part(self._shown)

    def description_for(self, part: dict):
        if self._parts is None or part.get("browse") or not part.get("fma"):
            return None
        try:
            return self._parts.describe(part.get("fma", ""), part.get("name", ""))
        except Exception:  # noqa: BLE001 - never let a bad entry break the panel
            return None

    def _names(self, about) -> dict:
        """Disease id -> name for the description's linked conditions (published ones)."""
        names = {}
        for note in (about.info.clinical if about is not None else []):
            if note.disease_id and note.disease_id not in names:
                try:
                    disease = self._diseases.get(note.disease_id)
                except Exception:  # noqa: BLE001
                    disease = None
                if disease is not None:
                    names[note.disease_id] = disease.name
        return names

    def system_for(self, key: str):
        """Akeso's BodySystem for a part's system key, or None."""
        word = SYSTEM_WORDS.get(key or "")
        if not word:
            return None
        try:
            systems = self._diseases.body_systems()
        except Exception:
            return None
        return next((s for s in systems if word in s.name.lower()), None)

    def show_part(self, part: dict) -> None:
        self._shown = part
        about = self.description_for(part)
        system = self.system_for(part.get("system", ""))
        if system is None:
            label = (part.get("system") or "").capitalize()
            self._view.show_part(part, label, about=about, disease_names=self._names(about))
            return
        diseases, symptoms, articles = [], [], []
        try:
            disease_list = self._diseases.group_by_body_system().get(system.name, [])
            diseases = [(d.id, d.name, getattr(d, "scientific_name", "") or "")
                        for d in disease_list]
        except Exception:
            disease_list = []
        try:
            symptoms = [(s.id, s.name, s.scientific_name or "")
                        for s in sorted(self._symptoms.all_symptoms(), key=lambda s: s.name.lower())
                        if s.body_system_id == system.id
                        or (s.body_system_name or "").lower() == system.name.lower()]
        except Exception:
            pass
        try:
            ids = {d.id for d in disease_list}
            articles = [(a.id, a.title, a.category) for a in self._articles.all()
                        if any(l.kind == "disease" and l.ref_id in ids for l in a.links)]
        except Exception:
            pass
        discussions = self._discussions_for(system.id) if self._discussions_for else None
        self._view.show_part(part, system.name, diseases, symptoms, articles, discussions,
                             about=about, disease_names=self._names(about))
