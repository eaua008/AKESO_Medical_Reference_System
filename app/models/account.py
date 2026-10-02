"""Domain models for the Account module.

Plain dataclasses. Like User, they know nothing about Supabase beyond the
from_row() translators, which are the only place its column names appear.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

# Bump when the Terms or Privacy Notice text changes (app/core/legal_text.py).
# Everyone is asked to accept the new version at their next sign-in.
TERMS_VERSION = "2026-09"
PRIVACY_VERSION = "2026-09"

DELETION_GRACE_DAYS = 30

PROGRAMS: list[tuple[str, str]] = [
    ("medicine", "Medicine"),
    ("nursing", "Nursing"),
    ("pharmacy", "Pharmacy"),
    ("medical_technology", "Medical Technology"),
    ("physical_therapy", "Physical Therapy"),
    ("midwifery", "Midwifery"),
    ("dentistry", "Dentistry"),
    ("public_health", "Public Health"),
    ("radiologic_technology", "Radiologic Technology"),
    ("nutrition", "Nutrition & Dietetics"),
    ("other", "Other health program"),
]
PROGRAM_LABELS = dict(PROGRAMS)

YEAR_LEVELS: list[tuple[int, str]] = [
    (1, "1st year"), (2, "2nd year"), (3, "3rd year"), (4, "4th year"),
    (5, "5th year"), (6, "6th year"), (7, "Internship"), (8, "Graduate / Board review"),
]
YEAR_LABELS = dict(YEAR_LEVELS)

INTEREST_OPTIONS = [
    "Cardiology", "Pulmonology", "Infectious disease", "Pediatrics",
    "Obstetrics & gynecology", "Surgery", "Emergency medicine", "Pharmacology",
    "Neurology", "Endocrinology", "Gastroenterology", "Nephrology",
    "Psychiatry", "Dermatology", "Community health", "Nutrition",
]
MAX_INTERESTS = 10

ROLE_LABELS = {"student": "Student", "educator": "Educator", "admin": "Admin"}

# Activity log: label and tone ("good", "warn", "danger", "info") per kind.
EVENT_LABELS: dict[str, tuple[str, str]] = {
    "sign_in": ("Signed in", "info"),
    "sign_out": ("Signed out", "info"),
    "sign_out_others": ("Signed out all other devices", "warn"),
    "password_changed": ("Password changed", "warn"),
    "password_check_failed": ("Wrong current password entered", "danger"),
    "email_change_requested": ("Email change requested", "warn"),
    "email_changed": ("Email address changed", "warn"),
    "mfa_enabled": ("Two-factor authentication turned on", "good"),
    "mfa_disabled": ("Two-factor authentication turned off", "danger"),
    "mfa_challenge_failed": ("Wrong two-factor code entered", "danger"),
    "device_forgotten": ("Device removed from the list", "info"),
    "profile_updated": ("Profile updated", "info"),
    "data_exported": ("Account data exported", "warn"),
    "deletion_requested": ("Account deletion requested", "danger"),
    "deletion_cancelled": ("Account deletion cancelled", "good"),
    "school_email_verified": ("School email verified", "good"),
    "role_changed": ("Role changed", "warn"),
    "consent_accepted": ("Terms and Privacy Notice accepted", "info"),
}

ACTIVITY_FIELDS: list[tuple[str, str]] = [
    ("diseases_viewed", "Diseases studied"),
    ("symptoms_viewed", "Symptoms looked up"),
    ("medicines_viewed", "Medicines reviewed"),
    ("notebook_edits", "Notebook saves"),
    ("checker_runs", "Symptom checker runs"),
    ("interaction_checks", "Interaction checks"),
]


def parse_time(value) -> Optional[datetime]:
    """Supabase timestamps arrive as ISO strings (sometimes with a 'Z')."""
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def friendly_time(value: Optional[datetime], with_time: bool = True) -> str:
    if value is None:
        return "—"
    local = value.astimezone()
    text = local.strftime("%b %d, %Y").replace(" 0", " ")
    if with_time:
        text += " · " + local.strftime("%I:%M %p").lstrip("0")
    return text


@dataclass
class Profile:
    id: str
    display_name: str = ""
    handle: Optional[str] = None
    bio: str = ""
    avatar_path: Optional[str] = None
    program: Optional[str] = None
    school: Optional[str] = None
    year_level: Optional[int] = None
    interests: list[str] = field(default_factory=list)
    is_public: bool = False
    show_school: bool = True
    show_program: bool = True
    track_study_activity: bool = True
    school_email_domain: Optional[str] = None
    school_email_verified_at: Optional[datetime] = None
    deletion_requested_at: Optional[datetime] = None
    deletion_scheduled_for: Optional[datetime] = None
    created_at: Optional[datetime] = None
    # set by an admin (migration 004); a suspended account cannot sign in
    suspended_at: Optional[datetime] = None
    suspended_reason: str = ""

    # Columns the app may change (the database refuses the rest anyway).
    EDITABLE = ("display_name", "handle", "bio", "avatar_path", "program", "school",
                "year_level", "interests", "is_public", "show_school", "show_program",
                "track_study_activity")

    @classmethod
    def from_row(cls, row: dict) -> "Profile":
        return cls(
            id=row["id"],
            display_name=row.get("display_name") or "",
            handle=row.get("handle"),
            bio=row.get("bio") or "",
            avatar_path=row.get("avatar_path"),
            program=row.get("program"),
            school=row.get("school"),
            year_level=row.get("year_level"),
            interests=list(row.get("interests") or []),
            is_public=bool(row.get("is_public")),
            show_school=row.get("show_school", True) is not False,
            show_program=row.get("show_program", True) is not False,
            track_study_activity=row.get("track_study_activity", True) is not False,
            school_email_domain=row.get("school_email_domain"),
            school_email_verified_at=parse_time(row.get("school_email_verified_at")),
            deletion_requested_at=parse_time(row.get("deletion_requested_at")),
            deletion_scheduled_for=parse_time(row.get("deletion_scheduled_for")),
            created_at=parse_time(row.get("created_at")),
            suspended_at=parse_time(row.get("suspended_at")),
            suspended_reason=row.get("suspended_reason") or "",
        )

    @property
    def program_label(self) -> str:
        return PROGRAM_LABELS.get(self.program or "", "")

    @property
    def year_label(self) -> str:
        return YEAR_LABELS.get(self.year_level or 0, "")

    @property
    def is_verified_student(self) -> bool:
        return self.school_email_verified_at is not None

    @property
    def deletion_pending(self) -> bool:
        return self.deletion_scheduled_for is not None


@dataclass
class Device:
    id: str
    device_name: str
    platform: str
    app_version: str
    first_seen: Optional[datetime]
    last_seen: Optional[datetime]
    is_current: bool
    is_active: Optional[bool]       # None: the server could not tell

    @classmethod
    def from_row(cls, row: dict) -> "Device":
        return cls(
            id=row["id"], device_name=row.get("device_name") or "Unknown computer",
            platform=row.get("platform") or "", app_version=row.get("app_version") or "",
            first_seen=parse_time(row.get("first_seen")), last_seen=parse_time(row.get("last_seen")),
            is_current=bool(row.get("is_current")), is_active=row.get("is_active"),
        )


@dataclass
class SecurityEvent:
    id: int
    kind: str
    device_name: str
    detail: dict
    created_at: Optional[datetime]

    @classmethod
    def from_row(cls, row: dict) -> "SecurityEvent":
        return cls(id=row["id"], kind=row["kind"], device_name=row.get("device_name") or "",
                   detail=row.get("detail") or {}, created_at=parse_time(row.get("created_at")))

    @property
    def label(self) -> str:
        return EVENT_LABELS.get(self.kind, (self.kind.replace("_", " ").capitalize(), "info"))[0]

    @property
    def tone(self) -> str:
        return EVENT_LABELS.get(self.kind, ("", "info"))[1]

    @property
    def note(self) -> str:
        """A short second line from the detail, without anything sensitive."""
        d = self.detail
        if self.kind == "email_changed":
            return f"{d.get('from_domain', '?')} → {d.get('to_domain', '?')}"
        if self.kind == "email_change_requested":
            return f"to an address at {d.get('to_domain', '?')}"
        if self.kind == "role_changed":
            return f"{ROLE_LABELS.get(d.get('from'), d.get('from'))} → " \
                   f"{ROLE_LABELS.get(d.get('to'), d.get('to'))}"
        if self.kind == "school_email_verified":
            return d.get("domain", "")
        if self.kind == "deletion_requested":
            when = parse_time(d.get("scheduled_for"))
            return f"scheduled for {friendly_time(when, with_time=False)}" if when else ""
        if self.kind == "profile_updated" and d.get("fields"):
            return ", ".join(str(f).replace("_", " ") for f in d["fields"][:5])
        if self.kind == "consent_accepted":
            return f"version {d.get('terms', '')}"
        return ""


@dataclass
class Consent:
    document: str
    version: str
    accepted_at: Optional[datetime]

    @classmethod
    def from_row(cls, row: dict) -> "Consent":
        return cls(row["document"], row["version"], parse_time(row.get("accepted_at")))


@dataclass
class ActivitySummary:
    streak: int = 0
    active_days_30: int = 0
    week: dict = field(default_factory=dict)
    all_time: dict = field(default_factory=dict)
    last_14_days: list[tuple[date, int]] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: Optional[dict]) -> "ActivitySummary":
        data = data or {}
        days = []
        for item in data.get("last_14_days") or []:
            try:
                days.append((date.fromisoformat(str(item["day"])[:10]), int(item["total"])))
            except (KeyError, ValueError, TypeError):
                continue
        return cls(streak=int(data.get("streak") or 0),
                   active_days_30=int(data.get("active_days_30") or 0),
                   week=dict(data.get("week") or {}), all_time=dict(data.get("all_time") or {}),
                   last_14_days=days)


@dataclass
class MfaStatus:
    enabled: bool
    factor_id: Optional[str] = None
    since: Optional[datetime] = None


@dataclass
class MfaEnrollment:
    factor_id: str
    qr_svg: str             # the QR code as SVG markup
    secret: str             # for typing in by hand
    uri: str


@dataclass
class CompletenessItem:
    key: str
    label: str
    done: bool
    tab: str                # which Account tab fixes it


@dataclass
class AccountSnapshot:
    """Everything the Account page shows at once, loaded in one go."""

    profile: Profile
    role: str
    email: str
    providers: list[str]
    has_password: bool
    mfa: MfaStatus
    consents: list[Consent]
    pending_email: Optional[str] = None

    def accepted(self, document: str, version: str) -> Optional[Consent]:
        for consent in self.consents:
            if consent.document == document and consent.version == version:
                return consent
        return None
