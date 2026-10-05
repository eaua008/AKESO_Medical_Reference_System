"""Builds the Akeso reference seed SQL from the researched JSON files.

Output: seed_reference_data.sql (idempotent: safe to run more than once)
        reset_reference_data.sql (optional, destructive: clears old data)
"""

import glob
import json
from pathlib import Path

R = Path(__file__).resolve().parent
D = [d for f in sorted(glob.glob(str(R / "diseases_*.json"))) for d in json.load(open(f))["diseases"]]
M = [m for f in sorted(glob.glob(str(R / "medicines_*.json"))) for m in json.load(open(f))["medicines"]]
# symptoms.json + symptoms_B.json ..., interactions.json + interactions_B.json ...
S = [s for f in sorted(glob.glob(str(R / "symptoms*.json"))) for s in json.load(open(f))["symptoms"]]
IX = {"pairs": [], "rules": []}
for f in sorted(glob.glob(str(R / "interactions*.json"))):
    part = json.load(open(f))
    IX["pairs"] += part.get("pairs", [])
    IX["rules"] += part.get("rules", [])

BODY_SYSTEMS = [
    ("bs_cardiovascular", "Cardiovascular System", "Heart and blood vessels."),
    ("bs_respiratory", "Respiratory System", "Airways and lungs."),
    ("bs_digestive", "Digestive System", "Gastrointestinal tract, liver and pancreas."),
    ("bs_urinary", "Urinary System", "Kidneys, ureters, bladder and urethra."),
    ("bs_endocrine", "Endocrine System", "Hormone-producing glands and metabolism."),
    ("bs_nervous", "Nervous System", "Brain, spinal cord and nerves."),
    ("bs_immune", "Immune & Lymphatic System", "Immune defences and lymphatic tissue."),
    ("bs_musculoskeletal", "Musculoskeletal System", "Bones, joints and muscles."),
    ("bs_integumentary", "Integumentary System", "Skin, hair and nails."),
    ("bs_hematologic", "Hematologic System", "Blood and blood-forming tissues."),
    ("bs_multisystem", "Multisystem (Systemic Infection)",
     "Infections that involve several organ systems at once."),
]
NO_SYSTEM = "Systemic / General"
CONDITIONS = [
    ("hypertension", "Hypertension", "High blood pressure", '{hypertension,"blood pressure"}', 1),
    ("diabetes", "Diabetes Mellitus", "Type 1 or Type 2", "{diabetes,glycemic,glucose}", 2),
    ("pregnant", "Pregnancy", "Gestational / 1st-3rd trimester", "{pregnan}", 3),
    ("asthma", "Asthma / Reactive Airway", "Bronchial hyperreactivity", "{asthma,copd,bronch}", 4),
    ("peptic_ulcer", "Peptic Ulcer / GI Bleed", "Gastric erosion or ulcer history",
     '{peptic,ulcer,"gi bleed","gastrointestinal bleed"}', 5),
    ("renal_impairment", "Chronic Kidney Disease", "Impaired renal filtration", "{kidney,renal,nephro}", 6),
    ("liver_disease", "Liver Disease", "Hepatic impairment or cirrhosis", "{liver,hepat,cirrhosis}", 7),
    ("autoimmune", "Autoimmune Condition", "Systemic lupus, RA, or biologics",
     "{autoimmune,lupus,rheumatoid}", 8),
]


def q(value) -> str:
    """SQL literal."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    return "'" + str(value).replace("'", "''") + "'"


def arr(values: list) -> str:
    if not values:
        return "'{}'::text[]"
    return "ARRAY[" + ", ".join(q(v) for v in values) + "]::text[]"


def ids(values) -> str:
    return "(" + ", ".join(q(v) for v in values) + ")"


def system(name: str) -> str:
    if not name or name == NO_SYSTEM:
        return "NULL"
    return f"(SELECT id FROM public.body_systems WHERE name = {q(name)} ORDER BY id LIMIT 1)"


def rows(values: list[list]) -> str:
    return ",\n".join("    (" + ", ".join(v) + ")" for v in values)


def upsert(table: str, key: str, cols: list[str], data: list[list]) -> str:
    """Update-then-insert through a temp table, so it works whether or not
    the table has a primary key on `key`."""
    tmp = f"_seed_{table}"
    set_cols = ", ".join(f"{c} = t.{c}" for c in cols if c != key)
    col_list = ", ".join(cols)
    return f"""
