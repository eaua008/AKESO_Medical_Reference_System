"""Step 6: pages for the Reference column (right).

    SearchPage      search diseases, symptoms and medicines; a result opens
                    as its own tab, so the search stays where it was
    MonographPage   a compact monograph with collapsible sections; every
                    section has "Insert into notes"

Everything here is read-only reference content. The student's writing
only happens in the notes editor.
"""

import html
from typing import Optional

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.core import lucide
from app.core.interaction_styles import tone_color
from app.services.reference_library import (
    DISEASE,
    KIND_LABELS,
    MEDICINE,
    SYMPTOM,
    Monograph,
    RefHit,
    ReferenceLibrary,
    Section,
)
from app.ui.views.interaction_widgets import FlowLayout

KIND_ICONS = {DISEASE: "book-open", SYMPTOM: "activity", MEDICINE: "pill"}


def _repolish(widget: QWidget) -> None:
    widget.style().unpolish(widget)
    widget.style().polish(widget)


class _Chip(QPushButton):
    def __init__(self, text: str, object_name: str = "nbFilterChip") -> None:
        super().__init__(text)
        self.setObjectName(object_name)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


# ======================================================================
#   Search
# ======================================================================

class SearchPage(QWidget):
    open_requested = Signal(str, str, str)          # kind, id, name

    def __init__(self, library: ReferenceLibrary, pins: Optional[list[RefHit]] = None) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._library = library
        self._kind = ""

        col = QVBoxLayout(self)
        col.setContentsMargins(14, 12, 14, 10)
        col.setSpacing(10)

        field = QFrame()
        field.setObjectName("nbSearchField")
        field.setFixedHeight(36)
        row = QHBoxLayout(field)
        row.setContentsMargins(10, 0, 8, 0)
        self._search_icon = QLabel()
        row.addWidget(self._search_icon)
        self.query = QLineEdit()
        self.query.setObjectName("nbSearchInput")
        self.query.setPlaceholderText("Search diseases, symptoms, medicines...")
        self.query.setClearButtonEnabled(True)
        row.addWidget(self.query, 1)
        col.addWidget(field)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(180)
        self._timer.timeout.connect(self._fill)
        self.query.textChanged.connect(lambda _t: self._timer.start())
        self.query.returnPressed.connect(self._open_current)

        chips = QHBoxLayout()
        chips.setSpacing(6)
        self._chips: dict[str, _Chip] = {}
        for kind, label in (("", "All"), (DISEASE, "Diseases"), (SYMPTOM, "Symptoms"),
                            (MEDICINE, "Medicines")):
            chip = _Chip(label)
            chip.clicked.connect(lambda _c=False, k=kind: self._set_kind(k))
            self._chips[kind] = chip
            chips.addWidget(chip)
        chips.addStretch(1)
        col.addLayout(chips)

        if pins:
            col.addWidget(QLabel("PINNED FOR THIS CASE", objectName="nbRailCap"))
            host = QWidget()
            host.setObjectName("panel")
            flow = FlowLayout(host, spacing=6)
            for hit in pins:
                chip = _Chip(hit.name, "nbPinChip")
                chip.setToolTip(f"{KIND_LABELS.get(hit.kind, '')}: open as a tab")
                chip.clicked.connect(lambda _c=False, h=hit: self.open_requested.emit(
                    h.kind, h.id, h.name))
                flow.addWidget(chip)
            col.addWidget(host)

        self.count = QLabel("", objectName="nbSmallMuted")
        col.addWidget(self.count)
        self.results = QListWidget()
        self.results.setObjectName("nbRefList")
        self.results.setIconSize(QSize(16, 16))
        self.results.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.results.itemClicked.connect(self._open_item)
        col.addWidget(self.results, 1)
        self._set_kind("")
        self.refresh_theme()

    def _set_kind(self, kind: str) -> None:
        self._kind = kind
        for key, chip in self._chips.items():
            chip.setProperty("on", "true" if key == kind else "false")
            _repolish(chip)
        self._fill()

    def _fill(self) -> None:
        hits = self._library.search(self.query.text(), self._kind)
        self.results.clear()
        for hit in hits:
            item = QListWidgetItem(f"{hit.name}\n{KIND_LABELS[hit.kind]}"
                                   f"{' · ' + hit.subtitle if hit.subtitle else ''}")
            item.setIcon(lucide.icon(KIND_ICONS[hit.kind], 16, tone_color("primary")))
            item.setData(Qt.ItemDataRole.UserRole, (hit.kind, hit.id, hit.name))
            item.setSizeHint(QSize(0, 46))
            self.results.addItem(item)
        if hits:
            self.count.setText(f"{len(hits)} result{'s' if len(hits) != 1 else ''}"
                               + ("  ·  showing the first 60" if len(hits) >= 60 else ""))
            self.results.setCurrentRow(0)
        elif self.query.text().strip():
            self.count.setText("Nothing in the reference data matches that search.")
        else:
            self.count.setText("The reference data isn't loaded yet.")

    def _open_item(self, item: QListWidgetItem) -> None:
        kind, item_id, name = item.data(Qt.ItemDataRole.UserRole)
        self.open_requested.emit(kind, item_id, name)

    def _open_current(self) -> None:
        item = self.results.currentItem()
        if item is not None:
            self._open_item(item)

    def refresh_theme(self) -> None:
        self._search_icon.setPixmap(lucide.pixmap("search", 15, tone_color("muted")))
        self._fill()


