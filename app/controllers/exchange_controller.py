"""Wires Clinical Exchange (feed, post, composer, moderation) to its service.

Every request runs in the background (core/background.py); results come
back on the UI thread. Other modules are reached only through signals the
shell connects: opening an encyclopedia entry, starring a bookmark, saving
into the notebook.
"""

from typing import Callable, Optional

from PySide6.QtCore import QObject, Signal

from app.core.avatar_image import circle_pixmap
from app.core.background import call_in_background
from app.core.theme import Theme
from app.models.exchange import PROFILE_REPORT_REASONS, Draft, ModItem, PostDetail, Tag
from app.models.notebook import NOTE
from app.services.exchange_service import PAGE_SIZE, ExchangeService
from app.services.notebook_service import NotebookService
from app.ui.views.account.account_dialogs import ConfirmDialog
from app.ui.views.exchange.exchange_dialogs import (
    ComposerPanel, EditReplyDialog, ModerateDialog, ReportDialog, RevealDialog,
)
from app.ui.views.exchange.exchange_page import ExchangePage
from app.ui.components.page_sheet import PageSheet

EXCHANGE_KIND = "exchange"


class ExchangeController(QObject):
    open_reference = Signal(str, str)        # kind, id  -> encyclopedia
    bookmark_changed = Signal(str, str, bool)
    notebook_saved = Signal(str)             # notebook item id
    activity = Signal(str)                   # for study counters
    notifications_changed = Signal()
    post_requested = Signal(str)             # open a post on top of the current page (shell)
    edit_profile_requested = Signal()        # "Edit my profile" -> Account Settings

    def __init__(self, page: ExchangePage, service: ExchangeService,
                 notebook: Optional[NotebookService] = None,
                 is_bookmarked: Optional[Callable[[str, str], bool]] = None,
                 describe_interaction: Optional[Callable[[str, list, list], dict]] = None,
                 is_moderator: bool = False,
                 avatar_loader: Optional[Callable[[str], Optional[bytes]]] = None) -> None:
        super().__init__(page)
        self._page = page
        self._avatar_loader = avatar_loader          # storage path -> PNG bytes
        self._profile_sheet = None
        self.profile_view = None
        self.before_profile_open: Optional[Callable[[], None]] = None   # the shell lends the sheet
        self._service = service
        self._notebook = notebook
        self._is_bookmarked = is_bookmarked or (lambda _k, _i: False)
        self._describe = describe_interaction
        self._is_mod = is_moderator
        self._tab = "newest"
        self._offset = 0
        self._loaded_once = False
        self._post_id: Optional[str] = None
        self._composer: Optional[ComposerPanel] = None
        self._sheet: Optional[PageSheet] = None

        feed = page.feed
        feed.tab_changed.connect(self._on_tab)
        feed.filters_changed.connect(self.reload_feed)
        feed.refresh_requested.connect(self.reload_feed)
        feed.load_more_requested.connect(self._load_more)
        feed.open_requested.connect(self.open_post)
        feed.new_post_requested.connect(lambda kind: self.new_post(Draft(kind=kind)))
        feed.queue_requested.connect(self.open_queue)
        feed.profile_requested.connect(self.show_profile)

        post = page.post
        post.back_requested.connect(self.back_to_feed)
        post.refresh_requested.connect(lambda: self._load_post(keep_scroll=True))
        post.post_action.connect(self._on_post_action)
        post.reply_action.connect(self._on_reply_action)
        post.reply_upvote.connect(self._on_reply_upvote)
        post.reply_submitted.connect(self._on_reply)
        post.option_comment.connect(self._on_option_comment)
        post.poll_vote.connect(self._on_poll_vote)
        post.poll_suggest.connect(self._on_poll_suggest)
        post.poll_reveal.connect(self._on_reveal)
        post.tag_opened.connect(lambda tag: self.open_reference.emit(tag.kind, tag.id))
        post.profile_requested.connect(self.show_profile)
        post.checker = lambda text: service.check_text(text)

        queue = page.queue
        queue.back_requested.connect(self.back_to_feed)
        queue.refresh_requested.connect(self.open_queue)
        queue.item_action.connect(self._on_queue_action)

        self._load_reference()
        feed.set_moderator(is_moderator)

    # ---------------------------------------------------------- plumbing

    def _run(self, call, on_done=None, on_error=None) -> None:
        call_in_background(call, on_done, on_error or self._error, owner=self._page)

    def _error(self, message: str) -> None:
        view = self._page.current_view()
        banner = getattr(view, "banner", None)
        if banner is not None:
            banner.show_message(message, "danger", "Dismiss")

    def _notice(self, message: str, tone: str = "good") -> None:
        banner = getattr(self._page.current_view(), "banner", None)
        if banner is not None:
            banner.show_message(message, tone, "Dismiss")

    def _load_reference(self) -> None:
        reference = self._service.reference
        self._page.feed.set_reference(reference.tag_options(), reference.body_systems())
        self._page.post.diseases = reference.diseases()

    def on_shown(self) -> None:
        """The shell calls this when the tab is opened."""
        if not self._loaded_once:
            self._load_reference()
            self.reload_feed()

    # -------------------------------------------------------------- feed

    def _on_tab(self, tab: str) -> None:
        self._tab = tab
        self.reload_feed()

    def reload_feed(self) -> None:
        self._loaded_once = True
        self._offset = 0
        self._page.feed.show_loading()
        filters = self._page.feed.filters()
        self._run(lambda: self._service.feed(self._tab, **filters),
                  lambda posts: self._page.feed.show_posts(posts, False, len(posts) >= PAGE_SIZE),
                  self._page.feed.show_error)
        if self._is_mod:
            self._run(self._service.mod_queue,
                      lambda items: self._page.feed.set_moderator(True, len(items)),
                      lambda _m: None)

    def _load_more(self) -> None:
        self._offset += PAGE_SIZE
        filters = self._page.feed.filters()
        offset = self._offset
        self._run(lambda: self._service.feed(self._tab, offset=offset, **filters),
                  lambda posts: self._page.feed.show_posts(posts, True, len(posts) >= PAGE_SIZE))

    def back_to_feed(self) -> None:
        self._page.show_feed()
        self.reload_feed()

    def filter_by_tag(self, tag: Tag) -> None:
        self._page.show_feed()
        self._page.feed.set_tag(tag)

    # -------------------------------------------------------------- post

    def open_post(self, post_id: str) -> None:
        self._post_id = post_id
        self._page.show_post()
        self._page.post.show_loading()
        self._load_post()

    def _load_post(self, keep_scroll: bool = False, then: Optional[Callable] = None) -> None:
        post_id = self._post_id
        if not post_id:
            return

        def done(post: PostDetail) -> None:
            self._page.post.show_post(post, self._is_bookmarked(EXCHANGE_KIND, post.id),
                                      keep_scroll)
            if then:
                then()
        self._run(lambda: self._service.post(post_id), done, self._page.post.show_error)

    @property
    def _post(self) -> Optional[PostDetail]:
        return self._page.post.post

    def _on_post_action(self, action: str) -> None:
        post = self._post
        if post is None:
            return
        if action in ("upvote", "unvote"):
            self._run(lambda: self._service.vote("post", post.id, action == "upvote"),
                      lambda _s: self._load_post(True))
        elif action in ("follow", "unfollow"):
            self._run(lambda: self._service.follow(post.id, action == "follow"),
                      lambda _r: self._load_post(True))
        elif action in ("bookmark", "unbookmark"):
            self.bookmark_changed.emit(EXCHANGE_KIND, post.id, action == "bookmark")
            self._page.post.show_post(post, action == "bookmark", keep_scroll=True)
        elif action == "notebook":
            self._save_to_notebook(post)
        elif action == "report":
            self._report("post", post.id)
        elif action == "edit":
            self._edit_post(post)
        elif action == "delete":
            dialog = ConfirmDialog("Delete this post?", "The post, its poll and every reply on "
                                   "it are deleted for good.", "Delete", "trash-2", danger=True,
                                   parent=self._page)
            if dialog.exec() == ConfirmDialog.DialogCode.Accepted:
                self._run(lambda: self._service.delete(post.id), lambda _r: self.back_to_feed())
        elif action == "moderate":
            self._moderate("post", post.id, post.status)

    def _save_to_notebook(self, post: PostDetail) -> None:
        if self._notebook is None:
            return
        title, html = self._service.notebook_copy(post)
        item = self._notebook.create_note(base=f"Exchange: {title}"[:80])
        self._notebook.save_body(item.id, f"<html><body>{html}</body></html>")
        self.notebook_saved.emit(item.id)
        self._notice("Saved to your Study Notebook.")

    def _edit_post(self, post: PostDetail) -> None:
        draft = Draft(kind=post.kind, title=post.title, body=post.body, question=post.question,
                      tags=list(post.tags))
        panel = ComposerPanel(draft, self._service.reference.tag_options(),
                              self._service.reference.diseases(), [], self._composer_check,
                              editing=True)

        def saved(_r) -> None:
            self._close_composer(force=True)
            self._load_post(True)

        panel.submitted.connect(lambda edited: self._run(
            lambda: self._service.edit(post, edited.title, edited.body, edited.question,
                                       edited.tags),
            saved, panel.show_error))
        self._show_composer(panel)

    # ----------------------------------------------------------- replies

    def _on_reply(self, parent_id: Optional[str], body: str, anonymous: bool) -> None:
        post = self._post
        if post is None:
            return
        box = self._page.post.box_for(parent_id)

        def done(_reply_id) -> None:
            if box is not None:
                box.done()
            self.activity.emit("reply")
            self._load_post(True)

        def failed(message: str) -> None:
            if box is not None:
                box.failed(message)
            else:
                self._error(message)
        self._run(lambda: self._service.reply(post.id, parent_id, body, anonymous), done, failed)

    def _on_option_comment(self, option_id: str, body: str, anonymous: bool) -> None:
        post = self._post
        if post is None:
            return
        box = self._page.post.option_box(option_id)

        def done(_reply_id) -> None:
            if box is not None:
                box.done()
            self.activity.emit("reply")
            self._load_post(True)

        def failed(message: str) -> None:
            if box is not None:
                box.failed(message)
            else:
                self._error(message)
        self._run(lambda: self._service.option_comment(post.id, option_id, body, anonymous),
                  done, failed)

    def _on_reply_upvote(self, reply_id: str, on: bool) -> None:
        self._run(lambda: self._service.vote("reply", reply_id, on), lambda _s: self._load_post(True))

    def _on_reply_action(self, action: str, reply_id: str) -> None:
        post = self._post
        if post is None:
            return
        reply = next((r for r in post.all_replies() if r.id == reply_id), None)
        if action in ("best", "unbest"):
            self._run(lambda: self._service.best_answer(post.id, reply_id if action == "best" else None),
                      lambda _r: self._load_post(True))
        elif action in ("verify", "unverify"):
            self._run(lambda: self._service.verify(reply_id, action == "verify"),
                      lambda _r: self._load_post(True))
        elif action == "edit" and reply is not None:
            dialog = EditReplyDialog(reply.body, parent=self._page)
            dialog.submitted.connect(lambda body: self._run(
                lambda: self._service.edit_reply(reply_id, body),
                lambda _r: (dialog.accept(), self._load_post(True)), dialog.show_error))
            dialog.exec()
        elif action == "delete":
            dialog = ConfirmDialog("Delete this reply?", "It can't be brought back.", "Delete",
                                   "trash-2", danger=True, parent=self._page)
            if dialog.exec() == ConfirmDialog.DialogCode.Accepted:
                self._run(lambda: self._service.delete_reply(reply_id), lambda _r: self._load_post(True))
        elif action == "report":
            self._report("reply", reply_id)
        elif action == "moderate" and reply is not None:
            self._moderate("reply", reply_id, reply.status)

    # -------------------------------------------------------------- poll

    def _on_poll_vote(self, option_id: str) -> None:
        post = self._post
        if post is None:
            return
        self._run(lambda: self._service.poll_vote(post.id, option_id or None),
                  lambda _r: self._load_post(True))

    def _on_poll_suggest(self, disease_id, label: str) -> None:
        post = self._post
        if post is None:
            return

        def done(option_id: str) -> None:
            # Suggesting is a vote for it too, unless you wrote the case.
            if not post.is_author and option_id:
                self._on_poll_vote(option_id)
            else:
                self._load_post(True)
        self._run(lambda: self._service.suggest(post.id, disease_id, label), done)

    def _on_reveal(self) -> None:
        post = self._post
        if post is None or post.poll is None:
            return
        dialog = RevealDialog(post.poll, parent=self._page)
        dialog.submitted.connect(lambda option_id, explanation: self._run(
            lambda: self._service.reveal(post.id, option_id, explanation),
            lambda _r: (dialog.accept(), self._load_post(True)), dialog.show_error))
        dialog.exec()

    # -------------------------------------------------------- moderation

    def _report(self, kind: str, target_id: str) -> None:
        reasons = PROFILE_REPORT_REASONS if kind == "profile" else None
        dialog = ReportDialog(kind, parent=self._page, reasons=reasons)

        def done(_r) -> None:
            dialog.accept()
            if kind == "profile" and self.profile_view is not None:
                self.profile_view.banner.show_message("Thanks. Moderators will review this "
                                                      "profile.", "good", "OK")
            else:
                self._notice("Thanks. Moderators will review it.")
        dialog.submitted.connect(lambda reason, note: self._run(
            lambda: self._service.report(kind, target_id, reason, note), done, dialog.show_error))
        dialog.exec()

    def _moderate(self, kind: str, target_id: str, status: str, after: Optional[Callable] = None) -> None:
        dialog = ModerateDialog(kind, status, parent=self._page)

        def done(_r) -> None:
            dialog.accept()
            (after or self._reload_after_moderation)()
        dialog.submitted.connect(lambda action, reason: self._run(
            lambda: self._service.moderate(kind, target_id, action, reason), done, dialog.show_error))
        dialog.exec()

    def _reload_after_moderation(self) -> None:
        """Hidden and removed posts are shown only to their author and admins
        (migration 010), so an educator who hides one can't reopen it: go back
        to the feed instead of showing "This post is not available"."""
        post_id = self._post_id
        if not post_id:
            return

        def done(post: PostDetail) -> None:
            self._page.post.show_post(post, self._is_bookmarked(EXCHANGE_KIND, post.id), True)

        def gone(_message: str) -> None:
            self.back_to_feed()
            self._notice("Done. Hidden and removed posts are visible only to their author "
                         "and admins.")
        self._run(lambda: self._service.post(post_id), done, gone)

    def open_queue(self) -> None:
        self._page.show_queue()
        self._run(self._service.mod_queue, self._page.queue.show_items, self._page.queue.show_error)

    def _on_queue_action(self, action: str, item: ModItem) -> None:
        if action == "open" and item.target_kind == "profile":
            if item.handle:
                self.show_profile(item.handle)
        elif action == "open" and item.post_id:
            self.open_post(item.post_id)
        elif action == "dismiss":
            self._run(lambda: self._service.dismiss(item.target_kind, item.target_id),
                      lambda _r: self.open_queue())
        elif action in ("hide", "lock", "remove", "make_private", "clear_bio"):
            dialog = ModerateDialog(item.target_kind, item.status, parent=self._page)
            dialog.action.setCurrentIndex(max(0, dialog.action.findData(action)))
            dialog.submitted.connect(lambda chosen, reason: self._run(
                lambda: self._service.moderate(item.target_kind, item.target_id, chosen, reason),
                lambda _r: (dialog.accept(), self.open_queue()), dialog.show_error))
            dialog.exec()

    # ----------------------------------------------------------- profile

    def attach_profile_sheet(self, sheet, view) -> None:
        """The shell hands over a full-page sheet and the ProfileView in it."""
        self._profile_sheet = sheet
        self.profile_view = view
        sheet.set_content(view)
        sheet.close_requested.connect(sheet.close_sheet)
        view.follow_toggled.connect(self._follow_user)
        view.report_requested.connect(lambda p: self._report("profile", p.id))
        view.moderate_requested.connect(self._moderate_profile)
        view.post_requested.connect(self.post_requested.emit)
        view.topic_requested.connect(lambda tag: self.open_reference.emit(tag.kind, tag.id))
        view.edit_requested.connect(self._edit_own_profile)

    def show_profile(self, handle: str) -> None:
        """A member's profile, on top of whatever is open (a post, the feed...)."""
        if not handle:
            return
        if self.profile_view is None:                  # outside the shell (tests)
            self._run(lambda: self._service.profile(handle), lambda p: None)
            return
        view, sheet = self.profile_view, self._profile_sheet
        if self.before_profile_open is not None:
            self.before_profile_open()
        view.show_loading()
        sheet.open_sheet()
        sheet.raise_()
        sheet.tab.raise_()

        def done(profile) -> None:
            initials = circle_pixmap(None, 88, profile.display_name or profile.handle,
                                     Theme.token("PRIMARY"), "#FFFFFF")
            view.show_profile(profile, initials)
            if profile.avatar_path and self._avatar_loader is not None:
                path = profile.avatar_path
                call_in_background(lambda: self._avatar_loader(path),
                                   lambda png: png and view.profile is profile and view.set_avatar(
                                       circle_pixmap(png, 88, profile.display_name,
                                                     Theme.token("PRIMARY"), "#FFFFFF")),
                                   lambda _m: None, owner=view)
        self._run(lambda: self._service.profile(handle), done, view.show_error)

    def _follow_user(self, handle: str, on: bool) -> None:
        view = self.profile_view
        profile = view.profile if view else None
        if profile is None:
            return

        def done(_r) -> None:
            if view.profile is profile:
                view.set_following(on, max(0, profile.followers + (1 if on else -1)))
        self._run(lambda: self._service.follow_user(handle, on), done,
                  lambda m: view.banner.show_message(m, "danger", "OK"))

    def _moderate_profile(self, profile) -> None:
        dialog = ModerateDialog("profile", profile.visibility, parent=self._page)

        def done(_r) -> None:
            dialog.accept()
            self.show_profile(profile.handle)
        dialog.submitted.connect(lambda action, reason: self._run(
            lambda: self._service.moderate("profile", profile.id, action, reason), done,
            dialog.show_error))
        dialog.exec()

    def _edit_own_profile(self) -> None:
        if self._profile_sheet is not None:
            self._profile_sheet.close_sheet()
        self.edit_profile_requested.emit()

    # ---------------------------------------------------------- composing

    def _composer_check(self, title: str, body: str, question: str) -> Optional[str]:
        return self._service.check_text(title, body, question)

    def _notebook_cases(self) -> list[tuple[str, str]]:
        if self._notebook is None:
            return []
        return [(item.id, item.title) for item in self._notebook.items()
                if item.kind != NOTE or item.has_case_data]

    def new_post(self, draft: Draft) -> None:
        panel = ComposerPanel(draft, self._service.reference.tag_options(),
                              self._service.reference.diseases(), self._notebook_cases(),
                              self._composer_check)

        def attach(item_id: str) -> None:
            item = self._notebook.get(item_id) if self._notebook else None
            if item is not None:
                panel.fill(self._service.draft_from_notebook(item, self._describe))

        def posted(post_id: str) -> None:
            self._close_composer(force=True)
            self.activity.emit("post")
            self.open_post(post_id)

        panel.attach_requested.connect(attach)
        panel.submitted.connect(lambda d: self._run(lambda: self._service.create(d), posted,
                                                    panel.show_error))
        self._show_composer(panel)

    # The composer is a full-page sheet over the content area, not a dialog,
    # so nothing here blocks: answers come back through the panel's signals.

    def attach_sheet(self, sheet: PageSheet) -> None:
        """The shell hands over the sheet that covers its content area."""
        self._sheet = sheet
        sheet.close_requested.connect(self._close_composer)
        sheet.closed.connect(self._composer_gone)
        sheet.opened.connect(lambda: self._composer.focus_first() if self._composer else None)

    def _ensure_sheet(self) -> PageSheet:
        if self._sheet is None:                 # not inside the shell (tests, previews)
            self.attach_sheet(PageSheet(self._page, self._page))
        return self._sheet

    def _show_composer(self, panel: ComposerPanel) -> None:
        if self._composer is not None and not self._close_composer():
            panel.deleteLater()                 # kept the post already being written
            return
        sheet = self._ensure_sheet()
        panel.cancel_requested.connect(self._close_composer)
        self._composer = panel
        sheet.set_content(panel)
        sheet.open_sheet()

    def _close_composer(self, force: bool = False) -> bool:
        """Close the composer; ask first if it holds unsaved work.
        Returns False if the user chose to keep writing."""
        panel = self._composer
        if panel is None:
            return True
        if not force and panel.busy:            # still posting: let it finish
            return False
        if not force and panel.is_dirty():
            dialog = ConfirmDialog("Discard this post?",
                                   "What you have written here will be lost.",
                                   "Discard", "trash-2", danger=True, parent=self._page)
            if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
                return False
        self._composer = None
        if self._sheet is not None:
            self._sheet.close_sheet()
        return True

    def _composer_gone(self) -> None:
        if self._sheet is not None and self._sheet.content is None:
            self._composer = None

    def present_case(self, kind: str, entry_id: str) -> None:
        """ "Present Case" from a disease, symptom or medicine page."""
        self._page.show_feed()
        self.new_post(self._service.draft_for_tag(kind, entry_id))

    def share_notebook_item(self, item_id: str) -> None:
        item = self._notebook.get(item_id) if self._notebook else None
        if item is not None:
            self._page.show_feed()
            self.new_post(self._service.draft_from_notebook(item, self._describe))
