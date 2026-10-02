"""The Study Notebook workspace: which tabs are open, in which column, in
which folder.

This file is pure Python, with no Qt. The views only draw these objects,
and every change goes through the methods below. That keeps the rules in
one place and makes them testable without opening a window.

The key idea: a tab stores WHAT IT POINTS TO (kind + ref, e.g. "disease" +
"dengue"), never a copy of the content. The content is looked up when the
tab is shown, so a workspace stays small and always shows current data.

    WorkspaceState          one per notebook item
      columns["left"]       ColumnState: tabs, folders, active tab
      columns["center"]
      columns["right"]
      sizes                 column width percentages, e.g. [30, 40, 30]
"""

import html
import re
import uuid
from dataclasses import dataclass, field
from typing import Optional

# ----------------------------------------------------------------------
#   Notebook items
# ----------------------------------------------------------------------

NOTE = "note"
SYMPTOM_CASE = "symptom_case"
INTERACTION_CASE = "interaction_case"

# kind -> (lucide icon, singular label, plural label, tone)
ITEM_KINDS = {
    NOTE: ("notebook-pen", "Note", "Notes", "primary"),
    SYMPTOM_CASE: ("stethoscope", "Symptom case", "Symptom Cases", "success"),
    INTERACTION_CASE: ("shield-check", "Interaction case", "Interaction Cases", "amber"),
}

# ----------------------------------------------------------------------
#   Workspace tabs
# ----------------------------------------------------------------------

COLUMNS = ("left", "center", "right")
COLUMN_TITLES = {"left": "Case", "center": "Notes", "right": "Reference"}

FOLDER_COLORS = ("purple", "amber", "green", "blue", "rose", "slate")

# kind -> (lucide icon, what a new tab of this kind is called)
TAB_KINDS = {
    "case": ("stethoscope", "Case"),
    "note": ("notebook-pen", "Untitled note"),
    "search": ("search", "Search"),
    "disease": ("book-open", "Disease"),
    "symptom": ("activity", "Symptom"),
    "medicine": ("pill", "Medicine"),
    "item": ("file-text", "Untitled item"),
    # open-items bar tabs use the notebook item's kind
    "symptom_case": ("stethoscope", "Symptom case"),
    "interaction_case": ("shield-check", "Interaction case"),
}

# What "+" opens in each column.
NEW_TAB_KIND = {"left": "case", "center": "note", "right": "search", "items": "item"}

DEFAULT_SIZES = [30, 40, 30]


def new_id() -> str:
    return uuid.uuid4().hex[:12]


@dataclass
class Tab:
    id: str
    kind: str
    title: str
    ref: str = ""            # the id it points to (a disease, a note...)
    folder_id: str = ""      # "" = not in a folder
    pinned: bool = False

    @property
    def icon(self) -> str:
        return TAB_KINDS.get(self.kind, ("file-text", ""))[0]

    @classmethod
    def create(cls, kind: str, title: str = "", ref: str = "") -> "Tab":
        return cls(id=new_id(), kind=kind,
                   title=title or TAB_KINDS.get(kind, ("", "Tab"))[1], ref=ref)


@dataclass
class TabFolder:
    id: str
    name: str
    color: str = "purple"
    open: bool = True


