"""Announcements from the Akeso admins (migration 015).

Plain data, built from what my_announcements() / admin_list_announcements()
return. Labels live here so the pop-up, the dashboard list and the admin
page agree on them.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from app.models.account import parse_time

# (value, label, description) in the order the editor shows them.
LEVELS = [
    ("info", "Info", "News and reminders."),
    ("important", "Important", "Something everyone should read (amber)."),
    ("critical", "Critical", "Urgent: outages, security, deadlines (red)."),
]
LEVEL_LABELS = {value: text for value, text, _ in LEVELS}
LEVEL_ICONS = {"info": "info", "important": "triangle-alert", "critical": "octagon-alert"}
LEVEL_PILLS = {"info": "acPill", "important": "acPillWarn", "critical": "acPillDanger"}

AUDIENCES = [
    ("everyone", "Everyone"),
    ("student", "Students only"),
    ("educator", "Educators only"),
]
AUDIENCE_LABELS = dict(AUDIENCES)

STATUS_LABELS = {"live": "Live", "scheduled": "Scheduled", "expired": "Expired",
                 "ended": "Ended"}
STATUS_TONES = {"live": "good", "scheduled": "blue", "expired": "", "ended": ""}

TITLE_MAX, BODY_MAX, LABEL_MAX = 120, 4000, 40
DEFAULT_LINK_LABEL = "Learn more"


@dataclass
class Announcement:
    id: str
    title: str
    body: str
    level: str = "info"
    audience: str = "everyone"
    link_url: str = ""
    link_label: str = ""
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    dismissed: bool = False          # my_announcements(): this user closed it
    author: str = ""                 # admin list only
    dismiss_count: int = 0           # admin list only

    @classmethod
    def from_row(cls, row: dict) -> "Announcement":
        return cls(
            id=str(row["id"]), title=row.get("title") or "", body=row.get("body") or "",
            level=row.get("level") if row.get("level") in LEVEL_LABELS else "info",
            audience=row.get("audience") if row.get("audience") in AUDIENCE_LABELS
            else "everyone",
            link_url=row.get("link_url") or "", link_label=row.get("link_label") or "",
            starts_at=parse_time(row.get("starts_at")), ends_at=parse_time(row.get("ends_at")),
            ended_at=parse_time(row.get("ended_at")),
            created_at=parse_time(row.get("created_at")),
            updated_at=parse_time(row.get("updated_at")),
            dismissed=bool(row.get("dismissed")), author=row.get("author") or "",
            dismiss_count=int(row.get("dismiss_count") or 0))

    @property
    def button_text(self) -> str:
        return self.link_label or DEFAULT_LINK_LABEL

    def status(self, now: Optional[datetime] = None) -> str:
        now = now or datetime.now(timezone.utc)
        if self.ended_at is not None:
            return "ended"
        if self.ends_at is not None and self.ends_at <= now:
            return "expired"
        if self.starts_at is not None and self.starts_at > now:
            return "scheduled"
        return "live"

    def to_payload(self, reshow: bool = False) -> dict:
        """What admin_save_announcement() takes."""
        def iso(value: Optional[datetime]) -> Optional[str]:
            return value.astimezone(timezone.utc).isoformat() if value else None
        return {"id": self.id or None, "title": self.title.strip(), "body": self.body.strip(),
                "level": self.level, "audience": self.audience,
                "link_url": self.link_url.strip() or None,
                "link_label": self.link_label.strip() or None,
                "starts_at": iso(self.starts_at), "ends_at": iso(self.ends_at),
                "reshow": reshow}


def check(item: Announcement) -> Optional[str]:
    """The first problem with an announcement being written, or None. (The
    database checks all of it again.)"""
    if not item.title.strip():
        return "Give the announcement a title."
    if len(item.title.strip()) > TITLE_MAX:
        return f"Keep the title under {TITLE_MAX} characters."
    if not item.body.strip():
        return "Write the message."
    if len(item.body.strip()) > BODY_MAX:
        return f"Keep the message under {BODY_MAX} characters."
    url = item.link_url.strip()
    if url and (not url.startswith(("https://", "http://")) or " " in url):
        return "The link must start with https:// (or http://) and have no spaces."
    if len(item.link_label.strip()) > LABEL_MAX:
        return f"Keep the button text under {LABEL_MAX} characters."
    if item.ends_at is not None:
        start = item.starts_at or datetime.now(timezone.utc)
        if item.ends_at <= start:
            return "The end date must be after the start."
    return None
