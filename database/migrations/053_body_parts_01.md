# Body part descriptions b01: review sheet

Run `053_body_parts_01.sql` in Supabase after you have checked this (after `052_body_part_info.sql`). Rows go in as **drafts**; the publish statement is at the end of the SQL file. Blank fields had no source and are left blank on purpose.

## Please check (batch 01)

### Decisions made while building B1 (2026-10-19, agreed with Eijkim)
- **Sources changed from the plan.** OpenStax *Anatomy & Physiology 2e* is not CC BY 4.0. Its
  pages say CC BY-NC-SA 4.0, and that the book "may not be used in the training of large language
  models or otherwise be ingested into large language models or generative AI offerings without
  OpenStax's prior written permission". StatPearls/NCBI shows a CAPTCHA. So B1 uses only US
  federal public-domain pages: NCI SEER Training Modules, MedlinePlus health topics (not the
  A.D.A.M. encyclopedia), NIDDK/NHLBI/NEI/NINDS/CDC. It also uses Gray's Anatomy 1918 (public
  domain), whose text is read on pubannotation.org. See BRIEF.md.
- **54 entries, not 53.** The left and right coronary arteries are two separate arteries, so each
  gets its own entry (`group:v_coronary_l`, `group:v_coronary_r`).
- **Rows go in as drafts.** Nothing shows in the app until it's published. The publish
  statement is at the end of the SQL file, ready for when the Explorer code exists.

