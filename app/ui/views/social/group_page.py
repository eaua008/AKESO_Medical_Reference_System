"""One study group, in a full-page sheet: Chat, Shared notes, Members.

Chat shows names with a role badge only (no anonymous posts). New
messages arrive by polling (StudyGroupsController); this view just adds
them. Owners and moderators also get the invite controls and member
management on the Members tab.
"""

from typing import Optional

import shiboken6
import re

from PySide6.QtCore import QEvent, QObject, QPoint, Qt, QTimer, Signal
from PySide6.QtGui import QGuiApplication, QKeySequence, QShortcut
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QButtonGroup, QCheckBox, QComboBox, QFrame, QHBoxLayout, QLabel, QMenu, QPushButton,
    QScrollArea, QVBoxLayout, QWidget,
)

from app.models.social import (
    GROUP_MEMBER_CAP, MESSAGE_MAX, Friend, GroupMessage, GroupNote, Person, StudyGroup,
)
from app.services.study_group_service import check_message
from app.ui.components.akeso_loader import LoadingLabel
from app.ui.components.avatar_cache import AvatarCache
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import (
    Banner, button, icon_label, label, pill, refresh_icons, repolish, set_text,
)
from app.ui.views.exchange.exchange_widgets import GrowingTextEdit
from app.ui.views.social.social_widgets import PersonRow, StatePanel, clear_layout, short_when

EXPIRY_CHOICES = [("No expiry", None), ("24 hours", 24), ("7 days", 24 * 7), ("30 days", 24 * 30)]


MENTION = re.compile(r"(?:^|\s)@([A-Za-z0-9_]{0,20})$")      # an @ being typed, just before the cursor
MENTION_ROWS = 6


class MentionPopup(QFrame):
    """Suggests members while you type @ in the chat box. Up / Down move,
    Enter or Tab picks, Esc closes, a click picks. It never takes the keyboard
    focus: the chat box keeps it (the key presses are passed on by the page)."""

    picked = Signal(str)                          # handle

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("scMention")
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        col = QVBoxLayout(self)
        col.setContentsMargins(4, 4, 4, 4)
        col.setSpacing(2)
        self._rows: list[QPushButton] = []
        self._handles: list[str] = []
        self._current = 0
        self.hide()

    def show_matches(self, people: list[Person], empty_text: str = "") -> None:
        """The suggestions; with none, empty_text (if given) tells why."""
        for row in self._rows:
            row.hide()
            row.deleteLater()
        self._rows, self._handles, self._current = [], [], 0
        layout = self.layout()
        if not people and empty_text:
            note = QPushButton(empty_text)
            note.setObjectName("scMentionRow")
            note.setEnabled(False)
            note.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            layout.addWidget(note)
            self._rows.append(note)
        for person in people[:MENTION_ROWS]:
            handle = person.mention or person.handle
            badge = f"   ·   {person.badge}" if person.badge else ""
            row = QPushButton(f"{person.name}     @{handle}{badge}")
            row.setObjectName("scMentionRow")
            row.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            row.setCursor(Qt.CursorShape.PointingHandCursor)
            row.clicked.connect(lambda _c=False, h=handle: self.picked.emit(h))
            layout.addWidget(row)
            self._rows.append(row)
            self._handles.append(handle)
        self._paint()
        layout.invalidate()                         # so sizeHint() counts the new rows
        layout.activate()
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)             # let it size to its rows again
        self.setVisible(bool(self._rows))

    def height_for_rows(self) -> int:
        """Rows plus the frame's padding (counted by hand: asking the layout
        right after the rows were added gave a stale, tiny answer)."""
        rows = [r.sizeHint().height() for r in self._rows]
        return 8 + sum(rows) + 2 * max(0, len(rows) - 1)

    def _paint(self) -> None:
        for i, row in enumerate(self._rows):
            row.setProperty("current", i == self._current)
            row.style().unpolish(row)
            row.style().polish(row)

    def move_by(self, step: int) -> None:
        if self._rows:
            self._current = (self._current + step) % len(self._rows)
            self._paint()

    def pick_current(self) -> None:
        if self._handles:
            self.picked.emit(self._handles[self._current])


