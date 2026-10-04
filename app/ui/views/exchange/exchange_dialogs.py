"""Clinical Exchange forms: the full-page composer (new post / edit post)
and the dialogs to report, moderate, reveal the answer, edit a reply and
show a profile card."""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QButtonGroup, QCheckBox, QComboBox, QDoubleSpinBox, QHBoxLayout, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QRadioButton, QScrollArea, QSpinBox, QVBoxLayout, QWidget,
    QFrame,
)

from app.models.account import PROGRAM_LABELS, ROLE_LABELS, YEAR_LABELS, friendly_time
from app.models.exchange import (
    CASE, QUESTION, REPORT_REASONS, SETTINGS, TAG_KINDS, Draft, Poll, ProfileCard, Tag,
)
from app.services.case_reference import AGE_RANGES
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import (
    button, field_block, icon_label, label, pill, refresh_icons, repolish,
)
from app.ui.views.exchange.exchange_widgets import SearchPicker, clear_layout, flow, tag_chip


def _text_edit(placeholder: str, height: int) -> QPlainTextEdit:
    edit = QPlainTextEdit()
    edit.setObjectName("acInput")
    edit.setPlaceholderText(placeholder)
    edit.setFixedHeight(height)
    return edit


def _line(placeholder: str, maximum: int) -> QLineEdit:
    edit = QLineEdit()
    edit.setObjectName("acInput")
    edit.setPlaceholderText(placeholder)
    edit.setMaxLength(maximum)
    return edit


def _combo(items: list[tuple[str, object]]) -> QComboBox:
    combo = QComboBox()
    combo.setObjectName("acInput")
    for text, data in items:
        combo.addItem(text, data)
    return combo


COMPOSER_MAX_WIDTH = 860     # the form column; wider lines are hard to read


