"""Community > Friends: your friends, requests (incoming and sent) and the
people you blocked.

Friends are mutual. They are not the same as Follow in Clinical Exchange,
which only tells you when someone posts; the page says so at the top.
Display only: FriendsController does the work.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QHBoxLayout, QLineEdit

from app.models.social import BlockedPerson, Friend, FriendRequests, Person
from app.ui.views.account.account_widgets import Card, button, label, set_text
from app.ui.views.social.social_widgets import (
    PersonRow, SocialPage, clear_layout, short_when,
)


class FriendsView(SocialPage):
    add_requested = Signal(str)               # handle as typed
    respond_requested = Signal(str, bool)     # user id, accept?
    cancel_requested = Signal(int)            # sent request id
    unfriend_requested = Signal(object)       # Person
    block_requested = Signal(object)          # Person
    unblock_requested = Signal(object)        # BlockedPerson
    profile_requested = Signal(str)           # handle

    def __init__(self) -> None:
        super().__init__(
            "Friends",
            "Friends are mutual: you both agree. Friends can share notes with each other and "
            "invite each other to study groups. This is separate from Follow in Clinical "
            "Exchange, which only tells you when someone posts.",
            "user-check")
        self._friends: list[Friend] = []
        self._requests = FriendRequests()
        self._blocked: list[BlockedPerson] = []
        self._loaded = False

        card = Card("Add a friend", "Ask them for their @handle (Account Settings → Profile), "
                    "or use Add friend on their profile.", "plus")
        row = QHBoxLayout()
        row.setSpacing(8)
        self.handle_input = QLineEdit()
        self.handle_input.setObjectName("acInput")
        self.handle_input.setPlaceholderText("@handle, e.g. @maria_santos")
        self.handle_input.setMaxLength(40)
        self.handle_input.returnPressed.connect(self._add)
        row.addWidget(self.handle_input, 1)
        self.add_button = button("Send request", "acPrimary", "plus", self._add)
        row.addWidget(self.add_button)
        card.body.addLayout(row)
        self.handle_error = label("", "acError")
        self.handle_error.hide()
        card.body.addWidget(self.handle_error)
        self.handle_input.textChanged.connect(lambda _t: self.handle_error.hide())
        mine = QHBoxLayout()
        mine.setSpacing(8)
        mine.addWidget(label("Your handle:", "acSmall", wrap=False))
        self.my_handle = label("", "scHandleBox", wrap=False)
        self.my_handle.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        mine.addWidget(self.my_handle)
        self.copy_handle = button("Copy", "acLink", "copy", self._copy_handle)
        mine.addWidget(self.copy_handle)
        mine.addStretch(1)
        card.body.addLayout(mine)
        self.top.addWidget(card)

        self.add_tab("friends", "Friends")
        self.add_tab("requests", "Requests")
        self.add_tab("blocked", "Blocked")

    # ---------------------------------------------------------- input

    def set_my_handle(self, handle: str) -> None:
        self.my_handle.setText(f"@{handle}" if handle else "Being assigned…")
        self.copy_handle.setEnabled(bool(handle))

    def _copy_handle(self) -> None:
        text = self.my_handle.text()
        if text.startswith("@"):
            QGuiApplication.clipboard().setText(text)
            set_text(self.copy_handle, "Copied")

    def _add(self) -> None:
        text = self.handle_input.text().strip()
        if text:
            self.add_requested.emit(text)

    def set_busy(self, busy: bool) -> None:
        self.add_button.setEnabled(not busy)
        self.handle_input.setEnabled(not busy)

    def show_handle_error(self, message: str) -> None:
        """Under the handle box, where the mistake is, instead of a banner."""
        self.set_busy(False)
        self.handle_error.setText(message)
        self.handle_error.show()
        self.handle_input.setFocus()
        self.handle_input.selectAll()

    def request_sent(self) -> None:
        self.handle_input.clear()
        self.set_busy(False)

    # ---------------------------------------------------------- data

    def show_data(self, friends: list[Friend], requests: FriendRequests,
                  blocked: list[BlockedPerson]) -> None:
        self._friends, self._requests, self._blocked = friends, requests, blocked
        self._loaded = True
        self.set_tab_text("friends", f"Friends ({len(friends)})")
        waiting = len(requests.incoming)
        self.set_tab_text("requests", f"Requests ({waiting})" if waiting else "Requests")
        self.set_tab_text("blocked", f"Blocked ({len(blocked)})" if blocked else "Blocked")
        self.draw()

    def draw(self) -> None:
        if not self._loaded:
            return
        clear_layout(self.body)
        if self.current_tab == "requests":
            self._draw_requests()
        elif self.current_tab == "blocked":
            self._draw_blocked()
        else:
            self._draw_friends()

    def _row(self, person: Person, subtitle: str = "") -> PersonRow:
        row = PersonRow(person, subtitle)
        row.profile_requested.connect(self.profile_requested.emit)
        self.body.addWidget(row)
        return row

    def _draw_friends(self) -> None:
        if not self._friends:
            self.show_state("No friends yet",
                            "Send a request with someone's @handle above. When they accept, you "
                            "can share notes and invite each other to study groups.", "user-check")
            return
        for friend in self._friends:
            row = self._row(friend.person, f"friends since {short_when(friend.since)}"
                            if friend.since else "")
            if friend.person.handle:
                row.add_action("Profile", lambda h=friend.person.handle: self.profile_requested.emit(h),
                               "acLink")
            row.add_action("Unfriend", lambda p=friend.person: self.unfriend_requested.emit(p),
                           "acGhost", tip="They are not told. Shares between you end.")
            row.add_action("Block", lambda p=friend.person: self.block_requested.emit(p), "acGhost")

    def _draw_requests(self) -> None:
        incoming, sent = self._requests.incoming, self._requests.sent
        self.section(f"Waiting for you ({len(incoming)})")
        if not incoming:
            self.body.addWidget(label("No requests waiting.", "acMuted"))
        for request in incoming:
            row = self._row(request.person, f"asked {short_when(request.requested_at)}")
            row.add_action("Accept", lambda uid=request.person.id: self.respond_requested.emit(uid, True),
                           "acPrimary", "check")
            row.add_action("Decline", lambda uid=request.person.id: self.respond_requested.emit(uid, False),
                           "acGhost", tip="They are not told.")
            row.add_action("Block", lambda p=request.person: self.block_requested.emit(p), "acGhost")
        self.section(f"Sent ({len(sent)})")
        self.body.addWidget(label("A request stays here until they accept it or you cancel it.", "acSmall"))
        if not sent:
            self.body.addWidget(label("No requests sent.", "acMuted"))
        for request in sent:
            row = PersonRow(Person(id="", name=f"@{request.handle}"),
                            f"sent {short_when(request.requested_at)}")
            row.add_action("Cancel", lambda rid=request.request_id: self.cancel_requested.emit(rid),
                           "acGhost")
            self.body.addWidget(row)

    def _draw_blocked(self) -> None:
        self.body.addWidget(label("People you blocked can't send you requests, shares or group "
                                  "invites, and you no longer show up when they look for friends. "
                                  "Unblocking does not make you friends again.", "acSmall"))
        if not self._blocked:
            self.body.addWidget(label("You haven't blocked anyone.", "acMuted"))
        for person in self._blocked:
            row = PersonRow(Person(id=person.id, name=person.name),
                            f"blocked {short_when(person.blocked_at)}")
            row.add_action("Unblock", lambda p=person: self.unblock_requested.emit(p), "acGhost")
            self.body.addWidget(row)

    @property
    def friends(self) -> list[Friend]:
        return self._friends

