"""Pop-ups that slide in over the module, like the reference browser.

Every Akeso pop-up (account forms, Terms / Privacy, announcements, admin
editors, Clinical Exchange dialogs, checker dialogs) is still a QDialog, so
the code that opens one is unchanged: dialog.exec() waits for the answer,
accept() / reject() close it. Only the way it appears changes:

    +--------+------------------------------------------+
    | header (stays visible)                             |
    +--------+--+---------------------------------------+
    | side  [X] | Title                          (bar)   |
    | bar    |  |---------------------------------------|
    |        |  |      the form, centred, scrolls        |
    |        |  |---------------------------------------|
    |        |  |                    [Cancel] [Save]     |
    +--------+------------------------------------------+

    full      covers the module area (right of the sidebar, below the
              header) and slides in from the right, with the same red X tab
              as the browser sheet.
    compact   a short card across the top of that area that drops down,
              the rest of the area dimmed (quick yes / no questions). A
              click on the dimmed part counts as Cancel.

While one is open, a transparent layer over the rest of the window takes
the clicks, so the module behind cannot be changed half-way (what a modal
window did before). The window's own title strip stays usable.

The dialog is moved into the main window only while it is showing; when it
closes it goes back to the parent it was created with, exactly as before.
Where there is no main window to slide into (tests, a script), it shows as a
normal window.

    SheetDialog        the frame (bar, scrolling column, button footer)
    SheetPresenter     the sliding / covering, usable by any QDialog
"""

from typing import Callable, Optional

from PySide6.QtCore import (
    QEasingCurve, QEvent, QObject, QPoint, QPropertyAnimation, QRect, QSize, Qt, QTimer,
)
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from app.core import lucide
from app.core.theme import Theme

TAB_SIZE = 44            # the red close tab (same as PageSheet)
TAB_TOP = 14
FULL_COLUMN = 720        # plain-window width of a full sheet (no main window)
FULL_MAX = 1000          # widest the content gets in a full sheet
BAR_LEFT = 24            # the bar's left padding; content lines up with its title
SLIDE_MS = 240
# The close tab: the same red as the reference browser's (exchange_styles.py,
# #pageSheetClose), so every X in Akeso looks alike.
TAB_RED = "#D32F2F"
TAB_RED_HOVER = "#B71C1C"
TAB_RED_PRESSED = "#8E1414"
DIM = QColor(0, 0, 0, 140)
# "Paper" sheets (announcements) are a white page whatever the theme.
PAPER = "#FFFFFF"
PAPER_LINE = "#E5E7EB"
PAPER_GHOST = ("QPushButton { background: #FFFFFF; color: #111827; border: 1px solid #D1D5DB;"
               " border-radius: 8px; padding: 7px 14px; font-weight: 600; }"
               "QPushButton:hover { background: #F3F4F6; }"
               "QPushButton:disabled { color: #9CA3AF; }")
PAPER_SCROLLBAR = ("QScrollBar:vertical { background: #FFFFFF; width: 10px; margin: 0; }"
                   "QScrollBar::handle:vertical { background: #D1D5DB; border-radius: 5px;"
                   " min-height: 40px; }"
                   "QScrollBar::handle:vertical:hover { background: #9CA3AF; }"
                   "QScrollBar::add-line, QScrollBar::sub-line { height: 0; }"
                   "QScrollBar::add-page, QScrollBar::sub-page { background: none; }")

animations_enabled = True


# ------------------------------------------------------------- the pieces

class _Scrim(QWidget):
    """Takes every click outside the sheet; dims the module area for a
    compact card."""

    def __init__(self, host: QWidget, on_click: Optional[Callable[[], None]]) -> None:
        super().__init__(host)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setMouseTracking(True)
        self.dim_rect: Optional[QRect] = None
        self._on_click = on_click

    def paintEvent(self, _event) -> None:  # noqa: N802
        if self.dim_rect is not None:
            p = QPainter(self)
            p.fillRect(self.dim_rect, DIM)
            p.end()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        event.accept()
        if (self._on_click is not None and self.dim_rect is not None
                and self.dim_rect.contains(event.position().toPoint())):
            self._on_click()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        event.accept()

    def wheelEvent(self, event) -> None:  # noqa: N802
        event.accept()


