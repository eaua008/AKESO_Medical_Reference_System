"""Level 1: the Study Notebook home.

    ┌ [▣] Study Notebook                        [+ New Note] [+ New Case ▾] ┐
    ├ open items: [Item A][Item B][+] ──────────────────────────────────────┤
    │ LIBRARY        │ [⌕ Search title, tags, or text…]   Sort ▾  [▦][☰]     │
    │  All items   6 │ 6 items found                                        │
    │  Pinned      3 │ ┌card┐ ┌card┐ ┌card┐                                 │
    │  Recent      0 │ └────┘ └────┘ └────┘                                 │
    │ SUBJECTS  +New │ ┌card┐ ...                                          │
    │ TYPE FILTER    │                                                      │
    │ TAGS           │                                                      │
    └────────────────┴──────────────────────────────────────────────────────┘

The view keeps the current filters (self.filters) and reports changes; the
controller asks the service for the matching items and hands them back.
"""

from datetime import datetime
from typing import Optional

from PySide6.QtCore import QPoint, QSize, Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.interaction_styles import tone_color
from app.core.theme import Theme
from app.models.notebook import ITEM_KINDS, NotebookItem, Subject
from app.services.notebook_service import SORTS, Counts, Filters
from app.ui.components.tab_strip import Popup, TabStrip
from app.ui.views.interaction_widgets import FlowLayout

CARD_MIN_WIDTH = 300


def _muted() -> str:
    return Theme.token("TEXT_MUTED")


def _repolish(widget: QWidget) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def short_date(stamp: str) -> str:
    try:
        when = datetime.fromisoformat(stamp)
    except ValueError:
        return ""
    return when.strftime("%b %d") if when.year == datetime.now().year \
        else when.strftime("%b %d, %Y")


class _Clickable(QFrame):
    clicked = Signal()
    right_clicked = Signal(QPoint)

    def __init__(self, object_name: str) -> None:
        super().__init__()
        self.setObjectName(object_name)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_on(self, on: bool) -> None:
        self.setProperty("on", "true" if on else "false")
        _repolish(self)
        for child in self.findChildren(QLabel):
            child.setProperty("on", "true" if on else "false")
            _repolish(child)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.RightButton:
            self.right_clicked.emit(event.globalPosition().toPoint())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
                event.position().toPoint()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)


# ======================================================================
#   Library rail
# ======================================================================

class RailRow(_Clickable):
    """One row in the left rail: icon, label and a count."""

    def __init__(self, icon: str, text: str, count: Optional[int] = None,
                 icon_color: str = "") -> None:
        super().__init__("nbRailRow")
        self.setFixedHeight(32)
        self._icon_name, self._icon_color = icon, icon_color
        row = QHBoxLayout(self)
        row.setContentsMargins(10, 0, 8, 0)
        row.setSpacing(9)
        self.icon = QLabel()
        row.addWidget(self.icon)
        label = QLabel(text, objectName="nbRailText")
        label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        row.addWidget(label, 1)
        if count is not None:
            pill = QLabel(str(count), objectName="nbCount")
            pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pill.setFixedHeight(18)
            pill.setMinimumWidth(22)
            row.addWidget(pill, 0, Qt.AlignmentFlag.AlignVCenter)
        self.paint_icon(False)

    def paint_icon(self, on: bool) -> None:
        color = self._icon_color or (Theme.token("PRIMARY_TEXT_ON_NAV") if on else _muted())
        self.icon.setPixmap(lucide.pixmap(self._icon_name, 15, color))

    def set_on(self, on: bool) -> None:
        super().set_on(on)
        self.paint_icon(on)


class TagChip(_Clickable):
    def __init__(self, tag: str, count: int, on: bool) -> None:
        super().__init__("nbTagChip")
        row = QHBoxLayout(self)
        row.setContentsMargins(9, 3, 9, 3)
        row.addWidget(QLabel(f"{tag}  ({count})", objectName="nbTagText"))
        self.set_on(on)


