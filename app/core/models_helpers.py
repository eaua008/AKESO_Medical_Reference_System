"""Small presentation helpers shared across views.

urgency_style lives here rather than on the Disease model because it maps a
domain value onto a stylesheet object name — that is a UI concern, and the
model is supposed to stay ignorant of the UI.
"""

from typing import Optional

# Maps the stored urgency value to (display label, stylesheet object name).
#
# None is handled explicitly: most source monographs carry no authored
# urgency, and the app must say so rather than imply a triage level nobody
# wrote.
_URGENCY = {
    "SELF_CARE": ("SELF CARE", "urgencyPillSelfCare"),
    "SEE_DOCTOR_SOON": ("SEE A DOCTOR SOON", "urgencyPillSoon"),
    "SEEK_URGENT_CARE": ("SEEK URGENT CARE", "urgencyPillUrgent"),
    "EMERGENCY": ("EMERGENCY", "urgencyPillEmergency"),
}


def urgency_style(urgency: Optional[str]) -> tuple[str, str]:
    if not urgency:
        return ("URGENCY NOT SPECIFIED", "urgencyPillUnknown")
    return _URGENCY.get(urgency, (urgency.replace("_", " "), "urgencyPillUnknown"))