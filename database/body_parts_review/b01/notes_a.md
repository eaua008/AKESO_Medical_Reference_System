# Notes: agent a, batch b01 (heart, aorta, pulmonary trunk, left and right coronary arteries)

## General
- Gray's Anatomy was not usable for any of these entries. The PubAnnotation GrayAnatomy source has only
  75 documents (embryology and osteology, e.g. 1-9, 19, 27, 30, 41, 42, 50, 59, 60), with no angiology
  or heart chapters (sourceid 138 is empty). So branch-level detail (sinuses, course of the coronaries,
  pulmonary bifurcation level, thoracic aortic intercostal branches) is limited to what SEER, NHLBI
  and MedlinePlus say.
- NCI Dictionary "pulmonary-artery" loaded only navigation; not cited.
- SEER respiratory page `.../respiratory/passages/lungs.html` returned 404; not used. The SEER lung
  cancer module anatomy page (https://training.seer.cancer.gov/lung/anatomy/) was used instead.
- All cited URLs opened on the first try.

## group:fma_FMA7088_o (Heart)
Blank: `aliases` (no everyday alternative name in sources), `details.lymph_drainage` (no source opened).
Doubts:
- `nerve_supply` describes control by the cardiac center in the medulla with sympathetic and
  parasympathetic components (SEER physiology page); no source opened names the vagus nerve or the
  cardiac plexus, so they are not mentioned.
- "Mediastinum" is not used in location: no source opened said it.
- Clinical line 1 links acute_coronary_syndrome; it is about CAD in general (which includes heart
  attack), so the link is my inference. Line 3 (valve disease) has no id.

## group:fma_FMA3734_v (Aorta)
Blank: `aliases`. All details filled.
Doubts:
- Thoracic aorta branches: only the bronchial arteries are sourced (SEER lung anatomy: they branch
  off the aorta; it does not say "thoracic aorta" explicitly; I placed them on the thoracic part).
  Intercostal and esophageal branches are not mentioned because no source opened gave them.
- The SEER pathways page lists the iliac arteries' branches but not the aortic bifurcation into the
  common iliac arteries by name; I wrote "then the iliac arteries".
- Aneurysm risk-factor line has no disease id (hypertension is only one risk factor among several).

## pulmonary trunk
Blank: none.
Doubts:
- `aliases` = ["pulmonary artery"]: NHLBI and the SEER lung page call the vessel leaving the right
  ventricle "the pulmonary artery"; SEER heart structure uses "pulmonary trunk".
- No source gives the level of the bifurcation or right vs left artery length; only "splits into two
  arteries, one for each lung" (SEER lung anatomy).
- Pulmonary hypertension line not linked to heart_failure (heart failure is only a complication).

## group:v_coronary_l / group:v_coronary_r
Blank: `aliases` (no source says "left main" etc.).
Doubts:
- Branches and territories are from the NHLBI Blood Flow page only. It says the right coronary's
  marginal arteries supply "the surface of the right atrium", which is how NHLBI puts it; standard
  texts usually describe the right marginal artery supplying the right ventricle. The owner may want
  to check this line. No source gave the coronary sulcus course, the sinuses of origin, or the SA/AV
  nodal arteries.
- Clinical lines are the same for both arteries (no source gave side-specific findings).
