"""Body System Explorer: a 3D body you can peel layer by layer.

Left: the 3D view (assets/anatomy/anatomy.html in the built-in browser
engine, three.js). Right: regions, the layer slider, the blood vessel and
nerve switches (colour coded, recolourable), and what you clicked:
its name and body system, then the diseases, symptoms, articles and peer
discussions for that body system.

Display only. BodyExplorerController decides what the lists contain; the
shell opens whatever is clicked on top of this page.

The browser engine is heavy, so the 3D view is created the first time the
page is shown, not when Akeso starts.
"""

import json
from typing import Optional

from PySide6.QtCore import QObject, QStringListModel, Qt, QUrl, Signal, Slot
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import (
    QButtonGroup, QCompleter, QFrame, QHBoxLayout, QLineEdit, QMenu, QPushButton, QScrollArea,
    QSlider, QVBoxLayout, QWidget,
)

from app.core.anatomy_colours import AnatomyColourStore
from app.ui.components.akeso_loader import LoaderOverlay, LoadingHold, LoadingLabel
from app.core.theme import Theme
from app.ui.views.account.account_widgets import (
    Card, button, icon_label, label, pill, refresh_icons, repolish,
)

REGIONS = [("body", "Whole body"), ("head", "Head"), ("chest", "Chest"),
           ("abdomen", "Abdomen"), ("arms", "Arms"), ("legs", "Legs")]
LAYER_NAMES = ["Skin", "Muscle", "Bone", "Organs"]
LAYER_LABELS = {"skin": "Skin", "muscle": "Muscle", "bone": "Bone", "organ": "Organ",
                "vessel": "Blood vessel", "nerve": "Nerve"}
# Switched on separately from the slider (the page loads them on first use).
EXTRAS = [("vessel", "Blood vessels"), ("nerve", "Nerves")]
# Colour-coded kinds, with the textbook colours (must match anatomy.js).
KINDS = [("artery", "Arteries", "#d63031"), ("vein", "Veins", "#2e6bd9"),
         ("pulmonary_artery", "Pulmonary arteries", "#2e6bd9"),
         ("pulmonary_vein", "Pulmonary veins", "#d63031"),
         ("portal_vein", "Portal veins", "#8e44ad"), ("nerve", "Nerves", "#f1c40f")]
KIND_DEFAULTS = {key: colour for key, _, colour in KINDS}
KIND_LABELS = {"artery": "Artery", "vein": "Vein", "pulmonary_artery": "Pulmonary artery",
               "pulmonary_vein": "Pulmonary vein", "portal_vein": "Portal vein",
               "nerve": "Nerve"}
PALETTE = [("#d63031", "Red"), ("#2e6bd9", "Blue"), ("#8e44ad", "Purple"),
           ("#27ae60", "Green"), ("#e67e22", "Orange"), ("#f1c40f", "Yellow"),
           ("#e84393", "Pink"), ("#00a8a8", "Teal"), ("#8d5524", "Brown"),
           ("#ecf0f1", "White")]
# Browse without clicking the model (and the fallback when 3D is unavailable).
SYSTEMS = [("nervous", "Nervous"), ("cardiovascular", "Cardiovascular"),
           ("respiratory", "Respiratory"), ("digestive", "Digestive"), ("urinary", "Urinary"),
           ("endocrine", "Endocrine"), ("musculoskeletal", "Musculoskeletal"),
           ("integumentary", "Skin (integumentary)")]
SYSTEM_KEYS = {key for key, _text in SYSTEMS}      # every one has parts in the 3D model
SHOW_MAX = 8
LAYER_INDEX = {"skin": 0, "muscle": 1, "bone": 2, "organ": 3}     # slider position / 100


