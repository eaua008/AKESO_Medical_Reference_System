"""Auto cards v2: templates, gates, determinism (fixture data, no network)."""

import unittest

from app.models.disease import Differential, Disease, Medicine as DiseaseMedicine, SymptomLink
from app.models.medicine import DoseNote, DoseRow, MedicineMonograph
from app.models.study import Card, CardType, Choice
from app.models.symptom import Symptom
from app.services.study import card_gates as G
from app.services.study.auto_cards import AutoCardBuilder
from app.services.study.dose_calc import work_out


def sym(i, name, intensity=5, primary=True, red=False):
    return SymptomLink(symptom_id=i, name=name, typical_intensity=intensity, is_primary=primary, is_red_flag=red)


def medicines():
    amox = MedicineMonograph(
        id="amoxicillin", name="Amoxicillin", drug_class="Antibiotic (aminopenicillin)",
        indications=["Ear, nose and throat infections"],
        adverse_reactions=["Diarrhea, nausea, vomiting", "Rash", "Anaphylaxis", "Thrush"],
        contraindications=["Suspected infectious mononucleosis"],
        interactions=["Probenecid: increases amoxicillin levels.", "no colon here"],
        doses=[DoseRow("adult", "Community-acquired pneumonia", route="PO", dose="500 mg – 1 g",
                       frequency="Every 8 h", duration="5 days", max_dose="4 g/day"),
               DoseRow("child", "Typhoid fever", dose="100 mg/kg/day ÷ 3", frequency="Every 8 h"),
               DoseRow("child", "Otitis media", dose="40–90 mg/kg/day, divided", frequency="Divided doses")],
        dose_notes=[DoseNote("renal", "At most 500 mg 2× a day", label="GFR 10–30"),
                    DoseNote("forms_ph", "Powder for suspension 250 mg/5 mL")])
    para = MedicineMonograph(id="paracetamol", name="Paracetamol", drug_class="Analgesic",
                             adverse_reactions=["Liver injury", "Skin reactions"],
                             contraindications=["Severe liver disease"])
    allo = MedicineMonograph(id="allopurinol", name="Allopurinol", drug_class="Xanthine oxidase inhibitor",
                             adverse_reactions=["Gout flare at start"], contraindications=["Acute gout attack"])
    osel = MedicineMonograph(id="oseltamivir", name="Oseltamivir", drug_class="Antiviral",
                             adverse_reactions=["Headache"], contraindications=["Kidney failure on dialysis"])
    bare = MedicineMonograph(id="bare", name="Bare drug")
    return [amox, para, allo, osel, bare]


def diseases():
    rf = Disease(
        id="rheumatic_fever", name="Rheumatic fever", body_system_name="Cardiovascular",
        description="Rheumatic fever is an autoimmune illness that follows strep throat. It affects the heart.",
        clinicopathologic_correlation="Symptoms begin about 2-4 weeks after the sore throat. Arthritis migrates.",
        pathophysiology="Antibodies against streptococcal antigens cross-react with heart tissue "
                        "(molecular mimicry). This leads to valvulitis.",
        symptoms=[sym("fever", "Fever", 7), sym("jp", "Joint pain (arthralgia)", 7), sym("js", "Joint swelling", 6),
                  sym("chorea", "Involuntary jerky movements (chorea)", 2, False),
                  sym("rash", "Ring-shaped rash", 1, False), sym("legs", "Leg swelling (edema)", 2, False)],
        emergency_warning_signs=["Swelling of the legs or abdomen", "Chest pain or a racing heartbeat"],
        urgency_criteria="A child with fever and migrating joint pain needs review.",
        differential_diagnosis=[Differential("Septic arthritis", "Usually one hot joint; organisms in joint fluid"),
                                Differential("Gout", "")],
        medicines=[DiseaseMedicine(id="amoxicillin", name="Amoxicillin", safety="safe", note="Eradicates strep."),
                   DiseaseMedicine(id="paracetamol", name="Paracetamol", safety="safe", note="For pain."),
                   DiseaseMedicine(id="cotrim", name="Co-trimoxazole", safety="avoid", note="Not for strep throat.")])
    septic = Disease(id="septic", name="Septic arthritis", body_system_name="Musculoskeletal",
                     description="A bacterial joint infection.",
                     symptoms=[sym("fever", "Fever"), sym("jp", "Joint pain (arthralgia)")])
    gout = Disease(id="gout", name="Gout", body_system_name="Musculoskeletal",
                   symptoms=[sym("jp", "Joint pain (arthralgia)"), sym("js", "Joint swelling")],
                   medicines=[DiseaseMedicine(id="allopurinol", name="Allopurinol", safety="safe")])
    flu = Disease(id="flu", name="Influenza", body_system_name="Respiratory",
                  symptoms=[sym("fever", "Fever")],
                  medicines=[DiseaseMedicine(id="oseltamivir", name="Oseltamivir", safety="safe")])
    return [rf, septic, gout, flu, Disease(id="empty", name="Empty")]


