"""Write a migration that fills the dosage table for some medicines.

    python database/medicine_review/gen_doses.py samples 031_medicine_doses_first3.sql

Reads the rows from a Python module (DoseRow / DoseNote / DoseSource lists per
medicine id). Each medicine is filled only if it has no rows yet, so running
the SQL twice, or after an admin edited a table, changes nothing.
"""

import importlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)


def q(v) -> str:
    return "'" + str(v).replace("'", "''") + "'"


def block(mid: str, doses, notes, sources) -> str:
    out = [f"-- {mid}"]
    guard = lambda table: (f"where exists (select 1 from public.medicines where id = {q(mid)})\n"  # noqa: E731
                           f"  and not exists (select 1 from public.{table} where medicine_id = {q(mid)})")
    if doses:
        vals = ",\n    ".join(
            f"({q(mid)}, {q(d.population)}, {i}, {q(d.indication)}, {q(d.route)}, {q(d.dose)}, "
            f"{q(d.frequency)}, {q(d.duration)}, {q(d.max_dose)}, {q(d.source)}, {q(d.note)})"
            for i, d in enumerate(doses))
        out.append("insert into public.medicine_doses (medicine_id, population, position, indication, "
                   "route, dose, frequency, duration, max_dose, source, note)\n"
                   f"select * from (values\n    {vals}\n) v(medicine_id, population, position, indication, "
                   "route, dose, frequency, duration, max_dose, source, note)\n" + guard("medicine_doses") + ";")
    if notes:
        vals = ",\n    ".join(f"({q(mid)}, {q(n.kind)}, {i}, {q(n.label)}, {q(n.content)}, {q(n.source)})"
                               for i, n in enumerate(notes))
        out.append("insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)\n"
                   f"select * from (values\n    {vals}\n) v(medicine_id, kind, position, label, content, source)\n"
                   + guard("medicine_dose_notes") + ";")
    if sources:
        vals = ",\n    ".join(f"({q(mid)}, {q(s.tag)}, {q(s.source_name)}, {q(s.citation_text)}, {q(s.url)}, {i})"
                               for i, s in enumerate(sources))
        out.append("insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)\n"
                   f"select * from (values\n    {vals}\n) v(medicine_id, tag, source_name, citation_text, url, position)\n"
                   + guard("medicine_dose_sources") + ";")
    return "\n".join(out) + "\n\n"


def main(module: str, out_name: str) -> None:
    if module == "samples":
        mod = importlib.import_module("app.services.dose_samples")
        data = {mid: (rows, notes, mod.SOURCES.get(mid, [])) for mid, (rows, notes) in mod.SAMPLES.items()}
    else:
        data = importlib.import_module(module).DATA      # {mid: (doses, notes, sources)}
    text = (f"-- {out_name}  -  dosage table rows for: {', '.join(data)}\n"
            "-- Needs 030_medicine_doses.sql first. Fills a medicine only if it has no rows yet;\n"
            "-- medicines.dosage_text is not touched. Safe to run twice.\n\nbegin;\n\n")
    text += "".join(block(mid, *rows) for mid, rows in data.items())
    text += "update public.content_version set version = version + 1, updated_at = now() where id = 1;\n\ncommit;\n"
    path = os.path.join(ROOT, "database", "migrations", out_name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    print(f"wrote {path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
