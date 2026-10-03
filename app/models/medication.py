"""The patient's own medication data: courses, intake logs, current meds.

This is PERSONAL data, unlike models/drug_safety.py. For now it lives in a
local SQLite file; the encrypted cloud vault is a later, separate step, and
it will store these same objects, so nothing here changes when it arrives.

Only plain values are stored. Everything shown on a card (remaining,
percent complete, adherence, missed dose) is computed from them, so the
numbers can never disagree with the log they came from.
"""

import math
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

# Course status as stored. "missed" and "on track" are NOT stored: they are
# worked out from the intake log every time (see MedicationCourse.state).
ACTIVE, COMPLETED, ABANDONED = "active", "completed", "abandoned"

# Display states for the badge.
STATE_ON_TRACK, STATE_MISSED = "on_track", "missed"

# What happened at one logged dose. Only TAKEN and DELAYED use up units;
# a MISSED entry is a record that a dose was skipped, so the countdown
# stays where it is.
INTAKE_TAKEN, INTAKE_DELAYED, INTAKE_MISSED = "taken", "delayed", "missed"
INTAKE_STATUSES = ((INTAKE_TAKEN, "Taken Now"), (INTAKE_DELAYED, "Delayed Intake"),
                   (INTAKE_MISSED, "Missed / Skipped"))

# Unit forms offered in the Track New Course dialog. UI choices, not
# medical data: they only label the countdown ("12 / 14 tablets").
UNIT_FORMS = ("Tablets", "Capsules", "Sachets", "mL", "Puffs", "Drops",
              "Injections", "Patches")

# Frequencies offered in the Add to Current Meds dialog.
FREQUENCIES = ("Daily", "Twice daily", "Three times daily", "Four times daily",
               "Every other day", "Weekly", "As needed")


def new_id() -> str:
    return uuid.uuid4().hex


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class IntakeLog:
    course_id: str
    taken_at: str          # ISO timestamp
    status: str = INTAKE_TAKEN
    units: int = 1
    note: str = ""
    id: int = 0            # row id, for deleting one entry

    @property
    def uses_units(self) -> bool:
        return self.status in (INTAKE_TAKEN, INTAKE_DELAYED)


@dataclass
class MedicationCourse:
    """A fixed-length prescribed course, e.g. 14 tablets over 7 days."""

    id: str
    medicine_name: str
    total_units: int
    unit_form: str
    dosage_schedule: str
    duration_days: int
    started_on: str                        # ISO date, "2026-09-14"
    medicine_id: str = ""                  # set when chosen from the database
    prescriber: str = ""
    is_protected: bool = False             # antibiotic or tapered steroid
    notes: str = ""
    status: str = ACTIVE
    ended_on: str = ""                     # ISO date, set on abandon/complete
    abandon_reason: str = ""
    created_at: str = ""                   # ISO timestamp, "Registered" in details
    intakes: list[IntakeLog] = field(default_factory=list)

    # ---------------------------------------------------------- countdown

    @property
    def taken(self) -> int:
        """Units actually taken (on time or late). Missed entries don't count."""
        return sum(log.units for log in self.intakes if log.uses_units)

    @property
    def on_time_count(self) -> int:
        return sum(log.status == INTAKE_TAKEN for log in self.intakes)

    @property
    def late_count(self) -> int:
        return sum(log.status == INTAKE_DELAYED for log in self.intakes)

    @property
    def next_dose_number(self) -> int:
        return min(self.taken + 1, self.total_units)

    @property
    def remaining(self) -> int:
        return max(self.total_units - self.taken, 0)

    @property
    def percent_complete(self) -> int:
        if self.total_units <= 0:
            return 0
        return min(100, round(self.taken * 100 / self.total_units))

    @property
    def unit_label(self) -> str:
        """"tablets", "capsules", "mL" for the countdown line."""
        return self.unit_form if self.unit_form == "mL" else self.unit_form.lower()

    # ---------------------------------------------------------- adherence

    @property
    def doses_per_day(self) -> float:
        """14 tablets over 7 days = 2 a day. Derived, so no schedule parsing."""
        return self.total_units / self.duration_days if self.duration_days > 0 else 0.0

    def expected_by(self, today: Optional[date] = None) -> int:
        """Doses that should have been taken by the START of today.

        Today's doses are not counted yet: at 8 a.m. nobody has "missed" the
        evening dose. An abandoned course stops expecting doses on the day
        it was abandoned.
        """
        today = today or date.today()
        end = date.fromisoformat(self.ended_on) if self.ended_on else today
        days = max((min(end, today) - date.fromisoformat(self.started_on)).days, 0)
        return min(self.total_units, math.floor(days * self.doses_per_day))

    def adherence(self, today: Optional[date] = None) -> int:
        """Taken vs expected, as a percentage. 100 when nothing is due yet."""
        expected = self.expected_by(today)
        if expected == 0:
            return 100
        return min(100, round(self.taken * 100 / expected))

    def state(self, today: Optional[date] = None) -> str:
        """completed / abandoned / missed / on_track, for the badge."""
        if self.status in (COMPLETED, ABANDONED):
            return self.status
        return STATE_MISSED if self.taken < self.expected_by(today) else STATE_ON_TRACK


@dataclass
class SafetyCheckLog:
    """One saved Interaction & Safety Check, for the Past Safety Checks Log."""

    id: str
    candidate_name: str
    candidate_id: str
    verdict: str
    condition_ids: list[str] = field(default_factory=list)
    regimen_ids: list[str] = field(default_factory=list)     # CurrentMedication ids
    created_at: str = ""


@dataclass
class CurrentMedication:
    """An ongoing medicine with no end date: the regimen the safety check reads."""

    id: str
    name: str
    dosage: str = ""
    frequency: str = "Daily"
    is_otc: bool = False
    notes: str = ""
    medicine_id: str = ""                  # set when chosen from the database
    added_at: str = ""
