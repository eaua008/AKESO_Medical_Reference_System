"""Medicine review migration: adds to medicines, never removes or rewords.

    python database/medicine_review/gen_med_review.py b01 033_medicines_review_01.sql

Reads database/medicine_review/<batch>/out_<medicine_id>.py (one MED dict each)
and the export CSV, and writes:
    database/migrations/<out>.sql        (run in Supabase)
    database/migrations/<out>.md         (review sheet: old vs new, every source)

What one medicine gets (each step guarded, so running twice changes nothing):
  * description: new sentences appended, only if it is still the exported text
  * source_attribution: new source names appended
  * medicine_facts: new indications / side effects / precautions / interactions / brands
  * medicine_references: new references (skipped if the URL is already there)
  * disease_medicines: new disease links with safety + note (skipped if linked)
  * dosage table rows, panels and sources (only if the medicine has no rows yet)
"""

import csv
import json
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_doses import ROOT, block, q  # noqa: E402

sys.path.insert(0, ROOT)
from app.models.medicine import DoseNote, DoseRow, DoseSource  # noqa: E402

EXPORT = os.path.join(HERE, "medicines_export_2026-10-13.csv")
KNOWN_DISEASES = set("""acute_coronary_syndrome acute_gastroenteritis ischemic_stroke asthma varicella chikungunya cholera copd
community_acquired_pneumonia covid19 dengue hypertension hfmd heart_failure hepatitis_a hepatitis_b hiv_infection influenza
leptospirosis malaria measles migraine peptic_ulcer_disease pertussis tuberculosis rabies schistosomiasis type2_diabetes
typhoid_fever urinary_tract_infection acute_appendicitis gerd iron_deficiency_anemia chronic_kidney_disease rheumatic_fever
post_strep_glomerulonephritis bacterial_meningitis graves_disease gout scabies""".split())
FACT_KINDS = ("indication", "adverse", "contraindication", "interaction", "brand_ph", "brand_intl")
FACT_TITLES = {"indication": "Uses", "adverse": "Side effects", "contraindication": "Precautions",
               "interaction": "Interactions", "brand_ph": "Brands (PH)", "brand_intl": "Brands (intl)"}
NOTE_KINDS = ("renal", "hepatic", "elderly", "pregnancy", "administration", "forms_ph", "monitor")
POPS = ("adult", "child", "neonate")


def check(med: dict, row: dict) -> None:
    mid = med["id"]
    old_facts = {(f["kind"], f["content"].strip().lower()) for f in json.loads(row["facts"] or "[]")}
    old_urls = {r.get("url") for r in json.loads(row["refs"] or "[]")}
    old_links = {d.split(":")[0].strip() for d in row["diseases"].split(",") if d.strip()}
    for kind, items in med["facts"].items():
        assert kind in FACT_KINDS, (mid, kind)
        for item in items:
            assert (kind, item.strip().lower()) not in old_facts, (mid, "fact exists", item)
    for _name, _cite, url in med["refs"]:
        assert url.startswith("https://") and url not in old_urls, (mid, url)
    for dis, safety, _note in med["links"]:
        assert dis in KNOWN_DISEASES and dis not in old_links, (mid, dis)
        assert safety in ("safe", "caution", "avoid"), (mid, safety)
    tags = {s[0] for s in med.get("sources", [])}
    for d in med.get("doses", []):
        assert len(d) == 9 and d[0] in POPS and d[7] in tags, (mid, d)
    for n in med.get("notes", []):
        assert len(n) == 4 and n[0] in NOTE_KINDS and (not n[3] or n[3] in tags), (mid, n)


def sql_for(med: dict, row: dict) -> str:
    mid = med["id"]
    out = [f"-- ================================================ {mid}  ({row['name']})"]
    if med.get("desc_add"):
        new_desc = row["description"].rstrip() + " " + med["desc_add"].strip()
        out.append(f"update public.medicines set description = {q(new_desc)}, updated_at = now()\n"
                   f"where id = {q(mid)} and description = {q(row['description'])};")
    names = []
    for name, *_rest in list(med["refs"]) + [(s[1],) for s in med.get("sources", [])]:
        if name not in names and name not in (row["source_attribution"] or ""):
            names.append(name)
    if names:
        out.append(f"update public.medicines set source_attribution = "
                   f"case when coalesce(source_attribution, '') = '' then {q('; '.join(names))} "
                   f"else source_attribution || {q('; ' + '; '.join(names))} end\n"
                   f"where id = {q(mid)} and position({q(names[0])} in coalesce(source_attribution, '')) = 0;")
    for kind in FACT_KINDS:
        for item in med["facts"].get(kind, []):
            out.append(
                f"insert into public.medicine_facts (medicine_id, kind, content, position)\n"
                f"select {q(mid)}, {q(kind)}, {q(item)}, coalesce((select max(position) + 1 from public.medicine_facts "
                f"where medicine_id = {q(mid)} and kind = {q(kind)}), 0)\n"
                f"where exists (select 1 from public.medicines where id = {q(mid)})\n"
                f"  and not exists (select 1 from public.medicine_facts where medicine_id = {q(mid)} "
                f"and kind = {q(kind)} and content = {q(item)});")
    for name, cite, url in med["refs"]:
        out.append(
            f"insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)\n"
            f"select {q(mid)}, {q(name)}, {q(cite)}, {q(url)}, false, coalesce((select max(position) + 1 from "
            f"public.medicine_references where medicine_id = {q(mid)}), 0)\n"
            f"where exists (select 1 from public.medicines where id = {q(mid)})\n"
            f"  and not exists (select 1 from public.medicine_references where medicine_id = {q(mid)} and url = {q(url)});")
    for dis, safety, note in med["links"]:
        out.append(
            f"insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)\n"
            f"select {q(dis)}, {q(mid)}, coalesce((select max(position) + 1 from public.disease_medicines "
            f"where disease_id = {q(dis)}), 0), {q(safety)}::condition_safety, {q(note)}\n"
            f"where exists (select 1 from public.diseases where id = {q(dis)})\n"
            f"  and exists (select 1 from public.medicines where id = {q(mid)})\n"
            f"  and not exists (select 1 from public.disease_medicines where disease_id = {q(dis)} and medicine_id = {q(mid)});")
    text = "\n".join(out) + "\n"
    if med.get("doses"):
        doses = [DoseRow(*d) for d in med["doses"]]
        notes = [DoseNote(kind=n[0], content=n[1], label=n[2], source=n[3]) for n in med.get("notes", [])]
        sources = [DoseSource(*s) for s in med.get("sources", [])]
        text += block(mid, doses, notes, sources)
    return text + "\n"


