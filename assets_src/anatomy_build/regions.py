import csv, collections, json, numpy as np
S = "/mnt/user-data/uploads/akeso/assets_src/bodyparts3d/"; D = "/var/tmp/bp3d/isa_BP3D_4.0_obj_99/"
el = collections.defaultdict(set)
for f in ("isa_element_parts.txt", "partof_element_parts.txt.txt"):
    for r in list(csv.reader(open(S + f, encoding="utf-8", errors="replace"), delimiter="\t"))[1:]:
        el[r[0]].add(r[2])
cache = {}
def bb(fj):
    if fj not in cache:
        v = np.array([l.split()[1:4] for l in open(D + fj + ".obj") if l.startswith("v ")], float)
        cache[fj] = (v.min(0), v.max(0))
    return cache[fj]
def union(*ids):
    fs = set().union(*(el[i] for i in ids))
    b = [bb(f) for f in fs]
    return [np.min([x[0] for x in b], 0).round(1).tolist(), np.max([x[1] for x in b], 0).round(1).tolist()]
R = {
  "body":    {"label": "Whole body", "box": union("FMA7163")},
  "head":    {"label": "Head",       "box": union("FMA46565", "FMA50801")},
  "chest":   {"label": "Chest",      "box": union("FMA7480", "FMA7088", "FMA7309", "FMA7310")},
  "abdomen": {"label": "Abdomen",    "box": union("FMA7197", "FMA7148", "FMA7200", "FMA7201", "FMA7204", "FMA7205", "FMA15900")},
  "arms":    {"label": "Arms",       "box": union("FMA24880", "FMA24881", "FMA23218", "FMA23219")},
  "legs":    {"label": "Legs",       "box": union("FMA24882", "FMA24883", "FMA16581")},
}
for k, v in R.items(): print(k, v["box"])
json.dump(R, open("/var/tmp/anat/build/regions.json", "w"), indent=1)
