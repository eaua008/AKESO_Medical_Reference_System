"""Pick the parts for each layer and give every element file a readable name."""
import csv, collections, json, os
S = "C:/Users/eijki/IdeaProjects/akeso/assets_src/bodyparts3d/"
D = "C:/Users/eijki/AppData/Local/Temp/claude/C--Users-eijki-IdeaProjects-akeso/76cf4ddd-5c85-42a6-a063-3a7b46c16906/scratchpad/bp3d/isa_BP3D_4.0_obj_99/"
el = collections.defaultdict(set); names = {}
for f in ("isa_element_parts.txt", "partof_element_parts.txt.txt"):
    for r in list(csv.reader(open(S + f, encoding="utf-8", errors="replace"), delimiter="\t"))[1:]:
        el[r[0]].add(r[2]); names[r[0]] = r[1]
def files(*ids):
    out = set()
    for i in ids: out |= el[i]
    return out
# organs, grouped by the body system they belong to (anatomical grouping only)
ORGANS = {
    "nervous": ["FMA50801", "FMA12514", "FMA12515"],                  # brain, eyeballs
    "cardiovascular": ["FMA7088"],                                      # heart
    "respiratory": ["FMA7309", "FMA7310", "FMA7394"],                   # lungs, trachea
    "digestive": ["FMA7131", "FMA7148", "FMA7197", "FMA7202", "FMA7198", "FMA7200", "FMA7201"],
    "urinary": ["FMA7204", "FMA7205", "FMA15900"],
    "endocrine": ["FMA13889", "FMA15629", "FMA15630"],                  # pituitary, adrenals
}
layer, system = {}, {}
for sysname, ids in ORGANS.items():
    for fj in files(*ids):
        layer.setdefault(fj, "organ"); system.setdefault(fj, sysname)
for fj in files("FMA5018", "FMA55107"):            # bone organ, cartilage organ
    if fj not in layer: layer[fj] = "bone"; system[fj] = "musculoskeletal"
for fj in files("FMA5022"):                        # muscle organ
    if fj not in layer: layer[fj] = "muscle"; system[fj] = "musculoskeletal"
for fj in files("FMA7163"):
    layer[fj] = "skin"; system[fj] = "integumentary"
# Blood vessels: every artery and vein, including the ones that used to sit
# inside the heart, lung and liver models (they move to this layer so they
# can be shown, hidden and coloured as vessels). vtype drives the default
# colour: arteries red, veins blue, and the conventional exceptions
# (pulmonary arteries carry deoxygenated blood, pulmonary veins oxygenated).
vtype = {}
# "artery"/"vein" miss the big trunks (aorta, venae cavae), which FMA files
# as segments of the arterial / venous tree, so both are included.
for fj in files("FMA50720", "FMA86187"): vtype[fj] = "artery"
for fj in files("FMA50723", "FMA86188"): vtype[fj] = "vein"
for fj in files("FMA8612"): vtype[fj] = "pulmonary_artery"     # pulmonary trunk
for fj in files("FMA66326"): vtype[fj] = "pulmonary_artery"
for fj in files("FMA66643"): vtype[fj] = "pulmonary_vein"
for fj in files("FMA66645"): vtype[fj] = "portal_vein"
for fj in vtype:
    layer[fj] = "vessel"; system[fj] = "cardiovascular"
# Nerves: what BodyParts3D models (the spinal cord and the nerves of the
# eye and orbit: optic, oculomotor, trochlear, ophthalmic branches).
for fj in files("FMA65132", "FMA5865", "FMA5913", "FMA7647", "FMA78497"):
    layer[fj] = "nerve"; system[fj] = "nervous"
# ---------------------------------------------------------------------------
# Added later (add-only): the BodyParts3D element files the first build left
# out. Everything above is untouched; these only fill in files that no rule
# above placed, by what the most specific concept containing each one is
# called. `extra_note` lists the odd ones for review.
# ---------------------------------------------------------------------------
_best_all = {}
for fma, fs in el.items():
    for fj in fs:
        if fj not in _best_all or len(fs) < len(el[_best_all[fj]]):
            _best_all[fj] = fma
