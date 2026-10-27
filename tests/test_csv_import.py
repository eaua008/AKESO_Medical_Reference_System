import unittest

from app.models.study import CardType
from app.services.study.csv_import import parse_csv


class CsvImportTest(unittest.TestCase):
    def test_good_and_bad_rows(self):
        text = (
            "type,front,back,choices_json,cloze_text,tags\n"
            "basic,Class of amoxicillin?,Penicillin,,,pharm;finals\n"
            'mcq,Which is a macrolide?,,"[{""text"": ""Azithromycin"", ""correct"": true}, '
            '{""text"": ""Amoxicillin""}]",,\n'
            "cloze,,,,Amoxicillin is a {{c1::penicillin}}.,\n"
            "basic,No back,,,,\n"
            "mcq,Broken,,not json,,\n"
            "essay,What?,,,,\n"
            ",,,,,\n")
        result = parse_csv(text, "d1")
        self.assertEqual([c.type for c in result.cards], [CardType.BASIC, CardType.MCQ, CardType.CLOZE])
        self.assertEqual(result.cards[0].tags, ["pharm", "finals"])
        self.assertEqual(len(result.errors), 3)
        self.assertTrue(result.errors[0].startswith("Line 5:"))
        self.assertIn("3 cards ready, 3 rows with problems", result.summary)

    def test_needs_header(self):
        self.assertTrue(parse_csv("basic,a,b\n").errors)
        self.assertTrue(parse_csv("").errors)


if __name__ == "__main__":
    unittest.main()
