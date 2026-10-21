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
