# Notes, agent f (batch b01)

## Fields left blank and why
- **Brain** (`group:fma_FMA50801_o`): `blood_supply`, `nerve_supply` and `lymph_drainage` are blank. None of the allowed pages I opened describe the arteries of the brain. The NINDS "Brain Basics: Know Your Brain" page returned 403 on both www and non-www URLs, and the NHLBI carotid page returned 404. Nerve supply and lymph drainage don't apply in the usual organ sense, and no source covered them.
- **Cerebellum**: same three fields blank, for the same reason. The SEER and MedlinePlus pages give only its location, size rank, peduncles and function.
- **Eyeball** (`group:eye_ball`): `blood_supply`, `nerve_supply` and `lymph_drainage` are blank. The only fact found was that the choroid carries blood vessels, and that came from an NCI Dictionary search snippet. Its page showed navigation only via WebFetch, so I didn't use it. `aliases` is empty.
- **Optic nerve**: everything is filled. `aliases` is empty.
- **Skull** (`group:skull`): everything is filled. `aliases` is empty. I didn't use "cranium" as an alias, because Gray's treats the cranium as only one part of the skull.

## Doubts
- **Optic nerve `type` = "sensory"**: this is my inference. The SEER PNS page says the cranial nerves for smell, vision, hearing and equilibrium carry only sensory fibers, but it never names the optic nerve. MedlinePlus and NEI say it carries visual signals from the retina to the brain.
- **Optic nerve and glaucoma**: MedlinePlus Optic Nerve Disorders says glaucoma is "the leading cause of blindness in the United States". I wrote "a leading cause ... in the United States". The NEI glaucoma page doesn't make that claim.
- **Skull `type` = "flat"**: SEER says most cranial bones are flat and some skull bones are irregular. The skull is a group of bones, so "flat" describes most of the cranium, not every bone.
- **Skull bone count**: SEER's axial skeleton page puts 28 bones under the skull, counting the 6 ossicles. I gave only the 8 cranial and 14 facial bones, matching the entry's group, and didn't state a total. SEER spells palatine as "Platine", a typo, so I used "palatine".
- **Terminology**: Gray's 1918 uses "hypophysis" and "squamosal suture". I wrote "pituitary" and "squamosal", which TA calls the squamous suture. You may want to change it to "squamous suture".
- **Brain exam tip**: "the thalamus is about 80 percent of the diencephalon" comes from SEER CNS. "About 80% of strokes are ischemic" comes from MedlinePlus Stroke, which gives no country.
- **Disease links**: `ischemic_stroke` on the stroke line and `bacterial_meningitis` on the meningitis line. I left diabetic retinopathy unlinked rather than tie it to `type2_diabetes`.
- **NCI tumor anatomy page title**: I wrote "Brain and Spine Tumor Anatomy - National Cancer Institute" from the URL path (cancer.gov/rare-brain-spine-tumor/tumors/anatomy). The exact page title wasn't confirmed.

## URLs
- PubAnnotation GrayAnatomy holds only 75 docs, mostly osteology. The nervous system and eye chapters aren't there: 150, 189 and 200 return the site index. Docs 46 (skull as a whole) and 47 (base of skull, fontanelles) were used.
- The NINDS Brain Basics page returned 403, the NEI "parts-eye" page 404, the NEI optic neuritis page 404, and the NHLBI carotid-artery-disease page 404. None of them is cited.
- NCI Dictionary pages for sclera, optic nerve and vitreous humor showed navigation only. None is cited.
