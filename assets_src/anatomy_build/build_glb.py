import json, numpy as np, trimesh, sys
D = "/var/tmp/bp3d/isa_BP3D_4.0_obj_99/"
parts = json.load(open("/var/tmp/anat/build/parts.json"))
def load(fj):
    v, f = [], []
    for line in open(D + fj + ".obj"):
        if line.startswith("v "): v.append(line.split()[1:4])
        elif line.startswith("f "):
            idx = [int(t.split("/")[0]) - 1 for t in line.split()[1:]]
            for i in range(1, len(idx) - 1): f.append((idx[0], idx[i], idx[i + 1]))
    return trimesh.Trimesh(np.array(v, float), np.array(f, int), process=False)
for layer in ("skin", "bone", "organ", "muscle"):
    scene = trimesh.Scene()
    for fj, p in parts.items():
        if p["layer"] == layer:
            m = load(fj)
            scene.add_geometry(m, node_name=fj, geom_name=fj)
    scene.export(f"/var/tmp/anat/build/{layer}_raw.glb")
    print(layer, len(scene.geometry), sum(len(g.faces) for g in scene.geometry.values()))