def symptoms():
    return [Symptom(id="cough", name="Cough", body_system_name="Respiratory",
                    causes=["Viral infection", "Asthma", "Smoking"], red_flags=["Coughing blood"]),
            Symptom(id="headache", name="Headache", body_system_name="Nervous",
                    causes=["Tension", "Migraine", "Dehydration", "Eye strain"])]


class TemplatesTest(unittest.TestCase):
    def setUp(self):
        self.builder = AutoCardBuilder(diseases(), symptoms(), medicines())
        self.result = self.builder.build()
        self.cards = {c.card_key: c for c in self.result.all_cards()}
        self.rf = self.result.by_entry[("disease", "rheumatic_fever")]

    def test_keys_are_stable_and_new_prefix(self):
        again = AutoCardBuilder(diseases(), symptoms(), medicines()).build()
        self.assertEqual({c.card_key: c.to_row() for c in again.all_cards()},
                         {k: c.to_row() for k, c in self.cards.items()})
        self.assertTrue(all(k.startswith("auto2:") for k in self.cards))
        self.assertTrue(all(c.content_hash for c in self.cards.values()))

    def test_rheumatic_fever_teaches_not_lists(self):
        families = {c.family for c in self.rf}
        self.assertTrue({"dz_picture", "dz_vs", "dz_mech", "dz_tx"} <= families, families)
        for card in self.rf:
            self.assertLessEqual(G.item_count(card.answer_short), 6)
            self.assertNotIn("Hallmark symptoms", card.front)

    def test_picture_card(self):
        card = self.cards["auto2:disease:rheumatic_fever:dz_picture"]
        self.assertIn("A patient has fever, joint pain (arthralgia) and joint swelling.", card.front)
        self.assertIn("2-4 weeks after the sore throat", card.front)
        self.assertNotIn("Rheumatic", card.front)
        right = [c.text for c in card.choices if c.correct]
        self.assertEqual(right, ["Rheumatic fever"])
        self.assertIn("Septic arthritis: Usually one hot joint", card.distinguish)
        self.assertIn("Shares", card.distinguish)
        self.assertEqual(card.hint, "Think: Cardiovascular")

    def test_whole_picture_rival_is_not_a_distractor(self):
        copycat = Disease(id="copycat", name="Copycat", body_system_name="Other",
                          symptoms=[sym("fever", "Fever"), sym("jp", "Joint pain (arthralgia)"),
                                    sym("js", "Joint swelling")])
        result = AutoCardBuilder(diseases() + [copycat], symptoms(), medicines()).build()
        card = next(c for c in result.all_cards() if c.card_key == "auto2:disease:rheumatic_fever:dz_picture")
        self.assertNotIn("Copycat", [c.text for c in card.choices])   # it has the whole picture

    def test_tell_apart_only_with_a_feature(self):
        keys = [k for k in self.cards if ":dz_vs:" in k]
        self.assertEqual(keys, ["auto2:disease:rheumatic_fever:dz_vs:septic-arthritis"])
        card = self.cards[keys[0]]
        self.assertIn("A bacterial joint infection.", card.explanation)        # the other disease's summary

    def test_mechanism_cloze(self):
        card = self.cards["auto2:disease:rheumatic_fever:dz_mech:1"]
        self.assertEqual(card.type, CardType.CLOZE)
        self.assertIn("{{c1::molecular mimicry}}", card.cloze_text)
        self.assertEqual(card.explanation, "This leads to valvulitis.")

    def test_red_flag_distractors_are_not_red_flags(self):
        card = self.cards["auto2:disease:rheumatic_fever:dz_redflag"]
        wrong = [c.text for c in card.choices if not c.correct]
        self.assertNotIn("Leg swelling (edema)", wrong)           # = "Swelling of the legs": a red flag
        self.assertTrue(all(not G.similar(w, r) for w in wrong
                            for r in ("Swelling of the legs or abdomen", "Chest pain or a racing heartbeat")))

    def test_treatment_cards(self):
        use = self.cards["auto2:disease:rheumatic_fever:dz_tx:use"]
        texts = [c.text for c in use.choices]
        self.assertNotIn("Co-trimoxazole", texts)
        self.assertTrue(any(c.correct and c.text in ("Amoxicillin", "Paracetamol") for c in use.choices))
        avoid = self.cards["auto2:disease:rheumatic_fever:dz_tx:avoid"]
        self.assertEqual([c.text for c in avoid.choices if c.correct], ["Co-trimoxazole"])
        self.assertEqual(avoid.explanation, "Not for strep throat.")

    def test_medicine_templates(self):
        calc = [c for k, c in self.cards.items() if ":amoxicillin:rx_calc:" in k]
        self.assertTrue(calc)
        for card in calc:
            weight = int(card.card_key.rsplit(":", 1)[1])
            self.assertEqual(card.answer_short, work_out("100 mg/kg/day ÷ 3", "Every 8 h", "", weight,
                                                         ["Powder for suspension 250 mg/5 mL"]).answer)
            self.assertIn("Practice calculation", card.explanation)
        self.assertNotIn("otitis", " ".join(k for k in self.cards if "rx_calc" in k))   # ambiguous row skipped
        dose = self.cards["auto2:medicine:amoxicillin:rx_dose:community-acquired-pneumonia"]
        self.assertEqual(dose.answer_short, "500 mg – 1 g every 8 h")
        self.assertIn("Max: 4 g/day", dose.explanation)
        self.assertEqual(dose.hint, "Route: PO")
        self.assertIn("auto2:medicine:amoxicillin:rx_renal:renal-gfr-10-30", self.cards)
        self.assertIn("auto2:medicine:amoxicillin:rx_ix:probenecid", self.cards)
        self.assertNotIn("auto2:medicine:bare:rx_class", self.cards)

    def test_symptom_cause_and_red_flag_skipped(self):
        card = self.cards["auto2:symptom:cough:sx_cause"]
        right = [c.text for c in card.choices if c.correct][0]
        self.assertIn(right, ["Viral infection", "Asthma", "Smoking"])
        self.assertFalse([k for k in self.cards if "sx_redflag" in k])

    def test_every_card_passes_the_gates(self):
        for card in self.cards.values():
            self.assertEqual(G.problems(card), [], card.card_key)
            if card.type == CardType.MCQ:
                self.assertEqual(sum(c.correct for c in card.choices), 1, card.card_key)

    def test_caps(self):
        per_entry = {}
        for card in self.cards.values():
            per_entry.setdefault(card.source_id, 0)
            per_entry[card.source_id] += 1
        self.assertTrue(all(n <= 8 for n in per_entry.values()))


