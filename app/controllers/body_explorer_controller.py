"""Body System Explorer: from a clicked part to what Akeso knows about it.

Each part in the 3D model carries the body system it belongs to (an
anatomical grouping from BodyParts3D / the Foundational Model of Anatomy:
brain -> nervous, heart -> cardiovascular...). This matches it to Akeso's
own body systems by name and lists that system's conditions, symptoms,
articles and Clinical Exchange posts. No medical text is generated here.
"""

from typing import Callable, Optional

from PySide6.QtCore import QObject

from app.ui.views.body_explorer_view import BodyExplorerView

# part system key -> words to look for in Akeso's body system names
SYSTEM_WORDS = {
    "nervous": "nervous", "cardiovascular": "cardiovascular", "respiratory": "respiratory",
    "digestive": "digestive", "urinary": "urinary", "endocrine": "endocrine",
    "musculoskeletal": "musculoskeletal", "integumentary": "integumentary",
}


class BodyExplorerController(QObject):
    def __init__(self, view: BodyExplorerView, diseases, symptoms, articles,
                 discussions_for: Optional[Callable[[str], object]] = None) -> None:
        """diseases / symptoms / articles: the shared services.
        discussions_for(body_system_id) -> widget listing tagged posts."""
        super().__init__(view)
        self._view = view
        self._diseases = diseases
        self._symptoms = symptoms
        self._articles = articles
        self._discussions_for = discussions_for
        view.part_selected.connect(self.show_part)

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
        system = self.system_for(part.get("system", ""))
        if system is None:
            label = (part.get("system") or "").capitalize()
            self._view.show_part(part, label)
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
        self._view.show_part(part, system.name, diseases, symptoms, articles, discussions)
