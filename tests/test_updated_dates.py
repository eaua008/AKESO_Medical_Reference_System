import unittest

from app.models.disease import Disease
from app.models.medicine import MedicineMonograph, medicine_from_json, medicine_to_json
from app.models.symptom import Symptom, symptom_from_json, symptom_to_json
from app.repositories.local_disease_cache import disease_from_json, disease_to_json


class UpdatedDateTest(unittest.TestCase):
    def test_disease_reads_updated_at_and_survives_the_cache(self):
        d = Disease.from_dict({"id": "dengue", "name": "Dengue",
                               "updated_at": "2026-10-19T03:15:00+00:00"})
        self.assertEqual(d.updated_label, "Oct 19, 2026")
        self.assertEqual(disease_from_json(disease_to_json(d)).updated_at, d.updated_at)

    def test_blank_or_bad_dates_show_nothing(self):
        self.assertEqual(Disease(id="x", name="X").updated_label, "")
        self.assertEqual(Symptom(id="s", name="S", updated_at="not a date").updated_label, "")

    def test_symptom_and_medicine_round_trip(self):
        s = Symptom(id="s", name="S", updated_at="2026-01-05T00:00:00Z")
        self.assertEqual(symptom_from_json(symptom_to_json(s)).updated_label, s.updated_label)
        m = MedicineMonograph(id="m", name="M", updated_at="2026-01-05T12:00:00+00:00")
        self.assertTrue(medicine_from_json(medicine_to_json(m)).updated_label.startswith("Jan 5"))

    def test_old_cache_rows_without_the_field_still_load(self):
        self.assertEqual(symptom_from_json('{"id": "s", "name": "S"}').updated_at, "")


if __name__ == "__main__":
    unittest.main()
