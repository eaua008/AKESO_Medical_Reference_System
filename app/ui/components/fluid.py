"""Keeps pages inside the window's width.

Why this exists: a QLabel that does not word-wrap refuses to be narrower
than its text. One long disease name in a top bar ("Acute Coronary Syndrome
(incl. Myocardial Infarction)") therefore raised the minimum width of the
whole page, the stacked widget holding it, and finally the main window,
which Qt then resized past the screen edge. Inside scroll areas the same
labels pushed the content wider than the viewport, so the right-hand cards
were cut off.

Three tools, used by the Disease, Symptom and Medicine pages:

    ElidedLabel     one line that shortens itself with "..." (full text in
                    the tooltip). For titles in fixed-height bars.
    contain(root)   after a page is built: long single-line labels wrap,
                    long button captions are shortened.
    ResponsiveGrid  card grid whose column count comes from the visible
                    viewport width, never from its own (possibly already
                    too wide) width, so it cannot feed back into itself.
"""

import weakref
from typing import Optional

from PySide6.QtCore import QEvent, QObject, QPoint, QSize, Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QWidget,
)

ELLIPSIS_MIN_CHARS = 8      # an elided title never shrinks below this many chars


class ElidedLabel(QLabel):
    """A single-line label that elides instead of forcing a minimum width."""

    def __init__(self, text: str = "", object_name: str = "",
                 parent: Optional[QWidget] = None, min_chars: int = ELLIPSIS_MIN_CHARS) -> None:
        super().__init__(parent)
        self._min_chars = min_chars
        if object_name:
            self.setObjectName(object_name)
        self._full = ""
        self.setWordWrap(False)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setText(text)

    # QLabel.text() would return the shortened text; callers want the real one.
    def text(self) -> str:  # noqa: D401
        return self._full

    def setText(self, text: str) -> None:  # noqa: N802 (Qt naming)
        self._full = text or ""
        self.setToolTip(self._full)
        self._refit()
        self.updateGeometry()

    def sizeHint(self) -> QSize:  # noqa: N802
        base = super().sizeHint()
        margins = self.contentsMargins()
        width = self.fontMetrics().horizontalAdvance(self._full) + margins.left() + margins.right() + 4
        return QSize(width, base.height())

    def minimumSizeHint(self) -> QSize:  # noqa: N802
        hint = self.sizeHint()
        floor = self.fontMetrics().horizontalAdvance("M" * self._min_chars)
        return QSize(min(hint.width(), floor), hint.height())

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._refit()

    def changeEvent(self, event) -> None:  # noqa: N802
        super().changeEvent(event)
        if event.type() in (QEvent.Type.FontChange, QEvent.Type.StyleChange):
            self._refit()
            self.updateGeometry()

    def _refit(self) -> None:
        available = max(self.contentsRect().width() - 2, 0)
        shown = self.fontMetrics().elidedText(self._full, Qt.TextElideMode.ElideRight, available)
        QLabel.setText(self, shown)


def elide_button(button: QPushButton, max_width: int) -> None:
    """Shorten a button caption to max_width pixels; full text in the tooltip."""
    full = button.property("fullText") or button.text()
    button.setProperty("fullText", full)
    metrics = button.fontMetrics()
    room = max_width - (button.sizeHint().width() - metrics.horizontalAdvance(button.text()))
    shown = metrics.elidedText(full, Qt.TextElideMode.ElideRight, max(room, 40))
    if shown != full:
        button.setText(shown)
        button.setToolTip(full)


def _layout_path(layout, widget) -> list:
    """Layouts from `layout` down to the one directly holding `widget`, each
    paired with the item (sub-layout or the widget) it holds on that path."""
    if layout is None:
        return []
    if layout.indexOf(widget) >= 0:
        return [(layout, widget)]
    for index in range(layout.count()):
        child = layout.itemAt(index).layout()
        if child is not None:
            below = _layout_path(child, widget)
            if below:
                return [(layout, child)] + below
    return []


def _claim_row_space(label: QLabel) -> None:
    """A wrapped QLabel asks for less width than its text needs (Qt makes
    wrapped labels compact on purpose), so in a row next to addStretch() it
    would break onto two lines, or three, even with plenty of room. Giving
    it (or the column it sits in) the row's stretch keeps it on one line
    until the row really is too narrow. Text stays left-aligned, so nothing
    moves visually."""
    parent = label.parentWidget()
    for layout, item in _layout_path(parent.layout() if parent is not None else None, label):
        if isinstance(layout, QHBoxLayout):
            layout.setStretchFactor(item, 100)


