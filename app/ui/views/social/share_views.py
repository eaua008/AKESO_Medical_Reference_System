"""Sharing Study Notebook notes (migration 041).

    ShareNoteDialog      who gets a read-only copy: friends (picked from a
                         searchable list, never typed handles), or one of
                         my study groups' Shared notes shelf
    ManageSharingDialog  who has it now: Unshare, Update shared copy
    SharedWithMeList     the notes friends shared with me (notebook home)
    SharedNoteReader     one shared note, read-only, with Save a copy
"""

from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup, QCheckBox, QFrame, QHBoxLayout, QLineEdit, QRadioButton, QScrollArea,
    QTextBrowser, QVBoxLayout, QWidget,
)

from app.models.social import Friend, Person, SharedNote, StudyGroup
from app.ui.components.akeso_loader import LoadingLabel
from app.ui.views.account.account_dialogs import AccountDialog
from app.ui.views.account.account_widgets import (
    button, icon_label, label, pill, refresh_icons, set_text,
)
from app.ui.views.social.social_widgets import PersonRow, StatePanel, clear_layout, short_when

UNSHARE_NOTE = ("They lose access to the shared copy straight away. Copies they already "
                "saved to their own notebook stay theirs.")


# ======================================================================
#   Share
# ======================================================================

class ShareNoteDialog(AccountDialog):
    share_friends = Signal(list)          # friend ids
    share_group = Signal(str)             # group id

    def __init__(self, title: str, friends: list[Friend], groups: list[StudyGroup],
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(f"Share “{title}”",
                         "They get a read-only copy of the note as it is now, text only "
                         "(pictures are left out). You can update or unshare it later.",
                         "share-2", parent, width=520)
        self._boxes: dict[str, QCheckBox] = {}
        self._group_buttons = QButtonGroup(self)
        self._group_buttons.setExclusive(True)

        target = QHBoxLayout()
        self._to_friends = QRadioButton("Friends")
        self._to_group = QRadioButton("A study group")
        self._to_friends.setChecked(True)
        target.addWidget(self._to_friends)
        target.addWidget(self._to_group)
        target.addStretch(1)
        self._to_group.setVisible(bool(groups))
        self.body.addLayout(target)

        # friends
        self._friends_box = QWidget()
        self._friends_box.setObjectName("panel")
        col = QVBoxLayout(self._friends_box)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(6)
        if not friends:
            col.addWidget(label("You have no friends to share with yet. Add friends under "
                                "Community → Friends.", "acMuted"))
        else:
            self._search = QLineEdit()
            self._search.setObjectName("acInput")
            self._search.setPlaceholderText("Search your friends")
            self._search.textChanged.connect(self._filter)
            col.addWidget(self._search)
            col.addWidget(self._scroll_list(
                [(f.person.id, f.person.label) for f in friends], self._boxes))
        self.body.addWidget(self._friends_box)

        # groups
        self._groups_box = QWidget()
        self._groups_box.setObjectName("panel")
        gcol = QVBoxLayout(self._groups_box)
        gcol.setContentsMargins(0, 0, 0, 0)
        gcol.setSpacing(6)
        gcol.addWidget(label("It goes on the group's Shared notes shelf, where every member "
                             "can read it and save a copy.", "acSmall"))
        host = QWidget()
        host.setObjectName("panel")
        hcol = QVBoxLayout(host)
        hcol.setContentsMargins(0, 0, 0, 0)
        for index, group in enumerate(groups):
            radio = QRadioButton(f"{group.name}  ·  {group.members} members")
            radio.setProperty("group_id", group.id)
            radio.setChecked(index == 0)
            self._group_buttons.addButton(radio)
            hcol.addWidget(radio)
        gcol.addWidget(host)
        self._groups_box.hide()
        self.body.addWidget(self._groups_box)
        self._to_group.toggled.connect(self._target_changed)

        self.add_button("Cancel", on_click=self.reject)
        self.go = self.add_button("Share", "acPrimary", "share-2", self._submit, default=True)
        self.go.setEnabled(bool(friends) or bool(groups))

    @staticmethod
    def _scroll_list(items: list[tuple[str, str]], boxes: dict) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setMaximumHeight(240)
        host = QWidget()
        host.setObjectName("panel")
        col = QVBoxLayout(host)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(4)
        for key, text in items:
            box = QCheckBox(text)
            boxes[key] = box
            col.addWidget(box)
        col.addStretch(1)
        scroll.setWidget(host)
        return scroll

    def _filter(self, text: str) -> None:
        words = text.lower().split()
        for box in self._boxes.values():
            box.setVisible(all(w in box.text().lower() for w in words))

    def _target_changed(self) -> None:
        to_group = self._to_group.isChecked()
        self._groups_box.setVisible(to_group)
        self._friends_box.setVisible(not to_group)

    def _submit(self) -> None:
        if self._to_group.isChecked():
            chosen = self._group_buttons.checkedButton()
            if chosen is None:
                self.show_error("Choose a study group.")
                return
            self.set_busy(True)
            self.share_group.emit(str(chosen.property("group_id")))
            return
        ids = [key for key, box in self._boxes.items() if box.isChecked()]
        if not ids:
            self.show_error("Tick at least one friend.")
            return
        self.set_busy(True)
        self.share_friends.emit(ids)


class ManageSharingDialog(AccountDialog):
    unshare_requested = Signal(object)    # Person, or None for everyone
    update_requested = Signal()

    def __init__(self, share: SharedNote, parent: Optional[QWidget] = None) -> None:
        super().__init__(f"Sharing “{share.title}”",
                         f"Shared copy last updated {short_when(share.updated_at)}. Recipients "
                         "see that copy, not your live note.", "share-2", parent, width=520)
        self.share = share
        self._rows = QVBoxLayout()
        self._rows.setSpacing(6)
        self.body.addLayout(self._rows)
        self.show_recipients(share.recipients)
        self.add_button("Close", on_click=self.accept)
        self.everyone = self.add_button("Unshare from everyone", "acGhost", "x",
                                        lambda: self.unshare_requested.emit(None))
        self.add_button("Update shared copy", "acPrimary", "refresh-cw", self.update_requested.emit,
                        default=True)

    def show_recipients(self, people: list[Person]) -> None:
        clear_layout(self._rows)
        if not people:
            self._rows.addWidget(label("Nobody has this note any more.", "acMuted"))
        for person in people:
            row = PersonRow(person)
            row.add_action("Unshare", lambda p=person: self.unshare_requested.emit(p), "acGhost")
            self._rows.addWidget(row)
        if hasattr(self, "everyone"):
            self.everyone.setEnabled(bool(people))


# ======================================================================
#   Receive
# ======================================================================

class SharedWithMeList(QWidget):
    """The notebook home's list area while "Shared with me" is selected."""

    open_requested = Signal(str)          # share id

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self._col = QVBoxLayout(self)
        self._col.setContentsMargins(0, 2, 6, 20)
        self._col.setSpacing(8)

    def show_loading(self) -> None:
        clear_layout(self._col)
        loading = LoadingLabel("", "acMuted")
        loading.set_loading("Loading notes shared with you…")
        self._col.addWidget(loading)
        self._col.addStretch(1)

    def show_message(self, title: str, text: str, icon: str = "share-2") -> None:
        clear_layout(self._col)
        self._col.addWidget(StatePanel(title, text, icon))
        self._col.addStretch(1)

    def show_notes(self, notes: list[SharedNote]) -> None:
        clear_layout(self._col)
        if not notes:
            self.show_message("Nothing shared with you yet",
                              "When a friend shares a note with you, it appears here. You can "
                              "read it and save your own copy.")
            return
        self._col.addWidget(label("Read-only copies your friends shared with you. Save a copy "
                                  "to keep it and edit it in your own notebook.", "acSmall"))
        for note in notes:
            row = PersonRow(note.owner, f"shared {short_when(note.shared_at)}",
                            title=note.title, clickable=True)
            row.clicked.connect(lambda sid=note.id: self.open_requested.emit(sid))
            if not note.opened:
                row.actions.addWidget(pill("New", "acPillGood"))
            row.add_action("Open", lambda sid=note.id: self.open_requested.emit(sid), "acPrimary")
            self._col.addWidget(row)
        self._col.addStretch(1)


class _TextOnly(QTextBrowser):
    """Shows the snapshot without loading anything (pictures were removed;
    any other resource is refused)."""

    def loadResource(self, kind, url):  # noqa: N802
        return None


class SharedNoteReader(QWidget):
    """One shared note, read-only, in a full-page sheet."""

    save_requested = Signal(object)       # SharedNote
    report_requested = Signal(object)     # GroupNote / SharedNote (group shelf only)
    close_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.note: Optional[SharedNote] = None
        col = QVBoxLayout(self)
        col.setContentsMargins(56, 22, 40, 24)
        col.setSpacing(12)

        self.banner = QFrame()
        self.banner.setObjectName("scReadOnlyBanner")
        row = QHBoxLayout(self.banner)
        row.setContentsMargins(14, 10, 10, 10)
        row.setSpacing(10)
        row.addWidget(icon_label("eye", 16))
        self.banner_text = label("", "scReadOnlyText")
        row.addWidget(self.banner_text, 1)
        self.save = button("Save a copy to my notebook", "acPrimary", "download",
                           lambda: self.note and self.save_requested.emit(self.note))
        row.addWidget(self.save)
        col.addWidget(self.banner)

        self.title = label("", "acTitle")
        col.addWidget(self.title)
        self.status = label("", "acSmall")
        col.addWidget(self.status)
        self.text = _TextOnly()
        self.text.setObjectName("scReader")
        self.text.setOpenLinks(False)
        self.text.setReadOnly(True)
        col.addWidget(self.text, 1)
        self.loading = LoadingLabel("", "acMuted")
        col.addWidget(self.loading)
        self.loading.hide()

    def show_loading(self) -> None:
        self.note = None
        self.title.setText("")
        self.text.clear()
        self.status.setText("")
        self.banner.hide()
        self.loading.set_loading("Opening the shared note…")
        self.loading.show()

    def show_note(self, note: SharedNote, origin: str = "") -> None:
        self.note = note
        self.loading.hide()
        self.banner.show()
        who = f"@{note.owner.handle}" if note.owner.handle else note.owner.name
        self.banner_text.setText(f"Shared by {who}{origin}  ·  read-only")
        self.title.setText(note.title)
        self.status.setText(f"Shared copy from {short_when(note.updated_at)}")
        self.text.setHtml(note.body or "<p><i>This note has no text.</i></p>")
        self.save.setEnabled(True)
        set_text(self.save, "Save a copy to my notebook")

    def show_error(self, message: str) -> None:
        self.loading.hide()
        self.banner.hide()
        self.title.setText("Not available")
        self.text.setHtml(f"<p>{message}</p>")

    def mark_saved(self, where: str) -> None:
        set_text(self.save, "Saved")
        self.save.setEnabled(False)
        self.status.setText(f"Saved to your notebook under “{where}”. That copy is yours "
                            "to edit.")

    def refresh_theme(self) -> None:
        refresh_icons(self)
