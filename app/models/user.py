from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Domain model for an authenticated user.

    Knows nothing about Supabase. Swap databases later and this file
    does not change.
    """

    id: str
    email: str
    display_name: Optional[str] = None

    @property
    def label(self) -> str:
        """What the UI shows. Falls back to the name part of the email."""
        if self.display_name:
            return self.display_name
        return self.email.split("@")[0]

    @classmethod
    def from_supabase(cls, raw) -> "User":
        """Translate a Supabase user object into our own model.

        The only place in the codebase that knows Supabase's field names.
        """
        metadata = getattr(raw, "user_metadata", None) or {}
        return cls(
            id=raw.id,
            email=raw.email,
            display_name=metadata.get("display_name"),
        )