def md_for(med: dict, row: dict) -> str:
    old_facts = json.loads(row["facts"] or "[]")
    lines = [f"## {row['name']}  (`{med['id']}`)", ""]
    lines += ["**Description (kept)**", "", row["description"], ""]
    if med.get("desc_add"):
        lines += ["**Description (added)**", "", med["desc_add"], ""]
    for kind in FACT_KINDS:
        old = [f["content"] for f in old_facts if f["kind"] == kind]
        new = med["facts"].get(kind, [])
        if new:
            lines += [f"**{FACT_TITLES[kind]}**: {len(old)} kept, {len(new)} added", ""]
            lines += [f"- NEW: {x}" for x in new] + [""]
    if med["links"]:
        lines += ["**Disease links added**", ""]
        lines += [f"- `{d}`: **{s}**: {n}" for d, s, n in med["links"]] + [""]
    if med.get("doses"):
        lines += ["**Dosage table**", "", "| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |",
                  "|---|---|---|---|---|---|---|---|"]
        for d in med["doses"]:
            cells = [c.replace("|", "/").replace("\n", " ") for c in (d[0], d[1] + (f" ({d[8]})" if d[8] else ""),
                                                                    d[2], d[3], d[4], d[5], d[6], d[7])]
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
        for n in med.get("notes", []):
            lines.append(f"- *{n[0]}*{(' ' + n[2]) if n[2] else ''}: {n[1]}{(' [' + n[3] + ']') if n[3] else ''}")
        lines.append("")
    lines += ["**References added**", ""]
    lines += [f"- [{n}]({u}): {c}" for n, c, u in med["refs"]]
    for tag, name, cite, url in med.get("sources", []):
        lines.append(f"- Dosing source `{tag}`: [{name}]({url}): {cite}")
    lines += ["", "**What was checked on each page**", ""]
    lines += [f"- {u}: {w}" for u, w in med.get("checked", [])]
    return "\n".join(lines) + "\n\n---\n\n"


def main(batch: str, out_name: str) -> None:
    rows = {r["id"]: r for r in csv.DictReader(open(EXPORT, encoding="utf-8"))}
    folder = os.path.join(HERE, batch)
    meds = [runpy.run_path(os.path.join(folder, f))["MED"]
            for f in sorted(os.listdir(folder)) if f.startswith("out_") and f.endswith(".py")]
    for med in meds:
        check(med, rows[med["id"]])
    sql = (f"-- {out_name}  -  medicine review {batch}: {', '.join(m['id'] for m in meds)}\n"
           "-- Adds only: longer descriptions, new facts, references, disease links, and dosage\n"
           "-- tables (for medicines that have none yet). Nothing is deleted or reworded.\n"
           "-- Needs 030_medicine_doses.sql first. Safe to run twice (every insert is guarded).\n\nbegin;\n\n")
    sql += "".join(sql_for(m, rows[m["id"]]) for m in meds)
    sql += "update public.content_version set version = version + 1, updated_at = now() where id = 1;\n\ncommit;\n"
    md = (f"# Medicine review {batch}: review sheet\n\nRun `{out_name}` in Supabase after you have checked this. "
          "Everything below is ADDED; the existing text stays as it is.\n\n"
          "Every link was opened twice: by the research step (to read the fact), and again in "
          "Akeso's own browser pane on your computer in the Philippines (to make sure it opens "
          "for you, not just from the cloud). See NOTES.md in the batch folder for any link "
          "that needs attention.\n\n"
          "UK SmPC links open the official MHRA Products search (free) for that medicine: the "
          "emc site (medicines.org.uk) now limits free page views for users outside the UK. "
          "The citation still names the exact product and PL number to pick.\n\n")
    notes = os.path.join(folder, "NOTES.md")
    if os.path.exists(notes):
        md += open(notes, encoding="utf-8").read() + "\n\n---\n\n"
    md += "".join(md_for(m, rows[m["id"]]) for m in meds)
    base = os.path.join(ROOT, "database", "migrations", out_name)
    open(base, "w", encoding="utf-8").write(sql)
    open(base[:-4] + ".md", "w", encoding="utf-8").write(md)
    for m in meds:
        print("%-36s facts +%-3d refs +%d links +%d doses %d notes %d" % (
            m["id"], sum(len(v) for v in m["facts"].values()), len(m["refs"]), len(m["links"]),
            len(m.get("doses", [])), len(m.get("notes", []))))
    print("wrote", base)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
