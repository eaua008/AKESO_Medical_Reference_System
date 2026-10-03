"""Pop-ups for the Drug Interaction Checker.

    OverlayDialog       a card over a dimmed copy of the app window
    ConfirmDialog       small yes/no (deleting a case)
    SaveCaseDialog      Save as Case Study: title, tags, notes
    AddDrugDialog       search the medicine database and add one to the case

The dialogs only collect input. The controller validates and saves.
"""

from typing import Optional

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.interaction_styles import tone_color
from app.models.case_study import SUGGESTED_TAGS
from app.services.case_study_service import MedicineOption
from app.ui.views.interaction_widgets import FlowLayout

HYPOTHETICAL_NOTE = ("Cases are hypothetical study scenarios. Do not enter real patient "
                     "names or identifiers.")


class OverlayDialog(QDialog):
    """A modal card over a dimmed copy of the app window."""

    def __init__(self, parent: QWidget, title: str, subtitle: str, width: int = 420) -> None:
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        window = parent.window()
        self.setGeometry(QRect(window.mapToGlobal(window.rect().topLeft()), window.size()))

        outer = QVBoxLayout(self)
        self.card = QFrame()
        self.card.setObjectName("ixDialogCard")
        self.card.setFixedWidth(width)
        # Aligned, so the card keeps its natural height instead of stretching.
        outer.addWidget(self.card, 0, Qt.AlignmentFlag.AlignCenter)

        self.body = QVBoxLayout(self.card)
        self.body.setContentsMargins(18, 16, 18, 16)
        self.body.setSpacing(10)
        head = QHBoxLayout()
        titles = QVBoxLayout()
        titles.setSpacing(1)
        titles.addWidget(QLabel(title, objectName="ixDialogTitle"))
        if subtitle:
            sub = QLabel(subtitle, objectName="ixSmallMuted")
            sub.setWordWrap(True)
            titles.addWidget(sub)
        head.addLayout(titles, 1)
        close = QPushButton()
        close.setObjectName("ixClose")
        close.setIcon(lucide.icon("x", 16, tone_color("muted")))
        close.setCursor(Qt.CursorShape.PointingHandCursor)
        close.clicked.connect(self.reject)
        head.addWidget(close, 0, Qt.AlignmentFlag.AlignTop)
        self.body.addLayout(head)
        self.body.addWidget(_divider())

        self.error = QLabel("", objectName="ixError")
        self.error.setWordWrap(True)
        self.error.hide()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 170))
        painter.end()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if not self.card.geometry().contains(event.position().toPoint()):
            self.reject()
        else:
            super().mousePressEvent(event)

    def add_buttons(self, confirm_text: str) -> QPushButton:
        self.body.addWidget(self.error)
        self.body.addWidget(_divider())
        row = QHBoxLayout()
        row.addStretch(1)
        cancel = QPushButton("Cancel")
        cancel.setObjectName("ixSecondary")
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.reject)
        confirm = QPushButton(confirm_text)
        confirm.setObjectName("ixPrimary")
        confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm.setDefault(True)
        row.addWidget(cancel)
        row.addWidget(confirm)
        self.body.addLayout(row)
        return confirm

    def show_error(self, message: str) -> None:
        self.error.setText(message)
        self.error.setVisible(bool(message))


class ConfirmDialog(OverlayDialog):
    def __init__(self, parent: QWidget, title: str, message: str, confirm_text: str) -> None:
        super().__init__(parent, title, "", width=380)
        text = QLabel(message, objectName="ixBoxBody")
        text.setWordWrap(True)
        self.body.addWidget(text)
        self.confirm = self.add_buttons(confirm_text)
        self.confirm.clicked.connect(self.accept)


