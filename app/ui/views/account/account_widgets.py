"""Small building blocks shared by the Account tabs and dialogs."""

from datetime import date
from typing import Callable, Optional

from PySide6.QtCore import QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QAbstractButton, QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget,
)

from app.core import lucide
from app.core.theme import Theme
from app.models.account import CompletenessItem, Device, SecurityEvent, friendly_time
from app.ui.views.compare_view import FlowLayout

TONE_TOKENS = {"good": "SUCCESS", "danger": "DANGER", "info": "BADGE_TEXT"}


def tone_color(tone: str) -> str:
    if tone == "warn":
        return "#FBBF24" if Theme.mode() == "dark" else "#B45309"
    return Theme.token(TONE_TOKENS.get(tone, "BADGE_TEXT"))


def label(text: str = "", name: str = "acMuted", wrap: bool = True) -> QLabel:
    widget = QLabel(text)
    widget.setObjectName(name)
    widget.setWordWrap(wrap)
    return widget


def button(text: str, name: str = "acGhost", icon: str = "",
           on_click: Optional[Callable[[], None]] = None) -> QPushButton:
    widget = QPushButton(f"  {text}" if icon else text)
    widget.setObjectName(name)
    widget.setCursor(Qt.CursorShape.PointingHandCursor)
    if icon:
        widget.setProperty("acIcon", icon)
        paint_button_icon(widget)
    if on_click is not None:
        widget.clicked.connect(lambda _checked=False: on_click())
    return widget


def set_text(widget: QPushButton, text: str) -> None:
    """Change a button's caption, keeping the gap after its icon."""
    widget.setText(f"  {text}" if widget.property("acIcon") else text)


def paint_button_icon(widget: QPushButton) -> None:
    name = widget.property("acIcon")
    if not name:
        return
    colour = {"acPrimary": "#FFFFFF", "acDanger": Theme.token("DANGER")}.get(
        widget.objectName(), Theme.token("TEXT_MUTED"))
    widget.setIcon(lucide.icon(name, 15, colour) if hasattr(lucide, "icon")
                   else lucide.pixmap(name, 15, colour))
    widget.setIconSize(QSize(15, 15))


def icon_label(name: str, size: int = 18, colour: Optional[str] = None) -> QLabel:
    widget = QLabel()
    widget.setObjectName("panel")
    widget.setFixedSize(size, size)
    widget.setProperty("acIcon", name)
    widget.setProperty("acIconColour", colour or "")
    widget.setPixmap(lucide.pixmap(name, size, colour or Theme.token("BADGE_TEXT")))
    return widget


def refresh_icons(root: QWidget) -> None:
    """Icons are baked in one colour; redraw them after a theme switch."""
    for child in root.findChildren(QPushButton):
        paint_button_icon(child)
    for child in root.findChildren(QLabel):
        name = child.property("acIcon")
        if name:
            colour = child.property("acIconColour") or Theme.token("BADGE_TEXT")
            child.setPixmap(lucide.pixmap(name, child.width(), colour))


def repolish(widget: QWidget) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def divider() -> QFrame:
    line = QFrame()
    line.setObjectName("acDivider")
    line.setFixedHeight(1)
    return line


class Card(QFrame):
    """A rounded panel with a title, an optional subtitle and a body."""

    def __init__(self, title: str = "", subtitle: str = "", icon: str = "",
                 danger: bool = False) -> None:
        super().__init__()
        self.setObjectName("acDangerCard" if danger else "acCard")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 18, 20, 20)
        outer.setSpacing(12)
        if title:
            head = QHBoxLayout()
            head.setSpacing(10)
            if icon:
                head.addWidget(icon_label(icon, 18, Theme.token("DANGER") if danger else None),
                               0, Qt.AlignmentFlag.AlignTop)
            text = QVBoxLayout()
            text.setSpacing(2)
            text.addWidget(label(title, "acDangerTitle" if danger else "acCardTitle"))
            if subtitle:
                self.subtitle = label(subtitle, "acMuted")
                text.addWidget(self.subtitle)
            head.addLayout(text, 1)
            self.head = head
            outer.addLayout(head)
        self.body = QVBoxLayout()
        self.body.setSpacing(10)
        outer.addLayout(self.body)
        # Cards in one grid row share its height; spare room goes below the
        # content instead of pushing the title down.
        outer.addStretch(1)


class Banner(QFrame):
    """A coloured strip at the top of the page: a message and one action."""

    action = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("acBanner")
        row = QHBoxLayout(self)
        row.setContentsMargins(14, 10, 12, 10)
        row.setSpacing(10)
        self._icon = icon_label("info", 18)
        self._text = label("", "acBannerText")
        self._button = button("", "acGhost")
        self._button.clicked.connect(self.action.emit)
        row.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignTop)
        row.addWidget(self._text, 1)
        row.addWidget(self._button, 0, Qt.AlignmentFlag.AlignVCenter)
        self.hide()

    def show_message(self, text: str, tone: str = "info", action: str = "") -> None:
        icon = {"danger": "triangle-alert", "warn": "circle-alert",
                "good": "circle-check"}.get(tone, "info")
        self._icon.setProperty("acIcon", icon)
        self._icon.setProperty("acIconColour", tone_color(tone))
        self._icon.setPixmap(lucide.pixmap(icon, 18, tone_color(tone)))
        self._text.setText(text)
        self._button.setText(action)
        self._button.setVisible(bool(action))
        self.setProperty("tone", tone)
        repolish(self)
        self.show()


