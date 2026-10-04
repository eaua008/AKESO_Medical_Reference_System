"""Health Articles: the list page and the reader.

Display only. HealthArticlesController loads the articles and decides what
a click does: a written article opens in ArticleReader (a full-page sheet,
like the inspect pages); an external link opens in the built-in browser.

The list is a directory grouped by topic (or one A–Z index), styled by
app/core/article_styles.py; the reader reuses the Account page's pieces.
"""

from html import escape
from typing import Optional
from urllib.parse import urlparse

from PySide6.QtCore import QPoint, QSize, Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QProgressBar,
    QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from app.core import lucide
from app.core.links import safe_url
from app.core.theme import Theme
from app.models.health_article import HealthArticle, body_blocks
from app.ui.components.fluid import contain
from app.ui.views.account.account_widgets import (
    Banner, button, icon_label, label, pill, refresh_icons, repolish,
)
from app.ui.views.compare_view import FlowLayout

LINK_ICONS = {"disease": "book-open", "symptom": "activity", "medicine": "pill"}
def _accent() -> str:
    """The theme's second accent (pink in Dracula, cyan in Space...)."""
    return Theme.token("ACCENT_2")


def _star(on: bool) -> object:
    return lucide.icon("bookmark", 16, Theme.token("PRIMARY") if on else Theme.token("TEXT_MUTED"))


def _polish_tree(widget: QWidget) -> None:
    for w in [widget] + widget.findChildren(QWidget):
        w.style().unpolish(w)
        w.style().polish(w)


