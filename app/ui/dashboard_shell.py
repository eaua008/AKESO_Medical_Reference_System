"""The application shell: header, sidebar, and a swappable content area.

The shell is where navigation decisions meet. The header and sidebar only
announce what the user did; this class decides where that leads:

    Ctrl+K                  -> focus the search box
    typing in search        -> ask SearchService, show suggestions
    choosing a suggestion   -> open that module, condition, symptom,
                               medicine, or first-aid protocol
    Emergency Guide button  -> Emergency Guide tab
    Account Settings        -> Account tab
    Search History          -> History tab (every chosen result is recorded
                               there, unless the user switched saving off)
    Sign Out                -> tell MainWindow, which owns logout

Cross-module jumps also land here, because no module should know about
another: a symptom's linked condition opens the Disease Encyclopedia, a
medicine's linked condition does the same, and "Present Case" goes to
Clinical Exchange.

Screens are plugged in with register_view(). Anything not built yet shows a
placeholder, so every destination leads somewhere.
"""

import sys
from typing import Callable, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.controllers.account_controller import AccountController
from app.controllers.account_gate import AccountContext
from app.controllers.bookmark_controller import BookmarkController
from app.controllers.admin_controller import AdminController
from app.controllers.exchange_controller import ExchangeController
from app.repositories.admin_repository import AdminRepository
from app.services.admin_service import AdminService
from app.ui.views.admin.content_view import ContentManagementView
from app.ui.views.admin.users_view import UserManagementView
from app.controllers.notifications_controller import NotificationsController
from app.repositories.exchange_repository import ExchangeRepository
from app.services.exchange_service import (
    ExchangeService, NotificationService, PostTitleCache, ReferenceIndex,
)
from app.ui.views.exchange.exchange_page import ExchangePage
from app.ui.views.notifications_view import NotificationsView
from app.controllers.disease_controller import DiseaseController
from app.controllers.emergency_controller import EmergencyController
from app.controllers.interaction_checker_controller import InteractionCheckerController
from app.controllers.medicine_controller import MedicineController
from app.controllers.notebook_controller import NotebookController
from app.controllers.symptom_checker_controller import SymptomCheckerController
from app.controllers.symptom_controller import SymptomController
from app.controllers.wellness_controller import WellnessController
from app.controllers.search_history_controller import SearchHistoryController
from app.controllers.settings_controller import SettingsController
from app.controllers.dashboard_controller import DashboardController
from app.ui.views.dashboard_view import DashboardView
from app.core.preferences import START_TABS, PreferenceStore
from app.core.theme import Theme
from app.models.search_history import HistoryEntry
from app.services.search_history_service import SearchHistoryService
from app.ui.views.search_history_view import SearchHistoryView
from app.ui.views.settings_view import SettingsView
from app.ui.theme_scope import ThemeScope, apply_app_stylesheet
from app.models.bookmark import DISEASE, EXCHANGE, MEDICINE, SYMPTOM
from app.services.bookmark_service import BookmarkService
from app.services.disease_service import DiseaseService
from app.services.drug_safety_service import DrugSafetyService
from app.services.emergency_service import EmergencyService
from app.services.case_study_service import CaseStudyService
from app.services.notebook_service import NotebookService
from app.services.case_reference import CaseReference
from app.services.matching_service import MatchingService
from app.services.reference_library import ReferenceLibrary
from app.repositories.local_case_store import default_case_path
from app.repositories.local_notebook_store import LocalNotebookStore
from app.repositories.notebook_case_store import NotebookCaseStore
from app.services.medicine_search import MedicineProvider
from app.services.medicine_service import MedicineService
from app.services.search_service import (
    DiseaseProvider,
    EmergencyProvider,
    ModuleProvider,
    SearchResult,
    SearchService,
)
from app.services.symptom_search import SymptomProvider
from app.services.symptom_service import SymptomService
from app.ui.components.header import AkesoHeader
from app.core.links import links
from app.core.background import call_in_background
from app.models.exchange import Tag
from app.ui.components.peer_discussions import PeerDiscussionList
from app.ui.components.related_articles import RelatedArticlesList
from app.controllers.health_articles_controller import HealthArticlesController
from app.models.bookmark import ARTICLE
from app.services.health_article_service import ArticleProvider, HealthArticleService
from app.ui.views.health_articles_view import HealthArticlesView
import time as _time
from app.ui.components.page_sheet import PageSheet
from app.ui.components.sidebar import NAV_SECTIONS, AkesoSidebarNav, visible_items
from app.ui.views.account.account_view import AccountView
from app.ui.views.bookmarks_view import BookmarksView
from app.ui.views.emergency_guide_view import EmergencyGuideView
from app.ui.views.encyclopedia_page import EncyclopediaPage
from app.ui.views.interaction_checker_view import InteractionCheckerView
from app.ui.views.medicine_reference_page import MedicineReferencePage
from app.ui.views.notebook_page import NotebookPage
from app.ui.views.symptom_checker_view import SymptomCheckerView
from app.ui.views.symptom_encyclopedia_page import SymptomEncyclopediaPage
from app.ui.views.wellness_view import WellnessView