class ToggleSwitch(QAbstractButton):
    """An on/off switch, painted in the theme's colours."""

    def __init__(self, checked: bool = False) -> None:
        super().__init__()
        self.setCheckable(True)
        self.setChecked(checked)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(40, 22)

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(40, 22)

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        on = self.isChecked()
        track = QColor(Theme.token("PRIMARY") if on else Theme.token("BORDER"))
        if not self.isEnabled():
            track.setAlpha(110)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track)
        painter.drawRoundedRect(QRectF(0, 0, 40, 22), 11, 11)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(QRectF(21 if on else 3, 3, 16, 16))
        painter.end()


class SwitchRow(QWidget):
    """Title, explanation and a switch on the right."""

    toggled = Signal(bool)

    def __init__(self, title: str, subtitle: str, checked: bool = False) -> None:
        super().__init__()
        self.setObjectName("panel")
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 2, 0, 2)
        row.setSpacing(14)
        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(label(title, "acRowTitle"))
        text.addWidget(label(subtitle, "acSmall"))
        row.addLayout(text, 1)
        self.switch = ToggleSwitch(checked)
        self.switch.toggled.connect(self.toggled.emit)
        row.addWidget(self.switch, 0, Qt.AlignmentFlag.AlignVCenter)

    def set_checked(self, on: bool) -> None:
        self.switch.blockSignals(True)
        self.switch.setChecked(on)
        self.switch.blockSignals(False)
        self.switch.update()


class ProgressRing(QWidget):
    """Profile completeness: a ring with the percentage in the middle."""

    def __init__(self, size: int = 76) -> None:
        super().__init__()
        self._value = 0
        self.setFixedSize(size, size)

    def set_value(self, value: int) -> None:
        self._value = max(0, min(100, value))
        self.setToolTip(f"Profile {self._value}% complete")
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        size = self.width()
        rect = QRectF(5, 5, size - 10, size - 10)
        pen = QPen(QColor(Theme.token("BORDER")), 7)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(rect, 0, 360 * 16)
        colour = Theme.token("SUCCESS") if self._value >= 100 else Theme.token("PRIMARY")
        pen.setColor(QColor(colour))
        painter.setPen(pen)
        painter.drawArc(rect, 90 * 16, int(-360 * 16 * self._value / 100))
        font = QFont()
        font.setPixelSize(max(12, size // 4))
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor(Theme.token("TEXT")))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self._value}%")
        painter.end()


