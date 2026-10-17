"""Sharing Study Notebook notes with friends or a study group (migration 041).

Sender side: "Share…" on a note card or in the editor, "Manage sharing…"
on a shared note, and the "Shared" badge on its card.
Receiver side: "Shared with me" in the notebook's library list, the
read-only reader (a full-page sheet) and "Save a copy to my notebook".

Normal notebook sync is untouched: a saved copy is just a new local note.
"""

import time
from typing import Callable, Optional

from PySide6.QtCore import QObject, QTimer, Signal

from app.controllers.social_common import is_not_installed, run
from app.models.social import SharedNote
from app.services.notebook_share_service import (
    SHARED_SUBJECT, NotebookShareService, ShareError, snapshot,
)
from app.ui.views.account.account_dialogs import ConfirmDialog, NoticeDialog
from app.ui.views.social.share_views import (
    UNSHARE_NOTE, ManageSharingDialog, ShareNoteDialog, SharedNoteReader,
)

STALE_SECONDS = 60


class NotebookShareController(QObject):
    notebook_changed = Signal()               # a copy was saved into the notebook

    def __init__(self, notebook_controller, service: NotebookShareService, friends,
                 groups: Optional[Callable] = None,
                 reader: Optional[SharedNoteReader] = None, sheet=None) -> None:
        """friends: FriendsController (for the picker). groups: callable that
        returns the StudyGroupService, or None while groups aren't set up."""
        super().__init__(notebook_controller.page)
        self._nb = notebook_controller
        self._home = notebook_controller.home
        self._service = service
        self._friends = friends
        self._groups = groups or (lambda: None)
        self._reader = reader or SharedNoteReader()
        self._sheet = sheet
        self._checked_at = 0.0
        self.installed = True

        notebook_controller.social_action.connect(self.handle)
        self._home.shared_shown.connect(self.show_received)
        self._home.shared_list.open_requested.connect(self.open)
        self._reader.save_requested.connect(self._save_copy)
        if sheet is not None:
            sheet.set_content(self._reader)
            sheet.close_requested.connect(sheet.close_sheet)

    # ----------------------------------------------------------- refresh

    def start(self) -> None:
        self.refresh()

    def refresh_if_stale(self) -> None:
        if time.monotonic() - self._checked_at > STALE_SECONDS:
            self.refresh()

    def refresh(self) -> None:
        """My shared notes (badges) and how many were shared with me."""
        self._checked_at = time.monotonic()

        def load():
            return self._service.shared_item_ids(), self._service.received()

        def done(data) -> None:
            ids, received = data
            self.installed = True
            self._home.shared_ids = ids
            self._home.rail.shared_count = len(received)
            self._nb.refresh_home()
            if self._home.filters.library == "shared":
                self._home.shared_list.show_notes(received)

        def failed(message: str) -> None:
            if is_not_installed(message):
                self.installed = False
                self._home.rail.shared_count = None      # the row stays hidden
                self._home.shared_ids = set()
                if self._home.filters.library == "shared":
                    self._home.filters.library = "all"
                self._nb.refresh_home()
        run(self._home, load, done, failed)

    def show_received(self) -> None:
        if not self.installed:
            self._home.shared_list.show_message(
                "Not set up yet", "Note sharing needs migration 041 on Akeso's server.", "database")
            return
        self._home.shared_list.show_loading()

        def done(notes: list[SharedNote]) -> None:
            self._home.rail.shared_count = len(notes)
            self._home.shared_list.show_notes(notes)
        run(self._home, self._service.received, done,
            lambda m: self._home.shared_list.show_message("Couldn't load shared notes", m, "share-2"))

    # ------------------------------------------------------------ receive

    def open(self, share_id: str) -> None:
        if self._sheet is not None:
            self._sheet.open_sheet()
            self._sheet.raise_()
            self._sheet.tab.raise_()
        self._reader.show_loading()

        def done(note: SharedNote) -> None:
            self._reader.show_note(note)
            if self._home.filters.library == "shared":
                QTimer.singleShot(0, self.show_received)      # "New" goes away
        run(self._reader, lambda: self._service.open(share_id), done, self._reader.show_error)

    def open_from_notification(self, share_id: str) -> None:
        self._home.filters.library = "shared"
        self._home.filters.subject_id = ""
        self._nb.refresh_home()
        self.open(share_id)

    def _save_copy(self, note: SharedNote) -> None:
        self._reader.save.setEnabled(False)
        who = f"@{note.owner.handle}" if note.owner.handle else note.owner.name

        def done(fresh: SharedNote) -> None:
            self._service.save_copy(fresh, who)          # local: on the UI thread
            self._reader.mark_saved(SHARED_SUBJECT)
            self._nb.refresh()
            self.notebook_changed.emit()

        def failed(message: str) -> None:
            self._reader.save.setEnabled(True)
            NoticeDialog("Couldn't save a copy", message, "circle-alert", parent=self._reader).exec()
        run(self._reader, lambda: self._service.fetch_copy(note.id), done, failed)

    # -------------------------------------------------------------- share

    def handle(self, action: str, item_id: str) -> None:
        if action == "manage_sharing":
            self.manage(item_id)
        else:
            self.share(item_id)

    def _notice(self, title: str, message: str, danger: bool = False) -> None:
        NoticeDialog(title, message, "circle-alert" if danger else "check",
                     danger=danger, parent=self._nb.page).exec()

    def share(self, item_id: str) -> None:
        if hasattr(self._nb, "pages"):
            self._nb.pages.save_note(item_id)            # share what is on screen now
        item = self._nb.service.get(item_id)
        if item is None:
            return
        if not self.installed:
            self._notice("Sharing isn't set up yet",
                         "Note sharing needs migration 041 on Akeso's server.", True)
            return
        try:
            snapshot(item)                               # patient-data check, before anything
        except ShareError as exc:
            self._notice("This note can't be shared", str(exc), True)
            return
        groups_service = self._groups()

        def load():
            friends = self._friends.load_friends_now()
            groups = []
            if groups_service is not None:
                try:
                    groups = groups_service.my_groups()
                except Exception:  # noqa: BLE001 - groups not set up: friends only
                    groups = []
            return friends, groups

        def ready(data) -> None:
            friends, groups = data
            dialog = ShareNoteDialog(item.title, friends, groups, parent=self._nb.page)

            def to_friends(ids: list) -> None:
                def done(count: int) -> None:
                    dialog.accept()
                    self.refresh()
                    self._notice("Shared", f"“{item.title}” is shared with {count} more "
                                 f"friend{'s' if count != 1 else ''}." if count else
                                 "They already had this note. Use Manage sharing to update "
                                 "their copy.")
                run(dialog, lambda: self._service.share(item_id, ids), done, dialog.show_error)

            def to_group(group_id: str) -> None:
                def done(_r) -> None:
                    dialog.accept()
                    self._notice("Shared", f"“{item.title}” is on the group's Shared notes shelf.")
                run(dialog, lambda: groups_service.share_note(group_id, item), done,
                    dialog.show_error)
            dialog.share_friends.connect(to_friends)
            dialog.share_group.connect(to_group)
            dialog.exec()

        run(self._nb.page, load, ready,
            lambda m: self._notice("Couldn't load your friends", m, True))

    def manage(self, item_id: str) -> None:
        def ready(share: Optional[SharedNote]) -> None:
            if share is None:
                self._notice("Not shared", "This note isn't shared with anyone now.")
                self.refresh()
                return
            dialog = ManageSharingDialog(share, parent=self._nb.page)

            def unshare(person) -> None:
                who = person.name if person is not None else "everyone"
                confirm = ConfirmDialog(f"Unshare from {who}?", UNSHARE_NOTE, "Unshare",
                                        "x", danger=True, parent=dialog)
                if confirm.exec() != ConfirmDialog.DialogCode.Accepted:
                    return
                dialog.set_busy(True)

                def done(_r) -> None:
                    dialog.set_busy(False)
                    if person is None:
                        dialog.show_recipients([])
                    else:
                        share.recipients = [p for p in share.recipients if p.id != person.id]
                        dialog.show_recipients(share.recipients)
                    dialog.show_info("Unshared.")
                    self.refresh()
                run(dialog, lambda: self._service.unshare(share.id, person.id if person else None),
                    done, dialog.show_error)

            def update() -> None:
                if hasattr(self._nb, "pages"):
                    self._nb.pages.save_note(item_id)
                dialog.set_busy(True)

                def done(_r) -> None:
                    dialog.set_busy(False)
                    dialog.show_info("Shared copy updated. Recipients now see the note as it "
                                     "is now.")
                run(dialog, lambda: self._service.update_copy(share.id, item_id), done,
                    dialog.show_error)
            dialog.unshare_requested.connect(unshare)
            dialog.update_requested.connect(update)
            dialog.exec()
        run(self._nb.page, lambda: self._service.manage(item_id), ready,
            lambda m: self._notice("Couldn't load sharing", m, True))

    def refresh_theme(self) -> None:
        self._reader.refresh_theme()
