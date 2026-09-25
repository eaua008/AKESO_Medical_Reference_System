"""The Symptom Correlation Engine: rule-based weighted matching.

Ported from the Akeso reference build, but scored against the real
encyclopedia rather than a bundled dataset. Everything it needs already
exists in the database:

    symptoms.diagnostic_weight           how much a symptom narrows things down
    disease_symptoms.is_primary          is it a hallmark of this condition
    disease_symptoms.typical_intensity   how severe it usually is here
    disease_symptoms.weight_multiplier   how much this condition leans on it

How a score is produced, for one condition:

    effective weight = symptom weight x multiplier x (1.5 if hallmark)
    maximum          = sum of effective weight x 10 over every hallmark
    earned           = effective weight x reported intensity, adjusted for
                       how closely intensity, onset and duration align
    score            = earned / maximum, then exposure and history boosters

No diagnosis is produced: this ranks conditions worth reading about, and the
view says so. Triage is decided by vitals and red flags first, and only then
by the top match.
"""

from typing import Iterable, Optional

from app.models.checker import (
    COMORBIDITIES,
    EXPOSURES,
    FAMILY_RISKS,
    CheckerInput,
    CheckerResult,
    MatchResult,
    MatchedSymptom,
    Vitals,
)

HALLMARK_BONUS = 1.5     # a hallmark counts for more than an associated sign
MAX_SCORE, MIN_SCORE = 98.0, 12.0   # never claim certainty, never claim zero


