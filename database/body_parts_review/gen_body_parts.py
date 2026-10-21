"""Body part descriptions: research files -> migration + review sheet.

    python database/body_parts_review/gen_body_parts.py b01 053_body_parts_01.sql
    python database/body_parts_review/gen_body_parts.py b01 --check            (check only)
    python database/body_parts_review/gen_body_parts.py b01 --check out_femur.py

Reads database/body_parts_review/<batch>/MANIFEST.py (the keys and what each covers)
and <batch>/out_<slug>.py (one PART dict each), and writes:
    database/migrations/<out>.sql   (run in Supabase after 052_body_part_info.sql)
    database/migrations/<out>.md    (review sheet: every field and every source)

Checks before writing: no duplicate keys, every key is in the manifest, every FMA id
exists in assets/anatomy/parts.json, every disease_id is a real disease, every text
has a source that was opened ("checked"), word limits, and layer-specific detail keys.
Rows go in as drafts and only replace a row that is still a draft and differs, so
running the file twice changes nothing, and nothing edited or reviewed in the app is
ever overwritten.
"""

import collections
import json
import os
import re
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PARTS = os.path.join(ROOT, "assets", "anatomy", "parts.json")

# Same list the medicine review links to (every id is a disease page in Supabase).
KNOWN_DISEASES = set("""acute_coronary_syndrome acute_gastroenteritis ischemic_stroke asthma varicella chikungunya cholera copd
community_acquired_pneumonia covid19 dengue hypertension hfmd heart_failure hepatitis_a hepatitis_b hiv_infection influenza
leptospirosis malaria measles migraine peptic_ulcer_disease pertussis tuberculosis rabies schistosomiasis type2_diabetes
typhoid_fever urinary_tract_infection acute_appendicitis gerd iron_deficiency_anemia chronic_kidney_disease rheumatic_fever
post_strep_glomerulonephritis bacterial_meningitis graves_disease gout scabies""".split())

DETAIL_KEYS = {
    "bone": ("type", "joints", "landmarks"),
    "muscle": ("origin", "insertion", "action", "nerve_supply", "blood_supply"),
    "organ": ("functions", "blood_supply", "nerve_supply", "lymph_drainage"),
    "vessel": ("origin", "territory", "branches"),
    "nerve": ("origin", "type", "supplies"),
}
DETAIL_TITLES = {"type": "Type", "joints": "Joints", "landmarks": "Landmarks", "origin": "Origin",
                 "insertion": "Insertion", "action": "Action", "nerve_supply": "Nerve supply",
                 "blood_supply": "Blood supply", "functions": "Main functions",
                 "lymph_drainage": "Lymph drainage", "territory": "Supplies / drains",
                 "branches": "Main branches", "supplies": "Supplies"}
# field: (max words, max sentences or 0)
LIMITS = {"summary_plain": (40, 2), "function_plain": (30, 1), "description": (100, 4),
          "location": (60, 0), "exam_tip": (35, 0)}
TEXT_FIELDS = ("summary_plain", "function_plain", "description", "location", "exam_tip")
LICENCES = ("Public domain", "CC BY 4.0")   # see BRIEF.md, Sources


def q(v) -> str:
    return "'" + str(v).replace("'", "''") + "'"