@dataclass
class ColumnState:
    """The tabs of one column (or of the open-items bar)."""

    tabs: list[Tab] = field(default_factory=list)
    folders: list[TabFolder] = field(default_factory=list)
    active_id: str = ""
    collapsed: bool = False     # shrunk to a slim rail
    visible: bool = True        # hidden with the column toggle

    # ------------------------------------------------------------ lookups

    def tab(self, tab_id: str) -> Optional[Tab]:
        return next((t for t in self.tabs if t.id == tab_id), None)

    def folder(self, folder_id: str) -> Optional[TabFolder]:
        return next((f for f in self.folders if f.id == folder_id), None)

    def index_of(self, tab_id: str) -> int:
        return next((i for i, t in enumerate(self.tabs) if t.id == tab_id), -1)

    def members(self, folder_id: str) -> list[Tab]:
        return [t for t in self.tabs if t.folder_id == folder_id]

    @property
    def active(self) -> Optional[Tab]:
        return self.tab(self.active_id)

    def is_hidden(self, tab: Tab) -> bool:
        """True when the tab sits inside a folded folder."""
        folder = self.folder(tab.folder_id) if tab.folder_id else None
        return folder is not None and not folder.open

    # ------------------------------------------------------------- tabs

    def add(self, tab: Tab, activate: bool = True, index: Optional[int] = None) -> Tab:
        if index is None or not 0 <= index <= len(self.tabs):
            self.tabs.append(tab)
        else:
            self.tabs.insert(index, tab)
        if activate or not self.active_id:
            self.active_id = tab.id
        self._normalise()
        return tab

    def activate(self, tab_id: str) -> None:
        tab = self.tab(tab_id)
        if tab is None:
            return
        # Activating a tab inside a folded folder opens that folder.
        folder = self.folder(tab.folder_id) if tab.folder_id else None
        if folder is not None:
            folder.open = True
        self.active_id = tab_id

    def close(self, tab_id: str) -> Optional[Tab]:
        """Remove a tab. The neighbour to its right (or left) becomes active,
        like a browser."""
        index = self.index_of(tab_id)
        if index < 0:
            return None
        tab = self.tabs.pop(index)
        if self.active_id == tab_id:
            self.active_id = self._neighbour(index)
        self._drop_empty_folders()
        return tab

    def close_others(self, keep_id: str) -> list[Tab]:
        """Close every tab except keep_id and the pinned ones."""
        closed = [t for t in self.tabs if t.id != keep_id and not t.pinned]
        self.tabs = [t for t in self.tabs if t.id == keep_id or t.pinned]
        self.active_id = keep_id if self.tab(keep_id) else self._neighbour(0)
        self._drop_empty_folders()
        return closed

    def duplicate(self, tab_id: str) -> Optional[Tab]:
        tab = self.tab(tab_id)
        if tab is None:
            return None
        copy = Tab(id=new_id(), kind=tab.kind, title=tab.title, ref=tab.ref,
                   folder_id=tab.folder_id)
        return self.add(copy, index=self.index_of(tab_id) + 1)

    def move(self, tab_id: str, index: int, folder_id: Optional[str] = None) -> None:
        """Drag and drop inside one column. folder_id None keeps the folder,
        "" takes the tab out, an id puts it in that folder."""
        old = self.index_of(tab_id)
        if old < 0:
            return
        tab = self.tabs.pop(old)
        if index > old:
            index -= 1              # the list got shorter in front of the target
        index = max(0, min(index, len(self.tabs)))
        self.tabs.insert(index, tab)
        if folder_id is not None and not tab.pinned:
            tab.folder_id = folder_id if self.folder(folder_id) else ""
        self._drop_empty_folders()
        self._normalise()

    def set_pinned(self, tab_id: str, pinned: bool) -> None:
        tab = self.tab(tab_id)
        if tab is None:
            return
        tab.pinned = pinned
        if pinned:
            tab.folder_id = ""      # pinned tabs live at the front, outside folders
        self._drop_empty_folders()
        self._normalise()

    def rename_tab(self, tab_id: str, title: str) -> None:
        tab = self.tab(tab_id)
        if tab is not None and title.strip():
            tab.title = title.strip()

    # ---------------------------------------------------------- folders

    def create_folder(self, name: str, color: str, tab_ids: list[str]) -> TabFolder:
        folder = TabFolder(id=new_id(), name=name.strip() or "Folder",
                           color=color if color in FOLDER_COLORS else "purple")
        self.folders.append(folder)
        for tab_id in tab_ids:
            tab = self.tab(tab_id)
            if tab is not None:
                tab.pinned = False
                tab.folder_id = folder.id
        self._drop_empty_folders()
        self._normalise()
        return folder

    def add_to_folder(self, tab_id: str, folder_id: str) -> None:
        tab, folder = self.tab(tab_id), self.folder(folder_id)
        if tab is None or folder is None:
            return
        tab.pinned = False
        tab.folder_id = folder_id
        # Move it to the end of the folder so the folder stays in one piece.
        self.tabs.remove(tab)
        members = [i for i, t in enumerate(self.tabs) if t.folder_id == folder_id]
        self.tabs.insert(members[-1] + 1 if members else len(self.tabs), tab)
        self._drop_empty_folders()
        self._normalise()

    def remove_from_folder(self, tab_id: str) -> None:
        tab = self.tab(tab_id)
        if tab is None or not tab.folder_id:
            return
        folder_id = tab.folder_id
        tab.folder_id = ""
        # Put it just after the folder instead of leaving it in the middle.
        self.tabs.remove(tab)
        members = [i for i, t in enumerate(self.tabs) if t.folder_id == folder_id]
        self.tabs.insert(members[-1] + 1 if members else len(self.tabs), tab)
        self._drop_empty_folders()

    def toggle_folder(self, folder_id: str) -> None:
        folder = self.folder(folder_id)
        if folder is None:
            return
        folder.open = not folder.open
        active = self.active
        if not folder.open and active is not None and active.folder_id == folder_id:
            # Folding hides the active tab: move focus to a visible one.
            visible = [t for t in self.tabs if not self.is_hidden(t)]
            if visible:
                self.active_id = visible[0].id
            else:
                folder.open = True  # nothing else to show, so refuse to fold

    def edit_folder(self, folder_id: str, name: str, color: str) -> None:
        folder = self.folder(folder_id)
        if folder is None:
            return
        if name.strip():
            folder.name = name.strip()
        if color in FOLDER_COLORS:
            folder.color = color

    def ungroup(self, folder_id: str) -> None:
        """Delete the folder but keep its tabs."""
        for tab in self.members(folder_id):
            tab.folder_id = ""
        self.folders = [f for f in self.folders if f.id != folder_id]

    def close_folder(self, folder_id: str) -> list[Tab]:
        """Close the folder and every tab in it."""
        closed = self.members(folder_id)
        for tab in closed:
            self.close(tab.id)
        self.folders = [f for f in self.folders if f.id != folder_id]
        return closed

    def next_folder_color(self) -> str:
        used = [f.color for f in self.folders]
        return next((c for c in FOLDER_COLORS if c not in used), FOLDER_COLORS[0])

    # ------------------------------------------------------------ rules

    def _neighbour(self, index: int) -> str:
        visible = [t for t in self.tabs if not self.is_hidden(t)] or self.tabs
        if not visible:
            return ""
        # Prefer the tab that slid into the closed tab's place.
        for tab in self.tabs[index:]:
            if tab in visible:
                return tab.id
        return visible[-1].id

    def _drop_empty_folders(self) -> None:
        used = {t.folder_id for t in self.tabs}
        self.folders = [f for f in self.folders if f.id in used]

    def _normalise(self) -> None:
        """Pinned tabs first, and each folder's tabs next to each other."""
        pinned = [t for t in self.tabs if t.pinned]
        rest = [t for t in self.tabs if not t.pinned]
        ordered: list[Tab] = []
        done: set[str] = set()
        for tab in rest:
            if not tab.folder_id:
                ordered.append(tab)
            elif tab.folder_id not in done:
                done.add(tab.folder_id)
                ordered.extend(t for t in rest if t.folder_id == tab.folder_id)
        self.tabs = pinned + ordered
        # Folders are listed in the order they appear in the strip.
        order = {fid: i for i, fid in enumerate(dict.fromkeys(t.folder_id for t in self.tabs))}
        self.folders.sort(key=lambda f: order.get(f.id, len(order)))

    # --------------------------------------------------------- storage

    def to_dict(self) -> dict:
        return {
            "tabs": [vars(t).copy() for t in self.tabs],
            "folders": [vars(f).copy() for f in self.folders],
            "active_id": self.active_id,
            "collapsed": self.collapsed,
            "visible": self.visible,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ColumnState":
        state = cls(tabs=[Tab(**t) for t in data.get("tabs", [])],
                    folders=[TabFolder(**f) for f in data.get("folders", [])],
                    active_id=data.get("active_id", ""),
                    collapsed=bool(data.get("collapsed", False)),
                    visible=bool(data.get("visible", True)))
        if not state.tab(state.active_id):
            state.active_id = state.tabs[0].id if state.tabs else ""
        state._drop_empty_folders()
        state._normalise()
        return state


@dataclass
class WorkspaceState:
    """Everything the three columns show for one notebook item."""

    columns: dict[str, ColumnState] = field(
        default_factory=lambda: {name: ColumnState() for name in COLUMNS})
    sizes: list[int] = field(default_factory=lambda: list(DEFAULT_SIZES))

    def column(self, name: str) -> ColumnState:
        return self.columns[name]

    def move_between(self, source: str, tab_id: str, target: str,
                     index: Optional[int] = None, folder_id: str = "") -> Optional[Tab]:
        """Drag a tab from one column into another."""
        if source == target:
            self.columns[source].move(tab_id, len(self.columns[source].tabs)
                                      if index is None else index, folder_id)
            return self.columns[source].tab(tab_id)
        tab = self.columns[source].close(tab_id)
        if tab is None:
            return None
        tab.folder_id = folder_id if self.columns[target].folder(folder_id) else ""
        tab.pinned = False
        target_column = self.columns[target]
        target_column.visible = True
        target_column.collapsed = False
        return target_column.add(tab, index=index)

    @classmethod
    def default_for(cls, item_kind: str, item_id: str = "") -> "WorkspaceState":
        """The starting layout. A plain note has no case, so its left
        column starts hidden. The first case and notes tabs point back at
        the item itself."""
        state = cls()
        if item_kind == NOTE:
            state.columns["left"].visible = False
        else:
            state.columns["left"].add(Tab.create("case", "Case", ref=item_id))
        state.columns["center"].add(Tab.create("note", "My notes", ref=item_id))
        state.columns["right"].add(Tab.create("search"))
        return state

    def to_dict(self) -> dict:
        return {"columns": {n: c.to_dict() for n, c in self.columns.items()},
                "sizes": list(self.sizes)}

    @classmethod
    def from_dict(cls, data: dict) -> "WorkspaceState":
        columns = {name: ColumnState.from_dict(data.get("columns", {}).get(name, {}))
                   for name in COLUMNS}
        sizes = data.get("sizes") or list(DEFAULT_SIZES)
        return cls(columns=columns, sizes=[int(s) for s in sizes][:3])


# ======================================================================
#   What the notebook stores
# ======================================================================

@dataclass
class Subject:
    """A folder on the notebook home, e.g. "Cardiology"."""

    id: str
    name: str
    created_at: str = ""


@dataclass
class NotebookItem:
    """One note or case study in the Study Notebook.

    body        the student's notes, as rich text (HTML from the editor)
    case        the case itself, by reference ids only. For an interaction
                case: candidate_id, regimen_ids, condition_ids. Never a
                real patient's details.
    workspace   the tabs, folders and column widths last used for it
    """

    id: str
    kind: str
    title: str
    subject_id: str = ""
    tags: list[str] = field(default_factory=list)
    body: str = ""
    case: dict = field(default_factory=dict)
    pinned: bool = False
    created_at: str = ""
    updated_at: str = ""
    opened_at: str = ""
    workspace: Optional[WorkspaceState] = None

    @property
    def icon(self) -> str:
        return ITEM_KINDS.get(self.kind, ITEM_KINDS[NOTE])[0]

    @property
    def kind_label(self) -> str:
        return ITEM_KINDS.get(self.kind, ITEM_KINDS[NOTE])[1]

    @property
    def tone(self) -> str:
        return ITEM_KINDS.get(self.kind, ITEM_KINDS[NOTE])[3]

    @property
    def is_case(self) -> bool:
        return self.kind != NOTE

    # A note (or case) can have a Symptom Checker run and a Drug Interaction
    # Checker run attached. A symptom case keeps its run at the top level of
    # `case` (as saved before), a note keeps it under case["symptom"].
    @property
    def symptom_data(self) -> dict:
        return self.case if self.kind == SYMPTOM_CASE else (self.case.get("symptom") or {})

    @property
    def interaction_data(self) -> dict:
        if self.kind == INTERACTION_CASE:
            return self.case
        return self.case.get("interaction") or {}

    @property
    def has_case_data(self) -> bool:
        return bool(self.symptom_data.get("symptoms")) or \
            bool(self.interaction_data.get("candidate_id"))

    @property
    def plain_text(self) -> str:
        """The notes without formatting, for previews and search."""
        text = self.body
        if "<" in text:
            text = re.sub(r"(?is)<(style|head)[^>]*>.*?</\1>", " ", text)
            text = re.sub(r"(?s)<[^>]+>", " ", text)
            text = html.unescape(text)
        text = text or str(self.case.get("notes", ""))
        return " ".join(text.split())