class _CloseTab(QPushButton):
    """The red X, painted so it never depends on a stylesheet. Same colours
    and shape as the reference browser's tab: rounded on the left only, so
    it looks attached to the sheet."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFixedSize(TAB_SIZE, TAB_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Close (Esc)")
        self.setAccessibleName("Close")
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        colour = (TAB_RED_PRESSED if self.isDown() else
                  TAB_RED_HOVER if self.underMouse() else TAB_RED)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(colour))
        r, w, h = 4, self.width(), self.height()
        shape = QPainterPath()
        if getattr(self, "inside", False):
            shape.addRoundedRect(self.rect(), r, r)       # in the sheet's corner
        else:
            shape.moveTo(w, 0)
            shape.lineTo(r, 0)
            shape.quadTo(0, 0, 0, r)
            shape.lineTo(0, h - r)
            shape.quadTo(0, h, r, h)
            shape.lineTo(w, h)
            shape.closeSubpath()
        p.drawPath(shape)
        icon = lucide.pixmap("x", 22, "#FFFFFF")
        p.drawPixmap((self.width() - 22) // 2, (self.height() - 22) // 2, icon)
        p.end()

    def enterEvent(self, event) -> None:  # noqa: N802
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self.update()
        super().leaveEvent(event)


class _Band(QFrame):
    """The bar at the top and the footer: a surface with a hairline."""

    def __init__(self, line_at_bottom: bool) -> None:
        super().__init__()
        self._bottom = line_at_bottom
        self.paper = False
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(PAPER if self.paper else Theme.token("SURFACE")))
        p.setPen(QPen(QColor(PAPER_LINE if self.paper else Theme.token("BORDER")), 1))
        y = self.height() - 1 if self._bottom else 0
        p.drawLine(0, y, self.width(), y)
        p.end()


def sheet_area(widget: QWidget) -> Optional[tuple[QWidget, QRect, int]]:
    """(host, module area in host coordinates, top of the clickable layer)
    from the main window, or None when there is none to slide into."""
    if widget is None:
        return None
    top = widget.window()
    area = getattr(top, "sheet_area", None)
    if area is None or not top.isVisible():
        return None
    try:
        return area()
    except Exception:  # noqa: BLE001 - fall back to a normal window
        return None


# -------------------------------------------------------------- presenter

class SheetPresenter(QObject):
    """Shows a QDialog as a sheet over the main window's module area.

    chrome=True:  the dialog is a SheetDialog and fills the sheet itself.
    chrome=False: any other dialog, shown as a compact card at its own size.
    """

    def __init__(self, dialog: QDialog, compact: bool, chrome: bool = True) -> None:
        super().__init__(dialog)
        self._dialog = dialog
        self.compact = compact
        self._chrome = chrome
        self._host: Optional[QWidget] = None
        self._origin: Optional[QWidget] = None
        self._origin_flags = None
        self._scrim: Optional[_Scrim] = None
        self._tab: Optional[_CloseTab] = None
        self._slide: Optional[QPropertyAnimation] = None
        self._ghost: Optional[QLabel] = None
        self.active = False
        dialog.finished.connect(lambda _r: self._dismantle())

    # The dialog calls this from setVisible(True), before it shows.
    def prepare(self) -> bool:
        if self.active:
            return True
        found = sheet_area(self._dialog.parentWidget())
        if found is None:
            return False
        host, _area, _top = found
        dialog = self._dialog
        self._host = host
        self._origin = dialog.parentWidget()
        self._origin_flags = dialog.windowFlags()
        self.active = True

        self._scrim = _Scrim(host, dialog.reject if self.compact else None)
        dialog.setParent(host, Qt.WindowType.Widget)
        if self._chrome and not self.compact:
            self._tab = _CloseTab(host)
            self._tab.clicked.connect(lambda _c=False: dialog.reject())
        host.installEventFilter(self)
        self.layout()
        self._scrim.show()
        self._scrim.raise_()
        return True

    # Then this, once it is visible: slide it in and give it the focus.
    def shown(self) -> None:
        if not self.active:
            return
        dialog = self._dialog
        dialog.raise_()
        if self._tab is not None:
            self._tab.show()
            self._tab.raise_()
        final = dialog.pos()
        picture = dialog.grab() if animations_enabled else None
        if picture is not None and not picture.isNull():
            # What slides is a picture of the sheet, not the sheet: moving the
            # real form repaints every field on every frame, which is slow on
            # a big page (the reference browser's sheet does the same). The
            # real sheet waits out of sight and takes its place at the end.
            start = (QPoint(final.x(), final.y() - min(dialog.height(), 160)) if self.compact
                     else QPoint(self._host.width(), final.y()))
            ghost = QLabel(self._host)
            ghost.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            ghost.setPixmap(picture)
            ghost.setGeometry(QRect(start, dialog.size()))
            ghost.show()
            ghost.raise_()
            if self._tab is not None:
                self._tab.raise_()
            self._ghost = ghost
            dialog.move(self._host.width() + 50, final.y())       # out of sight
            self._slide = QPropertyAnimation(ghost, b"pos", self)
            self._slide.setDuration(SLIDE_MS)
            self._slide.setEasingCurve(QEasingCurve.Type.OutCubic)
            self._slide.setStartValue(start)
            self._slide.setEndValue(final)
            self._slide.valueChanged.connect(self._place_tab)
            self._slide.finished.connect(self._landed)
            self._place_tab(start)
            self._slide.start()
        QTimer.singleShot(0, self._focus)

    def _landed(self) -> None:
        """The picture has arrived: the real sheet takes its place."""
        self._drop_ghost()
        if self.active:
            self.layout()
            self._dialog.raise_()
            if self._tab is not None:
                self._tab.raise_()

    def _drop_ghost(self) -> None:
        if self._ghost is not None:
            self._ghost.hide()
            self._ghost.deleteLater()
            self._ghost = None

    def _focus(self) -> None:
        dialog = self._dialog
        if not dialog.isVisible():
            return
        target = dialog.focusWidget()
        if target is None or not dialog.isAncestorOf(target):
            dialog.setFocus(Qt.FocusReason.PopupFocusReason)
            dialog.focusNextChild()

    def layout(self) -> None:
        """Place the scrim, the sheet and the tab for the current window size."""
        found = sheet_area(self._host) if self._host is not None else None
        if found is None:
            return
        host, area, layer_top = found
        dialog = self._dialog
        self._scrim.setGeometry(0, layer_top, host.width(), host.height() - layer_top)
        if self._chrome:
            if self.compact:
                height = min(dialog.compact_height(area.width()), area.height())
                rect = QRect(area.x(), area.y(), area.width(), height)
            else:
                rect = QRect(area)
        else:
            size = dialog.sizeHint().expandedTo(dialog.minimumSizeHint())
            width = min(max(size.width(), dialog.minimumWidth()), area.width())
            height = min(dialog.heightForWidth(width) if dialog.hasHeightForWidth()
                         else size.height(), area.height())
            rect = QRect(area.x() + (area.width() - width) // 2, area.y() + 24, width, height)
        dialog.setGeometry(rect)
        if self.compact or not self._chrome:
            dim = QRect(area)
            dim.translate(0, -layer_top)
            self._scrim.dim_rect = dim
            self._scrim.update()
        self._place_tab(rect.topLeft())

    def _place_tab(self, pos: QPoint) -> None:
        if self._tab is None:
            return
        found = sheet_area(self._host)
        inside = found is not None and found[1].x() < TAB_SIZE
        self._tab.inside = inside
        if inside:
            # No sidebar to overhang (the sign-in screen): the X sits in the
            # sheet's own corner instead.
            self._tab.move(pos.x() + self._dialog.width() - TAB_SIZE - 8, pos.y() + 6)
        else:
            self._tab.move(pos.x() - TAB_SIZE, pos.y() + TAB_TOP)
        self._tab.raise_()

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        if watched is self._host and event.type() == QEvent.Type.Resize and self.active:
            if self._slide is not None:
                self._slide.stop()
            self._drop_ghost()
            self.layout()
        return False

    def _dismantle(self) -> None:
        if not self.active:
            return
        self.active = False
        landing = self._ghost is not None        # closed while still sliding in
        if self._slide is not None:
            self._slide.stop()
            self._slide = None
        self._drop_ghost()
        if self._host is not None:
            self._host.removeEventFilter(self)
        dialog, origin, flags = self._dialog, self._origin, self._origin_flags
        scrim, tab = self._scrim, self._tab
        self._scrim = self._tab = None
        if landing or not self._slide_out(scrim, tab):
            for widget in (scrim, tab):
                if widget is not None:
                    widget.hide()
                    widget.deleteLater()

        def restore() -> None:
            # Back to where it came from, as a (hidden) window again, so it
            # can be shown a second time and is owned as before.
            try:
                if not dialog.isVisible():
                    dialog.setParent(origin, flags)
            except RuntimeError:
                pass                            # already deleted
        QTimer.singleShot(0, restore)


    def _slide_out(self, scrim: Optional[_Scrim], tab: Optional[_CloseTab]) -> bool:
        """Closing: a picture of the sheet slides back out (to the right, or
        up for a compact card) with its X, the way the reference browser
        closes. The dialog itself is already closed and its answer returned;
        only the picture moves. Everything here belongs to the main window,
        not to the dialog, so it finishes even if the dialog is deleted."""
        host, dialog = self._host, self._dialog
        if not animations_enabled or host is None or scrim is None:
            return False
        try:
            picture = dialog.grab()
            start = dialog.pos()
        except RuntimeError:
            return False
        if picture.isNull():
            return False
        ghost = QLabel(host)
        ghost.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        ghost.setPixmap(picture)
        ghost.setGeometry(QRect(start, picture.deviceIndependentSize().toSize()))
        ghost.show()
        ghost.raise_()
        scrim.dim_rect = None                 # the module comes back into view at once
        scrim.update()
        offset = None
        if tab is not None:
            tab.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            tab.raise_()
            offset = tab.pos() - start
        end = (QPoint(start.x(), start.y() - min(ghost.height(), 160)) if self.compact
               else QPoint(host.width(), start.y()))
        slide = QPropertyAnimation(ghost, b"pos", ghost)
        slide.setDuration(SLIDE_MS)
        slide.setEasingCurve(QEasingCurve.Type.InCubic)
        slide.setStartValue(start)
        slide.setEndValue(end)
        if tab is not None:
            slide.valueChanged.connect(lambda pos: tab.move(pos + offset))

        def done() -> None:
            for widget in (scrim, tab, ghost):
                try:
                    widget.hide()
                    widget.deleteLater()
                except (RuntimeError, AttributeError):
                    pass
        slide.finished.connect(done)
        slide.start()
        return True


# ------------------------------------------------------------------ frame

class SheetDialog(QDialog):
    """The sheet frame: title bar, a scrolling centred column, a footer.

        self.column   add the form here (a QVBoxLayout)
        self.footer   buttons, right-aligned (a QHBoxLayout, stretch first)
        self.bar_actions   extra buttons on the right of the title bar
    """

    compact = False            # subclasses for quick yes / no set True

    def __init__(self, parent: Optional[QWidget], title: str, subtitle: str = "",
                 icon: str = "", width: int = 560, danger: bool = False,
                 compact: Optional[bool] = None) -> None:
        super().__init__(parent)
        if compact is not None:
            self.compact = compact
        self.setWindowTitle(title)
        self.setModal(True)
        self.setObjectName("acSheet")
        self._column_width = max(width, 480) if self.compact else max(width, FULL_COLUMN)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._bar = _Band(line_at_bottom=True)
        bar = QHBoxLayout(self._bar)
        # Room on the right for the X when it sits inside (sign-in screen).
        bar.setContentsMargins(BAR_LEFT, 14, 24, 14)
        bar.setSpacing(12)
        self._icon_name, self._danger = icon, danger
        self._icon = QLabel()
        self._icon.setObjectName("panel")
        self._icon.setFixedSize(22, 22)
        if icon:
            bar.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignTop)
        titles = QVBoxLayout()
        titles.setSpacing(2)
        self.title_label = QLabel(title)
        self.title_label.setObjectName("acDangerTitle" if danger else "acCardTitle")
        self.title_label.setWordWrap(True)
        titles.addWidget(self.title_label)
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("acMuted")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setVisible(bool(subtitle))
        titles.addWidget(self.subtitle_label)
        bar.addLayout(titles, 1)
        self.bar_actions = QHBoxLayout()
        self.bar_actions.setSpacing(8)
        bar.addLayout(self.bar_actions)
        self._bar_layout = bar
        root.addWidget(self._bar)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        holder = QWidget()
        holder.setObjectName("panel")
        centre = QHBoxLayout(holder)
        centre.setContentsMargins(28, 22, 28, 22)
        self.content = QWidget()
        self.content.setObjectName("panel")
        self.column = QVBoxLayout(self.content)
        self.column.setContentsMargins(0, 0, 0, 0)
        self.column.setSpacing(12)
        if self.compact:
            # A short card: the text runs from the left edge, like the bar.
            centre.addWidget(self.content, 1)
        else:
            # A full sheet: the content starts on the left, lined up with the
            # title in the bar, and widens up to a comfortable reading width.
            centre.setContentsMargins(self._content_left(icon), 22, 28, 22)
            self.content.setMaximumWidth(FULL_MAX)
            centre.addWidget(self.content, 100)
            centre.addStretch(1)
        self._scroll.setWidget(holder)
        root.addWidget(self._scroll, 1)

        self._footer = _Band(line_at_bottom=False)
        foot = QHBoxLayout(self._footer)
        foot.setContentsMargins(24, 12, 24, 12)
        foot.setSpacing(8)
        foot.addStretch(1)
        self.footer = foot
        root.addWidget(self._footer)

        self.sheet = SheetPresenter(self, self.compact)
        self._paper = False
        self._holder = holder
        self.refresh_sheet_icon()

    @staticmethod
    def _content_left(icon: str) -> int:
        return BAR_LEFT + (22 + 12 if icon else 0)

    def make_paper(self) -> None:
        """A white page under the title bar (like a web page in the reference
        browser): the content and the footer on white. Labels on it need
        their own dark text colours."""
        self._paper = True
        self._footer.paper = True
        white = f"background-color: {PAPER};"
        self._scroll.setStyleSheet(f"QScrollArea {{ {white} border: none; }}" + PAPER_SCROLLBAR)
        self._scroll.viewport().setStyleSheet(white)
        self._holder.setStyleSheet(white)
        self.content.setStyleSheet(white)
        left = self._holder.layout().contentsMargins().left()
        self._holder.layout().setContentsMargins(left, 40, 40, 40)

    # ---------------------------------------------------------- showing

    def setVisible(self, visible: bool) -> None:  # noqa: N802
        if visible and not self.isVisible():
            self.sheet.prepare()
            if not self.sheet.active and not getattr(self, "_window_sized", False):
                # No main window: a normal dialog of a sensible size.
                self._window_sized = True
                self.resize(max(self._column_width + 56, 520),
                            min(max(self.compact_height(self._column_width + 56), 260), 720))
        super().setVisible(visible)
        if visible:
            self._footer.setVisible(self.footer.count() > 1)
            self.sheet.shown()

    def compact_height(self, width: int) -> int:
        """Height that fits everything (compact cards and plain windows)."""
        column = (max(width - 56, 200) if self.compact
                  else min(self._column_width, max(width - 56, 200)))
        content = (self.column.totalHeightForWidth(column) if self.column.hasHeightForWidth()
                   else self.column.totalSizeHint().height())
        bar_layout = self._bar_layout
        bar = (bar_layout.totalHeightForWidth(width) if bar_layout.hasHeightForWidth()
               else self._bar.sizeHint().height())
        footer = self._footer.sizeHint().height() if self.footer.count() > 1 else 0
        return bar + content + 44 + footer

    # ----------------------------------------------------------- frame

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(PAPER if self._paper else Theme.token("BG")))
        if self.sheet.active:
            p.setPen(QPen(QColor(Theme.token("BORDER")), 1))
            p.drawLine(0, 0, 0, self.height())
            if self.compact:
                p.drawLine(0, self.height() - 1, self.width(), self.height() - 1)
        p.end()

    def set_title(self, title: str, subtitle: Optional[str] = None) -> None:
        self.title_label.setText(title)
        self.setWindowTitle(title)
        if subtitle is not None:
            self.subtitle_label.setText(subtitle)
            self.subtitle_label.setVisible(bool(subtitle))

    def refresh_sheet_icon(self) -> None:
        if self._icon_name:
            colour = Theme.token("DANGER") if self._danger else Theme.token("BADGE_TEXT")
            self._icon.setPixmap(lucide.pixmap(self._icon_name, 22, colour))

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(self._column_width + 56, 480)
