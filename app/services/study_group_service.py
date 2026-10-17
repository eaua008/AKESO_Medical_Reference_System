"""Study Groups (migration 042): directory, membership, chat, notes shelf.

Invite links: the database returns the link's token once, when the link is
made (it keeps only a hash). The app builds a link and a plain code from
it. People join by pasting either into "Join with a link or code"; on
Windows, akeso://join/<token> also opens Akeso directly when the installer
registered the protocol (Messenger usually doesn't make such links
clickable, so the code is always shown too).
"""

import re
from typing import Optional

from app.models.notebook import NotebookItem
from app.models.social import (
    GroupInvite, GroupMessage, GroupNote, GroupReport, MESSAGE_MAX, StudyGroup,
)
from app.repositories.social_repository import SocialRepository
from app.services.notebook_share_service import snapshot
from app.services.phi_guard import find_phi, phi_message

JOIN_SCHEME = "akeso://join/"
_TOKEN = re.compile(r"(?:join/)?([0-9a-f]{64})\b", re.IGNORECASE)


def parse_invite(text: str) -> Optional[str]:
    """A pasted link (akeso://join/..., https://.../join/...) or the bare code
    -> the token, or None if nothing in it looks like one."""
    match = _TOKEN.search((text or "").strip())
    return match.group(1).lower() if match else None


def invite_link(token: str) -> str:
    return JOIN_SCHEME + token


def invite_text(group_name: str, token: str) -> str:
    """What "Copy invite" puts on the clipboard, ready to paste anywhere."""
    return (f"Join my Akeso study group “{group_name}”:\n{invite_link(token)}\n\n"
            f"If the link doesn't open, go to Akeso → Study Groups → Join with a link or code "
            f"and paste this code:\n{token}")


def check_message(text: str) -> Optional[str]:
    """Why a message can't be sent yet, or None (the database checks again)."""
    body = (text or "").strip()
    if not body:
        return "Write a message first."
    if len(body) > MESSAGE_MAX:
        return f"Keep messages under {MESSAGE_MAX:,} characters ({len(body):,} now)."
    found = find_phi(body)
    return phi_message(found) if found else None


