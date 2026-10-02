"""Business rules for the Account module: profile, privacy and your data.

Validation lives here, not in the screens, so any future interface (a test,
the Admin panel) enforces the same rules. The database enforces them again
(check constraints, column grants, RLS), because a desktop app can be
modified by whoever runs it.
"""

import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from app.core.device_identity import APP_VERSION
from app.models.account import (
    MAX_INTERESTS, PRIVACY_VERSION, PROGRAM_LABELS, ROLE_LABELS,
    TERMS_VERSION, YEAR_LABELS, AccountSnapshot, ActivitySummary, CompletenessItem,
    Consent, Profile, parse_time,
)
from app.repositories.account_data_repository import AccountDataRepository
from app.repositories.account_errors import AccountError
from app.repositories.local_account_data import LocalAccountData
from app.repositories.profile_repository import ProfileRepository
from app.repositories.security_repository import SecurityRepository

HANDLE_PATTERN = re.compile(r"^[a-z0-9_]{3,20}$")
MAX_AVATAR_BYTES = 1_000_000
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class AccountService:
    def __init__(self, profiles: ProfileRepository, security: SecurityRepository,
                 data: AccountDataRepository, local: LocalAccountData,
                 email: str, owner: str) -> None:
        self._profiles = profiles
        self._security = security
        self._data = data
        self._local = local
        self._email = email
        self._owner = owner          # the key the local stores use

    @property
    def owner(self) -> str:
        return self._owner

    # ------------------------------------------------------------ loading

    def snapshot(self) -> AccountSnapshot:
        user = self._security.current_user()
        providers = sorted({i.provider for i in (user.identities or [])}
                           or set((user.app_metadata or {}).get("providers") or []))
        return AccountSnapshot(
            profile=Profile.from_row(self._profiles.get()),
            role=self._profiles.role(),
            email=user.email or self._email,
            providers=providers,
            has_password=self._security.has_password(),
            mfa=self._security.mfa_status(),
            consents=[Consent.from_row(r) for r in self._data.consents()],
            pending_email=getattr(user, "new_email", None) or None,
        )

    def profile(self) -> Profile:
        return Profile.from_row(self._profiles.get())

    def role(self) -> str:
        return self._profiles.role()

    @staticmethod
    def header_role_label(role: str, profile: Optional[Profile]) -> str:
        """The small caption under the name in the header."""
        if role in ("admin", "educator"):
            return ROLE_LABELS[role].upper()
        if profile is not None and profile.program and profile.program != "other":
            return f"{PROGRAM_LABELS[profile.program].upper()} STUDENT"
        return "STUDENT"

    # ------------------------------------------------------------ profile

    def validate(self, changes: dict) -> dict:
        """Clean and check edited fields. Returns only valid, normalised values."""
        clean: dict = {}
        for key, value in changes.items():
            if key not in Profile.EDITABLE:
                continue
            if isinstance(value, str):
                value = " ".join(value.split()) if key != "bio" else value.strip()
            clean[key] = value

        if "display_name" in clean:
            if not clean["display_name"]:
                raise AccountError("Please enter the name you want shown.")
            if len(clean["display_name"]) > 60:
                raise AccountError("Names can be at most 60 characters.")
        if "handle" in clean:
            handle = (clean["handle"] or "").lstrip("@").lower()
            if not handle:
                clean["handle"] = None
            elif not HANDLE_PATTERN.match(handle):
                raise AccountError("Handles use 3–20 lowercase letters, numbers or underscores.")
            else:
                clean["handle"] = handle
        if "bio" in clean and len(clean["bio"]) > 280:
            raise AccountError("The bio can be at most 280 characters.")
        if "program" in clean and clean["program"] not in (None, *PROGRAM_LABELS):
            raise AccountError("Choose a program from the list.")
        if "school" in clean:
            clean["school"] = clean["school"] or None
            if clean["school"] and len(clean["school"]) > 120:
                raise AccountError("The school name can be at most 120 characters.")
        if "year_level" in clean and clean["year_level"] not in (None, *YEAR_LABELS):
            raise AccountError("Choose a year level from the list.")
        if "interests" in clean:
            interests = []
            for item in clean["interests"] or []:
                item = " ".join(str(item).split())[:40]
                if item and item.lower() not in (i.lower() for i in interests):
                    interests.append(item)
            if len(interests) > MAX_INTERESTS:
                raise AccountError(f"Pick up to {MAX_INTERESTS} interests.")
            clean["interests"] = interests
        return clean

    def save_profile(self, current: Profile, changes: dict) -> Profile:
        clean = self.validate(changes)
        diff = {k: v for k, v in clean.items() if getattr(current, k) != v}
        if not diff:
            return current
        if diff.get("handle") and diff["handle"] != (current.handle or "") \
                and not self._profiles.handle_available(diff["handle"]):
            raise AccountError(f"@{diff['handle']} is already taken.")
        updated = Profile.from_row(self._profiles.update(diff))
        self._log("profile_updated", {"fields": sorted(diff)})
        return updated

    def handle_available(self, handle: str) -> bool:
        handle = handle.lstrip("@").lower()
        return bool(HANDLE_PATTERN.match(handle)) and self._profiles.handle_available(handle)

    def set_avatar(self, png: bytes) -> Profile:
        if not png.startswith(PNG_SIGNATURE):
            raise AccountError("The photo could not be prepared. Try another image.")
        if len(png) > MAX_AVATAR_BYTES:
            raise AccountError("That photo is too large even after resizing. Try another one.")
        path = self._profiles.upload_avatar(png)
        updated = Profile.from_row(self._profiles.update({"avatar_path": path}))
        self._log("profile_updated", {"fields": ["avatar"]})
        return updated

    def remove_avatar(self, profile: Profile) -> Profile:
        if profile.avatar_path:
            self._profiles.remove_avatar(profile.avatar_path)
        updated = Profile.from_row(self._profiles.update({"avatar_path": None}))
        self._log("profile_updated", {"fields": ["avatar"]})
        return updated

    def avatar_bytes(self, profile: Profile) -> Optional[bytes]:
        if not profile.avatar_path:
            return None
        return self._profiles.download_avatar(profile.avatar_path)

    # -------------------------------------------------------- school email

    def send_school_code(self, email: str) -> str:
        email = email.strip().lower()
        if "@" not in email:
            raise AccountError("Enter your school email address.")
        return self._data.send_school_code(email).get("domain", email.split("@")[1])

    def verify_school_code(self, code: str) -> Profile:
        code = code.strip().replace(" ", "")
        if not (code.isdigit() and len(code) == 6):
            raise AccountError("Enter the 6-digit code from the email.")
        self._data.verify_school_code(code)
        return self.profile()

    # ------------------------------------------------------- completeness

    @staticmethod
    def completeness(snapshot: AccountSnapshot) -> tuple[int, list[CompletenessItem]]:
        p = snapshot.profile
        items = [
            CompletenessItem("photo", "Add a profile photo", bool(p.avatar_path), "profile"),
            CompletenessItem("program", "Choose your program", bool(p.program), "profile"),
            CompletenessItem("school", "Add your school and year level",
                             bool(p.school and p.year_level), "profile"),
            CompletenessItem("interests", "Pick your interest areas", bool(p.interests), "profile"),
            CompletenessItem("handle", "Claim an @handle", bool(p.handle), "profile"),
            CompletenessItem("verified", "Verify your school email",
                             p.is_verified_student, "profile"),
            CompletenessItem("mfa", "Turn on two-factor sign-in", snapshot.mfa.enabled, "security"),
            CompletenessItem("terms", "Accept the current Terms and Privacy Notice",
                             bool(snapshot.accepted("terms", TERMS_VERSION)), "privacy"),
        ]
        done = sum(1 for i in items if i.done)
        return round(done * 100 / len(items)), items

    # ----------------------------------------------------------- activity

    def activity(self) -> ActivitySummary:
        return ActivitySummary.from_json(self._data.activity_summary())

    def record_activity(self, counts: dict[str, int]) -> None:
        if counts:
            self._data.record_activity(counts)

    def set_tracking(self, current: Profile, on: bool) -> Profile:
        return self.save_profile(current, {"track_study_activity": on})

    # ------------------------------------------------------------ consent

    @staticmethod
    def needs_consent(snapshot: AccountSnapshot) -> bool:
        return not (snapshot.accepted("terms", TERMS_VERSION)
                    and snapshot.accepted("privacy", PRIVACY_VERSION))

    def accept_documents(self) -> None:
        self._data.accept(TERMS_VERSION, PRIVACY_VERSION)

    # ----------------------------------------------------------- deletion

    def request_deletion(self, confirm_text: str, erase_local: bool) -> datetime:
        if confirm_text.strip() != "DELETE":
            raise AccountError("Type DELETE (in capitals) to confirm.")
        due = parse_time(self._data.request_deletion("DELETE"))
        if erase_local:
            self._local.erase(self._owner)
        return due or datetime.now(timezone.utc)

    def cancel_deletion(self) -> Profile:
        self._data.cancel_deletion()
        return self.profile()

    # ------------------------------------------------------------- export

    def export(self, target: Path) -> Path:
        """Write everything Akeso holds about this account into one ZIP.

        Server rows come through the same row-level security as everything
        else, so this can only ever contain the signed-in account's data.
        """
        target = Path(target)
        if target.suffix.lower() != ".zip":
            target = target.with_suffix(".zip")
        profile = self.profile()
        user = self._security.current_user()
        local = self._local.export(self._owner)
        images = self._local.notebook_images(local)
        avatar = self.avatar_bytes(profile)

        server = {
            "profile": self._profiles.get(),
            "role": self._profiles.role(),
            "consents": self._data.consents(),
            "devices": self._security.all_devices(),
            "security_events": self._security.all_events(),
            "study_activity": self._data.all_activity(),
            "sign_in": {
                "email": user.email,
                "created_at": str(getattr(user, "created_at", "") or ""),
                "last_sign_in_at": str(getattr(user, "last_sign_in_at", "") or ""),
                "providers": sorted({i.provider for i in (user.identities or [])}),
                "two_factor": self._security.mfa_status().enabled,
            },
        }
        manifest = {
            "app": "Akeso",
            "app_version": APP_VERSION,
            "format": 1,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "account_id": profile.id,
            "files": [],
        }

        def dump(value) -> str:
            return json.dumps(value, indent=2, ensure_ascii=False, default=str)

        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, value in server.items():
                path = f"account/{name}.json"
                archive.writestr(path, dump(value))
                manifest["files"].append(path)
            for store, tables in local.items():
                path = f"this_computer/{store}.json"
                archive.writestr(path, dump(tables))
                manifest["files"].append(path)
            for image in images:
                path = f"this_computer/notebook_images/{image.name}"
                archive.write(image, path)
                manifest["files"].append(path)
            if avatar:
                archive.writestr("account/avatar.png", avatar)
                manifest["files"].append("account/avatar.png")
            archive.writestr("README.txt", EXPORT_README)
            archive.writestr("manifest.json", dump(manifest))

        self._log("data_exported", {"files": len(manifest["files"])})
        return target

    # ------------------------------------------------------------ helpers

    def _log(self, kind: str, detail: Optional[dict] = None) -> None:
        try:
            self._security.log(kind, "", detail or {})
        except AccountError:
            pass    # the change itself succeeded; a missing log line must not undo it


EXPORT_README = """Akeso account export
====================

This archive holds a copy of everything Akeso stores about your account.

account/            kept on Akeso's server (Supabase)
  profile.json          name, handle, bio, program, school, privacy switches
  role.json             student, educator or admin
  consents.json         which Terms / Privacy Notice versions you accepted
  devices.json          computers you signed in from
  security_events.json  the account activity log
  study_activity.json   your daily study counters
  sign_in.json          sign-in email, sign-in methods, two-factor status
  avatar.png            your profile photo (if you set one)

this_computer/      kept only on the computer that made this export
  bookmarks.json, saved_cases.json, medications.json, notebook.json
  notebook_images/      pictures pasted into your notes

Not included: your password (Akeso never has it; Supabase stores only a
one-way hash) and your two-factor secret.

Files are JSON (open with any text editor). Keep this archive private: it
contains your personal study data.
"""
