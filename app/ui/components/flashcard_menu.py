"""Right-click "Make a flashcard" on text in encyclopedia pages and notes.

One application-wide event filter, active only inside the pages registered
with watch(): a disease, symptom or medicine page, and the Study Notebook.

  * text on those pages becomes selectable (and copyable) when you point at
    it, except on rows you click to open something, which must keep their
    click;
  * right-clicking selected text (or a paragraph) offers Copy and "Make a
    flashcard", which opens the card editor with that text on the back and
    the page's entry linked;
  * in a note, the editor's usual menu gets "Make a flashcard" added.
"""

from typing import Callable, Optional

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QAction, QCursor, QGuiApplication
from PySide6.QtWidgets import QApplication, QLabel, QMenu, QPlainTextEdit, QTextEdit, QWidget

Entry = Callable[[], tuple[str, str]]          # -> (kind, entry id), or ("", "")


def _plain(label: QLabel) -> str:
    if label.textFormat() == Qt.TextFormat.PlainText:
        return label.text()
    from PySide6.QtGui import QTextDocument
    doc = QTextDocument()
    doc.setHtml(label.text())
    return doc.toPlainText()


class FlashcardMenu(QObject):
    def __init__(self, make: Callable[[str, str, str], None], parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._make = make                       # (text, kind, entry id)
        self._roots: list[tuple[QWidget, Entry]] = []
        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)

    def watch(self, root: QWidget, entry: Entry) -> None:
        self._roots.append((root, entry))

    def _root_of(self, widget) -> Optional[tuple[QWidget, Entry]]:
        node = widget
        hops = 0
        while node is not None and hops < 40:
            for root, entry in self._roots:
                if node is root:
                    return root, entry
            node = node.parent() if hasattr(node, "parent") else None
            hops += 1
        return None

    @staticmethod
    def _clickable_row(widget: QWidget) -> bool:
        node = widget
        while node is not None:
            if isinstance(node, QWidget) and node.cursor().shape() == Qt.CursorShape.PointingHandCursor:
                return True
            node = node.parentWidget() if isinstance(node, QWidget) else None
        return False

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        kind = event.type()
        if kind == QEvent.Type.Enter and isinstance(obj, QLabel):
            if self._roots and obj.wordWrap() and len(obj.text()) > 25 \
                    and not (obj.textInteractionFlags() & Qt.TextInteractionFlag.TextSelectableByMouse) \
                    and not obj.openExternalLinks() and self._root_of(obj) and not self._clickable_row(obj):
                obj.setTextInteractionFlags(obj.textInteractionFlags()
                                            | Qt.TextInteractionFlag.TextSelectableByMouse)
            return False
        if kind != QEvent.Type.ContextMenu or not self._roots:
            return False
        target = obj
        if isinstance(obj, QWidget) and isinstance(obj.parentWidget(), (QTextEdit, QPlainTextEdit)):
            target = obj.parentWidget()                      # the viewport of an editor
        if not isinstance(target, (QLabel, QTextEdit, QPlainTextEdit)):
            return False
        found = self._root_of(target)
        if found is None:
            return False
        _root, entry = found
        if isinstance(target, QLabel):
            text = target.selectedText() or _plain(target)
            menu = QMenu(target)
            if target.selectedText():
                copy = QAction("Copy", menu)
                copy.triggered.connect(lambda: QGuiApplication.clipboard().setText(target.selectedText()))
                menu.addAction(copy)
        else:
            text = target.textCursor().selectedText().replace(" ", "\n")
            menu = target.createStandardContextMenu()
            menu.addSeparator()
        text = (text or "").strip()
        if not text:
            return False
        make = QAction("Make a flashcard", menu)
        make.triggered.connect(lambda: self._make(text, *self._entry(entry)))
        menu.addAction(make)
        menu.exec(QCursor.pos())
        menu.deleteLater()
        return True

    @staticmethod
    def _entry(entry: Entry) -> tuple[str, str]:
        try:
            kind, entry_id = entry()
            return kind or "", entry_id or ""
        except Exception:  # noqa: BLE001
            return "", ""
