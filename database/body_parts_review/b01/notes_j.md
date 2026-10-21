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
