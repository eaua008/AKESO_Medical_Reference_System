"""Clinical Exchange and notifications, in Supabase.

Every call is one of the database functions from migration 003: the app
has no direct access to the Exchange tables. The functions decide what
this user may see (anonymous authors stay hidden) and may do.
"""

from typing import Optional

from app.core.supabase_session import SessionClient
from app.repositories.account_errors import AccountError, friendly


class ExchangeRepository:
    def __init__(self, session: SessionClient) -> None:
        self._s = session

    def _rpc(self, function: str, params: Optional[dict] = None):
        def call():
            return self._s.rpc(function, params or {}).execute().data
        try:
            return self._s.run(call)
        except AccountError:
            raise
        except Exception as exc:  # noqa: BLE001
            message = getattr(exc, "message", None) or str(exc)
            if "could not find the function" in message.lower() or "schema cache" in message.lower():
                raise AccountError("Clinical Exchange isn't installed yet. Run "
                                   "database/migrations/003_clinical_exchange.sql.") from exc
            raise AccountError(friendly(exc)) from exc

    # ------------------------------------------------------------ reading

    def feed(self, tab: str, tag_kind: Optional[str], tag_id: Optional[str],
             body_system: Optional[str], program: Optional[str], search: Optional[str],
             limit: int, offset: int) -> list[dict]:
        return self._rpc("ex_feed", {
            "p_tab": tab, "p_tag_kind": tag_kind, "p_tag_id": tag_id,
            "p_body_system": body_system, "p_program": program, "p_search": search,
            "p_limit": limit, "p_offset": offset}) or []

    def post(self, post_id: str) -> dict:
        return self._rpc("ex_post", {"p_id": post_id})

    def profile_card(self, handle: str) -> dict:
        return self._rpc("ex_profile_card", {"p_handle": handle})

    def profile(self, handle: str) -> dict:
        return self._rpc("ex_profile", {"p_handle": handle})

    def follow_user(self, handle: str, on: bool) -> bool:
        return bool(self._rpc("ex_follow_user", {"p_handle": handle, "p_on": on}))

    def mod_queue(self) -> list[dict]:
        return self._rpc("ex_mod_queue") or []

    # ------------------------------------------------------------ writing

    def create_post(self, payload: dict) -> str:
        return self._rpc("ex_create_post", payload)

    def edit_post(self, post_id: str, title: str, body: str, question: str, tags: list[dict]) -> None:
        self._rpc("ex_edit_post", {"p_id": post_id, "p_title": title, "p_body": body,
                                   "p_question": question, "p_tags": tags})

    def delete_post(self, post_id: str) -> None:
        self._rpc("ex_delete_post", {"p_id": post_id})

    def reply(self, post_id: str, parent_id: Optional[str], body: str, anonymous: bool) -> str:
        return self._rpc("ex_reply", {"p_post": post_id, "p_parent": parent_id,
                                      "p_body": body, "p_anonymous": anonymous})

    def option_comment(self, post_id: str, option_id: str, body: str, anonymous: bool) -> str:
        return self._rpc("ex_option_comment", {"p_post": post_id, "p_option": option_id,
                                               "p_body": body, "p_anonymous": anonymous})

    def edit_reply(self, reply_id: str, body: str) -> None:
        self._rpc("ex_edit_reply", {"p_id": reply_id, "p_body": body})

    def delete_reply(self, reply_id: str) -> None:
        self._rpc("ex_delete_reply", {"p_id": reply_id})

    def vote(self, kind: str, target_id: str, on: bool) -> int:
        return int(self._rpc("ex_vote", {"p_kind": kind, "p_id": target_id, "p_on": on}) or 0)

    def best_answer(self, post_id: str, reply_id: Optional[str]) -> None:
        self._rpc("ex_best_answer", {"p_post": post_id, "p_reply": reply_id})

    def verify_reply(self, reply_id: str, on: bool) -> None:
        self._rpc("ex_verify_reply", {"p_reply": reply_id, "p_on": on})

    def follow(self, post_id: str, on: bool) -> None:
        self._rpc("ex_follow", {"p_post": post_id, "p_on": on})

    # --------------------------------------------------------------- poll

    def poll_suggest(self, post_id: str, disease_id: Optional[str], label: str) -> str:
        return self._rpc("ex_poll_suggest", {"p_post": post_id, "p_disease_id": disease_id,
                                             "p_label": label})

    def poll_vote(self, post_id: str, option_id: Optional[str]) -> None:
        self._rpc("ex_poll_vote", {"p_post": post_id, "p_option": option_id})

    def poll_reveal(self, post_id: str, option_id: str, explanation: str) -> None:
        self._rpc("ex_poll_reveal", {"p_post": post_id, "p_option": option_id,
                                     "p_explanation": explanation})

    # --------------------------------------------------------- moderation

    def report(self, kind: str, target_id: str, reason: str, note: str) -> None:
        self._rpc("ex_report", {"p_kind": kind, "p_id": target_id, "p_reason": reason,
                                "p_note": note})

    def moderate(self, kind: str, target_id: str, action: str, reason: str) -> None:
        self._rpc("ex_moderate", {"p_kind": kind, "p_id": target_id, "p_action": action,
                                  "p_reason": reason})

    def dismiss_reports(self, kind: str, target_id: str) -> None:
        self._rpc("ex_dismiss_reports", {"p_kind": kind, "p_id": target_id})

    # ------------------------------------------------------ notifications

    def notifications(self, limit: int = 30, before: Optional[int] = None) -> list[dict]:
        return self._rpc("notif_list", {"p_limit": limit, "p_before": before}) or []

    def unread_count(self) -> int:
        return int(self._rpc("notif_unread_count") or 0)

    def mark_read(self, ids: Optional[list[int]] = None) -> None:
        self._rpc("notif_mark_read", {"p_ids": ids})

    def clear_read(self) -> None:
        self._rpc("notif_clear")

    def delete_notifications(self, ids: list[int]) -> None:
        """Migration 016."""
        self._rpc("notif_delete", {"p_ids": ids})
