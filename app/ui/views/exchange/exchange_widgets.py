"""Building blocks for Clinical Exchange: cards, author lines, the poll,
replies and the reply box."""

from typing import Optional

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QCompleter, QFrame, QHBoxLayout, QLabel, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QVBoxLayout, QWidget,
)

from app.core import lucide
from app.core.theme import Theme
from app.models.account import ROLE_LABELS
from app.models.exchange import (
    KIND_LABELS, STATUS_LABELS, TAG_KINDS, Author, FeedPost, Poll, Reply, Tag, time_ago,
)
from app.ui.components.avatar_cache import AvatarCache
from app.ui.components.fluid import contain
from app.ui.views.account.account_widgets import (
    button, icon_label, label, pill, repolish, set_text,
)
from app.ui.views.compare_view import FlowLayout


def clear_layout(layout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().hide()
            item.widget().deleteLater()
        elif item.layout():
            clear_layout(item.layout())


def flow(widgets: list[QWidget], spacing: int = 6) -> QWidget:
    holder = QWidget()
    holder.setObjectName("panel")
    layout = FlowLayout(spacing, spacing)
    holder.setLayout(layout)
    for widget in widgets:
        layout.addWidget(widget)
    return holder


def small_button(text: str, icon: str = "", name: str = "exAction") -> QPushButton:
    widget = QPushButton(f" {text}" if icon else text)
    widget.setObjectName(name)
    widget.setCursor(Qt.CursorShape.PointingHandCursor)
    if icon:
        widget.setProperty("exIcon", icon)
        widget.setIcon(lucide.icon(icon, 14, Theme.token("TEXT_MUTED")))
        widget.setIconSize(QSize(14, 14))
    return widget


def refresh_small_icons(root: QWidget) -> None:
    for child in root.findChildren(QPushButton):
        name = child.property("exIcon")
        if name:
            child.setIcon(lucide.icon(name, 14, Theme.token("TEXT_MUTED")))


class SearchPicker(QComboBox):
    """A drop-down you can type into: matches anywhere in the name."""

    def __init__(self, placeholder: str, editable_text: bool = False) -> None:
        super().__init__()
        self.setObjectName("acInput")
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.lineEdit().setPlaceholderText(placeholder)
        self._free_text = editable_text
        completer = QCompleter(self.model(), self)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.setCompleter(completer)
        self.setMinimumContentsLength(10)
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)

    def set_items(self, items: list[tuple[str, object]]) -> None:
        self.blockSignals(True)
        self.clear()
        for text, data in items:
            self.addItem(text, data)
        self.setCurrentIndex(-1)
        self.lineEdit().clear()
        self.blockSignals(False)

    def chosen(self) -> tuple[Optional[object], str]:
        """(data of the matching item or None, the typed text)."""
        text = self.currentText().strip()
        index = self.findText(text, Qt.MatchFlag.MatchFixedString)
        return (self.itemData(index) if index >= 0 else None), text

    def reset(self) -> None:
        self.setCurrentIndex(-1)
        self.lineEdit().clear()


AVATAR_SIZE = 24


class AuthorLine(QWidget):
    """ "(photo) Name · Nursing · Verified · Educator · 3h ago" ; the name
    opens the profile when the author has a public profile. The photo shows
    when the author allows it (otherwise their initial); anonymous posts get
    a plain "no face" icon instead."""

    profile_requested = Signal(str)        # handle

    def __init__(self, author: Author, when: str = "", extra: str = "") -> None:
        super().__init__()
        self.setObjectName("panel")
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        if author.anonymous and not author.is_me and author.name == "Anonymous student":
            face = icon_label("user-x", 14, Theme.token("TEXT_MUTED"))
            face.setFixedSize(AVATAR_SIZE, AVATAR_SIZE)
            face.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.addWidget(face)
        else:
            self.avatar = QLabel()
            self.avatar.setObjectName("panel")
            AvatarCache.apply(self.avatar, author.avatar_path, author.name, AVATAR_SIZE)
            row.addWidget(self.avatar)
        if author.handle:
            name = QPushButton(author.name)
            name.setObjectName("exAuthorLink")
            name.setCursor(Qt.CursorShape.PointingHandCursor)
            name.setToolTip(f"@{author.handle}: open profile")
            name.clicked.connect(lambda: self.profile_requested.emit(author.handle))
            row.addWidget(name)
        else:
            row.addWidget(label(author.name, "acRowTitle", wrap=False))
        if author.anonymous and author.name != "Anonymous student":
            row.addWidget(pill("Posted anonymously" if not author.is_me else "Anonymous to others",
                               "acPill"))
        if author.is_educator:
            row.addWidget(pill(ROLE_LABELS.get(author.role or "", "Educator"), "acPillGood"))
        if author.verified_domain:
            badge = icon_label("badge-check", 14, Theme.token("SUCCESS"))
            badge.setToolTip(f"Verified student · {author.verified_domain}")
            row.addWidget(badge)
        details = [author.program_label, when, extra]
        text = " · ".join(d for d in details if d)
        if text:
            row.addWidget(label(text, "acSmall", wrap=False))
        row.addStretch(1)


