"""Community > Friends, and the Add friend / Block buttons on member profiles.

Friends are mutual (migration 040). A handle that matches nobody is reported
under the box ("No user with the handle ..."), added in migration 047; someone
who blocked the sender still reads as "sent".
"""

from typing import Optional

from PySide6.QtCore import QObject, QTimer, Signal

from app.controllers.social_common import is_not_installed, run
from app.models.social import Friend
from app.services.friends_service import FriendsService
from app.ui.views.account.account_dialogs import ConfirmDialog
from app.ui.views.social.friends_view import FriendsView


class FriendsController(QObject):
    friends_changed = Signal()                # other screens (share, invites) refresh
    profile_requested = Signal(str)           # handle -> open the member profile
    unavailable = Signal(str)                 # migration 040 not run (message)

    def __init__(self, view: FriendsView, service: FriendsService) -> None:
        super().__init__(view)
        self._view = view
        self._service = service
        self._friends: list[Friend] = []
        self._loaded = False
        self.installed = True

        view.refresh_requested.connect(self.reload)
        view.add_requested.connect(self._add)
        view.respond_requested.connect(self._respond)
        view.cancel_requested.connect(lambda rid: self._act(lambda: service.cancel(rid)))
        view.unfriend_requested.connect(self._unfriend)
        view.block_requested.connect(self._block)
        view.unblock_requested.connect(lambda p: self._act(lambda: service.unblock(p.id),
                                                           f"Unblocked {p.name}."))
        view.profile_requested.connect(self.profile_requested.emit)

    # ------------------------------------------------------------ loading

    def on_shown(self) -> None:
        self.reload(quiet=self._loaded)

    def reload(self, quiet: bool = False) -> None:
        if not quiet:
            self._view.show_loading("Loading your friends…")

        def done(data) -> None:
            friends, requests, blocked = data
            self._friends = friends
            self._loaded = True
            self.installed = True
            self._view.show_data(friends, requests, blocked)
        run(self._view, self._service.overview, done, self._failed)

    def _failed(self, message: str) -> None:
        self._view.set_busy(False)
        if is_not_installed(message):
            self.installed = False
            self._view.show_not_installed(message)
            self.unavailable.emit(message)
            return
        self._view.banner.show_message(message, "danger", "Dismiss")

    @property
    def friends(self) -> list[Friend]:
        return self._friends

    def load_friends_now(self) -> list[Friend]:
        """The friends list, fetched now (call it from a background job)."""
        self._friends = self._service.friends()
        return self._friends

    def load_friends(self, then) -> None:
        """For other screens (share dialog, group invites): fresh list, then(friends)."""
        def done(friends) -> None:
            self._friends = friends
            then(friends)
        run(self._view, self._service.friends, done,
            lambda m: then(None if is_not_installed(m) else self._friends))

    # ------------------------------------------------------------ actions

    def _act(self, call, notice: str = "") -> None:
        def done(_r) -> None:
            if notice:
                self._view.banner.show_message(notice, "good", "OK")
            self.friends_changed.emit()
            self.reload(quiet=True)
        run(self._view, call, done, self._failed)

    def _add(self, handle: str) -> None:
        self._view.set_busy(True)

        def done(status: str) -> None:
            self._view.request_sent()
            if status == "accepted":
                self._view.banner.show_message("You're now friends: they had already asked you.",
                                               "good", "OK")
            else:
                self._view.banner.show_message(
                    "Request sent. They'll see it under Friends → Requests.", "good", "OK")
            self.friends_changed.emit()
            self.reload(quiet=True)

        def failed(message: str) -> None:
            # Mistakes in the handle belong next to the box; anything else is a banner.
            if is_not_installed(message) or "Slow down" in message:
                self._failed(message)
            else:
                self._view.show_handle_error(message)

        run(self._view, lambda: self._service.request(handle), done, failed)

    def _respond(self, user_id: str, accept: bool) -> None:
        self._act(lambda: self._service.respond(user_id, accept),
                  "You're now friends." if accept else "Request declined. They aren't told.")

    def _unfriend(self, person) -> None:
        dialog = ConfirmDialog(f"Unfriend {person.name}?",
                               "They aren't told. Notes you shared with each other stop being "
                               "available to the other (copies already saved stay).",
                               "Unfriend", "user-x", danger=True, parent=self._view)
        if dialog.exec() == ConfirmDialog.DialogCode.Accepted:
            self._act(lambda: self._service.remove(person.id), f"Unfriended {person.name}.")

    def _block(self, person) -> None:
        if self.confirm_block(person.name):
            self._act(lambda: self._service.block(person.id), f"Blocked {person.name}.")

    def confirm_block(self, name: str) -> bool:
        dialog = ConfirmDialog(f"Block {name}?",
                               "They can't send you friend requests, shared notes or group "
                               "invites, and you won't show up when they look for friends. Any "
                               "friendship ends and shares between you stop. If you're in the "
                               "same study group, messages stay. They aren't told.",
                               "Block", "user-x", danger=True, parent=self._view)
        return dialog.exec() == ConfirmDialog.DialogCode.Accepted

    # ------------------------------------------------------ member profiles

    def attach_profile(self, profile_view) -> None:
        """The member profile sheet (Clinical Exchange) gets Add friend / Block."""
        self._profile_view = profile_view
        profile_view.friend_action.connect(self._profile_action)

    def profile_shown(self, profile) -> None:
        view = getattr(self, "_profile_view", None)
        if view is None or profile.is_me or not self.installed:
            return

        def done(state: str, tries: int = 0) -> None:
            # The profile view holds its loader for a moment (LoadingHold):
            # wait until this profile is actually on screen.
            if view.profile is profile:
                view.set_friend_state(state)
            elif tries < 20:
                QTimer.singleShot(250, lambda: done(state, tries + 1))
        run(view, lambda: self._service.status(profile.handle), done, lambda _m: None)

    def _profile_action(self, action: str, profile) -> None:
        view = self._profile_view
        if action == "block" and not self.confirm_block(profile.display_name):
            return
        if action == "unfriend":
            dialog = ConfirmDialog(f"Unfriend {profile.display_name}?",
                                   "They aren't told. Shared notes between you stop being "
                                   "available.", "Unfriend", "user-x", danger=True, parent=view)
            if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
                return
        calls = {
            "request": lambda: self._service.request(profile.handle),
            "accept": lambda: self._service.respond(profile.id, True),
            "unfriend": lambda: self._service.remove(profile.id),
            "block": lambda: self._service.block(profile.id),
            "unblock": lambda: self._service.unblock(profile.id),
        }
        notices = {"request": "Friend request sent.", "accept": "You're now friends.",
                   "unfriend": "Unfriended.", "block": "Blocked.", "unblock": "Unblocked."}
        if action not in calls:
            return
        if view.friend_button is not None:
            view.friend_button.setEnabled(False)

        def done(_r) -> None:
            view.banner.show_message(notices[action], "good", "OK")
            self.friends_changed.emit()
            self.profile_shown(profile)
            self.reload(quiet=True)

        def failed(message: str) -> None:
            if view.friend_button is not None:
                view.friend_button.setEnabled(True)
            view.banner.show_message(message, "danger", "OK")
        run(view, calls[action], done, failed)

    def open_requests(self) -> None:
        """A friend-request notification was clicked."""
        self._view.select_tab("requests")
        self.reload(quiet=self._loaded)


def my_handle_from(snapshot) -> Optional[str]:
    profile = getattr(snapshot, "profile", None) if snapshot is not None else None
    return getattr(profile, "handle", None)
