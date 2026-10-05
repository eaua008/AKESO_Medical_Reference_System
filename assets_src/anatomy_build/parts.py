"""Pick the parts for each layer and give every element file a readable name."""
import csv, collections, json, os
S = "/mnt/user-data/uploads/akeso/assets_src/bodyparts3d/"
D = "/var/tmp/bp3d/isa_BP3D_4.0_obj_99/"
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
parts = {fj: {"fma": best[fj], "name": names[best[fj]], "layer": layer[fj], "system": system[fj],
              "group_fma": group.get(fj, ""), "group": names.get(group.get(fj, ""), "")}
         for fj in sorted(layer)}
json.dump(parts, open("/var/tmp/anat/build/parts.json", "w"), indent=0)
c = collections.Counter(p["layer"] for p in parts.values()); print(c, len(parts))
for fj in list(parts)[:3]: print(fj, parts[fj])
print([ (p["name"]) for p in parts.values() if p["layer"]=="organ"][:15])