def tag_chip(tag: Tag) -> QPushButton:
    chip = QPushButton(tag.label.replace("&", "&&"))
    chip.setObjectName("exTag")
    chip.setCursor(Qt.CursorShape.PointingHandCursor)
    chip.setToolTip(f"{TAG_KINDS.get(tag.kind, tag.kind)}: {tag.label}")
    return chip


class PostCard(QFrame):
    """One post in the feed."""

    open_requested = Signal(str)
    tag_requested = Signal(object)         # Tag
    profile_requested = Signal(str)

    def __init__(self, post: FeedPost) -> None:
        super().__init__()
        self.setObjectName("exPostCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._id = post.id
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        top = QHBoxLayout()
        top.setSpacing(6)
        top.addWidget(pill(KIND_LABELS.get(post.kind, post.kind), "acPill"))
        if post.age_range or post.sex:
            top.addWidget(label(" ".join(x for x in (f"{post.age_range} y/o" if post.age_range
                                                     else "", post.sex or "") if x), "acSmall",
                                wrap=False))
        if post.status != "open":
            top.addWidget(pill(STATUS_LABELS.get(post.status, post.status),
                               "acPillDanger" if post.status != "locked" else "acPillWarn"))
        top.addStretch(1)
        if post.has_poll:
            top.addWidget(pill("Answer revealed" if post.revealed else "Poll open",
                               "acPillGood" if post.revealed else "acPillWarn"))
        if post.has_best:
            top.addWidget(pill("Best answer chosen", "acPillGood"))
        layout.addLayout(top)

        layout.addWidget(label(post.title, "exPostTitle"))
        if post.excerpt:
            layout.addWidget(label(post.excerpt, "acMuted"))
        if post.tags:
            chips = []
            for tag in post.tags[:6]:
                chip = tag_chip(tag)
                chip.clicked.connect(lambda _c=False, t=tag: self.tag_requested.emit(t))
                chips.append(chip)
            layout.addWidget(flow(chips))

        bottom = QHBoxLayout()
        author = AuthorLine(post.author, time_ago(post.last_activity_at or post.created_at))
        author.profile_requested.connect(self.profile_requested.emit)
        bottom.addWidget(author, 1)
        stats = f"▲ {post.score}   ·   {post.reply_count} " \
                f"{'reply' if post.reply_count == 1 else 'replies'}"
        if post.following:
            stats += "   ·   Following"
        stats_label = label(stats, "exStat", wrap=False)
        stats_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        bottom.addWidget(stats_label)
        layout.addLayout(bottom)
        contain(self, limit=200, buttons=False)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_requested.emit(self._id)
        super().mouseReleaseEvent(event)


class VitalsBlock(QFrame):
    """Recorded vitals; values outside typical adult ranges are marked."""

    FIELDS = [("temperature", "Temp", "°C", lambda v: v >= 38.0 or v < 36.0),
              ("heart_rate", "HR", "bpm", lambda v: v > 100 or v < 60),
              ("bp", "BP", "mmHg", None),
              ("resp_rate", "RR", "/min", lambda v: v > 20 or v < 12),
              ("spo2", "SpO₂", "%", lambda v: v < 95)]

    def __init__(self, vitals: dict) -> None:
        super().__init__()
        self.setObjectName("exVitals")
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 8, 12, 8)
        row.setSpacing(18)
        for key, name, unit, flag in self.FIELDS:
            if key == "bp":
                if not vitals.get("bp_systolic"):
                    continue
                value = f"{vitals.get('bp_systolic')}/{vitals.get('bp_diastolic')}"
                flagged = (vitals.get("bp_systolic", 120) >= 140 or vitals.get("bp_systolic", 120) < 90
                           or vitals.get("bp_diastolic", 80) >= 90)
            else:
                if vitals.get(key) in (None, ""):
                    continue
                raw = vitals.get(key)
                value = f"{raw:.1f}" if isinstance(raw, float) else str(raw)
                try:
                    flagged = bool(flag and flag(float(raw)))
                except (TypeError, ValueError):
                    flagged = False
            box = QVBoxLayout()
            box.setSpacing(0)
            number = label(f"{value}", "exVitalValue", wrap=False)
            number.setProperty("flag", "true" if flagged else "false")
            if flagged:
                number.setToolTip("Outside the typical adult resting range")
            box.addWidget(number)
            box.addWidget(label(f"{name} {unit}", "acSmall", wrap=False))
            row.addLayout(box)
        row.addStretch(1)


