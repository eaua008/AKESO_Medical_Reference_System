"""Wires the Admin Control Panel (User Management, Content Management)
to AdminService.

Every request runs in the background (core/background.py). Editors open in
the shell's slide-in sheet, like the Clinical Exchange composer. After a
content change, content_changed tells the shell to refresh the
encyclopedias straight away instead of waiting for the next sync.
"""

from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.core.background import call_in_background
from app.models.admin import KIND_LABELS, KINDS, AdminUser
from app.services.admin_service import AdminService
from app.ui.components.page_sheet import PageSheet
from app.ui.views.account.account_dialogs import ConfirmDialog
from app.ui.views.admin.admin_dialogs import (
    DeleteUserDialog, RoleDialog, SuspendDialog, UserDetailDialog,
)
from app.ui.views.admin.content_editor import ContentEditor
from app.ui.views.admin.content_view import ContentManagementView
from app.ui.views.admin.users_view import UserManagementView


class AdminController(QObject):
    content_changed = Signal(str)       # kind
    my_role_changed = Signal(str)       # you changed your own role

    def __init__(self, users_view: UserManagementView, content_view: ContentManagementView,
                 service: AdminService) -> None:
        super().__init__(users_view)
        self._users_view = users_view
        self._content_view = content_view
        self._service = service
        self._sheet: Optional[PageSheet] = None
        self._editor: Optional[ContentEditor] = None
        self._users_loaded = False
        self._content_loaded = False

        users_view.refresh_requested.connect(self.reload_users)
        users_view.view_requested.connect(self._view_user)
        users_view.role_requested.connect(self._change_role)
        users_view.suspend_requested.connect(self._toggle_suspend)
        users_view.delete_requested.connect(self._delete_user)

        content_view.refresh_requested.connect(self.reload_content)
        content_view.add_requested.connect(self._add)
        content_view.edit_requested.connect(self._edit)
        content_view.publish_requested.connect(self._set_published)
        content_view.audit_requested.connect(self._load_audit)

    def _run(self, call, on_done=None, on_error=None, owner=None) -> None:
        call_in_background(call, on_done, on_error, owner=owner or self._users_view)

    # The shell calls these when the tabs are opened.
    def users_shown(self) -> None:
        if not self._users_loaded:
            self.reload_users()

    def content_shown(self) -> None:
        if not self._content_loaded:
            self.reload_content()

    # ------------------------------------------------------------ accounts

    def reload_users(self) -> None:
        self._users_loaded = True
        self._run(self._service.users, self._users_view.show_users,
                  self._users_view.show_error)

    def _view_user(self, user: AdminUser) -> None:
        def done(detail) -> None:
            UserDetailDialog(detail, parent=self._users_view).exec()
        self._run(lambda: self._service.user_detail(user.id), done, self._users_view.show_error)

    def _change_role(self, user: AdminUser) -> None:
        dialog = RoleDialog(user, parent=self._users_view)

        def save(role: str) -> None:
            dialog.set_busy(True)

            def done(_r) -> None:
                dialog.accept()
                self._users_view.show_notice(
                    f"{user.display_name} is now {'an' if role in ('admin', 'educator') else 'a'} "
                    f"{dict(admin='Administrator', educator='Educator', student='Student')[role]}. "
                    "They see the change the next time they sign in.")
                self.reload_users()
                if user.is_me:
                    self.my_role_changed.emit(role)
            self._run(lambda: self._service.set_role(user.id, role), done, dialog.show_error)
        dialog.submitted.connect(save)
        dialog.exec()

    def _toggle_suspend(self, user: AdminUser) -> None:
        if user.suspended:
            confirm = ConfirmDialog("Reactivate account",
                                    f"{user.display_name} ({user.email}) will be able to sign "
                                    "in again.", "Reactivate", "user-check",
                                    parent=self._users_view)
            if confirm.exec() != ConfirmDialog.DialogCode.Accepted:
                return
            self._run(lambda: self._service.set_suspended(user.id, False),
                      lambda _r: (self._users_view.show_notice(
                          f"{user.display_name}'s account is active again."), self.reload_users()),
                      self._users_view.show_error)
            return
        dialog = SuspendDialog(user, parent=self._users_view)

        def suspend(reason: str) -> None:
            dialog.set_busy(True)

            def done(_r) -> None:
                dialog.accept()
                self._users_view.show_notice(f"{user.display_name}'s account is suspended.")
                self.reload_users()
            self._run(lambda: self._service.set_suspended(user.id, True, reason), done,
                      dialog.show_error)
        dialog.submitted.connect(suspend)
        dialog.exec()

    def _delete_user(self, user: AdminUser) -> None:
        dialog = DeleteUserDialog(user, parent=self._users_view)

        def delete(confirm: str) -> None:
            dialog.set_busy(True)

            def done(result: str) -> None:
                dialog.accept()
                self._users_view.show_notice(
                    f"{user.email} was deleted." if result == "deleted" else
                    f"{user.email} is scheduled for deletion (the deletion job removes it).")
                self.reload_users()
            self._run(lambda: self._service.delete_user(user.id, confirm), done,
                      dialog.show_error)
        dialog.submitted.connect(delete)
        dialog.exec()

    # ------------------------------------------------------------- content

    def reload_content(self) -> None:
        self._content_loaded = True
        view = self._content_view

        def load():
            return self._service.body_systems(), self._service.all_content()

        def done(result) -> None:
            systems, items = result
            view.set_body_systems(systems)
            view.show_content(items)
        self._run(load, done, view.show_error, owner=view)
        self._load_audit()

    def _load_audit(self) -> None:
        self._run(lambda: self._service.audit(200),
                  lambda result: self._content_view.show_audit(*result),
                  self._content_view.show_error, owner=self._content_view)

    def _set_published(self, kind: str, entry_id: str, published: bool) -> None:
        item = next((i for i in self._content_view.items(kind) if i.id == entry_id), None)
        name = item.name if item else entry_id
        if not published:
            dialog = ConfirmDialog(
                f"Archive {KIND_LABELS[kind].lower()}",
                (f"“{name}” will be hidden from Health Articles, related-article lists "
                 "and search. Nothing is deleted: you can restore it from here at any time."
                 if kind == "article" else
                 f"“{name}” will be hidden from the encyclopedias, checkers and search on "
                 "every computer after its next sync. Nothing is deleted: you can restore "
                 "it from here at any time."), "Archive", "archive", danger=True,
                parent=self._content_view)
            if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
                return

        def done(_r) -> None:
            self._content_view.show_notice(
                f"“{name}” is {'restored' if published else 'archived'}.")
            self.reload_content()
            self.content_changed.emit(kind)
        self._run(lambda: self._service.set_published(kind, entry_id, published), done,
                  self._content_view.show_error, owner=self._content_view)

    # -------------------------------------------------------------- editor

    def attach_sheet(self, sheet: PageSheet) -> None:
        self._sheet = sheet
        sheet.close_requested.connect(self._close_editor)
        sheet.opened.connect(lambda: self._editor.focus_first() if self._editor else None)

    def _choices(self) -> tuple[list, list, list]:
        view = self._content_view
        names = {kind: sorted(((i.id, i.name) for i in view.items(kind)), key=lambda p: p[1].lower())
                 for kind in KINDS}
        return names["symptom"], names["medicine"], names["disease"]

    def _open_editor(self, kind: str, data: dict, is_new: bool) -> None:
        if self._editor is not None and not self._close_editor():
            return
        symptoms, medicines, diseases = self._choices()
        editor = ContentEditor(kind, data, is_new, self._content_view.body_systems(),
                               symptoms, medicines, diseases)
        editor.cancel_requested.connect(self._close_editor)
        editor.submitted.connect(lambda d, e=editor: self._save(e, d))
        self._editor = editor
        if self._sheet is None:          # outside the shell (tests): a plain sheet
            self.attach_sheet(PageSheet(self._content_view, self._content_view))
        self._sheet.set_content(editor)
        self._sheet.open_sheet()

    def _add(self, kind: str) -> None:
        self._open_editor(kind, {}, True)

    def _edit(self, kind: str, entry_id: str) -> None:
        self._run(lambda: self._service.entry(kind, entry_id),
                  lambda data: self._open_editor(kind, data, False),
                  self._content_view.show_error, owner=self._content_view)

    def _save(self, editor: ContentEditor, data: dict) -> None:
        existing = {i.id for i in self._content_view.items(editor.kind)}
        problem = self._service.check_entry(editor.kind, data, editor.is_new, existing)
        if problem:
            editor.show_error(problem)
            return

        def done(entry_id: str) -> None:
            self._close_editor(force=True)
            self._content_view.show_notice(
                f"“{data['name']}” is {'created' if editor.is_new else 'saved'}. "
                "Users get it on their next sync.")
            self.reload_content()
            self.content_changed.emit(editor.kind)
        self._run(lambda: self._service.save(editor.kind, data, editor.is_new), done,
                  editor.show_error, owner=editor)

    def _close_editor(self, force: bool = False) -> bool:
        editor = self._editor
        if editor is None:
            return True
        if not force and editor.busy:
            return False
        if not force and editor.is_dirty():
            dialog = ConfirmDialog("Discard changes?",
                                   "What you changed in this entry will be lost.",
                                   "Discard", "trash-2", danger=True, parent=self._content_view)
            if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
                return False
        self._editor = None
        if self._sheet is not None:
            self._sheet.close_sheet()
        return True
