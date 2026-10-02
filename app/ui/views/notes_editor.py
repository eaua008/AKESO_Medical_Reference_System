"""Step 5: the Word-like notes editor for the centre column.

    [undo][redo] | Normal ▾ | 11 ▾ | B I U S | A̲ 🖍 | ≡ ≡ ≡ | • 1. ☑ | ⇥ ⇤ | ▦ ― 🖼 </> ⌫
    [+ row above][+ row below][+ col left][+ col right] | [− row][− col] | [merge][split] [delete table]
    ┌───────────────────────── paper ──────────────────────────┐
    │  free rich text: headings, lists, checklists, tables,    │
    │  highlights, images, "Source:" links from the reference   │
    └──────────────────────────────────────────────────────────┘
    412 words                                   Saved · 2:41 PM

Built on QTextEdit / QTextDocument, which already understand rich text,
lists and tables. The editor does not own the document: the controller
keeps one QTextDocument per note, so the same note open in two tabs is the
same text, and saving happens in one place.

What QTextEdit cannot do (so neither can this): page layout, margins,
page breaks, track changes.
"""

import shutil
import uuid
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QPoint, QRect, QSize, Qt, QUrl, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QImage,
    QPainter,
    QTextBlockFormat,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
    QTextFormat,
    QTextFrameFormat,
    QTextImageFormat,
    QTextLength,
    QTextListFormat,
    QTextTableFormat,
)
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.interaction_styles import tone_color
from app.ui.components.tab_strip import Popup
from app.ui.views.interaction_widgets import FlowLayout

MONO = ["Consolas", "Cascadia Mono", "Courier New", "monospace"]
CODE_FLAG = QTextFormat.Property.UserProperty + 1
QUOTE_FLAG = QTextFormat.Property.UserProperty + 2
TABLE_BORDER = "#6B7280"          # readable on dark and light paper
SOURCE_COLOR = "#8B7CF6"

STYLES = (("normal", "Normal text"), ("h1", "Heading 1"), ("h2", "Heading 2"),
          ("h3", "Heading 3"), ("quote", "Quote"))
HEADING_PT = {"h1": 18.0, "h2": 15.0, "h3": 13.0}
SIZES = ("8", "9", "10", "11", "12", "14", "16", "18", "20", "24", "28")

TEXT_COLORS = (("Default", None), ("Red", "#EF4444"), ("Orange", "#F97316"),
               ("Amber", "#EAB308"), ("Green", "#22C55E"), ("Blue", "#3B82F6"),
               ("Purple", "#8B5CF6"), ("Grey", "#9CA3AF"))
HIGHLIGHTS = (("None", None), ("Yellow", "#FACC15"), ("Green", "#22C55E"),
              ("Pink", "#EC4899"), ("Blue", "#3B82F6"), ("Purple", "#8B5CF6"))


def images_dir() -> Path:
    from app.repositories.local_disease_cache import default_cache_path
    folder = default_cache_path().with_name("akeso_notebook_images")
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def new_document(parent=None, html: str = "") -> QTextDocument:
    doc = QTextDocument(parent)
    doc.setDocumentMargin(26)
    if html:
        doc.setHtml(html)
    return doc


# ======================================================================
#   Small popups
# ======================================================================

class ColorPopup(Popup):
    chosen = Signal(object)          # a hex string, or None for "clear"

    def __init__(self, parent: QWidget, title: str, options, translucent: bool) -> None:
        super().__init__(parent, 200)
        self.body.addWidget(QLabel(title, objectName="nbPopupTitle"))
        grid = QWidget()
        grid.setObjectName("panel")
        flow = FlowLayout(grid, spacing=6)
        for name, hexc in options:
            swatch = QPushButton()
            swatch.setObjectName("nbSwatch")
            swatch.setFixedSize(26, 26)
            swatch.setToolTip(name)
            swatch.setCursor(Qt.CursorShape.PointingHandCursor)
            if hexc:
                colour = QColor(hexc)
                if translucent:
                    colour.setAlpha(90)
                swatch.setStyleSheet(f"background-color: rgba({colour.red()}, {colour.green()}, "
                                     f"{colour.blue()}, {colour.alpha()});")
            else:
                swatch.setIcon(lucide.icon("x", 13, tone_color("muted")))
            swatch.clicked.connect(lambda _c=False, h=hexc: self._pick(h))
            flow.addWidget(swatch)
        self.body.addWidget(grid)

    def _pick(self, hexc) -> None:
        self.chosen.emit(hexc)
        self.close()


