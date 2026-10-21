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
