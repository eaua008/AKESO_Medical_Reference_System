"""Business rules for My Medication Courses and Current Meds.

No widgets and no SQL here, so every rule can be tested on its own:
filtering, the stat cards, finishing a course automatically, and matching
what the patient typed to a medicine in the database.

Medicine names come from MedicineService (your Supabase data, via the
offline cache). Nothing here holds its own list of drugs.
"""

from dataclasses import dataclass
from datetime import date
from typing import Callable, Iterable, Optional

from app.models.medication import (
    ABANDONED,
    ACTIVE,
    COMPLETED,
    INTAKE_MISSED,
    INTAKE_STATUSES,
    STATE_MISSED,
    CurrentMedication,
    MedicationCourse,
    SafetyCheckLog,
    new_id,
    now_iso,
)
from app.repositories.local_medication_store import LocalMedicationStore

# Sidebar filters. Keys are what the view sends back.
STATUS_FILTERS = (("all", "All Courses"), ("active", "Active Courses"),
                  ("completed", "Completed"), ("abandoned", "Abandoned"))
CATEGORY_FILTERS = (("all", "All Categories"),
                    ("protected", "Antibiotics & Steroids (Protected)"),
                    ("routine", "Routine / Maintenance"))


@dataclass
class MedicineOption:
    """One entry in the suggestions list: what is shown, and what it links to."""

    label: str            # "Amlodipine (Amlodipine besilate) · Norvasc"
    name: str             # what goes in the text box when chosen
    medicine_id: str
    is_otc: bool = False


@dataclass
class CourseStats:
    active_courses: int = 0
    doses_remaining: int = 0
    adherence: int = 100
    has_missed: bool = False
    completed_courses: int = 0
    regimen_count: int = 0


@dataclass
class RegimenItem:
    """One thing the patient is taking right now, as the safety check sees it.

    Two sources feed it: current meds (ongoing, no end date) and ACTIVE
    courses (fixed length, still running). Completed and abandoned courses
    are left out: the patient is no longer taking them.
    """

    key: str               # current-med id, or "course:<course id>"
    name: str
    medicine_id: str       # "" when not linked to the medicine database
    detail: str            # "5 mg orally • Daily" or "1 tablet twice daily • 12 left"
    is_course: bool = False


@dataclass
class Preset:
    """A regimen the patient has tracked before, offered for reuse."""

    title: str
    course: MedicationCourse


