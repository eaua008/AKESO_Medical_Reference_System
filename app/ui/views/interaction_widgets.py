"""Small building blocks shared by the Drug Interaction Checker's three tabs.

Result cards (drug x condition, drug x drug, combination rule), badges,
icon labels, section panels, a clickable frame, and a layout that wraps
chips onto new lines.
"""

from PySide6.QtCore import QPoint, QRect, QSize, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.interaction_styles import tone_color
from app.services.drug_safety_service import (
    UNKNOWN,
    VERDICT_AVOID,
    VERDICT_CAUTION,
    VERDICT_COMPATIBLE,
    VERDICT_NO_FLAGS,
)

# verdict -> (badge, tone, icon, summary). Written in reference voice: they
# describe what the data says about a combination, never about a person.
VERDICTS = {
    VERDICT_COMPATIBLE: ("NO INTERACTIONS ON RECORD", "success", "shield-check",
                         "Reference data records every checked combination as compatible."),
    VERDICT_NO_FLAGS: ("NO FLAGS, GAPS IN DATA", "primary", "shield",
                       "Nothing is flagged, but {unknown} of the checked combinations are "
                       "not on record. Treat those as unverified, not as compatible."),
    VERDICT_CAUTION: ("PRECAUTIONS ON RECORD", "amber", "triangle-alert",
                      "Reference data notes precautions in this combination."),
    VERDICT_AVOID: ("SIGNIFICANT INTERACTION ON RECORD", "danger", "shield-alert",
                    "Reference data flags a significant interaction in this combination."),
}
# severity -> (badge, tone)
SEVERITIES = {
    "safe": ("COMPATIBLE", "success"),
    "caution": ("PRECAUTION", "amber"),
    "avoid": ("AVOID", "danger"),
    UNKNOWN: ("NOT ON RECORD", "muted"),
}


# ---------------------------------------------------------------- basics

def icon_label(name: str, size: int, tone: str) -> QLabel:
    label = QLabel()
    label.setPixmap(lucide.pixmap(name, size, tone_color(tone)))
    label.setFixedSize(size, size)
    return label


def badge(text: str, tone: str) -> QLabel:
    label = QLabel(text, objectName="ixBadge")
    label.setProperty("tone", tone)
    return label


def severity_badge(severity: str) -> QLabel:
    return badge(*SEVERITIES.get(severity, SEVERITIES[UNKNOWN]))


def wrapped(text: str, name: str) -> QLabel:
    label = QLabel(text, objectName=name)
    label.setWordWrap(True)
    return label


def divider() -> QFrame:
    line = QFrame()
    line.setObjectName("ixDivider")
    line.setFixedHeight(1)
    return line


def clear(layout: QLayout) -> None:
    """Remove and delete everything in a layout, nested layouts included."""
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()
        elif item.layout() is not None:
            clear(item.layout())


def repolish(widget: QWidget) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def section_panel(icon_name: str, tone: str, title: str, note: str,
                  panel_tone: str = "") -> tuple[QFrame, QVBoxLayout]:
    """A titled panel that holds a group of result cards."""
    panel = QFrame()
    panel.setObjectName("ixSectionPanel")
    if panel_tone:
        panel.setProperty("tone", panel_tone)
    body = QVBoxLayout(panel)
    body.setContentsMargins(16, 14, 16, 16)
    body.setSpacing(12)
    head = QHBoxLayout()
    head.setSpacing(8)
    head.addWidget(icon_label(icon_name, 16, tone))
    title_label = QLabel(title, objectName="ixSectionTitle")
    if panel_tone == "danger":
        title_label.setStyleSheet(f"color: {tone_color('danger')};")
    head.addWidget(title_label)
    head.addStretch(1)
    if note:
        head.addWidget(QLabel(note, objectName="ixSmallMuted"))
    body.addLayout(head)
    return panel, body


def guidance_box(lines: list[tuple[str, str]], tone: str = "") -> QFrame:
    """The tinted box under a card: [("Clinical significance", text), ...]."""
    box = QFrame()
    box.setObjectName("ixGuidance")
    if tone in ("amber", "danger"):
        box.setProperty("tone", tone)
    layout = QVBoxLayout(box)
    layout.setContentsMargins(12, 9, 12, 9)
    layout.setSpacing(4)
    colour = tone_color(tone if tone in ("amber", "danger") else "primary")
    for key, text in lines:
        layout.addWidget(wrapped(f"<span style='color:{colour}; font-weight:800'>{key}:"
                                 f"</span> {text}", "ixSmallBody"))
    return box