class PlaceholderView(QWidget):
    """Stand-in for a screen that has not been built yet."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.setObjectName("panel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(8)
        layout.addStretch(1)

        heading = QLabel(title)
        heading.setObjectName("cardTitle")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        note = QLabel("Not built yet")
        note.setObjectName("cardSubtitle")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(heading)
        layout.addWidget(note)
        layout.addStretch(1)


class DashboardShell(QWidget):
    """Header + sidebar + swappable content area."""

    sign_out_requested = Signal()
    identity_changed = Signal(str)          # display name, after a profile edit

    def __init__(
            self,
            user_name: str = "User",
            user_email: str = "",
            role: str = "student",
            start_tab: str = "dashboard",
            account: Optional[AccountContext] = None,
            progress: Optional[Callable[[str], None]] = None,
    ) -> None:
        super().__init__()
        self.setObjectName("panel")
        # Called after each screen is built, so the caller can keep the
        # window responsive during the build (MainWindow._breathe).
        self._progress = progress or (lambda _step: None)
        self._pages: dict[str, QWidget] = {}
        self._sheets: list[tuple[str, PageSheet]] = []
        self._account = account
        self.account_controller: Optional[AccountController] = None
        self.notebook_sync = None              # NotebookSyncController, once signed in
        self.exchange_controller: Optional[ExchangeController] = None
        self.notifications_controller: Optional[NotificationsController] = None
        self._unread: dict[str, int] = {}          # bell badge, by source
        self.admin_controller: Optional[AdminController] = None
        self._exchange_service: Optional[ExchangeService] = None
        # The built-in reference browser, made on the first link click.
        self._browser_sheet: Optional[PageSheet] = None
        self._browser = None
        # Peer discussions on encyclopedia pages: (kind, id) -> (when, posts)
        self._peer_cache: dict[tuple[str, str], tuple[float, list]] = {}
        # Titles of Clinical Exchange posts seen, so a starred post shows in
        # Bookmarks even before the board has loaded.
        self._post_titles = PostTitleCache()
        # Light/dark switching, visible parts first (see theme_scope.py).
        self._theme_scope = ThemeScope(self)

        # One service per module, shared by its screen and by search, so both
        # read the same cached data rather than fetching it twice.
        self._disease_service = DiseaseService()
        self._symptom_service = SymptomService()
        self._medicine_service = MedicineService()
        self._emergency_service = EmergencyService()
        self._article_service = HealthArticleService()
        # Bookmarks are per account, so the signed-in user owns them. They
        # store ids only; titles come from the services above at display time.
        # Per-account data (bookmarks, saved case studies) belongs to the
        # signed-in account.
        self._owner = user_email or user_name
        self._bookmark_service = BookmarkService(
            owner=self._owner,
            disease_lookup=self._disease_service.get,
            symptom_lookup=self._symptom_service.get,
            medicine_lookup=self._medicine_service.get,
            exchange_lookup=lambda post_id: self._post_titles.get(post_id) or {
                "title": "Clinical Exchange post", "kind": "case",
                "excerpt": "Open it to load the discussion."},
            article_lookup=self._article_for_bookmark,
        )
        # Search history and app preferences (Settings). History belongs to
        # the account; preferences belong to this computer.
        self._first_name = (user_name or "").split(" ")[0] if user_name else ""
        self._prefs = PreferenceStore()
        self._history = SearchHistoryService(owner=self._owner)
        self._last_query = ""
        self._search = SearchService(
            providers=[
                # visible_items(role): search can never reach a module the
                # sidebar hides from this role.
                ModuleProvider(visible_items(role)),
                DiseaseProvider(self._disease_service.all_diseases),
                SymptomProvider(self._symptom_service.all_symptoms),
                MedicineProvider(self._medicine_service.all_medicines),
                EmergencyProvider(self._emergency_service.protocols),
                ArticleProvider(self._article_service.all),
            ]
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.header = AkesoHeader(user_name=user_name, user_email=user_email)
        root.addWidget(self.header)

        body = QWidget()
        body.setObjectName("panel")
        self._body = body          # full-page sheets slide over its content area
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.sidebar = AkesoSidebarNav(active_tab=start_tab, role=role,
                                       pinned=self._prefs.load().sidebar_pinned)
        body_layout.addWidget(self.sidebar)

        self.content = QStackedWidget()
        body_layout.addWidget(self.content, 1)
        root.addWidget(body, 1)

        self._build_placeholders()
        self._progress("placeholders")
        self._register_real_views()
        if account is not None:
            self._register_account(account)
        # The header redraws its own icons when its button is clicked.
        self._theme_scope.add(self.header)
        self._theme_scope.add(self.sidebar, self.sidebar.refresh_theme)
        self._theme_scope.add_backdrop(self, body, self.content)
        self._wire_header()
        self.sidebar.tabChanged.connect(self.show_tab)
        self.sidebar.pinChanged.connect(lambda on: self._prefs.update(sidebar_pinned=on))

        # Updates: a green dot on Settings when a newer Akeso is out. The
        # check runs a few seconds after sign-in, off the UI thread.
        from app.controllers.update_controller import UpdateManager
        self._updates = UpdateManager.instance()
        self._updates.changed.connect(self._on_update_state)
        self._on_update_state()
        QTimer.singleShot(4000, lambda: self._updates.check(quiet=True))

        # Ctrl+K from anywhere in the window. WindowShortcut scopes it to this
        # window, so it cannot fire while a dialog elsewhere has focus.
        self._search_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        self._search_shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
        self._search_shortcut.activated.connect(self.header.focus_search)

        self.show_tab(start_tab)
        self._progress = lambda _step: None     # the build is over
        # Reference links from any screen open in the built-in browser.
        links.listen(self._open_link)
        # Every "Recent peer case discussions" list fills itself from here.
        PeerDiscussionList.loader = self._load_peer_posts
        RelatedArticlesList.loader = self._load_related_articles
        # Articles feed search and the "Related health articles" lists, so
        # load them once in the background after sign-in.
        QTimer.singleShot(1500, lambda: self.articles_controller.refresh())
        # The reference library finishes loading just after sign-in; redraw
        # the dashboard's counts once it has, if the dashboard is showing.
        QTimer.singleShot(3000, self._refresh_dashboard_if_shown)

    # -------------------------------------------------------------- wiring

    def _wire_header(self) -> None:
        h = self.header
        h.themeToggled.connect(self._on_theme_changed)
        h.navigationRequested.connect(self.show_tab)
        h.emergencyClicked.connect(lambda: self.show_tab("emergency"))
        h.accountRequested.connect(lambda: self.show_tab("account"))
        h.historyRequested.connect(lambda: self.show_tab("history"))
        h.signOutRequested.connect(self.sign_out_requested.emit)
        h.searchTextChanged.connect(self._on_search_text)
        h.searchResultChosen.connect(self._on_search_chosen)

    # ------------------------------------------------------------- search

    def _on_search_text(self, text: str) -> None:
        self._last_query = text.strip()
        try:
            results = self._search.search(text)
        except Exception:
            # A failed lookup (network down, say) must not break typing.
            # Fall back to module matches only.
            results = ModuleProvider(visible_items(self.sidebar.role)).search(text)
            results = sorted(results, key=lambda r: -r.score)[:8]
        self.header.show_suggestions(list(results))

    def _on_search_chosen(self, result: SearchResult) -> None:
        try:
            if self._history.record(result.kind, result.target_id, result.title,
                                    result.subtitle, result.icon, self._last_query):
                self.history_controller.mark_stale()
        except Exception:
            pass        # a locked or read-only history file must not block opening
        self._last_query = ""
        self._open_result(result.kind, result.target_id)

    def _open_result(self, kind: str, target_id: str) -> None:
        """Open a search result, or the same thing again from Search History."""
        if kind == "disease":
            self.show_tab("diseases")
            self.disease_controller.inspect(target_id)
        elif kind == "symptom":
            self.show_tab("symptoms")
            self.symptom_controller.inspect(target_id)
        elif kind == "medicine":
            self.show_tab("medicines")
            self.medicine_controller.inspect(target_id)
        elif kind == "protocol":
            self.show_tab("emergency")
            self.emergency_view.focus_protocol(target_id)
        elif kind == "article":
            article = self._article_service.get(target_id)
            if article is None or not article.is_external:
                self.show_tab("articles")      # an external link opens over the current tab
            self.articles_controller.open_article(target_id)
        else:
            self.show_tab(target_id)

    # ------------------------------------------------------------ dashboard

    def _library_counts(self) -> dict:
        return {
            "diseases": len(self._disease_service.all_diseases()),
            "symptoms": len(self._symptom_service.all_symptoms()),
            "medicines": len(self._medicine_service.all_medicines()),
            "emergency": len(self._emergency_service.protocols()),
        }

    # ------------------------------------------------- peer discussions

    PEER_CACHE_S = 30

    def _load_peer_posts(self, widget: PeerDiscussionList) -> None:
        """Clinical Exchange posts tagged with the entry this list belongs to.
        Read again at most every 30 s per entry, so flipping between
        monographs does not hit the server each time."""
        widget.post_requested.connect(self._open_post_here)
        if self._exchange_service is None:
            widget.show_message("Sign in to see peer discussions from Clinical Exchange.")
            return
        key = (widget.kind, widget.entry_id)
        cached = self._peer_cache.get(key)
        if cached and _time.monotonic() - cached[0] < self.PEER_CACHE_S:
            widget.show_posts(cached[1])
            return
        widget.show_loading()
        service = self._exchange_service
        kind, entry_id = key

        def fetch() -> list:
            return service.feed("newest", tag=Tag(kind, entry_id, ""))

        def done(posts: list) -> None:
            self._peer_cache[key] = (_time.monotonic(), posts)
            widget.show_posts(posts)

        call_in_background(
            fetch, done,
            lambda _m: widget.show_message("Couldn\u2019t load peer discussions right now."),
            owner=widget)

    # ------------------------------------------------------ health articles

    def _entry_name(self, kind: str, ref_id: str):
        service = {"disease": self._disease_service, "symptom": self._symptom_service,
                   "medicine": self._medicine_service}.get(kind)
        try:
            entry = service.get(ref_id) if service else None
        except Exception:
            entry = None
        return getattr(entry, "name", None)

    def _article_for_bookmark(self, article_id: str):
        article = self._article_service.get(article_id)
        if article is None and not self._article_service.loaded:
            # Not loaded yet: show a placeholder rather than "no longer available".
            from app.models.health_article import HealthArticle
            return HealthArticle(id=article_id, title="Health article",
                                 summary="Open it to load the article.")
        return article

    def _load_related_articles(self, widget: RelatedArticlesList) -> None:
        widget.article_requested.connect(self._open_article_here)
        if self._article_service.loaded:
            widget.show_articles(self._article_service.related_to(widget.kind, widget.entry_id))

    def _articles_loaded(self) -> None:
        """Articles arrived: fill any related-articles list already on screen."""
        for widget in self.findChildren(RelatedArticlesList):
            widget.show_articles(self._article_service.related_to(widget.kind, widget.entry_id))
        self.bookmark_controller.reload()

    # ---------------------------------------------------- reference browser

    def _current_tab(self) -> str:
        current = self.content.currentWidget()
        return next((tab for tab, page in self._pages.items() if page is current), "")

    def _open_link(self, url: str, title: str = "") -> None:
        """A reference link: slide a browser sheet over the current tab,
        on top of whatever is open there (a monograph, say), so closing it
        lands back where the link was."""
        if self._browser_sheet is None:
            # Imported here: QtWebEngine is heavy, and most sessions never
            # open a link.
            from app.ui.components.reference_browser import ReferenceBrowser
            self._browser = ReferenceBrowser()
            sheet = PageSheet(self._body, self.content, keep_content=True)
            sheet.set_content(self._browser)
            sheet.close_requested.connect(sheet.close_sheet)
            sheet.closed.connect(self._browser.stop)
            self._theme_scope.add(sheet, sheet.refresh_theme)
            self._theme_scope.add(sheet.tab)
            self._browser_sheet = sheet
        sheet = self._browser_sheet
        # The sheet belongs to the tab it was opened from, so switching
        # tabs tucks it away and coming back shows it again.
        self._sheets = [(t, s) for t, s in self._sheets if s is not sheet]
        self._sheets.append((self._current_tab(), sheet))
        self._browser.load(url, title)
        sheet.open_sheet()
        sheet.raise_()
        sheet.tab.raise_()

    def _system_counts(self) -> list:
        """[(body system id, name, disease count)], largest first."""
        groups = self._disease_service.group_by_body_system()
        rows = [(system.id, system.name, len(groups.get(system.name, [])))
                for system in self._disease_service.body_systems()]
        return sorted((r for r in rows if r[2]), key=lambda r: (-r[2], r[1]))

    def _open_body_system(self, system_id: str) -> None:
        """Disease Encyclopedia, filtered to one body system."""
        self.show_tab("diseases")
        combo = self.encyclopedia_page.grid_view.system_combo
        index = combo.findData(system_id)
        if index >= 0:
            combo.setCurrentIndex(index)

    def _open_account_tab(self, tab: str) -> None:
        self.show_tab("account")
        if hasattr(self, "account_view"):
            self.account_view.show_tab(tab)

    def _refresh_dashboard_if_shown(self) -> None:
        if self.content.currentWidget() is self._pages.get("dashboard"):
            self.dashboard_controller.refresh()

    def _dashboard_action(self, key: str) -> None:
        if key == "new-note":
            self.show_tab("notebook")
            self.notebook_controller.new_note()
        else:
            self.show_tab(key)

    def _open_note(self, item_id: str) -> None:
        self.show_tab("notebook")
        self.notebook_controller.open_item(item_id)

    def _open_history_entry(self, entry: HistoryEntry) -> None:
        # Opening it again counts as a fresh visit, so it moves to the top.
        try:
            self._history.record(entry.kind, entry.target_id, entry.title,
                                 entry.subtitle, entry.icon, entry.query)
        except Exception:
            pass
        self.history_controller.mark_stale()
        self._open_result(entry.kind, entry.target_id)

    # -------------------------------------------------------------- pages

    def _build_placeholders(self) -> None:
        """One placeholder per nav item, from the same config the sidebar
        uses, so every nav entry and search result leads somewhere."""
        for section in NAV_SECTIONS:
            for item in section["items"]:
                page = PlaceholderView(item["label"])
                self._pages[item["id"]] = page
                self.content.addWidget(page)
                self._theme_scope.add(page)

    def _register_real_views(self) -> None:
        """Swap built screens in for their placeholders."""
        # --- Disease Encyclopedia
        self.encyclopedia_page = EncyclopediaPage()
        self.disease_controller = DiseaseController(
            self.encyclopedia_page, service=self._disease_service
        )
        self.encyclopedia_page.detail_view.case_requested.connect(
            lambda _id: self.show_tab("exchange")
        )
        self.register_view("diseases", self.encyclopedia_page)
        self._disease_sheet = self.add_sheet("diseases", keep_content=True)
        self.encyclopedia_page.attach_sheet(self._disease_sheet)
        detail = self.encyclopedia_page.detail_view
        # Cardinal symptoms "Inspect", pharmacotherapy "Open Pharmacology" and
        # the related-entity pills: shown on top of the disease page.
        detail.symptom_requested.connect(lambda sid: self._inspect_here("symptom", sid))
        detail.medicine_requested.connect(lambda mid: self._inspect_here("medicine", mid))
        detail.check_symptoms_requested.connect(lambda _id: self.show_tab("symptom-checker"))
        detail.compare_requested.connect(self._compare_condition)

        # --- Symptom Encyclopedia
        self.symptom_page = SymptomEncyclopediaPage()
        self.symptom_controller = SymptomController(
            self.symptom_page, service=self._symptom_service
        )
        self.symptom_controller.condition_chosen.connect(self._open_condition)
        # Both send the symptom across to the checker and open it there.
        self.symptom_controller.session_requested.connect(self._send_to_checker)
        self.symptom_controller.matching_requested.connect(self._send_to_checker)
        self.symptom_controller.case_requested.connect(
            lambda _id: self.show_tab("exchange")
        )
        self.register_view("symptoms", self.symptom_page)
        self._symptom_sheet = self.add_sheet("symptoms", keep_content=True)
        self.symptom_page.attach_sheet(self._symptom_sheet)

        # --- Medicine Reference
        self.medicine_page = MedicineReferencePage()
        self.medicine_controller = MedicineController(
            self.medicine_page, service=self._medicine_service
        )
        self.medicine_controller.condition_chosen.connect(self._open_condition)
        self.medicine_controller.case_requested.connect(
            lambda _id: self.show_tab("exchange")
        )
        self.register_view("medicines", self.medicine_page)
        self.medicine_page.attach_sheet(self._medicine_sheet_new())

        # --- Drug Interaction Checker
        # A reference tool: it cross-references hypothetical cases. Medicine
        # names come from the same MedicineService the Medicine Reference uses.
        self.interaction_view = InteractionCheckerView()
        # Saved interaction cases live in the Study Notebook: one library.
        # The first run copies any cases from the old akeso_cases.db.
        self._notebook_store = LocalNotebookStore()
        self._notebook_service = NotebookService(self._owner, self._notebook_store)
        self._notebook_service.import_legacy(default_case_path())
        self._safety_service = DrugSafetyService(medicines=self._medicine_service.all_medicines)
        # One correlation engine, shared by the Symptom Checker and the
        # notebook's saved symptom cases, so both always agree.
        self._engine = MatchingService(disease_source=self._disease_service.all_diseases,
                                       symptom_source=self._symptom_service.all_symptoms)
        self.interaction_controller = InteractionCheckerController(
            self.interaction_view,
            CaseStudyService(owner=self._owner,
                             store=NotebookCaseStore(self._notebook_store),
                             medicines=self._medicine_service.all_medicines),
            self._safety_service,
            brands_for=self._medicine_brands,
            notebook=self._notebook_service,
        )
        self.interaction_controller.monograph_requested.connect(self._open_medicine)
        self.register_view("drug-checker", self.interaction_view)

        # --- Study Notebook: home, half panel, full workspace
        self.notebook_page = NotebookPage()
        self.notebook_controller = NotebookController(
            self.notebook_page, self._notebook_service,
            library=ReferenceLibrary(self._disease_service, self._symptom_service,
                                     self._medicine_service),
            cases=CaseReference(self._engine, self._safety_service, self._medicine_service))
        self.notebook_controller.open_full_reference.connect(self._open_reference_entry)
        # "Add / Edit in ..." on a note opens that checker linked to the note.
        self.notebook_controller.edit_in_drug_checker.connect(self._edit_in_drug_checker)
        self.notebook_controller.edit_in_symptom_checker.connect(self._edit_in_symptom_checker)
        self.interaction_controller.case_saved.connect(
            self.notebook_controller.item_changed_elsewhere)
        self.notebook_controller.new_case_requested.connect(self._new_notebook_case)
        self.notebook_controller.open_interaction_case.connect(self._open_interaction_case)
        self.notebook_controller.data_changed.connect(self.interaction_controller.refresh)
        app = QApplication.instance()
        if app is not None:
            # Layouts are saved half a second after a change; flush on exit.
            app.aboutToQuit.connect(self.notebook_controller.shutdown)
        self.register_view("notebook", self.notebook_page)

        # --- Symptom Correlation Engine
        self.checker_view = SymptomCheckerView()
        self.checker_controller = SymptomCheckerController(
            self.checker_view,
            symptom_service=self._symptom_service,
            disease_service=self._disease_service,
            engine=self._engine,
            notebook=self._notebook_service,
        )
        self.checker_controller.disease_requested.connect(self._open_condition)
        self.checker_controller.case_saved.connect(
            self.notebook_controller.item_changed_elsewhere)
        self.checker_controller.notebook_requested.connect(self._open_notebook_item)
        self.register_view("symptom-checker", self.checker_view)

        # --- Bookmarks
        self.bookmarks_view = BookmarksView()
        self.bookmark_controller = BookmarkController(
            self.bookmarks_view, self._bookmark_service
        )
        self.bookmark_controller.open_requested.connect(self._open_bookmark)
        self.register_view("favorites", self.bookmarks_view)
        self._wire_bookmarks()

        # --- Emergency Guide
        self.emergency_view = EmergencyGuideView()
        self.emergency_controller = EmergencyController(
            self.emergency_view, service=self._emergency_service
        )
        self.register_view("emergency", self.emergency_view)

        # --- Wellness Calculators
        self.wellness_view = WellnessView()
        self.wellness_controller = WellnessController(self.wellness_view)
        self.register_view("wellness", self.wellness_view)

        # --- Health Articles (written + curated links; migration 005)
        self.articles_view = HealthArticlesView()
        self.articles_controller = HealthArticlesController(
            self.articles_view, self._article_service, self._bookmark_service,
            self._notebook_service, entry_name=self._entry_name,
            open_entry=self._inspect_here)
        self.register_view("articles", self.articles_view)
        self._article_sheet = self.add_sheet("articles", keep_content=True)
        self.articles_controller.attach_sheet(self._article_sheet)
        self.articles_controller.bookmark_changed.connect(
            lambda *_: self.bookmark_controller.reload())
        self.articles_controller.notebook_saved.connect(
            self.notebook_controller.item_changed_elsewhere)
        self.articles_controller.loaded.connect(self._articles_loaded)

        # --- Body System Explorer (3D body; the browser engine starts on first visit)
        from app.controllers.body_explorer_controller import BodyExplorerController
        from app.ui.views.body_explorer_view import BodyExplorerView
        self.body_view = BodyExplorerView()
        self.body_controller = BodyExplorerController(
            self.body_view, self._disease_service, self._symptom_service, self._article_service,
            discussions_for=lambda system_id: PeerDiscussionList("body_system", system_id))
        # Whatever is clicked opens on top of the explorer, like everywhere else.
        self.body_view.disease_requested.connect(lambda i: self._inspect_here("disease", i))
        self.body_view.symptom_requested.connect(lambda i: self._inspect_here("symptom", i))
        self.body_view.article_requested.connect(self._open_article_here)
        self.register_view("body-systems", self.body_view)

        # --- Search History and Settings
        self.history_view = SearchHistoryView()
        self.history_controller = SearchHistoryController(
            self.history_view, self._history, self._open_history_entry)
        self.register_view("history", self.history_view)

        visible = {item["id"] for item in visible_items(self.sidebar.role)}
        self.settings_view = SettingsView()
        self.settings_controller = SettingsController(
            self.settings_view, self._prefs, self._history, self.history_controller,
            start_options=[(tab, text) for tab, text in START_TABS if tab in visible],
            apply_theme=self._set_theme,
            apply_color_theme=self._set_color_theme,
            apply_pinned=self.sidebar.set_pinned,
            open_history=lambda: self.show_tab("history"),
        )
        self.register_view("settings", self.settings_view)

        # --- Dashboard Overview (the landing page). Account parts (study
        # activity, Clinical Exchange) attach in _register_account.
        self.dashboard_view = DashboardView()
        self.dashboard_controller = DashboardController(
            self.dashboard_view, first_name=self._first_name,
            notebook=self._notebook_service, history=self._history,
            bookmarks=self._bookmark_service, library_counts=self._library_counts,
            body_systems=self._system_counts)
        dv = self.dashboard_view
        dv.action_requested.connect(self._dashboard_action)
        dv.note_opened.connect(self._open_note)
        dv.search_opened.connect(
            lambda row: self._open_result(row.extra, row.key))
        dv.bookmark_opened.connect(self._open_bookmark)
        dv.post_opened.connect(self._open_exchange_post)
        dv.system_opened.connect(self._open_body_system)
        dv.profile_step.connect(self._open_account_tab)
        self.register_view("dashboard", self.dashboard_view)

    def _register_account(self, account: AccountContext) -> None:
        """Account Settings, the header chip, and study-activity counting."""
        snapshot = account.snapshot
        if snapshot is not None:
            self.header.set_identity(
                account.display_name,
                account.account.header_role_label(snapshot.role, snapshot.profile))

        self.account_view = AccountView()
        self.account_controller = AccountController(
            self.account_view, account.account, account.security, account.tracker,
            account.local, snapshot)
        self.account_controller.identity_changed.connect(self._on_identity)
        self.account_controller.sign_out_requested.connect(self.sign_out_requested.emit)
        self.register_view("account", self.account_view)

        # Study activity: the modules announce what happened; the tracker
        # only counts, and the account controller sends the totals once a
        # minute. Nothing is counted while tracking is switched off.
        bump = account.tracker.bump
        self.disease_controller.opened.connect(lambda _id: bump("diseases_viewed"))
        self.symptom_controller.opened.connect(lambda _id: bump("symptoms_viewed"))
        self.medicine_controller.opened.connect(lambda _id: bump("medicines_viewed"))
        self.checker_view.calculate_requested.connect(lambda *_: bump("checker_runs"))
        self.interaction_view.checker.add_drug_requested.connect(
            lambda *_: bump("interaction_checks"))
        self.notebook_controller.data_changed.connect(lambda: bump("notebook_edits"))
        self._register_exchange(account)
        self._register_notebook_sync(account)
        if account.role == "admin":
            self._register_admin(account)
        self.checker_controller.case_saved.connect(lambda _id: bump("notebook_edits"))
        self.interaction_controller.case_saved.connect(lambda *_: bump("notebook_edits"))

        role_text = {"admin": "Admin", "educator": "Educator", "student": "Student"}.get(
            account.role, "")

        def load_activity() -> dict:
            if not account.tracker.enabled:
                return {"streak": None, "note": "Study tracking is off. Turn it on in "
                        "Account Settings \u2192 Privacy & data."}
            summary = account.account.activity()
            return {"streak": summary.streak, "days": summary.last_14_days,
                    "week": summary.week}

        def load_profile() -> tuple:
            percent, items = account.account.completeness(account.account.snapshot())
            return percent, [(i.label, i.tab) for i in items if not i.done]

        posts = None
        if self._exchange_service is not None:
            service = self._exchange_service
            posts = lambda: service.feed("newest")
        self.dashboard_controller.attach_account(role_text, load_activity, load_profile,
                                                 posts)
        if self.notifications_controller is not None:
            self.notifications_controller.unread_changed.connect(
                self.dashboard_view.set_unread)

        # Announcements from the admins: pop up once, then listed on the
        # dashboard while live (migration 015).
        from app.controllers.announcement_controller import AnnouncementController
        from app.repositories.announcement_repository import AnnouncementRepository
        self.announcement_controller = AnnouncementController(
            AnnouncementRepository(account.session), self.dashboard_view.announcements)
        self.announcement_controller.start()
        # They also count on the bell's red badge and are listed first in
        # Notifications; only Critical ones open by themselves.
        ann = self.announcement_controller
        ann.unread_changed.connect(lambda n: self._set_unread("announcements", n))
        if self.notifications_controller is not None:
            view = self.notifications_view
            ann.items_changed.connect(view.show_announcements)
            view.announcement_requested.connect(ann.open)
            view.mark_all_requested.connect(ann.mark_all_read)
            view.announcement_delete_requested.connect(ann.hide)
            view.clear_requested.connect(ann.clear_read)
            # The bell's regular check also looks for new announcements.
            self.notifications_controller.unread_changed.connect(
                lambda _n: ann.refresh_if_stale())

    def _set_unread(self, source: str, count: int) -> None:
        """The bell's badge: Clinical Exchange notifications + unread
        announcements."""
        self._unread[source] = max(0, int(count or 0))
        try:
            self.header.set_unread(sum(self._unread.values()))
        except RuntimeError:
            pass                                # this dashboard was closed

    def _register_notebook_sync(self, account: AccountContext) -> None:
        """The Study Notebook's cloud copy (migration 011): the same notes on
        every computer the account signs in on. See notebook_sync.py."""
        from app.controllers.notebook_sync_controller import NotebookSyncController
        from app.repositories.notebook_cloud_repository import NotebookCloudRepository
        from app.services.notebook_sync import NotebookSync
        from app.ui.views.notes_editor import images_dir

        sync = NotebookSync(self._owner, self._notebook_store,
                            NotebookCloudRepository(account.session), images_dir)

        def downloaded() -> None:            # changes from another computer
            self.notebook_controller.refresh_home()
            self.interaction_controller.refresh()

        self.notebook_sync = NotebookSyncController(
            sync, self.notebook_page.home, downloaded,
            before_sync=self.notebook_controller.save_now, parent=self)
        self.notebook_sync.start()
        app = QApplication.instance()
        if app is not None:
            # After the notebook's own save on quit (connected earlier).
            app.aboutToQuit.connect(self.notebook_sync.shutdown)

    def _register_exchange(self, account: AccountContext) -> None:
        """Clinical Exchange and Notifications (both need a signed-in account)."""
        repository = ExchangeRepository(account.session)
        reference = ReferenceIndex(self._disease_service.all_diseases,
                                   self._symptom_service.all_symptoms,
                                   self._medicine_service.all_medicines,
                                   self._disease_service.body_systems)
        self.exchange_page = ExchangePage()
        self._exchange_service = ExchangeService(repository, reference, self._post_titles)
        from app.repositories.profile_repository import ProfileRepository
        photos = ProfileRepository(account.session)        # other members' allowed photos
        self.exchange_controller = ExchangeController(
            self.exchange_page, self._exchange_service,
            notebook=self._notebook_service,
            is_bookmarked=self._bookmark_service.is_bookmarked,
            describe_interaction=self.interaction_controller.describe,
            is_moderator=account.role in ("educator", "admin"),
            avatar_loader=photos.download_avatar)
        # Small photos next to names on posts and replies (migration 013).
        from app.ui.components.avatar_cache import AvatarCache
        AvatarCache.loader = photos.download_avatar
        self.register_view("exchange", self.exchange_page)
        ex = self.exchange_controller
        # A post and the composer both slide in over the feed.
        self._post_sheet = self.add_sheet("exchange", keep_content=True)
        self.exchange_page.attach_sheet(self._post_sheet)
        self.exchange_sheet = self.add_sheet("exchange")
        ex.attach_sheet(self.exchange_sheet)
        ex.open_reference.connect(self._open_exchange_reference)
        # Member profiles open on top of whatever is showing (a post, the feed,
        # an encyclopedia page...), like the other pop-ups.
        from app.ui.views.exchange.profile_view import ProfileView
        self.profile_view = ProfileView()
        self._profile_sheet = self.add_sheet("exchange", keep_content=True)
        ex.attach_profile_sheet(self._profile_sheet, self.profile_view)
        ex.before_profile_open = lambda: self._lend_sheet(self._profile_sheet, "exchange")
        ex.post_requested.connect(self._open_post_here)
        ex.edit_profile_requested.connect(lambda: self.show_tab("account"))
        if hasattr(self, "account_view"):
            self.account_view.profile.preview_requested.connect(ex.show_profile)
        ex.bookmark_changed.connect(self.bookmark_controller.set_bookmarked)
        ex.notebook_saved.connect(self.notebook_controller.item_changed_elsewhere)

        # "Present Case" on encyclopedia pages starts a post tagged with that entry.
        for signal, kind in ((self.encyclopedia_page.detail_view.case_requested, "disease"),
                             (self.symptom_controller.case_requested, "symptom"),
                             (self.medicine_controller.case_requested, "medicine")):
            signal.disconnect()
            signal.connect(lambda entry_id, k=kind: self._present_case(k, entry_id))
        self.notebook_controller.share_requested.connect(self._share_to_exchange)

        self.notifications_view = NotificationsView()
        self.notifications_controller = NotificationsController(
            self.notifications_view, NotificationService(repository))
        self.register_view("notifications", self.notifications_view)
        self.notifications_controller.unread_changed.connect(
            lambda n: self._set_unread("exchange", n))
        self.notifications_controller.open_post.connect(self._open_exchange_post)
        ex.notifications_changed.connect(self.notifications_controller.check_count)

    def _register_admin(self, account: AccountContext) -> None:
        """User Management and Content Management (admins only; the database
        refuses everyone else whatever the app shows)."""
        self.admin_users_view = UserManagementView()
        self.admin_content_view = ContentManagementView()
        self.admin_controller = AdminController(
            self.admin_users_view, self.admin_content_view,
            AdminService(AdminRepository(account.session)))
        self.register_view("admin-users", self.admin_users_view)
        self.register_view("admin-content", self.admin_content_view)
        self.admin_controller.attach_sheet(self.add_sheet("admin-content"))
        self.admin_controller.content_changed.connect(self._content_edited)

        # Announcements (migration 015): pop-ups on everyone's dashboard.
        from app.controllers.announcement_admin_controller import AnnouncementAdminController
        from app.repositories.announcement_repository import AnnouncementRepository
        from app.ui.views.admin.announcements_view import AnnouncementsAdminView
        self.admin_announcements_view = AnnouncementsAdminView()
        self.announcement_admin_controller = AnnouncementAdminController(
            self.admin_announcements_view, AnnouncementRepository(account.session))
        self.register_view("admin-announcements", self.admin_announcements_view)

    def _content_edited(self, kind: str) -> None:
        """An admin saved an entry: refresh the encyclopedias on this computer
        now (other computers pick it up at their next sync)."""
        if kind == "article":
            # Articles are read live: just fetch the list again.
            self._article_service.invalidate()
            self.articles_controller.refresh(force=True)
            return
        for controller in (self.disease_controller, self.symptom_controller,
                           self.medicine_controller):
            controller.start_sync(force=True)

    def _present_case(self, kind: str, entry_id: str) -> None:
        self.show_tab("exchange")
        self.exchange_controller.present_case(kind, entry_id)

    def _share_to_exchange(self, item_id: str) -> None:
        self.show_tab("exchange")
        self.exchange_controller.share_notebook_item(item_id)

    def _open_exchange_post(self, post_id: str) -> None:
        self.show_tab("exchange")
        self.exchange_controller.open_post(post_id)

    def _on_identity(self, name: str, caption: str, avatar) -> None:
        self.header.set_identity(name, caption, avatar)
        self.dashboard_controller.set_name((name or "").split(" ")[0])
        self.identity_changed.emit(name)

    def _on_update_state(self) -> None:
        try:
            self.sidebar.set_dot("settings", self._updates.available)
        except RuntimeError:
            pass                        # this dashboard was closed (signed out)

    def shutdown(self) -> None:
        """Called by MainWindow just before signing out."""
        links.stop_listening(self._open_link)
        if PeerDiscussionList.loader == self._load_peer_posts:
            PeerDiscussionList.loader = None
        if RelatedArticlesList.loader == self._load_related_articles:
            RelatedArticlesList.loader = None
        if self._browser is not None:
            self._browser.stop()
        if self.notebook_sync is not None:
            self.notebook_sync.shutdown()       # last notebook upload
        from app.ui.components.avatar_cache import AvatarCache
        AvatarCache.clear()                     # the next account starts fresh
        if self.account_controller is not None:
            self.account_controller.shutdown()
        if self.notifications_controller is not None:
            self.notifications_controller.shutdown()

    def _wire_bookmarks(self) -> None:
        """Every star in the app reports here, and reads its state from here.

        The encyclopedias never import the Bookmarks page: they emit that an
        entry was starred, and the shell decides what that means.
        """
        service = self._bookmark_service

        # Reading: a lookup per entity type, so an entry opens already starred.
        self.encyclopedia_page.grid_view.bookmark_lookup = (
            lambda entry_id: service.is_bookmarked(DISEASE, entry_id))
        self.symptom_page.detail.bookmark_lookup = (
            lambda entry_id: service.is_bookmarked(SYMPTOM, entry_id))
        self.medicine_page.monograph.bookmark_lookup = (
            lambda entry_id: service.is_bookmarked(MEDICINE, entry_id))

        # Writing: each star routes to the one controller that owns the store.
        setter = self.bookmark_controller.set_bookmarked
        self.encyclopedia_page.grid_view.bookmark_toggled.connect(
            lambda entry_id, state: setter(DISEASE, entry_id, state))
        self.encyclopedia_page.detail_view.bookmark_toggled.connect(
            lambda entry_id, state: setter(DISEASE, entry_id, state))
        self.symptom_page.detail.bookmark_toggled.connect(
            lambda entry_id, state: setter(SYMPTOM, entry_id, state))
        self.medicine_page.monograph.bookmark_toggled.connect(
            lambda entry_id, state: setter(MEDICINE, entry_id, state))

    def _open_bookmark(self, entity_type: str, entity_id: str) -> None:
        """Open a starred entry in the module it came from."""
        if entity_type == DISEASE:
            self.show_tab("diseases")
            self.disease_controller.inspect(entity_id)
        elif entity_type == SYMPTOM:
            self.show_tab("symptoms")
            self.symptom_controller.inspect(entity_id)
        elif entity_type == MEDICINE:
            self.show_tab("medicines")
            self.medicine_controller.inspect(entity_id)
        elif entity_type == EXCHANGE and self.exchange_controller is not None:
            self._open_exchange_post(entity_id)
        elif entity_type == ARTICLE:
            self._open_result("article", entity_id)
        elif entity_type == "body_system":
            self.show_tab("diseases")

    def register_view(self, tab_id: str, widget: QWidget) -> None:
        old = self._pages.get(tab_id)
        if old is not None:
            self._theme_scope.remove(old)
            self.content.removeWidget(old)
            old.deleteLater()
        self._pages[tab_id] = widget
        self.content.addWidget(widget)
        # Pages with icons drawn in code redraw them when they get the theme.
        refresh = getattr(widget, "refresh_theme", None)
        self._theme_scope.add(widget, refresh if callable(refresh) else None)
        if self.sidebar.active_tab == tab_id:
            self.content.setCurrentWidget(widget)
        self._progress(tab_id)

    # --------------------------------------------------------------- sheets

    def add_sheet(self, tab_id: str, keep_content: bool = False) -> PageSheet:
        """A full-page sheet for one tab (see page_sheet.py). It slides in
        over the content area, and its X tab overlaps the sidebar. Opening
        another tab tucks it away; coming back shows it again as it was."""
        sheet = PageSheet(self._body, self.content, keep_content=keep_content)
        self._theme_scope.add(sheet, sheet.refresh_theme)
        self._theme_scope.add(sheet.tab)
        self._sheets.append((tab_id, sheet))
        return sheet

    def _show_sheets_for(self, tab_id: str) -> None:
        for owner, sheet in self._sheets:
            if owner != tab_id:
                sheet.suspend()
        # Oldest first, so the one opened last ends up on top.
        for owner, sheet in sorted(self._sheets, key=lambda pair: pair[1].opened_at):
            if owner == tab_id:
                sheet.resume()

    def show_tab(self, tab_id: str) -> None:
        page = self._pages.get(tab_id)
        if page is None:
            return
        self._show_sheets_for(tab_id)
        self.content.setCurrentWidget(page)
        # The notebook and the checker share saved cases: redraw on arrival.
        # Redrawn only if something changed while away: a full redraw on
        # every visit is what made these two tabs slow to switch to.
        if tab_id == "dashboard" and hasattr(self, "dashboard_controller"):
            if self.account_controller is not None:
                self.account_controller.flush_activity()   # so "this week" is current
            self.dashboard_controller.refresh()
            if getattr(self, "announcement_controller", None) is not None:
                self.announcement_controller.dashboard_shown()
        elif tab_id == "notebook" and hasattr(self, "notebook_controller"):
            self.notebook_controller.refresh_if_stale()
        elif tab_id == "drug-checker" and hasattr(self, "interaction_controller"):
            self.interaction_controller.refresh_if_stale()
        elif tab_id == "exchange" and self.exchange_controller is not None:
            self.exchange_controller.on_shown()
        elif tab_id == "notifications" and self.notifications_controller is not None:
            self.notifications_controller.reload()
            if getattr(self, "announcement_controller", None) is not None:
                self.announcement_controller.refresh_if_stale()
        elif tab_id == "articles" and hasattr(self, "articles_controller"):
            self.articles_controller.refresh()
        elif tab_id == "history":
            self.history_controller.refresh_if_stale()
        elif tab_id == "settings":
            self.settings_controller.refresh()
        elif tab_id == "admin-users" and self.admin_controller is not None:
            self.admin_controller.users_shown()
        elif tab_id == "admin-content" and self.admin_controller is not None:
            self.admin_controller.content_shown()
        elif tab_id == "admin-announcements" and \
                getattr(self, "announcement_admin_controller", None) is not None:
            self.announcement_admin_controller.shown()

        # select_tab emits tabChanged, which is wired back to this method.
        # Blocking signals moves the highlight without the echo loop.
        self.sidebar.blockSignals(True)
        self.sidebar.select_tab(tab_id)
        self.sidebar.blockSignals(False)

    # --------------------------------------------------- cross-module jumps

    def _send_to_checker(self, symptom_id: str) -> None:
        """From a symptom's monograph into the checker, already selected."""
        self.show_tab("symptom-checker")
        self.checker_controller.add_symptom(symptom_id)

    def _medicine_brands(self, medicine_id: str) -> list[str]:
        medicine = self._medicine_service.get(medicine_id)
        return [*medicine.ph_brands, *medicine.intl_brands] if medicine else []

    def _medicine_sheet_new(self) -> PageSheet:
        self._medicine_sheet = self.add_sheet("medicines", keep_content=True)
        return self._medicine_sheet

    def _inspect_here(self, kind: str, entry_id: str) -> None:
        """Open a disease, symptom or medicine monograph over the page you are
        on (the notebook, a checker, an article...) instead of jumping to its
        encyclopedia. Closing it (X, Back or Esc) leaves you where you were.

        The monograph sheet normally belongs to its encyclopedia tab; here it
        is lent to the current tab, and handed back when it closes."""
        targets = {
            "disease": (self._disease_sheet, "diseases", self.disease_controller),
            "symptom": (self._symptom_sheet, "symptoms", self.symptom_controller),
            "medicine": (self._medicine_sheet, "medicines", self.medicine_controller),
        }
        if kind not in targets:
            self._open_result(kind, entry_id)
            return
        sheet, home, controller = targets[kind]
        self._lend_sheet(sheet, home)
        controller.inspect(entry_id)
        sheet.raise_()
        sheet.tab.raise_()

    def _lend_sheet(self, sheet: PageSheet, home: str) -> None:
        """Move a module's sheet onto the current tab, on top of anything
        open there; it goes back to its own module when it closes."""
        here = self._current_tab() or home
        self._sheets = [(here if s is sheet else owner, s) for owner, s in self._sheets]
        if not getattr(sheet, "_akeso_rehomes", False):
            sheet.closed.connect(lambda s=sheet, h=home: self._rehome_sheet(s, h))
            sheet._akeso_rehomes = True
        sheet.opened_at = next(PageSheet._order)

    def _open_article_here(self, article_id: str) -> None:
        """A related article on a disease, symptom or medicine page: read it
        on top of that page. External links open in the browser sheet."""
        if not hasattr(self, "_article_sheet"):
            self._open_result("article", article_id)
            return
        article = self._article_service.get(article_id)
        if article is None or not article.is_external:
            self._lend_sheet(self._article_sheet, "articles")
        self.articles_controller.open_article(article_id)

    def _open_post_here(self, post_id: str) -> None:
        """A peer discussion on an entry page: open the post on top of it,
        not in the Clinical Exchange tab."""
        if self.exchange_controller is None or not hasattr(self, "_post_sheet"):
            self._open_exchange_post(post_id)
            return
        self._lend_sheet(self._post_sheet, "exchange")
        self.exchange_controller.open_post(post_id)
        self._post_sheet.raise_()
        self._post_sheet.tab.raise_()

    def _open_exchange_reference(self, kind: str, entry_id: str) -> None:
        """A tag on a post or profile: diseases, symptoms and medicines open on
        top; anything else (body system, topic) goes where it lives."""
        if kind in ("disease", "symptom", "medicine"):
            self._inspect_here(kind, entry_id)
        else:
            self._open_bookmark(kind, entry_id)

    def _compare_condition(self, disease_id: str) -> None:
        """"Compare Condition" on a disease page: the comparison screen with
        this disease already in the first slot."""
        self._disease_sheet.close_sheet()
        self.show_tab("diseases")
        self.encyclopedia_page.show_compare()
        self.encyclopedia_page.compare_view.preselect(disease_id)

    def _rehome_sheet(self, sheet: PageSheet, home: str) -> None:
        self._sheets = [(home if s is sheet else owner, s) for owner, s in self._sheets]

    def _open_medicine(self, medicine_id: str) -> None:
        """A medicine from the Drug Interaction Checker, a disease page or a
        note: shown over the current page."""
        self._inspect_here("medicine", medicine_id)

    def _open_reference_entry(self, kind: str, entry_id: str) -> None:
        """"Open full monograph" from the notebook's Reference column."""
        self._inspect_here(kind, entry_id)

    def _edit_in_drug_checker(self, item_id: str) -> None:
        self.show_tab("drug-checker")
        self.interaction_controller.edit_for_item(item_id)

    def _edit_in_symptom_checker(self, item_id: str) -> None:
        self.show_tab("symptom-checker")
        self.checker_controller.edit_for_item(item_id)

    def _open_notebook_item(self, item_id: str) -> None:
        """"Open in Notebook" after saving a case in the Symptom Checker."""
        if item_id:
            self.show_tab("notebook")
            self.notebook_controller.open_item(item_id, "full")

    def _open_interaction_case(self, item_id: str) -> None:
        self.show_tab("drug-checker")
        self.interaction_controller.open_case(item_id)

    def _new_notebook_case(self, kind: str) -> None:
        """Cases are built in the checkers, then saved to the notebook."""
        self.show_tab("symptom-checker" if kind == "symptom_case" else "drug-checker")

    def _open_condition(self, disease_id: str) -> None:
        """A disease from the Symptom Checker ("View protocol"), or a symptom's
        or medicine's linked condition: shown over the current page."""
        self._inspect_here("disease", disease_id)

    # -------------------------------------------------------------- theme

    def _on_theme_changed(self, _is_dark: bool) -> None:
        # Visible-first: the header, sidebar and current page switch now;
        # other pages switch when opened, or in the background when idle.
        # (Restyling the whole app at once is what used to lag.)
        self._theme_scope.switch()
        self._prefs.update(theme=Theme.mode())      # remembered for next time
        if self.content.currentWidget() is self._pages.get("settings"):
            self.settings_controller.refresh()

    def _set_theme(self, mode: str) -> None:
        """Settings picked a theme: same path as the header's sun/moon button."""
        if mode == Theme.mode():
            return
        Theme.set_mode(mode)
        self.header.refresh_theme()
        self._on_theme_changed(mode == "dark")

    def _set_color_theme(self, theme_id: str) -> None:
        """Settings picked a colour theme (Dracula, Nord...). Light/dark stays
        as it is; the same visible-first restyle as the sun/moon button."""
        if theme_id == Theme.color_theme():
            return
        Theme.set_color_theme(theme_id)
        self._prefs.update(color_theme=Theme.color_theme())
        self.header.refresh_theme()
        self._on_theme_changed(Theme.mode() == "dark")


def main() -> int:
    app = QApplication(sys.argv)
    apply_app_stylesheet()
    shell = DashboardShell(user_name="Eijkim", user_email="eijkim@example.com")
    shell.resize(1480, 920)
    shell.setWindowTitle("Akeso")
    shell.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
