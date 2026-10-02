"""Lets the Drug Interaction Checker keep its saved cases in the notebook.

CaseStudyService only needs three methods from a store: list_for(), add()
and delete(). The old LocalCaseStore had them; this class offers the same
three, but reads and writes interaction-case items in the Study Notebook.

Because the service only relies on those three methods (not on the class),
swapping the store needs no change to the service or the checker. That is
the point of keeping storage behind a small repository interface.
"""

from app.models.case_study import CaseStudy, now_iso
from app.models.notebook import INTERACTION_CASE, NotebookItem
from app.repositories.local_notebook_store import LocalNotebookStore


class NotebookCaseStore:
    def __init__(self, store: LocalNotebookStore) -> None:
        self._store = store

    def list_for(self, owner: str) -> list[CaseStudy]:
        items = [i for i in self._store.list_items(owner) if i.kind == INTERACTION_CASE]
        items.sort(key=lambda i: i.created_at, reverse=True)
        return [CaseStudy(id=i.id, title=i.title,
                          candidate_id=str(i.case.get("candidate_id", "")),
                          regimen_ids=list(i.case.get("regimen_ids", [])),
                          condition_ids=list(i.case.get("condition_ids", [])),
                          tags=list(i.tags), notes=str(i.case.get("notes", "")),
                          created_at=i.created_at)
                for i in items]

    def add(self, owner: str, case: CaseStudy) -> None:
        item = NotebookItem(
            id=case.id, kind=INTERACTION_CASE, title=case.title, tags=list(case.tags),
            case={"candidate_id": case.candidate_id, "regimen_ids": list(case.regimen_ids),
                  "condition_ids": list(case.condition_ids), "notes": case.notes},
            created_at=case.created_at or now_iso())
        self._store.save_item(owner, item)

    def delete(self, owner: str, case_id: str) -> None:
        self._store.delete_item(owner, case_id)
