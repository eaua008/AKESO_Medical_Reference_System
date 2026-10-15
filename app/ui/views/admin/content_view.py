"""Content Management: author, edit, archive and restore encyclopedia
entries, plus the audit trail of every admin change."""

from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QFrame, QHBoxLayout, QLineEdit, QPushButton, QScrollArea,
    QVBoxLayout, QWidget,
)

from app.core.theme import Theme
from app.models.account import friendly_time
from app.models.admin import (
    CATEGORIES, KIND_LABELS, SEVERITIES, URGENCY_LABELS, AuditEntry, ContentItem,
)
from app.ui.views.account.account_widgets import Banner, button, icon_label, label, refresh_icons
from app.ui.views.admin.admin_widgets import (
    DataTable, IconButton, actions_cell, page_header, pill_cell, pills_cell, text_cell,
    title_cell, tone_label,
)

AUDIT = "audit"
SECTIONS = [("disease", "Diseases", "stethoscope", "primary"),
            ("symptom", "Symptoms", "activity", "danger"),
            ("medicine", "Medicines", "pill", "good"),
            ("article", "Articles", "file-text", "primary"),
            (AUDIT, "Audit Trail", "history", "amber")]
SEVERITY_TONES = {"Mild": "", "Moderate": "", "Severe": "amber", "Critical": "danger"}
ACTION_TONES = {"create": "good", "update": "", "archive": "muted", "restore": "teal",
                "role": "amber", "suspend": "danger", "reactivate": "good",
                "delete_user": "danger"}

COLUMNS = {
    "disease": (["Disease / condition", "Body system", "Severity & urgency",
                 "Cardinal symptoms", "Status", "Last updated", "Actions"], [0]),
    "symptom": (["Symptom", "Body system", "Diagnostic weight", "Linked diseases",
                 "Status", "Last updated", "Actions"], [0]),
    "medicine": (["Medicine", "Drug class", "Category", "Linked diseases",
                  "Status", "Last updated", "Actions"], [0, 1]),
    "article": (["Article", "Type", "Topic", "Linked entries",
                 "Status", "Last updated", "Actions"], [0]),
    AUDIT: (["When", "Who", "Action", "Target", "Details"], [3, 4]),
}


class _SectionTab(QPushButton):
    """Icon, name and a count badge, as one checkable button."""

    def __init__(self, text: str, icon: str, tone: str) -> None:
        super().__init__()
        self.setObjectName("adTab")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        row = QHBoxLayout(self)
        row.setContentsMargins(10, 4, 10, 4)
        row.setSpacing(7)
        self._icon_name = icon
        self._icon = icon_label(icon, 15)
        row.addWidget(self._icon)
        self._text = label(text, "adTabText", wrap=False)
        row.addWidget(self._text)
        self.count = tone_label("0", "adCount", tone)
        row.addWidget(self.count)
        self.setMinimumHeight(34)
        self.toggled.connect(self._restyle)

    def sizeHint(self):  # noqa: N802
        # As wide as the icon, name and badge inside (a QPushButton with a
        # layout otherwise sizes itself for its own, empty, text).
        return self.layout().sizeHint()

    def minimumSizeHint(self):  # noqa: N802
        return self.layout().sizeHint()

    def _restyle(self, on: bool) -> None:
        self._text.setStyleSheet(
            f"color: {Theme.token('BADGE_TEXT') if on else Theme.token('TEXT_MUTED')};"
            "font-size: 12px; font-weight: 700; background: transparent;")


