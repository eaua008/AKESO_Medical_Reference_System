"""The full-page editor for a disease, symptom or medicine.

Opens in the shell's slide-in sheet (page_sheet.py). It builds a plain dict
in the shape the admin_save_* database functions expect and emits it with
submitted; the controller sends it and answers with show_error() or by
closing the sheet. Every list is saved in the order shown here, which is
the order the encyclopedia displays it.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView, QCheckBox, QComboBox, QCompleter, QDoubleSpinBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLineEdit, QPlainTextEdit, QScrollArea, QSpinBox, QTableWidget,
    QVBoxLayout, QWidget,
)

from app.models.admin import (
    CATEGORIES, KIND_LABELS, MEDICINE_FACTS, PREVENTION_TIERS, SAFETY, SEVERITIES, URGENCIES, slug,
)
from app.ui.views.account.account_widgets import button, field_block, icon_label, label, refresh_icons
from app.ui.views.admin.admin_widgets import IconButton

EDITOR_MAX_WIDTH = 980


# ------------------------------------------------------------------ fields

def _line(text: str = "", placeholder: str = "", maximum: int = 200) -> QLineEdit:
    edit = QLineEdit(text or "")
    edit.setObjectName("acInput")
    edit.setPlaceholderText(placeholder)
    edit.setMaxLength(maximum)
    edit.setCursorPosition(0)
    return edit


def _text(text: str = "", placeholder: str = "", height: int = 90) -> QPlainTextEdit:
    edit = QPlainTextEdit(text or "")
    edit.setObjectName("acInput")
    edit.setPlaceholderText(placeholder)
    edit.setFixedHeight(height)
    edit.setTabChangesFocus(True)
    return edit


def _combo(items: list[tuple[str, str]], value: Optional[str]) -> QComboBox:
    combo = QComboBox()
    combo.setObjectName("acInput")
    for data, text in items:
        combo.addItem(text, data)
    index = combo.findData(value if value is not None else "")
    combo.setCurrentIndex(max(index, 0))
    return combo


class LinesEdit(QPlainTextEdit):
    """A list edited as text: one item per line, in order."""

    def __init__(self, lines: list[str], placeholder: str, height: int = 96) -> None:
        super().__init__("\n".join(lines or []))
        self.setObjectName("acInput")
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(height)
        self.setTabChangesFocus(True)

    def lines(self) -> list[str]:
        return [line.strip() for line in self.toPlainText().splitlines() if line.strip()]


class RowsTable(QWidget):
    """A small editable table for structured lists (references, links).

    columns: (key, caption, kind, options) where kind is "text", "combo",
    "check", "int" or "float"; options is a list of (value, label) for
    combos and (minimum, maximum) for numbers.
    """

    def __init__(self, columns: list[tuple], rows: list[dict], add_label: str,
                 stretch: tuple[int, ...] = (0,)) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._columns = columns
        column = QVBoxLayout(self)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(6)
        # One extra column at the end: move up / move down / remove, per row.
        self.table = QTableWidget(0, len(columns) + 1)
        self.table.setObjectName("adRows")
        self.table.setHorizontalHeaderLabels([c[1] for c in columns] + [""])
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.table.verticalHeader().setDefaultSectionSize(38)
        header = self.table.horizontalHeader()
        for index, spec in enumerate(columns):
            if index in stretch:
                header.setSectionResizeMode(index, QHeaderView.ResizeMode.Stretch)
            else:
                header.setSectionResizeMode(index, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(len(columns), QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(len(columns), 100)
        column.addWidget(self.table)
        buttons = QHBoxLayout()
        buttons.addWidget(button(add_label, "acGhost", "plus", lambda: self.add_row({})))
        buttons.addStretch(1)
        column.addLayout(buttons)
        for row in rows or []:
            self.add_row(row)
        self._fit()

    def _fit(self) -> None:
        rows = max(self.table.rowCount(), 1)
        self.table.setFixedHeight(self.table.horizontalHeader().height() + 38 * rows + 6)

    def _editor(self, kind: str, options, value):
        if kind == "combo":
            combo = QComboBox()
            combo.setObjectName("acInput")
            for data, text in options:
                combo.addItem(text, data)
            if len(options) > 12:
                # Long lists (every symptom or medicine): type to filter.
                combo.setEditable(True)
                combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
                combo.completer().setFilterMode(Qt.MatchFlag.MatchContains)
                combo.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
            index = combo.findData(value)
            combo.setCurrentIndex(index if index >= 0 else 0)
            return combo
        if kind == "check":
            box = QCheckBox()
            box.setChecked(bool(value))
            holder = QWidget()
            holder.setObjectName("panel")
            row = QHBoxLayout(holder)
            row.setContentsMargins(10, 0, 0, 0)
            row.addWidget(box)
            holder.box = box
            return holder
        if kind in ("int", "float"):
            low, high = options
            spin = QSpinBox() if kind == "int" else QDoubleSpinBox()
            spin.setObjectName("acInput")
            spin.setRange(low, high)
            if kind == "float":
                spin.setSingleStep(0.1)
                spin.setDecimals(1)
            spin.setValue(value if value is not None else (5 if kind == "int" else 1.0))
            return spin
        edit = QLineEdit(str(value or ""))
        edit.setObjectName("acInput")
        return edit

    def add_row(self, values: dict) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        for index, (key, _caption, kind, options) in enumerate(self._columns):
            default = None
            if kind == "float":
                default = float(values.get(key, 1.0) or 1.0)
            elif kind == "int":
                default = int(values.get(key, 5) or 5)
            else:
                default = values.get(key)
            editor = self._editor(kind, options, default)
            if isinstance(editor, QLineEdit):
                editor.setCursorPosition(0)       # show the start of long text
            self.table.setCellWidget(row, index, editor)
        tools = QWidget()
        tools.setObjectName("panel")
        line = QHBoxLayout(tools)
        line.setContentsMargins(4, 0, 4, 0)
        line.setSpacing(2)
        for icon, tip, action in (("chevron-up", "Move up", lambda t=tools: self._move(t, -1)),
                                  ("chevron-down", "Move down", lambda t=tools: self._move(t, 1)),
                                  ("x", "Remove", lambda t=tools: self._remove(t))):
            line.addWidget(IconButton(icon, tip, on_click=action))
        self.table.setCellWidget(row, len(self._columns), tools)
        self._fit()

    def _row_of(self, tools: QWidget) -> int:
        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, len(self._columns)) is tools:
                return row
        return -1

    def _remove(self, tools: QWidget) -> None:
        row = self._row_of(tools)
        if row >= 0:
            self.table.removeRow(row)
            self._fit()

    def _move(self, tools: QWidget, step: int) -> None:
        row = self._row_of(tools)
        target = row + step
        if row < 0 or not 0 <= target < self.table.rowCount():
            return
        values = self.rows(skip_empty=False)
        values[row], values[target] = values[target], values[row]
        self.set_rows(values)

    def set_rows(self, rows: list[dict]) -> None:
        self.table.setRowCount(0)
        for row in rows:
            self.add_row(row)
        self._fit()

    def rows(self, skip_empty: bool = True) -> list[dict]:
        result = []
        for row in range(self.table.rowCount()):
            values = {}
            for index, (key, _caption, kind, _options) in enumerate(self._columns):
                widget = self.table.cellWidget(row, index)
                if kind == "combo":
                    data = widget.currentData()
                    if widget.isEditable() and widget.currentText() != widget.itemText(widget.currentIndex()):
                        data = None        # typed something that is not in the list
                    values[key] = data
                elif kind == "check":
                    values[key] = widget.box.isChecked()
                elif kind in ("int", "float"):
                    values[key] = widget.value()
                else:
                    values[key] = widget.text().strip()
            first_key, first_kind = self._columns[0][0], self._columns[0][2]
            if skip_empty and not values.get(first_key) and first_kind in ("text", "combo"):
                continue
            result.append(values)
        return result


def _section(title: str, hint: str = "") -> tuple[QFrame, QVBoxLayout]:
    box = QFrame()
    box.setObjectName("adSection")
    column = QVBoxLayout(box)
    column.setContentsMargins(18, 16, 18, 18)
    column.setSpacing(12)
    column.addWidget(label(title, "adSectionTitle", wrap=False))
    if hint:
        column.addWidget(label(hint, "acSmall"))
    return box, column


def _pair(left: QWidget, right: QWidget) -> QWidget:
    holder = QWidget()
    holder.setObjectName("panel")
    row = QHBoxLayout(holder)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(14)
    row.addWidget(left, 1, Qt.AlignmentFlag.AlignTop)
    row.addWidget(right, 1, Qt.AlignmentFlag.AlignTop)
    return holder


REFERENCE_COLUMNS = [
    ("source_name", "Source", "text", None),
    ("citation_text", "Citation", "text", None),
    ("url", "URL", "text", None),
    ("is_mother_book", "Textbook", "check", None),
]


# ------------------------------------------------------------------ editor

class ContentEditor(QWidget):
    submitted = Signal(object)          # dict
    cancel_requested = Signal()

    def __init__(self, kind: str, data: dict, is_new: bool,
                 body_systems: list[tuple[str, str]],
                 symptoms: list[tuple[str, str]], medicines: list[tuple[str, str]],
                 diseases: list[tuple[str, str]], parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("adEditor")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.kind = kind
        self.is_new = is_new
        self._data = data or {}
        self._systems = [("", "No body system")] + list(body_systems)
        # A blank first choice, so a new row never silently picks the first item.
        self._symptoms = [("", "Choose a symptom…")] + list(symptoms)
        self._medicines = [("", "Choose a medicine…")] + list(medicines)
        self._diseases = [("", "Choose a condition…")] + [
            d for d in diseases if d[0] != self._data.get("id")]
        self._id_touched = not is_new
        self._busy = False
        self._busy_widgets: list[QWidget] = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        centre = QHBoxLayout(page)
        centre.setContentsMargins(40, 26, 40, 30)
        column = QWidget()
        column.setObjectName("panel")
        column.setMaximumWidth(EDITOR_MAX_WIDTH)
        self._form = QVBoxLayout(column)
        self._form.setContentsMargins(0, 0, 0, 0)
        self._form.setSpacing(16)
        centre.addStretch(1)
        centre.addWidget(column, 100)
        centre.addStretch(1)
        scroll.setWidget(page)
        outer.addWidget(scroll, 1)

        what = KIND_LABELS[kind].lower()
        head = QHBoxLayout()
        head.setSpacing(12)
        icon = {"disease": "stethoscope", "symptom": "activity", "medicine": "pill"}[kind]
        head.addWidget(icon_label(icon, 26), 0, Qt.AlignmentFlag.AlignTop)
        titles = QVBoxLayout()
        titles.setSpacing(4)
        titles.addWidget(label(f"New {what}" if is_new else f"Edit {what}: {self._data.get('name', '')}",
                               "acTitle"))
        titles.addWidget(label(
            "Saved changes reach every running copy of Akeso on its next sync. Archived "
            "entries stay in the database but are hidden from users.", "acSubtitle"))
        head.addLayout(titles, 1)
        self._form.addLayout(head)

        self._build_identity()
        getattr(self, f"_build_{kind}")()
        self._build_references()
        self._form.addStretch(1)

        foot = QFrame()
        foot.setObjectName("adEditorFoot")
        foot_row = QHBoxLayout(foot)
        foot_row.setContentsMargins(40, 12, 40, 12)
        foot_row.setSpacing(10)
        self.error = label("", "acError")
        self.error.hide()
        foot_row.addWidget(self.error, 1)
        foot_row.addStretch(1)
        cancel = button("Cancel", "acGhost", on_click=self.cancel_requested.emit)
        self._go = button(f"Create {what}" if is_new else "Save changes", "acPrimary", "check",
                          self._submit)
        for widget in (cancel, self._go):
            foot_row.addWidget(widget)
            self._busy_widgets.append(widget)
        outer.addWidget(foot)
        self._saved = self._snapshot()

    # ------------------------------------------------------------- shared

    def _build_identity(self) -> None:
        d = self._data
        box, column = _section("Identity")
        self.name = _line(d.get("name"), {"disease": "e.g. Dengue Fever",
                                          "symptom": "e.g. Fever",
                                          "medicine": "e.g. Paracetamol"}[self.kind], 160)
        self.entry_id = _line(d.get("id"), "letters, numbers and underscores", 60)
        self.entry_id.setReadOnly(not self.is_new)
        self.entry_id.textEdited.connect(lambda _t: setattr(self, "_id_touched", True))
        self.name.textChanged.connect(self._suggest_id)
        column.addWidget(_pair(field_block("Name", self.name),
                               field_block("ID", self.entry_id,
                                           "Set once; links and bookmarks use it." if self.is_new
                                           else "IDs cannot change after creation.")))
        second = {"disease": ("Scientific name", "scientific_name"),
                  "symptom": ("Scientific / clinical term", "scientific_name"),
                  "medicine": ("International generic name (INN)", "international_generic_name")}
        caption, key = second[self.kind]
        self.second_name = _line(d.get(key), "", 200)
        self.published = QCheckBox("Published (visible to users)")
        self.published.setChecked(d.get("is_published", True) is not False)
        column.addWidget(_pair(field_block(caption, self.second_name),
                               field_block("Visibility", self.published)))
        self._form.addWidget(box)

    def _suggest_id(self, name: str) -> None:
        if self.is_new and not self._id_touched:
            self.entry_id.setText(slug(name, self.kind))

    def _build_references(self) -> None:
        box, column = _section("Clinical references",
                               "Sources shown at the end of the entry. Tick Textbook for the "
                               "main textbook (shown first).")
        self.references = RowsTable(REFERENCE_COLUMNS, self._data.get("references") or [],
                                    "Add reference", stretch=(1,))
        column.addWidget(self.references)
        self.source = _line(self._data.get("source_attribution"),
                            "e.g. WHO 2024 guidelines; Harrison's 21st ed.", 300)
        column.addWidget(field_block("Source attribution (one line)", self.source))
        self._form.addWidget(box)

    # ------------------------------------------------------------- disease

    def _build_disease(self) -> None:
        d = self._data
        box, column = _section("Classification")
        self.body_system = _combo(self._systems, d.get("body_system_id") or "")
        self.severity = _combo([(s, s) for s in SEVERITIES], d.get("severity") or "Moderate")
        self.urgency = _combo(URGENCIES, d.get("urgency") or "")
        self.contagious = QCheckBox("Contagious")
        self.contagious.setChecked(bool(d.get("contagious")))
        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(10)
        grid.addWidget(field_block("Body system", self.body_system), 0, 0)
        grid.addWidget(field_block("Severity", self.severity), 0, 1)
        grid.addWidget(field_block("Urgency (triage)", self.urgency), 1, 0)
        grid.addWidget(field_block("Transmission", self.contagious), 1, 1)
        column.addLayout(grid)
        self.urgency_criteria = _text(d.get("urgency_criteria"),
                                      "The objective criteria behind the urgency level", 70)
        column.addWidget(field_block("Urgency criteria", self.urgency_criteria))
        self.tags = _line(", ".join(d.get("tags") or []), "comma separated, e.g. vector-borne, endemic", 300)
        column.addWidget(field_block("Tags", self.tags))
        self._form.addWidget(box)

        box, column = _section("Clinical text")
        self.description = _text(d.get("description"), "Plain-language clinical summary (required)", 110)
        self.onset = _text(d.get("onset_progression"), "How it starts and progresses", 80)
        self.patho = _text(d.get("pathophysiology"), "Mechanism of disease", 110)
        self.correlation = _text(d.get("clinicopathologic_correlation"),
                                 "How the mechanism explains the findings", 90)
        self.follow_up = _text(d.get("follow_up_monitoring"), "Monitoring plan", 80)
        for caption, widget in (("Clinical summary", self.description),
                                ("Onset & progression", self.onset),
                                ("Pathophysiology", self.patho),
                                ("Clinicopathologic correlation", self.correlation),
                                ("Follow-up & monitoring", self.follow_up)):
            column.addWidget(field_block(caption, widget))
        self._form.addWidget(box)

        box, column = _section("Lists", "One item per line. Blank lines are ignored.")
        self.lists: dict[str, LinesEdit] = {}
        pairs = [("causes", "Causes & etiology"), ("risk_factors", "Risk factors"),
                 ("recommended_tests", "Recommended tests"), ("treatments", "Treatments"),
                 ("home_care", "Home care"), ("emergency_signs", "Emergency red flags")]
        for index in range(0, len(pairs), 2):
            widgets = []
            for key, caption in pairs[index:index + 2]:
                self.lists[key] = LinesEdit(d.get(key) or [], caption)
                widgets.append(field_block(caption, self.lists[key]))
            column.addWidget(_pair(*widgets))
        self._form.addWidget(box)

        box, column = _section("Prevention", "One item per line, by tier.")
        by_tier: dict[str, list[str]] = {}
        for item in d.get("prevention") or []:
            by_tier.setdefault(item.get("tier") or "", []).append(item.get("content", ""))
        self.prevention: dict[str, LinesEdit] = {}
        widgets = []
        for tier, caption in PREVENTION_TIERS:
            self.prevention[tier] = LinesEdit(by_tier.get(tier, []), caption, 80)
            widgets.append(field_block(caption, self.prevention[tier]))
        column.addWidget(_pair(widgets[0], widgets[1]))
        column.addWidget(_pair(widgets[2], widgets[3]))
        self._form.addWidget(box)

        box, column = _section("Differential diagnosis")
        self.differentials = RowsTable(
            [("condition", "Condition", "text", None),
             ("distinguishing_feature", "Distinguishing feature", "text", None)],
            d.get("differentials") or [], "Add differential", stretch=(0, 1))
        column.addWidget(self.differentials)
        self._form.addWidget(box)

        box, column = _section("Symptoms",
                               "Cardinal (primary) symptoms weigh most in the Symptom Checker. "
                               "Intensity 1–10; weight multiplier 0.1–5.")
        self.symptom_links = RowsTable(
            [("symptom_id", "Symptom", "combo", self._symptoms),
             ("typical_intensity", "Intensity", "int", (1, 10)),
             ("is_primary", "Cardinal", "check", None),
             ("weight_multiplier", "Weight ×", "float", (0.1, 5.0))],
            d.get("symptoms") or [], "Add symptom")
        column.addWidget(self.symptom_links)
        self._form.addWidget(box)

        box, column = _section("Medicines", "Safety of each medicine for this condition.")
        self.medicine_links = RowsTable(
            [("medicine_id", "Medicine", "combo", self._medicines),
             ("safety", "Safety", "combo", SAFETY),
             ("note", "Note", "text", None)],
            d.get("medicines") or [], "Add medicine", stretch=(0, 2))
        column.addWidget(self.medicine_links)
        self._form.addWidget(box)

        box, column = _section("Related conditions")
        self.related = RowsTable([("id", "Condition", "combo", self._diseases)],
                                 [{"id": i} for i in d.get("related") or []], "Add related condition")
        column.addWidget(self.related)
        self._form.addWidget(box)

    # ------------------------------------------------------------- symptom

    def _build_symptom(self) -> None:
        d = self._data
        box, column = _section("Classification")
        self.body_system = _combo(self._systems, d.get("body_system_id") or "")
        self.red_flag = QCheckBox("Red-flag symptom (always warrants attention)")
        self.red_flag.setChecked(bool(d.get("is_red_flag")))
        self.weight = QSpinBox()
        self.weight.setObjectName("acInput")
        self.weight.setRange(1, 10)
        self.weight.setValue(int(d.get("diagnostic_weight") or 5))
        column.addWidget(_pair(field_block("Body system", self.body_system),
                               field_block("Diagnostic weight (1–10)", self.weight)))
        column.addWidget(self.red_flag)
        self.rationale = _text(d.get("weight_rationale"), "Why this weight", 70)
        column.addWidget(field_block("Weight rationale", self.rationale))
        self.tags = _line(", ".join(d.get("tags") or []), "comma separated", 300)
        column.addWidget(field_block("Tags", self.tags))
        self._form.addWidget(box)

        box, column = _section("Clinical text")
        self.description = _text(d.get("description"), "What the symptom is and how it presents", 110)
        column.addWidget(field_block("Description", self.description))
        self.lists = {"causes": LinesEdit(d.get("causes") or [], "Common causes"),
                      "red_flags": LinesEdit(d.get("red_flags") or [], "When it is an emergency")}
        column.addWidget(_pair(field_block("Causes (one per line)", self.lists["causes"]),
                               field_block("Red flags (one per line)", self.lists["red_flags"])))
        self._form.addWidget(box)

    # ------------------------------------------------------------ medicine

    def _build_medicine(self) -> None:
        d = self._data
        box, column = _section("Classification")
        self.generic = _line(d.get("generic_name"), "Local generic name", 200)
        self.trade = _line(d.get("trade_name"), "Best-known trade name", 200)
        self.drug_class = _line(d.get("drug_class"), "e.g. Analgesic / antipyretic", 200)
        self.category = _combo(CATEGORIES, d.get("category") or "Prescription")
        column.addWidget(_pair(field_block("Generic name", self.generic),
                               field_block("Trade name", self.trade)))
        column.addWidget(_pair(field_block("Drug class", self.drug_class),
                               field_block("Regulatory category", self.category)))
        self._form.addWidget(box)

        box, column = _section("Monograph")
        self.description = _text(d.get("description"), "What it is and how it works", 100)
        self.dosage = _text(d.get("dosage_text"), "Usual adult and paediatric dosing", 90)
        self.storage = _line(d.get("storage"), "e.g. Store below 30 °C", 300)
        self.black_box = _text(d.get("black_box_warning"), "Leave empty if none", 70)
        column.addWidget(field_block("Description", self.description))
        column.addWidget(field_block("Dosage", self.dosage))
        column.addWidget(field_block("Storage", self.storage))
        column.addWidget(field_block("Black box warning", self.black_box))
        self._form.addWidget(box)

        box, column = _section("Facts", "One item per line.")
        facts = d.get("facts") or {}
        self.lists = {}
        for index in range(0, len(MEDICINE_FACTS), 2):
            widgets = []
            for key, caption in MEDICINE_FACTS[index:index + 2]:
                self.lists[key] = LinesEdit(facts.get(key) or [], caption)
                widgets.append(field_block(caption, self.lists[key]))
            column.addWidget(_pair(*widgets))
        self._form.addWidget(box)

    # ------------------------------------------------------------ results

    def data(self) -> dict:
        common = {
            "id": self.entry_id.text().strip().lower(),
            "name": self.name.text().strip(),
            "is_published": self.published.isChecked(),
            "references": self.references.rows(),
            "source_attribution": self.source.text().strip(),
        }
        if self.kind == "disease":
            prevention = [{"tier": tier, "content": line}
                          for tier, edit in self.prevention.items() for line in edit.lines()]
            return {**common,
                    "scientific_name": self.second_name.text().strip(),
                    "body_system_id": self.body_system.currentData() or None,
                    "severity": self.severity.currentData(),
                    "urgency": self.urgency.currentData() or None,
                    "urgency_criteria": self.urgency_criteria.toPlainText().strip(),
                    "contagious": self.contagious.isChecked(),
                    "tags": [t.strip() for t in self.tags.text().split(",") if t.strip()],
                    "description": self.description.toPlainText().strip(),
                    "onset_progression": self.onset.toPlainText().strip(),
                    "pathophysiology": self.patho.toPlainText().strip(),
                    "clinicopathologic_correlation": self.correlation.toPlainText().strip(),
                    "follow_up_monitoring": self.follow_up.toPlainText().strip(),
                    **{key: edit.lines() for key, edit in self.lists.items()},
                    "prevention": prevention,
                    "differentials": self.differentials.rows(),
                    "symptoms": self.symptom_links.rows(),
                    "medicines": self.medicine_links.rows(),
                    "related": [r["id"] for r in self.related.rows() if r.get("id")]}
        if self.kind == "symptom":
            return {**common,
                    "scientific_name": self.second_name.text().strip(),
                    "body_system_id": self.body_system.currentData() or None,
                    "is_red_flag": self.red_flag.isChecked(),
                    "diagnostic_weight": self.weight.value(),
                    "weight_rationale": self.rationale.toPlainText().strip(),
                    "tags": [t.strip() for t in self.tags.text().split(",") if t.strip()],
                    "description": self.description.toPlainText().strip(),
                    **{key: edit.lines() for key, edit in self.lists.items()}}
        return {**common,
                "international_generic_name": self.second_name.text().strip(),
                "generic_name": self.generic.text().strip(),
                "trade_name": self.trade.text().strip(),
                "drug_class": self.drug_class.text().strip(),
                "category": self.category.currentData(),
                "description": self.description.toPlainText().strip(),
                "dosage_text": self.dosage.toPlainText().strip(),
                "storage": self.storage.text().strip(),
                "black_box_warning": self.black_box.toPlainText().strip(),
                "facts": {key: edit.lines() for key, edit in self.lists.items()}}

    def _snapshot(self) -> str:
        import json
        return json.dumps(self.data(), sort_keys=True, default=str)

    def is_dirty(self) -> bool:
        return self._snapshot() != self._saved

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self.data())

    # --------------------------------------------------- for the controller

    @property
    def busy(self) -> bool:
        return self._busy

    def set_busy(self, busy: bool) -> None:
        self._busy = busy
        for widget in self._busy_widgets:
            widget.setEnabled(not busy)
        self.setCursor(Qt.CursorShape.WaitCursor if busy else Qt.CursorShape.ArrowCursor)

    def show_error(self, message: str) -> None:
        self.set_busy(False)
        self.error.setText(message)
        self.error.setVisible(bool(message))

    def focus_first(self) -> None:
        self.name.setFocus()

    def refresh_theme(self) -> None:
        refresh_icons(self)


