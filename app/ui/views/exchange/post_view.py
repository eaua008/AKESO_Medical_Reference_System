"""One post: the case, the poll and the discussion."""

from typing import Callable, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from app.models.account import friendly_time
from app.models.exchange import KIND_LABELS, STATUS_LABELS, PostDetail, Tag
from app.ui.views.account.account_widgets import (
    Banner, Card, button, icon_label, label, pill, refresh_icons, set_text,
)
from app.ui.views.exchange.exchange_widgets import (
    AuthorLine, PollWidget, ReplyBox, ReplyWidget, VitalsBlock, clear_layout, flow,
    refresh_small_icons, small_button, tag_chip,
)


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
        clear_layout(self._content)
        self._content.addWidget(label("Loading…", "acMuted"))

    def show_error(self, message: str) -> None:
        clear_layout(self._content)
        self._content.addWidget(label(message, "acError"))

    def show_post(self, post: PostDetail, bookmarked: bool, keep_scroll: bool = False) -> None:
        position = self.scroll.verticalScrollBar().value() if keep_scroll else 0
        if self.post is None or self.post.id != post.id:
            self._open_threads = set()              # a different post: start closed
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

    def _build_post(self, post: PostDetail) -> QFrame:
        card = Card()
        body = card.body
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
        top = QHBoxLayout()
        top.addWidget(pill(KIND_LABELS.get(post.kind, post.kind), "acPill"))
        if post.source:
            top.addWidget(pill("From the Symptom Checker" if post.source == "symptom_case"
                               else "From the Drug Interaction Checker", "acPill"))
        top.addStretch(1)
        body.addLayout(top)
        body.addWidget(label(post.title, "exDetailTitle"))
        author = AuthorLine(post.author, friendly_time(post.created_at),
                            "edited" if post.edited_at else "")
        author.profile_requested.connect(self.profile_requested.emit)
        body.addWidget(author)

        details = [x for x in (f"{post.age_range} years" if post.age_range else "",
                               (post.sex or "").capitalize(), post.setting or "") if x]
        if details:
            body.addWidget(label("PATIENT", "acFieldLabel", wrap=False))
            body.addWidget(label(" · ".join(details), "acValue"))
        if post.vitals:
            body.addWidget(VitalsBlock(post.vitals))
        data = post.case_data
        if data.get("symptoms"):
            body.addWidget(label("REPORTED SYMPTOMS", "acFieldLabel", wrap=False))
            chips = []
            for s in data["symptoms"]:
                text = f"{s.get('name')} · {s.get('intensity', '?')}/10"
                if s.get("onset"):
                    text += f" · {str(s['onset']).replace('_', ' ')}"
                chips.append(pill(text, "acPill"))
            body.addWidget(flow(chips))
        if data.get("candidate"):
            body.addWidget(label("MEDICINES", "acFieldLabel", wrap=False))
            meds = [pill(f"Adding: {data['candidate'].get('name', '')}", "acPillWarn")]
            meds += [pill(r.get("name", ""), "acPill") for r in data.get("regimen", [])]
            body.addWidget(flow(meds))
        history = (data.get("comorbidities") or []) + (data.get("conditions") or [])
        if history:
            body.addWidget(label("HISTORY / CONDITIONS", "acFieldLabel", wrap=False))
            body.addWidget(label(", ".join(history), "acValue"))
        if data.get("exposures"):
            body.addWidget(label("EXPOSURES", "acFieldLabel", wrap=False))
            body.addWidget(label(", ".join(data["exposures"]), "acValue"))
        if post.body:
            text = label(post.body, "exBody")
            text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            body.addWidget(text)
        if post.question:
            body.addWidget(label(post.question, "exQuestion"))
        if post.tags:
            chips = []
            for tag in post.tags:
                chip = tag_chip(tag)
                if tag.kind != "topic":
                    chip.clicked.connect(lambda _c=False, t=tag: self.tag_opened.emit(t))
                chips.append(chip)
            body.addWidget(flow(chips))

        actions = QHBoxLayout()
        actions.setSpacing(4)
        up = small_button(f"▲ {post.score}", "", "exVote")
        up.setCheckable(True)
        up.setChecked(post.voted)
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
        ordered = sorted(general, key=lambda r: (not r.is_best, -r.score,
                                                      r.created_at.timestamp() if r.created_at else 0))
        for reply in ordered:
            widget = self._reply_widget(reply, False, post, vote_label)
            for child in reply.children:
                widget.add_child(self._reply_widget(child, True, post, vote_label))
            card.body.addWidget(widget)
        return card

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
