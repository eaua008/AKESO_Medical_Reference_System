"""Preview the new dosage table on the medicine page, before the database
has the rows.

    .venv\Scripts\python scripts\preview_dosage.py                 (paracetamol)
    .venv\Scripts\python scripts\preview_dosage.py med_amoxicillin
    .venv\Scripts\python scripts\preview_dosage.py med_aciclovir dark
    .venv\Scripts\python scripts\preview_dosage.py med_amoxicillin 80    (at 80%)

Uses the sample rows in app/services/dose_samples.py and the medicine's own
text from database/medicine_review/medicines_export_2026-10-13.csv.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication  # noqa: E402


EXPORT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "database", "medicine_review", "medicines_export_2026-10-13.csv")


def from_export(medicine_id: str):
    """The medicine's real text from the export, so the page looks real."""
    import csv
    import json
    from app.models.medicine import MedicineMonograph, MedicineReference
    if not os.path.exists(EXPORT):
        return None
    with open(EXPORT, encoding="utf-8") as handle:
        row = next((r for r in csv.DictReader(handle) if r["id"] == medicine_id), None)
    if row is None:
        return None
    facts = json.loads(row["facts"] or "[]")
    kind = lambda k: [f["content"] for f in facts if f["kind"] == k]  # noqa: E731
    refs = [MedicineReference(r["source"], r.get("citation", ""), r.get("url", ""),
                              bool(r.get("mother"))) for r in json.loads(row["refs"] or "[]")]
    return MedicineMonograph(
        id=row["id"], name=row["name"], generic_name=row["generic_name"],
        drug_class=row["drug_class"], category=row["category"],
        dosage_text=row["dosage_text"], storage=row["storage"],
        black_box_warning=row["black_box_warning"],
        ph_brands=kind("brand_ph"), intl_brands=kind("brand_intl"),
        indications=kind("indication"), adverse_reactions=kind("adverse"),
        contraindications=kind("contraindication"), interactions=kind("interaction"),
        references=refs)


def main() -> int:
    medicine_id = next((a for a in sys.argv[1:] if a.startswith("med_")), "med_paracetamol")
    mode = "dark" if "dark" in sys.argv[1:] else "light"
    app = QApplication(sys.argv)
    scale = next((int(a) for a in sys.argv[1:] if a in ("80", "90")), 100)
    if scale < 100:
        from app.core import soft_scale
        soft_scale.install(scale / 100, app)
    from app.core.theme import Theme
    try:
        Theme.set_mode(mode)
    except Exception:  # noqa: BLE001 - older theme API
        pass
    app.setStyleSheet(Theme.stylesheet())

    from app.models.medicine import MedicineMonograph
    from app.services.dose_samples import SAMPLES, apply_samples
    from app.ui.views.medicine_monograph_view import MedicineMonographView

    medicine = from_export(medicine_id)
    if medicine is None:
        name = medicine_id.removeprefix("med_").replace("_", " ").title()
        medicine = MedicineMonograph(
            id=medicine_id, name=name, generic_name=name.lower(),
            dosage_text="(The current dosing paragraph shows here, folded under the table.)")
    if not apply_samples(medicine):
        print(f"No sample rows for {medicine_id}. Try: {', '.join(SAMPLES)}")
        return 1

    view = MedicineMonographView()
    view.resize(1280, 900)
    view.show_medicine(medicine)
    view.show()
    view._scroll_to("dosage")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