def search_index() -> dict[str, tuple[list[str], str]]:
    """Search entries for the part search: "shown text" -> (part ids, layer).

    One entry per part name (a name can cover several meshes, e.g. both
    halves of a muscle) and one per whole group ("Heart (whole organ)").
    Read from parts.json, the same list the 3D page uses.
    """
    from app.ui.components.anatomy_scheme import ANATOMY_DIR
    try:
        parts = json.loads((ANATOMY_DIR / "parts.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    by_name: dict[str, list[str]] = {}
    by_group: dict[str, list[str]] = {}
    layer_of: dict[str, str] = {}
    for part_id, part in parts.items():
        name = (part.get("name") or "").strip()
        if not name:
            continue
        by_name.setdefault(name, []).append(part_id)
        layer_of.setdefault(name, part.get("layer") or "")
        group = (part.get("group") or "").strip()
        if group:
            by_group.setdefault(group, []).append(part_id)
            layer_of.setdefault("group:" + group, part.get("layer") or "")
    index: dict[str, tuple[list[str], str]] = {}
    for group, ids in by_group.items():
        index[f"{group[:1].upper()}{group[1:]} (whole)"] = (ids, layer_of["group:" + group])
    for name, ids in by_name.items():
        layer = layer_of[name]
        index[f"{name[:1].upper()}{name[1:]} \u00b7 {LAYER_LABELS.get(layer, 'Part')}"] = (
            ids, layer)
    return dict(sorted(index.items(), key=lambda item: item[0].lower()))


GUIDE = [
    ("Rotate", "Drag with the left mouse button."),
    ("Move", "Drag with the right mouse button."),
    ("Zoom", "Scroll the mouse wheel."),
    ("Zoom in", "Click the body or a Regions button. Whole body goes back."),
    ("Search", "Type a part's name (femur, aorta, liver) and pick it: Akeso peels to it, "
               "flies there and makes it glow."),
    ("Peel", "Layers slider: Skin → Muscle → Bone → Organs."),
    ("Select", "Once zoomed in, click a part. Point at it to see its name."),
    ("Hide", "Hide button or H. Shift + H hides the whole group (e.g. all of the skull)."),
    ("See-through", "See-through button or T (Shift + T for the group). Again makes it solid."),
    ("Only this", "Only this button or O (Shift + O for the group)."),
    ("Focus", "Focus on system: only that body system's parts. Show all brings back the rest."),
    ("Reset", "Show all, or R. Esc clears the selection."),
    ("Vessels", "Blood vessels / Nerves switches under Layers. Peel to Bone to see them."),
    ("Colours", "Click a vessel, then a colour. Vessel colours recolours a whole kind."),
    ("Systems", "Body-system chips list conditions without using the model."),
]


class _Bridge(QObject):
    """What the page calls (through QWebChannel)."""

    page_ready = Signal()
    part_clicked = Signal(dict)
    region_moved = Signal(str)
    no_webgl = Signal()
    visibility = Signal(dict)
    extra_loaded = Signal(str)
    extra_failed = Signal(str)
    colours = Signal(dict)

    @Slot(str)
    def extraLoaded(self, name: str) -> None:  # noqa: N802
        self.extra_loaded.emit(name)

    @Slot(str)
    def extraFailed(self, name: str) -> None:  # noqa: N802
        self.extra_failed.emit(name)

    @Slot(str)
    def coloursChanged(self, payload: str) -> None:  # noqa: N802
        try:
            self.colours.emit(json.loads(payload))
        except ValueError:
            pass

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
    repair_requested = Signal()             # a 3D file is missing: Settings > Repair
    symptom_requested = Signal(str)
    article_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.web = None
        self._ready = False
        self._layer = 0.0
        self._extras = {"vessel": False, "nerve": False}
        self._colour_store = AnatomyColourStore()
        self._colours = self._colour_store.load()       # {"kinds": {}, "custom": {}}
        self._part: Optional[dict] = None
        self._swatches: Optional[QButtonGroup] = None
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        self._stage = QWidget()
        self._stage.setObjectName("panel")
        self._stage_layout = QVBoxLayout(self._stage)
        self._stage_layout.setContentsMargins(0, 0, 0, 0)
        self._placeholder = LoadingLabel("", "acMuted")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.set_loading("Loading the 3D body…")
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
        self._side.addWidget(self._build_search())       # above the long guide: in view
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
        layers.body.addWidget(label("ALSO SHOW", "acFieldLabel"))
        extras = QHBoxLayout()
        extras.setSpacing(6)
        self.extra_buttons: dict[str, QPushButton] = {}
        for key, text in EXTRAS:
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.toggled.connect(lambda on, k=key: self._set_extra(k, on))
            self.extra_buttons[key] = chip
            extras.addWidget(chip)
        extras.addStretch(1)
        layers.body.addLayout(extras)
        self.extra_note = LoadingLabel("", "acSmall", inline=True)
        self.extra_note.hide()
        layers.body.addWidget(self.extra_note)
        self.repair_button = button("Repair Akeso", "acPrimary", "rotate-ccw",
                                    self.repair_requested.emit)
        self.repair_button.hide()
        layers.body.addWidget(self.repair_button, 0, Qt.AlignmentFlag.AlignLeft)
        self._side.addWidget(layers)
        self.layers_card = layers
        self.colours_card = self._build_colours()
        self.colours_card.hide()
        self._side.addWidget(self.colours_card)


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

    # ---------------------------------------------------------------- search

    def _build_search(self) -> Card:
        """Find a part by name: it is peeled into view, flown to and glows."""
        card = Card("Find a body part", "", "search")
        self._index = search_index()
        self.search = QLineEdit()
        self.search.setObjectName("filterSearch")
        self.search.setPlaceholderText("Search a part, e.g. femur, aorta, liver\u2026")
        self.search.setClearButtonEnabled(True)
        self.search.setFixedHeight(36)
        completer = QCompleter(QStringListModel(list(self._index)), self.search)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setMaxVisibleItems(10)
        completer.activated.connect(self._find)
        self.search.setCompleter(completer)
        self.search.returnPressed.connect(self._find_typed)
        self.search.textEdited.connect(lambda _t: self.search_note.hide())
        card.body.addWidget(self.search)
        self.search_note = label("", "acSmall")
        self.search_note.hide()
        card.body.addWidget(self.search_note)
        if not self._index:
            self.search.setEnabled(False)
        return card

    def _find_typed(self) -> None:
        """Enter: the exact entry, else the first suggestion that contains it."""
        text = self.search.text().strip()
        if not text:
            return
        if text in self._index:
            self._find(text)
            return
        lower = text.lower()
        match = next((k for k in self._index if k.lower().startswith(lower)), None) \
            or next((k for k in self._index if lower in k.lower()), None)
        if match:
            self.search.setText(match)
            self._find(match)
        else:
            self.search_note.setText("No part with that name. Try another word, "
                                     "e.g. \u201cheart\u201d or \u201cfemur\u201d.")
            self.search_note.show()

    def _find(self, text: str) -> None:
        entry = self._index.get(text)
        if entry is None:
            return
        ids, layer = entry
        self.search.completer().popup().hide()
        if not self._ready:
            self.search_note.setText("The 3D body is still loading. Try again in a moment.")
            self.search_note.show()
            return
        # Peel to the part's own layer: outer layers fade away, it stays solid.
        if layer in LAYER_INDEX:
            self.slider.setValue(LAYER_INDEX[layer] * 100)
        elif layer in self._extras and not self._extras[layer]:
            self.extra_buttons[layer].setChecked(True)      # loads vessels / nerves
        name = text.split(" \u00b7 ")[0]
        self.search_note.setText(f"Showing: {name}.")
        self.search_note.show()
        self._js(f"akeso.findParts({json.dumps(ids)})")

    def _slider_moved(self, value: int) -> None:
        self._layer = value / 100
        index = min(3, int(self._layer + 0.5))
        self.layer_now.setText(f"Showing: {LAYER_NAMES[index]}")
        self._js(f"akeso.setLayer({self._layer:.2f})")

    # ------------------------------------------------------ vessels, nerves

    def _set_extra(self, key: str, on: bool) -> None:
        self._extras[key] = on
        if on and self.slider.value() < 200:
            # They sit under the skin and muscle: peel to Bone so they show.
            self.slider.setValue(200)
        self._js(f"akeso.setExtra({json.dumps(key)}, {'true' if on else 'false'})")
        if on and self._ready:
            LoadingHold.of(self, "_extra_hold").begin()   # loader shows for at least 3 s
            self.extra_note.set_loading("Loading… the first time takes a few seconds.")
            self.extra_note.show()
        self.colours_card.setVisible(any(self._extras.values()))
        self._update_legend()

    def _extra_failed(self, name: str) -> None:
        """vessel.glb / nerve.glb would not load: a damaged install. Offer Repair."""
        if LoadingHold.of(self, "_extra_hold").wait(self._extra_failed, name):
            return
        what = {"vessel": "blood vessels", "nerve": "nerves"}.get(name, "this layer")
        self.extra_note.setText(f"Couldn't load the {what}. A file of Akeso is missing or "
                                "damaged; Repair Akeso puts it back.")
        self.extra_note.show()
        self.repair_button.show()

    def _extra_loaded(self, _name: str) -> None:
        if LoadingHold.of(self, "_extra_hold").wait(self._extra_loaded, _name):
            return
        self.extra_note.hide()

    def _build_colours(self) -> Card:
        card = Card("Vessel colours", "Arteries red, veins blue. The lung arteries carry "
                    "oxygen-poor blood, so they are blue (and the lung veins red). Click a "
                    "colour to change a whole kind.", "palette")
        self._legend: dict[str, tuple] = {}
        for key, text, _default in KINDS:
            line = QHBoxLayout()
            line.setSpacing(8)
            chip = QPushButton()
            chip.setFixedSize(30, 20)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.setToolTip(f"Change the colour of all {text.lower()}")
            menu = QMenu(chip)
            for hex_, name in PALETTE:
                action = menu.addAction(self._dot(hex_), name)
                action.triggered.connect(
                    lambda _c=False, k=key, h=hex_: self._js(
                        f"akeso.setKindColor({json.dumps(k)}, {json.dumps(h)})"))
            menu.addSeparator()
            menu.addAction("Default colour").triggered.connect(
                lambda _c=False, k=key: self._js(
                    f"akeso.setKindColor({json.dumps(k)}, {json.dumps(KIND_DEFAULTS[k])})"))
            chip.setMenu(menu)
            name = label(text, "acRowTitle")
            line.addWidget(chip)
            line.addWidget(name, 1)
            self._legend[key] = (chip, name)
            card.body.addLayout(line)
        card.body.addWidget(button("Reset all colours", "acGhost", "rotate-ccw",
                                   lambda: self._js("akeso.resetAllColors()")),
                            0, Qt.AlignmentFlag.AlignLeft)
        self._update_legend()
        return card

    @staticmethod
    def _dot(hex_: str) -> QIcon:
        pixmap = QPixmap(14, 14)
        pixmap.fill(QColor(hex_))
        return QIcon(pixmap)

    @staticmethod
    def _swatch_style(hex_: str) -> str:
        ring = Theme.token("TEXT") if Theme.token("TEXT") else "#ffffff"
        return (f"QPushButton {{ background-color: {hex_}; border: 2px solid transparent; "
                f"border-radius: 6px; }} QPushButton:hover {{ border-color: {ring}; }} "
                f"QPushButton:checked {{ border: 3px solid {ring}; }} "
                "QPushButton::menu-indicator { width: 0px; }")

    def _kind_colour(self, kind: str) -> str:
        return self._colours["kinds"].get(kind) or KIND_DEFAULTS.get(kind, "#cccccc")

    def _update_legend(self) -> None:
        """Swatch colours, and only the kinds whose layer is switched on."""
        for key, (chip, text) in getattr(self, "_legend", {}).items():
            chip.setStyleSheet(self._swatch_style(self._kind_colour(key)))
            show = self._extras["nerve" if key == "nerve" else "vessel"]
            chip.setVisible(show)
            text.setVisible(show)

    def _colours_changed(self, colours: dict) -> None:
        """The page changed a colour: remember it, refresh the swatches."""
        self._colours = {"kinds": dict(colours.get("kinds") or {}),
                         "custom": dict(colours.get("custom") or {})}
        self._colour_store.save(self._colours)
        self._update_legend()
        self._mark_swatch()

    def _part_colour(self, part: dict) -> Optional[str]:
        kind = part.get("kind")
        if not kind:
            return None
        return self._colours["custom"].get(part.get("id", "")) or self._kind_colour(kind)

    def _mark_swatch(self) -> None:
        if self._swatches is None or not self._part:
            return
        current = (self._part_colour(self._part) or "").lower()
        for b in self._swatches.buttons():
            b.setChecked(b.property("hex") == current)

    def _colour_picker(self, part: dict) -> QVBoxLayout:
        """A row of colours for the selected vessel or nerve, plus Reset."""
        box = QVBoxLayout()
        box.setSpacing(4)
        box.addWidget(label("COLOUR", "acFieldLabel"))
        from app.ui.views.compare_view import FlowLayout
        host = QWidget()
        host.setObjectName("panel")
        flow = FlowLayout(6, 6)
        host.setLayout(flow)
        self._swatches = QButtonGroup(host)
        self._swatches.setExclusive(False)          # checks are set from the page's state
        pid = json.dumps(part["id"])
        for hex_, name in PALETTE:
            b = QPushButton()
            b.setCheckable(True)
            b.setFixedSize(24, 24)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setToolTip(name)
            b.setProperty("hex", hex_)
            b.setStyleSheet(self._swatch_style(hex_))
            b.clicked.connect(lambda _c=False, h=hex_: self._js(
                f"akeso.setColor({pid}, false, {json.dumps(h)})"))
            self._swatches.addButton(b)
            flow.addWidget(b)
        box.addWidget(host)
        reset = button("Back to the default colour", "acLink",
                       on_click=lambda: self._js(f"akeso.resetColor({pid}, false)"))
        box.addWidget(reset, 0, Qt.AlignmentFlag.AlignLeft)
        self._mark_swatch()
        return box

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
        self._part = part
        self._swatches = None
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
            kind = part.get("kind")
            chips.addWidget(pill(KIND_LABELS.get(kind) or LAYER_LABELS.get(part.get("layer"),
                                                                           "Part"), "acPill"))
        if system_label and not browsing:
            chips.addWidget(pill(system_label, "acPillGood"))
        if browsing:
            chips.addWidget(pill("Body system", "acPillGood"))
        chips.addStretch(1)
        self._part_body.addLayout(chips)
        system_key = part.get("system") or ""
        if system_key in SYSTEM_KEYS and self.web:
            name_of = dict(SYSTEMS).get(system_key, system_key.capitalize())
            text = ("Focus on this system" if browsing
                    else f"Focus on the {name_of.split(' (')[0].lower()} system")
            self._part_body.addWidget(
                button(text, "acGhost", "target",
                       lambda _c=False, k=system_key, t=system_label or name_of:
                       self.focus_system(k, t)),
                0, Qt.AlignmentFlag.AlignLeft)
        if part.get("fma"):
            self._part_body.addWidget(label(f"Anatomy ID: {part['fma']} (Foundational Model "
                                            "of Anatomy)", "acSmall"))
        if part.get("id") and not browsing and part.get("kind"):
            self._part_body.addLayout(self._colour_picker(part))
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

    def focus_system(self, key: str, title: str) -> None:
        """Show only the parts of one body system (Show all brings the rest
        back). Vessels and nerves are extra layers: switched on first."""
        if not self._ready:
            return
        extra = {"cardiovascular": "vessel", "nervous": "nerve"}.get(key)
        if extra and not self._extras.get(extra):
            self.extra_buttons[extra].setChecked(True)      # loads the layer
        self._js(f"akeso.isolateSystem({json.dumps(key)}, {json.dumps(title)})")

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
                                      "Use Repair Akeso to put them back.")
            self.repair_button.show()
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
        page.javaScriptConsoleMessage = self._console          # only errors, in the terminal
        self.web.setPage(page)
        page.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        self.bridge = _Bridge(self)
        self.bridge.page_ready.connect(self._page_ready)
        self.bridge.part_clicked.connect(self.part_selected.emit)
        self.bridge.region_moved.connect(self._region_moved)
        self.bridge.no_webgl.connect(self._no_webgl)
        self.bridge.visibility.connect(self._visibility)
        self.bridge.extra_loaded.connect(self._extra_loaded)
        self.bridge.extra_failed.connect(self._extra_failed)
        self.bridge.colours.connect(self._colours_changed)
        self.channel = QWebChannel(page)
        self.channel.registerObject("bridge", self.bridge)
        page.setWebChannel(self.channel)
        page.loadFinished.connect(lambda ok: self._apply_theme())
        self.web.setUrl(QUrl("akeso://anatomy/anatomy.html"))
        self._stage_layout.removeWidget(self._placeholder)
        self._placeholder.hide()
        self._stage_layout.addWidget(self.web)
        # The page draws its models one by one; the Akeso loader covers it
        # until everything is in (page_ready) or 3D turns out unavailable.
        self._web_loader = LoaderOverlay(self._stage, "Loading the 3D body…", opaque=True)
        LoadingHold.of(self, "_web_hold").begin()         # loader shows for at least 3 s
        self._web_loader.show_over()

    def _hide_web_loader(self) -> None:
        if LoadingHold.of(self, "_web_hold").wait(self._hide_web_loader):
            return
        if getattr(self, "_web_loader", None) is not None:
            self._web_loader.hide()

    @staticmethod
    def _console(level, message, line, source) -> None:
        """Errors from the 3D page go to the terminal (and the crash log of the
        packaged app), so "the vessels don't load" can be traced. Ordinary
        page messages stay quiet."""
        from PySide6.QtWebEngineCore import QWebEnginePage
        if level == QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel:
            import sys
            print(f"[3D body] {message} ({source.rsplit('/', 1)[-1]}:{line})", file=sys.stderr)

    def _page_ready(self) -> None:
        self._ready = True
        self._hide_web_loader()
        self._apply_theme()
        self._js(f"akeso.setColors({json.dumps(self._colours)})")
        if self._layer:
            self._js(f"akeso.setLayer({self._layer:.2f})")
        for key, on in self._extras.items():
            if on:                       # switched on before the page was ready
                self._js(f"akeso.setExtra({json.dumps(key)}, true)")

    def _no_webgl(self) -> None:
        """3D can't run here: say so and keep browsing by body system."""
        self._hide_web_loader()
        self.layers_card.setEnabled(False)
        self.colours_card.hide()
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
        self._update_legend()
        self._mark_swatch()
        self._apply_theme()
