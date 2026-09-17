"""Domain models for the disease encyclopedia.

Same principle as User: these classes know nothing about where the data came
from. They do not import a database client, they do not know Supabase exists.
Swapping storage later touches the repository only.

urgency is deliberately Optional. Most source monographs carry no authored
urgency value, and defaulting one would mean the app displaying a triage
recommendation that nobody wrote — not acceptable in a clinical reference.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ClinicalReference:
    """A citation backing a monograph."""

    id: str
    source_name: str
    citation_text: str

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "ClinicalReference":
        return cls(
            id=raw.get("id", ""),
            source_name=raw.get("sourceName") or raw.get("source_name", ""),
            citation_text=raw.get("citationText") or raw.get("citation_text", ""),
        )


@dataclass
class SymptomLink:
    """Join between a disease and a symptom, carrying the matching weights.

    This is what the symptom matcher scores against later: how intense the
    symptom typically is, whether it is a hallmark, and how much it counts.
    """

    symptom_id: str
    typical_intensity: int = 0
    is_primary: bool = False
    weight_multiplier: float = 1.0

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "SymptomLink":
        return cls(
            symptom_id=raw.get("symptomId") or raw.get("symptom_id", ""),
            typical_intensity=raw.get("typicalIntensity")
                              or raw.get("typical_intensity", 0),
            is_primary=raw.get("isPrimary") or raw.get("is_primary", False),
            weight_multiplier=raw.get("weightMultiplier")
                              or raw.get("weight_multiplier", 1.0),
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
    organs: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    icon_name: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "BodySystem":
        return cls(
            id=raw.get("id", ""),
            name=raw.get("name", ""),
            description=raw.get("description") or "",
            organs=raw.get("organs", []),
            functions=raw.get("functions", []),
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
    severity: str = "Moderate"
    urgency: Optional[str] = None
    urgency_criteria: str = ""
    contagious: bool = False
    tags: list[str] = field(default_factory=list)
    views_count: int = 0

    # Clinical content
    pathophysiology: str = ""
    clinicopathologic_correlation: str = ""
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
    related_disease_ids: list[str] = field(default_factory=list)
    related_medicine_ids: list[str] = field(default_factory=list)
    source_attribution: str = ""
    clinical_references: list[ClinicalReference] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Disease":
        """Build from a raw record.

        Accepts both camelCase (the original JSON export) and snake_case
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
            causes=raw.get("causes", []),
            risk_factors=pick("riskFactors", "risk_factors", []),
            symptoms=[
                SymptomLink.from_dict(s) for s in raw.get("symptoms", [])
            ],
            differential_diagnosis=[
                Differential.from_dict(d)
                for d in pick("differentialDiagnosis", "differential_diagnosis", [])
            ],
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
            related_disease_ids=pick(
                "relatedDiseaseIds", "related_disease_ids", []
            ),
            related_medicine_ids=pick(
                "relatedMedicineIds", "related_medicine_ids", []
            ),
            source_attribution=pick(
                "sourceAttribution", "source_attribution", ""
            ),
            clinical_references=[
                ClinicalReference.from_dict(r)
                for r in pick("clinicalReferences", "clinical_references", [])
            ],
        )

    # ------------------------------------------------------------ behaviour

    @property
    def hallmark_symptom_ids(self) -> list[str]:
        """Symptoms flagged as primary — the cardinal presentation."""
        return [s.symptom_id for s in self.symptoms if s.is_primary]

    @property
    def urgency_label(self) -> str:
        """Human-readable urgency. None means nobody has assessed it yet."""
        if not self.urgency:
            return "Not specified"
        return {
            "SELF_CARE": "Self-care",
            "SEE_DOCTOR_SOON": "See a clinician",
            "SEEK_URGENT_CARE": "Seek urgent care",
            "EMERGENCY": "Emergency",
        }.get(self.urgency, self.urgency.replace("_", " ").title())

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