def contain(root: QWidget, limit: int = 300, buttons: bool = True) -> None:
    """Stop long single-line text inside root from widening the page.

    Labels wider than limit px wrap instead (they still show on one line
    whenever there is room). Buttons wider than limit are shortened.
    Badges, chips and numbers are short, so they are left alone.
    buttons=False leaves button captions untouched (tabs, main actions).
    """
    for label in root.findChildren(QLabel):
        if isinstance(label, ElidedLabel) or label.wordWrap():
            continue
        pixmap = label.pixmap()
        if pixmap is not None and not pixmap.isNull():
            continue
        if label.sizeHint().width() > limit:
            label.setWordWrap(True)
            _claim_row_space(label)
    if not buttons:
        return
    for button in root.findChildren(QPushButton):
        if button.text() and button.sizeHint().width() > limit:
            elide_button(button, limit)


class ResponsiveGrid(QWidget):
    """Cards in as many columns as the visible width allows.

    The column count is worked out from the scroll area's viewport, because
    the grid's own width is not trustworthy: if the cards were too wide it
    has already grown, and counting columns from that width made it grow
    further (the Symptom list reached 1,258 px wider than the screen).
    """

    # Settings > Display > "Cards per row" for the encyclopedia grids
    # (0 = as many as fit). Only grids that call follow_user_columns() obey it.
    user_columns = 0
    USER_MIN_CARD = 250             # how narrow a card may get when the user asks for more
    _followers: "weakref.WeakSet[ResponsiveGrid]" = weakref.WeakSet()

    @classmethod
    def set_user_columns(cls, columns: int) -> None:
        cls.user_columns = max(0, int(columns or 0))
        for grid in list(cls._followers):
            grid._apply_user_columns()

    def __init__(self, min_card_width: int, max_columns: int = 3, spacing: int = 16,
                 parent: Optional[QWidget] = None, steps: tuple[int, ...] = ()) -> None:
        super().__init__(parent)
        self._follows_user = False
        self._base_min_card = min_card_width
        self._base_max_columns = max_columns
        # Optional allowed column counts, e.g. (8, 4, 2): 8 parts reflow as
        # 4 + 4 or 2 x 4 rather than an uneven 6 + 2.
        self._steps = tuple(sorted(steps, reverse=True))
        self.setObjectName("panel")
        self._min_card = min_card_width
        self._max_columns = max_columns
        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setSpacing(spacing)
        self._grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._cards: list[QWidget] = []
        self._fixed_columns: Optional[int] = None
        self._columns = 0
        self._viewport: Optional[QWidget] = None
        # The widest card's minimum width, worked out once per set of cards.
        # Asking every card on every resize event made resizing the window
        # crawl on the Symptom and Medicine pages.
        self._need: Optional[int] = None
        self._measured_shown = False

    # ---------------------------------------------------------------- setup

    def viewport(self) -> Optional[QWidget]:
        return self._viewport

    def follow_user_columns(self) -> None:
        """Let Settings > Display > "Cards per row" decide the columns."""
        self._follows_user = True
        ResponsiveGrid._followers.add(self)
        self._apply_user_columns()

    def _apply_user_columns(self) -> None:
        wanted = ResponsiveGrid.user_columns
        if wanted:
            # Up to that many; fewer when the window is too narrow for them.
            self._max_columns = wanted
            self._min_card = min(self._base_min_card, self.USER_MIN_CARD)
        else:
            self._max_columns = self._base_max_columns
            self._min_card = self._base_min_card
        for card in self._cards:
            self._fit_card(card)
        self._need = None
        self._columns = 0
        self._relayout()

    def _fit_card(self, card: QWidget) -> None:
        """Cards fix their own minimum width; relax it while the user asks
        for more per row, and restore it on "Auto"."""
        if not self._follows_user:
            return
        base = card.property("akesoBaseMinWidth")
        if base is None:
            base = card.minimumWidth()
            card.setProperty("akesoBaseMinWidth", base)
        card.setMinimumWidth(min(base, self._min_card) if ResponsiveGrid.user_columns else base)

    def watch(self, viewport: QWidget) -> None:
        """Follow this scroll viewport's width (call once after building)."""
        self._viewport = viewport
        viewport.installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if watched is self._viewport and event.type() == QEvent.Type.Resize:
            self._relayout()
        return False

    # ------------------------------------------------------------------ api

    def set_cards(self, cards: list[QWidget], columns: Optional[int] = None) -> None:
        """Replace the cards. columns=None means "as many as fit"."""
        for card in self._cards:
            self._grid.removeWidget(card)
            card.hide()
            card.deleteLater()
        self._cards = list(cards)
        for card in self._cards:
            self._fit_card(card)
        self._fixed_columns = columns
        self._columns = 0
        self._need = None
        self._measured_shown = self.isVisible()
        self._relayout()

    def cards(self) -> list[QWidget]:
        return list(self._cards)

    # --------------------------------------------------------------- layout

    def available_width(self) -> int:
        if self._viewport is None:
            return self.width()
        if not self._viewport.isAncestorOf(self):
            # Not placed on the page yet; resizeEvent re-checks once it is.
            return self._viewport.width()
        # The grid sits inside page margins; assume they are symmetric.
        left = max(self.mapTo(self._viewport, QPoint(0, 0)).x(), 0)
        return max(self._viewport.width() - 2 * left, 0)

    def column_count(self) -> int:
        if self._fixed_columns:
            return self._fixed_columns
        spacing = self._grid.horizontalSpacing()
        # Trust the cards over the estimate: one unusually wide card (a long
        # body-system chip, say) means fewer columns, not an overflow.
        if self._need is None:
            self._need = max([self._min_card]
                             + [card.minimumSizeHint().width() for card in self._cards])
        fit = (self.available_width() + spacing) // (self._need + spacing)
        fit = max(1, min(self._max_columns, fit))
        if self._steps:
            fit = next((step for step in self._steps if step <= fit), 1)
        return fit

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._relayout()

    def changeEvent(self, event) -> None:  # noqa: N802
        # A new theme or font can change how wide the cards need to be.
        if event.type() in (QEvent.Type.StyleChange, QEvent.Type.FontChange):
            self._need = None
        super().changeEvent(event)

    def showEvent(self, event) -> None:  # noqa: N802
        # Cards measured while the page was still hidden (never styled) are
        # measured again the first time they are seen.
        if not self._measured_shown:
            self._measured_shown = True
            self._need = None
        super().showEvent(event)
        self._relayout()

    def _relayout(self) -> None:
        columns = self.column_count()
        if columns == self._columns:
            return
        self._columns = columns
        for card in self._cards:
            self._grid.removeWidget(card)
        for index, card in enumerate(self._cards):
            row, column = divmod(index, columns)
            self._grid.addWidget(card, row, column)
            card.show()
        for column in range(max(self._max_columns, columns, 8)):
            self._grid.setColumnStretch(column, 1 if column < columns else 0)


