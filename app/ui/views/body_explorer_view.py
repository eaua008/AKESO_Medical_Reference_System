"""Body System Explorer: a 3D body you can peel layer by layer.

Left: the 3D view (assets/anatomy/anatomy.html in the built-in browser
engine, three.js). Right: regions, the layer slider, and what you clicked:
its name and body system, then the diseases, symptoms, articles and peer
discussions for that body system.

Display only. BodyExplorerController decides what the lists contain; the
shell opens whatever is clicked on top of this page.

The browser engine is heavy, so the 3D view is created the first time the
page is shown, not when Akeso starts.
"""

import json
from typing import Optional

from PySide6.QtCore import QObject, Qt, QUrl, Signal, Slot
from PySide6.QtWidgets import (
    QButtonGroup, QFrame, QHBoxLayout, QPushButton, QScrollArea, QSlider, QVBoxLayout, QWidget,
)

from app.core.theme import Theme
from app.ui.views.account.account_widgets import (
    Card, button, icon_label, label, pill, refresh_icons, repolish,
)

REGIONS = [("body", "Whole body"), ("head", "Head"), ("chest", "Chest"),
           ("abdomen", "Abdomen"), ("arms", "Arms"), ("legs", "Legs")]
LAYER_NAMES = ["Skin", "Muscle", "Bone", "Organs"]
LAYER_LABELS = {"skin": "Skin", "muscle": "Muscle", "bone": "Bone", "organ": "Organ"}
# Browse without clicking the model (and the fallback when 3D is unavailable).
SYSTEMS = [("nervous", "Nervous"), ("cardiovascular", "Cardiovascular"),
           ("respiratory", "Respiratory"), ("digestive", "Digestive"), ("urinary", "Urinary"),
           ("endocrine", "Endocrine"), ("musculoskeletal", "Musculoskeletal"),
           ("integumentary", "Skin (integumentary)")]
SHOW_MAX = 8
GUIDE = [
    ("Rotate", "Drag with the left mouse button."),
    ("Move", "Drag with the right mouse button."),
    ("Zoom", "Scroll the mouse wheel."),
    ("Zoom in", "Click the body or a Regions button. Whole body goes back."),
    ("Peel", "Layers slider: Skin → Muscle → Bone → Organs."),
    ("Select", "Once zoomed in, click a part. Point at it to see its name."),
    ("Hide", "Hide button or H. Shift + H hides the whole group (e.g. all of the skull)."),
    ("See-through", "See-through button or T (Shift + T for the group). Again makes it solid."),
    ("Only this", "Only this button or O (Shift + O for the group)."),
    ("Reset", "Show all, or R. Esc clears the selection."),
    ("Systems", "Body-system chips list conditions without using the model."),
]


class _Bridge(QObject):
    """What the page calls (through QWebChannel)."""

    page_ready = Signal()
    part_clicked = Signal(dict)
    region_moved = Signal(str)
    no_webgl = Signal()
    visibility = Signal(dict)

    @Slot()
    def webglFailed(self) -> None:  # noqa: N802
        self.no_webgl.emit()

    @Slot(str)
    def visibilityChanged(self, payload: str) -> None:  # noqa: N802
        try:
            self.visibility.emit(json.loads(payload))
        except ValueError:
            pass

    @Slot()
    def ready(self) -> None:
        self.page_ready.emit()

    @Slot(str)
    def partSelected(self, payload: str) -> None:  # noqa: N802
        try:
            self.part_clicked.emit(json.loads(payload))
        except ValueError:
            pass

    @Slot(str)
    def regionChanged(self, key: str) -> None:  # noqa: N802
        self.region_moved.emit(key)


class _Row(QFrame):
    clicked = Signal(str)

    def __init__(self, item_id: str, title: str, subtitle: str, icon: str) -> None:
        super().__init__()
        self.setObjectName("acRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = item_id
        row = QHBoxLayout(self)
        row.setContentsMargins(10, 7, 10, 7)
        row.setSpacing(9)
        row.addWidget(icon_label(icon, 15), 0, Qt.AlignmentFlag.AlignTop)
        text = QVBoxLayout()
        text.setSpacing(1)
        text.addWidget(label(title, "acRowTitle"))
        if subtitle:
            text.addWidget(label(subtitle, "acSmall"))
        row.addLayout(text, 1)
        row.addWidget(icon_label("chevron-right", 14, Theme.token("ICON_MUTED")))

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._id)
        super().mouseReleaseEvent(event)