class NamePopup(Popup):
    """Type a name: used for new and renamed subjects. The popup stays
    open to show an error, so the controller can reject a duplicate."""

    def __init__(self, parent: QWidget, title: str, name: str = "",
                 placeholder: str = "e.g. Cardiology") -> None:
        super().__init__(parent, 250)
        self.on_accept = None           # set by whoever opens it
        self.body.addWidget(QLabel(title, objectName="nbPopupTitle"))
        self.name = QLineEdit(name)
        self.name.setObjectName("nbInput")
        self.name.setPlaceholderText(placeholder)
        self.name.setMaxLength(40)
        self.name.returnPressed.connect(self._accept)
        self.body.addWidget(self.name)
        self.error = QLabel("", objectName="nbError")
        self.error.setWordWrap(True)
        self.error.hide()
        self.body.addWidget(self.error)
        done = QPushButton("Save")
        done.setObjectName("nbButton")
        done.setCursor(Qt.CursorShape.PointingHandCursor)
        done.clicked.connect(self._accept)
        self.body.addWidget(done, 0, Qt.AlignmentFlag.AlignRight)
        self.name.setFocus()
        self.name.selectAll()

    def _accept(self) -> None:
        error = self.on_accept(self.name.text()) if self.on_accept else ""
        if error:
            self.error.setText(error)
            self.error.show()
            self.adjustSize()
        else:
            self.close()


class LibraryRail(QScrollArea):
    changed = Signal()
    subject_new = Signal(QPoint)
    subject_menu = Signal(str, QPoint)

    def __init__(self, filters: Filters) -> None:
        super().__init__()
        self.filters = filters
        self.setWidgetResizable(True)
        self.setFixedWidth(240)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setObjectName("nbLibRail")
        host = QWidget()
        host.setObjectName("panel")
        self._col = QVBoxLayout(host)
        self._col.setContentsMargins(14, 16, 14, 16)
        self._col.setSpacing(3)
        self.setWidget(host)

    def _cap(self, text: str, action: Optional[QWidget] = None) -> None:
        row = QHBoxLayout()
        row.setContentsMargins(4, 14, 2, 4)
        row.addWidget(QLabel(text, objectName="nbRailCap"))
        row.addStretch(1)
        if action is not None:
            row.addWidget(action)
        self._col.addLayout(row)

    def show_counts(self, counts: Counts, subjects: list[Subject]) -> None:
        # Clear everything, including nested layouts.
        def wipe(layout) -> None:
            while layout.count():
                item = layout.takeAt(0)
                widget, child = item.widget(), item.layout()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                elif child is not None:
                    wipe(child)
        wipe(self._col)
        f = self.filters

        self._cap("LIBRARY")
        for key, icon, text in (("all", "book-open", "All items"),
                                ("pinned", "pin", "Pinned"),
                                ("recent", "clock", "Recent")):
            row = RailRow(icon, text, counts.library.get(key, 0))
            row.set_on(f.library == key and not f.subject_id)
            row.clicked.connect(lambda k=key: self._set(library=k, subject_id=""))
            self._col.addWidget(row)

        new = QPushButton("+ New")
        new.setObjectName("nbLinkButton")
        new.setCursor(Qt.CursorShape.PointingHandCursor)
        new.clicked.connect(lambda: self.subject_new.emit(new.mapToGlobal(QPoint(0, 22))))
        self._cap("SUBJECTS", new)
        if not subjects:
            hint = QLabel("No subjects yet. Use + New to add folders like Cardiology.",
                          objectName="nbRailHint")
            hint.setWordWrap(True)
            self._col.addWidget(hint)
        for subject in subjects:
            row = RailRow("folder", subject.name, counts.subjects.get(subject.id, 0))
            row.set_on(f.subject_id == subject.id)
            row.setToolTip("Right-click to rename or delete")
            row.clicked.connect(lambda sid=subject.id: self._set(
                library="all", subject_id="" if self.filters.subject_id == sid else sid))
            row.right_clicked.connect(lambda where, sid=subject.id: self.subject_menu.emit(sid, where))
            self._col.addWidget(row)

        self._cap("TYPE FILTER")
        every = RailRow("layers", "All types", counts.total)
        every.set_on(not f.kind)
        every.clicked.connect(lambda: self._set(kind=""))
        self._col.addWidget(every)
        for kind, (icon, _one, many, tone) in ITEM_KINDS.items():
            row = RailRow(icon, many, counts.kinds.get(kind, 0), tone_color(tone))
            row.set_on(f.kind == kind)
            row.clicked.connect(lambda k=kind: self._set(kind="" if self.filters.kind == k else k))
            self._col.addWidget(row)

        self._cap("TAGS")
        if not counts.tags:
            hint = QLabel("Tags you add to items show up here.", objectName="nbRailHint")
            hint.setWordWrap(True)
            self._col.addWidget(hint)
        else:
            cloud = QWidget()
            cloud.setObjectName("panel")
            flow = FlowLayout(cloud, spacing=5)
            for tag, count in counts.tags:
                chip = TagChip(tag, count, tag in f.tags)
                chip.clicked.connect(lambda t=tag: self._toggle_tag(t))
                flow.addWidget(chip)
            self._col.addWidget(cloud)
        self._col.addStretch(1)

    def _set(self, **changes) -> None:
        for key, value in changes.items():
            setattr(self.filters, key, value)
        self.changed.emit()

    def _toggle_tag(self, tag: str) -> None:
        self.filters.tags ^= {tag}
        self.changed.emit()


