"""Symptom Encyclopedia, full clinical monograph.

Lays out the 7-part reference entry as eight numbered sections, following
the reference build:

    1. Body system classification       5. Cardinal conditions linked
    2. Diagnostic weight & calibration  6. Emergency warning signs
    3. Clinical definition              7. Diagnostic correlation
    4. Common clinical etiologies       8. Academic citations

The left rail lists those sections, tracks reading progress as you scroll,
and cross-links the related entities. Conditions are clickable: the view
emits condition_chosen(disease_id) and the shell opens that disease.
"""

from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.theme import Theme
from app.models.symptom import AssociatedCondition, Symptom
from app.ui.views.compare_view import FlowLayout, WrapChip
from app.ui.views.section_highlight import SectionHighlighter

SEVERITY_COLOURS = {"severe": "#F43F5E", "moderate": "#F59E0B", "mild": "#10B981"}


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
    """One linked condition, with its typical severity."""

    clicked = Signal(str)

    def __init__(self, condition: AssociatedCondition) -> None:
        super().__init__()
        self.setObjectName("syConditionCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Inspect this condition in the Disease Encyclopedia")
        self._id = condition.disease_id

        row = QHBoxLayout(self)
        row.setContentsMargins(14, 10, 12, 10)
        text = QVBoxLayout()
        text.setSpacing(2)
        text.addWidget(_label(condition.name, "syConditionName"))
        severity = condition.severity or "Unclassified"
        meta = _label(f"Typical Severity: {severity}", "syConditionMeta", wrap=False)
        meta.setProperty("severity", severity.lower())
        text.addWidget(meta)
        row.addLayout(text, 1)
        row.addWidget(_label("\u203a", "syChevron", wrap=False))

    def mouseReleaseEvent(self, event) -> None:
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._id)
        super().mouseReleaseEvent(event)


