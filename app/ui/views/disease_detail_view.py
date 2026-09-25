"""Disease monograph — the Inspect Entry page.

Display only. It renders a fully hydrated Disease and announces what the user
clicked. It never fetches anything.

Every section is registered through _add_section(), which builds the card,
adds the matching TOC button, and records the scroll anchor in one step — so
the nav can never list a section the page does not have.

Sections appear only when their data exists. An empty "Pharmacotherapy" header
on a clinical page reads as a failed load, and a condition with no linked
drugs should say nothing rather than show a blank frame.
"""

from typing import Optional

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
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
from app.core.models_helpers import urgency_style
from app.core.theme import Theme
from app.models.disease import Disease, Medicine, SymptomLink
from app.ui.views.section_highlight import SectionHighlighter

# key, TOC label, icon name
SECTION_META = {
    "triage": ("Triage & Urgency", "alert"),
    "summary": ("Clinical Summary", "book"),
    "pathophysiology": ("Pathophysiology", "pulse"),
    "causes": ("Causes & Etiology", "stack"),
    "symptoms": ("Cardinal Symptoms", "pulse"),
    "differentials": ("Differential Diagnosis", "search"),
    "prevention": ("Prevention Tiers", "shield"),
    "treatments": ("Treatments & Tests", "heart"),
    "monitoring": ("Monitoring Plan", "clock"),
    "pharmacotherapy": ("Pharmacotherapy", "pill"),
    "redflags": ("Emergency Red Flags", "alert"),
    "references": ("Textbook References", "book"),
}


def _card(object_name: str = "detailCard") -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setObjectName(object_name)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(22, 20, 22, 20)
    layout.setSpacing(13)
    return frame, layout


def _heading(text: str, icon_name: str, color: Optional[str] = None) -> QWidget:
    row = QWidget()
    row.setObjectName("panel")
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(9)

    glyph = QLabel()
    glyph.setObjectName("panel")
    glyph.setPixmap(
        icons.to_pixmap(
            icons.draw(icon_name, 15, color or Theme.token("BADGE_TEXT"))
        )
    )
    glyph.setFixedSize(15, 15)

    label = QLabel(text.upper())
    label.setObjectName("sectionHeading")

    layout.addWidget(glyph)
    layout.addWidget(label)
    layout.addStretch(1)
    return row


def _body(text: str, object_name: str = "bodyText") -> QLabel:
    label = QLabel(text)
    label.setObjectName(object_name)
    label.setWordWrap(True)
    return label


def _chip(text: str, object_name: str) -> QLabel:
    chip = QLabel(text)
    chip.setObjectName(object_name)
    chip.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
    return chip


class Tile(QFrame):
    """A bordered list item with a leading marker."""

    def __init__(
            self, text: str, marker: str = "\u25CF", variant: str = "default"
    ) -> None:
        super().__init__()
        self.setObjectName(
            {
                "danger": "bulletTileDanger",
                "success": "bulletTileSuccess",
            }.get(variant, "bulletTile")
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 11, 14, 11)
        layout.setSpacing(10)

        dot = QLabel(marker)
        dot.setObjectName(
            {
                "danger": "bulletDotDanger",
                "success": "bulletDotSuccess",
            }.get(variant, "bulletDot")
        )
        dot.setFixedWidth(13)
        dot.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        label = QLabel(text)
        label.setObjectName("bulletText")
        label.setWordWrap(True)

        layout.addWidget(dot)
        layout.addWidget(label, 1)


