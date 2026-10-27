"""Which description belongs to a clicked part of the 3D body.

The lookup goes by FMA id, not by name. Every entry lists the FMA ids of
all the model parts it covers (both sides), and the entry with the fewest
ids that still covers the part wins, i.e. the most specific one:

    left femur                  -> "Femur"            (its own entry)
    long head of biceps brachii -> "Biceps brachii"   (shown as "Part of")
    mitral valve leaflet        -> "Heart"            (shown as "Part of")

Names alone would not work: some whole muscles exist in the model only as
their heads, and "left"/"right" is part of some names ("left coronary
artery"), so stripping it would merge different structures.

Admins also see drafts (set_drafts); a draft replaces the published entry
with the same key so they can check new text in place.
"""

from dataclasses import dataclass
from typing import Optional

from app.models.body_part import BodyPartInfo, concept_key
from app.repositories.cached_body_part_repository import CachedBodyPartRepository


@dataclass
class PartDescription:
    info: BodyPartInfo
    exact: bool            # False: the part is one piece of info (show "Part of")


class BodyPartService:
    def __init__(self, repository: Optional[CachedBodyPartRepository] = None) -> None:
        self._repository = repository or CachedBodyPartRepository()
        self._published: list[BodyPartInfo] = []
        self._drafts: list[BodyPartInfo] = []
        self._by_fma: dict[str, list[BodyPartInfo]] = {}
        self._loaded = False

    # ----------------------------------------------------------------- data

    def reload(self) -> None:
        """UI thread: re-read the local copy (after a sync wrote a newer one)."""
        try:
            self._published = self._repository.load()
        except Exception:  # noqa: BLE001 - a damaged cache file: show none, resync later
            self._published = []
        self._loaded = True
        self._index()

    def sync(self, force: bool = False) -> bool:
        """Background thread only."""
        return self._repository.sync(force=force)

    def set_drafts(self, rows: list[dict]) -> None:
        """Admins: every row from the preview, drafts included."""
        self._drafts = [BodyPartInfo.from_row(r) for r in rows or [] if isinstance(r, dict)]
        self._index()

    def _index(self) -> None:
        merged = {p.key: p for p in self._published}
        merged.update({p.key: p for p in self._drafts})
        self._by_fma = {}
        for info in merged.values():
            for fma in info.fma_ids:
                self._by_fma.setdefault(fma, []).append(info)

    def count(self) -> int:
        if not self._loaded:
            self.reload()
        return len({p.key for entries in self._by_fma.values() for p in entries})

    # --------------------------------------------------------------- lookup

    def describe(self, fma: str, name: str) -> Optional[PartDescription]:
        """The description for one model part, or None ("No description yet")."""
        if not self._loaded:
            self.reload()
        entries = self._by_fma.get(fma or "")
        if not entries:
            return None
        info = min(entries, key=lambda e: (len(e.fma_ids), e.kind != "part", e.key))
        exact = info.kind == "part" and info.key == concept_key(name)
        return PartDescription(info, exact)
