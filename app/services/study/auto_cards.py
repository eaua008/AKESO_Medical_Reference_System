"""Flashcards made on this computer from the encyclopedia ("Auto" cards), v2.

Cards that teach rather than list. Nothing here is invented: every card is
built only from what the disease, symptom or medicine entry already says,
and a template is skipped when its data is missing or too thin. No network.

Keys are stable, never random:

    auto2:<kind>:<entry id>:<template>[:<detail>]

The first generation ("auto:..." keys) is retired: those cards are no
longer built, but their review history stays where it is.

    Disease    dz_picture  clinical picture MCQ (+ how to tell the others apart)
               dz_vs       "X vs Y: the key difference" (from differentials)
               dz_mech     mechanism cloze (from pathophysiology)
               dz_redflag  which finding means urgent care (MCQ)
               dz_tx       which medicine is used / should be avoided, and why
               dz_feature  skipped: needs a diagnostic-criteria field
    Medicine   rx_calc     weight-based dose, worked step by step
               rx_dose     adult dose and how often
               rx_class    drug class (MCQ)
               rx_se       which is NOT an adverse effect (MCQ)
               rx_contra   contraindicated in which situation (MCQ)
               rx_renal    kidney / liver dose changes
               rx_ix       interaction risk
    Symptom    sx_cause    a common cause (MCQ)
               sx_redflag  skipped: needs non-red-flag features to compare with

Every card then passes the gates in card_gates.py.
"""

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Iterable, Optional

from app.models.study import Card, CardType, Choice, Deck, Origin
from app.services.study import card_gates as G
from app.services.study.dose_calc import work_out

PREFIX = "auto2"
WEIGHTS = (10, 15, 20, 25, 30)
MECH_WORDS = ("because", "leads to", "lead to", "causes", "causing", "cross-react", "obstruct",
              "inflammation", "deficiency", "triggers", "results in", "damage", "due to")
GENERIC_CONTRA = ("hypersensitivity", "allergy", "allergic", "pregnan", "breastfeed", "lactation",
                  "children", "infants", "neonates")
DISEASE_PRIORITY = ["dz_picture", "dz_vs", "dz_tx", "dz_redflag", "dz_mech"]
MEDICINE_PRIORITY = ["rx_calc", "rx_dose", "rx_class", "rx_se", "rx_contra", "rx_renal", "rx_ix"]
CAPS = {"disease": 8, "medicine": 8, "symptom": 3}
TEMPLATE_NAMES = {
    "dz_picture": "Clinical picture", "dz_vs": "Tell them apart", "dz_mech": "Mechanism",
    "dz_redflag": "Red flag", "dz_tx": "Treatment", "dz_feature": "Key features",
    "rx_calc": "Dose calculation", "rx_dose": "Dose recall", "rx_class": "Drug class",
    "rx_se": "Side effects", "rx_contra": "Contraindications", "rx_renal": "Kidney / liver dosing",
    "rx_ix": "Interactions", "sx_cause": "Causes", "sx_redflag": "Red flag"}


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")[:40] or "x"


def _rank(seed: str, items: list, key=lambda x: x) -> list:
    """The same shuffle every time for the same seed."""
    return sorted(items, key=lambda item: hashlib.sha256(f"{seed}|{key(item)}".encode()).hexdigest())


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


