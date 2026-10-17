"""Friends, notebook sharing and Study Groups, plugged into the dashboard.

Kept out of dashboard_shell.py so the shell only calls register_social()
and forwards tab visits. Needs a signed-in account; before migrations
040-042 are run every screen shows a friendly "not set up yet" state and
the notebook simply doesn't show its sharing parts.
"""

from dataclasses import dataclass
from typing import Optional

from PySide6.QtCore import QTimer

from app.controllers.friends_controller import FriendsController, my_handle_from
from app.controllers.notebook_share_controller import NotebookShareController
from app.controllers.study_groups_controller import StudyGroupsController
from app.repositories.social_repository import SocialRepository
from app.services.friends_service import FriendsService
from app.services.notebook_share_service import NotebookShareService
from app.services.study_group_service import StudyGroupService, parse_invite
from app.ui.views.social.friends_view import FriendsView
from app.ui.views.social.group_page import GroupPage
from app.ui.views.social.study_groups_view import StudyGroupsView


@dataclass
class Social:
    friends: FriendsController
    groups: StudyGroupsController
    sharing: NotebookShareController
    pending_join: Optional[str] = None

    def on_tab(self, tab_id: str) -> None:
        if tab_id == "friends":
            self.friends.on_shown()
        elif tab_id == "groups":
            self.groups.on_shown()
        elif tab_id == "notebook":
            self.sharing.refresh_if_stale()

    def shutdown(self) -> None:
        self.groups.shutdown()


def register_social(shell, account) -> Social:
    repository = SocialRepository(account.session)

    # Friends
    friends_view = FriendsView()
    friends = FriendsController(friends_view, FriendsService(repository))
    friends_view.set_my_handle(my_handle_from(account.snapshot) or "")
    shell.register_view("friends", friends_view)
    accounts = getattr(shell, "account_controller", None)
    if accounts is not None:              # the handle can change (migration 043)
        accounts.identity_changed.connect(
            lambda *_a: friends_view.set_my_handle(accounts.my_handle))

    # Study Groups: the list page, and a group (and a shelf note) in sheets.
    group_service = StudyGroupService(repository)
    share_service = NotebookShareService(repository, shell._notebook_service)
    groups_view = StudyGroupsView()
    group_page = GroupPage()
    groups = StudyGroupsController(
        groups_view, group_page, group_service, friends,
        notebook=shell._notebook_service, share=share_service,
        is_moderator=account.role in ("educator", "admin"),
        sheet=shell.add_sheet("groups", keep_content=True),
        reader_sheet=shell.add_sheet("groups", keep_content=True))
    try:
        groups.set_body_systems([(s.id, s.name) for s in shell._disease_service.body_systems()])
    except Exception:  # noqa: BLE001 - the encyclopedia isn't downloaded yet: no filter
        pass
    shell.register_view("groups", groups_view)
    shell._theme_scope.add(group_page, group_page.refresh_theme)

    # Notebook sharing: "Share…", the Shared badge, "Shared with me".
    sharing = NotebookShareController(
        shell.notebook_controller, share_service, friends,
        groups=lambda: group_service if groups.installed else None,
        sheet=shell.add_sheet("notebook", keep_content=True))
    sharing.start()

    # Member profiles (Clinical Exchange) get Add friend / Block.
    exchange = getattr(shell, "exchange_controller", None)
    if exchange is not None and getattr(shell, "profile_view", None) is not None:
        friends.attach_profile(shell.profile_view)
        exchange.profile_loaded.connect(friends.profile_shown)
        friends.profile_requested.connect(exchange.show_profile)
        groups.profile_requested.connect(exchange.show_profile)

    # Changes that other screens should see.
    friends.friends_changed.connect(sharing.refresh)
    groups.notebook_changed.connect(shell.notebook_controller.refresh)
    sharing.notebook_changed.connect(lambda: None)

    social = Social(friends=friends, groups=groups, sharing=sharing)
    # A dot on "Study Groups" in the sidebar while something is unread.
    groups.unread_changed.connect(lambda n: shell.sidebar.set_dot("groups", n > 0))
    QTimer.singleShot(2500, lambda: groups.reload(quiet=True))        # once, after sign-in

    # The bell: friend requests, shared notes, group invites and mentions.
    notifications = getattr(shell, "notifications_controller", None)
    if notifications is not None:
        def open_ref(kind: str, ref_id: str) -> None:
            if kind == "friend":
                shell.show_tab("friends")
                friends.open_requests()
            elif kind == "notebook_share":
                shell.show_tab("notebook")
                sharing.open_from_notification(ref_id)
            elif kind == "group_invite":
                shell.show_tab("groups")
            elif kind == "group":
                shell.show_tab("groups")
                groups.open_group(ref_id)
        notifications.open_ref.connect(open_ref)
    return social


def join_link_from_args(argv: list[str]) -> Optional[str]:
    """akeso://join/<token> passed by Windows (installer protocol handler)."""
    for arg in argv[1:]:
        if arg.lower().startswith("akeso://"):
            return parse_invite(arg)
    return None