class MatchingService:
    """Scores the encyclopedia against what the user reported."""

    def __init__(self, disease_source, symptom_source) -> None:
        # Callables, so the engine reads whatever the encyclopedias hold now.
        self._diseases = disease_source
        self._symptoms = symptom_source

    # ------------------------------------------------------------- public

    def evaluate(self, data: CheckerInput) -> CheckerResult:
        if not data.symptoms:
            return CheckerResult(
                triage_level="ROUTINE",
                triage_label="No symptoms entered",
                triage_action="Add at least one symptom to evaluate.",
                specificity_guidance="Add two or three symptoms to narrow the differential.",
            )

        weights = {s.id: s.diagnostic_weight for s in self._symptoms()}
        reported = {s.symptom_id: s for s in data.symptoms}

        alerts, vitals_emergency = self._read_vitals(data.vitals)
        matches = []
        for disease in self._diseases():
            match = self._score(disease, reported, weights, data)
            if match is not None:
                matches.append(match)
        matches.sort(key=lambda m: m.rank_value, reverse=True)

        result = CheckerResult(
            matches=matches,
            vital_alerts=alerts,
            suggested_symptoms=self._suggestions(matches, reported),
        )
        self._set_specificity(result, data)
        self._set_triage(result, vitals_emergency, data)
        return result

    # ------------------------------------------------------------ scoring

    def _score(self, disease, reported: dict, weights: dict,
               data: CheckerInput) -> Optional[MatchResult]:
        links = getattr(disease, "symptoms", []) or []
        if not links:
            return None

        earned = max_possible = 0.0
        matched, missing, inconsistent = [], [], []
        alignment_sum = alignment_count = 0

        for link in links:
            base = float(weights.get(link.symptom_id, 6))
            multiplier = float(getattr(link, "weight_multiplier", 1.0) or 1.0)
            typical = float(getattr(link, "typical_intensity", 6) or 6)
            is_primary = bool(getattr(link, "is_primary", False))

            effective = base * multiplier * (HALLMARK_BONUS if is_primary else 1.0)
            max_possible += effective * 10.0

            entry = reported.get(link.symptom_id)
            if entry is None:
                # Only hallmarks count as "missing": an associated sign being
                # absent says little, a hallmark being absent rules a lot out.
                if is_primary:
                    missing.append(link.name)
                continue

            intensity = float(entry.intensity)
            # Intensity alignment: 1.0 when it matches the textbook picture,
            # never below 0.7, so a mismatch weakens rather than erases.
            gap = abs(intensity - typical)
            align = max(0.7, 1.0 - gap / 25.0)
            alignment_sum += align
            alignment_count += 1

            severity = (disease.severity or "").lower()
            acute = severity in ("severe", "critical")
            duration_factor = 1.0
            if acute and entry.duration in ("today", "few_days"):
                duration_factor = 1.15          # acute illness, acute story
            elif acute and entry.duration == "month_plus":
                duration_factor = 0.85          # months of it argues against
            onset_factor = 1.1 if (acute and entry.onset == "sudden") else 1.0

            earned += effective * intensity * align * duration_factor * onset_factor
            matched.append(MatchedSymptom(
                name=link.name, user_intensity=entry.intensity,
                typical_intensity=int(typical), is_primary=is_primary,
                onset=entry.onset, pattern=entry.pattern, trend=entry.trend))

        if not matched or max_possible <= 0:
            return None

        # Reported symptoms this condition does not explain at all.
        linked_ids = {link.symptom_id for link in links}
        inconsistent = [entry.name for sid, entry in reported.items()
                        if sid not in linked_ids]

        raw = earned / max_possible * 100.0
        boost, reasons = self._boosters(disease, data)
        ranked = raw * boost
        # The cap keeps the UI honest (never "100% certain"), but two capped
        # conditions must still rank against each other, so sorting uses the
        # uncapped value.
        score = min(MAX_SCORE, max(MIN_SCORE, ranked))

        return MatchResult(
            disease_id=disease.id, name=disease.name,
            scientific_name=disease.scientific_name or "",
            score=round(score, 1), rank_value=ranked,
            urgency=disease.urgency or "",
            severity=disease.severity or "",
            matched=matched, missing=missing, inconsistent=inconsistent,
            boosters=reasons,
            matched_count=len(matched), total_hallmarks=len(links),
            weighted_sum=int(earned), weighted_max=int(max_possible),
            alignment=int(alignment_sum / alignment_count * 100) if alignment_count else 0,
            emergency_signs=list(getattr(disease, "emergency_warning_signs", []) or []),
        )

    @staticmethod
    def _haystack(disease) -> str:
        """The condition's own words, used to decide which boosters apply."""
        parts = [disease.name, disease.description or "",
                 *(getattr(disease, "causes", []) or []),
                 *(getattr(disease, "risk_factors", []) or []),
                 *(getattr(disease, "tags", []) or [])]
        return " ".join(parts).lower()

    def _boosters(self, disease, data: CheckerInput) -> tuple[float, list[str]]:
        """Exposure and history multipliers, matched against the entry's text.

        Data-driven on purpose: a new mosquito-borne condition is boosted by a
        mosquito bite because its own causes say so, with no code change.
        """
        text = self._haystack(disease)
        boost, reasons = 1.0, []

        for key, label, keywords in EXPOSURES:
            if key not in data.exposures:
                continue
            if key == "sick_contact" and getattr(disease, "contagious", False):
                boost *= 1.20
                reasons.append(f"{label} (+20%: this condition is contagious)")
            elif any(word in text for word in keywords):
                factor = 1.35 if key == "mosquito" else 1.15
                boost *= factor
                reasons.append(f"{label} (+{int((factor - 1) * 100)}%: matches this "
                               "condition's risk factors)")

        for key, label, keywords in COMORBIDITIES:
            if key in data.comorbidities and any(word in text for word in keywords):
                boost *= 1.25
                reasons.append(f"{label} (+25%: named in this condition's risk factors)")

        # First-degree family history, weighted per condition type.
        for key, label, _domain, factor, keywords in FAMILY_RISKS:
            if key in data.family_history and any(word in text for word in keywords):
                boost *= factor
                reasons.append(f"Family history: {label} "
                               f"(+{int((factor - 1) * 100)}%: heritable risk)")

        if data.age >= 55 and "age" in text:
            boost *= 1.10
            reasons.append("Age 55+ (+10%: age is a stated risk factor)")
        return boost, reasons

    # -------------------------------------------------------------- vitals

    @staticmethod
    def _read_vitals(v: Vitals) -> tuple[list[str], bool]:
        """Objective findings. These can force an emergency on their own."""
        alerts, emergency = [], False

        if v.temperature >= 39.0:
            alerts.append(f"Hyperpyrexia: {v.temperature:.1f} °C.")
        elif v.temperature >= 38.0:
            alerts.append(f"Fever confirmed: {v.temperature:.1f} °C.")
        elif v.temperature <= 35.0:
            alerts.append(f"Hypothermia: {v.temperature:.1f} °C.")
            emergency = True

        if v.heart_rate >= 105:
            alerts.append(f"Tachycardia: {v.heart_rate} bpm.")
        elif v.heart_rate <= 50:
            alerts.append(f"Bradycardia: {v.heart_rate} bpm.")

        if v.spo2 <= 92:
            alerts.append(f"Hypoxaemia: SpO2 {v.spo2}% on room air. Needs oxygen.")
            emergency = True
        if v.bp_systolic >= 180 or v.bp_diastolic >= 120:
            alerts.append(f"Hypertensive crisis: {v.bp_systolic}/{v.bp_diastolic} mmHg.")
            emergency = True
        elif v.bp_systolic < 90:
            alerts.append(f"Hypotension, shock risk: systolic {v.bp_systolic} mmHg.")
            emergency = True
        if v.resp_rate >= 24:
            alerts.append(f"Tachypnoea: {v.resp_rate} breaths/min.")
        return alerts, emergency

    # ------------------------------------------------------ specificity

    @staticmethod
    def _set_specificity(result: CheckerResult, data: CheckerInput) -> None:
        """How well the reported picture distinguishes between conditions."""
        count = len(data.symptoms)
        hallmarks = sum(1 for m in result.matches[:3] if m.has_primary)
        if count == 1:
            result.specificity, result.specificity_label = 25, "Low"
            result.specificity_guidance = (
                "One symptom rarely separates conditions. Add two or three more.")
        elif count == 2:
            result.specificity, result.specificity_label = 55, "Moderate"
            result.specificity_guidance = (
                "Consistent with several causes. More detail would narrow it.")
        elif count >= 4 and hallmarks:
            result.specificity, result.specificity_label = 92, "Very high"
            result.specificity_guidance = (
                "A distinct pattern of hallmark features.")
        else:
            result.specificity, result.specificity_label = 75, "High"
            result.specificity_guidance = "Good coverage of hallmark features."

    # ----------------------------------------------------------- triage

    def _set_triage(self, result: CheckerResult, vitals_emergency: bool,
                    data: CheckerInput) -> None:
        """Vitals and red flags decide first; the ranking only breaks ties.

        A high-scoring mild condition must never soften an emergency vital
        sign, so the checks run in that order.
        """
        top = result.top
        severe_symptom = any(s.intensity >= 9 for s in data.symptoms)

        if top:
            result.emergency_warnings = top.emergency_signs

        # Any credible emergency match escalates, not only the top one: a
        # condition ranked second at 98% is still an emergency, and softening
        # that to "same-day" would be the worst kind of wrong here.
        emergency_match = next(
            (m for m in result.matches[:5]
             if m.urgency == "EMERGENCY" and m.score >= 55), None)

        if vitals_emergency or emergency_match:
            result.triage_level = "EMERGENCY"
            result.triage_label = "Level 1: emergency, seek care now"
            result.triage_action = ("Call 911 or go to the nearest emergency "
                                    "department immediately.")
            result.triage_rationale = (
                "Critical vital signs detected." if vitals_emergency else
                f"{emergency_match.name} scores {emergency_match.score:.0f}% and can "
                "deteriorate within hours.")
            if emergency_match and not vitals_emergency:
                result.emergency_warnings = emergency_match.emergency_signs
        elif top and (top.urgency == "SEEK_URGENT_CARE" or severe_symptom):
            result.triage_level = "URGENT"
            result.triage_label = "Level 2: same-day assessment"
            result.triage_action = ("See a doctor today, at an urgent care centre or "
                                    "your nearest clinic.")
            result.triage_rationale = ("Severe reported intensity." if severe_symptom
                                       else "The closest match needs same-day review.")
        elif top and top.urgency == "SEE_DOCTOR_SOON":
            result.triage_level = "PROMPT"
            result.triage_label = "Level 3: see a doctor within 1 to 3 days"
            result.triage_action = "Book an appointment with your primary care doctor."
            result.triage_rationale = "Subacute picture needing a proper workup."
        else:
            result.triage_level = "ROUTINE"
            result.triage_label = "Level 4: self-care and monitoring"
            result.triage_action = ("Rest, fluids and monitoring. See a doctor if it "
                                    "worsens or does not settle.")
            result.triage_rationale = "Nothing reported meets an urgent threshold."

    # -------------------------------------------------------- suggestions

    @staticmethod
    def _suggestions(matches: Iterable[MatchResult],
                     reported: dict) -> list[tuple[str, str, int]]:
        """Symptoms worth asking about: they appear in several top matches.

        Returns (symptom name, symptom name, how many conditions) so the view
        can offer them as one-click additions.
        """
        tally: dict[str, int] = {}
        for match in list(matches)[:6]:
            for name in match.missing:
                tally[name] = tally.get(name, 0) + 1
        ranked = sorted(tally.items(), key=lambda item: -item[1])
        return [(name, name, count) for name, count in ranked[:6] if count >= 1]