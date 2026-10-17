"""Sharing Study Notebook notes as read-only snapshots (migration 041).

Sender side: the note's title and text (pictures removed) are checked for
patient data here, so the warning shows before anything is sent; the
database runs the same check again.

Receiver side: "Save a copy to my notebook" makes a normal local note in a
"Shared with me" subject, which then syncs like any other note.
"""

import re
from typing import Optional

from app.models.notebook import NotebookItem
from app.models.social import SharedNote
from app.repositories.social_repository import SocialRepository
from app.services.notebook_service import NotebookService
from app.services.phi_guard import find_phi, phi_message

SHARED_SUBJECT = "Shared with me"
MAX_BODY = 200_000
IMAGE_PLACEHOLDER = "[image not shared]"
_IMG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


def strip_images(html: str) -> str:
    """Pictures live in the owner's private folder, which recipients can't
    read: each one becomes a short placeholder."""
    return _IMG.sub(IMAGE_PLACEHOLDER, html or "")


def plain(html: str) -> str:
    text = _TAG.sub(" ", html or "")
    return re.sub(r"&nbsp;|&#160;", " ", text)


class ShareError(ValueError):
    """Something to tell the owner instead of sharing."""


def snapshot(item: NotebookItem) -> dict:
    """The payload for notebook_share_create / group_share_note."""
    body = strip_images(item.body)
    if len(body) > MAX_BODY:
        raise ShareError("This note is too long to share (over 200,000 characters of text). "
                         "Split it into smaller notes.")
    found = find_phi(item.title, plain(body))
    if found:
        raise ShareError("Not shared: " + phi_message(found))
    return {"source_item_id": item.id, "kind": item.kind, "title": item.title, "body": body}


class NotebookShareService:
    def __init__(self, repository: SocialRepository, notebook: NotebookService) -> None:
        self._repo = repository
        self._notebook = notebook

    # ------------------------------------------------------------ sender

    def share(self, item_id: str, friend_ids: list[str]) -> int:
        item = self._item(item_id)
        result = self._repo.share_create(snapshot(item), friend_ids)
        return int(result.get("shared_with") or 0)

    def manage(self, item_id: str) -> Optional[SharedNote]:
        data = self._repo.share_manage(item_id)
        return SharedNote.from_json(data) if data else None

    def shared_item_ids(self) -> set[str]:
        return set(self._repo.share_my_items())

    def update_copy(self, share_id: str, item_id: str) -> None:
        payload = snapshot(self._item(item_id))
        self._repo.share_update(share_id, payload["title"], payload["body"])

    def unshare(self, share_id: str, recipient_id: Optional[str]) -> None:
        self._repo.share_revoke(share_id, recipient_id)

    def _item(self, item_id: str) -> NotebookItem:
        item = self._notebook.get(item_id)
        if item is None:
            raise ShareError("That note is no longer in your notebook.")
        return item

    # ---------------------------------------------------------- receiver

    def received(self) -> list[SharedNote]:
        return [SharedNote.from_json(row) for row in self._repo.share_received()]

    def open(self, share_id: str) -> SharedNote:
        return SharedNote.from_json(self._repo.share_get(share_id))

    def fetch_copy(self, share_id: str) -> SharedNote:
        """The snapshot to save (network; run off the UI thread)."""
        return SharedNote.from_json(self._repo.share_save_copy(share_id))

    def save_copy(self, note: SharedNote, from_label: str = "") -> NotebookItem:
        """Write a fetched snapshot into my notebook (local; on the UI thread)."""
        subject_id = self._shared_subject()
        item = self._notebook.create_note(subject_id, base=note.title)
        body = note.body
        if from_label:
            body = (f"<p><i>Shared by {from_label}. This is your own copy: edits stay in "
                    f"your notebook.</i></p>") + body
        self._notebook.save_body(item.id, body)
        return self._notebook.get(item.id) or item

    def _shared_subject(self) -> str:
        for subject in self._notebook.subjects():
            if subject.name.lower() == SHARED_SUBJECT.lower():
                return subject.id
        subject, _error = self._notebook.create_subject(SHARED_SUBJECT)
        return subject.id if subject else ""
