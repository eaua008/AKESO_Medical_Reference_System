"""Official decks for educators and admins (migration 050's admin_* functions).

Educators save drafts; only admins publish, unpublish, or delete a published
deck (the database enforces this whatever the screen shows). Every request
runs in the background; server errors arrive already in plain words.
"""

from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QDialog, QFileDialog, QWidget

from app.core.background import call_in_background
from app.models.study import Card
from app.services.study.csv_import import parse_csv
from app.ui.views.account.account_dialogs import ConfirmDialog
from app.ui.views.study.card_editor import CardEditorDialog
from app.ui.views.study.official_decks_view import OfficialDecksView


class StudyAdminController(QObject):
    def __init__(self, remote, is_admin: bool, entry_names: Callable[[], list], sheet,
                 parent_widget: QWidget, on_published: Optional[Callable[[], None]] = None,
                 parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.remote = remote
        self.view = OfficialDecksView(is_admin)
        self.sheet = sheet
        sheet.set_content(self.view)
        sheet.close_requested.connect(sheet.close_sheet)                    # the X tab and Esc
        self._parent = parent_widget
        self._entries = entry_names
        self._on_published = on_published or (lambda: None)
        self._deck: dict = {}
        self._cards: list[Card] = []
        v = self.view
        v.open_requested.connect(self.open_deck)
        v.back_requested.connect(self.load_list)
        v.reports_requested.connect(self._reports)
        v.resolve_requested.connect(self._resolve)
        v.add_card_requested.connect(lambda: self._edit(-1))
        v.edit_card_requested.connect(self._edit)
        v.delete_card_requested.connect(self._delete_card)
        v.move_card_requested.connect(self._move)
        v.import_requested.connect(self._import)
        v.save_requested.connect(lambda: self._save())
        v.publish_requested.connect(self._publish)
        v.delete_requested.connect(self._delete_deck)

    # ---------------------------------------------------------------- list

    def open(self) -> None:
        self.load_list()
        if not self.sheet.is_open:
            self.sheet.open_sheet()

    def load_list(self) -> None:
        self.view.banner.hide()

        def load():
            decks = self.remote.admin_list_decks()
            try:
                reports = len(self.remote.admin_list_card_reports())
            except Exception:  # noqa: BLE001
                reports = 0
            return decks, reports

        call_in_background(load, lambda r: self.view.show_list(*r), self._error, owner=self.view)

    # -------------------------------------------------------------- editor

    def open_deck(self, deck_id: str) -> None:
        self.view.banner.hide()
        if not deck_id:
            self._deck, self._cards = {"title": "", "status": "draft"}, []
            self.view.show_editor(self._deck, self._cards)
            return

        def shown(data: dict) -> None:
            self._deck = data
            self._cards = [Card.from_row(c) for c in data.get("cards") or []]
            self.view.show_editor(self._deck, self._cards)

        call_in_background(lambda: self.remote.admin_get_deck(deck_id), shown, self._error, owner=self.view)

    def _edit(self, index: int) -> None:
        card = self._cards[index] if 0 <= index < len(self._cards) else Card("", self._deck.get("id") or "")
        dialog = CardEditorDialog(card, self._entries(), None, parent=self._parent)

        def save(value: Card) -> None:
            value.id = card.id
            if 0 <= index < len(self._cards):
                self._cards[index] = value
            else:
                self._cards.append(value)
            dialog.accept()

        dialog.saved.connect(save)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.view.show_cards(self._cards)

    def _delete_card(self, index: int) -> None:
        if 0 <= index < len(self._cards):
            del self._cards[index]
            self.view.show_cards(self._cards)

    def _move(self, index: int, step: int) -> None:
        other = index + step
        if 0 <= index < len(self._cards) and 0 <= other < len(self._cards):
            self._cards[index], self._cards[other] = self._cards[other], self._cards[index]
            self.view.show_cards(self._cards)

    def _import(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self._parent, "Import cards from CSV", "", "CSV files (*.csv)")
        if not path:
            return
        try:
            text = Path(path).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            self._error("That file couldn't be read. Save it as CSV (UTF-8) and try again.")
            return
        result = parse_csv(text, self._deck.get("id") or "")
        details = result.summary
        if result.errors:
            details += "\n\n" + "\n".join(result.errors[:10])
            if len(result.errors) > 10:
                details += f"\n…and {len(result.errors) - 10} more."
        if not result.cards:
            ConfirmDialog("Nothing to import", details, "OK", "file-text", parent=self._parent).exec()
            return
        dialog = ConfirmDialog("Import these cards?", details + "\n\nThey are added to the end of the deck; "
                               "nothing is saved until you press Save.", f"Add {len(result.cards)} cards",
                               "file-text", parent=self._parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._cards.extend(result.cards)
            self.view.show_cards(self._cards)

    def _payload(self) -> Optional[dict]:
        values = self.view.editor_values()
        if not values["title"]:
            self._error("Give the deck a title.")
            return None
        for n, card in enumerate(self._cards, start=1):
            problems = card.problems()
            if problems:
                self._error(f"Card {n}: {problems[0]}")
                return None
        payload = dict(values)
        if self._deck.get("id"):
            payload["id"] = self._deck["id"]
        rows = []
        for card in self._cards:
            row = card.to_row()
            row.pop("deck_id", None)
            if not card.id:
                row.pop("id", None)
            rows.append(row)
        payload["cards"] = rows
        return payload

    def _save(self, then: Optional[Callable[[str], None]] = None) -> None:
        payload = self._payload()
        if payload is None:
            return

        def saved(deck_id: str) -> None:
            self._deck["id"] = deck_id
            if then is not None:
                then(deck_id)
            else:
                self.view.banner.show_message("Saved.", "good", "OK")
                self.open_deck(deck_id)
                if self._deck.get("status") == "published":
                    self._on_published()

        call_in_background(lambda: self.remote.admin_save_deck(payload), saved, self._error, owner=self.view)

    def _publish(self, publish: bool) -> None:
        def set_status(deck_id: str) -> None:
            def done(_r) -> None:
                self.view.banner.show_message("Published: students see it at their next sync."
                                              if publish else "Unpublished: students no longer see it.",
                                              "good", "OK")
                self._on_published()
                self.open_deck(deck_id)
            call_in_background(lambda: self.remote.admin_set_deck_status(deck_id, "published" if publish else "draft"),
                               done, self._error, owner=self.view)

        if publish:
            self._save(then=set_status)             # publish exactly what is on screen
        else:
            set_status(self._deck.get("id"))

    def _delete_deck(self) -> None:
        deck_id = self._deck.get("id")
        if not deck_id:
            return
        dialog = ConfirmDialog("Delete this official deck?", "Students lose it at their next sync. "
                               "Their review history stays.", "Delete", "trash-2", danger=True,
                               parent=self._parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            call_in_background(lambda: self.remote.admin_delete_deck(deck_id),
                               lambda _r: (self._on_published(), self.load_list()), self._error,
                               owner=self.view)

    # ------------------------------------------------------------- reports

    def _reports(self) -> None:
        call_in_background(self.remote.admin_list_card_reports, self.view.show_reports, self._error,
                           owner=self.view)

    def _resolve(self, report_id: str) -> None:
        call_in_background(lambda: self.remote.admin_resolve_card_report(report_id),
                           lambda _r: self._reports(), self._error, owner=self.view)

    def _error(self, message: str) -> None:
        self.view.banner.show_message(message or "Something went wrong. Try again.", "danger", "Dismiss")