class ComposerPanel(QWidget):
    """New case / new question (and editing an existing post).

    A full-page form shown inside a PageSheet (app/ui/components/page_sheet.py).
    The controller listens to submitted / attach_requested / cancel_requested
    and answers with show_error(), set_busy() or fill().
    """

    submitted = Signal(object)               # Draft
    attach_requested = Signal(str)           # notebook item id
    cancel_requested = Signal()

    def __init__(self, draft: Draft, tags: list[Tag], diseases: list[tuple[str, str]],
                 notebook_cases: list[tuple[str, str]], checker, editing: bool = False,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("exComposer")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._draft = draft
        self._checker = checker
        self._editing = editing
        self._tags: list[Tag] = list(draft.tags)
        self._diseases = diseases
        self._busy_widgets: list[QWidget] = []
        self._busy = False

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
        # Extra left margin: the sheet's close tab sits over the top-left corner.
        centre.setContentsMargins(56, 26, 40, 30)
        column = QWidget()
        column.setObjectName("panel")
        column.setMaximumWidth(COMPOSER_MAX_WIDTH)
        self._form = QVBoxLayout(column)
        self._form.setContentsMargins(0, 0, 0, 0)
        self._form.setSpacing(14)
        centre.addStretch(1)
        centre.addWidget(column, 100)
        centre.addStretch(1)
        scroll.setWidget(page)
        outer.addWidget(scroll, 1)

        head = QHBoxLayout()
        head.setSpacing(12)
        head.addWidget(icon_label("message-circle", 26), 0, Qt.AlignmentFlag.AlignTop)
        titles = QVBoxLayout()
        titles.setSpacing(4)
        titles.addWidget(label("Edit post" if editing else "Share with Clinical Exchange",
                               "acTitle"))
        titles.addWidget(label("Every case is hypothetical: no names, exact ages, dates, "
                               "places or record numbers.", "acSubtitle"))
        head.addLayout(titles, 1)
        self._form.addLayout(head)
        self._form.addSpacing(4)

        # kind
        kind_row = QHBoxLayout()
        self._kind_group = QButtonGroup(self)
        self._case_radio = QRadioButton("Case discussion")
        self._question_radio = QRadioButton("Quick question")
        for radio in (self._case_radio, self._question_radio):
            self._kind_group.addButton(radio)
            kind_row.addWidget(radio)
            radio.toggled.connect(self._kind_changed)
            radio.setEnabled(not editing)
        kind_row.addStretch(1)
        self._form.addLayout(kind_row)

        # attach from notebook
        self._attach_box = QWidget()
        self._attach_box.setObjectName("panel")
        attach_row = QHBoxLayout(self._attach_box)
        attach_row.setContentsMargins(0, 0, 0, 0)
        self.attach = _combo([("Start from a saved notebook case…", None)]
                             + [(title, item_id) for item_id, title in notebook_cases])
        self.attach.currentIndexChanged.connect(self._attach_changed)
        attach_row.addWidget(self.attach, 1)
        self._attached = label(f"Filled from “{draft.attached_from}”"
                               if draft.attached_from else "", "acOk")
        attach_row.addWidget(self._attached)
        self._attach_box.setVisible(bool(notebook_cases) and not editing)
        self._form.addWidget(self._attach_box)

        self.title_edit = _line("A short title, e.g. “Febrile child with rash after a flood”", 140)
        self.title_edit.setText(draft.title)
        self._form.addWidget(field_block("Title", self.title_edit))

        # case details
        self._case_box = QWidget()
        self._case_box.setObjectName("panel")
        case = QVBoxLayout(self._case_box)
        case.setContentsMargins(0, 0, 0, 0)
        case.setSpacing(10)
        row = QHBoxLayout()
        row.setSpacing(10)
        self.age = _combo([("Age range", None)] + [(f"{name} years", name) for name, _l, _h in AGE_RANGES])
        self.sex = _combo([("Sex", None), ("Female", "female"), ("Male", "male")])
        self.setting = _combo([("Setting", None)] + [(s, s) for s in SETTINGS])
        for combo, value in ((self.age, draft.age_range), (self.sex, draft.sex),
                             (self.setting, draft.setting)):
            combo.setCurrentIndex(max(0, combo.findData(value)))
            row.addWidget(combo, 1)
        case.addWidget(field_block("Patient (de-identified)", self._row_widget(row),
                                   "An age range, never an exact age or birth date."))
        self.include_vitals = QCheckBox("Include vitals")
        case.addWidget(self.include_vitals)
        vitals = draft.vitals or {}
        vrow = QHBoxLayout()
        vrow.setSpacing(8)
        self.temp = self._spin(QDoubleSpinBox(), 30, 43, vitals.get("temperature", 37.0), " °C", 1)
        self.hr = self._spin(QSpinBox(), 20, 250, vitals.get("heart_rate", 75), " bpm")
        self.sys = self._spin(QSpinBox(), 50, 260, vitals.get("bp_systolic", 120), "")
        self.dia = self._spin(QSpinBox(), 30, 160, vitals.get("bp_diastolic", 80), "")
        self.rr = self._spin(QSpinBox(), 4, 60, vitals.get("resp_rate", 18), " /min")
        self.spo2 = self._spin(QSpinBox(), 50, 100, vitals.get("spo2", 98), " %")
        for caption, widget in (("Temp", self.temp), ("HR", self.hr), ("BP sys", self.sys),
                                ("BP dia", self.dia), ("RR", self.rr), ("SpO₂", self.spo2)):
            vrow.addWidget(field_block(caption, widget), 1)
        self._vitals_box = self._row_widget(vrow)
        case.addWidget(self._vitals_box)
        self.include_vitals.toggled.connect(self._vitals_box.setVisible)
        self.include_vitals.setChecked(bool(draft.vitals))
        self._vitals_box.setVisible(bool(draft.vitals))
        self._case_summary = label("", "acSmall")
        case.addWidget(self._case_summary)
        self._form.addWidget(self._case_box)

        self.body_edit = _text_edit("", 220)
        self.body_edit.setPlainText(draft.body)
        self._body_block = field_block("Case vignette", self.body_edit)
        self._form.addWidget(self._body_block)
        self.question_edit = _line("What do you want others to answer?", 500)
        self.question_edit.setText(draft.question)
        self._question_block = field_block("Your question", self.question_edit)
        self._form.addWidget(self._question_block)

        # tags
        self.tag_picker = SearchPicker("Add a tag: disease, symptom, medicine or body system")
        self.tag_picker.set_items([(f"{t.label}  ·  {TAG_KINDS.get(t.kind, t.kind)}", t) for t in tags])
        self.tag_picker.activated.connect(lambda _i: self._add_tag())
        self._tag_chips = QVBoxLayout()
        tag_holder = QWidget()
        tag_holder.setObjectName("panel")
        tag_col = QVBoxLayout(tag_holder)
        tag_col.setContentsMargins(0, 0, 0, 0)
        tag_col.addWidget(self.tag_picker)
        tag_col.addLayout(self._tag_chips)
        self._form.addWidget(field_block("Tags", tag_holder, "Tags help others find your post."))

        # poll
        self._poll_box = QWidget()
        self._poll_box.setObjectName("panel")
        poll = QVBoxLayout(self._poll_box)
        poll.setContentsMargins(0, 0, 0, 0)
        poll.setSpacing(8)
        self.add_poll = QCheckBox("Add a differential poll (others vote and can suggest more)")
        poll.addWidget(self.add_poll)
        self._poll_inner = QWidget()
        self._poll_inner.setObjectName("panel")
        inner = QVBoxLayout(self._poll_inner)
        inner.setContentsMargins(0, 0, 0, 0)
        add_row = QHBoxLayout()
        self.option_picker = SearchPicker("Pick a disease or type a diagnosis", editable_text=True)
        self.option_picker.set_items([(name, disease_id) for disease_id, name in diseases])
        add_row.addWidget(self.option_picker, 1)
        add_row.addWidget(button("Add choice", "acGhost", "plus", self._add_option))
        inner.addLayout(add_row)
        self._options = QVBoxLayout()
        self._options.setSpacing(4)
        inner.addLayout(self._options)
        inner.addWidget(label("2–8 choices. Keep the intended answer to yourself; you "
                              "reveal it later with an explanation.", "acSmall"))
        poll.addWidget(self._poll_inner)
        self.add_poll.toggled.connect(self._poll_inner.setVisible)
        self._poll_options = list(draft.poll_options)
        self.add_poll.setChecked(bool(self._poll_options))
        self._poll_inner.setVisible(bool(self._poll_options))
        self._poll_box.setVisible(not editing)
        self._form.addWidget(self._poll_box)

        self.anonymous = QCheckBox("Post anonymously (moderators can still see who posted)")
        self.anonymous.setChecked(draft.anonymous)
        self.anonymous.setVisible(not editing)
        self._form.addWidget(self.anonymous)
        self._form.addStretch(1)

        for widget in (self.title_edit, self.question_edit):
            widget.textChanged.connect(self._check)
        self.body_edit.textChanged.connect(self._check)

        # Footer: always visible under the scrolling form.
        foot = QFrame()
        foot.setObjectName("exComposerFoot")
        foot_row = QHBoxLayout(foot)
        foot_row.setContentsMargins(56, 12, 40, 12)
        foot_row.setSpacing(10)
        self.error = label("", "acError")
        self.error.hide()
        foot_row.addWidget(self.error, 1)
        foot_row.addStretch(0)
        cancel = button("Cancel", "acGhost", on_click=self.cancel_requested.emit)
        self._go = button("Save changes" if editing else "Post", "acPrimary", "check",
                          self._submit)
        for widget in (cancel, self._go):
            foot_row.addWidget(widget)
            self._busy_widgets.append(widget)
        outer.addWidget(foot)

        (self._case_radio if draft.kind == CASE else self._question_radio).setChecked(True)
        self._kind_changed()
        self._draw_tags()
        self._draw_options()
        self._draw_case_summary()
        self._saved = self._snapshot()

    # ------------------------------------------------------------ for the controller

    def show_error(self, message: str) -> None:
        self.set_busy(False)
        self.error.setText(message)
        self.error.setVisible(bool(message))

    @property
    def busy(self) -> bool:
        return self._busy

    def set_busy(self, busy: bool) -> None:
        self._busy = busy
        for widget in self._busy_widgets:
            widget.setEnabled(not busy)
        if not busy:
            self._check()
        self.setCursor(Qt.CursorShape.WaitCursor if busy else Qt.CursorShape.ArrowCursor)

    def is_dirty(self) -> bool:
        """Has the user typed or picked anything since the form opened?"""
        return self._snapshot() != self._saved

    def focus_first(self) -> None:
        (self.title_edit if not self.title_edit.text() else self.body_edit).setFocus()

    def refresh_theme(self) -> None:
        refresh_icons(self)

    def _snapshot(self) -> tuple:
        return (self.title_edit.text(), self.body_edit.toPlainText(), self.question_edit.text(),
                tuple((t.kind, t.id) for t in self._tags),
                tuple(o["label"] for o in self._poll_options),
                self.age.currentIndex(), self.sex.currentIndex(), self.setting.currentIndex())

    # --------------------------------------------------------------- bits

    @staticmethod
    def _row_widget(row: QHBoxLayout) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        row.setContentsMargins(0, 0, 0, 0)
        holder.setLayout(row)
        return holder

    @staticmethod
    def _spin(widget, low, high, value, suffix, decimals: int = 0):
        widget.setObjectName("acInput")
        widget.setRange(low, high)
        if decimals:
            widget.setDecimals(decimals)
            widget.setSingleStep(0.1)
        widget.setValue(value)
        widget.setSuffix(suffix)
        return widget

    def _kind_changed(self, *_args) -> None:
        is_case = self._case_radio.isChecked()
        self._case_box.setVisible(is_case)
        self._question_block.setVisible(is_case)
        self._poll_box.setVisible(is_case and not self._editing)
        self._attach_box.setVisible(is_case and not self._editing and self.attach.count() > 1)
        caption = self._body_block.findChild(QLabel)
        if caption is not None:
            caption.setText("CASE VIGNETTE" if is_case else "YOUR QUESTION")
        self.body_edit.setPlaceholderText(
            "Describe the hypothetical patient: presenting complaint, history, findings…"
            if is_case else "Ask anything, e.g. “How do I tell dengue from chikungunya at the bedside?”")

    def _attach_changed(self, _index: int) -> None:
        item_id = self.attach.currentData()
        if item_id:
            self.attach_requested.emit(item_id)

    def fill(self, draft: Draft) -> None:
        """Called with a draft made from a notebook case."""
        self._draft = draft
        self.title_edit.setText(draft.title)
        self.body_edit.setPlainText(draft.body)
        self.question_edit.setText(draft.question)
        for combo, value in ((self.age, draft.age_range), (self.sex, draft.sex),
                             (self.setting, draft.setting)):
            combo.setCurrentIndex(max(0, combo.findData(value)))
        if draft.vitals:
            v = draft.vitals
            self.temp.setValue(float(v.get("temperature", 37.0)))
            self.hr.setValue(int(v.get("heart_rate", 75)))
            self.sys.setValue(int(v.get("bp_systolic", 120)))
            self.dia.setValue(int(v.get("bp_diastolic", 80)))
            self.rr.setValue(int(v.get("resp_rate", 18)))
            self.spo2.setValue(int(v.get("spo2", 98)))
        self.include_vitals.setChecked(bool(draft.vitals))
        for tag in draft.tags:
            if all((t.kind, t.id) != (tag.kind, tag.id) for t in self._tags):
                self._tags.append(tag)
        self._attached.setText(f"Filled from “{draft.attached_from}”")
        self._draw_tags()
        self._draw_case_summary()

    def _draw_case_summary(self) -> None:
        data = self._draft.case_data or {}
        parts = []
        if data.get("symptoms"):
            parts.append("Symptoms: " + ", ".join(
                f"{s.get('name')} {s.get('intensity', '')}/10" for s in data["symptoms"]))
        if data.get("candidate"):
            parts.append("Medicines: " + ", ".join(
                [data["candidate"].get("name", "")] + [r.get("name", "") for r in data.get("regimen", [])]))
        if data.get("comorbidities") or data.get("conditions"):
            parts.append("Conditions: " + ", ".join(data.get("comorbidities") or data.get("conditions")))
        self._case_summary.setText("Attached from the checker — " + "; ".join(parts) if parts else "")
        self._case_summary.setVisible(bool(parts))

    def _add_tag(self) -> None:
        tag, _text = self.tag_picker.chosen()
        if tag and all((t.kind, t.id) != (tag.kind, tag.id) for t in self._tags):
            self._tags.append(tag)
            self._draw_tags()
        self.tag_picker.reset()

    def _draw_tags(self) -> None:
        clear_layout(self._tag_chips)
        chips = []
        for tag in self._tags:
            chip = tag_chip(tag)
            chip.setText(f"{tag.label.replace('&', '&&')}  ✕")
            chip.setToolTip("Remove this tag")
            chip.clicked.connect(lambda _c=False, t=tag: self._remove_tag(t))
            chips.append(chip)
        if chips:
            self._tag_chips.addWidget(flow(chips))

    def _remove_tag(self, tag: Tag) -> None:
        self._tags = [t for t in self._tags if (t.kind, t.id) != (tag.kind, tag.id)]
        self._draw_tags()

    def _add_option(self) -> None:
        disease_id, text = self.option_picker.chosen()
        text = " ".join(text.split())
        if not text:
            return
        key = disease_id or text.lower()
        if any((o.get("disease_id") or o["label"].lower()) == key for o in self._poll_options):
            self.option_picker.reset()
            return
        if len(self._poll_options) >= 8:
            self.show_error("A poll can start with at most 8 choices.")
            return
        self._poll_options.append({"disease_id": disease_id, "label": text})
        self.option_picker.reset()
        self._draw_options()

    def _draw_options(self) -> None:
        clear_layout(self._options)
        for index, option in enumerate(self._poll_options):
            row = QHBoxLayout()
            row.addWidget(label(f"{index + 1}. {option['label']}", "acValue"), 1)
            if option.get("disease_id"):
                row.addWidget(pill("Linked", "acPill"))
            remove = button("Remove", "acLink",
                            on_click=lambda i=index: self._remove_option(i))
            row.addWidget(remove)
            holder = QWidget()
            holder.setObjectName("panel")
            row.setContentsMargins(0, 0, 0, 0)
            holder.setLayout(row)
            self._options.addWidget(holder)

    def _remove_option(self, index: int) -> None:
        del self._poll_options[index]
        self._draw_options()

    def _check(self) -> None:
        message = self._checker(self.title_edit.text(), self.body_edit.toPlainText(),
                                self.question_edit.text())
        if message:
            self.show_error(message)
        else:
            self.error.hide()
        self._go.setEnabled(not message)

    def _submit(self) -> None:
        is_case = self._case_radio.isChecked()
        draft = Draft(
            kind=CASE if is_case else QUESTION,
            title=self.title_edit.text(), body=self.body_edit.toPlainText(),
            question=self.question_edit.text() if is_case else "",
            anonymous=self.anonymous.isChecked(),
            age_range=self.age.currentData() if is_case else None,
            sex=self.sex.currentData() if is_case else None,
            setting=self.setting.currentData() if is_case else None,
            vitals={"temperature": round(self.temp.value(), 1), "heart_rate": self.hr.value(),
                    "bp_systolic": self.sys.value(), "bp_diastolic": self.dia.value(),
                    "resp_rate": self.rr.value(), "spo2": self.spo2.value()}
            if is_case and self.include_vitals.isChecked() else None,
            case_data=self._draft.case_data if is_case else {},
            source=self._draft.source if is_case else None,
            tags=list(self._tags),
            poll_options=list(self._poll_options) if is_case and self.add_poll.isChecked() else [],
        )
        self.set_busy(True)
        self.submitted.emit(draft)


class ReportDialog(AccountDialog):
    submitted = Signal(str, str)

    def __init__(self, what: str, parent: Optional[QWidget] = None,
                 reasons: Optional[list] = None) -> None:
        super().__init__(f"Report this {what}", "Moderators (educators and admins) will "
                         "review it. The " + ("person" if what == "profile" else "author")
                         + " isn't told who reported.", "flag", parent)
        self._group = QButtonGroup(self)
        for index, (key, text) in enumerate(reasons or REPORT_REASONS):
            radio = QRadioButton(text)
            radio.setProperty("reason", key)
            radio.setChecked(index == 0)
            self._group.addButton(radio)
            self.body.addWidget(radio)
        self.note = _text_edit("Anything moderators should know (optional)", 70)
        self.body.addWidget(self.note)
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Send report", "acDanger", "flag", self._submit)

    def _submit(self) -> None:
        reason = self._group.checkedButton().property("reason")
        self.set_busy(True)
        self.submitted.emit(reason, self.note.toPlainText()[:500])


class ModerateDialog(AccountDialog):
    submitted = Signal(str, str)

    def __init__(self, what: str, status: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(f"Moderate this {what}", "The author is notified (without your name) "
                         "and the action is logged.", "shield-alert", parent)
        actions = [("hide", "Hide (only the author and admins can see it)"),
                   ("remove", "Remove (only the author and admins can see it)")]
        if what == "profile":
            actions = [("make_private", "Make the profile private"),
                       ("clear_bio", "Clear the bio")]
        if what == "post":
            actions.insert(1, ("lock", "Lock (no new replies or votes)"))
        if status == "hidden":
            actions.insert(0, ("unhide", "Show it again"))
        if status == "locked":
            actions.insert(0, ("unlock", "Unlock"))
        self.action = _combo([(text, key) for key, text in actions])
        self.body.addWidget(field_block("Action", self.action))
        self.reason = _line("Reason shown to the author, e.g. “Contains a full date of birth”", 300)
        self.body.addWidget(field_block("Reason", self.reason))
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Apply", "acDanger", "shield-alert", self._submit)

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self.action.currentData(), self.reason.text())


class RevealDialog(AccountDialog):
    submitted = Signal(str, str)

    def __init__(self, poll: Poll, parent: Optional[QWidget] = None) -> None:
        super().__init__("Reveal the intended answer", "Everyone who voted or follows the "
                         "case is notified. Voting closes.", "sparkles", parent)
        self.option = _combo([(o.label, o.id) for o in poll.options])
        self.body.addWidget(field_block("Intended answer", self.option))
        self.explanation = _text_edit("Why this is the answer: the key findings, and what rules "
                                      "out the others", 120)
        self.body.addWidget(field_block("Explanation", self.explanation))
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Reveal", "acPrimary", "sparkles", self._submit)

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self.option.currentData(), self.explanation.toPlainText())


