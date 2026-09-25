"""Medicine Reference, full clinical monograph.

The 8-part entry, laid out as numbered sections with the same rail as the
Symptom Encyclopedia: section links, reading progress, at-a-glance metadata
and cross-links.

    1. Regulatory classification & pharmacologic class
    2. Nomenclature & Philippine commercial brands
    3. Clinical indications & approved therapeutic uses
    4. Dosage guidelines & administration protocols
    5. Adverse reactions & known side effects
    6. Contraindications & clinical precautions
    7. Interactions & storage
    8. Academic citations & mother book references

Plus the FDA black box warning (only when there is one), the diseases this
drug is listed against, and the peer discussion block.
"""

from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.models.medicine import LinkedCondition, MedicineMonograph
from app.ui.views.compare_view import FlowLayout, WrapChip
from app.ui.views.section_highlight import SectionHighlighter


def _label(text: str, name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(name)
    label.setWordWrap(wrap)
    return label


def _icon(name: str, size: int, token: str) -> QLabel:
    label = QLabel()
    label.setObjectName("panel")
    label.setFixedSize(size, size)
    label.setPixmap(icons.to_pixmap(icons.draw(name, size, Theme.token(token))))
    return label


def _clear(layout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item.widget() is not None:
            item.widget().hide()
            item.widget().deleteLater()
        elif item.layout() is not None:
            _clear(item.layout())


class ConditionCard(QFrame):
    """One disease this drug is listed against."""

    clicked = Signal(str)

    def __init__(self, condition: LinkedCondition) -> None:
        super().__init__()
        self.setObjectName("mdConditionCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Open in the Disease Encyclopedia")
        self._id = condition.disease_id

        row = QHBoxLayout(self)
        row.setContentsMargins(14, 10, 12, 10)
        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(_label(condition.name, "mdConditionName"))
        detail = condition.note or condition.severity
        if detail:
            text.addWidget(_label(detail, "mdConditionMeta"))
        row.addLayout(text, 1)
        row.addWidget(_label("\u203a", "mdChevron", wrap=False))

    def mouseReleaseEvent(self, event) -> None:
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._id)
        super().mouseReleaseEvent(event)


class MedicineMonographView(QWidget):
    back_requested = Signal()
    condition_chosen = Signal(str)
    case_requested = Signal(str)
    bookmark_toggled = Signal(str, bool)   # entry id, starred?

    SECTIONS = (
        ("classification", "Classification & Class", "pill"),
        ("names", "Names & Brands (PH)", "notebook"),
        ("indications", "Approved Indications", "pulse"),
        ("dosage", "Dosage & Regimen", "clock"),
        ("adverse", "Adverse Reactions", "alert"),
        ("contraindications", "Contraindications", "shield"),
        ("interactions", "Interactions & Storage", "stack"),
        ("blackbox", "Black Box Warning", "alert"),
        ("conditions", "Linked Conditions", "heart"),
        ("references", "Pharmacology References", "book"),
    )

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._medicine: Optional[MedicineMonograph] = None
        self._sections: dict[str, QWidget] = {}
        self._rail_links: dict[str, QPushButton] = {}
        # Set by the shell so an entry opens with its star already correct.
        self.bookmark_lookup = None
        self._highlighter = SectionHighlighter(self)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_top_bar())

        body = QHBoxLayout()
        body.setContentsMargins(22, 16, 10, 0)
        body.setSpacing(18)
        body.addWidget(self._build_rail())

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.verticalScrollBar().valueChanged.connect(self._on_scrolled)
        content = QWidget()
        content.setObjectName("panel")
        self._content = QVBoxLayout(content)
        self._content.setContentsMargins(0, 0, 14, 24)
        self._content.setSpacing(16)
        self._scroll.setWidget(content)
        body.addWidget(self._scroll, 1)
        root.addLayout(body, 1)

    # ------------------------------------------------------------ chrome

    def _build_top_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("detailTopBar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(22, 10, 22, 10)
        row.setSpacing(12)

        back = QPushButton("\u2190  Back to Medicines")
        back.setObjectName("mdBackButton")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)
        row.addWidget(back)

        self._title = _label("", "detailTitle", wrap=False)
        self._generic = _label("", "detailScientific", wrap=False)
        row.addWidget(self._title)
        row.addWidget(self._generic)
        row.addStretch(1)

        self._copy_button = QPushButton("Copy Clinical Monograph")
        self._copy_button.setObjectName("mdGhostAction")
        self._copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._copy_button.clicked.connect(self._copy_monograph)
        row.addWidget(self._copy_button)

        # Jumps to section 7 rather than pretending to run a checker.
        interactions = QPushButton("Check Interactions")
        interactions.setObjectName("mdPrimaryAction")
        interactions.setCursor(Qt.CursorShape.PointingHandCursor)
        interactions.clicked.connect(lambda: self._scroll_to("interactions"))
        row.addWidget(interactions)

        self._bookmark = QPushButton("\u2606")
        self._bookmark.setObjectName("mdBookmark")
        self._bookmark.setCheckable(True)
        self._bookmark.setFixedWidth(40)
        self._bookmark.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bookmark.setToolTip("Bookmark this entry (saved once Bookmarks is built)")
        self._bookmark.toggled.connect(self._on_bookmark_toggled)
        row.addWidget(self._bookmark)
        return bar

    def _build_rail(self) -> QWidget:
        rail = QWidget()
        rail.setObjectName("panel")
        rail.setFixedWidth(250)
        layout = QVBoxLayout(rail)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        nav = QFrame()
        nav.setObjectName("mdRailBox")
        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(12, 12, 12, 12)
        nav_layout.setSpacing(2)

        head = QHBoxLayout()
        head.addWidget(_label("PAGE SECTIONS", "mdSectionLabel", wrap=False))
        head.addStretch(1)
        self._progress_label = _label("0%", "mdProgress", wrap=False)
        head.addWidget(self._progress_label)
        nav_layout.addLayout(head)

        self._progress_bar = QProgressBar()
        self._progress_bar.setObjectName("readProgress")
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setFixedHeight(3)
        self._progress_bar.setRange(0, 100)
        nav_layout.addWidget(self._progress_bar)
        nav_layout.addSpacing(6)

        self._rail_group = QButtonGroup(self)
        self._rail_group.setExclusive(True)
        for key, text, _icon_name in self.SECTIONS:
            # "&&" renders one "&": a single "&" marks a shortcut key.
            link = QPushButton(text.replace("&", "&&"))
            link.setObjectName("mdRailLink")
            link.setCheckable(True)
            link.setCursor(Qt.CursorShape.PointingHandCursor)
            link.clicked.connect(lambda _c=False, k=key: self._scroll_to(k))
            self._rail_group.addButton(link)
            self._rail_links[key] = link
            nav_layout.addWidget(link)

        jump = QPushButton("Jump to Mother Book Citation")
        jump.setObjectName("mdRailJump")
        jump.setCursor(Qt.CursorShape.PointingHandCursor)
        jump.clicked.connect(lambda: self._scroll_to("references"))
        nav_layout.addWidget(jump)
        layout.addWidget(nav)

        glance = QFrame()
        glance.setObjectName("mdRailBox")
        self._glance = QGridLayout(glance)
        self._glance.setContentsMargins(12, 12, 12, 12)
        self._glance.setVerticalSpacing(8)
        layout.addWidget(glance)

        related = QFrame()
        related.setObjectName("mdRailBox")
        self._related = QVBoxLayout(related)
        self._related.setContentsMargins(12, 12, 12, 12)
        self._related.setSpacing(8)
        layout.addWidget(related)
        layout.addStretch(1)
        return rail

    # ---------------------------------------------------------- sections

    def _section(self, key: str, number: int, title: str, icon_name: str,
                 style: str = "mdSection") -> QVBoxLayout:
        card = QFrame()
        card.setObjectName(style)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 18)
        layout.setSpacing(10)

        danger = style == "mdRedSection"
        head = QHBoxLayout()
        head.setSpacing(8)
        head.addWidget(_icon(icon_name, 16, "DANGER" if danger else "BADGE_TEXT"))
        heading = f"{number}. {title.upper()}" if number else title.upper()
        head.addWidget(_label(heading, "mdRedHeading" if danger else "mdHeading", wrap=False))
        head.addStretch(1)
        layout.addLayout(head)

        self._content.addWidget(card)
        self._sections[key] = card
        return layout

    @staticmethod
    def _tile_grid(items: list[str], style: str, marker: str, columns: int = 2) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(10)
        for index, text in enumerate(items):
            tile = QFrame()
            tile.setObjectName(style)
            tile_layout = QHBoxLayout(tile)
            tile_layout.setContentsMargins(12, 9, 12, 9)
            tile_layout.setSpacing(8)
            tile_layout.addWidget(_label(marker, f"{style}Marker", wrap=False), 0,
                                  Qt.AlignmentFlag.AlignTop)
            tile_layout.addWidget(_label(text, "mdItem"), 1)
            row, column = divmod(index, columns)
            grid.addWidget(tile, row, column)
        for column in range(columns):
            grid.setColumnStretch(column, 1)
        return grid

    def show_medicine(self, m: MedicineMonograph) -> None:
        self._medicine = m
        self._title.setText(m.name)
        self._generic.setText(f"(Generic: {m.generic_label})")
        starred = bool(self.bookmark_lookup(m.id)) if self.bookmark_lookup else False
        self._bookmark.blockSignals(True)
        self._bookmark.setChecked(starred)
        self._bookmark.setText("\u2605" if starred else "\u2606")
        self._bookmark.blockSignals(False)
        self._copy_button.setText("Copy Clinical Monograph")
        _clear(self._content)
        self._sections.clear()
        self._highlighter.clear()

        # 1. Regulatory classification
        layout = self._section("classification", 1,
                               "Regulatory Classification & Pharmacologic Class", "pill")
        facts = QHBoxLayout()
        facts.setSpacing(12)
        for caption, value, style in (
                ("Category", m.category_display, "mdFactValue"),
                ("Therapeutic Class", m.drug_class or "\u2014", "mdFactAccent")):
            box = QFrame()
            box.setObjectName("mdFactBox")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(14, 10, 14, 10)
            box_layout.setSpacing(2)
            box_layout.addWidget(_label(caption.upper(), "mdSectionLabel", wrap=False))
            box_layout.addWidget(_label(value, style))
            facts.addWidget(box, 1)
        layout.addLayout(facts)

        # 2. Nomenclature & brands
        layout = self._section("names", 2, "Nomenclature & Philippine Commercial Brands",
                               "notebook")
        generic_box = QFrame()
        generic_box.setObjectName("mdFactBox")
        generic_layout = QHBoxLayout(generic_box)
        generic_layout.setContentsMargins(14, 10, 14, 10)
        generic_layout.setSpacing(6)
        generic_layout.addWidget(_label("International Generic Name:", "mdStrong", wrap=False))
        generic_layout.addWidget(_label(m.generic_label, "mdFactAccent"))
        generic_layout.addStretch(1)
        layout.addWidget(generic_box)

        brands = QHBoxLayout()
        brands.setSpacing(12)
        for caption, items in (("Philippine Commercial Brands", m.ph_brands),
                               ("International Reference Brands", m.intl_brands)):
            box = QFrame()
            box.setObjectName("mdFactBox")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(14, 10, 14, 10)
            box_layout.setSpacing(4)
            box_layout.addWidget(_label(caption, "mdStrong"))
            box_layout.addWidget(_label(", ".join(items) if items else "None recorded yet.",
                                        "mdItem"))
            brands.addWidget(box, 1)
        layout.addLayout(brands)

        notice = QFrame()
        notice.setObjectName("mdNotice")
        notice_layout = QVBoxLayout(notice)
        notice_layout.setContentsMargins(14, 10, 14, 10)
        notice_layout.addWidget(_label(
            "Regulatory verification notice: confirm local brand availability with "
            "a dispensing pharmacy before relying on it; distributor licences and "
            "regional stock change over time.", "mdNoticeText"))
        layout.addWidget(notice)

        # 3. Indications
        layout = self._section("indications", 3,
                               "Clinical Indications & Approved Therapeutic Uses", "check")
        if m.indications:
            layout.addLayout(self._tile_grid(m.indications, "mdGoodTile", "\u2713"))
        else:
            layout.addWidget(_label("No approved indications recorded yet.", "mdMuted"))

        # 4. Dosage
        layout = self._section("dosage", 4, "Dosage Guidelines & Administration Protocols",
                               "clock")
        dosage = QFrame()
        dosage.setObjectName("mdDosageBox")
        dosage_layout = QVBoxLayout(dosage)
        dosage_layout.setContentsMargins(16, 12, 16, 12)
        dosage_layout.addWidget(_label(
            m.dosage_text or "No dosing recorded yet.", "mdDosageText"))
        layout.addWidget(dosage)
        layout.addWidget(_label(
            "Educational reference only. Dosing is individual: always follow the "
            "prescriber and the product insert.", "mdMuted"))

        # 5. Adverse reactions
        layout = self._section("adverse", 5, "Adverse Reactions & Known Side Effects", "alert")
        if m.adverse_reactions:
            layout.addLayout(self._tile_grid(m.adverse_reactions, "mdWarnTile", "\u25cf", 3))
        else:
            layout.addWidget(_label("No adverse reactions recorded yet.", "mdMuted"))

        # 6. Contraindications
        layout = self._section("contraindications", 6,
                               "Contraindications & Clinical Precautions", "shield")
        if m.contraindications:
            layout.addLayout(self._tile_grid(m.contraindications, "mdBadTile", "\u2715"))
        else:
            layout.addWidget(_label("No contraindications recorded yet.", "mdMuted"))

        # 7. Interactions & storage, side by side
        layout = self._section("interactions", 7, "Interactions & Storage", "stack")
        columns = QHBoxLayout()
        columns.setSpacing(12)

        interactions_box = QFrame()
        interactions_box.setObjectName("mdFactBox")
        box_layout = QVBoxLayout(interactions_box)
        box_layout.setContentsMargins(14, 10, 14, 12)
        box_layout.setSpacing(8)
        box_layout.addWidget(_label("DRUG-DRUG & FOOD INTERACTIONS", "mdSectionLabel", wrap=False))
        if m.interactions:
            for item in m.interactions:
                box_layout.addWidget(_label(f"\u25cf  {item}", "mdItem"))
        else:
            box_layout.addWidget(_label("None recorded yet.", "mdMuted"))
        columns.addWidget(interactions_box, 1)

        storage_box = QFrame()
        storage_box.setObjectName("mdFactBox")
        storage_layout = QVBoxLayout(storage_box)
        storage_layout.setContentsMargins(14, 10, 14, 12)
        storage_layout.setSpacing(8)
        storage_layout.addWidget(_label("STORAGE & DISPENSING", "mdSectionLabel", wrap=False))
        storage_layout.addWidget(_label(m.storage or "No storage guidance recorded yet.",
                                        "mdItem"))
        storage_layout.addStretch(1)
        columns.addWidget(storage_box, 1)
        layout.addLayout(columns)

        # Black box warning: only when there is one.
        if m.has_black_box:
            layout = self._section("blackbox", 0, "FDA Black Box Warning", "alert",
                                   style="mdRedSection")
            layout.addWidget(_label(m.black_box_warning, "mdBlackBoxText"))
        self._rail_links["blackbox"].setEnabled(m.has_black_box)

        # Linked conditions
        layout = self._section("conditions", 0,
                               f"Primary Disease Applications ({len(m.conditions)})", "heart")
        if m.conditions:
            grid = QGridLayout()
            grid.setSpacing(10)
            for index, condition in enumerate(m.conditions):
                card = ConditionCard(condition)
                card.clicked.connect(self.condition_chosen.emit)
                row, column = divmod(index, 3)
                grid.addWidget(card, row, column)
            for column in range(3):
                grid.setColumnStretch(column, 1)
            layout.addLayout(grid)
        else:
            layout.addWidget(_label(
                "No condition in the Disease Encyclopedia lists this medicine yet. "
                "Links come from the disease_medicines table.", "mdMuted"))

        # 8. References
        layout = self._section("references", 8, "Academic Citations & Mother Book References",
                               "book")
        layout.addWidget(_label(
            "Two-tier academic provenance for medical students and clinicians.", "mdMuted"))
        tiers = QHBoxLayout()
        tiers.setSpacing(12)
        mother = m.mother_book
        supporting = m.supporting_references
        tiers.addWidget(self._reference_box(
            "TIER 1 \u2014 MOTHER BOOK",
            mother.source_name if mother else "Not recorded",
            mother.citation_text if mother else "", primary=True), 1)
        tiers.addWidget(self._reference_box(
            "TIER 2 \u2014 SPECIFIC REFERENCE",
            supporting[0].source_name if supporting else "Not recorded",
            supporting[0].citation_text if supporting else "", primary=False), 1)
        layout.addLayout(tiers)

        if m.source_attribution or len(supporting) > 1:
            box = QFrame()
            box.setObjectName("mdFactBox")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(14, 10, 14, 10)
            box_layout.setSpacing(4)
            box_layout.addWidget(_label(
                "CONSOLIDATED CLINICAL GUIDELINES & ATTRIBUTIONS", "mdSectionLabel", wrap=False))
            for line in [s.strip() for s in m.source_attribution.split(";") if s.strip()]:
                box_layout.addWidget(_label(f"\u2022  {line}", "mdItem"))
            for reference in supporting[1:]:
                box_layout.addWidget(_label(f"\u2022  {reference.source_name}", "mdItem"))
            layout.addWidget(box)

        # Peer discussions
        layout = self._section("peer", 0, "Recent Peer Case Discussions", "chat")
        row = QHBoxLayout()
        row.addWidget(_label(
            f"De-identified academic case reviews tagged with {m.name}.", "mdMuted"), 1)
        present = QPushButton("+  Present Case")
        present.setObjectName("mdPrimaryAction")
        present.setCursor(Qt.CursorShape.PointingHandCursor)
        present.clicked.connect(lambda: self.case_requested.emit(m.id))
        row.addWidget(present)
        layout.addLayout(row)
        layout.addWidget(_label("No peer discussions are linked to this entry yet.",
                                "mdEmptyCentre"))

        self._content.addStretch(1)
        self._fill_glance(m)
        self._fill_related(m)
        self._scroll.verticalScrollBar().setValue(0)
        QTimer.singleShot(0, lambda: self._on_scrolled(
            self._scroll.verticalScrollBar().value()))

    @staticmethod
    def _reference_box(tier: str, source: str, citation: str, primary: bool) -> QFrame:
        box = QFrame()
        box.setObjectName("mdRefPrimary" if primary else "mdRef")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        layout.addWidget(_label(tier, "mdRefTierPrimary" if primary else "mdRefTier", wrap=False))
        layout.addWidget(_label(source, "mdRefSource"))
        if citation:
            layout.addWidget(_label(citation, "mdRefCitation"))
        layout.addStretch(1)
        return box

    # -------------------------------------------------------------- rail

    def _fill_glance(self, m: MedicineMonograph) -> None:
        _clear(self._glance)
        self._glance.addWidget(_label("AT-A-GLANCE METADATA", "mdSectionLabel", wrap=False),
                               0, 0, 1, 2)
        rows = (
            ("Category", "OTC" if m.is_otc else "Rx"),
            ("Drug Class", m.drug_class or "\u2014"),
            ("Philippine Brands", f"{len(m.ph_brands)} brands"),
            ("Indications", str(len(m.indications))),
            ("Storage", m.storage_summary or "\u2014"),
            ("Black Box Warning", "Present" if m.has_black_box else "None"),
        )
        for index, (caption, value) in enumerate(rows, start=1):
            self._glance.addWidget(_label(caption, "mdGlanceKey", wrap=False), index, 0)
            value_label = _label(value, "mdGlanceValue")
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            if caption == "Black Box Warning" and m.has_black_box:
                value_label.setObjectName("mdGlanceDanger")
            self._glance.addWidget(value_label, index, 1)

    def _fill_related(self, m: MedicineMonograph) -> None:
        _clear(self._related)
        head = QHBoxLayout()
        head.addWidget(_label("RELATED ENTITIES", "mdSectionLabel", wrap=False))
        head.addStretch(1)
        head.addWidget(_label("CROSS-LINKS", "mdCrossLinks", wrap=False))
        self._related.addLayout(head)

        if not m.conditions:
            self._related.addWidget(_label("No cross-links yet.", "mdMuted"))
            return
        self._related.addWidget(_label("Linked Conditions:", "mdMuted"))
        holder = QWidget()
        holder.setObjectName("panel")
        flow = FlowLayout()
        holder.setLayout(flow)
        for condition in m.conditions:
            chip = WrapChip(condition.name, "mdRelatedChip")
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.setToolTip("Open in the Disease Encyclopedia")
            chip.mousePressEvent = (
                lambda _e, did=condition.disease_id: self.condition_chosen.emit(did))
            flow.addWidget(chip)
        self._related.addWidget(holder)

    # ------------------------------------------------------- interaction

    def _scroll_to(self, key: str) -> None:
        widget = self._sections.get(key)
        if widget is None:
            return
        bar = self._scroll.verticalScrollBar()
        bar.setValue(max(widget.y() - 4, 0))
        self._highlighter.flash(widget)
        self._on_scrolled(bar.value())
        link = self._rail_links.get(key)
        if link is not None and bar.value() >= bar.maximum():
            link.setChecked(True)

    def _on_scrolled(self, value: int) -> None:
        bar = self._scroll.verticalScrollBar()
        percent = round(value / bar.maximum() * 100) if bar.maximum() else 0
        self._progress_label.setText(f"{percent}%")
        self._progress_bar.setValue(percent)

        current = self.SECTIONS[0][0]
        for key, _text, _icon_name in self.SECTIONS:
            widget = self._sections.get(key)
            if widget is None or widget.y() == 0:
                continue
            if widget.y() <= value + 80:
                current = key
        for key, link in self._rail_links.items():
            link.setChecked(key == current)

    def _on_bookmark_toggled(self, on: bool) -> None:
        self._bookmark.setText("\u2605" if on else "\u2606")
        if self._medicine is not None:
            self.bookmark_toggled.emit(self._medicine.id, on)

    def _copy_monograph(self) -> None:
        if self._medicine is not None:
            QApplication.clipboard().setText(self._medicine.as_text())
            self._copy_button.setText("Copied")