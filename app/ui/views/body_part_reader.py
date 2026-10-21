"""A body part's full description, as a white page over the Explorer.

Same look as an announcement (AnnouncementDialog): big title, a meta line,
a rule, then easy-to-read text on white in every theme.

    LIVER
    ORGAN · DIGESTIVE  [DRAFT]  ·  You clicked: caudate lobe of liver
    ───────────────────────────────────────────────────────────────
    IN SHORT / WHAT IT DOES / FOR STUDENTS / LOCATION & NEIGHBOURS /
    details (two columns) / CLINICAL RELEVANCE / EXAM TIP / SOURCES

It lives in a PageSheet (like a monograph or an article), not a pop-up, so
a source opens in the reference browser ON TOP of it and closing the
browser comes back to the description. A linked condition opens on top too.

Display only: the text is reviewed content from body_part_info.
"""

from html import escape

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget,
)

from app.core.links import open_link
from app.ui.components.sheet_dialog import PAPER, PAPER_GHOST, PAPER_LINE, PAPER_SCROLLBAR
from app.ui.views.account.account_widgets import button, icon_label, label
from app.ui.views.announcement_widgets import INK, INK_SOFT, PAPER_BADGES, RULE

LINK = PAPER_BADGES["info"][1]                       # the page's indigo
TIP_BACK, TIP_INK = PAPER_BADGES["important"]        # soft amber box
LAYER_NAMES = {"bone": "Bone", "muscle": "Muscle", "organ": "Organ", "vessel": "Blood vessel",
               "nerve": "Nerve", "skin": "Skin"}
COLUMN = 1000                                        # widest the text gets


def _ink(text: str, size: int, colour: str = INK, weight: int = 400,
         selectable: bool = True) -> QLabel:
    widget = QLabel(text)
    widget.setWordWrap(True)
    widget.setTextFormat(Qt.TextFormat.PlainText)            # never HTML from the server
    widget.setStyleSheet(f"color: {colour}; font-size: {size}px; font-weight: {weight}; "
                         "background: transparent;")
    if selectable:
        widget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    return widget


def _rule() -> QFrame:
    line = QFrame()
    line.setFixedHeight(1)
    line.setStyleSheet(f"background-color: {RULE}; border: none;")
    return line


