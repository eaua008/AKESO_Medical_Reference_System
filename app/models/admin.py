"""Admin Control Panel data: accounts, content rows, the audit trail.

Plain data, built from what the admin_* database functions return
(migration 004). Labels for roles, severities and so on live here too, so
the screens and the editors agree on them.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.models.account import parse_time

# ---------------------------------------------------------------- roles

# (value, label, what it allows) — the order the role picker shows.
ROLES = [
    ("admin", "Administrator",
     "Full access: User Management, Content Management (disease, symptom and "
     "medicine editing) and the audit trail."),
    ("educator", "Educator",
     "Moderates Clinical Exchange (reports queue, hide / lock / remove) and "
     "verifies replies. Everything a student can do."),
    ("student", "Student",
     "The learning view: encyclopedias, checkers, notebook and Clinical Exchange."),
]
ROLE_LABELS = {value: label for value, label, _ in ROLES}

STATUS_LABELS = {"active": "Active", "suspended": "Suspended", "deleting": "Deletion pending"}

# ---------------------------------------------------------- content enums

SEVERITIES = ["Mild", "Moderate", "Severe", "Critical"]
URGENCIES = [
    ("", "Not set"),
    ("SELF_CARE", "Self-care"),
    ("SEE_DOCTOR_SOON", "See a doctor soon"),
    ("SEEK_URGENT_CARE", "Seek urgent care"),
    ("EMERGENCY", "Emergency"),
]
URGENCY_LABELS = dict(URGENCIES)
CATEGORIES = [("Prescription", "Prescription (Rx)"), ("OTC", "Over-the-counter (OTC)")]
SAFETY = [("safe", "Safe"), ("caution", "Caution"), ("avoid", "Avoid")]
PREVENTION_TIERS = [("primary", "Primary prevention"), ("secondary", "Secondary prevention"),
                    ("tertiary", "Tertiary prevention"), ("", "General (no tier)")]
# medicine_facts kinds the app reads, with their editor captions
MEDICINE_FACTS = [
    ("brand_ph", "Philippine brands"),
    ("brand_intl", "International brands"),
    ("indication", "Indications"),
    ("adverse", "Adverse effects"),
    ("contraindication", "Contraindications"),
    ("interaction", "Interactions"),
]

KINDS = ("disease", "symptom", "medicine", "article")
KIND_LABELS = {"disease": "Disease", "symptom": "Symptom", "medicine": "Medicine",
               "article": "Article", "user": "Account"}
# New ids follow the seed data: diseases plain, symptoms sym_..., medicines med_...
ID_PREFIX = {"disease": "", "symptom": "sym_", "medicine": "med_", "article": "art_"}
# Health Articles (migration 005)
ARTICLE_KINDS = [("written", "Akeso article (written here)"),
                 ("external", "External link (curated source)")]
ARTICLE_CATEGORIES = ["General", "Infectious disease", "Nutrition", "Mental health",
                      "Maternal & child health", "First aid", "Medicines", "Prevention",
                      "Chronic disease"]

ACTION_LABELS = {
    "create": "Created", "update": "Edited", "archive": "Archived", "restore": "Restored",
    "role": "Changed role", "suspend": "Suspended", "reactivate": "Reactivated",
    "delete_user": "Deleted account",
}


def slug(name: str, kind: str) -> str:
    """A suggested id from a name: "Dengue Fever" -> "dengue_fever"."""
    import re
    base = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")[:50]
    prefix = ID_PREFIX.get(kind, "")
    if base.startswith(prefix):
        prefix = ""
    return (prefix + base)[:60]


# -------------------------------------------------------------- accounts

@dataclass
class AdminUser:
    id: str
    email: str
    display_name: str
    handle: Optional[str]
    role: str
    created_at: Optional[datetime]
    last_sign_in_at: Optional[datetime]
    suspended: bool
    suspended_reason: str
    deletion_scheduled_for: Optional[datetime]
    registry_id: str
    is_me: bool

    @classmethod
    def from_row(cls, row: dict) -> "AdminUser":
        return cls(
            id=str(row["id"]), email=row.get("email") or "",
            display_name=row.get("display_name") or "", handle=row.get("handle"),
            role=row.get("role") or "student",
            created_at=parse_time(row.get("created_at")),
            last_sign_in_at=parse_time(row.get("last_sign_in_at")),
            suspended=bool(row.get("suspended")),
            suspended_reason=row.get("suspended_reason") or "",
            deletion_scheduled_for=parse_time(row.get("deletion_scheduled_for")),
            registry_id=row.get("registry_id") or "", is_me=bool(row.get("is_me")))

    @property
    def status(self) -> str:
        if self.deletion_scheduled_for is not None:
            return "deleting"
        return "suspended" if self.suspended else "active"

    @property
    def role_label(self) -> str:
        return ROLE_LABELS.get(self.role, self.role.title())

    @property
    def initial(self) -> str:
        return (self.display_name or self.email or "?")[:1].upper()

    def matches(self, query: str) -> bool:
        query = query.strip().lower()
        if not query:
            return True
        return any(query in (text or "").lower()
                   for text in (self.display_name, self.email, self.handle, self.registry_id))


@dataclass
class UserStats:
    total: int = 0
    active: int = 0
    suspended: int = 0
    admins: int = 0
    educators: int = 0
    students: int = 0

    @classmethod
    def of(cls, users: list[AdminUser]) -> "UserStats":
        return cls(
            total=len(users),
            active=sum(1 for u in users if u.status == "active"),
            suspended=sum(1 for u in users if u.status == "suspended"),
            admins=sum(1 for u in users if u.role == "admin"),
            educators=sum(1 for u in users if u.role == "educator"),
            students=sum(1 for u in users if u.role == "student"))


@dataclass
class UserDetail:
    user: AdminUser
    program: Optional[str] = None
    school: Optional[str] = None
    year_level: Optional[int] = None
    school_email_domain: Optional[str] = None
    school_email_verified_at: Optional[datetime] = None
    role_granted_at: Optional[datetime] = None
    role_granted_by: str = ""
    suspended_at: Optional[datetime] = None
    device_count: int = 0
    recent_events: list[dict] = field(default_factory=list)

    @classmethod
    def from_row(cls, row: dict) -> "UserDetail":
        return cls(
            user=AdminUser.from_row(row),
            program=row.get("program"), school=row.get("school"),
            year_level=row.get("year_level"),
            school_email_domain=row.get("school_email_domain"),
            school_email_verified_at=parse_time(row.get("school_email_verified_at")),
            role_granted_at=parse_time(row.get("role_granted_at")),
            role_granted_by=row.get("role_granted_by") or "",
            suspended_at=parse_time(row.get("suspended_at")),
            device_count=int(row.get("device_count") or 0),
            recent_events=[dict(e, at=parse_time(e.get("at")))
                           for e in row.get("recent_events") or []])


# --------------------------------------------------------------- content

@dataclass
class ContentItem:
    """One row of a Content Management table (any of the three kinds)."""

    kind: str
    id: str
    name: str
    subtitle: str = ""
    body_system_id: Optional[str] = None
    body_system: str = ""
    severity: str = ""
    urgency: Optional[str] = None
    category: str = ""
    drug_class: str = ""
    is_red_flag: bool = False
    weight: int = 0
    black_box: bool = False
    count: int = 0             # symptoms (disease) / linked diseases (symptom, medicine)
    primary_count: int = 0
    published: bool = True
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, kind: str, row: dict) -> "ContentItem":
        common = dict(kind=kind, id=row["id"], name=row.get("name") or "",
                      published=row.get("published", True) is not False,
                      updated_at=parse_time(row.get("updated_at")))
        if kind == "disease":
            return cls(**common, subtitle=row.get("scientific_name") or "",
                       body_system_id=row.get("body_system_id"),
                       body_system=row.get("body_system") or "",
                       severity=row.get("severity") or "", urgency=row.get("urgency"),
                       count=int(row.get("symptom_count") or 0),
                       primary_count=int(row.get("primary_count") or 0))
        if kind == "article":
            return cls(**common, subtitle=row.get("source_name") or "",
                       category=row.get("kind") or "written",
                       drug_class=row.get("category") or "General",
                       count=int(row.get("link_count") or 0))
        if kind == "symptom":
            return cls(**common, subtitle=row.get("scientific_name") or "",
                       body_system_id=row.get("body_system_id"),
                       body_system=row.get("body_system") or "",
                       is_red_flag=bool(row.get("is_red_flag")),
                       weight=int(row.get("diagnostic_weight") or 0),
                       count=int(row.get("disease_count") or 0))
        return cls(**common, subtitle=row.get("generic_name") or "",
                   drug_class=row.get("drug_class") or "",
                   category=row.get("category") or "", black_box=bool(row.get("black_box")),
                   count=int(row.get("disease_count") or 0))

    def matches(self, query: str) -> bool:
        query = query.strip().lower()
        if not query:
            return True
        return any(query in (text or "").lower()
                   for text in (self.name, self.subtitle, self.id, self.body_system,
                                self.drug_class))


@dataclass
class AuditEntry:
    id: int
    actor_label: str
    action: str
    target_kind: str
    target_id: str
    target_label: str
    detail: dict
    created_at: Optional[datetime]

    @classmethod
    def from_row(cls, row: dict) -> "AuditEntry":
        return cls(id=int(row["id"]), actor_label=row.get("actor_label") or "Someone",
                   action=row.get("action") or "", target_kind=row.get("target_kind") or "",
                   target_id=row.get("target_id") or "",
                   target_label=row.get("target_label") or "",
                   detail=row.get("detail") or {}, created_at=parse_time(row.get("created_at")))

    @property
    def action_label(self) -> str:
        return ACTION_LABELS.get(self.action, self.action.replace("_", " ").title())

    @property
    def summary(self) -> str:
        if self.action == "role":
            old = ROLE_LABELS.get(self.detail.get("from"), self.detail.get("from"))
            new = ROLE_LABELS.get(self.detail.get("to"), self.detail.get("to"))
            return f"{old} → {new}"
        if self.action == "suspend" and self.detail.get("reason"):
            return f"Reason: {self.detail['reason']}"
        return ""