CREATE TEMP TABLE {tmp} ON COMMIT DROP AS SELECT {col_list} FROM public.{table} WITH NO DATA;
INSERT INTO {tmp} ({col_list}) VALUES
{rows(data)};
UPDATE public.{table} AS x SET {set_cols}, updated_at = now()
  FROM {tmp} AS t WHERE x.{key} = t.{key};
INSERT INTO public.{table} ({col_list})
  SELECT {col_list} FROM {tmp} AS t
  WHERE NOT EXISTS (SELECT 1 FROM public.{table} AS x WHERE x.{key} = t.{key});
"""


def insert(table: str, cols: list[str], data: list[list]) -> str:
    if not data:
        return ""
    return f"INSERT INTO public.{table} ({', '.join(cols)}) VALUES\n{rows(data)};\n"


def refs_attribution(refs: list[dict]) -> str:
    return "; ".join(dict.fromkeys(r["source_name"] for r in refs if r.get("source_name")))


# ------------------------------------------------------------ checks
# Rules the data must follow; the build stops rather than write bad SQL.
#  1. Drug labels (DailyMed / FDA prescribing information) belong to the
#     medicine they describe, never to a disease or a symptom.
#  2. Textbook ("mother book") references carry no URL: there is no page
#     for the book itself, and a publisher press release is not the book.
LABEL_WORDS = ("dailymed", "prescribing information", "fda label")
problems = []
for kind, items in (("disease", D), ("symptom", S)):
    for item in items:
        for r in item.get("references", []):
            text = f"{r.get('source_name', '')} {r.get('citation_text', '')}".lower()
            if any(word in text for word in LABEL_WORDS):
                problems.append(f"{kind} {item['id']}: drug label cited ({r['source_name']})")
for kind, items in (("disease", D), ("symptom", S), ("medicine", M)):
    for item in items:
        for r in item.get("references", []):
            if r.get("is_mother_book") and r.get("url"):
                problems.append(f"{kind} {item['id']}: mother book has a URL ({r['url']})")
if problems:
    raise SystemExit("Fix the research JSON first:\n  " + "\n  ".join(problems))


# ------------------------------------------------------------------ build

dids = [d["id"] for d in D]
sids = [s["id"] for s in S]
mids = [m["id"] for m in M]
rids = [r["id"] for r in IX["rules"]]
out: list[str] = []
w = out.append

w(f"""-- =====================================================================
-- Akeso reference data seed
-- {len(D)} diseases, {len(S)} symptoms, {len(M)} medicines,
-- {len(IX['pairs'])} drug-drug interaction pairs, {len(IX['rules'])} multi-drug rules.
--
-- Researched from StatPearls (NCBI Bookshelf), WHO, CDC, DOH Philippines,
-- PSMID/PCP, GINA, GOLD, ADA, AHA/ESC, NICE and FDA labels on DailyMed.
-- Every clinical reference URL was opened and checked when this file was
-- made. Textbook ("mother book") references carry no URL on purpose.
--
-- Educational reference content for a student platform, not a substitute
-- for current product labeling or clinical judgment.
--
-- Safe to run more than once: rows with these ids are updated, and their
-- child rows (lists, links, references) are replaced.
-- Requires database/migrations/001_medication_safety_reference.sql.
-- =====================================================================

