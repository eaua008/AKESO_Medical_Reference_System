"""A Clinical Exchange member's profile, opened on top of the current page.

Display only: ExchangeController loads the profile (ex_profile) and handles
Follow, Report, Moderate and clicks on posts or topics. Anonymous posts and
replies never reach this page (the database leaves them out), so a profile
can't reveal who wrote them.
"""

from datetime import datetime
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QButtonGroup, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from app.models.account import PROGRAM_LABELS, ROLE_LABELS, YEAR_LABELS
from app.models.exchange import VISIBILITY_LABELS, MemberProfile, ProfileActivity, time_ago
from app.ui.components.fluid import ResponsiveGrid, contain
from app.ui.views.account.account_widgets import (
    Banner, Card, button, icon_label, label, pill, refresh_icons, repolish,
)
from app.ui.views.exchange.exchange_widgets import clear_layout, flow, tag_chip

BADGE_ICONS = {"first_case": "file-text", "best_answer": "badge-check", "verified_1": "shield-check",
               "verified_10": "shield-check", "helpful_10": "thumbs-up", "helpful_25": "thumbs-up",
               "sharp": "target", "goto": "graduation-cap"}


def _count(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def _month(value: Optional[datetime]) -> str:
    return value.strftime("%b %Y") if value else ""


class _StatTile(QFrame):
    def __init__(self, number: str, caption: str, icon: str) -> None:
        super().__init__()
        self.setObjectName("acCard")
        column = QVBoxLayout(self)
        column.setContentsMargins(14, 12, 14, 12)
        column.setSpacing(2)
        top = QHBoxLayout()
        top.setSpacing(8)
        top.addWidget(icon_label(icon, 16))
        top.addStretch(1)
        column.addLayout(top)
        column.addWidget(label(number, "acStatNumber", wrap=False))
        column.addWidget(label(caption, "acStatLabel"))


class _ActivityRow(QFrame):
    clicked = Signal(str)                    # post id

    def __init__(self, item: ProfileActivity) -> None:
        super().__init__()
        self.setObjectName("acRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._post = item.post_id
        column = QVBoxLayout(self)
        column.setContentsMargins(12, 9, 12, 9)
        column.setSpacing(3)
        top = QHBoxLayout()
        top.setSpacing(6)
        if item.kind == "reply":
            top.addWidget(label(f"Reply on “{item.title}”", "acRowTitle"), 1)
        else:
            top.addWidget(pill("Case" if item.kind == "case" else "Question", "acPill"))
            top.addWidget(label(item.title, "acRowTitle"), 1)
        column.addLayout(top)
        if item.excerpt:
            column.addWidget(label(item.excerpt, "acMuted"))
        bits = [time_ago(item.created_at), f"▲ {item.score}"]
        if item.kind != "reply":
            bits.append(f"{item.reply_count} repl{'y' if item.reply_count == 1 else 'ies'}")
        foot = QHBoxLayout()
        foot.setSpacing(6)
        foot.addWidget(label(" · ".join(b for b in bits if b), "acSmall", wrap=False))
        if item.is_best:
            foot.addWidget(pill("★ Best answer", "acPillGood"))
        if item.verified:
            foot.addWidget(pill("✓ Educator verified", "acPillGood"))
        foot.addStretch(1)
        column.addLayout(foot)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if (event.button() == Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit(self._post)
        super().mouseReleaseEvent(event)


class ProfileView(QWidget):
    follow_toggled = Signal(str, bool)       # handle, follow?
    report_requested = Signal(object)        # MemberProfile
    moderate_requested = Signal(object)      # MemberProfile
    post_requested = Signal(str)             # post id
    topic_requested = Signal(object)         # Tag
    edit_requested = Signal()                # "Edit my profile" (own profile)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.profile: Optional[MemberProfile] = None
        self._tab = "posts"
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        outer.addWidget(self.scroll)
        page = QWidget()
        page.setObjectName("panel")
        centre = QHBoxLayout(page)
        centre.setContentsMargins(30, 22, 30, 30)
        self._body = QWidget()
        self._body.setObjectName("panel")
        self._body.setMaximumWidth(920)
        self._column = QVBoxLayout(self._body)
        self._column.setContentsMargins(0, 0, 0, 0)
        self._column.setSpacing(14)
        centre.addStretch(1)
        centre.addWidget(self._body, 100)
        centre.addStretch(1)
        self.scroll.setWidget(page)
        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        self._picture: Optional[QLabel] = None
        self.follow_button: Optional[QPushButton] = None

    # ---------------------------------------------------------------- api

    def show_loading(self) -> None:
        self._reset()
        self._column.addWidget(label("Loading profile…", "acMuted"))

    def show_error(self, message: str) -> None:
        self._reset()
        box = Card("Profile unavailable", "", "lock")
        box.body.addWidget(label(message, "acMuted"))
        self._column.addWidget(box)
        self._column.addStretch(1)

    def set_avatar(self, pixmap: QPixmap) -> None:
        if self._picture is not None:
            self._picture.setPixmap(pixmap)

    def set_following(self, on: bool, followers: int) -> None:
        if self.profile is not None:
            self.profile.following, self.profile.followers = on, followers
            self.show_profile(self.profile, keep_scroll=True)

    def show_profile(self, profile: MemberProfile, avatar: Optional[QPixmap] = None,
                     keep_scroll: bool = False) -> None:
        position = self.scroll.verticalScrollBar().value() if keep_scroll else 0
        old_picture = self._picture.pixmap() if (keep_scroll and self._picture) else None
        self.profile = profile
        self._reset()
        self._column.addWidget(self.banner)
        if profile.is_me:
            self.banner.show_message(
                f"This is how others see your profile. Visibility: "
                f"{VISIBILITY_LABELS.get(profile.visibility, profile.visibility)}. "
                "Change it in Account Settings → Profile.", "info", "Got it")
        else:
            self.banner.hide()
        self._column.addWidget(self._header(profile, avatar or old_picture))
        shows = profile.shows
        if profile.stats is not None:
            self._column.addWidget(self._stats(profile))
            if profile.badges:
                self._column.addWidget(self._badges(profile))
        elif not shows.get("stats", True):
            self._column.addWidget(self._private_note("Contribution stats are kept private."))
        if shows.get("activity", True) and (profile.topics or profile.posts or profile.replies
                                            or profile.is_me):
            if profile.topics:
                self._column.addWidget(self._topics(profile))
            self._column.addWidget(self._activity(profile))
        elif not shows.get("activity", True):
            self._column.addWidget(self._private_note("Posts and replies are kept private."))
        elif not profile.posts and not profile.replies:
            self._column.addWidget(self._private_note(
                f"{profile.display_name} hasn't posted publicly yet."))
        self._column.addStretch(1)
        contain(self._body)
        self.scroll.verticalScrollBar().setValue(position)

    # ------------------------------------------------------------ sections

    def _reset(self) -> None:
        self._column.removeWidget(self.banner)
        clear_layout(self._column)
        self._picture = None
        self.follow_button = None

    def _header(self, p: MemberProfile, avatar: Optional[QPixmap]) -> Card:
        card = Card()
        row = QHBoxLayout()
        row.setSpacing(18)
        self._picture = QLabel()
        self._picture.setObjectName("panel")
        self._picture.setFixedSize(88, 88)
        if avatar is not None:
            self._picture.setPixmap(avatar)
        row.addWidget(self._picture, 0, Qt.AlignmentFlag.AlignTop)

        text = QVBoxLayout()
        text.setSpacing(5)
        text.addWidget(label(p.display_name, "acTitle"))
        chips = [label(f"@{p.handle}", "acMuted", wrap=False)]
        if p.role:
            chips.append(pill(ROLE_LABELS.get(p.role, p.role.capitalize()),
                              "acPillGood" if p.role in ("educator", "admin") else "acPill"))
        if p.verified_domain:
            chips.append(pill(f"✓ Verified student · {p.verified_domain}", "acPillGood"))
        text.addWidget(flow(chips))
        study = [PROGRAM_LABELS.get(p.program or "", ""), YEAR_LABELS.get(p.year_level or 0, ""),
                 p.school or ""]
        if any(study):
            text.addWidget(label(" · ".join(s for s in study if s), "acValue"))
        meta = [f"Joined {_month(p.member_since)}" if p.member_since else ""]
        if p.last_active:
            meta.append(f"Active {time_ago(p.last_active)}")
        meta.append(f"{p.followers} follower{'s' if p.followers != 1 else ''}")
        text.addWidget(label(" · ".join(m for m in meta if m), "acSmall"))
        row.addLayout(text, 1)

        actions = QVBoxLayout()
        actions.setSpacing(6)
        if p.is_me:
            actions.addWidget(button("Edit my profile", "acGhost", "pencil",
                                     self.edit_requested.emit))
        else:
            self.follow_button = button("Following" if p.following else "Follow",
                                        "acGhost" if p.following else "acPrimary",
                                        "user-check" if p.following else "plus",
                                        lambda: self.follow_toggled.emit(p.handle, not p.following))
            self.follow_button.setToolTip("You'll be notified when they post a new case or "
                                          "question" if not p.following else "Stop following")
            actions.addWidget(self.follow_button)
            actions.addWidget(button("Report", "acLink", "flag",
                                     lambda: self.report_requested.emit(p)))
        if p.can_moderate and not p.is_me:
            actions.addWidget(button("Moderate", "acLink", "shield-alert",
                                     lambda: self.moderate_requested.emit(p)))
        actions.addStretch(1)
        row.addLayout(actions)
        card.body.addLayout(row)

        if p.bio:
            card.body.addWidget(label(p.bio, "exBody"))
        if p.interests:
            card.body.addWidget(label("INTERESTS", "acFieldLabel", wrap=False))
            card.body.addWidget(flow([pill(i, "acPill") for i in p.interests]))
        return card

    def _stats(self, p: MemberProfile) -> QWidget:
        s = p.stats or {}
        accuracy = p.poll_accuracy
        tiles = [
            (str(s.get("posts", 0)), "Posts · " + _count(s.get("cases", 0), "case") + ", "
                                     + _count(s.get("questions", 0), "question"), "file-text"),
            (str(s.get("replies", 0)), "Replies", "message-circle"),
            (str(s.get("best_answers", 0)), "Best answers", "badge-check"),
            (str(s.get("verified_answers", 0)), "Educator-verified replies", "shield-check"),
            (str(s.get("helpful_votes", 0)), "Helpful votes received", "thumbs-up"),
            (f"{round(100 * accuracy[0] / accuracy[1])}%" if accuracy else "–",
             f"Poll accuracy · {accuracy[0]} of {accuracy[1]} revealed" if accuracy
             else "Poll accuracy · no revealed polls yet", "target"),
        ]
        grid = ResponsiveGrid(170, max_columns=3, spacing=10, steps=(3, 2))
        grid.set_cards([_StatTile(n, c, i) for n, c, i in tiles])
        grid.watch(self.scroll.viewport())
        return grid

    def _badges(self, p: MemberProfile) -> Card:
        card = Card("Badges", "Earned from their contributions.", "sparkles")
        chips = []
        for badge in p.badges:
            chip = button(badge.get("label", ""), "acChip", BADGE_ICONS.get(badge.get("key"), "sparkles"))
            chip.setToolTip(badge.get("detail", ""))
            chips.append(chip)
        card.body.addWidget(flow(chips))
        return card

    def _topics(self, p: MemberProfile) -> Card:
        card = Card("Active in", "Topics of the cases they post and discuss most.", "tag")
        chips = []
        for tag in p.topics:
            chip = tag_chip(tag)
            chip.clicked.connect(lambda _c=False, t=tag: self.topic_requested.emit(t))
            chips.append(chip)
        card.body.addWidget(flow(chips))
        return card

    def _activity(self, p: MemberProfile) -> Card:
        card = Card("Recent activity", "Public posts and replies only; anonymous ones are "
                    "never shown here.", "history")
        tabs = QHBoxLayout()
        tabs.setSpacing(6)
        group = QButtonGroup(card)
        group.setExclusive(True)
        for key, text in (("posts", f"Posts ({len(p.posts)})"),
                          ("replies", f"Replies ({len(p.replies)})")):
            chip = QPushButton(text)
            chip.setObjectName("acChip")
            chip.setCheckable(True)
            chip.setChecked(key == self._tab)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.clicked.connect(lambda _c=False, k=key: self._switch_tab(k))
            group.addButton(chip)
            tabs.addWidget(chip)
        tabs.addStretch(1)
        card.body.addLayout(tabs)
        items = p.posts if self._tab == "posts" else p.replies
        for item in items:
            row = _ActivityRow(item)
            row.clicked.connect(self.post_requested.emit)
            card.body.addWidget(row)
        if not items:
            card.body.addWidget(label("Nothing here yet.", "acMuted"))
        return card

    def _switch_tab(self, key: str) -> None:
        self._tab = key
        if self.profile is not None:
            self.show_profile(self.profile, keep_scroll=True)

    def _private_note(self, text: str) -> Card:
        card = Card()
        line = QHBoxLayout()
        line.setSpacing(10)
        line.addWidget(icon_label("lock", 16))
        line.addWidget(label(text, "acMuted"), 1)
        card.body.addLayout(line)
        return card

    def refresh_theme(self) -> None:
        refresh_icons(self)
        repolish(self)