class BodyExplorerView(QWidget):
    part_selected = Signal(dict)            # the part the user clicked (from parts.json)
    disease_requested = Signal(str)
    symptom_requested = Signal(str)
    article_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.web = None
        self._ready = False
        self._layer = 0.0
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        self._stage = QWidget()
        self._stage.setObjectName("panel")
        self._stage_layout = QVBoxLayout(self._stage)
        self._stage_layout.setContentsMargins(0, 0, 0, 0)
        self._placeholder = label("Loading the 3D body…", "acMuted")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._stage_layout.addWidget(self._placeholder)
        row.addWidget(self._stage, 1)

        side = QScrollArea()
        side.setWidgetResizable(True)
        side.setFrameShape(QFrame.Shape.NoFrame)
        side.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        side.setFixedWidth(370)
        panel = QWidget()
        panel.setObjectName("panel")
        panel.setMaximumWidth(356)             # the column minus its scrollbar: text wraps
        self._side = QVBoxLayout(panel)
        self._side.setContentsMargins(18, 20, 20, 24)
        self._side.setSpacing(14)
        side.setWidget(panel)
        row.addWidget(side)
        self._build_side()

    # ------------------------------------------------------------ side panel

    def _build_side(self) -> None:
        title = QVBoxLayout()
        title.setSpacing(3)
        title.addWidget(label("Body System Explorer", "acTitle"))
        title.addWidget(label("Click a region to zoom in, slide to peel the layers, then click "
                              "a part to see related conditions.", "acSubtitle"))
        self._side.addLayout(title)
        self._side.addWidget(self._build_guide())

        nav = Card("Regions", "", "layout-grid")
        host = QWidget()
        host.setObjectName("panel")
        grid = QHBoxLayout(host)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(6)
        rows = QVBoxLayout()
        rows.setSpacing(6)
        self._region_group = QButtonGroup(self)
        self._region_group.setExclusive(True)
        self.region_buttons: dict[str, QPushButton] = {}
        line = None
        for i, (key, text) in enumerate(REGIONS):
            if i % 3 == 0:
                line = QHBoxLayout()
                line.setSpacing(6)
                rows.addLayout(line)
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setChecked(key == "body")
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.clicked.connect(lambda _c=False, k=key: self.focus(k))
            self._region_group.addButton(chip)
            self.region_buttons[key] = chip
            line.addWidget(chip)
        grid.addLayout(rows)
        nav.body.addWidget(host)
        self._side.addWidget(nav)

        layers = Card("Layers", "Slide right to peel away the outer layers.", "layers")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 300)
        self.slider.setSingleStep(10)
        self.slider.setPageStep(100)
        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.slider.valueChanged.connect(self._slider_moved)
        layers.body.addWidget(self.slider)
        ticks = QHBoxLayout()
        for i, name in enumerate(LAYER_NAMES):
            tick = label(name, "acSmall", wrap=False)
            if i:
                ticks.addStretch(1)
            ticks.addWidget(tick)
        layers.body.addLayout(ticks)
        self.layer_now = label("Showing: Skin", "acValue")
        layers.body.addWidget(self.layer_now)
        self._side.addWidget(layers)
        self.layers_card = layers

        systems = Card("Browse by body system", "", "activity")
        from app.ui.views.compare_view import FlowLayout
        host = QWidget()
        host.setObjectName("panel")
        flow = FlowLayout(6, 6)
        host.setLayout(flow)
        for key, text in SYSTEMS:
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.clicked.connect(lambda _c=False, k=key, t=text: self.part_selected.emit(
                {"browse": True, "name": f"{t} system" if "(" not in t else "Skin",
                 "system": k, "layer": ""}))
            flow.addWidget(chip)
        systems.body.addWidget(host)
        self._side.addWidget(systems)

        self.part_card = Card("Selected", "", "search")
        self._part_body = QVBoxLayout()
        self._part_body.setSpacing(8)
        self.part_card.body.addLayout(self._part_body)
        self._side.addWidget(self.part_card)

        self.hidden_card = Card("Hidden & see-through", "Click Show to bring one back.", "eye-off")
        self._hidden_body = QVBoxLayout()
        self._hidden_body.setSpacing(6)
        self.hidden_card.body.addLayout(self._hidden_body)
        self.hidden_card.body.addWidget(button("Show all", "acGhost", "rotate-ccw",
                                               lambda: self._js("akeso.showAll()")),
                                        0, Qt.AlignmentFlag.AlignLeft)
        self.hidden_card.hide()
        self._side.addWidget(self.hidden_card)

        self._lists = QVBoxLayout()
        self._lists.setSpacing(14)
        self._side.addLayout(self._lists)
        self._side.addStretch(1)
        self._side.addWidget(label("3D models: BodyParts3D, © The Database Center for Life "
                                   "Science (CC BY 4.0). Educational reference only.", "acSmall"))
        self.show_part(None)

    def _slider_moved(self, value: int) -> None:
        self._layer = value / 100
        index = min(3, int(self._layer + 0.5))
        self.layer_now.setText(f"Showing: {LAYER_NAMES[index]}")
        self._js(f"akeso.setLayer({self._layer:.2f})")

    def _clear(self, layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().hide()               # gone now, freed a moment later
                item.widget().deleteLater()
            elif item.layout():
                self._clear(item.layout())

    # ------------------------------------------------------------------ api

    def focus(self, key: str) -> None:
        chip = self.region_buttons.get(key)
        if chip is not None:
            chip.setChecked(True)
        self._js(f"akeso.focus({json.dumps(key)})")

    def show_part(self, part: Optional[dict], system_label: str = "", diseases=(),
                  symptoms=(), articles=(), discussions: Optional[QWidget] = None) -> None:
        self._clear(self._part_body)
        self._clear(self._lists)
        if not part:
            self._part_body.addWidget(label(
                "Nothing selected yet. Zoom into a region, then click any bone, muscle or "
                "organ.", "acMuted"))
            return
        name = (part.get("name") or "").strip()
        browsing = bool(part.get("browse"))
        self._part_body.addWidget(label(system_label if browsing and system_label
                                        else name[:1].upper() + name[1:], "acCardTitle"))
        if part.get("group") and part.get("group") != part.get("name"):
            self._part_body.addWidget(label(f"Part of: {part['group']}", "acSmall"))
        chips = QHBoxLayout()
        chips.setSpacing(6)
        if not browsing:
            chips.addWidget(pill(LAYER_LABELS.get(part.get("layer"), "Part"), "acPill"))
        if system_label and not browsing:
            chips.addWidget(pill(system_label, "acPillGood"))
        if browsing:
            chips.addWidget(pill("Body system", "acPillGood"))
        chips.addStretch(1)
        self._part_body.addLayout(chips)
        if part.get("fma"):
            self._part_body.addWidget(label(f"Anatomy ID: {part['fma']} (Foundational Model "
                                            "of Anatomy)", "acSmall"))
        if part.get("id") and not browsing:
            self._part_body.addLayout(self._actions(part["id"], False, "This part"))
            group = part.get("group") or ""
            if group and group != part.get("name"):
                self._part_body.addLayout(self._actions(part["id"], True,
                                                        f"Whole {group}"))

        self._list_card(f"Conditions · {system_label}" if system_label else "Conditions",
                        "book-open", diseases, self.disease_requested,
                        "No conditions are filed under this body system yet.")
        self._list_card("Symptoms", "activity", symptoms, self.symptom_requested,
                        "No symptoms are filed under this body system yet.")
        if articles:
            self._list_card("Health articles", "file-text", articles, self.article_requested, "")
        if discussions is not None:
            card = Card("Peer discussions", "Clinical Exchange posts tagged with this body "
                        "system.", "message-circle")
            card.body.addWidget(discussions)
            self._lists.addWidget(card)

    def _actions(self, part_id: str, whole: bool, caption: str) -> QVBoxLayout:
        """Hide / See-through / Show only, for one part or its whole group."""
        box = QVBoxLayout()
        box.setSpacing(4)
        box.addWidget(label(caption.upper(), "acFieldLabel"))
        from app.ui.views.compare_view import FlowLayout
        host = QWidget()
        host.setObjectName("panel")
        line = FlowLayout(6, 6)                  # wraps inside the narrow side panel
        host.setLayout(line)
        arg = f"{json.dumps(part_id)}, {'true' if whole else 'false'}"
        for text, icon, call, tip in (
                ("Hide", "eye-off", "hide", "Hide it to see what's behind (H)"),
                ("See-through", "eye", "ghost", "Make it transparent; press again for solid (T)"),
                ("Only this", "target", "isolate", "Hide everything else and fly to it (O)")):
            b = button(text, "acGhost", icon, lambda c=call: self._js(f"akeso.{c}({arg})"))
            b.setToolTip(tip + (" — add Shift for the whole group" if whole else ""))
            line.addWidget(b)
        box.addWidget(host)
        return box

    def _build_guide(self) -> Card:
        card = Card("How to use", "", "circle-help")
        self._guide_toggle = button("Hide guide", "acLink", on_click=self._toggle_guide)
        card.head.addWidget(self._guide_toggle, 0, Qt.AlignmentFlag.AlignTop)
        self._guide = QWidget()
        self._guide.setObjectName("panel")
        column = QVBoxLayout(self._guide)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(7)
        from PySide6.QtWidgets import QGridLayout
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(6)
        grid.setColumnStretch(1, 1)
        for i, (what, how) in enumerate(GUIDE):
            title = label(what, "acRowTitle")
            title.setFixedWidth(96)
            grid.addWidget(title, i, 0, Qt.AlignmentFlag.AlignTop)
            grid.addWidget(label(how, "acSmall"), i, 1, Qt.AlignmentFlag.AlignTop)
        column.addLayout(grid)
        column.addWidget(label("Keys work after you click the 3D view once.", "acSmall"))
        card.body.addWidget(self._guide)
        return card

    def _toggle_guide(self) -> None:
        from app.ui.views.account.account_widgets import set_text
        show = not self._guide.isVisible()
        self._guide.setVisible(show)
        set_text(self._guide_toggle, "Hide guide" if show else "Show guide")

    def _visibility(self, state: dict) -> None:
        """The page reports what is hidden, see-through or shown alone."""
        self._clear(self._hidden_body)
        entries = state.get("entries") or []
        only = state.get("isolated")
        if only:
            self._hidden_body.addWidget(label(f"Showing only: {only}", "acValue"))
        for entry in entries:
            line = QHBoxLayout()
            line.setSpacing(6)
            count = entry.get("count", 1)
            text = entry.get("label", "") + (f" ({count} pieces)" if count > 1 else "")
            line.addWidget(label(text, "acRowTitle"), 1)
            line.addWidget(pill("Hidden" if entry.get("kind") == "hide" else "See-through",
                                "acPill"))
            key = json.dumps(entry.get("key", ""))
            line.addWidget(button("Show", "acLink",
                                  on_click=lambda k=key: self._js(f"akeso.restore({k})")))
            self._hidden_body.addLayout(line)
        self.hidden_card.setVisible(bool(entries or only))

    def _list_card(self, title: str, icon: str, items, signal, empty: str) -> None:
        items = list(items)
        card = Card(f"{title} ({len(items)})" if items else title, "", icon)
        for item_id, name, subtitle in items[:SHOW_MAX]:
            row = _Row(item_id, name, subtitle, icon)
            row.clicked.connect(signal.emit)
            card.body.addWidget(row)
        if len(items) > SHOW_MAX:
            card.body.addWidget(label(f"+ {len(items) - SHOW_MAX} more in the encyclopedia",
                                      "acSmall"))
        if not items:
            card.body.addWidget(label(empty, "acMuted"))
        self._lists.addWidget(card)

    # ------------------------------------------------------------ 3D view

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        if self.web is None:
            self._create_web()

    def _create_web(self) -> None:
        from app.ui.components import anatomy_scheme
        if not anatomy_scheme.models_present():
            self._placeholder.setText("The 3D body files are missing (assets/anatomy/). "
                                      "Reinstall Akeso or ask an admin.")
            self.web = False
            return
        from PySide6.QtWebChannel import QWebChannel
        from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
        from PySide6.QtWebEngineWidgets import QWebEngineView
        from app.ui.components.reference_browser import _shared_profile

        profile = _shared_profile()
        anatomy_scheme.install(profile)
        self.web = QWebEngineView(self._stage)
        page = QWebEnginePage(profile, self.web)
        page.javaScriptConsoleMessage = lambda *a: None        # quiet terminal
        self.web.setPage(page)
        page.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        self.bridge = _Bridge(self)
        self.bridge.page_ready.connect(self._page_ready)
        self.bridge.part_clicked.connect(self.part_selected.emit)
        self.bridge.region_moved.connect(self._region_moved)
        self.bridge.no_webgl.connect(self._no_webgl)
        self.bridge.visibility.connect(self._visibility)
        self.channel = QWebChannel(page)
        self.channel.registerObject("bridge", self.bridge)
        page.setWebChannel(self.channel)
        page.loadFinished.connect(lambda ok: self._apply_theme())
        self.web.setUrl(QUrl("akeso://anatomy/anatomy.html"))
        self._stage_layout.removeWidget(self._placeholder)
        self._placeholder.hide()
        self._stage_layout.addWidget(self.web)

    def _page_ready(self) -> None:
        self._ready = True
        self._apply_theme()
        if self._layer:
            self._js(f"akeso.setLayer({self._layer:.2f})")

    def _no_webgl(self) -> None:
        """3D can't run here: say so and keep browsing by body system."""
        self.layers_card.setEnabled(False)
        for chip in self.region_buttons.values():
            chip.setEnabled(False)

    def _region_moved(self, key: str) -> None:
        chip = self.region_buttons.get(key)
        if chip is not None:
            chip.setChecked(True)

    def _js(self, code: str) -> None:
        if self.web:
            self.web.page().runJavaScript(f"window.akeso && {code}")

    def _apply_theme(self) -> None:
        self._js(f"akeso.setTheme({json.dumps(Theme.token('BG'))}, "
                 f"{'true' if Theme.mode() == 'dark' else 'false'}, "
                 f"{json.dumps(Theme.token('BADGE_TEXT'))})")

    def refresh_theme(self) -> None:
        refresh_icons(self)
        repolish(self)
        self._apply_theme()
