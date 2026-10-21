"""Study Hub: wires the screens to StudyService.

    Today / Decks tabs        counts, deck tiles, weak cards
    deck page (sheet)         browse a deck; rename, add, edit, delete
    review (sheet)            one session: rate, undo, edit, report, summary
    "Make a flashcard"        from text selected on an encyclopedia page or
                              in a note: the card editor, pre-filled
    the sidebar badge         cards due today

The views only draw and emit; nothing here talks to Supabase except the
card report (through the repository) and StudySyncController.
"""

from datetime import datetime, timezone
from typing import Callable, Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QDialog

from app.core.background import call_in_background
from app.models.study import Card, Origin, Rating
from app.services.study.study_service import StudyService
from app.ui.views.account.account_dialogs import ConfirmDialog, NoticeDialog
from app.ui.views.study.card_editor import CardEditorDialog
from app.ui.views.study.deck_page import DeckPage
from app.ui.views.study.review_view import ReviewView
from app.ui.views.study.study_dialogs import NewDeckDialog, ReportCardDialog, StudySettingsDialog
from app.ui.views.study.study_hub_page import StudyHubPage


class _Session:
    def __init__(self, scope: Optional[str], keys: Optional[list[str]], title: str) -> None:
        self.scope = scope                    # deck id, or None for Today
        self.keys = keys                      # a fixed list ("Review these"), shown once each
        self.title = title
        self.done: list[str] = []
        self.undo: list = []
        self.started = datetime.now(timezone.utc)
        self.current: Optional[str] = None
        self.shown_at = datetime.now(timezone.utc)
        self.difficulties: Optional[list] = None   # None: the Study settings filters
        self.families: Optional[list] = None


