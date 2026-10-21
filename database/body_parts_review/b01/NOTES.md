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
