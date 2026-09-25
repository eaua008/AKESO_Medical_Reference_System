"""The application shell: header, sidebar, and a swappable content area.

The shell is where navigation decisions meet. The header and sidebar only
announce what the user did; this class decides where that leads:

    Ctrl+K                  -> focus the search box
    typing in search        -> ask SearchService, show suggestions
    choosing a suggestion   -> open that module, condition, symptom,
                               medicine, or first-aid protocol
    Emergency Guide button  -> Emergency Guide tab
    Account Settings        -> Account tab
    Search History          -> History tab
    Sign Out                -> tell MainWindow, which owns logout

Cross-module jumps also land here, because no module should know about
another: a symptom's linked condition opens the Disease Encyclopedia, a
medicine's linked condition does the same, and "Present Case" goes to
Clinical Exchange.

Screens are plugged in with register_view(). Anything not built yet shows a
placeholder, so every destination leads somewhere.
"""

import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.controllers.bookmark_controller import BookmarkController
from app.controllers.disease_controller import DiseaseController
from app.controllers.emergency_controller import EmergencyController
from app.controllers.interaction_checker_controller import InteractionCheckerController
from app.controllers.medicine_controller import MedicineController
from app.controllers.notebook_controller import NotebookController
from app.controllers.symptom_checker_controller import SymptomCheckerController
from app.controllers.symptom_controller import SymptomController
from app.controllers.wellness_controller import WellnessController
from app.core.theme import Theme
from app.models.bookmark import DISEASE, MEDICINE, SYMPTOM
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
from app.ui.components.sidebar import NAV_SECTIONS, AkesoSidebarNav, visible_items
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

    def __init__(
            self,
            user_name: str = "User",
            user_email: str = "",
            role: str = "user",
            start_tab: str = "dashboard",
    ) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._pages: dict[str, QWidget] = {}

        # One service per module, shared by its screen and by search, so both
        # read the same cached data rather than fetching it twice.
        self._disease_service = DiseaseService()
        self._symptom_service = SymptomService()
        self._medicine_service = MedicineService()
        self._emergency_service = EmergencyService()
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
        )
        self._search = SearchService(
            providers=[
                # visible_items(role): search can never reach a module the
                # sidebar hides from this role.
                ModuleProvider(visible_items(role)),
                DiseaseProvider(self._disease_service.all_diseases),
                SymptomProvider(self._symptom_service.all_symptoms),
                MedicineProvider(self._medicine_service.all_medicines),
                EmergencyProvider(self._emergency_service.protocols),
            ]
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.header = AkesoHeader(user_name=user_name, user_email=user_email)
        root.addWidget(self.header)

        body = QWidget()
        body.setObjectName("panel")
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.sidebar = AkesoSidebarNav(active_tab=start_tab, role=role)
        body_layout.addWidget(self.sidebar)

        self.content = QStackedWidget()
        body_layout.addWidget(self.content, 1)
        root.addWidget(body, 1)

        self._build_placeholders()
        self._register_real_views()
        self._wire_header()
        self.sidebar.tabChanged.connect(self.show_tab)

        # Ctrl+K from anywhere in the window. WindowShortcut scopes it to this
        # window, so it cannot fire while a dialog elsewhere has focus.
        self._search_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        self._search_shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
        self._search_shortcut.activated.connect(self.header.focus_search)

        self.show_tab(start_tab)

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
        try:
            results = self._search.search(text)
        except Exception:
            # A failed lookup (network down, say) must not break typing.
            # Fall back to module matches only.
            results = ModuleProvider(visible_items(self.sidebar.role)).search(text)
            results = sorted(results, key=lambda r: -r.score)[:8]
        self.header.show_suggestions(list(results))

    def _on_search_chosen(self, result: SearchResult) -> None:
        if result.kind == "disease":
            self.show_tab("diseases")
            self.disease_controller.inspect(result.target_id)
        elif result.kind == "symptom":
            self.show_tab("symptoms")
            self.symptom_controller.inspect(result.target_id)
        elif result.kind == "medicine":
            self.show_tab("medicines")
            self.medicine_controller.inspect(result.target_id)
        elif result.kind == "protocol":
            self.show_tab("emergency")
            self.emergency_view.focus_protocol(result.target_id)
        else:
            self.show_tab(result.target_id)

    # -------------------------------------------------------------- pages

    def _build_placeholders(self) -> None:
        """One placeholder per nav item, from the same config the sidebar
        uses, so every nav entry and search result leads somewhere."""
        for section in NAV_SECTIONS:
            for item in section["items"]:
                page = PlaceholderView(item["label"])
                self._pages[item["id"]] = page
                self.content.addWidget(page)

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
        self.checker_controller.case_saved.connect(lambda _id: self.notebook_controller.refresh())
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

    def register_view(self, tab_id: str, widget: QWidget) -> None:
        old = self._pages.get(tab_id)
        if old is not None:
            self.content.removeWidget(old)
            old.deleteLater()
        self._pages[tab_id] = widget
        self.content.addWidget(widget)
        if self.sidebar.active_tab == tab_id:
            self.content.setCurrentWidget(widget)

    def show_tab(self, tab_id: str) -> None:
        page = self._pages.get(tab_id)
        if page is None:
            return
        self.content.setCurrentWidget(page)
        # The notebook and the checker share saved cases: redraw on arrival.
        if tab_id == "notebook" and hasattr(self, "notebook_controller"):
            self.notebook_controller.refresh()
        elif tab_id == "drug-checker" and hasattr(self, "interaction_controller"):
            self.interaction_controller.refresh()

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

    def _open_medicine(self, medicine_id: str) -> None:
        """From the Drug Interaction Checker's monograph buttons to that medicine."""
        self.show_tab("medicines")
        self.medicine_controller.inspect(medicine_id)

    def _open_reference_entry(self, kind: str, entry_id: str) -> None:
        """"Open full monograph" from the notebook's Reference column."""
        if kind == "disease":
            self._open_condition(entry_id)
        elif kind == "symptom":
            self.show_tab("symptoms")
            self.symptom_controller.inspect(entry_id)
        elif kind == "medicine":
            self._open_medicine(entry_id)

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
        """From a symptom's or medicine's linked condition to that disease."""
        self.show_tab("diseases")
        self.disease_controller.inspect(disease_id)

    # -------------------------------------------------------------- theme

    def _on_theme_changed(self, _is_dark: bool) -> None:
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(Theme.stylesheet())
        # Stylesheets reapply themselves; baked pixmaps must be redrawn.
        self.header.refresh_theme()
        self.sidebar.refresh_theme()
        # Pages with painted icons opt in by defining refresh_theme().
        for page in self._pages.values():
            refresh = getattr(page, "refresh_theme", None)
            if callable(refresh):
                refresh()


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(Theme.stylesheet())
    shell = DashboardShell(user_name="Eijkim", user_email="eijkim@example.com")
    shell.resize(1480, 920)
    shell.setWindowTitle("Akeso")
    shell.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())