BEGIN;
""")

# ---------------------------------------------------------- body systems
w("\n-- ---------------------------------------------------------------- body systems")
w("-- Added only when no body system with the same name exists yet.")
for i, (bid, name, desc) in enumerate(BODY_SYSTEMS, start=1):
    w(f"INSERT INTO public.body_systems (id, name, description, sort_order)\n"
      f"  SELECT {q(bid)}, {q(name)}, {q(desc)}, {i}\n"
      f"  WHERE NOT EXISTS (SELECT 1 FROM public.body_systems WHERE name = {q(name)});")

w("\n-- ---------------------------------------------------------- patient conditions")
for cid, label, desc, kw, order in CONDITIONS:
    w(f"INSERT INTO public.patient_conditions (id, label, description, match_keywords, sort_order)\n"
      f"  SELECT {q(cid)}, {q(label)}, {q(desc)}, {q(kw)}::text[], {order}\n"
      f"  WHERE NOT EXISTS (SELECT 1 FROM public.patient_conditions WHERE id = {q(cid)});")

# ------------------------------------------------ clear child rows first
w("--SPLIT:clear")
w("\n-- ------------------------------------------------ replace child rows of these ids")
for table in ("disease_symptoms",):
    w(f"DELETE FROM public.{table} WHERE disease_id IN {ids(dids)} OR symptom_id IN {ids(sids)};")
w(f"DELETE FROM public.disease_medicines WHERE disease_id IN {ids(dids)} OR medicine_id IN {ids(mids)};")
w(f"DELETE FROM public.disease_related WHERE disease_id IN {ids(dids)} OR related_disease_id IN {ids(dids)};")
for table in ("disease_tags", "disease_causes", "disease_emergency_signs", "disease_home_care",
              "disease_recommended_tests", "disease_risk_factors", "disease_treatments",
              "disease_prevention", "disease_differentials", "clinical_references"):
    w(f"DELETE FROM public.{table} WHERE disease_id IN {ids(dids)};")
for table in ("symptom_causes", "symptom_red_flags", "symptom_references"):
    w(f"DELETE FROM public.{table} WHERE symptom_id IN {ids(sids)};")
for table in ("medicine_facts", "medicine_references", "medicine_brands", "medicine_uses",
              "medicine_side_effects", "medicine_warnings", "medicine_contraindications",
              "medicine_interactions", "medicine_condition_safety"):
    w(f"DELETE FROM public.{table} WHERE medicine_id IN {ids(mids)};")
w(f"DELETE FROM public.drug_interactions WHERE medicine_a_id IN {ids(mids)} AND medicine_b_id IN {ids(mids)};")
w(f"DELETE FROM public.interaction_rule_members WHERE rule_id IN {ids(rids)};")

# ------------------------------------------------------------- symptoms
w("--SPLIT:symptoms")
w("\n-- ==================================================================== SYMPTOMS")
cols = ["id", "name", "scientific_name", "description", "body_system_id", "is_red_flag",
        "diagnostic_weight", "weight_rationale", "tags", "source_attribution", "is_published"]
w(upsert("symptoms", "id", cols, [[
    q(s["id"]), q(s["name"]), q(s.get("scientific_name") or ""), q(s["description"]),
    system(s.get("body_system")), q(bool(s["is_red_flag"])), q(int(s["diagnostic_weight"])),
    q(s.get("weight_rationale") or ""), arr(s.get("tags", [])),
    q(refs_attribution(s.get("references", []))), "true"] for s in S]))
w(insert("symptom_causes", ["symptom_id", "content", "position"],
         [[q(s["id"]), q(c), str(i)] for s in S for i, c in enumerate(s.get("causes", []))]))
w(insert("symptom_red_flags", ["symptom_id", "content", "position"],
         [[q(s["id"]), q(c), str(i)] for s in S for i, c in enumerate(s.get("red_flags", []))]))
w(insert("symptom_references", ["symptom_id", "source_name", "citation_text", "url",
                                "is_mother_book", "position"],
         [[q(s["id"]), q(r["source_name"]), q(r.get("citation_text") or ""), q(r.get("url") or ""),
           q(bool(r.get("is_mother_book"))), str(i)]
          for s in S for i, r in enumerate(s.get("references", []))]))

# ------------------------------------------------------------ medicines
w("--SPLIT:medicines")
w("\n-- =================================================================== MEDICINES")
cols = ["id", "name", "generic_name", "trade_name", "drug_class", "category", "description",
        "dosage_info", "dosage_text", "storage_instructions", "storage", "black_box_warning",
        "international_generic_name", "source_attribution", "is_published"]
w(upsert("medicines", "id", cols, [[
    q(m["id"]), q(m["name"]), q(m.get("generic_name")), q(m.get("trade_name")), q(m["drug_class"]),
    q(m["category"]), q(m.get("description")), q(m.get("dosage_text")), q(m.get("dosage_text") or ""),
    q(m.get("storage")), q(m.get("storage") or ""), q(m.get("black_box_warning") or None),
    q(m.get("international_generic_name") or ""), q(m.get("source_attribution") or ""), "true"]
    for m in M]))
facts = []
for m in M:
    for kind, key in (("brand_ph", "brands_ph"), ("brand_intl", "brands_intl"),
                      ("indication", "indications"), ("adverse", "adverse"),
                      ("contraindication", "contraindications"), ("interaction", "interactions")):
        for i, text in enumerate(m.get(key, [])):
            facts.append([q(m["id"]), q(kind), q(text), str(i)])
w(insert("medicine_facts", ["medicine_id", "kind", "content", "position"], facts))
w(insert("medicine_brands", ["medicine_id", "market", "position", "brand_name"],
         [[q(m["id"]), q(market), str(i), q(b)] for m in M
          for market, key in (("philippine", "brands_ph"), ("international", "brands_intl"))
          for i, b in enumerate(m.get(key, []))]))
w(insert("medicine_references", ["medicine_id", "source_name", "citation_text", "url",
                                 "is_mother_book", "position"],
         [[q(m["id"]), q(r["source_name"]), q(r.get("citation_text") or ""), q(r.get("url") or ""),
           q(bool(r.get("is_mother_book"))), str(i)]
          for m in M for i, r in enumerate(m.get("references", []))]))

# ------------------------------------------------------------- diseases
w("--SPLIT:diseases")
w("\n-- ==================================================================== DISEASES")
cols = ["id", "name", "scientific_name", "description", "body_system_id", "severity", "urgency",
        "urgency_criteria", "contagious", "pathophysiology", "clinicopathologic_correlation",
        "onset_progression", "follow_up_monitoring", "source_attribution", "is_published"]
w(upsert("diseases", "id", cols, [[
    q(d["id"]), q(d["name"]), q(d.get("scientific_name")), q(d["description"]),
    system(d.get("body_system")), q(d["severity"]), q(d.get("urgency")),
    q(d.get("urgency_criteria")), q(bool(d.get("contagious"))), q(d.get("pathophysiology")),
    q(d.get("clinicopathologic_correlation")), q(d.get("onset_progression")),
    q(d.get("follow_up_monitoring")), q(d.get("source_attribution")), "true"] for d in D]))
for table, key in (("disease_causes", "causes"), ("disease_risk_factors", "risk_factors"),
                   ("disease_recommended_tests", "recommended_tests"),
                   ("disease_treatments", "treatments"), ("disease_home_care", "home_care"),
                   ("disease_emergency_signs", "emergency_signs")):
    w(insert(table, ["disease_id", "position", "content"],
             [[q(d["id"]), str(i), q(c)] for d in D for i, c in enumerate(d.get(key, []))]))
w(insert("disease_prevention", ["disease_id", "position", "content", "tier"],
         [[q(d["id"]), str(i), q(p["content"]), q(p.get("tier") or None)]
          for d in D for i, p in enumerate(d.get("prevention", []))]))
w(insert("disease_differentials", ["disease_id", "position", "condition", "distinguishing_feature"],
         [[q(d["id"]), str(i), q(x["condition"]), q(x["distinguishing_feature"])]
          for d in D for i, x in enumerate(d.get("differentials", []))]))
w(insert("disease_tags", ["disease_id", "tag"],
         [[q(d["id"]), q(t)] for d in D for t in dict.fromkeys(d.get("tags", []))]))
w(insert("clinical_references", ["id", "disease_id", "position", "source_name", "citation_text",
                                 "url", "specialty", "is_mother_book"],
         [[q(f"ref_{d['id']}_{i + 1}"), q(d["id"]), str(i), q(r["source_name"]),
           q(r.get("citation_text") or ""), q(r.get("url") or None), q(r.get("specialty") or None),
           q(bool(r.get("is_mother_book")))]
          for d in D for i, r in enumerate(d.get("references", []))]))

w("\n-- ------------------------------------- disease <-> symptom (drives the Symptom Checker)")
w(insert("disease_symptoms", ["disease_id", "symptom_id", "typical_intensity", "is_primary",
                              "weight_multiplier"],
         [[q(d["id"]), q(l["symptom_id"]), str(int(l["typical_intensity"])),
           q(bool(l["is_primary"])), str(float(l["weight_multiplier"]))]
          for d in D for l in d["symptoms"]]))
w("\n-- ------------------------------------------- disease <-> medicine (safety in that disease)")
w(insert("disease_medicines", ["disease_id", "medicine_id", "position", "safety", "note"],
         [[q(d["id"]), q(x["medicine_id"]), str(i), q(x["safety"]), q(x.get("note"))]
          for d in D for i, x in enumerate(d.get("medicines", []))]))
related = []
seen = set()
for d in D:
    for r in d.get("related", []):
        for a, b in ((d["id"], r), (r, d["id"])):      # both directions
            if a != b and (a, b) not in seen:
                seen.add((a, b))
                related.append([q(a), q(b)])
w(insert("disease_related", ["disease_id", "related_disease_id"], related))

# ------------------------------------------------ Drug Interaction Checker
w("--SPLIT:checker")
w("\n-- ============================================= DRUG INTERACTION CHECKER")
w("-- Drug x patient condition")
w(insert("medicine_condition_safety", ["medicine_id", "condition_id", "safety", "summary",
                                       "guidance", "source_attribution"],
         [[q(m["id"]), q(c["condition_id"]), q(c["safety"]), q(c.get("summary") or ""),
           q(c.get("guidance") or ""), q(c.get("source_attribution") or "")]
          for m in M for c in m.get("condition_safety", [])]))
w("\n-- Drug x drug (stored once per pair, lower id first)")
pairs = []
for p in IX["pairs"]:
    a, b = sorted((p["a"], p["b"]))
    source = p.get("source_attribution") or ""
    if p.get("url"):
        source = f"{source} ({p['url']})" if source else p["url"]
    pairs.append([q(a), q(b), q(p["severity"]), q(p["description"]),
                  q(p.get("clinical_significance") or ""), q(p.get("recommendation") or ""),
                  q(source), "true"])
w(insert("drug_interactions", ["medicine_a_id", "medicine_b_id", "severity", "description",
                               "clinical_significance", "recommendation", "source_attribution",
                               "is_published"], pairs))
w("\n-- Multi-drug rules (members match drug_class keywords)")
cols = ["id", "name", "severity", "description", "clinical_significance", "recommendation",
        "required_condition_id", "source_attribution", "is_published"]
data = []
for r in IX["rules"]:
    source = r.get("source_attribution") or ""
    if r.get("url"):
        source = f"{source} ({r['url']})" if source else r["url"]
    data.append([q(r["id"]), q(r["name"]), q(r["severity"]), q(r["description"]),
                 q(r.get("clinical_significance") or ""), q(r.get("recommendation") or ""),
                 q(r.get("required_condition_id") or None), q(source), "true"])
w(upsert("interaction_rules", "id", cols, data))
members = []
for r in IX["rules"]:
    for mem in r["members"]:
        if isinstance(mem, dict):
            members.append([q(r["id"]), q(mem["medicine_id"]), "NULL"])
        else:
            members.append([q(r["id"]), "NULL", q(mem)])
w(insert("interaction_rule_members", ["rule_id", "medicine_id", "drug_class_keyword"], members))

w("""
-- Tell every installed app to re-download the reference data.
UPDATE public.content_version SET version = version + 1, updated_at = now() WHERE id = 1;

