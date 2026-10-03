"""Domain models for the disease encyclopedia.

These classes know nothing about where the data came from. No database
client, no knowledge that Supabase exists. Swapping storage touches the
repository only.

urgency is Optional on purpose. Most monographs carry no authored urgency,
and defaulting one would make the app display a triage recommendation that
nobody wrote.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ClinicalReference:
    """A citation backing a monograph.

    is_mother_book marks the Tier 1 primary specialty textbook; everything
    else is a Tier 2 exact-chapter reference.
    """

    id: str
    source_name: str
    citation_text: str
    url: str = ""
    specialty: str = ""
    is_mother_book: bool = False

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "ClinicalReference":
        return cls(
            id=raw.get("id", ""),
            source_name=raw.get("sourceName") or raw.get("source_name", ""),
            citation_text=raw.get("citationText") or raw.get("citation_text", ""),
            url=raw.get("url") or "",
            specialty=raw.get("specialty") or "",
            is_mother_book=raw.get("is_mother_book", False),
        )


@dataclass
class SymptomLink:
    """A symptom as it presents in one specific condition.

    Carries both the symptom's own identity (name, red-flag status) and how
    it behaves in this condition (intensity, whether it is cardinal). The
    weights are what the symptom matcher scores against.
    """

    symptom_id: str
    name: str = ""
    typical_intensity: int = 0
    is_primary: bool = False
    weight_multiplier: float = 1.0
    is_red_flag: bool = False

    @property
    def intensity_label(self) -> str:
        return f"{self.typical_intensity}/10"

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "SymptomLink":
        # Resource embedding puts the joined symptom row under "symptoms".
        joined = raw.get("symptoms") or {}
        return cls(
            symptom_id=raw.get("symptomId") or raw.get("symptom_id", ""),
            name=joined.get("name", "") or raw.get("name", ""),
            typical_intensity=raw.get("typicalIntensity")
                              or raw.get("typical_intensity", 0),
            is_primary=raw.get("isPrimary") or raw.get("is_primary", False),
            weight_multiplier=float(
                raw.get("weightMultiplier") or raw.get("weight_multiplier", 1.0)
            ),
            is_red_flag=joined.get("is_red_flag", False),
        )


@dataclass
class Medicine:
    """A drug as it relates to one condition.

    safety lives here rather than on the drug itself because it is a property
    of the pairing: losartan is first-line for hypertension and contra-
    indicated in pregnancy. "Safe" is never an abstract claim.
    """

    id: str
    name: str
    generic_name: str = ""
    drug_class: str = ""
    category: str = "Prescription"
    safety: str = "safe"
    note: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Medicine":
        joined = raw.get("medicines") or {}
        return cls(
            id=joined.get("id") or raw.get("medicine_id", ""),
            name=joined.get("name", ""),
            generic_name=joined.get("generic_name") or "",
            drug_class=joined.get("drug_class") or "",
            category=joined.get("category") or "Prescription",
            safety=raw.get("safety", "safe"),
            note=raw.get("note") or "",
        )


@dataclass
class Differential:
    """A condition that can be mistaken for this one, and how to tell them apart."""

    condition: str
    distinguishing_feature: str

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Differential":
        return cls(
            condition=raw.get("condition", ""),
            distinguishing_feature=raw.get("distinguishingFeature")
                                   or raw.get("distinguishing_feature", ""),
        )


@dataclass
class BodySystem:
    id: str
    name: str
    description: str = ""
    icon_name: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "BodySystem":
        return cls(
            id=raw.get("id", ""),
            name=raw.get("name", ""),
            description=raw.get("description") or "",
            icon_name=raw.get("iconName") or raw.get("icon_name", ""),
        )


@dataclass
class Disease:
    """One clinical monograph."""

    id: str
    name: str
    scientific_name: str = ""
    description: str = ""
    body_system_id: str = ""
    body_system_name: str = ""
    severity: str = "Moderate"
    urgency: Optional[str] = None
    urgency_criteria: str = ""
    contagious: bool = False
    tags: list[str] = field(default_factory=list)
    views_count: int = 0

    # Clinical content
    pathophysiology: str = ""
    clinicopathologic_correlation: str = ""
    onset_progression: str = ""
    causes: list[str] = field(default_factory=list)
    risk_factors: list[str] = field(default_factory=list)
    symptoms: list[SymptomLink] = field(default_factory=list)
    differential_diagnosis: list[Differential] = field(default_factory=list)
    recommended_tests: list[str] = field(default_factory=list)
    treatments: list[str] = field(default_factory=list)
    home_care: list[str] = field(default_factory=list)
    prevention: list[str] = field(default_factory=list)
    prevention_tiers: dict[str, list[str]] = field(default_factory=dict)
    follow_up_monitoring: str = ""
    emergency_warning_signs: list[str] = field(default_factory=list)

    # Cross-links and provenance
    medicines: list[Medicine] = field(default_factory=list)
    related_disease_ids: list[str] = field(default_factory=list)
    source_attribution: str = ""
    clinical_references: list[ClinicalReference] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Disease":
        """Build from a raw record.

        Accepts camelCase (the original JSON export) and snake_case
        (Postgres columns), so either source works.
        """

        def pick(camel: str, snake: str, default=None):
            value = raw.get(camel)
            if value is None:
                value = raw.get(snake)
            return default if value is None else value

        return cls(
            id=raw.get("id", ""),
            name=raw.get("name", ""),
            scientific_name=pick("scientificName", "scientific_name", ""),
            description=raw.get("description") or "",
            body_system_id=pick("bodySystemId", "body_system_id", ""),
            severity=raw.get("severity") or "Moderate",
            urgency=raw.get("urgency"),  # stays None when unauthored
            urgency_criteria=pick("urgencyCriteria", "urgency_criteria", ""),
            contagious=raw.get("contagious", False),
            tags=raw.get("tags", []),
            views_count=pick("viewsCount", "views_count", 0),
            pathophysiology=raw.get("pathophysiology") or "",
            clinicopathologic_correlation=pick(
                "clinicopathologicCorrelation",
                "clinicopathologic_correlation",
                "",
            ),

            onset_progression=pick("onsetProgression", "onset_progression", ""),
            causes=raw.get("causes", []),
            risk_factors=pick("riskFactors", "risk_factors", []),
            recommended_tests=pick("recommendedTests", "recommended_tests", []),
            treatments=raw.get("treatments", []),
            home_care=pick("homeCare", "home_care", []),
            prevention=raw.get("prevention", []),
            prevention_tiers=pick("preventionTiers", "prevention_tiers", {}),
            follow_up_monitoring=pick(
                "followUpMonitoring", "follow_up_monitoring", ""
            ),
            emergency_warning_signs=pick(
                "emergencyWarningSigns", "emergency_warning_signs", []
            ),
            source_attribution=pick(
                "sourceAttribution", "source_attribution", ""
            ),
        )

    # ------------------------------------------------------------ behaviour

    @property
    def hallmark_symptoms(self) -> list[SymptomLink]:
        """Symptoms flagged as cardinal — the defining presentation."""
        return [s for s in self.symptoms if s.is_primary]

    @property
    def hallmark_symptom_ids(self) -> list[str]:
        return [s.symptom_id for s in self.hallmark_symptoms]

    @property
    def mother_book_references(self) -> list[ClinicalReference]:
        return [r for r in self.clinical_references if r.is_mother_book]

    @property
    def chapter_references(self) -> list[ClinicalReference]:
        return [r for r in self.clinical_references if not r.is_mother_book]

    @property
    def urgency_label(self) -> str:
        """Human-readable urgency. None means nobody has assessed it yet."""
        if not self.urgency:
            return "Not specified"
        return {
            "SELF_CARE": "Self-care",
            "SEE_DOCTOR_SOON": "See a Doctor Soon",
            "SEEK_URGENT_CARE": "Seek Urgent Care",
            "EMERGENCY": "Emergency",
        }.get(self.urgency, self.urgency.replace("_", " ").title())

    @property
    def triage_window(self) -> str:
        """Plain-language time frame implied by the urgency level."""
        return {
            "SELF_CARE": "Manage at home; review if symptoms persist",
            "SEE_DOCTOR_SOON": "Outpatient evaluation within 1 to 3 days",
            "SEEK_URGENT_CARE": "Same-day clinical assessment",
            "EMERGENCY": "Immediate emergency care",
        }.get(self.urgency or "", "No triage window recorded")

    @property
    def is_emergency(self) -> bool:
        return self.urgency == "EMERGENCY"

    def matches(self, query: str) -> bool:
        """Case-insensitive match across the fields a user would search by."""
        if not query:
            return True
        q = query.strip().lower()
        haystack = [self.name, self.scientific_name, self.description]
        haystack.extend(self.tags)
        return any(q in text.lower() for text in haystack if text)