def fit_width(scroll) -> None:
    """Make a fixed-width scroll area's content exactly as wide as its viewport.

    For the narrow left rails: whatever is inside is squeezed to the rail
    instead of sliding out past its right edge, where it was being cut off
    ("Textbook Referenc...", the progress "92%").
    """
    widget = scroll.widget()
    if widget is not None:
        widget.setMinimumWidth(1)


class TitlePair(QWidget):
    """A page title and its subtitle on one line, for fixed-height top bars.

    The title keeps its full width first; the subtitle (scientific or
    generic name) gets whatever is left and shortens with "..." (or
    disappears) before the title does. Hover either for the full text.
    """

    GAP = 10

    def __init__(self, title_object: str, subtitle_object: str,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self.title = ElidedLabel("", title_object, self, min_chars=6)
        self.subtitle = ElidedLabel("", subtitle_object, self, min_chars=0)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    def set_texts(self, title: str, subtitle: str) -> None:
        self.title.setText(title)
        self.subtitle.setText(subtitle)
        self.subtitle.setVisible(bool(subtitle))
        self.updateGeometry()
        self._place()

    def sizeHint(self) -> QSize:  # noqa: N802
        title = self.title.sizeHint()
        width = title.width()
        if self.subtitle.text():
            width += self.GAP + self.subtitle.sizeHint().width()
        return QSize(width, max(title.height(), self.subtitle.sizeHint().height()))

    def minimumSizeHint(self) -> QSize:  # noqa: N802
        return QSize(self.title.minimumSizeHint().width(), self.sizeHint().height())

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._place()

    def _place(self) -> None:
        width, height = self.width(), self.height()
        title_width = min(self.title.sizeHint().width(), width)
        title_height = self.title.sizeHint().height()
        self.title.setGeometry(0, (height - title_height) // 2, title_width, title_height)
        rest = width - title_width - self.GAP
        sub_height = self.subtitle.sizeHint().height()
        # Baseline-ish: the subtitle is smaller, so centre it on the title.
        self.subtitle.setGeometry(title_width + self.GAP, (height - sub_height) // 2,
                                  max(rest, 0), sub_height)
        self.subtitle.setVisible(bool(self.subtitle.text()) and rest > 24)


class HScrollArea(QScrollArea):
    """Scrolls left-right only, and never traps the mouse wheel.

    A plain wheel turn scrolls the PAGE as usual (passed to the parent);
    Shift + wheel, a sideways trackpad swipe, or dragging the bar underneath
    scrolls the table sideways.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def wheelEvent(self, event) -> None:  # noqa: N802
        delta = event.angleDelta()
        bar = self.horizontalScrollBar()
        sideways = delta.x() != 0 or bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        if sideways and bar.maximum() > 0:
            step = delta.x() or delta.y()
            bar.setValue(bar.value() - step)
            event.accept()
        else:
            event.ignore()          # let the page scroll vertically

    def fit_height(self) -> None:
        """Exactly as tall as the table plus room for the scrollbar."""
        widget = self.widget()
        if widget is not None:
            extra = self.horizontalScrollBar().sizeHint().height() + 4
            self.setFixedHeight(widget.sizeHint().height() + extra)