class StudyHubController(QObject):
    due_changed = Signal(int)

    def __init__(self, page: StudyHubPage, service: StudyService, deck_sheet, review_sheet,
                 inspect: Callable[[str, str], None], remote=None, staff: bool = False,
                 entry_names: Optional[Callable[[], list]] = None,
                 open_staff_editor: Optional[Callable[[], None]] = None,
                 parent: Optional[QObject] = None) -> None:
        super().__init__(parent or page)
        self.page = page
        self.service = service
        self.remote = remote
        self.sync = None                      # StudySyncController, set by the shell
        # Show a sheet over whatever tab is showing (set by the shell)
        self.lend_sheet: Callable = lambda _sheet: None
        self._inspect = inspect
        self._entry_names = entry_names or (lambda: [])
        self._open_staff_editor = open_staff_editor
        self._session: Optional[_Session] = None

        self.deck_page = DeckPage()
        self.deck_sheet = deck_sheet
        deck_sheet.set_content(self.deck_page)
        deck_sheet.close_requested.connect(deck_sheet.close_sheet)          # the X tab and Esc
        self.review = ReviewView()
        self.review_sheet = review_sheet
        review_sheet.set_content(self.review)
        review_sheet.close_requested.connect(self._end)
        review_sheet.closed.connect(self._session_closed)

        page.settings_requested.connect(self._settings)
        page.sync_requested.connect(lambda: self.sync and self.sync.sync_now())
        page.tab_changed.connect(lambda _k: self.refresh())
        today = page.today
        today.start_requested.connect(lambda: self.study(None))
        today.deck_requested.connect(self.study)
        today.weak_requested.connect(lambda keys: self.study(None, keys, "Weak cards"))
        today.browse_requested.connect(lambda: page.open_tab("decks"))
        today.subject_requested.connect(self._show_subject)
        decks = page.decks
        decks.open_requested.connect(self.open_deck)
        decks.study_requested.connect(self.study)
        decks.new_requested.connect(self._new_deck)
        decks.set_staff(staff and open_staff_editor is not None)
        decks.staff_requested.connect(lambda: self._open_staff_editor and self._open_staff_editor())

        dp = self.deck_page
        dp.study_requested.connect(lambda d: self.study(d, difficulties=dp.difficulties(),
                                                        families=dp.families()))
        dp.rename_requested.connect(self._rename)
        dp.delete_requested.connect(self._delete_deck)
        dp.reset_requested.connect(self._reset_deck)
        dp.add_card_requested.connect(lambda d: self.edit_card(Card("", d)))
        dp.edit_card_requested.connect(self._edit_card_id)
        dp.delete_card_requested.connect(self._delete_card)

        rv = self.review
        rv.rated.connect(self._rated)
        rv.undo_requested.connect(self._undo)
        rv.edit_requested.connect(self._edit_current)
        rv.report_requested.connect(self._report_current)
        rv.open_entry.connect(self._inspect)
        rv.end_requested.connect(self._end)
        rv.again_requested.connect(self._again)

    # -------------------------------------------------------------- drawing

    def refresh(self) -> None:
        summaries = self.service.summaries()
        due, new = self.service.due_today()
        first_time = not any(s.started for s in summaries) and not self.service.local.reviews()
        self.page.today.show_today(due, new, self.service.streak(), summaries,
                                   self.service.weak_cards(), first_time,
                                   reviewed=self.service.reviewed_today(),
                                   seconds_per_card=self.service.seconds_per_card(),
                                   forecast=self.service.forecast(7),
                                   hour=datetime.now().hour)
        self.page.decks.show_decks(summaries)
        self.due_changed.emit(due)
        if self.deck_sheet.is_open and self.deck_page.deck_id:
            self.open_deck(self.deck_page.deck_id, reopen=False)

    def _show_subject(self, subject: str) -> None:
        self.page.open_tab("decks")
        self.page.decks.set_subject(subject)

    def due_count(self) -> int:
        return self.service.due_today()[0]

    def open_deck(self, deck_id: str, reopen: bool = True) -> None:
        summary = self.service.summary(deck_id)
        if summary is None:
            if self.deck_sheet.is_open:
                self.deck_sheet.close_sheet()
            return
        self.deck_page.show_deck(summary, self.service.cards(deck_id), self.service.local.states())
        if reopen and not self.deck_sheet.is_open:
            self.lend_sheet(self.deck_sheet)
            self.deck_sheet.open_sheet()

    def open_card(self, card_id: str) -> None:
        card = self.service.card(card_id)
        if card is not None:
            self.open_deck(card.deck_id)

    def entry_deck(self, kind: str, entry_id: str, name: str) -> bool:
        """"Study {name} cards" on an encyclopedia page. False when it has none."""
        deck = self.service.entry_deck(kind, entry_id, name)
        if deck is None:
            return False
        self.study(deck.id)
        return True

    # ------------------------------------------------------------- sessions

    def study(self, deck_id: Optional[str], keys: Optional[list[str]] = None, title: str = "",
              difficulties: Optional[list] = None, families: Optional[list] = None) -> None:
        if deck_id is not None:
            deck = self.service.deck(deck_id)
            title = deck.title if deck else "Deck"
        self._session = _Session(deck_id, list(keys) if keys else None, title or "Today's review")
        self._session.difficulties, self._session.families = difficulties, families
        self.review.type_answer = self.service.settings().type_answer
        if self.sync is not None:
            self.sync.reviewing = True
        if self.deck_sheet.is_open:
            self.deck_sheet.close_sheet()
        self._next()
        if not self.review_sheet.is_open:
            self.lend_sheet(self.review_sheet)
            self.review_sheet.open_sheet()
        self.review_sheet.raise_()
        self.review_sheet.tab.raise_()
        self.review.setFocus()

    def _remaining(self) -> tuple[Optional[str], int]:
        s = self._session
        if s.keys is not None:
            left = [k for k in s.keys if k not in s.done]
            return (left[0] if left else None), len(left)
        queue = self.service.queue(s.scope, difficulties=s.difficulties, families=s.families)
        return self.service.next_key(queue), queue.total

    def _next(self) -> None:
        s = self._session
        while True:
            key, left = self._remaining()
            card = self.service.card(key) if key else None
            if key and card is None:          # an auto card whose entry is gone: skip it
                s.done.append(key)
                continue
            break
        if card is None:
            self._summary()
            return
        s.current = key
        s.shown_at = datetime.now(timezone.utc)
        self._show(card, key, len(s.done) + left)

    def _show(self, card: Card, key: str, total: int) -> None:
        s = self._session
        deck = self.service.deck(card.deck_id)
        origin = deck.origin if deck else Origin.AUTO
        self.review.show_card(card, s.title, len(s.done) + 1, total,
                              self.service.preview(key), can_edit=origin == Origin.PERSONAL,
                              can_report=origin in (Origin.OFFICIAL, Origin.AUTO),
                              can_undo=bool(s.undo), entry_name=self._entry_name(card),
                              updated=self.service.is_updated(card),
                              subject_id=(deck.subject_id or "") if deck else "")

    def _entry_name(self, card: Card) -> str:
        if not (card.source_kind and card.source_id):
            return ""
        for text, ref in self._entry_names():
            if ref == (card.source_kind, card.source_id):
                return text.split(" · ")[0]
        return ""

    def _rated(self, rating: int) -> None:
        s = self._session
        if s is None or s.current is None:
            return
        elapsed = (datetime.now(timezone.utc) - s.shown_at).total_seconds() * 1000
        s.undo.append((s.current, self.service.answer(s.current, Rating(rating), int(elapsed),
                                                      hinted=self.review.hinted)))
        s.done.append(s.current)
        self._next()

    def _undo(self) -> None:
        s = self._session
        if s is None or not s.undo:
            return
        key, token = s.undo.pop()
        self.service.undo(token)
        if s.done and s.done[-1] == key:
            s.done.pop()
        s.current = key
        card = self.service.card(key)
        if card is not None:
            _next, left = self._remaining()
            s.shown_at = datetime.now(timezone.utc)
            self._show(card, key, max(left, 1) + len(s.done))

    def _summary(self) -> None:
        s = self._session
        stats = self.service.session_stats(s.started)
        states = self.service.local.states()
        upcoming = sorted(st.due for st in states.values() if st.due and st.due > datetime.now(timezone.utc))
        if upcoming:
            when = upcoming[0].astimezone()
            next_due = f"Next card due {when.strftime('%a %b %d, %I:%M %p').replace(' 0', ' ')}"
        else:
            next_due = "No cards scheduled yet."
        if not stats["reviewed"]:
            next_due = "Nothing to review here right now. " + next_due
        self.review.show_summary(stats["reviewed"], stats["correct"], stats["seconds"], next_due)

    def _again(self) -> None:
        s = self._session
        if s is not None:
            self.study(s.scope, None, s.title)

    def _end(self) -> None:
        if self.review_sheet.is_open:
            self.review_sheet.close_sheet()
        else:
            self._session_closed()

    def _session_closed(self) -> None:
        if self._session is None:
            return
        self._session = None
        if self.sync is not None:
            self.sync.reviewing = False
            self.sync.sync_now()               # after a review session
        self.refresh()

    # ------------------------------------------------------------- editing

    def _edit_current(self) -> None:
        s = self._session
        if s is None or s.current is None:
            return
        card = self.service.card(s.current)
        if card is not None:
            self.edit_card(card, after=lambda: self._next())

    def _edit_card_id(self, card_id: str) -> None:
        card = self.service.card(card_id)
        if card is not None:
            self.edit_card(card)

    def edit_card(self, card: Card, after: Optional[Callable[[], None]] = None,
                  pick_deck: bool = False) -> None:
        decks = self.service.own_decks() if pick_deck else None
        if pick_deck and not card.deck_id:
            card.deck_id = self.service.my_cards_deck().id
            decks = self.service.own_decks()
        dialog = CardEditorDialog(card, self._entry_names(), decks, parent=self.page)

        def save(value: Card) -> None:
            deck_id, name = dialog.chosen_deck()
            if deck_id is None:
                deck_id = self.service.create_deck(name).id
            value.deck_id = deck_id
            try:
                self.service.save_card(value)
            except ValueError as exc:
                dialog.show_error(str(exc))
                return
            dialog.accept()

        dialog.saved.connect(save)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh()
            if after is not None:
                after()

    def make_flashcard(self, text: str, kind: str = "", entry_id: str = "") -> None:
        """Text selected on a page -> a new card (back = the text)."""
        card = Card("", "", back=(text or "").strip()[:2000])
        if kind in ("disease", "symptom", "medicine", "article") and entry_id:
            card.source_kind, card.source_id = kind, entry_id
        self.edit_card(card, pick_deck=True)

    def _delete_card(self, card_id: str) -> None:
        if self._confirm("Delete this card?", "It is removed from the deck on every computer.", "Delete"):
            self.service.delete_card(card_id)
            self.refresh()

    # --------------------------------------------------------------- decks

    def _new_deck(self) -> None:
        dialog = NewDeckDialog(self.page)

        def create(title: str, subject: str, description: str) -> None:
            deck = self.service.create_deck(title, subject, description)
            dialog.accept()
            self.refresh()
            self.open_deck(deck.id)

        dialog.submitted.connect(create)
        dialog.exec()

    def _rename(self, deck_id: str, title: str) -> None:
        self.service.rename_deck(deck_id, title)
        self.page.decks.show_decks(self.service.summaries())

    def _delete_deck(self, deck_id: str) -> None:
        deck = self.service.deck(deck_id)
        if deck and self._confirm(f"Delete “{deck.title}”?",
                                  "The deck and its cards are removed on every computer. "
                                  "Your review history stays.", "Delete deck"):
            self.service.delete_deck(deck_id)
            if self.deck_sheet.is_open:
                self.deck_sheet.close_sheet()
            self.refresh()

    def _reset_deck(self, deck_id: str) -> None:
        deck = self.service.deck(deck_id)
        if deck and self._confirm("Reset progress?", f"Every card in “{deck.title}” becomes new "
                                  "again. Your history stays.", "Reset"):
            self.service.reset_deck(deck_id)
            self.refresh()

    def _settings(self) -> None:
        started = [s.deck for s in self.service.summaries() if s.started]
        dialog = StudySettingsDialog(self.service.settings(), started, self.page)

        def save(settings) -> None:
            self.service.save_settings(settings)
            dialog.accept()
            self.refresh()

        def reset(deck_id: str) -> None:
            dialog.reject()
            self._reset_deck(deck_id)

        dialog.saved.connect(save)
        dialog.reset_requested.connect(reset)
        dialog.exec()

    # ------------------------------------------------------------- reports

    def _report_current(self) -> None:
        s = self._session
        if s is None or s.current is None:
            return
        key = s.current
        dialog = ReportCardDialog(self.page)

        def send(reason: str, note: str) -> None:
            if self.remote is None:
                dialog.show_error("Reports need an internet connection and a signed-in account.")
                return
            call_in_background(lambda: self.remote.report_card(key, reason, note),
                               lambda _r: (dialog.accept(), NoticeDialog(
                                   "Thanks for the report", "The Akeso team will check this card.",
                                   "check", parent=self.page).exec()),
                               dialog.show_error, owner=dialog)

        dialog.submitted.connect(send)
        dialog.exec()

    def _confirm(self, title: str, message: str, action: str) -> bool:
        dialog = ConfirmDialog(title, message, action, "trash-2", danger=True, parent=self.page)
        return dialog.exec() == QDialog.DialogCode.Accepted