class PollWidget(QFrame):
    """The differential poll: vote, see results after voting, suggest a
    diagnosis; the author reveals the intended answer."""

    vote_requested = Signal(str)            # option id ("" = take my vote back)
    suggest_requested = Signal(object, str)  # disease id or None, typed label
    reveal_requested = Signal()

    def __init__(self, poll: Poll, is_author: bool, is_open: bool,
                 diseases: list[tuple[str, str]], thread_for=None,
                 open_threads: Optional[set] = None) -> None:
        """thread_for(option_id) -> QWidget builds a choice's comment thread
        (the post view supplies it); open_threads: choices whose thread was
        open before a reload, so it stays open."""
        super().__init__()
        self.setObjectName("acCard")
        self._thread_for = thread_for
        self.open_threads: set = open_threads if open_threads is not None else set()
        self._threads: dict[str, QWidget] = {}
        self._comment_buttons: dict[str, QPushButton] = {}
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        head = QHBoxLayout()
        head.addWidget(icon_label("chart-bar", 18))
        head.addWidget(label("Differential poll: what's the diagnosis?", "acCardTitle"), 1)
        if poll.total is not None:
            head.addWidget(label(f"{poll.total} vote{'s' if poll.total != 1 else ''}", "acSmall",
                                 wrap=False))
        layout.addLayout(head)

        # Results, the intended answer and "Why" are shown once you have
        # voted (the server only sends them then); the author always sees them.
        unlocked = is_author or poll.my_option is not None or poll.show_results
        # Before the reveal a vote can be changed or taken back. After it, a
        # student who has not voted gets one final vote, which unlocks the answer.
        can_vote = is_open and not is_author and not (poll.revealed and poll.my_option)
        closed = poll.revealed or not is_open          # no new suggestions
        if poll.revealed and unlocked:
            note = "The author revealed the intended answer."
        elif poll.revealed:
            note = ("The author has revealed the intended answer. Vote to see it and how "
                    "others voted. Your vote is final once you cast it.")
        elif is_author:
            note = "You wrote this case, so you don't vote. Reveal the answer when discussion settles."
        elif poll.my_option:
            note = "Your vote is shown next to your replies. You can change it until the answer is revealed."
        else:
            note = "Vote to see how others voted. Your choice appears on your replies as your justification."
        layout.addWidget(label(note, "acSmall"))

        total = max(poll.total or 0, 1)
        for option in poll.options:
            row = QFrame()
            row.setObjectName("exPollRow")
            mine = option.id == poll.my_option
            answer = unlocked and option.id == poll.revealed_option
            row.setProperty("mine", "true" if mine else "false")
            row.setProperty("answer", "true" if answer else "false")
            inner = QVBoxLayout(row)
            inner.setContentsMargins(12, 8, 12, 8)
            inner.setSpacing(5)
            line = QHBoxLayout()
            line.setSpacing(8)
            line.addWidget(label(option.label, "acRowTitle"), 1)
            if not option.by_author:
                line.addWidget(pill("Suggested", "acPill"))
            if answer:
                line.addWidget(pill("Intended answer", "acPillGood"))
            if mine:
                line.addWidget(pill("Your vote", "acPill"))
            if option.votes is not None:
                share = round(100 * option.votes / total)
                line.addWidget(label(f"{share}% · {option.votes}", "exStat", wrap=False))
            if can_vote:
                vote = small_button("Voted" if mine else "Vote", "", "exVote")
                vote.setCheckable(True)
                vote.setChecked(mine)
                vote.clicked.connect(lambda _c=False, oid=option.id, m=mine:
                                     self.vote_requested.emit("" if m else oid))
                line.addWidget(vote)
            if thread_for is not None and (is_open or option.comments):
                count = f" ({option.comments})" if option.comments else ""
                talk = small_button(f"Comment{count}", "message-circle")
                talk.setCheckable(True)
                talk.setToolTip(f"Discuss “{option.label}”: why it fits or doesn't")
                talk.clicked.connect(lambda _c=False, oid=option.id, box=inner:
                                     self._toggle_thread(oid, box))
                line.addWidget(talk)
                self._comment_buttons[option.id] = talk
            inner.addLayout(line)
            if option.votes is not None:
                bar = QProgressBar()
                bar.setObjectName("exPollBar")
                bar.setProperty("answer", "true" if answer else "false")
                bar.setTextVisible(False)
                bar.setFixedHeight(6)
                bar.setRange(0, total)
                bar.setValue(option.votes)
                inner.addWidget(bar)
            layout.addWidget(row)
            if option.id in self.open_threads and thread_for is not None:
                self._toggle_thread(option.id, inner, force=True)

        if poll.revealed and unlocked and poll.explanation:
            layout.addWidget(label("WHY", "acFieldLabel", wrap=False))
            layout.addWidget(label(poll.explanation, "exBody"))

        if not closed:
            suggest = QHBoxLayout()
            suggest.setSpacing(8)
            self.picker = SearchPicker("Suggest a diagnosis (pick or type)…", editable_text=True)
            self.picker.set_items([(name, disease_id) for disease_id, name in diseases])
            suggest.addWidget(self.picker, 1)
            add = button("Suggest", "acGhost", "plus", self._suggest)
            suggest.addWidget(add)
            layout.addLayout(suggest)
        if is_author and not poll.revealed and poll.options:
            layout.addWidget(button("Reveal the intended answer", "acPrimary", "sparkles",
                                    self.reveal_requested.emit), 0, Qt.AlignmentFlag.AlignLeft)

    def _toggle_thread(self, option_id: str, box: QVBoxLayout, force: bool = False) -> None:
        thread = self._threads.get(option_id)
        if thread is None:
            thread = self._thread_for(option_id)
            self._threads[option_id] = thread
            box.addWidget(thread)
            show = True
        else:
            show = force or not thread.isVisible()
        thread.setVisible(show)
        (self.open_threads.add if show else self.open_threads.discard)(option_id)
        button = self._comment_buttons.get(option_id)
        if button is not None:
            button.setChecked(show)

    def _suggest(self) -> None:
        disease_id, text = self.picker.chosen()
        self.suggest_requested.emit(disease_id, text)
        self.picker.reset()


