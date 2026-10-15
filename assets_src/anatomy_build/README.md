# Rebuilding the 3D body (assets/anatomy/)

Source: BodyParts3D 4.0, (c) The Database Center for Life Science, CC BY 4.0
(the zips and lists in ../bodyparts3d/).

1. Unzip `isa_BP3D_4.0_obj_99.zip` and adjust the paths at the top of the scripts.
2. `python parts.py`     -> parts.json (which parts go in which layer, names, systems)
3. `python regions.py`   -> regions.json (camera boxes: head, chest, abdomen, arms, legs)
4. `python build_glb.py [layer ...]` -> <layer>_raw.glb (all six layers if none given)  (needs `pip install trimesh numpy`)
5. Compress each layer (`npm install` first):
   npx gltfpack -i skin_raw.glb   -o skin.glb   -kn -gn 50 -si 0.3  -cc
   npx gltfpack -i bone_raw.glb   -o bone.glb   -kn -gn 50 -si 0.3  -cc
   npx gltfpack -i organ_raw.glb  -o organ.glb  -kn -gn 50 -si 0.25 -cc
   npx gltfpack -i muscle_raw.glb -o muscle.glb -kn -gn 50 -si 0.15 -cc
   npx gltfpack -i vessel_raw.glb -o vessel.glb -kn -gn 50 -si 0.4  -cc
   npx gltfpack -i nerve_raw.glb  -o nerve.glb  -kn -gn 50 -si 0.5  -cc
   (raise -si for more detail, at the cost of size)
6. Bundle the viewer:
   npx esbuild src/anatomy.js --bundle --format=iife --minify --target=chrome100 --outfile=anatomy.bundle.js
7. Copy anatomy.html, anatomy.bundle.js, parts.json, regions.json and the six .glb files
   into assets/anatomy/.

Blood vessels and nerves (vessel.glb, nerve.glb) are switched on separately in the app
and loaded on first use. Every vessel has a `vtype` in parts.json (artery, vein,
pulmonary_artery, pulmonary_vein, portal_vein) that picks its default colour; the user's
own colours are saved on their computer (akeso_anatomy_colours.json). BodyParts3D models
the major vessels; its nerves are limited to the eye and orbit plus the spinal canal.