class ActivityBars(QWidget):
    """The last 14 days as small bars (hover a bar for the day and count)."""

    def __init__(self) -> None:
        super().__init__()
        self._days: list[tuple[date, int]] = []
        self.setMinimumHeight(96)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

    def set_days(self, days: list[tuple[date, int]]) -> None:
        self._days = days
        self.update()

    def _bar_rects(self) -> list[QRectF]:
        count = max(len(self._days), 1)
        gap = 6
        width = max(4.0, (self.width() - gap * (count - 1)) / count)
        top, bottom = 6, self.height() - 20
        peak = max([n for _d, n in self._days] + [1])
        rects = []
        for i, (_day, total) in enumerate(self._days):
            h = max(3.0, (bottom - top) * total / peak) if total else 3.0
            rects.append(QRectF(i * (width + gap), bottom - h, width, h))
        return rects

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        for rect, (day, total) in zip(self._bar_rects(), self._days):
            if rect.left() <= event.position().x() <= rect.right():
                self.setToolTip(f"{day.strftime('%a %b %d')}: {total} "
                                f"{'activity' if total == 1 else 'activities'}")
                return
        self.setToolTip("")

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        today = date.today()
        muted = QColor(Theme.token("TEXT_MUTED"))
        for rect, (day, total) in zip(self._bar_rects(), self._days):
            colour = QColor(Theme.token("PRIMARY") if total else Theme.token("BORDER"))
            if day == today and total:
                colour = QColor(Theme.token("PRIMARY_HOVER"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(colour)
            painter.drawRoundedRect(rect, 3, 3)
        if self._days:
            font = QFont()
            font.setPixelSize(10)
            painter.setFont(font)
            painter.setPen(muted)
            first, last = self._days[0][0], self._days[-1][0]
            painter.drawText(QRectF(0, self.height() - 16, 120, 16),
                             Qt.AlignmentFlag.AlignLeft, first.strftime("%b %d"))
            painter.drawText(QRectF(self.width() - 120, self.height() - 16, 120, 16),
                             Qt.AlignmentFlag.AlignRight,
                             "Today" if last == today else last.strftime("%b %d"))
        painter.end()


class StatTile(QFrame):
    def __init__(self, caption: str, icon: str = "") -> None:
        super().__init__()
        self.setObjectName("acStat")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(2)
        top = QHBoxLayout()
        self.number = label("0", "acStatNumber", wrap=False)
        top.addWidget(self.number)
        top.addStretch(1)
        if icon:
            top.addWidget(icon_label(icon, 18))
        layout.addLayout(top)
        layout.addWidget(label(caption, "acStatLabel"))

    def set_number(self, value) -> None:
        self.number.setText(f"{value:,}" if isinstance(value, int) else str(value))


class EventRow(QFrame):
    def __init__(self, event: SecurityEvent) -> None:
        super().__init__()
        self.setObjectName("acRow")
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 9, 12, 9)
        row.setSpacing(10)
        dot = QLabel()
        dot.setObjectName("panel")
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background-color: {tone_color(event.tone)}; border-radius: 5px;")
        row.addWidget(dot, 0, Qt.AlignmentFlag.AlignVCenter)
        text = QVBoxLayout()
        text.setSpacing(1)
        text.addWidget(label(event.label, "acRowTitle"))
        note = event.note
        where = event.device_name
        second = " · ".join(x for x in (note, where) if x)
        if second:
            text.addWidget(label(second, "acSmall"))
        row.addLayout(text, 1)
        when = label(friendly_time(event.created_at), "acSmall", wrap=False)
        row.addWidget(when, 0, Qt.AlignmentFlag.AlignVCenter)


class DeviceRow(QFrame):
    forget = Signal(object)

    def __init__(self, device: Device) -> None:
        super().__init__()
        self.setObjectName("acRow")
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 10, 12, 10)
        row.setSpacing(12)
        row.addWidget(icon_label("monitor", 22), 0, Qt.AlignmentFlag.AlignVCenter)
        text = QVBoxLayout()
        text.setSpacing(2)
        title = QHBoxLayout()
        title.setSpacing(8)
        title.addWidget(label(device.device_name, "acRowTitle", wrap=False))
        if device.is_current:
            title.addWidget(pill("This computer", "acPillGood"))
        elif device.is_active is False:
            title.addWidget(pill("Signed out", "acPill"))
        title.addStretch(1)
        text.addLayout(title)
        details = [device.platform, f"Akeso {device.app_version}" if device.app_version else "",
                   f"last active {friendly_time(device.last_seen)}"]
        text.addWidget(label(" · ".join(d for d in details if d), "acSmall"))
        row.addLayout(text, 1)
        if not device.is_current:
            remove = button("Remove", "acGhost")
            remove.setToolTip("Take this computer off the list. To also end its session, "
                              "use “Sign out all other devices”.")
            remove.clicked.connect(lambda: self.forget.emit(device))
            row.addWidget(remove, 0, Qt.AlignmentFlag.AlignVCenter)


class ChecklistRow(QWidget):
    fix = Signal(str)

    def __init__(self, item: CompletenessItem) -> None:
        super().__init__()
        self.setObjectName("panel")
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 3, 0, 3)
        row.setSpacing(10)
        icon = "circle-check" if item.done else "circle"
        colour = Theme.token("SUCCESS") if item.done else Theme.token("ICON_MUTED")
        row.addWidget(icon_label(icon, 18, colour), 0, Qt.AlignmentFlag.AlignVCenter)
        row.addWidget(label(item.label, "acValue" if not item.done else "acMuted"), 1)
        if not item.done:
            go = button("Set up", "acLink")
            go.clicked.connect(lambda: self.fix.emit(item.tab))
            row.addWidget(go)


def pill(text: str, name: str = "acPill") -> QLabel:
    widget = QLabel(text)
    widget.setObjectName(name)
    widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return widget


class ChipGroup(QWidget):
    """Toggle chips that wrap onto new lines (interest areas)."""

    changed = Signal()

    def __init__(self, maximum: int) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._maximum = maximum
        self._chips: dict[str, QPushButton] = {}
        self._flow = FlowLayout(8, 8)
        self.setLayout(self._flow)

    def set_options(self, options: list[str], selected: list[str]) -> None:
        while self._flow.count():
            item = self._flow.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._chips.clear()
        for option in [*options, *[s for s in selected if s not in options]]:
            chip = QPushButton(option.replace("&", "&&"))   # "&" alone would be a shortcut
            chip.setProperty("option", option)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setChecked(option in selected)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.toggled.connect(self._on_toggle)
            self._flow.addWidget(chip)
            self._chips[option] = chip

    def _on_toggle(self, _on: bool) -> None:
        full = len(self.selected()) >= self._maximum
        for chip in self._chips.values():
            chip.setEnabled(chip.isChecked() or not full)
        self.changed.emit()

    def selected(self) -> list[str]:
        return [name for name, chip in self._chips.items() if chip.isChecked()]


def field_block(caption: str, widget: QWidget, hint: str = "") -> QWidget:
    holder = QWidget()
    holder.setObjectName("panel")
    column = QVBoxLayout(holder)
    column.setContentsMargins(0, 0, 0, 0)
    column.setSpacing(5)
    column.addWidget(label(caption.upper(), "acFieldLabel", wrap=False))
    column.addWidget(widget)
    if hint:
        column.addWidget(label(hint, "acSmall"))
    return holder
