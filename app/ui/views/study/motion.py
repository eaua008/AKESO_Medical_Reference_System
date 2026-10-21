"""Study Hub's moving parts: a progress ring that fills, numbers that count
up, lists that fade in one after another, tiles that lift when pointed at,
a 7-day forecast and a mastery bar that grow into place.

Everything is short (under half a second) and drawn from the theme, so it
reads as feedback, not decoration.
"""

from typing import Iterable, Optional

from PySide6.QtCore import (
    Property, QEasingCurve, QObject, QPointF, QPropertyAnimation, QRectF, QTimer, QVariantAnimation, Qt,
)
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QLabel, QWidget

from app.core.theme import Theme

SUBJECT_COLOURS = {"anatomy": "#E05D5D", "pathology": "#8B7CF6", "pharmacology": "#2BB673",
                   "microbiology": "#E0A030"}
DEFAULT_COLOUR = "#7C8496"


def subject_colour(subject_id: str) -> str:
    return SUBJECT_COLOURS.get(subject_id or "", DEFAULT_COLOUR)


# ------------------------------------------------------------------ basics

def _has_effect_nearby(widget: QWidget) -> bool:
    """Whether the widget, a parent or a child already has a graphics effect
    (a hover shadow, another fade). Qt can't draw one effect inside another:
    it floods the console with "QPainter::begin: A paint device can only be
    painted by one painter at a time" and may draw nothing."""
    parent = widget
    while parent is not None:
        if parent.graphicsEffect() is not None:
            return True
        parent = parent.parentWidget()
    return any(child.graphicsEffect() is not None for child in widget.findChildren(QWidget))


def fade_in(widget: QWidget, delay_ms: int = 0, duration: int = 260) -> None:
    """Fade a widget in (after a delay); the effect is removed afterwards.
    Shown at once instead when an effect is already near it."""
    if _has_effect_nearby(widget):
        return
    effect = QGraphicsOpacityEffect(widget)
    effect.setOpacity(0.0)
    widget.setGraphicsEffect(effect)
    animation = QPropertyAnimation(effect, b"opacity", widget)
    animation.setDuration(duration)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def done() -> None:
        try:
            if widget.graphicsEffect() is effect:
                widget.setGraphicsEffect(None)
        except RuntimeError:
            pass
    animation.finished.connect(done)
    QTimer.singleShot(max(0, delay_ms), lambda: animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped))


def stagger(widgets: Iterable[QWidget], step_ms: int = 45, limit: int = 14) -> None:
    """Fade a list in, one after another (only the first few; the rest at once)."""
    for i, widget in enumerate(widgets):
        if i >= limit:
            break
        fade_in(widget, i * step_ms)


def count_up(label: QLabel, target: int, template: str = "{}", duration: int = 600) -> None:
    """Count a number up from 0 in a label."""
    animation = QVariantAnimation(label)
    animation.setStartValue(0)
    animation.setEndValue(max(0, int(target)))
    animation.setDuration(duration if target else 1)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.valueChanged.connect(lambda v: label.setText(template.format(int(v))))
    animation.start(QVariantAnimation.DeletionPolicy.DeleteWhenStopped)
    label.setText(template.format(0 if target else 0))


class HoverLift(QObject):
    """Give a widget a soft shadow that grows when the pointer is over it."""

    def __init__(self, widget: QWidget) -> None:
        super().__init__(widget)
        self._shadow = QGraphicsDropShadowEffect(widget)
        self._shadow.setOffset(QPointF(0, 2))
        self._shadow.setBlurRadius(0)
        colour = QColor(Theme.token("PRIMARY"))
        colour.setAlpha(70)
        self._shadow.setColor(colour)
        widget.setGraphicsEffect(self._shadow)
        self._blur = QPropertyAnimation(self._shadow, b"blurRadius", self)
        self._blur.setDuration(160)
        widget.installEventFilter(self)

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        kind = event.type()
        if kind == event.Type.Enter:
            self._go(22)
        elif kind == event.Type.Leave:
            self._go(0)
        return False

    def _go(self, value: float) -> None:
        self._blur.stop()
        self._blur.setStartValue(self._shadow.blurRadius())
        self._blur.setEndValue(value)
        self._blur.start()


# -------------------------------------------------------------- the ring

