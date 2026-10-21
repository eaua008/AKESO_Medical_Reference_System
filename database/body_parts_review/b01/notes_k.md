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
