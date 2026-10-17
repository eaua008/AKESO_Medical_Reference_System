"""Friends (migration 040): mutual, separate from Clinical Exchange's Follow.

No Qt here; the controller runs these calls off the UI thread.
"""

import re
from typing import Optional

from app.models.social import BlockedPerson, Friend, FriendRequests
from app.repositories.social_repository import SocialRepository

HANDLE = re.compile(r"^[a-z0-9_]{3,20}$")


def clean_handle(text: str) -> Optional[str]:
    """'@Maria_S', 'maria_s ' or a pasted profile line -> 'maria_s', or None."""
    value = (text or "").strip().lstrip("@").strip().lower()
    return value if HANDLE.match(value) else None


class FriendsService:
    def __init__(self, repository: SocialRepository) -> None:
        self._repo = repository

    def friends(self) -> list[Friend]:
        return [Friend.from_json(row) for row in self._repo.friend_list()]

    def requests(self) -> FriendRequests:
        return FriendRequests.from_json(self._repo.friend_requests())

    def blocked(self) -> list[BlockedPerson]:
        return [BlockedPerson.from_json(row) for row in self._repo.friend_blocked_list()]

    def overview(self) -> tuple[list[Friend], FriendRequests, list[BlockedPerson]]:
        """Everything the Friends page shows, in one background call."""
        return self.friends(), self.requests(), self.blocked()

    def request(self, handle: str) -> str:
        """'sent' or 'accepted'. An unknown handle raises ValueError with a message
        for the form (migration 047); someone who blocked you still reads 'sent'."""
        clean = clean_handle(handle)
        if clean is None:
            raise ValueError("Enter a handle like @maria_santos (3 to 20 letters, numbers or _).")
        status = self._repo.friend_request(clean)
        if status == "not_found":
            raise ValueError(f"No user with the handle @{clean}. Check the spelling and try again.")
        if status == "self":
            raise ValueError("That is your own handle. Enter a classmate's @handle instead.")
        return status

    def respond(self, user_id: str, accept: bool) -> None:
        self._repo.friend_respond(user_id, accept)

    def cancel(self, request_id: int) -> None:
        self._repo.friend_cancel(request_id)

    def status(self, handle: str) -> str:
        return self._repo.friend_status(handle)

    def remove(self, user_id: str) -> None:
        self._repo.friend_remove(user_id)

    def block(self, user_id: str) -> None:
        self._repo.friend_block(user_id)

    def unblock(self, user_id: str) -> None:
        self._repo.friend_unblock(user_id)
