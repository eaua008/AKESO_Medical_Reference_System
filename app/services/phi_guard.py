"""Catch real patient information before it is posted.

The same checks run in the database (public.ex_phi_check in migration 003),
so a modified app can't skip them. This copy only makes the warning appear
while typing, before anything is sent.

It is a safety net, not a guarantee: no pattern can recognise every name.
Students are still responsible for keeping cases hypothetical.
"""

import re
from typing import Optional

_CHECKS: list[tuple[str, re.Pattern]] = [
    ("a phone number", re.compile(r"(\+?63|\b0)9\d{2}[\s.-]?\d{3}[\s.-]?\d{4}")),
    ("an email address", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("an exact date of birth", re.compile(
        r"\b\d{1,2}[/.-]\d{1,2}[/.-](19|20)\d{2}\b"
        r"|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{1,2},?\s+(19|20)\d{2}\b"
        r"|\b(birthday|date of birth|dob)\b", re.IGNORECASE)),
    ("a record or ID number", re.compile(
        r"\b(mrn|hrn|philhealth|record\s*(no|number|#)|hospital\s*(no|number|#)"
        r"|case\s*(no|number|#)|bed\s*(no|number|#))", re.IGNORECASE)),
    ("a patient's name", re.compile(r"\b(Mr|Mrs|Ms|Miss|Mx)\.?\s+[A-Z][a-z]+")),
    ("a patient's name", re.compile(r"\b(patient|pt)('s)?\s*name\b", re.IGNORECASE)),
]


def find_phi(*texts: str) -> Optional[str]:
    """What looks like real patient data in the texts, or None."""
    joined = " ".join(t for t in texts if t)
    for label, pattern in _CHECKS:
        if pattern.search(joined):
            return label
    return None


def phi_message(found: str) -> str:
    return (f"This looks like it contains {found}. Cases must be hypothetical: "
            "remove anything that could identify a real person.")
