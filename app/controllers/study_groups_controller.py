"""Community > Study Groups (migration 042).

Chat delivery: no live connection in this version. While a group is open
AND the Akeso window is visible, the controller asks for messages newer
than the last one it has (group_messages_after), every 4 seconds, slowing
down to every 30 seconds while nothing new arrives, and back to 4 seconds
as soon as something does or the user sends. Nothing is fetched while the
group is closed, the window is minimised or hidden.
"""

from typing import Optional

from PySide6.QtCore import QObject, QPoint, QTimer, Signal
from PySide6.QtWidgets import QMenu

from app.controllers.social_common import is_not_installed, run
from app.models.social import GroupMessage, GroupNote, SharedNote, StudyGroup
from app.services.notebook_share_service import NotebookShareService, ShareError, snapshot
from app.services.study_group_service import StudyGroupService, invite_text
from app.ui.views.account.account_dialogs import AccountDialog, ConfirmDialog, NoticeDialog
from app.ui.views.account.account_widgets import label
from app.ui.views.social.group_page import GroupPage, InviteFriendsDialog
from app.ui.views.social.share_views import SharedNoteReader
from app.ui.views.social.study_groups_view import (
    CreateGroupDialog, GroupReportDialog, StudyGroupsView,
)

POLL_STEPS_MS = (4_000, 4_000, 8_000, 15_000, 30_000)    # backoff while quiet


