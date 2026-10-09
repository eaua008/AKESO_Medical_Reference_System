"""Admin > Announcements: list, write, edit, preview and end announcements.

Every request runs in the background. The database refuses non-admins
whatever this screen shows (migration 015).
"""

from PySide6.QtCore import QObject

from app.core.background import call_in_background
from app.models.announcement import AUDIENCE_LABELS, Announcement, check
from app.repositories.announcement_repository import AnnouncementRepository
from app.ui.views.account.account_dialogs import ConfirmDialog
from app.ui.views.admin.announcements_view import AnnouncementEditor, AnnouncementsAdminView
from app.ui.views.announcement_widgets import AnnouncementDialog


class AnnouncementAdminController(QObject):
    def __init__(self, view: AnnouncementsAdminView, repository: AnnouncementRepository) -> None:
        super().__init__(view)
        self._view = view
        self._repo = repository
        self._loaded = False
        view.refresh_requested.connect(self.reload)
        view.new_requested.connect(lambda: self._open_editor(None))
        view.edit_requested.connect(self._open_editor)
        view.preview_requested.connect(self._preview)
        view.end_requested.connect(self._end)

    def shown(self) -> None:
        if not self._loaded:
            self.reload()

    def reload(self) -> None:
        self._loaded = True
        call_in_background(self._repo.all, self._view.show_items, self._view.show_error,
                           owner=self._view)

    # ------------------------------------------------------------ private

    def _preview(self, item: Announcement, parent=None) -> None:
        AnnouncementDialog(item, parent=parent or self._view, preview=True).exec()

    def _open_editor(self, item) -> None:
        editor = AnnouncementEditor(item, parent=self._view)
        editor.preview_requested.connect(lambda a: self._preview(a, editor))

        def save(value: Announcement, reshow: bool) -> None:
            problem = check(value)
            if problem:
                editor.show_error(problem)
                return
            editor.set_busy(True)

            def done(_id) -> None:
                editor.accept()
                who = AUDIENCE_LABELS[value.audience].lower()
                if item is None:
                    status = value.status()
                    self._view.show_notice(
                        f"“{value.title}” is scheduled for "
                        f"{value.starts_at.astimezone():%b %d, %I:%M %p}." if status == "scheduled"
                        else f"“{value.title}” is published. {who.capitalize()} "
                             "will see it the next time they open the dashboard.")
                else:
                    self._view.show_notice(f"“{value.title}” is saved."
                                           + (" It pops up again for everyone." if reshow
                                              else ""))
                self.reload()
            call_in_background(lambda: self._repo.save(value, reshow), done,
                               editor.show_error, owner=editor)

        editor.submitted.connect(save)
        editor.exec()

    def _end(self, item: Announcement) -> None:
        dialog = ConfirmDialog(
            "End announcement",
            f"“{item.title}” stops popping up and leaves everyone's dashboard now. "
            "It stays in this list.", "End now", "x", danger=True, parent=self._view)
        if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
            return
        call_in_background(lambda: self._repo.end(item.id),
                           lambda _r: (self._view.show_notice(f"“{item.title}” has ended."),
                                       self.reload()),
                           self._view.show_error, owner=self._view)
