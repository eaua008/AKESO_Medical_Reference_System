"""Domain model for the Medicine Reference (8-part clinical monograph).

Named MedicineMonograph, not Medicine, because models/disease.py already has
a Medicine: that one is the *pairing* between a drug and one condition
(safety, note), while this is the full drug entry. Two different things that
happen to share a word.

Linked conditions come from the disease_medicines join table, so "what is
paracetamol used for" and "what treats dengue" stay one stored fact.
"""

import json
from dataclasses import asdict, dataclass, field

# Fact kinds, matching the CHECK constraint on medicine_facts.kind.
BRAND_PH, BRAND_INTL = "brand_ph", "brand_intl"
INDICATION, ADVERSE, CONTRAINDICATION, INTERACTION = (
    "indication", "adverse", "contraindication", "interaction")

# Regulatory classes for the filter. The key is what is stored.
REGULATORY_CLASSES = (
    ("OTC", "OTC (Over-the-Counter)"),
    ("Prescription", "Rx (Prescription)"),
    ("Controlled", "Controlled substance"),
)


@dataclass
class MedicineReference:
    """A citation. is_mother_book marks the Tier 1 primary textbook."""

    source_name: str
    citation_text: str = ""
    url: str = ""
    is_mother_book: bool = False


@dataclass
class LinkedCondition:
    """A disease this drug is listed against, from disease_medicines."""

    disease_id: str
    name: str
    severity: str = ""
    safety: str = ""      # safety of THIS drug for THAT condition
    note: str = ""


# Dosage table (medicine_doses / medicine_dose_notes). Population groups in
# display order; anything else is shown after them under its own name.
POPULATIONS = (("adult", "Adults"), ("child", "Children"), ("neonate", "Newborns"))

# Panels under the dosage table, in display order: kind -> title. A panel is
# shown only when the medicine has notes of that kind.
DOSE_NOTE_KINDS = (
    ("renal", "Dose changes \u00b7 kidney function"),
    ("hepatic", "Dose changes \u00b7 liver"),
    ("elderly", "Older adults"),
    ("pregnancy", "Pregnancy and breastfeeding"),
    ("administration", "How to give it"),
    ("forms_ph", "Forms in the Philippines"),
    ("monitor", "Monitor"),
)


@dataclass
class DoseRow:
    """One line of the dosage table."""

    population: str              # "adult", "child", "neonate"
    indication: str
    route: str = ""              # "PO", "IV", "IM", "Topical"...
    dose: str = ""               # "500 mg", "15 mg/kg", "40-90 mg/kg/day \u00f7 3"
    frequency: str = ""
    duration: str = ""
    max_dose: str = ""
    source: str = ""             # short tag: "PNF", "WHO", "Label \u00b7 FDA PH"
    note: str = ""               # small grey line under the indication


@dataclass
class DoseNote:
    """One line in a panel under the table (kidney band, a form, a check)."""

    kind: str                    # one of DOSE_NOTE_KINDS
    content: str
    label: str = ""              # left column, e.g. "CrCl 10-30"
    source: str = ""


@dataclass
class DoseSource:
    """Where a dosing row comes from. DoseRow.source / DoseNote.source hold
    the short tag ("Label \u00b7 FDA PH"); this is the full citation for it,
    shown in the references section with its own DOSING badge."""

    tag: str
    source_name: str
    citation_text: str = ""
    url: str = ""
    is_mother_book: bool = False      # never; lets it sit in the reference grid