class StudyGroupsController(QObject):
    profile_requested = Signal(str)
    notebook_changed = Signal()               # a shelf note was saved as a copy
    unread_changed = Signal(int)              # unread messages + waiting invites (sidebar dot)

    def __init__(self, view: StudyGroupsView, page: GroupPage, service: StudyGroupService,
                 friends, notebook=None, share: Optional[NotebookShareService] = None,
                 is_moderator: bool = False, sheet=None, reader_sheet=None) -> None:
        super().__init__(view)
        self._view = view
        self._page = page
        self._service = service
        self._friends = friends                   # FriendsController
        self._notebook = notebook                 # NotebookService (share a note, save copies)
        self._share = share
        self._is_mod = is_moderator
        self._sheet = sheet
        self._reader_sheet = reader_sheet
        self._reader = SharedNoteReader()
        self._group: Optional[StudyGroup] = None
        self._pictures: dict[str, bytes] = {}      # downloaded chat pictures, by storage path
        self._loaded = False
        self._polling = False                     # a poll request is in flight
        self._quiet = 0
        self.installed = True

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._poll)

        view.refresh_requested.connect(lambda: self.reload(quiet=False))
        view.open_requested.connect(self.open_group)
        view.create_requested.connect(self._create)
        view.join_public_requested.connect(self._join_public)
        view.join_token_requested.connect(self._join_token)
        view.invite_answered.connect(self._answer_invite)
        view.browse_requested.connect(self._browse)
        view.report_action.connect(self._report_action)
        view.set_moderator(is_moderator)

        p = page
        p.send_requested.connect(self._send)
        p.attach_requested.connect(self._attach_picture)
        p.image_requested.connect(self._load_picture)
        p.image_opened.connect(self._view_picture)
        p.message_menu.connect(self._message_menu)
        p.share_note_requested.connect(self._share_note)
        p.note_action.connect(self._note_action)
        p.invite_friends_requested.connect(self._invite_friends)
        p.link_create_requested.connect(self._new_link)
        p.link_copy_requested.connect(self._copy_link)
        p.link_revoke_requested.connect(self._revoke_link)
        p.member_action.connect(self._member_action)
        p.leave_requested.connect(self._leave)
        p.delete_requested.connect(self._delete)
        p.mute_toggled.connect(self._mute)
        p.join_requested.connect(lambda: self._group and self._join_public(self._group.id))
        p.profile_requested.connect(self.profile_requested.emit)
        p.tab_changed.connect(self._tab_changed)

        if sheet is not None:
            sheet.set_content(page)
            sheet.close_requested.connect(sheet.close_sheet)
            sheet.closed.connect(self._closed)
        if reader_sheet is not None:
            reader_sheet.set_content(self._reader)
            reader_sheet.close_requested.connect(reader_sheet.close_sheet)
        self._reader.save_requested.connect(self._save_shelf_copy)

    # ============================================================ directory

    def on_shown(self) -> None:
        self.reload(quiet=self._loaded)
        if self._group is not None and self._sheet is not None and self._sheet.is_open:
            self._schedule(0)

    def reload(self, quiet: bool = True) -> None:
        if not quiet:
            self._view.show_loading("Loading your study groups…")

        def done(data) -> None:
            groups, invites = data
            self._loaded = True
            self.installed = True
            self._view.show_home(groups, invites)
            self.unread_changed.emit(sum(g.unread for g in groups) + len(invites))
        run(self._view, self._service.home, done, self._failed)
        if self._is_mod:
            run(self._view, self._service.report_queue, self._view.show_reports, lambda _m: None)

    def set_body_systems(self, systems: list[tuple[str, str]]) -> None:
        self._view.set_body_systems(systems)
        self._body_systems = systems

    def _failed(self, message: str) -> None:
        self._view.set_busy(False)
        if is_not_installed(message):
            self.installed = False
            self._view.show_not_installed(message)
            return
        self._view.banner.show_message(message, "danger", "Dismiss")

    def _browse(self, search: str, topic: str, body_system: str) -> None:
        run(self._view, lambda: self._service.browse(search, topic, body_system),
            self._view.show_browse, self._failed)

    def _create(self) -> None:
        dialog = CreateGroupDialog(getattr(self, "_body_systems", []), parent=self._view)

        def submit(name, description, visibility, topic, body_system) -> None:
            def done(group_id: str) -> None:
                dialog.accept()
                self.reload()
                self.open_group(group_id)
            run(dialog, lambda: self._service.create(name, description, visibility, topic,
                                                      body_system), done, dialog.show_error)
        dialog.submitted.connect(submit)
        dialog.exec()

    def _join_public(self, group_id: str) -> None:
        def done(_r) -> None:
            self.reload()
            self.open_group(group_id)
        run(self._view, lambda: self._service.join_public(group_id), done, self._failed)

    def _join_token(self, text: str) -> None:
        self._view.set_busy(True)

        def done(group_id: str) -> None:
            self._view.joined()
            self._view.banner.show_message("You joined the group.", "good", "OK")
            self.reload()
            self.open_group(group_id)
        run(self._view, lambda: self._service.join_with(text), done, self._failed)

    def join_from_link(self, token: str) -> None:
        """akeso://join/<token> opened Akeso (installer protocol handler)."""
        self._view.join_input.setText(token)
        self._join_token(token)

    def _answer_invite(self, invite_id: str, accept: bool) -> None:
        def done(group_id: str) -> None:
            self.reload()
            if accept:
                self.open_group(group_id)
        run(self._view, lambda: self._service.respond(invite_id, accept), done, self._failed)

    def _report_action(self, report, action: str) -> None:
        def done(_r) -> None:
            self._view.banner.show_message("Done. The report is closed.", "good", "OK")
            self.reload()
        run(self._view, lambda: self._service.moderate(report.group_id, report.target_kind,
                                                       report.target_id, action),
            done, self._failed)

    # ================================================================ a group

    def open_group(self, group_id: str) -> None:
        if not group_id:
            return
        same = self._group is not None and self._group.id == group_id
        if not same:
            self._group = None
            self._page.show_loading()
        if self._sheet is not None:
            self._sheet.open_sheet()
            self._sheet.raise_()
            self._sheet.tab.raise_()
        self._load_group(group_id, first=not same)

    def _load_group(self, group_id: str, first: bool = False) -> None:
        def done(group: StudyGroup) -> None:
            self._group = group
            self._page.show_group(group)
            if group.is_member:
                if first:
                    self._fetch_messages(initial=True)
                    self._load_notes()
                else:
                    self._schedule(0)
        run(self._page, lambda: self._service.get(group_id), done, self._page.show_error)

    def _closed(self) -> None:
        self._timer.stop()
        self.reload()                                   # unread counts, and the sidebar dot

    def _tab_changed(self, tab: str) -> None:
        if self._group is None:
            return
        if tab == "notes":
            self._load_notes()
        elif tab == "members":
            self._load_group(self._group.id)

    def _load_notes(self) -> None:
        group = self._group
        if group is None:
            return
        run(self._page, lambda: self._service.notes(group.id),
            lambda notes: self._group is group and self._page.show_notes(notes),
            lambda m: self._page.banner.show_message(m, "danger", "OK"))

    # ---------------------------------------------------------------- chat

    def _window_visible(self) -> bool:
        window = self._page.window()
        return bool(window and window.isVisible() and not window.isMinimized())

    def _schedule(self, delay: Optional[int] = None) -> None:
        if delay is None:
            delay = POLL_STEPS_MS[min(self._quiet, len(POLL_STEPS_MS) - 1)]
        self._timer.start(delay)

    def _poll(self) -> None:
        group = self._group
        if group is None or not group.is_member:
            return
        sheet_open = self._sheet is None or self._sheet.is_open
        if not sheet_open:
            return                                      # closed: no more polling
        if not self._window_visible() or not self._page.isVisible():
            self._schedule(POLL_STEPS_MS[-1])           # check back later, fetch nothing
            return
        self._fetch_messages()

    def _fetch_messages(self, initial: bool = False) -> None:
        group = self._group
        if group is None or self._polling:
            return
        self._polling = True
        after = None if initial else self._page.last_id

        def done(data) -> None:
            self._polling = False
            if self._group is not group:
                return
            messages, more, last_read = data
            self._page.add_messages(messages, force_scroll=initial,
                                    last_read=last_read if initial else None)
            self._quiet = 0 if messages else self._quiet + 1
            if more and not initial:
                self._schedule(200)                     # catch up quickly
            else:
                self._schedule()

        def failed(message: str) -> None:
            self._polling = False
            self._quiet += 1
            if "not available" in message:
                self._page.show_error(message)          # removed from the group
                return
            self._schedule()
        run(self._page, lambda: self._service.messages_after(group.id, after), done, failed)

    def _send(self, text: str) -> None:
        group = self._group
        if group is None:
            return

        def done(message: GroupMessage) -> None:
            self._page.sent()
            self._quiet = 0
            self._fetch_messages()                      # anything others wrote meanwhile
            if self._page.last_id is None or message.id > (self._page.last_id or 0):
                self._page.add_messages([message], force_scroll=True)
        run(self._page, lambda: self._service.send(group.id, text), done, self._page.send_failed)

    # ------------------------------------------------------------ pictures

    def _attach_picture(self) -> None:
        """The picture button: choose a file, check and shrink it, show it for
        confirmation, then upload and send."""
        group = self._group
        if group is None:
            return
        from PySide6.QtWidgets import QFileDialog
        file_path, _filter = QFileDialog.getOpenFileName(
            self._page, "Choose a picture", "", "Pictures (*.png *.jpg *.jpeg)")
        if not file_path:
            return
        self._page.set_busy(True)

        def prepared(result) -> None:
            self._page.set_busy(False)
            self._confirm_picture(group, result)

        def failed(message: str) -> None:
            self._page.set_busy(False)
            NoticeDialog("Can't send that picture", message, "circle-alert",
                         danger=True, parent=self._page).exec()
        run(self._page, lambda: self._service.prepare_picture(file_path), prepared, failed)

    def _confirm_picture(self, group: StudyGroup, prepared) -> None:
        from app.ui.views.social.picture_dialogs import PictureConfirmDialog
        size = f"{prepared.width} × {prepared.height} px, {len(prepared.data) / 1_048_576:.1f} MB"
        caption = self._page.input.toPlainText().strip()
        dialog = PictureConfirmDialog(prepared.data, size, caption, parent=self._page)

        def submit(text: str) -> None:
            def done(message: GroupMessage) -> None:
                dialog.accept()
                self._pictures[message.attachment or ""] = prepared.data
                self._page.set_picture(message.attachment or "", prepared.data)
                self._page.input.clear()
                self._quiet = 0
                self._page.add_messages([message], force_scroll=True)
                self._fetch_messages()
            run(dialog, lambda: self._service.send_picture(group.id, prepared, text), done,
                dialog.show_error)
        dialog.submitted.connect(submit)
        dialog.exec()

    def _load_picture(self, path: str) -> None:
        """A bubble needs its picture: download it once (kept in memory)."""
        if path in self._pictures:
            self._page.set_picture(path, self._pictures[path])
            return

        def done(data: bytes) -> None:
            if len(self._pictures) >= 60:                       # keep memory modest
                self._pictures.pop(next(iter(self._pictures)))
            self._pictures[path] = data
            self._page.set_picture(path, data)
        run(self._page, lambda: self._service.picture(path), done,
            lambda _m: self._page.set_picture(path, None))

    def _view_picture(self, path: str) -> None:
        pixmap = self._page.pixmap_for(path)
        if pixmap is None:
            return
        from app.ui.views.social.picture_dialogs import PictureViewDialog
        PictureViewDialog(pixmap, self._group.name if self._group else "Picture",
                          parent=self._page).exec()

    def _message_menu(self, message: GroupMessage, where: QPoint) -> None:
        group = self._group
        if group is None:
            return
        menu = QMenu(self._page)
        menu.setObjectName("exMenu")
        if not message.is_mine:
            menu.addAction("Report…", lambda: self._report(group.id, "message", str(message.id),
                                                           "message"))
        if group.is_staff:
            if message.hidden:
                menu.addAction("Unhide", lambda: self._moderate(group.id, "message",
                                                                str(message.id), "unhide"))
            else:
                menu.addAction("Hide from members", lambda: self._moderate(
                    group.id, "message", str(message.id), "hide"))
        if message.author.handle and not message.author.is_me:
            menu.addAction("Open profile", lambda: self.profile_requested.emit(message.author.handle))
        if menu.actions():
            menu.exec(where)

    def _report(self, group_id: str, kind: str, target_id: str, what: str) -> None:
        dialog = GroupReportDialog(what, parent=self._page)

        def submit(reason: str, note: str) -> None:
            def done(_r) -> None:
                dialog.accept()
                self._page.banner.show_message("Thanks. The report was sent.", "good", "OK")
            run(dialog, lambda: self._service.report(group_id, kind, target_id, reason, note),
                done, dialog.show_error)
        dialog.submitted.connect(submit)
        dialog.exec()

    def _moderate(self, group_id: str, kind: str, target_id: str, action: str) -> None:
        def done(_r) -> None:
            if kind == "note":
                self._load_notes()
                return
            self._page.reset_chat()                     # redraw with the new state
            self._fetch_messages(initial=True)
        run(self._page, lambda: self._service.moderate(group_id, kind, target_id, action), done,
            lambda m: self._page.banner.show_message(m, "danger", "OK"))

    # --------------------------------------------------------------- notes

    def _share_note(self) -> None:
        group = self._group
        if group is None or self._notebook is None:
            return
        items = sorted(self._notebook.items(), key=lambda i: i.title.lower())
        dialog = PickNoteDialog(items, parent=self._page)

        def chosen(item_id: str) -> None:
            item = self._notebook.get(item_id)
            if item is None:
                return
            try:
                snapshot(item)
            except ShareError as exc:
                dialog.show_error(str(exc))
                return
            dialog.set_busy(True)

            def done(_r) -> None:
                dialog.accept()
                self._load_notes()
            run(dialog, lambda: self._service.share_note(group.id, item), done, dialog.show_error)
        dialog.chosen.connect(chosen)
        dialog.exec()

    def _note_action(self, action: str, note: GroupNote) -> None:
        group = self._group
        if group is None:
            return
        if action == "open":
            self._open_note(note)
        elif action == "save":
            self._fetch_note(note, then=self._save_note_copy)
        elif action == "remove":
            confirm = ConfirmDialog("Remove this note from the shelf?",
                                    "Members' saved copies stay theirs.", "Remove", "x",
                                    danger=True, parent=self._page)
            if confirm.exec() == ConfirmDialog.DialogCode.Accepted:
                run(self._page, lambda: self._service.remove_note(note.id),
                    lambda _r: self._load_notes(),
                    lambda m: self._page.banner.show_message(m, "danger", "OK"))
        elif action == "report":
            self._report(group.id, "note", note.id, "note")
        elif action in ("hide", "unhide"):
            self._moderate(group.id, "note", note.id, action)

    def _fetch_note(self, note: GroupNote, then) -> None:
        run(self._page, lambda: self._service.note(note.id), then,
            lambda m: self._page.banner.show_message(m, "danger", "OK"))

    def _as_shared(self, note: GroupNote) -> SharedNote:
        return SharedNote(id=note.id, title=note.title, kind=note.kind, owner=note.owner,
                          body=note.body, updated_at=note.updated_at)

    def _open_note(self, note: GroupNote) -> None:
        if self._reader_sheet is not None:
            self._reader_sheet.open_sheet()
            self._reader_sheet.raise_()
            self._reader_sheet.tab.raise_()
        self._reader.show_loading()
        origin = f" in “{self._group.name}”" if self._group else ""
        run(self._reader, lambda: self._service.note(note.id),
            lambda full: self._reader.show_note(self._as_shared(full), origin),
            self._reader.show_error)

    def _save_note_copy(self, note: GroupNote) -> None:
        if self._share is None:
            return
        who = f"@{note.owner.handle}" if note.owner.handle else note.owner.name
        self._share.save_copy(self._as_shared(note), who)
        self.notebook_changed.emit()
        self._page.banner.show_message(f"Saved “{note.title}” to your notebook under "
                                       "“Shared with me”.", "good", "OK")

    def _save_shelf_copy(self, shared: SharedNote) -> None:
        if self._share is None:
            return
        who = f"@{shared.owner.handle}" if shared.owner.handle else shared.owner.name
        self._share.save_copy(shared, who)
        self._reader.mark_saved("Shared with me")
        self.notebook_changed.emit()

    # ------------------------------------------------------------- members

    def _invite_friends(self) -> None:
        group = self._group
        if group is None:
            return

        def ready(friends) -> None:
            members = {p.id for p in group.members_list}
            pending = {p.id for p in group.pending_invites}
            dialog = InviteFriendsDialog(friends or [], members, pending, parent=self._page)

            def submit(ids: list) -> None:
                def send_all():
                    errors = []
                    for friend_id in ids:
                        try:
                            self._service.invite_friend(group.id, friend_id)
                        except Exception as exc:  # noqa: BLE001 - reported together
                            errors.append(str(exc))
                    return errors

                def done(errors: list) -> None:
                    if errors:
                        dialog.show_error(errors[0])
                        return
                    dialog.accept()
                    self._page.banner.show_message("Invites sent.", "good", "OK")
                    self._load_group(group.id)
                run(dialog, send_all, done, dialog.show_error)
            dialog.submitted.connect(submit)
            dialog.exec()
        run(self._page, self._friends.load_friends_now, ready,
            lambda m: self._page.banner.show_message(m, "danger", "OK"))

    def _new_link(self, expires_hours) -> None:
        group = self._group
        if group is None:
            return
        if group.invite_link:
            confirm = ConfirmDialog("Make a new invite link?",
                                    "The current link and its code stop working.", "New link",
                                    "refresh-cw", parent=self._page)
            if confirm.exec() != ConfirmDialog.DialogCode.Accepted:
                return

        def done(token: str) -> None:
            self._page.set_new_token(token)
            self._copy_link()
            self._load_group(group.id)
        run(self._page, lambda: self._service.new_link(group.id, expires_hours), done,
            lambda m: self._page.banner.show_message(m, "danger", "OK"))

    def _copy_link(self) -> None:
        if self._group is not None and self._page.token:
            self._page.copy_invite(invite_text(self._group.name, self._page.token))

    def _revoke_link(self) -> None:
        group = self._group
        if group is None:
            return

        def done(_r) -> None:
            self._page.set_new_token(None)
            self._page.banner.show_message("The invite link is off. Nobody new can join with it.",
                                           "good", "OK")
            self._load_group(group.id)
        run(self._page, lambda: self._service.revoke_link(group.id), done,
            lambda m: self._page.banner.show_message(m, "danger", "OK"))

    def _member_action(self, action: str, person) -> None:
        group = self._group
        if group is None:
            return
        if action == "remove":
            confirm = ConfirmDialog(f"Remove {person.name}?",
                                    "They leave the group. Their messages stay.", "Remove",
                                    "user-x", danger=True, parent=self._page)
            if confirm.exec() != ConfirmDialog.DialogCode.Accepted:
                return
            call = lambda: self._service.remove_member(group.id, person.id)  # noqa: E731
        else:
            if action == "owner":
                confirm = ConfirmDialog(f"Make {person.name} the owner?",
                                        "You become a moderator. Only the owner can change "
                                        "roles or delete the group.", "Make owner", "users",
                                        parent=self._page)
                if confirm.exec() != ConfirmDialog.DialogCode.Accepted:
                    return
            call = lambda: self._service.set_role(group.id, person.id, action)  # noqa: E731
        run(self._page, call, lambda _r: self._load_group(group.id),
            lambda m: self._page.banner.show_message(m, "danger", "OK"))

    def _leave(self) -> None:
        group = self._group
        if group is None:
            return
        extra = (" As the owner, the longest-standing moderator becomes the owner." if
                 group.my_role == "owner" else "")
        confirm = ConfirmDialog(f"Leave “{group.name}”?",
                                "You can rejoin a public group, or a private one with a new "
                                "invite." + extra, "Leave", "log-out", danger=True,
                                parent=self._page)
        if confirm.exec() != ConfirmDialog.DialogCode.Accepted:
            return

        def done(_r) -> None:
            self._group = None
            self._timer.stop()
            if self._sheet is not None:
                self._sheet.close_sheet()
            self.reload()
        run(self._page, lambda: self._service.leave(group.id), done,
            lambda m: NoticeDialog("Can't leave yet", m, "circle-alert", parent=self._page).exec())

    def _delete(self) -> None:
        group = self._group
        if group is None:
            return
        confirm = ConfirmDialog(f"Delete “{group.name}”?",
                                "The chat, the shared notes shelf and the invites are deleted "
                                "for everyone. Copies members saved to their notebooks stay.",
                                "Delete group", "trash-2", danger=True, parent=self._page)
        if confirm.exec() != ConfirmDialog.DialogCode.Accepted:
            return

        def done(_r) -> None:
            self._group = None
            self._timer.stop()
            if self._sheet is not None:
                self._sheet.close_sheet()
            self.reload()
        def delete_all():
            self._service.delete_group_pictures(group.id)       # while you are still the owner
            self._service.delete(group.id)
        run(self._page, delete_all, done,
            lambda m: self._page.banner.show_message(m, "danger", "OK"))

    def _mute(self, muted: bool) -> None:
        group = self._group
        if group is None:
            return
        run(self._page, lambda: self._service.set_muted(group.id, muted),
            lambda _r: self._load_group(group.id),
            lambda m: self._page.banner.show_message(m, "danger", "OK"))

    def shutdown(self) -> None:
        self._timer.stop()


class PickNoteDialog(AccountDialog):
    """Choose one of my notes to put on the group's Shared notes shelf."""

    chosen = Signal(str)

    def __init__(self, items, parent=None) -> None:
        super().__init__("Share a note with the group", "Members get a read-only copy, text "
                         "only. You can share it again later to update it.", "share-2", parent,
                         width=480)
        from PySide6.QtWidgets import QListWidget, QListWidgetItem
        self.list = QListWidget()
        self.list.setObjectName("acInput")
        self.list.setMinimumHeight(240)
        for item in items:
            row = QListWidgetItem(item.title)
            row.setData(256, item.id)
            self.list.addItem(row)
        if not items:
            self.body.addWidget(label("Your notebook has no notes yet.", "acMuted"))
        self.body.addWidget(self.list)
        self.list.itemDoubleClicked.connect(lambda _i: self._submit())
        self.add_button("Cancel", on_click=self.reject)
        self.add_button("Share", "acPrimary", "share-2", self._submit, default=True)

    def _submit(self) -> None:
        current = self.list.currentItem()
        if current is None:
            self.show_error("Choose a note.")
            return
        self.chosen.emit(str(current.data(256)))