class BodyPartReader(QWidget):
    disease_requested = Signal(str)
    close_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # The bar: same as the pop-up sheets (icon and title), on the theme.
        bar = QFrame()
        bar.setObjectName("detailTopBar")
        bar.setFixedHeight(50)
        line = QHBoxLayout(bar)
        line.setContentsMargins(68, 0, 24, 0)          # clear of the red X tab
        line.setSpacing(10)
        line.addWidget(icon_label("info", 18))
        self._bar_title = label("", "acCardTitle", wrap=False)
        line.addWidget(self._bar_title, 1)
        root.addWidget(bar)

        # The white page.
        white = f"background-color: {PAPER};"
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet(f"QScrollArea {{ {white} border: none; }}" + PAPER_SCROLLBAR)
        self._scroll.viewport().setStyleSheet(white)
        holder = QWidget()
        holder.setStyleSheet(white)
        outer = QHBoxLayout(holder)
        outer.setContentsMargins(68, 36, 40, 40)
        page = QWidget()
        page.setStyleSheet(white)
        page.setMaximumWidth(COLUMN)
        self.body = QVBoxLayout(page)
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(10)
        outer.addWidget(page, 1)
        outer.addStretch(0)
        self._scroll.setWidget(holder)
        root.addWidget(self._scroll, 1)

        footer = QFrame()
        footer.setStyleSheet(f"QFrame {{ {white} border: none; border-top: 1px solid {PAPER_LINE}; }}")
        row = QHBoxLayout(footer)
        row.setContentsMargins(24, 12, 24, 12)
        row.addStretch(1)
        row.addWidget(button("Got it", "acPrimary", "check",
                             lambda _c=False: self.close_requested.emit()))
        root.addWidget(footer)

    # ---------------------------------------------------------------- api

    def show_part(self, about, clicked_name: str = "", disease_names=None) -> None:
        """Fill the page for one PartDescription (BodyPartService.describe)."""
        self._clear(self.body)
        info = about.info
        disease_names = disease_names or {}
        self._bar_title.setText(info.display_name)

        self.body.addWidget(_ink(info.display_name, 34, INK, 600))
        self.body.addSpacing(4)
        meta = QHBoxLayout()
        meta.setSpacing(10)
        kind = " · ".join(x for x in (LAYER_NAMES.get(info.layer, ""),
                                           info.system.capitalize()) if x)
        if kind:
            tag = _ink(kind.upper(), 13, INK_SOFT, 600, selectable=False)
            tag.setWordWrap(False)
            meta.addWidget(tag)
        if info.is_draft:
            back, fore = PAPER_BADGES["important"]
            badge = QLabel("DRAFT")
            badge.setStyleSheet(f"background-color: {back}; color: {fore}; font-size: 11px; "
                                "font-weight: 700; border-radius: 9px; padding: 2px 10px;")
            meta.addWidget(badge)
        meta.addStretch(1)
        self.body.addLayout(meta)
        if clicked_name and not about.exact:
            self.body.addWidget(_ink(f"You clicked: {clicked_name}, part of the "
                                     f"{info.display_name.lower()}.", 14, INK_SOFT))
        if info.aliases:
            self.body.addWidget(_ink("Also called " + ", ".join(info.aliases) + ".", 14, INK_SOFT))
        self.body.addSpacing(8)
        self.body.addWidget(_rule())

        self._section("IN SHORT", info.summary_plain, 17)
        self._section("WHAT IT DOES", info.function_plain, 17)
        if info.has_student_text():
            self._section("FOR STUDENTS", info.description)
            self._section("LOCATION & NEIGHBOURS", info.location)
            rows = info.detail_rows()
            if rows:
                grid = QGridLayout()
                grid.setHorizontalSpacing(18)
                grid.setVerticalSpacing(12)
                grid.setColumnStretch(1, 1)
                for i, (title, text) in enumerate(rows):
                    key = _ink(title, 15, INK, 600)
                    key.setMinimumWidth(130)
                    grid.addWidget(key, i, 0, Qt.AlignmentFlag.AlignTop)
                    grid.addWidget(_ink(text, 16), i, 1, Qt.AlignmentFlag.AlignTop)
                self.body.addSpacing(8)
                self.body.addLayout(grid)

        if info.clinical:
            self._heading("CLINICAL RELEVANCE")
            for note in info.clinical:
                line = QHBoxLayout()
                line.setSpacing(10)
                dot = _ink("•", 16, INK, 700, selectable=False)
                dot.setWordWrap(False)
                line.addWidget(dot, 0, Qt.AlignmentFlag.AlignTop)
                line.addWidget(_ink(note.text, 16), 1)
                self.body.addLayout(line)
            linked = dict.fromkeys(n.disease_id for n in info.clinical
                                   if n.disease_id in disease_names)
            for disease_id in linked:
                widget = button(f"Open condition: {disease_names[disease_id]}", "acGhost",
                                "book-open",
                                lambda _c=False, d=disease_id: self.disease_requested.emit(d))
                widget.setStyleSheet(PAPER_GHOST)
                self.body.addWidget(widget, 0, Qt.AlignmentFlag.AlignLeft)

        if info.exam_tip:
            self.body.addSpacing(14)
            tip = QFrame()
            tip.setStyleSheet(f"QFrame {{ background-color: {TIP_BACK}; border-radius: 12px; }}")
            box = QVBoxLayout(tip)
            box.setContentsMargins(16, 12, 16, 14)
            box.setSpacing(4)
            box.addWidget(_ink("EXAM TIP", 12, TIP_INK, 700, selectable=False))
            box.addWidget(_ink(info.exam_tip, 16, INK))
            self.body.addWidget(tip)

        if info.sources:
            self._heading("SOURCES")
            for source in info.sources:
                text = escape(source.title) + (f" ({escape(source.licence)})" if source.licence
                                               else "")
                link = QLabel(f'<a href="{escape(source.url, quote=True)}" style="color:{LINK}; '
                              f'text-decoration:none">{text}</a>')
                link.setWordWrap(True)
                link.setTextFormat(Qt.TextFormat.RichText)
                link.setOpenExternalLinks(False)
                link.setStyleSheet("font-size: 14px; background: transparent;")
                link.setCursor(Qt.CursorShape.PointingHandCursor)
                link.setToolTip("Opens on top of this page; close it to come back here.")
                # The browser sheet slides over this page; closing it lands here again.
                link.linkActivated.connect(lambda url, t=source.title: open_link(url, t))
                self.body.addWidget(link)
        self.body.addSpacing(10)
        self.body.addWidget(_ink(
            "Draft: written from the sources above, not reviewed yet. Only admins see drafts."
            if info.is_draft else
            "Educational reference only. Written from the sources above and reviewed by the "
            "Akeso team.", 13, INK_SOFT))
        self.body.addStretch(1)
        self._scroll.verticalScrollBar().setValue(0)

    # ------------------------------------------------------------- pieces

    def _heading(self, text: str) -> None:
        self.body.addSpacing(16)
        self.body.addWidget(_ink(text, 13, INK_SOFT, 700, selectable=False))

    def _section(self, title: str, text: str, size: int = 16) -> None:
        if text:
            self._heading(title)
            self.body.addWidget(_ink(text, size))

    def _clear(self, layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().hide()
                item.widget().deleteLater()
            elif item.layout():
                self._clear(item.layout())