class StudyGroupService:
    def __init__(self, repository: SocialRepository) -> None:
        self._repo = repository

    # ---------------------------------------------------------- directory

    def my_groups(self) -> list[StudyGroup]:
        return [StudyGroup.from_json(row) for row in self._repo.group_my_list()]

    def browse(self, search: str = "", topic: str = "", body_system: str = "") -> list[StudyGroup]:
        return [StudyGroup.from_json(row)
                for row in self._repo.group_browse(search, topic, body_system)]

    def invites(self) -> list[GroupInvite]:
        return [GroupInvite.from_json(row) for row in self._repo.group_my_invites()]

    def home(self) -> tuple[list[StudyGroup], list[GroupInvite]]:
        return self.my_groups(), self.invites()

    def get(self, group_id: str) -> StudyGroup:
        return StudyGroup.from_json(self._repo.group_get(group_id))

    def create(self, name: str, description: str, visibility: str, topic: str,
               body_system: Optional[str]) -> str:
        name = " ".join((name or "").split())
        if len(name) < 3:
            raise ValueError("Give the group a name of at least 3 characters.")
        found = find_phi(name, description)
        if found:
            raise ValueError(phi_message(found))
        return self._repo.group_create(name, (description or "").strip(), visibility,
                                       (topic or "").strip(), body_system or None)

    # -------------------------------------------------------- membership

    def join_public(self, group_id: str) -> None:
        self._repo.group_join_public(group_id)

    def join_with(self, text: str) -> str:
        token = parse_invite(text)
        if token is None:
            raise ValueError("Paste the whole invite link, or the 64-character code from it.")
        return self._repo.group_join_with_token(token)

    def respond(self, invite_id: str, accept: bool) -> str:
        return self._repo.group_invite_respond(invite_id, accept)

    def new_link(self, group_id: str, expires_hours: Optional[int]) -> str:
        return str(self._repo.group_link_create(group_id, expires_hours).get("token") or "")

    def revoke_link(self, group_id: str) -> None:
        self._repo.group_link_revoke(group_id)

    def invite_friend(self, group_id: str, friend_id: str) -> None:
        self._repo.group_invite_friend(group_id, friend_id)

    def leave(self, group_id: str) -> str:
        return self._repo.group_leave(group_id)

    def set_role(self, group_id: str, user_id: str, role: str) -> None:
        self._repo.group_set_role(group_id, user_id, role)

    def remove_member(self, group_id: str, user_id: str) -> None:
        self._repo.group_remove_member(group_id, user_id)

    def set_muted(self, group_id: str, muted: bool) -> None:
        self._repo.group_set_muted(group_id, muted)

    def delete(self, group_id: str) -> None:
        self._repo.group_delete(group_id)

    # --------------------------------------------------------------- chat

    def send(self, group_id: str, body: str) -> GroupMessage:
        problem = check_message(body)
        if problem:
            raise ValueError(problem)
        return GroupMessage.from_json(self._repo.group_send(group_id, body.strip()))

    # ---- pictures (migration 045)

    def prepare_picture(self, file_path: str):
        """Check, rotate, strip metadata, shrink: see chat_images.py. Raises
        PictureError with a message for the user."""
        from app.services.chat_images import prepare
        return prepare(file_path)

    def send_picture(self, group_id: str, prepared, caption: str) -> GroupMessage:
        """Upload an already prepared picture, then send the message that
        points at it. If sending fails after the upload, the file is removed
        again (the daily purge sweeps anything left over)."""
        problem = check_message(caption) if (caption or "").strip() else None
        if problem:
            raise ValueError(problem)
        path = prepared.new_path(group_id, self._repo.user_id())
        self._repo.group_upload_image(path, prepared.data, prepared.mime)
        try:
            return GroupMessage.from_json(
                self._repo.group_send_image(group_id, (caption or "").strip(), path))
        except Exception:
            try:
                self._repo.group_remove_images([path])
            except Exception:  # noqa: BLE001 - best effort; the purge sweep catches it
                pass
            raise

    def picture(self, path: str) -> bytes:
        return self._repo.group_download_image(path)

    def delete_group_pictures(self, group_id: str) -> None:
        """Before deleting a group: remove its picture files while you are
        still its owner (best effort; the purge sweep catches the rest)."""
        try:
            self._repo.group_remove_images(self._repo.group_list_images(group_id))
        except Exception:  # noqa: BLE001
            pass

    def messages_after(self, group_id: str, after: Optional[int]
                       ) -> tuple[list[GroupMessage], bool, Optional[int]]:
        """(messages, more to fetch, the last message I had read before this
        call). The last one is None before migration 044 is run."""
        data = self._repo.group_messages_after(group_id, after, 50)
        last_read = data.get("last_read")
        return ([GroupMessage.from_json(m) for m in data.get("messages") or []],
                bool(data.get("more")), int(last_read) if last_read is not None else None)

    # -------------------------------------------------------------- notes

    def share_note(self, group_id: str, item: NotebookItem) -> str:
        return self._repo.group_share_note(group_id, snapshot(item))

    def notes(self, group_id: str) -> list[GroupNote]:
        return [GroupNote.from_json(row) for row in self._repo.group_notes(group_id)]

    def note(self, note_id: str) -> GroupNote:
        return GroupNote.from_json(self._repo.group_note_get(note_id))

    def remove_note(self, note_id: str) -> None:
        self._repo.group_note_remove(note_id)

    # --------------------------------------------------------- moderation

    def report(self, group_id: str, kind: str, target_id: str, reason: str, note: str) -> None:
        self._repo.group_report(group_id, kind, target_id, reason, note)

    def moderate(self, group_id: str, kind: str, target_id: str, action: str) -> None:
        self._repo.group_moderate(group_id, kind, target_id, action)

    def report_queue(self) -> list[GroupReport]:
        return [GroupReport.from_json(row) for row in self._repo.group_report_queue()]
