"""Friends, shared notes and study groups, in Supabase.

Every call is one of the database functions from migrations 040 (friends),
041 (notebook sharing) and 042 (study groups). As with Clinical Exchange,
the app has no direct access to those tables: the functions decide what
this user may see and do.

Before the migrations are run the functions don't exist; that raises
SocialNotInstalled, which the screens show as a friendly "not set up yet"
state instead of an error.
"""

from typing import Optional

from app.core.supabase_session import SessionClient
from app.repositories.account_errors import AccountError, friendly

MIGRATIONS = {
    "friends": "040_friends.sql",
    "sharing": "041_notebook_sharing.sql",
    "groups": "042_study_groups.sql",
    "images": "045_group_images.sql",
}
IMAGE_BUCKET = "group-attachments"


class SocialNotInstalled(AccountError):
    """The feature's migration hasn't been run on this Supabase project."""

    def __init__(self, feature: str) -> None:
        self.feature = feature
        names = {"friends": "Friends", "sharing": "Note sharing", "groups": "Study Groups",
                 "images": "Pictures in group chat"}
        super().__init__(f"{names.get(feature, 'This feature')} isn't set up on Akeso's server "
                         f"yet. The administrator needs to run "
                         f"database/migrations/{MIGRATIONS.get(feature, '040_friends.sql')}.")


def not_installed(exc: BaseException) -> bool:
    message = (getattr(exc, "message", None) or str(exc)).lower()
    return ("could not find the function" in message or "schema cache" in message
            or "pgrst202" in message)