# ======================================================================
#   Cards
# ======================================================================

class NotebookCard(_Clickable):
    pin_clicked = Signal()

    def __init__(self, item: NotebookItem, subject: str, selected: bool,
                 compact: bool) -> None:
        super().__init__("nbCard")
        self.item = item
        self.setProperty("selected", "true" if selected else "false")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(78 if compact else 150)

        tile = QLabel()
        tile.setObjectName("nbKindTile")
        tile.setProperty("tone", item.tone)
        tile.setFixedSize(30, 30)
        tile.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tile.setPixmap(lucide.pixmap(item.icon, 15, tone_color(item.tone)))

        title = QLabel(item.title, objectName="nbCardTitle")
        title.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self._title = title

        pin = QPushButton()
        pin.setObjectName("nbIconButton")
        pin.setFixedSize(26, 26)
        pin.setCursor(Qt.CursorShape.PointingHandCursor)
        pin.setToolTip("Unpin" if item.pinned else "Pin")
        pin.setIcon(lucide.icon("pin", 14, tone_color("amber") if item.pinned else _muted()))
        pin.clicked.connect(self.pin_clicked.emit)

        text = item.plain_text or ("Hypothetical study scenario." if item.is_case
                                   else "Empty note.")
        preview = QLabel(text[:200], objectName="nbCardPreview")
        preview.setWordWrap(not compact)
        preview.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self._preview_text = text

        meta = QHBoxLayout()
        meta.setSpacing(8)
        subject_label = QLabel(subject or "No subject", objectName="nbCardSubject")
        subject_label.setProperty("empty", "false" if subject else "true")
        meta.addWidget(subject_label)
        if item.tags:
            tags = QLabel(" · ".join(item.tags[:2]) + (" …" if len(item.tags) > 2 else ""),
                          objectName="nbCardMeta")
            tags.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
            meta.addWidget(tags, 1)
        else:
            meta.addStretch(1)
        meta.addWidget(QLabel(short_date(item.updated_at), objectName="nbCardMeta"))

        if compact:
            row = QHBoxLayout(self)
            row.setContentsMargins(14, 10, 12, 10)
            row.setSpacing(12)
            row.addWidget(tile)
            middle = QVBoxLayout()
            middle.setSpacing(3)
            middle.addWidget(title)
            middle.addWidget(preview)
            row.addLayout(middle, 3)
            side = QVBoxLayout()
            side.addLayout(meta)
            row.addLayout(side, 2)
            row.addWidget(pin)
        else:
            col = QVBoxLayout(self)
            col.setContentsMargins(14, 12, 12, 12)
            col.setSpacing(8)
            head = QHBoxLayout()
            head.setSpacing(10)
            head.addWidget(tile)
            head.addWidget(title, 1)
            head.addWidget(pin, 0, Qt.AlignmentFlag.AlignTop)
            col.addLayout(head)
            preview.setMaximumHeight(2 * preview.fontMetrics().lineSpacing() + 2)
            preview.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            col.addWidget(preview, 1)
            col.addLayout(meta)
        self._preview = preview
        self._compact = compact

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        # Elide by hand: Qt labels clip text but never add "…" when wrapping.
        width = max(60, self._title.width())
        self._title.setText(self._title.fontMetrics().elidedText(
            self.item.title, Qt.TextElideMode.ElideRight, width))
        lines = 1 if self._compact else 2
        pw = max(60, self._preview.width())
        self._preview.setText(self._preview.fontMetrics().elidedText(
            self._preview_text, Qt.TextElideMode.ElideRight, pw * lines - 24 * lines))