class MedicationService:
    def __init__(self, owner: str,
                 medicines: Callable[[], Iterable] = list,
                 store: Optional[LocalMedicationStore] = None) -> None:
        self._owner = owner
        self._medicines = medicines        # MedicineService.all_medicines
        self._store = store or LocalMedicationStore()

    # ------------------------------------------------------------- courses

    def courses(self) -> list[MedicationCourse]:
        return self._store.courses_for(self._owner)

    def filtered(self, query: str = "", status: str = "all",
                 category: str = "all") -> list[MedicationCourse]:
        words = query.lower().split()
        out = []
        for course in self.courses():
            if status == "active" and course.status != ACTIVE:
                continue
            if status in (COMPLETED, ABANDONED) and course.status != status:
                continue
            if category == "protected" and not course.is_protected:
                continue
            if category == "routine" and course.is_protected:
                continue
            haystack = f"{course.medicine_name} {course.prescriber}".lower()
            if words and not all(w in haystack for w in words):
                continue
            out.append(course)
        return out

    def status_counts(self) -> dict[str, int]:
        courses = self.courses()
        return {
            "all": len(courses),
            "active": sum(c.status == ACTIVE for c in courses),
            "completed": sum(c.status == COMPLETED for c in courses),
            "abandoned": sum(c.status == ABANDONED for c in courses),
        }

    def stats(self, today: Optional[date] = None) -> CourseStats:
        courses = self.courses()
        active = [c for c in courses if c.status == ACTIVE]
        # Adherence pools every course that expected a dose, abandoned ones
        # included: their expectation simply stopped on the day they ended.
        expected = sum(c.expected_by(today) for c in courses)
        taken = sum(min(c.taken, c.expected_by(today)) for c in courses)
        return CourseStats(
            active_courses=len(active),
            doses_remaining=sum(c.remaining for c in active),
            adherence=100 if expected == 0 else round(taken * 100 / expected),
            has_missed=any(c.state(today) == STATE_MISSED for c in active),
            completed_courses=sum(c.status == COMPLETED for c in courses),
            regimen_count=len(self.regimen()),
        )

    def presets(self, limit: int = 3) -> list[Preset]:
        """The patient's own past regimens, most recent first, no repeats.

        Deliberately not a built-in list of drugs: all medical content comes
        from your database, and a preset is just "track this again".
        """
        seen, out = set(), []
        for course in self.courses():
            key = (course.medicine_name.lower(), course.total_units, course.unit_form,
                   course.duration_days)
            if key in seen:
                continue
            seen.add(key)
            out.append(Preset(f"{course.medicine_name} {course.duration_days}-Day Course",
                              course))
            if len(out) == limit:
                break
        return out

    def add_course(self, medicine_name: str, total_units: int, unit_form: str,
                   dosage_schedule: str, duration_days: int, prescriber: str = "",
                   is_protected: bool = False, notes: str = "",
                   started_on: Optional[date] = None) -> Optional[str]:
        """Save a new course. Returns an error message, or None when saved."""
        name = medicine_name.strip()
        if not name:
            return "Enter the medicine and strength."
        if total_units <= 0:
            return "Prescribed units must be at least 1."
        if duration_days <= 0:
            return "Duration must be at least 1 day."
        self._store.add_course(self._owner, MedicationCourse(
            id=new_id(),
            medicine_name=name,
            medicine_id=self.match_medicine(name),
            total_units=total_units,
            unit_form=unit_form,
            dosage_schedule=dosage_schedule.strip(),
            duration_days=duration_days,
            started_on=(started_on or date.today()).isoformat(),
            prescriber=prescriber.strip(),
            is_protected=is_protected,
            notes=notes.strip(),
        ))
        return None

    def get(self, course_id: str) -> Optional[MedicationCourse]:
        return next((c for c in self.courses() if c.id == course_id), None)

    def log_intake(self, course_id: str, status: str = "taken", units: int = 1,
                   note: str = "") -> Optional[str]:
        """Record one log entry. Returns an error message, or None when saved.

        Taken and delayed entries use up units, capped at what remains so
        the countdown can't go below zero. The last unit completes the
        course automatically.
        """
        course = self.get(course_id)
        if course is None or course.status != ACTIVE:
            return "This course is no longer active."
        if status not in {key for key, _ in INTAKE_STATUSES}:
            return "Choose an intake status."
        if units < 1:
            return "Units must be at least 1."
        if status != INTAKE_MISSED and units > course.remaining:
            return f"Only {course.remaining} {course.unit_label} remain in this course."
        self._store.log_intake(self._owner, course_id, now_iso(), status, units,
                               note.strip())
        self._complete_if_done(course_id)
        return None

    def delete_intake(self, course_id: str, log_id: int) -> None:
        """Remove one entry. A completed course that is short again reopens."""
        self._store.delete_intake(self._owner, course_id, log_id)
        course = self.get(course_id)
        if course is not None and course.status == COMPLETED and course.remaining > 0:
            self._store.set_status(self._owner, course_id, ACTIVE, "")

    def update_course(self, course_id: str, medicine_name: str, total_units: int,
                      unit_form: str, dosage_schedule: str, duration_days: int,
                      prescriber: str = "", is_protected: bool = False,
                      notes: str = "") -> Optional[str]:
        """Edit a course's regimen. Returns an error message, or None when saved."""
        course = self.get(course_id)
        if course is None:
            return "This course no longer exists."
        name = medicine_name.strip()
        if not name:
            return "Enter the medicine and strength."
        if total_units < max(course.taken, 1):
            return (f"{course.taken} {course.unit_label} are already logged, so the "
                    f"total can't be lower than that.")
        if duration_days <= 0:
            return "Duration must be at least 1 day."
        self._store.update_course(self._owner, course_id, {
            "medicine_name": name, "medicine_id": self.match_medicine(name),
            "total_units": total_units, "unit_form": unit_form,
            "dosage_schedule": dosage_schedule.strip(), "duration_days": duration_days,
            "prescriber": prescriber.strip(), "is_protected": is_protected,
            "notes": notes.strip(),
        })
        self._complete_if_done(course_id)
        return None

    def _complete_if_done(self, course_id: str) -> None:
        course = self.get(course_id)
        if course is not None and course.status == ACTIVE and course.remaining == 0:
            self._store.set_status(self._owner, course_id, COMPLETED,
                                   date.today().isoformat())

    def abandon(self, course_id: str, reason: str) -> None:
        self._store.set_status(self._owner, course_id, ABANDONED,
                               date.today().isoformat(), reason.strip())

    # -------------------------------------------------------- current meds

    def current_meds(self) -> list[CurrentMedication]:
        return self._store.current_meds_for(self._owner)

    def add_current_med(self, name: str, dosage: str = "", frequency: str = "Daily",
                        is_otc: bool = False, notes: str = "") -> Optional[str]:
        name = name.strip()
        if not name:
            return "Enter the medicine name."
        self._store.add_current_med(self._owner, CurrentMedication(
            id=new_id(), name=name, dosage=dosage.strip(), frequency=frequency,
            is_otc=is_otc, notes=notes.strip(), medicine_id=self.match_medicine(name),
            added_at=now_iso()))
        return None

    def regimen(self) -> list[RegimenItem]:
        """Current meds first, then active courses."""
        items = [RegimenItem(key=m.id, name=m.name, medicine_id=m.medicine_id,
                             detail=" \u2022 ".join(x for x in (m.dosage, m.frequency) if x))
                 for m in self.current_meds()]
        for c in self.courses():
            if c.status != ACTIVE:
                continue
            bits = [c.dosage_schedule, f"{c.remaining} {c.unit_label} left"]
            items.append(RegimenItem(key=f"course:{c.id}", name=c.medicine_name,
                                     medicine_id=c.medicine_id,
                                     detail=" \u2022 ".join(b for b in bits if b),
                                     is_course=True))
        return items

    def remove_current_med(self, med_id: str) -> None:
        self._store.remove_current_med(self._owner, med_id)

    # ------------------------------------------- database-backed suggestions

    def medicine_options(self) -> list[MedicineOption]:
        """Every published medicine, for the suggestions list in both dialogs."""
        options = []
        for m in self._medicines():
            generic = m.international_generic_name or m.generic_name
            brands = [*m.ph_brands, *m.intl_brands]
            label = m.name
            if generic and generic.lower() != m.name.lower():
                label += f" ({generic})"
            if brands:
                label += " · " + ", ".join(brands[:3])
            options.append(MedicineOption(label=label, name=m.name,
                                          medicine_id=m.id, is_otc=m.is_otc))
        return sorted(options, key=lambda o: o.name.lower())

    def match_medicine(self, typed: str) -> str:
        """The database id for what the patient typed, or "" if it isn't there.

        Matches the medicine's name, generic name, or any brand, ignoring
        case, and also accepts the typed text STARTING with one of those
        ("Amoxicillin 500mg" still links to Amoxicillin). The longest name
        wins, so "Co-Amoxiclav" is not mistaken for "Amoxi..." anything.
        """
        text = typed.strip().lower()
        if not text:
            return ""
        best_id, best_len = "", 0
        for m in self._medicines():
            names = [m.name, m.generic_name, m.international_generic_name,
                     *m.ph_brands, *m.intl_brands]
            for name in (n.strip().lower() for n in names if n):
                if (text == name or text.startswith(name + " ")) and len(name) > best_len:
                    best_id, best_len = m.id, len(name)
        return best_id

    # ------------------------------------------ health profile and checks

    def health_profile(self) -> set[str]:
        return self._store.health_profile(self._owner)

    def set_condition(self, condition_id: str, on: bool) -> None:
        self._store.set_condition(self._owner, condition_id, on)

    def safety_checks(self) -> list[SafetyCheckLog]:
        return self._store.safety_checks(self._owner)

    def save_safety_check(self, candidate_name: str, candidate_id: str, verdict: str,
                          condition_ids: list[str], regimen_ids: list[str]) -> None:
        self._store.add_safety_check(self._owner, SafetyCheckLog(
            id=new_id(), candidate_name=candidate_name, candidate_id=candidate_id,
            verdict=verdict, condition_ids=list(condition_ids),
            regimen_ids=list(regimen_ids), created_at=now_iso()))

    def clear_safety_checks(self) -> None:
        self._store.clear_safety_checks(self._owner)

    def quick_candidates(self, limit: int = 8) -> list[MedicineOption]:
        """Chips under the search box: the patient's recent checks first, then
        medicines from the database to fill the row. No built-in drug list."""
        options = {o.medicine_id: o for o in self.medicine_options()}
        out, seen = [], set()
        for log in self.safety_checks():
            option = options.get(log.candidate_id)
            if option is not None and option.medicine_id not in seen:
                out.append(option)
                seen.add(option.medicine_id)
        for option in options.values():
            if len(out) >= limit:
                break
            if option.medicine_id not in seen:
                out.append(option)
                seen.add(option.medicine_id)
        return out[:limit]
