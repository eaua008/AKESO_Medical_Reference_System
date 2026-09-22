"""Disease monograph — the Inspect Entry page.

Display only, like every other view here. It renders a fully hydrated Disease
object and announces what the user clicked. It never fetches anything.

Sections are registered through _add_section(), which does three jobs at once:
builds the card, adds the matching entry to the left nav, and records the
scroll anchor. Adding the remaining sections means writing one _build_* method
and one _add_section call — no layout plumbing.

Four sections exist so far: Triage, Clinical Summary, Pathophysiology, and
Causes. The other eight follow the same pattern.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.core import icons
from app.core.models_helpers import urgency_style
from app.core.theme import Theme
from app.models.disease import Disease

# Sections listed in the left nav, in page order. icon is an icons.py name.
SECTION_ORDER = [
    ("triage", "Triage & Urgency", "alert"),
    ("summary", "Clinical Summary", "book"),
    ("pathophysiology", "Pathophysiology", "pulse"),
    ("causes", "Causes & Etiology", "stack"),
]


def _card(object_name: str = "detailCard") -> tuple[QFrame, QVBoxLayout]:
    """A bordered content card plus its layout, ready to fill."""
    frame = QFrame()
    frame.setObjectName(object_name)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(22, 20, 22, 20)
    layout.setSpacing(12)
    return frame, layout


def _section_heading(text: str, icon_name: str, color: str) -> QWidget:
    row = QWidget()
    row.setObjectName("panel")
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(9)

    glyph = QLabel()
    glyph.setObjectName("panel")
    glyph.setPixmap(icons.to_pixmap(icons.draw(icon_name, 16, color)))
    glyph.setFixedSize(16, 16)

    label = QLabel(text.upper())
    label.setObjectName("sectionHeading")

    layout.addWidget(glyph)
    layout.addWidget(label)
    layout.addStretch(1)
    return row


class BulletItem(QFrame):
    """One entry in a clinical list — a dot and wrapped text in a tile."""

    def __init__(self, text: str, accent: str = "primary") -> None:
        super().__init__()
        self.setObjectName(
            "bulletTileDanger" if accent == "danger" else "bulletTile"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 11, 14, 11)
        layout.setSpacing(10)

        dot = QLabel("\u25CF" if accent != "danger" else "\u26A0")
        dot.setObjectName(
            "bulletDotDanger" if accent == "danger" else "bulletDot"
        )
        dot.setFixedWidth(12)
        dot.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        label = QLabel(text)
        label.setObjectName("bulletText")
        label.setWordWrap(True)

        layout.addWidget(dot)
        layout.addWidget(label, 1)


class DiseaseDetailView(QWidget):
    """The full clinical monograph for one condition."""

    back_requested = Signal()
    bookmark_toggled = Signal(str, bool)
    check_symptoms_requested = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")

        self._disease: Optional[Disease] = None
        self._anchors: dict[str, QWidget] = {}
        self._nav_buttons: dict[str, QPushButton] = {}
        self._bookmarked = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_top_bar())

        body = QWidget()
        body.setObjectName("panel")
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(24, 20, 24, 24)
        body_layout.setSpacing(20)

        body_layout.addWidget(self._build_left_rail())
        body_layout.addWidget(self._build_content_scroll(), 1)

        root.addWidget(body, 1)

    # ------------------------------------------------------------- top bar

    def _build_top_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("detailTopBar")
        bar.setFixedHeight(60)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(14)

        back = QPushButton("  \u2190  Back to Conditions")
        back.setObjectName("secondaryButton")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.clicked.connect(self.back_requested.emit)

        self._title_label = QLabel("")
        self._title_label.setObjectName("detailTitle")

        self._scientific_label = QLabel("")
        self._scientific_label.setObjectName("detailScientific")

        self._check_btn = QPushButton("Check Symptoms")
        self._check_btn.setObjectName("primaryButton")
        self._check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._check_btn.clicked.connect(self._emit_check_symptoms)

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
        layout.addWidget(self._bookmark_btn)
        return bar

    # ----------------------------------------------------------- left rail

    def _build_left_rail(self) -> QWidget:
        rail = QWidget()
        rail.setObjectName("panel")
        rail.setFixedWidth(250)

        layout = QVBoxLayout(rail)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        nav_card, nav_layout = _card("detailCard")
        nav_layout.setSpacing(4)

        heading = QLabel("PAGE SECTIONS")
        heading.setObjectName("railHeading")
        nav_layout.addWidget(heading)

        # Filled by _add_section as sections are registered, so the nav can
        # never drift out of sync with what is actually on the page.
        self._nav_layout = nav_layout
        nav_layout.addStretch(1)

        layout.addWidget(nav_card)
        layout.addWidget(self._build_metadata_card())
        layout.addStretch(1)
        return rail

    def _build_metadata_card(self) -> QWidget:
        card, layout = _card("detailCard")

        heading = QLabel("AT-A-GLANCE METADATA")
        heading.setObjectName("railHeading")
        layout.addWidget(heading)

        self._meta_grid = QGridLayout()
        self._meta_grid.setContentsMargins(0, 4, 0, 0)
        self._meta_grid.setHorizontalSpacing(10)
        self._meta_grid.setVerticalSpacing(9)
        layout.addLayout(self._meta_grid)
        return card

    def _set_metadata(self, rows: list[tuple[str, str]]) -> None:
        while self._meta_grid.count():
            item = self._meta_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

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
        self._content_layout.setContentsMargins(0, 0, 8, 0)
        self._content_layout.setSpacing(18)
        self._content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._scroll.setWidget(holder)
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

        self._clear_content()
        self._build_sections(disease)
        self._set_metadata(self._metadata_rows(disease))

        self._scroll.verticalScrollBar().setValue(0)

    def _metadata_rows(self, disease: Disease) -> list[tuple[str, str]]:
        return [
            ("Severity", disease.severity),
            ("Urgency", disease.urgency_label),
            ("Contagious", "Yes" if disease.contagious else "No"),
            ("Hallmark Symptoms", str(len(disease.hallmark_symptom_ids))),
            ("Citations", str(len(disease.clinical_references))),
        ]

    # ------------------------------------------------------------ sections

    def _clear_content(self) -> None:
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._anchors.clear()

        # Rebuild the nav too, minus its heading and trailing stretch.
        for button in self._nav_buttons.values():
            self._nav_layout.removeWidget(button)
            button.deleteLater()
        self._nav_buttons.clear()

    def _build_sections(self, disease: Disease) -> None:
        self._add_section("triage", self._build_triage(disease))
        self._add_section("summary", self._build_summary(disease))

        if disease.pathophysiology:
            self._add_section(
                "pathophysiology", self._build_pathophysiology(disease)
            )
        if disease.causes:
            self._add_section("causes", self._build_causes(disease))

    def _add_section(self, key: str, widget: QWidget) -> None:
        """Place a section and give it a matching left-nav entry."""
        self._content_layout.addWidget(widget)
        self._anchors[key] = widget

        meta = next((s for s in SECTION_ORDER if s[0] == key), None)
        if meta is None:
            return
        _, label, icon_name = meta

        button = QPushButton(f"  {label}")
        button.setObjectName("railNavButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFixedHeight(32)
        button.clicked.connect(lambda _=False, k=key: self._scroll_to(k))

        from PySide6.QtCore import QSize
        from PySide6.QtGui import QIcon

        image = icons.draw(icon_name, 14, Theme.token("TEXT_MUTED"))
        button.setIcon(QIcon(icons.to_pixmap(image)))
        button.setIconSize(QSize(14, 14))

        # Insert before the trailing stretch so the list stays top-aligned.
        self._nav_layout.insertWidget(self._nav_layout.count() - 1, button)
        self._nav_buttons[key] = button

    def _scroll_to(self, key: str) -> None:
        widget = self._anchors.get(key)
        if widget is None:
            return
        self._scroll.verticalScrollBar().setValue(widget.y())

    # ---------------------------------------------------- section builders

    def _build_triage(self, disease: Disease) -> QWidget:
        """Urgency banner.

        When urgency is None the card says so plainly rather than showing a
        colour-coded level. An unassessed condition must never look like a
        triage decision that someone made.
        """
        text, pill_object = urgency_style(disease.urgency)
        card, layout = _card(
            "triageCardUnknown" if not disease.urgency else "triageCard"
        )

        layout.addWidget(
            _section_heading(
                "Urgency / when to see a doctor",
                "alert",
                Theme.token("BADGE_TEXT"),
            )
        )

        headline = QLabel(disease.urgency_label)
        headline.setObjectName("triageHeadline")

        pill = QLabel(text)
        pill.setObjectName(pill_object)
        pill.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

        top = QHBoxLayout()
        top.addWidget(headline)
        top.addStretch(1)
        top.addWidget(pill)
        layout.addLayout(top)

        if disease.urgency_criteria:
            criteria = QLabel(disease.urgency_criteria)
            criteria.setObjectName("bodyText")
            criteria.setWordWrap(True)
            layout.addWidget(criteria)
        elif not disease.urgency:
            note = QLabel(
                "No urgency level has been recorded for this condition yet. "
                "Do not read this as reassurance \u2014 it means the entry is "
                "incomplete."
            )
            note.setObjectName("bodyTextMuted")
            note.setWordWrap(True)
            layout.addWidget(note)

        return card

    def _build_summary(self, disease: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(
            _section_heading(
                "Clinical summary", "book", Theme.token("BADGE_TEXT")
            )
        )

        body = QLabel(disease.description)
        body.setObjectName("bodyText")
        body.setWordWrap(True)
        layout.addWidget(body)

        if disease.source_attribution:
            source = QLabel(f"Source: {disease.source_attribution}")
            source.setObjectName("bodyTextMuted")
            source.setWordWrap(True)
            layout.addWidget(source)

        return card

    def _build_pathophysiology(self, disease: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(
            _section_heading(
                "Pathophysiology & cellular mechanism",
                "pulse",
                Theme.token("BADGE_TEXT"),
            )
        )

        body = QLabel(disease.pathophysiology)
        body.setObjectName("bodyText")
        body.setWordWrap(True)
        layout.addWidget(body)

        if disease.clinicopathologic_correlation:
            sub = QLabel("CLINICOPATHOLOGIC CORRELATION")
            sub.setObjectName("subHeading")
            layout.addWidget(sub)

            detail = QLabel(disease.clinicopathologic_correlation)
            detail.setObjectName("bodyText")
            detail.setWordWrap(True)
            layout.addWidget(detail)

        return card

    def _build_causes(self, disease: Disease) -> QWidget:
        card, layout = _card()
        layout.addWidget(
            _section_heading(
                "Causes & contributing etiology",
                "stack",
                Theme.token("BADGE_TEXT"),
            )
        )

        # Two columns, matching the mockup. The list order is the author's
        # ranking, so fill left-to-right rather than down each column.
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)
        for index, cause in enumerate(disease.causes):
            row, column = divmod(index, 2)
            grid.addWidget(BulletItem(cause), row, column)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        layout.addLayout(grid)

        return card

    # ----------------------------------------------------------- behaviour

    def _emit_check_symptoms(self) -> None:
        if self._disease:
            self.check_symptoms_requested.emit(self._disease.id)

    def _toggle_bookmark(self) -> None:
        if not self._disease:
            return
        self._bookmarked = not self._bookmarked
        self._refresh_bookmark_icon()
        self.bookmark_toggled.emit(self._disease.id, self._bookmarked)

    def _refresh_bookmark_icon(self) -> None:
        from PySide6.QtCore import QSize
        from PySide6.QtGui import QIcon

        color = (
            Theme.token("PRIMARY") if self._bookmarked
            else Theme.token("TEXT_MUTED")
        )
        self._bookmark_btn.setIcon(
            QIcon(icons.to_pixmap(icons.star(17, color)))
        )
        self._bookmark_btn.setIconSize(QSize(17, 17))

    def show_error(self, message: str) -> None:
        self._clear_content()
        label = QLabel(message)
        label.setObjectName("bodyTextMuted")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._content_layout.addWidget(label)