class ReplyBox(QFrame):
    """Write a reply (or an answer to a reply)."""

    submitted = Signal(str, bool)            # body, anonymous

    def __init__(self, placeholder: str = "Add to the discussion…", vote_label: str = "",
                 compact: bool = False, checker=None) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._checker = checker
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        self.text = QPlainTextEdit()
        self.text.setObjectName("acInput")
        self.text.setPlaceholderText(placeholder)
        self.text.setFixedHeight(64 if compact else 90)
        self.text.textChanged.connect(self._check)
        layout.addWidget(self.text)
        self.warning = label("", "acError")
        self.warning.hide()
        layout.addWidget(self.warning)
        row = QHBoxLayout()
        self.anonymous = QCheckBox("Reply anonymously")
        self.anonymous.setToolTip("Others see “Anonymous student”. Moderators can "
                                  "still see who wrote it.")
        row.addWidget(self.anonymous)
        if vote_label:
            row.addWidget(label(f"Your poll vote ({vote_label}) will show on this reply.",
                                "acSmall"), 1)
        else:
            row.addStretch(1)
        self.send = button("Reply", "acPrimary", "reply", self._submit)
        row.addWidget(self.send)
        layout.addLayout(row)

    def _check(self) -> None:
        message = self._checker(self.text.toPlainText()) if self._checker else None
        self.warning.setText(message or "")
        self.warning.setVisible(bool(message))
        self.send.setEnabled(not message and bool(self.text.toPlainText().strip()))

    def _submit(self) -> None:
        self.send.setEnabled(False)
        self.submitted.emit(self.text.toPlainText(), self.anonymous.isChecked())

    def done(self) -> None:
        self.text.clear()
        self.anonymous.setChecked(False)
        self.send.setEnabled(False)

    def failed(self, message: str) -> None:
        self.warning.setText(message)
        self.warning.show()
        self.send.setEnabled(True)


