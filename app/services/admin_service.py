"""Admin Control Panel rules the app can check before asking the server.

The database checks everything again (it must: anyone can edit this
Python). These checks only exist so a mistake is caught while typing,
with a clear message, instead of after a round trip.
"""

import re
from typing import Optional

from app.models.admin import KINDS, AdminUser, AuditEntry, ContentItem, UserDetail
from app.repositories.admin_repository import AdminRepository

ID_PATTERN = re.compile(r"^[a-z0-9_]{2,60}$")


class AdminService:
    def __init__(self, repository: AdminRepository) -> None:
        self._repo = repository

    # ------------------------------------------------------------ accounts

    def users(self) -> list[AdminUser]:
        return [AdminUser.from_row(row) for row in self._repo.users()]

    def user_detail(self, user_id: str) -> UserDetail:
        return UserDetail.from_row(self._repo.user_detail(user_id))

    def set_role(self, user_id: str, role: str) -> None:
        self._repo.set_role(user_id, role)

    def set_suspended(self, user_id: str, suspend: bool, reason: str = "") -> None:
        self._repo.set_suspended(user_id, suspend, reason.strip()[:300])

    def delete_user(self, user_id: str, confirm: str) -> str:
        """'deleted', or 'scheduled' if the project only allows a scheduled delete."""
        return self._repo.delete_user(user_id, confirm.strip())

    # ------------------------------------------------------------- content

    def body_systems(self) -> list[tuple[str, str]]:
        return [(row["id"], row["name"]) for row in self._repo.body_systems()]

    def content(self, kind: str) -> list[ContentItem]:
        assert kind in KINDS
        return [ContentItem.from_row(kind, row) for row in self._repo.list_content(kind)]

    def all_content(self) -> dict[str, list[ContentItem]]:
        return {kind: self.content(kind) for kind in KINDS}

    def entry(self, kind: str, entry_id: str) -> dict:
        return self._repo.get_content(kind, entry_id)

    def save(self, kind: str, data: dict, is_new: bool) -> str:
        return self._repo.save_content(kind, data, is_new)

    def set_published(self, kind: str, entry_id: str, published: bool) -> None:
        self._repo.set_published(kind, entry_id, published)

    def audit(self, limit: int = 200, before: Optional[int] = None) -> tuple[list[AuditEntry], int]:
        data = self._repo.audit(limit, before)
        return ([AuditEntry.from_row(row) for row in data.get("items") or []],
                int(data.get("total") or 0))

    # ----------------------------------------------------------- checking

    @staticmethod
    def check_entry(kind: str, data: dict, is_new: bool,
                    existing_ids: set[str]) -> Optional[str]:
        """A message for the first problem in an editor's data, or None."""
        entry_id = (data.get("id") or "").strip()
        if not (data.get("name") or "").strip():
            return f"Give the {kind} a name."
        if not ID_PATTERN.match(entry_id):
            return "The ID must be 2 to 60 lowercase letters, numbers or underscores."
        if is_new and entry_id in existing_ids:
            return f"Another {kind} already uses the ID “{entry_id}”."
        if kind == "disease" and not (data.get("description") or "").strip():
            return "Write a clinical summary for the disease."
        for ref in data.get("references") or []:
            if (ref.get("citation_text") or ref.get("url")) and not ref.get("source_name"):
                return "Every reference needs a source name."
        return None