class SymptomTile(QFrame):
    """One cardinal or associated symptom, with intensity."""

    inspect_requested = Signal(str)

    def __init__(self, symptom: SymptomLink) -> None:
        super().__init__()
        self._symptom = symptom
        self.setObjectName("symptomTile")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 13, 15, 13)
        layout.setSpacing(8)

        top = QHBoxLayout()
        top.setSpacing(8)

        name = QLabel(symptom.name or symptom.symptom_id)
        name.setObjectName("symptomName")
        name.setWordWrap(True)
        top.addWidget(name, 1)

        if symptom.is_primary:
            top.addWidget(_chip("Cardinal Sign", "cardinalChip"))
        layout.addLayout(top)

        bottom = QHBoxLayout()
        intensity = QLabel(f"Intensity: {symptom.intensity_label}")
        intensity.setObjectName("metaLabel")

        inspect = QPushButton("Inspect  \u203A")
        inspect.setObjectName("inspectLink")
        inspect.setCursor(Qt.CursorShape.PointingHandCursor)
        inspect.clicked.connect(
            lambda: self.inspect_requested.emit(symptom.symptom_id)
        )

        bottom.addWidget(intensity)
        bottom.addStretch(1)
        bottom.addWidget(inspect)
        layout.addLayout(bottom)


class MedicineTile(QFrame):
    """One linked drug in the pharmacotherapy strip."""

    open_requested = Signal(str)

    def __init__(self, medicine: Medicine) -> None:
        super().__init__()
        self.setObjectName("medicineTile")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 13, 15, 13)
        layout.setSpacing(6)

        top = QHBoxLayout()
        top.setSpacing(8)
        top.addWidget(
            _chip(
                medicine.category,
                "rxChip" if medicine.category == "Prescription" else "otcChip",
            )
        )
        top.addStretch(1)

        drug_class = QLabel(medicine.drug_class)
        drug_class.setObjectName("metaLabel")
        drug_class.setMaximumWidth(190)
        # Long class names would otherwise force the tile wider than its
        # column; elide instead of wrapping to keep tiles the same height.
        metrics = drug_class.fontMetrics()
        drug_class.setText(
            metrics.elidedText(
                medicine.drug_class, Qt.TextElideMode.ElideRight, 190
            )
        )
        drug_class.setToolTip(medicine.drug_class)
        top.addWidget(drug_class)
        layout.addLayout(top)

        name = QLabel(medicine.name)
        name.setObjectName("symptomName")
        name.setWordWrap(True)
        layout.addWidget(name)

        if medicine.generic_name:
            generic = QLabel(f"Generic: {medicine.generic_name}")
            generic.setObjectName("cardScientificName")
            generic.setWordWrap(True)
            layout.addWidget(generic)

        open_btn = QPushButton("Open Pharmacology  \u203A")
        open_btn.setObjectName("inspectLink")
        open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_btn.clicked.connect(
            lambda: self.open_requested.emit(medicine.id)
        )
        layout.addWidget(open_btn, 0, Qt.AlignmentFlag.AlignLeft)


