"""Friends, shared notes and study groups (migrations 040, 041, 042).

Plain data, built from what the database functions return. A person is
always shown through ex_author on the server, so these never hold more of
someone's profile than their own switches allow.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.models.account import parse_time

GROUP_MEMBER_CAP = 50
MESSAGE_MAX = 2000
IMAGE_MAX_BYTES = 5 * 1024 * 1024         # per picture (the storage bucket enforces it too)

GROUP_ROLE_LABELS = {"owner": "Owner", "moderator": "Moderator", "member": "Member"}
APP_ROLE_LABELS = {"educator": "Educator", "admin": "Admin"}

# The same reasons as Clinical Exchange reports (the database checks them).
GROUP_REPORT_REASONS = [
    ("patient_data", "Contains real patient information"),
    ("harassment", "Harassment or disrespect"),
    ("misinformation", "Medically wrong or misleading"),
    ("spam", "Spam"),
    ("off_topic", "Off topic"),
    ("other", "Something else"),
]


@dataclass
class Person:
    id: str
    name: str
    handle: Optional[str] = None
    program: Optional[str] = None
    role: Optional[str] = None              # app role: student / educator / admin
    group_role: Optional[str] = None        # in a study group: owner / moderator / member
    avatar_path: Optional[str] = None
    is_me: bool = False
    mention: Optional[str] = None            # what to type after @ in a group chat (migration 046)

    @classmethod
    def from_json(cls, d: Optional[dict]) -> "Person":
        d = d or {}
        return cls(id=str(d.get("id") or ""), name=d.get("name") or "Akeso student",
                   handle=d.get("handle"), program=d.get("program"), role=d.get("role"),
                   group_role=d.get("group_role"), avatar_path=d.get("avatar_path") or None,
                   is_me=bool(d.get("is_me")), mention=d.get("mention") or None)

    @property
    def label(self) -> str:
        return f"{self.name} (@{self.handle})" if self.handle else self.name

    @property
    def badge(self) -> str:
        """Group role first (Owner, Moderator), then an app role (Educator)."""
        if self.group_role in ("owner", "moderator"):
            return GROUP_ROLE_LABELS[self.group_role]
        return APP_ROLE_LABELS.get(self.role or "", "")


# ------------------------------------------------------------------ friends

@dataclass
class Friend:
    person: Person
    since: Optional[datetime] = None

    @classmethod
    def from_json(cls, d: dict) -> "Friend":
        return cls(person=Person.from_json(d), since=parse_time(d.get("since")))


@dataclass
class IncomingRequest:
    person: Person
    requested_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, d: dict) -> "IncomingRequest":
        return cls(person=Person.from_json(d), requested_at=parse_time(d.get("requested_at")))


@dataclass
class SentRequest:
    """A handle I asked, exactly as typed: the server never says whether it
    exists, so neither can the app."""
    request_id: int
    handle: str
    requested_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, d: dict) -> "SentRequest":
        return cls(request_id=int(d.get("request_id") or 0), handle=d.get("handle") or "",
                   requested_at=parse_time(d.get("requested_at")))


@dataclass
class FriendRequests:
    incoming: list[IncomingRequest] = field(default_factory=list)
    sent: list[SentRequest] = field(default_factory=list)

    @classmethod
    def from_json(cls, d: Optional[dict]) -> "FriendRequests":
        d = d or {}
        return cls(incoming=[IncomingRequest.from_json(x) for x in d.get("incoming") or []],
                   sent=[SentRequest.from_json(x) for x in d.get("sent") or []])


@dataclass
class BlockedPerson:
    id: str
    name: str
    blocked_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, d: dict) -> "BlockedPerson":
        return cls(id=str(d.get("id") or ""), name=d.get("name") or "Akeso student",
                   blocked_at=parse_time(d.get("blocked_at")))


# Friend state of a profile, for its buttons (friend_status).
FRIEND_NONE, FRIENDS, REQUEST_SENT, REQUEST_RECEIVED, BLOCKED = (
    "none", "friends", "sent", "received", "blocked")


# ------------------------------------------------------------ shared notes

@dataclass
class SharedNote:
    """A note shared with me (or one of mine, in Manage sharing)."""
    id: str
    title: str
    kind: str = "note"
    owner: Person = field(default_factory=lambda: Person("", "Akeso student"))
    is_mine: bool = False
    body: str = ""
    source_item_id: Optional[str] = None
    opened: bool = False
    shared_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    recipients: list[Person] = field(default_factory=list)

    @classmethod
    def from_json(cls, d: Optional[dict]) -> "SharedNote":
        d = d or {}
        return cls(id=str(d.get("id") or ""), title=d.get("title") or "Untitled note",
                   kind=d.get("kind") or "note", owner=Person.from_json(d.get("owner")),
                   is_mine=bool(d.get("is_mine")), body=d.get("body") or "",
                   source_item_id=d.get("source_item_id"), opened=bool(d.get("opened")),
                   shared_at=parse_time(d.get("shared_at") or d.get("created_at")),
                   updated_at=parse_time(d.get("updated_at")),
                   recipients=[Person.from_json(r) for r in d.get("recipients") or []])


# ------------------------------------------------------------ study groups

@dataclass
class StudyGroup:
    id: str
    name: str
    description: str = ""
    visibility: str = "public"
    topic: str = ""
    body_system_id: Optional[str] = None
    members: int = 0
    my_role: Optional[str] = None
    owner: Optional[Person] = None
    unread: int = 0
    muted: bool = False
    can_join: bool = False
    last_message_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    members_list: list[Person] = field(default_factory=list)
    blocked_ids: set = field(default_factory=set)
    invite_link: Optional[dict] = None          # {id, created_at, expires_at, uses}
    pending_invites: list[Person] = field(default_factory=list)

    @classmethod
    def from_json(cls, d: Optional[dict]) -> "StudyGroup":
        d = d or {}
        members_list = [Person.from_json(m) for m in d.get("members_list") or []]
        return cls(
            id=str(d.get("id") or ""), name=d.get("name") or "Study group",
            description=d.get("description") or "", visibility=d.get("visibility") or "public",
            topic=d.get("topic") or "", body_system_id=d.get("body_system_id"),
            members=int(d.get("members") or 0), my_role=d.get("my_role"),
            owner=Person.from_json(d["owner"]) if d.get("owner") else None,
            unread=int(d.get("unread") or 0), muted=bool(d.get("muted")),
            can_join=bool(d.get("can_join")), last_message_at=parse_time(d.get("last_message_at")),
            created_at=parse_time(d.get("created_at")), members_list=members_list,
            blocked_ids={str(m.get("id")) for m in d.get("members_list") or [] if m.get("blocked")},
            invite_link=d.get("invite_link"),
            pending_invites=[Person.from_json(p) for p in d.get("pending_invites") or []])

    @property
    def is_member(self) -> bool:
        return self.my_role is not None

    @property
    def is_staff(self) -> bool:
        return self.my_role in ("owner", "moderator")

    @property
    def is_private(self) -> bool:
        return self.visibility == "private"

    @property
    def full(self) -> bool:
        return self.members >= GROUP_MEMBER_CAP


@dataclass
class GroupMessage:
    id: int
    body: str
    author: Person
    status: str = "open"
    is_mine: bool = False
    created_at: Optional[datetime] = None
    attachment: Optional[str] = None          # storage path of a picture (migration 045)

    @classmethod
    def from_json(cls, d: dict) -> "GroupMessage":
        return cls(id=int(d.get("id") or 0), body=d.get("body") or "",
                   author=Person.from_json(d.get("author")), status=d.get("status") or "open",
                   is_mine=bool(d.get("is_mine")), created_at=parse_time(d.get("created_at")),
                   attachment=d.get("attachment") or None)

    @property
    def hidden(self) -> bool:
        return self.status == "hidden"


@dataclass
class GroupNote:
    id: str
    title: str
    kind: str = "note"
    owner: Person = field(default_factory=lambda: Person("", "Akeso student"))
    is_mine: bool = False
    status: str = "open"
    body: str = ""
    updated_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, d: dict) -> "GroupNote":
        return cls(id=str(d.get("id") or ""), title=d.get("title") or "Untitled note",
                   kind=d.get("kind") or "note", owner=Person.from_json(d.get("owner")),
                   is_mine=bool(d.get("is_mine")), status=d.get("status") or "open",
                   body=d.get("body") or "", updated_at=parse_time(d.get("updated_at")))


@dataclass
class GroupInvite:
    invite_id: str
    group: StudyGroup
    inviter: Person
    invited_at: Optional[datetime] = None

    @classmethod
    def from_json(cls, d: dict) -> "GroupInvite":
        return cls(invite_id=str(d.get("invite_id") or ""), group=StudyGroup.from_json(d.get("group")),
                   inviter=Person.from_json(d.get("from")), invited_at=parse_time(d.get("invited_at")))


@dataclass
class GroupReport:
    """One reported item, for app educators and admins (reported content only)."""
    group_id: str
    group_name: str
    target_kind: str
    target_id: str
    reports: int
    reasons: list[str]
    excerpt: str
    author: Person

    @classmethod
    def from_json(cls, d: dict) -> "GroupReport":
        return cls(group_id=str(d.get("group_id") or ""), group_name=d.get("group_name") or "",
                   target_kind=d.get("target_kind") or "message",
                   target_id=str(d.get("target_id") or ""), reports=int(d.get("reports") or 0),
                   reasons=list(d.get("reasons") or []), excerpt=d.get("excerpt") or "",
                   author=Person.from_json(d.get("author")))
