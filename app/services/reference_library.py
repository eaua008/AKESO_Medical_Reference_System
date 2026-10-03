"""The reference column's data: search and compact monographs.

One place that turns diseases, symptoms and medicines into the same simple
shape, so the Study Notebook can show any of them without knowing their
models:

    search(query, kind)     -> list[RefHit]
    monograph(kind, id)     -> Monograph (header, badges, sections)

No Qt here. Every section's text comes straight from the encyclopedias,
the same content the student can open in the full modules.
"""

import html
from dataclasses import dataclass, field
from typing import Optional

DISEASE, SYMPTOM, MEDICINE = "disease", "symptom", "medicine"
KINDS = (DISEASE, SYMPTOM, MEDICINE)
KIND_LABELS = {DISEASE: "Disease", SYMPTOM: "Symptom", MEDICINE: "Medicine"}

URGENCY_LABELS = {
    "EMERGENCY": "Emergency",
    "SEEK_URGENT_CARE": "Urgent",
    "SEE_DOCTOR_SOON": "See doctor soon",
    "SELF_CARE": "Self-care",
}


@dataclass
class RefHit:
    kind: str
    id: str
    name: str
    subtitle: str = ""


@dataclass
class Section:
    title: str
    paragraphs: list[str] = field(default_factory=list)
    bullets: list[str] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return not any(p.strip() for p in self.paragraphs) and not self.bullets

    def to_html(self) -> str:
        """For "Insert into notes": plain paragraphs and a bullet list."""
        parts = [f"<p>{html.escape(p)}</p>" for p in self.paragraphs if p.strip()]
        if self.bullets:
            items = "".join(f"<li>{html.escape(b)}</li>" for b in self.bullets)
            parts.append(f"<ul>{items}</ul>")
        return "".join(parts)


@dataclass
class Monograph:
    kind: str
    id: str
    name: str
    subtitle: str = ""
    badges: list[tuple[str, str]] = field(default_factory=list)     # (text, tone)
    sections: list[Section] = field(default_factory=list)


