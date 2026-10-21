"""Dose arithmetic with real dose strings from Akeso's medicine table."""

import unittest

from app.services.study.dose_calc import parse_dose, parse_max, times_per_day, work_out


class ParseTest(unittest.TestCase):
    def test_accepts_clear_strings(self):
        for text in ("15 mg/kg", "100 mg/kg/day ÷ 3", "10–20 mg/kg/day", "0.25 mg/kg",
                     "7.5 mg/kg", "20–60 mg/kg/day ÷ 3", "50–100 mg/kg"):
            self.assertIsNotNone(parse_dose(text), text)

    def test_skips_ambiguous_strings(self):
        for text in ("40–90 mg/kg/day, divided", "20 mg/kg (range 15–25)", "50,000 units/kg",
                     "200 micrograms/kg", "100/20 mg/kg/day ÷ 2 or more", "1–2 mg/kg elemental iron",
                     "10 mg/kg day 1, then 5 mg/kg", "1–2 mg/kg/day ÷ 1–2", "5 mL/kg/h",
                     ">22 kg: 1 tab; >44 kg: 1 tab 2×"):
            self.assertIsNone(parse_dose(text), text)

    def test_frequency_and_max(self):
        self.assertEqual(times_per_day("Every 8 h"), 3)
        self.assertEqual(times_per_day("2× a day"), 2)
        self.assertEqual(times_per_day("Once a day"), 1)
        self.assertIsNone(times_per_day("Every 4–6 h as needed"))
        self.assertIsNone(times_per_day("Divided doses; 2× a day only at the upper range"))
        self.assertEqual(parse_max("4 g/day").mg, 4000)
        self.assertEqual(parse_max("500 mg/dose").per, "dose")
        self.assertEqual(parse_max("1,500 mg/day").mg, 1500)
        self.assertEqual(parse_max("60 mg/kg/day").per_kg, 60)
        self.assertIsNone(parse_max("1 g/dose · 60 mg/kg/day, not over 4 g").mg if parse_max(
            "1 g/dose · 60 mg/kg/day, not over 4 g") else None)
        self.assertIsNone(parse_max("500 mg day 1; 250 mg/day"))
        self.assertIsNone(parse_max("Adult dose"))
        self.assertEqual(parse_max("—").mg, None)


class WorkTest(unittest.TestCase):
    def test_amoxicillin_typhoid_per_day_divided(self):
        w = work_out("100 mg/kg/day ÷ 3", "Every 8 h", "", 15,
                     ["Powder for suspension 250 mg/5 mL, 60 mL bottle (add 41 mL water)"])
        self.assertEqual(w.answer, "500 mg every 8 h (10 mL)")
        self.assertIn("100 mg/kg/day × 15 kg = 1,500 mg a day", w.steps[0])
        self.assertIn("No maximum", " ".join(w.steps))
        self.assertTrue(w.steps[-1].startswith("Practice calculation"))

    def test_ciprofloxacin_cap_per_dose(self):
        w = work_out("20 mg/kg", "2× a day", "750 mg/dose", 30)          # 600 mg: fine
        self.assertFalse(w.capped)
        self.assertEqual(w.per_intake_high, 600)
        w = work_out("20 mg/kg", "2× a day", "750 mg/dose", 40)          # 800 -> 750
        self.assertTrue(w.capped)
        self.assertEqual(w.per_intake_high, 750)

    def test_daily_cap(self):
        w = work_out("10 mg/kg", "Every 8 h", "1,500 mg/day", 60)              # 600 x3 = 1800 > 1500
        self.assertTrue(w.capped)
        self.assertEqual(w.per_intake_high, 500)

    def test_range_and_weight_based_max(self):
        w = work_out("20–60 mg/kg/day ÷ 3", "Every 8 h", "", 15)
        self.assertEqual(w.answer, "100–300 mg every 8 h")
        w = work_out("45–70 mg/kg/day ÷ 2", "2× a day", "70 mg/kg/day", 20)
        self.assertFalse(w.capped)
        self.assertEqual((w.per_intake_low, w.per_intake_high), (450, 700))

    def test_ambiguous_rows_are_skipped(self):
        self.assertIsNone(work_out("40–90 mg/kg/day, divided", "Divided doses", "", 15))
        self.assertIsNone(work_out("15 mg/kg/day ÷ 2", "Every 12 h", "Adult dose", 15))
        self.assertIsNone(work_out("10–20 mg/kg/day", "Every 8 h", "", 15))         # /day, no divisor
        self.assertIsNone(work_out("20 mg/kg/day ÷ 3–4", "Every 6–8 h", "", 15))

    def test_frequency_mismatch_is_skipped(self):
        self.assertIsNone(work_out("100 mg/kg/day ÷ 3", "Every 6 h", "", 15))


if __name__ == "__main__":
    unittest.main()
