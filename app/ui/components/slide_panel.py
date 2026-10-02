"""SlidePanel: a panel that slides in from the right over a page.

Reusable by any module. The Study Notebook uses it for its layers:

    closed   the page underneath is all you see
    half     the panel covers about half the page; the page is dimmed
             behind it so you keep your place
    full     the panel grows to cover the whole page

Only the panel's position and size change, with a QPropertyAnimation on
its geometry (about 220 ms, fast start and soft landing). The panel does
not own its content: the page puts whatever it wants inside `body`.

    settled(mode)    emitted when an animation has finished. Heavy content
                     should be swapped in here, not before, so the slide
                     itself stays smooth.
    closed()         the panel has finished sliding out.

Set SlidePanel.animations_enabled = False (a future setting) to make every
change instant, for users who prefer less motion.
"""

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QRect,
    Qt,
    Signal,
)
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QFrame, QGraphicsOpacityEffect, QVBoxLayout, QWidget

CLOSED, HALF, FULL = "closed", "half", "full"


class _Dim(QWidget):
    """The dark veil over the page. Clicking it closes the panel."""

    clicked = Signal()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))
        painter.end()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


class SlidePanel(QFrame):
    settled = Signal(str)
    closed = Signal()

    DURATION = 220
    animations_enabled = True

    def __init__(self, host: QWidget, half_ratio: float = 0.56, min_half: int = 640) -> None:
        super().__init__(host)
        self._host = host
        self._ratio = half_ratio
        self._min_half = min_half
        self.mode = CLOSED
        self._pending = CLOSED
        self.setObjectName("nbSlidePanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.hide()

        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(0)

        self._dim = _Dim(host)
        self._dim.hide()
        self._dim.clicked.connect(self.close_panel)
        self._fade = QGraphicsOpacityEffect(self._dim)
        self._dim.setGraphicsEffect(self._fade)

        self._slide = QPropertyAnimation(self, b"geometry", self)
        self._veil = QPropertyAnimation(self._fade, b"opacity", self)
        for animation in (self._slide, self._veil):
            animation.setDuration(self.DURATION)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._group = QParallelAnimationGroup(self)
        self._group.addAnimation(self._slide)
        self._group.addAnimation(self._veil)
        self._group.finished.connect(self._finished)

        host.installEventFilter(self)

    @property
    def target_mode(self) -> str:
        """Where the panel is heading (differs from `mode` mid-animation)."""
        return self._pending

    # ------------------------------------------------------------ geometry

    def _rect(self, mode: str) -> QRect:
        area = self._host.rect()
        if mode == FULL:
            return QRect(area)
        width = min(area.width(), max(self._min_half, int(area.width() * self._ratio)))
        if mode == HALF:
            return QRect(area.width() - width, 0, width, area.height())
        return QRect(area.width(), 0, width, area.height())      # just off-screen

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if watched is self._host and event.type() == QEvent.Type.Resize:
            self._dim.setGeometry(self._host.rect())
            if self.mode != CLOSED and self._group.state() != QParallelAnimationGroup.State.Running:
                self.setGeometry(self._rect(self.mode))
        return False

    # ----------------------------------------------------------- moving

    def open_half(self) -> None:
        if self.mode == HALF and self._pending == HALF:
            return
        start = self.geometry() if self.isVisible() else self._rect(CLOSED)
        self._go(HALF, start, fade_from=None if self._dim.isVisible() else 0.0)

    def expand(self) -> None:
        if self.mode == CLOSED:
            self.open_half()
        self._go(FULL, self.geometry())

    def shrink(self) -> None:
        self._go(HALF, self.geometry())

    def close_panel(self) -> None:
        if self.mode == CLOSED and not self.isVisible():
            return
        self._go(CLOSED, self.geometry(), fade_to=0.0)

    def _go(self, mode: str, start: QRect, fade_from=None, fade_to: float = 1.0) -> None:
        self._group.stop()
        self._pending = mode
        self._dim.setGeometry(self._host.rect())
        self._dim.show()
        self._dim.raise_()
        self.show()
        self.raise_()
        if fade_from is not None:
            self._fade.setOpacity(fade_from)
        if not self.animations_enabled:
            self.setGeometry(self._rect(mode))
            self._fade.setOpacity(fade_to)
            self._finished()
            return
        self._slide.setStartValue(start)
        self._slide.setEndValue(self._rect(mode))
        self._veil.setStartValue(self._fade.opacity())
        self._veil.setEndValue(fade_to)
        self._group.start()

    def _finished(self) -> None:
        self.mode = self._pending
        if self.mode == CLOSED:
            self.hide()
            self._dim.hide()
            self.closed.emit()
        self.settled.emit(self.mode)
