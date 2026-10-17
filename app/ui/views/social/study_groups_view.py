"""Community > Study Groups: my groups, Browse (public groups), invites,
"Join with a link or code", and for educators and admins a Reported tab
(reported messages and notes only: they can't browse private groups).

Display only: StudyGroupsController does the work. A group itself opens in
a full-page sheet (group_page.py).
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QHBoxLayout, QLineEdit, QPlainTextEdit, QRadioButton, QVBoxLayout,
    QWidget,
)

from app.models.social import GROUP_MEMBER_CAP, GROUP_REPORT_REASONS, GroupInvite, GroupReport, StudyGroup
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import Card, button, field_block, label, pill
from app.ui.views.social.social_widgets import PersonRow, SocialPage, clear_layout, short_when


class GroupRow(PersonRow):
    """A group in a list: name, Public/Private, members, unread count."""

    def __init__(self, group: StudyGroup) -> None:
        from app.models.social import Person
        bits = [f"{group.members}/{GROUP_MEMBER_CAP} members"]
        if group.topic:
            bits.append(group.topic)
        if group.my_role in ("owner", "moderator"):
            bits.append("you are " + group.my_role)
        super().__init__(Person(id=group.id, name=group.name), "  ·  ".join(bits),
                         badge="Private" if group.is_private else "Public", clickable=True)
        self.group = group
        if group.unread:
            self.actions.addWidget(pill(f"{group.unread} new", "acPillGood"))
        if group.muted:
            self.actions.addWidget(pill("Muted", "acPill"))
        if group.description:
            self.setToolTip(group.description)


class StudyGroupsView(SocialPage):
    open_requested = Signal(str)              # group id
    create_requested = Signal()
    join_public_requested = Signal(str)       # group id
    join_token_requested = Signal(str)        # pasted link or code
    invite_answered = Signal(str, bool)       # invite id, accept?
    browse_requested = Signal(str, str, str)  # search, topic, body system
    report_action = Signal(object, str)       # GroupReport, hide | dismiss

    def __init__(self) -> None:
        super().__init__("Study Groups",
                         "Small groups (up to 50) to study together: a chat, a shelf of shared "
                         "notes, and members. Public groups are listed in Browse; private ones "
                         "only take people invited by friends or with an invite link.",
                         "users")
        self._groups: list[StudyGroup] = []
        self._invites: list[GroupInvite] = []
        self._browse: Optional[list[StudyGroup]] = None
        self._reports: Optional[list[GroupReport]] = None
        self._loaded = False
        self._body_systems: list[tuple[str, str]] = []

        new = button("New group", "acPrimary", "plus", self.create_requested.emit)
        self.head_actions.insertWidget(0, new, 0, Qt.AlignmentFlag.AlignTop)

        card = Card("Join with a link or code", "Paste the invite link or the code someone "
                    "sent you (Messenger, email, anywhere).", "share-2")
        row = QHBoxLayout()
        row.setSpacing(8)
        self.join_input = QLineEdit()
        self.join_input.setObjectName("acInput")
        self.join_input.setPlaceholderText("akeso://join/… or the 64-character code")
        self.join_input.returnPressed.connect(self._join_token)
        row.addWidget(self.join_input, 1)
        self.join_button = button("Join", "acPrimary", "", self._join_token)
        row.addWidget(self.join_button)
        card.body.addLayout(row)
        self.top.addWidget(card)

        self.add_tab("mine", "My groups")
        self.add_tab("browse", "Browse public groups")

        # Browse filters (shown on the Browse tab only).
        self._filters = QWidget()
        self._filters.setObjectName("panel")
        frow = QHBoxLayout(self._filters)
        frow.setContentsMargins(0, 0, 0, 0)
        frow.setSpacing(8)
        self.search = QLineEdit()
        self.search.setObjectName("acInput")
        self.search.setPlaceholderText("Search groups")
        self.search.returnPressed.connect(self._browse_now)
        frow.addWidget(self.search, 2)
        self.topic = QLineEdit()
        self.topic.setObjectName("acInput")
        self.topic.setPlaceholderText("Topic, e.g. Cardiology")
        self.topic.returnPressed.connect(self._browse_now)
        frow.addWidget(self.topic, 1)
        self.body_system = QComboBox()
        self.body_system.setObjectName("acInput")
        self.body_system.addItem("Any body system", "")
        self.body_system.currentIndexChanged.connect(lambda _i: self._browse_now())
        frow.addWidget(self.body_system, 1)
        frow.addWidget(button("Search", "acGhost", "search", self._browse_now))

    # ------------------------------------------------------------ setup

    def set_body_systems(self, systems: list[tuple[str, str]]) -> None:
        self._body_systems = systems
        self.body_system.blockSignals(True)
        self.body_system.clear()
        self.body_system.addItem("Any body system", "")
        for key, name in systems:
            self.body_system.addItem(name, key)
        self.body_system.blockSignals(False)

    def set_moderator(self, on: bool) -> None:
        if on and "reported" not in self.tabs:
            self.add_tab("reported", "Reported")

    # ------------------------------------------------------------ input

    def _join_token(self) -> None:
        text = self.join_input.text().strip()
        if text:
            self.join_token_requested.emit(text)

    def joined(self) -> None:
        self.join_input.clear()
        self.set_busy(False)

    def set_busy(self, busy: bool) -> None:
        self.join_button.setEnabled(not busy)
        self.join_input.setEnabled(not busy)

    def _browse_now(self) -> None:
        self.browse_requested.emit(self.search.text().strip(), self.topic.text().strip(),
                                   self.body_system.currentData() or "")

    def select_tab(self, key: str) -> None:
        super().select_tab(key)
        if key == "browse" and self._browse is None:
            self._browse_now()

    # ------------------------------------------------------------- data

    def show_home(self, groups: list[StudyGroup], invites: list[GroupInvite]) -> None:
        self._groups, self._invites = groups, invites
        self._loaded = True
        unread = sum(g.unread for g in groups)
        self.set_tab_text("mine", f"My groups ({len(groups)})" + (f" · {unread} new" if unread else ""))
        self.draw()

    def show_browse(self, groups: list[StudyGroup]) -> None:
        self._browse = groups
        if self.current_tab == "browse":
            self.draw()

    def show_reports(self, reports: list[GroupReport]) -> None:
        self._reports = reports
        self.set_tab_text("reported", f"Reported ({len(reports)})" if reports else "Reported")
        if self.current_tab == "reported":
            self.draw()

    def draw(self) -> None:
        self._filters.setParent(None)
        if not self._loaded:
            return
        clear_layout(self.body)
        if self.current_tab == "browse":
            self._draw_browse()
        elif self.current_tab == "reported":
            self._draw_reports()
        else:
            self._draw_mine()

    def _draw_mine(self) -> None:
        if self._invites:
            self.section(f"Invites ({len(self._invites)})")
            for invite in self._invites:
                row = PersonRow(invite.inviter, f"invited you {short_when(invite.invited_at)}",
                                title=f"{invite.group.name}  ·  "
                                      f"{'Private' if invite.group.is_private else 'Public'}")
                row.add_action("Join", lambda i=invite.invite_id: self.invite_answered.emit(i, True),
                               "acPrimary", "check")
                row.add_action("Decline", lambda i=invite.invite_id: self.invite_answered.emit(i, False),
                               "acGhost")
                self.body.addWidget(row)
            self.section("Your groups")
        if not self._groups:
            panel = self.show_state(
                "You're not in a study group yet",
                "Start one with New group, browse public groups, or paste an invite link above.",
                "users") if not self._invites else None
            if panel is None:
                self.body.addWidget(label("You're not in any group yet.", "acMuted"))
            return
        for group in self._groups:
            row = GroupRow(group)
            row.clicked.connect(lambda gid=group.id: self.open_requested.emit(gid))
            row.add_action("Open", lambda gid=group.id: self.open_requested.emit(gid), "acPrimary")
            self.body.addWidget(row)

    def _draw_browse(self) -> None:
        self.body.addWidget(self._filters)
        self._filters.show()
        if self._browse is None:
            self.body.addWidget(label("Searching…", "acMuted"))
            return
        if not self._browse:
            self.body.addWidget(label("No public groups match. Try other words, or start one "
                                      "with New group.", "acMuted"))
            return
        for group in self._browse:
            row = GroupRow(group)
            row.clicked.connect(lambda gid=group.id: self.open_requested.emit(gid))
            if group.is_member:
                row.add_action("Open", lambda gid=group.id: self.open_requested.emit(gid), "acPrimary")
            elif group.full:
                row.actions.addWidget(pill("Full", "acPillWarn"))
            else:
                row.add_action("Join", lambda gid=group.id: self.join_public_requested.emit(gid),
                               "acPrimary", "plus")
            self.body.addWidget(row)

    def _draw_reports(self) -> None:
        self.body.addWidget(label("Reported messages and shared notes from study groups. You see "
                                  "only what was reported, not the groups' other content.",
                                  "acSmall"))
        if self._reports is None:
            self.body.addWidget(label("Loading reports…", "acMuted"))
            return
        if not self._reports:
            self.body.addWidget(label("No open reports.", "acMuted"))
            return
        reasons = dict(GROUP_REPORT_REASONS)
        for report in self._reports:
            what = "Message" if report.target_kind == "message" else "Shared note"
            row = PersonRow(report.author,
                            f"{what} in “{report.group_name}”  ·  {report.reports} report"
                            f"{'s' if report.reports != 1 else ''}: "
                            + ", ".join(reasons.get(r, r) for r in report.reasons),
                            title=report.excerpt or "(no text)")
            row.add_action("Hide", lambda r=report: self.report_action.emit(r, "hide"), "acDanger")
            row.add_action("Dismiss", lambda r=report: self.report_action.emit(r, "dismiss"), "acGhost")
            self.body.addWidget(row)

    @property
    def groups(self) -> list[StudyGroup]:
        return self._groups


# ======================================================================
#   Dialogs
# ======================================================================

class CreateGroupDialog(AccountDialog):
    submitted = Signal(str, str, str, str, object)   # name, description, visibility, topic, body system

    def __init__(self, body_systems: list[tuple[str, str]], parent: Optional[QWidget] = None) -> None:
        super().__init__("New study group", "You become the owner. You can invite friends, make "
                         "an invite link and choose moderators.", "users", parent, width=520)
        self.name = QLineEdit()
        self.name.setObjectName("acInput")
        self.name.setMaxLength(60)
        self.name.setPlaceholderText("e.g. Cardio Crew 2nd year")
        self.body.addWidget(field_block("Name", self.name))
        self.description = QPlainTextEdit()
        self.description.setObjectName("acInput")
        self.description.setFixedHeight(80)
        self.description.setPlaceholderText("What the group is for (optional)")
        self.body.addWidget(field_block("Description", self.description))

        kind = QVBoxLayout()
        kind.setSpacing(4)
        group = QButtonGroup(self)
        self.public = QRadioButton("Public: listed in Browse; anyone signed in can join")
        self.private = QRadioButton("Private: not listed; people join by a friend invite or an "
                                    "invite link")
        self.public.setChecked(True)
        for radio in (self.public, self.private):
            group.addButton(radio)
            kind.addWidget(radio)
        holder = QWidget()
        holder.setObjectName("panel")
        kind.setContentsMargins(0, 0, 0, 0)
        holder.setLayout(kind)
        self.body.addWidget(field_block("Type", holder))

        row = QHBoxLayout()
        row.setSpacing(8)
        self.topic = QLineEdit()
        self.topic.setObjectName("acInput")
        self.topic.setMaxLength(60)
        self.topic.setPlaceholderText("Topic (optional)")
        row.addWidget(self.topic, 1)
        self.body_system = QComboBox()
        self.body_system.setObjectName("acInput")
        self.body_system.addItem("No body system", None)
        for key, name in body_systems:
            self.body_system.addItem(name, key)
        row.addWidget(self.body_system, 1)
        holder2 = QWidget()
        holder2.setObjectName("panel")
        row.setContentsMargins(0, 0, 0, 0)
        holder2.setLayout(row)
        self.body.addWidget(field_block("Topic and body system", holder2,
                                        "Helps people find a public group in Browse."))
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Create group", "acPrimary", "check", self._submit, default=True)

    def _submit(self) -> None:
        if len(" ".join(self.name.text().split())) < 3:
            self.show_error("Give the group a name of at least 3 characters.")
            return
        self.set_busy(True)
        self.submitted.emit(self.name.text(), self.description.toPlainText(),
                            "private" if self.private.isChecked() else "public",
                            self.topic.text(), self.body_system.currentData())


class GroupReportDialog(AccountDialog):
    submitted = Signal(str, str)              # reason, note

    def __init__(self, what: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(f"Report this {what}", "The group's owner and moderators, and Akeso's "
                         "educators and admins, can see reports. The author isn't told who "
                         "reported.", "flag", parent)
        self._group = QButtonGroup(self)
        for index, (key, text) in enumerate(GROUP_REPORT_REASONS):
            radio = QRadioButton(text)
            radio.setProperty("reason", key)
            radio.setChecked(index == 0)
            self._group.addButton(radio)
            self.body.addWidget(radio)
        self.note = QLineEdit()
        self.note.setObjectName("acInput")
        self.note.setMaxLength(500)
        self.note.setPlaceholderText("Anything moderators should know (optional)")
        self.body.addWidget(self.note)
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Send report", "acDanger", "flag", self._submit)

    def _submit(self) -> None:
        self.set_busy(True)
        self.submitted.emit(self._group.checkedButton().property("reason"), self.note.text())