class ContentManagementView(QWidget):
    refresh_requested = Signal()
    add_requested = Signal(str)                    # kind
    edit_requested = Signal(str, str)              # kind, id
    publish_requested = Signal(str, str, bool)     # kind, id, published
    audit_requested = Signal()                     # the Audit Trail tab was opened

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._items: dict[str, list[ContentItem]] = {"disease": [], "symptom": [], "medicine": [],
                                                     "article": []}
        self._audit: list[AuditEntry] = []
        self._systems: list[tuple[str, str]] = []
        self._section = "disease"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        column = QVBoxLayout(page)
        column.setContentsMargins(30, 22, 30, 30)
        column.setSpacing(16)

        header, right = page_header(
            "ADMIN MODULE", "good", "Authoring & Clinical Database Curation", "database",
            Theme.token("SUCCESS"), "Content Management",
            "Author, edit, validate and curate clinical monographs. Saved changes reach "
            "the encyclopedias and checkers on every computer at their next sync.")
        right.addWidget(self._section_tabs(), 0, Qt.AlignmentFlag.AlignTop)
        column.addWidget(header)

        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        column.addWidget(self.banner)
        column.addWidget(self._filter_bar())

        self.tables: dict[str, DataTable] = {}
        for kind, (headers, stretch) in COLUMNS.items():
            fixed = {len(headers) - 1: 96} if kind != AUDIT else {}
            table = DataTable(headers, stretch=stretch, fixed=fixed)
            table.hide()
            column.addWidget(table)
            self.tables[kind] = table
        self._empty = label("", "adEmpty")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.hide()
        column.addWidget(self._empty)
        column.addStretch(1)
        scroll.setWidget(page)
        outer.addWidget(scroll)
        self._tabs["disease"].setChecked(True)
        self._apply_section()

    # ------------------------------------------------------------- pieces

    def _section_tabs(self) -> QWidget:
        box = QFrame()
        box.setObjectName("adTabs")
        row = QHBoxLayout(box)
        row.setContentsMargins(4, 4, 4, 4)
        row.setSpacing(2)
        group = QButtonGroup(self)
        group.setExclusive(True)
        self._tabs: dict[str, _SectionTab] = {}
        for kind, text, icon, tone in SECTIONS:
            tab = _SectionTab(text, icon, tone)
            tab.clicked.connect(lambda _c=False, k=kind: self.show_section(k))
            group.addButton(tab)
            row.addWidget(tab)
            self._tabs[kind] = tab
        return box

    def _filter_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("adFilterBar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(14, 12, 14, 12)
        row.setSpacing(10)
        self.search = QLineEdit()
        self.search.setObjectName("acInput")
        self.search.setClearButtonEnabled(True)
        row.addWidget(self.search, 1)
        self._funnel = icon_label("funnel", 16)
        row.addWidget(self._funnel)
        self.system = QComboBox()
        self.system.setObjectName("acInput")
        self.system.setMinimumWidth(180)
        row.addWidget(self.system)
        self.second = QComboBox()            # severity / red flag / category
        self.second.setObjectName("acInput")
        row.addWidget(self.second)
        self.status = QComboBox()
        self.status.setObjectName("acInput")
        for text, data in (("Published & archived", ""), ("Published", "published"),
                           ("Archived", "archived")):
            self.status.addItem(text, data)
        row.addWidget(self.status)
        self.add = button("Add Disease", "acPrimary", "plus",
                          lambda: self.add_requested.emit(self._section))
        row.addWidget(self.add)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(150)
        self._timer.timeout.connect(self._render)
        self.search.textChanged.connect(lambda _t: self._timer.start())
        for combo in (self.system, self.second, self.status):
            combo.currentIndexChanged.connect(lambda _i: self._render())
        return bar

    # ------------------------------------------------------------- data in

    def set_body_systems(self, systems: list[tuple[str, str]]) -> None:
        self._systems = systems
        self._fill_filters()

    def show_content(self, items: dict[str, list[ContentItem]]) -> None:
        self._items.update(items)
        for kind, rows in items.items():
            self._tabs[kind].count.setText(str(len(rows)))
        self._render()

    def show_audit(self, entries: list[AuditEntry], total: int) -> None:
        self._audit = entries
        self._tabs[AUDIT].count.setText(str(total))
        if self._section == AUDIT:
            self._render()

    def items(self, kind: str) -> list[ContentItem]:
        return list(self._items.get(kind, []))

    def body_systems(self) -> list[tuple[str, str]]:
        return list(self._systems)

    # ------------------------------------------------------------ sections

    def show_section(self, kind: str) -> None:
        self._section = kind
        self._tabs[kind].setChecked(True)
        self._apply_section()
        if kind == AUDIT:
            self.audit_requested.emit()

    def current_section(self) -> str:
        return self._section

    def _apply_section(self) -> None:
        kind = self._section
        for tab_kind, tab in self._tabs.items():
            tab._restyle(tab_kind == kind)
        is_audit = kind == AUDIT
        for widget in (self.system, self.second, self.status, self.add, self._funnel):
            widget.setVisible(not is_audit)
        self.system.setVisible(kind in ("disease", "symptom"))
        if not is_audit:
            self.add.setText(f"  Add {KIND_LABELS[kind]}")
        self.search.setPlaceholderText({
            "disease": "Search diseases by name, scientific term or ID…",
            "symptom": "Search symptoms by name, clinical term or ID…",
            "medicine": "Search medicines by name, generic name, class or ID…",
            "article": "Search articles by title, topic, source or ID…",
            AUDIT: "Search the audit trail by person, action or entry…"}[kind])
        self._fill_filters()
        self._render()

    def _fill_filters(self) -> None:
        kind = self._section
        for combo in (self.system, self.second):
            combo.blockSignals(True)
            combo.clear()
        self.system.addItem("All body systems", "")
        for system_id, name in self._systems:
            self.system.addItem(name, system_id)
        if kind == "disease":
            self.second.addItem("All severities", "")
            for severity in SEVERITIES:
                self.second.addItem(severity, severity)
        elif kind == "symptom":
            self.second.addItem("All symptoms", "")
            self.second.addItem("Red flags only", "red")
        elif kind == "medicine":
            self.second.addItem("All categories", "")
            for value, text in CATEGORIES:
                self.second.addItem(text, value)
            self.second.addItem("Black box warning", "blackbox")
        elif kind == "article":
            self.second.addItem("All types", "")
            self.second.addItem("Akeso articles", "written")
            self.second.addItem("External links", "external")
        for combo in (self.system, self.second):
            combo.blockSignals(False)

    # ------------------------------------------------------------- showing

    def _visible(self) -> list[ContentItem]:
        kind = self._section
        query = self.search.text()
        system, second, status = (self.system.currentData(), self.second.currentData(),
                                  self.status.currentData())
        rows = []
        for item in self._items.get(kind, []):
            if not item.matches(query):
                continue
            if system and item.body_system_id != system:
                continue
            if status == "published" and not item.published:
                continue
            if status == "archived" and item.published:
                continue
            if second:
                if kind == "disease" and item.severity != second:
                    continue
                if kind == "symptom" and second == "red" and not item.is_red_flag:
                    continue
                if kind == "article" and item.category != second:
                    continue
                if kind == "medicine":
                    if second == "blackbox" and not item.black_box:
                        continue
                    if second != "blackbox" and item.category != second:
                        continue
            rows.append(item)
        return rows

    def _render(self) -> None:
        kind = self._section
        for table_kind, table in self.tables.items():
            table.setVisible(table_kind == kind)
        table = self.tables[kind]
        if kind == AUDIT:
            query = self.search.text().strip().lower()
            entries = [e for e in self._audit if not query or query in " ".join(
                (e.actor_label, e.action_label, e.target_label, e.target_id, e.summary)).lower()]
            table.set_rows([self._audit_row(e) for e in entries])
            empty = "Nothing has been changed from the admin panel yet." if not self._audit \
                else "No entry matches this search."
            shown = bool(entries)
        else:
            items = self._visible()
            table.set_rows([self._row(item) for item in items])
            total = len(self._items.get(kind, []))
            empty = (f"No {KIND_LABELS[kind].lower()}s yet. Use “Add {KIND_LABELS[kind]}” "
                     "to write the first one." if not total
                     else "Nothing matches these filters.")
            shown = bool(items)
        table.fit_height()
        table.setVisible(shown)
        self._empty.setText(empty)
        self._empty.setVisible(not shown)

    def _row(self, item: ContentItem) -> list[QWidget]:
        status = pill_cell("Published", "good") if item.published else pill_cell("Archived", "muted")
        updated = text_cell(friendly_time(item.updated_at, with_time=False), "adCellMuted")
        edit = IconButton("pencil", f"Edit {item.name}",
                          on_click=lambda i=item: self.edit_requested.emit(i.kind, i.id))
        if item.published:
            toggle = IconButton("archive", "Archive (hide from users)", Theme.token("DANGER"),
                                lambda i=item: self.publish_requested.emit(i.kind, i.id, False))
        else:
            toggle = IconButton("rotate-ccw", "Restore (show to users again)",
                                Theme.token("SUCCESS"),
                                lambda i=item: self.publish_requested.emit(i.kind, i.id, True))
        actions = actions_cell([edit, toggle])
        if item.kind == "disease":
            return [title_cell(item.name, item.subtitle),
                    pill_cell(item.body_system or "Unclassified", "muted", name="adChip"),
                    pill_cell(f"{item.severity} severity", SEVERITY_TONES.get(item.severity, ""),
                              URGENCY_LABELS.get(item.urgency or "", "").upper()),
                    text_cell(f"{item.count} symptom{'s' if item.count != 1 else ''}",
                              "adCellTitle", f"({item.primary_count} primary cardinal)"),
                    status, updated, actions]
        if item.kind == "symptom":
            weight = [(f"Weight {item.weight}/10", "")]
            if item.is_red_flag:
                weight.append(("Red flag", "danger"))
            return [title_cell(item.name, item.subtitle),
                    pill_cell(item.body_system or "General", "muted", name="adChip"),
                    pills_cell(weight),
                    text_cell(f"{item.count} disease{'s' if item.count != 1 else ''}"),
                    status, updated, actions]
        if item.kind == "article":
            written = item.category == "written"
            return [title_cell(item.name, item.subtitle or item.id),
                    pill_cell("Akeso article" if written else "External link",
                              "good" if written else "blue"),
                    pill_cell(item.drug_class or "General", "muted", name="adChip"),
                    text_cell(f"{item.count} entr{'y' if item.count == 1 else 'ies'}"),
                    status, updated, actions]
        category = [("Rx" if item.category == "Prescription" else "OTC",
                     "blue" if item.category == "Prescription" else "teal")]
        if item.black_box:
            category.append(("Black box", "danger"))
        return [title_cell(item.name, item.subtitle),
                title_cell(item.drug_class or "—", name="adCellText"),
                pills_cell(category),
                text_cell(f"{item.count} disease{'s' if item.count != 1 else ''}"),
                status, updated, actions]

    @staticmethod
    def _audit_row(entry: AuditEntry) -> list[QWidget]:
        return [text_cell(friendly_time(entry.created_at), "adCellMuted"),
                text_cell(entry.actor_label, "adCellTitle"),
                pill_cell(entry.action_label, ACTION_TONES.get(entry.action, "")),
                text_cell(entry.target_label or entry.target_id, "adCellTitle",
                          KIND_LABELS.get(entry.target_kind, entry.target_kind)
                          + ("" if entry.target_kind == "user" else f" · {entry.target_id}")),
                text_cell(entry.summary or "—", "adCellMuted")]

    def show_error(self, message: str) -> None:
        self.banner.show_message(message, "danger", "Dismiss")

    def show_notice(self, message: str) -> None:
        self.banner.show_message(message, "good", "Dismiss")

    def refresh_theme(self) -> None:
        refresh_icons(self)
        self._apply_section()