class _PictureLabel(QLabel):
    clicked = Signal()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class MessageBubble(QFrame):
    """One chat message. Right-click: Report, or Hide / Unhide for staff."""

    menu_requested = Signal(object, QPoint)       # GroupMessage, where
    picture_clicked = Signal(str)                 # storage path
    THUMB = (380, 260)

    def __init__(self, message: GroupMessage) -> None:
        super().__init__()
        self.message = message
        hidden_from_me = message.hidden and not message.body
        self.setObjectName("scBubbleHidden" if message.hidden else
                           "scBubbleMine" if message.is_mine else "scBubble")
        col = QVBoxLayout(self)
        col.setContentsMargins(12, 8, 12, 9)
        col.setSpacing(3)
        top = QHBoxLayout()
        top.setSpacing(6)
        avatar = QLabel()
        avatar.setObjectName("panel")
        AvatarCache.apply(avatar, message.author.avatar_path, message.author.name, 20)
        top.addWidget(avatar)
        top.addWidget(label(message.author.name, "scBubbleName", wrap=False))
        if message.author.badge:
            top.addWidget(pill(message.author.badge, "acPillGood"))
        top.addStretch(1)
        top.addWidget(label(short_when(message.created_at), "scBubbleTime", wrap=False))
        col.addLayout(top)
        if hidden_from_me:
            text = label("This message was hidden by a moderator.", "acSmall")
        else:
            text = label(message.body, "scBubbleText")
            text.setTextFormat(Qt.TextFormat.PlainText)
            text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.picture: Optional[_PictureLabel] = None
        if message.attachment and not hidden_from_me:
            self.picture = _PictureLabel("Loading picture…")
            self.picture.setObjectName("scPicture")
            self.picture.setMinimumSize(160, 90)
            self.picture.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.picture.setCursor(Qt.CursorShape.PointingHandCursor)
            self.picture.setToolTip("Click to see it full size")
            self.picture.clicked.connect(lambda p=message.attachment: self.picture_clicked.emit(p))
            col.addWidget(self.picture, 0, Qt.AlignmentFlag.AlignLeft)
        if message.body or not message.attachment:
            col.addWidget(text)
        if message.hidden and message.body:
            col.addWidget(label("Hidden from members by a moderator.", "acSmall"))

    def set_picture(self, pixmap: Optional[QPixmap]) -> None:
        if self.picture is None:
            return
        if pixmap is None or pixmap.isNull():
            self.picture.setText("Picture unavailable")
            self.picture.setCursor(Qt.CursorShape.ArrowCursor)
            return
        self.picture.setPixmap(pixmap.scaled(*self.THUMB, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation))
        self.picture.setMinimumSize(0, 0)

    def contextMenuEvent(self, event) -> None:  # noqa: N802
        self.menu_requested.emit(self.message, event.globalPos())