class ArticleRow(QFrame):
    """One line in the directory: topic label, title, bookmark, chevron."""

    open_requested = Signal(str)          # article id
    star_requested = Signal(str)

    def __init__(self, article: HealthArticle, starred: bool, alt: bool, pos: str) -> None:
        super().__init__()
        self.setObjectName("haRow")
        self.setProperty("alt", alt)
        self.setProperty("pos", pos)
        self.setProperty("hover", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = article.id
        self._external = article.is_external
        row = QHBoxLayout(self)
        row.setContentsMargins(30, 18, 22, 18)
        row.setSpacing(12)

        text = QVBoxLayout()
        text.setSpacing(5)
        top = QHBoxLayout()
        top.setSpacing(8)
        top.addWidget(label(article.category.upper(), "haRowTopic", wrap=False))
        meta = " · ".join(x for x in (
            ("External link · " if article.is_external else "") + article.meta_line(),) if x)
        top.addWidget(label(meta, "haRowMeta", wrap=False))
        top.addStretch(1)
        text.addLayout(top)
        self.title = label(article.title, "haRowTitle")
        text.addWidget(self.title)
        row.addLayout(text, 1)

        self.star = QPushButton()
        self.star.setObjectName("haStar")
        self.star.setFixedSize(30, 30)
        self.star.setCursor(Qt.CursorShape.PointingHandCursor)
        self.star.setToolTip("Remove bookmark" if starred else "Bookmark")
        self.star.setIcon(_star(starred))
        self.star.setIconSize(QSize(16, 16))
        self.star.clicked.connect(lambda _c=False: self.star_requested.emit(self._id))
        row.addWidget(self.star, 0, Qt.AlignmentFlag.AlignVCenter)
        self.chevron = QLabel()
        self.chevron.setObjectName("panel")
        self.chevron.setFixedSize(18, 18)
        row.addWidget(self.chevron, 0, Qt.AlignmentFlag.AlignVCenter)
        self._paint_chevron(False)

    def _paint_chevron(self, hover: bool) -> None:
        colour = _accent() if hover else Theme.token("ICON_MUTED")
        self.chevron.setPixmap(lucide.pixmap(
            "external-link" if self._external else "chevron-right", 16 if self._external else 18,
            colour))

    def _set_hover(self, on: bool) -> None:
        self.setProperty("hover", on)
        _polish_tree(self)
        self._paint_chevron(on)

    def enterEvent(self, event) -> None:  # noqa: N802
        self._set_hover(True)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._set_hover(False)
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.open_requested.emit(self._id)
        super().mouseReleaseEvent(event)


class ArticleGroup(QFrame):
    """A rounded box holding rows stacked edge to edge."""

    def __init__(self, rows: list[ArticleRow]) -> None:
        super().__init__()
        self.setObjectName("haGroup")
        column = QVBoxLayout(self)
        column.setContentsMargins(1, 1, 1, 1)
        column.setSpacing(0)
        for row in rows:
            column.addWidget(row)


def _section_header(title: str, count: int) -> QWidget:
    host = QWidget()
    host.setObjectName("panel")
    column = QVBoxLayout(host)
    column.setContentsMargins(0, 8, 0, 0)
    column.setSpacing(8)
    line = QHBoxLayout()
    line.setContentsMargins(6, 0, 0, 0)
    line.setSpacing(10)
    dot = QFrame()
    dot.setObjectName("haDot")
    dot.setFixedSize(8, 8)
    line.addWidget(dot, 0, Qt.AlignmentFlag.AlignVCenter)
    line.addWidget(label(title.upper(), "haSection", wrap=False))
    line.addStretch(1)
    line.addWidget(label(f"{count} {'entry' if count == 1 else 'entries'}",
                         "haSectionCount", wrap=False))
    column.addLayout(line)
    divider = QFrame()
    divider.setObjectName("haDivider")
    divider.setFixedHeight(1)
    column.addWidget(divider)
    return host


class HealthArticlesView(QWidget):
    open_requested = Signal(str)
    star_requested = Signal(str)
    filters_changed = Signal(str, str, str)     # query, category, kind
    retry_requested = Signal()

    BY_TOPIC, INDEX = "topic", "index"

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._category = ""
        self._mode = self.BY_TOPIC
        self._last: tuple[list, set, int] = ([], set(), 0)
        self.rows: list[ArticleRow] = []
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        column = QVBoxLayout(page)
        column.setContentsMargins(30, 22, 30, 30)
        column.setSpacing(16)

        # -- header: icon + title, subtitle, published count
        head = QHBoxLayout()
        head.setSpacing(10)
        text = QVBoxLayout()
        text.setSpacing(2)
        title_line = QHBoxLayout()
        title_line.setSpacing(8)
        title_line.addWidget(icon_label("book-open", 22))
        title_line.addWidget(label("Health & Wellness Articles", "haTitle", wrap=False))
        title_line.addStretch(1)
        text.addLayout(title_line)
        text.addWidget(label("Clinical insights, preventive guidance and healthy lifestyle "
                             "reads from trusted sources. Educational only, not medical advice.",
                             "haSubtitle"))
        head.addLayout(text, 1)
        self.count = pill("", "haCountPill")
        head.addWidget(self.count, 0, Qt.AlignmentFlag.AlignTop)
        column.addLayout(head)

        self.banner = Banner()
        self.banner.action.connect(self.retry_requested.emit)
        column.addWidget(self.banner)

        # -- toolbar: search, topic dropdown, By Topic / Index List
        toolbar = QFrame()
        toolbar.setObjectName("haToolbar")
        bar = QHBoxLayout(toolbar)
        bar.setContentsMargins(16, 14, 16, 14)
        bar.setSpacing(10)
        self.search = QLineEdit()
        self.search.setObjectName("haSearch")
        self.search.setPlaceholderText("Search articles by title, topic, or keyword…")
        self.search.setClearButtonEnabled(True)
        self.search.setMinimumWidth(220)
        self._search_icon = icon_label("search", 15, Theme.token("TEXT_MUTED"))
        self._search_icon.setParent(self.search)
        self._search_icon.move(12, 0)
        self.search.textChanged.connect(lambda _t: self._emit())
        bar.addWidget(self.search, 3)
        self.topic = QComboBox()
        self.topic.setObjectName("haTopic")
        self.topic.setMinimumWidth(190)
        self.topic.setCursor(Qt.CursorShape.PointingHandCursor)
        self.topic.currentIndexChanged.connect(self._topic_changed)
        bar.addWidget(self.topic, 1)
        segment = QFrame()
        segment.setObjectName("haSegment")
        seg = QHBoxLayout(segment)
        seg.setContentsMargins(3, 3, 3, 3)
        seg.setSpacing(2)
        self._mode_group = QButtonGroup(self)
        self._mode_group.setExclusive(True)
        self.mode_buttons: dict[str, QPushButton] = {}
        for value, text_, icon in ((self.BY_TOPIC, "By Topic", "layers"),
                                   (self.INDEX, "Index List", "list")):
            b = button(text_, "haSegBtn", icon, lambda v=value: self._set_mode(v))
            b.setCheckable(True)
            b.setChecked(value == self._mode)
            self._mode_group.addButton(b)
            self.mode_buttons[value] = b
            seg.addWidget(b)
        bar.addWidget(segment)
        column.addWidget(toolbar)

        # -- the sections (rebuilt on every filter change)
        self._list_host = QWidget()
        self._list_host.setObjectName("panel")
        self._list = QVBoxLayout(self._list_host)
        self._list.setContentsMargins(0, 0, 0, 0)
        self._list.setSpacing(12)
        column.addWidget(self._list_host)
        self.empty = label("", "haEmpty")
        self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        column.addWidget(self.empty)
        column.addStretch(1)
        self.scroll.setWidget(page)
        outer.addWidget(self.scroll)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._search_icon.move(12, (self.search.height() - self._search_icon.height()) // 2)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._search_icon.move(12, (self.search.height() - self._search_icon.height()) // 2)

    # ------------------------------------------------------------ filters

    def _emit(self) -> None:
        self.filters_changed.emit(self.search.text(), self._category, "")

    def _topic_changed(self, index: int) -> None:
        value = self.topic.itemData(index) or ""
        if value != self._category:
            self._category = value
            self._emit()

    def _set_mode(self, mode: str) -> None:
        self._mode = mode
        self.mode_buttons[mode].setChecked(True)
        self._rebuild()

    # ---------------------------------------------------------------- api

    def show_loading(self) -> None:
        self.empty.setText("Loading articles…")
        self.empty.show()

    def show_error(self, message: str) -> None:
        self.banner.show_message(message, "danger", "Try again")

    def set_categories(self, categories: list[tuple[str, int]], total: int) -> None:
        if self._category not in {c for c, _n in categories}:
            self._category = ""
        self.topic.blockSignals(True)
        self.topic.clear()
        self.topic.addItem(f"All Topics ({total})", "")
        for name, n in categories:
            self.topic.addItem(f"{name} ({n})", name)
        self.topic.setCurrentIndex(max(0, self.topic.findData(self._category)))
        self.topic.blockSignals(False)

    def show_articles(self, articles: list[HealthArticle], starred: set[str],
                      total: int) -> None:
        self.banner.hide()
        self._last = (list(articles), set(starred), total)
        self.count.setText(f"{total} Article{'' if total == 1 else 's'} Published")
        self.count.setVisible(bool(total))
        self._rebuild()

    def _rebuild(self) -> None:
        articles, starred, total = self._last
        while self._list.count():
            item = self._list.takeAt(0)
            if item.widget():
                item.widget().hide()               # gone at once, freed a moment later
                item.widget().deleteLater()
        self.rows = []
        if self._mode == self.INDEX:
            ordered = sorted(articles, key=lambda a: a.title.lower())
            if ordered:
                self._list.addWidget(_section_header("All articles", len(ordered)))
                self._list.addWidget(self._group(ordered, starred))
        else:
            topics: dict[str, list[HealthArticle]] = {}
            for article in articles:
                topics.setdefault(article.category, []).append(article)
            for name in sorted(topics, key=str.lower):
                self._list.addWidget(_section_header(name, len(topics[name])))
                self._list.addWidget(self._group(topics[name], starred))
        if not total:
            self.empty.setText("No articles yet. Admins add them in Content Management "
                               "→ Articles.")
        elif not articles:
            self.empty.setText("No article matches this search or topic.")
        self.empty.setVisible(not articles)

    def _group(self, articles: list[HealthArticle], starred: set[str]) -> ArticleGroup:
        rows = []
        last = len(articles) - 1
        for i, article in enumerate(articles):
            pos = "only" if last == 0 else "first" if i == 0 else "last" if i == last else "mid"
            row = ArticleRow(article, article.id in starred, alt=i % 2 == 1, pos=pos)
            row.open_requested.connect(self.open_requested.emit)
            row.star_requested.connect(self.star_requested.emit)
            rows.append(row)
        self.rows.extend(rows)
        return ArticleGroup(rows)

    def refresh_theme(self) -> None:
        self._search_icon.setPixmap(lucide.pixmap("search", 15, Theme.token("TEXT_MUTED")))
        refresh_icons(self)
        repolish(self)
        self._rebuild()


class _LinkRow(QFrame):
    """A source in the rail: publisher, title, domain. Opens in the built-in browser."""

    clicked = Signal(str, str)                # url, title

    def __init__(self, source: str, title: str, url: str) -> None:
        super().__init__()
        self.setObjectName("haLinkRow")
        self.setProperty("hover", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._url, self._title = url, title or source
        column = QVBoxLayout(self)
        column.setContentsMargins(12, 10, 12, 10)
        column.setSpacing(3)
        column.addWidget(label(source.upper(), "haLinkSource"))
        column.addWidget(label(self._title, "haLinkTitle"))
        foot = QHBoxLayout()
        foot.setSpacing(5)
        host = urlparse(url).netloc.lower()
        foot.addWidget(label(host[4:] if host.startswith("www.") else host, "haLinkDomain",
                             wrap=False))
        foot.addStretch(1)
        foot.addWidget(icon_label("external-link", 13, _accent()))
        column.addLayout(foot)

    def enterEvent(self, event) -> None:  # noqa: N802
        self.setProperty("hover", True)
        _polish_tree(self)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self.setProperty("hover", False)
        _polish_tree(self)
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._url, self._title)
        super().mouseReleaseEvent(event)


def _rail_card(title: str) -> tuple[QFrame, QVBoxLayout]:
    card = QFrame()
    card.setObjectName("detailCard")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(14, 16, 14, 16)
    layout.setSpacing(6)
    heading = QLabel(title)
    heading.setObjectName("railHeading")
    heading.setWordWrap(True)
    layout.addWidget(heading)
    return card, layout


def _rich(text: str) -> str:
    """Plain text -> label HTML with comfortable line spacing."""
    return f'<div style="line-height:155%;">{escape(text)}</div>'


class ArticleReader(QWidget):
    """One written article as a full page, laid out like the encyclopedia:

        left rail   on this page (with reading progress), sources and further
                    reading (open in the built-in browser), related entries
        main        hero header, then the article text section by section
    """

    star_requested = Signal(str)
    notebook_requested = Signal(str)
    entry_requested = Signal(str, str)        # kind, id (a linked encyclopedia entry)
    link_requested = Signal(str, str)         # url, title (a source)

    RAIL_WIDTH = 290

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._article: Optional[HealthArticle] = None
        self._starred = False
        self._links: list[tuple[str, str, str]] = []
        self._anchors: list[tuple[QPushButton, QWidget]] = []
        row = QHBoxLayout(self)
        row.setContentsMargins(22, 18, 22, 0)
        row.setSpacing(20)

        self.rail = QScrollArea()
        self.rail.setWidgetResizable(True)
        self.rail.setFrameShape(QFrame.Shape.NoFrame)
        self.rail.setFixedWidth(self.RAIL_WIDTH)
        self.rail.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        row.addWidget(self.rail)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.verticalScrollBar().valueChanged.connect(self._on_scrolled)
        row.addWidget(self.scroll, 1)
        self._page: Optional[QWidget] = None
        self.star: Optional[QPushButton] = None
        self.notice = label("", "acOk")
        self.source_rows: list[_LinkRow] = []

    # ---------------------------------------------------------------- api

    def show_article(self, article: HealthArticle, starred: bool,
                     links: list[tuple[str, str, str]]) -> None:
        """links: (kind, id, display name) for the linked entries that exist."""
        self._article, self._starred, self._links = article, starred, links
        self._anchors = []
        sections = self._sections(article)
        self.scroll.setWidget(self._build_main(article, starred, sections))
        self.rail.setWidget(self._build_rail(article, links))
        self.scroll.verticalScrollBar().setValue(0)
        self.rail.verticalScrollBar().setValue(0)
        self._on_scrolled(0)

    def set_starred(self, on: bool) -> None:
        self._starred = on
        if self.star is not None:
            from app.ui.views.account.account_widgets import set_text
            set_text(self.star, "Bookmarked" if on else "Bookmark")

    def show_notice(self, text: str) -> None:
        self.notice.setText(text)
        self.notice.setVisible(bool(text))

    def refresh_theme(self) -> None:
        if self._article is not None:            # icons and accents are baked in
            value = self.scroll.verticalScrollBar().value()
            self.show_article(self._article, self._starred, self._links)
            self.scroll.verticalScrollBar().setValue(value)
        refresh_icons(self)
        repolish(self)

    # -------------------------------------------------------------- main

    @staticmethod
    def _sections(article: HealthArticle) -> list[tuple[str, list[tuple[str, str]]]]:
        """Group the text into (heading, blocks); text before the first
        heading becomes "Overview"."""
        sections: list[tuple[str, list[tuple[str, str]]]] = []
        for kind, text in body_blocks(article.body):
            if kind == "h":
                sections.append((text, []))
            else:
                if not sections:
                    sections.append(("Overview", []))
                sections[-1][1].append((kind, text))
        return sections

    def _build_main(self, article: HealthArticle, starred: bool,
                    sections: list) -> QWidget:
        page = QWidget()
        page.setObjectName("panel")
        column = QVBoxLayout(page)
        column.setContentsMargins(0, 0, 10, 30)
        column.setSpacing(18)

        # -- hero
        hero = QFrame()
        hero.setObjectName("haHero")
        h = QVBoxLayout(hero)
        h.setContentsMargins(34, 30, 34, 28)
        h.setSpacing(10)
        chips = QHBoxLayout()
        chips.setSpacing(6)
        chips.addWidget(pill(article.category.upper(), "haHeroChip"))
        chips.addStretch(1)
        h.addLayout(chips)
        h.addWidget(label(article.title, "haHeroTitle"))
        if article.summary:
            h.addWidget(label(article.summary, "haHeroLead"))
        meta = [x for x in (article.author_name, article.meta_line(),
                            f"{len(article.references)} source"
                            f"{'' if len(article.references) == 1 else 's'}"
                            if article.references else "") if x]
        h.addWidget(label("  ·  ".join(meta), "haHeroMeta"))
        actions = QHBoxLayout()
        actions.setSpacing(8)
        self.star = button("Bookmarked" if starred else "Bookmark", "acGhost", "bookmark",
                           lambda: self.star_requested.emit(article.id))
        actions.addWidget(self.star)
        actions.addWidget(button("Save to notebook", "acGhost", "notebook-pen",
                                 lambda: self.notebook_requested.emit(article.id)))
        actions.addStretch(1)
        h.addSpacing(4)
        h.addLayout(actions)
        column.addWidget(hero)

        self.notice = label("", "acOk")
        self.notice.hide()
        column.addWidget(self.notice)

        # -- the article
        body = QFrame()
        body.setObjectName("haArticle")
        b = QVBoxLayout(body)
        b.setContentsMargins(38, 30, 38, 34)
        b.setSpacing(26)
        for heading, blocks in sections:
            section = QWidget()
            section.setObjectName("panel")
            s = QVBoxLayout(section)
            s.setContentsMargins(0, 0, 0, 0)
            s.setSpacing(10)
            s.addWidget(label(heading, "haH2"))
            bar = QFrame()
            bar.setObjectName("haH2Bar")
            bar.setFixedSize(36, 3)
            s.addWidget(bar)
            s.addSpacing(2)
            for kind, text in blocks:
                if kind == "li":
                    line = QHBoxLayout()
                    line.setContentsMargins(6, 0, 0, 0)
                    line.setSpacing(12)
                    holder = QWidget()                 # nudges the dot onto the first line
                    holder.setObjectName("panel")
                    holder.setFixedWidth(6)
                    hv = QVBoxLayout(holder)
                    hv.setContentsMargins(0, 10, 0, 0)
                    dot = QFrame()
                    dot.setObjectName("haBullet")
                    dot.setFixedSize(6, 6)
                    hv.addWidget(dot)
                    hv.addStretch(1)
                    line.addWidget(holder)
                    item = label(_rich(text), "haP")
                    item.setTextFormat(Qt.TextFormat.RichText)
                    line.addWidget(item, 1)
                    s.addLayout(line)
                else:
                    para = label(_rich(text), "haP")
                    para.setTextFormat(Qt.TextFormat.RichText)
                    s.addWidget(para)
            b.addWidget(section)
            self._anchors.append((QPushButton(), section))      # buttons set in the rail
        column.addWidget(body)

        foot = []
        if article.references:
            foot.append("Sources are listed on the left. Open them for the full, most "
                        "up-to-date information.")
        foot.append("Educational reference only, not a diagnosis or medical advice.")
        column.addWidget(label("  ".join(foot), "acSmall"))
        column.addStretch(1)
        contain(page)
        self._page = page
        return page

    # -------------------------------------------------------------- rail

    def _build_rail(self, article: HealthArticle, links: list) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        column = QVBoxLayout(holder)
        column.setContentsMargins(0, 0, 4, 20)
        column.setSpacing(14)

        # on this page + reading progress
        toc, t = _rail_card("ON THIS PAGE")
        head = t.itemAt(0).widget()
        t.removeWidget(head)
        top = QHBoxLayout()
        top.addWidget(head)
        top.addStretch(1)
        self._progress_label = QLabel("0%")
        self._progress_label.setObjectName("progressLabel")
        top.addWidget(self._progress_label)
        t.addLayout(top)
        self._progress = QProgressBar()
        self._progress.setObjectName("readProgress")
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(3)
        self._progress.setRange(0, 100)
        t.addWidget(self._progress)
        anchors = []
        for i, (_old, section) in enumerate(self._anchors):
            title = section.findChild(QLabel, "haH2").text()
            b = QPushButton(f"  {title.replace('&', '&&')}")
            b.setObjectName("tocButton")
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setMinimumHeight(31)
            b.setToolTip(title)
            b.clicked.connect(lambda _c=False, n=i: self._scroll_to(n))
            t.addWidget(b)
            anchors.append((b, section))
        self._anchors = anchors
        column.addWidget(toc)

        # sources and further reading
        self.source_rows = []
        refs = [r for r in article.references if safe_url(r.url)]
        if refs:
            card, c = _rail_card("SOURCES & FURTHER READING")
            c.addWidget(label("Opens in the built-in browser.", "acSmall"))
            c.addSpacing(2)
            for ref in refs:
                row = _LinkRow(ref.source_name, ref.citation_text, safe_url(ref.url))
                row.clicked.connect(self.link_requested.emit)
                c.addWidget(row)
                self.source_rows.append(row)
            column.addWidget(card)

        # related encyclopedia entries
        if links:
            card, c = _rail_card("RELATED IN THE ENCYCLOPEDIA")
            host = QWidget()
            host.setObjectName("panel")
            flow = FlowLayout(6, 6)
            host.setLayout(flow)
            for kind, ref_id, name in links:
                chip = button(name, "acChip", LINK_ICONS.get(kind, "circle"),
                              lambda k=kind, r=ref_id: self.entry_requested.emit(k, r))
                flow.addWidget(chip)
            c.addWidget(host)
            column.addWidget(card)
        column.addStretch(1)
        contain(holder, limit=self.RAIL_WIDTH - 40)
        return holder

    # --------------------------------------------------------- scrolling

    def _scroll_to(self, index: int) -> None:
        if 0 <= index < len(self._anchors):
            _b, section = self._anchors[index]
            y = section.mapTo(self._page, QPoint(0, 0)).y() if self._page else 0
            self.scroll.verticalScrollBar().setValue(max(0, y - 14))
            self._set_active(index)

    def _on_scrolled(self, value: int) -> None:
        if not self._anchors or self._page is None:
            return
        bar = self.scroll.verticalScrollBar()
        percent = int(value / bar.maximum() * 100) if bar.maximum() else 100
        self._progress.setValue(percent)
        self._progress_label.setText(f"{percent}%")
        current = 0
        for i, (_b, section) in enumerate(self._anchors):
            if section.mapTo(self._page, QPoint(0, 0)).y() <= value + 80:
                current = i
        if bar.maximum() and value >= bar.maximum() - 2:
            current = len(self._anchors) - 1
        self._set_active(current)

    def _set_active(self, index: int) -> None:
        for i, (b, _s) in enumerate(self._anchors):
            b.setChecked(i == index)
