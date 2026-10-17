"""Ctrl+F on any screen: a find bar for the page you are looking at.

    Ctrl+F   open (selects what you typed last time)
    Enter / Down arrow / F3             next match
    Shift+Enter / Up arrow / Shift+F3   previous match
    Esc      close

What it searches: the visible text of the current screen, or of the
full-page sheet on top of it (a post, a disease, a group). Labels and
paragraphs show every match in yellow and the current one in orange, in
the text itself; text boxes and readers (notes, shared notes) do the same. Pages
inside the built-in browser (reference pages, the 3D explorer's page) use
the browser's own find when they have the focus.

Only text that is on screen and already built is searched (a collapsed
panel or a tab you haven't opened is not).
"""

import html
import re
from typing import Optional

import shiboken6
from PySide6.QtCore import QEvent, QObject, QPointF, Qt, QTimer
from PySide6.QtGui import QColor, QKeySequence, QPainter, QPen, QShortcut, QTextCursor, QTextDocument
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QScrollArea, QTextEdit,
    QWidget,
)

from app.core.theme import Theme

MAX_MATCHES = 2000
_TEXT_BOXES = (QTextEdit, QPlainTextEdit)        # QTextBrowser is a QTextEdit


def _plain(text: str) -> str:
    """A label's text as it reads (rich-text tags removed)."""
    if "<" in text and ">" in text:
        doc = QTextDocument()
        doc.setHtml(text)
        return doc.toPlainText()
    return text


def _highlight(text: str, query: str, background: str, foreground: str) -> str:
    """The label's text as rich text with every match marked. Works on plain
    text and on text that is already HTML (only the words are touched, never
    the tags)."""
    def wrap(match) -> str:
        return (f"<span style='background-color:{background}; color:{foreground};'>"
                f"{match.group(0)}</span>")

    def mark(chunk: str, word: str) -> str:
        return re.sub(re.escape(word), wrap, chunk, flags=re.IGNORECASE)

    if "<" in text and ">" in text and Qt.mightBeRichText(text):
        parts = re.split(r"(<[^>]*>)", text)
        return "".join(part if part.startswith("<") and part.endswith(">") else mark(part, query)
                       for part in parts)
    escaped = html.escape(text, quote=False)
    return mark(escaped, html.escape(query, quote=False)).replace(chr(10), "<br>")


class _Hit:
    """One match: a whole label, or one occurrence inside a text box."""

    def __init__(self, widget: QWidget, start: int = -1, length: int = 0) -> None:
        self.widget, self.start, self.length = widget, start, length

    @property
    def alive(self) -> bool:
        return shiboken6.isValid(self.widget) and self.widget.isVisible()


class _GlyphButton(QPushButton):
    """A small button that draws its own arrow or cross, in the theme's text
    colour. (The arrows used to be font or icon images and went missing; lines
    drawn here always show.)"""

    def __init__(self, glyph: str) -> None:
        super().__init__()
        self.glyph = glyph                       # up | down | close

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.underMouse() and self.isEnabled():
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(Theme.token("PRIMARY_SOFT")))
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)
        colour = QColor(Theme.token("TEXT"))
        pen = QPen(colour, 2.0)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        cx, cy = self.width() / 2, self.height() / 2
        if self.glyph == "up":
            painter.drawPolyline([QPointF(cx - 5, cy + 2.5), QPointF(cx, cy - 2.5), QPointF(cx + 5, cy + 2.5)])
        elif self.glyph == "down":
            painter.drawPolyline([QPointF(cx - 5, cy - 2.5), QPointF(cx, cy + 2.5), QPointF(cx + 5, cy - 2.5)])
        else:
            painter.drawLine(QPointF(cx - 4.5, cy - 4.5), QPointF(cx + 4.5, cy + 4.5))
            painter.drawLine(QPointF(cx - 4.5, cy + 4.5), QPointF(cx + 4.5, cy - 4.5))
        painter.end()