class ReferenceLibrary:
    def __init__(self, diseases, symptoms, medicines) -> None:
        # DiseaseService, SymptomService, MedicineService
        self._diseases = diseases
        self._symptoms = symptoms
        self._medicines = medicines

    # ------------------------------------------------------------ search

    def search(self, query: str, kind: str = "", limit: int = 60) -> list[RefHit]:
        words = query.lower().split()
        hits: list[RefHit] = []

        def keep(*texts: str) -> bool:
            haystack = " ".join(t for t in texts if t).lower()
            return all(w in haystack for w in words)

        if kind in ("", DISEASE):
            for d in self._safe(self._diseases.all_diseases):
                if keep(d.name, d.scientific_name, " ".join(d.tags)):
                    hits.append(RefHit(DISEASE, d.id, d.name,
                                       d.scientific_name or d.body_system_name))
        if kind in ("", SYMPTOM):
            for s in self._safe(self._symptoms.all_symptoms):
                if keep(s.name, s.scientific_name, " ".join(s.tags)):
                    hits.append(RefHit(SYMPTOM, s.id, s.name, s.system_label))
        if kind in ("", MEDICINE):
            for m in self._safe(self._medicines.all_medicines):
                if keep(m.name, m.generic_name, m.international_generic_name, m.drug_class,
                        " ".join(m.ph_brands), " ".join(m.intl_brands)):
                    hits.append(RefHit(MEDICINE, m.id, m.name, m.drug_class))

        # Names that start with the query first, then alphabetical.
        first = words[0] if words else ""
        hits.sort(key=lambda h: (not h.name.lower().startswith(first), h.name.lower()))
        return hits[:limit]

    @staticmethod
    def _safe(source) -> list:
        try:
            return list(source())
        except Exception:           # cache not synced yet: search what we have
            return []

    def name(self, kind: str, item_id: str) -> str:
        mono = self.monograph(kind, item_id)
        return mono.name if mono else ""

    # ---------------------------------------------------------- monographs

    def monograph(self, kind: str, item_id: str) -> Optional[Monograph]:
        try:
            if kind == DISEASE:
                d = self._diseases.get(item_id)
                return self._disease(d) if d else None
            if kind == SYMPTOM:
                s = self._symptoms.get(item_id)
                return self._symptom(s) if s else None
            if kind == MEDICINE:
                m = self._medicines.get(item_id)
                return self._medicine(m) if m else None
        except Exception:
            return None
        return None

    @staticmethod
    def _disease(d) -> Monograph:
        badges = [(f"Severity: {d.severity}", "amber" if d.severity in ("Severe", "Critical")
                   else "muted")]
        if d.urgency:
            badges.append((f"Reference urgency: {URGENCY_LABELS.get(d.urgency, d.urgency)}",
                           "danger" if d.urgency == "EMERGENCY" else "primary"))
        if d.contagious:
            badges.append(("Contagious", "danger"))
        hallmarks = [f"{s.name} (hallmark, typical {s.intensity_label})"
                     for s in d.symptoms if s.is_primary]
        others = [f"{s.name} (typical {s.intensity_label})"
                  for s in d.symptoms if not s.is_primary]
        return Monograph(
            kind=DISEASE, id=d.id, name=d.name,
            subtitle=" · ".join(x for x in (d.scientific_name, d.body_system_name) if x),
            badges=badges,
            sections=[s for s in (
                Section("Overview", [d.description]),
                Section("Pathophysiology", [d.pathophysiology]),
                Section("Hallmark symptoms", bullets=hallmarks + others),
                Section("Causes", bullets=list(d.causes)),
                Section("Risk factors", bullets=list(d.risk_factors)),
                Section("Recommended tests", bullets=list(d.recommended_tests)),
                Section("Differentials", bullets=[
                    f"{x.condition}: {x.distinguishing_feature}"
                    for x in d.differential_diagnosis]),
                Section("Treatment", bullets=list(d.treatments)),
                Section("Warning signs", bullets=list(d.emergency_warning_signs)),
                Section("Urgency criteria", [d.urgency_criteria]),
            ) if not s.empty])

    @staticmethod
    def _symptom(s) -> Monograph:
        badges = [(s.tier_label, "amber" if s.tier_key in ("critical", "high") else "muted")]
        if s.is_red_flag:
            badges.append(("Red flag", "danger"))
        return Monograph(
            kind=SYMPTOM, id=s.id, name=s.name,
            subtitle=" · ".join(x for x in (s.scientific_name, s.system_label) if x),
            badges=badges,
            sections=[x for x in (
                Section("Overview", [s.description]),
                Section("Diagnostic weight",
                        [f"{s.diagnostic_weight}/10. {s.weight_rationale}".strip()]),
                Section("Causes", bullets=list(s.causes)),
                Section("Red flags", bullets=list(s.red_flags)),
                Section("Associated conditions", bullets=[
                    f"{c.name}{' (hallmark)' if c.is_primary else ''}" for c in s.conditions]),
            ) if not x.empty])

    @staticmethod
    def _medicine(m) -> Monograph:
        badges = [(m.category_display, "primary")]
        if m.has_black_box:
            badges.append(("Boxed warning", "danger"))
        overview = [f"Generic name: {m.generic_label}",
                    f"Class: {m.drug_class}" if m.drug_class else ""]
        brands = [*m.ph_brands, *m.intl_brands]
        if brands:
            overview.append("Brands: " + ", ".join(brands))
        return Monograph(
            kind=MEDICINE, id=m.id, name=m.name, subtitle=m.drug_class, badges=badges,
            sections=[x for x in (
                Section("Overview", overview),
                Section("Boxed warning", [m.black_box_warning]),
                Section("Indications", bullets=list(m.indications)),
                Section("Dosage", [m.dosage_text]),
                Section("Contraindications", bullets=list(m.contraindications)),
                Section("Adverse reactions", bullets=list(m.adverse_reactions)),
                Section("Interactions", bullets=list(m.interactions)),
                Section("Linked conditions", bullets=[
                    f"{c.name}{f' ({c.safety})' if c.safety else ''}" for c in m.conditions]),
                Section("Storage", [m.storage]),
            ) if not x.empty])
