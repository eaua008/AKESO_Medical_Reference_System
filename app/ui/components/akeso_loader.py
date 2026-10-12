"""Akeso's loading animation: the logo builds itself, like Google's logo
animations.

One loop (about 2.8 s):

    1. outline   the logo's outline is drawn on, stroke by stroke, in a
                 blue-to-violet gradient
    2. fill      the full-color logo sweeps in from bottom-left to top-right
                 over the outline, growing slightly into place
    3. sparkle   the star in the middle of the A flashes and a shine passes
                 across the logo
    4. rest      it holds for a moment, fades, and builds again

    loader = AkesoLoader(72)        # size in px
    layout.addWidget(loader)        # show() starts it, hide() stops it

The outline comes from assets/loader_outline.json and the image from
assets/loader_mark.png (both made from DARKLOGO.png). Drawn with QPainter,
so it is sharp at any size and only runs while visible.
"""

import json
import math
from typing import Optional

from PySide6.QtCore import QElapsedTimer, QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QColor, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap, QRadialGradient,
)
from PySide6.QtWidgets import QLabel, QSizePolicy, QWidget

from app.core.paths import resource

LOOP_MS = 2800
FRAME_MS = 16                     # about 60 frames per second
STAR = (0.532, 0.603)             # the sparkle in the A, as a fraction of the mark
BLUE, VIOLET, SKY = "#3D6BE0", "#8B5CF6", "#38BDF8"

_outline: Optional[list] = None
_mark: Optional[QPixmap] = None


def _assets() -> tuple[list, Optional[QPixmap]]:
    global _outline, _mark
    if _outline is None:
        try:
            _outline = json.loads(resource("assets", "loader_outline.json").read_text("utf-8"))
        except (OSError, ValueError):
            _outline = []
        path = resource("assets", "loader_mark.png")
        _mark = QPixmap(str(path)) if path.exists() else None
    return _outline, _mark