# ======================================================================
#   Monograph
# ======================================================================

class _SectionCard(QFrame):
    insert_requested = Signal()

    def __init__(self, section: Section, expanded: bool) -> None:
        super().__init__()
        self.setObjectName("nbRefSection")
        col = QVBoxLayout(self)
        col.setContentsMargins(12, 8, 10, 10)
        col.setSpacing(6)
        head = QHBoxLayout()
        head.setSpacing(6)
        self.toggle = QPushButton(f"  {section.title}")
        self.toggle.setObjectName("nbSectionToggle")
        self.toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle.clicked.connect(self._flip)
        head.addWidget(self.toggle, 1)
        insert = QPushButton("  Insert into notes")
        insert.setObjectName("nbInsertButton")
        insert.setCursor(Qt.CursorShape.PointingHandCursor)
        insert.setIcon(lucide.icon("arrow-down-to-line", 13, tone_color("primary")))
        insert.setToolTip("Copy this section into the open note, with a Source link")
        insert.clicked.connect(self.insert_requested.emit)
        head.addWidget(insert)
        col.addLayout(head)

        body = []
        body += [f"<p>{html.escape(p)}</p>" for p in section.paragraphs if p.strip()]
        if section.bullets:
            body.append("<ul style='margin-left:-18px'>" + "".join(
                f"<li>{html.escape(b)}</li>" for b in section.bullets) + "</ul>")
        self.text = QLabel("".join(body), objectName="nbRefText")
        self.text.setWordWrap(True)
        self.text.setTextFormat(Qt.TextFormat.RichText)
        self.text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        col.addWidget(self.text)
        self._expanded = expanded
        self._show()

    def _flip(self) -> None:
        self._expanded = not self._expanded
        self._show()

    def _show(self) -> None:
        self.text.setVisible(self._expanded)
        self.toggle.setIcon(lucide.icon("chevron-down" if self._expanded else "chevron-right",
                                        14, tone_color("muted")))


class MonographPage(QWidget):
    insert_requested = Signal(str, str)         # section title, html
    open_full_requested = Signal(str, str)      # kind, id

    def __init__(self, mono: Optional[Monograph], kind: str, item_id: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.mono = mono
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        if mono is None:
            missing = QLabel(f"This {KIND_LABELS.get(kind, 'entry').lower()} isn't in the "
                             "reference data any more, or the data hasn't loaded yet.",
                             objectName="nbEmpty")
            missing.setWordWrap(True)
            missing.setAlignment(Qt.AlignmentFlag.AlignCenter)
            outer.addWidget(missing)
            return

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        host = QWidget()
        host.setObjectName("panel")
        col = QVBoxLayout(host)
        col.setContentsMargins(14, 14, 14, 16)
        col.setSpacing(8)

        head = QHBoxLayout()
        head.setSpacing(10)
        icon = QLabel()
        icon.setObjectName("nbKindTile")
        icon.setProperty("tone", "primary")
        icon.setFixedSize(32, 32)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setPixmap(lucide.pixmap(KIND_ICONS[mono.kind], 16, tone_color("primary")))
        head.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)
        titles = QVBoxLayout()
        titles.setSpacing(1)
        name = QLabel(mono.name, objectName="nbMonoTitle")
        name.setWordWrap(True)
        titles.addWidget(name)
        if mono.subtitle:
            sub = QLabel(mono.subtitle, objectName="nbSmallMuted")
            sub.setWordWrap(True)
            titles.addWidget(sub)
        head.addLayout(titles, 1)
        col.addLayout(head)

        lock = QHBoxLayout()
        lock_icon = QLabel()
        lock_icon.setPixmap(lucide.pixmap("lock", 12, tone_color("muted")))
        lock.addWidget(lock_icon)
        lock.addWidget(QLabel(f"{KIND_LABELS[mono.kind]} · Reference · read-only",
                              objectName="nbLockLabel"))
        lock.addStretch(1)
        col.addLayout(lock)

        if mono.badges:
            badges = QWidget()
            badges.setObjectName("panel")
            flow = FlowLayout(badges, spacing=6)
            for text, tone in mono.badges:
                badge = QLabel(f" {text} ", objectName="nbVerdict")
                badge.setProperty("tone", tone)
                flow.addWidget(badge)
            col.addWidget(badges)

        for index, section in enumerate(mono.sections):
            card = _SectionCard(section, expanded=index < 2)
            card.insert_requested.connect(
                lambda s=section: self.insert_requested.emit(s.title, s.to_html()))
            col.addWidget(card)
        if not mono.sections:
            col.addWidget(QLabel("This entry has no sections written yet.",
                                 objectName="nbSmallMuted"))

        full = QPushButton("  Open full monograph")
        full.setObjectName("nbButton")
        full.setCursor(Qt.CursorShape.PointingHandCursor)
        full.setIcon(lucide.icon("external-link", 14, tone_color("text")))
        full.clicked.connect(lambda: self.open_full_requested.emit(mono.kind, mono.id))
        col.addWidget(full, 0, Qt.AlignmentFlag.AlignLeft)
        col.addStretch(1)
        scroll.setWidget(host)
        outer.addWidget(scroll)
