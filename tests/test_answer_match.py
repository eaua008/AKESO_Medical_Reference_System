import unittest

from app.services.study import answer_match as A


class AnswerMatchTest(unittest.TestCase):
    def test_score_ignores_case_filler_plurals_and_brackets(self):
        self.assertEqual(A.score("penicillin", "Penicillin (beta-lactam)"), 1.0)
        self.assertEqual(A.score("Infections of the joints", "joint infection"), 1.0)
        self.assertAlmostEqual(A.score("fever", "Fever and joint pain"), 1 / 3)
        self.assertEqual(A.score("", "anything"), 0.0)
        self.assertEqual(A.score("x", "(only brackets)"), 0.0)          # nothing outside the brackets

    def test_suggested_rating(self):
        self.assertEqual(A.suggested("667 mg every 8 h", "667 mg every 8 h (13 mL)"), 3)
        self.assertEqual(A.suggested("500 mg", "667 mg every 8 h"), 1)
        self.assertIsNone(A.suggested("   ", "Penicillin"))

    def test_marks_for_highlighting(self):
        self.assertEqual(A.marks("the penicillins", "Penicillin"), [("the", False), ("penicillins", True)])
        self.assertEqual(A.marks("Beta-lactam ring", "beta-lactam"), [("Beta-lactam", True), ("ring", False)])


if __name__ == "__main__":
    unittest.main()
