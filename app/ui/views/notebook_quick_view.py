"""Level 2: the quick view inside the half-width slide panel.

    ┌ [NOTE] Title (editable)     [⤢ Open Workspace] [pin][copy][bin][✕] ┐
    │ Subject ▾   Tags: a, b                  Edited Mar 24 · Created …   │
    │ ┌ Case summary · Reference ───────────────────────────────┐        │
    │ └──────────────────────────────────────────────────────────┘        │
    │ ┌ My notes ────────────────────────────────────────────────┐        │
    │ └──────────────────────────────────────────────────────────┘        │
    │ ⓘ Cases are hypothetical study scenarios…                          │
    └─────────────────────────────────────────────────────────────────────┘

Title, subject and tags are edited right here; everything else is read-only
until you open the workspace.
"""

from typing import Optional

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.interaction_styles import tone_color
from app.models.notebook import NotebookItem, Subject
from app.services.notebook_service import HYPOTHETICAL_NOTE
from app.ui.views.interaction_widgets import FlowLayout
from app.ui.views.notebook_home import short_date


def _repolish(widget: QWidget) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)


class QuickView(QWidget):
    open_workspace = Signal()
    close_requested = Signal()
    action = Signal(str)                        # pin | duplicate | delete | open_checker
    details_changed = Signal(str, str, list)    # title, subject id, tags

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("nbPanelBody")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._item: Optional[NotebookItem] = None
        self._icon_jobs: list = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._build_header())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        host = QWidget()
        host.setObjectName("panel")
        self._col = QVBoxLayout(host)
        self._col.setContentsMargins(22, 16, 22, 22)
        self._col.setSpacing(14)
        self._col.addLayout(self._build_details())
        self.error = QLabel("", objectName="nbError")
        self.error.hide()
        self._col.addWidget(self.error)
        self._sections = QVBoxLayout()
        self._sections.setSpacing(14)
        self._col.addLayout(self._sections)
        self._col.addStretch(1)
        scroll.setWidget(host)
        outer.addWidget(scroll, 1)
        self.refresh_icons()

    # ------------------------------------------------------------ building

    def _icon_button(self, icon: str, tip: str, signal_name: str) -> QPushButton:
        button = QPushButton()
        button.setObjectName("nbIconButton")
        button.setFixedSize(32, 32)
        button.setToolTip(tip)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._icon_jobs.append((button, icon, 16, "muted"))
        button.clicked.connect(lambda: self.action.emit(signal_name)
                               if signal_name != "close" else self.close_requested.emit())
        return button

    def _build_header(self) -> QWidget:
        head = QFrame()
        head.setObjectName("nbPanelHead")
        row = QHBoxLayout(head)
        row.setContentsMargins(18, 12, 12, 12)
        row.setSpacing(8)
        self.badge = QLabel("", objectName="nbKindBadge")
        row.addWidget(self.badge)
        self.title = QLineEdit()
        self.title.setObjectName("nbTitleEdit")
        self.title.setMaxLength(120)
        self.title.setToolTip("Click to rename")
        self.title.editingFinished.connect(self._emit_details)
        row.addWidget(self.title, 1)

        self.open_button = QPushButton("  Open Workspace")
        self.open_button.setObjectName("nbPrimary")
        self.open_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._icon_jobs.append((self.open_button, "maximize-2", 14, "white"))
        self.open_button.clicked.connect(self.open_workspace.emit)
        row.addWidget(self.open_button)
        self.pin_button = self._icon_button("pin", "Pin", "pin")
        row.addWidget(self.pin_button)
        row.addWidget(self._icon_button("copy", "Duplicate", "duplicate"))
        row.addWidget(self._icon_button("trash-2", "Delete", "delete"))
        row.addWidget(self._icon_button("x", "Close (Esc)", "close"))
        return head

    def _build_details(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(10)
        self.subject = QComboBox()
        self.subject.setObjectName("nbCombo")
        self.subject.setMinimumWidth(170)
        self.subject.activated.connect(lambda _i: self._emit_details())
        row.addWidget(QLabel("Subject", objectName="nbFieldLabel"))
        row.addWidget(self.subject)
        row.addSpacing(6)
        row.addWidget(QLabel("Tags", objectName="nbFieldLabel"))
        self.tags = QLineEdit()
        self.tags.setObjectName("nbInput")
        self.tags.setPlaceholderText("Comma separated, e.g. Pneumonia, CURB-65")
        self.tags.editingFinished.connect(self._emit_details)
        row.addWidget(self.tags, 1)
        self.dates = QLabel("", objectName="nbSmallMuted")
        row.addWidget(self.dates)
        return row

    def _section(self, icon: str, title: str, reference: bool = False) -> tuple[QFrame, QVBoxLayout]:
        frame = QFrame()
        frame.setObjectName("nbSection")
        col = QVBoxLayout(frame)
        col.setContentsMargins(16, 13, 16, 15)
        col.setSpacing(9)
        head = QHBoxLayout()
        head.setSpacing(8)
        glyph = QLabel()
        glyph.setPixmap(lucide.pixmap(icon, 15, tone_color("primary")))
        head.addWidget(glyph)
        head.addWidget(QLabel(title, objectName="nbSectionTitle"))
        head.addStretch(1)
        if reference:
            lock = QLabel()
            lock.setPixmap(lucide.pixmap("lock", 12, tone_color("muted")))
            head.addWidget(lock)
            head.addWidget(QLabel("Reference · read-only", objectName="nbLockLabel"))
        col.addLayout(head)
        self._sections.addWidget(frame)
        return frame, col

    @staticmethod
    def _chips(parent_col: QVBoxLayout, label: str, values: list[str], empty: str) -> None:
        parent_col.addWidget(QLabel(label, objectName="nbFieldLabel"))
        if not values:
            parent_col.addWidget(QLabel(empty, objectName="nbSmallMuted"))
            return
        host = QWidget()
        host.setObjectName("panel")
        flow = FlowLayout(host, spacing=6)
        for value in values:
            flow.addWidget(QLabel(value, objectName="nbChip"))
        parent_col.addWidget(host)

    # ------------------------------------------------------------- drawing

    def show_item(self, item: NotebookItem, subjects: list[Subject],
                  case_summary: Optional[dict] = None) -> None:
        self._item = item
        self.error.hide()
        self.badge.setText(f"  {item.kind_label.upper()}  ")
        self.badge.setProperty("tone", item.tone)
        _repolish(self.badge)
        self.title.setText(item.title)
        self.title.setCursorPosition(0)
        self.pin_button.setToolTip("Unpin" if item.pinned else "Pin")
        self.pin_button.setIcon(lucide.icon(
            "pin", 16, tone_color("amber") if item.pinned else tone_color("muted")))

        self.subject.blockSignals(True)
        self.subject.clear()
        self.subject.addItem("No subject", "")
        for subject in subjects:
            self.subject.addItem(subject.name, subject.id)
        self.subject.setCurrentIndex(max(0, self.subject.findData(item.subject_id)))
        self.subject.blockSignals(False)
        self.tags.setText(", ".join(item.tags))
        self.dates.setText(f"Edited {short_date(item.updated_at)}  ·  "
                           f"Created {short_date(item.created_at)}")

        while self._sections.count():
            child = self._sections.takeAt(0).widget()
            if child is not None:
                child.setParent(None)
                child.deleteLater()

        summary = case_summary or {}
        self._symptom_card(item, summary.get("symptom"))
        self._interaction_card(item, summary.get("interaction"))
        if item.has_case_data:
            add = QPushButton("  Add case summary to my notes")
            add.setObjectName("nbInsertButton")
            add.setCursor(Qt.CursorShape.PointingHandCursor)
            add.setIcon(lucide.icon("arrow-down-to-line", 13, tone_color("primary")))
            add.setToolTip("Adds the attached case(s) to the end of your notes as tables. "
                           "The answer key is left out.")
            add.clicked.connect(lambda: self.action.emit("summary"))
            self._sections.addWidget(add, 0, Qt.AlignmentFlag.AlignLeft)

        _frame, col = self._section("notebook-pen", "My notes")
        if item.body.strip() and "<" in item.body:
            viewer = QTextBrowser()
            viewer.setObjectName("nbNotesView")
            viewer.setOpenExternalLinks(False)
            viewer.setHtml(item.body)
            viewer.setMinimumHeight(160)
            viewer.setMaximumHeight(380)
            col.addWidget(viewer)
        elif item.plain_text:
            text = QLabel(item.plain_text, objectName="nbBody")
            text.setWordWrap(True)
            text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            col.addWidget(text)
        else:
            hint = QLabel("No notes yet. Open the workspace to start writing.",
                          objectName="nbSmallMuted")
            col.addWidget(hint)

        if item.has_case_data:
            note = QFrame()
            note.setObjectName("nbNoteBox")
            row = QHBoxLayout(note)
            row.setContentsMargins(12, 9, 12, 9)
            row.setSpacing(8)
            icon = QLabel()
            icon.setPixmap(lucide.pixmap("info", 14, tone_color("primary")))
            row.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)
            text = QLabel(HYPOTHETICAL_NOTE, objectName="nbSmallMuted")
            text.setWordWrap(True)
            row.addWidget(text, 1)
            self._sections.addWidget(note)

    # ------------------------------------------------ attached checker runs

    def _link_card(self, badge_text: str, tone: str, attached: bool) -> QVBoxLayout:
        frame = QFrame()
        frame.setObjectName("nbLinkCard")
        frame.setProperty("attached", "true" if attached else "false")
        col = QVBoxLayout(frame)
        col.setContentsMargins(14, 11, 14, 13)
        col.setSpacing(8)
        head = QHBoxLayout()
        badge = QLabel(f"  {badge_text}  ", objectName="nbKindBadge")
        badge.setProperty("tone", tone)
        head.addWidget(badge)
        head.addStretch(1)
        state = QLabel("Attached to this note" if attached else "Not added yet",
                       objectName="nbLinkState")
        state.setProperty("attached", "true" if attached else "false")
        head.addWidget(state)
        col.addLayout(head)
        self._sections.addWidget(frame)
        return col

    def _card_button(self, col: QVBoxLayout, text: str, icon: str, action: str,
                     primary: bool) -> None:
        button = QPushButton(f"  {text}")
        button.setObjectName("nbPrimary" if primary else "nbButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setIcon(lucide.icon(icon, 14, tone_color("white" if primary else "text")))
        button.clicked.connect(lambda: self.action.emit(action))
        col.addWidget(button, 0, Qt.AlignmentFlag.AlignLeft)

    def _symptom_card(self, item: NotebookItem, overview: Optional[dict]) -> None:
        data = item.symptom_data
        col = self._link_card("SYMPTOM CHECKER CASE", "success", bool(data.get("symptoms")))
        if not data.get("symptoms"):
            hint = QLabel("Build the presentation in the Symptom Checker: symptoms, vitals "
                          "and history. Saving there attaches it to this note, with its "
                          "hallmark correlation.", objectName="nbSmallMuted")
            hint.setWordWrap(True)
            col.addWidget(hint)
            self._card_button(col, "Add a case from the Symptom Checker", "activity",
                              "symptom_checker", True)
            return
        if overview:
            col.addWidget(QLabel(overview["facts"], objectName="nbBodyStrong"))
        if data.get("chief_complaint"):
            quote = QLabel(f"“{data['chief_complaint']}”", objectName="nbQuote")
            quote.setWordWrap(True)
            col.addWidget(quote)
        if data.get("vignette"):
            vignette = QLabel(data["vignette"], objectName="nbBody")
            vignette.setWordWrap(True)
            col.addWidget(vignette)
        self._chips(col, "Reported symptoms",
                    [s.get("name", "") for s in data.get("symptoms", [])], "None recorded.")
        if overview:
            col.addWidget(QLabel("Best hallmark match (reference)", objectName="nbFieldLabel"))
            top = QLabel(overview["top"], objectName="nbBody")
            top.setWordWrap(True)
            col.addWidget(top)
        self._card_button(col, "Edit in Symptom Checker", "pencil", "symptom_checker", False)

    def _interaction_card(self, item: NotebookItem, summary: Optional[dict]) -> None:
        data = item.interaction_data
        attached = bool(data.get("candidate_id"))
        col = self._link_card("DRUG INTERACTION CHECK", "amber", attached)
        if not attached:
            hint = QLabel("Check a candidate drug against a regimen and comorbidities in the "
                          "Drug Interaction Checker. Saving there attaches it to this note.",
                          objectName="nbSmallMuted")
            hint.setWordWrap(True)
            col.addWidget(hint)
            self._card_button(col, "Add a check from the Drug Interaction Checker", "shield",
                              "drug_checker", True)
            return
        if summary is None:
            col.addWidget(QLabel("The drug-safety reference data isn't loaded yet.",
                                 objectName="nbSmallMuted"))
        else:
            verdict_text, verdict_tone = summary.get("verdict", ("", "muted"))
            if verdict_text:
                badge = QLabel(f"  {verdict_text}  ", objectName="nbVerdict")
                badge.setProperty("tone", verdict_tone)
                col.addWidget(badge, 0, Qt.AlignmentFlag.AlignLeft)
                col.addWidget(QLabel("Worked out again from today's reference data.",
                                     objectName="nbSmallMuted"))
            col.addWidget(QLabel("Candidate drug", objectName="nbFieldLabel"))
            col.addWidget(QLabel(summary.get("candidate") or "Not in reference data",
                                 objectName="nbBodyStrong"))
            self._chips(col, "Case regimen", summary.get("regimen", []), "No other drugs.")
            self._chips(col, "Case comorbidities", summary.get("conditions", []),
                        "No comorbidities.")
        self._card_button(col, "Edit in Drug Interaction Checker", "pencil", "drug_checker",
                          False)

    # --------------------------------------------------------------- input

    def _emit_details(self) -> None:
        if self._item is None:
            return
        tags = [t for t in self.tags.text().split(",") if t.strip()]
        self.details_changed.emit(self.title.text(), self.subject.currentData() or "", tags)

    def show_error(self, message: str) -> None:
        self.error.setText(message)
        self.error.setVisible(bool(message))

    # --------------------------------------------------------------- theme

    def refresh_icons(self) -> None:
        for button, icon, size, tone in self._icon_jobs:
            button.setIcon(lucide.icon(icon, size, tone_color(tone)))
            button.setIconSize(QSize(size, size))
        if self._item is not None:
            self.pin_button.setIcon(lucide.icon(
                "pin", 16, tone_color("amber") if self._item.pinned else tone_color("muted")))

    def refresh_theme(self) -> None:
        # Section icons are baked pixmaps: the controller shows the item again.
        self.refresh_icons()

    @property
    def item_id(self) -> str:
        return self._item.id if self._item else ""

