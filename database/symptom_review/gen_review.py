"""Symptom review migration: adds to symptoms, never removes.
python3 gen_review.py s01 021_symptoms_review_01.sql
"""
import csv, importlib, json, sys

KNOWN_DISEASES = set("""acute_coronary_syndrome acute_gastroenteritis ischemic_stroke asthma varicella chikungunya cholera copd
community_acquired_pneumonia covid19 dengue hypertension hfmd heart_failure hepatitis_a hepatitis_b hiv_infection influenza
leptospirosis malaria measles migraine peptic_ulcer_disease pertussis tuberculosis rabies schistosomiasis type2_diabetes
typhoid_fever urinary_tract_infection acute_appendicitis gerd iron_deficiency_anemia chronic_kidney_disease rheumatic_fever
post_strep_glomerulonephritis bacterial_meningitis graves_disease gout scabies""".split())

def q(v):
    if v is None: return "null"
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, (int, float)): return repr(v)
    return "'" + str(v).replace("'", "''") + "'"

def main(mod, out):
    data = importlib.import_module(mod).SYMPTOMS
    rows = {r["id"]: r for r in csv.DictReader(open("symptoms_export.csv"))}
    o = ["begin;\n\n"]
    w = o.append
    report = []
    for sid, d in data.items():
        r = rows[sid]
        old_causes = json.loads(r["causes"] or "[]")
        old_flags = json.loads(r["red_flags"] or "[]")
        old_refs = json.loads(r["refs"] or "[]")
        old_links = [x.strip() for x in (r["diseases"] or "").split(",") if x.strip()]
        w(f"-- ================================================ {sid}  ({r['name']})\n")
        new_desc = r["description"].rstrip() + " " + d["desc_add"]
        w(f"update public.symptoms set description = {q(new_desc)}, updated_at = now()\n"
          f"where id = {q(sid)} and description = {q(r['description'])};\n")
        tags = json.loads(r["tags"] or "[]")
        add_tags = [t for t in d.get("tags", []) if t not in tags]
        if add_tags:
            w(f"update public.symptoms set tags = tags || array[{', '.join(q(t) for t in add_tags)}]::text[]\n"
              f"where id = {q(sid)} and not (tags @> array[{', '.join(q(t) for t in add_tags)}]::text[]);\n")
        names = [ref[0] for ref in d["refs"] if ref[0] not in (r["source_attribution"] or "")]
        if names:
            w(f"update public.symptoms set source_attribution = source_attribution || {q('; ' + '; '.join(names))}\n"
              f"where id = {q(sid)} and position({q(names[0])} in source_attribution) = 0;\n")
        for table, items, old in (("symptom_causes", d["causes"], old_causes),
                                  ("symptom_red_flags", d["red_flags"], old_flags)):
            for item in items:
                assert item not in old, (sid, item)
                w(f"insert into public.{table} (symptom_id, content, position)\n"
                  f"select {q(sid)}, {q(item)}, coalesce((select max(position) + 1 from public.{table} where symptom_id = {q(sid)}), 0)\n"
                  f"where exists (select 1 from public.symptoms where id = {q(sid)})\n"
                  f"  and not exists (select 1 from public.{table} where symptom_id = {q(sid)} and content = {q(item)});\n")
        for name, cite, url in d["refs"]:
            assert url not in [x.get("url") for x in old_refs], (sid, url)
            w(f"insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)\n"
              f"select {q(sid)}, {q(name)}, {q(cite)}, {q(url)}, false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = {q(sid)}), 0)\n"
              f"where exists (select 1 from public.symptoms where id = {q(sid)})\n"
              f"  and not exists (select 1 from public.symptom_references where symptom_id = {q(sid)} and url = {q(url)});\n")
        for dis, inten, prim, wm in d["links"]:
            assert dis in KNOWN_DISEASES, dis
            assert dis not in old_links, (sid, dis)
            w(f"insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)\n"
              f"select {q(dis)}, {q(sid)}, {inten}::smallint, {q(prim)}, {wm}::numeric\n"
              f"where exists (select 1 from public.diseases where id = {q(dis)})\n"
              f"  and exists (select 1 from public.symptoms where id = {q(sid)})\n"
              f"  and not exists (select 1 from public.disease_symptoms where disease_id = {q(dis)} and symptom_id = {q(sid)});\n")
        w("\n")
        report.append((sid, r["name"], len(old_causes), len(d["causes"]), len(old_flags), len(d["red_flags"]),
                       len(old_refs), len(d["refs"]), len(old_links), len(d["links"])))
    w("update public.content_version set version = version + 1, updated_at = now() where id = 1;\n\ncommit;\n")
    head = (f"-- {out}  -  symptom review, session {mod[1:]}: {len(data)} symptoms\n"
            "-- Adds only: longer descriptions, extra causes, red flags, references and disease links.\n"
            "-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).\n"
            "-- A description is only extended if it is still the exported text (your own edits are kept).\n\n")
    open(out, "w").write(head + "".join(o))
    for x in report:
        print("%-24s causes %d+%d  red flags %d+%d  refs %d+%d  diseases %d+%d" % (x[0], *x[2:]))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