# ----------------------------------------------------------------- cards

def condition_card(title: str, severity: str, summary: str, guidance: str,
                   drug_name: str = "") -> QFrame:
    _text, tone = SEVERITIES.get(severity, SEVERITIES[UNKNOWN])
    card = QFrame()
    card.setObjectName("ixInnerCard")
    card.setProperty("tone", tone)
    layout = QVBoxLayout(card)
    layout.setContentsMargins(14, 12, 14, 12)
    layout.setSpacing(8)
    head = QHBoxLayout()
    head.addWidget(wrapped(title, "ixFindingTitle"), 1)
    head.addWidget(severity_badge(severity), 0, Qt.AlignmentFlag.AlignTop)
    layout.addLayout(head)
    if severity == UNKNOWN:
        subject = drug_name or "this medicine"
        summary = (f"No entry for {subject} in {title.lower()} in the reference data. "
                   "This is not confirmation that it is compatible.")
    layout.addWidget(wrapped(summary or "No summary on record.", "ixBoxBody"))
    if guidance:
        layout.addWidget(guidance_box([("Reference guidance", guidance)], tone))
    layout.addStretch(1)
    return card


def pair_card(first: str, second: str, severity: str, description: str,
              significance: str, recommendation: str, duplicate: bool = False) -> QFrame:
    badge_text, tone = SEVERITIES.get(severity, SEVERITIES[UNKNOWN])
    card = QFrame()
    card.setObjectName("ixInnerCard")
    card.setProperty("tone", tone)
    layout = QVBoxLayout(card)
    layout.setContentsMargins(14, 12, 14, 12)
    layout.setSpacing(8)
    head = QHBoxLayout()
    head.setSpacing(6)
    head.addWidget(QLabel(first, objectName="ixFindingTitle"))
    head.addWidget(icon_label("arrow-left-right", 13, "primary"))
    head.addWidget(QLabel(second, objectName="ixFindingTitle"))
    head.addStretch(1)
    head.addWidget(badge("DUPLICATE THERAPY", "amber") if duplicate
                   else badge(badge_text, tone))
    layout.addLayout(head)
    if severity == UNKNOWN:
        description = (f"No documented entry for {first} with {second} in the reference "
                       "data. This is not confirmation that they are compatible.")
    layout.addWidget(wrapped(description or "No description on record.", "ixBoxBody"))
    lines = []
    if significance:
        lines.append(("Clinical significance", significance))
    if recommendation:
        lines.append(("Reference recommendation", recommendation))
    if lines:
        layout.addWidget(guidance_box(lines, tone))
    return card


def rule_card(name: str, severity: str, description: str, drug_names: list[str],
              significance: str, recommendation: str) -> QFrame:
    _text, tone = SEVERITIES.get(severity, SEVERITIES["caution"])
    card = QFrame()
    card.setObjectName("ixInnerCard")
    card.setProperty("tone", tone)
    layout = QVBoxLayout(card)
    layout.setContentsMargins(14, 12, 14, 12)
    layout.setSpacing(8)
    head = QHBoxLayout()
    head.addWidget(wrapped(name, "ixFindingTitle"), 1)
    head.addWidget(severity_badge(severity), 0, Qt.AlignmentFlag.AlignTop)
    layout.addLayout(head)
    layout.addWidget(wrapped(description, "ixBoxBody"))
    if drug_names:
        chips = QHBoxLayout()
        chips.setSpacing(6)
        chips.addWidget(QLabel("Triggered by:", objectName="ixSmallMuted"))
        for drug in drug_names:
            chips.addWidget(QLabel(drug, objectName="ixDrugChip"))
        chips.addStretch(1)
        layout.addLayout(chips)
    lines = []
    if significance:
        lines.append(("Clinical significance", significance))
    if recommendation:
        lines.append(("Reference recommendation", recommendation))
    if lines:
        layout.addWidget(guidance_box(lines, tone))
    return card


