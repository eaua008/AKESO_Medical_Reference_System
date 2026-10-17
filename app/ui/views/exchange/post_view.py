"""One post: the case, the poll and the discussion."""

from typing import Callable, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLineEdit, QMenu, QScrollArea, QVBoxLayout, QWidget,
)

from app.models.account import friendly_time
from app.models.exchange import KIND_LABELS, STATUS_LABELS, PostDetail, Tag
from app.ui.views.account.account_widgets import (
    Banner, Card, button, icon_label, label, pill, refresh_icons, set_text,
)
from app.ui.views.exchange.exchange_widgets import (
    AuthorLine, PollWidget, ReplyBox, ReplyWidget, VitalsBlock, clear_layout, flow,
    refresh_small_icons, small_button, tag_chip, vote_button,
)

# Discussion: how replies are ordered, and which are shown.
SORTS = [("top", "Top (best answer first)"), ("newest", "Newest"), ("oldest", "Oldest"),
         ("votes", "Most upvoted"), ("replies", "Most replies")]
SHOWS = [("all", "All replies"), ("best", "Best answer & educator verified"),
         ("unanswered", "Without replies yet"), ("mine", "My replies")]
from app.ui.components.akeso_loader import LoadingHold, LoadingLabel


class PostView(QWidget):
    back_requested = Signal()
    refresh_requested = Signal()
    post_action = Signal(str)                # follow, unfollow, bookmark, unbookmark, notebook,
                                             # report, edit, delete, moderate, upvote, unvote
    reply_action = Signal(str, str)          # action, reply id
    reply_upvote = Signal(str, bool)
    reply_submitted = Signal(object, str, bool)   # parent id or None, body, anonymous
    option_comment = Signal(str, str, bool)       # poll choice id, body, anonymous
    poll_vote = Signal(str)
    poll_suggest = Signal(object, str)
    poll_reveal = Signal()
    tag_opened = Signal(object)              # Tag -> open in the encyclopedia
    profile_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.post: Optional[PostDetail] = None
        self.checker: Optional[Callable[[str], Optional[str]]] = None
        self.diseases: list[tuple[str, str]] = []
        self._reply_widgets: dict[str, ReplyWidget] = {}
        self._option_boxes: dict[str, ReplyBox] = {}
        self._open_threads: set = set()           # choices whose comments are open
        # Discussion search, sort and filter: kept while the post refreshes
        # (after a vote or a reply), reset when another post opens.
        self._query = ""
        self._sort = "top"
        self._show = "all"
        self._thread_items: list = []             # (reply, widget, [(child, widget)])
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page = QWidget()
        page.setObjectName("panel")
        self._page = QVBoxLayout(page)
        self._page.setContentsMargins(30, 18, 30, 30)
        self._page.setSpacing(14)

        top = QHBoxLayout()
        self.back_button = button("Back to the feed", "acLink", "arrow-left",
                                  self.back_requested.emit)     # hidden in a PageSheet
        top.addWidget(self.back_button)
        top.addStretch(1)
        top.addWidget(button("Refresh", "acLink", on_click=self.refresh_requested.emit))
        self._page.addLayout(top)
        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        self._page.addWidget(self.banner)
        self._content = QVBoxLayout()
        self._content.setSpacing(14)
        self._page.addLayout(self._content)
        self._page.addStretch(1)
        self.scroll.setWidget(page)
        outer.addWidget(self.scroll)
        self.reply_box: Optional[ReplyBox] = None
        self.bookmarked = False

    # ---------------------------------------------------------------- api

    def show_loading(self) -> None:
        LoadingHold.of(self).begin()                  # the loader shows for at least 3 s
        clear_layout(self._content)
        loading = LoadingLabel("", "acMuted")
        loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading.set_loading("Loading the discussion…")
        self._content.addWidget(loading)

    def show_error(self, message: str) -> None:
        if LoadingHold.of(self).wait(self.show_error, message):
            return
        clear_layout(self._content)
        self._content.addWidget(label(message, "acError"))

    def show_post(self, post: PostDetail, bookmarked: bool, keep_scroll: bool = False) -> None:
        if LoadingHold.of(self).wait(self.show_post, post, bookmarked, keep_scroll):
            return
        position = self.scroll.verticalScrollBar().value() if keep_scroll else 0
        if self.post is None or self.post.id != post.id:
            self._open_threads = set()              # a different post: start closed
            self._query, self._sort, self._show = "", "top", "all"
        self.post = post
        self.bookmarked = bookmarked
        clear_layout(self._content)
        self._reply_widgets.clear()
        self._option_boxes.clear()
        self._content.addWidget(self._build_post(post))
        if post.poll is not None:
            poll = PollWidget(post.poll, post.is_author, post.is_open, self.diseases,
                              thread_for=self._option_thread, open_threads=self._open_threads)
            poll.vote_requested.connect(self.poll_vote.emit)
            poll.suggest_requested.connect(self.poll_suggest.emit)
            poll.reveal_requested.connect(self.poll_reveal.emit)
            self._content.addWidget(poll)
        self._content.addWidget(self._build_discussion(post))
        if keep_scroll:
            self.scroll.verticalScrollBar().setValue(position)
        else:
            self.scroll.verticalScrollBar().setValue(0)

    # -------------------------------------------------------------- build

    def _section(self, title: str, icon: str) -> tuple[QFrame, QVBoxLayout]:
        """A titled panel, like the extras in the composer (patient, tags, poll)."""
        panel = QFrame()
        panel.setObjectName("exAttachPanel")
        column = QVBoxLayout(panel)
        column.setContentsMargins(14, 10, 14, 12)
        column.setSpacing(8)
        head = QHBoxLayout()
        head.setSpacing(8)
        head.addWidget(icon_label(icon, 15), 0, Qt.AlignmentFlag.AlignVCenter)
        head.addWidget(label(title, "exAttachTitle", wrap=False), 1)
        column.addLayout(head)
        return panel, column

    def _build_post(self, post: PostDetail) -> QFrame:
        """The post laid out like the composer that wrote it: who posted and
        what kind, the title and text, the patient in a panel of its own, the
        question, tags, then the actions under a rule."""
        card = QFrame()
        card.setObjectName("exPostComposer")
        outer = QVBoxLayout(card)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        body = QVBoxLayout()
        body.setContentsMargins(24, 18, 24, 16)
        body.setSpacing(12)
        outer.addLayout(body)

        if post.status != "open":
            note = Banner()
            if post.status in ("hidden", "removed"):
                detail = ". Only the author and admins can see it."
            elif post.status == "locked":
                detail = ". No new replies or votes."
            else:
                detail = "."
            note.show_message(STATUS_LABELS.get(post.status, post.status) + detail,
                              "danger" if post.status != "locked" else "warn")
            body.addWidget(note)

        # who posted, and what kind of post it is
        top = QHBoxLayout()
        top.setSpacing(6)
        author = AuthorLine(post.author, friendly_time(post.created_at),
                            "edited" if post.edited_at else "")
        author.profile_requested.connect(self.profile_requested.emit)
        top.addWidget(author, 1)
        top.addWidget(pill(KIND_LABELS.get(post.kind, post.kind), "acPill"))
        if post.source:
            top.addWidget(pill("From the Symptom Checker" if post.source == "symptom_case"
                               else "From the Drug Interaction Checker", "acPill"))
        body.addLayout(top)

        # the post itself
        body.addWidget(label(post.title, "exDetailTitle"))
        if post.body:
            text = label(post.body, "exBody")
            text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            body.addWidget(text)

        # patient details (de-identified), one panel
        data = post.case_data
        details = [x for x in (f"{post.age_range} years" if post.age_range else "",
                               (post.sex or "").capitalize(), post.setting or "") if x]
        history = (data.get("comorbidities") or []) + (data.get("conditions") or [])
        if details or post.vitals or data.get("symptoms") or data.get("candidate")                 or history or data.get("exposures"):
            panel, column = self._section("Patient details (de-identified)", "user")
            if details:
                column.addWidget(flow([pill(x, "acPill") for x in details]))
            if post.vitals:
                column.addWidget(VitalsBlock(post.vitals))
            if data.get("symptoms"):
                column.addWidget(label("REPORTED SYMPTOMS", "acFieldLabel", wrap=False))
                chips = []
                for s in data["symptoms"]:
                    chip = f"{s.get('name')} · {s.get('intensity', '?')}/10"
                    if s.get("onset"):
                        chip += f" · {str(s['onset']).replace('_', ' ')}"
                    chips.append(pill(chip, "acPill"))
                column.addWidget(flow(chips))
            if data.get("candidate"):
                column.addWidget(label("MEDICINES", "acFieldLabel", wrap=False))
                meds = [pill(f"Adding: {data['candidate'].get('name', '')}", "acPillWarn")]
                meds += [pill(r.get("name", ""), "acPill") for r in data.get("regimen", [])]
                column.addWidget(flow(meds))
            if history:
                column.addWidget(label("HISTORY / CONDITIONS", "acFieldLabel", wrap=False))
                column.addWidget(flow([pill(x, "acPill") for x in history]))
            if data.get("exposures"):
                column.addWidget(label("EXPOSURES", "acFieldLabel", wrap=False))
                column.addWidget(flow([pill(x, "acPill") for x in data["exposures"]]))
            body.addWidget(panel)

        if post.question:
            body.addWidget(label(post.question, "exQuestion"))
        if post.tags:
            panel, column = self._section("Tags", "tag")
            chips = []
            for tag in post.tags:
                chip = tag_chip(tag)
                if tag.kind != "topic":
                    chip.clicked.connect(lambda _c=False, t=tag: self.tag_opened.emit(t))
                chips.append(chip)
            column.addWidget(flow(chips))
            body.addWidget(panel)

        rule = QFrame()
        rule.setObjectName("exComposerRule")
        rule.setFixedHeight(1)
        body.addWidget(rule)

        actions = QHBoxLayout()
        actions.setSpacing(4)
        up = vote_button(post.score, post.voted)
        up.setEnabled(not post.is_author and post.status in ("open", "locked"))
        up.clicked.connect(lambda on: self.post_action.emit("upvote" if on else "unvote"))
        actions.addWidget(up)
        follow = small_button("Following" if post.following else "Follow", "bell")
        follow.setToolTip("Get notified about new replies and the answer reveal")
        follow.clicked.connect(lambda: self.post_action.emit(
            "unfollow" if post.following else "follow"))
        actions.addWidget(follow)
        star = small_button("Bookmarked" if self.bookmarked else "Bookmark", "bookmark")
        star.clicked.connect(lambda: self.post_action.emit(
            "unbookmark" if self.bookmarked else "bookmark"))
        actions.addWidget(star)
        actions.addWidget(self._action_button("Save to notebook", "notebook-pen", "notebook"))
        if post.is_author:
            if post.status == "open":
                actions.addWidget(self._action_button("Edit", "pencil", "edit"))
            actions.addWidget(self._action_button("Delete", "trash-2", "delete"))
        else:
            actions.addWidget(self._action_button("Report", "flag", "report"))
        if post.can_moderate:
            actions.addWidget(self._action_button("Moderate", "shield-alert", "moderate"))
        actions.addStretch(1)
        body.addLayout(actions)
        return card

    def _action_button(self, text: str, icon: str, action: str):
        b = small_button(text, icon)
        b.clicked.connect(lambda: self.post_action.emit(action))
        return b

    def _option_thread(self, option_id: str) -> QWidget:
        """The comments under one poll choice, and a box to add one."""
        post = self.post
        host = QFrame()
        host.setObjectName("panel")              # transparent inside the choice row
        column = QVBoxLayout(host)
        column.setContentsMargins(0, 6, 0, 2)
        column.setSpacing(6)
        vote_label = post.poll.label_for(post.poll.my_option) if post.poll else ""
        comments = sorted((r for r in post.replies if r.option_id == option_id),
                          key=lambda r: r.created_at.timestamp() if r.created_at else 0)
        for reply in comments:
            widget = self._reply_widget(reply, False, post, vote_label)
            for child in reply.children:
                widget.add_child(self._reply_widget(child, True, post, vote_label))
            column.addWidget(widget)
        if not comments:
            column.addWidget(label("No comments on this choice yet.", "acSmall"))
        if post.is_open:
            name = post.poll.label_for(option_id) if post.poll else "this choice"
            box = ReplyBox(f"Comment on {name}: why it fits, or why not…", vote_label,
                           compact=True, checker=self.checker)
            set_text(box.send, "Comment")
            box.submitted.connect(lambda body, anon, oid=option_id:
                                  self.option_comment.emit(oid, body, anon))
            self._option_boxes[option_id] = box
            column.addWidget(box)
        return host

    def option_box(self, option_id: str) -> Optional[ReplyBox]:
        return self._option_boxes.get(option_id)

    def _build_discussion(self, post: PostDetail) -> QFrame:
        general = [r for r in post.replies if not r.option_id]
        count = len(general) + sum(len(r.children) for r in general)
        card = Card(f"Discussion ({count})", "", "message-circle")
        vote_label = post.poll.label_for(post.poll.my_option) if post.poll else ""
        if post.is_open:
            self.reply_box = ReplyBox(vote_label=vote_label, checker=self.checker)
            self.reply_box.submitted.connect(lambda body, anon: self.reply_submitted.emit(None, body, anon))
            card.body.addWidget(self.reply_box)
            if post.poll and not post.poll.my_option and not post.poll.revealed and not post.is_author:
                card.body.addWidget(label("Tip: vote in the poll first, so your reply shows which "
                                          "diagnosis you're arguing for.", "acSmall"))
        else:
            self.reply_box = None
            card.body.addWidget(label("Replies are closed on this post.", "acMuted"))
        if not general:
            card.body.addWidget(label("No replies yet. Start the discussion.", "acMuted"))
            return card

        # Search and Sort & filter, on the Discussion heading's line.
        self._search = QLineEdit()
        self._search.setObjectName("filterSearch")
        self._search.setPlaceholderText("Search replies or authors\u2026")
        self._search.setClearButtonEnabled(True)
        self._search.setFixedHeight(32)
        self._search.setMaximumWidth(280)
        self._search.setText(self._query)
        self._search.textChanged.connect(self._on_search)
        card.head.addWidget(self._search, 1)
        self._filter_button = small_button("Sort & filter", "funnel")
        self._filter_button.setMenu(self._filter_menu())
        card.head.addWidget(self._filter_button)

        self._match_note = label("", "acSmall")
        card.body.addWidget(self._match_note)
        self._thread = QVBoxLayout()
        self._thread.setSpacing(10)
        card.body.addLayout(self._thread)
        self._thread_items = []
        for reply in general:
            widget = self._reply_widget(reply, False, post, vote_label)
            kids = []
            for child in reply.children:
                child_widget = self._reply_widget(child, True, post, vote_label)
                widget.add_child(child_widget)
                kids.append((child, child_widget))
            self._thread_items.append((reply, widget, kids))
        self._apply_discussion()
        return card

    # ------------------------------------------------- discussion: search, sort, filter

    def _filter_menu(self) -> QMenu:
        menu = QMenu(self)
        menu.setObjectName("exMenu")
        for title, options, current, setter in (
                ("Sort by", SORTS, self._sort, self._set_sort),
                ("Show", SHOWS, self._show, self._set_show)):
            menu.addSection(title)
            group = QActionGroup(menu)
            group.setExclusive(True)
            for key, text in options:
                action = QAction(text, menu)
                action.setCheckable(True)
                action.setChecked(key == current)
                action.triggered.connect(lambda _c=False, k=key, s=setter: s(k))
                group.addAction(action)
                menu.addAction(action)
        return menu

    def _set_sort(self, key: str) -> None:
        self._sort = key
        self._apply_discussion()

    def _set_show(self, key: str) -> None:
        self._show = key
        self._apply_discussion()

    def _on_search(self, text: str) -> None:
        self._query = text
        self._apply_discussion()

    @staticmethod
    def _matches(reply, words: list[str]) -> bool:
        author = reply.author
        haystack = " ".join((reply.body or "", author.name or "", author.handle or "",
                             "anonymous" if author.anonymous else "")).lower()
        return all(word in haystack for word in words)

    def _apply_discussion(self) -> None:
        """Order and show the replies for the current search, sort and filter."""
        if not self._thread_items:
            return
        stamp = (lambda r: r.created_at.timestamp() if r.created_at else 0)
        keys = {
            "top": lambda r: (not r.is_best, -r.score, stamp(r)),
            "newest": lambda r: -stamp(r),
            "oldest": stamp,
            "votes": lambda r: (-r.score, -stamp(r)),
            "replies": lambda r: (-len(r.children), -stamp(r)),
        }
        ordered = sorted(self._thread_items, key=lambda item: keys[self._sort](item[0]))
        words = self._query.lower().split()
        shown = 0
        for reply, widget, kids in ordered:
            self._thread.removeWidget(widget)
            self._thread.addWidget(widget)
            keep = {
                "all": True,
                "best": reply.is_best or reply.verified
                        or any(c.verified for c, _w in kids),
                "unanswered": not kids,
                "mine": reply.author.is_me or reply.is_mine
                        or any(c.is_mine for c, _w in kids),
            }[self._show]
            child_hits = [self._matches(child, words) for child, _w in kids] if words else []
            hit = not words or self._matches(reply, words) or any(child_hits)
            visible = keep and hit
            widget.setVisible(visible)
            # While searching, a matching reply shows its whole thread, and a
            # matching answer shows with its parent but without unrelated answers.
            parent_hit = not words or self._matches(reply, words)
            for (child, child_widget), child_hit in zip(kids, child_hits or [True] * len(kids)):
                child_widget.setVisible(parent_hit or child_hit)
            shown += visible
        total = len(self._thread_items)
        filtering = bool(words) or self._show != "all"
        if filtering:
            self._match_note.setText(
                f"Showing {shown} of {total} threads." if shown else
                "No replies match. Try another word, or Sort & filter \u2192 All replies.")
        self._match_note.setVisible(filtering)
        label_text = "Sort & filter" if not filtering and self._sort == "top" else \
            f"{dict(SORTS)[self._sort].split(' (')[0]}" + (" \u00b7 filtered" if filtering else "")
        self._filter_button.setText(f" {label_text}")       # the gap after its icon

    def _reply_widget(self, reply, child: bool, post: PostDetail, vote_label: str) -> ReplyWidget:
        widget = ReplyWidget(reply, child=child, post_open=post.is_open,
                             is_post_author=post.is_author, can_moderate=post.can_moderate,
                             vote_label=vote_label, checker=self.checker)
        widget.action.connect(self.reply_action.emit)
        widget.upvote.connect(self.reply_upvote.emit)
        widget.answer_submitted.connect(self.reply_submitted.emit)
        widget.profile_requested.connect(self.profile_requested.emit)
        self._reply_widgets[reply.id] = widget
        return widget

    def box_for(self, parent_id: Optional[str]) -> Optional[ReplyBox]:
        if parent_id is None:
            return self.reply_box
        widget = self._reply_widgets.get(parent_id)
        return widget.box if widget else None

    def refresh_theme(self) -> None:
        refresh_icons(self)
        refresh_small_icons(self)


__all__ = ["PostView", "Tag", "icon_label", "set_text"]