### For the code phase (the lookup chain in the plan needs these)
1. **Look entries up by FMA id, not only by name.** Every row has `fma_ids` (all the model parts
   it covers, both sides; there's a GIN index on it). A clicked part should get the entry whose
   `fma_ids` contains its FMA id; when several do, the one with the fewest ids (most
   specific) wins. That one rule covers concepts, groups and the cases below.
2. **Whole muscles that aren't in the model.** Biceps brachii, triceps brachii, pectoralis
   major, trapezius and gastrocnemius exist only as their heads/parts ("long head of left biceps
   brachii"...). There is no whole-muscle part and no group for them. Their entries cover the
   heads' FMA ids, so rule 1 finds them. The plan's "walk the groups" step alone would not.
3. **"Left"/"right" is sometimes part of the anatomical name, not the side.** Stripping it
   merges different structures: "trunk of left coronary artery" and "trunk of right coronary
   artery" both become "trunk of coronary artery". The same goes for the left/right lobe of the
   liver, hemilivers, left/right portal vein, and the left/right side of the heart. Don't build
   concept keys from these names. Rule 1 avoids the problem.
4. **Eyeball** has no side-free curated group (only `eye_ball_l`/`eye_ball_r`). Its key is
   `group:eye_ball`, and its fma_ids cover both eyes.
5. **Heart, liver and brain** use the organ-layer FMA groups the plan named (`fma_FMA7088_o`,
   `fma_FMA7197_o`, `fma_FMA50801_o`). The vessel-layer copies (`fma_FMA7088_v`...) aren't
   covered, so cardiac vessels fall back to their own entries or to auto facts.
6. **parts.json data quirk:** the spleen's `system` is "endocrine". The entry keeps what
   parts.json says. Fix it in the model build if you want it under "lymphatic"/"immune".

### Sources to approve (not on the brief's list)
- **Gray's 1918 on the Internet Archive** (muscles): the same public-domain book, as OCR text.
  PubAnnotation only has the bone chapters. The cited link
  `archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt` redirects
  to the archive.org mirror the agents actually read. I swapped the mirror host names for this
  stable link.
- **NCI Dictionary (webapis.cancer.gov), NLM MeSH (id.nlm.nih.gov), NCI Thesaurus (EVS API,
  CC BY 4.0)** (mostly the great vessels): NIH/NLM definitions read through their data APIs,
  because the normal pages showed only navigation via WebFetch. **These links open raw JSON, not
  a readable page.** If you reject them, most vessel details and exam tips go blank.

### Top medical points to check (details in the agents' notes below)
1. **Right coronary artery, marginal branch:** the text says the marginal arteries supply "the
   surface of the right atrium". I rechecked: the NHLBI blood-flow page does say this. Standard
   anatomy texts say the right marginal artery supplies the right ventricle. Either drop that
   clause or replace it from another public-domain source.
2. **Hip bone type "flat":** Gray's lists it as flat in one place and irregular in another;
   modern texts say irregular.
3. **Inferred disease links:** hiatal hernia → `gerd`; coronary artery disease →
   `acute_coronary_syndrome`; carotid blockage → `ischemic_stroke`; pyelonephritis →
   `urinary_tract_infection`. Keep or remove each one.
4. **Inferred part ↔ fact links:** the femoral artery clinical lines (the sources say "leg
   arteries"); the neck strain lines on the SCM and trapezius; torticollis → SCM; the tibial
   shaft fracture (only a link title); the "venous drainage only" blood supply of the
   gallbladder, pancreas and small intestine.
5. **Blank on purpose (no allowed source):** the diaphragm's nerve supply (phrenic nerve), the
   clavicle's clinical lines, biceps and triceps clinical lines, the mandible's bone type, most
   organ nerve/artery/lymph fields, and the liver segments.
6. **Spelling is mixed** (British "oesophagus/haemorrhage" vs American "cecum"). Pick one and
   I'll normalise it.
7. **Aliases to reconsider:** "colon" for the whole large intestine; the veterinary
   "anterior/posterior vena cava".


#### From notes_a.md

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

#### From notes_b.md

# Notes, agent b (batch b01): six vessels

## Source situation (please review)
- **Gray's on PubAnnotation doesn't help here.** The GrayAnatomy sourcedb holds only 75 docs (embryology and osteology). Doc ids 143 and 170 return only the site front page, so it has no vessel chapters.
- **SEER** covers these vessels only in outline: the circulatory pathways page and the digestive accessory organs page.
- **No NLM-written MedlinePlus topic page** exists for most of these vessels. MedlinePlus was used only for carotid artery disease and peripheral arterial disease.
- **NCI Dictionary of Cancer Terms.** As the brief warned, the HTML page (cancer.gov .../def/portal-vein) showed only navigation. I read the definitions through NCI's own glossary API instead (webapis.cancer.gov/glossary/v1/...) and cite those API URLs. Licence: "Public domain" (NCI Dictionary). The API has no entries for "jugular-vein", "femoral-artery" or "central-venous-catheter" (404).
- **MeSH scope notes (NLM)** are read via id.nlm.nih.gov/mesh/M....json, licence "Public domain". Please check: MeSH is an NLM product, not one of the four source types the brief names, though it is a federal NIH work.
- **NCI Thesaurus (NCIt)** is read via the NCI EVS REST API (api-evsrest.nci.nih.gov). Its terms page (evs.nci.nih.gov/ftp1/NCI_Thesaurus/ThesaurusTermsofUse.htm, opened) says NCIt is released under **CC BY 4.0**, so those sources carry "CC BY 4.0". I used **only the NCI-authored (P97) definitions**. I did not use the CDISC, ACC/AHA or UBERON alternative definitions, because their own licensing is unclear. NCIt is an NCI/NIH resource, but it is not one of the brief's listed source types, so please confirm it is acceptable.
- **Link format.** All API URLs return JSON, so they open fine for the owner but are not pretty pages. Human-facing equivalents (the MeSH browser and the NCIt browser) were not opened, so they are not cited.

## Blank or omitted fields
- **Internal jugular vein, `details.branches`:** omitted, because no opened source lists its tributaries.
- **Internal jugular vein, `details.territory`:** taken from the MeSH note for the jugular veins as a group ("drain the brain, face and neck"), not from an internal-only definition. The field text says so.
- **Internal jugular vein, central venous catheter use:** not included; there was no allowed source.
- **Inferior vena cava, location:** only the start (L5, right side) and the end (right atrium) are sourced. The passage through the diaphragm and the IVC's position beside the aorta are not, so they are left out.
- **Superior vena cava:** the azygos vein as a tributary is not sourced, so it is left out.
- **Femoral artery:** the continuation as the popliteal artery, the femoral triangle, the pulse point and the adductor hiatus come only from CDISC, UBERON or ACC/AHA definitions in NCIt, so they are left out.
- **Common carotid artery:** no clinical statistic was used.

## Doubts and inferences
- **Femoral artery clinical lines.** The PAD sources (MedlinePlus, NHLBI) speak of arteries to the legs and do not name the femoral artery. The NHLBI catheter lines say "artery in the groin", not "femoral artery". The lines are worded to match the sources, but placing them under the femoral artery is my inference. The US PAD statistic is marked "in the United States".
- **Internal jugular vein clinical lines.** The NCIt definitions of jugular venous distension and JVP say "jugular vein", not "internal jugular vein". The heart_failure link rests on the NCIt heart-failure definition listing jugular venous distension as a sign.
- **Common carotid, ischemic_stroke link.** MedlinePlus says carotid disease can cause a stroke by blocking blood flow (plaque or clot), which is ischemic in mechanism. The page does not use the word "ischemic", so linking ischemic_stroke is my inference.
- **Inferior vena cava, renal veins.** The NCIt definition says the renal veins drain "to the vena cava" without saying "inferior". I listed them as an IVC tributary.
- **Hepatic portal vein, cirrhosis.** No disease id is linked: cirrhosis and portal hypertension have no page in the list.
- **Hepatic portal vein, territory.** NIDDK and the NCI Dictionary list the stomach, intestines, spleen, pancreas and gallbladder. The NCIt P97 definition mentions only the intestines. These do not conflict; the broader list was used.
- **Aliases.** "anterior/cranial vena cava" and "posterior/caudal vena cava" are CDISC synonyms in NCIt, mainly veterinary terms. Drop them if they are unwanted.

## URLs that might not open nicely
- The webapis.cancer.gov, api-evsrest.nci.nih.gov and id.nlm.nih.gov URLs return JSON, not HTML.
- These failed and are not cited: nhlbi.nih.gov/health/carotid-artery-disease (404); the NCI glossary API for jugular-vein, femoral-artery and central-venous-catheter (404).

#### From notes_c.md

# Notes, agent c (batch b01)

Entries: trachea, group:airways, esophagus, stomach, diaphragm. All five pass `--check`.

## Gray's Anatomy was not usable
The PubAnnotation GrayAnatomy source DB holds only 75 docs (embryology and osteology;
e.g. 60 = patella). The respiratory, digestive and muscle chapters are not there
(sourceid 117, 237 and 247 open only the generic index). So no Gray's facts were used,
and the landmark-type facts (blood supply, origin and insertion of the diaphragm,
segmental bronchi) had no allowed source.

## Blank or omitted fields and why
- **trachea**: `blood_supply`, `nerve_supply`, `lymph_drainage` omitted (none of the opened pages give them).
- **group:airways**: `blood_supply`, `lymph_drainage` omitted. No opened page names the
  segmental (tertiary) bronchi or gives the number of segments, so the entry stops at
  "lobar bronchi, then smaller branches". `nerve_supply` gives only the NHLBI autonomic
  effect (parasympathetic narrows, sympathetic widens); no named nerves.
- **esophagus**: `blood_supply` omitted (no source). `nerve_supply` is general
  (brain triggers peristalsis, gut-wall nerves help, from NIDDK); the vagus is not named
  on any opened page. Alias "food pipe" removed: no source used it.
- **stomach**: `blood_supply` omitted (SEER UGI stomach page says nothing on arteries).
  `nerve_supply` is general (enteric nerves, neural and hormonal control); no named nerves.
  Rugae, HCl, pepsinogen and intrinsic factor were not on the pages, so not mentioned.
- **diaphragm**: `origin`, `insertion`, `nerve_supply`, `blood_supply` omitted.
  The phrenic nerve is not named on any allowed page I could open (NHLBI only says
  "nerves in the upper spinal cord"; the NCI Dictionary pages for "diaphragm" and
  "phrenic nerve" showed only navigation). Every search hit for it was StatPearls,
  PMC or Wikipedia, which are banned. Only `action` is filled.

## Doubts and inferences
- Hiatal hernia clinical lines (stomach, diaphragm) are linked to `gerd`. MedlinePlus says
  a hiatal hernia makes acid reflux (GERD) easier, so the link is my inference. Change it to
  `""` if you only want direct disease lines.
- The bronchitis line has id `""`: there is no bronchitis disease page.
- Spelling: "oesophagus/oesophageal" in my own text, to match the manifest display name.
  "GERD" kept as in the disease id and the MedlinePlus page.
- Oesophageal cancer distribution by thirds (10/40/50%) comes from the SEER registrar module.
  It is not marked as US-only on the page.
- The oesophagus `location` uses "about the sixth cervical vertebra". SEER says "6th vertebra",
  and the cervical level is implied by the cricoid. Worth a check.
- Lymph drainage lists for oesophagus and stomach are cut down from SEER's registrar
  "regional lymph nodes" lists. Those lists are for cancer staging, not anatomy, though they
  follow the anatomic drainage.

## URLs
- training.seer.cancer.gov/anatomy/respiratory/passages/trachea.html and
  .../digestive/regions/esophagus.html return 404. The real pages are larynx.html and
  pharynx.html.
- nhlbi.nih.gov/health/lungs/how-lungs-work returns 404. I used the respiratory-system,
  breathing-benefits and body-controls-breathing subpages.
- WebFetch hit a session usage limit partway through. Every cited URL opened successfully
  later (gerd, pepticulcer, acutebronchitis, asthma, ugi/anatomy/layers after retry).

#### From notes_d.md

# Notes, agent d (batch b01)

Entries: liver (group:fma_FMA7197_o), gallbladder, pancreas, spleen, small intestine (group:small_intestine).

## Gray's Anatomy not available for these organs
The PubAnnotation GrayAnatomy collection has only 75 documents (embryology and osteology).
sourceid/248 and /250, where the small intestine and liver would be, redirect to the
PubAnnotation home page. So none of these entries uses Gray's. Arterial supply, nerve
supply and Couinaud segments could not be sourced from the permitted sites; searches
only returned Kenhub, Radiopaedia, PMC and similar sites, which I did not open.

## Blank or omitted fields and why
- All five: `aliases` is []. No source gave an everyday name.
- Liver: `nerve_supply` was omitted (no source). The group is "lobes and segments", but
  only the lobes are covered (right, left, quadrate, caudate). The Couinaud 8 segments
  are not mentioned because no permitted source covered them.
- Gallbladder: `nerve_supply` was omitted. `blood_supply` gives only the venous drainage
  to the portal vein (NIDDK cirrhosis page). The cystic artery is not in any source I opened.
- Pancreas: `nerve_supply` was omitted. `blood_supply` gives only the venous drainage
  to the portal vein.
- Spleen: `nerve_supply` and `lymph_drainage` were omitted (no source). It has 3 clinical
  lines only.
- Small intestine: `lymph_drainage` was omitted. The SEER lymph-node page covers only the
  pancreas and biliary tract. `blood_supply` gives only the venous drainage to the portal
  vein; the superior mesenteric artery is not sourced. It has 3 clinical lines.

## Doubts / judgement calls
- The partial `blood_supply` values (venous drainage only) come from one NIDDK sentence:
  the portal vein carries blood from the stomach, intestines, spleen, gallbladder and
  pancreas to the liver. The owner may prefer to blank these instead.
- Small intestine exam tip: the source says "about 20 feet". The "roughly 6 metres"
  is my own unit conversion.
- Pancreas: the type 2 diabetes link is `type2_diabetes`. The same line also mentions
  type 1 diabetes (MedlinePlus covers both); type 1 has no disease page.
- Spleen: the malaria link is `malaria` (CDC clinical features: enlarged spleen; rare
  P. vivax rupture).
- Typhoid fever: the CDC clinical guidance page mentions intestinal perforation and
  bleeding after 2-3 weeks, but it does not say the small intestine. So I left the
  line out rather than infer the site.
- Gallbladder: the clinical line "about 70 percent of gallbladder tumours spread
  directly into the liver" is from the SEER biliary liver page ("invade the liver by
  direct extension").
- Liver: "dual blood supply" is my summary wording of the SEER accessory-organs page,
  which describes two sources (hepatic artery and portal vein).
- Spelling: I wrote British forms ("oesophageal", "haemorrhage", "tumours",
  "metabolises") to match the display name "Oesophagus" in MANIFEST. Change them if
  US spelling is preferred.
- During fetches, the WebFetch summariser twice said a SEER page "contained embedded
  instructions". This looked like my own prompt being echoed back. Nothing on the
  pages was acted on.

## URLs
All opened on the first try. No retries were needed.

#### From notes_e.md

# Notes, agent e (batch b01)

Gray's Anatomy was not usable for these four: the PubAnnotation GrayAnatomy source has
only 75 documents (osteology/embryology). Doc ids 249, 253 and 275 redirect to the
PubAnnotation home page. All facts below come from SEER, NIDDK, MedlinePlus and cancer.gov.

## group:large_intestine
- Blank: `blood_supply` (no opened page names the colic or mesenteric arteries),
  `nerve_supply` (no source).
- `lymph_drainage` is general: nodes along the colon and along the arteries that supply each
  segment (SEER). The EOD Regional Nodes page lists only the general node names; the
  per-segment table appeared in a search snippet, not on the fetched page, so it is not used.
- Alias "colon": MedlinePlus Colonic Diseases says the colon is also called the large
  intestine. Strictly the colon is only one part, so the owner may want to drop it.
- The screening age (45) comes from MedlinePlus, a US page; the line says "in the United States".
- No disease id: none of the allowed ids fits colon disease. acute_appendicitis was left out
  because the appendix has its own entry.

## kidney
- Blank: `nerve_supply`, `lymph_drainage` (no opened source).
- Size: SEER gives 12 x 6 x 3 cm; NIDDK and MedlinePlus say "about the size of a fist". Both are used.
- Nephron count: SEER says "over a million"; NIDDK says "about a million". The text says "about a million".
- The pyelonephritis line links urinary_tract_infection. That link is my choice: MedlinePlus
  lists kidney infection under UTIs.

## urinary bladder
- Blank: `blood_supply`, `nerve_supply`, `lymph_drainage` (no opened source). NIDDK says
  signals go to the brain as the bladder fills but names no nerves.
- The capacity (1.5 to 2 cups) is from NIDDK. SEER gives no capacity.
- SEER describes only the internal urethral sphincter. NIDDK describes both the internal and
  the external sphincters.
- The statistic "sixth most common cancer in the United States" is from MedlinePlus Bladder Cancer.

## pituitary gland
- Blank: `blood_supply`, `lymph_drainage` (no opened source).
- `nerve_supply` is based on SEER: the posterior lobe is controlled by nerve stimulation
  from the hypothalamus, through the infundibulum. SEER does not use the term
  hypothalamo-hypophyseal tract, so the entry does not use it either.
- Location wording differs between sources: NCI says "in the center of the brain, just above
  the back of the nose", MedlinePlus says "base of the brain", and SEER says sella turcica of
  the sphenoid. The plain summary uses the base of the brain and the back of the nose.
- No clinical line names compression of the optic chiasm. MedlinePlus lists vision problems
  as a symptom but gives no mechanism, so the line only says vision problems.
- No disease id is linked. graves_disease was not used: the source says tumors can cause
  hyperthyroidism but does not mention Graves disease.

## URLs
- All URLs opened on the first try.
- cancer.gov PDQ pages can change over time.

#### From notes_f.md

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

#### From notes_g.md

# Notes, agent g (batch b01)

Entries: mandible, group:spine, group:ribcage, clavicle, scapula. All five pass `--check`.

## Blank fields
- **mandible / details.type**: left out. SEER says "some skull bones" are irregular but does not name the mandible, and Gray's doc 44 does not classify it.
- **clavicle / clinical**: left empty. The only clavicle-fracture pages found were MedlinePlus A.D.A.M. pages (`/ency/...`), which are not allowed, and the NIAMS shoulder page returned 404. The MedlinePlus shoulder topic page lists "fractures" and "separations" but does not link them to the clavicle, so I did not use it for a clavicle line.

## Doubts and terminology
- **Vertebra count**: Gray's says 33 vertebrae (counting 5 sacral + 4 coccygeal separately). MedlinePlus says the spine has 26 vertebrae (sacrum and coccyx each counted as one). Both are correct for what they count. The description uses Gray's 33 and explains the fusion.
- **Spine joints**: "lumbosacral" is my modern term for Gray's "sacrovertebral articulation". "Ribs attach to the thoracic vertebrae" is from Gray's docs 26 and 28 (ribs and thoracic vertebrae form the back wall; true ribs connect to the vertebral column).
- **Spine curves**: Gray's calls the pelvic curve "concave downward and forward". I kept that wording.
- **Clavicle**: modern terms "conoid tubercle" (Gray's: coracoid tuberosity) and "trapezoid line" (Gray's: oblique/trapezoid ridge). The joint names "sternoclavicular" and "acromioclavicular" are the standard modern names. Gray's doc 49 describes these articulations and the acromioclavicular ligament but does not use the name "sternoclavicular joint".
- **Clavicle function_plain**: no source states its function outright (e.g. as a strut). I wrote it only from the articulations and the muscle list in Gray's.
- **Scapula**: modern terms used: superior angle (Gray's: medial angle); lateral and medial borders (Gray's: axillary and vertebral); supraspinous and infraspinous fossae (Gray's: "supraspinatous"/"infraspinatous"); suprascapular notch (Gray's: scapular notch). "Glenohumeral" is my modern name for the shoulder joint.
- **Scapula clinical**: the MedlinePlus shoulder page is about the shoulder joint as a whole, not the scapula alone. Saying the humeral head is "larger than its socket" refers to the glenoid cavity. That link is my inference from Gray's doc 50 (glenoid cavity articulates with the humeral head). I did not name the rotator cuff muscles because neither source ties them to that term.
- **Mandible**: "condylar process" is the modern term (Gray's: condyloid process). The TMJ articulation with the temporal bone comes from Gray's; the NIDCR page does not name the bones. The 5% TMD figure is labelled "in the United States".
- **Rib cage type**: "flat" refers to the sternum (Gray's: "long, flat bone"). Gray's did not classify the ribs on the page I read.
- No disease ids were linked; none of the conditions are on the allowed list.

## URLs
- PubAnnotation GrayAnatomy doc 21 redirected to the PubAnnotation home page (it seems not to exist), so it was not used. Doc 23 turned out to be the lumbar vertebrae, so it was not used either; the sacrum is doc 24.
- https://www.niams.nih.gov/health-topics/shoulder-problems returned 404 and was not used.
- All cited URLs opened on the first try.

#### From notes_h.md

# Notes, agent h (batch b01): humerus, radius, ulna, hip bone, patella

All five files pass `--check` (ok). Main source: Gray's 1918 on PubAnnotation, docs 51 (humerus),
52 (ulna), 53 (radius), 57 (hip bone), 60 (patella), and 17 (general classification of bones).
I took the clinical lines from MedlinePlus (arm, shoulder, elbow, wrist, hip) and NIAMS Sports Injuries.

## Blank fields
- radius: `aliases` is empty. Gray's heading gives no everyday name, and no source I opened gave one.
- No other field is blank. Each entry has type, joints and landmarks.

## Terminology changed from 1918 Gray's
- "semilunar notch" (greater sigmoid cavity) became trochlear notch (ulna, humerus).
- "musculospiral / radial sulcus" became radial groove (humerus).
- "navicular" (carpal) became scaphoid (radius, joints).
- "proximal radioulnar joint" (ulna): Gray's describes the radial notch receiving the radial head
  inside the elbow region. I used the modern joint name.

## Doubts and inferences
- Hip bone `type` = "flat": Gray's doc 17 lists the os coxae among flat bones, but doc 57 calls it
  "irregularly shaped". Many modern texts call it irregular. The owner should choose.
- Patella `type` = "sesamoid": Gray's doc 60 says it is usually regarded as sesamoid. Doc 17 notes
  that some authorities call it short or flat.
- Humerus tennis/golfer's elbow lines: NIAMS gives the conditions, and Gray's gives the
  epicondyle attachments of the common extensor and flexor tendons. Linking the two is my own synthesis.
- Humerus line "ulnar nerve runs behind the medial epicondyle" is anatomy rather than a condition.
  It is clinically relevant, but it could move to location/landmarks if the owner prefers.
- Radius wrist-fracture line: MedlinePlus says the wrist is two forearm bones plus carpals and that
  falls on an outstretched hand cause injuries. It does not name the radius (Gray's gives the
  radius-carpal joint), and it does not say distal radius fracture. Colles fracture is not in any source I opened.
- Ulna: the UCL injury (NIAMS) is tied to its attachments on the coronoid process and olecranon (Gray's).
  The olecranon bursa is from Gray's, and bursitis is in MedlinePlus's elbow list. I did not claim
  olecranon bursitis as a named condition.
- Hip bone clinical lines (dysplasia, osteoarthritis) are about the hip joint. That joint includes the acetabulum.
- No disease ids used; none of the allowed ids fit.

## URLs
- https://www.niams.nih.gov/health-topics/knee-problems returned 404 (not used).
- The NIAMS Knee Problems PDF on webharvest.gov downloaded but was unreadable (compressed PDF); not used.
- All cited URLs opened on the first try.

#### From notes_i.md

# Notes, agent i (batch b01)

Entries: tibia, fibula, group:deltoid, biceps brachii, triceps brachii. All five pass `--check`.

## Blank fields and why
- **biceps brachii, clinical: []** and **triceps brachii, clinical: []**. I found no allowed public-domain page
  (MedlinePlus NLM summary, NIH/NIAMS, CDC) with a condition specific to these muscles. MedlinePlus "Arm Injuries
  and Disorders" and NIAMS "Sports Injuries" don't mention biceps or triceps. Search results for biceps tendon
  rupture or tendinitis were all StatPearls/PubMed/PMC, which are off limits. The NIAMS "shoulder-problems" URL returned 404.
- **aliases: []** for all three muscles: no source gave an everyday name.
- **fibula clinical** has only one line (stress fractures, NIAMS). No other allowed source covered the fibula.

## Sources and doubts
- **Gray's muscles and arteries are not on PubAnnotation.** The GrayAnatomy sourcedb holds only 75 docs, all
  osteology. Doc ids 122/123 redirect to the home page. bartleby is 403, and theodora.com returned 403 too. So for
  the three muscles I used the public-domain 1918 scan text on the Internet Archive (item
  `anatomyofhumanbo1918gray`, "Anatomy of the Human Body", Gray/Lewis, 20th ed.). Pages used: Deltoideus pp. 439-440,
  Biceps brachii pp. 443-444, Triceps brachii pp. 444-445, axillary and brachial artery branches pp. 587-592.
  - The cited URL is the mirror that `https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt`
    redirects to (`dn720102.ca.archive.org/...`). The mirror host name may change, so the owner should open the
    archive.org/download URL instead. The file is about 4.7 million characters long. I read it with offsets 1,420,000
    (muscles) and 1,980,000 (arteries).
  - The `archive.org/stream/...` view stops at about page 300, so it does not reach the muscles.
- **Terms modernised from Gray's 1918:**
  - supraglenoid/infraglenoid "tuberosity" -> tubercle
  - "deltoid prominence" -> deltoid tuberosity
  - "lacertus fibrosus" -> bicipital aponeurosis
  - "intercondyloid eminence" -> intercondylar eminence
  - peroneus -> fibularis
  - "posterior/scapular humeral circumflex" -> posterior circumflex humeral / circumflex scapular artery
  - "profunda brachii" kept as is
- **Deltoid part names:** Gray's describes anterior, middle (acromial) and posterior fibres. I mapped them to the
  manifest's TA names, clavicular, acromial and spinal parts, by their origins. That mapping is mine, not quoted.
- **Deltoid blood supply:** Gray's names several arteries, so I listed them all. The thoracoacromial (deltoid and
  acromial branches) and the posterior circumflex humeral are the main ones. "Main" is my wording.
- **Muscle actions:** Gray's says "forearm" (e.g. triceps is the "extensor of the forearm"). I wrote "extensor of the elbow".
- **Deltoid clinical lines** come from the CDC Pink Book. It is US guidance, so I marked it "United States".
- **Tibia clinical line 3** (tibial shaft fractures) rests only on a link title on the MedlinePlus Leg Injuries page.
  The owner may drop it.
- **Fibula function_plain:** "gives attachment to many leg muscles" is my summary of Gray's list of muscles arising
  from the fibula. Gray's says nothing about the fibula bearing weight, so I left weight-bearing out.
- No disease ids were linked. None of the conditions has a page in the list.

## URLs that might not open
- The archive.org mirror URL above (see the first item under "Sources and doubts").
- `https://www.cdc.gov/vaccines/hcp/administration/administer.html` returned 404, so I didn't use it.
  I used the Pink Book chapter instead.

#### From notes_j.md

# Notes, batch b01, agent j

Entries: pectoralis major, trapezius, sternocleidomastoid, group:quadriceps.

## Gray's Anatomy source (applies to all four)
- PubAnnotation's GrayAnatomy collection only holds docs 1-67 (osteology). I listed every doc via
  its JSON listing and probed ids 100-140, 200, 300, 400, 500 and 1000: none exist. It has no myology or angiology.
- I used instead the Internet Archive OCR full text of the 1918 20th edition (Lea & Febiger),
  item `anatomyofhumanbo1918gray`. The stable link is
  https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt, which 302-redirects
  to a mirror host. WebFetch read the mirror URL
  (https://dn720102.ca.archive.org/0/items/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt), so the
  `sources` cite that one. The mirror host name may change. If it fails for the owner, use the
  archive.org/download link. The file is 4.7 MB. The `checked` entries give the WebFetch character offsets I read
  (SCM 1269000, trapezius/pectoralis 1418000, quadriceps 1550000, neck arteries 1847000, transverse
  cervical/thoracoacromial 1963000, lateral femoral circumflex 2124500). Page numbers are in the source titles.
- The site is not on the brief's source list, but the text is the same public-domain 1918 Gray's. The owner may
  want to approve this host.
- The `https://archive.org/stream/...` URL renders only part of the text (about 918k chars), so I didn't use it.

## Terminology changed from 1918
- "anterior thoracic nerves" became the medial and lateral pectoral nerves (Gray's term is kept in brackets).
- "supraspinal ligament" became the supraspinous ligament. "ligamentum patellae" became the patellar ligament.
  "anterior divisions" of cervical nerves became anterior rami.
- Pectoralis insertion: "crest of the greater tubercle" is Gray's term. "(lateral lip of the intertubercular groove)"
  is the modern equivalent I added; Gray's doesn't say it.
- The upper/middle/lower trapezius fibers are labelled descending/transverse/ascending to match the manifest
  part names. Gray's only says superior, middle and inferior fibers.
- Rectus femoris "straight" and "reflected" heads are from Gray's ("anterior or straight", "posterior or reflected").

## Blank fields
- trapezius `aliases`: no source gave an everyday name.
- Every other field is filled for all four entries. The clinical lists are short (1-2 lines) because no allowed
  page covered muscle-specific conditions.

## Doubts / inferences
- sternocleidomastoid and trapezius clinical "neck pain from strained neck muscles": the MedlinePlus page is about
  neck muscles in general and doesn't name either muscle. Linking it to these muscles is my inference. Gray's says
  the trapezius covers the back of the neck, and SEER names both as superficial neck muscles.
- sternocleidomastoid clinical "torticollis": the MeSH note describes the twisted neck and its causes but doesn't
  name the SCM. The link to this muscle is my inference, based on Gray's action (it tilts the head and turns the
  face to the opposite side). I couldn't open the NINDS dystonia page (403). The MedlinePlus torticollis pages are
  A.D.A.M. (ency), so I didn't use them.
- sternocleidomastoid exam tip: SEER explains the name by its attachments (sternum, clavicle, mastoid process).
- pectoralis major clinical line 2 (partial or complete absence) is a congenital variation from Gray's. Drop it if
  the owner thinks it is anatomy, not clinical.
- pectoralis major alias "chest muscle": MedlinePlus Genetics calls it "the main chest muscle".
- quadriceps clinical "patellar tendinitis": MedlinePlus Tendinitis/Knee pages give patellar tendinitis
  (jumper's knee). Calling that tendon the quadriceps' true tendon of insertion comes from Gray's
  (ligamentum patellae). Joining the two is my inference.
- quadriceps blood supply: Gray's (angiology) only says clearly that the lateral femoral circumflex
  descending branch supplies vastus lateralis. I didn't add other arteries.
- No disease ids were linked; none of the allowed ids fit.

## URLs
- NIAMS knee-problems page: 404. The webharvest NIAMS PDF couldn't be read (compressed), so I didn't cite it.
- meshb.nlm.nih.gov records opened fine. MeSH IDs were found with the id.nlm.nih.gov lookup API.

#### From notes_k.md

# Notes, agent k (batch b01)

Entries: group:hamstrings, gluteus maximus, gastrocnemius. All three pass `--check`.

## Blank fields
- gluteus maximus `aliases`: []. No allowed source I opened gives an everyday alias. Gray's says it "forms the prominence of the nates" (the buttock), but that describes the muscle and is not a name for it.
- No other fields are blank. Every muscle `details` key is filled.

## Gray's Anatomy source (important)
- PubAnnotation's GrayAnatomy source has only 75 docs (embryology and osteology). It has no muscle or artery sections; I tried sourceids 129, 130 and 131.
- So I used the 1918 20th edition full OCR text on the Internet Archive (item `anatomyofhumanbo1918gray`).
  - `https://archive.org/download/.../anatomyofhumanbo1918gray_djvu.txt` returns a 302 redirect to `https://dn760101.eu.archive.org/0/items/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt`. That mirror URL is the one I opened and the one I cited.
  - The mirror hostname may change. If it does not open for the owner, the stable URL is `https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt`.
  - The text is about 4.7M characters. Myology pp. 474-483 is at about offset 1,560,000; the angiology of the lower limb, pp. 608-636, is at about offset 2,050,000.
- The `archive.org/stream/...` URL serves only about the first 918k characters, so it does not reach the muscles.
- A search result offered hithera.com as a copy of Gray's. Its figure numbers (648, 649) suggest a later, possibly copyrighted edition, so I did not open or use it.

## 1918 terms I modernised
- nates -> buttock
- Sacrospinalis -> erector spinae
- tendo calcaneus -> calcaneal (Achilles) tendon
- common peroneal -> common fibular (peroneal)
- profunda femoris -> deep femoral (profunda femoris) artery
- iliotibial band -> iliotibial band (iliotibial tract)
- Gray's "extends the foot" -> plantar flexes. SEER uses "plantar flex", so I used that.
- Gray's "flexes the leg" (meaning the knee) is written as "flex the leg at the knee".

## Doubts
- SEER lower-extremity page: as fetched, it says the gluteal muscles as a group "adduct the thigh". This looks like a possible error on the page or in the fetch, since the gluteal group mainly abducts. I did not use it.
- Hamstrings and hip extension: Gray's (as summarised to me) does not state outright that the hamstrings extend the hip. It says they help the gluteus maximus restore the erect posture after stooping, so I wrote only that. The owner may want to add hip extension from another source.
- Hamstrings `nerve_supply`: Gray's gives L4-S3 for the group. I say they come from sciatic nerve branches (tibial and common fibular). Gray's names the tibial and common peroneal nerves, and the sciatic is the parent nerve, but Gray's did not say "sciatic" in the passage I read. That part is standard anatomy rather than a quoted fact.
- Gluteus maximus `description`: "Its name means the large gluteal muscle" comes from SEER's naming list ("maximus (large)"). I did not claim "largest muscle in the body", because no opened source said it.
- Gastrocnemius `exam_tip`: NIAMS says the Achilles is the "largest tendon in the body", and Gray's says "thickest and strongest". Both are cited, and they don't conflict.
- Gluteus maximus clinical line 3 comes from a 2002 ACIP document (MMWR rr5102a1), so it is labelled as older guidance. I left the disease id blank: the line is about where the injection is given, not about the disease. Linking `rabies` or `hepatitis_b` would be my own inference.
- Nothing I fetched gave a hamstring-specific treatment. The strain treatment line is general advice for all strains on MedlinePlus Sprains and Strains, applied here to hamstring strains.

#### From notes_pilot.md

# Notes: pilot agent, batch b01 (femur, appendix)

## femur
Blank fields: none. `aliases` = ["thigh bone"] (Gray's heading and MedlinePlus).

Doubts:
- Gray's 1918 text came from PubAnnotation (https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/59),
  not bartleby. The page carries the Gray's femur text (same wording and figure numbers 244/245) but does
  not itself state the edition or year. I labelled it "20th ed. (1918)" and "Public domain" on that basis;
  the owner may want to confirm that the PubAnnotation GrayAnatomy source is the 1918 edition.
- Gray's on that page does not say outright "forms the hip joint"; it says weight passes from the acetabulum
  to the head and the hip-joint capsule attaches to the neck. "Ball-and-socket" and "femur meets the pelvis"
  come from MedlinePlus Hip Injuries. The knee articulations (tibial condyles and menisci, patella) are from Gray's.
- Clinical line 1 (neck-shaft angle) is an anatomy fact rather than a disease line; kept because Gray's
  gives it and it matters for hip problems. Clinical line 2 is about hip fractures in general (MedlinePlus),
  not femoral-neck fractures specifically; no source opened named the femoral neck as the fracture site.
- The NCI Dictionary pages for "femur" (/def/femur and /def/467871) loaded only navigation, no definition,
  so they are not cited.
- MedlinePlus "Leg Injuries and Disorders" (legsinjuriesanddisorders.html) returned 404; not used.

## appendix
Blank fields: `aliases` ([]: no everyday name besides "appendix" in the sources), `details.blood_supply`,
`details.nerve_supply`, `details.lymph_drainage` (no allowed page opened gave the appendicular artery,
nerves or lymph nodes; the SEER colorectal anatomy page does not cover them, and the Gray's text was not
available on PubAnnotation for the large intestine).

Doubts:
- `functions` = "No known function." (MedlinePlus). Some literature proposes an immune role, but no allowed
  source I opened says so, so it is not mentioned.
- All four clinical lines link `acute_appendicitis`; this is direct (each line is about appendicitis).
- The "most common cause of acute abdominal pain needing surgery" and "5 to 9 of every 100 people" figures
  are US figures (NIDDK); the text says "in the United States" for the first; the exam tip does not say
  US explicitly.
- The SEER "Small & Large Intestine" anatomy page does not mention the appendix; it is cited only for the
  ileocecal valve/junction in `location`.
- NCI Dictionary "appendix" page loaded only navigation; not cited.

## URLs
All cited URLs opened on the first try.

---

## Heart  (`group:fma_FMA7088_o`)

*group · organ · cardiovascular · 22 FMA ids · covers: anterior cusp of aortic valve, anterior cusp of pulmonary valve, anterior leaflet of mitral valve, anterior leaflet of tricuspid valve, anterior papillary muscle of ventricle, anterolateral head of lateral papillary muscle of ventricle, cavity of atrium, cavity of ventricle …*

**Summary (plain)**

The heart is a hollow, muscular organ about the size of a closed fist. It sits in the middle of the chest near the lungs, with most of it slightly to the left.

**What it does (plain)**

It pumps blood all the time, sending blood to the lungs to pick up oxygen and then out to every part of the body.

**For students: description**

The heart is a four-chambered muscular pump. The thin-walled right and left atria receive blood from veins; the thick-walled right and left ventricles pump it out, the right side to the lungs and the left side to the body, and a wall of tissue (septum) separates the two sides. Four valves (tricuspid, mitral, pulmonary and aortic) keep blood moving one way. The wall has three layers (endocardium, myocardium, epicardium) inside the pericardial sac.

**Location & neighbours**

In the center of the chest, close to the lungs, with about two-thirds of its mass to the left of the midline. It lies inside a protective, fluid-containing sac, the pericardium.

| Detail | |
|---|---|
| Main functions | Pumps about 5 liters of blood a minute in a normal adult. The right ventricle drives the pulmonary circuit to the lungs; the left ventricle drives the systemic circuit. The SA node in the right atrium starts each beat; the signal passes through the AV node to the ventricles. |
| Blood supply | The right and left coronary arteries, branches of the ascending aorta, supply the heart wall. Cardiac veins drain it, mostly into the coronary sinus, which opens into the right atrium. |
| Nerve supply | Heart rate is adjusted mainly by the cardiac center in the medulla oblongata, which has sympathetic and parasympathetic components; without nerve input the SA node fires about 70 to 80 times a minute. |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Coronary artery disease, plaque buildup (atherosclerosis) in the coronary arteries, is the most common heart disease in the United States and can cause angina, heart attack and heart failure.  → disease page `acute_coronary_syndrome`
- Heart failure means the heart cannot pump enough blood to meet the body's needs.  → disease page `heart_failure`
- Valve disease causes leaking (regurgitation) or narrowing (stenosis); aortic stenosis is a common type, and prolapse, most often of the mitral valve, a common cause of leaking.
- Untreated strep throat can lead to rheumatic fever, which can damage the heart valves years later.  → disease page `rheumatic_fever`
- Tetralogy of Fallot, the most common complex congenital heart defect, combines pulmonary stenosis, a ventricular septal defect, an overriding aorta and right ventricular hypertrophy.

**Exam tip**

Valve closure makes the heart sounds: the atrioventricular valves close first (lub), then the aortic and pulmonary valves (dub). Abnormal heart sounds are called murmurs.

**Sources**

- [Structure of the Heart - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html) (Public domain)
- [Heart - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/heart/) (Public domain)
- [Physiology of the Heart - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/heart/physiology.html) (Public domain)
- [Circulatory Pathways - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html) (Public domain)
- [How the Heart Works: Heart Anatomy - NHLBI](https://www.nhlbi.nih.gov/health/heart/anatomy) (Public domain)
- [How the Heart Works: Blood Flow - NHLBI](https://www.nhlbi.nih.gov/health/heart/blood-flow) (Public domain)
- [How the Heart Works: How the Heart Beats - NHLBI](https://www.nhlbi.nih.gov/health/heart/heart-beats) (Public domain)
- [Coronary Artery Disease - MedlinePlus (NLM)](https://medlineplus.gov/coronaryarterydisease.html) (Public domain)
- [Heart Valve Diseases - MedlinePlus (NLM)](https://medlineplus.gov/heartvalvediseases.html) (Public domain)
- [Congenital Heart Defects: Types - NHLBI](https://www.nhlbi.nih.gov/health/congenital-heart-defects/types) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html: Four-chambered muscular organ shaped and sized roughly like a closed fist; two-thirds of mass left of midline; pericardial sac; wall = epicardium, myocardium, endocardium; atria thin-walled receive blood, ventricles thick-walled pump; tricuspid and bicuspid (mitral) AV valves; pulmonary and aortic semilunar valves; right and left coronary arteries from ascending aorta; cardiac veins drain to coronary sinus, which opens into right atrium.
- https://training.seer.cancer.gov/anatomy/cardiovascular/heart/: Normal adult heart pumps about 5 liters of blood every minute.
- https://training.seer.cancer.gov/anatomy/cardiovascular/heart/physiology.html: SA node is the pacemaker, fires 70 to 80 times per minute without neural input; AV node, AV bundle, bundle branches; cardiac center in medulla oblongata with sympathetic and parasympathetic components mediates most rate changes; heart sounds from valve closure; abnormal sounds are murmurs.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html: Right ventricle is the pump for the pulmonary circuit, carrying oxygen-poor blood to the lungs; blood returns to the left atrium.
- https://www.nhlbi.nih.gov/health/heart/anatomy: Heart in the center of the chest near the lungs; four hollow chambers; atria receive, ventricles pump to lungs and body; septum divides right and left sides; endocardium, myocardium, pericardium with fluid reducing friction.
- https://www.nhlbi.nih.gov/health/heart/blood-flow: Tricuspid, mitral, pulmonary and aortic valves and their positions; coronary arteries branch from the aorta and supply heart muscle.
- https://www.nhlbi.nih.gov/health/heart/heart-beats: Signal starts in SA node in the right atrium, passes to AV node between atria and ventricles; lub from AV valves closing, dub from aortic and pulmonary valves closing.
- https://medlineplus.gov/coronaryarterydisease.html: CAD most common type of heart disease in the United States; plaque buildup (atherosclerosis) in coronary arteries; can lead to angina, heart attack, heart failure (heart cannot pump enough blood to meet the body's needs), arrhythmia.
- https://medlineplus.gov/heartvalvediseases.html: Regurgitation and stenosis; prolapse a common cause, most often mitral; aortic valve stenosis a common type; untreated strep throat can become rheumatic fever, which can harm valves; damage may take years.
- https://www.nhlbi.nih.gov/health/congenital-heart-defects/types: Tetralogy of Fallot is the most common complex congenital heart disorder: pulmonary stenosis, large VSD, overriding aorta, right ventricular hypertrophy.

---

## Trachea  (`trachea`)

*part · organ · respiratory · 1 FMA ids · covers: trachea*

**Also called:** windpipe

**Summary (plain)**

The trachea, or windpipe, is the main air tube to the lungs. It runs down from the voice box in the neck into the chest.

**What it does (plain)**

It carries air down to the lungs when you breathe in and carries used air back out when you breathe out.

**For students: description**

The trachea is the main airway leading to the lungs. Hyaline cartilage in its wall holds it open so it does not collapse, while its back wall is soft. It is lined with ciliated pseudostratified columnar epithelium; goblet cells make mucus that traps dust and germs, and cilia sweep the mucus upward to be swallowed or coughed out.

**Location & neighbours**

In the neck and chest, continuing down from the larynx (voice box). The oesophagus lies directly behind it. At about the level of the fifth thoracic vertebra, in the mediastinum, it divides into the right and left main bronchi.

| Detail | |
|---|---|
| Main functions | Conducts air between the larynx and the main bronchi; its mucus and cilia trap and clear inhaled particles and microorganisms. |
| Blood supply | *(blank)* |
| Nerve supply | *(blank)* |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Trachea problems include narrowing (stenosis), inflammation and some inherited conditions.
- A tracheostomy may help breathing in people with swallowing problems, blocked airways or poor coughing, and in critical care patients who need a breathing machine.

**Exam tip**

Its soft back wall lets the oesophagus, which lies right behind it, expand when food is swallowed.

**Sources**

- [Larynx & Trachea - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/respiratory/passages/larynx.html) (Public domain)
- [Bronchi, Bronchial Tree, & Lungs - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/respiratory/passages/bronchi.html) (Public domain)
- [Tracheal Disorders - MedlinePlus (NLM)](https://medlineplus.gov/trachealdisorders.html) (Public domain)
- [How the Lungs Work: What Breathing Does for the Body - NHLBI](https://www.nhlbi.nih.gov/health/lungs/breathing-benefits) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/respiratory/passages/larynx.html: Trachea commonly called windpipe, main airway to the lungs; divides into right and left bronchi at level of fifth thoracic vertebra; hyaline cartilage in wall keeps it from collapsing; soft posterior tissue lets the esophagus, immediately posterior, expand; lined with ciliated pseudostratified columnar epithelium; goblet cells make mucus that traps particles and microorganisms; cilia move mucus upward to be swallowed or expelled; larynx is the air passage between pharynx above and trachea below.
- https://training.seer.cancer.gov/anatomy/respiratory/passages/bronchi.html: Trachea divides into right and left primary bronchi in the mediastinum at the level of the fifth thoracic vertebra.
- https://medlineplus.gov/trachealdisorders.html: Trachea (windpipe) is part of the airway system; airways carry oxygen-rich air to the lungs and carbon dioxide out; windpipe splits into two bronchi; problems include narrowing, inflammation and some inherited conditions; tracheostomy may help breathing with swallowing problems, conditions affecting coughing or blocked airways, or in critical care on a breathing machine.
- https://www.nhlbi.nih.gov/health/lungs/breathing-benefits: On inhaling, air travels down the trachea through the bronchial tubes to the alveoli; on exhaling, carbon dioxide-rich air flows out through the windpipe.

---

## Bronchial tree  (`group:airways`)

*group · organ · respiratory · 22 FMA ids · covers: anterior basal segmental bronchial tree, anterior segmental bronchial tree, apical segmental bronchial tree, inferior lingular bronchial tree, lateral basal segmental bronchial tree, lateral segmental bronchial tree, main bronchus, main bronchus proper …*

**Also called:** bronchial tubes, bronchi

**Summary (plain)**

The bronchial tree is the set of branching air tubes inside the chest. It starts where the windpipe splits in two and keeps dividing into smaller tubes inside each lung.

**What it does (plain)**

It carries air from the windpipe deep into the lungs, down to the tiny air sacs where oxygen enters the blood.

**For students: description**

The trachea divides into the right and left main (primary) bronchi, which have cartilage and a lining like the trachea. Inside the lungs they keep branching: each lobe gets its own lobar (secondary) bronchus, and the branches become smaller and smaller, ending as bronchioles and then alveoli. As the tubes narrow, cartilage in the wall decreases and smooth muscle increases.

**Location & neighbours**

In the chest. The split of the trachea lies in the mediastinum at about the fifth thoracic vertebra; the bronchi enter each lung at the hilum on its medial side. The right lung has three lobes and the left lung two.

| Detail | |
|---|---|
| Main functions | Conducts air to and from the alveoli, where gas exchange happens. Cartilage rings help keep the larger tubes open. |
| Blood supply | *(blank)* |
| Nerve supply | Autonomic: parasympathetic signals narrow the bronchial tubes; sympathetic signals widen them. |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Inflammation of the bronchial tubes (bronchitis) is most often caused by cold and flu viruses and gives a cough with mucus, wheezing and chest tightness.
- In asthma the airways become swollen and tight, causing wheezing, coughing, chest tightness and shortness of breath; attacks can be life-threatening.  → disease page `asthma`

**Exam tip**

Cartilage fades out as the bronchi branch and is absent in the smallest bronchioles, while smooth muscle increases.

**Sources**

- [Bronchi, Bronchial Tree, & Lungs - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/respiratory/passages/bronchi.html) (Public domain)
- [How the Lungs Work: The Respiratory System - NHLBI](https://www.nhlbi.nih.gov/health/lungs/respiratory-system) (Public domain)
- [How the Lungs Work: How Your Body Controls Breathing - NHLBI](https://www.nhlbi.nih.gov/health/lungs/body-controls-breathing) (Public domain)
- [Acute Bronchitis - MedlinePlus (NLM)](https://medlineplus.gov/acutebronchitis.html) (Public domain)
- [Asthma - MedlinePlus (NLM)](https://medlineplus.gov/asthma.html) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/respiratory/passages/bronchi.html: Trachea divides into right and left primary bronchi in the mediastinum at fifth thoracic vertebra; primary bronchi have cartilage and mucous membrane similar to trachea; each lobe supplied by one secondary bronchus; branching continues, hyaline cartilage decreases and is absent in smallest bronchioles while smooth muscle increases; terminate in alveoli; bronchi enter lung at the hilum on medial side; right lung three lobes, left lung two lobes.
- https://www.nhlbi.nih.gov/health/lungs/respiratory-system: Bronchial tubes (bronchi) are two tubes branching off the trachea carrying air to the lungs; inside the lungs they branch into thousands of thinner bronchioles ending in alveoli; cartilage rings support airways and keep bronchial tubes open; right lung three lobes, left lung two.
- https://www.nhlbi.nih.gov/health/lungs/body-controls-breathing: Parasympathetic system narrows the bronchial tubes; sympathetic system widens them.
- https://medlineplus.gov/acutebronchitis.html: Bronchitis is inflammation of the bronchial tubes; viruses causing colds and flu are the most common cause; symptoms cough with mucus, shortness of breath, wheezing, low fever, chest tightness.
- https://medlineplus.gov/asthma.html: Asthma is a long-term lung disease; airways become swollen and tight; symptoms chest tightness, coughing, shortness of breath, wheezing; attacks can be life-threatening.

---

## Oesophagus  (`esophagus`)

*part · organ · digestive · 1 FMA ids · covers: esophagus*

**Summary (plain)**

The oesophagus is a muscular tube about 25 cm long that runs from the throat down through the chest to the stomach.

**What it does (plain)**

It moves swallowed food and drink down to the stomach by waves of muscle squeezing, without digesting it.

**For students: description**

The oesophagus is a collapsible muscular tube linking the pharynx to the stomach. Its wall has a mucosa, submucosa, muscularis and an outer adventitia; it has no serosa. The muscle is striated in the upper third, mixed in the middle third and smooth in the lower third. Upper and lower oesophageal sphincters control food entering and leaving it.

**Location & neighbours**

Begins at the lower end of the pharynx (about the sixth cervical vertebra, lower border of the cricoid cartilage), descends through the mediastinum behind the trachea and heart and in front of the vertebral column, then passes through the oesophageal hiatus of the diaphragm to join the stomach.

| Detail | |
|---|---|
| Main functions | Carries food from the pharynx to the stomach by peristalsis; glands in its lining make mucus that lubricates the passage. No digestive juices are added. The lower oesophageal sphincter relaxes to let food in and stays closed to stop stomach contents flowing back. |
| Blood supply | *(blank)* |
| Nerve supply | Swallowing becomes automatic once started: the brain signals the oesophageal muscles to begin peristalsis, helped by nerves in the gut wall. |
| Lymph drainage | Cervical part: deep cervical (internal jugular), supraclavicular and paratracheal nodes. Upper and middle thoracic: tracheobronchial, carinal, hilar, posterior mediastinal and periesophageal nodes. Lower thoracic: left gastric, cardial and perigastric nodes. |

**Clinical relevance**

- GERD, where stomach acid flows back into the oesophagus, is its most common problem; it can happen when the muscle at the lower end is weak or relaxes at the wrong time.  → disease page `gerd`
- Long-term GERD can inflame and scar the oesophagus and change its lining (Barrett's oesophagus).  → disease page `gerd`
- In achalasia the lower oesophageal muscle does not relax properly, causing trouble swallowing.
- About half of oesophageal cancers arise in the lower third, 40% in the middle third and 10% in the upper third.

**Exam tip**

The oesophagus has no serosa; its outer layer is adventitia, connective tissue that blends with nearby structures.

**Sources**

- [Anatomy of the Esophagus - NCI SEER Training Modules](https://training.seer.cancer.gov/ugi/anatomy/esophagus.html) (Public domain)
- [Layers of the UGI Organs - NCI SEER Training Modules](https://training.seer.cancer.gov/ugi/anatomy/layers.html) (Public domain)
- [Regional Lymph Nodes - NCI SEER Training Modules](https://training.seer.cancer.gov/ugi/anatomy/lymph-nodes.html) (Public domain)
- [Pharynx & Esophagus - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/pharynx.html) (Public domain)
- [Your Digestive System & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works) (Public domain)
- [Esophagus Disorders - MedlinePlus (NLM)](https://medlineplus.gov/esophagusdisorders.html) (Public domain)
- [GERD - MedlinePlus (NLM)](https://medlineplus.gov/gerd.html) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/ugi/anatomy/esophagus.html: Muscular tube about 10 inches (25 cm) from hypopharynx to stomach; posterior to trachea and heart; passes through mediastinum and the hiatus in the diaphragm; no serosal layer, surrounded by adventitia; cervical part begins at level of 6th vertebra or lower border of cricoid; upper third 10%, middle 40%, lower third 50% of esophageal cancers.
- https://training.seer.cancer.gov/ugi/anatomy/layers.html: Four layers mucosa, submucosa, muscularis, adventitia; striated muscle upper third, striated and smooth middle third, smooth lower third; adventitia merges with surrounding connective tissue.
- https://training.seer.cancer.gov/ugi/anatomy/lymph-nodes.html: Regional nodes: cervical - superior mediastinal, anterior deep cervical (internal jugular), supraclavicular, lowest paratracheal, periesophageal; upper/middle thoracic - tracheobronchial, peritracheal, carinal, hilar, posterior mediastinal, periesophageal; lower thoracic - left gastric, cardial, perigastric, posterior mediastinal.
- https://training.seer.cancer.gov/anatomy/digestive/regions/pharynx.html: Collapsible muscular tube between pharynx and stomach; behind trachea and in front of vertebral column; passes through esophageal hiatus of diaphragm; mucosal glands secrete lubricating mucus; upper and lower esophageal sphincters; lower sometimes called cardiac sphincter at esophagogastric junction.
- https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works: Esophagus connects mouth to stomach; after swallowing starts the brain signals esophageal muscles and peristalsis begins; no digestive juices added; lower esophageal sphincter relaxes to let food into stomach and normally stays closed to prevent backflow; nerves and brain control the movements.
- https://medlineplus.gov/esophagusdisorders.html: Esophagus is the tube moving food from mouth to stomach; GERD most common esophagus problem; Barrett's esophagus; achalasia, lower esophageal muscle does not relax properly; esophageal cancer.
- https://medlineplus.gov/gerd.html: GERD when the muscle at the end of the esophagus does not close properly, becomes weak or relaxes at the wrong time; untreated can cause inflammation, scarring and Barrett's esophagus.

---

## Stomach  (`stomach`)

*part · organ · digestive · 1 FMA ids · covers: stomach*

**Summary (plain)**

The stomach is a hollow, muscular organ in the upper left part of the belly, just under the diaphragm. It sits between the food pipe and the small intestine.

**What it does (plain)**

It stores swallowed food, mixes it with acid and digestive juices, and slowly passes the mixture on to the small intestine.

**For students: description**

The stomach has four parts: the cardia around the opening from the oesophagus, the fundus above it, the central body and the lower pyloric antrum. Its lining has gastric glands with mucous, parietal, chief and endocrine cells; the endocrine cells release the hormone gastrin. Three smooth muscle layers (longitudinal, circular and oblique) churn food into chyme.

**Location & neighbours**

In the upper abdomen, just below the diaphragm, mostly left of the midline and partly under the liver. The lesser curvature faces right and the greater curvature left. It joins the duodenum at the pylorus; the greater omentum links it to the transverse colon, spleen and diaphragm.

| Detail | |
|---|---|
| Main functions | Stores food, mixes it with acid and enzymes (protein digestion begins here) and empties chyme into the duodenum through the pyloric sphincter. Lining cells release hormones that control digestion and signal hunger or fullness. Gastric secretion has cephalic, gastric and intestinal phases. |
| Blood supply | *(blank)* |
| Nerve supply | Enteric nerves in the stomach wall control muscle contractions and speed up or slow food movement and digestive juice production; secretion is also under neural and hormonal control. |
| Lymph drainage | Perigastric nodes along the lesser curvature (left gastric, cardial) and greater curvature (gastroepiploic, pyloric, gastroduodenal), splenic hilar and peripancreatic nodes, then celiac and hepatic nodes. |

**Clinical relevance**

- A peptic ulcer is a sore in the lining of the stomach or duodenum, most often caused by Helicobacter pylori infection or long-term NSAID use; burning stomach pain is the usual symptom.  → disease page `peptic_ulcer_disease`
- A hiatal hernia is when the top of the stomach pushes up through the opening in the diaphragm, making acid reflux (GERD) more likely.  → disease page `gerd`
- Indigestion and heartburn are common stomach problems; blood in the stool, severe belly pain or ongoing vomiting need medical attention.

**Exam tip**

The stomach wall has three smooth muscle layers: outer longitudinal, middle circular and inner oblique.

**Sources**

- [Anatomy of the Stomach - NCI SEER Training Modules](https://training.seer.cancer.gov/ugi/anatomy/stomach.html) (Public domain)
- [Stomach - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/stomach.html) (Public domain)
- [Layers of the UGI Organs - NCI SEER Training Modules](https://training.seer.cancer.gov/ugi/anatomy/layers.html) (Public domain)
- [Regional Lymph Nodes - NCI SEER Training Modules](https://training.seer.cancer.gov/ugi/anatomy/lymph-nodes.html) (Public domain)
- [Your Digestive System & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works) (Public domain)
- [Stomach Disorders - MedlinePlus (NLM)](https://medlineplus.gov/stomachdisorders.html) (Public domain)
- [Peptic Ulcer - MedlinePlus (NLM)](https://medlineplus.gov/pepticulcer.html) (Public domain)
- [Hiatal Hernia - MedlinePlus (NLM)](https://medlineplus.gov/hiatalhernia.html) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/ugi/anatomy/stomach.html: Lies just below diaphragm in upper abdominal cavity, mainly left of midline under part of liver; lesser omentum suspends it; greater omentum attaches it to transverse colon, spleen and diaphragm; connects to duodenum at pylorus; cardia surrounds cardioesophageal junction; fundus upper-left above cardiac orifice; body central; pyloric antrum distal; pyloric sphincter regulates chyme into duodenum.
- https://training.seer.cancer.gov/anatomy/digestive/regions/stomach.html: Receives food from esophagus; upper left quadrant; lesser curvature on right, greater on left; simple columnar mucosa with gastric glands; mucous, parietal, chief and endocrine cells; endocrine cells secrete gastrin; neural and hormonal regulation in cephalic, gastric and intestinal phases; pyloric sphincter relaxation lets chyme pass.
- https://training.seer.cancer.gov/ugi/anatomy/layers.html: Stomach wall includes serosa, muscularis, submucosa, mucosa; muscularis has three smooth muscle layers, outer longitudinal, middle circular, inner oblique, which mix contents into chyme and move it into the duodenum.
- https://training.seer.cancer.gov/ugi/anatomy/lymph-nodes.html: Stomach regional nodes: greater curvature, gastroepiploic, gastroduodenal, pyloric; splenic hilar, peripancreatic; lesser curvature, left gastric, cardial; perigastric; celiac; hepatic.
- https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works: Stomach between esophagus and small intestine; muscles mix food with digestive juices; glands make acid and enzymes that break down food including proteins; empties chyme into small intestine; lining cells release hormones, hunger/fullness signals; enteric nerves in wall speed or slow food movement and juice production.
- https://medlineplus.gov/stomachdisorders.html: Organ between esophagus and small intestine; protein digestion begins there; stores food, mixes with acids, sends mixture to small intestine; indigestion and heartburn common; see a doctor for blood in bowel movement, severe abdominal pain, ongoing vomiting.
- https://medlineplus.gov/pepticulcer.html: Peptic ulcer is a sore in the lining of the stomach or duodenum; burning stomach pain most common symptom; most common cause H. pylori; long-term NSAIDs another cause.
- https://medlineplus.gov/hiatalhernia.html: Hiatal hernia when top of the stomach pushes up through an opening in the diaphragm; makes it easier for acid to come up, GERD.

---

## Liver  (`group:fma_FMA7197_o`)

*group · organ · digestive · 19 FMA ids · covers: anterior inferior tributary of hepatic biliary tree, anterior superior tributary of hepatic biliary tree, caudate lobe of liver, caudate lobe tributary of hepatic biliary tree, hepatic duct, hepatovenous segment ii, hepatovenous segment iii, hepatovenous segment iv …*

**Summary (plain)**

The liver is the largest organ inside the body. It sits in the upper right part of the belly, just under the diaphragm.

**What it does (plain)**

It makes bile to help digest fat, stores and processes nutrients from food, and removes harmful substances from the blood.

**For students: description**

The liver is the largest gland in the body. On its surface it shows two large lobes, a larger right and a smaller left, plus two small lobes, the quadrate and caudate. Inside, it is built of lobules, where liver cells (hepatocytes) line blood channels called sinusoids that drain to a central vein. It makes bile, which leaves through the hepatic ducts.

**Location & neighbours**

In the upper abdomen, mostly in the right hypochondriac and epigastric regions, directly beneath the diaphragm. The gallbladder is attached to its under (visceral) surface, and the hepatic artery, portal vein and bile ducts enter or leave at the porta hepatis.

| Detail | |
|---|---|
| Main functions | Makes bile and bile salts; makes plasma proteins; stores nutrients; metabolises carbohydrates, fats and proteins; detoxifies and excretes waste; filters blood, with phagocytic Kupffer cells lining the sinusoids. |
| Blood supply | Dual supply: the common hepatic artery (a branch of the celiac trunk from the abdominal aorta) brings oxygen-rich blood, and the hepatic portal vein brings nutrient-rich blood from the digestive tract, spleen, pancreas and gallbladder. |
| Nerve supply | *(blank)* |
| Lymph drainage | Regional nodes are the hepatic hilar nodes (hepatic and periportal nodes); lymphatic vessels pass through the porta hepatis. |

**Clinical relevance**

- Viruses (hepatitis A, B and C), drugs, toxins, heavy alcohol use, inherited conditions and cancer can all damage the liver; jaundice and abdominal or leg swelling are common signs.
- Chronic hepatitis B can lead to cirrhosis, liver cancer and liver failure; vaccination is the best protection.  → disease page `hepatitis_b`
- In cirrhosis, scar tissue permanently replaces healthy liver tissue; about 1 in 400 adults in the United States are estimated to have it.
- Scarring slows portal blood flow, causing portal hypertension with ascites, oesophageal or gastric varices that can bleed, and hepatic encephalopathy.
- Most people who develop liver cancer already have cirrhosis.

**Exam tip**

The liver has a dual blood supply: oxygen-rich blood from the hepatic artery and nutrient-rich blood from the hepatic portal vein.

**Sources**

- [Accessory Organs of the Digestive System - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html) (Public domain)
- [Anatomy of the Liver & Gallbladder - NCI SEER Training Modules](https://training.seer.cancer.gov/biliary/anatomy/liver.html) (Public domain)
- [Regional Lymph Nodes (Biliary) - NCI SEER Training Modules](https://training.seer.cancer.gov/biliary/anatomy/lymph-nodes.html) (Public domain)
- [Your Digestive System & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works) (Public domain)
- [Liver Diseases - MedlinePlus (NLM)](https://medlineplus.gov/liverdiseases.html) (Public domain)
- [Hepatitis B - MedlinePlus (NLM)](https://medlineplus.gov/hepatitisb.html) (Public domain)
- [Definition & Facts for Cirrhosis - NIDDK](https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html: Largest gland in the body; mainly in right hypochondriac and epigastric regions just under the diaphragm; two major and two smaller lobes visible on the surface; lobules with sinusoids draining to central vein; hepatocytes; Kupffer cells line sinusoids; common hepatic artery from celiac trunk of abdominal aorta brings oxygenated blood; hepatic portal vein brings nutrient-rich blood from digestive tract; functions: secretion, bile salt synthesis, plasma protein synthesis, storage, detoxification, excretion, carbohydrate/lipid/protein metabolism, filtering; gallbladder attached to visceral surface of liver.
- https://training.seer.cancer.gov/biliary/anatomy/liver.html: Largest internal organ; right (larger) and left lobes; quadrate and caudate lobes, round and falciform ligaments labelled; porta hepatis contains hepatic artery, portal vein, lymphatics and extrahepatic bile ducts; produces bile; right and left hepatic ducts join to form common hepatic duct.
- https://training.seer.cancer.gov/biliary/anatomy/lymph-nodes.html: Liver regional lymph nodes: hepatic hilar (hepatic, periportal).
- https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works: Liver makes bile that helps digest fats and some vitamins; receives nutrients from the digestive tract and stores, processes and delivers them to the body.
- https://medlineplus.gov/liverdiseases.html: Liver is the largest organ inside the body; helps digest food, store energy and remove toxins; liver disease from hepatitis A, B, C viruses, drugs, toxins, heavy alcohol use, cancer, inherited conditions (hemochromatosis, Wilson disease); signs include abdominal and leg swelling, easy bruising, jaundice.
- https://medlineplus.gov/hepatitisb.html: Hepatitis B is a viral infection causing liver inflammation; chronic infection can lead to cirrhosis, liver cancer and liver failure; vaccine is the best protection.
- https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts: Cirrhosis: liver scarred and permanently damaged, scar tissue replaces healthy tissue; about 1 in 400 US adults; portal vein carries blood from stomach, intestines, spleen, gallbladder and pancreas to the liver; portal hypertension leading to ascites, edema, varices in esophagus/stomach/intestines that can bleed, hepatic encephalopathy; most people who develop liver cancer already have cirrhosis.

---

## Gallbladder  (`gallbladder`)

*part · organ · digestive · 1 FMA ids · covers: gallbladder*

**Summary (plain)**

The gallbladder is a small, pear-shaped pouch tucked under the liver in the upper right part of the belly.

**What it does (plain)**

It stores bile made by the liver and squeezes it into the small intestine during a meal to help digest fat.

**For students: description**

The gallbladder is a pear-shaped sac on the under (visceral) surface of the liver. It has a fundus (the wide end), a body and a neck that narrows into the cystic duct. Its main job is to store bile, a yellow-green fluid of water, bile salts, bile pigments and cholesterol. Bile salts break fat into small droplets so it can be digested.

**Location & neighbours**

Upper right abdomen, under the liver and attached to its visceral surface. The cystic duct joins the common hepatic duct to form the common bile duct, which carries bile to the duodenum.

| Detail | |
|---|---|
| Main functions | Stores bile between meals and releases it into the duodenum after eating. Its wall has a mucosa, lamina propria, smooth muscle and serosa; there is no serosa where it lies against the liver. |
| Blood supply | Its venous blood goes to the liver through the portal vein. |
| Nerve supply | *(blank)* |
| Lymph drainage | Regional nodes include the cystic duct, pericholedochal, hepatic hilar, periportal, periduodenal, peripancreatic, celiac and superior mesenteric nodes, and the node of the foramen of Winslow. |

**Clinical relevance**

- Gallstones are hard deposits, usually of cholesterol or bilirubin; they affect about 10 to 15 percent of people in the United States.
- Most gallstones are 'silent', but a stone blocking a bile duct causes sudden upper right abdominal pain (biliary colic).
- Gallstones can cause inflammation of the gallbladder, infection of the bile ducts or liver, and gallstone pancreatitis.
- Removing the gallbladder (cholecystectomy) treats many gallbladder problems; people can live without it.
- Gallbladder cancer is rare; about 70 percent of gallbladder tumours spread directly into the liver.

**Exam tip**

The cystic duct from the gallbladder joins the common hepatic duct to form the common bile duct.

**Sources**

- [Accessory Organs of the Digestive System - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html) (Public domain)
- [Anatomy of the Liver & Gallbladder - NCI SEER Training Modules](https://training.seer.cancer.gov/biliary/anatomy/liver.html) (Public domain)
- [Regional Lymph Nodes (Biliary) - NCI SEER Training Modules](https://training.seer.cancer.gov/biliary/anatomy/lymph-nodes.html) (Public domain)
- [Gallbladder Diseases - MedlinePlus (NLM)](https://medlineplus.gov/gallbladderdiseases.html) (Public domain)
- [Definition & Facts for Gallstones - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/gallstones/definition-facts) (Public domain)
- [Your Digestive System & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works) (Public domain)
- [Definition & Facts for Cirrhosis - NIDDK](https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html: Gallbladder is a pear-shaped sac attached to the visceral surface of the liver by the cystic duct; principal function is storing bile; bile is yellowish-green, made of water, bile salts, bile pigments and cholesterol; bile salts emulsify fats.
- https://training.seer.cancer.gov/biliary/anatomy/liver.html: Gallbladder sac-like organ under the liver; fundus, body, neck tapering into cystic duct; wall: mucosa, lamina propria, smooth muscle, serosa (absent on hepatic surface); about 70% of gallbladder tumours invade the liver by direct extension; cystic duct connects common hepatic duct to gallbladder; common bile duct formed by cystic duct and common hepatic duct.
- https://training.seer.cancer.gov/biliary/anatomy/lymph-nodes.html: Gallbladder regional nodes: cystic duct, pericholedochal, hepatic hilar, celiac, periduodenal, periportal, peripancreatic (head), superior mesenteric, node of foramen of Winslow.
- https://medlineplus.gov/gallbladderdiseases.html: Small pear-shaped organ under the liver; stores bile; releases it through the common bile duct to the small intestine; gallstones; gallbladder cancer is rare; cholecystectomy; people can live without a gallbladder.
- https://www.niddk.nih.gov/health-information/digestive-diseases/gallstones/definition-facts: Gallbladder in upper right abdomen under the liver; releases bile into the duodenum after eating; gallstones usually cholesterol or bilirubin; 10-15% of US population; most are silent; blocked bile duct causes sudden upper right abdominal pain (biliary colic); complications: gallbladder inflammation, infection of gallbladder, bile ducts or liver, gallstone pancreatitis.
- https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works: Gallbladder stores bile between meals and squeezes it through the bile ducts into the small intestine when you eat.
- https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts: Portal vein carries blood from the stomach, intestines, spleen, gallbladder and pancreas to the liver.

---

## Pancreas  (`pancreas`)

*part · organ · digestive · 1 FMA ids · covers: pancreas*

**Summary (plain)**

The pancreas is a long, soft gland that lies across the back of the belly, behind the stomach and in front of the spine.

**What it does (plain)**

It makes digestive juices that break down food in the small intestine and hormones, such as insulin, that control blood sugar.

**For students: description**

The pancreas is a gland with two jobs. Its exocrine part, most of the gland, is made of acinar cells that release digestive enzymes (amylase, trypsin, peptidase, lipase) into ducts that reach the duodenum. Its endocrine part is the scattered pancreatic islets (islets of Langerhans), which release insulin and glucagon into the blood. It is divided into a head, body and tail.

**Location & neighbours**

Across the posterior abdominal wall, behind the stomach, stretching from the duodenum to the spleen. The head lies to the right of the superior mesenteric vein, the body between that vein and the aorta, and the tail reaches the hilum of the spleen.

| Detail | |
|---|---|
| Main functions | Exocrine: digestive enzymes for carbohydrates, fats and proteins, carried by the main pancreatic duct (duct of Wirsung) into the duodenum; release is controlled by secretin and cholecystokinin. Endocrine: alpha cells release glucagon when blood glucose is low; beta cells release insulin when it is high. |
| Blood supply | Its venous blood goes to the liver through the portal vein. |
| Nerve supply | *(blank)* |
| Lymph drainage | Regional nodes include the peripancreatic, pancreaticoduodenal, pyloric, superior mesenteric, celiac (head), hepatic artery, splenic and splenic hilar (body and tail), retroperitoneal and lateral aortic nodes. |

**Clinical relevance**

- Pancreatitis is inflammation caused by the gland's own digestive enzymes; gallstones and heavy alcohol use are major risk factors.
- Acute pancreatitis starts suddenly and usually settles within days; chronic pancreatitis does not heal and causes lasting damage.
- In type 2 diabetes the pancreas cannot release enough insulin in response to meals; in type 1 diabetes the immune system destroys the beta cells.  → disease page `type2_diabetes`
- In cystic fibrosis, thick, sticky mucus can block the ducts of the pancreas.
- The head of the pancreas is the most common site of pancreatic cancer.

**Exam tip**

The pancreas is both an exocrine gland (digestive enzymes to the duodenum) and an endocrine gland (insulin and glucagon from the islets of Langerhans).

**Sources**

- [Accessory Organs of the Digestive System - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html) (Public domain)
- [Pancreas - Islets of Langerhans - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/endocrine/glands/pancreas.html) (Public domain)
- [Anatomy of the Pancreas & Duodenum - NCI SEER Training Modules](https://training.seer.cancer.gov/biliary/anatomy/) (Public domain)
- [Regional Lymph Nodes (Biliary) - NCI SEER Training Modules](https://training.seer.cancer.gov/biliary/anatomy/lymph-nodes.html) (Public domain)
- [Pancreatic Diseases - MedlinePlus (NLM)](https://medlineplus.gov/pancreaticdiseases.html) (Public domain)
- [Definition & Facts for Pancreatitis - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/pancreatitis/definition-facts) (Public domain)
- [Your Digestive System & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works) (Public domain)
- [Definition & Facts for Cirrhosis - NIDDK](https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html: Pancreas has endocrine (scattered islets of Langerhans, insulin and glucagon) and exocrine parts; exocrine is the major part, acinar cells secrete into tiny ducts; enzymes amylase, trypsin, peptidase, lipase; secretion controlled by secretin and cholecystokinin.
- https://training.seer.cancer.gov/anatomy/endocrine/glands/pancreas.html: Long, soft organ lying transversely along the posterior abdominal wall, posterior to the stomach, from the region of the duodenum to the spleen; exocrine enzymes travel through a duct to the duodenum; alpha cells secrete glucagon for low blood glucose; beta cells secrete insulin for high blood glucose.
- https://training.seer.cancer.gov/biliary/anatomy/: Head right of left border of superior mesenteric vein; body between SMV and left border of aorta; tail between aorta and hilum of spleen; head is the most common site of primaries; contacts stomach, duodenum, spleen, major vessels; duct of Wirsung is the pancreatic duct opening into the duodenum; uncinate process labelled.
- https://training.seer.cancer.gov/biliary/anatomy/lymph-nodes.html: Pancreas regional nodes: superior/inferior to head and body, anterior and posterior pancreaticoduodenal, pyloric, proximal mesenteric, common bile duct, splenic hilar, peripancreatic, hepatic artery, celiac (head only), superior mesenteric, pancreaticolienal and splenic (body and tail only), retroperitoneal, lateral aortic.
- https://medlineplus.gov/pancreaticdiseases.html: Gland behind the stomach and in front of the spine; makes digestive juices and blood-sugar hormones; pancreatitis when enzymes digest the pancreas; cystic fibrosis mucus blocks tubes in the pancreas; type 1 immune attack on beta cells; type 2 pancreas loses ability to secrete enough insulin in response to meals.
- https://www.niddk.nih.gov/health-information/digestive-diseases/pancreatitis/definition-facts: Pancreas behind the stomach near the duodenum; pancreatitis is inflammation when digestive enzymes damage it; acute starts suddenly, most recover in several days; chronic does not heal and worsens; risk factors gallstones and heavy alcohol use.
- https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works: Pancreatic juice enzymes break down carbohydrates, fats and proteins and reach the small intestine through ducts.
- https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts: Portal vein carries blood from the stomach, intestines, spleen, gallbladder and pancreas to the liver.

---

## Spleen  (`spleen`)

*part · organ · endocrine · 1 FMA ids · covers: spleen*

**Summary (plain)**

The spleen is a fist-sized organ in the upper left part of the belly, under the ribs and behind the stomach.

**What it does (plain)**

It filters the blood, removes old red blood cells and helps the body fight infections.

**For students: description**

The spleen is the largest lymphatic organ in the body. It is wrapped in a connective tissue capsule that sends partitions inward. Its white pulp is lymphatic tissue, mostly lymphocytes gathered around arteries; its red pulp is blood-filled venous sinuses with cords of lymphocytes and macrophages. It filters blood much as lymph nodes filter lymph.

**Location & neighbours**

In the upper left abdominal cavity, just beneath the diaphragm, under the ribs and behind (posterior to) the stomach. The tail of the pancreas reaches its hilum.

| Detail | |
|---|---|
| Main functions | Filters blood; lymphocytes attack blood-borne germs and macrophages engulf debris; removes old and damaged red blood cells (with the liver); stores blood that can be squeezed into the circulation after a haemorrhage; produces lymphocytes. |
| Blood supply | Blood enters through the splenic artery, is filtered in the sinuses and leaves through the splenic vein; this venous blood reaches the liver through the portal vein. |
| Nerve supply | *(blank)* |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Some diseases cause the spleen to enlarge, and an enlarged spleen is more easily damaged or ruptured by injury.
- A badly damaged spleen may be removed (splenectomy); people can live without it but lose some ability to fight infections.
- An enlarged spleen is a physical finding in malaria; rarely, P. vivax malaria causes rupture of the spleen.  → disease page `malaria`

**Exam tip**

The spleen is the largest lymphatic organ in the body.

**Sources**

- [Spleen - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/lymphatic/components/spleen.html) (Public domain)
- [Spleen Diseases - MedlinePlus (NLM)](https://medlineplus.gov/spleendiseases.html) (Public domain)
- [Anatomy of the Pancreas & Duodenum - NCI SEER Training Modules](https://training.seer.cancer.gov/biliary/anatomy/) (Public domain)
- [Definition & Facts for Cirrhosis - NIDDK](https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts) (Public domain)
- [Clinical Features of Malaria - CDC](https://www.cdc.gov/malaria/hcp/clinical-features/index.html) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/lymphatic/components/spleen.html: Upper left abdominal cavity just beneath the diaphragm, posterior to the stomach; largest lymphatic organ; capsule extends inward into lobules; white pulp lymphocytes around arteries; red pulp venous sinuses and cords of lymphocytes and macrophages; filters blood like nodes filter lymph; splenic artery in, sinuses, splenic vein out; removes old red cells with the liver; blood reservoir released in hemorrhage; produces lymphocytes.
- https://medlineplus.gov/spleendiseases.html: Above the stomach and under the ribs on the left; about the size of a fist; part of lymphatic system; diseases can enlarge it; swollen spleen more easily ruptured; splenectomy; can live without it but lose some ability to fight infections.
- https://training.seer.cancer.gov/biliary/anatomy/: Tail of the pancreas extends to the hilum of the spleen; pancreas contacts the spleen.
- https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts: Portal vein carries blood from the stomach, intestines, spleen, gallbladder and pancreas to the liver.
- https://www.cdc.gov/malaria/hcp/clinical-features/index.html: Enlarged spleen listed as a physical finding in uncomplicated malaria; on rare occasions P. vivax malaria can cause rupture of the spleen.

---

## Small intestine  (`group:small_intestine`)

*group · organ · digestive · 8 FMA ids · covers: distal part of ileum, distal part of jejunum, duodenum, mesentery of small intestine, middle part of ileum, middle part of jejunum, proximal part of ileum, proximal part of jejunum*

**Summary (plain)**

The small intestine is a long, folded tube in the belly that connects the stomach to the large intestine.

**What it does (plain)**

It finishes digesting food and absorbs most of its nutrients and water into the body.

**For students: description**

The small intestine runs from the pyloric sphincter of the stomach to the ileocecal valve. It has three parts: the duodenum (first), the jejunum (middle) and the ileum (last). Its own juices mix with bile and pancreatic juice to finish digesting proteins, carbohydrates and fats. Circular folds (plicae circulares), villi and microvilli greatly increase its absorbing surface.

**Location & neighbours**

Coiled in the abdomen between the stomach and the large intestine. The duodenum receives bile and pancreatic juice through the ampulla of Vater; the ileum empties into the large intestine at the ileocecal valve.

| Detail | |
|---|---|
| Main functions | Completes digestion and absorbs nutrients and water. Mucosal cells secrete mucus and enzymes (peptidase, sucrase, maltase, lactase, lipase, enterokinase); endocrine cells release secretin and cholecystokinin. |
| Blood supply | Its venous blood goes to the liver through the portal vein. |
| Nerve supply | The enteric nervous system in its wall controls muscle contractions and secretion when food stretches the wall; the brain and spinal cord also influence digestion. |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- A peptic ulcer can form in the lining of the duodenum (duodenal ulcer), most often from H. pylori infection or NSAID use.  → disease page `peptic_ulcer_disease`
- Celiac disease is an immune reaction to gluten that damages the small intestine and prevents nutrient absorption.
- Other small intestine disorders include Crohn's disease, infections, bleeding, intestinal obstruction and cancer.

**Exam tip**

The small intestine is the longest part of the digestive system, about 20 feet (roughly 6 metres), folded many times to fit in the abdomen.

**Sources**

- [Small & Large Intestine - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/intestine.html) (Public domain)
- [Small Intestine Disorders - MedlinePlus (NLM)](https://medlineplus.gov/smallintestinedisorders.html) (Public domain)
- [Your Digestive System & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works) (Public domain)
- [Anatomy of the Liver & Gallbladder - NCI SEER Training Modules](https://training.seer.cancer.gov/biliary/anatomy/liver.html) (Public domain)
- [Definition & Facts for Cirrhosis - NIDDK](https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts) (Public domain)
- [Definition & Facts for Peptic Ulcers - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/peptic-ulcers-stomach-ulcers/definition-facts) (Public domain)
- [Definition & Facts for Celiac Disease - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/celiac-disease/definition-facts) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/digestive/regions/intestine.html: Extends from pyloric sphincter to ileocecal valve; duodenum, jejunum, ileum; plicae circulares, villi and microvilli increase surface; completes digestion, absorbs nutrients, passes residue to large intestine; mucosal secretions mucus, peptidase, sucrase, maltase, lactase, lipase, enterokinase; endocrine cells secrete cholecystokinin and secretin.
- https://medlineplus.gov/smallintestinedisorders.html: Connects stomach to large intestine; longest part of the digestive system, about 20 feet; folds many times to fit in the abdomen; does most digestion; three sections duodenum, jejunum, ileum; disorders: bleeding, celiac disease, Crohn's disease, infections, intestinal cancer, obstruction, IBS, ulcers.
- https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works: Duodenum first, jejunum middle, ileum end; own juice mixes with bile and pancreatic juice to complete breakdown of proteins, carbohydrates, fats; absorbs water and most nutrients; enteric nervous system in GI wall controls contractions and juice production when food stretches the wall; central nervous system controls some digestive functions.
- https://training.seer.cancer.gov/biliary/anatomy/liver.html: Ampulla of Vater, a dilated duct under 1.5 cm long, empties into the duodenum.
- https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts: Portal vein carries blood from the stomach, intestines, spleen, gallbladder and pancreas to the liver.
- https://www.niddk.nih.gov/health-information/digestive-diseases/peptic-ulcers-stomach-ulcers/definition-facts: Peptic ulcer is a sore on the lining of the stomach or duodenum (first part of small intestine); also called duodenal ulcer; most common causes H. pylori and NSAIDs.
- https://www.niddk.nih.gov/health-information/digestive-diseases/celiac-disease/definition-facts: Celiac disease is a chronic digestive and immune disorder that damages the small intestine, triggered by gluten; can prevent the body getting nutrients.

---

## Large intestine  (`group:large_intestine`)

*group · organ · digestive · 11 FMA ids · covers: appendix, ascending colon, descending colon, ileocecal junction, mesoappendix, rectum, taenia libera, taenia mesocolica …*

**Also called:** large bowel, colon

**Summary (plain)**

The large intestine is the last part of the digestive tube. It is a wide tube in the belly that starts where the small intestine ends and finishes at the anus.

**What it does (plain)**

It takes water out of leftover food, turns the waste into stool and stores it until a bowel movement.

**For students: description**

The large intestine runs from the ileocecal junction to the anus. Its parts are the cecum (with the appendix), the colon (ascending, transverse, descending and sigmoid) and the rectum, ending in the anal canal; the colon alone is about 150 cm long. It is wider than the small intestine, has no villi, and its outer muscle forms three bands, the teniae coli, which gather the wall into pouches (haustra).

**Location & neighbours**

The cecum and ascending colon form the right colon; the hepatic flexure lies under the right lobe of the liver; the transverse colon lies at the front of the abdomen; the splenic flexure lies near the spleen and tail of the pancreas; the descending and sigmoid colon form the left colon; the rectum follows the curve of the sacrum.

| Detail | |
|---|---|
| Main functions | Absorbs water and electrolytes, turns liquid waste into stool, and stores stool in the rectum until it is passed. It makes no digestive enzymes; its bacteria break down leftover nutrients and make vitamin K. |
| Blood supply | *(blank)* |
| Nerve supply | *(blank)* |
| Lymph drainage | To lymph nodes along the colon (pericolic, epicolic and mesenteric nodes) and along the major arteries that supply each segment; the colon's mesentery holds about 100 to 150 lymph nodes. |

**Clinical relevance**

- Colorectal cancer starts in the colon or rectum; adenomatous polyps can turn into cancer, so screening (stool tests, colonoscopy) is recommended from age 45 in the United States.
- Diverticulitis is inflammation or infection of small pouches in the colon wall.
- Ulcerative colitis causes ulcers in the colon and rectum; long-standing colitis raises colorectal cancer risk.
- Irritable bowel syndrome causes abdominal cramping and changes in bowel habit.

**Exam tip**

The longitudinal muscle of the colon is limited to three bands, the teniae coli, whose pull forms the pouches called haustra.

**Sources**

- [Small & Large Intestine - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/intestine.html) (Public domain)
- [Colorectal Anatomy - NCI SEER Training Modules](https://training.seer.cancer.gov/colorectal/anatomy/) (Public domain)
- [Colorectal Anatomy and ICD-O-3 - NCI SEER Training Modules](https://training.seer.cancer.gov/colorectal/anatomy/colorectal-anatomy-and-icdO3.html) (Public domain)
- [Colorectal Wall of Pathology - NCI SEER Training Modules](https://training.seer.cancer.gov/colorectal/anatomy/colorectal-wall-of-pathology.html) (Public domain)
- [EOD Regional Nodes - NCI SEER Training Modules](https://training.seer.cancer.gov/colorectal/staging/eod-regional-nodes.html) (Public domain)
- [Your Digestive System & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works) (Public domain)
- [Colonic Diseases - MedlinePlus (NLM)](https://medlineplus.gov/colonicdiseases.html) (Public domain)
- [Colorectal Cancer - MedlinePlus (NLM)](https://medlineplus.gov/colorectalcancer.html) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/digestive/regions/intestine.html: Large intestine wider than small; begins at ileocecal junction, ends at anus; colon, rectum, anal canal; no villi, many goblet cells; longitudinal muscle limited to three teniae coli whose contraction forms haustra; no digestive enzymes; absorbs water and electrolytes; eliminates feces; rectum follows curve of sacrum.
- https://training.seer.cancer.gov/colorectal/anatomy/: Colon and rectum absorb water and electrolytes, form and store stool; colon about 5 feet (150 cm) long; segments cecum, ascending, transverse, descending, sigmoid; rectum stores stool.
- https://training.seer.cancer.gov/colorectal/anatomy/colorectal-anatomy-and-icdO3.html: Cecum part of right colon with appendiceal orifice and ileocecal valve; hepatic flexure under right lobe of liver; transverse colon anterior; splenic flexure near tail of pancreas and spleen; ascending and descending colon behind the peritoneum; rectum about 12 cm; anal canal at distal end.
- https://training.seer.cancer.gov/colorectal/anatomy/colorectal-wall-of-pathology.html: About 100 to 150 lymph nodes in the colon's mesentery; regional nodes are those along the colon and along the major arteries supplying that segment.
- https://training.seer.cancer.gov/colorectal/staging/eod-regional-nodes.html: General regional nodes for colorectal sites: colic, epicolic, mesenteric, paracolic, pericolic/perirectal.
- https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works: Large intestine includes appendix, cecum, colon and rectum; absorbs water and changes waste from liquid into stool; bacteria break down remaining nutrients and make vitamin K; rectum stores stool until it is pushed out of the anus.
- https://medlineplus.gov/colonicdiseases.html: Colon (large intestine) is a long hollow tube at the end of the digestive tract that makes and stores stool; diverticulitis is inflammation or infection of small pouches; ulcerative colitis causes ulcers in colon and rectum; IBS causes cramping.
- https://medlineplus.gov/colorectalcancer.html: Starts in colon or rectum; adenomas can turn into cancer; ulcerative colitis or Crohn disease for 8+ years is a risk factor; screening recommended starting at 45 (stool tests, colonoscopy, sigmoidoscopy).

---

## Appendix  (`appendix`)

*part · organ · digestive · 1 FMA ids · covers: appendix*

**Summary (plain)**

The appendix is a small, finger-shaped pouch attached to the start of the large intestine, in the lower right part of the belly.

**What it does (plain)**

It has no known function.

**For students: description**

The appendix (vermiform appendix) is a narrow, worm-like pouch that branches off the cecum, the first part of the large intestine. It counts as part of the large intestine along with the cecum, colon and rectum. It has no known function, but it can become blocked and inflamed.

**Location & neighbours**

In the lower right area of the abdomen, hanging from the lower part of the cecum, near where the small intestine (ileum) empties into the large intestine at the ileocecal valve.

| Detail | |
|---|---|
| Main functions | No known function. |
| Blood supply | *(blank)* |
| Nerve supply | *(blank)* |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Inflammation of the appendix (appendicitis) is a medical emergency and is the most common cause of sudden abdominal pain needing surgery in the United States.  → disease page `acute_appendicitis`
- Appendicitis is usually caused by a blockage inside the appendix, such as hardened stool or a growth.  → disease page `acute_appendicitis`
- Pain often starts near the navel and moves lower and to the right; treatment almost always means removing the appendix.  → disease page `acute_appendicitis`
- If untreated, the appendix can burst, causing peritonitis (a serious abdominal infection) or an appendiceal abscess.  → disease page `acute_appendicitis`

**Exam tip**

About 5 to 9 out of every 100 people get appendicitis at some point, most often in their teens and 20s.

**Sources**

- [Appendicitis - MedlinePlus (NLM)](https://medlineplus.gov/appendicitis.html) (Public domain)
- [Definition & Facts for Appendicitis - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/appendicitis/definition-facts) (Public domain)
- [Symptoms & Causes of Appendicitis - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/appendicitis/symptoms-causes) (Public domain)
- [Your Digestive System & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works) (Public domain)
- [Colorectal Anatomy and ICD-O-3 - NCI SEER Training Modules](https://training.seer.cancer.gov/colorectal/anatomy/colorectal-anatomy-and-icdO3.html) (Public domain)
- [Small & Large Intestine - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/intestine.html) (Public domain)

**What was checked on each page**

- https://medlineplus.gov/appendicitis.html: Appendix is a small tube-like organ attached to the first part of the large intestine, in the lower right abdomen; has no known function; blockage inside it causes appendicitis; main symptom is abdominal pain, often on the right; appendicitis is a medical emergency; treatment almost always involves removing the appendix.
- https://www.niddk.nih.gov/health-information/digestive-diseases/appendicitis/definition-facts: Appendicitis is inflammation of the appendix, a finger-like pouch attached to the large intestine; appendix in lower-right abdomen; most common cause of acute abdominal pain needing surgery in the US; about 5 to 9 of every 100 people develop it; more often in teens and 20s; untreated it can burst, causing peritonitis; appendiceal abscess.
- https://www.niddk.nih.gov/health-information/digestive-diseases/appendicitis/symptoms-causes: Pain may begin near the belly button and move lower and to the right; hardened stool or growths can block the opening inside the appendix.
- https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works: The large intestine includes the appendix, cecum, colon and rectum; the appendix is a finger-shaped pouch attached to the cecum.
- https://training.seer.cancer.gov/colorectal/anatomy/colorectal-anatomy-and-icdO3.html: Appendix (C18.1): a vermiform (wormlike) diverticulum located in the lower cecum; cecum is part of the right colon, synonyms include ileocecal valve/junction and appendiceal orifice.
- https://training.seer.cancer.gov/anatomy/digestive/regions/intestine.html: Small intestine ends at the ileocecal valve, where it empties into the large intestine; the large intestine begins at the ileocecal junction where the ileum enters.

---

## Kidney  (`kidney`)

*part · organ · urinary · 2 FMA ids · covers: kidney*

**Summary (plain)**

The kidneys are two bean-shaped organs, each about the size of a fist. They sit at the back of the belly, just below the ribs, one on each side of the spine.

**What it does (plain)**

They clean the blood by taking out wastes and extra water, which leave the body as urine.

**For students: description**

The kidneys are the main organs of the urinary system. Each adult kidney is roughly 12 cm long, 6 cm wide and 3 cm thick, with an indented medial border, the hilum. Inside, an outer cortex surrounds a medulla made of renal pyramids; urine drains through minor and major calyces into the renal pelvis and on into the ureter. Each kidney holds about a million nephrons, the filtering units.

**Location & neighbours**

On the posterior abdominal wall, behind the peritoneum (retroperitoneal), between the 12th thoracic and 3rd lumbar vertebrae, partly shielded by the lower ribs. The right kidney usually sits a little lower than the left because the liver pushes it down.

| Detail | |
|---|---|
| Main functions | Filter the blood and remove wastes, extra fluid and acid in urine; balance water, sodium, potassium, calcium and phosphorus; make hormones that help control blood pressure, stimulate red blood cell production and support bone health. The juxtaglomerular apparatus secretes renin. |
| Blood supply | The renal artery enters at the hilum and branches down to the nephrons; each glomerulus receives an afferent arteriole and is drained by an efferent arteriole. Filtered blood leaves through the renal vein at the hilum. |
| Nerve supply | *(blank)* |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Chronic kidney disease slowly damages the nephrons over years; diabetes and high blood pressure are its most common causes, and many people have no symptoms until it is advanced.  → disease page `chronic_kidney_disease`
- Kidney failure is treated with dialysis or a kidney transplant.  → disease page `chronic_kidney_disease`
- Kidney stones are solid masses formed from substances in urine; a stuck stone can block urine flow and cause severe back or side pain and blood in the urine.
- A urinary tract infection can reach the kidney (pyelonephritis); pain in the back or side below the ribs and fever are possible symptoms.  → disease page `urinary_tract_infection`

**Exam tip**

The right kidney usually lies slightly lower than the left, because the liver displaces it downward.

**Sources**

- [Kidneys - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/urinary/components/kidney.html) (Public domain)
- [Your Kidneys & How They Work - NIDDK](https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work) (Public domain)
- [Your Urinary Tract & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/urologic-diseases/urinary-tract-how-it-works) (Public domain)
- [Kidney Diseases - MedlinePlus (NLM)](https://medlineplus.gov/kidneydiseases.html) (Public domain)
- [Chronic Kidney Disease - MedlinePlus (NLM)](https://medlineplus.gov/chronickidneydisease.html) (Public domain)
- [Kidney Stones - MedlinePlus (NLM)](https://medlineplus.gov/kidneystones.html) (Public domain)
- [Urinary Tract Infections - MedlinePlus (NLM)](https://medlineplus.gov/urinarytractinfections.html) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/urinary/components/kidney.html: Kidneys lie between T12 and L3; right slightly lower because liver displaces it; against posterior abdominal wall, protected by lower ribs; retroperitoneal; about 3 cm thick, 6 cm wide, 12 cm long; bean-shaped with medial indentation (hilum) leading to renal sinus; renal artery enters, ureter and renal vein leave at hilum; cortex, medulla of renal pyramids, renal columns; minor and major calyces drain into renal pelvis continuous with ureter; over a million nephrons; afferent arteriole enters and efferent leaves the renal corpuscle; primary organs of urinary system; juxtaglomerular apparatus secretes renin.
- https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work: Bean-shaped, about the size of a fist, below the rib cage one on each side of the spine; about a million nephrons each; remove wastes, extra fluid and acid; balance water, sodium, calcium, phosphorus, potassium; make hormones for blood pressure, red blood cell production and bone health; renal artery brings blood in, renal vein takes filtered blood out.
- https://www.niddk.nih.gov/health-information/urologic-diseases/urinary-tract-how-it-works: Kidneys are two bean-shaped, fist-sized organs below the rib cage on each side of the spine; filter about 120 to 150 quarts of blood a day making about 1 to 2 quarts of urine.
- https://medlineplus.gov/kidneydiseases.html: Two kidneys, each about the size of a fist, near the middle of the back just below the rib cage; filter blood to make urine; urine travels through ureters to the bladder; kidney failure treated with dialysis or transplant.
- https://medlineplus.gov/chronickidneydisease.html: CKD: damaged kidneys cannot filter blood well; diabetes and high blood pressure are the most common causes; slow damage over years, many have no symptoms until very advanced; may lead to kidney failure needing dialysis or transplant.
- https://medlineplus.gov/kidneystones.html: Kidney stones are solid masses formed in the kidneys from substances in urine; a stuck stone can block urine flow and cause intense pain; warning signs include severe back or side pain and blood in urine.
- https://medlineplus.gov/urinarytractinfections.html: Kidney infection (pyelonephritis) listed as a UTI type; symptoms include fever and pain in the back or side below the ribs; treatment with antibiotics.

---

## Urinary bladder  (`urinary bladder`)

*part · organ · urinary · 1 FMA ids · covers: urinary bladder*

**Also called:** bladder

**Summary (plain)**

The bladder is a hollow, balloon-shaped bag of muscle low in the belly, in the pelvis between the hip bones.

**What it does (plain)**

It stores urine from the kidneys and then squeezes to push it out of the body.

**For students: description**

The urinary bladder is a muscular reservoir that stores urine until it is passed. Its size and shape change with how full it is. Its wall has a mucosa of transitional epithelium that folds into rugae when empty, a submucosa, and smooth muscle called the detrusor, whose contraction empties the bladder. The trigone on its floor lies between the two ureter openings and the urethral opening.

**Location & neighbours**

In the pelvic cavity, behind the pubic symphysis and below the parietal peritoneum, which covers only its upper surface. The two ureters enter it from the kidneys, and the urethra leaves from the apex of the trigone on its floor.

| Detail | |
|---|---|
| Main functions | Stores urine, holding about 1.5 to 2 cups in an adult, and expels it when the detrusor contracts. Flaps over the ureter openings stop urine flowing back up to the kidneys. Internal and external sphincters keep urine in until urination. |
| Blood supply | *(blank)* |
| Nerve supply | *(blank)* |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Cystitis is inflammation of the bladder, often caused by infection; urinary tract infections are far more common in women than in men.  → disease page `urinary_tract_infection`
- Bladder infection can cause painful or burning urination, a frequent urge to urinate and pressure in the lower belly; it is treated with antibiotics.  → disease page `urinary_tract_infection`
- Bladder cancer forms in the bladder lining; smoking and workplace chemicals are risk factors, and blood in the urine is a key symptom. It is the sixth most common cancer in the United States.
- Urinary incontinence (loss of bladder control) and overactive bladder are common bladder problems.
- Cystoscopy uses a scope to look at the inside of the bladder wall.

**Exam tip**

The trigone is a triangle on the bladder floor: the two ureter openings form its base and the urethral opening is its apex.

**Sources**

- [Urinary Bladder - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/urinary/components/bladder.html) (Public domain)
- [Your Urinary Tract & How It Works - NIDDK](https://www.niddk.nih.gov/health-information/urologic-diseases/urinary-tract-how-it-works) (Public domain)
- [Bladder Diseases - MedlinePlus (NLM)](https://medlineplus.gov/bladderdiseases.html) (Public domain)
- [Urinary Tract Infections - MedlinePlus (NLM)](https://medlineplus.gov/urinarytractinfections.html) (Public domain)
- [Bladder Cancer - MedlinePlus (NLM)](https://medlineplus.gov/bladdercancer.html) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/urinary/components/bladder.html: Temporary storage reservoir for urine; in pelvic cavity, posterior to the symphysis pubis, below the parietal peritoneum; size and shape vary with fullness; mucosa of transitional epithelium with rugae when empty; submucosa with elastic fibres; smooth muscle called detrusor, whose contraction expels urine; parietal peritoneum on superior surface, fibrous tissue elsewhere; trigone formed by two ureteral openings (base) and urethral opening (apex); mucosal flaps over ureteral openings prevent backflow; internal urethral sphincter.
- https://www.niddk.nih.gov/health-information/urologic-diseases/urinary-tract-how-it-works: Hollow muscular balloon-shaped organ in the pelvis between the hip bones; expands as it fills; holds about 1.5 to 2 cups of urine; wall relaxes while filling and tightens to empty; internal and external sphincters; ureters carry urine from kidneys to bladder.
- https://medlineplus.gov/bladderdiseases.html: Bladder is a hollow organ in the lower abdomen that stores urine; cystitis is inflammation often caused by infection; urinary incontinence; overactive bladder; cystoscopy examines the bladder wall.
- https://medlineplus.gov/urinarytractinfections.html: Women get UTIs far more often than men; symptoms include painful or burning urination, frequent urge, pressure in the lower belly; cystitis listed; treatment with antibiotics.
- https://medlineplus.gov/bladdercancer.html: Cancer in the bladder lining; sixth most common cancer in the United States; blood in urine; risk factors smoking and workplace chemical exposure.

---

## Brain  (`group:fma_FMA50801_o`)

*group · organ · nervous · 52 FMA ids · covers: angular gyrus, cardinal segment of brain, cerebellum, cerebral aqueduct, cerebral white matter, cingulate gyrus, fourth ventricle, fusiform gyrus …*

**Summary (plain)**

The brain is the body's control center. It sits inside the skull and joins the spinal cord at a large opening in the base of the skull.

**What it does (plain)**

It controls thinking, memory, speech and movement, and helps run many of the body's organs.

**For students: description**

The brain and spinal cord form the central nervous system. The cerebrum, the largest part, is split into right and left hemispheres joined by the corpus callosum; each has frontal, parietal, occipital and temporal lobes plus the deep insula. The diencephalon (thalamus, hypothalamus, epithalamus) lies centrally. The brainstem (midbrain, pons, medulla oblongata) links it to the spinal cord, and the cerebellum is the second largest part.

**Location & neighbours**

In the cranial cavity of the skull. It is continuous with the spinal cord at the foramen magnum. A fold of dura, the tentorium, separates the cerebrum above from the cerebellum and brainstem below. It is wrapped by three meninges: dura mater, arachnoid and pia mater.

| Detail | |
|---|---|
| Main functions | Controls thought, memory, speech and movement and helps regulate many organs. The thalamus relays sensory signals (except smell) to the cerebral cortex; the hypothalamus helps keep homeostasis by regulating visceral activities; all ascending and descending tracts pass through the medulla oblongata. |
| Blood supply | *(blank)* |
| Nerve supply | *(blank)* |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- A stroke is a loss of blood flow to part of the brain; brain cells start dying within minutes. About 80% of strokes are ischemic (a clot blocks a vessel).  → disease page `ischemic_stroke`
- A hemorrhagic stroke happens when a blood vessel breaks and bleeds into the brain.
- Meningitis is inflammation of the meninges; bacterial meningitis is rare but can be deadly and can cause hearing loss or brain damage.  → disease page `bacterial_meningitis`
- Brain tumors are named supratentorial when in the cerebral lobes and infratentorial when in the cerebellum or brainstem.
- Degenerative diseases such as Alzheimer's and Parkinson's disease, encephalitis and traumatic brain injury are other important brain disorders.

**Exam tip**

The cerebrum is the largest part of the brain and the cerebellum the second largest; the thalamus makes up about 80 percent of the diencephalon.

**Sources**

- [Central Nervous System - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/nervous/organization/cns.html) (Public domain)
- [Brain Diseases - MedlinePlus (NLM)](https://medlineplus.gov/braindiseases.html) (Public domain)
- [Stroke - MedlinePlus (NLM)](https://medlineplus.gov/stroke.html) (Public domain)
- [Meningitis - MedlinePlus (NLM)](https://medlineplus.gov/meningitis.html) (Public domain)
- [Tentorium - NCI SEER Training Modules](https://training.seer.cancer.gov/cns/cns-anatomy/tentorium.html) (Public domain)
- [Brain and Spine Tumor Anatomy - National Cancer Institute](https://www.cancer.gov/rare-brain-spine-tumor/tumors/anatomy) (Public domain)
- [The Nervous System - NCI SEER Training Modules](https://training.seer.cancer.gov/cns/nervous-system/) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/nervous/organization/cns.html: Brain in cranium, continuous with spinal cord at foramen magnum; meninges dura, arachnoid, pia; CSF in subarachnoid space; cerebrum largest, two hemispheres, longitudinal fissure, corpus callosum; frontal, parietal, occipital, temporal lobes and insula; diencephalon with thalamus (about 80%, relays sensory except smell), hypothalamus (homeostasis, visceral activities), epithalamus; brainstem midbrain, pons, medulla (all ascending and descending fibers pass); cerebellum second largest, below occipital lobes; ventricles with CSF.
- https://medlineplus.gov/braindiseases.html: Brain is the control center; controls thoughts, memory, speech, movement, regulates many organs; types of brain disease: tumors, degenerative diseases (Alzheimer's, Parkinson's), encephalitis, genetic disorders, stroke, traumatic brain injury.
- https://medlineplus.gov/stroke.html: Stroke is loss of blood flow to part of brain; brain cells begin to die within minutes; ischemic (clot) about 80% of strokes; hemorrhagic is a vessel breaking and bleeding into brain.
- https://medlineplus.gov/meningitis.html: Meningitis is inflammation of the meninges around brain and spinal cord; viral most common; bacterial rare but can be deadly; can cause stroke, hearing loss, brain damage.
- https://training.seer.cancer.gov/cns/cns-anatomy/tentorium.html: Tentorium is a dural fold separating cerebellum from cerebrum; cerebrum supratentorial; cerebellum and brainstem infratentorial.
- https://www.cancer.gov/rare-brain-spine-tumor/tumors/anatomy: Tumors in the lobes are supratentorial; tumors in cerebellum or brainstem are infratentorial; four lobes per hemisphere.
- https://training.seer.cancer.gov/cns/nervous-system/: Brain and spinal cord make up the CNS; brain in the cranial vault; continuous with spinal cord at foramen magnum.

---

## Cerebellum  (`cerebellum`)

*part · organ · nervous · 1 FMA ids · covers: cerebellum*

**Summary (plain)**

The cerebellum is a part of the brain at the lower back of the head, tucked under the back of the main brain (cerebrum).

**What it does (plain)**

It controls coordination and balance, for example when you play the piano or hit a tennis ball.

**For students: description**

The cerebellum is the second largest part of the brain. It lies below the occipital lobes of the cerebrum and is joined to the rest of the central nervous system by three paired bundles of myelinated fibers, the cerebellar peduncles. It controls coordination and balance.

**Location & neighbours**

At the back of the cranial cavity, in the posterior cranial fossa, which also holds the pons and medulla oblongata. It lies below the occipital lobes and below the tentorium, the dural fold that separates it from the cerebrum.

| Detail | |
|---|---|
| Main functions | Coordination and balance. |
| Blood supply | *(blank)* |
| Nerve supply | *(blank)* |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Ataxias, a loss of muscle control in the arms and legs, are a key sign of cerebellar disorders.
- Other cerebellar disorders include cancer, genetic disorders and degeneration, in which brain cells waste away; some have no cure but treatment may ease symptoms.
- Tumors of the cerebellum or brainstem are called infratentorial tumors.

**Exam tip**

The cerebellum sits in the posterior cranial fossa, which Gray's Anatomy calls the largest and deepest of the three cranial fossae.

**Sources**

- [Central Nervous System - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/nervous/organization/cns.html) (Public domain)
- [Cerebellar Disorders - MedlinePlus (NLM)](https://medlineplus.gov/cerebellardisorders.html) (Public domain)
- [Tentorium - NCI SEER Training Modules](https://training.seer.cancer.gov/cns/cns-anatomy/tentorium.html) (Public domain)
- [Brain and Spine Tumor Anatomy - National Cancer Institute](https://www.cancer.gov/rare-brain-spine-tumor/tumors/anatomy) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), skull (interior of the base) - PubAnnotation GrayAnatomy doc 47](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/nervous/organization/cns.html: Cerebellum is the second largest portion of the brain, located below the occipital lobes; connected to other parts of the CNS by three paired bundles of myelinated fibers, the cerebellar peduncles.
- https://medlineplus.gov/cerebellardisorders.html: Cerebellum controls coordination and balance; example of playing piano or hitting a tennis ball; problems include cancer, genetic disorders, ataxias (loss of muscle control in arms and legs), degeneration; some have no cure, treatment may ease symptoms.
- https://training.seer.cancer.gov/cns/cns-anatomy/tentorium.html: Tentorium is a dural fold separating cerebellum from cerebrum; cerebellum and brainstem are infratentorial.
- https://www.cancer.gov/rare-brain-spine-tumor/tumors/anatomy: Tumors located in the cerebellum or brainstem are called infratentorial.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47: Posterior fossa is the largest and deepest; it lodges the cerebellum, pons and medulla oblongata.

---

## Pituitary gland  (`pituitary gland`)

*part · organ · endocrine · 1 FMA ids · covers: pituitary gland*

**Also called:** hypophysis, master gland

**Summary (plain)**

The pituitary gland is a pea-sized gland at the base of the brain, just above the back of the nose.

**What it does (plain)**

It makes hormones that control growth and tell many other glands, such as the thyroid and adrenal glands, how much hormone to make.

**For students: description**

The pituitary gland (hypophysis) is a small endocrine gland, about 1 cm across, hanging from the hypothalamus by a stalk, the infundibulum. Its anterior lobe (adenohypophysis) is controlled by releasing hormones from the hypothalamus; its posterior lobe (neurohypophysis) is controlled by nerve signals. Because it regulates other glands, it is often called the master gland.

**Location & neighbours**

In the sella turcica, a hollow in the sphenoid bone at the base of the skull, where it is almost surrounded by bone. It lies below the hypothalamus of the brain, to which the infundibulum attaches it.

| Detail | |
|---|---|
| Main functions | Anterior lobe: growth hormone, thyroid-stimulating hormone, adrenocorticotropic hormone (ACTH, which drives cortisol release), the gonadotropins LH and FSH, and prolactin. Posterior lobe: antidiuretic hormone, which makes the kidneys keep water, and oxytocin, which contracts the uterus and ejects milk. |
| Blood supply | *(blank)* |
| Nerve supply | The posterior lobe is controlled by nerve stimulation from the hypothalamus, which is connected to it through the infundibulum. |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Pituitary tumors are the most common cause of pituitary disorders; most are benign adenomas, and very few are malignant.
- Many pituitary tumors make excess hormone and can cause conditions such as Cushing's syndrome or hyperthyroidism; headaches and vision problems can also occur.
- Pituitary disorders often mean too much or too little of one hormone, for example acromegaly, hyperprolactinemia or hypopituitarism.
- Surgery to remove a pituitary tumor can be done through the nose or upper lip, since the gland lies just above the sphenoid bone.

**Exam tip**

The pituitary sits in the sella turcica of the sphenoid bone and is linked to the hypothalamus by the infundibulum.

**Sources**

- [Pituitary Gland - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/endocrine/glands/pituitary.html) (Public domain)
- [Pituitary Disorders - MedlinePlus (NLM)](https://medlineplus.gov/pituitarydisorders.html) (Public domain)
- [Pituitary Tumors - MedlinePlus (NLM)](https://medlineplus.gov/pituitarytumors.html) (Public domain)
- [What Are Pituitary Tumors? - National Cancer Institute](https://www.cancer.gov/types/pituitary/what-are-pituitary-tumors) (Public domain)
- [Pituitary Tumors Treatment (PDQ) Patient Version - National Cancer Institute](https://www.cancer.gov/types/pituitary/patient/pituitary-treatment-pdq) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/endocrine/glands/pituitary.html: About 1 cm in diameter; rests in the sella turcica of the sphenoid bone, nearly surrounded by bone; attached to the hypothalamus by the infundibulum; anterior lobe (adenohypophysis) controlled by hypothalamic releasing hormones, makes GH, TSH, ACTH, gonadotropins, prolactin; posterior lobe (neurohypophysis) controlled by nerve stimulation, releases ADH (water reabsorption by kidney tubules) and oxytocin (uterine contraction, milk ejection).
- https://medlineplus.gov/pituitarydisorders.html: Pea-sized gland at the base of the brain; called the master control gland; disorders mean too much or too little of a hormone; pituitary tumors are the most common cause; acromegaly, hyperprolactinemia, hypopituitarism listed.
- https://medlineplus.gov/pituitarytumors.html: Most common type makes hormones that upset hormone balance, causing e.g. Cushing's syndrome or hyperthyroidism; symptoms include headaches and vision problems; surgery is often the main treatment.
- https://www.cancer.gov/types/pituitary/what-are-pituitary-tumors: Pea-sized organ in the centre of the brain just above the back of the nose; called the master endocrine gland; makes prolactin, ACTH, growth hormone, TSH, LH, FSH; most pituitary tumors are benign adenomas, very few malignant; most are functioning.
- https://www.cancer.gov/types/pituitary/patient/pituitary-treatment-pdq: Pituitary gland lies just above the sphenoid bone; surgery can reach it through the nose or upper lip.

---

## Eyeball  (`group:eye_ball`)

*group · organ · nervous · 20 FMA ids · covers: anterior chamber of eyeball, choroid, cornea, corona ciliaris, iris, lens, optic part of retina, sclera …*

**Summary (plain)**

The eyeball is the round organ of sight that sits in the eye socket of the skull. Light enters at the front and is sensed at the back.

**What it does (plain)**

It focuses light onto the light-sensitive retina, which turns it into signals that the optic nerve carries to the brain.

**For students: description**

The eyeball has three layers: the white sclera outside, the middle uvea (iris, ciliary body and choroid), and the light-sensitive retina at the back. At the front, the clear dome-shaped cornea and the lens behind it focus light onto the retina; the colored iris controls how much light enters through the pupil. Gel called vitreous fills the eye.

**Location & neighbours**

In the orbit, a four-sided, pyramid-shaped cavity of the skull. The optic nerve links the retina at the back of the eye to the brain, passing through the optic foramen at the apex of the orbit.

| Detail | |
|---|---|
| Main functions | Cornea bends and focuses light and protects the eye from germs and dust; iris controls light entering the pupil; lens works with the cornea to focus light on the retina; retinal photoreceptors turn light into electrical signals; the macula, the center of the retina, gives fine detail. |
| Blood supply | *(blank)* |
| Nerve supply | *(blank)* |
| Lymph drainage | *(blank)* |

**Clinical relevance**

- Cataract is clouding of the lens, mostly from aging; surgery replaces the cloudy lens with an artificial intraocular lens.
- Glaucoma is a group of diseases that damage the optic nerve, usually as fluid pressure inside the eye slowly rises; vision loss starts in side vision.
- Retinal detachment, in which the retina pulls away from the back of the eye, is a medical emergency.
- Diabetic retinopathy is damage to the small blood vessels of the retina caused by diabetes.
- Refractive errors are the most common vision problems.

**Exam tip**

The cornea and lens together focus light on the retina; with age, strands in the vitreous gel clump and cast shadows on the retina, seen as floaters.

**Sources**

- [How the Eyes Work - National Eye Institute](https://www.nei.nih.gov/learn-about-eye-health/healthy-vision/how-eyes-work) (Public domain)
- [Uveitis - National Eye Institute](https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/uveitis) (Public domain)
- [Floaters - National Eye Institute](https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/floaters) (Public domain)
- [Corneal Disorders - MedlinePlus (NLM)](https://medlineplus.gov/cornealdisorders.html) (Public domain)
- [Retinal Disorders - MedlinePlus (NLM)](https://medlineplus.gov/retinaldisorders.html) (Public domain)
- [Cataract - MedlinePlus (NLM)](https://medlineplus.gov/cataract.html) (Public domain)
- [Glaucoma - MedlinePlus (NLM)](https://medlineplus.gov/glaucoma.html) (Public domain)
- [Eye Diseases - MedlinePlus (NLM)](https://medlineplus.gov/eyediseases.html) (Public domain)
- [Glaucoma - National Eye Institute](https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/glaucoma) (Public domain)
- [Optic Nerve Disorders - MedlinePlus (NLM)](https://medlineplus.gov/opticnervedisorders.html) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), the skull as a whole - PubAnnotation GrayAnatomy doc 46](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/46) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), skull (interior of the base) - PubAnnotation GrayAnatomy doc 47](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47) (Public domain)

**What was checked on each page**

- https://www.nei.nih.gov/learn-about-eye-health/healthy-vision/how-eyes-work: Cornea is the clear dome-shaped front layer that bends light; pupil lets light in; iris is colored part controlling light through pupil; lens works with cornea to focus light on retina; retina photoreceptors turn light into electrical signals; optic nerve carries signals from retina to brain.
- https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/uveitis: Uvea is the middle layer of the eye between sclera and retina; sclera is the white part of the eye; retina is light-sensitive layer at back; uvea includes iris, ciliary body, choroid.
- https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/floaters: Vitreous is the gel-like fluid that fills the eye; with age strands clump and cast shadows on the retina (floaters); vitreous can pull away from retina.
- https://medlineplus.gov/cornealdisorders.html: Cornea is the clear dome-shaped outer layer; protects eye from germs and dust; role in focusing.
- https://medlineplus.gov/retinaldisorders.html: Retina is thin light-sensitive tissue at back of eye; macula is center of retina for fine detail; retinal detachment is an emergency; diabetic retinopathy damages small retinal vessels.
- https://medlineplus.gov/cataract.html: Cataract is clouding of the lens; most related to aging; surgery replaces lens with intraocular lens (IOL).
- https://medlineplus.gov/glaucoma.html: Glaucoma damages the optic nerve; in common types fluid pressure inside the eye slowly rises.
- https://medlineplus.gov/eyediseases.html: Refractive errors are the most common vision problems; cataract, glaucoma, retinal disorders, macular degeneration, conjunctivitis listed.
- https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/glaucoma: Glaucoma vision loss usually starts in side (peripheral) vision.
- https://medlineplus.gov/opticnervedisorders.html: Each eye has one optic nerve connecting its retina to the brain.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/46: Each orbit is a quadrilateral pyramidal cavity; its apex corresponds to the optic foramen.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47: Optic foramen transmits the optic nerve and ophthalmic artery.

---

## Skull  (`group:skull`)

*group · bone · musculoskeletal · 22 FMA ids · covers: ethmoid, frontal bone, inferior nasal concha, lacrimal bone, mandible, maxilla, nasal bone, occipital bone …*

**Summary (plain)**

The skull is the bony framework of the head. It is made of the cranium, which surrounds the brain, and the bones of the face.

**What it does (plain)**

It is hard and protects the brain, and it forms the eye sockets, nose and jaws.

**For students: description**

The skull has the cranium above and behind and the face below and in front. The 8 cranial bones are the paired parietal and temporal bones and the single frontal, occipital, ethmoid and sphenoid bones. The 14 facial bones are the paired maxillae, zygomatic, nasal, palatine, lacrimal and inferior nasal conchae, plus the mandible and vomer. Most of its bones meet at fixed joints called sutures.

**Location & neighbours**

Forms the head. The brain sits in the cranial cavity and joins the spinal cord through the foramen magnum in the occipital bone. The orbits and nasal cavity open on the front of the face.

| Detail | |
|---|---|
| Type | flat |
| Joints | Sutures: coronal (frontal with parietals), sagittal (between parietals), lambdoid (parietals with occipital), squamosal (temporal with parietal). Temporomandibular joints on each side connect the lower jaw (mandible) to the skull. |
| Landmarks | Foramen magnum; anterior, middle and posterior cranial fossae; sella turcica holding the pituitary; optic foramen; orbits; zygomatic arch; mastoid process; temporal fossa; bregma and lambda, marking the anterior and posterior fontanelles of the fetal skull. |

**Clinical relevance**

- A closed head injury does not break through the skull; in an open (penetrating) injury an object pierces the skull and enters the brain.
- Skull fractures are among the more severe head injuries, along with concussion and traumatic brain injury.
- Temporomandibular disorders, over 30 conditions of the jaw joint and chewing muscles, cause jaw pain, stiffness and trouble chewing.

**Exam tip**

The anterior fontanelle, the largest, is not fully closed until about the middle of the second year; the posterior fontanelle closes within a month or two after birth.

**Sources**

- [Axial Skeleton - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/divisions/axial.html) (Public domain)
- [Classification of Bones - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/classification.html) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), the skull as a whole - PubAnnotation GrayAnatomy doc 46](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/46) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), skull (interior of the base) - PubAnnotation GrayAnatomy doc 47](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47) (Public domain)
- [Head Injuries - MedlinePlus (NLM)](https://medlineplus.gov/headinjuries.html) (Public domain)
- [Temporomandibular Joint Dysfunction - MedlinePlus (NLM)](https://medlineplus.gov/temporomandibularjointdysfunction.html) (Public domain)
- [Central Nervous System - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/nervous/organization/cns.html) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/skeletal/divisions/axial.html: Skull lists 8 cranial bones (parietal 2, temporal 2, frontal, occipital, ethmoid, sphenoid), 14 facial bones (maxilla 2, zygomatic 2, mandible, nasal 2, palatine 2, inferior nasal concha 2, lacrimal 2, vomer) and 6 auditory ossicles; hyoid separate.
- https://training.seer.cancer.gov/anatomy/skeletal/classification.html: Flat bones are thin, flattened, usually curved; most bones of the cranium are flat; some skull bones are irregular.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/46: Skull consists of the cranium above and behind and the face below and in front; coronal suture between frontal and parietals; sagittal between parietals; lambdoid between parietals and occipital; squamosal between temporal squama and parietal; foramen magnum transmits medulla oblongata, vertebral arteries; orbits; zygomatic arch; mastoid process; temporal fossa; bregma and lambda mark anterior and posterior fontanelles of fetal skull.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47: Anterior, middle and posterior cranial fossae; sella turcica lodges the hypophysis; optic foramen; anterior fontanelle largest, not completely closed until about middle of second year; posterior and lateral fontanelles close within a month or two after birth.
- https://medlineplus.gov/headinjuries.html: Skull is hard and protects the brain; closed injury does not break through the skull; open (penetrating) injury pierces skull and enters brain; skull fracture among more severe head injuries with concussion and TBI.
- https://medlineplus.gov/temporomandibularjointdysfunction.html: Two TMJs, one on each side of the jaw, connect the lower jaw to the skull; TMDs are more than 30 conditions causing pain and trouble with jaw joint and chewing muscles.
- https://training.seer.cancer.gov/anatomy/nervous/organization/cns.html: Brain in the cranium, continuous with the spinal cord at the foramen magnum.

---

## Mandible  (`mandible`)

*part · bone · musculoskeletal · 1 FMA ids · covers: mandible*

**Also called:** lower jaw

**Summary (plain)**

The mandible is the lower jaw bone. It is the largest and strongest bone of the face and holds the lower teeth.

**What it does (plain)**

It holds the lower teeth and moves at the two jaw joints just in front of the ears, so the mouth can open, close and chew.

**For students: description**

The mandible is the largest and strongest bone of the face. It has a curved, horseshoe-shaped body in front and two upright rami behind. The upper (alveolar) border of the body carries sockets for the 16 lower teeth. The two halves of the bone meet in the midline at the symphysis, which fuses during the first year of life.

**Location & neighbours**

Forms the lower part of the face and the chin. At the back, each ramus rises to meet the temporal bone of the skull at the temporomandibular joint, which can be felt just in front of the ear when the mouth opens.

| Detail | |
|---|---|
| Type | *(blank)* |
| Joints | Temporomandibular joint on each side: the condyle meets the temporal bone, with an articular disc between them. The lower teeth sit in sockets along the alveolar border. |
| Landmarks | Symphysis and mental protuberance; mental foramen below the second premolar (mental nerve and vessels); mylohyoid line; ramus with mandibular foramen (inferior alveolar nerve and vessels) and lingula; angle; coronoid process; condylar process with head and neck; mandibular notch. |

**Clinical relevance**

- Temporomandibular disorders (TMDs) are over 30 conditions causing pain and poor function in the jaw joint and chewing muscles; they affect about 5% of adults in the United States.
- TMDs are about twice as common in women as in men; clicking or popping of the jaw joint without pain is common and normal.
- After the teeth are lost, the alveolar part of the mandible is absorbed, so the bone shrinks and the mental foramen comes to lie close to its upper border.

**Exam tip**

The angle of the mandible changes with age: about 175 degrees at birth, about 110 to 120 degrees in adults, and back to about 140 degrees in old age.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Mandible (Inferior Maxillary Bone) - PubAnnotation GrayAnatomy doc 44](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/44) (Public domain)
- [TMD (Temporomandibular Disorders) - NIDCR](https://www.nidcr.nih.gov/health-info/tmd) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/44: Mandible is the largest and strongest bone of the face, receives the lower teeth; horseshoe-shaped body and two rami; symphysis marks fusion of halves, fuses in first year; mental protuberance; mental foramen below second premolar transmits mental vessels and nerve; mylohyoid line; alveolar border with 16 sockets; mandibular foramen admits inferior alveolar vessels and nerve; lingula; angle; coronoid process; condyloid process with condyle and neck; mandibular notch; articulates with the two temporal bones at the temporomandibular joint with an articular disk; angle about 175 degrees at birth, about 140 by age four, 110-120 in adult, about 140 in old age; alveolar process absorbed after tooth loss, mental foramen near alveolar border in old age.
- https://www.nidcr.nih.gov/health-info/tmd: TMJ is the jaw joint, one on each side, felt in front of the ears when opening the mouth; TMDs are more than 30 conditions causing pain and dysfunction in the jaw joint and muscles controlling jaw movement; about 5% of US adults; about twice as common in women; clicking or popping without pain is common and normal.

---

## Vertebral column  (`group:spine`)

*group · bone · musculoskeletal · 48 FMA ids · covers: atlas, axis, eighth thoracic vertebra, eleventh thoracic vertebra, fifth cervical vertebra, fifth lumbar vertebra, fifth thoracic vertebra, first lumbar vertebra …*

**Also called:** spine, backbone

**Summary (plain)**

The vertebral column, or backbone, is the chain of bones running down the middle of the back, from the base of the skull to the back of the pelvis.

**What it does (plain)**

It holds up the head and body so you can stand and bend, and it protects the spinal cord that runs inside it.

**For students: description**

The vertebral column is a flexible column of 33 vertebrae: 7 cervical, 12 thoracic, 5 lumbar, 5 sacral and 4 coccygeal. The upper 24 stay separate and movable; in adults the sacral vertebrae fuse into the sacrum and the coccygeal ones into the coccyx. Soft disks with a jelly-like centre lie between the vertebrae and cushion them. A typical vertebra has a body in front and a vertebral arch behind, enclosing the vertebral foramen.

**Location & neighbours**

In the midline of the back of the neck and trunk, from the base of the skull down to the coccyx. The thoracic part forms the back wall of the chest, and the sacrum sits at the back of the pelvis, wedged between the two hip bones.

| Detail | |
|---|---|
| Type | irregular (the vertebrae) |
| Joints | Supports the skull at its top; the ribs attach to the thoracic vertebrae; the fifth lumbar vertebra meets the sacrum at the sacrovertebral (lumbosacral) joint; the sacrum joins the coccyx below and a hip bone on each side. |
| Landmarks | Typical vertebra: body, and a vertebral arch of two pedicles and two laminae carrying seven processes (one spinous, two transverse, four articular). Seen from the side there are four curves: cervical and lumbar convex forward, thoracic concave forward, pelvic concave downward and forward. |

**Clinical relevance**

- Scoliosis is a sideways S- or C-shaped curve of the spine; the most common (idiopathic) type usually starts at age 11 or older and is more frequent in girls.
- A herniated disk is a ruptured disk whose jelly-like centre leaks out and irritates nearby nerves, causing back pain or sciatica.
- Age-related changes such as spinal stenosis and herniated disks can press on the spinal cord or nerves and cause pain.
- Incomplete fusion of the vertebral laminae (spina bifida) is most common in the lumbosacral region; the spinal membranes, and sometimes the cord, may protrude through the gap.

**Exam tip**

The thoracic and pelvic curves are primary curves, present before birth; the cervical and lumbar curves are secondary, appearing as the child holds up its head, sits and walks.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Vertebral Column - PubAnnotation GrayAnatomy doc 19](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/19) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), General Characteristics of the Vertebrae - PubAnnotation GrayAnatomy doc 20](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/20) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Sacrum and Coccyx - PubAnnotation GrayAnatomy doc 24](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/24) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Vertebral Column as a Whole - PubAnnotation GrayAnatomy doc 25](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/25) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Thorax - PubAnnotation GrayAnatomy doc 26](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/26) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Skull - PubAnnotation GrayAnatomy doc 30](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/30) (Public domain)
- [Classification of Bones - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/classification.html) (Public domain)
- [Spine Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/spineinjuriesanddisorders.html) (Public domain)
- [Herniated Disk - MedlinePlus (NLM)](https://medlineplus.gov/herniateddisk.html) (Public domain)
- [Scoliosis - NIAMS](https://www.niams.nih.gov/health-topics/scoliosis) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/19: Vertebral column is a flexuous and flexible column of vertebrae; 33 vertebrae: 7 cervical, 12 thoracic, 5 lumbar, 5 sacral, 4 coccygeal; upper three regions are true (movable) vertebrae, separate throughout life; sacral and coccygeal are false (fixed); in adults sacral fuse into sacrum and coccygeal into coccyx.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/20: Typical vertebra has an anterior body and posterior vertebral arch enclosing the vertebral foramen; arch has a pair of pedicles and a pair of laminae; seven processes: four articular, two transverse, one spinous.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/24: Sacrum is a large triangular bone in the lower vertebral column, set between the two hip bones at the back of the pelvis; articulates with the last lumbar vertebra above (sacrovertebral angle), the coccyx below and a hip bone on each side; coccyx usually four rudimentary vertebrae.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/25: Curves: cervical convex forward, thoracic concave forward, lumbar convex forward, pelvic concave downward and forward; thoracic and pelvic are primary curves present in fetal life; cervical and lumbar secondary, developing after birth as the child holds up its head, sits and walks; spina bifida from imperfect fusion of laminae, most common in lumbosacral region; membranes and sometimes cord may protrude.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/26: The twelve thoracic vertebrae and the ribs form the posterior wall of the thorax.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/30: The skull is supported on the summit of the vertebral column.
- https://training.seer.cancer.gov/anatomy/skeletal/classification.html: The vertebrae and some skull bones are irregular bones.
- https://medlineplus.gov/spineinjuriesanddisorders.html: Spine is also called the backbone; made of 26 bone discs called vertebrae; vertebrae protect the spinal cord and let you stand and bend; spinal stenosis and herniated disks with aging; bone changes can put pressure on the spinal cord or nerves and cause pain; scoliosis listed.
- https://medlineplus.gov/herniateddisk.html: 26 vertebrae with soft disks filled with a jelly-like substance between them; disks cushion the vertebrae and keep them in place; a herniated disk ruptures and its jelly-like centre leaks and irritates nearby nerves; can cause sciatica or back pain.
- https://www.niams.nih.gov/health-topics/scoliosis: Scoliosis is a sideways curve of the spine, S- or C-shaped; idiopathic is the most common type, more common in girls, usually occurs in children age 11 and older.

---

## Rib cage  (`group:ribcage`)

*group · bone · musculoskeletal · 41 FMA ids · covers: body of sternum, eighth rib, eleventh rib, fifth costal cartilage, fifth rib, first costal cartilage, first rib, fourth costal cartilage …*

**Also called:** thoracic cage

**Summary (plain)**

The rib cage is the cage of bone and cartilage around the chest. It is made of the breastbone in front, the ribs around the sides and the spine behind.

**What it does (plain)**

It protects the heart and lungs, and its springy cartilages let the chest wall stretch and spring back when you breathe.

**For students: description**

The skeleton of the thorax is a cone-shaped cage of bone and cartilage, narrow above and broad below. Its front wall is the sternum and costal cartilages, its sides are the 12 pairs of ribs with 11 intercostal spaces between them, and its back wall is the 12 thoracic vertebrae. Ribs 1-7 are true ribs reaching the sternum by their own cartilage; ribs 8-10 join the cartilage above; ribs 11-12 are floating ribs.

**Location & neighbours**

Encloses the chest between the neck and the abdomen. Its upper opening is bounded by the first thoracic vertebra, the first ribs and the top of the sternum; its lower opening is closed by the diaphragm, which forms the floor of the thorax.

| Detail | |
|---|---|
| Type | flat (the sternum is a long, flat bone); the costal cartilages are hyaline cartilage |
| Joints | Behind, the ribs join the thoracic vertebrae. In front, the costal cartilages of ribs 1-7 join the sternum and those of ribs 8-10 join the cartilage above. The manubrium also joins both clavicles. |
| Landmarks | Sternum: manubrium with jugular notch, body with notches for costal cartilages 2-7, xiphoid process; sternal angle between manubrium and body. Typical rib: head, neck, tubercle, shaft with angle and costal groove for intercostal vessels and nerve. First rib: most curved, usually shortest, with scalene tubercle. |

**Clinical relevance**

- Broken ribs are a chest injury, usually from car accidents, falls or sports; some chest injuries can be life-threatening because of the important organs inside.
- Costochondritis, slipping rib syndrome and pectus excavatum are other disorders of the ribs and chest wall.

**Exam tip**

The sternal angle, the ridge where the manubrium meets the body of the sternum, is a useful surface landmark.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Thorax - PubAnnotation GrayAnatomy doc 26](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/26) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Sternum (Breast Bone) - PubAnnotation GrayAnatomy doc 27](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/27) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Ribs - PubAnnotation GrayAnatomy doc 28](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/28) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Costal Cartilages - PubAnnotation GrayAnatomy doc 29](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/29) (Public domain)
- [Axial Skeleton - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/divisions/axial.html) (Public domain)
- [Chest Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/chestinjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/26: Thorax skeleton is an osseo-cartilaginous cage that protects the principal organs of respiration and circulation; conical, narrow above, broad below; posterior wall twelve thoracic vertebrae and ribs; sides formed by ribs separated by eleven intercostal spaces; anterior wall sternum and costal cartilages; inlet bounded by first thoracic vertebra, upper margin of sternum and first rib; outlet closed by the diaphragm, which forms the floor of the thorax.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/27: Sternum is a long, flat bone in the middle of the front of the thorax; three parts: manubrium, body (gladiolus), xiphoid process; jugular (presternal) notch on manubrium with clavicular facets; sternal angle at manubrium-body junction is a useful landmark; body has notches for cartilages of ribs 2-7; articulates with the clavicles and upper seven pairs of costal cartilages.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/28: Twelve pairs of ribs; first seven true (vertebrosternal) ribs connect to vertebral column behind and sternum in front by costal cartilages; ribs 8-10 join cartilage of rib above (vertebrochondral); 11 and 12 free in front, floating ribs; typical rib has head with two facets, neck, tubercle, shaft with angle and costal groove for intercostal vessels and nerve; first rib most curved, usually shortest, with scalene tubercle.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/29: Costal cartilages are bars of hyaline cartilage prolonging the ribs forward; they add elasticity to the thoracic walls.
- https://training.seer.cancer.gov/anatomy/skeletal/divisions/axial.html: Thoracic cage listed in the axial skeleton: sternum (1) and ribs (24).
- https://medlineplus.gov/chestinjuriesanddisorders.html: Chest is between neck and abdomen and holds ribs and breastbone; broken ribs listed as a chest injury; chest injuries can come from car accidents, falls or sports; some may be life-threatening; costochondritis, slipping rib syndrome and pectus excavatum listed.

---

## Clavicle  (`clavicle`)

*part · bone · musculoskeletal · 2 FMA ids · covers: clavicle*

**Also called:** collarbone, collar bone

**Summary (plain)**

The clavicle is the collarbone. It is a long bone with a gentle double curve that lies across the top of the chest, from the breastbone to the shoulder.

**What it does (plain)**

It links the breastbone to the shoulder blade, forming the front of the shoulder girdle, and gives attachment to muscles of the neck, chest and shoulder.

**For students: description**

The clavicle is a long bone lying almost horizontally at the upper front of the chest, just above the first rib. It has a double curve, somewhat like an italic letter f. Its medial two-thirds are rounded, while its lateral third is flattened from above downward. It forms the front part of the shoulder girdle, with the scapula forming the back.

**Location & neighbours**

At the upper front of the chest, just above the first rib. Its medial (sternal) end meets the manubrium of the sternum and its lateral (acromial) end meets the acromion of the scapula at the top of the shoulder. Much of it lies just under the skin.

| Detail | |
|---|---|
| Type | long |
| Joints | Sternoclavicular joint: the sternal end meets the manubrium of the sternum through an articular disc and also touches the first costal cartilage. Acromioclavicular joint: the acromial end meets the acromion of the scapula. |
| Landmarks | Sternal end; acromial end with a small oval facet; conoid tubercle and trapezoid line on the underside of the lateral third (for the conoid and trapezoid ligaments); costal tuberosity for the costoclavicular ligament; subclavian groove for the subclavius muscle. |

**Exam tip**

The clavicle starts to ossify earlier than any other bone in the body, from two centres that appear in the fifth or sixth week of fetal life.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Clavicle (Collar Bone) - PubAnnotation GrayAnatomy doc 49](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/49) (Public domain)
- [Shoulder Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/shoulderinjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/49: Clavicle (collar bone) forms the anterior part of the shoulder girdle; long bone, nearly horizontal at upper front of thorax just above first rib; double curvature like an italic f; lateral third flattened from above downward, medial two-thirds rounded/prismatic; articulates medially with manubrium via articular disk, lower sternal end with first rib cartilage, laterally with acromion; coracoid tuberosity (conoid tubercle), oblique (trapezoid) ridge, costal tuberosity, subclavian groove for subclavius; conoid, trapezoid, costoclavicular, acromioclavicular ligaments; deltoid, trapezius, pectoralis major, sternocleidomastoid, subclavius, sternohyoid attach; parts subcutaneous, covered only by platysma; ossifies earlier than any other bone, two primary centres in fifth or sixth fetal week.
- https://medlineplus.gov/shoulderinjuriesanddisorders.html: Shoulder bones include the clavicle (collarbone), scapula (shoulder blade) and humerus.

---

## Scapula  (`scapula`)

*part · bone · musculoskeletal · 2 FMA ids · covers: scapula*

**Also called:** shoulder blade

**Summary (plain)**

The scapula is the shoulder blade, a flat, triangular bone at the back of the shoulder.

**What it does (plain)**

It forms the socket of the shoulder joint and anchors many of the muscles of the shoulder and arm.

**For students: description**

The scapula forms the back part of the shoulder girdle. It is a flat, triangular bone with two surfaces (costal and dorsal), three borders (superior, lateral and medial) and three angles (superior, inferior and lateral). A prominent spine crosses the back surface and ends as the acromion, the summit of the shoulder; the lateral angle carries the shallow glenoid cavity.

**Location & neighbours**

At the back of the upper chest wall, its front (costal) surface facing the thorax. Its lateral angle lies at the shoulder, where the glenoid cavity meets the humerus and the acromion meets the clavicle.

| Detail | |
|---|---|
| Type | flat |
| Joints | Shoulder (glenohumeral) joint: the glenoid cavity meets the head of the humerus. Acromioclavicular joint: a small oval facet on the acromion meets the acromial end of the clavicle. |
| Landmarks | Subscapular fossa on the front; spine dividing the back into supraspinous and infraspinous fossae; acromion; coracoid process; glenoid cavity with supraglenoid and infraglenoid tubercles; suprascapular notch on the superior border for the suprascapular nerve. |

**Clinical relevance**

- The shoulder is the most movable joint in the body but is unstable because the head of the humerus is larger than its socket; problems include dislocations, separations, fractures and torn rotator cuffs.

**Exam tip**

The spine of the scapula ends as the acromion, which forms the summit of the shoulder and overhangs the glenoid cavity.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Scapula (Shoulder Blade) - PubAnnotation GrayAnatomy doc 50](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/50) (Public domain)
- [Shoulder Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/shoulderinjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/50: Scapula (shoulder blade) forms the posterior part of the shoulder girdle; flat, triangular bone with two surfaces, three borders, three angles; costal surface with subscapular fossa faces the thorax; spine divides dorsal surface into supraspinatous and infraspinatous fossae and ends in the acromion, which forms the summit of the shoulder and overhangs the glenoid cavity; coracoid process; glenoid cavity on lateral angle articulates with head of humerus; oval facet on acromion for acromial end of clavicle; scapular notch for suprascapular nerve; supraglenoid and infraglenoid tubercles; many muscles attach (subscapularis, supraspinatus, infraspinatus, teres minor and major, deltoid, trapezius, serratus anterior, levator scapulae, rhomboids, pectoralis minor).
- https://medlineplus.gov/shoulderinjuriesanddisorders.html: Shoulder bones are clavicle, scapula and humerus; shoulders are the most movable joints; the ball of the upper arm is larger than the socket that holds it, so it must be anchored by muscles, tendons and ligaments; problems listed include dislocations, separations, fractures and torn rotator cuffs.

---

## Humerus  (`humerus`)

*part · bone · musculoskeletal · 2 FMA ids · covers: humerus*

**Also called:** arm bone, upper arm bone

**Summary (plain)**

The humerus is the upper arm bone. It runs from the shoulder down to the elbow and is the longest and largest bone of the arm.

**What it does (plain)**

It links the shoulder to the elbow, forms part of both joints and gives muscles of the shoulder, arm and forearm a place to attach.

**For students: description**

The humerus is a long bone with a shaft and two ends. Its upper end has a rounded head, the anatomical and surgical necks and the greater and lesser tubercles, with the intertubercular groove between them. Its lower end widens into the capitulum and trochlea, which meet the forearm bones, with an epicondyle on each side.

**Location & neighbours**

In the upper arm, between the shoulder and the elbow. The head meets the glenoid cavity of the scapula above; the lower end meets the radius and ulna at the elbow. The radial nerve runs in a shallow spiral groove on the shaft.

| Detail | |
|---|---|
| Type | long |
| Joints | Shoulder joint: the head meets the glenoid cavity of the scapula. Elbow joint: the capitulum meets the head of the radius and the trochlea meets the trochlear notch of the ulna. |
| Landmarks | Head; anatomical and surgical necks; greater and lesser tubercles; intertubercular (bicipital) groove for the long head of biceps; deltoid tuberosity; radial groove for the radial nerve; capitulum; trochlea; medial and lateral epicondyles; coronoid, radial and olecranon fossae. |

**Clinical relevance**

- The surgical neck, just below the tubercles, is a frequent site of fracture; fracture of the anatomical neck is rare.
- Tennis elbow (lateral epicondylitis) is overuse damage of the tendons on the outer elbow, where the common extensor tendon attaches to the lateral epicondyle.
- Golfer's elbow (medial epicondylitis) is tendinitis on the inner elbow, the side of the medial epicondyle and the common flexor tendon, from repeated wrist use or gripping.
- The ulnar nerve runs in a groove behind the medial epicondyle.

**Exam tip**

Gray's Anatomy calls the humerus the longest and largest bone of the upper limb.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Humerus (Arm Bone) - PubAnnotation GrayAnatomy doc 51](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/51) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), General classification of bones - PubAnnotation GrayAnatomy doc 17](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17) (Public domain)
- [Classification of Bones - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/classification.html) (Public domain)
- [Arm Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/arminjuriesanddisorders.html) (Public domain)
- [Shoulder Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/shoulderinjuriesanddisorders.html) (Public domain)
- [Sports Injuries - NIAMS](https://www.niams.nih.gov/health-topics/sports-injuries) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/51: Heading 'Arm Bone'; longest and largest bone of the upper extremity; body and two extremities; head articulates with glenoid cavity of scapula; anatomical neck; surgical neck below tubercles frequently fractured, anatomical neck fracture rare; greater and lesser tubercles; intertubercular (bicipital) groove holds long head of biceps; deltoid tuberosity; radial (musculospiral) sulcus carries radial nerve and profunda artery; capitulum articulates with radial head; trochlea with semilunar notch of ulna; medial epicondyle with common flexor tendon and ulnar nerve groove behind it; lateral epicondyle with common extensor tendon; coronoid, radial and olecranon fossae.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17: Long bones listed include the humerus, radius and ulna; central shaft with two expanded ends.
- https://training.seer.cancer.gov/anatomy/skeletal/classification.html: Long bones are longer than they are wide; examples include the bones of the arm and forearm.
- https://medlineplus.gov/arminjuriesanddisorders.html: The arm is made up of three bones: humerus, radius and ulna; injuries include dislocations and broken bones.
- https://medlineplus.gov/shoulderinjuriesanddisorders.html: Shoulder is made of clavicle, scapula and upper arm bone (humerus); dislocations and fractures listed.
- https://www.niams.nih.gov/health-topics/sports-injuries: Tennis elbow (lateral epicondylitis): small tendon tears and inflammation from repeated forearm use, pain on the outside of the elbow; golfer's elbow (medial epicondylitis): tendinitis on the inner elbow from repeated wrist use or finger clenching.

---

## Radius  (`radius`)

*part · bone · musculoskeletal · 2 FMA ids · covers: radius*

**Summary (plain)**

The radius is one of the two forearm bones. It lies on the outer side of the forearm, next to the ulna, and runs from the elbow to the wrist.

**What it does (plain)**

It joins the elbow above and forms the main bony part of the wrist joint below, and it gives the biceps and several forearm muscles a place to attach.

**For students: description**

The radius is a long, slightly curved bone with a shaft and two ends. Its upper end is a short cylindrical head on a narrow neck, with the radial tuberosity below for the biceps brachii tendon. Its lower end is broad, with a styloid process on the outer side and a concave surface that meets the wrist bones.

**Location & neighbours**

On the lateral side of the forearm, alongside the longer and larger ulna. It is narrow above at the elbow and widens below at the wrist; an interosseous membrane joins its shaft to the ulna.

| Detail | |
|---|---|
| Type | long |
| Joints | Elbow: the head meets the capitulum of the humerus and the radial notch of the ulna. Wrist joint: the lower end meets the scaphoid and lunate. Distal radioulnar joint: the ulnar notch meets the head of the ulna. |
| Landmarks | Head with a shallow cup (fovea); neck; radial tuberosity for the biceps brachii tendon; interosseous crest for the interosseous membrane; ulnar notch; carpal articular surface; styloid process on the lateral side. |

**Clinical relevance**

- The wrist, where the radius meets the carpal bones, can be fractured or sprained; falling on an outstretched hand during sports such as skating is one cause.

**Exam tip**

The biceps brachii tendon inserts on the rough back part of the radial tuberosity, just below the neck of the radius.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Radius - PubAnnotation GrayAnatomy doc 53](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/53) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), General classification of bones - PubAnnotation GrayAnatomy doc 17](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17) (Public domain)
- [Arm Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/arminjuriesanddisorders.html) (Public domain)
- [Wrist Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/wristinjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/53: Radius on lateral side of forearm, ulna longer and larger; long, prismatic, slightly curved; head cylindrical with shallow cup (fovea) for capitulum; circumference meets radial notch of ulna; neck; radial tuberosity, rough posterior part for biceps brachii tendon; interosseous crest for interosseous membrane; lower end large and quadrilateral; carpal surface meets navicular and lunate; ulnar notch meets head of ulna; styloid process on lateral side; elbow, wrist and distal radioulnar joints.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17: Long bones listed include the radius.
- https://medlineplus.gov/arminjuriesanddisorders.html: Arm made up of humerus, radius and ulna.
- https://medlineplus.gov/wristinjuriesanddisorders.html: Wrist made of two forearm bones and eight carpals; fractures and sprains listed; falling on an outstretched hand in sports like skating or snowboarding raises risk.

---

## Ulna  (`ulna`)

*part · bone · musculoskeletal · 2 FMA ids · covers: ulna*

**Also called:** elbow bone

**Summary (plain)**

The ulna is one of the two forearm bones. It lies on the inner side of the forearm, next to the radius, and its curved top (the olecranon) lies just under the skin at the back of the elbow.

**What it does (plain)**

It forms the elbow joint with the upper arm bone and gives many forearm muscles, including the triceps and brachialis, a place to attach.

**For students: description**

The ulna is a long bone that is large and strong at the top and thin at the bottom. Its upper end has the olecranon and the coronoid process, which together form the trochlear notch that grips the humerus. Its small lower end has a rounded head and a styloid process, and is kept off the wrist joint by an articular disc.

**Location & neighbours**

On the medial side of the forearm, parallel to the radius, from the elbow to the wrist. The back of the olecranon lies just under the skin at the elbow.

| Detail | |
|---|---|
| Type | long |
| Joints | Elbow: the trochlear notch meets the trochlea of the humerus. Proximal radioulnar joint: the radial notch meets the head of the radius. Distal radioulnar joint: the head of the ulna fits the ulnar notch of the radius. |
| Landmarks | Olecranon (triceps brachii insertion); coronoid process; trochlear notch; radial notch; ulnar tuberosity (part of brachialis insertion); interosseous crest; head; styloid process. |

**Clinical relevance**

- Repeated throwing can tear the ulnar collateral ligament on the inner elbow, which attaches to the coronoid process and olecranon of the ulna.
- Elbow problems include fractures, dislocations, bursitis and arthritis; the back of the olecranon lies under the skin, covered by a bursa.

**Exam tip**

The lower end of the ulna does not take part in the wrist joint: a triangular articular disc lies between it and the wrist bones.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Ulna (Elbow Bone) - PubAnnotation GrayAnatomy doc 52](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/52) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), General classification of bones - PubAnnotation GrayAnatomy doc 17](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Radius - PubAnnotation GrayAnatomy doc 53](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/53) (Public domain)
- [Elbow Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/elbowinjuriesanddisorders.html) (Public domain)
- [Sports Injuries - NIAMS](https://www.niams.nih.gov/health-topics/sports-injuries) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/52: Heading 'Elbow Bone'; long prismatic bone on medial side of forearm parallel to radius; large and strong above, smaller below; lower end does not reach wrist joint, articular disk between; olecranon fits olecranon fossa, back subcutaneous and covered by a bursa, triceps inserts on it; coronoid process fits coronoid fossa, brachialis inserts; ulnar tuberosity; semilunar notch articulates with trochlea; radial notch receives radial head, annular ligament; interosseous crest; head fits ulnar notch of radius; styloid process; ulnar collateral ligament attaches to coronoid medial margin and olecranon.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17: Long bones listed include the ulna.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/53: Distal radioulnar joint: ulnar notch of radius meets head of ulna; head of radius meets radial notch of ulna.
- https://medlineplus.gov/elbowinjuriesanddisorders.html: Elbow problems include tendinitis, sprains and strains, fractures, dislocations, bursitis and arthritis.
- https://www.niams.nih.gov/health-topics/sports-injuries: Ulnar collateral ligament injury: tears in an inner elbow ligament from repeated throwing.

---

## Hip bone  (`hip bone`)

*part · bone · musculoskeletal · 2 FMA ids · covers: hip bone*

**Also called:** innominate bone, coxal bone

**Summary (plain)**

The hip bone is the large, flat bone on each side of the pelvis. The two hip bones meet at the front and join the sacrum at the back.

**What it does (plain)**

It holds the socket for the thigh bone at the hip joint and forms the side and front walls of the pelvis.

**For students: description**

The hip bone (os coxae) is a large, flattened, irregular bone, narrow in the middle and wide above and below. It is made of three parts, the ilium, ischium and pubis, which are separate in children and fused in adults. They meet at the acetabulum, the deep cup that holds the head of the femur.

**Location & neighbours**

In the pelvis, one on each side. The two hip bones meet at the front in the midline (pubic symphysis) and join the sacrum at the back, forming the sides and front wall of the pelvic cavity. The femur hangs from the acetabulum below.

| Detail | |
|---|---|
| Type | flat |
| Joints | Hip joint: the acetabulum holds the head of the femur. Sacroiliac joint: the auricular surface of the ilium meets the sacrum. Pubic symphysis: the pubis meets the other hip bone through a fibrocartilage disc. |
| Landmarks | Iliac crest; anterior and posterior superior and inferior iliac spines; auricular surface; greater and lesser sciatic notches, separated by the ischial spine; ischial tuberosity; pubic tubercle; acetabulum; obturator foramen, oval in males and more triangular in females. |

**Clinical relevance**

- In hip dysplasia the femoral head fits loosely in the socket, which can lead to dislocation; it is usually present at birth.
- Osteoarthritis of the hip joint causes pain and less movement and is common in older adults; treatment may include hip replacement.

**Exam tip**

The acetabulum is shared by all three parts: the ischium gives a little over two-fifths, the ilium a little under two-fifths and the pubis about one-fifth.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Hip Bone (Os Coxae; Innominate Bone) - PubAnnotation GrayAnatomy doc 57](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/57) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), General classification of bones - PubAnnotation GrayAnatomy doc 17](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17) (Public domain)
- [Appendicular Skeleton - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/divisions/appendicular.html) (Public domain)
- [Hip Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/hipinjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/57: Heading 'Os Coxae; Innominate Bone'; large, flattened, irregularly shaped, constricted in center, expanded above and below; two meet in front midline, form sides and front wall of pelvic cavity; ilium, ischium, pubis separate in young, fused in adult, unite at acetabulum; acetabulum shares (ilium a little less than two-fifths, ischium a little more than two-fifths, pubis one-fifth); obturator foramen oval in male, triangular in female; iliac crest and spines; sciatic notches; ischial spine; ischial tuberosity; pubic tubercle; symphysis with fibrocartilaginous disc; auricular surface meets sacrum; acetabulum meets femur head.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/17: Flat bones listed include the os coxae (hip bone).
- https://training.seer.cancer.gov/anatomy/skeletal/divisions/appendicular.html: Pelvic girdle listed as coxal, innominate or hip bones, 2 bones.
- https://medlineplus.gov/hipinjuriesanddisorders.html: Hip is where femur meets pelvis, ball in cup-shaped socket; osteoarthritis causes pain and reduced movement, common in older adults; hip dysplasia: ball fits loosely in socket, can lead to dislocation, usually present at birth; treatment can include hip replacement.

---

## Femur  (`femur`)

*part · bone · musculoskeletal · 2 FMA ids · covers: femur*

**Also called:** thigh bone

**Summary (plain)**

The femur is the thigh bone. It runs down the thigh from the hip to the knee and is the longest and strongest bone in the body.

**What it does (plain)**

It carries the body's weight from the hip down to the shin bone and forms part of both the hip and the knee joints.

**For students: description**

The femur is a long bone with a nearly cylindrical shaft and two expanded ends. Its upper end has a rounded head, a neck and the greater and lesser trochanters; its lower end has the medial and lateral condyles. Body weight passes from the acetabulum through the femur to the tibia.

**Location & neighbours**

In the thigh, between the pelvis above and the knee below. When standing it is not vertical: the shaft slants downward and medially, so the two femurs come closer together near the knees.

| Detail | |
|---|---|
| Type | long |
| Joints | Hip joint: the head fits into the socket (acetabulum) of the hip bone, a ball-and-socket joint. Knee joint: the condyles meet the condyles of the tibia and the menisci, and the patellar surface meets the patella. |
| Landmarks | Head with a small pit (fovea) for the ligamentum teres; neck; greater and lesser trochanters; linea aspera, a long ridge on the back of the shaft; medial and lateral condyles with epicondyles; intercondylar fossa; patellar surface. The neck meets the shaft at about 125 degrees in adults (wider in infancy). |

**Clinical relevance**

- Fractures of the hip can follow falls, sports or overuse; osteoporosis of the hip makes the bones weak and easy to break and is common in older people.

**Exam tip**

Gray's Anatomy calls the femur the longest and strongest bone in the skeleton.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Femur (Thigh Bone) - PubAnnotation GrayAnatomy doc 59](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/59) (Public domain)
- [Classification of Bones - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/classification.html) (Public domain)
- [Hip Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/hipinjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/59: Heading '(Thigh Bone)'; longest and strongest bone in the skeleton; almost cylindrical; not vertical when erect, inclines downward and medially toward its fellow; weight transmitted from acetabulum to femur head and on to tibia; head globular with fovea for ligamentum teres; neck connects head to body; greater and lesser trochanters; linea aspera on middle third; medial and lateral condyles with epicondyles; intercondylar fossa; patellar surface articulates with patella; condyles articulate with tibial condyles and menisci; hip-joint capsule attaches to neck; knee joint; neck-shaft angle about 125 degrees in adult, widest in infancy, lessens with growth.
- https://training.seer.cancer.gov/anatomy/skeletal/classification.html: Long bones are longer than wide, with a shaft and two bulky ends; long bones include the bones of the thigh.
- https://medlineplus.gov/hipinjuriesanddisorders.html: Hip is the joint where the femur (thigh bone) meets the pelvis (hip bone); ball-and-socket joint; ball fits into a socket in the pelvis; fractures can result from sports, running, overuse or falling; osteoporosis of the hip causes weak bones that break easily; common in older people.

---

## Patella  (`patella`)

*part · bone · musculoskeletal · 2 FMA ids · covers: patella*

**Also called:** kneecap, knee cap

**Summary (plain)**

The patella is the kneecap. It is a flat, triangular bone at the front of the knee, sitting in a groove on the end of the thigh bone.

**What it does (plain)**

It shields the front of the knee and gives the big thigh muscle (quadriceps) better leverage.

**For students: description**

The patella is a flat, triangular bone usually counted as a sesamoid bone, because it forms inside the tendon of the quadriceps femoris. It protects the front of the knee joint and improves the leverage of the quadriceps. Its back has a smooth surface, split by a ridge into medial and lateral facets, that glides on the femur.

**Location & neighbours**

At the front of the knee joint, embedded in the quadriceps tendon. Its broad base faces up and its pointed apex faces down toward the patellar ligament; its back rests on the patellar surface of the femur.

| Detail | |
|---|---|
| Type | sesamoid |
| Joints | Knee joint: its back articular surface meets the patellar surface of the femur. |
| Landmarks | Base (top border) for rectus femoris and vastus intermedius; medial and lateral borders for vastus medialis and vastus lateralis; apex for the patellar ligament; back articular surface with a vertical ridge and a broader lateral facet and a medial facet. |

**Clinical relevance**

- Kneecap fractures are the most common knee fracture and usually follow a hard fall or a direct blow to the knee.
- A strong impact can knock the kneecap out of its groove on the femur (kneecap dislocation); it usually needs prompt care, though it sometimes slides back by itself.
- Runner's knee causes pain or tenderness near or under the front of the kneecap; it is common in runners, hikers and cyclists.

**Exam tip**

The patella usually starts to ossify from a single centre in the second or third year of life, and ossification is complete about puberty.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Patella (Knee Cap) - PubAnnotation GrayAnatomy doc 60](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/60) (Public domain)
- [Appendicular Skeleton - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/divisions/appendicular.html) (Public domain)
- [Sports Injuries - NIAMS](https://www.niams.nih.gov/health-topics/sports-injuries) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/60: Heading 'Knee Cap'; flat triangular bone on front of knee joint; usually regarded as sesamoid bone developed in tendon of quadriceps femoris; protects front of knee and increases leverage of quadriceps; posterior articular surface divided by vertical ridge into medial and lateral facets, lateral broader and deeper, ridge fits groove on patellar surface of femur; base for rectus femoris and vastus intermedius; borders for vastus medialis and lateralis; apex for patellar ligament; ossifies from one center in 2nd or 3rd year, complete about puberty.
- https://training.seer.cancer.gov/anatomy/skeletal/divisions/appendicular.html: Patella listed as a bone of the lower extremity, 2 bones.
- https://www.niams.nih.gov/health-topics/sports-injuries: Runner's knee: pain or tenderness near or under front of kneecap, common in runners, hikers, cyclists; kneecap fractures most common knee fracture, from hard fall or blow; kneecap dislocation when strong impact knocks kneecap out of its groove on thigh bone, usually needs prompt care, sometimes slides back on its own.

---

## Tibia  (`tibia`)

*part · bone · musculoskeletal · 2 FMA ids · covers: tibia*

**Also called:** shin bone

**Summary (plain)**

The tibia is the shin bone. It is the larger of the two bones in the lower leg and runs on the inner side from the knee down to the ankle.

**What it does (plain)**

It carries body weight from the thigh bone down to the ankle and forms part of both the knee and the ankle joints.

**For students: description**

The tibia is a long, three-sided (prismoid) bone, widest at its upper end and narrowest in its lower third. Its upper end spreads into the medial and lateral condyles that meet the femur; its shaft has anterior, medial and interosseous borders; its lower end extends downward on the inner side as the medial malleolus.

**Location & neighbours**

On the medial (inner) side of the leg, between the knee above and the ankle below, with the fibula alongside it on the lateral side. Its medial surface and medial malleolus lie just under the skin.

| Detail | |
|---|---|
| Type | long |
| Joints | Knee joint: its condyles meet the femoral condyles, with the menisci between them. Superior and inferior tibiofibular joints with the fibula. Ankle joint: the lower articular surface and medial malleolus meet the talus. |
| Landmarks | Medial and lateral condyles; intercondylar eminence with two tubercles; tibial tuberosity for the patellar ligament; facet for the fibular head on the lateral condyle; sharp anterior border (shin); popliteal line and a large nutrient foramen behind; medial malleolus. |

**Clinical relevance**

- Shin splints are pain from inflammation where muscle attaches along the shinbone; they are seen mainly in runners, especially those just starting a running program.
- Stress fractures occur mostly in the weight-bearing bones of the lower limb, including the tibia.
- Fractures of the tibial shaft are among the leg injuries MedlinePlus lists.

**Exam tip**

Apart from the femur, the tibia is the longest bone in the skeleton.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Tibia (Shin Bone) - PubAnnotation GrayAnatomy doc 61](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/61) (Public domain)
- [Classification of Bones - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/classification.html) (Public domain)
- [Sports Injuries - NIAMS](https://www.niams.nih.gov/health-topics/sports-injuries) (Public domain)
- [Leg Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/leginjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/61: 'Shin Bone'; on the medial side of the leg; except the femur the longest bone in the skeleton; prismoid, widest above, narrowest in lower third; medial and lateral condyles articulate with femur, menisci on facets; intercondyloid eminence with tubercles; tuberosity for patellar ligament; lateral condyle facet for fibular head; anterior, medial and interosseous borders; medial surface largely subcutaneous; popliteal line and large oblique nutrient foramen; medial malleolus subcutaneous; inferior articular surface with talus; articulates with femur, fibula and talus.
- https://training.seer.cancer.gov/anatomy/skeletal/classification.html: Long bones are longer than wide, with a shaft and two bulky ends; long bones include bones of the thigh, leg, arm and forearm.
- https://www.niams.nih.gov/health-topics/sports-injuries: Shinbone (tibia) at the front of the lower leg; shin splints mainly in runners, particularly those starting a running program, pain from inflammation where muscle attaches along the shinbone; stress fractures occur largely in weight-bearing bones of the lower extremity including femur, tibia, fibula and foot bones.
- https://medlineplus.gov/leginjuriesanddisorders.html: Fractures are named as common leg injuries; 'Tibial (Shinbone) Shaft Fractures' listed among specific leg conditions.

---

## Fibula  (`fibula`)

*part · bone · musculoskeletal · 2 FMA ids · covers: fibula*

**Also called:** calf bone

**Summary (plain)**

The fibula is the thin outer bone of the lower leg. It runs beside the shin bone from just below the knee down to the outer ankle.

**What it does (plain)**

It gives attachment to many leg muscles and forms the outer part of the ankle joint.

**For students: description**

The fibula is the smaller of the two leg bones and, for its length, the most slender of all the long bones. It has a small head with an upward-pointing apex, a shaft with four borders and four surfaces, and a lower end, the lateral malleolus. It is joined to the tibia at both ends but takes no part in the knee joint.

**Location & neighbours**

On the lateral (outer) side of the leg, beside the tibia. Its head sits toward the back of the tibia's lateral condyle, below the level of the knee joint; its lower end reaches lower than the medial malleolus.

| Detail | |
|---|---|
| Type | long |
| Joints | Superior tibiofibular joint: the head meets the lateral condyle of the tibia. It is also joined to the tibia below. Ankle joint: the lateral malleolus meets the lateral side of the talus. It is excluded from the knee joint. |
| Landmarks | Head with its apex (styloid process); shaft with interosseous border for the interosseous membrane and a nutrient foramen on the back; lateral malleolus with a groove behind it for the fibularis tendons. |

**Clinical relevance**

- Stress fractures occur mostly in the weight-bearing bones of the lower limb, including the fibula.

**Exam tip**

Gray's Anatomy calls the fibula, relative to its length, the most slender of all the long bones.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), The Fibula (Calf Bone) - PubAnnotation GrayAnatomy doc 62](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/62) (Public domain)
- [Classification of Bones - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/skeletal/classification.html) (Public domain)
- [Sports Injuries - NIAMS](https://www.niams.nih.gov/health-topics/sports-injuries) (Public domain)

**What was checked on each page**

- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/62: '(Calf Bone)'; on lateral side of tibia, connected above and below; smaller of the two leg bones; most slender of all long bones relative to length; head below knee-joint level, excluded from knee joint, facet for lateral condyle of tibia; apex (styloid process); four borders and four surfaces; many leg muscles arise from it (extensors, fibularis/peroneus, soleus, flexor hallucis longus, tibialis posterior groove); nutrient foramen on posterior surface; interosseous crest; lateral malleolus descends lower than medial, forms lateral part of ankle joint, articulates with talus; malleolar sulcus for peroneal tendons.
- https://training.seer.cancer.gov/anatomy/skeletal/classification.html: Long bones are longer than wide; include bones of the leg.
- https://www.niams.nih.gov/health-topics/sports-injuries: Stress fractures occur largely in weight-bearing bones of the lower extremity, including femur, tibia and fibula, and foot bones.

---

## Diaphragm  (`diaphragm`)

*part · muscle · musculoskeletal · 1 FMA ids · covers: diaphragm*

**Summary (plain)**

The diaphragm is a thin, dome-shaped muscle at the base of the lungs. It forms a wall between the chest and the belly.

**What it does (plain)**

It is the main muscle for breathing: it tightens and moves down to pull air in, then relaxes to let air out.

**For students: description**

The diaphragm is a dome-shaped sheet of muscle that separates the thoracic cavity from the abdominal cavity. It has three openings that let structures pass from chest to abdomen, including the oesophageal hiatus. Its contraction drives breathing in; breathing out at rest is mostly passive.

**Location & neighbours**

Below the lungs and above the abdominal organs; the stomach lies just beneath it on the left. It is crossed by the oesophagus through the oesophageal hiatus.

| Detail | |
|---|---|
| Origin | *(blank)* |
| Insertion | *(blank)* |
| Action | Contracts and moves down during inhalation, enlarging the chest cavity so the lungs expand and air flows in; relaxes during exhalation, so elastic recoil shrinks the chest and pushes air out. |
| Nerve supply | *(blank)* |
| Blood supply | *(blank)* |

**Clinical relevance**

- A hiatal hernia occurs when the top of the stomach pushes up through the diaphragm's opening; risk rises after age 50 and with obesity and smoking.  → disease page `gerd`
- Hiccups are sudden involuntary movements of the diaphragm with quick closing of the vocal cords, often triggered by something irritating the diaphragm.
- Damage to nerves in the upper spinal cord, as in spinal cord injury or stroke, can impair diaphragm movement and lead to respiratory failure.

**Exam tip**

Breathing in is active because the diaphragm contracts; quiet breathing out is passive and needs no muscle effort.

**Sources**

- [Muscle Groups: Trunk - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/trunk.html) (Public domain)
- [Mechanics of Ventilation - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/respiratory/mechanics.html) (Public domain)
- [How the Lungs Work: What Breathing Does for the Body - NHLBI](https://www.nhlbi.nih.gov/health/lungs/breathing-benefits) (Public domain)
- [How the Lungs Work: How Your Body Controls Breathing - NHLBI](https://www.nhlbi.nih.gov/health/lungs/body-controls-breathing) (Public domain)
- [Pharynx & Esophagus - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/pharynx.html) (Public domain)
- [Anatomy of the Stomach - NCI SEER Training Modules](https://training.seer.cancer.gov/ugi/anatomy/stomach.html) (Public domain)
- [Hiatal Hernia - MedlinePlus (NLM)](https://medlineplus.gov/hiatalhernia.html) (Public domain)
- [Hiccups - MedlinePlus (NLM)](https://medlineplus.gov/hiccups.html) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/muscular/groups/trunk.html: Diaphragm is a dome-shaped muscle forming a partition between thorax and abdomen; has three openings for structures passing from thorax to abdomen.
- https://training.seer.cancer.gov/anatomy/respiratory/mechanics.html: Inspiration active: diaphragm contracts, thoracic volume increases, intraalveolar pressure falls, air flows in; expiration passive: diaphragm relaxes, elastic recoil decreases thoracic volume, air forced out.
- https://www.nhlbi.nih.gov/health/lungs/breathing-benefits: On inhaling the diaphragm contracts and moves downward, increasing chest cavity space, lungs expand; on exhaling it relaxes; breathing out requires no effort unless lung disease or physical activity.
- https://www.nhlbi.nih.gov/health/lungs/body-controls-breathing: Diaphragm is the main breathing muscle; damage to nerves in upper spinal cord (spinal cord injury, stroke, muscular dystrophy) can interfere with diaphragm movement and lead to respiratory failure; phrenic nerve not named.
- https://training.seer.cancer.gov/anatomy/digestive/regions/pharynx.html: Esophagus passes through an opening in the diaphragm called the esophageal hiatus.
- https://training.seer.cancer.gov/ugi/anatomy/stomach.html: Stomach lies just below the diaphragm, mainly left of midline.
- https://medlineplus.gov/hiatalhernia.html: Diaphragm is a thin muscle separating chest from abdomen; hiatal hernia when top of stomach pushes up through an opening in it; risk higher over 50, obesity and smoking.
- https://medlineplus.gov/hiccups.html: Diaphragm is a muscle at the base of the lungs and the main muscle used for breathing; hiccup is involuntary diaphragm movement plus quick closing of vocal cords; often when something irritates the diaphragm.

---

## Deltoid  (`group:deltoid`)

*group · muscle · musculoskeletal · 6 FMA ids · covers: acromial part of deltoid, clavicular part of deltoid, spinal part of deltoid*

**Summary (plain)**

The deltoid is the large, thick, triangle-shaped muscle that forms the rounded cap of the shoulder. It covers the shoulder joint at the front, side and back.

**What it does (plain)**

It lifts the arm out to the side, and its front and back parts help swing the arm forward and backward.

**For students: description**

The deltoid is a coarse, triangular muscle named for its shape. It has three parts: a clavicular (anterior) part from the clavicle, an acromial (middle) part from the acromion and a spinal (posterior) part from the spine of the scapula. The fibres converge into a thick tendon on the side of the humerus, and the acromial part is multipennate, built around several tendinous bands.

**Location & neighbours**

Over the shoulder joint, covering it in front, at the side and behind. It runs from the lateral clavicle, acromion and scapular spine down to the middle of the lateral side of the humerus, under the deep fascia.

| Detail | |
|---|---|
| Origin | Clavicular part: front border and upper surface of the lateral third of the clavicle. Acromial part: lateral margin and upper surface of the acromion. Spinal part: lower lip of the posterior border of the spine of the scapula. |
| Insertion | Deltoid tuberosity, midway down the lateral side of the shaft of the humerus. |
| Action | Abducts the arm to a right angle with the trunk. The clavicular part, with pectoralis major, draws the arm forward; the spinal part, with teres major and latissimus dorsi, draws it backward. |
| Nerve supply | Axillary nerve (C5, C6). |
| Blood supply | Deltoid and acromial branches of the thoracoacromial artery and the posterior circumflex humeral artery; small branches also from the circumflex scapular artery and the profunda brachii. |

**Clinical relevance**

- The deltoid is the recommended site for intramuscular vaccine injections in adults and the preferred site for children aged 3 to 18 years (CDC guidance, United States).
- Intramuscular injections go into the middle of the muscle where it is thickest, at 90 degrees, which lowers the chance of hitting nerves or blood vessels.

**Exam tip**

The name deltoid means triangular: the muscle is named for its shape.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), full text - Internet Archive](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Muscle Groups - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/) (Public domain)
- [Muscles of the Upper Extremity - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html) (Public domain)
- [Pink Book Chapter 6: Vaccine Administration - CDC](https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-6-vaccine-administration.html) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: Deltoideus (pp. 439-440): large, thick, triangular, remarkably coarse; covers shoulder joint in front, behind and laterally; arises from anterior border and upper surface of lateral third of clavicle, lateral margin and upper surface of acromion, lower lip of posterior border of scapular spine; inserts into deltoid prominence on middle of lateral side of humeral body; acromial part multipennate with tendinous intersections; axillary nerve, C5 and C6; raises arm to a right angle; anterior fibres with pectoralis major draw arm forward, posterior fibres with teres major and latissimus dorsi draw it backward; covered by deep fascia. Arteries (pp. 587-590): thoracoacromial deltoid and acromial branches, posterior humeral circumflex distributed to the Deltoideus, scapular circumflex to its back part, profunda brachii gives branches to it.
- https://training.seer.cancer.gov/anatomy/muscular/groups/: Muscles named by shape, e.g. 'deltoid (triangular)'.
- https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html: Pectoralis major, latissimus dorsi, deltoid and rotator cuff muscles connect to the humerus and move the arm.
- https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-6-vaccine-administration.html: Deltoid preferred for children 3 through 18 years; for adults the deltoid is recommended; inject into the middle of the muscle where tissue is thickest; 90-degree angle; these sites reduce the chance of involving neural or vascular structures.

---

## Biceps brachii  (`biceps brachii`)

*part · muscle · musculoskeletal · 4 FMA ids · covers: long head of biceps brachii, short head of biceps brachii*

**Summary (plain)**

The biceps brachii is the long muscle on the front of the upper arm. It has two heads that start at the shoulder blade and join to attach just below the elbow.

**What it does (plain)**

It bends the elbow and turns the forearm so the palm faces up.

**For students: description**

The biceps brachii is a long, spindle-shaped (fusiform) muscle of the front of the arm, named for its two heads. The short head arises from the coracoid process and the long head from the supraglenoid tubercle, its tendon running inside the shoulder joint and down the intertubercular groove. The bellies join above the elbow and end in a tendon on the radius, which also gives off the bicipital aponeurosis.

**Location & neighbours**

On the front of the arm, from the scapula over the front of the shoulder joint down to the radius below the elbow. Its long-head tendon lies in the intertubercular groove of the humerus, and the bicipital aponeurosis crosses the brachial artery at the bend of the elbow.

| Detail | |
|---|---|
| Origin | Short head: tip of the coracoid process of the scapula (with coracobrachialis). Long head: supraglenoid tubercle at the top of the glenoid cavity; its tendon arches over the head of the humerus inside the joint and descends in the intertubercular groove. |
| Insertion | Back part of the radial tuberosity, with a bursa between tendon and bone; the bicipital aponeurosis passes medially to blend with the deep fascia over the forearm flexors. |
| Action | Flexes the elbow and, less strongly, the shoulder; a powerful supinator of the forearm. With the forearm fixed, it pulls the arm up toward the forearm, as in climbing. |
| Nerve supply | Musculocutaneous nerve (C5, C6). |
| Blood supply | Muscular branches of the brachial artery. |

**Exam tip**

Biceps means two heads. Besides bending the elbow, Gray's Anatomy calls the biceps a powerful supinator of the forearm.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), full text - Internet Archive](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Muscle Groups - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/) (Public domain)
- [Muscles of the Upper Extremity - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: Biceps brachii (pp. 443-444): long fusiform muscle on front of arm, named for two heads; short head from apex of coracoid process with coracobrachialis; long head from supraglenoid tuberosity, tendon in synovial sheath of shoulder joint, arches over humeral head, descends in intertubercular groove; bellies separable until about 7.5 cm above elbow; inserts into rough posterior part of radial tuberosity with a bursa in front; lacertus fibrosus crosses brachial artery and joins deep fascia over forearm flexors; musculocutaneous nerve, C5 and C6; flexes elbow and to a lesser extent shoulder; powerful supinator; with forearm fixed flexes arm on forearm as in climbing. Arteries (pp. 590-592): brachial muscular branches distributed to coracobrachialis, biceps brachii and brachialis.
- https://training.seer.cancer.gov/anatomy/muscular/groups/: Naming by number of origins: 'biceps (two heads)'.
- https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html: Muscles that move the forearm, located along the humerus, include triceps brachii, biceps brachii, brachialis and brachioradialis.

---

## Triceps brachii  (`triceps brachii`)

*part · muscle · musculoskeletal · 6 FMA ids · covers: lateral head of triceps brachii, long head of triceps brachii, medial head of triceps brachii*

**Summary (plain)**

The triceps brachii is the large muscle on the back of the upper arm. It has three heads that join into one tendon at the point of the elbow.

**What it does (plain)**

It straightens the elbow, working against the biceps, which bends it.

**For students: description**

The triceps brachii is a large muscle covering the whole back of the humerus, named for its three heads: long, lateral and medial. The long head arises from the scapula and the other two from the back of the humerus, above and below the groove for the radial nerve. They join in a tendon on the olecranon of the ulna.

**Location & neighbours**

On the back of the arm, along the full length of the posterior humerus, from the scapula and humerus down to the olecranon. Its long head passes between teres minor and teres major, separating the triangular and quadrangular spaces.

| Detail | |
|---|---|
| Origin | Long head: infraglenoid tubercle of the scapula, blending with the shoulder joint capsule. Lateral head: back of the humerus above the radial groove, lateral border and lateral intermuscular septum. Medial head: back of the humerus below the radial groove, medial border and medial intermuscular septum. |
| Insertion | Mainly the upper back part of the olecranon of the ulna; a band continues over anconeus to blend with the deep fascia of the forearm. |
| Action | Main extensor of the elbow, the direct antagonist of biceps and brachialis. The long head helps draw the humerus backward and adduct it, and supports the underside of the shoulder joint. |
| Nerve supply | Radial nerve (C7, C8). |
| Blood supply | Branches of the profunda brachii artery (one descends in the medial head, another runs between the long and lateral heads); the circumflex scapular artery also sends branches to the long head. |

**Exam tip**

Triceps means three heads. The long head separates the triangular space (circumflex scapular vessels) from the quadrangular space (posterior circumflex humeral vessels and axillary nerve).

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), full text - Internet Archive](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Muscle Groups - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/) (Public domain)
- [Muscles of the Upper Extremity - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: Triceps brachii (pp. 444-445): large muscle on back of arm along whole dorsal humerus; long, lateral and medial heads; long head from infraglenoid tuberosity, upper part blends with shoulder capsule; lateral head from posterior humerus between teres minor insertion and upper radial groove, lateral border and lateral intermuscular septum; medial head below radial groove, medial border and medial intermuscular septum; inserts mainly into posterior upper olecranon, band over anconeus to forearm fascia; long head divides space into triangular (scapular circumflex vessels) and quadrangular (posterior humeral circumflex vessels, axillary nerve) spaces; radial nerve, C7 and C8; main extensor of forearm, direct antagonist of biceps and brachialis; long head assists drawing humerus backward and adducting it, supports underside of shoulder joint. Arteries: profunda brachii middle collateral branch descends in medial head, ascending branch between long and lateral heads; scapular circumflex branches to long head.
- https://training.seer.cancer.gov/anatomy/muscular/groups/: Naming by number of origins: 'triceps (three heads)'.
- https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html: Muscles that move the forearm, located along the humerus, include triceps brachii and biceps brachii.

---

## Pectoralis major  (`pectoralis major`)

*part · muscle · musculoskeletal · 6 FMA ids · covers: abdominal part of pectoralis major, clavicular part of pectoralis major, sternocostal part of pectoralis major*

**Also called:** chest muscle

**Summary (plain)**

The pectoralis major is the main chest muscle. It is a thick, fan-shaped muscle on the upper front of the chest that runs out to the upper arm bone.

**What it does (plain)**

It pulls the arm in toward the body and across the chest, turns it inward, and brings a raised arm back down.

**For students: description**

The pectoralis major is a thick, fan-shaped muscle with a wide origin from the clavicle, sternum, upper costal cartilages and the external oblique aponeurosis, giving clavicular, sternocostal and abdominal parts. Its fibers converge on a flat tendon about 5 cm wide, made of two layers. The tendon looks twisted because the lowest fibers turn behind the others and insert highest on the humerus.

**Location & neighbours**

Upper front of the chest, in front of the armpit (axilla). Its clavicular part covers the clavipectoral fascia, which protects the axillary vessels and nerves.

| Detail | |
|---|---|
| Origin | Front of the sternal (medial) half of the clavicle; front of the sternum down to the sixth or seventh costal cartilage; cartilages of the true ribs (often not the first or seventh); aponeurosis of the external oblique. |
| Insertion | By a flat two-layered tendon into the crest of the greater tubercle of the humerus (lateral lip of the intertubercular groove); expansions reach the shoulder-joint capsule, line the groove and join the fascia of the arm. |
| Action | Adducts the arm and draws it forward across the chest while rotating it medially; with latissimus dorsi and teres major it lowers a raised arm. With the arms fixed, it lifts the ribs and helps forced inspiration. |
| Nerve supply | Medial and lateral pectoral nerves (Gray's 'anterior thoracic nerves'), which bring fibers from all the spinal nerves forming the brachial plexus. |
| Blood supply | Pectoral branch of the thoracoacromial artery, which runs down between the pectoralis major and minor. |

**Clinical relevance**

- In Poland syndrome, muscles on one side of the body are missing or underdeveloped, most often the sternal part of pectoralis major; it affects about 1 in 20,000 newborns, more often males.
- Partial absence of the sternocostal part is not uncommon; absence of the clavicular part is less frequent, and absence of the whole muscle is rare.

**Exam tip**

Its tendon is twisted: fibers from the lowest costal cartilages pass behind the upper ones and insert highest on the humerus.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), Myology: Pectoralis major (p. 436-438) and Angiology: thoracoacromial artery - Internet Archive full text](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Pectoralis Muscles - MeSH (NLM)](https://meshb.nlm.nih.gov/record/ui?ui=D010369) (Public domain)
- [Upper Extremity (Muscle Groups) - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html) (Public domain)
- [Poland syndrome - MedlinePlus Genetics (NLM)](https://medlineplus.gov/genetics/condition/poland-syndrome/) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: Read at offset 1418000: Pectoralis major thick, fan-shaped, upper and forepart of chest; arises from anterior surface of sternal half of clavicle, half breadth of sternum to 6th/7th cartilage, cartilages of true ribs (often not 1st or 7th), aponeurosis of external oblique; flat tendon about 5 cm broad into crest of greater tubercle of humerus; two laminae, tendon appears twisted as deep lower fibers ascend higher; expansions to shoulder-joint capsule, intertubercular groove, fascia of arm; clavipectoral fascia under cover of clavicular portion, protects axillary vessels and nerves; variations: abdominal part varies or absent, deficiency of sternocostal part not uncommon, clavicular less frequent, whole muscle rarely wanting; supplied by medial and lateral anterior thoracic nerves with fibers from all brachial plexus nerves; adducts, draws forward across chest and rotates arm inward, depresses raised arm with latissimus dorsi and teres major; arms fixed: raises ribs in forced inspiration. Offset 1963000: pectoral branch of thoracoacromial descends between the two pectorales and supplies them.
- https://meshb.nlm.nih.gov/record/ui?ui=D010369: Pectoralis major and minor make up the upper and fore part of the chest in front of the axilla.
- https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html: Pectoralis major, latissimus dorsi, deltoid and rotator cuff connect to the humerus and move the arm.
- https://medlineplus.gov/genetics/condition/poland-syndrome/: Poland syndrome: muscles on one side of the body absent or underdeveloped; most often part of pectoralis major (the main chest muscle) missing, usually the part connecting upper arm to sternum; about 1 in 20,000 newborns; more than twice as common in males.

---

## Trapezius  (`trapezius`)

*part · muscle · musculoskeletal · 6 FMA ids · covers: ascending part of trapezius, descending part of trapezius, transverse part of trapezius*

**Summary (plain)**

The trapezius is a large, flat, triangle-shaped muscle on the upper back. It covers the back of the neck and the tops of the shoulders.

**What it does (plain)**

It pulls the shoulder blades back, lifts the shoulders when carrying weight, and helps pull the head backward or to one side.

**For students: description**

The trapezius is a flat, triangular muscle in the top layer of the back muscles, which move the scapula. Its upper (descending) fibers run down and outward, its middle (transverse) fibers run across, and its lower (ascending) fibers run up and outward toward the shoulder girdle. The right and left muscles together form a diamond-shaped figure, with corners at the shoulders, the external occipital protuberance and the twelfth thoracic spine.

**Location & neighbours**

Back of the neck and upper back, from the base of the skull down to the twelfth thoracic vertebra and out to the clavicle and scapula. It lies superficially; its front edge forms the back border of the posterior triangle of the neck, behind the sternocleidomastoid.

| Detail | |
|---|---|
| Origin | External occipital protuberance and medial third of the superior nuchal line; ligamentum nuchae; spinous process of C7 and the spinous processes of all thoracic vertebrae, with the supraspinous ligament. |
| Insertion | Upper fibers: posterior border of the lateral third of the clavicle. Middle fibers: medial margin of the acromion and upper lip of the spine of the scapula. Lower fibers: by an aponeurosis to a tubercle at the medial end of the scapular spine. |
| Action | Retracts the scapula and braces the shoulder back. Upper fibers raise the point of the shoulder, as in carrying weights; lower fibers help depress the scapula; middle and lower fibers rotate it, raising the acromion. With shoulders fixed, both draw the head back; one tilts it sideways. |
| Nerve supply | Accessory nerve, with branches from the third and fourth cervical nerves. |
| Blood supply | Branches of the transverse cervical artery (its ascending and descending branches) and the descending branch of the occipital artery. |

**Clinical relevance**

- Neck pain is often due to strained or tense neck muscles, for example after long computer work, sleeping in an awkward position or overdoing exercise.

**Exam tip**

Named for its shape: the right and left trapezius together look like a trapezium, a four-sided figure.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), Myology: Trapezius (p. 432-434) and Angiology: occipital and transverse cervical arteries - Internet Archive full text](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Superficial Back Muscles - MeSH (NLM)](https://meshb.nlm.nih.gov/record/ui?ui=D064171) (Public domain)
- [Muscle Groups - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/) (Public domain)
- [Upper Extremity (Muscle Groups) - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html) (Public domain)
- [Head and Neck (Muscle Groups) - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/head_neck.html) (Public domain)
- [Neck Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/neckinjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: Read at offset 1418000: Trapezius is a flat, triangular muscle covering upper back of neck and shoulders; arises from external occipital protuberance, medial third of superior nuchal line, ligamentum nuchae, spine of C7 and all thoracic spines, supraspinal ligament; superior fibers downward to posterior border of lateral third of clavicle, middle horizontal to acromion and spine of scapula, inferior upward to tubercle at medial end of spine; two muscles resemble a trapezium/diamond with angles at shoulders, occipital protuberance and T12 spine; accessory nerve plus C3, C4; retracts scapula, upper fibers elevate shoulder as in supporting weights, lower depress scapula, middle and lower rotate scapula raising acromion; shoulders fixed: head drawn back, or to same side if one acts. Offset 1847000: descending branch of occipital artery supplies Trapezius. Offset 1963000: ascending and descending branches of transverse cervical supply Trapezius. Offset 1269000: posterior triangle bounded behind by Trapezius.
- https://meshb.nlm.nih.gov/record/ui?ui=D064171: Superficial back muscles: top layer of back muscles whose function is to move the scapula; includes trapezius.
- https://training.seer.cancer.gov/anatomy/muscular/groups/: Trapezius named for its shape, like a trapezoid, a four-sided figure.
- https://training.seer.cancer.gov/anatomy/muscular/groups/upper.html: Muscles that move the shoulder and arm include the trapezius.
- https://training.seer.cancer.gov/anatomy/muscular/groups/head_neck.html: Trapezius named as one of the obvious superficial neck muscles.
- https://medlineplus.gov/neckinjuriesanddisorders.html: Muscle strain or tension often causes neck pain; neck muscles can be strained by sleeping awkwardly or overdoing exercise; long computer use.

---

## Sternocleidomastoid  (`sternocleidomastoid`)

*part · muscle · musculoskeletal · 2 FMA ids · covers: sternocleidomastoid*

**Also called:** sternomastoid

**Summary (plain)**

The sternocleidomastoid is a long muscle on each side of the neck. It runs at a slant from the breastbone and collarbone up to the bony bump behind the ear.

**What it does (plain)**

It tips the head toward the shoulder and turns the face to the other side, and both muscles together bend the neck forward.

**For students: description**

The sternocleidomastoid crosses the side of the neck obliquely; it is thick and narrow in the middle and broader and thinner at each end. It starts as two heads, sternal and clavicular, separated by a small triangular gap, which merge below the middle of the neck into one rounded belly. It divides the side of the neck into the anterior and posterior triangles.

**Location & neighbours**

Side of the neck, from the top of the sternum (manubrium) and the inner third of the clavicle up to the mastoid process behind the ear. Its front border bounds the anterior triangle of the neck; its back border bounds the posterior triangle, which the trapezius closes behind.

| Detail | |
|---|---|
| Origin | Sternal head: upper part of the front surface of the manubrium of the sternum. Clavicular head: upper border and front surface of the medial third of the clavicle. |
| Insertion | By a strong tendon into the lateral surface of the mastoid process of the temporal bone, from apex to upper border, and by a thin aponeurosis into the lateral half of the superior nuchal line of the occipital bone. |
| Action | One muscle: tilts the head toward the shoulder of the same side and rotates the face toward the opposite side. Both together: flex the cervical spine. With the head fixed, they help raise the thorax in forced inspiration. |
| Nerve supply | Accessory nerve, plus branches from the anterior rami of the second and third cervical nerves. |
| Blood supply | Sternocleidomastoid branch of the superior thyroid artery, and the sternocleidomastoid artery, usually from the occipital artery (sometimes from the external carotid), which enters the muscle with the accessory nerve. |

**Clinical relevance**

- Torticollis (wryneck) is a twisted neck: the head tips to one side and the chin turns to the other, from congenital defects, trauma, inflammation, tumours or nerve disorders.
- Neck pain is often due to strained or tense neck muscles, for example after long computer work, sleeping in an awkward position or overdoing exercise.

**Exam tip**

Its name gives its attachments: it arises from the sternum and clavicle and inserts on the mastoid process.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), Myology: Sternocleidomastoideus (p. 390-391) and Angiology: superior thyroid and occipital arteries - Internet Archive full text](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Muscle Groups - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/) (Public domain)
- [Head and Neck (Muscle Groups) - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/head_neck.html) (Public domain)
- [Torticollis - MeSH (NLM)](https://meshb.nlm.nih.gov/record/ui?ui=D014103) (Public domain)
- [Neck Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/neckinjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: Read at offset 1269000: Sternocleidomastoideus (sternomastoid muscle) passes obliquely across the side of the neck, thick and narrow centrally, broader at ends; two heads, sternal from upper anterior manubrium, clavicular from superior border and anterior surface of medial third of clavicle, separated by triangular interval, blend below middle of neck; inserted into lateral surface of mastoid process and lateral half of superior nuchal line; divides side of neck into anterior and posterior triangles, posterior bounded behind by Trapezius; supplied by accessory nerve and anterior divisions of C2 and C3; one muscle draws head toward same shoulder and rotates face to opposite side; together flex cervical column; with head fixed assist forced inspiration. Read at offset 1847000: sternocleidomastoid branch of superior thyroid supplies the muscle; sternocleidomastoid artery usually from occipital, sometimes external carotid, enters muscle with accessory nerve.
- https://training.seer.cancer.gov/anatomy/muscular/groups/: Naming by attachments: sternocleidomastoideus has origin on the sternum and clavicle and insertion on the mastoid process.
- https://training.seer.cancer.gov/anatomy/muscular/groups/head_neck.html: Sternocleidomastoid and trapezius named as two of the more obvious superficial neck muscles.
- https://meshb.nlm.nih.gov/record/ui?ui=D014103: Torticollis: symptom of a twisted neck; head usually tipped to one side and chin rotated to the other; involuntary neck muscle contractions from congenital defects, trauma, inflammation, tumours, neurological or other factors; entry terms include wryneck, spasmodic torticollis, cervical dystonia.
- https://medlineplus.gov/neckinjuriesanddisorders.html: Muscle strain or tension often causes neck pain, often from overuse such as long computer use; neck muscles can be strained by sleeping awkwardly or overdoing exercise.

---

## Quadriceps femoris  (`group:quadriceps`)

*group · muscle · musculoskeletal · 8 FMA ids · covers: rectus femoris, vastus intermedius, vastus lateralis, vastus medialis*

**Also called:** quadriceps, quadriceps extensor

**Summary (plain)**

The quadriceps is the big group of four muscles on the front of the thigh. It covers the front and sides of the thigh bone and ends in a tendon at the kneecap.

**What it does (plain)**

It straightens the knee, and one of its parts, the rectus femoris, also helps bend the hip.

**For students: description**

The quadriceps femoris is the great extensor of the knee, a large fleshy mass covering the front and sides of the femur. It has four parts: the rectus femoris in the middle of the thigh, and three vasti (lateralis, medialis and intermedius) that cover the femoral shaft from the trochanters to the condyles. Vastus lateralis is the largest. Their tendons join into one quadriceps tendon above the knee.

**Location & neighbours**

Front and sides of the thigh, between the hip and the knee. Rectus femoris lies in the middle front; vastus lateralis on the outer side, vastus medialis on the inner side, and vastus intermedius in front, lying directly on the femur.

| Detail | |
|---|---|
| Origin | Rectus femoris: anterior inferior iliac spine (straight head) and a groove above the acetabulum (reflected head). Vasti: the femoral shaft, including the intertrochanteric line, greater trochanter, gluteal tuberosity, linea aspera, and (intermedius) the front and lateral surfaces. |
| Insertion | The four tendons unite into the quadriceps tendon on the base of the patella; the patellar ligament continues from the patella to the tibial tuberosity as the true tendon of insertion. Vastus lateralis and medialis also attach to the patellar borders. |
| Action | Extends the knee. Rectus femoris also helps flex the hip and supports the pelvis and trunk on the femur; vastus medialis pulls the patella medially as well as upward. |
| Nerve supply | Femoral nerve (second, third and fourth lumbar nerves). |
| Blood supply | Lateral femoral circumflex artery, a branch of the deep femoral artery; its descending branch runs behind rectus femoris and supplies vastus lateralis. |

**Clinical relevance**

- Patellar tendinitis ('jumper's knee') is swelling of the tendon below the kneecap that carries the quadriceps' pull to the tibia; it usually follows repeated strain, often in sport.

**Exam tip**

The quadriceps (named for its four heads) straightens the knee; the hamstrings at the back of the thigh are its antagonists and bend the knee.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), Myology: Quadriceps femoris (p. 470-471) and Angiology: lateral femoral circumflex artery - Internet Archive full text](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Quadriceps Muscle - MeSH (NLM)](https://meshb.nlm.nih.gov/record/ui?ui=D052097) (Public domain)
- [Lower Extremity (Muscle Groups) - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/lower.html) (Public domain)
- [Muscle Groups - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/) (Public domain)
- [Tendinitis - MedlinePlus (NLM)](https://medlineplus.gov/tendinitis.html) (Public domain)
- [Knee Injuries and Disorders - MedlinePlus (NLM)](https://medlineplus.gov/kneeinjuriesanddisorders.html) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: Read at offset 1550000: Quadriceps femoris (Quadriceps extensor) is the great extensor of the leg, large fleshy mass covering front and sides of femur; Rectus femoris in middle, from anterior inferior iliac spine and groove above acetabulum, inserted into base of patella; three vasti cover femur from trochanters to condyles; Vastus lateralis the largest, from intertrochanteric line, greater trochanter, gluteal tuberosity, linea aspera, into lateral border of patella; Vastus medialis into medial border; Vastus intermedius from front and lateral surfaces of femur; tendons unite into one tendon into base of patella; patella a sesamoid bone in the tendon; ligamentum patellae from patella apex to tibial tuberosity is proper tendon of insertion; femoral nerve, L2-L4; extends leg; rectus femoris supports pelvis and trunk, flexes thigh; vastus medialis draws patella medially and upward. Offset 2124500: lateral femoral circumflex from profunda; descending branch behind rectus femoris supplies vastus lateralis.
- https://meshb.nlm.nih.gov/record/ui?ui=D052097: Quadriceps femoris: collective name of the four-headed skeletal muscle of the thigh: rectus femoris, vastus intermedius, vastus lateralis, vastus medialis.
- https://training.seer.cancer.gov/anatomy/muscular/groups/lower.html: Quadriceps femoris group straightens the leg at the knee; hamstrings are antagonists to the quadriceps and flex the leg at the knee.
- https://training.seer.cancer.gov/anatomy/muscular/groups/: Muscle naming: quadriceps means four heads (number of origins); vastus means huge; rectus means straight.
- https://medlineplus.gov/tendinitis.html: Tendinitis is severe swelling of a tendon; tendons connect muscle to bone; patellar tendinitis ('jumper's knee'); usually after repeated injury; some forms named after sports that raise risk.
- https://medlineplus.gov/kneeinjuriesanddisorders.html: Lists patellar tendinitis among knee problems; muscles and tendons help the knee move.

---

## Hamstrings  (`group:hamstrings`)

*group · muscle · musculoskeletal · 8 FMA ids · covers: long head of biceps femoris, semimembranosus, semitendinosus, short head of biceps femoris*

**Also called:** hamstring muscles, posterior femoral muscles

**Summary (plain)**

The hamstrings are a group of three muscles that run down the back of the thigh, from the bottom of the pelvis to just below the knee.

**What it does (plain)**

They bend the knee, and they help the buttock muscle pull the trunk back upright after bending forward.

**For students: description**

The hamstrings (posterior femoral muscles) are the biceps femoris, with a long and a short head, the semitendinosus and the semimembranosus. Except for the short head of biceps, they arise from the ischial tuberosity. The biceps tendon forms the lateral hamstring; the semitendinosus and semimembranosus tendons form the medial hamstrings. They act against the quadriceps.

**Location & neighbours**

In the back of the thigh. The biceps femoris lies on the lateral side and passes to the fibula; the semitendinosus and semimembranosus lie medially and pass to the tibia. The semitendinosus tendon runs along the medial side of the popliteal fossa behind the knee.

| Detail | |
|---|---|
| Origin | Long head of biceps femoris and semitendinosus: lower medial impression on the ischial tuberosity. Semimembranosus: upper lateral impression on the ischial tuberosity, by a thick tendon. Short head of biceps: lateral lip of the linea aspera and the lateral intermuscular septum. |
| Insertion | Biceps femoris: lateral side of the head of the fibula, with a small slip to the lateral condyle of the tibia. Semitendinosus: upper medial surface of the tibial shaft, behind the sartorius and joined to the gracilis tendon. Semimembranosus: groove on the back of the medial tibial condyle. |
| Action | Flex the leg at the knee. With the knee half bent, the biceps turns the leg slightly outward and the semitendinosus (and a little the semimembranosus) turns it inward. They help the gluteus maximus restore the upright posture after stooping. |
| Nerve supply | Sciatic nerve branches (L4 to S3): the tibial nerve to the semitendinosus, semimembranosus and long head of biceps; the common fibular (peroneal) nerve to the short head of biceps. |
| Blood supply | Mainly the perforating branches of the deep femoral (profunda femoris) artery; the inferior gluteal artery supplies the muscles near their attachment to the ischial tuberosity. |

**Clinical relevance**

- Hamstring strains (stretched or torn muscle or tendon) are common; they cause pain, spasm, swelling and trouble moving the muscle.
- Hamstring strains happen in sports with much running, jumping and sudden starts and stops, such as basketball, football and soccer.
- Strains are first treated with rest, ice, compression and medicines; exercise and physical therapy may follow.

**Exam tip**

The short head of biceps femoris is the only hamstring part supplied by the common fibular (peroneal) nerve; the others are supplied by the tibial nerve.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), Posterior Femoral Muscles and Arteries of the Lower Extremity - Internet Archive full text](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Muscles of the Lower Extremity - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/lower.html) (Public domain)
- [Muscle Groups - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/) (Public domain)
- [Sports Injuries - NIAMS](https://www.niams.nih.gov/health-topics/sports-injuries) (Public domain)
- [Sprains and Strains - MedlinePlus (NLM)](https://medlineplus.gov/sprainsandstrains.html) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: pp. 478-480 '4. The Posterior Femoral Muscles (Hamstring Muscles)': long head of biceps from lower inner impression on ischial tuberosity; short head from lateral lip of linea aspera and lateral intermuscular septum; inserted into lateral side of head of fibula with slip to lateral tibial condyle; semitendinosus from lower medial impression on ischial tuberosity, inserted into upper medial surface of tibial body behind sartorius, below and united to gracilis tendon, lies along medial side of popliteal fossa; semimembranosus by thick tendon from upper outer impression, inserted mainly into horizontal groove on posterior medial aspect of medial tibial condyle; biceps tendon forms lateral hamstring, other two medial hamstrings; nerves L4, L5, S1-S3; short head from common peroneal, others tibial; flex leg on thigh; semiflexed knee: biceps rotates outward, semitendinosus and slightly semimembranosus inward. p. 478: gluteus maximus restores erect position after stooping, assisted by the hamstrings. Angiology pp. 608-636: second and third perforating arteries supply the posterior femoral muscles; first perforating to biceps femoris; inferior gluteal supplies muscles attached to ischial tuberosity.
- https://training.seer.cancer.gov/anatomy/muscular/groups/lower.html: Hamstrings are antagonists to the quadriceps femoris and flex the leg at the knee.
- https://training.seer.cancer.gov/anatomy/muscular/groups/: Muscle naming: biceps means two heads.
- https://www.niams.nih.gov/health-topics/sports-injuries: Three muscles run along the back of the thigh and form the hamstring; hamstring strains with running, jumping, sudden starts and stops; basketball, football and soccer players commonly get them.
- https://medlineplus.gov/sprainsandstrains.html: A strain is a stretched or torn muscle or tendon; back and hamstring strains are common; symptoms pain, spasm, swelling, trouble moving the muscle; treatment rest, ice, compression, medicines, later exercise and physical therapy.

---

## Gluteus maximus  (`gluteus maximus`)

*part · muscle · musculoskeletal · 2 FMA ids · covers: gluteus maximus*

**Summary (plain)**

The gluteus maximus is the big, thick muscle of the buttock. It sits behind the hip and gives the buttock its rounded shape.

**What it does (plain)**

It pulls the thigh backward, holds the pelvis and trunk steady when standing, and straightens the body after bending forward.

**For students: description**

The gluteus maximus is a broad, thick, four-sided muscle that forms the prominence of the buttock. Its name means the large gluteal muscle. Gray's Anatomy notes that its great size is one of the most typical features of human muscles, linked to keeping the trunk upright. Bursae lie under its deep surface.

**Location & neighbours**

In the gluteal region (buttock), behind the hip joint. It runs from the back of the ilium, sacrum and coccyx down and outward to the upper femur and the iliotibial band, and it covers the gluteus medius.

| Detail | |
|---|---|
| Origin | Posterior gluteal line and nearby iliac crest; back of the lower sacrum and side of the coccyx; aponeurosis of the erector spinae; sacrotuberous ligament; gluteal aponeurosis over the gluteus medius. |
| Insertion | Upper and larger part into the iliotibial band (iliotibial tract) of the fascia lata; deeper lower fibres into the gluteal tuberosity of the femur. |
| Action | Extends the thigh at the hip; supports the pelvis and trunk on the femur, especially on one leg; strongly restores the upright posture after stooping; tightens the fascia lata; its lower part adducts and laterally rotates the thigh. |
| Nerve supply | Inferior gluteal nerve (L5, S1, S2). |
| Blood supply | Inferior and superior gluteal arteries; the first perforating branch of the deep femoral artery also sends branches. |

**Clinical relevance**

- CDC advises against using the buttock muscles for vaccine injections in infants and children because of the risk of injuring the sciatic nerve.
- If a gluteal injection is needed, it is given above and lateral to a line from the posterior superior iliac spine to the greater trochanter, or at the ventrogluteal site.
- Older CDC guidance (2002) reports that hepatitis B and rabies vaccines work less well when given in the buttock than in the deltoid.

**Exam tip**

Gray's Anatomy calls its large size one of the most characteristic features of human muscles, tied to the human ability to hold the trunk erect.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), Muscles of the Gluteal Region and Arteries of the Lower Extremity - Internet Archive full text](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Muscle Groups - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/) (Public domain)
- [Pink Book Chapter 6: Vaccine Administration - CDC](https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-6-vaccine-administration.html) (Public domain)
- [General Recommendations on Immunization (ACIP/AAFP, MMWR 2002) - CDC](https://www.cdc.gov/mmWr/preview/mmwrhtml/rr5102a1.htm) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: pp. 474-478 '3. The Muscles of the Gluteal Region': broad and thick fleshy mass of quadrilateral shape forming the prominence of the nates; arises from posterior gluteal line and iliac crest, lower sacrum, side of coccyx, aponeurosis of Sacrospinalis, sacrotuberous ligament, aponeurosis over gluteus medius; inserted into iliotibial band and gluteal tuberosity; three bursae on deep surface; large size one of most characteristic features of human muscles, connected with keeping trunk erect; nerve L5, S1, S2 through inferior gluteal nerve; extends femur, supports pelvis and trunk on femoral head especially on one leg, most powerful in restoring erect position after stooping (assisted by hamstrings), tenses fascia lata, lower part adducts and rotates limb outward. Angiology: inferior gluteal and superior gluteal arteries supply gluteus maximus; first perforating artery gives branches to gluteus maximus.
- https://training.seer.cancer.gov/anatomy/muscular/groups/: Muscle naming by size: maximus (large).
- https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-6-vaccine-administration.html: Buttock muscles not used for vaccines in infants and children because of potential sciatic nerve injury; gluteal injection lateral and superior to a line between posterior superior iliac spine and greater trochanter, or ventrogluteal site.
- https://www.cdc.gov/mmWr/preview/mmwrhtml/rr5102a1.htm: Buttock injection associated with decreased immunogenicity of hepatitis B and rabies vaccines in adults; immunogenicity substantially lower at gluteal than deltoid site.

---

## Gastrocnemius  (`gastrocnemius`)

*part · muscle · musculoskeletal · 4 FMA ids · covers: lateral head of gastrocnemius, medial head of gastrocnemius*

**Also called:** calf muscle

**Summary (plain)**

The gastrocnemius is the muscle that makes up most of the calf, at the back of the lower leg. It has two heads that start just above the knee.

**What it does (plain)**

It points the foot down, as when standing on tiptoe, and helps bend the knee.

**For students: description**

The gastrocnemius is the most superficial calf muscle and forms most of the calf. It arises by two heads, medial (the larger) and lateral, from the femoral condyles. Its tendon joins that of the soleus to form the calcaneal (Achilles) tendon; together the two muscles are sometimes called the triceps surae.

**Location & neighbours**

In the back of the leg (calf), superficial to the soleus. Its two heads start on the back of the femur just above the knee, and the muscle runs down to join the calcaneal tendon, which attaches to the heel bone.

| Detail | |
|---|---|
| Origin | Medial head: upper back part of the medial femoral condyle and the nearby femur. Lateral head: side of the lateral femoral condyle and the back of the femur just above it. Both arise by strong, flat tendons. |
| Insertion | Its aponeurosis joins the soleus tendon to form the calcaneal (Achilles) tendon, which inserts into the middle of the back surface of the calcaneus, with a bursa between tendon and bone. |
| Action | Plantar flexes the foot at the ankle (with the soleus, the chief muscles doing this) and helps flex the knee. |
| Nerve supply | Tibial nerve (S1, S2). |
| Blood supply | Sural arteries, branches of the popliteal artery that arise opposite the knee joint. |

**Clinical relevance**

- An Achilles tendon injury is a stretch, tear or irritation of the tendon joining the calf muscle to the back of the heel.
- Achilles tendinitis is usually a chronic overuse problem, with pain and stiffness at the back of the heel, worst in the morning; serious cases can tear and may need surgery.

**Exam tip**

Its tendon, the calcaneal (Achilles) tendon, is the largest tendon in the body; Gray's Anatomy calls it the thickest and strongest.

**Sources**

- [Gray's Anatomy of the Human Body, 20th ed. (1918), Posterior Crural Muscles and Arteries of the Lower Extremity - Internet Archive full text](https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt) (Public domain)
- [Muscles of the Lower Extremity - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/muscular/groups/lower.html) (Public domain)
- [Sports Injuries - NIAMS](https://www.niams.nih.gov/health-topics/sports-injuries) (Public domain)

**What was checked on each page**

- https://archive.org/download/anatomyofhumanbo1918gray/anatomyofhumanbo1918gray_djvu.txt: pp. 482-483 'The Posterior Crural Muscles, Superficial Group': gastrocnemius is the most superficial muscle and forms the greater part of the calf; arises by two heads connected to the femoral condyles by strong flat tendons; medial head larger, from upper back part of medial condyle and adjacent femur; lateral head from side of lateral condyle and posterior femur above it; aponeurosis unites with soleus tendon to form tendo calcaneus, thickest and strongest in the body, inserted into middle of posterior surface of calcaneus with a bursa between; gastrocnemius and soleus occasionally called triceps surae; supplied by S1, S2 through tibial nerve; calf muscles chief extensors of foot at ankle; gastrocnemius flexes femur on tibia. Angiology: sural arteries from popliteal opposite knee joint distributed to gastrocnemius, soleus and plantaris.
- https://training.seer.cancer.gov/anatomy/muscular/groups/lower.html: Gastrocnemius and soleus plantar flex the foot (antagonists of tibialis anterior).
- https://www.niams.nih.gov/health-topics/sports-injuries: Achilles tendon injury is a stretch, tear or irritation of the tendon connecting the calf muscle to the back of the heel; Achilles is the largest tendon in the body; tendinitis usually chronic from overuse, pain and stiffness at back of heel especially in morning; serious cases can lead to a tear that may require surgery.

---

## Aorta  (`group:fma_FMA3734_v`)

*group · vessel · cardiovascular · 5 FMA ids · covers: abdominal aorta, arch of aorta, ascending aorta, descending aorta, descending thoracic aorta*

**Summary (plain)**

The aorta is the body's main artery. It leaves the heart, arches over in the chest and runs down through the chest and belly.

**What it does (plain)**

It carries oxygen-rich blood from the heart's left ventricle to the rest of the body through its many branches.

**For students: description**

The aorta is the large elastic artery that receives blood from the left ventricle through the aortic valve. It has three parts: the ascending aorta, the aortic arch and the descending aorta, which is divided into thoracic and abdominal parts. Every systemic artery branches from it, directly or indirectly.

**Location & neighbours**

It rises from the left ventricle, curves backward and to the left as the arch, then descends through the chest (thoracic aorta) and into the abdomen (abdominal aorta).

| Detail | |
|---|---|
| Origin | Arises from the left ventricle; the aortic valve lies between them. |
| Supplies / drains | The whole systemic circulation: all systemic arteries come from it, directly or indirectly, including those to the heart wall, head and arms, the lungs' own tissue, the abdominal and pelvic organs and the legs. |
| Main branches | Ascending aorta: right and left coronary arteries only. Arch: brachiocephalic, left common carotid, left subclavian. Thoracic: bronchial arteries. Abdominal: celiac, superior mesenteric, suprarenal, renal, gonadal, inferior mesenteric and lumbar arteries; then the iliac arteries. |

**Clinical relevance**

- An aortic aneurysm is a balloon-like bulge of a weakened aortic wall and usually causes no symptoms; abdominal aortic aneurysms are the most common type, thoracic ones form in the chest.
- A ruptured aortic aneurysm or an aortic dissection (a tear in the wall) can cause sudden, life-threatening internal bleeding and is a medical emergency.
- Risk factors for aortic aneurysm include atherosclerosis, smoking, high blood pressure, high cholesterol and a family history of aneurysms.
- In tetralogy of Fallot the aorta is out of place (overriding aorta), so oxygen-poor blood from the right ventricle can flow into it.
- Patent ductus arteriosus is a connection between the aorta and the pulmonary artery that does not close properly after birth.

**Exam tip**

The right and left coronary arteries are the only branches of the ascending aorta.

**Sources**

- [Circulatory Pathways - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html) (Public domain)
- [Structure of the Heart - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html) (Public domain)
- [Classification & Structure of Blood Vessels - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/classification.html) (Public domain)
- [Lung Anatomy - NCI SEER Training Modules](https://training.seer.cancer.gov/lung/anatomy/) (Public domain)
- [Aortic Aneurysm - MedlinePlus (NLM)](https://medlineplus.gov/aorticaneurysm.html) (Public domain)
- [How the Heart Works: Blood Flow - NHLBI](https://www.nhlbi.nih.gov/health/heart/blood-flow) (Public domain)
- [Congenital Heart Defects: Types - NHLBI](https://www.nhlbi.nih.gov/health/congenital-heart-defects/types) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html: Aorta ascends from the left ventricle, curves posteriorly and to the left, descends through thorax and abdomen; ascending aorta, arch, descending (thoracic and abdominal); all systemic arteries branch directly or indirectly from it; coronary arteries only branches of ascending aorta; arch gives brachiocephalic, left common carotid, left subclavian; abdominal gives celiac, superior mesenteric, suprarenal, renal, gonadal, inferior mesenteric; lumbar arteries; external and internal iliac branches.
- https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html: Aortic semilunar valve lies between the left ventricle and the aorta; coronary arteries are branches of the ascending aorta.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/classification.html: Blood leaving the ventricles enters large elastic arteries; systemic arteries carry oxygenated blood from the left ventricle.
- https://training.seer.cancer.gov/lung/anatomy/: Bronchial arteries branch off the aorta and supply the lung's own nutrients.
- https://medlineplus.gov/aorticaneurysm.html: Aorta is the main artery from the heart through chest and abdomen; aneurysm is a balloon-like bulge; most cause no symptoms; AAA most common, TAA in chest; wall weakens over time; atherosclerosis, smoking, high blood pressure, high cholesterol, family history; rupture is a medical emergency; dissection is a tear in the wall; both can cause life-threatening bleeding.
- https://www.nhlbi.nih.gov/health/heart/blood-flow: Aorta is the large artery carrying blood from the heart to the rest of the body.
- https://www.nhlbi.nih.gov/health/congenital-heart-defects/types: Aorta: main artery carrying oxygen-rich blood to the body; PDA connects aorta and pulmonary artery and does not close properly after birth; overriding aorta in tetralogy lets oxygen-poor blood from the right ventricle into the aorta.

---

## Superior vena cava  (`superior vena cava`)

*part · vessel · cardiovascular · 1 FMA ids · covers: superior vena cava*

**Also called:** anterior vena cava, cranial vena cava

**Summary (plain)**

The superior vena cava is a large vein in the chest. It ends in the right upper chamber of the heart.

**What it does (plain)**

It brings blood that has given up its oxygen back to the heart from the head, neck, arms and chest.

**For students: description**

The superior vena cava is the large venous trunk that returns deoxygenated blood from the upper body to the heart. It is formed where the left and right brachiocephalic veins join, and it ends in the right atrium. Together with the inferior vena cava, it carries all the blood returning from the systemic circulation into the right atrium.

**Location & neighbours**

In the chest, running down to end in the right atrium of the heart. Its opening into the right atrium has no valve.

| Detail | |
|---|---|
| Origin | Formed by the union of the left and right brachiocephalic (innominate) veins; drains into the right atrium. |
| Supplies / drains | Drains the head, neck, upper limbs (arms) and chest. |
| Main branches | Main tributaries: the left and right brachiocephalic veins, each formed by the internal jugular vein joining the subclavian vein. |

**Clinical relevance**

- Superior vena cava syndrome: blockage of the vessel, for example by a tumour, a blood clot, an aneurysm or pressure from outside, stops blood from the head, arms and chest reaching the right atrium.
- In superior vena cava syndrome the face, neck and upper arms may swell and turn bluish (Pemberton's sign).
- A rise in superior vena cava pressure makes the jugular vein bulge, so it is seen higher in the neck than usual (jugular venous distension).

**Exam tip**

The superior vena cava enters the right atrium through an opening that has no valve.

**Sources**

- [superior vena cava - NCI Dictionary of Cancer Terms (glossary API)](https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/superior-vena-cava) (Public domain)
- [Vena Cava, Superior - MeSH concept M0022585 (NLM)](https://id.nlm.nih.gov/mesh/M0022585.json) (Public domain)
- [Superior Vena Cava Syndrome - MeSH concept M0020822 (NLM)](https://id.nlm.nih.gov/mesh/M0020822.json) (Public domain)
- [Superior Vena Cava C12816 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12816?include=definitions,synonyms) (CC BY 4.0)
- [Superior Vena Cava Opening C33702 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C33702?include=definitions) (CC BY 4.0)
- [Left Brachiocephalic Vein C32964 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32964?include=definitions) (CC BY 4.0)
- [Internal Jugular Vein C32849 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32849?include=definitions,synonyms) (CC BY 4.0)
- [Jugular Venous Distension C191482 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C191482?include=definitions) (CC BY 4.0)
- [Circulatory Pathways - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html) (Public domain)

**What was checked on each page**

- https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/superior-vena-cava: The large vein that carries blood from the head, neck, arms and chest to the heart.
- https://id.nlm.nih.gov/mesh/M0022585.json: Scope note: the venous trunk returning blood from the head, neck, upper extremities and chest.
- https://id.nlm.nih.gov/mesh/M0020822.json: SVC syndrome: obstruction of the SVC blocking flow from head, arms and chest to the right atrium; causes include tumours, clots, aneurysms, external pressure; swelling and/or bluish colour of face, neck, upper arms (Pemberton's sign).
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12816?include=definitions,synonyms: NCI definition: large vein ending in the right atrium, carrying deoxygenated blood from head, neck, arms and chest; synonyms Anterior Vena Cava, Cranial Vena Cava (CDISC).
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C33702?include=definitions: Superior vena cava opening: the non-valve opening where the SVC enters the right atrium.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32964?include=definitions: Left brachiocephalic vein, in the upper chest, joins the right innominate vein to form the superior vena cava.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32849?include=definitions,synonyms: Internal jugular vein joins the subclavian vein to form the brachiocephalic vein.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C191482?include=definitions: Jugular venous distension: the jugular vein bulges because SVC pressure is raised, so it is visible higher in the neck than usual.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html: Systemic blood drains into larger veins until it reaches either the superior or inferior vena cava, both of which drain into the right atrium.

---

## Inferior vena cava  (`inferior vena cava`)

*part · vessel · cardiovascular · 1 FMA ids · covers: inferior vena cava*

**Also called:** posterior vena cava, caudal vena cava

**Summary (plain)**

The inferior vena cava is a large vein that runs up through the belly and empties into the heart.

**What it does (plain)**

It brings blood back to the heart from the legs and feet and from the organs of the belly and pelvis.

**For students: description**

The inferior vena cava is the large venous trunk that returns blood from the lower half of the body to the heart. It begins where the two common iliac veins join and receives veins such as the renal veins from the kidneys and the hepatic veins from the liver. Together with the superior vena cava, it drains into the right atrium.

**Location & neighbours**

In the abdomen, starting at the right side of the fifth lumbar vertebra, where the two common iliac veins meet, and running up to empty into the right atrium of the heart.

| Detail | |
|---|---|
| Origin | Formed by the union of the left and right common iliac veins near the right side of the fifth lumbar vertebra; drains into the right atrium. |
| Supplies / drains | Drains the lower limbs (legs and feet) and the organs of the abdomen and pelvis. |
| Main branches | Main tributaries: the common iliac veins, the renal veins (from the kidneys) and the hepatic veins (from the liver). |

**Clinical relevance**

- A vena cava filter is a device placed in the inferior vena cava to stop blood clots from the deep veins of the legs travelling on to the lungs.

**Exam tip**

The inferior vena cava begins where the left and right common iliac veins join, near the right side of the fifth lumbar vertebra.

**Sources**

- [inferior vena cava - NCI Dictionary of Cancer Terms (glossary API)](https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/inferior-vena-cava) (Public domain)
- [Vena Cava, Inferior - MeSH concept M0022584 (NLM)](https://id.nlm.nih.gov/mesh/M0022584.json) (Public domain)
- [Vena Cava Filters - MeSH concept M0024920 (NLM)](https://id.nlm.nih.gov/mesh/M0024920.json) (Public domain)
- [Inferior Vena Cava C12815 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12815?include=definitions,synonyms) (CC BY 4.0)
- [Common Iliac Vein C32359 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32359?include=definitions) (CC BY 4.0)
- [Hepatic Vein C32736 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32736?include=definitions) (CC BY 4.0)
- [Renal Vein C33462 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C33462?include=definitions) (CC BY 4.0)
- [Circulatory Pathways - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html) (Public domain)

**What was checked on each page**

- https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/inferior-vena-cava: A large vein that empties into the heart; carries blood from the legs and feet and from organs in the abdomen and pelvis.
- https://id.nlm.nih.gov/mesh/M0022584.json: Scope note: venous trunk receiving blood from the lower extremities and the pelvic and abdominal organs.
- https://id.nlm.nih.gov/mesh/M0024920.json: Vena cava filters: mechanical devices placed in the inferior vena cava to stop clots from the deep veins of the leg travelling to the lungs.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12815?include=definitions,synonyms: NCI definition: large vein returning blood from the lower half of the body to the heart; synonyms Caudal Vena Cava, Posterior Vena Cava (CDISC).
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32359?include=definitions: Common iliac vein formed by internal and external iliac veins at the pelvic brim; ends at the right side of the fifth lumbar vertebra, joining its fellow to form the inferior vena cava.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32736?include=definitions: Hepatic veins carry blood from the central veins of the liver to the inferior vena cava.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C33462?include=definitions: Renal veins return blood from the kidneys to the vena cava.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html: Superior and inferior vena cava both drain into the right atrium.

---

## Pulmonary trunk  (`pulmonary trunk`)

*part · vessel · cardiovascular · 1 FMA ids · covers: pulmonary trunk*

**Also called:** pulmonary artery

**Summary (plain)**

The pulmonary trunk is the large artery that leaves the right side of the heart and carries blood to the lungs.

**What it does (plain)**

It takes oxygen-poor blood from the heart to the lungs, where the blood picks up oxygen and gets rid of carbon dioxide.

**For students: description**

The pulmonary trunk carries oxygen-poor blood out of the right ventricle, the pump of the pulmonary circuit. The pulmonary valve sits at its base. It splits into two pulmonary arteries, one for each lung, which keep dividing until they end in capillaries around the air sacs. Unlike systemic arteries, it carries low-oxygen blood.

**Location & neighbours**

It leaves the right ventricle at the pulmonary valve and runs toward the lungs; its branches enter each lung at the hilum on the lung's medial surface.

| Detail | |
|---|---|
| Origin | Arises from the right ventricle; the pulmonary semilunar valve lies between them. |
| Supplies / drains | Carries blood to both lungs for gas exchange in the capillaries around the alveoli; the lung tissue itself is nourished by the bronchial arteries from the aorta instead. |
| Main branches | Divides into two pulmonary arteries, one to each lung, which branch into smaller and smaller vessels. |

**Clinical relevance**

- Pulmonary embolism is a sudden blockage of a lung artery, most often by a clot from a leg vein (deep vein thrombosis).
- Pulmonary hypertension is higher than normal blood pressure in the lung vessels and can lead to heart failure and arrhythmias.
- Pulmonary valve stenosis makes the valve too narrow or stiff and limits flow into the pulmonary artery; it is one of the four defects of tetralogy of Fallot.
- Patent ductus arteriosus is a connection between the pulmonary artery and the aorta that does not close properly after birth.

**Exam tip**

Pulmonary arteries carry oxygen-poor blood from the right ventricle to the lungs, the opposite of systemic arteries.

**Sources**

- [Structure of the Heart - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html) (Public domain)
- [Circulatory Pathways - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html) (Public domain)
- [Classification & Structure of Blood Vessels - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/classification.html) (Public domain)
- [Lung Anatomy - NCI SEER Training Modules](https://training.seer.cancer.gov/lung/anatomy/) (Public domain)
- [How the Heart Works: Blood Flow - NHLBI](https://www.nhlbi.nih.gov/health/heart/blood-flow) (Public domain)
- [Pulmonary Embolism - MedlinePlus (NLM)](https://medlineplus.gov/pulmonaryembolism.html) (Public domain)
- [Pulmonary Hypertension - MedlinePlus (NLM)](https://medlineplus.gov/pulmonaryhypertension.html) (Public domain)
- [Congenital Heart Defects: Types - NHLBI](https://www.nhlbi.nih.gov/health/congenital-heart-defects/types) (Public domain)

**What was checked on each page**

- https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html: Pulmonary semilunar valve lies between the right ventricle and the pulmonary trunk; semilunar valves at bases of vessels leaving the ventricles.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html: Right ventricle is the pump for the pulmonary circuit; oxygen-poor blood from right ventricle to lungs, returns to left atrium.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/classification.html: Pulmonary arteries carry low-oxygen blood from the right ventricle to the lungs; systemic arteries carry oxygenated blood.
- https://training.seer.cancer.gov/lung/anatomy/: Pulmonary artery carries oxygen-poor blood from the right side of the heart, splits into two arteries, one per lung, keeps dividing, ends in capillaries around alveolar sacs (O2 taken up, CO2 released); pulmonary artery enters at the hilus on the medial surface; bronchial arteries from the aorta nourish the lung.
- https://www.nhlbi.nih.gov/health/heart/blood-flow: Pulmonary valve between right ventricle and pulmonary artery; pulmonary artery carries oxygen-poor blood to the lungs.
- https://medlineplus.gov/pulmonaryembolism.html: Sudden blockage in a lung artery; usually a clot from deep vein thrombosis in a leg vein.
- https://medlineplus.gov/pulmonaryhypertension.html: PH: blood pressure in the lungs higher than normal; complications include heart failure and arrhythmias.
- https://www.nhlbi.nih.gov/health/congenital-heart-defects/types: Pulmonary stenosis: pulmonary valve too narrow or stiff, limits flow to pulmonary artery; one of the four defects of tetralogy of Fallot; PDA connects aorta with pulmonary artery.

---

## Common carotid artery  (`common carotid artery`)

*part · vessel · cardiovascular · 1 FMA ids · covers: common carotid artery*

**Summary (plain)**

The common carotid arteries are two large blood vessels, one on each side of the neck, that carry blood from the heart up to the head.

**What it does (plain)**

They bring oxygen-rich blood to the head and neck, including the brain, through their two branches.

**For students: description**

The common carotid arteries are a pair of arteries that supply oxygenated blood to the head and neck. The left one branches from the aorta (at the aortic arch); the right one arises from the brachiocephalic (innominate) artery. Each runs up the side of the neck and divides into an internal carotid artery, which supplies the brain and eyes, and an external carotid artery, which supplies the face, tongue and outer head.

**Location & neighbours**

In the neck, one on each side, running upward until it divides at the level of the upper border of the thyroid cartilage.

| Detail | |
|---|---|
| Origin | Left: from the aortic arch. Right: from the brachiocephalic (innominate) artery. |
| Supplies / drains | The structures of the head and neck, including the brain, eyes, face and tongue, through its branches. |
| Main branches | Ends by dividing into the internal carotid artery (brain and eyes) and the external carotid artery (face, tongue and outer parts of the head). |

**Clinical relevance**

- In carotid artery disease the carotid arteries become narrowed or blocked, usually by atherosclerosis (plaque made of fat, cholesterol, calcium and other substances).
- Carotid artery disease can block blood flow to the brain and cause a stroke; a piece of plaque or a clot may lodge in a smaller brain artery.  → disease page `ischemic_stroke`
- Carotid disease often causes no symptoms until narrowing is severe; signs include a bruit heard with a stethoscope or a transient ischemic attack (mini-stroke).
- Treatment may include carotid endarterectomy (surgery to remove the plaque) or angioplasty with a stent.

**Exam tip**

Each common carotid artery divides into the internal and external carotid arteries at the level of the upper border of the thyroid cartilage.

**Sources**

- [Carotid Artery, Common - MeSH concept M0026594 (NLM)](https://id.nlm.nih.gov/mesh/M0026594.json) (Public domain)
- [Carotid artery - NCI Dictionary of Cancer Terms (glossary API)](https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/carotid-artery) (Public domain)
- [Common Carotid Artery C12687 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12687?include=definitions) (CC BY 4.0)
- [Circulatory Pathways - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html) (Public domain)
- [Carotid Artery Disease - MedlinePlus (NLM)](https://medlineplus.gov/carotidarterydisease.html) (Public domain)

**What was checked on each page**

- https://id.nlm.nih.gov/mesh/M0026594.json: Scope note: the two principal arteries supplying the head and neck; each ascends one side of the neck and divides at the upper border of the thyroid cartilage into external and internal carotid arteries.
- https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/carotid-artery: Large vessel carrying blood from the heart to the head; one on each side of the neck; divides into two branches, one to brain and eyes, the other to face, tongue and outer head.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12687?include=definitions: NCI definition: one of a pair supplying oxygenated blood to head and neck; left branches from the aorta; right arises from the innominate (brachiocephalic) artery.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html: Branches of the aortic arch are the brachiocephalic, left common carotid and left subclavian arteries; the internal carotid and vertebral arteries supply the brain.
- https://medlineplus.gov/carotidarterydisease.html: Carotid arteries are two large vessels in the neck supplying brain and head; disease narrows/blocks them, usually atherosclerosis (plaque of fat, cholesterol, calcium...); plaque piece or clot can lodge in smaller brain artery; can cause stroke; often no symptoms until severe; bruit, TIA; endarterectomy; angioplasty and stent.

---

## Internal jugular vein  (`internal jugular vein`)

*part · vessel · cardiovascular · 2 FMA ids · covers: internal jugular vein*

**Summary (plain)**

The internal jugular vein is a large vein in the neck. It starts at the base of the skull and runs down the neck to join another large vein.

**What it does (plain)**

It carries blood away from the brain, face and neck back toward the heart.

**For students: description**

The internal jugular vein is one of the jugular veins, the veins of the neck that drain the brain, face and neck. It begins as a continuation of the sigmoid sinus, a venous channel of the dura mater, and leaves the skull through the jugular foramen. It then joins the subclavian vein to form the brachiocephalic vein, which leads to the superior vena cava.

**Location & neighbours**

In the neck. It leaves the skull base through the jugular foramen, where the temporal and occipital bones meet, and ends by joining the subclavian vein.

| Detail | |
|---|---|
| Origin | Continues from the sigmoid sinus of the dura mater; drains into the brachiocephalic vein (formed with the subclavian vein). |
| Supplies / drains | Drains the brain, face and neck (as stated for the jugular veins). |
| Main branches | *(blank)* |

**Clinical relevance**

- Jugular venous distension: when superior vena cava pressure rises, the jugular vein bulges and can be seen higher in the neck than usual.
- Jugular venous distension is one of the signs of heart failure, along with breathlessness and fluid build-up.  → disease page `heart_failure`
- Jugular venous pressure is estimated from the height of the jugular venous pulse above the right atrium, viewed with the patient lying back with the neck at 45 degrees.

**Exam tip**

The internal jugular vein leaves the skull through the jugular foramen together with the glossopharyngeal, vagus and accessory nerves (cranial nerves IX, X and XI).

**Sources**

- [Internal Jugular Vein C32849 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32849?include=definitions,synonyms) (CC BY 4.0)
- [Jugular Foramen C12496 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12496?include=definitions) (CC BY 4.0)
- [Jugular Veins - MeSH concept M0011872 (NLM)](https://id.nlm.nih.gov/mesh/M0011872.json) (Public domain)
- [Left Brachiocephalic Vein C32964 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32964?include=definitions) (CC BY 4.0)
- [Jugular Venous Distension C191482 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C191482?include=definitions) (CC BY 4.0)
- [Jugular Venous Pressure C191459 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C191459?include=definitions) (CC BY 4.0)
- [Heart Failure C50577 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C50577?include=definitions) (CC BY 4.0)

**What was checked on each page**

- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32849?include=definitions,synonyms: NCI definition: continuation of the sigmoid sinus of the dura mater; joins the subclavian vein to form the brachiocephalic vein.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12496?include=definitions: Jugular foramen: opening at the skull base between temporal and occipital bones, transmitting cranial nerves IX, X and XI, the inferior petrosal sinus and the internal jugular vein.
- https://id.nlm.nih.gov/mesh/M0011872.json: Jugular veins: veins in the neck which drain the brain, face and neck into the brachiocephalic or subclavian veins.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32964?include=definitions: Left brachiocephalic vein joins the right innominate vein to form the superior vena cava.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C191482?include=definitions: Jugular venous distension: jugular vein bulges from raised SVC pressure and is visible higher in the neck than usual.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C191459?include=definitions: JVP: estimated height of the mean jugular venous pulse above the right atrium, observed with the patient supine and neck at 45 degrees.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C50577?include=definitions: Heart failure: heart cannot pump enough blood for tissue needs; signs include breathlessness on mild exertion, orthopnoea, fluid retention, jugular venous distension, pulmonary oedema.

---

## Left coronary artery  (`group:v_coronary_l`)

*group · vessel · cardiovascular · 7 FMA ids · covers: circumflex branch of coronary artery, conus branch of anterior interventricular branch of coronary artery, diagonal branch of anterior descending branch of coronary artery, first anterior branch of anterior interventricular branch of coronary artery, second anterior branch of anterior interventricular branch of coronary artery, third anterior branch of anterior interventricular branch of coronary artery, trunk of coronary artery*

**Summary (plain)**

The left coronary artery is one of the two arteries that feed the heart muscle itself. It starts from the aorta just above the heart and runs over the heart's surface.

**What it does (plain)**

It brings oxygen-rich blood to most of the left side of the heart and to the wall between the two lower chambers.

**For students: description**

The left coronary artery is one of the two coronary arteries, which are the only branches of the ascending aorta. It supplies the left atrium, the left ventricle and the septum between the ventricles. Its two main branches are the left anterior descending artery and the circumflex artery.

**Location & neighbours**

On the surface of the heart, starting from the ascending aorta.

| Detail | |
|---|---|
| Origin | Arises from the ascending aorta. |
| Supplies / drains | Left atrium, left ventricle and the interventricular septum; the left anterior descending artery supplies parts of both ventricles, and the circumflex artery part of the left ventricle. |
| Main branches | Left anterior descending artery; circumflex artery. |

**Clinical relevance**

- Plaque buildup (atherosclerosis) narrows the coronary arteries in coronary artery disease, the most common heart disease in the United States; reduced flow causes angina.  → disease page `acute_coronary_syndrome`
- A heart attack happens when a blood clot suddenly blocks blood flow to part of the heart, permanently damaging the muscle.  → disease page `acute_coronary_syndrome`
- Blocked coronary arteries can be opened with angioplasty or bypassed with coronary artery bypass grafting (CABG).

**Exam tip**

The right and left coronary arteries are the only branches of the ascending aorta.

**Sources**

- [How the Heart Works: Blood Flow - NHLBI](https://www.nhlbi.nih.gov/health/heart/blood-flow) (Public domain)
- [Circulatory Pathways - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html) (Public domain)
- [Structure of the Heart - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html) (Public domain)
- [Coronary Artery Disease - MedlinePlus (NLM)](https://medlineplus.gov/coronaryarterydisease.html) (Public domain)

**What was checked on each page**

- https://www.nhlbi.nih.gov/health/heart/blood-flow: Coronary arteries branch from the aorta and supply the heart muscle; left coronary artery supplies left atrium, left ventricle and septum between ventricles; circumflex branches from left coronary, supplies part of left ventricle; left anterior descending branches from left coronary, supplies parts of both ventricles.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html: Coronary arteries are the only vessels that branch from the ascending aorta.
- https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html: Right and left coronary arteries, branches of the ascending aorta, supply the heart wall (myocardium).
- https://medlineplus.gov/coronaryarterydisease.html: CAD most common heart disease in the United States; plaque buildup (atherosclerosis); angina from reduced flow; heart attack when a clot suddenly blocks blood flow, permanent damage; angioplasty and CABG.

---

## Right coronary artery  (`group:v_coronary_r`)

*group · vessel · cardiovascular · 7 FMA ids · covers: first anterior ventricular branch of coronary artery, first septal branch of posterior interventricular artery, marginal branch of coronary artery, posterior interventricular branch of coronary artery, posterior ventricular branch of coronary artery, second septal branch of posterior interventricular artery, trunk of coronary artery*

**Summary (plain)**

The right coronary artery is one of the two arteries that feed the heart muscle itself. It starts from the aorta just above the heart and runs over the heart's surface.

**What it does (plain)**

It brings oxygen-rich blood to the right upper chamber and to parts of both lower chambers, including their underside.

**For students: description**

The right coronary artery is one of the two coronary arteries, which are the only branches of the ascending aorta. It supplies the right atrium and parts of both ventricles. Its branches include the marginal arteries and the posterior descending artery, which supplies the bottom of both ventricles.

**Location & neighbours**

On the surface of the heart, starting from the ascending aorta.

| Detail | |
|---|---|
| Origin | Arises from the ascending aorta. |
| Supplies / drains | Right atrium and parts of both ventricles; the marginal arteries supply the surface of the right atrium, and the posterior descending artery the bottom of both ventricles. |
| Main branches | Marginal arteries; posterior descending artery. |

**Clinical relevance**

- Plaque buildup (atherosclerosis) narrows the coronary arteries in coronary artery disease, the most common heart disease in the United States; reduced flow causes angina.  → disease page `acute_coronary_syndrome`
- A heart attack happens when a blood clot suddenly blocks blood flow to part of the heart, permanently damaging the muscle.  → disease page `acute_coronary_syndrome`
- Blocked coronary arteries can be opened with angioplasty or bypassed with coronary artery bypass grafting (CABG).

**Exam tip**

The posterior descending artery, which supplies the bottom of both ventricles, is a branch of the right coronary artery.

**Sources**

- [How the Heart Works: Blood Flow - NHLBI](https://www.nhlbi.nih.gov/health/heart/blood-flow) (Public domain)
- [Circulatory Pathways - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html) (Public domain)
- [Structure of the Heart - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html) (Public domain)
- [Coronary Artery Disease - MedlinePlus (NLM)](https://medlineplus.gov/coronaryarterydisease.html) (Public domain)

**What was checked on each page**

- https://www.nhlbi.nih.gov/health/heart/blood-flow: Right coronary artery supplies the right atrium and parts of both ventricles; marginal arteries branch from it and supply the surface of the right atrium; posterior descending artery branches from it and supplies the bottom of both ventricles.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html: Coronary arteries are the only vessels that branch from the ascending aorta.
- https://training.seer.cancer.gov/anatomy/cardiovascular/heart/structure.html: Right and left coronary arteries, branches of the ascending aorta, supply the heart wall (myocardium).
- https://medlineplus.gov/coronaryarterydisease.html: CAD most common heart disease in the United States; plaque buildup (atherosclerosis); angina from reduced flow; heart attack when a clot suddenly blocks blood flow, permanent damage; angioplasty and CABG.

---

## Hepatic portal vein  (`hepatic portal vein`)

*part · vessel · cardiovascular · 1 FMA ids · covers: hepatic portal vein*

**Also called:** portal vein

**Summary (plain)**

The hepatic portal vein is a short, thick vein in the belly that carries blood from the gut and nearby organs into the liver.

**What it does (plain)**

It brings nutrient-rich blood from digestion to the liver, so the liver handles it before it reaches the rest of the body.

**For students: description**

The hepatic portal vein is a short, thick vein formed by the union of the superior mesenteric vein and the splenic vein. It carries blood rich in absorbed products of digestion from the stomach, intestines, spleen, pancreas and gallbladder to the liver. The liver therefore gets blood from two sources: this vein and the common hepatic artery, which brings oxygenated blood.

**Location & neighbours**

In the abdomen, running into the liver. At its far end it divides into the left and right portal veins.

| Detail | |
|---|---|
| Origin | Formed by the union of the superior mesenteric vein and the splenic vein; drains into the liver, where it divides into the left and right portal veins. |
| Supplies / drains | Drains the stomach, intestines, spleen, pancreas and gallbladder. |
| Main branches | Tributaries: the superior mesenteric vein and the splenic vein. Ends by dividing into the left and right portal veins. |

**Clinical relevance**

- Portal hypertension: scar tissue in a cirrhotic liver slows blood flow and raises pressure in the portal vein.
- Portal hypertension can cause enlarged veins (varices) in the oesophagus, stomach or intestines, which may burst and bleed internally.
- Portal hypertension can also cause fluid in the abdomen (ascites), swelling of the legs and confusion from toxins reaching the brain (hepatic encephalopathy).
- A blood clot can form in the portal vein (portal vein thrombosis).

**Exam tip**

The hepatic portal vein is formed by the union of the superior mesenteric vein and the splenic vein.

**Sources**

- [Portal Vein - MeSH concept M0017339 (NLM)](https://id.nlm.nih.gov/mesh/M0017339.json) (Public domain)
- [portal vein - NCI Dictionary of Cancer Terms (glossary API)](https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/portal-vein) (Public domain)
- [Portal Vein C33343 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C33343?include=definitions) (CC BY 4.0)
- [Portal Vein Bifurcation C132413 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C132413?include=definitions) (CC BY 4.0)
- [Portal Vein Thrombosis C78565 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C78565?include=definitions) (CC BY 4.0)
- [Accessory Organs of the Digestive System - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html) (Public domain)
- [Definition & Facts for Cirrhosis - NIDDK](https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts) (Public domain)

**What was checked on each page**

- https://id.nlm.nih.gov/mesh/M0017339.json: Scope note: a short thick vein formed by union of the superior mesenteric vein and the splenic vein.
- https://webapis.cancer.gov/glossary/v1/Terms/Cancer.gov/Patient/en/portal-vein: A blood vessel carrying blood to the liver from the intestines, spleen, pancreas and gallbladder; also called hepatic portal vein.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C33343?include=definitions: NCI definition: short thick trunk vein carrying blood with absorbed products of digestion from the intestines directly to the liver; synonym Hepatic Portal Vein.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C132413?include=definitions: Distal end of the main portal vein branches into the left and right portal veins.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C78565?include=definitions: Portal vein thrombosis: formation of a blood clot in the portal vein.
- https://training.seer.cancer.gov/anatomy/digestive/regions/accessory.html: Liver receives blood from two sources: oxygenated blood via the common hepatic artery, nutrient-rich blood from the digestive tract via the hepatic portal vein.
- https://www.niddk.nih.gov/health-information/liver-disease/cirrhosis/definition-facts: Portal vein carries blood from stomach, intestines, spleen, gallbladder and pancreas to the liver; portal hypertension when liver scar tissue slows flow and raises portal pressure; complications: ascites, oedema of legs/ankles/feet, varices in oesophagus/stomach/intestines that can burst and bleed, hepatic encephalopathy.

---

## Femoral artery  (`femoral artery`)

*part · vessel · cardiovascular · 1 FMA ids · covers: femoral artery*

**Summary (plain)**

The femoral artery is the main artery of the thigh. It starts in the groin and runs down toward the leg.

**What it does (plain)**

It carries oxygen-rich blood down into the leg.

**For students: description**

The femoral artery is the main artery of the thigh and continues on from the external iliac artery. Its first part, the common femoral artery, begins at the inguinal ligament in the groin and splits into the deep and superficial femoral arteries. Through it and its branches, blood reaches the lower limb.

**Location & neighbours**

In the groin (inguinal region) and thigh, beginning at the inguinal ligament and running down toward the lower limb.

| Detail | |
|---|---|
| Origin | Continuation of the external iliac artery; the common femoral artery begins at the inguinal ligament. |
| Supplies / drains | The lower limb (thigh and the leg below). |
| Main branches | The common femoral artery divides into the deep femoral artery and the superficial femoral artery. |

**Clinical relevance**

- Peripheral artery disease is narrowing of arteries outside the heart, mostly from atherosclerosis; in the legs it can cause pain on walking and weak or absent pulses in the legs or feet.
- In the United States, more than 8 million people aged 40 and older have peripheral artery disease.
- For some heart and artery tests, a catheter is passed into an artery in the groin and guided to the heart or the narrowed vessel.

**Exam tip**

A delay between the right radial pulse and the femoral pulse (radial-femoral lag) suggests coarctation of the aorta.

**Sources**

- [Femoral Artery - MeSH concept M0008311 (NLM)](https://id.nlm.nih.gov/mesh/M0008311.json) (Public domain)
- [Femoral Artery C12715 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12715?include=definitions,synonyms) (CC BY 4.0)
- [Common Femoral Artery C32354 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32354?include=definitions) (CC BY 4.0)
- [Radial-Femoral Lag C168415 - NCI Thesaurus (EVS API)](https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C168415?include=definitions) (CC BY 4.0)
- [Circulatory Pathways - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html) (Public domain)
- [Peripheral Arterial Disease - MedlinePlus (NLM)](https://medlineplus.gov/peripheralarterialdisease.html) (Public domain)
- [Peripheral Artery Disease - What Is PAD? - NHLBI](https://www.nhlbi.nih.gov/health/peripheral-artery-disease) (Public domain)
- [Peripheral Artery Disease - Diagnosis - NHLBI](https://www.nhlbi.nih.gov/health/peripheral-artery-disease/diagnosis) (Public domain)
- [Cardiac Catheterization - During - NHLBI](https://www.nhlbi.nih.gov/health/cardiac-catheterization/during) (Public domain)

**What was checked on each page**

- https://id.nlm.nih.gov/mesh/M0008311.json: Scope note: the main artery of the thigh, a continuation of the external iliac artery.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C12715?include=definitions,synonyms: NCI definition: an artery that starts within the inguinal region and extends to the lower extremities.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C32354?include=definitions: Common femoral artery arises from the external iliac artery at the inguinal ligament and bifurcates into the deep and superficial femoral arteries.
- https://api-evsrest.nci.nih.gov/api/v1/concept/ncit/C168415?include=definitions: Radial-femoral lag: delay between the right radial pulse upstroke and the femoral pulse; its presence suggests aortic coarctation.
- https://training.seer.cancer.gov/anatomy/cardiovascular/blood/pathways.html: Branches of the external iliac artery supply the lower extremity.
- https://medlineplus.gov/peripheralarterialdisease.html: PAD is narrowing of vessels outside the heart; usually affects flow to the legs; caused by atherosclerosis; leg pain or heaviness when walking; weak or absent pulses in legs or feet.
- https://www.nhlbi.nih.gov/health/peripheral-artery-disease: PAD caused by atherosclerosis; lower extremity PAD reduces flow to legs and feet; in the US more than 8 million people aged 40 and older have PAD.
- https://www.nhlbi.nih.gov/health/peripheral-artery-disease/diagnosis: Doctors check for weak pulses in the legs; ABI is usually the first test; for angiography a catheter is inserted into an artery in the groin and guided to the affected area.
- https://www.nhlbi.nih.gov/health/cardiac-catheterization/during: Illustration caption: catheter inserted through the groin to the heart; numbing at upper thigh, arm or neck site.

---

## Optic nerve  (`optic nerve`)

*part · nerve · nervous · 2 FMA ids · covers: optic nerve*

**Summary (plain)**

The optic nerve is a cable of nerve fibers that runs from the back of each eye to the brain.

**What it does (plain)**

It carries signals from the retina to the brain, which turns them into the images you see.

**For students: description**

The optic nerve is a bundle of more than a million nerve fibers. Each eye has one, linking its retina to the brain. It is one of the cranial nerves serving a special sense (vision), and those nerves carry only sensory fibers. Damage to it can cause vision loss.

**Location & neighbours**

It runs from the retina at the back of the eye to the brain, passing through the optic foramen at the apex of the orbit together with the ophthalmic artery. Inside the skull it lies above the tentorium (supratentorial).

| Detail | |
|---|---|
| Origin | The retina at the back of the eye. |
| Type | sensory |
| Supplies | Carries visual signals from the retina to the brain. |

**Clinical relevance**

- Glaucoma damages the optic nerve, usually through slowly rising fluid pressure in the eye; it is a leading cause of blindness in the United States.
- Optic neuritis is inflammation of the optic nerve, often from infection or immune conditions such as multiple sclerosis.
- Optic nerve atrophy is degeneration of the nerve from poor blood flow, disease, injury or toxins.
- Optic nerve head drusen are deposits of protein and calcium salts that build up in the nerve over time.

**Exam tip**

Each optic nerve is a bundle of more than a million nerve fibers carrying visual signals.

**Sources**

- [Optic Nerve Disorders - MedlinePlus (NLM)](https://medlineplus.gov/opticnervedisorders.html) (Public domain)
- [How the Eyes Work - National Eye Institute](https://www.nei.nih.gov/learn-about-eye-health/healthy-vision/how-eyes-work) (Public domain)
- [Peripheral Nervous System - NCI SEER Training Modules](https://training.seer.cancer.gov/anatomy/nervous/organization/pns.html) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), the skull as a whole - PubAnnotation GrayAnatomy doc 46](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/46) (Public domain)
- [Gray's Anatomy of the Human Body, 20th ed. (1918), skull (interior of the base) - PubAnnotation GrayAnatomy doc 47](https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47) (Public domain)
- [Tentorium - NCI SEER Training Modules](https://training.seer.cancer.gov/cns/cns-anatomy/tentorium.html) (Public domain)
- [Glaucoma - MedlinePlus (NLM)](https://medlineplus.gov/glaucoma.html) (Public domain)

**What was checked on each page**

- https://medlineplus.gov/opticnervedisorders.html: Optic nerve is a bundle of more than 1 million nerve fibers carrying visual messages; one connecting the back of each eye (retina) to the brain; damage causes vision loss; glaucoma is the leading cause of blindness in the United States, usually from increased eye pressure; optic neuritis (infections, immune diseases like MS); optic nerve atrophy (poor blood flow, disease, trauma, toxins); optic nerve head drusen (protein and calcium salts).
- https://www.nei.nih.gov/learn-about-eye-health/healthy-vision/how-eyes-work: Optic nerve carries electrical signals from the retina to the brain, which turns them into images.
- https://training.seer.cancer.gov/anatomy/nervous/organization/pns.html: Twelve pairs of cranial nerves; three nerves associated with special senses of smell, vision, hearing and equilibrium have only sensory fibers (page does not name the optic nerve itself).
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/46: Apex of the orbit corresponds to the optic foramen.
- https://pubannotation.org/docs/sourcedb/GrayAnatomy/sourceid/47: Optic foramen transmits the optic nerve and ophthalmic artery.
- https://training.seer.cancer.gov/cns/cns-anatomy/tentorium.html: Optic nerve listed among supratentorial structures.
- https://medlineplus.gov/glaucoma.html: Glaucoma damages the optic nerve; fluid pressure inside the eye slowly rises in the most common types.

---