class TablePicker(Popup):
    """Hover a grid to choose rows × columns, like Word's Insert Table."""

    chosen = Signal(int, int)
    ROWS, COLS, CELL = 8, 8, 20

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, self.COLS * self.CELL + 26)
        self._hover = (3, 3)
        self.label = QLabel("3 × 3 table", objectName="nbPopupTitle")
        self.body.addWidget(self.label)
        self.grid = QWidget()
        self.grid.setObjectName("panel")
        self.grid.setFixedSize(self.COLS * self.CELL, self.ROWS * self.CELL)
        self.grid.setMouseTracking(True)
        self.grid.paintEvent = self._paint
        self.grid.mouseMoveEvent = self._move
        self.grid.mousePressEvent = self._press
        self.body.addWidget(self.grid)

    def _cell(self, pos: QPoint) -> tuple[int, int]:
        return (max(1, min(self.ROWS, pos.y() // self.CELL + 1)),
                max(1, min(self.COLS, pos.x() // self.CELL + 1)))

    def _move(self, event) -> None:
        self._hover = self._cell(event.position().toPoint())
        self.label.setText(f"{self._hover[0]} × {self._hover[1]} table")
        self.grid.update()

    def _press(self, event) -> None:
        rows, cols = self._cell(event.position().toPoint())
        self.chosen.emit(rows, cols)
        self.close()

    def _paint(self, _event) -> None:
        painter = QPainter(self.grid)
        on, off, line = QColor(tone_color("primary")), QColor(0, 0, 0, 0), QColor(TABLE_BORDER)
        on.setAlpha(110)
        for r in range(self.ROWS):
            for c in range(self.COLS):
                rect = QRect(c * self.CELL + 1, r * self.CELL + 1, self.CELL - 3, self.CELL - 3)
                painter.fillRect(rect, on if r < self._hover[0] and c < self._hover[1] else off)
                painter.setPen(line)
                painter.drawRect(rect)
        painter.end()


# ======================================================================
#   The text area
# ======================================================================

class NoteTextEdit(QTextEdit):
    link_clicked = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("nbEditor")
        self.setAcceptRichText(True)
        self.setTabChangesFocus(False)
        self.viewport().setMouseTracking(True)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        # Clicking a checklist box ticks it.
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            block = self.cursorForPosition(pos).block()
            fmt = block.blockFormat()
            if block.textList() is not None and fmt.marker() != QTextBlockFormat.MarkerType.NoMarker:
                start = self.cursorRect(QTextCursor(block))
                if pos.x() < start.left() and abs(pos.y() - start.center().y()) < start.height():
                    fmt.setMarker(QTextBlockFormat.MarkerType.Checked
                                  if fmt.marker() == QTextBlockFormat.MarkerType.Unchecked
                                  else QTextBlockFormat.MarkerType.Unchecked)
                    QTextCursor(block).setBlockFormat(fmt)
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        anchor = self.anchorAt(event.position().toPoint())
        self.viewport().setCursor(Qt.CursorShape.PointingHandCursor if anchor.startswith("akeso://")
                                  else Qt.CursorShape.IBeamCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and not self.textCursor().hasSelection():
            anchor = self.anchorAt(event.position().toPoint())
            if anchor.startswith("akeso://"):
                self.link_clicked.emit(anchor)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        cursor = self.textCursor()
        block = cursor.block()
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and block.textList() is not None:
            if not block.text().strip():
                # Enter on an empty list item ends the list, like Word.
                block.textList().remove(block)
                fmt = cursor.blockFormat()
                fmt.setIndent(0)
                fmt.setMarker(QTextBlockFormat.MarkerType.NoMarker)
                cursor.setBlockFormat(fmt)
                return
            super().keyPressEvent(event)
            # A new checklist item starts unticked.
            fmt = self.textCursor().blockFormat()
            if fmt.marker() == QTextBlockFormat.MarkerType.Checked:
                fmt.setMarker(QTextBlockFormat.MarkerType.Unchecked)
                self.textCursor().setBlockFormat(fmt)
            return
        super().keyPressEvent(event)


# ======================================================================
#   The editor
# ======================================================================

class NotesEditor(QWidget):
    link_clicked = Signal(str)

    def __init__(self, document: QTextDocument) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._buttons: dict[str, QPushButton] = {}
        self._icons: list[tuple[QPushButton, str]] = []

        col = QVBoxLayout(self)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(0)
        col.addWidget(self._build_toolbar())
        self.table_bar = self._build_table_bar()
        col.addWidget(self.table_bar)

        paper = QFrame()
        paper.setObjectName("nbPaperHost")
        paper_col = QVBoxLayout(paper)
        paper_col.setContentsMargins(14, 12, 14, 8)
        self.text = NoteTextEdit()
        self.text.setDocument(document)
        self.text.link_clicked.connect(self.link_clicked.emit)
        self.text.currentCharFormatChanged.connect(lambda _f: self._sync())
        self.text.cursorPositionChanged.connect(self._sync)
        document.contentsChanged.connect(self._count)
        paper_col.addWidget(self.text, 1)
        col.addWidget(paper, 1)

        foot = QHBoxLayout()
        foot.setContentsMargins(16, 4, 16, 8)
        self.words = QLabel("", objectName="nbSmallMuted")
        foot.addWidget(self.words)
        foot.addStretch(1)
        self.saved = QLabel("", objectName="nbSmallMuted")
        foot.addWidget(self.saved)
        col.addLayout(foot)

        self.refresh_icons()
        self._count()
        self._sync()

    # ------------------------------------------------------------ building

    def _tool(self, key: str, icon: str, tip: str, action: Callable,
              checkable: bool = False) -> QPushButton:
        button = QPushButton()
        button.setObjectName("nbToolButton")
        button.setFixedSize(28, 28)
        button.setCheckable(checkable)
        button.setToolTip(tip)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)      # keep the text's selection
        button.clicked.connect(lambda _c=False: action())
        self._buttons[key] = button
        self._icons.append((button, icon))
        return button

    @staticmethod
    def _gap() -> QFrame:
        line = QFrame()
        line.setObjectName("nbToolGap")
        line.setFixedSize(1, 20)
        return line

    def _build_toolbar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("nbToolbar")
        flow = FlowLayout(bar, spacing=3)
        bar.setContentsMargins(10, 6, 10, 6)
        t = self._tool
        for widget in (
            t("undo", "undo-2", "Undo (Ctrl+Z)", lambda: self.text.undo()),
            t("redo", "redo-2", "Redo (Ctrl+Y)", lambda: self.text.redo()),
            self._gap(),
        ):
            flow.addWidget(widget)

        self.style_box = QComboBox()
        self.style_box.setObjectName("nbToolCombo")
        for key, label in STYLES:
            self.style_box.addItem(label, key)
        self.style_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.style_box.activated.connect(lambda _i: self._apply_style(self.style_box.currentData()))
        flow.addWidget(self.style_box)
        self.size_box = QComboBox()
        self.size_box.setObjectName("nbToolCombo")
        self.size_box.addItems(SIZES)
        self.size_box.setToolTip("Font size (pt)")
        self.size_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.size_box.activated.connect(lambda _i: self._set_size(float(self.size_box.currentText())))
        flow.addWidget(self.size_box)
        flow.addWidget(self._gap())

        for widget in (
            t("bold", "bold", "Bold (Ctrl+B)", self._bold, True),
            t("italic", "italic", "Italic (Ctrl+I)", self._italic, True),
            t("underline", "underline", "Underline (Ctrl+U)", self._underline, True),
            t("strike", "strikethrough", "Strikethrough", self._strike, True),
            t("color", "baseline", "Text colour", self._pick_color),
            t("highlight", "highlighter", "Highlight", self._pick_highlight),
            self._gap(),
            t("left", "align-left", "Align left",
              lambda: self.text.setAlignment(Qt.AlignmentFlag.AlignLeft), True),
            t("center", "align-center", "Centre",
              lambda: self.text.setAlignment(Qt.AlignmentFlag.AlignHCenter), True),
            t("right", "align-right", "Align right",
              lambda: self.text.setAlignment(Qt.AlignmentFlag.AlignRight), True),
            self._gap(),
            t("bullets", "list", "Bulleted list",
              lambda: self._list(QTextListFormat.Style.ListDisc)),
            t("numbers", "list-ordered", "Numbered list",
              lambda: self._list(QTextListFormat.Style.ListDecimal)),
            t("checklist", "list-checks", "Checklist", self._checklist),
            t("indent", "indent-increase", "Indent", lambda: self._indent(1)),
            t("outdent", "indent-decrease", "Outdent", lambda: self._indent(-1)),
            self._gap(),
            t("table", "table", "Insert table", self._pick_table),
            t("rule", "minus", "Horizontal line", self._rule),
            t("image", "image", "Insert image", self._image),
            t("code", "code", "Code / lab values (monospace)", self._code),
            t("clear", "remove-formatting", "Clear formatting", self._clear_formatting),
        ):
            flow.addWidget(widget)
        return bar

    def _build_table_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("nbTableBar")
        flow = FlowLayout(bar, spacing=4)
        bar.setContentsMargins(10, 5, 10, 5)
        flow.addWidget(QLabel("Table:", objectName="nbSmallMuted"))
        for key, text in (("row_above", "+ Row above"), ("row_below", "+ Row below"),
                          ("col_left", "+ Col left"), ("col_right", "+ Col right"),
                          ("del_row", "− Row"), ("del_col", "− Col"),
                          ("merge", "Merge cells"), ("split", "Split cell"),
                          ("delete", "Delete table")):
            button = QPushButton(text)
            button.setObjectName("nbTableButton")
            button.setProperty("danger", "true" if key == "delete" else "false")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.clicked.connect(lambda _c=False, k=key: self._table_op(k))
            flow.addWidget(button)
        bar.hide()
        return bar

    # --------------------------------------------------------- formatting

    def _merge(self, fmt: QTextCharFormat) -> None:
        cursor = self.text.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.text.mergeCurrentCharFormat(fmt)
        self.text.setFocus()

    def _edit_fragments(self, change: Callable[[QTextCharFormat], None],
                        whole_blocks: bool = False) -> None:
        """Change each piece of the selection's formatting in place. Needed
        to REMOVE a property (a colour, a size), which merging cannot do."""
        cursor = self.text.textCursor()
        doc = self.text.document()
        if whole_blocks or not cursor.hasSelection():
            start = doc.findBlock(cursor.selectionStart()).position()
            last = doc.findBlock(cursor.selectionEnd())
            end = last.position() + last.length() - 1
        else:
            start, end = cursor.selectionStart(), cursor.selectionEnd()
        pieces = []
        block = doc.findBlock(start)
        while block.isValid() and block.position() <= end:
            it = block.begin()
            while not it.atEnd():
                fragment = it.fragment()
                it += 1
                f_start = fragment.position()
                f_end = f_start + fragment.length()
                lo, hi = max(f_start, start), min(f_end, end)
                if lo < hi:
                    pieces.append((lo, hi, QTextCharFormat(fragment.charFormat())))
            block = block.next()
        edit = QTextCursor(doc)
        edit.beginEditBlock()
        for s, e, fmt in pieces:
            change(fmt)
            edit.setPosition(s)
            edit.setPosition(e, QTextCursor.MoveMode.KeepAnchor)
            edit.setCharFormat(fmt)
        edit.endEditBlock()
        current = self.text.currentCharFormat()
        change(current)
        self.text.setCurrentCharFormat(current)
        self.text.setFocus()

    def _bold(self) -> None:
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if self._buttons["bold"].isChecked()
                          else QFont.Weight.Normal)
        self._merge(fmt)

    def _italic(self) -> None:
        fmt = QTextCharFormat()
        fmt.setFontItalic(self._buttons["italic"].isChecked())
        self._merge(fmt)

    def _underline(self) -> None:
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self._buttons["underline"].isChecked())
        self._merge(fmt)

    def _strike(self) -> None:
        fmt = QTextCharFormat()
        fmt.setFontStrikeOut(self._buttons["strike"].isChecked())
        self._merge(fmt)

    def _set_size(self, points: float) -> None:
        fmt = QTextCharFormat()
        fmt.setFontPointSize(points)
        self._merge(fmt)

    def _pick_color(self) -> None:
        popup = ColorPopup(self, "Text colour", TEXT_COLORS, translucent=False)
        popup.chosen.connect(self._set_color)
        popup.show_at(self._below("color"))

    def _set_color(self, hexc) -> None:
        if hexc is None:
            self._edit_fragments(lambda f: f.clearForeground())
        else:
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(hexc))
            self._merge(fmt)

    def _pick_highlight(self) -> None:
        popup = ColorPopup(self, "Highlight", HIGHLIGHTS, translucent=True)
        popup.chosen.connect(self._set_highlight)
        popup.show_at(self._below("highlight"))

    def _set_highlight(self, hexc) -> None:
        if hexc is None:
            self._edit_fragments(lambda f: f.clearBackground())
        else:
            colour = QColor(hexc)
            colour.setAlpha(90)
            fmt = QTextCharFormat()
            fmt.setBackground(colour)
            self._merge(fmt)

    def _below(self, key: str) -> QPoint:
        button = self._buttons[key]
        return button.mapToGlobal(QPoint(0, button.height() + 4))

    def _apply_style(self, style: str) -> None:
        cursor = self.text.textCursor()
        cursor.beginEditBlock()
        block_fmt = cursor.blockFormat()
        block_fmt.setHeadingLevel(int(style[1]) if style.startswith("h") else 0)
        if style == "quote":
            block_fmt.setLeftMargin(22)
            block_fmt.setProperty(QUOTE_FLAG, True)
        else:
            block_fmt.setLeftMargin(0)
            block_fmt.clearProperty(QUOTE_FLAG)
        cursor.setBlockFormat(block_fmt)
        cursor.endEditBlock()

        def change(fmt: QTextCharFormat) -> None:
            fmt.clearProperty(QTextFormat.Property.FontPointSize)
            fmt.setFontWeight(QFont.Weight.Normal)
            fmt.setFontItalic(False)
            if style in HEADING_PT:
                fmt.setFontPointSize(HEADING_PT[style])
                fmt.setFontWeight(QFont.Weight.Bold)
            elif style == "quote":
                fmt.setFontItalic(True)
        self._edit_fragments(change, whole_blocks=True)

    def _list(self, style: QTextListFormat.Style) -> None:
        cursor = self.text.textCursor()
        current = cursor.currentList()
        if current is not None and current.format().style() == style and \
                cursor.blockFormat().marker() == QTextBlockFormat.MarkerType.NoMarker:
            self._remove_list(cursor)
            return
        cursor.beginEditBlock()
        fmt = cursor.blockFormat()
        fmt.setMarker(QTextBlockFormat.MarkerType.NoMarker)
        cursor.setBlockFormat(fmt)
        cursor.createList(style)
        cursor.endEditBlock()

    def _checklist(self) -> None:
        cursor = self.text.textCursor()
        if cursor.currentList() is not None and \
                cursor.blockFormat().marker() != QTextBlockFormat.MarkerType.NoMarker:
            self._remove_list(cursor)
            return
        cursor.beginEditBlock()
        if cursor.currentList() is None:
            cursor.createList(QTextListFormat.Style.ListDisc)
        doc = self.text.document()
        block = doc.findBlock(cursor.selectionStart())
        end = cursor.selectionEnd()
        while block.isValid() and block.position() <= end:
            fmt = block.blockFormat()
            fmt.setMarker(QTextBlockFormat.MarkerType.Unchecked)
            QTextCursor(block).setBlockFormat(fmt)
            block = block.next()
        cursor.endEditBlock()

    @staticmethod
    def _remove_list(cursor: QTextCursor) -> None:
        cursor.beginEditBlock()
        doc = cursor.document()
        block = doc.findBlock(cursor.selectionStart())
        end = cursor.selectionEnd()
        while block.isValid() and block.position() <= end:
            if block.textList() is not None:
                block.textList().remove(block)
            fmt = block.blockFormat()
            fmt.setIndent(0)
            fmt.setMarker(QTextBlockFormat.MarkerType.NoMarker)
            QTextCursor(block).setBlockFormat(fmt)
            block = block.next()
        cursor.endEditBlock()

    def _indent(self, step: int) -> None:
        cursor = self.text.textCursor()
        current = cursor.currentList()
        if current is not None:
            fmt = QTextListFormat(current.format())
            fmt.setIndent(max(1, fmt.indent() + step))
            if step > 0:
                cursor.createList(fmt)          # a nested list for this item
            else:
                current.setFormat(fmt)
            return
        block = cursor.blockFormat()
        block.setIndent(max(0, block.indent() + step))
        cursor.setBlockFormat(block)

    def _rule(self) -> None:
        cursor = self.text.textCursor()
        cursor.insertHtml("<hr />")
        cursor.insertBlock()

    def _code(self) -> None:
        cursor = self.text.textCursor()
        is_code = bool(cursor.blockFormat().property(CODE_FLAG))
        cursor.beginEditBlock()
        doc = self.text.document()
        block = doc.findBlock(cursor.selectionStart())
        end = cursor.selectionEnd()
        while block.isValid() and block.position() <= end:
            fmt = block.blockFormat()
            if is_code:
                fmt.clearBackground()
                fmt.clearProperty(CODE_FLAG)
            else:
                shade = QColor(127, 127, 127, 38)
                fmt.setBackground(shade)
                fmt.setProperty(CODE_FLAG, True)
            QTextCursor(block).setBlockFormat(fmt)
            block = block.next()
        cursor.endEditBlock()

        def change(fmt: QTextCharFormat) -> None:
            if is_code:
                fmt.clearProperty(QTextFormat.Property.FontFamilies)
                fmt.clearProperty(QTextFormat.Property.FontFamily)
            else:
                fmt.setFontFamilies(MONO)
        self._edit_fragments(change, whole_blocks=True)

    def _clear_formatting(self) -> None:
        def change(fmt: QTextCharFormat) -> None:
            anchor = fmt.anchorHref()
            fmt.clearForeground()
            fmt.clearBackground()
            for prop in (QTextFormat.Property.FontWeight, QTextFormat.Property.FontItalic,
                         QTextFormat.Property.TextUnderlineStyle,
                         QTextFormat.Property.FontUnderline,
                         QTextFormat.Property.FontStrikeOut,
                         QTextFormat.Property.FontPointSize,
                         QTextFormat.Property.FontFamilies, QTextFormat.Property.FontFamily):
                fmt.clearProperty(prop)
            if anchor:
                fmt.setAnchorHref(anchor)     # keep links working
        self._edit_fragments(change)

    # --------------------------------------------------------------- tables

    def _pick_table(self) -> None:
        picker = TablePicker(self)
        picker.chosen.connect(self.insert_table)
        picker.show_at(self._below("table"))

    @staticmethod
    def _table_format() -> QTextTableFormat:
        fmt = QTextTableFormat()
        fmt.setCellPadding(6)
        fmt.setCellSpacing(0)
        fmt.setBorder(1)
        fmt.setBorderBrush(QBrush(QColor(TABLE_BORDER)))
        fmt.setBorderStyle(QTextFrameFormat.BorderStyle.BorderStyle_Solid)
        fmt.setBorderCollapse(True)
        fmt.setWidth(QTextLength(QTextLength.Type.PercentageLength, 100))
        fmt.setHeaderRowCount(1)
        return fmt

    def insert_table(self, rows: int, cols: int) -> None:
        cursor = self.text.textCursor()
        table = cursor.insertTable(rows, cols, self._table_format())
        bold = QTextCharFormat()
        bold.setFontWeight(QFont.Weight.Bold)
        for c in range(cols):
            table.cellAt(0, c).firstCursorPosition().setBlockCharFormat(bold)
        self.text.setTextCursor(table.cellAt(0, 0).firstCursorPosition())
        self.text.setFocus()

    def insert_table_data(self, caption: str, headers: list[str], rows: list[list[str]],
                          source: str = "") -> None:
        """Insert a filled table, e.g. the hallmark correlation of a case.
        It becomes an ordinary editable table in the notes."""
        cursor = self.text.textCursor()
        cursor.beginEditBlock()
        self._fresh_block(cursor)
        if source:
            self._insert_source(cursor, source[0], source[1])
        if caption:
            title = QTextCharFormat()
            title.setFontWeight(QFont.Weight.Bold)
            cursor.insertText(caption, title)
            cursor.insertBlock()
            cursor.setCharFormat(QTextCharFormat())
        table = cursor.insertTable(len(rows) + 1, len(headers), self._table_format())
        bold = QTextCharFormat()
        bold.setFontWeight(QFont.Weight.Bold)
        plain = QTextCharFormat()
        for c, text in enumerate(headers):
            table.cellAt(0, c).firstCursorPosition().insertText(text, bold)
        for r, row in enumerate(rows, start=1):
            for c, text in enumerate(row[:len(headers)]):
                table.cellAt(r, c).firstCursorPosition().insertText(str(text), plain)
        after = table.lastCursorPosition()
        after.movePosition(QTextCursor.MoveOperation.NextBlock)
        cursor.endEditBlock()
        self.text.setTextCursor(after)
        self.text.setFocus()

    def _table_op(self, op: str) -> None:
        cursor = self.text.textCursor()
        table = cursor.currentTable()
        if table is None:
            return
        cell = table.cellAt(cursor)
        r, c = cell.row(), cell.column()
        if op == "row_above":
            table.insertRows(r, 1)
        elif op == "row_below":
            table.insertRows(r + cell.rowSpan(), 1)
        elif op == "col_left":
            table.insertColumns(c, 1)
        elif op == "col_right":
            table.insertColumns(c + cell.columnSpan(), 1)
        elif op == "del_row":
            if table.rows() > 1:
                table.removeRows(r, 1)
            else:
                self._delete_table(table)
        elif op == "del_col":
            if table.columns() > 1:
                table.removeColumns(c, 1)
            else:
                self._delete_table(table)
        elif op == "merge":
            if cursor.hasSelection():
                table.mergeCells(cursor)
        elif op == "split":
            table.splitCell(r, c, 1, 1)
        elif op == "delete":
            self._delete_table(table)
        self._sync()
        self.text.setFocus()

    def _delete_table(self, table) -> None:
        cursor = QTextCursor(self.text.document())
        cursor.setPosition(table.firstPosition() - 1)
        cursor.setPosition(table.lastPosition() + 1, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()

    # --------------------------------------------------------------- images

    def _image(self) -> None:
        path, _filter = QFileDialog.getOpenFileName(
            self, "Insert image", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp *.webp)")
        if not path:
            return
        source = Path(path)
        # Copied next to the notebook, so the note still shows it if the
        # original file is moved. Images stay on this computer.
        target = images_dir() / f"{uuid.uuid4().hex}{source.suffix.lower()}"
        shutil.copyfile(source, target)
        image = QImage(str(target))
        fmt = QTextImageFormat()
        fmt.setName(QUrl.fromLocalFile(str(target)).toString())
        if not image.isNull():
            width = min(image.width(), 560)
            fmt.setWidth(width)
            fmt.setHeight(image.height() * width / max(1, image.width()))
        self.text.textCursor().insertImage(fmt)

    # ------------------------------------------------------ from reference

    @staticmethod
    def _fresh_block(cursor: QTextCursor) -> None:
        """Start inserted content on its own plain line: not inside a list,
        a checklist or a heading the cursor happened to be in."""
        if cursor.block().text().strip():
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
            cursor.insertBlock()
        if cursor.currentList() is not None:
            cursor.currentList().remove(cursor.block())
        cursor.setBlockFormat(QTextBlockFormat())
        cursor.setCharFormat(QTextCharFormat())

    @staticmethod
    def _insert_source(cursor: QTextCursor, label: str, href: str) -> None:
        link = QTextCharFormat()
        link.setAnchor(True)
        link.setAnchorHref(href)
        link.setForeground(QColor(SOURCE_COLOR))
        link.setFontWeight(QFont.Weight.DemiBold)
        link.setFontPointSize(9)
        cursor.insertText(f"Source: {label}  ↗", link)
        cursor.setCharFormat(QTextCharFormat())
        cursor.insertBlock()
        cursor.setCharFormat(QTextCharFormat())

    def insert_reference(self, label: str, href: str, html: str) -> None:
        """A section from the reference column, with a clickable
        "Source:" line above it pointing back to where it came from."""
        cursor = self.text.textCursor()
        cursor.beginEditBlock()
        self._fresh_block(cursor)
        self._insert_source(cursor, label, href)
        cursor.insertHtml(html)
        cursor.insertBlock()
        cursor.setBlockFormat(QTextBlockFormat())
        cursor.setCharFormat(QTextCharFormat())
        cursor.endEditBlock()
        self.text.setTextCursor(cursor)
        self.text.ensureCursorVisible()
        self.text.setFocus()

    def insert_html_block(self, html: str) -> None:
        """Insert ready-made content (e.g. the case summary) on its own lines."""
        cursor = self.text.textCursor()
        cursor.beginEditBlock()
        self._fresh_block(cursor)
        cursor.insertHtml(html)
        cursor.insertBlock()
        cursor.setBlockFormat(QTextBlockFormat())
        cursor.setCharFormat(QTextCharFormat())
        cursor.endEditBlock()
        self.text.setTextCursor(cursor)
        self.text.ensureCursorVisible()
        self.text.setFocus()

    # ---------------------------------------------------------------- state

    def _sync(self) -> None:
        """Make the toolbar reflect the formatting under the cursor."""
        fmt = self.text.currentCharFormat()
        cursor = self.text.textCursor()
        block = cursor.blockFormat()
        states = {
            "bold": fmt.fontWeight() >= QFont.Weight.DemiBold,
            "italic": fmt.fontItalic(),
            "underline": fmt.fontUnderline(),
            "strike": fmt.fontStrikeOut(),
            "left": bool(block.alignment() & Qt.AlignmentFlag.AlignLeft)
                    or not (block.alignment() & (Qt.AlignmentFlag.AlignHCenter
                                                 | Qt.AlignmentFlag.AlignRight)),
            "center": bool(block.alignment() & Qt.AlignmentFlag.AlignHCenter),
            "right": bool(block.alignment() & Qt.AlignmentFlag.AlignRight),
        }
        for key, on in states.items():
            self._buttons[key].blockSignals(True)
            self._buttons[key].setChecked(on)
            self._buttons[key].blockSignals(False)
        level = block.headingLevel()
        style = f"h{level}" if level in (1, 2, 3) else (
            "quote" if block.property(QUOTE_FLAG) else "normal")
        self.style_box.setCurrentIndex(max(0, self.style_box.findData(style)))
        size = fmt.fontPointSize() or self.text.document().defaultFont().pointSizeF()
        text = f"{size:g}" if size > 0 else "11"
        if self.size_box.findText(text) < 0:
            self.size_box.setEditText(text)
        self.size_box.setCurrentIndex(max(0, self.size_box.findText(text)))
        self.table_bar.setVisible(cursor.currentTable() is not None)

    def _count(self) -> None:
        words = len(self.text.document().toPlainText().split())
        self.words.setText(f"{words} word{'s' if words != 1 else ''}")

    def set_saved(self, text: str) -> None:
        self.saved.setText(text)

    def refresh_icons(self) -> None:
        for button, icon in self._icons:
            button.setIcon(lucide.icon(icon, 15, tone_color("text")))
            button.setIconSize(QSize(15, 15))

    def refresh_theme(self) -> None:
        self.refresh_icons()


class NotesPage(QWidget):
    """A centre-column tab showing one note."""

    def __init__(self, editor: NotesEditor, item_id: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.item_id = item_id
        self.editor = editor
        col = QVBoxLayout(self)
        col.setContentsMargins(0, 0, 0, 0)
        col.addWidget(editor)

    def refresh_theme(self) -> None:
        self.editor.refresh_theme()


class MissingPage(QWidget):
    """Shown when a tab points at something that no longer exists."""

    def __init__(self, text: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        col = QVBoxLayout(self)
        label = QLabel(text, objectName="nbEmpty")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col.addWidget(label)