def _smooth(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _window(p: float, start: float, end: float) -> float:
    """0 before start, 1 after end, eased in between."""
    return _smooth((p - start) / (end - start))


class AkesoLoader(QWidget):
    def __init__(self, diameter: int = 72, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedSize(diameter, diameter)
        self._d = self.width()          # the real size (80% / 90% shrink it)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAccessibleName("Loading")
        self._clock = QElapsedTimer()
        self._timer = QTimer(self)
        self._timer.setInterval(FRAME_MS)
        self._timer.timeout.connect(self.update)
        contours, _ = _assets()
        # Outline as polylines in widget pixels, with their lengths.
        self._lines = []
        for contour in contours:
            pts = [QPointF(x * self._d, y * self._d) for x, y in contour]
            if len(pts) < 2:
                continue
            pts.append(pts[0])                                   # closed
            seg = [math.dist((a.x(), a.y()), (b.x(), b.y())) for a, b in zip(pts, pts[1:])]
            self._lines.append((pts, seg, sum(seg)))
        self._total = sum(line[2] for line in self._lines) or 1.0

    # ------------------------------------------------------------ control

    def start(self) -> None:
        if not self._clock.isValid():
            self._clock.start()
        if not self._timer.isActive():
            self._timer.start()

    def stop(self) -> None:
        self._timer.stop()

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self.start()

    def hideEvent(self, event) -> None:  # noqa: N802
        self.stop()
        super().hideEvent(event)

    def _progress(self) -> float:
        ms = self._clock.elapsed() if self._clock.isValid() else 0
        return (ms % LOOP_MS) / LOOP_MS

    # ------------------------------------------------------------- frame

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = self._progress()
        d = self._d
        fade = 1.0 - _window(p, 0.90, 1.0)                       # end of loop
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(fade)

        # 1. outline drawn on
        drawn = _window(p, 0.0, 0.42)
        outline_alpha = 1.0 - _window(p, 0.58, 0.74)
        if drawn > 0 and outline_alpha > 0:
            self._draw_outline(painter, drawn * self._total, outline_alpha)

        # 2. full-color logo sweeping in
        fill = _window(p, 0.30, 0.66)
        if fill > 0:
            self._draw_fill(painter, fill, p)

        # 3. sparkle flash on the star
        flash = _window(p, 0.66, 0.73) * (1.0 - _window(p, 0.73, 0.84))
        if flash > 0:
            self._draw_sparkle(painter, flash)
        painter.end()

    def _draw_outline(self, painter: QPainter, length: float, alpha: float) -> None:
        d = self._d
        grad = QLinearGradient(0, d, d, 0)
        sky, violet = QColor(SKY), QColor(VIOLET)
        sky.setAlphaF(alpha)
        violet.setAlphaF(alpha)
        grad.setColorAt(0.0, violet)
        grad.setColorAt(1.0, sky)
        pen = QPen(grad, max(1.2, d * 0.018))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # All strokes are drawn at the same time, each proportionally, so
        # the whole shape appears together like a sketch.
        share = length / self._total
        for pts, seg, total in self._lines:
            left = total * share
            path = QPainterPath(pts[0])
            for a, b, s in zip(pts, pts[1:], seg):
                if left <= 0:
                    break
                if s <= left:
                    path.lineTo(b)
                else:
                    k = left / s
                    path.lineTo(a + (b - a) * k)
                left -= s
            painter.drawPath(path)

    def _draw_fill(self, painter: QPainter, fill: float, p: float) -> None:
        _, mark = _assets()
        if mark is None or mark.isNull():
            return
        d = self._d
        ratio = self.devicePixelRatioF()
        layer = QPixmap(int(d * ratio), int(d * ratio))
        layer.setDevicePixelRatio(ratio)
        layer.fill(Qt.GlobalColor.transparent)
        lp = QPainter(layer)
        lp.setRenderHint(QPainter.RenderHint.Antialiasing)
        lp.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        scale = 0.92 + 0.08 * fill                               # grows into place
        size = d * scale
        target = QRectF((d - size) / 2, (d - size) / 2, size, size)
        lp.drawPixmap(target, mark, QRectF(mark.rect()))

        # Shine: a soft white band passing across the finished logo.
        shine = _window(p, 0.70, 0.88)
        if 0 < shine < 1:
            lp.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceAtop)
            centre = -0.3 + 1.6 * shine
            band = QLinearGradient(0, d, d, 0)
            for at, a in ((centre - 0.12, 0.0), (centre, 0.35), (centre + 0.12, 0.0)):
                c = QColor(255, 255, 255)
                c.setAlphaF(a)
                band.setColorAt(max(0.0, min(1.0, at)), c)
            lp.fillRect(QRectF(0, 0, d, d), band)

        # Reveal: keep only the part the sweep has reached (soft edge).
        if fill < 1:
            lp.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
            edge = 0.18
            front = fill * (1 + edge)
            mask = QLinearGradient(0, d, d, 0)                    # bottom-left -> top-right
            mask.setColorAt(0.0, QColor(0, 0, 0, 255))
            mask.setColorAt(max(0.0, min(1.0, front - edge)), QColor(0, 0, 0, 255))
            mask.setColorAt(max(0.001, min(1.0, front)), QColor(0, 0, 0, 0))
            mask.setColorAt(1.0, QColor(0, 0, 0, 0))
            lp.fillRect(QRectF(0, 0, d, d), mask)
        lp.end()
        painter.drawPixmap(0, 0, layer)

    def _draw_sparkle(self, painter: QPainter, flash: float) -> None:
        d = self._d
        cx, cy = STAR[0] * d, STAR[1] * d
        r = d * 0.16 * flash
        glow = QRadialGradient(QPointF(cx, cy), r * 1.4)
        glow.setColorAt(0.0, QColor(255, 255, 255, int(200 * flash)))
        glow.setColorAt(0.4, QColor(192, 132, 252, int(110 * flash)))
        glow.setColorAt(1.0, QColor(192, 132, 252, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(glow)
        painter.drawEllipse(QPointF(cx, cy), r * 1.4, r * 1.4)
        # four-point star, like the one in the logo
        star = QPainterPath(QPointF(cx, cy - r))
        w = r * 0.22
        for tip, side in (((cx + r, cy), (cx + w, cy - w)), ((cx, cy + r), (cx + w, cy + w)),
                          ((cx - r, cy), (cx - w, cy + w)), ((cx, cy - r), (cx - w, cy - w))):
            star.quadTo(QPointF(*side), QPointF(*tip))
        painter.setBrush(QColor(255, 255, 255, int(235 * flash)))
        painter.drawPath(star)


class LoadingLabel(QLabel):
    """A label that can show the Akeso loader with its text.

        status = LoadingLabel("", "acMuted")          # use like any QLabel
        status.set_loading("Loading posts…")          # logo animation + text
        status.setText("No posts yet.")               # plain text again

    Any plain setText() ends the loading state, so existing code that later
    replaces the text (results, errors, "nothing found") needs no changes.
    inline=True puts a small loader to the left of the text (status rows);
    otherwise a larger one sits above the centered text (empty pages).
    """

    def __init__(self, text: str = "", object_name: str = "", size: int = 0,
                 inline: bool = False, wrap: bool = True) -> None:
        super().__init__(text)
        if object_name:
            self.setObjectName(object_name)
        self.setWordWrap(wrap)
        self._inline = inline
        self._size = size or (20 if inline else 64)
        self._gap = 8 if inline else 10
        self._loader = AkesoLoader(self._size, self)
        self._loader.hide()
        self._loading = False

    def set_loading(self, text: str) -> None:
        super().setText(text)
        self._loading = True
        if self._inline:
            self.setContentsMargins(self._size + self._gap, 0, 0, 0)
        else:
            self.setContentsMargins(0, self._size + self._gap, 0, 0)
            self.setMinimumHeight(self._size + self._gap + self.fontMetrics().height() * 2)
        self._place()
        self._loader.show()

    def is_loading(self) -> bool:
        return self._loading

    def setText(self, text: str) -> None:  # noqa: N802
        if self._loading:
            self._loading = False
            self._loader.hide()
            self.setContentsMargins(0, 0, 0, 0)
            self.setMinimumHeight(0)
        super().setText(text)

    def clear(self) -> None:
        self.setText("")

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._place()

    def _place(self) -> None:
        if self._inline:
            y = max(0, (self.height() - self._size) // 2)
            self._loader.move(0, y)
        else:
            self._loader.move(max(0, (self.width() - self._size) // 2), 0)


class LoaderOverlay(QWidget):
    """The Akeso loader (and optional text) laid over another widget, e.g.
    a web page or the 3D view while it loads. It follows the target's size.

        overlay = LoaderOverlay(self.view, "Loading the 3D body…", opaque=True)
        overlay.show_over()  /  overlay.hide()

    opaque=True covers the target with the page background (nothing half
    drawn shows through); otherwise only the loader floats in the middle.
    """

    def __init__(self, target: QWidget, text: str = "", opaque: bool = False,
                 size: int = 72) -> None:
        super().__init__(target)
        self._target = target
        self._opaque = opaque
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, not opaque)
        if not opaque:
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        from PySide6.QtWidgets import QVBoxLayout
        column = QVBoxLayout(self)
        column.setContentsMargins(16, 16, 16, 16)
        column.addStretch(1)
        self.label = LoadingLabel("", "acMuted", size=size)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.set_loading(text)
        column.addWidget(self.label)
        column.addStretch(1)
        target.installEventFilter(self)
        self.hide()

    def set_text(self, text: str) -> None:
        self.label.set_loading(text)

    def show_over(self, text: Optional[str] = None) -> None:
        if text is not None:
            self.set_text(text)
        elif not self.label.is_loading():
            self.label.set_loading(self.label.text())
        self.setGeometry(self._target.rect())
        self.show()
        self.raise_()

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        from PySide6.QtCore import QEvent
        if watched is self._target and event.type() == QEvent.Type.Resize:
            self.setGeometry(self._target.rect())
        return False

    def paintEvent(self, _event) -> None:  # noqa: N802
        if self._opaque:
            from app.core.theme import Theme
            p = QPainter(self)
            p.fillRect(self.rect(), QColor(Theme.token("BG")))
            p.end()


class LoadingHold:
    """Keeps a loading animation on screen for at least min_ms (3 s), so it
    always plays through instead of flashing for a split second.

        self._hold = LoadingHold(self)
        def show_loading(self):
            self._hold.begin()
            self.status.set_loading("Loading…")
        def show_posts(self, posts):
            if self._hold.wait(self.show_posts, posts):
                return                      # comes back here when 3 s are up
            ...draw the posts...

    Only the latest waiting call of each method runs, so a newer result
    replaces an older one. Calls made when no loading is showing go straight through.
    """

    def __init__(self, owner: QWidget, min_ms: int = 3000) -> None:
        self._owner = owner
        self._min_ms = min_ms
        self._clock = QElapsedTimer()
        self._active = False
        self._load = 0                      # which load the waiting calls belong to
        self._tickets: dict = {}            # one waiting call per method
        self._order = 0

    @classmethod
    def of(cls, owner: QWidget, name: str = "_loading_hold") -> "LoadingHold":
        """The hold kept on owner (made the first time it is asked for)."""
        hold = getattr(owner, name, None)
        if hold is None:
            hold = cls(owner)
            setattr(owner, name, hold)
        return hold

    def begin(self) -> None:
        self._clock.start()
        self._active = True
        self._load += 1                    # forget results of an older load
        self._tickets.clear()
        self._order = 0

    def remaining(self) -> int:
        if not self._active:
            return 0
        return max(0, self._min_ms - self._clock.elapsed())

    def wait(self, fn, *args, **kwargs) -> bool:
        """True if fn(*args) was put off until the minimum time is up."""
        left = self.remaining()
        if left <= 0:
            self._active = False
            return False
        key = getattr(fn, "__name__", id(fn))
        ticket = self._tickets[key] = self._tickets.get(key, 0) + 1
        load = self._load
        self._order += 1

        def later() -> None:
            if load == self._load and self._tickets.get(key) == ticket:
                self._active = False
                fn(*args, **kwargs)
        # same moment for every waiting call, in the order they came in
        QTimer.singleShot(left + 10 + self._order, self._owner, later)
        return True


class MinimumLoading:
    """The Refresh buttons: the Akeso loader over a page for at least
    min_ms, even when the download finishes sooner, so the refresh is
    visible and the logo animation can play through a few times.

        gate = MinimumLoading(page, "Refreshing the encyclopedia…")
        gate.begin()
        ... later, when the work is done:
        gate.finish(then=redraw)                     # waits out the rest
        gate.finish(then=None, message="Offline…")   # shows a note, then hides
    """

    def __init__(self, target: QWidget, text: str, min_ms: int = 10_000) -> None:
        self._overlay = LoaderOverlay(target, text, opaque=True, size=96)
        self._text = text
        self._min_ms = min_ms
        self._clock = QElapsedTimer()
        self.active = False

    def begin(self) -> None:
        self.active = True
        self._clock.start()
        self._overlay.show_over(self._text)

    def restart_animation(self) -> None:
        """Play the logo build from the start (after the app was busy and
        the animation was frozen on one frame)."""
        self._overlay.label._loader._clock.restart()

    def finish(self, then=None, message: str = "") -> None:
        if not self.active:
            if then is not None:
                then()
            return
        wait = max(0, self._min_ms - self._clock.elapsed())

        def done() -> None:
            if then is not None:
                then()
            if message:
                self._overlay.label.setText(message)        # stops the animation
                QTimer.singleShot(2500, self._close)
            else:
                self._close()
        QTimer.singleShot(wait, done)

    def _close(self) -> None:
        self.active = False
        self._overlay.hide()
