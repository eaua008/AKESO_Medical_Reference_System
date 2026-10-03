"""Clinical Exchange home: the feed, its tabs and filters."""

from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QFrame, QHBoxLayout, QLineEdit, QPushButton, QScrollArea,
    QVBoxLayout, QWidget,
)

from app.models.account import PROGRAMS
from app.models.exchange import FEED_TABS, TAG_KINDS, FeedPost, Tag
from app.ui.views.account.account_widgets import Banner, button, label, refresh_icons, set_text
from app.ui.views.exchange.exchange_widgets import PostCard, SearchPicker, clear_layout


class FeedView(QWidget):
    tab_changed = Signal(str)
    filters_changed = Signal()
    open_requested = Signal(str)
    new_post_requested = Signal(str)         # "case" | "question"
    load_more_requested = Signal()
    queue_requested = Signal()
    refresh_requested = Signal()
    profile_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.tag: Optional[Tag] = None
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        self._page = QVBoxLayout(page)
        self._page.setContentsMargins(30, 22, 30, 30)
        self._page.setSpacing(14)

        self._page.addWidget(self._build_header())
        notice = Banner()
        notice.show_message("Hypothetical cases only. Never post a real patient's name, record "
                            "number, photo or exact birth date. Posts are checked before they go up.",
                            "warn")
        self._page.addWidget(notice)
        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        self._page.addWidget(self.banner)
        self._page.addWidget(self._build_tabs())
        self._page.addWidget(self._build_filters())

        self._list = QVBoxLayout()
        self._list.setSpacing(10)
        self._page.addLayout(self._list)
        self._empty = label("", "acMuted")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.hide()
        self._page.addWidget(self._empty)
        self._more = button("Load more", "acGhost", on_click=self.load_more_requested.emit)
        self._more.hide()
        self._page.addWidget(self._more, 0, Qt.AlignmentFlag.AlignHCenter)
        self._page.addStretch(1)
        self.scroll.setWidget(page)
        outer.addWidget(self.scroll)

        self._search_timer = QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(400)
        self._search_timer.timeout.connect(self.filters_changed.emit)

    # -------------------------------------------------------------- build

    def _build_header(self) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)
        text = QVBoxLayout()
        text.setSpacing(4)
        text.addWidget(label("Clinical Exchange", "acTitle"))
        text.addWidget(label("Discuss hypothetical cases with other students. Vote on the "
                             "differential, back your vote with your reasoning.", "acSubtitle"))
        row.addLayout(text, 1)
        self.queue_button = button("Moderation queue", "acGhost", "shield-alert",
                                   self.queue_requested.emit)
        self.queue_button.hide()
        row.addWidget(self.queue_button, 0, Qt.AlignmentFlag.AlignTop)
        row.addWidget(button("Ask a question", "acGhost", "message-circle",
                             lambda: self.new_post_requested.emit("question")),
                      0, Qt.AlignmentFlag.AlignTop)
        row.addWidget(button("New case", "acPrimary", "plus",
                             lambda: self.new_post_requested.emit("case")),
                      0, Qt.AlignmentFlag.AlignTop)
        return holder

    def _build_tabs(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("acTabRow")
        bar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        row = QHBoxLayout(bar)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)
        group = QButtonGroup(self)
        self._tabs: dict[str, QPushButton] = {}
        for key, text in FEED_TABS:
            tab = QPushButton(text)
            tab.setObjectName("acTab")
            tab.setCheckable(True)
            tab.setCursor(Qt.CursorShape.PointingHandCursor)
            tab.clicked.connect(lambda _c=False, k=key: self._pick_tab(k))
            group.addButton(tab)
            self._tabs[key] = tab
            row.addWidget(tab)
        row.addStretch(1)
        refresh = button("Refresh", "acLink", on_click=self.refresh_requested.emit)
        row.addWidget(refresh)
        self.current_tab = "newest"
        self._tabs["newest"].setChecked(True)
        return bar

    def _build_filters(self) -> QWidget:
        holder = QWidget()
        holder.setObjectName("panel")
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        self.search = QLineEdit()
        self.search.setObjectName("acInput")
        self.search.setPlaceholderText("Search posts…")
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(lambda _t: self._search_timer.start())
        row.addWidget(self.search, 2)
        self.tag_picker = SearchPicker("Any tag")
        self.tag_picker.activated.connect(lambda _i: self._tag_picked())
        row.addWidget(self.tag_picker, 2)
        self.system = QComboBox()
        self.system.setObjectName("acInput")
        self.system.currentIndexChanged.connect(lambda _i: self.filters_changed.emit())
        row.addWidget(self.system, 1)
        self.program = QComboBox()
        self.program.setObjectName("acInput")
        self.program.addItem("Any program", None)
        for key, text in PROGRAMS:
            self.program.addItem(text, key)
        self.program.currentIndexChanged.connect(lambda _i: self.filters_changed.emit())
        row.addWidget(self.program, 1)
        self.clear_button = button("Clear", "acLink", on_click=self.clear_filters)
        row.addWidget(self.clear_button)
        return holder

    # ---------------------------------------------------------------- api

    def set_reference(self, tags: list[Tag], body_systems: list[tuple[str, str]]) -> None:
        self.tag_picker.set_items([(f"{t.label}  ·  {TAG_KINDS.get(t.kind, t.kind)}", t)
                                   for t in tags])
        self.system.blockSignals(True)
        self.system.clear()
        self.system.addItem("Any body system", None)
        for system_id, name in body_systems:
            self.system.addItem(name, system_id)
        self.system.blockSignals(False)

    def set_moderator(self, is_mod: bool, open_reports: int = 0) -> None:
        self.queue_button.setVisible(is_mod)
        set_text(self.queue_button, f"Moderation queue ({open_reports})" if open_reports
                 else "Moderation queue")

    def filters(self) -> dict:
        return {"tag": self.tag, "body_system": self.system.currentData(),
                "program": self.program.currentData(), "search": self.search.text()}

    def set_tag(self, tag: Optional[Tag]) -> None:
        self.tag = tag
        if tag is None:
            self.tag_picker.reset()
        else:
            for i in range(self.tag_picker.count()):
                data = self.tag_picker.itemData(i)
                if data and data.kind == tag.kind and data.id == tag.id:
                    self.tag_picker.setCurrentIndex(i)
                    break
        self.filters_changed.emit()

    def clear_filters(self) -> None:
        for widget in (self.search, self.system, self.program):
            widget.blockSignals(True)
        self.search.clear()
        self.system.setCurrentIndex(0)
        self.program.setCurrentIndex(0)
        for widget in (self.search, self.system, self.program):
            widget.blockSignals(False)
        self.set_tag(None)

    def _tag_picked(self) -> None:
        data, _text = self.tag_picker.chosen()
        self.tag = data
        self.filters_changed.emit()

    def _pick_tab(self, key: str) -> None:
        self.current_tab = key
        self._tabs[key].setChecked(True)
        self.tab_changed.emit(key)

    def show_loading(self) -> None:
        self._empty.setText("Loading posts…")
        self._empty.show()

    def show_posts(self, posts: list[FeedPost], append: bool, has_more: bool) -> None:
        if not append:
            clear_layout(self._list)
        for post in posts:
            card = PostCard(post)
            card.open_requested.connect(self.open_requested.emit)
            card.tag_requested.connect(self.set_tag)
            card.profile_requested.connect(self.profile_requested.emit)
            self._list.addWidget(card)
        empty = not append and not posts
        self._empty.setText(self._empty_text() if empty else "")
        self._empty.setVisible(empty)
        self._more.setVisible(has_more)

    def show_error(self, message: str) -> None:
        self._empty.setText(message)
        self._empty.show()
        self._more.hide()

    def _empty_text(self) -> str:
        if self.current_tab == "following":
            return "You aren't following any posts yet. Posts you write or reply to are followed automatically."
        if self.current_tab == "mine":
            return "You haven't posted yet. Start with “New case”."
        if any(self.filters().values()):
            return "No posts match these filters."
        return "No posts yet. Be the first: share a case from your notebook or ask a question."

    def refresh_theme(self) -> None:
        refresh_icons(self)
