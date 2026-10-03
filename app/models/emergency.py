"""Domain models for the Emergency Guide.

Plain, frozen dataclasses: they describe data and nothing else. Loading them
is the repository's job, filtering is the service's, drawing is the view's.

Frozen because this is safety-critical reference text. Nothing in the app
should be able to edit a protocol step after it has been loaded.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Hotline:
    """One number people can call."""

    name: str
    number: str
    description: str
    alt_numbers: tuple[str, ...] = ()


@dataclass(frozen=True)
class EmergencyProtocol:
    """One first-aid procedure, shown as a card."""

    id: str
    title: str
    urgency: str                     # "critical" | "urgent" | "same_day"
    warning_signs: tuple[str, ...]
    steps: tuple[str, ...]
    avoid: tuple[str, ...]
    call_when: str
    source: str
    local_name: str = ""             # Filipino name, when there's a common one
    keywords: tuple[str, ...] = field(default=())

    # Labels live with the model so every screen names urgency the same way.
    URGENCY_LABELS = {
        "critical": "LIFE-THREATENING",
        "urgent": "URGENT",
        "same_day": "SAME-DAY CARE",
    }

    @property
    def urgency_label(self) -> str:
        return self.URGENCY_LABELS.get(self.urgency, self.urgency.upper())


@dataclass(frozen=True)
class EmergencyGuide:
    """Everything the Emergency Guide screen shows, as one unit."""

    region: str
    featured_hotline: Hotline
    hotlines: tuple[Hotline, ...]
    call_tips: tuple[str, ...]
    local_note: str
    protocols: tuple[EmergencyProtocol, ...]