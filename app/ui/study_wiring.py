"""Study Hub in the dashboard (migration 050): built once someone is signed in.

    register_study(shell, account) -> StudyWiring

Makes the page, its two sheets (a deck, a review session), the controller,
the sync, the sidebar badge, the dashboard card, Ctrl+K results, and the
"Make a flashcard" menu on encyclopedia pages and notes.
"""

from typing import Optional

from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QApplication

from app.controllers.study_hub_controller import StudyHubController
from app.controllers.study_sync_controller import StudySyncController
from app.repositories.study_local_repository import StudyLocalRepository
from app.repositories.supabase_study_repository import SupabaseStudyRepository
from app.services.study.search_provider import StudyProvider
from app.services.study.study_service import StudyService
from app.services.study.study_sync import StudySync
from app.ui.components.flashcard_menu import FlashcardMenu
from app.ui.views.study.study_hub_page import StudyHubPage

BADGE_EVERY_MS = 10 * 60_000
TAB = "study-hub"


class _LiveScheduler:
    """The scheduler with today's settings (they can change while Akeso runs)."""

    def __init__(self, service: StudyService) -> None:
        self._service = service

    def answer(self, state, rating, now):
        return self._service.scheduler().answer(state, rating, now)


class StudyWiring(QObject):
    def __init__(self, shell, account) -> None:
        super().__init__(shell)
        self.shell = shell
        self.local = StudyLocalRepository(owner=shell._owner)
        self.service = StudyService(self.local, shell._disease_service.all_diseases,
                                    shell._symptom_service.all_symptoms,
                                    shell._medicine_service.all_medicines)
        self.page = StudyHubPage()
        shell.register_view(TAB, self.page)
        deck_sheet = shell.add_sheet(TAB, keep_content=True)
        review_sheet = shell.add_sheet(TAB, keep_content=True)
        self.remote = SupabaseStudyRepository(account.session)
        staff = account.role in ("educator", "admin")
        self.staff = staff
        self.is_admin = account.role == "admin"
        self.controller = StudyHubController(
            self.page, self.service, deck_sheet, review_sheet, inspect=shell._inspect_here,
            remote=self.remote, staff=staff, entry_names=self._entry_names,
            open_staff_editor=self._open_staff_editor if staff else None, parent=self)
        self.sync = StudySyncController(StudySync(self.local, self.remote, _LiveScheduler(self.service)),
                                        self.page.sync_chip.set_status, self.controller.refresh, parent=self)
        self.controller.sync = self.sync
        self.controller.lend_sheet = lambda sheet: shell._lend_sheet(sheet, TAB)
        self.controller.due_changed.connect(self._badge)
        self._entry_cache: Optional[list] = None
        self._staff_editor = None

        # Ctrl+K
        shell._search._providers.append(StudyProvider(lambda: self.service))
        # "Make a flashcard" on encyclopedia pages and in notes
        self.menu = FlashcardMenu(self.controller.make_flashcard, parent=self)
        enc = shell.encyclopedia_page
        self.menu.watch(enc.detail_view, lambda: ("disease", getattr(getattr(enc.detail_view, "_disease", None), "id", "")))
        sym = shell.symptom_page
        self.menu.watch(sym.detail, lambda: ("symptom", getattr(getattr(sym.detail, "_symptom", None), "id", "")))
        med = shell.medicine_page
        self.menu.watch(med.monograph, lambda: ("medicine", getattr(getattr(med.monograph, "_medicine", None), "id", "")))
        self.menu.watch(shell.notebook_page, lambda: ("", ""))
        # "Study cards" next to the bookmark star on each entry page
        self._study_button(enc.detail_view, "_bookmark_btn", "disease", "_disease")
        self._study_button(sym.detail, "_bookmark", "symptom", "_symptom")
        self._study_button(med.monograph, "_bookmark", "medicine", "_medicine")

        # the badge, now and then
        self._timer = QTimer(self)
        self._timer.setInterval(BADGE_EVERY_MS)
        self._timer.timeout.connect(self.update_badge)
        self._timer.start()
        QTimer.singleShot(4000, self.update_badge)
        QTimer.singleShot(6000, self.sync.sync_now)          # bring other computers' reviews in
        app = QApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(self.sync.shutdown)

    def _study_button(self, view, star_attr: str, kind: str, entry_attr: str) -> None:
        """A small "Study cards" button before the page's bookmark star."""
        from PySide6.QtWidgets import QPushButton
        from app.ui.views.account.account_widgets import button
        star = getattr(view, star_attr, None)
        parent = star.parentWidget() if star is not None else None
        layout = parent.layout() if parent is not None else None
        if layout is None:
            return
        index = layout.indexOf(star)

        def study() -> None:
            entry = getattr(view, entry_attr, None)
            if entry is None:
                return
            if not self.controller.entry_deck(kind, entry.id, entry.name):
                from app.ui.views.account.account_dialogs import NoticeDialog
                NoticeDialog("No cards yet", f"There's not enough in “{entry.name}” to make "
                             "flashcards from yet.", "layers", parent=view).exec()

        widget: QPushButton = button("Study cards", "acGhost", "graduation-cap", study)
        widget.setToolTip("Flashcards made from this entry (Study Hub)")
        if index >= 0:
            layout.insertWidget(index, widget)

    # ------------------------------------------------------------------ api

    def on_tab(self, tab_id: str) -> None:
        if tab_id == TAB:
            self.controller.refresh()
            self.sync.hub_opened()
        else:
            self.sync.hub_closed()

    def update_badge(self) -> None:
        try:
            due, new = self.service.due_today()
        except Exception:  # noqa: BLE001 - a broken local file must not break the dashboard
            return
        self._badge(due, new)

    def _badge(self, due: int, new: Optional[int] = None) -> None:
        self.shell.sidebar.set_count(TAB, due)
        if new is None:
            new = self.service.due_today()[1]
        dashboard = getattr(self.shell, "dashboard_view", None)
        if dashboard is not None and hasattr(dashboard, "show_study"):
            dashboard.show_study(due, new)

    def open_result(self, kind: str, target_id: str) -> None:
        self.shell.show_tab(TAB)
        if kind == "deck":
            self.controller.open_deck(target_id)
        else:
            self.controller.open_card(target_id)

    def _entry_names(self) -> list:
        if self._entry_cache is None:
            shell = self.shell
            items = []
            items += [(f"{d.name} · Condition", ("disease", d.id)) for d in shell._disease_service.all_diseases()]
            items += [(f"{s.name} · Symptom", ("symptom", s.id)) for s in shell._symptom_service.all_symptoms()]
            items += [(f"{m.name} · Medicine", ("medicine", m.id)) for m in shell._medicine_service.all_medicines()]
            self._entry_cache = sorted(items, key=lambda x: x[0].lower())
        return self._entry_cache

    def _open_staff_editor(self) -> None:
        """Official decks (educators and admins): over whatever tab is showing,
        so Content Management can open it too."""
        from app.controllers.study_admin_controller import StudyAdminController
        if self._staff_editor is None:
            sheet = self.shell.add_sheet(TAB, keep_content=True)
            self._staff_editor = StudyAdminController(
                self.remote, self.is_admin, self._entry_names, sheet, parent_widget=self.page,
                on_published=self.sync.sync_now, parent=self)
        self.shell._lend_sheet(self._staff_editor.sheet, TAB)
        self._staff_editor.open()
        self._staff_editor.sheet.raise_()
        self._staff_editor.sheet.tab.raise_()

    def open_official_decks(self) -> None:
        if self.staff:
            self._open_staff_editor()


def register_study(shell, account) -> Optional[StudyWiring]:
    try:
        return StudyWiring(shell, account)
    except Exception as exc:  # noqa: BLE001 - Study Hub must never stop the app from opening
        import sys
        print(f"[study] could not start Study Hub: {exc}", file=sys.stderr)
        return None