def message_card(icon_name: str, title: str, body: str) -> QFrame:
    card = QFrame()
    card.setObjectName("ixPanel")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(24, 30, 24, 30)
    layout.setSpacing(8)
    layout.addWidget(icon_label(icon_name, 28, "primary"), 0, Qt.AlignmentFlag.AlignHCenter)
    heading = wrapped(title, "ixEmptyTitle")
    heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(heading)
    text = wrapped(body, "ixMuted")
    text.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(text)
    return card


def note_card(text: str) -> QFrame:
    card = QFrame()
    card.setObjectName("ixPanel")
    layout = QHBoxLayout(card)
    layout.setContentsMargins(16, 12, 16, 12)
    layout.setSpacing(10)
    layout.addWidget(icon_label("info", 15, "muted"), 0, Qt.AlignmentFlag.AlignTop)
    layout.addWidget(wrapped(text, "ixMuted"), 1)
    return card


def two_column(cards: list[QWidget]) -> QGridLayout:
    grid = QGridLayout()
    grid.setSpacing(12)
    for index, card in enumerate(cards):
        grid.addWidget(card, index // 2, index % 2)
    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 1)
    return grid


# ------------------------------------------------------------ interaction

class ClickFrame(QFrame):
    """A clickable card. Unlike a QPushButton it grows to fit the labels
    inside it, so wrapped text never overlaps. The "on" property drives the
    selected look in the stylesheet."""

    clicked = Signal()

    def __init__(self, object_name: str, on: bool = False) -> None:
        super().__init__()
        self.setObjectName(object_name)
        self.setProperty("on", "true" if on else "false")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
                event.position().toPoint()):
            self.clicked.emit()
        super().mouseReleaseEvent(event)


def chip(name: str, is_otc: bool, on: bool) -> ClickFrame:
    """A medicine chip: name plus a small OTC / Rx tag."""
    frame = ClickFrame("ixChipButton", on=on)
    row = QHBoxLayout(frame)
    row.setContentsMargins(10, 5, 6, 5)
    row.setSpacing(6)
    text = QLabel(name, objectName="ixChipText")
    text.setProperty("on", "true" if on else "false")
    row.addWidget(text)
    row.addWidget(QLabel("OTC" if is_otc else "RX", objectName="ixChipTag"))
    return frame


class FlowLayout(QLayout):
    """Lays chips left to right and wraps to a new line when full."""

    def __init__(self, parent: QWidget, spacing: int = 6) -> None:
        super().__init__(parent)
        self._items = []
        self._spacing = spacing
        self.setContentsMargins(0, 0, 0, 0)
        # heightForWidth is asked for again and again during one resize
        # (thousands of times across a page of cards); the answer only
        # changes when the items do, so remember it per width.
        self._hfw: dict[int, int] = {}

    def addItem(self, item) -> None:  # noqa: N802
        self._items.append(item)
        self.invalidate()

    def invalidate(self) -> None:
        cache = getattr(self, "_hfw", None)    # Qt calls this during __init__ too
        if cache:
            cache.clear()
        super().invalidate()

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int):  # noqa: N802
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int):  # noqa: N802
        if not 0 <= index < len(self._items):
            return None
        self._hfw.clear()
        return self._items.pop(index)

    def expandingDirections(self):  # noqa: N802
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:  # noqa: N802
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802
        height = self._hfw.get(width)
        if height is None:
            height = self._hfw[width] = self._arrange(QRect(0, 0, width, 0), apply=False)
        return height

    def setGeometry(self, rect: QRect) -> None:  # noqa: N802
        super().setGeometry(rect)
        self._arrange(rect, apply=True)

    def sizeHint(self) -> QSize:  # noqa: N802
        return self.minimumSize()

    def minimumSize(self) -> QSize:  # noqa: N802
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        return size

    def _arrange(self, rect: QRect, apply: bool) -> int:
        x, y, line_height = rect.x(), rect.y(), 0
        for item in self._items:
            hint = item.sizeHint().expandedTo(item.minimumSize())
            if x + hint.width() > rect.right() + 1 and line_height > 0:
                x, y = rect.x(), y + line_height + self._spacing
                line_height = 0
            if apply:
                item.setGeometry(QRect(QPoint(x, y), hint))
            x += hint.width() + self._spacing
            line_height = max(line_height, hint.height())
        return y + line_height - rect.y()