def concept_key(name: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\b(left|right)\b", " ", name.lower())).strip()


def slug(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.lower().replace("group:", "group_")).strip("_")


def words(s: str) -> int:
    return len(s.split())


def sentences(s: str) -> int:
    return len([x for x in re.split(r"(?<=[.!?])\s+", s.strip()) if x])


def load_parts():
    with open(PARTS, encoding="utf-8") as f:
        parts = json.load(f)
    by_concept, by_group = collections.defaultdict(list), collections.defaultdict(list)
    for p in parts.values():
        by_concept[concept_key(p["name"])].append(p)
        for g in p["groups"]:
            by_group[g["id"]].append(p)
    return by_concept, by_group


def resolve(entries):
    """Manifest rows -> {key: info} with fma_ids, kind and body system."""
    by_concept, by_group = load_parts()
    out = {}
    for key, name, layer, select in entries:
        assert key not in out, ("duplicate key", key)
        members = []
        for s in select:
            kind, _, ref = s.partition(":")
            found = by_concept.get(ref) if kind == "c" else by_group.get(ref)
            assert found, (key, "not in parts.json", s)
            members += found
        fmas = sorted({p["fma"] for p in members})
        system = collections.Counter(p["system"] for p in members).most_common(1)[0][0]
        out[key] = {"key": key, "display_name": name, "layer": layer, "system": system,
                    "kind": "group" if key.startswith("group:") else "part", "fma_ids": fmas,
                    "covers": sorted({concept_key(p["name"]) for p in members})}
    return out


def check(part: dict, info: dict) -> list:
    """Problems with one research file (empty list = fine)."""
    k = part.get("key")
    bad = []
    need = ("key", "aliases", "details", "clinical", "sources", "checked") + TEXT_FIELDS
    bad += [f"missing field {f}" for f in need if f not in part]
    if bad:
        return bad
    for f, (mw, ms) in LIMITS.items():
        v = part[f].strip()
        if v and words(v) > mw:
            bad.append(f"{f}: {words(v)} words (max {mw})")
        if v and ms and sentences(v) > ms:
            bad.append(f"{f}: {sentences(v)} sentences (max {ms})")
    allowed = DETAIL_KEYS[info["layer"]]
    for dk, dv in part["details"].items():
        if dk not in allowed:
            bad.append(f"details.{dk} is not a {info['layer']} field ({', '.join(allowed)})")
        elif not isinstance(dv, str) or words(dv) > 50:
            bad.append(f"details.{dk} must be text of at most 50 words")
    if len(part["clinical"]) > 5:
        bad.append("clinical: at most 5 lines")
    for line in part["clinical"]:
        if len(line) != 2 or not line[0].strip():
            bad.append(f"clinical line must be (text, disease_id or ''): {line!r}")
            continue
        if words(line[0]) > 35:
            bad.append(f"clinical line over 35 words: {line[0][:40]}...")
        if line[1] and line[1] not in KNOWN_DISEASES:
            bad.append(f"clinical disease_id {line[1]!r} is not a disease page")
    for a in part["aliases"]:
        if not a.strip() or a.strip().lower() == info["display_name"].lower():
            bad.append(f"alias {a!r} is blank or the same as the name")
    has_text = any(part[f].strip() for f in TEXT_FIELDS) or part["details"] or part["clinical"]
    if has_text and not part["sources"]:
        bad.append("text without any source")
    checked = {u for u, _ in part["checked"]}
    for src in part["sources"]:
        if len(src) != 3:
            bad.append(f"source must be (title, url, licence): {src!r}")
            continue
        title, url, lic = src
        if not title.strip() or not url.startswith("https://"):
            bad.append(f"source needs a title and an https link: {src!r}")
        if url not in checked:
            bad.append(f"source not in checked (open it first): {url}")
        if lic not in LICENCES:
            bad.append(f"licence {lic!r} not one of {LICENCES}")
    return bad


def row_sql(part: dict, info: dict) -> str:
    def arr(xs):
        return "'{}'::text[]" if not xs else "array[" + ", ".join(q(x) for x in xs) + "]::text[]"

    def js(v):
        return q(json.dumps(v, ensure_ascii=False)) + "::jsonb"

    details = {k: v.strip() for k, v in part["details"].items() if v.strip()}
    clinical = [({"text": t.strip(), "disease_id": d} if d else {"text": t.strip()}) for t, d in part["clinical"]]
    sources = [{"title": t, "url": u, "licence": lic} for t, u, lic in part["sources"]]
    cols = ["kind", "fma_ids", "layer", "system", "display_name", "aliases", "summary_plain",
            "function_plain", "description", "location", "details", "clinical", "exam_tip", "sources"]
    vals = [q(info["kind"]), arr(info["fma_ids"]), q(info["layer"]), q(info["system"]),
            q(info["display_name"]), arr([a.strip() for a in part["aliases"]])]
    vals += [q(part[f].strip()) for f in ("summary_plain", "function_plain", "description", "location")]
    vals += [js(details), js(clinical), q(part["exam_tip"].strip()), js(sources)]
    sets = ",\n    ".join(f"{c} = excluded.{c}" for c in cols)
    old = ", ".join(f"b.{c}" for c in cols)
    new = ", ".join(f"excluded.{c}" for c in cols)
    return (f"-- {info['display_name']}  ({len(info['fma_ids'])} FMA ids)\n"
            f"insert into public.body_part_info as b (key, {', '.join(cols)}, status)\nvalues ({q(info['key'])},\n    "
            + ",\n    ".join(vals) + ",\n    'draft')\n"
            f"on conflict (key) do update set\n    {sets},\n    updated_at = now()\n"
            f"where b.status = 'draft'\n  and ({old})\n  is distinct from ({new});\n\n")


def md_for(part: dict, info: dict) -> str:
    L = [f"## {info['display_name']}  (`{info['key']}`)", "",
         f"*{info['kind']} · {info['layer']} · {info['system']} · {len(info['fma_ids'])} FMA ids · "
         f"covers: {', '.join(info['covers'][:8])}{' …' if len(info['covers']) > 8 else ''}*", ""]
    if part["aliases"]:
        L += [f"**Also called:** {', '.join(part['aliases'])}", ""]
    for f, title in (("summary_plain", "Summary (plain)"), ("function_plain", "What it does (plain)"),
                     ("description", "For students: description"), ("location", "Location & neighbours")):
        L += [f"**{title}**", "", part[f].strip() or "*(blank: no source found)*", ""]
    rows = [(DETAIL_TITLES[k], part["details"].get(k, "").strip()) for k in DETAIL_KEYS[info["layer"]]]
    L += ["| Detail | |", "|---|---|"] + [f"| {t} | {v.replace('|', '/') or '*(blank)*'} |" for t, v in rows] + [""]
    if part["clinical"]:
        L += ["**Clinical relevance**", ""]
        L += [f"- {t}" + (f"  → disease page `{d}`" if d else "") for t, d in part["clinical"]] + [""]
    L += ["**Exam tip**", "", part["exam_tip"].strip() or "*(blank)*", "", "**Sources**", ""]
    L += [f"- [{t}]({u}) ({lic})" for t, u, lic in part["sources"]]
    L += ["", "**What was checked on each page**", ""] + [f"- {u}: {w}" for u, w in part["checked"]]
    return "\n".join(L) + "\n\n---\n\n"


def load_batch(batch: str):
    folder = os.path.join(HERE, batch)
    infos = resolve(runpy.run_path(os.path.join(folder, "MANIFEST.py"))["ENTRIES"])
    parts = {}
    for f in sorted(os.listdir(folder)):
        if f.startswith("out_") and f.endswith(".py"):
            p = runpy.run_path(os.path.join(folder, f))["PART"]
            assert p.get("key") in infos, (f, "key not in MANIFEST", p.get("key"))
            assert f == f"out_{slug(p['key'])}.py", (f, "should be named", f"out_{slug(p['key'])}.py")
            assert p["key"] not in parts, (f, "duplicate key")
            parts[p["key"]] = p
    return folder, infos, parts


def main(argv) -> int:
    batch = argv[0]
    folder, infos, parts = load_batch(batch)
    only = argv[2] if len(argv) > 2 and argv[1] == "--check" else None
    problems = 0
    for key, part in parts.items():
        if only and f"out_{slug(key)}.py" != only:
            continue
        for b in check(part, infos[key]):
            print(f"{key}: {b}")
            problems += 1
    if only:
        print("ok" if not problems else f"{problems} problem(s)")
        return 1 if problems else 0
    missing = [k for k in infos if k not in parts]
    print(f"{len(parts)}/{len(infos)} entries written; missing: {', '.join(missing) or 'none'}")
    if problems or argv[1] == "--check":
        print("ok" if not problems else f"{problems} problem(s)")
        return 1 if problems else 0
    out_name = argv[1]
    keys = [k for k in infos if k in parts]
    sql = (f"-- {out_name}  -  body part descriptions, batch {batch} ({len(keys)} entries)\n"
           "-- Needs 052_body_part_info.sql first. Adds draft rows only: a row that is already\n"
           "-- reviewed or published, or that has not changed, is left alone, so this is safe\n"
           "-- to run twice. Drafts are not shown in the app until they are published.\n\nbegin;\n\n")
    sql += "".join(row_sql(parts[k], infos[k]) for k in keys)
    sql += ("commit;\n\n-- After the review, to publish this batch (bumps content_version so apps re-download):\n"
            "-- begin;\n-- update public.body_part_info set status = 'published', updated_at = now()\n"
            f"--  where status <> 'published' and key in ({', '.join(q(k) for k in keys)});\n"
            "-- update public.content_version set version = version + 1, updated_at = now() where id = 1;\n"
            "-- commit;\n")
    md = (f"# Body part descriptions {batch}: review sheet\n\nRun `{out_name}` in Supabase after you have "
          "checked this (after `052_body_part_info.sql`). Rows go in as **drafts**; the publish statement "
          "is at the end of the SQL file. Blank fields had no source and are left blank on purpose.\n\n")
    notes = os.path.join(folder, "NOTES.md")
    if os.path.exists(notes):
        md += open(notes, encoding="utf-8").read() + "\n\n"
    for f in sorted(os.listdir(folder)):   # each research agent's notes
        if f.startswith("notes_") and f.endswith(".md"):
            md += f"#### From {f}\n\n" + open(os.path.join(folder, f), encoding="utf-8").read().strip() + "\n\n"
    md += "---\n\n"
    md += "".join(md_for(parts[k], infos[k]) for k in keys)
    base = os.path.join(ROOT, "database", "migrations", out_name)
    open(base, "w", encoding="utf-8", newline="\n").write(sql)
    open(base[:-4] + ".md", "w", encoding="utf-8", newline="\n").write(md)
    print("wrote", base)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
