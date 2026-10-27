import unittest

from app.models.study import Card, CardType, Choice
from app.services.study import cloze


class ClozeTest(unittest.TestCase):
    def test_parse_numbered_unnumbered_and_hints(self):
        text = "{{c1::Dengue::a virus}} spreads by {{c2::mosquito}} bites; give {{fluids}}."
        found = cloze.blanks(text)
        self.assertEqual([(b.number, b.answer, b.hint) for b in found],
                         [(1, "Dengue", "a virus"), (2, "mosquito", ""), (0, "fluids", "")])
        self.assertEqual(cloze.question(text), "[ a virus ] spreads by [ … ] bites; give [ … ].")
        self.assertEqual(cloze.answer(text), "Dengue spreads by mosquito bites; give fluids.")

    def test_html_is_escaped(self):
        self.assertEqual(cloze.answer_html("<i>x</i> {{c1::a<b}}"), "&lt;i&gt;x&lt;/i&gt; <b>a&lt;b</b>")

    def test_make_blank_numbers_and_trims(self):
        text = "Amoxicillin is a penicillin."
        start = text.index("penicillin") - 1                # includes the space before
        one = cloze.make_blank(text, start, start + len(" penicillin"))
        self.assertEqual(one, "Amoxicillin is a {{c1::penicillin}}.")
        two = cloze.make_blank(one, 0, len("Amoxicillin"))
        self.assertEqual(two, "{{c2::Amoxicillin}} is a {{c1::penicillin}}.")
        self.assertEqual(cloze.make_blank(text, 3, 3), text)

    def test_no_blank_is_a_problem(self):
        card = Card("1", "d", type=CardType.CLOZE, cloze_text="no blanks here")
        self.assertTrue(card.problems())
        card.cloze_text = "a {{c1::blank}}"
        self.assertEqual(card.problems(), [])


class CardProblemsTest(unittest.TestCase):
    def test_mcq_rules(self):
        card = Card("1", "d", type=CardType.MCQ, front="Q?",
                    choices=[Choice("A"), Choice("B")])
        self.assertIn("Mark at least one choice as correct.", card.problems())
        card.choices[0].correct = True
        self.assertEqual(card.problems(), [])
        card.choices.append(Choice("a"))
        self.assertIn("Two choices say the same thing.", card.problems())

    def test_basic_needs_both_sides(self):
        self.assertEqual(len(Card("1", "d", front="", back="").problems()), 2)


if __name__ == "__main__":
    unittest.main()