class ProgressRing(QWidget):
    """Today's progress: an arc that fills to `value` (0..1), a big number
    in the middle and a caption under it."""

    def __init__(self, size: int = 140) -> None:
        super().__init__()
        self.setFixedSize(size, size)
        self._value = 0.0
        self._text = ""
        self._caption = ""
        self._anim = QPropertyAnimation(self, b"value", self)
        self._anim.setDuration(900)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _get(self) -> float:
        return self._value

    def _set(self, value: float) -> None:
        self._value = max(0.0, min(1.0, float(value)))
        self.update()

    value = Property(float, _get, _set)

    def show_progress(self, fraction: float, text: str, caption: str) -> None:
        self._text, self._caption = text, caption
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(max(0.0, min(1.0, fraction)))
        self._anim.start()

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        side = min(self.width(), self.height())
        thick = max(6.0, side * 0.075)
        rect = QRectF(thick, thick, side - 2 * thick, side - 2 * thick)
        rect.moveCenter(QPointF(self.width() / 2, self.height() / 2))
        pen = QPen(QColor(Theme.token("BORDER")), thick)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        p.drawArc(rect, 0, 360 * 16)
        done = self._value >= 0.999
        pen.setColor(QColor(Theme.token("SUCCESS") if done else Theme.token("PRIMARY")))
        p.setPen(pen)
        if self._value > 0:
            p.drawArc(rect, 90 * 16, int(-360 * 16 * self._value))
        font = QFont(self.font())
        font.setPixelSize(max(14, int(side * 0.22)))
        font.setBold(True)
        p.setFont(font)
        p.setPen(QColor(Theme.token("TEXT")))
        upper = QRectF(0, side * 0.26, self.width(), side * 0.3)
        p.drawText(upper, Qt.AlignmentFlag.AlignCenter, self._text)
        font.setPixelSize(max(9, int(side * 0.085)))
        font.setBold(False)
        p.setFont(font)
        p.setPen(QColor(Theme.token("TEXT_MUTED")))
        lower = QRectF(0, side * 0.56, self.width(), side * 0.16)
        p.drawText(lower, Qt.AlignmentFlag.AlignCenter, self._caption)
        p.end()


# ---------------------------------------------------------- forecast bars

class ForecastBars(QWidget):
    """Cards due on each of the next 7 days; bars grow into place."""

    def __init__(self) -> None:
        super().__init__()
        self.setMinimumHeight(110)
        self._days: list[tuple[str, int]] = []
        self._grow = 0.0
        self._anim = QPropertyAnimation(self, b"grow", self)
        self._anim.setDuration(700)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _get(self) -> float:
        return self._grow

    def _set(self, value: float) -> None:
        self._grow = float(value)
        self.update()

    grow = Property(float, _get, _set)

    def set_days(self, days: list[tuple[str, int]]) -> None:
        self._days = days
        self.setToolTip("\n".join(f"{d}: {n} card{'s' if n != 1 else ''}" for d, n in days))
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def paintEvent(self, _event) -> None:  # noqa: N802
        if not self._days:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        count = len(self._days)
        gap = 10.0
        width = (self.width() - gap * (count - 1)) / count
        top, bottom = 18.0, self.height() - 20.0
        peak = max([n for _d, n in self._days] + [1])
        font = QFont(self.font())
        font.setPixelSize(10)
        p.setFont(font)
        for i, (day, n) in enumerate(self._days):
            x = i * (width + gap)
            height = (bottom - top) * (n / peak) * self._grow
            colour = QColor(Theme.token("PRIMARY"))
            if i > 0:
                colour.setAlpha(150)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(Theme.token("BORDER")))
            p.drawRoundedRect(QRectF(x, bottom - 3, width, 3), 1.5, 1.5)
            if height > 0:
                p.setBrush(colour)
                p.drawRoundedRect(QRectF(x, bottom - height, width, height), 4, 4)
            p.setPen(QColor(Theme.token("TEXT") if i == 0 else Theme.token("TEXT_MUTED")))
            p.drawText(QRectF(x - 4, bottom + 4, width + 8, 14), Qt.AlignmentFlag.AlignHCenter, day)
            if n:
                p.drawText(QRectF(x - 4, bottom - height - 16, width + 8, 14), Qt.AlignmentFlag.AlignHCenter, str(n))
        p.end()


# ------------------------------------------------------------- mastery bar

class MasteryBar(QWidget):
    """A deck's cards as one bar: learned (green), learning (accent), new (grey)."""

    def __init__(self, learned: int, learning: int, total: int, accent: str) -> None:
        super().__init__()
        self.setFixedHeight(6)
        self._learned, self._learning, self._total = learned, learning, max(1, total)
        self._accent = accent
        self._grow = 0.0
        self._anim = QPropertyAnimation(self, b"grow", self)
        self._anim.setDuration(650)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        QTimer.singleShot(60, self._anim.start)
        self.setToolTip(f"{learned} learned · {learning} in progress · "
                        f"{max(0, total - learned - learning)} new")

    def _get(self) -> float:
        return self._grow

    def _set(self, value: float) -> None:
        self._grow = float(value)
        self.update()

    grow = Property(float, _get, _set)

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(0, 0, self.width(), self.height())
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(Theme.token("BORDER")))
        p.drawRoundedRect(r, 3, 3)
        w = self.width() * self._grow
        learned = w * self._learned / self._total
        learning = w * self._learning / self._total
        if learned + learning > 0:
            p.setBrush(QColor(self._accent))
            p.drawRoundedRect(QRectF(0, 0, learned + learning, r.height()), 3, 3)
        if learned > 0:
            p.setBrush(QColor(Theme.token("SUCCESS")))
            p.drawRoundedRect(QRectF(0, 0, learned, r.height()), 3, 3)
        p.end()


def accent_strip(colour: str, parent: Optional[QWidget] = None, width: int = 4) -> QWidget:
    """A thin coloured edge for a tile (its subject's colour)."""
    strip = QWidget(parent)
    strip.setFixedWidth(width)
    strip.setStyleSheet(f"background-color: {colour}; border-radius: {width // 2}px;")
    return strip