@dataclass
class MedicineMonograph:
    id: str
    name: str
    generic_name: str = ""
    international_generic_name: str = ""
    drug_class: str = ""
    category: str = "Prescription"
    dosage_text: str = ""
    storage: str = ""
    black_box_warning: str = ""
    source_attribution: str = ""
    ph_brands: list[str] = field(default_factory=list)
    intl_brands: list[str] = field(default_factory=list)
    indications: list[str] = field(default_factory=list)
    adverse_reactions: list[str] = field(default_factory=list)
    contraindications: list[str] = field(default_factory=list)
    interactions: list[str] = field(default_factory=list)
    references: list[MedicineReference] = field(default_factory=list)
    conditions: list[LinkedCondition] = field(default_factory=list)
    doses: list[DoseRow] = field(default_factory=list)
    dose_notes: list[DoseNote] = field(default_factory=list)
    dose_sources: list[DoseSource] = field(default_factory=list)

    @property
    def has_dose_table(self) -> bool:
        return bool(self.doses)

    def dose_groups(self) -> list[tuple[str, list[DoseRow]]]:
        """[("Adults", rows), ("Children", rows)...] in display order."""
        known = dict(POPULATIONS)
        order = [key for key, _ in POPULATIONS]
        extra = [p for p in dict.fromkeys(r.population for r in self.doses) if p not in known]
        groups = []
        for key in order + extra:
            rows = [r for r in self.doses if r.population == key]
            if rows:
                groups.append((known.get(key, key.title()), rows))
        return groups

    def dose_source(self, tag: str):
        return next((s for s in self.dose_sources if s.tag == tag), None)

    def notes_of(self, kind: str) -> list[DoseNote]:
        return [n for n in self.dose_notes if n.kind == kind]

    @property
    def is_otc(self) -> bool:
        return self.category.lower().startswith("otc")

    @property
    def category_label(self) -> str:
        if self.is_otc:
            return "OTC (OVER-THE-COUNTER)"
        if self.category.lower().startswith("controlled"):
            return "CONTROLLED SUBSTANCE"
        return "RX (PRESCRIPTION)"

    @property
    def category_key(self) -> str:
        if self.is_otc:
            return "otc"
        return "controlled" if self.category.lower().startswith("controlled") else "rx"

    @property
    def category_display(self) -> str:
        """Title case, but without .title() mangling "OTC" into "Otc"."""
        if self.is_otc:
            return "Over-the-Counter (OTC)"
        if self.category.lower().startswith("controlled"):
            return "Controlled Substance"
        return "Prescription (Rx)"

    @property
    def storage_summary(self) -> str:
        """Short enough for the metadata rail: "Store below 30 C..." -> "<30 C"."""
        if not self.storage:
            return ""
        import re
        match = re.search(r"(below|above|under|at)\s*([\d.]+\s*\u00b0?C)", self.storage, re.I)
        if match:
            prefix = "<" if match.group(1).lower() in ("below", "under") else ">"
            return prefix + match.group(2).replace(" ", "")
        first = self.storage.split(".")[0]
        return first if len(first) <= 24 else first[:24].rsplit(" ", 1)[0] + "\u2026"

    @property
    def has_black_box(self) -> bool:
        return bool(self.black_box_warning.strip())

    @property
    def generic_label(self) -> str:
        return self.international_generic_name or self.generic_name or self.name

    @property
    def mother_book(self):
        return next((r for r in self.references if r.is_mother_book), None)

    @property
    def supporting_references(self) -> list[MedicineReference]:
        return [r for r in self.references if not r.is_mother_book]

    def as_text(self) -> str:
        """Plain-text monograph for the Copy buttons."""
        lines = [f"{self.name} ({self.generic_label})",
                 f"Class: {self.drug_class}",
                 f"Category: {self.category_display}"]
        if self.ph_brands:
            lines.append("Philippine brands: " + ", ".join(self.ph_brands))
        if self.indications:
            lines.append("Indications: " + "; ".join(self.indications))
        if self.doses:
            lines.append("Dosage:")
            for title, rows in self.dose_groups():
                lines.append(f"  {title}")
                for r in rows:
                    parts = [r.route, r.dose, r.frequency, r.duration]
                    line = f"    {r.indication}: " + ", ".join(x for x in parts if x)
                    if r.max_dose:
                        line += f" (max {r.max_dose})"
                    lines.append(line)
        elif self.dosage_text:
            lines.append(f"Dosage: {self.dosage_text}")
        if self.contraindications:
            lines.append("Contraindications: " + "; ".join(self.contraindications))
        if self.has_black_box:
            lines.append(f"BLACK BOX WARNING: {self.black_box_warning}")
        mother = self.mother_book
        if mother:
            lines.append(f"Reference: {mother.source_name}")
        lines.append("Akeso study reference. Not a prescription.")
        return "\n".join(lines)


# ---------------------------------------------------- cache serialisation

def medicine_to_json(medicine: MedicineMonograph) -> str:
    return json.dumps(asdict(medicine))


def medicine_from_json(text: str) -> MedicineMonograph:
    data = json.loads(text)
    data["references"] = [MedicineReference(**r) for r in data.get("references", [])]
    data["conditions"] = [LinkedCondition(**c) for c in data.get("conditions", [])]
    data["doses"] = [DoseRow(**d) for d in data.get("doses", [])]
    data["dose_notes"] = [DoseNote(**n) for n in data.get("dose_notes", [])]
    data["dose_sources"] = [DoseSource(**s) for s in data.get("dose_sources", [])]
    known = set(MedicineMonograph.__dataclass_fields__)
    return MedicineMonograph(**{k: v for k, v in data.items() if k in known})