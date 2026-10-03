"""TabStrip: browser-style tabs with Chrome-style folders.

Qt's own QTabBar cannot show folders, so this is a custom widget. It is
reused twice in the Study Notebook:

    the open-items bar      one tab per notebook item you have open
    each workspace column   the tabs inside Case / Notes / Reference

The strip only DRAWS a ColumnState and reports what the user did. It never
changes the state itself: it emits a signal, the controller changes the
model, and the strip is drawn again. One direction, easy to follow.

    [pinned][tab][tab] (Folder ▾)[tab][tab] (Folder 3 ▸)[tab] ...  [+] [≡] [«]

Mouse:
    click                   activate
    middle-click / ✕        close
    drag                    reorder, drop on a folder label, or drop into
                            another column's strip
    right-click             tab or folder menu
    wheel                   scroll when there are more tabs than fit
"""

from typing import Optional

from PySide6.QtCore import QMimeData, QPoint, QRect, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QDrag, QFontMetrics, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QScrollArea,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.notebook_styles import folder_hex
from app.core.theme import Theme
from app.models.notebook import FOLDER_COLORS, ColumnState, Tab, TabFolder

MIME = "application/x-akeso-tab"
TAB_HEIGHT = 30
TITLE_WIDTH = 132           # longer titles are elided with "…"


def _muted() -> str:
    return Theme.token("TEXT_MUTED")


def _icon_button(icon: str, tooltip: str, size: int = 26) -> QPushButton:
    button = QPushButton()
    button.setObjectName("nbIconButton")
    button.setFixedSize(size, size)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setToolTip(tooltip)
    button.setProperty("lucide", icon)
    button.setIcon(lucide.icon(icon, 15, _muted()))
    return button


def _repolish(widget: QWidget) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def dot_icon(color: str, size: int = 10) -> QIcon:
    image = QPixmap(size * 2, size * 2)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(folder_hex(color)))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(0, 0, size * 2, size * 2)
    painter.end()
    image.setDevicePixelRatio(2)
    return QIcon(image)


def _encode(group: str, column: str, tab_id: str) -> bytes:
    return f"{group}|{column}|{tab_id}".encode()


def decode(mime: QMimeData) -> Optional[tuple[str, str, str]]:
    if not mime.hasFormat(MIME):
        return None
    parts = bytes(mime.data(MIME)).decode().split("|")
    return (parts[0], parts[1], parts[2]) if len(parts) == 3 else None


# ======================================================================
#   One tab
# ======================================================================