class FindBar(QFrame):
    def __init__(self, shell: QWidget) -> None:
        super().__init__(shell)
        self.setObjectName("findBar")
        self._shell = shell
        self._hits: list[_Hit] = []
        self._index = -1
        self._scope: Optional[QWidget] = None
        self._saved: dict = {}                   # widget -> what it had before we marked it
        self._current: Optional[_Hit] = None
        self._came_from: Optional[QWidget] = None
        self._web = None

        row = QHBoxLayout(self)
        row.setContentsMargins(10, 6, 6, 6)
        row.setSpacing(6)
        self.input = QLineEdit()
        self.input.setObjectName("findInput")
        self.input.setPlaceholderText("Find on this page")
        self.input.setClearButtonEnabled(True)
        self.input.setFixedWidth(230)
        self.input.textChanged.connect(lambda _t: self._timer.start())
        self.input.installEventFilter(self)
        row.addWidget(self.input)
        self.count = QLabel("")
        self.count.setObjectName("findCount")
        self.count.setMinimumWidth(62)
        row.addWidget(self.count)
        self.prev = self._button("up", "Previous match (Up arrow, Shift+Enter)", lambda: self.step(-1))
        self.next = self._button("down", "Next match (Down arrow, Enter)", lambda: self.step(1))
        self.close_button = self._button("close", "Close (Esc)", self.close_bar)
        for button in (self.prev, self.next, self.close_button):
            row.addWidget(button)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(150)
        self._timer.timeout.connect(self.search)

        self.hide()
        shell.installEventFilter(self)           # keep it in the corner on resize
        QShortcut(QKeySequence("F3"), self, activated=lambda: self.step(1))
        QShortcut(QKeySequence("Shift+F3"), self, activated=lambda: self.step(-1))
        self.refresh_theme()

    @staticmethod
    def _button(glyph: str, tip: str, on_click) -> QPushButton:
        button = _GlyphButton(glyph)
        button.setObjectName("findButton")
        button.setFixedSize(26, 26)
        button.setToolTip(tip)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda _c=False: on_click())
        return button

    # --------------------------------------------------------------- open

    def open(self) -> None:
        if QApplication.activeModalWidget() is not None:
            return                                  # a dialog is open: leave it alone
        focus = self.window().focusWidget() if self.window() else None
        if focus is not None and focus is not self.input and not self.isAncestorOf(focus):
            self._came_from = focus
        self.refresh_theme()
        self._place()
        self.show()
        self.raise_()
        self.input.setFocus()
        self.input.selectAll()
        if self.input.text():
            self.search()

    def close_bar(self) -> None:
        self._clear_marks()
        if self._web is not None:
            self._web.findText("")
            self._web = None
        self.hide()
        back = self._came_from
        if back is not None and shiboken6.isValid(back) and back.isVisible():
            back.setFocus()

    def _place(self) -> None:
        shell = self._shell
        self.adjustSize()
        top = getattr(getattr(shell, "header", None), "height", lambda: 56)() + 8
        self.move(max(8, shell.width() - self.width() - 24), top)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if watched is self._shell and event.type() == QEvent.Type.Resize and self.isVisible():
            self._place()
        if watched is self.input and event.type() == QEvent.Type.KeyPress:
            key, shift = event.key(), bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
            if key == Qt.Key.Key_Escape:
                self.close_bar()
                return True
            if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.step(-1 if shift else 1)
                return True
            if key == Qt.Key.Key_Down:               # arrow keys step through the matches
                self.step(1)
                return True
            if key == Qt.Key.Key_Up:
                self.step(-1)
                return True
        return super().eventFilter(watched, event)

    # ------------------------------------------------------------- scope

    def _scope_root(self) -> Optional[QWidget]:
        """The full-page sheet on top, else the current screen."""
        shell = self._shell
        sheets = [s for _tab, s in getattr(shell, "_sheets", []) if s.isVisible() and s.is_open]
        if sheets:
            return max(sheets, key=lambda s: getattr(s, "opened_at", 0))
        content = getattr(shell, "content", None)
        return content.currentWidget() if content is not None else None

    @staticmethod
    def _sort_key(widget: QWidget, root: QWidget) -> tuple:
        """Reading order that doesn't change while scrolling: by the scroll
        area it sits in (left to right, top to bottom), then its place in
        that area's content."""
        area = None
        parent = widget.parentWidget()
        while parent is not None and parent is not root:
            if isinstance(parent, QScrollArea):
                area = parent
            parent = parent.parentWidget()
        if area is None or area.widget() is None:
            pos = widget.mapTo(root, widget.rect().topLeft())
            return (0, 0, pos.y(), pos.x())
        outer = area.mapTo(root, area.rect().topLeft())
        inner = widget.mapTo(area.widget(), widget.rect().topLeft())
        return (outer.x() // 40, outer.y(), inner.y(), inner.x())

    # ------------------------------------------------------------ search

    def search(self) -> None:
        self._clear_marks()
        self._hits, self._index = [], -1
        query = self.input.text().strip()
        self._scope = self._scope_root()
        if self._web_find(query):
            return
        if not query or self._scope is None:
            self._show_count()
            return
        needle = query.lower()
        found: list[tuple[tuple, _Hit]] = []
        for widget in self._scope.findChildren(QWidget):
            if len(found) >= MAX_MATCHES:
                break
            if not widget.isVisible() or self.isAncestorOf(widget) or widget is self:
                continue
            if isinstance(widget, _TEXT_BOXES):
                found.extend(self._text_box_hits(widget, query))
            elif isinstance(widget, QLabel) and widget.text():
                if needle in _plain(widget.text()).lower():
                    found.append((self._sort_key(widget, self._scope), _Hit(widget)))
        found.sort(key=lambda item: (item[0], item[1].start))
        self._hits = [hit for _key, hit in found]
        if self._hits:
            self._paint_all()
            self.step(1)
        else:
            self._show_count()

    def _text_box_hits(self, box, query: str) -> list[tuple[tuple, _Hit]]:
        out = []
        doc = box.document()
        cursor = doc.find(query, 0)
        key = self._sort_key(box, self._scope)
        while not cursor.isNull() and len(out) < MAX_MATCHES:
            out.append(((key[0], key[1], key[2], key[3]), _Hit(box, cursor.selectionStart(),
                                                              cursor.selectionEnd() - cursor.selectionStart())))
            cursor = doc.find(query, cursor)
        return out

    def _web_find(self, query: str) -> bool:
        """The built-in browser has the focus: use its own find."""
        try:
            from PySide6.QtWebEngineWidgets import QWebEngineView
        except ImportError:
            return False
        focus = self._came_from
        view = None
        parent = focus
        while parent is not None:
            if isinstance(parent, QWebEngineView):
                view = parent
                break
            parent = parent.parentWidget()
        if view is None:
            if self._web is not None:
                self._web.findText("")
                self._web = None
            return False
        self._web = view

        def done(result) -> None:
            if shiboken6.isValid(self.count):
                total = result.numberOfMatches()
                self.count.setText(f"{result.activeMatchOrdinal()} / {total}" if total else
                                   ("No matches" if query else ""))
        self._web_run(view, query, done)
        return True

    @staticmethod
    def _web_run(view, query, done) -> None:
        page = view.page()
        try:                                       # Qt 6.8+: results arrive on a signal
            page.findTextFinished.disconnect()
        except (RuntimeError, TypeError):
            pass
        page.findTextFinished.connect(done)
        page.findText(query)

    # -------------------------------------------------------------- step

    def step(self, direction: int) -> None:
        if self._web is not None and shiboken6.isValid(self._web):
            from PySide6.QtWebEngineCore import QWebEnginePage
            flags = QWebEnginePage.FindFlag.FindBackward if direction < 0 else QWebEnginePage.FindFlag(0)
            self._web.page().findText(self.input.text().strip(), flags)
            return
        if self._hits and not all(h.alive for h in self._hits):
            self.search()                           # the screen changed under us
            return
        if not self._hits:
            if self.input.text().strip():
                self.search()
            return
        self._index = (self._index + direction) % len(self._hits)
        self._go(self._hits[self._index])
        self._show_count()

    def _show_count(self) -> None:
        if not self.input.text().strip():
            self.count.setText("")
        elif not self._hits:
            self.count.setText("No matches")
        else:
            capped = "+" if len(self._hits) >= MAX_MATCHES else ""
            self.count.setText(f"{self._index + 1} / {len(self._hits)}{capped}")

    # ----------------------------------------------------------- showing

    def _go(self, hit: _Hit) -> None:
        """Make hit the current match: it turns orange, the rest stay yellow."""
        previous = self._current
        self._current = hit
        if previous is not None and previous.alive:
            self._paint(previous.widget)
        self._paint(hit.widget)
        widget = hit.widget
        if isinstance(widget, _TEXT_BOXES):
            cursor = QTextCursor(widget.document())
            cursor.setPosition(hit.start)
            cursor.setPosition(hit.start + hit.length, QTextCursor.MoveMode.KeepAnchor)
            widget.setTextCursor(cursor)
            widget.ensureCursorVisible()
        self._scroll_to(widget)

    # Colours that read on every theme: every match yellow with dark text, the
    # current one orange (a frame or a faint tint wasn't easy enough to see).
    ALL_BG, CURRENT_BG, MATCH_FG = "#FACC15", "#FB923C", "#111111"

    def _paint_all(self) -> None:
        for hit in self._hits:
            self._paint(hit.widget)

    def _paint(self, widget: QWidget) -> None:
        """(Re)draw the highlights of one widget for the current query."""
        query = self.input.text().strip()
        current = self._current is not None and self._current.widget is widget
        if isinstance(widget, _TEXT_BOXES):
            if widget not in self._saved:
                self._saved[widget] = widget.extraSelections()
            selections = list(self._saved[widget])
            for hit in self._hits:
                if hit.widget is not widget:
                    continue
                cursor = QTextCursor(widget.document())
                cursor.setPosition(hit.start)
                cursor.setPosition(hit.start + hit.length, QTextCursor.MoveMode.KeepAnchor)
                extra = QTextEdit.ExtraSelection()
                extra.cursor = cursor
                is_now = current and hit is self._current
                extra.format.setBackground(QColor(self.CURRENT_BG if is_now else self.ALL_BG))
                extra.format.setForeground(QColor(self.MATCH_FG))
                selections.append(extra)
            widget.setExtraSelections(selections)
        elif isinstance(widget, QLabel):
            if widget not in self._saved:
                self._saved[widget] = (widget.text(), widget.textFormat())
            original = self._saved[widget][0]
            widget.setTextFormat(Qt.TextFormat.RichText)
            widget.setText(_highlight(original, query,
                                      self.CURRENT_BG if current else self.ALL_BG, self.MATCH_FG))

    @staticmethod
    def _scroll_to(widget: QWidget) -> None:
        """Bring the match into view, near the middle of the screen (not
        jammed against an edge, where it hides behind the find bar)."""
        parent = widget.parentWidget()
        first = True
        while parent is not None:
            if isinstance(parent, QScrollArea) and parent.widget() is not None:
                if first:
                    centre = widget.mapTo(parent.widget(), widget.rect().center()).y()
                    bar = parent.verticalScrollBar()
                    bar.setValue(max(0, centre - parent.viewport().height() // 2))
                    first = False
                parent.ensureWidgetVisible(widget, 40, 90)
            parent = parent.parentWidget()

    def _clear_marks(self) -> None:
        for widget, saved in self._saved.items():
            if not shiboken6.isValid(widget):
                continue
            if isinstance(widget, _TEXT_BOXES):
                widget.setExtraSelections(saved)
            else:
                text, fmt = saved
                widget.setTextFormat(fmt)
                widget.setText(text)
        self._saved = {}
        self._current = None

    def tab_changed(self) -> None:
        """The user moved to another screen: search that one."""
        if self.isVisible():
            self._timer.start()

    def refresh_theme(self) -> None:
        p = Theme
        self.setStyleSheet(f"""
            #findBar {{
                background-color: {p.token('SURFACE_RAISED')};
                border: 1px solid {p.token('BORDER')};
                border-radius: 10px;
            }}
            #findInput {{
                background-color: {p.token('SURFACE_ALT')};
                border: 1px solid {p.token('BORDER')};
                border-radius: 7px;
                padding: 4px 8px;
                color: {p.token('TEXT')};
            }}
            #findInput:focus {{ border-color: {p.token('PRIMARY')}; }}
            #findCount {{ color: {p.token('TEXT_MUTED')}; font-size: 12px; }}
            #findButton {{
                background: transparent;
                border: none;
                border-radius: 6px;
                color: {p.token('TEXT_MUTED')};
                font-size: 11px;
            }}
        """)
        for button in self.findChildren(_GlyphButton):      # redraw in the new colours
            button.update()


def install(shell: QWidget) -> FindBar:
    """Ctrl+F for a window; call once with the dashboard shell."""
    bar = FindBar(shell)
    shortcut = QShortcut(QKeySequence(QKeySequence.StandardKey.Find), shell)
    shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
    shortcut.activated.connect(bar.open)
    bar._shortcut = shortcut
    return bar