class SaveCaseDialog(OverlayDialog):
    def __init__(self, parent: QWidget, candidate_name: str, regimen_count: int,
                 condition_count: int, verdict_text: str, verdict_tone: str) -> None:
        super().__init__(parent, "Save as Case Study",
                         "Keep this scenario to reopen, compare or study later", width=460)

        summary = QFrame()
        summary.setObjectName("ixCountdown")
        column = QVBoxLayout(summary)
        column.setContentsMargins(12, 9, 12, 9)
        column.setSpacing(6)
        column.addWidget(QLabel(f"Candidate: <b>{candidate_name}</b>  •  Regimen: "
                                f"<b>{regimen_count}</b>  •  Comorbidities: "
                                f"<b>{condition_count}</b>", objectName="ixSmallBody"))
        badge = QLabel(verdict_text, objectName="ixBadge")
        badge.setProperty("tone", verdict_tone)
        column.addWidget(badge, 0, Qt.AlignmentFlag.AlignLeft)
        self.body.addWidget(summary)

        self.body.addWidget(QLabel("Case Title *", objectName="ixFieldLabel"))
        self.title = QLineEdit()
        self.title.setObjectName("ixInput")
        self.title.setPlaceholderText("e.g. Elderly patient on anticoagulant")
        self.body.addWidget(self.title)

        self.body.addWidget(QLabel("Tags", objectName="ixFieldLabel"))
        self._tag_buttons: list[QPushButton] = []
        tags_host = QWidget()
        tags_host.setObjectName("panel")
        tags = FlowLayout(tags_host, spacing=6)     # wraps, so long tags never clip
        for tag in SUGGESTED_TAGS:
            chip = QPushButton(tag)
            chip.setObjectName("ixFilterChip")
            chip.setCheckable(True)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            self._tag_buttons.append(chip)
            tags.addWidget(chip)
        self.body.addWidget(tags_host)
        self.extra_tags = QLineEdit()
        self.extra_tags.setObjectName("ixInput")
        self.extra_tags.setPlaceholderText("Other tags, comma separated")
        self.body.addWidget(self.extra_tags)

        self.body.addWidget(QLabel("Study Notes", objectName="ixFieldLabel"))
        self.notes = QPlainTextEdit()
        self.notes.setObjectName("ixText")
        self.notes.setPlaceholderText("Key observations or discussion questions...")
        self.notes.setFixedHeight(70)
        self.body.addWidget(self.notes)

        note = QFrame()
        note.setObjectName("ixNoteBox")
        note_row = QHBoxLayout(note)
        note_row.setContentsMargins(10, 8, 10, 8)
        note_row.setSpacing(8)
        icon = QLabel()
        icon.setPixmap(lucide.pixmap("info", 14, tone_color("primary")))
        note_row.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)
        text = QLabel(HYPOTHETICAL_NOTE, objectName="ixNoteText")
        text.setWordWrap(True)
        note_row.addWidget(text, 1)
        self.body.addWidget(note)

        self.confirm = self.add_buttons("Save Case Study")
        self.title.setFocus()

    def values(self) -> dict:
        tags = [b.text() for b in self._tag_buttons if b.isChecked()]
        tags += [t.strip() for t in self.extra_tags.text().split(",") if t.strip()]
        return {"title": self.title.text(), "tags": tags,
                "notes": self.notes.toPlainText()}


class AddDrugDialog(OverlayDialog):
    """Search the medicine database and pick one drug for the case regimen.

    Only database medicines can be added: the checker can only evaluate
    what the reference data describes.
    """

    def __init__(self, parent: QWidget, options: list[MedicineOption],
                 exclude: set[str]) -> None:
        super().__init__(parent, "Add Drug to Case Regimen",
                         "Search the medicine reference by name, generic or brand", width=440)
        self._options = [o for o in options if o.medicine_id not in exclude]
        self.chosen: Optional[MedicineOption] = None

        field = QFrame()
        field.setObjectName("ixSearchField")
        row = QHBoxLayout(field)
        row.setContentsMargins(10, 0, 6, 0)
        row.setSpacing(6)
        icon = QLabel()
        icon.setPixmap(lucide.pixmap("search", 15, tone_color("muted")))
        row.addWidget(icon)
        self.search = QLineEdit()
        self.search.setObjectName("ixSearchInput")
        self.search.setPlaceholderText("Type to filter...")
        self.search.textChanged.connect(self._fill)
        row.addWidget(self.search, 1)
        field.setFixedHeight(38)
        self.body.addWidget(field)

        self.list = QListWidget()
        self.list.setObjectName("ixSuggestList")
        self.list.setFixedHeight(260)
        self.list.itemDoubleClicked.connect(lambda _item: self._choose())
        self.body.addWidget(self.list)
        self.empty = QLabel("", objectName="ixSmallMuted")
        self.empty.setWordWrap(True)
        self.body.addWidget(self.empty)

        self.confirm = self.add_buttons("Add to Regimen")
        self.confirm.clicked.connect(self._choose)
        self._fill("")
        self.search.setFocus()

    def _fill(self, text: str) -> None:
        words = text.lower().split()
        self.list.clear()
        for option in self._options:
            haystack = f"{option.label} {option.drug_class}".lower()
            if words and not all(w in haystack for w in words):
                continue
            item = QListWidgetItem(f"{option.name}    —  {option.drug_class or 'No class'}"
                                   f"  ({'OTC' if option.is_otc else 'Rx'})")
            item.setData(Qt.ItemDataRole.UserRole, option.medicine_id)
            self.list.addItem(item)
        if self.list.count():
            self.list.setCurrentRow(0)
            self.empty.setText("")
        else:
            self.empty.setText("No medicine in the reference data matches that search."
                               if self._options else "Every medicine is already in the case.")

    def _choose(self) -> None:
        item = self.list.currentItem()
        if item is None:
            self.show_error("Pick a medicine from the list.")
            return
        medicine_id = item.data(Qt.ItemDataRole.UserRole)
        self.chosen = next(o for o in self._options if o.medicine_id == medicine_id)
        self.accept()


def _divider() -> QFrame:
    line = QFrame()
    line.setObjectName("ixDivider")
    line.setFixedHeight(1)
    return line
