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