class DiseaseDetailView(QWidget):
    """The full clinical monograph for one condition."""

    back_requested = Signal()
    bookmark_toggled = Signal(str, bool)
    check_symptoms_requested = Signal(str)
    compare_requested = Signal(str)
    symptom_requested = Signal(str)
    medicine_requested = Signal(str)
    case_requested = Signal(str)          # "Present Case" in peer discussions

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")

        self._disease: Optional[Disease] = None
        self._anchors: dict[str, QWidget] = {}
        self._toc_buttons: dict[str, QPushButton] = {}
        self._active_key: Optional[str] = None
        self._highlighter = SectionHighlighter(self)
        self._bookmarked = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_top_bar())

        body = QWidget()
        body.setObjectName("panel")
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(22, 18, 22, 22)
        body_layout.setSpacing(20)
        body_layout.addWidget(self._build_left_rail())
        body_layout.addWidget(self._build_content_scroll(), 1)

        root.addWidget(body, 1)

    # ------------------------------------------------------------- top bar

    def _build_top_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("detailTopBar")
        bar.setFixedHeight(58)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(22, 0, 22, 0)
        layout.setSpacing(12)

        back = QPushButton("  \u2190  Back to Conditions")
        back.setObjectName("secondaryButton")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(lambda _checked: self.back_requested.emit())

        self._title_label = QLabel("")
        self._title_label.setObjectName("detailTitle")

        self._scientific_label = QLabel("")
        self._scientific_label.setObjectName("detailScientific")

        self._check_btn = QPushButton("  Check Symptoms")
        self._check_btn.setObjectName("primaryButton")
        self._check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._check_btn.setIcon(
            QIcon(icons.to_pixmap(icons.pulse(14, "#FFFFFF")))
        )
        self._check_btn.setIconSize(QSize(14, 14))
        self._check_btn.clicked.connect(self._emit_check_symptoms)

        self._compare_btn = QPushButton("  Compare Condition")
        self._compare_btn.setObjectName("secondaryButton")
        self._compare_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._compare_btn.clicked.connect(self._emit_compare)

        self._bookmark_btn = QPushButton()
        self._bookmark_btn.setObjectName("bookmarkButton")
        self._bookmark_btn.setFixedSize(34, 34)
        self._bookmark_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bookmark_btn.clicked.connect(self._toggle_bookmark)

        layout.addWidget(back)
        layout.addWidget(self._title_label)
        layout.addWidget(self._scientific_label)
        layout.addStretch(1)
        layout.addWidget(self._check_btn)
        layout.addWidget(self._compare_btn)
        layout.addWidget(self._bookmark_btn)
        return bar

    # ----------------------------------------------------------- left rail

    def _build_left_rail(self) -> QWidget:
        rail = QScrollArea()
        rail.setWidgetResizable(True)
        rail.setFrameShape(QFrame.Shape.NoFrame)
        rail.setFixedWidth(252)
        rail.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        holder = QWidget()
        holder.setObjectName("panel")
        layout = QVBoxLayout(holder)
        layout.setContentsMargins(0, 0, 6, 0)
        layout.setSpacing(14)

        layout.addWidget(self._build_toc_card())
        layout.addWidget(self._build_metadata_card())
        layout.addWidget(self._build_related_card())
        layout.addStretch(1)

        rail.setWidget(holder)
        return rail

    def _build_toc_card(self) -> QWidget:
        card, layout = _card()
        layout.setSpacing(4)

        header = QHBoxLayout()
        heading = QLabel("PAGE SECTIONS")
        heading.setObjectName("railHeading")

        self._progress_label = QLabel("0%")
        self._progress_label.setObjectName("progressLabel")

        header.addWidget(heading)
        header.addStretch(1)
        header.addWidget(self._progress_label)
        layout.addLayout(header)

        self._progress_bar = QProgressBar()
        self._progress_bar.setObjectName("readProgress")
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setFixedHeight(3)
        self._progress_bar.setRange(0, 100)
        layout.addWidget(self._progress_bar)

        self._toc_layout = layout
        layout.addStretch(1)
        return card

    def _build_metadata_card(self) -> QWidget:
        card, layout = _card()

        heading = QLabel("AT-A-GLANCE METADATA")
        heading.setObjectName("railHeading")
        layout.addWidget(heading)

        self._meta_grid = QGridLayout()
        self._meta_grid.setContentsMargins(0, 2, 0, 0)
        self._meta_grid.setHorizontalSpacing(10)
        self._meta_grid.setVerticalSpacing(9)
        self._meta_grid.setColumnStretch(0, 1)
        layout.addLayout(self._meta_grid)
        return card

    def _build_related_card(self) -> QWidget:
        self._related_card, layout = _card()

        header = QHBoxLayout()
        heading = QLabel("RELATED ENTITIES")
        heading.setObjectName("railHeading")
        link = QLabel("CROSS-LINKS")
        link.setObjectName("linkLabel")
        header.addWidget(heading)
        header.addStretch(1)
        header.addWidget(link)
        layout.addLayout(header)

        self._related_layout = layout
        return self._related_card

    # -------------------------------------------------------- content area

    def _build_content_scroll(self) -> QWidget:
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        holder = QWidget()
        holder.setObjectName("panel")
        self._content_layout = QVBoxLayout(holder)
        self._content_layout.setContentsMargins(0, 0, 8, 20)
        self._content_layout.setSpacing(17)
        self._content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._scroll.setWidget(holder)
        self._scroll.verticalScrollBar().valueChanged.connect(
            self._on_scrolled
        )
        return self._scroll

    # ---------------------------------------------------------- public api

    def show_disease(self, disease: Disease, bookmarked: bool = False) -> None:
        """Render a fully hydrated Disease. Safe to call repeatedly."""
        self._disease = disease
        self._bookmarked = bookmarked

        self._title_label.setText(disease.name)
        self._scientific_label.setText(
            f"({disease.scientific_name})" if disease.scientific_name else ""
        )
        self._refresh_bookmark_icon()

        self._clear()
        self._build_sections(disease)
        self._fill_metadata(disease)
        self._fill_related(disease)

        self._scroll.verticalScrollBar().setValue(0)
        self._on_scrolled(0)

    # ------------------------------------------------------------ sections

    def _clear(self) -> None:
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._anchors.clear()
        self._highlighter.clear()

        for button in self._toc_buttons.values():
            self._toc_layout.removeWidget(button)
            button.deleteLater()
        self._toc_buttons.clear()
        self._active_key = None

    def _build_sections(self, d: Disease) -> None:
        """Order matters: this is the reading order of the monograph."""
        self._add("triage", self._triage(d))
        self._add("summary", self._summary(d))

        if d.pathophysiology:
            self._add("pathophysiology", self._pathophysiology(d))
        if d.causes:
            self._add("causes", self._causes(d))
        if d.symptoms:
            self._add("symptoms", self._symptoms(d), badge=str(len(d.symptoms)))
        if d.differential_diagnosis:
            self._add("differentials", self._differentials(d))
        if d.prevention_tiers or d.prevention:
            self._add("prevention", self._prevention(d))
        if d.treatments or d.recommended_tests:
            self._add("treatments", self._treatments(d))
        if d.follow_up_monitoring:
            self._add("monitoring", self._monitoring(d))
        if d.medicines:
            self._add(
                "pharmacotherapy",
                self._pharmacotherapy(d),
                badge=str(len(d.medicines)),
            )
        if d.emergency_warning_signs:
            self._add("redflags", self._redflags(d))
        if d.clinical_references:
            badge = "2-Tier" if d.chapter_references else "1-Tier"
            self._add("references", self._references(d), badge=badge)

        # Always last, and deliberately not in the table of contents: it is
        # a discussion thread about the entry, not part of the monograph.
        self._content_layout.addWidget(self._discussion(d))

    def _add(self, key: str, widget: QWidget, badge: str = "") -> None:
        """Place a section and give it a matching TOC button."""
        self._content_layout.addWidget(widget)
        self._anchors[key] = widget

        label, icon_name = SECTION_META[key]

        # "&&" renders one "&": a single "&" marks the next letter as a
        # keyboard shortcut, which is why "Causes & Etiology" showed as
        # "Causes _Etiology".
        button = QPushButton(f"  {label.replace('&', '&&')}")
        button.setObjectName("tocButton")
        button.setCheckable(True)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFixedHeight(31)
        button.setIcon(
            QIcon(
                icons.to_pixmap(
                    icons.draw(icon_name, 13, Theme.token("TEXT_MUTED"))
                )
            )
        )
        button.setIconSize(QSize(13, 13))
        button.clicked.connect(lambda _=False, k=key: self._scroll_to(k))

        if badge:
            # Parented to the button and positioned manually: a layout inside
            # a QPushButton fights the button's own icon/text placement.
            chip = QLabel(badge, button)
            chip.setObjectName("tocBadge")
            chip.adjustSize()
            chip.move(252 - 44 - 26 - chip.width(), (31 - chip.height()) // 2)

        # Insert before the trailing stretch so the list stays top-aligned.
        self._toc_layout.insertWidget(self._toc_layout.count() - 1, button)
        self._toc_buttons[key] = button

    # ------------------------------------------------------------ scrolling

    def _scroll_to(self, key: str) -> None:
        widget = self._anchors.get(key)
        if widget is not None:
            self._scroll.ensureWidgetVisible(widget, 0, 18)
            # Outline the card you landed on, so it is obvious which one
            # the link meant on a long monograph.
            self._highlighter.flash(widget)
        self._set_active(key)

    def _on_scrolled(self, value: int) -> None:
        """Highlight whichever section the reader is currently inside."""
        bar = self._scroll.verticalScrollBar()
        maximum = bar.maximum()
        percent = int((value / maximum) * 100) if maximum else 0
        self._progress_bar.setValue(percent)
        self._progress_label.setText(f"{percent}%")

        # The active section is the last one whose top edge has passed the
        # reading line, a little below the viewport top.
        line = value + 60
        current = None
        for key, widget in self._anchors.items():
            if widget.y() <= line:
                current = key
        if current and current != self._active_key:
            self._set_active(current)

    def _set_active(self, key: str) -> None:
        self._active_key = key
        for section_key, button in self._toc_buttons.items():
            active = section_key == key
            button.setChecked(active)
            color = "#FFFFFF" if active else Theme.token("TEXT_MUTED")
            _, icon_name = SECTION_META[section_key]
            button.setIcon(
                QIcon(icons.to_pixmap(icons.draw(icon_name, 13, color)))
            )

    # ---------------------------------------------------- section builders

    def _triage(self, d: Disease) -> QWidget:
        """Urgency banner.

        With no authored urgency the card stays neutral and says so. An
        unassessed condition must never look like a triage decision.
        """
        text, pill_object = urgency_style(d.urgency)
        card, layout = _card(
            "triageCard" if d.urgency else "triageCardUnknown"
        )

        layout.addWidget(
            _heading("Urgency / when to see a doctor (rule-based triage)", "clock")
        )

        top = QHBoxLayout()
        headline = QLabel(d.urgency_label)
        headline.setObjectName("triageHeadline")
        top.addWidget(headline)
        top.addStretch(1)
        top.addWidget(_chip(d.triage_window, pill_object))
        layout.addLayout(top)

        if d.urgency_criteria:
            grid = QGridLayout()
            grid.setSpacing(12)

            action, action_layout = _card("innerCard")
            action_layout.setSpacing(6)
            action_layout.addWidget(_body("Objective Triage Criteria:", "subHeading"))
            action_layout.addWidget(_body(d.urgency_criteria))
            grid.addWidget(action, 0, 0)
            grid.setColumnStretch(0, 1)
            layout.addLayout(grid)
        elif not d.urgency:
            layout.addWidget(
                _body(
                    "No urgency level has been recorded for this condition. "
                    "Do not read this as reassurance \u2014 the entry is "
                    "incomplete.",
                    "bodyTextMuted",
                )
            )
        return card

    def _summary(self, d: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(_heading("Clinical summary (plain-language definition)", "book"))
        layout.addWidget(_body(d.description))
        return card

    def _pathophysiology(self, d: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(_heading("Pathophysiology & cellular mechanism", "pulse"))
        layout.addWidget(_body(d.pathophysiology))

        if d.clinicopathologic_correlation:
            layout.addWidget(_body("CLINICOPATHOLOGIC CORRELATION", "subHeading"))
            layout.addWidget(_body(d.clinicopathologic_correlation))
        return card

    def _causes(self, d: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(_heading("Causes & contributing etiology", "stack"))
        layout.addLayout(self._two_column([Tile(c) for c in d.causes]))
        return card

    def _symptoms(self, d: Disease) -> QWidget:
        card, layout = _card()

        header = QHBoxLayout()
        header.addWidget(
            _heading(f"Cardinal & associated symptoms ({len(d.symptoms)})", "pulse")
        )
        header.addStretch(1)
        hint = QLabel("Click any symptom to inspect detail")
        hint.setObjectName("metaLabel")
        header.addWidget(hint)
        layout.addLayout(header)

        tiles = []
        for symptom in d.symptoms:
            tile = SymptomTile(symptom)
            tile.inspect_requested.connect(self.symptom_requested.emit)
            tiles.append(tile)
        layout.addLayout(self._grid(tiles, columns=3))
        return card

    def _differentials(self, d: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(
            _heading("Differential diagnosis & distinguishing features", "search")
        )

        tiles = []
        for diff in d.differential_diagnosis:
            tile, tile_layout = _card("innerCard")
            tile_layout.setSpacing(5)
            tile_layout.addWidget(_body(diff.condition, "symptomName"))
            tile_layout.addWidget(
                _body(
                    f"Distinguishing feature: {diff.distinguishing_feature}",
                    "bodyTextMuted",
                )
            )
            tiles.append(tile)
        layout.addLayout(self._grid(tiles, columns=2))
        return card

    def _prevention(self, d: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(
            _heading("Structured prevention tiers (primary, secondary, tertiary)", "shield")
        )

        tiers = [
            ("primary", "1. Primary Prevention", "tierHeadingPrimary"),
            ("secondary", "2. Secondary Screening", "tierHeadingSecondary"),
            ("tertiary", "3. Tertiary Management", "tierHeadingTertiary"),
        ]

        columns = QHBoxLayout()
        columns.setSpacing(12)
        shown = 0
        for key, title, heading_object in tiers:
            items = d.prevention_tiers.get(key, [])
            if not items:
                continue
            column, column_layout = _card("innerCard")
            column_layout.setSpacing(8)

            title_label = QLabel(title.upper())
            title_label.setObjectName(heading_object)
            column_layout.addWidget(title_label)

            for item in items:
                column_layout.addWidget(_body(f"\u2022  {item}", "bulletText"))
            column_layout.addStretch(1)
            columns.addWidget(column, 1)
            shown += 1

        if shown:
            layout.addLayout(columns)

        if d.prevention:
            layout.addWidget(_body("GENERAL PREVENTION", "subHeading"))
            layout.addLayout(self._two_column([Tile(p) for p in d.prevention]))
        return card

    def _treatments(self, d: Disease) -> QWidget:
        card, layout = _card()

        columns = QHBoxLayout()
        columns.setSpacing(14)

        if d.treatments:
            left, left_layout = _card("innerCard")
            left_layout.addWidget(
                _heading("Evidence-based treatments & therapies", "heart")
            )
            for item in d.treatments:
                left_layout.addWidget(Tile(item, "\u2713", "success"))
            left_layout.addStretch(1)
            columns.addWidget(left, 1)

        if d.recommended_tests:
            right, right_layout = _card("innerCard")
            right_layout.addWidget(
                _heading("Recommended diagnostic tests & labs", "pulse")
            )
            for item in d.recommended_tests:
                right_layout.addWidget(Tile(item, "\u25CF"))
            right_layout.addStretch(1)
            columns.addWidget(right, 1)

        layout.addLayout(columns)
        return card

    def _monitoring(self, d: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(_heading("Follow-up & clinical monitoring protocol", "clock"))
        layout.addWidget(_body(d.follow_up_monitoring))
        return card

    def _pharmacotherapy(self, d: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(
            _heading(
                f"Associated pharmacotherapy & formulary ({len(d.medicines)})",
                "pill",
            )
        )

        tiles = []
        for medicine in d.medicines:
            tile = MedicineTile(medicine)
            tile.open_requested.connect(self.medicine_requested.emit)
            tiles.append(tile)
        layout.addLayout(self._grid(tiles, columns=2))
        return card

    def _redflags(self, d: Disease) -> QWidget:
        card, layout = _card("redflagCard")
        layout.addWidget(
            _heading(
                "Emergency warning signs & critical red flags",
                "alert",
                Theme.token("DANGER"),
            )
        )
        layout.addLayout(
            self._two_column(
                [
                    Tile(sign, "\u26A0", "danger")
                    for sign in d.emergency_warning_signs
                ]
            )
        )
        return card

    def _discussion(self, d: Disease) -> QWidget:
        """Peer case discussions. Clinical Exchange fills this once built."""
        card, layout = _card()

        header = QHBoxLayout()
        header.addWidget(_heading("Recent peer case discussions", "chat"))
        header.addWidget(_chip("0 cases", "systemChip"))
        header.addStretch(1)

        present = QPushButton("+  Present Case")
        present.setObjectName("primaryButton")
        present.setCursor(Qt.CursorShape.PointingHandCursor)
        present.clicked.connect(lambda: self.case_requested.emit(d.id))
        header.addWidget(present)
        layout.addLayout(header)

        layout.addWidget(
            _body(
                f"De-identified academic case reviews tagged with {d.name}.",
                "bodyTextMuted",
            )
        )

        empty = _body(
            "No peer discussions are linked to this entry yet.", "bodyTextMuted"
        )
        empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(empty)
        return card

    def _references(self, d: Disease) -> QWidget:
        card, layout = _card()

        header = QHBoxLayout()
        header.addWidget(
            _heading("Academic citations & mother book references", "book")
        )
        header.addStretch(1)
        header.addWidget(
            _chip(
                "Tier 1 & 2 citations" if d.chapter_references
                else "Tier 1 citation",
                "systemChip",
            )
        )
        layout.addLayout(header)
        layout.addWidget(
            _body(
                "Structured academic provenance for medical students, "
                "clinicians, and researchers.",
                "bodyTextMuted",
            )
        )

        # A grid, two per row: monographs now carry three to six citations,
        # and a single row squeezed them until each was unreadable.
        columns = QGridLayout()
        columns.setHorizontalSpacing(14)
        columns.setVerticalSpacing(12)
        columns.setColumnStretch(0, 1)
        columns.setColumnStretch(1, 1)

        for index, reference in enumerate(d.clinical_references):
            tile, tile_layout = _card("innerCard")
            tile_layout.setSpacing(7)

            tier_row = QHBoxLayout()
            tier_row.addWidget(
                _chip(
                    "Tier 1 \u2014 Mother Book" if reference.is_mother_book
                    else "Tier 2 \u2014 Specific Reference",
                    "tier1Chip" if reference.is_mother_book else "tier2Chip",
                )
            )
            tier_row.addStretch(1)
            if reference.specialty:
                specialty = QLabel(reference.specialty)
                specialty.setObjectName("metaLabel")
                tier_row.addWidget(specialty)
            tile_layout.addLayout(tier_row)

            tile_layout.addWidget(_body(reference.source_name, "symptomName"))
            tile_layout.addWidget(_body(reference.citation_text, "bodyTextMuted"))

            if reference.url:
                link = QLabel(
                    f'<a href="{reference.url}" style="color:'
                    f'{Theme.token("BADGE_TEXT")}; text-decoration:none;">'
                    f"{'Access Mother Book' if reference.is_mother_book else 'Open reference'} \u2197</a>"
                )
                link.setObjectName("cardSubtitle")
                link.setTextFormat(Qt.TextFormat.RichText)
                link.setOpenExternalLinks(True)
                tile_layout.addWidget(link)

            tile_layout.addStretch(1)
            row, column = divmod(index, 2)
            columns.addWidget(tile, row, column)

        layout.addLayout(columns)

        if d.source_attribution:
            attribution, attribution_layout = _card("innerCard")
            attribution_layout.setSpacing(5)
            attribution_layout.addWidget(
                _body(
                    "CONSOLIDATED CLINICAL GUIDELINES & INSTITUTIONAL "
                    "ATTRIBUTIONS",
                    "subHeading",
                )
            )
            attribution_layout.addWidget(
                _body(f"\u2022  {d.source_attribution}", "bulletText")
            )
            layout.addWidget(attribution)

        return card

    # -------------------------------------------------------------- layout

    @staticmethod
    def _grid(widgets: list[QWidget], columns: int) -> QGridLayout:
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(11)
        for index, widget in enumerate(widgets):
            row, column = divmod(index, columns)
            grid.addWidget(widget, row, column)
        # Equal stretch on every column, occupied or not, so a lone tile does
        # not expand to fill the whole row.
        for column in range(columns):
            grid.setColumnStretch(column, 1)
        return grid

    def _two_column(self, widgets: list[QWidget]) -> QGridLayout:
        return self._grid(widgets, 2)

    # ------------------------------------------------------------- sidebar

    def _fill_metadata(self, d: Disease) -> None:
        while self._meta_grid.count():
            item = self._meta_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        rows = [
            ("Body System", d.body_system_name or "Unclassified"),
            ("Severity", d.severity),
            ("Contagious", "Yes" if d.contagious else "No"),
            ("Hallmark Symptoms", str(len(d.hallmark_symptoms))),
            ("Related Medications", str(len(d.medicines))),
        ]

        for index, (label_text, value_text) in enumerate(rows):
            label = QLabel(label_text)
            label.setObjectName("metaLabel")

            value = QLabel(value_text)
            value.setObjectName("metaValue")
            value.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            value.setWordWrap(True)

            self._meta_grid.addWidget(label, index, 0)
            self._meta_grid.addWidget(value, index, 1)

    def _fill_related(self, d: Disease) -> None:
        """Cross-links built from real rows only.

        No linked medicines means no Medicines group — an empty heading
        would imply the data is loading or broken.
        """
        # Wipe everything after the header row.
        while self._related_layout.count() > 1:
            item = self._related_layout.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        has_content = False

        if d.medicines:
            has_content = True
            self._related_layout.addWidget(
                self._related_group_label("Medicines", "pill")
            )
            for medicine in d.medicines:
                self._related_layout.addWidget(
                    self._related_pill(
                        medicine.name, medicine.id, self.medicine_requested,
                        "relatedPillPrimary",
                    )
                )

        if d.symptoms:
            has_content = True
            self._related_layout.addWidget(
                self._related_group_label("Cardinal Symptoms", "pulse")
            )
            for symptom in d.symptoms:
                self._related_layout.addWidget(
                    self._related_pill(
                        symptom.name or symptom.symptom_id,
                        symptom.symptom_id,
                        self.symptom_requested,
                        "relatedPill",
                        )
                )

        if not has_content:
            empty = QLabel("No cross-links recorded for this condition.")
            empty.setObjectName("bodyTextMuted")
            empty.setWordWrap(True)
            self._related_layout.addWidget(empty)

        self._related_card.setVisible(True)

    @staticmethod
    def _related_group_label(text: str, icon_name: str) -> QWidget:
        row = QWidget()
        row.setObjectName("panel")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 6, 0, 2)
        layout.setSpacing(7)

        glyph = QLabel()
        glyph.setObjectName("panel")
        glyph.setPixmap(
            icons.to_pixmap(
                icons.draw(icon_name, 13, Theme.token("BADGE_TEXT"))
            )
        )
        glyph.setFixedSize(13, 13)

        label = QLabel(f"{text}:")
        label.setObjectName("metaLabel")

        layout.addWidget(glyph)
        layout.addWidget(label)
        layout.addStretch(1)
        return row

    @staticmethod
    def _related_pill(
            text: str, entity_id: str, signal, object_name: str
    ) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName(object_name)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setToolTip(text)
        button.clicked.connect(lambda _=False: signal.emit(entity_id))
        return button

    # ----------------------------------------------------------- behaviour

    def _emit_check_symptoms(self) -> None:
        if self._disease:
            self.check_symptoms_requested.emit(self._disease.id)

    def _emit_compare(self) -> None:
        if self._disease:
            self.compare_requested.emit(self._disease.id)

    def _toggle_bookmark(self) -> None:
        if not self._disease:
            return
        self._bookmarked = not self._bookmarked
        self._refresh_bookmark_icon()
        self.bookmark_toggled.emit(self._disease.id, self._bookmarked)

    def _refresh_bookmark_icon(self) -> None:
        color = (
            Theme.token("DANGER") if self._bookmarked
            else Theme.token("TEXT_MUTED")
        )
        self._bookmark_btn.setIcon(
            QIcon(icons.to_pixmap(
                (icons.star_filled if self._bookmarked else icons.star)(17, color)))
        )
        self._bookmark_btn.setIconSize(QSize(17, 17))

    def show_error(self, message: str) -> None:
        self._clear()
        label = QLabel(message)
        label.setObjectName("bodyTextMuted")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._content_layout.addWidget(label)