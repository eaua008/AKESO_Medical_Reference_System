"""NotebookController: the whole Study Notebook module.

    NotebookService     notes, cases, subjects, saved layouts (no Qt)
    NotebookPage        home (level 1), quick view (2), workspace (3)

The rule from the design:
    the top bar picks WHICH notebook item you are studying;
    the column tabs pick WHAT you are looking at inside it.

So every open item has its own WorkspaceState (tabs, folders, collapsed
columns, widths). Switching the top tab swaps the whole workspace.

Every handler follows the same loop:
    view signal  ->  change the model / call the service  ->  draw

Layouts are saved half a second after the last change (a debounce), so
dragging tabs around doesn't write to the database on every movement.
"""

from typing import Optional

from app.core.theme import Theme
from PySide6.QtCore import QObject, QPoint, QTimer, Signal
from PySide6.QtWidgets import QDialog, QMenu

from app.models.notebook import (
    COLUMNS,
    DEFAULT_SIZES,
    NOTE,
    ColumnState,
    NotebookItem,
    Tab,
    WorkspaceState,
)
from app.controllers.notebook_pages import NotebookPages
from app.services.case_reference import CaseReference
from app.services.notebook_service import LIBRARIES, NotebookService
from app.services.reference_library import ReferenceLibrary
from app.ui.components.slide_panel import CLOSED, FULL
from app.ui.views.interaction_dialogs import ConfirmDialog
from app.ui.views.notebook_home import NamePopup
from app.ui.views.notebook_page import NotebookPage

SAVE_DELAY_MS = 500