class SocialRepository:
    def __init__(self, session: SessionClient) -> None:
        self._s = session

    def _rpc(self, feature: str, function: str, params: Optional[dict] = None):
        def call():
            return self._s.rpc(function, params or {}).execute().data
        try:
            return self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            if not_installed(exc):
                raise SocialNotInstalled(feature) from exc
            raise AccountError(friendly(exc)) from exc

    # ------------------------------------------------------------ friends

    def friend_request(self, handle: str) -> str:
        result = self._rpc("friends", "friend_request", {"p_handle": handle}) or {}
        return result.get("status", "sent")

    def friend_respond(self, user_id: str, accept: bool) -> None:
        self._rpc("friends", "friend_respond", {"p_from": user_id, "p_accept": accept})

    def friend_cancel(self, request_id: int) -> None:
        self._rpc("friends", "friend_cancel", {"p_request": request_id})

    def friend_list(self) -> list[dict]:
        return self._rpc("friends", "friend_list") or []

    def friend_requests(self) -> dict:
        return self._rpc("friends", "friend_requests") or {}

    def friend_status(self, handle: str) -> str:
        return self._rpc("friends", "friend_status", {"p_handle": handle}) or "none"

    def friend_remove(self, user_id: str) -> None:
        self._rpc("friends", "friend_remove", {"p_user": user_id})

    def friend_block(self, user_id: str) -> None:
        self._rpc("friends", "friend_block", {"p_user": user_id})

    def friend_unblock(self, user_id: str) -> None:
        self._rpc("friends", "friend_unblock", {"p_user": user_id})

    def friend_blocked_list(self) -> list[dict]:
        return self._rpc("friends", "friend_blocked_list") or []

    # ------------------------------------------------------- shared notes

    def share_create(self, item: dict, recipients: list[str]) -> dict:
        return self._rpc("sharing", "notebook_share_create",
                         {"p_item": item, "p_recipients": recipients}) or {}

    def share_manage(self, item_id: str) -> Optional[dict]:
        return self._rpc("sharing", "notebook_share_manage", {"p_item_id": item_id})

    def share_my_items(self) -> list[str]:
        return [str(x) for x in self._rpc("sharing", "notebook_share_my_items") or []]

    def share_update(self, share_id: str, title: str, body: str) -> None:
        self._rpc("sharing", "notebook_share_update_snapshot",
                  {"p_id": share_id, "p_title": title, "p_body": body})

    def share_revoke(self, share_id: str, recipient: Optional[str]) -> None:
        self._rpc("sharing", "notebook_share_revoke", {"p_id": share_id, "p_recipient": recipient})

    def share_received(self) -> list[dict]:
        return self._rpc("sharing", "notebook_share_list_received") or []

    def share_get(self, share_id: str) -> dict:
        return self._rpc("sharing", "notebook_share_get", {"p_id": share_id}) or {}

    def share_save_copy(self, share_id: str) -> dict:
        return self._rpc("sharing", "notebook_share_save_copy", {"p_id": share_id}) or {}

    # ------------------------------------------------------- study groups

    def group_create(self, name: str, description: str, visibility: str, topic: str,
                     body_system: Optional[str]) -> str:
        return str(self._rpc("groups", "group_create", {
            "p_name": name, "p_description": description, "p_visibility": visibility,
            "p_topic": topic, "p_body_system": body_system}))

    def group_browse(self, search: str, topic: str, body_system: str,
                     limit: int = 30, offset: int = 0) -> list[dict]:
        return self._rpc("groups", "group_browse_public", {
            "p_search": search or None, "p_topic": topic or None,
            "p_body_system": body_system or None, "p_limit": limit, "p_offset": offset}) or []

    def group_my_list(self) -> list[dict]:
        return self._rpc("groups", "group_my_list") or []

    def group_get(self, group_id: str) -> dict:
        return self._rpc("groups", "group_get", {"p_group": group_id}) or {}

    def group_join_public(self, group_id: str) -> None:
        self._rpc("groups", "group_join_public", {"p_group": group_id})

    def group_join_with_token(self, token: str) -> str:
        return str(self._rpc("groups", "group_join_with_token", {"p_token": token}))

    def group_link_create(self, group_id: str, expires_hours: Optional[int]) -> dict:
        return self._rpc("groups", "group_invite_link_create",
                         {"p_group": group_id, "p_expires_hours": expires_hours}) or {}

    def group_link_revoke(self, group_id: str) -> None:
        self._rpc("groups", "group_invite_link_revoke", {"p_group": group_id})

    def group_invite_friend(self, group_id: str, friend_id: str) -> None:
        self._rpc("groups", "group_invite_friend", {"p_group": group_id, "p_friend": friend_id})

    def group_my_invites(self) -> list[dict]:
        return self._rpc("groups", "group_my_invites") or []

    def group_invite_respond(self, invite_id: str, accept: bool) -> str:
        return str(self._rpc("groups", "group_invite_respond",
                             {"p_invite": invite_id, "p_accept": accept}))

    def group_leave(self, group_id: str) -> str:
        return str(self._rpc("groups", "group_leave", {"p_group": group_id}))

    def group_set_role(self, group_id: str, user_id: str, role: str) -> None:
        self._rpc("groups", "group_set_role", {"p_group": group_id, "p_user": user_id, "p_role": role})

    def group_remove_member(self, group_id: str, user_id: str) -> None:
        self._rpc("groups", "group_remove_member", {"p_group": group_id, "p_user": user_id})

    def group_set_muted(self, group_id: str, muted: bool) -> None:
        self._rpc("groups", "group_set_muted", {"p_group": group_id, "p_muted": muted})

    def group_delete(self, group_id: str) -> None:
        self._rpc("groups", "group_delete", {"p_group": group_id})

    def group_send(self, group_id: str, body: str) -> dict:
        return self._rpc("groups", "group_send_message", {"p_group": group_id, "p_body": body}) or {}

    def group_messages_after(self, group_id: str, after: Optional[int], limit: int = 50) -> dict:
        return self._rpc("groups", "group_messages_after",
                         {"p_group": group_id, "p_after": after, "p_limit": limit}) or {}

    # ---- pictures in chat (migration 045): a private bucket, one file per picture

    def user_id(self) -> str:
        return self._s.user_id()

    def group_upload_image(self, path: str, data: bytes, mime: str) -> None:
        def call():
            self._s.bucket(IMAGE_BUCKET).upload(
                path, data, {"content-type": mime, "upsert": "false", "cache-control": "3600"})
        try:
            self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            text = (getattr(exc, "message", None) or str(exc)).lower()
            if "bucket not found" in text or "not found" in text and "bucket" in text:
                raise SocialNotInstalled("images") from exc
            if "row-level security" in text or "unauthorized" in text or "403" in text:
                raise AccountError("You can't send pictures in this group.") from exc
            if "too large" in text or "exceeded" in text or "413" in text:
                raise AccountError("That picture is over 5 MB. Choose a smaller one.") from exc
            raise AccountError(friendly(exc)) from exc

    def group_send_image(self, group_id: str, caption: str, path: str) -> dict:
        return self._rpc("images", "group_send_image",
                         {"p_group": group_id, "p_caption": caption, "p_path": path}) or {}

    def group_download_image(self, path: str) -> bytes:
        def call():
            return self._s.bucket(IMAGE_BUCKET).download(path)
        try:
            return self._s.run(call)
        except Exception as exc:  # noqa: BLE001
            raise AccountError("That picture isn't available.") from exc

    def group_remove_images(self, paths: list[str]) -> None:
        if paths:
            self._s.run(lambda: self._s.bucket(IMAGE_BUCKET).remove(paths))

    def group_list_images(self, group_id: str) -> list[str]:
        """Every picture file of one group (its sender folders, one level down)."""
        def call():
            bucket = self._s.bucket(IMAGE_BUCKET)
            paths = []
            for folder in bucket.list(group_id, {"limit": 1000}):
                if folder.get("id") is None:               # a sender's folder
                    for item in bucket.list(f"{group_id}/{folder['name']}", {"limit": 1000}):
                        paths.append(f"{group_id}/{folder['name']}/{item['name']}")
            return paths
        return self._s.run(call)

    def group_share_note(self, group_id: str, item: dict) -> str:
        return str(self._rpc("groups", "group_share_note", {"p_group": group_id, "p_item": item}))

    def group_notes(self, group_id: str) -> list[dict]:
        return self._rpc("groups", "group_notes_list", {"p_group": group_id}) or []

    def group_note_get(self, note_id: str) -> dict:
        return self._rpc("groups", "group_note_get", {"p_note": note_id}) or {}

    def group_note_remove(self, note_id: str) -> None:
        self._rpc("groups", "group_note_remove", {"p_note": note_id})

    def group_report(self, group_id: str, kind: str, target_id: str, reason: str, note: str) -> None:
        self._rpc("groups", "group_report", {"p_group": group_id, "p_kind": kind,
                                             "p_id": target_id, "p_reason": reason, "p_note": note})

    def group_moderate(self, group_id: str, kind: str, target_id: str, action: str) -> None:
        self._rpc("groups", "group_moderate", {"p_group": group_id, "p_kind": kind,
                                               "p_id": target_id, "p_action": action})

    def group_report_queue(self) -> list[dict]:
        return self._rpc("groups", "group_report_queue") or []