class GatesTest(unittest.TestCase):
    def mcq(self, *texts, correct=0):
        return Card("x", "d", type=CardType.MCQ, front="Which one?",
                    choices=[Choice(t, i == correct, "r") for i, t in enumerate(texts)])

    def test_answer_in_question(self):
        card = Card("x", "d", front="Is the answer penicillin?", answer_short="Penicillin", back="Penicillin")
        self.assertIn("answer appears in the question", G.problems(card))

    def test_too_many_items_and_too_long(self):
        card = Card("x", "d", front="List them?", answer_short="a; b; c; d; e; f; g", back="x")
        self.assertIn("answer has more than 6 items", G.problems(card))
        card = Card("x", "d", front="Q" * 230, answer_short="a", back="a")
        self.assertIn("front too long", G.problems(card))

    def test_mcq_rules(self):
        self.assertIn("duplicate choices", G.problems(self.mcq("Joint pain (arthralgia)", "Arthralgia", "Fever")))
        self.assertIn("needs 2 to 4 distractors", G.problems(self.mcq("A", "B")))
        self.assertIn("a distractor is true for this entry",
                      G.problems(self.mcq("A", "Rash", "Fever"), forbidden=["Rash (maculopapular)"]))
        self.assertEqual(G.problems(self.mcq("Alpha", "Bravo", "Charlie")), [])

    def test_same_finding_in_other_words(self):
        self.assertTrue(G.similar("Palpitations", "Chest pain or a racing, irregular heartbeat"))
        self.assertTrue(G.similar("Leg swelling (edema)", "Swelling of the legs or abdomen"))
        self.assertFalse(G.similar("Sore throat", "Chest pain or a racing heartbeat"))

    def test_dedupe_and_cap(self):
        a = Card("1", "d", front="Q1?", answer_short="X", back="X", source_kind="disease", source_id="e", family="dz_vs")
        b = Card("2", "d", front="Q2?", answer_short="X", back="X", source_kind="disease", source_id="e", family="dz_vs")
        self.assertEqual(len(G.dedupe([a, b])), 1)
        cards = [Card(str(i), "d", family=f) for i, f in enumerate(["dz_mech", "dz_picture", "dz_vs"])]
        self.assertEqual([c.family for c in G.cap(cards, 2, ["dz_picture", "dz_vs", "dz_mech"])],
                         ["dz_picture", "dz_vs"])


if __name__ == "__main__":
    unittest.main()
