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