class GroupPage(QWidget):
    close_requested = Signal()
    send_requested = Signal(str)
    attach_requested = Signal()                   # the picture button (migration 045)
    image_requested = Signal(str)                 # a bubble needs this picture downloaded
    image_opened = Signal(str)                    # a picture was clicked: show it full size
    message_menu = Signal(object, QPoint)         # GroupMessage, where (the controller builds it)
    share_note_requested = Signal()
    note_action = Signal(str, object)             # open | save | remove | report | hide | unhide, GroupNote
    invite_friends_requested = Signal()
    link_create_requested = Signal(object)        # expiry hours or None
    link_copy_requested = Signal()
    link_revoke_requested = Signal()
    member_action = Signal(str, object)           # moderator | member | owner | remove, Person
    leave_requested = Signal()
    delete_requested = Signal()
    mute_toggled = Signal(bool)
    join_requested = Signal()
    profile_requested = Signal(str)
    tab_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.group: Optional[StudyGroup] = None
        self._last_id = 0
        self._seen_ids: set[int] = set()
        self._token: Optional[str] = None          # a link made in this session (copyable)
        self.tab = "chat"

        outer = QVBoxLayout(self)
        # Extra left margin: the sheet's close tab sits over the top-left corner.
        outer.setContentsMargins(56, 18, 34, 14)
        outer.setSpacing(10)

        head = QHBoxLayout()
        head.setSpacing(10)
        head.addWidget(icon_label("users", 24), 0, Qt.AlignmentFlag.AlignTop)
        titles = QVBoxLayout()
        titles.setSpacing(4)
        self.title = label("", "acTitle")
        titles.addWidget(self.title)
        self.meta = QHBoxLayout()
        self.meta.setSpacing(6)
        titles.addLayout(self.meta)
        self.description = label("", "acMuted")
        titles.addWidget(self.description)
        head.addLayout(titles, 1)
        self.mute = button("Mute mentions", "acGhost", "bell", self._toggle_mute)
        self.mute.setCheckable(True)
        head.addWidget(self.mute, 0, Qt.AlignmentFlag.AlignTop)
        self.more = button("", "acGhost", "ellipsis", self._more_menu)
        self.more.setToolTip("Leave or delete the group")
        head.addWidget(self.more, 0, Qt.AlignmentFlag.AlignTop)
        outer.addLayout(head)

        self.banner = Banner()
        self.banner.action.connect(self.banner.hide)
        outer.addWidget(self.banner)

        tab_row = QWidget()
        tab_row.setObjectName("acTabRow")
        tabs = QHBoxLayout(tab_row)
        tabs.setContentsMargins(0, 0, 0, 0)
        tabs.setSpacing(0)
        self._tab_group = QButtonGroup(self)
        self._tab_group.setExclusive(True)
        self.tabs: dict[str, QPushButton] = {}
        for key, text in (("chat", "Chat"), ("notes", "Shared notes"), ("members", "Members")):
            tab = QPushButton(text)
            tab.setObjectName("acTab")
            tab.setCheckable(True)
            tab.setChecked(key == "chat")
            tab.setCursor(Qt.CursorShape.PointingHandCursor)
            tab.clicked.connect(lambda _c=False, k=key: self.select_tab(k))
            self._tab_group.addButton(tab)
            tabs.addWidget(tab)
            self.tabs[key] = tab
        tabs.addStretch(1)
        self._tab_row = tab_row
        outer.addWidget(tab_row)

        # ---- chat
        self.chat = QWidget()
        self.chat.setObjectName("panel")
        chat_col = QVBoxLayout(self.chat)
        chat_col.setContentsMargins(0, 0, 0, 0)
        chat_col.setSpacing(8)
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setObjectName("scChat")
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        host = QWidget()
        host.setObjectName("panel")
        self.messages = QVBoxLayout(host)
        self.messages.setContentsMargins(12, 12, 12, 12)
        self.messages.setSpacing(8)
        self.messages.addStretch(1)
        self.chat_scroll.setWidget(host)
        chat_col.addWidget(self.chat_scroll, 1)
        # "N new messages": shown when messages arrive while you are reading
        # further up; one click goes to the bottom.
        self.jump = button("New messages", "acPrimary", "chevron-down", self._jump_down)
        self.jump.hide()
        chat_col.addWidget(self.jump, 0, Qt.AlignmentFlag.AlignHCenter)
        self._pending_new = 0
        self._bubbles: dict[str, list[MessageBubble]] = {}     # picture path -> bubbles showing it
        self._pixmaps: dict[str, Optional[QPixmap]] = {}       # downloaded pictures
        self._asked: set[str] = set()
        self._divider: Optional[QWidget] = None
        self._divider_done = False
        self.chat_scroll.verticalScrollBar().valueChanged.connect(self._scrolled)
        self.empty_chat = label("No messages yet. Say hello!", "acMuted")
        self.messages.insertWidget(0, self.empty_chat)

        composer = QFrame()
        composer.setObjectName("scComposer")
        ccol = QVBoxLayout(composer)
        ccol.setContentsMargins(0, 8, 0, 0)
        ccol.setSpacing(4)
        crow = QHBoxLayout()
        crow.setSpacing(8)
        self.input = GrowingTextEdit(44, 160)
        self.input.setObjectName("acInput")
        self.input.setPlaceholderText("Message the group (Ctrl+Enter sends). @handle mentions a "
                                      "member. Keep cases hypothetical.")
        self.input.textChanged.connect(self._check_input)
        # Suggest who to mention while you type @ ...
        self.mentions = MentionPopup(self)
        self.mentions.picked.connect(self._insert_mention)
        self.input.textChanged.connect(self._suggest_mentions)
        self.input.cursorPositionChanged.connect(self._suggest_mentions)
        self.input.installEventFilter(self)
        for keys in ("Ctrl+Return", "Ctrl+Enter"):             # send without the mouse
            QShortcut(QKeySequence(keys), self.input, activated=self._send)
        crow.addWidget(self.input, 1)
        self.attach = button("", "acGhost", "image", self.attach_requested.emit)
        self.attach.setText("")
        self.attach.setToolTip("Send a picture (PNG or JPEG, up to 5 MB)")
        crow.addWidget(self.attach, 0, Qt.AlignmentFlag.AlignBottom)
        self.send = button("Send", "acPrimary", "message-circle", self._send)
        self.send.setEnabled(False)
        crow.addWidget(self.send, 0, Qt.AlignmentFlag.AlignBottom)
        ccol.addLayout(crow)
        foot = QHBoxLayout()
        self.input_warning = label("", "acError")
        foot.addWidget(self.input_warning, 1)
        self.count = label("", "acSmall", wrap=False)
        foot.addWidget(self.count)
        ccol.addLayout(foot)
        chat_col.addWidget(composer)
        outer.addWidget(self.chat, 1)

        # ---- notes and members (scrolling lists)
        self.lists = QScrollArea()
        self.lists.setWidgetResizable(True)
        self.lists.setFrameShape(QFrame.Shape.NoFrame)
        self.lists.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        list_host = QWidget()
        list_host.setObjectName("panel")
        self.list_col = QVBoxLayout(list_host)
        self.list_col.setContentsMargins(0, 0, 6, 10)
        self.list_col.setSpacing(8)
        self.lists.setWidget(list_host)
        outer.addWidget(self.lists, 1)
        self.lists.hide()

        # ---- outsiders (a public group you haven't joined)
        self.outside = StatePanel("You're not in this group",
                                  "Join to read the chat and the shared notes.", "users", "Join group")
        self.outside.action_clicked.connect(self.join_requested.emit)
        outer.addWidget(self.outside)
        self.outside.hide()

        self.loading = LoadingLabel("", "acMuted")
        outer.addWidget(self.loading)
        self.loading.hide()
        self._notes: list[GroupNote] = []

    # ================================================================ header

    def show_loading(self) -> None:
        self.group = None
        self.title.setText("")
        self.description.setText("")
        clear_layout(self.meta)
        self.chat.hide()
        self.lists.hide()
        self.outside.hide()
        self._tab_row.hide()
        self.loading.set_loading("Opening the group…")
        self.loading.show()

    def show_error(self, message: str) -> None:
        self.loading.hide()
        self.title.setText("Not available")
        self.description.setText(message)

    def show_group(self, group: StudyGroup) -> None:
        first = self.group is None or self.group.id != group.id
        self.group = group
        self.loading.hide()
        self.title.setText(group.name)
        self.description.setText(group.description)
        self.description.setVisible(bool(group.description))
        clear_layout(self.meta)
        self.meta.addWidget(pill("Private" if group.is_private else "Public", "acPill"))
        self.meta.addWidget(pill(f"{group.members}/{GROUP_MEMBER_CAP} members", "acPill"))
        if group.my_role:
            self.meta.addWidget(pill(group.my_role.capitalize(), "acPillGood"))
        if group.topic:
            self.meta.addWidget(label(group.topic, "acSmall", wrap=False))
        self.meta.addStretch(1)
        self.mute.setVisible(group.is_member)
        self.more.setVisible(group.is_member)
        self.mute.blockSignals(True)
        self.mute.setChecked(group.muted)
        self.mute.blockSignals(False)
        set_text(self.mute, "Mentions muted" if group.muted else "Mute mentions")
        if first:
            self._token = None
            self.reset_chat()
        if not group.is_member:
            self._tab_row.hide()
            self.chat.hide()
            self.lists.hide()
            self.outside.show()
            return
        self.outside.hide()
        self._tab_row.show()
        self.select_tab(self.tab if not first else "chat", emit=first)

    def _toggle_mute(self) -> None:
        self.mute_toggled.emit(self.mute.isChecked())

    def _more_menu(self) -> None:
        if self.group is None:
            return
        menu = QMenu(self)
        menu.setObjectName("exMenu")
        menu.addAction("Leave group…", self.leave_requested.emit)
        if self.group.my_role == "owner":
            menu.addSeparator()
            menu.addAction("Delete group…", self.delete_requested.emit)
        menu.exec(self.more.mapToGlobal(QPoint(0, self.more.height() + 4)))

    def select_tab(self, key: str, emit: bool = True) -> None:
        self.tab = key
        self.tabs[key].setChecked(True)
        self.chat.setVisible(key == "chat")
        self.lists.setVisible(key != "chat")
        if key == "members":
            self._draw_members()
        elif key == "notes":
            self._draw_notes()
        if emit:
            self.tab_changed.emit(key)

    # ================================================================== chat

    def reset_chat(self) -> None:
        while self.messages.count() > 1:
            item = self.messages.takeAt(0)
            if item.widget() is not None and item.widget() is not self.empty_chat:
                item.widget().hide()
                item.widget().deleteLater()
        self.messages.insertWidget(0, self.empty_chat)
        self.empty_chat.show()
        self._last_id = 0
        self._seen_ids = set()
        self._divider, self._divider_done = None, False
        self._pending_new = 0
        self._bubbles = {}
        self.jump.hide()

    @property
    def last_id(self) -> Optional[int]:
        return self._last_id or None

    def _at_bottom(self) -> bool:
        bar = self.chat_scroll.verticalScrollBar()
        return bar.value() >= bar.maximum() - 40

    def set_picture(self, path: str, data: Optional[bytes]) -> None:
        """A picture finished downloading (None: it couldn't be fetched)."""
        pixmap = None
        if data:
            pixmap = QPixmap()
            if not pixmap.loadFromData(data):
                pixmap = None
        self._pixmaps[path] = pixmap
        for bubble in self._bubbles.get(path, []):
            if shiboken6.isValid(bubble):
                bubble.set_picture(pixmap)

    def pixmap_for(self, path: str) -> Optional[QPixmap]:
        return self._pixmaps.get(path)

    def set_busy(self, busy: bool) -> None:
        """While a picture uploads: no second send."""
        self.attach.setEnabled(not busy)
        if busy:
            self.send.setEnabled(False)
        else:
            self._check_input()

    def _make_divider(self, count: int) -> QWidget:
        """A line with "N new messages" in it, drawn where the unread start."""
        holder = QWidget()
        holder.setObjectName("panel")
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 6, 0, 2)
        row.setSpacing(10)
        for part in (0, 1, 2):
            if part == 1:
                row.addWidget(label(f"{count} new message{'s' if count != 1 else ''}"
                                    + ("+" if count >= 50 else ""), "scNewTag", wrap=False))
            else:
                line = QFrame()
                line.setObjectName("scNewLine")
                line.setFixedHeight(2)
                row.addWidget(line, 1)
        return holder

    def _scrolled(self, _value: int) -> None:
        if self._pending_new and self._at_bottom():
            self._pending_new = 0
            self.jump.hide()

    def _jump_down(self) -> None:
        bar = self.chat_scroll.verticalScrollBar()
        bar.setValue(bar.maximum())

    def add_messages(self, messages: list[GroupMessage], force_scroll: bool = False,
                     last_read: Optional[int] = None) -> None:
        """Add messages at the bottom. last_read (only for the first load):
        the last message id you had read before opening, so a "N new
        messages" divider goes in front of the first newer one."""
        if not messages:
            return
        stick = force_scroll or self._at_bottom()
        unread = ([m for m in messages if m.id > last_read and not m.is_mine
                   and m.id not in self._seen_ids] if last_read is not None else [])
        added = 0
        for message in messages:
            if message.id in self._seen_ids:
                continue
            added += 1
            self._seen_ids.add(message.id)
            if unread and not self._divider_done and message.id == unread[0].id:
                self._divider = self._make_divider(len(unread))
                self._divider_done = True
                self.messages.insertWidget(self.messages.count() - 1, self._divider)
            bubble = MessageBubble(message)
            bubble.menu_requested.connect(self.message_menu.emit)
            bubble.picture_clicked.connect(self.image_opened.emit)
            if bubble.picture is not None:
                path = message.attachment
                self._bubbles.setdefault(path, []).append(bubble)
                if path in self._pixmaps:
                    bubble.set_picture(self._pixmaps[path])
                elif path not in self._asked:
                    self._asked.add(path)
                    self.image_requested.emit(path)
            holder = QHBoxLayout()
            holder.setContentsMargins(0, 0, 0, 0)
            if message.is_mine:
                holder.addStretch(1)
            holder.addWidget(bubble, 4)
            if not message.is_mine:
                holder.addStretch(1)
            wrap = QWidget()
            wrap.setObjectName("panel")
            wrap.setLayout(holder)
            self.messages.insertWidget(self.messages.count() - 1, wrap)
            self._last_id = max(self._last_id, message.id)
        self.empty_chat.hide()
        if self._divider is not None and force_scroll and unread:
            # Opening a group with unread messages: start where they start.
            divider = self._divider
            QTimer.singleShot(80, lambda: self.chat_scroll.verticalScrollBar().setValue(
                max(0, divider.y() - 12)) if shiboken6.isValid(divider) else None)
        elif stick:
            QTimer.singleShot(30, lambda: self.chat_scroll.verticalScrollBar().setValue(
                self.chat_scroll.verticalScrollBar().maximum()))
        elif added and last_read is None:
            self._pending_new += sum(1 for m in messages if not m.is_mine)
            if self._pending_new:
                set_text(self.jump, f"{self._pending_new} new message"
                         f"{'s' if self._pending_new != 1 else ''}")
                self.jump.show()

    # ------------------------------------------------------------ mentions

    def _mention_query(self) -> Optional[tuple[int, str]]:
        """(position of the @, the letters typed after it), or None."""
        cursor = self.input.textCursor()
        before = self.input.toPlainText()[:cursor.position()]
        match = MENTION.search(before)
        if match is None:
            return None
        return match.start(1) - 1, match.group(1)

    def _suggest_mentions(self) -> None:
        found = self._mention_query()
        group = self.group
        if found is None or group is None:
            self.mentions.hide()
            return
        query = found[1].lower()
        others = [m for m in group.members_list
                  if (m.mention or m.handle) and not m.is_me and m.id not in group.blocked_ids]
        people = [m for m in others
                  if not query or query in (m.mention or m.handle).lower() or query in m.name.lower()]
        # people whose handle or name STARTS with it first, then the rest by name
        people.sort(key=lambda m: (not ((m.mention or m.handle).lower().startswith(query)
                                        or m.name.lower().startswith(query)), m.name.lower()))
        if people:
            empty = ""
        elif not others:
            empty = "Nobody else in this group can be mentioned yet."
        else:
            empty = f"No member matches “{found[1]}”."
        self.mentions.show_matches(people, empty)
        if self.mentions.isVisible():
            top = self.input.mapTo(self, QPoint(0, 0))
            width = min(420, max(260, self.input.width()))
            self.mentions.setFixedWidth(width)
            height = self.mentions.height_for_rows()
            self.mentions.setFixedHeight(height)
            self.mentions.move(top.x(), max(0, top.y() - height - 4))
            self.mentions.raise_()

    def _insert_mention(self, handle: str) -> None:
        found = self._mention_query()
        if found is None:
            return
        start, _typed = found
        cursor = self.input.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(self.input.textCursor().position(), cursor.MoveMode.KeepAnchor)
        cursor.insertText(f"@{handle} ")
        self.input.setTextCursor(cursor)
        self.mentions.hide()
        self.input.setFocus()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if watched is self.input and event.type() == QEvent.Type.KeyPress                 and self.mentions.isVisible():
            key = event.key()
            if key == Qt.Key.Key_Down:
                self.mentions.move_by(1)
                return True
            if key == Qt.Key.Key_Up:
                self.mentions.move_by(-1)
                return True
            if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Tab)                     and not event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self.mentions.pick_current()
                return True
            if key == Qt.Key.Key_Escape:
                self.mentions.hide()
                return True
        return super().eventFilter(watched, event)

    def _check_input(self) -> None:
        text = self.input.toPlainText()
        problem = check_message(text) if text.strip() else None
        self.input_warning.setText(problem or "")
        self.send.setEnabled(bool(text.strip()) and problem is None)
        n = len(text.strip())
        self.count.setText(f"{n:,} / {MESSAGE_MAX:,}" if n > MESSAGE_MAX - 300 else "")

    def _send(self) -> None:
        text = self.input.toPlainText().strip()
        if text and check_message(text) is None:
            self.send.setEnabled(False)
            self.input.setReadOnly(True)
            self.send_requested.emit(text)

    def sent(self) -> None:
        self.input.setReadOnly(False)
        self.input.clear()
        self.input.setFocus()

    def send_failed(self, message: str) -> None:
        self.input.setReadOnly(False)
        self.input_warning.setText(message)
        self._check_input()
        self.input_warning.setText(message)

    # ================================================================= notes

    def show_notes(self, notes: list[GroupNote]) -> None:
        self._notes = notes
        if self.tab == "notes":
            self._draw_notes()

    def _draw_notes(self) -> None:
        clear_layout(self.list_col)
        if self.group is None:
            return
        top = QHBoxLayout()
        top.addWidget(label("Read-only copies members shared. Open one to read it, or save "
                            "your own copy to your notebook.", "acSmall"), 1)
        top.addWidget(button("Share a note…", "acPrimary", "share-2", self.share_note_requested.emit))
        self.list_col.addLayout(top)
        if not self._notes:
            self.list_col.addWidget(label("No notes shared yet.", "acMuted"))
        for note in self._notes:
            sub = f"updated {short_when(note.updated_at)}"
            if note.status == "hidden":
                sub += "  ·  hidden from members"
            row = PersonRow(note.owner, sub, title=note.title, clickable=True)
            row.clicked.connect(lambda n=note: self.note_action.emit("open", n))
            row.add_action("Open", lambda n=note: self.note_action.emit("open", n), "acLink")
            row.add_action("Save a copy", lambda n=note: self.note_action.emit("save", n), "acGhost",
                           "download")
            extra = button("", "acGhost", "ellipsis")
            extra.clicked.connect(lambda _c=False, n=note, b=extra: self._note_menu(n, b))
            row.actions.addWidget(extra)
            row.profile_requested.connect(self.profile_requested.emit)
            self.list_col.addWidget(row)
        self.list_col.addStretch(1)

    def _note_menu(self, note: GroupNote, anchor: QWidget) -> None:
        menu = QMenu(self)
        menu.setObjectName("exMenu")
        if note.is_mine or (self.group and self.group.is_staff):
            menu.addAction("Remove from the shelf", lambda: self.note_action.emit("remove", note))
        if self.group and self.group.is_staff and not note.is_mine:
            menu.addAction("Unhide" if note.status == "hidden" else "Hide from members",
                           lambda: self.note_action.emit("unhide" if note.status == "hidden" else "hide",
                                                         note))
        if not note.is_mine:
            menu.addAction("Report…", lambda: self.note_action.emit("report", note))
        if not menu.actions():
            return
        menu.exec(anchor.mapToGlobal(QPoint(0, anchor.height() + 4)))

    # =============================================================== members

    def set_new_token(self, token: Optional[str]) -> None:
        self._token = token
        if self.tab == "members":
            self._draw_members()

    @property
    def token(self) -> Optional[str]:
        return self._token

    def _draw_members(self) -> None:
        clear_layout(self.list_col)
        group = self.group
        if group is None:
            return
        if group.is_staff:
            self._draw_invites(group)
        self.list_col.addWidget(label(f"MEMBERS ({len(group.members_list)}/{GROUP_MEMBER_CAP})",
                                      "scSection", wrap=False))
        for person in group.members_list:
            blocked = person.id in group.blocked_ids
            row = PersonRow(person, "blocked by one of you" if blocked else "")
            row.profile_requested.connect(self.profile_requested.emit)
            actions = self._member_actions(group, person)
            if actions:
                more = button("", "acGhost", "ellipsis")
                more.clicked.connect(lambda _c=False, p=person, b=more, a=actions:
                                     self._member_menu(p, b, a))
                row.actions.addWidget(more)
            self.list_col.addWidget(row)
        self.list_col.addStretch(1)

    @staticmethod
    def _member_actions(group: StudyGroup, person: Person) -> list[tuple[str, str]]:
        if person.is_me:
            return []
        out = []
        if group.my_role == "owner":
            if person.group_role == "member":
                out.append(("moderator", "Make moderator"))
            elif person.group_role == "moderator":
                out.append(("member", "Make member (not moderator)"))
            out.append(("owner", "Make owner (you become a moderator)"))
            out.append(("remove", "Remove from the group"))
        elif group.my_role == "moderator" and person.group_role == "member":
            out.append(("remove", "Remove from the group"))
        return out

    def _member_menu(self, person: Person, anchor: QWidget, actions: list) -> None:
        menu = QMenu(self)
        menu.setObjectName("exMenu")
        for key, text in actions:
            menu.addAction(text, lambda k=key: self.member_action.emit(k, person))
        menu.exec(anchor.mapToGlobal(QPoint(0, anchor.height() + 4)))

    def _draw_invites(self, group: StudyGroup) -> None:
        self.list_col.addWidget(label("INVITE PEOPLE", "scSection", wrap=False))
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(button("Invite friends…", "acPrimary", "plus", self.invite_friends_requested.emit))
        row.addStretch(1)
        self.list_col.addLayout(row)

        box = QFrame()
        box.setObjectName("scRow")
        col = QVBoxLayout(box)
        col.setContentsMargins(14, 12, 14, 12)
        col.setSpacing(8)
        col.addWidget(label("Invite link", "scRowTitle"))
        link = group.invite_link
        if self._token:
            col.addWidget(label("New link ready. Copy it now: for safety Akeso keeps only a "
                                "scrambled form of it, so it can't be shown again later.", "acSmall"))
        elif link:
            expires = (f"expires {link.get('expires_at', '')[:16].replace('T', ' ')}"
                       if link.get("expires_at") else "no expiry")
            col.addWidget(label(f"A link is active ({expires}, used {link.get('uses', 0)} times). "
                                "It can only be copied when it's made: make a new one to copy it "
                                "again (the old one then stops working).", "acSmall"))
        else:
            col.addWidget(label("Anyone with the link or its code can join (up to 50 members). "
                                "Paste it into Messenger, email or any app.", "acSmall"))
        actions = QHBoxLayout()
        actions.setSpacing(6)
        if self._token:
            actions.addWidget(button("Copy invite", "acPrimary", "copy", self.link_copy_requested.emit))
        self._expiry = QComboBox()
        self._expiry.setObjectName("acInput")
        for text, hours in EXPIRY_CHOICES:
            self._expiry.addItem(text, hours)
        actions.addWidget(self._expiry)
        actions.addWidget(button("New link" if (link or self._token) else "Make invite link",
                                 "acGhost", "refresh-cw",
                                 lambda: self.link_create_requested.emit(self._expiry.currentData())))
        if link or self._token:
            actions.addWidget(button("Turn off link", "acGhost", "x", self.link_revoke_requested.emit))
        actions.addStretch(1)
        col.addLayout(actions)
        self.list_col.addWidget(box)

        if group.pending_invites:
            self.list_col.addWidget(label(f"WAITING FOR AN ANSWER ({len(group.pending_invites)})",
                                          "scSection", wrap=False))
            for person in group.pending_invites:
                self.list_col.addWidget(PersonRow(person, "invited"))

    def copy_invite(self, text: str) -> None:
        QGuiApplication.clipboard().setText(text)
        self.banner.show_message("Invite copied. Paste it into Messenger or any app.", "good",
                                 "OK")

    def refresh_theme(self) -> None:
        refresh_icons(self)
        for tab in self.tabs.values():
            repolish(tab)


