"""The dosage table on the medicine page, plus the panels under it.

    Indication | Route | Dose | Frequency | Duration | Max | Source
    ── ADULTS ───────────────────────────────────────────────
    ...
    ── CHILDREN ─────────────────────────────────────────────
    ...

    [Dose changes · kidney]  [How to give it]  [Forms in the PH]  [Monitor]

Rows come from MedicineMonograph.doses and the panels from .dose_notes. A
panel only appears when there is something in it. The table keeps a
sensible minimum width and scrolls sideways inside its own box on narrow
windows, so the page itself never does.
"""

from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core import soft_scale
from app.models.medicine import DOSE_NOTE_KINDS, DoseRow, MedicineMonograph
from app.ui.components.fluid import ResponsiveGrid

COLUMNS = (
    # title, stretch, minimum width
    ("Indication", 5, 170),
    ("Route", 1, 52),
    ("Dose", 3, 110),
    ("Frequency", 4, 130),
    ("Duration", 3, 100),
    ("Max", 3, 100),
    ("Source", 2, 112),
)
TABLE_MIN_WIDTH = 820
MAX_BOX_HEIGHT = 680      # (at 100%) taller tables scroll inside their box, with a hint


def _label(text: str, name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(name)
    label.setWordWrap(wrap)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    return label


def _source_tag(tag: str, medicine: MedicineMonograph, on_click) -> QWidget:
    """The Source cell: a button that jumps to the citation in References
    when the medicine has one for this tag, plain text otherwise."""
    if medicine.dose_source(tag) is None:
        return _label(tag, "mdDoseSource")
    button = QPushButton(tag)
    button.setObjectName("mdDoseSourceLink")
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setToolTip(f"{medicine.dose_source(tag).source_name}\nClick to see it in References")
    button.clicked.connect(lambda _c=False, t=tag: on_click(t))
    return button


class DosageTable(QFrame):
    """The grouped table itself (no panels)."""

    source_clicked = Signal(str)          # the tag, e.g. "Label \u00b7 FDA PH"

    def __init__(self, medicine: MedicineMonograph, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._medicine = medicine
        self.setObjectName("mdDoseTable")
        self.setMinimumWidth(TABLE_MIN_WIDTH)
        grid = QGridLayout(self)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        for column, (_title, stretch, minimum) in enumerate(COLUMNS):
            grid.setColumnStretch(column, stretch)
            grid.setColumnMinimumWidth(column, minimum)

        row = 0
        for column, (title, _s, _m) in enumerate(COLUMNS):
            cell = _label(title.upper(), "mdDoseHead", wrap=False)
            cell.setProperty("first", column == 0)
            grid.addWidget(cell, row, column)
        row += 1
        for group_title, rows in medicine.dose_groups():
            band = _label(group_title.upper(), "mdDoseGroup", wrap=False)
            grid.addWidget(band, row, 0, 1, len(COLUMNS))
            row += 1
            for index, dose in enumerate(rows):
                self._add_row(grid, row, dose, last=index == len(rows) - 1)
                row += 1

    def _add_row(self, grid: QGridLayout, row: int, dose: DoseRow, last: bool) -> None:
        # Indication with its small note under it, in one cell.
        first = QWidget()
        first.setObjectName("mdDoseCell")
        first.setProperty("last", last)
        box = QVBoxLayout(first)
        box.setContentsMargins(12, 9, 10, 9)
        box.setSpacing(2)
        box.addWidget(_label(dose.indication, "mdDoseIndication"))
        if dose.note:
            box.addWidget(_label(dose.note, "mdDoseNote"))
        box.addStretch(1)
        grid.addWidget(first, row, 0)

        values = (
            (dose.route or "—", "mdDoseText"),
            (dose.dose or "—", "mdDoseNumber"),
            (dose.frequency or "—", "mdDoseText"),
            (dose.duration or "—", "mdDoseText"),
            (dose.max_dose or "—", "mdDoseNumber"),
        )
        for column, (text, name) in enumerate(values, start=1):
            cell = QWidget()
            cell.setObjectName("mdDoseCell")
            cell.setProperty("last", last)
            layout = QVBoxLayout(cell)
            layout.setContentsMargins(8, 9, 8, 9)
            layout.addWidget(_label(text, name))
            layout.addStretch(1)
            grid.addWidget(cell, row, column)

        source = QWidget()
        source.setObjectName("mdDoseCell")
        source.setProperty("last", last)
        layout = QVBoxLayout(source)
        layout.setContentsMargins(8, 9, 10, 9)
        if dose.source:
            layout.addWidget(_source_tag(dose.source, self._medicine, self.source_clicked.emit),
                             0, Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(1)
        grid.addWidget(source, row, len(COLUMNS) - 1)


class DosePanel(QFrame):
    """One panel under the table: "Dose changes · kidney function", etc."""

    def __init__(self, title: str, notes, medicine: Optional[MedicineMonograph] = None,
                 on_source=None) -> None:
        super().__init__()
        self.setObjectName("mdDosePanel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)
        layout.addWidget(_label(title, "mdDosePanelTitle"))
        sources = []
        for note in notes:
            if note.label:
                line = QHBoxLayout()
                line.setSpacing(10)
                key = _label(note.label, "mdDosePanelKey", wrap=False)
                key.setMinimumWidth(96)
                line.addWidget(key, 0, Qt.AlignmentFlag.AlignTop)
                line.addWidget(_label(note.content, "mdDosePanelText"), 1)
                layout.addLayout(line)
            else:
                line = QHBoxLayout()
                line.setSpacing(6)
                line.addWidget(_label("•", "mdDosePanelKey", wrap=False), 0,
                               Qt.AlignmentFlag.AlignTop)
                line.addWidget(_label(note.content, "mdDosePanelText"), 1)
                layout.addLayout(line)
            if note.source and note.source not in sources:
                sources.append(note.source)
        if sources:
            from html import escape
            from app.core.theme import Theme
            parts = []
            for tag in sources:
                if medicine is not None and on_source and medicine.dose_source(tag):
                    parts.append(f'<a href="{escape(tag, quote=True)}" style="color:'
                                 f'{Theme.token("BADGE_TEXT")}; text-decoration:none;">'
                                 f'{escape(tag)}</a>')
                else:
                    parts.append(escape(tag))
            line = QLabel("Source: " + ", ".join(parts))
            line.setObjectName("mdDoseNote")
            line.setWordWrap(True)
            line.setTextFormat(Qt.TextFormat.RichText)
            line.setOpenExternalLinks(False)
            if on_source:
                line.linkActivated.connect(on_source)
            layout.addWidget(line)
        layout.addStretch(1)


class DosageSection(QWidget):
    """Table + panels, ready to drop into the monograph's dosage section."""

    source_clicked = Signal(str)          # a source tag was clicked

    def __init__(self, medicine: MedicineMonograph, viewport: Optional[QWidget] = None,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        column = QVBoxLayout(self)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(12)

        # The table scrolls sideways in its own box when the window is narrow.
        holder = QScrollArea()
        holder.setObjectName("mdDoseScroll")
        holder.setFrameShape(QFrame.Shape.NoFrame)
        holder.setWidgetResizable(True)
        holder.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        holder.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table = DosageTable(medicine)
        self.table.source_clicked.connect(self.source_clicked.emit)
        holder.setWidget(self.table)
        holder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._holder = holder
        column.addWidget(holder)
        # "There is more": shown under the box only while rows are hidden
        # below (or to the right of) what the box shows.
        self._more = QLabel("")
        self._more.setObjectName("mdDoseMore")
        self._more.setWordWrap(False)
        self._more.hide()
        column.addWidget(self._more, 0, Qt.AlignmentFlag.AlignHCenter)
        holder.verticalScrollBar().valueChanged.connect(lambda _v: self._update_more())
        holder.horizontalScrollBar().valueChanged.connect(lambda _v: self._update_more())
        holder.verticalScrollBar().rangeChanged.connect(lambda _a, _b: self._update_more())
        holder.horizontalScrollBar().rangeChanged.connect(lambda _a, _b: self._update_more())

        panels = [DosePanel(title, medicine.notes_of(kind), medicine, self.source_clicked.emit)
                  for kind, title in DOSE_NOTE_KINDS if medicine.notes_of(kind)]
        if panels:
            grid = ResponsiveGrid(300, 2, spacing=12)
            if viewport is not None:
                grid.watch(viewport)
            grid.set_cards(panels)
            column.addWidget(grid)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._fit_height()

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._fit_height()

    def _fit_height(self) -> None:
        """Show the whole table, nothing cut off. The table is told its full
        height for the width it really has, so rows can't be squeezed; only a
        very long table (over MAX_BOX_HEIGHT) scrolls inside its box, with a
        visible scroll bar and the hint under it. Checked again once the page
        has settled, because the first width Qt reports can be provisional."""
        self._apply_height()
        if not getattr(self, "_settling", False):
            self._settling = True
            QTimer.singleShot(0, self._settled)

    def _settled(self) -> None:
        self._settling = False
        self._apply_height()

    def _apply_height(self) -> None:
        capped = self._full_height(self.width()) > self._max_box()
        if capped:                                    # room for the vertical bar
            self._holder.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            bar_w = self._holder.verticalScrollBar().sizeHint().width()
            full = self._full_height(self.width() - bar_w)
        else:
            self._holder.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            full = self._full_height(self.width())
        # Measured heights are real pixels already, so they skip the 80%/90%
        # shrink (soft_scale) - shrinking them again cut the table off.
        soft_scale.exact(self.table, "setMinimumHeight", full)   # rows keep full height
        narrow = self.width() < self.table.minimumWidth()
        side = self._holder.horizontalScrollBar().sizeHint().height() if narrow else 0
        soft_scale.exact(self._holder, "setFixedHeight", min(full, self._max_box()) + side)
        self._update_more()
        self.updateGeometry()

    def _full_height(self, width: int) -> int:
        """The table's real height at this width: its rows (word-wrapped)
        plus the table's own border/padding from the style sheet."""
        layout, table = self.table.layout(), self.table
        m = table.contentsMargins()
        inner = max(width, table.minimumWidth()) - m.left() - m.right()
        rows = layout.heightForWidth(inner) if layout.hasHeightForWidth() else -1
        if rows <= 0:
            rows = layout.sizeHint().height()
        return rows + m.top() + m.bottom()

    @staticmethod
    def _max_box() -> int:
        return soft_scale.px(MAX_BOX_HEIGHT)

    def _update_more(self) -> None:
        down = self._holder.verticalScrollBar()
        side = self._holder.horizontalScrollBar()
        parts = []
        if down.maximum() > 0 and down.value() < down.maximum():
            parts.append("\u2193 Scroll for more rows")
        if side.maximum() > 0 and side.value() < side.maximum():
            parts.append("\u2192 Scroll for more columns")
        text = "   \u00b7   ".join(parts)
        if text != self._more.text():
            self._more.setText(text)
            self._more.ensurePolished()
            # Full height for its font + padding, so the hint is never cut.
            soft_scale.exact(self._more, "setMinimumHeight",
                             self._more.fontMetrics().height() + soft_scale.px(10))
            self._more.adjustSize()
        self._more.setWordWrap(False)       # fluid.contain() may have wrapped it
        if self._more.isHidden() == bool(parts):
            self._more.setVisible(bool(parts))
            self.updateGeometry()