def content_hash(card: Card) -> str:
    row = card.to_row()
    for k in ("id", "deck_id", "position", "content_hash"):
        row.pop(k, None)
    return hashlib.sha256(json.dumps(row, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


@dataclass
class AutoSet:
    decks: list[Deck] = field(default_factory=list)
    cards: dict[str, list[Card]] = field(default_factory=dict)     # deck id -> cards
    by_entry: dict[tuple[str, str], list[Card]] = field(default_factory=dict)
    rejected: dict[str, int] = field(default_factory=dict)           # gate problem -> count

    def all_cards(self) -> list[Card]:
        seen, out = set(), []
        for cards in self.cards.values():
            for card in cards:
                if card.card_key not in seen:
                    seen.add(card.card_key)
                    out.append(card)
        return out


class AutoCardBuilder:
    def __init__(self, diseases: Iterable = (), symptoms: Iterable = (), medicines: Iterable = ()) -> None:
        self.diseases = [d for d in diseases if getattr(d, "id", "")]
        self.symptoms = [s for s in symptoms if getattr(s, "id", "")]
        self.medicines = [m for m in medicines if getattr(m, "id", "")]
        self._disease_by_name = {d.name.strip().lower(): d for d in self.diseases}
        self._medicine_by_id = {m.id: m for m in self.medicines}
        self._medicine_by_name = {m.name.strip().lower(): m for m in self.medicines}
        self.rejected: dict[str, int] = {}

    # ------------------------------------------------------------ helpers

    def _card(self, kind: str, entry, template: str, deck_id: str, detail: str = "",
              difficulty: str = "basic", source_field: str = "", **fields) -> Card:
        key = f"{PREFIX}:{kind}:{entry.id}:{template}" + (f":{detail}" if detail else "")
        card = Card(id=key, key=key, deck_id=deck_id, source_kind=kind, source_id=entry.id,
                    family=template, difficulty=difficulty,
                    source_ref={"kind": kind, "id": entry.id, "field": source_field,
                                "system": getattr(entry, "body_system_name", "") or ""}, **fields)
        return card

    def _mcq(self, seed: str, right: tuple[str, str], wrong: list[tuple[str, str]], limit: int = 4) -> list[Choice]:
        """The right answer plus up to `limit` distractors that don't duplicate each other."""
        choices = [Choice(_cap(right[0].strip()), True, right[1])]
        for text, why in wrong:
            if len(choices) > limit:
                break
            if not text.strip() or any(G.overlaps(text, c.text) for c in choices):
                continue
            choices.append(Choice(_cap(text.strip()), False, why))
        by_text = {c.text: c for c in choices}
        return [by_text[t] for t in _rank(seed, list(by_text))]

    def _keep(self, cards: list[Card], forbidden: dict[str, list[str]], kind: str,
              priority: list[str]) -> list[Card]:
        out = []
        for card in cards:
            problems = G.problems(card, forbidden.get(card.family, []))
            if problems:
                self.rejected[problems[0]] = self.rejected.get(problems[0], 0) + 1
                continue
            out.append(card)
        out = G.cap(G.dedupe(out), CAPS[kind], priority)
        for card in out:
            card.content_hash = content_hash(card)
        return out

    def _summary(self, disease) -> str:
        return G.first_sentence(disease.description)

    # ------------------------------------------------------------ disease

    def disease_cards(self, d, deck_id: str) -> list[Card]:
        cards: list[Card] = []
        forbidden: dict[str, list[str]] = {}
        system = d.body_system_name or ""
        primary = sorted([s for s in d.symptoms if s.is_primary and s.name],
                         key=lambda s: (-s.typical_intensity, s.name))
        shown = primary[:3]

        # 1. clinical picture
        if len(shown) >= 2:
            card = self._picture(d, shown, deck_id)
            if card:
                cards.append(card)
                forbidden["dz_picture"] = [d.name]

        # 2. tell them apart
        n = 0
        for diff in d.differential_diagnosis:
            if n >= 3:
                break
            feature = " ".join((diff.distinguishing_feature or "").split())
            if not feature or not diff.condition:
                continue
            n += 1
            why = [s for s in (self._summary(d), self._summary_of(diff.condition)) if s]
            cards.append(self._card(
                "disease", d, "dz_vs", deck_id, detail=slug(diff.condition), difficulty="clinical",
                source_field="differential_diagnosis",
                front=f"{d.name} vs {diff.condition}: what's the key difference?",
                answer_short=feature, back=feature, explanation="\n".join(why)))

        # 3. mechanism cloze
        cards.extend(self._mechanism(d, deck_id))

        # 4. red flag
        red = [r for r in d.emergency_warning_signs if r and r.strip()]
        mild = sorted([s for s in d.symptoms if s.name and not s.is_red_flag],
                      key=lambda s: (s.typical_intensity, s.name))
        mild = [s.name for s in mild if not any(G.similar(s.name, r) for r in red)]
        if red and len(mild) >= 2:
            flag = _rank(d.id, red)[0]
            triage = " ".join((d.urgency_criteria or "").split())
            cards.append(self._card(
                "disease", d, "dz_redflag", deck_id, difficulty="clinical",
                source_field="emergency_warning_signs", type=CardType.MCQ,
                front=f"In {d.name}, which finding means urgent care is needed?",
                choices=self._mcq(d.id + "redflag", (flag, "A warning sign listed for this condition."),
                                  [(m, "A usual symptom of the illness, not a warning sign.") for m in mild[:3]]),
                answer_short=flag, explanation=triage if len(triage) <= 400 else G.first_sentence(triage)))
            forbidden["dz_redflag"] = red

        # 5. treatment
        cards.extend(self._treatment(d, deck_id, forbidden))

        return self._keep(cards, forbidden, "disease", DISEASE_PRIORITY)

    def _summary_of(self, name: str) -> str:
        other = self._disease_by_name.get((name or "").strip().lower())
        if other is None:
            return ""
        sentence = self._summary(other)
        return sentence

    def _picture(self, d, shown, deck_id: str) -> Optional[Card]:
        mine = {s.symptom_id for s in d.symptoms if s.symptom_id}
        shown_ids = [s.symptom_id for s in shown if s.symptom_id]
        rivals = []
        for other in self.diseases:
            if other.id == d.id:
                continue
            theirs = {s.symptom_id for s in other.symptoms if s.symptom_id}
            shared = set(shown_ids) & theirs
            # a disease with the whole picture would be a right answer too: not a fair distractor
            if shared and shared != set(shown_ids):
                rivals.append((-len(shared), other.name.lower(), other, shared, theirs))
        rivals.sort(key=lambda r: (r[0], r[1]))
        if len(rivals) < 2:
            return None
        features = {(x.condition or "").strip().lower(): " ".join((x.distinguishing_feature or "").split())
                    for x in d.differential_diagnosis if x.distinguishing_feature}
        names = {s.symptom_id: s.name for s in d.symptoms}
        wrong, distinguish = [], []
        for _n, _k, other, shared, theirs in rivals[:3]:
            feature = features.get(other.name.strip().lower())
            if feature:
                why = feature
            else:
                common = G.joined([G.lower_first(names[i]) for i in shown_ids if i in shared and i in names])
                missing = next((s.name for s in shown if s.symptom_id not in theirs), "")
                why = (f"Shares {common}, but not typical: {G.lower_first(missing)}"
                       if missing else f"Shares {common}; tell them apart by the rest of the picture")
            wrong.append((other.name, why))
            distinguish.append(f"{other.name}: {why}")
        listed = G.joined([G.lower_first(s.name) for s in shown])
        context = ""
        lead = G.first_sentence(d.clinicopathologic_correlation, 110)
        name_words = {w for w in G.norm(d.name).split() if len(w) > 3}
        if lead and re.search(r"\b(after|weeks?|days?|following|years?|children|adults|age)\b", lead, re.I) \
                and not (name_words & set(G.norm(lead).split())):
            context = f" {lead}"
        front = f"A patient has {listed}.{context} Most likely diagnosis?"
        if len(front) > G.FRONT_MAX:
            front = f"A patient has {listed}. Most likely diagnosis?"
        return self._card(
            "disease", d, "dz_picture", "", difficulty="clinical", source_field="symptoms",
            type=CardType.MCQ, front=front,
            choices=self._mcq(d.id + "picture", (d.name, self._summary(d) or f"The hallmark picture of {d.name}."),
                              wrong),
            answer_short=d.name, explanation=self._summary(d), distinguish="\n".join(distinguish),
            hint=f"Think: {d.body_system_name}" if d.body_system_name else "")

    def _known_terms(self) -> list[str]:
        if not hasattr(self, "_terms"):
            terms = {d.name for d in self.diseases} | {s.name for s in self.symptoms}
            for d in self.diseases:
                terms |= {s.name for s in d.symptoms}
            plain = set()
            for t in terms:
                plain.add(re.sub(r"\s*\([^)]*\)", "", t).strip())
            self._terms = sorted({t for t in plain if len(t) >= 5}, key=len, reverse=True)
        return self._terms

    def _mechanism(self, d, deck_id: str) -> list[Card]:
        out: list[Card] = []
        parts = G.sentences(d.pathophysiology)
        for i, sentence in enumerate(parts):
            if len(out) >= 2:
                break
            if len(sentence.split()) > 45 or not any(w in sentence.lower() for w in MECH_WORDS):
                continue
            term = None
            bracket = re.search(r"\(([^()]{4,40})\)", sentence)
            if bracket and not re.search(r"\d", bracket.group(1)):
                term = bracket.group(1).strip()
            else:
                lowered = sentence.lower()
                term = next((t for t in self._known_terms() if t.lower() in lowered
                             and t.lower() not in d.name.lower()), None)
                if term:
                    start = lowered.index(term.lower())
                    term = sentence[start:start + len(term)]
            if not term or G.norm(term) in G.norm(d.name):
                continue
            blanked = sentence.replace(term, f"{{{{c1::{term}}}}}", 1)
            following = parts[i + 1] if i + 1 < len(parts) and len(parts[i + 1]) <= 260 else ""
            out.append(self._card(
                "disease", d, "dz_mech", deck_id, detail=str(len(out) + 1), difficulty="advanced",
                source_field="pathophysiology", type=CardType.CLOZE,
                cloze_text=f"{d.name}: {blanked}", answer_short=term, explanation=following,
                hint=f"Starts with “{term[0].upper()}”"))
        return out

    def _treatment(self, d, deck_id: str, forbidden: dict) -> list[Card]:
        out: list[Card] = []
        safe = [m for m in d.medicines if (m.safety or "").lower() == "safe" and m.name]
        avoid = [m for m in d.medicines if (m.safety or "").lower() == "avoid" and m.name]
        linked = {m.name.strip().lower() for m in d.medicines}
        # a distractor of the same drug family as anything linked here could be right too
        linked_classes = set()
        for m in d.medicines:
            drug = self._medicine_by_name.get(m.name.strip().lower())
            if drug and drug.drug_class:
                linked_classes.add(G.norm(drug.drug_class).split()[0])
        if safe:
            right = _rank(d.id + "tx", safe, key=lambda m: m.name)[0]
            pool = []
            for other in self.diseases:
                if other.id == d.id or (other.body_system_name or "") == (d.body_system_name or ""):
                    continue
                for m in other.medicines:
                    if (m.safety or "").lower() == "safe" and m.name and m.name.strip().lower() not in linked:
                        drug = self._medicine_by_name.get(m.name.strip().lower())
                        family = G.norm(drug.drug_class).split()[0] if drug and drug.drug_class else ""
                        if family and family in linked_classes:
                            continue
                        pool.append((m.name, other.name))
            seen, wrong = set(), []
            for name, where in _rank(d.id + "txpool", pool, key=lambda p: p[0] + p[1]):
                if name.lower() in seen:
                    continue
                seen.add(name.lower())
                wrong.append((name, f"Listed for {where}, not for {d.name}."))
                if len(wrong) == 3:
                    break
            drug = self._medicine_by_id.get(getattr(right, "id", ""))
            out.append(self._card(
                "disease", d, "dz_tx", deck_id, detail="use", difficulty="clinical", source_field="medicines",
                type=CardType.MCQ, front=f"Which medicine is used for {d.name}?",
                choices=self._mcq(d.id + "txmcq", (right.name, right.note or f"Listed as used for {d.name}."), wrong),
                answer_short=right.name, explanation=right.note,
                hint=f"Think: {drug.drug_class}" if drug and drug.drug_class else ""))
        if avoid and len(safe) >= 2:
            bad = _rank(d.id + "avoid", avoid, key=lambda m: m.name)[0]
            out.append(self._card(
                "disease", d, "dz_tx", deck_id, detail="avoid", difficulty="clinical", source_field="medicines",
                type=CardType.MCQ, front=f"Which medicine should be AVOIDED in {d.name}?",
                choices=self._mcq(d.id + "avoidmcq", (bad.name, bad.note or f"Listed to avoid in {d.name}."),
                                  [(m.name, m.note or f"Listed as safe in {d.name}.") for m in safe[:3]]),
                answer_short=bad.name, explanation=bad.note))
        forbidden["dz_tx"] = []           # distractors come from other diseases' lists by construction
        return out

    # ----------------------------------------------------------- medicine

    def medicine_cards(self, m, deck_id: str) -> list[Card]:
        cards: list[Card] = []
        forbidden: dict[str, list[str]] = {}
        name = m.name
        forms = [n.content for n in m.dose_notes if n.kind == "forms_ph"]

        # 7. dose calculation
        calc = 0
        for row in m.doses:
            if calc >= 2 or (row.population or "").lower() == "adult" or not row.indication:
                continue
            for w in _rank(m.id + row.indication, list(WEIGHTS))[:2]:
                if calc >= 2:
                    break
                worked = work_out(row.dose, row.frequency, row.max_dose, w, forms)
                if worked is None:
                    break
                calc += 1
                cards.append(self._card(
                    "medicine", m, "rx_calc", deck_id, detail=f"{slug(row.indication)}:{w}", difficulty="clinical",
                    source_field="doses", front=f"Child, {w} kg, {row.indication}: {name} dose per intake?",
                    answer_short=worked.answer, back=worked.answer, explanation="\n".join(worked.steps),
                    hint="Work out mg per kg × weight first, then split into the doses."))

        # 8. dose recall
        seen = set()
        for row in m.doses:
            if len(seen) >= 3:
                break
            if (row.population or "").lower() != "adult" or not row.dose or not row.frequency or not row.indication:
                continue
            key = slug(row.indication)
            if key in seen:
                continue
            seen.add(key)
            extra = [f"Duration: {row.duration}" if row.duration and row.duration not in ("—", "-") else "",
                     f"Max: {row.max_dose}" if row.max_dose and row.max_dose not in ("—", "-") else "",
                     row.note]
            answer = f"{row.dose} {G.lower_first(row.frequency)}"
            cards.append(self._card(
                "medicine", m, "rx_dose", deck_id, detail=key, source_field="doses",
                front=f"{name} for {row.indication} (adult): dose and how often?",
                answer_short=answer, back=answer, explanation="\n".join(e for e in extra if e),
                hint=f"Route: {row.route}" if row.route else ""))

        # 9. class
        if m.drug_class:
            classes = sorted({x.drug_class for x in self.medicines if x.drug_class and x.id != m.id
                              and not G.overlaps(x.drug_class, m.drug_class)})
            wrong = [(c, "Another drug class in Akeso.") for c in _rank(m.id + "class", classes)[:3]]
            cards.append(self._card(
                "medicine", m, "rx_class", deck_id, source_field="drug_class", type=CardType.MCQ,
                front=f"{name} belongs to which drug class?",
                choices=self._mcq(m.id + "classmcq", (m.drug_class, f"{name}: {m.drug_class}."), wrong),
                answer_short=m.drug_class,
                explanation=f"Used for: {G.lower_first(m.indications[0])}." if m.indications else ""))

        # 10. not a side effect
        own = [a.strip() for a in m.adverse_reactions if a and a.strip()]
        if len(own) >= 3:
            pool = []
            for other in self.medicines:
                if other.id == m.id or not other.drug_class or G.norm(other.drug_class).split()[:1] == \
                        G.norm(m.drug_class).split()[:1]:
                    continue
                for effect in other.adverse_reactions:
                    if effect and not any(G.similar(effect, o) for o in own):
                        pool.append((effect.strip(), other.name))
            if pool:
                effect, source = _rank(m.id + "se", pool, key=lambda p: p[0] + p[1])[0]
                cards.append(self._card(
                    "medicine", m, "rx_se", deck_id, difficulty="clinical", source_field="adverse",
                    type=CardType.MCQ, front=f"Which is NOT an adverse effect of {name}?",
                    choices=self._mcq(m.id + "semcq", (effect, f"Listed for {source}, not for {name}."),
                                      [(o, f"A listed adverse effect of {name}.") for o in _rank(m.id, own)[:3]]),
                    answer_short=effect, explanation=f"“{effect}” comes from {source}'s list."))
                forbidden["rx_se"] = []

        # 11. contraindication
        contra = [c.strip() for c in m.contraindications if c and c.strip()]
        if contra:
            right = _rank(m.id + "contra", contra)[0]
            pool = []
            for other in self.medicines:
                if other.id == m.id or not other.drug_class or G.norm(other.drug_class).split()[:1] == \
                        G.norm(m.drug_class).split()[:1]:
                    continue
                for c in other.contraindications:
                    low = (c or "").lower()
                    if c and not any(g in low for g in GENERIC_CONTRA) and not any(G.similar(c, x) for x in contra):
                        pool.append(c.strip())
            wrong = [(c, "Listed for another medicine, not this one.") for c in _rank(m.id + "cpool", pool)[:3]]
            if len(wrong) >= 2:
                cards.append(self._card(
                    "medicine", m, "rx_contra", deck_id, difficulty="clinical", source_field="contraindication",
                    type=CardType.MCQ, front=f"{name} is contraindicated in which situation?",
                    choices=self._mcq(m.id + "contramcq", (right, f"A listed contraindication of {name}."), wrong),
                    answer_short=right))
                forbidden["rx_contra"] = contra

        # 12. kidney / liver
        notes = [n for n in m.dose_notes if n.kind in ("renal", "hepatic") and n.label and n.content]
        notes.sort(key=lambda n: (n.content.strip().lower() in ("no change", "no dose change"), n.kind))
        for note in notes[:2]:
            organ = "kidney function" if note.kind == "renal" else "liver"
            cards.append(self._card(
                "medicine", m, "rx_renal", deck_id, detail=slug(f"{note.kind}-{note.label}"), difficulty="advanced",
                source_field=f"dose_notes:{note.kind}", front=f"{name}, {organ} {note.label}: dose change?",
                answer_short=note.content.strip(), back=note.content.strip()))

        # 13. interactions
        n = 0
        for fact in m.interactions:
            if n >= 2:
                break
            match = re.match(r"^([^:]{2,40}):\s*(.+)$", (fact or "").strip())
            if not match:
                continue
            other, risk = match.group(1).strip(), match.group(2).strip()
            n += 1
            cards.append(self._card(
                "medicine", m, "rx_ix", deck_id, detail=slug(other), difficulty="clinical",
                source_field="interaction", front=f"{name} + {other}: what's the risk?",
                answer_short=_cap(risk), back=_cap(risk)))

        return self._keep(cards, forbidden, "medicine", MEDICINE_PRIORITY)

    # ------------------------------------------------------------ symptom

    def symptom_cards(self, s, deck_id: str) -> list[Card]:
        cards: list[Card] = []
        causes = [c.strip() for c in s.causes if c and c.strip()]
        if causes:
            right = _rank(s.id + "cause", causes)[0]
            pool = []
            for other in self.symptoms:
                if other.id == s.id or (other.body_system_name or "") == (s.body_system_name or ""):
                    continue
                for c in other.causes:
                    if c and not any(G.similar(c, x) for x in causes):
                        pool.append((c.strip(), other.name))
            wrong = [(c, f"A cause of {where.lower()}, not listed for {s.name.lower()}.")
                     for c, where in _rank(s.id + "cpool", pool, key=lambda p: p[0] + p[1])[:3]]
            others = [c for c in causes if c != right][:3]
            cards.append(self._card(
                "symptom", s, "sx_cause", deck_id, source_field="causes", type=CardType.MCQ,
                front=f"Which is a common cause of {G.lower_first(s.name)}?",
                choices=self._mcq(s.id + "causemcq", (right, f"Listed as a cause of {G.lower_first(s.name)}."), wrong),
                answer_short=right,
                explanation=f"Other causes listed: {G.joined([G.lower_first(o) for o in others])}." if others else "",
                hint=f"Think: {s.body_system_name}" if s.body_system_name else ""))
        return self._keep(cards, {"sx_cause": causes}, "symptom", ["sx_cause"])

    # -------------------------------------------------------------- decks

    def build(self) -> AutoSet:
        result = AutoSet()
        self.rejected = {}

        def group_deck(deck_id: str, title: str, subject: str, group: str) -> list[Card]:
            if deck_id not in result.cards:
                result.decks.append(Deck(id=deck_id, title=title, subject_id=subject,
                                         origin=Origin.AUTO, group=group, status="published"))
                result.cards[deck_id] = []
            return result.cards[deck_id]

        for m in sorted(self.medicines, key=lambda x: x.name.lower()):
            group = m.drug_class.split("(")[0].strip() if m.drug_class else "Other medicines"
            deck_id = f"auto-deck:pharmacology:{slug(group)}"
            cards = self.medicine_cards(m, deck_id)
            for card in cards:
                card.deck_id = deck_id
            if cards:
                group_deck(deck_id, f"Pharmacology · {group} (Auto)", "pharmacology", group).extend(cards)
                result.by_entry[("medicine", m.id)] = cards
        for d in sorted(self.diseases, key=lambda x: x.name.lower()):
            group = d.body_system_name or "Other conditions"
            deck_id = f"auto-deck:pathology:{slug(group)}"
            cards = self.disease_cards(d, deck_id)
            for card in cards:
                card.deck_id = deck_id
            if cards:
                group_deck(deck_id, f"Pathology · {group} (Auto)", "pathology", group).extend(cards)
                result.by_entry[("disease", d.id)] = cards
        for s in sorted(self.symptoms, key=lambda x: x.name.lower()):
            group = s.body_system_name or "Other symptoms"
            deck_id = f"auto-deck:pathology:{slug(group)}"
            cards = self.symptom_cards(s, deck_id)
            for card in cards:
                card.deck_id = deck_id
            if cards:
                group_deck(deck_id, f"Pathology · {group} (Auto)", "pathology", group).extend(cards)
                result.by_entry[("symptom", s.id)] = cards
        result.decks.sort(key=lambda deck: deck.title.lower())
        result.rejected = dict(self.rejected)
        return result

    def entry_deck(self, auto: AutoSet, kind: str, entry_id: str, name: str) -> Optional[Deck]:
        """"Study {name} cards": a deck of one entry's cards (opened from its page)."""
        cards = auto.by_entry.get((kind, entry_id))
        if not cards:
            return None
        deck_id = f"auto-deck:entry:{kind}:{entry_id}"
        if deck_id not in auto.cards:
            auto.cards[deck_id] = list(cards)
        subject = "pharmacology" if kind == "medicine" else "pathology"
        return Deck(id=deck_id, title=f"{name} (Auto)", subject_id=subject, origin=Origin.AUTO,
                    status="published", source=(kind, entry_id))