class InviteFriendsDialog(AccountDialog):
    submitted = Signal(list)                      # friend ids

    def __init__(self, friends: list[Friend], member_ids: set, pending_ids: set,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__("Invite friends", "They get a notification and can join with one "
                         "click.", "plus", parent, width=480)
        self._boxes: dict[str, QCheckBox] = {}
        available = [f for f in friends if f.person.id not in member_ids]
        if not available:
            self.body.addWidget(label("All your friends are already in this group, or you have "
                                      "no friends yet (Community → Friends).", "acMuted"))
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setMaximumHeight(260)
        host = QWidget()
        host.setObjectName("panel")
        col = QVBoxLayout(host)
        col.setContentsMargins(0, 0, 0, 0)
        for friend in available:
            box = QCheckBox(friend.person.label + ("  (invited)" if friend.person.id in pending_ids else ""))
            box.setEnabled(friend.person.id not in pending_ids)
            self._boxes[friend.person.id] = box
            col.addWidget(box)
        col.addStretch(1)
        scroll.setWidget(host)
        if available:
            self.body.addWidget(scroll)
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Send invites", "acPrimary", "check", self._submit, default=True)

    def _submit(self) -> None:
        ids = [key for key, box in self._boxes.items() if box.isChecked() and box.isEnabled()]
        if not ids:
            self.show_error("Tick at least one friend.")
            return
        self.set_busy(True)
        self.submitted.emit(ids)