extra_group, extra_flags, extra_note = {}, {}, []
def _has(n, *words): return any(w in n for w in words)
def classify(n):
    """-> (layer, system, vtype, group_fma, group) for a concept name, or None to skip."""
    if _has(n, "tooth", "gingiva"):
        g = ("FMA12516", "teeth") if "tooth" in n else ("", "")
        return "bone", "musculoskeletal", None, g[0], g[1]
    if _has(n, "hair"): return "skin", "integumentary", None, "HAIR", "hair"
    if _has(n, "external ear", "eyebrow"): return "skin", "integumentary", None, "", ""
    if _has(n, "ciliary ganglion"): return "nerve", "nervous", None, "", ""
    # vessels
    if _has(n, "pulmonary vein"): return "vessel", "cardiovascular", "pulmonary_vein", "", ""
    if _has(n, "palmar arch") and "venous" not in n: return "vessel", "cardiovascular", "artery", "", ""
    if _has(n, "vein", "venous"): return "vessel", "cardiovascular", "vein", "", ""
    if _has(n, "artery", "arteries", "arterial", "branches of thoracic aorta"):
        return "vessel", "cardiovascular", "artery", "", ""
    # larynx / pharynx ligaments and small muscles: organs of the respiratory system
    if _has(n, "aryepiglotticus", "cricothyroid", "vocal ligament", "thyrohyoid", "stylohyoid",
            "epiglottic", "extrinsic ligament of larynx", "main bronchus", "subdivision of pharynx"):
        return "organ", "respiratory", None, "", ""
    if "conus elasticus" in n: return "muscle", "musculoskeletal", None, "", ""
    # bones and cartilage
    if _has(n, "costal cartilage", "manubrium", "body of sternum", "xiphoid"):
        return "bone", "musculoskeletal", None, "", ""
    # eye and orbit
    if _has(n, "retina", "lacrimal", "corona ciliaris", "anterior chamber", "check ligament",
            "common tendinous ring", "tarsal plate", "trochlea"):
        grp = ("FMA12514", "right eyeball") if "right" in n else ("FMA12515", "left eyeball")
        if not _has(n, "retina", "corona ciliaris", "anterior chamber"): grp = ("", "")
        if "anterior chamber of right" in n: grp = ("FMA12514", "right eyeball")
        return "organ", "nervous", None, grp[0], grp[1]
    # brain
    if _has(n, "thalamus", "caudate nucleus", "putamen", "globus pallidus", "corpus callosum",
            "fornix", "amygdala", "choroid plexus", "stria ", "lamina terminalis", "commissure",
            "wall of ventricle", "gyrus", "peduncle of midbrain", "brachium", "geniculate",
            "mammillary", "septum of telencephalon", "decussation", "subarachnoid", "dura mater"):
        return "organ", "nervous", None, "FMA50801", "brain"
    # organs
    if _has(n, "spleen", "thymus"): return "organ", "endocrine", None, "", ""
    if _has(n, "appendix", "mesentery", "mesocolon", "hepatic duct", "cystic duct",
            "duct of caudate", "tongue", "lip", "submandibular", "sublingual", "hepatovenous",
            "subdivision of mouth"): return "organ", "digestive", None, "", ""
    if _has(n, "testis", "epididymis", "prostate", "seminal vesicle", "deferent duct",
            "corpus cavernosum", "corpus spongiosum", "glans penis"):
        return "organ", "reproductive", None, "", ""
    if _has(n, "ureter", "urethra"): return "organ", "urinary", None, "", ""
    # muscles, tendons, ligaments
    if _has(n, "head of", "part of", "set of", "vastus", "rectus femoris", "iliococcygeus",
            "pubococcygeus", "puborectalis", "tendon", "retinaculum", "plantar ligament",
            "interosseous membrane", "iliotibial", "raphe", "tendinous arch", "intermediate tendon"):
        return "muscle", "musculoskeletal", None, "", ""
    return None
for fj in sorted(f[:-4] for f in os.listdir(D) if f.endswith(".obj")):
    if fj in layer: continue
    n = names.get(_best_all.get(fj, ""), "")
    if "conduit space" in n:        # an empty space, not a structure: not drawn
        extra_note.append((fj, n + " (skipped)")); continue
    c = classify(n)
    if c is None:
        c = ("organ", "musculoskeletal", None, "", ""); extra_note.append((fj, n))
    layer[fj], system[fj] = c[0], c[1]
    if c[2]: vtype[fj] = c[2]
    if c[3]: extra_group[fj] = (c[3], c[4])
    if c[3] == "HAIR": extra_flags[fj] = {"hair": True}
layer = {k: v for k, v in layer.items() if os.path.exists(D + k + ".obj")}
# the most specific concept containing each file is its name
best = {}
for fma, fs in el.items():
    for fj in fs:
        if fj in layer and (fj not in best or len(fs) < len(el[best[fj]])):
            best[fj] = fma
# a friendlier group name for the side panel ("heart", "skull", "right lung")
GROUPS = ["FMA12514", "FMA12515", "FMA50801", "FMA7088", "FMA7309", "FMA7310", "FMA7394", "FMA7131",
          "FMA7197", "FMA7202", "FMA7148", "FMA7198", "FMA7200", "FMA7201", "FMA7204", "FMA7205",
          "FMA15900", "FMA46565", "FMA7480", "FMA13478"]
group = {}
for g in GROUPS:
    for fj in el.get(g, ()):
        if fj in layer and fj not in group: group[fj] = g
for fj, (g, gname) in extra_group.items():
    group[fj] = g; names.setdefault(g, gname)
    if g in ("FMA12516", "HAIR"): names[g] = gname          # "teeth", "hair"
parts = {fj: {"fma": best[fj], "name": names[best[fj]], "layer": layer[fj], "system": system[fj],
              "group_fma": group.get(fj, ""), "group": names.get(group.get(fj, ""), "")}
         for fj in sorted(layer)}
for fj, flags in extra_flags.items(): parts[fj].update(flags)
for fj, kind in vtype.items():
    if fj in parts:
        parts[fj]["vtype"] = kind
        parts[fj]["group_fma"] = parts[fj]["group"] = ""     # a vessel is its own group
json.dump(parts, open("C:/Users/eijki/AppData/Local/Temp/claude/C--Users-eijki-IdeaProjects-akeso/76cf4ddd-5c85-42a6-a063-3a7b46c16906/scratchpad/anat/parts.json", "w"), indent=0)
c = collections.Counter(p["layer"] for p in parts.values()); print(c, len(parts))
for fj in list(parts)[:3]: print(fj, parts[fj])
print(collections.Counter(p.get("vtype") for p in parts.values() if p["layer"] == "vessel"))

print("odd ones (placed in organ / musculoskeletal):", extra_note)