class TabButton(QFrame):
    clicked = Signal(str)
    close_clicked = Signal(str)
    context = Signal(str, QPoint)

    def __init__(self, tab: Tab, active: bool, group: str, column: str,
                 folder_color: str = "") -> None:
        super().__init__()
        self.tab = tab
        self._group = group
        self._column = column
        self._press: Optional[QPoint] = None
        self.setObjectName("nbTab")
        self.setProperty("active", "true" if active else "false")
        if folder_color:
            self.setProperty("folder", folder_color)
        self.setFixedHeight(TAB_HEIGHT)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tab.title)

        row = QHBoxLayout(self)
        row.setContentsMargins(9, 0, 5 if not tab.pinned else 9, 0)
        row.setSpacing(6)
        tone = Theme.token("PRIMARY_TEXT_ON_NAV") if active else _muted()
        icon = QLabel()
        icon.setPixmap(lucide.pixmap(tab.icon, 13, tone))
        row.addWidget(icon)
        if tab.pinned:
            pin = QLabel()
            pin.setPixmap(lucide.pixmap("pin", 11, _muted()))
            row.addWidget(pin)

        metrics = QFontMetrics(self.font())
        title = QLabel(metrics.elidedText(tab.title, Qt.TextElideMode.ElideRight,
                                          TITLE_WIDTH))
        title.setObjectName("nbTabTitle")
        row.addWidget(title)

        if not tab.pinned:
            close = QPushButton()
            close.setObjectName("nbTabClose")
            close.setFixedSize(18, 18)
            close.setIcon(lucide.icon("x", 12, _muted()))
            close.setCursor(Qt.CursorShape.PointingHandCursor)
            close.setToolTip("Close tab")
            close.clicked.connect(lambda: self.close_clicked.emit(self.tab.id))
            row.addWidget(close)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.RightButton:
            self.context.emit(self.tab.id, event.globalPosition().toPoint())
        elif event.button() == Qt.MouseButton.MiddleButton and not self.tab.pinned:
            self.close_clicked.emit(self.tab.id)
        elif event.button() == Qt.MouseButton.LeftButton:
            self._press = event.position().toPoint()

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if self._press is None:
            return
        distance = (event.position().toPoint() - self._press).manhattanLength()
        if distance < QApplication.startDragDistance():
            return
        self._press = None
        mime = QMimeData()
        mime.setData(MIME, _encode(self._group, self._column, self.tab.id))
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.setPixmap(self.grab())
        drag.setHotSpot(QPoint(self.width() // 2, self.height() // 2))
        # exec() runs its own event loop until the drop. The strip may be
        # redrawn after it returns, so nothing below may touch `self`.
        drag.exec(Qt.DropAction.MoveAction)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if self._press is not None and event.button() == Qt.MouseButton.LeftButton:
            self._press = None
            self.clicked.emit(self.tab.id)


# ======================================================================
#   A folder label
# ======================================================================

class FolderChip(QFrame):
    clicked = Signal(str)
    context = Signal(str, QPoint)

    def __init__(self, folder: TabFolder, count: int) -> None:
        super().__init__()
        self.folder = folder
        self.setObjectName("nbFolderChip")
        self.setProperty("color", folder.color)
        self.setProperty("open", "true" if folder.open else "false")
        self.setFixedHeight(22)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Click to fold or unfold. Drop a tab here to add it.")

        row = QHBoxLayout(self)
        row.setContentsMargins(9, 0, 7, 0)
        row.setSpacing(4)
        text = folder.name if folder.open else f"{folder.name} · {count}"
        row.addWidget(QLabel(text))
        dark = Theme.mode() == "dark"
        chevron_tone = folder_hex(folder.color) if not folder.open else (
            "#111118" if dark else "#FFFFFF")
        chevron = QLabel()
        chevron.setPixmap(lucide.pixmap(
            "chevron-down" if folder.open else "chevron-right", 12, chevron_tone))
        row.addWidget(chevron)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.RightButton:
            self.context.emit(self.folder.id, event.globalPosition().toPoint())
        elif event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.folder.id)

    # Drops onto the label are handled by the strip, which knows the state.


# ======================================================================
#   Popups
# ======================================================================

class _Popup(QFrame):
    """A small floating card that closes when you click elsewhere."""

    def __init__(self, parent: QWidget, width: int) -> None:
        super().__init__(parent, Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setObjectName("nbPopup")
        self.setFixedWidth(width)
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(12, 11, 12, 12)
        self.body.setSpacing(8)

    def show_at(self, global_pos: QPoint) -> None:
        self.adjustSize()
        screen = QApplication.screenAt(global_pos) or QApplication.primaryScreen()
        area = screen.availableGeometry()
        x = min(global_pos.x(), area.right() - self.width() - 8)
        y = min(global_pos.y(), area.bottom() - self.height() - 8)
        self.move(max(area.left(), x), max(area.top(), y))
        self.show()


Popup = _Popup      # public name, for other views that need a small popup


class FolderEditor(_Popup):
    """Name and colour for a new or existing folder, like Chrome's."""

    accepted = Signal(str, str)

    def __init__(self, parent: QWidget, title: str, name: str, color: str) -> None:
        super().__init__(parent, 250)
        self._color = color
        self.body.addWidget(QLabel(title, objectName="nbPopupTitle"))
        self.name = QLineEdit(name)
        self.name.setObjectName("nbInput")
        self.name.setPlaceholderText("Folder name, e.g. Fever DDx")
        self.name.setMaxLength(40)
        self.name.returnPressed.connect(self._accept)
        self.body.addWidget(self.name)

        dots = QHBoxLayout()
        dots.setSpacing(6)
        self._dots: dict[str, QFrame] = {}
        for option in FOLDER_COLORS:
            dot = QFrame()
            dot.setObjectName("nbColorDot")
            dot.setProperty("color", option)
            dot.setFixedSize(18, 18)
            dot.setCursor(Qt.CursorShape.PointingHandCursor)
            dot.setToolTip(option.capitalize())
            dot.mousePressEvent = lambda _e, c=option: self._pick(c)
            self._dots[option] = dot
            dots.addWidget(dot)
        dots.addStretch(1)
        self.body.addLayout(dots)

        done = QPushButton("Done")
        done.setObjectName("nbButton")
        done.setCursor(Qt.CursorShape.PointingHandCursor)
        done.clicked.connect(self._accept)
        self.body.addWidget(done, 0, Qt.AlignmentFlag.AlignRight)
        self._pick(color)
        self.name.setFocus()
        self.name.selectAll()

    def _pick(self, color: str) -> None:
        self._color = color
        for option, dot in self._dots.items():
            dot.setProperty("selected", "true" if option == color else "false")
            _repolish(dot)

    def _accept(self) -> None:
        self.accepted.emit(self.name.text(), self._color)
        self.close()


class AllTabsPopup(_Popup):
    """Every tab in the strip, grouped by folder, with a search box.

    This is how you get around once there are more tabs than fit."""

    chosen = Signal(str)

    def __init__(self, parent: QWidget, state: ColumnState, title: str) -> None:
        super().__init__(parent, 290)
        self._state = state
        self.body.addWidget(QLabel(title, objectName="nbPopupTitle"))
        self.search = QLineEdit()
        self.search.setObjectName("nbInput")
        self.search.setPlaceholderText("Find a tab...")
        self.search.textChanged.connect(self._fill)
        self.search.returnPressed.connect(self._choose_first)
        self.body.addWidget(self.search)

        self.tree = QTreeWidget()
        self.tree.setObjectName("nbTabList")
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(14)
        self.tree.setFixedHeight(280)
        self.tree.setIconSize(QSize(14, 14))
        self.tree.itemClicked.connect(self._clicked)
        self.body.addWidget(self.tree)
        self._fill("")
        self.search.setFocus()

    def _fill(self, text: str) -> None:
        words = text.lower().split()
        self.tree.clear()
        muted = _muted()

        def matches(tab: Tab) -> bool:
            return all(w in tab.title.lower() for w in words)

        loose = QTreeWidgetItem(["Not in a folder"])
        loose.setFlags(Qt.ItemFlag.ItemIsEnabled)
        for tab in self._state.tabs:
            if not tab.folder_id and matches(tab):
                loose.addChild(self._tab_item(tab, muted))
        for folder in self._state.folders:
            members = [t for t in self._state.members(folder.id) if matches(t)]
            if not members:
                continue
            node = QTreeWidgetItem([f"{folder.name}  ({len(members)})"])
            node.setIcon(0, dot_icon(folder.color))
            node.setFlags(Qt.ItemFlag.ItemIsEnabled)
            for tab in members:
                node.addChild(self._tab_item(tab, muted))
            self.tree.addTopLevelItem(node)
            node.setExpanded(folder.open or bool(words))
        if loose.childCount():
            self.tree.addTopLevelItem(loose)
            loose.setExpanded(True)
        if not self.tree.topLevelItemCount():
            empty = QTreeWidgetItem(["No tab matches that search."])
            empty.setFlags(Qt.ItemFlag.NoItemFlags)
            self.tree.addTopLevelItem(empty)

    def _tab_item(self, tab: Tab, tone: str) -> QTreeWidgetItem:
        item = QTreeWidgetItem([("● " if tab.id == self._state.active_id else "")
                                + tab.title])
        item.setIcon(0, lucide.icon(tab.icon, 14, tone))
        item.setData(0, Qt.ItemDataRole.UserRole, tab.id)
        return item

    def _clicked(self, item: QTreeWidgetItem, _column: int) -> None:
        tab_id = item.data(0, Qt.ItemDataRole.UserRole)
        if tab_id:
            self.chosen.emit(tab_id)
            self.close()

    def _choose_first(self) -> None:
        for i in range(self.tree.topLevelItemCount()):
            top = self.tree.topLevelItem(i)
            if top.childCount():
                self._clicked(top.child(0), 0)
                return


# ======================================================================
#   The strip
# ======================================================================

class _HorizontalScroll(QScrollArea):
    """No visible scrollbar; the mouse wheel scrolls sideways instead."""

    def wheelEvent(self, event) -> None:  # noqa: N802
        bar = self.horizontalScrollBar()
        delta = event.angleDelta().y() or event.angleDelta().x()
        bar.setValue(bar.value() - delta)
        event.accept()


class TabStrip(QFrame):
    tab_activated = Signal(str)
    tab_closed = Signal(str)
    new_tab_requested = Signal()
    collapse_requested = Signal()
    # (column, command, target id, argument)
    command = Signal(str, str, str, object)
    # (source column, tab id, target column, index, folder id)
    tab_dropped = Signal(str, str, str, int, str)

    def __init__(self, column: str, *, group: str = "ws", title: str = "Tabs",
                 allow_folders: bool = True, allow_duplicate: bool = True,
                 move_targets: Optional[list[tuple[str, str]]] = None,
                 collapse_icon: str = "", new_tooltip: str = "New tab",
                 object_name: str = "nbStrip") -> None:
        super().__init__()
        self.column = column
        self._group = group
        self._title = title
        self._allow_folders = allow_folders
        self._allow_duplicate = allow_duplicate
        self._move_targets = move_targets or []
        self._state = ColumnState()
        self.setObjectName(object_name)
        self.setFixedHeight(TAB_HEIGHT + 8)
        self.setAcceptDrops(True)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(6, 0, 6, 0)
        outer.setSpacing(4)

        self._scroll = _HorizontalScroll()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setAcceptDrops(False)
        self._row_host = QWidget()
        self._row_host.setObjectName("nbStripRow")
        self._row = QHBoxLayout(self._row_host)
        self._row.setContentsMargins(0, 8, 0, 0)
        self._row.setSpacing(3)
        self._row.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self._scroll.setWidget(self._row_host)
        outer.addWidget(self._scroll, 1)

        self._marker = QFrame(self._row_host)
        self._marker.setObjectName("nbDropMarker")
        self._marker.setFixedSize(2, TAB_HEIGHT - 6)
        self._marker.hide()

        self._buttons: list[QPushButton] = []
        self.new_button = _icon_button("plus", new_tooltip)
        self.new_button.clicked.connect(self.new_tab_requested.emit)
        self.list_button = _icon_button("list", "All tabs")
        self.list_button.clicked.connect(self._show_all_tabs)
        self._buttons += [self.new_button, self.list_button]
        outer.addWidget(self.new_button)
        outer.addWidget(self.list_button)
        if collapse_icon:
            self.collapse_button = _icon_button(collapse_icon, "Collapse column")
            self.collapse_button.clicked.connect(self.collapse_requested.emit)
            self._buttons.append(self.collapse_button)
            outer.addWidget(self.collapse_button)

    # ------------------------------------------------------------- drawing

    def show_state(self, state: ColumnState) -> None:
        self._state = state
        while self._row.count():
            item = self._row.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        shown_folder = ""
        active_widget: Optional[QWidget] = None
        for tab in state.tabs:
            if tab.folder_id and tab.folder_id != shown_folder:
                shown_folder = tab.folder_id
                folder = state.folder(tab.folder_id)
                if folder is not None:
                    chip = FolderChip(folder, len(state.members(folder.id)))
                    chip.clicked.connect(
                        lambda fid: self.command.emit(self.column, "toggle_folder", fid, None))
                    chip.context.connect(self._folder_menu)
                    self._row.addWidget(chip, 0, Qt.AlignmentFlag.AlignVCenter)
            if state.is_hidden(tab):
                continue
            folder = state.folder(tab.folder_id) if tab.folder_id else None
            button = TabButton(tab, tab.id == state.active_id, self._group, self.column,
                               folder.color if folder else "")
            button.clicked.connect(self.tab_activated.emit)
            button.close_clicked.connect(self.tab_closed.emit)
            button.context.connect(self._tab_menu)
            self._row.addWidget(button, 0, Qt.AlignmentFlag.AlignBottom)
            if tab.id == state.active_id:
                active_widget = button
        self._row.addStretch(1)
        self._marker.raise_()
        if active_widget is not None:
            QTimer.singleShot(0, lambda w=active_widget: self._reveal(w))

    def _reveal(self, widget: QWidget) -> None:
        try:
            self._scroll.ensureWidgetVisible(widget, 24, 0)
        except RuntimeError:
            pass        # redrawn again before this ran

    def refresh_theme(self) -> None:
        for button in self._buttons:
            button.setIcon(lucide.icon(button.property("lucide"), 15, _muted()))
        self.show_state(self._state)

    # --------------------------------------------------------------- menus

    def _menu(self) -> QMenu:
        menu = QMenu(self)
        menu.setObjectName("nbMenu")
        return menu

    def _submenu(self, parent: QMenu, title: str) -> QMenu:
        sub = parent.addMenu(title)
        sub.setObjectName("nbMenu")
        return sub

    def _tab_menu(self, tab_id: str, where: QPoint) -> None:
        tab = self._state.tab(tab_id)
        if tab is None:
            return
        emit = lambda name, arg=None: self.command.emit(self.column, name, tab_id, arg)  # noqa: E731
        menu = self._menu()
        if tab.pinned:
            menu.addAction("Unpin tab", lambda: emit("unpin"))
        else:
            menu.addAction("Pin tab", lambda: emit("pin"))
        if self._allow_duplicate:
            menu.addAction("Duplicate", lambda: emit("duplicate"))

        if self._allow_folders:
            menu.addSeparator()
            menu.addAction("Add to new folder...", lambda: self._new_folder(tab_id, where))
            others = [f for f in self._state.folders if f.id != tab.folder_id]
            if others:
                sub = self._submenu(menu, "Add to folder")
                for folder in others:
                    sub.addAction(dot_icon(folder.color), folder.name,
                                  lambda fid=folder.id: emit("add_to_folder", fid))
            if tab.folder_id:
                menu.addAction("Remove from folder", lambda: emit("remove_from_folder"))

        targets = [(c, t) for c, t in self._move_targets if c != self.column]
        if targets:
            menu.addSeparator()
            sub = self._submenu(menu, "Move to column")
            for column, title in targets:
                sub.addAction(title, lambda c=column: emit("move_to", c))

        menu.addSeparator()
        menu.addAction("Close other tabs", lambda: emit("close_others"))
        close = menu.addAction("Close tab", lambda: emit("close"))
        close.setEnabled(not tab.pinned)
        menu.exec(where)

    def _folder_menu(self, folder_id: str, where: QPoint) -> None:
        folder = self._state.folder(folder_id)
        if folder is None:
            return
        emit = lambda name, arg=None: self.command.emit(self.column, name, folder_id, arg)  # noqa: E731
        menu = self._menu()
        menu.addAction("Fold" if folder.open else "Unfold", lambda: emit("toggle_folder"))
        menu.addAction("Rename or recolour...", lambda: self._edit_folder(folder, where))
        menu.addSeparator()
        menu.addAction("Ungroup (keep the tabs)", lambda: emit("ungroup"))
        menu.addAction("Close folder and its tabs", lambda: emit("close_folder"))
        menu.exec(where)

    def _new_folder(self, tab_id: str, where: QPoint) -> None:
        editor = FolderEditor(self, "New folder", "", self._state.next_folder_color())
        editor.accepted.connect(
            lambda name, color: self.command.emit(self.column, "new_folder", tab_id,
                                                  (name, color)))
        editor.show_at(where)

    def _edit_folder(self, folder: TabFolder, where: QPoint) -> None:
        editor = FolderEditor(self, "Edit folder", folder.name, folder.color)
        editor.accepted.connect(
            lambda name, color: self.command.emit(self.column, "edit_folder", folder.id,
                                                  (name, color)))
        editor.show_at(where)

    def _show_all_tabs(self) -> None:
        popup = AllTabsPopup(self, self._state, f"All tabs · {self._title}")
        popup.chosen.connect(self.tab_activated.emit)
        corner = self.list_button.mapToGlobal(QPoint(0, self.list_button.height() + 4))
        popup.show_at(QPoint(corner.x() - 290 + self.list_button.width(), corner.y()))

    # --------------------------------------------------------- drag & drop

    def _accepts(self, event) -> Optional[tuple[str, str, str]]:
        source = decode(event.mimeData())
        return source if source is not None and source[0] == self._group else None

    def dragEnterEvent(self, event) -> None:  # noqa: N802
        if self._accepts(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event) -> None:  # noqa: N802
        if not self._accepts(event):
            event.ignore()
            return
        event.acceptProposedAction()
        _index, _folder, x = self._drop_target(event.position().toPoint())
        if x is None:
            self._marker.hide()
        else:
            self._marker.move(x, 8 + 3)
            self._marker.show()
            self._marker.raise_()

    def dragLeaveEvent(self, event) -> None:  # noqa: N802
        self._marker.hide()

    def dropEvent(self, event) -> None:  # noqa: N802
        self._marker.hide()
        source = self._accepts(event)
        if source is None:
            event.ignore()
            return
        event.acceptProposedAction()
        index, folder_id, _x = self._drop_target(event.position().toPoint())
        _group, column, tab_id = source
        # Queued: the tab being dragged is still inside its QDrag.exec().
        # Redrawing now would delete it mid-call, so apply after it returns.
        QTimer.singleShot(0, lambda: self.tab_dropped.emit(
            column, tab_id, self.column, index, folder_id))

    def _drop_target(self, pos: QPoint) -> tuple[int, str, Optional[int]]:
        """Where a drop at `pos` (strip coordinates) lands: the index in the
        state's tab list, the folder it joins, and where to draw the marker
        (None when dropping onto a folder label)."""
        row_pos = self._row_host.mapFrom(self, pos)
        widgets = [self._row.itemAt(i).widget() for i in range(self._row.count())]
        widgets = [w for w in widgets if w is not None]

        for widget in widgets:
            if isinstance(widget, FolderChip) and widget.geometry().contains(row_pos):
                members = self._state.members(widget.folder.id)
                last = self._state.index_of(members[-1].id) + 1 if members else 0
                return last, widget.folder.id, None

        tabs = [w for w in widgets if isinstance(w, TabButton)]
        for widget in tabs:
            rect: QRect = widget.geometry()
            if row_pos.x() < rect.center().x():
                folder = widget.tab.folder_id if rect.contains(row_pos) else ""
                return self._state.index_of(widget.tab.id), folder, rect.left() - 2
            if rect.contains(row_pos):
                return (self._state.index_of(widget.tab.id) + 1, widget.tab.folder_id,
                        rect.right() + 1)
        end = tabs[-1].geometry().right() + 2 if tabs else 0
        return len(self._state.tabs), "", end
