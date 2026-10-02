"""Business rules for saved case studies and the medicine pickers.

No widgets and no SQL here. Medicine names always come from MedicineService
(your Supabase data via the offline cache); this module never holds its
own list of drugs.
"""

from dataclasses import dataclass
from typing import Callable, Iterable, Optional

from app.models.case_study import CaseStudy, new_id, now_iso
from app.repositories.local_case_store import LocalCaseStore


@dataclass
class MedicineOption:
    """One medicine as the pickers show it."""

    label: str            # "Amlodipine (Amlodipine besilate) · Norvasc"
    name: str
    medicine_id: str
    drug_class: str = ""
    generic_name: str = ""
    is_otc: bool = False


class CaseStudyService:
    def __init__(self, owner: str, medicines: Callable[[], Iterable] = list,
                 store=None) -> None:
        # store: anything with list_for(), add() and delete(). The app passes
        # NotebookCaseStore so saved cases live in the Study Notebook; the
        # old LocalCaseStore is the fallback.
        self._owner = owner
        self._medicines = medicines          # MedicineService.all_medicines
        self._store = store or LocalCaseStore()

    # ------------------------------------------------------------ medicines

    def medicine_options(self) -> list[MedicineOption]:
        options = []
        for m in self._medicines():
            generic = m.international_generic_name or m.generic_name
            brands = [*m.ph_brands, *m.intl_brands]
            label = m.name
            if generic and generic.lower() != m.name.lower():
                label += f" ({generic})"
            if brands:
                label += " · " + ", ".join(brands[:3])
            options.append(MedicineOption(label=label, name=m.name, medicine_id=m.id,
                                          drug_class=m.drug_class, generic_name=generic,
                                          is_otc=m.is_otc))
        return sorted(options, key=lambda o: o.name.lower())

    def option(self, medicine_id: str) -> Optional[MedicineOption]:
        return next((o for o in self.medicine_options() if o.medicine_id == medicine_id),
                    None)

    def match_medicine(self, typed: str) -> str:
        """The database id for a typed name, generic name or brand, or ""."""
        text = typed.strip().lower()
        if not text:
            return ""
        best_id, best_len = "", 0
        for m in self._medicines():
            names = [m.name, m.generic_name, m.international_generic_name,
                     *m.ph_brands, *m.intl_brands]
            for name in (n.strip().lower() for n in names if n):
                if (text == name or text.startswith(name + " ")) and len(name) > best_len:
                    best_id, best_len = m.id, len(name)
        return best_id

    def quick_candidates(self, limit: int = 8) -> list[MedicineOption]:
        """Chips under the search box: candidates from recent case studies
        first, then medicines from the database to fill the row."""
        options = {o.medicine_id: o for o in self.medicine_options()}
        out, seen = [], set()
        for case in self.cases():
            option = options.get(case.candidate_id)
            if option is not None and option.medicine_id not in seen:
                out.append(option)
                seen.add(option.medicine_id)
        for option in options.values():
            if len(out) >= limit:
                break
            if option.medicine_id not in seen:
                out.append(option)
                seen.add(option.medicine_id)
        return out[:limit]

    # ---------------------------------------------------------------- cases

    def cases(self) -> list[CaseStudy]:
        return self._store.list_for(self._owner)

    def get(self, case_id: str) -> Optional[CaseStudy]:
        return next((c for c in self.cases() if c.id == case_id), None)

    def search(self, query: str = "", tag: str = "") -> list[CaseStudy]:
        """Cases whose title, candidate name, tags or notes contain every word."""
        names = {o.medicine_id: o.name.lower() for o in self.medicine_options()}
        words = query.lower().split()
        out = []
        for case in self.cases():
            if tag and tag not in case.tags:
                continue
            haystack = " ".join((case.title, names.get(case.candidate_id, ""),
                                 " ".join(case.tags), case.notes)).lower()
            if all(w in haystack for w in words):
                out.append(case)
        return out

    def all_tags(self) -> list[str]:
        """Tags in use, in first-seen order."""
        seen: list[str] = []
        for case in self.cases():
            for tag in case.tags:
                if tag not in seen:
                    seen.append(tag)
        return seen

    def save(self, title: str, candidate_id: str, regimen_ids: list[str],
             condition_ids: list[str], tags: list[str], notes: str) -> Optional[str]:
        """Returns an error message, or None when saved."""
        title = title.strip()
        if not title:
            return "Enter a case title."
        if not candidate_id:
            return "Choose a candidate drug before saving."
        clean_tags = []
        for tag in tags:
            tag = tag.strip()
            if tag and tag not in clean_tags:
                clean_tags.append(tag)
        self._store.add(self._owner, CaseStudy(
            id=new_id(), title=title, candidate_id=candidate_id,
            regimen_ids=list(regimen_ids), condition_ids=list(condition_ids),
            tags=clean_tags, notes=notes.strip(), created_at=now_iso()))
        return None

    def duplicate(self, case_id: str) -> None:
        case = self.get(case_id)
        if case is not None:
            self._store.add(self._owner, CaseStudy(
                id=new_id(), title=f"{case.title} (Copy)", candidate_id=case.candidate_id,
                regimen_ids=list(case.regimen_ids), condition_ids=list(case.condition_ids),
                tags=list(case.tags), notes=case.notes, created_at=now_iso()))

    def delete(self, case_id: str) -> None:
        self._store.delete(self._owner, case_id)