# ======================================================================
#   The page
# ======================================================================

class NotebookHome(QWidget):
    filters_changed = Signal()
    new_note_requested = Signal()
    sync_requested = Signal()                   # "Sync now" (cloud copy, migration 011)
    new_case_requested = Signal(str)            # symptom_case | interaction_case
    item_clicked = Signal(str)
    item_action = Signal(str, str)              # action, item id
    subject_new = Signal(object)                # NamePopup
    subject_menu = Signal(str, QPoint)
    view_mode_changed = Signal(str)             # grid | list

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("nbPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.filters = Filters()
        self.view_mode = "grid"
        self._cards: list[NotebookCard] = []
        self._columns = 0
        self._icon_jobs: list = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._build_header())

        self.item_strip = TabStrip("items", group="items", title="Open items",
                                   allow_folders=False, allow_duplicate=False,
                                   new_tooltip="New note", object_name="nbItemBar")
        outer.addWidget(self.item_strip)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        self.rail = LibraryRail(self.filters)
        self.rail.changed.connect(self.filters_changed.emit)
        self.rail.subject_new.connect(self._new_subject)
        self.rail.subject_menu.connect(self.subject_menu.emit)
        body.addWidget(self.rail)
        body.addWidget(self._build_list(), 1)
        outer.addLayout(body, 1)
        self.refresh_icons()

    # ------------------------------------------------------------- building

    def _job(self, widget, icon: str, size: int, tone: str) -> None:
        self._icon_jobs.append((widget, icon, size, tone))

    def _build_header(self) -> QWidget:
        head = QFrame()
        head.setObjectName("nbHomeHeader")
        row = QHBoxLayout(head)
        row.setContentsMargins(24, 18, 24, 16)
        row.setSpacing(14)
        tile = QLabel()
        tile.setObjectName("nbIconTile")
        tile.setFixedSize(42, 42)
        tile.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._job(tile, "notebook-pen", 20, "white")
        row.addWidget(tile)
        titles = QVBoxLayout()
        titles.setSpacing(1)
        titles.addWidget(QLabel("Study Notebook", objectName="nbTitle"))
        titles.addWidget(QLabel("Your notes and case studies, organised by subject.",
                                objectName="nbSubtitle"))
        # Cloud copy status: "Synced to your account just now" / offline.
        sync_row = QHBoxLayout()
        sync_row.setSpacing(8)
        self._sync_label = QLabel("", objectName="nbSubtitle")
        self._sync_tone = "muted"
        self._sync_button = QPushButton("Sync now")
        self._sync_button.setObjectName("nbLink")
        self._sync_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._sync_button.setFlat(True)
        self._sync_button.clicked.connect(self.sync_requested.emit)
        self._sync_button.hide()
        sync_row.addWidget(self._sync_label)
        sync_row.addWidget(self._sync_button)
        sync_row.addStretch(1)
        titles.addLayout(sync_row)
        row.addLayout(titles, 1)

        note = QPushButton("  New Note")
        note.setObjectName("nbButton")
        note.setCursor(Qt.CursorShape.PointingHandCursor)
        self._job(note, "plus", 14, "text")
        note.clicked.connect(self.new_note_requested.emit)
        row.addWidget(note)

        case = QPushButton("  New Case  ")
        case.setObjectName("nbPrimary")
        case.setCursor(Qt.CursorShape.PointingHandCursor)
        self._job(case, "plus", 14, "white")
        menu = QMenu(case)
        menu.setObjectName("nbMenu")
        symptom = menu.addAction("Symptom case  ·  build it in the Symptom Checker")
        symptom.triggered.connect(lambda: self.new_case_requested.emit("symptom_case"))
        interaction = menu.addAction("Interaction case  ·  build it in the Drug Interaction Checker")
        interaction.triggered.connect(lambda: self.new_case_requested.emit("interaction_case"))
        case.clicked.connect(lambda: menu.exec(case.mapToGlobal(QPoint(0, case.height() + 4))))
        row.addWidget(case)
        return head

    def _build_list(self) -> QWidget:
        host = QWidget()
        host.setObjectName("panel")
        col = QVBoxLayout(host)
        col.setContentsMargins(22, 16, 22, 0)
        col.setSpacing(10)

        tools = QHBoxLayout()
        tools.setSpacing(8)
        field = QFrame()
        field.setObjectName("nbSearchField")
        field.setFixedHeight(38)
        frow = QHBoxLayout(field)
        frow.setContentsMargins(11, 0, 8, 0)
        frow.setSpacing(7)
        icon = QLabel()
        self._job(icon, "search", 15, "muted")
        frow.addWidget(icon)
        self.search = QLineEdit()
        self.search.setObjectName("nbSearchInput")
        self.search.setPlaceholderText("Search title, tags, or text...")
        self.search.setClearButtonEnabled(True)
        self._search_timer = QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(200)
        self._search_timer.timeout.connect(self._query_changed)
        self.search.textChanged.connect(lambda _t: self._search_timer.start())
        frow.addWidget(self.search, 1)
        tools.addWidget(field, 1)

        tools.addWidget(QLabel("Sort:", objectName="nbSmallMuted"))
        self.sort = QComboBox()
        self.sort.setObjectName("nbCombo")
        for key, label in SORTS.items():
            self.sort.addItem(label, key)
        self.sort.currentIndexChanged.connect(self._sort_changed)
        tools.addWidget(self.sort)

        self.mode_buttons: dict[str, QPushButton] = {}
        for mode, icon_name, tip in (("grid", "layout-grid", "Grid"), ("list", "list", "List")):
            button = QPushButton()
            button.setObjectName("nbToggle")
            button.setCheckable(True)
            button.setFixedSize(34, 32)
            button.setToolTip(tip)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self._job(button, icon_name, 15, "primary")
            button.clicked.connect(lambda _c, m=mode: self.set_view_mode(m, emit=True))
            self.mode_buttons[mode] = button
            tools.addWidget(button)
        col.addLayout(tools)

        self.found = QLabel("", objectName="nbSmallMuted")
        col.addWidget(self.found)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        grid_host = QWidget()
        grid_host.setObjectName("panel")
        wrap = QVBoxLayout(grid_host)
        wrap.setContentsMargins(0, 2, 6, 20)
        wrap.setSpacing(0)
        self.grid = QGridLayout()
        self.grid.setSpacing(12)
        wrap.addLayout(self.grid)
        self.empty = QFrame()
        self.empty.setObjectName("nbPlaceholder")
        ecol = QVBoxLayout(self.empty)
        ecol.setContentsMargins(24, 30, 24, 30)
        ecol.setSpacing(6)
        self.empty_icon = QLabel()
        self.empty_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._job(self.empty_icon, "notebook-pen", 30, "primary")
        ecol.addWidget(self.empty_icon)
        self.empty_title = QLabel("", objectName="nbPlaceholderTitle")
        self.empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ecol.addWidget(self.empty_title)
        self.empty_text = QLabel("", objectName="nbPlaceholderText")
        self.empty_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_text.setWordWrap(True)
        ecol.addWidget(self.empty_text)
        wrap.addWidget(self.empty)
        wrap.addStretch(1)
        self.scroll.setWidget(grid_host)
        col.addWidget(self.scroll, 1)
        self.set_view_mode("grid")
        return host

    # -------------------------------------------------------------- events

    def _query_changed(self) -> None:
        self.filters.query = self.search.text()
        self.filters_changed.emit()

    def _sort_changed(self) -> None:
        self.filters.sort = self.sort.currentData()
        self.filters_changed.emit()

    def set_view_mode(self, mode: str, emit: bool = False) -> None:
        self.view_mode = mode
        for key, button in self.mode_buttons.items():
            button.setChecked(key == mode)
        if emit:
            self.view_mode_changed.emit(mode)
            self.filters_changed.emit()

    def set_sort(self, key: str) -> None:
        index = self.sort.findData(key)
        if index >= 0:
            self.sort.blockSignals(True)
            self.sort.setCurrentIndex(index)
            self.sort.blockSignals(False)
            self.filters.sort = key

    def _new_subject(self, where: QPoint) -> None:
        popup = NamePopup(self, "New subject")
        self.subject_new.emit(popup)        # the controller sets on_accept
        popup.show_at(where)

    # ------------------------------------------------------------- drawing

    def show_counts(self, counts: Counts, subjects: list[Subject]) -> None:
        self.rail.show_counts(counts, subjects)

    def show_items(self, items: list[NotebookItem], subjects: dict[str, str],
                   selected_id: str, total: int) -> None:
        for card in self._cards:
            card.setParent(None)
            card.deleteLater()
        self._cards = []
        compact = self.view_mode == "list"
        for item in items:
            card = NotebookCard(item, subjects.get(item.subject_id, ""),
                                item.id == selected_id, compact)
            card.clicked.connect(lambda iid=item.id: self.item_clicked.emit(iid))
            card.pin_clicked.connect(lambda iid=item.id: self.item_action.emit("pin", iid))
            card.right_clicked.connect(lambda where, it=item: self._card_menu(it, where))
            self._cards.append(card)
        self._columns = 0
        self._layout_cards()

        n = len(items)
        self.found.setText(f"{n} item{'s' if n != 1 else ''} found")
        self.empty.setVisible(n == 0)
        if total == 0:
            self.empty_title.setText("Nothing here yet")
            self.empty_text.setText("Write a note, or save a case from the Symptom Checker "
                                    "or the Drug Interaction Checker.")
        else:
            self.empty_title.setText("No items match")
            self.empty_text.setText("Try another search, subject, type or tag.")

    def _layout_cards(self) -> None:
        width = self.scroll.viewport().width() - 6
        columns = 1 if self.view_mode == "list" else max(1, width // CARD_MIN_WIDTH)
        if columns == self._columns and self.grid.count() == len(self._cards):
            return
        self._columns = columns
        while self.grid.count():
            self.grid.takeAt(0)
        for c in range(4):
            self.grid.setColumnStretch(c, 1 if c < columns else 0)
        for i, card in enumerate(self._cards):
            self.grid.addWidget(card, i // columns, i % columns)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._layout_cards()

    def _card_menu(self, item: NotebookItem, where: QPoint) -> None:
        menu = QMenu(self)
        menu.setObjectName("nbMenu")
        menu.addAction("Open", lambda: self.item_clicked.emit(item.id))
        menu.addAction("Open workspace", lambda: self.item_action.emit("workspace", item.id))
        menu.addAction("Unpin" if item.pinned else "Pin",
                       lambda: self.item_action.emit("pin", item.id))
        menu.addAction("Duplicate", lambda: self.item_action.emit("duplicate", item.id))
        if item.has_case_data:
            menu.addAction("Share to Clinical Exchange…",
                           lambda: self.item_action.emit("share", item.id))
        menu.addSeparator()
        menu.addAction("Delete...", lambda: self.item_action.emit("delete", item.id))
        menu.exec(where)

    # --------------------------------------------------------------- theme

    def refresh_icons(self) -> None:
        for widget, icon, size, tone in self._icon_jobs:
            if isinstance(widget, QPushButton):
                widget.setIcon(lucide.icon(icon, size, tone_color(tone)))
                widget.setIconSize(QSize(size, size))
            else:
                widget.setPixmap(lucide.pixmap(icon, size, tone_color(tone)))

    def set_sync_status(self, text: str, tone: str = "muted") -> None:
        """tone: muted (working), good (synced) or warn (offline / not set up)."""
        self._sync_tone = tone
        self._sync_label.setText(text)
        self._sync_button.setVisible(bool(text) and tone != "muted")
        self._paint_sync()

    def _paint_sync(self) -> None:
        color = {"good": tone_color("success"), "warn": tone_color("amber")}.get(
            self._sync_tone, Theme.token("TEXT_MUTED"))
        self._sync_label.setStyleSheet(f"color: {color};")
        self._sync_button.setStyleSheet(
            f"QPushButton {{ color: {Theme.token('PRIMARY_TEXT_ON_NAV')}; background: transparent;"
            f" border: none; font-weight: 600; padding: 0; }}"
            f" QPushButton:hover {{ text-decoration: underline; }}")

    def refresh_theme(self) -> None:
        self._paint_sync()
        self.refresh_icons()
        self.item_strip.refresh_theme()