class ReplyWidget(QFrame):
    """One reply, with its answers underneath (one level)."""

    action = Signal(str, str)                # action name, reply id
    upvote = Signal(str, bool)
    answer_submitted = Signal(str, str, bool)   # parent id, body, anonymous
    profile_requested = Signal(str)

    def __init__(self, reply: Reply, *, child: bool = False, post_open: bool = True,
                 is_post_author: bool = False, can_moderate: bool = False,
                 vote_label: str = "", checker=None) -> None:
        super().__init__()
        self.setObjectName("exChildReply" if child else "exReply")
        self.setProperty("best", "true" if reply.is_best else "false")
        self._reply = reply
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(6)

        badges = []
        if reply.is_best:
            badges.append(pill("★ Best answer", "acPillGood"))
        if reply.verified:
            badges.append(pill("✓ Educator verified", "acPillGood"))
        if reply.voted_label:
            text = f"Voted: {reply.voted_label}"
            if reply.current_label and reply.current_label != reply.voted_label:
                text += f" → now {reply.current_label}"
            vote_pill = pill(text, "acPill")
            vote_pill.setToolTip("What this student had voted for in the poll when they wrote "
                                 "this reply")
            badges.append(vote_pill)
        if reply.status != "open":
            badges.append(pill(STATUS_LABELS.get(reply.status, reply.status) or reply.status,
                               "acPillDanger"))

        author = AuthorLine(reply.author, time_ago(reply.created_at),
                            "edited" if reply.edited_at else "")
        author.profile_requested.connect(self.profile_requested.emit)
        layout.addWidget(author)
        if badges:
            layout.addWidget(flow(badges))
        body = label(reply.body or "[removed]", "exBody")
        body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(body)

        actions = QHBoxLayout()
        actions.setSpacing(2)
        if reply.status == "open":
            up = small_button(f"▲ {reply.score}", "", "exVote")
            up.setCheckable(True)
            up.setChecked(reply.voted)
            up.setEnabled(not reply.is_mine)
            up.setToolTip("You can't upvote your own reply" if reply.is_mine else "Helpful")
            up.clicked.connect(lambda on: self.upvote.emit(reply.id, on))
            actions.addWidget(up)
            if not child and post_open:
                answer = small_button("Reply", "reply")
                answer.clicked.connect(self._toggle_box)
                actions.addWidget(answer)
            if is_post_author and not child:
                best = small_button("Unmark best" if reply.is_best else "Mark best answer",
                                    "badge-check")
                best.clicked.connect(lambda: self.action.emit(
                    "unbest" if reply.is_best else "best", reply.id))
                actions.addWidget(best)
            if can_moderate:
                verify = small_button("Remove verification" if reply.verified else "Verify",
                                      "shield-check")
                verify.clicked.connect(lambda: self.action.emit(
                    "unverify" if reply.verified else "verify", reply.id))
                actions.addWidget(verify)
            if reply.is_mine:
                for name, icon, key in (("Edit", "pencil", "edit"), ("Delete", "trash-2", "delete")):
                    b = small_button(name, icon)
                    b.clicked.connect(lambda _c=False, k=key: self.action.emit(k, reply.id))
                    actions.addWidget(b)
            else:
                report = small_button("Report", "flag")
                report.clicked.connect(lambda: self.action.emit("report", reply.id))
                actions.addWidget(report)
        if can_moderate:
            moderate = small_button("Moderate", "shield-alert")
            moderate.clicked.connect(lambda: self.action.emit("moderate", reply.id))
            actions.addWidget(moderate)
        actions.addStretch(1)
        layout.addLayout(actions)

        self._box: Optional[ReplyBox] = None
        self._vote_label = vote_label
        self._checker = checker
        self._children = QVBoxLayout()
        self._children.setContentsMargins(18, 4, 0, 0)
        self._children.setSpacing(6)
        layout.addLayout(self._children)
        contain(self, limit=200, buttons=False)

    def add_child(self, widget: QWidget) -> None:
        self._children.addWidget(widget)

    def _toggle_box(self) -> None:
        if self._box is None:
            self._box = ReplyBox(f"Reply to {self._reply.author.name}…", self._vote_label,
                                 compact=True, checker=self._checker)
            self._box.submitted.connect(
                lambda body, anon: self.answer_submitted.emit(self._reply.id, body, anon))
            self._children.addWidget(self._box)
            self._box.text.setFocus()
        else:
            self._box.setVisible(not self._box.isVisible())

    @property
    def box(self) -> Optional[ReplyBox]:
        return self._box


def tags_text(tags: list[Tag]) -> str:
    return ", ".join(t.label for t in tags)


def stat_label(text: str) -> QLabel:
    return label(text, "exStat", wrap=False)


def expanding(widget: QWidget) -> QWidget:
    widget.setSizePolicy(QSizePolicy.Policy.Expanding, widget.sizePolicy().verticalPolicy())
    return widget


__all__ = ["AuthorLine", "PostCard", "PollWidget", "ReplyBox", "ReplyWidget", "SearchPicker",
           "VitalsBlock", "clear_layout", "flow", "set_text", "small_button", "tag_chip",
           "refresh_small_icons", "repolish"]
