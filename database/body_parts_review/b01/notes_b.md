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
