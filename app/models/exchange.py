"""Domain models for Clinical Exchange (the case discussion board).

Plain dataclasses built from the JSON the database functions return
(migration 003). from_json() is the only place those field names appear.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.models.account import PROGRAM_LABELS, parse_time

CASE, QUESTION = "case", "question"
KIND_LABELS = {CASE: "Case", QUESTION: "Question"}

# Feed tabs: (key, label)
FEED_TABS = [("newest", "Newest"), ("active", "Most active"), ("unanswered", "Unanswered"),
             ("following", "Following"), ("mine", "My posts")]

TAG_KINDS = {"disease": "Disease", "symptom": "Symptom", "medicine": "Medicine",
             "body_system": "Body system", "topic": "Topic"}

REPORT_REASONS = [
    ("patient_data", "Looks like real patient information"),
    ("misinformation", "Medically wrong or dangerous"),
    ("harassment", "Rude, harassing or hateful"),
    ("spam", "Spam or advertising"),
    ("off_topic", "Off topic"),
    ("other", "Something else"),
]

SETTINGS = ["Outpatient clinic", "Emergency department", "Inpatient ward", "Community"]

STATUS_LABELS = {"open": "", "locked": "Locked", "hidden": "Hidden by a moderator",
                 "removed": "Removed by a moderator"}

NOTIFICATION_KINDS = {
    "reply": ("message-circle", "New reply"),
    "best_answer": ("badge-check", "Best answer"),
    "verified": ("shield-check", "Educator verified"),
    "reveal": ("sparkles", "Answer revealed"),
    "moderation": ("shield-alert", "Moderation"),
    "mention": ("at-sign", "Mention"),
}


def time_ago(value: Optional[datetime]) -> str:
    if value is None:
        return ""
    from datetime import timezone
    seconds = (datetime.now(timezone.utc) - value).total_seconds()
    if seconds < 60:
        return "just now"
    for size, unit in ((86400 * 365, "y"), (86400 * 30, "mo"), (86400 * 7, "w"),
                       (86400, "d"), (3600, "h"), (60, "m")):
        if seconds >= size:
            return f"{int(seconds // size)}{unit} ago"
    return "just now"


@dataclass
class Author:
    name: str
    anonymous: bool = False
    handle: Optional[str] = None
    program: Optional[str] = None
    verified_domain: Optional[str] = None
    role: Optional[str] = None
    is_me: bool = False

    @classmethod
    def from_json(cls, data: Optional[dict]) -> "Author":
        data = data or {}
        return cls(name=data.get("name") or "Akeso student",
                   anonymous=bool(data.get("anonymous")), handle=data.get("handle"),
                   program=data.get("program"), verified_domain=data.get("verified_domain"),
                   role=data.get("role"), is_me=bool(data.get("is_me")))

    @property
    def program_label(self) -> str:
        return PROGRAM_LABELS.get(self.program or "", "")

    @property
    def is_educator(self) -> bool:
        return self.role in ("educator", "admin")


@dataclass
class Tag:
    kind: str
    id: str
    label: str

    @classmethod
    def from_json(cls, data: dict) -> "Tag":
        return cls(kind=data.get("kind", "topic"), id=str(data.get("id", "")),
                   label=data.get("label") or str(data.get("id", "")))

    def to_json(self) -> dict:
        return {"kind": self.kind, "id": self.id, "label": self.label}


@dataclass
class FeedPost:
    id: str
    kind: str
    title: str
    excerpt: str
    author: Author
    status: str
    has_poll: bool
    revealed: bool
    has_best: bool
    reply_count: int
    score: int
    age_range: Optional[str]
    sex: Optional[str]
    source: Optional[str]
    created_at: Optional[datetime]
    last_activity_at: Optional[datetime]
    voted: bool
    following: bool
    tags: list[Tag] = field(default_factory=list)

    @classmethod
    def from_json(cls, d: dict) -> "FeedPost":
        return cls(id=d["id"], kind=d.get("kind", QUESTION), title=d.get("title", ""),
                   excerpt=d.get("excerpt") or "", author=Author.from_json(d.get("author")),
                   status=d.get("status", "open"), has_poll=bool(d.get("has_poll")),
                   revealed=bool(d.get("revealed")), has_best=bool(d.get("has_best")),
                   reply_count=int(d.get("reply_count") or 0), score=int(d.get("score") or 0),
                   age_range=d.get("age_range"), sex=d.get("sex"), source=d.get("source"),
                   created_at=parse_time(d.get("created_at")),
                   last_activity_at=parse_time(d.get("last_activity_at")),
                   voted=bool(d.get("voted")), following=bool(d.get("following")),
                   tags=[Tag.from_json(t) for t in d.get("tags") or []])


@dataclass
class PollOption:
    id: str
    label: str
    disease_id: Optional[str]
    by_author: bool
    votes: Optional[int]          # None while results are hidden

    @classmethod
    def from_json(cls, d: dict) -> "PollOption":
        votes = d.get("votes")
        return cls(id=d["id"], label=d.get("label", ""), disease_id=d.get("disease_id"),
                   by_author=bool(d.get("by_author")),
                   votes=None if votes is None else int(votes))


@dataclass
class Poll:
    options: list[PollOption]
    my_option: Optional[str]
    show_results: bool
    revealed_option: Optional[str]
    explanation: Optional[str]
    total: Optional[int]

    @classmethod
    def from_json(cls, d: Optional[dict]) -> Optional["Poll"]:
        if not d:
            return None
        total = d.get("total")
        return cls(options=[PollOption.from_json(o) for o in d.get("options") or []],
                   my_option=d.get("my_option"), show_results=bool(d.get("show_results")),
                   revealed_option=d.get("revealed_option"), explanation=d.get("explanation"),
                   total=None if total is None else int(total))

    @property
    def revealed(self) -> bool:
        return self.revealed_option is not None

    def label_for(self, option_id: Optional[str]) -> str:
        return next((o.label for o in self.options if o.id == option_id), "")


@dataclass
class Reply:
    id: str
    parent_id: Optional[str]
    body: str
    status: str
    author: Author
    score: int
    created_at: Optional[datetime]
    edited_at: Optional[datetime]
    voted: bool
    is_best: bool
    verified: bool
    voted_label: Optional[str]      # their poll vote when they wrote this
    current_label: Optional[str]    # their poll vote now
    is_mine: bool
    children: list["Reply"] = field(default_factory=list)

    @classmethod
    def from_json(cls, d: dict) -> "Reply":
        return cls(id=d["id"], parent_id=d.get("parent_id"), body=d.get("body") or "",
                   status=d.get("status", "open"), author=Author.from_json(d.get("author")),
                   score=int(d.get("score") or 0), created_at=parse_time(d.get("created_at")),
                   edited_at=parse_time(d.get("edited_at")), voted=bool(d.get("voted")),
                   is_best=bool(d.get("is_best")), verified=bool(d.get("verified")),
                   voted_label=d.get("voted_label"), current_label=d.get("current_label"),
                   is_mine=bool(d.get("is_mine")))


@dataclass
class PostDetail:
    id: str
    kind: str
    title: str
    body: str
    question: str
    author: Author
    is_anonymous: bool
    age_range: Optional[str]
    sex: Optional[str]
    setting: Optional[str]
    vitals: dict
    case_data: dict
    source: Optional[str]
    status: str
    score: int
    reply_count: int
    created_at: Optional[datetime]
    edited_at: Optional[datetime]
    best_reply_id: Optional[str]
    voted: bool
    following: bool
    is_author: bool
    can_moderate: bool
    tags: list[Tag]
    poll: Optional[Poll]
    replies: list[Reply]            # top level, each with .children

    @classmethod
    def from_json(cls, d: dict) -> "PostDetail":
        flat = [Reply.from_json(r) for r in d.get("replies") or []]
        by_id = {r.id: r for r in flat}
        top: list[Reply] = []
        for reply in flat:
            parent = by_id.get(reply.parent_id or "")
            (parent.children if parent else top).append(reply)
        return cls(id=d["id"], kind=d.get("kind", QUESTION), title=d.get("title", ""),
                   body=d.get("body") or "", question=d.get("question") or "",
                   author=Author.from_json(d.get("author")),
                   is_anonymous=bool(d.get("is_anonymous")), age_range=d.get("age_range"),
                   sex=d.get("sex"), setting=d.get("setting"), vitals=d.get("vitals") or {},
                   case_data=d.get("case_data") or {}, source=d.get("source"),
                   status=d.get("status", "open"), score=int(d.get("score") or 0),
                   reply_count=int(d.get("reply_count") or 0),
                   created_at=parse_time(d.get("created_at")),
                   edited_at=parse_time(d.get("edited_at")),
                   best_reply_id=d.get("best_reply_id"), voted=bool(d.get("voted")),
                   following=bool(d.get("following")), is_author=bool(d.get("is_author")),
                   can_moderate=bool(d.get("can_moderate")),
                   tags=[Tag.from_json(t) for t in d.get("tags") or []],
                   poll=Poll.from_json(d.get("poll")), replies=top)

    @property
    def is_open(self) -> bool:
        return self.status == "open"

    def all_replies(self) -> list[Reply]:
        out = []
        for reply in self.replies:
            out.append(reply)
            out.extend(reply.children)
        return out


@dataclass
class Notification:
    id: int
    kind: str
    post_id: Optional[str]
    reply_id: Optional[str]
    message: str
    created_at: Optional[datetime]
    read: bool

    @classmethod
    def from_json(cls, d: dict) -> "Notification":
        return cls(id=int(d["id"]), kind=d.get("kind", "reply"), post_id=d.get("post_id"),
                   reply_id=d.get("reply_id"), message=d.get("message", ""),
                   created_at=parse_time(d.get("created_at")), read=bool(d.get("read")))

    @property
    def icon(self) -> str:
        return NOTIFICATION_KINDS.get(self.kind, ("bell", ""))[0]

    @property
    def kind_label(self) -> str:
        return NOTIFICATION_KINDS.get(self.kind, ("", "Notice"))[1]


@dataclass
class ModItem:
    target_kind: str
    target_id: str
    reports: int
    reasons: list[str]
    notes: list[str]
    post_id: Optional[str]
    title: str
    excerpt: str
    status: str
    author: Author
    first_reported: Optional[datetime]

    @classmethod
    def from_json(cls, d: dict) -> "ModItem":
        return cls(target_kind=d.get("target_kind", "post"), target_id=d["target_id"],
                   reports=int(d.get("reports") or 0), reasons=list(d.get("reasons") or []),
                   notes=[n for n in d.get("notes") or [] if n], post_id=d.get("post_id"),
                   title=d.get("title") or "", excerpt=d.get("excerpt") or "",
                   status=d.get("status") or "open", author=Author.from_json(d.get("author")),
                   first_reported=parse_time(d.get("first_reported")))


@dataclass
class ProfileCard:
    handle: str
    display_name: str
    bio: str
    program: Optional[str]
    school: Optional[str]
    verified_domain: Optional[str]
    year_level: Optional[int]
    role: Optional[str]
    posts: int
    replies: int
    best_answers: int
    verified_answers: int
    member_since: Optional[datetime]
    avatar_path: Optional[str]

    @classmethod
    def from_json(cls, d: dict) -> "ProfileCard":
        return cls(handle=d.get("handle") or "", display_name=d.get("display_name") or "",
                   bio=d.get("bio") or "", program=d.get("program"), school=d.get("school"),
                   verified_domain=d.get("verified_school_domain"),
                   year_level=d.get("year_level"), role=d.get("role"),
                   posts=int(d.get("posts") or 0), replies=int(d.get("replies") or 0),
                   best_answers=int(d.get("best_answers") or 0),
                   verified_answers=int(d.get("verified_answers") or 0),
                   member_since=parse_time(d.get("member_since")),
                   avatar_path=d.get("avatar_path"))


@dataclass
class Draft:
    """What the composer collects before it is posted."""

    kind: str = CASE
    title: str = ""
    body: str = ""
    question: str = ""
    anonymous: bool = False
    age_range: Optional[str] = None
    sex: Optional[str] = None
    setting: Optional[str] = None
    vitals: Optional[dict] = None
    case_data: dict = field(default_factory=dict)
    source: Optional[str] = None
    tags: list[Tag] = field(default_factory=list)
    poll_options: list[dict] = field(default_factory=list)   # {"disease_id", "label"}
    attached_from: str = ""     # notebook item title, shown in the composer