class NotebookController(QObject):
    new_case_requested = Signal(str)            # symptom_case | interaction_case
    open_interaction_case = Signal(str)         # item id -> Drug Interaction Checker
    open_full_reference = Signal(str, str)      # kind, id -> that encyclopedia
    # "Add / Edit in ..." on a note: the checker opens linked to that note,
    # and saving there writes the run back into it.
    edit_in_symptom_checker = Signal(str)       # item id
    edit_in_drug_checker = Signal(str)          # item id
    data_changed = Signal()                     # other modules may need a refresh
    share_requested = Signal(str)               # item id -> Clinical Exchange composer

    def __init__(self, page: NotebookPage, service: NotebookService,
                 library: Optional[ReferenceLibrary] = None,
                 cases: Optional[CaseReference] = None) -> None:
        super().__init__(page)
        self.page = page
        self.home = page.home
        self.quick = page.quick
        self.view = page.workspace
        self.service = service

        self.items = ColumnState()                  # the open-items bar
        self.workspaces: dict[str, WorkspaceState] = {}
        self._dirty: set[str] = set()
        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(SAVE_DELAY_MS)
        self._save_timer.timeout.connect(self._save_layouts)

        self._wire_home()
        self._wire_quick()
        self._wire_workspace()
        # Steps 5 to 7: what each tab shows (notes, reference, case).
        self.pages = NotebookPages(self, library, cases)
        page.panel_closed.connect(self._draw_home)
        page.theme_changed.connect(self._theme_changed)

        self._restore()
        self.refresh()

    # ============================================================ wiring

    def _wire_home(self) -> None:
        h = self.home
        h.filters_changed.connect(self._on_filters)
        h.new_note_requested.connect(self.new_note)
        h.new_case_requested.connect(self.new_case_requested.emit)
        h.item_clicked.connect(lambda iid: self.open_item(iid, "half"))
        h.item_action.connect(self._item_action)
        h.subject_new.connect(self._subject_new)
        h.subject_menu.connect(self._subject_menu)
        h.view_mode_changed.connect(lambda _m: self._save_home_view())
        self._wire_item_strip(h.item_strip, level="half")

    def _wire_quick(self) -> None:
        q = self.quick
        q.open_workspace.connect(self._show_workspace)
        q.close_requested.connect(self.page.close_panel)
        q.action.connect(lambda name: self._item_action(name, q.item_id))
        q.details_changed.connect(self._details_changed)

    def _wire_workspace(self) -> None:
        v = self.view
        self._wire_item_strip(v.item_strip, level="full")
        for name, column in v.columns.items():
            s = column.strip
            s.tab_activated.connect(lambda tab_id, c=name: self._activate_tab(c, tab_id))
            s.tab_closed.connect(lambda tab_id, c=name: self._close_tab(c, tab_id))
            s.new_tab_requested.connect(lambda c=name: self.pages.plus_menu(c))
            s.collapse_requested.connect(lambda c=name: self._set_collapsed(c, True))
            s.command.connect(self._on_command)
            s.tab_dropped.connect(self._on_tab_dropped)
            column.rail.clicked.connect(lambda c=name: self._set_collapsed(c, False))
        v.column_toggled.connect(self._toggle_column)
        v.reset_layout_requested.connect(self._reset_layout)
        v.sizes_changed.connect(self._remember_sizes)
        v.shrink_requested.connect(self._show_quick)
        v.close_requested.connect(self.page.close_panel)

    def _wire_item_strip(self, strip, level: str) -> None:
        strip.tab_activated.connect(lambda iid: self.open_item(iid, level))
        strip.tab_closed.connect(self._close_item_tab)
        strip.new_tab_requested.connect(self.new_note)
        strip.command.connect(self._on_item_command)
        strip.tab_dropped.connect(self._on_item_dropped)

    # ========================================================== startup

    def _restore(self) -> None:
        """Reopen the tabs that were open last time, and the home view."""
        ids, active = self.service.open_items()
        for item_id in ids:
            item = self.service.get(item_id)
            if item is not None:
                self.items.add(Tab(id=item.id, kind=item.kind, title=item.title),
                               activate=False)
        if active:
            self.items.activate(active)
        view = self.service.last_view()
        self.home.set_view_mode(view.get("mode", "grid"))
        self.home.set_sort(view.get("sort", "edited"))
        if view.get("library") in LIBRARIES:
            self.home.filters.library = view["library"]

    def _save_home_view(self) -> None:
        f = self.home.filters
        self.service.save_last_view({"mode": self.home.view_mode, "sort": f.sort,
                                     "library": f.library})

    def _save_open_items(self) -> None:
        self.service.save_open_items([t.id for t in self.items.tabs], self.items.active_id)

    # ========================================================== drawing

    def _signature(self) -> tuple:
        return (Theme.mode(),
                tuple((i.id, i.title, i.updated_at, i.pinned, i.subject_id, tuple(i.tags))
                      for i in self.service.items()),
                tuple(repr(s) for s in self.service.subjects()))

    def refresh_if_stale(self) -> None:
        """Redraw only if something changed since the last redraw (the shell
        calls this every time the tab is opened)."""
        if self._signature() != getattr(self, "_drawn", None):
            self.refresh()

    def refresh(self) -> None:
        """Redraw everything from the database, e.g. after another module
        saved a case, or after a theme switch."""
        self._drawn = self._signature()
        self.pages.sync_tab_titles()
        # Items renamed or deleted elsewhere: keep the open-items bar honest.
        for tab in list(self.items.tabs):
            item = self.service.get(tab.id)
            if item is None:
                self._forget_item(tab.id)
            else:
                tab.title = item.title
        if self.page.level != CLOSED and not self.items.active_id:
            self.page.close_panel()
        self._draw_home()
        self._draw_panel()

    def _draw_home(self) -> None:
        subjects = self.service.subjects()
        f = self.home.filters
        if f.subject_id and f.subject_id not in {s.id for s in subjects}:
            f.subject_id = ""
        counts = self.service.counts()
        f.tags &= {t for t, _n in counts.tags}
        self.home.show_counts(counts, subjects)
        selected = self.items.active_id if self.page.level != CLOSED else ""
        self.home.show_items(self.service.filtered(f), {s.id: s.name for s in subjects},
                             selected, counts.total)
        self.home.item_strip.show_state(self.items)

    def _draw_panel(self) -> None:
        item = self.service.get(self.items.active_id) if self.items.active_id else None
        subject = self.service.subject_name(item.subject_id) if item else ""
        self.view.show_items(self.items, subject)
        if item is None:
            return
        self.quick.show_item(item, self.service.subjects(), self._summary(item))
        self.view.show_workspace(self._workspace(item.id))

    def _summary(self, item: NotebookItem) -> dict:
        """What the quick view's two checker cards show."""
        summary: dict = {"symptom": None, "interaction": None}
        try:
            summary["symptom"] = self.pages.cases.symptom_overview(item.symptom_data)
        except Exception:           # reference data not synced yet: show the rest
            pass
        if item.interaction_data.get("candidate_id"):
            try:
                summary["interaction"] = self.pages.cases.interaction(item.interaction_data)
            except Exception:
                pass
        return summary

    def item_changed_elsewhere(self, item_id: str) -> None:
        """A checker saved a run into this item: reload its notes and case
        pages, and make sure its workspace has a Case tab to show it."""
        self.pages.reload_note(item_id)
        self.pages.rebuild(lambda page: getattr(getattr(page, "item", None), "id", "")
                           == item_id)
        workspace = self.workspaces.get(item_id)
        item = self.service.get(item_id)
        if workspace is not None and item is not None and item.has_case_data:
            left = workspace.column("left")
            if not any(t.kind == "case" and t.ref in ("", item_id) for t in left.tabs):
                left.add(Tab.create("case", "Case", ref=item_id), index=0)
            left.visible = True
            self._dirty.add(item_id)
            self._save_timer.start()
        self.refresh()

    def _theme_changed(self) -> None:
        self.pages.refresh_theme()
        self.refresh()

    # Called by NotebookPages.
    def layout_changed(self) -> None:
        self._changed()

    def refresh_home(self) -> None:
        self._draw_home()

    def notes_saved(self, _item_id: str) -> None:
        # The home cards show a preview of the notes; the list is only
        # visible when the panel is not full width.
        if self.page.level != FULL:
            self._draw_home()

    def _draw_workspace(self) -> None:
        workspace = self.workspace
        self.view.show_items(self.items, self._subject_of(self.items.active_id))
        if workspace is not None:
            self.view.show_workspace(workspace)

    def _subject_of(self, item_id: str) -> str:
        item = self.service.get(item_id) if item_id else None
        return self.service.subject_name(item.subject_id) if item else ""

    # ======================================================= open items

    @property
    def workspace(self) -> Optional[WorkspaceState]:
        return self._workspace(self.items.active_id) if self.items.active_id else None

    def _workspace(self, item_id: str) -> Optional[WorkspaceState]:
        if item_id not in self.workspaces:
            item = self.service.get(item_id)
            if item is None:
                return None
            self.workspaces[item_id] = self.service.workspace_for(item)
        return self.workspaces[item_id]

    def open_item(self, item_id: str, level: str = "half") -> None:
        """Open an item from a card or a tab: add it to the top bar,
        make it active, and slide the panel to the wanted level."""
        item = self.service.get(item_id)
        if item is None:
            self.refresh()
            return
        if self.items.tab(item_id) is None:
            self.items.add(Tab(id=item.id, kind=item.kind, title=item.title))
        self.items.activate(item_id)
        self.service.mark_opened(item_id)
        self._save_open_items()
        self._draw_panel()
        if level == "full":
            self.page.show_full()
        else:
            self.page.show_half()
        self._draw_home()

    def _show_workspace(self) -> None:
        self._draw_workspace()
        self.page.show_full()

    def _show_quick(self) -> None:
        self._draw_panel()
        self.page.show_half()

    def new_note(self) -> None:
        item = self.service.create_note(self.home.filters.subject_id)
        # A new note goes straight to the workspace: you want to write.
        self.open_item(item.id, "full")
        self.data_changed.emit()

    def _forget_item(self, item_id: str) -> None:
        """Take an item out of the top bar and drop its pages."""
        self.items.close(item_id)
        workspace = self.workspaces.pop(item_id, None)
        self._dirty.discard(item_id)
        if workspace is not None:
            for name in COLUMNS:
                self.view.columns[name].drop_pages({t.id for t in workspace.column(name).tabs})

    def _close_item_tab(self, item_id: str) -> None:
        self._flush(item_id)
        self._forget_item(item_id)
        self._save_open_items()
        if not self.items.tabs:
            self.page.close_panel()
        self._draw_panel()
        self._draw_home()

    def _on_item_command(self, _column: str, name: str, target: str, _arg) -> None:
        if name == "pin":
            self.items.set_pinned(target, True)
        elif name == "unpin":
            self.items.set_pinned(target, False)
        elif name == "close":
            self._close_item_tab(target)
            return
        elif name == "close_others":
            for tab in [t for t in self.items.tabs if t.id != target and not t.pinned]:
                self._flush(tab.id)
                self._forget_item(tab.id)
        self._save_open_items()
        self._draw_panel()
        self._draw_home()

    def _on_item_dropped(self, _source: str, item_id: str, _target: str,
                         index: int, _folder: str) -> None:
        self.items.move(item_id, index, "")
        self._save_open_items()
        self._draw_panel()
        self._draw_home()

    # ================================================== item actions

    def _item_action(self, action: str, item_id: str) -> None:
        item = self.service.get(item_id)
        if item is None:
            return
        if action == "share":
            self.share_requested.emit(item_id)
            return
        if action == "pin":
            self.service.set_pinned(item_id, not item.pinned)
        elif action == "duplicate":
            copy = self.service.duplicate(item_id)
            if copy is not None:
                self.data_changed.emit()
                self.open_item(copy.id, "half")
                return
        elif action == "delete":
            self._delete(item)
            return
        elif action == "workspace":
            self.open_item(item_id, "full")
            return
        elif action in ("open_checker", "drug_checker"):
            self.edit_in_drug_checker.emit(item_id)
            return
        elif action == "symptom_checker":
            self.edit_in_symptom_checker.emit(item_id)
            return
        elif action == "summary":
            self.pages.save_note(item_id)
            self.service.attach_summary(item_id, self.pages.cases.summary_html(item))
            self.item_changed_elsewhere(item_id)
            return
        self._draw_home()
        self._draw_panel()

    def _delete(self, item: NotebookItem) -> None:
        what = "case study" if item.is_case else "note"
        dialog = ConfirmDialog(self.page, f"Delete this {what}?",
                               f"“{item.title}” and its notes will be removed from your "
                               "Study Notebook.", "Delete")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        self.service.delete(item.id)
        self.pages.forget_note(item.id)
        self._forget_item(item.id)
        self._save_open_items()
        if not self.items.tabs:
            self.page.close_panel()
        self.data_changed.emit()
        self.refresh()

    def _details_changed(self, title: str, subject_id: str, tags: list) -> None:
        item_id = self.quick.item_id
        error = self.service.update_details(item_id, title, subject_id, tags)
        self.quick.show_error(error)
        if error:
            return
        tab = self.items.tab(item_id)
        if tab is not None:
            tab.title = " ".join(title.split())
        self._draw_home()
        self.view.show_items(self.items, self._subject_of(self.items.active_id))
        self.data_changed.emit()

    # ======================================================= subjects

    def _subject_new(self, popup: NamePopup) -> None:
        def accept(name: str) -> str:
            subject, error = self.service.create_subject(name)
            if subject is not None:
                self._draw_home()
                self._draw_panel()
            return error
        popup.on_accept = accept

    def _subject_menu(self, subject_id: str, where: QPoint) -> None:
        name = self.service.subject_name(subject_id)
        menu = QMenu(self.home)
        menu.setObjectName("nbMenu")
        menu.addAction("Rename...", lambda: self._rename_subject(subject_id, name, where))
        menu.addAction("Delete subject...", lambda: self._delete_subject(subject_id, name))
        menu.exec(where)

    def _rename_subject(self, subject_id: str, name: str, where: QPoint) -> None:
        popup = NamePopup(self.home, "Rename subject", name)

        def accept(new_name: str) -> str:
            error = self.service.rename_subject(subject_id, new_name)
            if not error:
                self.refresh()
            return error
        popup.on_accept = accept
        popup.show_at(where)

    def _delete_subject(self, subject_id: str, name: str) -> None:
        dialog = ConfirmDialog(self.page, "Delete this subject?",
                               f"“{name}” will be removed. Its notes and cases stay in "
                               "your notebook, with no subject.", "Delete")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.service.delete_subject(subject_id)
            self.refresh()

    def _on_filters(self) -> None:
        self._save_home_view()
        self._draw_home()

    # ==================================================== column tabs

    def _changed(self) -> None:
        """A layout changed: redraw now, save shortly."""
        if self.items.active_id:
            self._dirty.add(self.items.active_id)
            self.view.show_saved("Saving…")
            self._save_timer.start()
        self._draw_workspace()

    def _save_layouts(self) -> None:
        for item_id in list(self._dirty):
            self._flush(item_id)
        self.view.show_saved("Saved")

    def _flush(self, item_id: str) -> None:
        if item_id in self._dirty and item_id in self.workspaces:
            self.service.save_workspace(item_id, self.workspaces[item_id])
        self._dirty.discard(item_id)

    def _activate_tab(self, column: str, tab_id: str) -> None:
        if self.workspace is None:
            return
        self.workspace.column(column).activate(tab_id)
        self._changed()

    def _close_tab(self, column: str, tab_id: str) -> None:
        if self.workspace is None:
            return
        if self.workspace.column(column).close(tab_id) is not None:
            self.view.columns[column].drop_pages({tab_id})
        self._changed()

    def _on_command(self, column: str, name: str, target: str, arg) -> None:
        workspace = self.workspace
        if workspace is None:
            return
        state = workspace.column(column)
        if name == "pin":
            state.set_pinned(target, True)
        elif name == "unpin":
            state.set_pinned(target, False)
        elif name == "duplicate":
            state.duplicate(target)
        elif name == "close":
            self._close_tab(column, target)
            return
        elif name == "close_others":
            closed = state.close_others(target)
            self.view.columns[column].drop_pages({t.id for t in closed})
        elif name == "new_folder":
            folder_name, color = arg
            state.create_folder(folder_name, color, [target])
        elif name == "add_to_folder":
            state.add_to_folder(target, arg)
        elif name == "remove_from_folder":
            state.remove_from_folder(target)
        elif name == "toggle_folder":
            state.toggle_folder(target)
        elif name == "edit_folder":
            folder_name, color = arg
            state.edit_folder(target, folder_name, color)
        elif name == "ungroup":
            state.ungroup(target)
        elif name == "close_folder":
            closed = state.close_folder(target)
            self.view.columns[column].drop_pages({t.id for t in closed})
        elif name == "move_to":
            self._move_tab(column, target, arg, None, "")
            return
        self._changed()

    def _on_tab_dropped(self, source: str, tab_id: str, target: str,
                        index: int, folder_id: str) -> None:
        self._move_tab(source, tab_id, target, index, folder_id)

    def _move_tab(self, source: str, tab_id: str, target: str,
                  index: Optional[int], folder_id: str) -> None:
        workspace = self.workspace
        if workspace is None or workspace.column(source).tab(tab_id) is None:
            return      # the tab belongs to another item's workspace
        if source != target:
            # Carry the page along so anything typed in it survives the move.
            page = self.view.columns[source].take_page(tab_id)
            if page is not None:
                self.view.columns[target].put_page(tab_id, page)
        workspace.move_between(source, tab_id, target, index, folder_id)
        if source != target:
            workspace.column(target).activate(tab_id)
        self._changed()

    # ========================================================= layout

    def _set_collapsed(self, column: str, collapsed: bool) -> None:
        if self.workspace is None:
            return
        self.workspace.column(column).collapsed = collapsed
        self._changed()

    def _toggle_column(self, column: str, visible: bool) -> None:
        workspace = self.workspace
        if workspace is None:
            return
        shown = [c for c in COLUMNS if workspace.column(c).visible]
        if not visible and shown == [column]:
            self._draw_workspace()      # keep at least one column on screen
            return
        workspace.column(column).visible = visible
        if visible:
            workspace.column(column).collapsed = False
        self._changed()

    def _reset_layout(self) -> None:
        workspace = self.workspace
        if workspace is None:
            return
        item = self.service.get(self.items.active_id)
        workspace.sizes = list(DEFAULT_SIZES)
        for name in COLUMNS:
            state = workspace.column(name)
            state.collapsed = False
            state.visible = not (name == "left" and item is not None and item.kind == NOTE
                                 and not state.tabs)
        self._changed()

    def _remember_sizes(self, pixels: list) -> None:
        """Store the dragged widths as percentages, only for the columns
        that are fully open (a rail or a hidden column has no real width)."""
        workspace = self.workspace
        if workspace is None:
            return
        open_columns = [i for i, c in enumerate(COLUMNS)
                        if workspace.column(c).visible and not workspace.column(c).collapsed]
        total_px = sum(pixels[i] for i in open_columns) or 1
        total_pct = sum(workspace.sizes[i] for i in open_columns)
        for i in open_columns:
            workspace.sizes[i] = max(1, round(pixels[i] / total_px * total_pct))
        self._dirty.add(self.items.active_id)
        self._save_timer.start()

    def shutdown(self) -> None:
        """Save anything still waiting (called when the app closes)."""
        self.pages.save_all()
        self._save_timer.stop()
        for item_id in list(self._dirty):
            self._flush(item_id)