class EditReplyDialog(AccountDialog):
    submitted = Signal(str)

    def __init__(self, body: str, parent: Optional[QWidget] = None) -> None:
        super().__init__("Edit reply", "", "pencil", parent)
        self.text = _text_edit("", 140)
        self.text.setPlainText(body)
        self.body.addWidget(self.text)
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Save", "acPrimary", "check", self._submit)

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self.text.toPlainText())


class ProfileCardDialog(AccountDialog):
    def __init__(self, card: ProfileCard, avatar: QPixmap, parent: Optional[QWidget] = None) -> None:
        super().__init__(card.display_name or f"@{card.handle}", "", "", parent, width=400)
        top = QHBoxLayout()
        picture = QLabel()
        picture.setObjectName("panel")
        picture.setFixedSize(64, 64)
        picture.setPixmap(avatar)
        top.addWidget(picture)
        text = QVBoxLayout()
        text.addWidget(label(f"@{card.handle}", "acMuted"))
        bits = [PROGRAM_LABELS.get(card.program or "", ""), YEAR_LABELS.get(card.year_level or 0, ""),
                card.school or ""]
        line = " · ".join(b for b in bits if b)
        if line:
            text.addWidget(label(line, "acSmall"))
        badges = []
        if card.role in ("educator", "admin"):
            badges.append(pill(ROLE_LABELS[card.role], "acPillGood"))
        if card.verified_domain:
            badges.append(pill(f"Verified student · {card.verified_domain}", "acPillGood"))
        if badges:
            text.addWidget(flow(badges))
        top.addLayout(text, 1)
        self.body.addLayout(top)
        if card.bio:
            self.body.addWidget(label(card.bio, "exBody"))
        stats = QHBoxLayout()
        for number, caption in ((card.posts, "posts"), (card.replies, "replies"),
                                (card.best_answers, "best answers"),
                                (card.verified_answers, "verified")):
            box = QVBoxLayout()
            box.addWidget(label(str(number), "acStatNumber", wrap=False))
            box.addWidget(label(caption, "acStatLabel", wrap=False))
            stats.addLayout(box)
        self.body.addLayout(stats)
        if card.member_since:
            self.body.addWidget(label(f"Member since {friendly_time(card.member_since, False)}",
                                      "acSmall"))
        self.add_button("Close", "acPrimary", on_click=self.accept, default=True)


__all__ = ["ComposerPanel", "ReportDialog", "ModerateDialog", "RevealDialog",
           "EditReplyDialog", "ProfileCardDialog", "repolish", "QPushButton"]
