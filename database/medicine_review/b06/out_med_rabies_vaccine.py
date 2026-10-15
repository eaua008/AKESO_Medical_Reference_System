DOH_URL = "https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures"
WHO_PEP_URL = "https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations"
WHO_PP_URL = "https://cdn.who.int/media/docs/default-source/immunization/position_paper_documents/rabies/pp-rabies-summary-2018.pdf"
MSF_URL = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/rabies-vaccine-16687811.html"
ABTC_URL = "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186"

MED = {
  "id": "med_rabies_vaccine",
  "desc_add": "WHO recommends the intradermal route for PEP because it uses 60–80% less vaccine (1–2 vials per course versus 4–5 for intramuscular schedules) and a single vial can be shared between several patients. Philippine Animal Bite Treatment Centers (513 by July 2017) give the vaccine almost exclusively intradermally using the modified 2-site Thai Red Cross regimen, and DOH requires WHO-prequalified vaccine for PEP. Since 2016, government policy has provided all four vaccine visits free of charge, although stock-outs still force some patients to buy vaccine privately.",
  "facts": {
    "indication": [
      "Infants born to rabid mothers: vaccine together with RIG as early as possible after birth (DOH)",
      "Pre-exposure prophylaxis for people in remote rabies-endemic areas with poor PEP access or dog-bite incidence above 5% per year (WHO)",
    ],
    "adverse": [],
    "contraindication": [
      "Nerve-tissue vaccines should be avoided: less immunogenic and more severe adverse effects than cell-culture vaccines (MSF)",
      "Intradermal route only where correct ID technique can be assured; otherwise use IM (MSF)",
    ],
    "interaction": [
      "Other vaccines given the same day: use separate syringes and injection sites (MSF).",
      "Chronic liver disease, chloroquine use or systemic steroids: DOH gives the standard IM regimen, without delaying vaccination.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("DOH Administrative Order 2018-0013", "Department of Health (Philippines). Administrative Order No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 16 April 2018. (Text reproduced on LegalDex.)", DOH_URL),
    ("WHO PEP recommendations", "World Health Organization. Rabies: PEP recommendations – WHO recommends the intradermal route for rabies post-exposure prophylaxis. WHO Control of Neglected Tropical Diseases.", WHO_PEP_URL),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Rabies vaccine. MSF Medical Guidelines.", MSF_URL),
    ("PLOS ONE", "Amparo ACB, Jayme SI, Roces MCR, et al. The evaluation of operating Animal Bite Treatment Centers in the Philippines from a health provider perspective. PLoS ONE. 2018;13(7):e0199186.", ABTC_URL),
  ],
  "links": [
    ("hiv_infection", "caution", "HIV/AIDS counts as immunocompromised: DOH uses the standard IM regimen (not the ID regimen) plus RIG for category II and III exposures; WHO adds a third PrEP dose on day 21–28."),
  ],
  "sources": [
    ("DOH AO 2018", "DOH Administrative Order 2018-0013", "Department of Health (Philippines). AO No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 2018.", DOH_URL),
    ("WHO 2018", "WHO position paper (summary)", "World Health Organization. Rabies vaccines and immunoglobulins: WHO position, April 2018 (summary).", WHO_PP_URL),
    ("MSF", "MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Rabies vaccine.", MSF_URL),
  ],
  "doses": [
    ("adult", "PEP, category II/III (DOH ID regimen)", "ID", "0.1 mL at 2 sites", "Days 0, 3, 7, 28", "4 visits (2-2-2-0-2)", "—", "DOH AO 2018", "One dose per deltoid; day 28 may be omitted with WHO-prequalified vaccine (2-2-2-0-0)"),
    ("adult", "PEP, category II/III (WHO 1-week ID)", "ID", "0.1 mL at 2 sites", "Days 0, 3, 7", "1 week", "—", "WHO 2018", "Category III: plus RIG"),
    ("adult", "PEP, Zagreb (2-0-1-0-1)", "IM", "0.5 mL PVRV or 1 mL PCECV", "2 doses day 0; 1 dose days 7, 21", "3 weeks", "—", "DOH AO 2018", "Day 0 dose in both deltoids"),
    ("adult", "PEP, shortened IM (1-1-1-1-0)", "IM", "0.5 mL PVRV or 1 mL PCECV", "Days 0, 3, 7, 14", "2 weeks", "—", "DOH AO 2018", "WHO: 4th dose any day from 14 to 28"),
    ("adult", "PEP, previously vaccinated", "ID", "0.1 mL at 1 site", "Days 0, 3", "2 visits", "—", "DOH AO 2018", "Or 0.1 mL at 4 sites on day 0; no RIG; IM boosters discouraged"),
    ("adult", "PrEP, immunocompetent", "ID", "0.1 mL at 2 sites", "Days 0, 7", "1 week", "—", "WHO 2018", "Or 1 vial IM at 1 site on days 0, 7"),
    ("adult", "PrEP, immunocompromised", "IM", "1 vial (0.5 mL PVRV / 1 mL PCECV)", "Days 0, 7, 21–28", "3–4 weeks", "—", "DOH AO 2018", "WHO: ID or IM plus third dose day 21–28"),
    ("child", "PEP, category II/III (DOH ID regimen)", "ID", "0.1 mL at 2 sites", "Days 0, 3, 7, 28", "4 visits (2-2-2-0-2)", "—", "DOH AO 2018", "Same dose as adults; anterolateral thigh in infants"),
    ("child", "PEP, IM regimens", "IM", "0.5 mL PVRV or 1 mL PCECV", "As adult schedule", "2–3 weeks", "—", "MSF", "Anterolateral thigh if < 2 y; deltoid if ≥ 2 y; never gluteal"),
    ("child", "PrEP, immunocompetent", "ID", "0.1 mL at 2 sites", "Days 0, 7", "1 week", "—", "WHO 2018", "Schedules apply to all age groups"),
  ],
  "notes": [
    ("forms_ph", "DOH program vaccines: PVRV 0.5 mL/vial and PCECV 1 mL/vial (powder with diluent); ID dose 0.1 mL for both. PNF entry not readable.", "", "DOH AO 2018"),
    ("administration", "Each ID dose must raise a wheal of at least 3 mm (1 mL syringe, 27 G needle); repeat any dose given SC or IM by mistake.", "", "DOH AO 2018"),
    ("administration", "A delayed dose does not restart the schedule; changing vaccine product or route mid-course is acceptable if unavoidable.", "", "DOH AO 2018"),
    ("administration", "Biting dog or cat is observed for 14 days; non-WHO-prequalified PEP is stopped if the animal stays healthy. New exposure within 3 months of completed PEP needs wound care only (WHO).", "", "DOH AO 2018"),
    ("administration", "Start PEP as soon as possible even if the patient presents long after exposure; check national schedules (MSF).", "", "MSF"),
    ("administration", "DOH allows reconstituted vaccine to be kept refrigerated and used within 8 hours (enables ID vial sharing); MSF says use immediately.", "", "DOH AO 2018"),
    ("pregnancy", "Pregnancy and infancy are not contraindications to PVRV or PCECV; none in breast-feeding (MSF).", "", "DOH AO 2018"),
    ("monitor", "Anaphylaxis: epinephrine 0.1% 0.5 mL (adults) or 0.01 mL/kg, max 0.5 mL (children), repeat every 10–20 min up to 3 doses; then steroids. Record and report severe adverse events.", "", "DOH AO 2018"),
    ("monitor", "Routine boosters or neutralizing-antibody serology after PrEP only if exposure risk remains high.", "", "WHO 2018"),
  ],
  "checked": [
    (DOH_URL, "DOH AO 2018-0013: Table 2 PVRV 0.5 mL/vial, PCECV 1 mL/vial, ID 0.1 mL, IM 0.5/1.0 mL; ID PEP 2-2-2-0-2 (days 0, 3, 7, 28), day 28 omissible for WHO-prequalified (2-2-2-0-0); wheal ≥3 mm, 1 mL 27G syringe, repeat if SC/IM; Zagreb 2-0-1-0-1 and 1-1-1-1-0 IM; never gluteal; PrEP ID/IM days 0, 7, 21/28 (21/28 dropped for immunocompetent with prequalified vaccine; full IM for immunocompromised); booster ID 1 site days 0, 3 or 4 sites day 0, IM boosters discouraged; immunocompromised standard IM + RIG; chronic liver disease/chloroquine/steroids standard IM no delay; pregnancy/infancy not contraindications; infants of rabid mothers vaccine + RIG; delayed dose continue; product/route change acceptable; 14-day animal observation; anaphylaxis epinephrine doses; reconstituted refrigerated use within 8 h; 2–8 °C."),
    (WHO_PP_URL, "WHO 2018 summary: PrEP 2-site ID or 1-site IM days 0 and 7, all ages; IM <2 y anterolateral thigh, ≥2 y deltoid; immunocompromised PrEP third dose day 21–28 and full PEP with RIG; PEP ID 2-site days 0, 3, 7; IM 1-site days 0, 3, 7 + one dose day 14–28; Zagreb; previously immunized 1-site ID days 0, 3 or 4-site day 0, no RIG; new exposure within 3 months only wound care; delayed dose resume; booster/serology only if high risk persists; PrEP for remote areas with dog-bite incidence >5%/yr."),
    (WHO_PEP_URL, "WHO PEP page: ID recommended; reduces vaccine volume 60–80%; full ID course 1–2 vials vs IM 4–5 vials; one-week 2-site ID days 0, 3, 7; route/product change acceptable."),
    (MSF_URL, "MSF rabies vaccine: CCEEV powder + diluent 0.5 or 1 mL; IM not gluteal, <2 y thigh, ≥2 y deltoid; ID 0.1 mL; Zagreb, Essen; continue schedule if delayed/route changed; start even if presenting late; check national schedules; ID only if correct technique assured else IM; separate syringes/sites with RIG or other vaccines; no contraindication in pregnancy/breast-feeding; avoid nerve-tissue vaccines; reconstituted use immediately."),
    (ABTC_URL, "Amparo et al. 2018: 513 ABTCs by July 2017; ARV almost exclusively ID using modified 2-site Thai Red Cross regimen 2-2-2-0-2; immunocompromised/HIV get IM; only WHO pre-qualified vaccine; PVRV and PCECV; since 2016 all four ARV visits free; stock-outs force private purchase; single vial for multiple patients."),
  ],
}
