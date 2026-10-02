"""Citation cards shared by the Symptom and Medicine monographs.

Same layout the Disease monograph already uses: every reference gets its own
card in a two-column grid (Tier 1 mother book first), and any reference with
a web address gets an "Open reference" link that opens in the browser.
Textbooks (mother books) carry no URL on purpose, so they have no link.
"""

from html import escape
from urllib.parse import urlparse

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from app.core.theme import Theme
from app.ui.components.fluid import ResponsiveGrid

TIER_1 = "TIER 1 — MOTHER BOOK"
TIER_2 = "TIER 2 — SPECIFIC REFERENCE"


def safe_url(url: str) -> str:
    """Only plain web links are clickable. Anything else (javascript:, file:)
    coming from the database is ignored rather than handed to the OS."""
    url = (url or "").strip()
    parsed = urlparse(url)
    return url if parsed.scheme in ("http", "https") and parsed.netloc else ""


def link_label(url: str, text: str, object_name: str) -> QLabel:
    label = QLabel(
        f'<a href="{escape(url, quote=True)}" style="color:{Theme.token("BADGE_TEXT")};'
        f' text-decoration:none;">{escape(text)} ↗</a>')
    label.setObjectName(object_name)
    label.setTextFormat(Qt.TextFormat.RichText)
    label.setOpenExternalLinks(True)
    label.setCursor(Qt.CursorShape.PointingHandCursor)
    label.setToolTip(url)
    return label


def _text(text: str, object_name: str, wrap: bool = True) -> QLabel:
    label = QLabel(text)
    label.setObjectName(object_name)
    label.setWordWrap(wrap)
    return label


def reference_card(reference, prefix: str) -> QFrame:
    """One citation. prefix is the page's style prefix: "sy" or "md"."""
    primary = bool(reference.is_mother_book)
    box = QFrame()
    box.setObjectName(f"{prefix}RefPrimary" if primary else f"{prefix}Ref")
    layout = QVBoxLayout(box)
    layout.setContentsMargins(14, 12, 14, 12)
    layout.setSpacing(4)
    layout.addWidget(_text(TIER_1 if primary else TIER_2,
                           f"{prefix}RefTierPrimary" if primary else f"{prefix}RefTier"))
    layout.addWidget(_text(reference.source_name or "Untitled source", f"{prefix}RefSource"))
    if reference.citation_text:
        layout.addWidget(_text(reference.citation_text, f"{prefix}RefCitation"))
    url = safe_url(reference.url)
    if url:
        layout.addSpacing(2)
        layout.addWidget(link_label(
            url, "Access Mother Book" if primary else "Open reference", f"{prefix}RefLink"))
    layout.addStretch(1)
    return box


def reference_grid(references: list, prefix: str, viewport=None, columns: int = 2):
    """All references, mother book first: two per row, one on narrow windows.

    viewport is the page's scroll viewport, which decides how many fit.
    """
    ordered = sorted(references, key=lambda r: not r.is_mother_book)
    grid = ResponsiveGrid(320, columns, spacing=12)
    if viewport is not None:
        grid.watch(viewport)
    grid.set_cards([reference_card(reference, prefix) for reference in ordered])
    return grid