COMMIT;
""")

full = "\n".join(l for l in out if not l.startswith("--SPLIT:"))
(R.parent / "seed_reference_data.sql").write_text(full, encoding="utf-8")

# The same seed in 4 smaller files, for SQL editors with a size limit.
# Run them in order; each is its own transaction.
sections, name = {}, "head"
for line in out:
    if line.startswith("--SPLIT:"):
        name = line.split(":", 1)[1]
        continue
    sections.setdefault(name, []).append(line)
head = sections["head"]          # header comment + BEGIN + body systems + conditions
header, begin = head[0].split("\nBEGIN;")[0], "\nBEGIN;"
tail = "\n-- Tell every installed app to re-download the reference data.\n" \
       "UPDATE public.content_version SET version = version + 1, updated_at = now() WHERE id = 1;\n\nCOMMIT;\n"
parts = {
    "part1_symptoms.sql": head + sections["clear"] + sections["symptoms"],
    "part2_medicines.sql": [header, begin] + sections["medicines"],
    "part3_diseases.sql": [header, begin] + sections["diseases"],
    "part4_interaction_checker.sql": [header, begin] + sections["checker"],
}
split_dir = R.parent / "split"
split_dir.mkdir(exist_ok=True)
for i, (fname, lines) in enumerate(parts.items(), start=1):
    body = "\n".join(lines)
    body = body.replace("\nCOMMIT;\n", "\n")   # the last part carries the only COMMIT
    if not body.rstrip().endswith("COMMIT;"):
        last = i == len(parts) and "content_version" not in body   # bump only once
        body = body.rstrip() + "\n" + (tail if last else "\nCOMMIT;\n")
    (split_dir / fname).write_text(f"-- Part {i} of {len(parts)}. Run the parts in order.\n" + body,
                                   encoding="utf-8")

# ------------------------------------------------------------- reset file
reset = """-- =====================================================================
-- OPTIONAL and DESTRUCTIVE: clears ALL reference content (diseases,
-- symptoms, medicines, their lists, links and references, and the drug
-- interaction data) so seed_reference_data.sql starts from a clean slate.
--
-- It does NOT touch users/auth, body_systems or patient_conditions.
-- Run it only if you want to remove the old data. Take a backup first
-- (Supabase: Database > Backups) if you might need the old rows.
-- =====================================================================