class SymptomDetailView(QWidget):
    back_requested = Signal()
    condition_chosen = Signal(str)
    session_requested = Signal(str)     # "Add to Active Session"
    matching_requested = Signal(str)    # "Find Matching Diseases"
    case_requested = Signal(str)        # "Present Case" in peer discussions
    bookmark_toggled = Signal(str, bool)   # entry id, starred?

    SECTIONS = (
        ("system", "System Classification", "pulse"),
        ("weight", "Diagnostic Weight", "shield"),
        ("definition", "Clinical Definition", "book"),
        ("causes", "Common Causes", "stack"),
        ("conditions", "Associated Conditions", "heart"),
        ("redflags", "Emergency Red Flags", "alert"),
        ("correlation", "Diagnostic Correlation", "search"),
        ("references", "Clinical References", "book"),
    )

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self._symptom: Optional[Symptom] = None
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

        back = QPushButton("\u2190  Back to Symptoms")
        back.setObjectName("syBackButton")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)
        row.addWidget(back)

        self._title = _label("", "detailTitle", wrap=False)
        self._scientific = _label("", "detailScientific", wrap=False)
        row.addWidget(self._title)
        row.addWidget(self._scientific)
        row.addStretch(1)

        self._session_button = QPushButton("\u26a1  Add to Active Session")
        self._session_button.setObjectName("syPrimaryAction")
        self._session_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._session_button.clicked.connect(self._emit_session)
        row.addWidget(self._session_button)

        self._match_button = QPushButton("Find Matching Diseases")
        self._match_button.setObjectName("syGhostAction")
        self._match_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._match_button.clicked.connect(self._emit_matching)
        row.addWidget(self._match_button)

        self._bookmark = QPushButton("\u2606")
        self._bookmark.setObjectName("syBookmark")
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
        nav.setObjectName("syRailBox")
        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(12, 12, 12, 12)
        nav_layout.setSpacing(2)

        head = QHBoxLayout()
        head.addWidget(_label("PAGE SECTIONS", "sySectionLabel", wrap=False))
        head.addStretch(1)
        self._progress_label = _label("0%", "syProgress", wrap=False)
        head.addWidget(self._progress_label)
        nav_layout.addLayout(head)

        # Reading progress, same as the Disease Encyclopedia rail.
        self._progress_bar = QProgressBar()
        self._progress_bar.setObjectName("readProgress")
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setFixedHeight(3)
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        nav_layout.addWidget(self._progress_bar)
        nav_layout.addSpacing(6)

        # One highlighted link at a time. Checkable buttons are independent
        # unless they share an exclusive group, which is why clicking two
        # links used to leave both lit.
        self._rail_group = QButtonGroup(self)
        self._rail_group.setExclusive(True)

        for key, text, icon_name in self.SECTIONS:
            link = QPushButton(text)
            link.setObjectName("syRailLink")
            link.setCheckable(True)
            link.setCursor(Qt.CursorShape.PointingHandCursor)
            link.clicked.connect(lambda _c=False, k=key: self._scroll_to(k))
            self._rail_group.addButton(link)
            self._rail_links[key] = link
            nav_layout.addWidget(link)

        jump = QPushButton("Jump to Mother Book Citation")
        jump.setObjectName("syRailJump")
        jump.setCursor(Qt.CursorShape.PointingHandCursor)
        jump.clicked.connect(lambda: self._scroll_to("references"))
        nav_layout.addWidget(jump)
        layout.addWidget(nav)

        glance = QFrame()
        glance.setObjectName("syRailBox")
        self._glance = QGridLayout(glance)
        self._glance.setContentsMargins(12, 12, 12, 12)
        self._glance.setVerticalSpacing(8)
        layout.addWidget(glance)

        related = QFrame()
        related.setObjectName("syRailBox")
        self._related = QVBoxLayout(related)
        self._related.setContentsMargins(12, 12, 12, 12)
        self._related.setSpacing(8)
        layout.addWidget(related)
        layout.addStretch(1)
        return rail

    # ---------------------------------------------------------- sections

    def _section(self, key: str, number: int, title: str, icon_name: str,
                 style: str = "sySection") -> QVBoxLayout:
        card = QFrame()
        card.setObjectName(style)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 18)
        layout.setSpacing(10)

        danger = style == "syRedSection"
        head = QHBoxLayout()
        head.setSpacing(8)
        head.addWidget(_icon(icon_name, 16, "DANGER" if danger else "BADGE_TEXT"))
        heading = f"{number}. {title.upper()}" if number else title.upper()
        head.addWidget(_label(heading, "syRedHeading" if danger else "syHeading", wrap=False))
        head.addStretch(1)
        layout.addLayout(head)

        self._content.addWidget(card)
        self._sections[key] = card
        return layout

    def show_symptom(self, s: Symptom) -> None:
        self._symptom = s
        self._title.setText(s.name)
        self._scientific.setText(f"({s.scientific_name})" if s.scientific_name else "")
        starred = bool(self.bookmark_lookup(s.id)) if self.bookmark_lookup else False
        self._bookmark.blockSignals(True)
        self._bookmark.setChecked(starred)
        self._bookmark.setText("\u2605" if starred else "\u2606")
        self._bookmark.blockSignals(False)
        _clear(self._content)
        self._sections.clear()
        self._highlighter.clear()

        # 1. Body system classification & anatomical mapping
        layout = self._section("system", 1, "Body System Classification & Anatomical Mapping", "pulse")
        facts = QHBoxLayout()
        facts.setSpacing(12)
        for caption, value, style in (
                ("Primary Anatomical System", s.system_label, "syFactValue"),
                ("Formal Medical Synonym", s.scientific_name or "\u2014", "syFactAccent")):
            box = QFrame()
            box.setObjectName("syFactBox")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(14, 10, 14, 10)
            box_layout.setSpacing(2)
            box_layout.addWidget(_label(caption.upper(), "sySectionLabel", wrap=False))
            box_layout.addWidget(_label(value, style))
            facts.addWidget(box, 1)
        layout.addLayout(facts)

        # 2. Diagnostic weight & algorithmic specificity calibration
        layout = self._section("weight", 2, "Diagnostic Weight & Specificity Calibration", "shield")
        gauge_box = QFrame()
        gauge_box.setObjectName("syWeightBox")
        gauge = QVBoxLayout(gauge_box)
        gauge.setContentsMargins(16, 14, 16, 14)
        gauge.setSpacing(8)

        head = QHBoxLayout()
        head.addWidget(_label(
            f"Base Clinical Weight:  {s.diagnostic_weight} / 10", "syWeightValue", wrap=False))
        head.addStretch(1)
        tier = _label(s.tier_label, "syTierBadge", wrap=False)
        tier.setProperty("tier", s.tier_key)
        head.addWidget(tier)
        gauge.addLayout(head)

        bar = QProgressBar()
        bar.setObjectName("syWeightBar")
        bar.setProperty("tier", s.tier_key)
        bar.setRange(0, 10)
        bar.setValue(s.diagnostic_weight)
        bar.setTextVisible(False)
        bar.setFixedHeight(8)
        gauge.addWidget(bar)

        rationale = s.weight_rationale or (
            "Base weight used when this symptom is scored against candidate conditions.")
        row = QHBoxLayout()
        row.setSpacing(6)
        row.addWidget(_label("Clinical Rationale:", "syStrong", wrap=False), 0, Qt.AlignmentFlag.AlignTop)
        row.addWidget(_label(rationale, "syBody"), 1)
        gauge.addLayout(row)
        layout.addWidget(gauge_box)

        # 3. Clinical definition
        layout = self._section("definition", 3, "Clinical Definition & Diagnostic Value", "book")
        layout.addWidget(_label(s.description or "No definition recorded yet.", "syBodyLarge"))
        if s.tags:
            holder = QWidget()
            holder.setObjectName("panel")
            flow = FlowLayout()
            holder.setLayout(flow)
            for tag in s.tags:
                flow.addWidget(WrapChip(tag, "syChip"))
            layout.addWidget(holder)

        # 4. Common clinical etiologies
        layout = self._section("causes", 4, "Common Clinical Etiologies & Diagnostic Triggers", "stack")
        if s.causes:
            grid = QGridLayout()
            grid.setSpacing(10)
            for index, cause in enumerate(s.causes):
                item = QFrame()
                item.setObjectName("syCauseBox")
                item_layout = QHBoxLayout(item)
                item_layout.setContentsMargins(12, 9, 12, 9)
                item_layout.setSpacing(8)
                item_layout.addWidget(_label("\u25cf", "syBullet", wrap=False), 0,
                                      Qt.AlignmentFlag.AlignTop)
                item_layout.addWidget(_label(cause, "syItem"), 1)
                row, column = divmod(index, 2)
                grid.addWidget(item, row, column)
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            layout.addLayout(grid)
        else:
            layout.addWidget(_label("Etiologic investigation in progress.", "syMuted"))

        # 5. Cardinal conditions linked
        layout = self._section("conditions", 5, "Cardinal Conditions Linked in Knowledge Graph", "heart")
        if s.conditions:
            grid = QGridLayout()
            grid.setSpacing(10)
            for index, condition in enumerate(s.conditions):
                card = ConditionCard(condition)
                card.clicked.connect(self.condition_chosen.emit)
                row, column = divmod(index, 3)
                grid.addWidget(card, row, column)
            for column in range(3):
                grid.setColumnStretch(column, 1)
            layout.addLayout(grid)
        else:
            layout.addWidget(_label(
                "No condition in the Disease Encyclopedia lists this symptom yet. "
                "Links come from the disease_symptoms table.", "syMuted"))

        # 6. Emergency warning signs
        layout = self._section("redflags", 6, "Emergency Warning Signs & Critical Red Flags",
                               "alert", style="syRedSection")
        if s.red_flags:
            layout.addWidget(_label(
                "Immediate emergency evaluation is required if any of the "
                "following occur. In the Philippines, call 911.", "syFlagIntro"))
            for flag in s.red_flags:
                item = QFrame()
                item.setObjectName("syFlagBox")
                item_layout = QHBoxLayout(item)
                item_layout.setContentsMargins(12, 9, 12, 9)
                item_layout.setSpacing(8)
                item_layout.addWidget(_icon("alert", 14, "DANGER"), 0, Qt.AlignmentFlag.AlignTop)
                item_layout.addWidget(_label(flag, "syFlagItem"), 1)
                layout.addWidget(item)
        else:
            layout.addWidget(_label("No red-flag criteria recorded yet.", "syMuted"))

        # 7. Diagnostic correlation
        layout = self._section("correlation", 7, "Diagnostic Correlation", "search",
                               style="syCorrelation")
        layout.addWidget(_label(
            f"Review how {s.name} is weighted against candidate conditions, "
            "alongside onset, pattern and intensity.", "syCorrelationText"))
        button = QPushButton("Open Symptom Correlation")
        button.setObjectName("syPrimaryAction")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        button.clicked.connect(self._emit_session)
        layout.addWidget(button)

        # 8. Academic citations
        layout = self._section("references", 8, "Academic Citations & Mother Book References", "book")
        layout.addWidget(_label(
            "Two-tier academic provenance for medical students and clinicians.", "syMuted"))
        tiers = QHBoxLayout()
        tiers.setSpacing(12)
        mother = s.mother_book
        tiers.addWidget(self._reference_box(
            "TIER 1 \u2014 MOTHER BOOK",
            mother.source_name if mother else "Not recorded",
            mother.citation_text if mother else "", primary=True), 1)
        supporting = s.supporting_references
        tiers.addWidget(self._reference_box(
            "TIER 2 \u2014 SPECIFIC REFERENCE",
            supporting[0].source_name if supporting else "Not recorded",
            supporting[0].citation_text if supporting else "", primary=False), 1)
        layout.addLayout(tiers)

        if s.source_attribution or len(supporting) > 1:
            box = QFrame()
            box.setObjectName("syFactBox")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(14, 10, 14, 10)
            box_layout.setSpacing(4)
            box_layout.addWidget(_label(
                "CONSOLIDATED CLINICAL GUIDELINES & ATTRIBUTIONS", "sySectionLabel", wrap=False))
            if s.source_attribution:
                box_layout.addWidget(_label(f"\u2022  {s.source_attribution}", "syItem"))
            for reference in supporting[1:]:
                box_layout.addWidget(_label(f"\u2022  {reference.source_name}", "syItem"))
            layout.addWidget(box)

        # Peer discussions (Clinical Exchange feeds this once it is built)
        layout = self._section("peer", 0, "Recent Peer Case Discussions", "chat")
        row = QHBoxLayout()
        row.addWidget(_label(
            f"De-identified academic case reviews tagged with {s.name}.", "syMuted"), 1)
        present = QPushButton("+  Present Case")
        present.setObjectName("syPrimaryAction")
        present.setCursor(Qt.CursorShape.PointingHandCursor)
        present.clicked.connect(lambda: self.case_requested.emit(s.id))
        row.addWidget(present)
        layout.addLayout(row)
        layout.addWidget(_label("No peer discussions are linked to this entry yet.", "syEmptyCentre"))

        self._content.addStretch(1)
        self._fill_glance(s)
        self._fill_related(s)
        self._scroll.verticalScrollBar().setValue(0)
        # One event-loop turn later the sections have real positions.
        QTimer.singleShot(0, lambda: self._on_scrolled(
            self._scroll.verticalScrollBar().value()))

    @staticmethod
    def _reference_box(tier: str, source: str, citation: str, primary: bool) -> QFrame:
        box = QFrame()
        box.setObjectName("syRefPrimary" if primary else "syRef")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        layout.addWidget(_label(tier, "syRefTierPrimary" if primary else "syRefTier", wrap=False))
        layout.addWidget(_label(source, "syRefSource"))
        if citation:
            layout.addWidget(_label(citation, "syRefCitation"))
        layout.addStretch(1)
        return box

    # -------------------------------------------------------------- rail

    def _fill_glance(self, s: Symptom) -> None:
        _clear(self._glance)
        self._glance.addWidget(_label("AT-A-GLANCE METADATA", "sySectionLabel", wrap=False), 0, 0, 1, 2)
        rows = (
            ("Body System", s.system_label),
            ("Diagnostic Weight", f"{s.diagnostic_weight} / 10"),
            ("Severity Tier", s.tier_label),
            ("Common Causes", str(len(s.causes))),
            ("Linked Conditions", str(len(s.conditions))),
            ("Red Flags", str(len(s.red_flags))),
        )
        for index, (caption, value) in enumerate(rows, start=1):
            self._glance.addWidget(_label(caption, "syGlanceKey", wrap=False), index, 0)
            value_label = _label(value, "syGlanceValue")
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self._glance.addWidget(value_label, index, 1)

    def _fill_related(self, s: Symptom) -> None:
        _clear(self._related)
        head = QHBoxLayout()
        head.addWidget(_label("RELATED ENTITIES", "sySectionLabel", wrap=False))
        head.addStretch(1)
        head.addWidget(_label("CROSS-LINKS", "syCrossLinks", wrap=False))
        self._related.addLayout(head)

        if not s.conditions:
            self._related.addWidget(_label("No cross-links yet.", "syMuted"))
            return
        holder = QWidget()
        holder.setObjectName("panel")
        flow = FlowLayout()
        holder.setLayout(flow)
        for condition in s.conditions:
            chip = WrapChip(condition.name, "syRelatedChip")
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.setToolTip("Open in the Disease Encyclopedia")
            # WrapChip is a QLabel, so wire the click through mousePressEvent.
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
        target = max(widget.y() - 4, 0)
        bar.setValue(target)
        # Outline the section you landed on for a couple of seconds.
        self._highlighter.flash(widget)
        # At the bottom of the page the scrollbar cannot move any further,
        # so valueChanged never fires; refresh the highlight by hand.
        self._on_scrolled(bar.value())
        # The last sections share the final screen, so scroll position alone
        # would highlight the wrong one. The link you clicked wins.
        link = self._rail_links.get(key)
        if link is not None and bar.value() >= bar.maximum():
            link.setChecked(True)

    def _on_scrolled(self, value: int) -> None:
        """Update the reading-progress percentage and the active rail link."""
        bar = self._scroll.verticalScrollBar()
        percent = round(value / bar.maximum() * 100) if bar.maximum() else 0
        self._progress_label.setText(f"{percent}%")
        self._progress_bar.setValue(percent)

        # Sections report y() == 0 until the layout has run, so ignore those
        # (bar the first) or every link would look active at once.
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
        if self._symptom is not None:
            self.bookmark_toggled.emit(self._symptom.id, on)

    def _emit_session(self) -> None:
        if self._symptom is not None:
            self.session_requested.emit(self._symptom.id)

    def _emit_matching(self) -> None:
        if self._symptom is not None:
            self.matching_requested.emit(self._symptom.id)