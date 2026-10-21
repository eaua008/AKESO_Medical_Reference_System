"""Official decks (Content Management -> Decks, and Study Hub for educators).

    list      every official deck: status, subject, cards, author, updated
    editor    title, subject, description, the cards (add, edit, delete,
              move), Import CSV, Save draft; admins also Publish / Unpublish
    reports   cards students reported, with Resolve

Display only: StudyAdminController does the work."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox, QFrame, QHBoxLayout, QLineEdit, QScrollArea, QStackedWidget, QVBoxLayout, QWidget,
)

from app.models.study import Card, TYPE_LABELS
from app.ui.views.account.account_widgets import Banner, Card as Panel, button, label, pill
from app.ui.views.study.deck_page import card_preview
from app.ui.views.study.widgets import SUBJECT_NAMES, RowItem, clear_layout


class OfficialDecksView(QWidget):
    open_requested = Signal(str)                 # deck id ("" = new)
    reports_requested = Signal()
    back_requested = Signal()
    save_requested = Signal()
    publish_requested = Signal(bool)             # True publish, False unpublish
    delete_requested = Signal()
    add_card_requested = Signal()
    edit_card_requested = Signal(int)            # index in the editor's list
    delete_card_requested = Signal(int)
    move_card_requested = Signal(int, int)       # index, -1 up / +1 down
    import_requested = Signal()
    resolve_requested = Signal(str)              # report id

    def __init__(self, is_admin: bool) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.is_admin = is_admin
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        column = QVBoxLayout(page)
        column.setContentsMargins(56, 22, 30, 30)
        column.setSpacing(14)
        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        column.addWidget(self.banner)
        self.stack = QStackedWidget()
        column.addWidget(self.stack, 1)
        scroll.setWidget(page)
        outer.addWidget(scroll)

        # ---- list
        self.list_page = QWidget()
        self.list_page.setObjectName("panel")
        lp = QVBoxLayout(self.list_page)
        lp.setContentsMargins(0, 0, 0, 0)
        lp.setSpacing(12)
        head = QHBoxLayout()
        titles = QVBoxLayout()
        titles.addWidget(label("Official decks", "pageTitle", wrap=False))
        titles.addWidget(label("Educators save drafts; admins publish. Students see published decks "
                               "with the Official badge.", "pageSubtitle"))
        head.addLayout(titles, 1)
        self.reports_button = button("Reports", "acGhost", "flag", self.reports_requested.emit)
        head.addWidget(self.reports_button, 0, Qt.AlignmentFlag.AlignTop)
        head.addWidget(button("New official deck", "acPrimary", "plus", lambda: self.open_requested.emit("")),
                       0, Qt.AlignmentFlag.AlignTop)
        lp.addLayout(head)
        self._rows = QVBoxLayout()
        self._rows.setSpacing(6)
        lp.addLayout(self._rows)
        lp.addStretch(1)
        self.stack.addWidget(self.list_page)

        # ---- editor
        self.editor = QWidget()
        self.editor.setObjectName("panel")
        ed = QVBoxLayout(self.editor)
        ed.setContentsMargins(0, 0, 0, 0)
        ed.setSpacing(12)
        bar = QHBoxLayout()
        bar.addWidget(button("All official decks", "acLink", "arrow-left", self.back_requested.emit))
        bar.addStretch(1)
        self.status_pill = pill("", "acPill")
        bar.addWidget(self.status_pill)
        ed.addLayout(bar)
        self.title_edit = QLineEdit()
        self.title_edit.setObjectName("exComposerTitle")
        self.title_edit.setMaxLength(120)
        self.title_edit.setPlaceholderText("Deck title")
        ed.addWidget(self.title_edit)
        row = QHBoxLayout()
        row.setSpacing(8)
        self.subject = QComboBox()
        self.subject.setObjectName("acInput")
        self.subject.addItem("No subject", "")
        for key, name in SUBJECT_NAMES.items():
            self.subject.addItem(name, key)
        row.addWidget(self.subject)
        self.description = QLineEdit()
        self.description.setObjectName("acInput")
        self.description.setMaxLength(1000)
        self.description.setPlaceholderText("Short description (optional)")
        row.addWidget(self.description, 1)
        ed.addLayout(row)
        actions = QHBoxLayout()
        actions.setSpacing(8)
        actions.addWidget(button("Add card", "acGhost", "plus", self.add_card_requested.emit))
        actions.addWidget(button("Import CSV", "acGhost", "file-text", self.import_requested.emit))
        actions.addStretch(1)
        self.delete_button = button("Delete deck", "acDanger", "trash-2", self.delete_requested.emit)
        actions.addWidget(self.delete_button)
        self.save_button = button("Save draft", "acGhost", "check", self.save_requested.emit)
        actions.addWidget(self.save_button)
        self.publish_button = button("Publish", "acPrimary", "badge-check", lambda: self.publish_requested.emit(True))
        self.unpublish_button = button("Unpublish", "acGhost", "eye", lambda: self.publish_requested.emit(False))
        actions.addWidget(self.unpublish_button)
        actions.addWidget(self.publish_button)
        ed.addLayout(actions)
        self.cards_panel = Panel("Cards", "", "layers")
        self._card_rows = QVBoxLayout()
        self._card_rows.setSpacing(6)
        self.cards_panel.body.addLayout(self._card_rows)
        ed.addWidget(self.cards_panel)
        ed.addStretch(1)
        self.stack.addWidget(self.editor)

        # ---- reports
        self.reports_page = QWidget()
        self.reports_page.setObjectName("panel")
        rp = QVBoxLayout(self.reports_page)
        rp.setContentsMargins(0, 0, 0, 0)
        rp.setSpacing(10)
        rbar = QHBoxLayout()
        rbar.addWidget(button("All official decks", "acLink", "arrow-left", self.back_requested.emit))
        rbar.addStretch(1)
        rp.addLayout(rbar)
        rp.addWidget(label("Reported cards", "pageTitle", wrap=False))
        self._report_rows = QVBoxLayout()
        self._report_rows.setSpacing(6)
        rp.addLayout(self._report_rows)
        rp.addStretch(1)
        self.stack.addWidget(self.reports_page)

    # ------------------------------------------------------------------ list

    def show_list(self, decks: list[dict], open_reports: int) -> None:
        clear_layout(self._rows)
        self.reports_button.setText(f"  Reports ({open_reports})" if open_reports else "  Reports")
        if not decks:
            self._rows.addWidget(label("No official decks yet. Make the first one.", "acMuted"))
        for d in decks:
            status = "Published" if d.get("status") == "published" else "Draft"
            when = str(d.get("updated_at") or "")[:10]
            row = RowItem("badge-check" if status == "Published" else "pencil", d.get("title") or "Untitled",
                          f"{SUBJECT_NAMES.get(d.get('subject_id') or '', 'No subject')} · "
                          f"{d.get('card_count', 0)} cards · by {d.get('author') or 'unknown'} · {when}",
                          status, "stCountDue" if status == "Published" else "stCount")
            row.clicked.connect(lambda i=str(d.get("id")): self.open_requested.emit(i))
            self._rows.addWidget(row)
        self.stack.setCurrentWidget(self.list_page)

    # ---------------------------------------------------------------- editor

    def show_editor(self, deck: dict, cards: list[Card]) -> None:
        self.title_edit.setText(deck.get("title") or "")
        index = self.subject.findData(deck.get("subject_id") or "")
        self.subject.setCurrentIndex(max(0, index))
        self.description.setText(deck.get("description") or "")
        published = deck.get("status") == "published"
        is_new = not deck.get("id")
        self.status_pill.setText("Published" if published else ("New draft" if is_new else "Draft"))
        locked = published and not self.is_admin
        for widget in (self.title_edit, self.subject, self.description, self.save_button):
            widget.setEnabled(not locked)
        self.publish_button.setVisible(self.is_admin and not published and not is_new)
        self.unpublish_button.setVisible(self.is_admin and published)
        self.delete_button.setVisible(not is_new and (self.is_admin or not published))
        self.save_button.setText("  Save changes" if published else "  Save draft")
        if locked:
            self.banner.show_message("This deck is published. Ask an admin to unpublish it before editing.",
                                     "warn", "OK")
        self.show_cards(cards, editable=not locked)
        self.stack.setCurrentWidget(self.editor)

    def show_cards(self, cards: list[Card], editable: bool = True) -> None:
        clear_layout(self._card_rows)
        if not cards:
            self._card_rows.addWidget(label("No cards yet. Add one, or import a CSV file.", "acMuted"))
        for i, card in enumerate(cards):
            row = QFrame()
            row.setObjectName("stRow")
            line = QHBoxLayout(row)
            line.setContentsMargins(12, 8, 10, 8)
            line.setSpacing(8)
            line.addWidget(label(f"{i + 1}.", "stCount", wrap=False))
            text = card_preview(card)
            body = QVBoxLayout()
            body.setSpacing(1)
            body.addWidget(label(text[:160] + ("…" if len(text) > 160 else ""), "acRowTitle"))
            body.addWidget(label(TYPE_LABELS[card.type] + (f" · {', '.join(card.tags)}" if card.tags else ""),
                                 "acSmall"))
            line.addLayout(body, 1)
            if editable:
                line.addWidget(button("", "acGhost", "arrow-up", lambda _c=False, n=i: self.move_card_requested.emit(n, -1)))
                line.addWidget(button("", "acGhost", "arrow-down", lambda _c=False, n=i: self.move_card_requested.emit(n, 1)))
                line.addWidget(button("", "acGhost", "pencil", lambda _c=False, n=i: self.edit_card_requested.emit(n)))
                line.addWidget(button("", "acGhost", "trash-2", lambda _c=False, n=i: self.delete_card_requested.emit(n)))
            self._card_rows.addWidget(row)

    def editor_values(self) -> dict:
        return {"title": self.title_edit.text().strip(), "subject_id": self.subject.currentData() or "",
                "description": self.description.text().strip()}

    # --------------------------------------------------------------- reports

    def show_reports(self, reports: list[dict]) -> None:
        clear_layout(self._report_rows)
        if not reports:
            self._report_rows.addWidget(label("No open reports.", "acMuted"))
        for r in reports:
            ref = str(r.get("card_ref") or "")
            text = (r.get("front") or r.get("cloze_text") or ref)[:140]
            where = r.get("deck_title") or ("Auto card" if ref.startswith("auto:") else "Unknown deck")
            row = QFrame()
            row.setObjectName("stRow")
            line = QHBoxLayout(row)
            line.setContentsMargins(12, 8, 10, 8)
            body = QVBoxLayout()
            body.setSpacing(1)
            body.addWidget(label(text, "acRowTitle"))
            note = f" — “{r.get('note')}”" if r.get("note") else ""
            body.addWidget(label(f"{str(r.get('reason') or '').capitalize()} · {where}{note}", "acSmall"))
            line.addLayout(body, 1)
            line.addWidget(button("Resolve", "acGhost", "check",
                                  lambda _c=False, i=str(r.get("id")): self.resolve_requested.emit(i)))
            self._report_rows.addWidget(row)
        self.stack.setCurrentWidget(self.reports_page)