BEGIN;

DELETE FROM public.interaction_rule_members;
DELETE FROM public.interaction_rules;
DELETE FROM public.drug_interactions;
DELETE FROM public.medicine_condition_safety;

DELETE FROM public.disease_symptoms;
DELETE FROM public.disease_medicines;
DELETE FROM public.disease_related;
DELETE FROM public.disease_tags;
DELETE FROM public.disease_causes;
DELETE FROM public.disease_emergency_signs;
DELETE FROM public.disease_home_care;
DELETE FROM public.disease_recommended_tests;
DELETE FROM public.disease_risk_factors;
DELETE FROM public.disease_treatments;
DELETE FROM public.disease_prevention;
DELETE FROM public.disease_differentials;
DELETE FROM public.clinical_references;

DELETE FROM public.symptom_causes;
DELETE FROM public.symptom_red_flags;
DELETE FROM public.symptom_references;

DELETE FROM public.medicine_facts;
DELETE FROM public.medicine_references;
DELETE FROM public.medicine_brands;
DELETE FROM public.medicine_uses;
DELETE FROM public.medicine_side_effects;
DELETE FROM public.medicine_warnings;
DELETE FROM public.medicine_contraindications;
DELETE FROM public.medicine_interactions;

DELETE FROM public.diseases;
DELETE FROM public.symptoms;
DELETE FROM public.medicines;

UPDATE public.content_version SET version = version + 1, updated_at = now() WHERE id = 1;

COMMIT;
"""
(R.parent / "reset_reference_data.sql").write_text(reset, encoding="utf-8")
print("written", len("\n".join(out)))
