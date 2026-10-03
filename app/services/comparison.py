"""Differential comparison between two or three conditions.

Pure computation over Disease objects — no database, no widgets. That makes
the set arithmetic testable on its own, and it keeps the view from doing
clinical reasoning in a paint method.

A deliberate limit: everything here is derived from recorded data. Nothing
generates clinical prose. Where the UI shows a "differentiating question",
it is assembling facts that already exist in the database (hallmark symptoms,
contagiousness, distinctive tests), not writing new clinical claims.
"""

from dataclasses import dataclass, field

from app.models.disease import Disease, SymptomLink


@dataclass
class SharedSymptom:
    """One symptom present in every condition being compared.

    presentations maps disease id -> the link for that disease, so the view
    can show how the same symptom differs in intensity and cardinality
    across conditions.
    """

    symptom_id: str
    name: str
    presentations: dict[str, SymptomLink] = field(default_factory=dict)

    def intensity_for(self, disease_id: str) -> int:
        link = self.presentations.get(disease_id)
        return link.typical_intensity if link else 0

    def is_cardinal_for(self, disease_id: str) -> bool:
        link = self.presentations.get(disease_id)
        return bool(link and link.is_primary)

    def distinction(self, diseases: list[Disease]) -> str:
        """State the factual difference, not a paraphrase of the bars.

        Reports the intensity gap and which condition carries it more
        strongly. Where intensities match, says so rather than inventing a
        distinction that is not in the data.
        """
        scored = [
            (d, self.intensity_for(d.id))
            for d in diseases
            if d.id in self.presentations
        ]
        if len(scored) < 2:
            return "Recorded in only one of the selected conditions."

        scored.sort(key=lambda pair: pair[1], reverse=True)
        top, top_score = scored[0]
        second, second_score = scored[1]

        cardinal_in = [d.name for d in diseases if self.is_cardinal_for(d.id)]

        if top_score == second_score:
            base = (
                f"Equal recorded intensity ({top_score}/10) across both "
                "conditions; intensity alone does not separate them."
            )
        else:
            base = (
                f"Recorded {top_score - second_score} point(s) higher in "
                f"{top.name} ({top_score}/10 vs {second_score}/10)."
            )

        if cardinal_in:
            base += f" Cardinal sign in: {', '.join(cardinal_in)}."
        else:
            base += " Not cardinal in either condition."
        return base


@dataclass
class Comparison:
    """The result of comparing two or three conditions."""

    diseases: list[Disease]
    shared: list[SharedSymptom] = field(default_factory=list)
    unique: dict[str, list[SymptomLink]] = field(default_factory=dict)

    @property
    def names(self) -> list[str]:
        return [d.name for d in self.diseases]

    def unique_for(self, disease_id: str) -> list[SymptomLink]:
        return self.unique.get(disease_id, [])

    def differentiating_facts(self) -> list[str]:
        """Factual contrasts drawn straight from recorded fields.

        Each line is something stored in the database. Nothing here is
        inferred or written fresh.
        """
        facts: list[str] = []

        for disease in self.diseases:
            transmissible = "Transmissible" if disease.contagious else "Non-communicable"
            facts.append(
                f"{disease.name}: {transmissible}, severity recorded as "
                f"{disease.severity}."
            )

        # Rule-in tests, where each condition has at least one recorded.
        with_tests = [d for d in self.diseases if d.recommended_tests]
        if len(with_tests) >= 2:
            pairs = " vs ".join(
                f"{d.recommended_tests[0]} ({d.name})" for d in with_tests
            )
            facts.append(f"Distinctive first-line test: {pairs}")

        onset = [d for d in self.diseases if d.onset_progression]
        if len(onset) >= 2:
            facts.append(
                "Onset patterns differ; see the progression cards above."
            )
        return facts

    def hallmark_summary(self) -> str:
        """One line naming each condition's cardinal signs.

        Returns an empty string when no condition has recorded hallmarks,
        rather than producing a question with blanks in it.
        """
        parts = []
        for disease in self.diseases:
            hallmarks = [s.name for s in disease.hallmark_symptoms if s.name]
            if hallmarks:
                parts.append(f"{disease.name} ({', '.join(hallmarks)})")

        if len(parts) < 2:
            return ""
        return " or ".join(parts)


def compare(diseases: list[Disease]) -> Comparison:
    """Split symptoms into shared and unique across the given conditions.

    Shared means present in EVERY condition, not merely more than one — with
    three conditions selected, a symptom in two of them is still unique to
    that pair, and calling it shared would be wrong.
    """
    result = Comparison(diseases=diseases)
    if len(diseases) < 2:
        return result

    by_disease = {
        d.id: {s.symptom_id: s for s in d.symptoms} for d in diseases
    }

    id_sets = [set(links.keys()) for links in by_disease.values()]
    shared_ids = set.intersection(*id_sets) if id_sets else set()

    for symptom_id in shared_ids:
        first = next(
            links[symptom_id]
            for links in by_disease.values()
            if symptom_id in links
        )
        shared = SharedSymptom(symptom_id=symptom_id, name=first.name)
        for disease in diseases:
            link = by_disease[disease.id].get(symptom_id)
            if link:
                shared.presentations[disease.id] = link
        result.shared.append(shared)

    # Highest combined intensity first — the ones worth scanning.
    result.shared.sort(
        key=lambda s: -sum(
            s.intensity_for(d.id) for d in diseases
        )
    )

    for disease in diseases:
        result.unique[disease.id] = [
            link
            for link in disease.symptoms
            if link.symptom_id not in shared_ids
        ]

    return result