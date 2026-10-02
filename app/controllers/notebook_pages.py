"""What each workspace tab shows (steps 5 to 7), and how the pages talk.

NotebookController owns the tabs; this class builds the page behind a tab
the first time it is shown, and wires the page's signals:

    tab kind            page                    column it usually lives in
    note                NotesEditor             centre
    search              SearchPage              right
    disease / symptom /
    medicine            MonographPage           right
    case                CasePage                left

Pages talk to each other only through here:
    monograph "Insert into notes"   -> the active note in the centre column
    case "Insert as table"          -> the active note in the centre column
    a "Source:" link in a note      -> opens that entry in the right column
    a condition in a case           -> opens that entry in the right column

Notes: one QTextDocument per note, shared by every tab showing it, and
saved 0.7 s after the last keystroke.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import QObject, QTimer
from PySide6.QtGui import QCursor, QTextDocument
from PySide6.QtWidgets import QMenu, QWidget

from app.models.notebook import Tab
from app.services.case_reference import CaseReference
from app.services.reference_library import (
    DISEASE,
    KIND_LABELS,
    KINDS,
    SYMPTOM,
    RefHit,
    ReferenceLibrary,
)
from app.ui.views.case_page import CasePage
from app.ui.views.notebook_dialogs import SymptomCaseDialog
from app.ui.views.notebook_workspace import PlaceholderPage
from app.ui.views.notes_editor import MissingPage, NotesEditor, NotesPage, new_document
from app.ui.views.reference_pages import MonographPage, SearchPage

if TYPE_CHECKING:
    from app.controllers.notebook_controller import NotebookController

SAVE_NOTE_MS = 700
REFERENCE_KINDS = set(KINDS)


class NotebookPages(QObject):
    def __init__(self, owner: "NotebookController", library: Optional[ReferenceLibrary],
                 cases: Optional[CaseReference]) -> None:
        super().__init__(owner)
        self.c = owner
        self.library = library
        self.cases = cases or CaseReference()
        self._docs: dict[str, QTextDocument] = {}
        self._timers: dict[str, QTimer] = {}
        owner.view.set_page_factory(self.build)

    # ============================================================ building

    def build(self, tab: Tab, column: str) -> QWidget:
        if tab.kind == "note":
            return self._note_page(tab)
        if tab.kind == "case":
            return self._case_page(tab)
        if tab.kind == "search":
            return self._search_page()
        if tab.kind in REFERENCE_KINDS:
            return self._monograph_page(tab)
        return PlaceholderPage(tab, column)

    # -------------------------------------------------------------- notes

    def document(self, item_id: str) -> Optional[QTextDocument]:
        if item_id not in self._docs:
            item = self.c.service.get(item_id)
            if item is None:
                return None
            doc = new_document(self, item.body)
            doc.setModified(False)
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.setInterval(SAVE_NOTE_MS)
            timer.timeout.connect(lambda iid=item_id: self.save_note(iid))
            doc.contentsChanged.connect(lambda t=timer, iid=item_id: self._typed(iid, t))
            self._docs[item_id] = doc
            self._timers[item_id] = timer
        return self._docs[item_id]

    def _typed(self, item_id: str, timer: QTimer) -> None:
        self._set_saved_label(item_id, "Saving…")
        timer.start()

    def save_note(self, item_id: str) -> None:
        doc = self._docs.get(item_id)
        if doc is None or not doc.isModified():
            return
        self.c.service.save_body(item_id, doc.toHtml())
        doc.setModified(False)
        self._set_saved_label(item_id, f"Saved · {datetime.now():%I:%M %p}".replace(" 0", " "))
        self.c.notes_saved(item_id)

    def save_all(self) -> None:
        for item_id, timer in self._timers.items():
            timer.stop()
            self.save_note(item_id)

    def reload_note(self, item_id: str) -> None:
        """The notes were changed outside the editor (a summary was added):
        load them again, keeping undo history out of it."""
        doc = self._docs.get(item_id)
        item = self.c.service.get(item_id)
        if doc is None or item is None:
            return
        timer = self._timers.get(item_id)
        if timer is not None:
            timer.stop()
        doc.setHtml(item.body)
        doc.setModified(False)
        self._set_saved_label(item_id, "Updated")

    def forget_note(self, item_id: str) -> None:
        """The note was deleted: stop editing it."""
        timer = self._timers.pop(item_id, None)
        if timer is not None:
            timer.stop()
        self._docs.pop(item_id, None)

    def _set_saved_label(self, item_id: str, text: str) -> None:
        for page in self._all_pages():
            if isinstance(page, NotesPage) and page.item_id == item_id:
                page.editor.set_saved(text)

    def _note_page(self, tab: Tab) -> QWidget:
        if not tab.ref:
            # An old empty tab: give it a real note to write in.
            item = self.c.service.create_note(self._current_subject(), base=tab.title)
            tab.ref = item.id
            self.c.layout_changed()
        doc = self.document(tab.ref)
        if doc is None:
            return MissingPage("This note was deleted. Close the tab, or press + to open "
                               "another note.")
        editor = NotesEditor(doc)
        editor.link_clicked.connect(self.follow_link)
        return NotesPage(editor, tab.ref)

    def _current_subject(self) -> str:
        item = self.c.service.get(self.c.items.active_id) if self.c.items.active_id else None
        return item.subject_id if item else ""

    # --------------------------------------------------------------- cases

    def _case_page(self, tab: Tab) -> QWidget:
        item = self.c.service.get(tab.ref or self.c.items.active_id)
        if item is None or not item.has_case_data:
            return MissingPage("No case here. Press + in this column to open one of your "
                               "saved cases, or add one from the Symptom Checker or the "
                               "Drug Interaction Checker.")
        result = interaction = None
        answer_name = ""
        symptom = item.symptom_data
        if symptom.get("symptoms"):
            result = self.cases.symptom_result(symptom)
            if symptom.get("answer_key") and self.library:
                answer_name = self.library.name(DISEASE, symptom["answer_key"])
        if item.interaction_data.get("candidate_id"):
            try:
                interaction = self.cases.interaction(item.interaction_data)
            except Exception:
                interaction = None
        page = CasePage(item, result, interaction, answer_name)
        page.insert_table.connect(self.insert_table)
        page.summary_requested.connect(lambda i=item: self.insert_summary(i.id))
        page.open_reference.connect(self.open_reference)
        page.edit_requested.connect(lambda iid=item.id: self.edit_case(iid))
        page.open_checker.connect(lambda iid=item.id: self.c.edit_in_drug_checker.emit(iid))
        page.open_symptom_checker.connect(
            lambda iid=item.id: self.c.edit_in_symptom_checker.emit(iid))
        return page

    def diagnoses(self, case: dict) -> list[tuple[str, str]]:
        """Answer-key choices: the case's top matches first, then every
        disease in the reference."""
        first: list[tuple[str, str]] = []
        result = self.cases.symptom_result(case)
        if result is not None:
            first = [(m.disease_id, m.name) for m in result.matches[:10]]
        seen = {d for d, _n in first}
        rest = []
        if self.library:
            rest = [(h.id, h.name) for h in self.library.search("", DISEASE, limit=2000)
                    if h.id not in seen]
        return first + rest

    def edit_case(self, item_id: str) -> None:
        item = self.c.service.get(item_id)
        if item is None or not item.symptom_data.get("symptoms"):
            return
        dialog = SymptomCaseDialog(self.c.page, item.symptom_data, self.c.service.subjects(),
                                   self.diagnoses(item.symptom_data), title=item.title,
                                   subject_id=item.subject_id, tags=item.tags, editing=True)

        def save() -> None:
            v = dialog.values()
            error = self.c.service.attach(item_id, "symptom", v["changes"], title=v["title"],
                                          subject_id=v["subject_id"], tags=v["tags"])
            if error:
                dialog.show_error(error)
            else:
                dialog.accept()
        dialog.confirm.clicked.connect(save)
        if dialog.exec():
            self.rebuild(lambda page: isinstance(page, CasePage) and page.item.id == item_id)
            self.c.refresh()

    # ----------------------------------------------------------- reference

    def pins(self) -> list[RefHit]:
        """Suggested entries for the item being studied: its reported
        symptoms and its best-matching conditions."""
        item = self.c.service.get(self.c.items.active_id) if self.c.items.active_id else None
        if item is None or not item.symptom_data.get("symptoms"):
            return []
        symptom = item.symptom_data
        pins = [RefHit(SYMPTOM, s.get("symptom_id", ""), s.get("name", ""))
                for s in symptom.get("symptoms", []) if s.get("symptom_id")]
        result = self.cases.symptom_result(symptom)
        if result is not None:
            pins += [RefHit(DISEASE, m.disease_id, m.name) for m in result.matches[:4]]
        return pins

    def _search_page(self) -> QWidget:
        if self.library is None:
            return MissingPage("The reference data isn't connected.")
        page = SearchPage(self.library, self.pins())
        page.open_requested.connect(self.open_reference)
        return page

    def _monograph_page(self, tab: Tab) -> QWidget:
        mono = self.library.monograph(tab.kind, tab.ref) if self.library else None
        page = MonographPage(mono, tab.kind, tab.ref)
        if mono is not None:
            href = f"akeso://{mono.kind}/{mono.id}"
            page.insert_requested.connect(
                lambda section, html, m=mono: self.insert_reference(
                    f"{m.name} · {section} ({KIND_LABELS[m.kind].lower()} reference)",
                    href, html))
        page.open_full_requested.connect(self.c.open_full_reference.emit)
        return page

    def open_reference(self, kind: str, item_id: str, name: str = "") -> None:
        """Open an entry as a tab in the Reference column (or switch to it)."""
        workspace = self.c.workspace
        if workspace is None or kind not in REFERENCE_KINDS or not item_id:
            return
        right = workspace.column("right")
        right.visible, right.collapsed = True, False
        existing = next((t for t in right.tabs if t.kind == kind and t.ref == item_id), None)
        if existing is not None:
            right.activate(existing.id)
        else:
            name = name or (self.library.name(kind, item_id) if self.library else "") \
                or KIND_LABELS[kind]
            index = right.index_of(right.active_id) + 1 if right.active_id else None
            right.add(Tab.create(kind, name, ref=item_id), index=index)
        self.c.layout_changed()

    def follow_link(self, url: str) -> None:
        """akeso://disease/<id> from a "Source:" line in a note."""
        parts = url.removeprefix("akeso://").split("/", 1)
        if len(parts) == 2:
            self.open_reference(parts[0], parts[1])

    # ------------------------------------------------------ into the notes

    def _target_editor(self) -> Optional[NotesEditor]:
        """The note to write into: the centre column's active note, or its
        first note, or a new "My notes" tab for the item being studied."""
        workspace = self.c.workspace
        if workspace is None:
            return None
        center = workspace.column("center")
        center.visible, center.collapsed = True, False
        active = center.active
        if active is None or active.kind != "note":
            note = next((t for t in center.tabs if t.kind == "note"), None)
            if note is None:
                note = center.add(Tab.create("note", "My notes", ref=self.c.items.active_id))
            center.activate(note.id)
        self.c.layout_changed()
        page = self.c.view.columns["center"].page_for(center.active_id)
        return page.editor if isinstance(page, NotesPage) else None

    def insert_reference(self, label: str, href: str, html: str) -> None:
        editor = self._target_editor()
        if editor is not None:
            editor.insert_reference(label, href, html)

    def insert_summary(self, item_id: str) -> None:
        item = self.c.service.get(item_id)
        editor = self._target_editor()
        if item is not None and editor is not None:
            editor.insert_html_block(self.cases.summary_html(item))

    def insert_table(self, caption: str, headers: list, rows: list) -> None:
        editor = self._target_editor()
        if editor is not None:
            editor.insert_table_data(caption, headers, rows)

    # ------------------------------------------------------------ "+" menus

    def plus_menu(self, column: str) -> None:
        """What "+" offers in each column."""
        workspace = self.c.workspace
        if workspace is None:
            return
        if column == "right":
            self._add(column, Tab.create("search"))
            return
        menu = QMenu(self.c.view)
        menu.setObjectName("nbMenu")
        state = workspace.column(column)
        open_refs = {t.ref for t in state.tabs if t.kind == ("note" if column == "center"
                                                                   else "case")}
        current = self.c.service.get(self.c.items.active_id)
        if column == "center":
            menu.addAction("New note", self._new_note_tab)
            if current is not None and current.id not in open_refs:
                menu.addAction(f"This item's notes ({current.title})", lambda: self._add(
                    "center", Tab.create("note", "My notes", ref=current.id)))
            others = [i for i in self.c.service.notes()
                      if i.id not in open_refs and (current is None or i.id != current.id)]
            sub = menu.addMenu("Open a note")
            sub.setObjectName("nbMenu")
            for item in others[:40]:
                sub.addAction(item.title, lambda i=item: self._add(
                    "center", Tab.create("note", i.title, ref=i.id)))
            sub.setEnabled(bool(others))
        else:
            cases = [i for i in self.c.service.items()
                     if i.has_case_data and i.id not in open_refs]
            if current is not None and current.has_case_data and current.id not in open_refs:
                menu.addAction("This case", lambda: self._add(
                    "left", Tab.create("case", "Case", ref=current.id)))
            sub = menu.addMenu("Open another case to compare")
            sub.setObjectName("nbMenu")
            for item in cases:
                if current is not None and item.id == current.id:
                    continue
                sub.addAction(item.title, lambda i=item: self._add(
                    "left", Tab.create("case", i.title, ref=i.id)))
            sub.setEnabled(any(current is None or i.id != current.id for i in cases))
        menu.exec(QCursor.pos())

    def _new_note_tab(self) -> None:
        item = self.c.service.create_note(self._current_subject())
        self._add("center", Tab.create("note", item.title, ref=item.id))
        self.c.data_changed.emit()
        self.c.refresh_home()

    def _add(self, column: str, tab: Tab) -> None:
        workspace = self.c.workspace
        if workspace is None:
            return
        state = workspace.column(column)
        state.visible, state.collapsed = True, False
        state.add(tab)
        self.c.layout_changed()

    # ------------------------------------------------------------ upkeep

    def _all_pages(self) -> list[QWidget]:
        pages = []
        for column in self.c.view.columns.values():
            pages += column.pages().values()
        return pages

    def rebuild(self, which) -> None:
        """Drop pages that must be built again (edited case, theme change)."""
        for column in self.c.view.columns.values():
            ids = {tab_id for tab_id, page in column.pages().items() if which(page)}
            column.drop_pages(ids)

    def refresh_theme(self) -> None:
        # Reference and case pages bake their icons: build them again.
        self.rebuild(lambda page: isinstance(page, (CasePage, MonographPage, SearchPage)))

    def sync_tab_titles(self) -> None:
        """Notes renamed or deleted elsewhere: update or close their tabs."""
        for item_id, workspace in self.c.workspaces.items():
            for name in ("left", "center"):
                state = workspace.column(name)
                for tab in list(state.tabs):
                    if tab.kind not in ("note", "case") or not tab.ref:
                        continue
                    item = self.c.service.get(tab.ref)
                    if item is None:
                        state.close(tab.id)
                        self.c.view.columns[name].drop_pages({tab.id})
                        if tab.kind == "note":
                            self.forget_note(tab.ref)
                    elif tab.ref != item_id:
                        tab.title = item.title
