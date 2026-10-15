DOH_URL = "https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures"
WHO_PEP_URL = "https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations"
WHO_PP_URL = "https://cdn.who.int/media/docs/default-source/immunization/position_paper_documents/rabies/pp-rabies-summary-2018.pdf"
MSF_URL = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/human-rabies-immunoglobulin-hrig-16688380.html"
ABTC_URL = "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186"
PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"

MED = {
  "id": "med_rabies_immunoglobulin",
  "desc_add": "In the Philippine public program, the DOH supplies only equine RIG to government Animal Bite Treatment Centers, and patients often pay out of pocket for it when stocks run out. Under DOH Administrative Order 2018-0013, RIG volume left after wound infiltration need not be injected IM and may be kept aseptically and fractionated for the next patient. When supply is limited, WHO gives priority to multiple or deep bites, bites to highly innervated parts of the body, severely immunodeficient patients, exposures to confirmed or probable rabid animals, and bat exposures.",
  "facts": {
    "indication": [
      "Category II exposures to the head or neck, which DOH manages as category III (vaccine plus RIG)",
      "Category II as well as category III exposures in immunocompromised patients (DOH, MSF)",
      "Infants born to rabid mothers, with vaccine, as early as possible after birth (DOH)",
    ],
    "adverse": [
      "Fever and joint pain (MSF)",
    ],
    "contraindication": [
      "Finger or toe wounds: infiltrate cautiously to avoid raised compartment pressure or impaired circulation",
      "Aspirate before injecting; intravascular injection risks shock (MSF)",
    ],
    "interaction": [
      "Other vaccines given the same day: use separate syringes and injection sites (MSF).",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("DOH Administrative Order 2018-0013", "Department of Health (Philippines). Administrative Order No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 16 April 2018. (Text reproduced on LegalDex.)", DOH_URL),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Human rabies immunoglobulin (HRIG). MSF Medical Guidelines.", MSF_URL),
    ("WHO PEP recommendations", "World Health Organization. Rabies: PEP recommendations – WHO recommends the intradermal route for rabies post-exposure prophylaxis. WHO Control of Neglected Tropical Diseases.", WHO_PEP_URL),
    ("PLOS ONE", "Amparo ACB, Jayme SI, Roces MCR, et al. The evaluation of operating Animal Bite Treatment Centers in the Philippines from a health provider perspective. PLoS ONE. 2018;13(7):e0199186.", ABTC_URL),
  ],
  "links": [
    ("hiv_infection", "safe", "HIV/AIDS counts as immunocompromised: DOH gives RIG with the standard IM vaccine regimen for both category II and III exposures."),
  ],
  "sources": [
    ("DOH AO 2018", "DOH Administrative Order 2018-0013", "Department of Health (Philippines). AO No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 2018.", DOH_URL),
    ("WHO 2018", "WHO position paper (summary)", "World Health Organization. Rabies vaccines and immunoglobulins: WHO position, April 2018 (summary).", WHO_PP_URL),
    ("MSF", "MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Human rabies immunoglobulin (HRIG).", MSF_URL),
  ],
  "doses": [
    ("adult", "Category III exposure, HRIG", "Infiltration", "20 IU/kg", "Single dose", "Day 0 (up to day 7)", "20 IU/kg", "DOH AO 2018", "Infiltrate full dose into and around wound(s); 150 IU/mL, 2 mL vial"),
    ("adult", "Category III exposure, ERIG / F(ab')2", "Infiltration", "40 IU/kg", "Single dose", "Day 0 (up to day 7)", "40 IU/kg", "DOH AO 2018", "200 IU/mL, 5 mL vial; e.g. 50 kg = 2000 IU = 10 mL"),
    ("adult", "Category III exposure (WHO)", "Infiltration", "HRIG 20 IU/kg; ERIG 40 IU/kg", "Single dose", "≤ day 7 after first vaccine dose", "20 / 40 IU/kg; no minimum", "WHO 2018", "As much as possible into the wound"),
    ("child", "Category III exposure, HRIG", "Infiltration", "20 IU/kg", "Single dose", "Day 0 (up to day 7)", "20 IU/kg", "MSF", "Same dose for all ages"),
    ("child", "Category III exposure, ERIG / F(ab')2", "Infiltration", "40 IU/kg", "Single dose", "Day 0 (up to day 7)", "40 IU/kg", "MSF", "If HRIG unavailable"),
  ],
  "notes": [
    ("administration", "If the computed dose is too small to cover all wounds, dilute it 2–3-fold with sterile 0.9% saline; never exceed the computed dose. Infiltrate even healed wounds.", "", "DOH AO 2018"),
    ("administration", "Use a 23–24 G, 1-inch needle and avoid repeated needle punctures into the same wound. Delay suturing for at least 2 hours after RIG if suturing cannot be avoided.", "", "DOH AO 2018"),
    ("administration", "If RIG and vaccine cannot be given on the same day, give the vaccine first; RIG is given only once per PEP course and is not indicated after day 7.", "", "DOH AO 2018"),
    ("administration", "Leftover RIG may be fractionated aseptically for other patients; remaining volume does not need IM injection.", "", "WHO 2018"),
    ("administration", "DOH still highly recommends an ERIG skin test, whereas WHO 2018 says skin testing is unnecessary and should be abandoned; follow the local program protocol.", "", "DOH AO 2018"),
    ("pregnancy", "Pregnancy and infancy are not contraindications to RIG; no contraindication in breast-feeding.", "", "DOH AO 2018"),
    ("monitor", "Observe patients for at least 1 hour after ERIG, with epinephrine available.", "", "DOH AO 2018"),
    ("monitor", "After infiltrating fingers or toes, check circulation and signs of raised compartment pressure.", "", "MSF"),
  ],
  "checked": [
    (PNF_URL, "WebFetch text of the PNF-EML PDF runs only from Abacavir to Multivitamins (offset 50000 also ends at M; total 65,922 chars). No rabies immunoglobulin entry readable, so no forms_ph note written."),
    (DOH_URL, "DOH AO 2018-0013 (16 Apr 2018), Revised Guidelines on the Management of Rabies Exposures: HRIG 20 IU/kg max, 150 IU/mL 2 mL vial; ERIG/F(ab')2 40 IU/kg max, 200 IU/mL 5 mL vial; 50 kg example 1000 IU = 6.7 mL / 2000 IU = 10 mL; infiltrate full dose even if healed; 23–24 G 1-inch needle; leftover need not be IM, may be fractionated; dilute 2–3x saline, do not exceed dose; caution fingers/toes; delay suturing ≥2 h; give with day 0 vaccine, up to day 7; vaccine first if not same day; once per course; observe ≥1 h after ERIG; ERIG skin testing highly recommended; category II head/neck managed as category III; immunocompromised (systemic steroids, chemo, HIV/AIDS) get standard IM regimen + RIG for category II and III; pregnancy and infancy not contraindications; infants of rabid mothers get vaccine + RIG ASAP after birth."),
    (WHO_PP_URL, "WHO 2018 summary: max dose 20 IU/kg hRIG, 40 IU/kg eRIG, no minimum; once, no later than day 7; infiltrate as much as possible into the wound; leftover fractionated aseptically; eRIG skin testing unnecessary; RIG prioritisation (multiple/deep bites, highly innervated parts, severe immunodeficiency, confirmed/probable rabid animal, bat exposures); vaccine never withheld for lack of RIG."),
    (WHO_PEP_URL, "WHO PEP recommendations page: category III gets RIG with vaccine plus immediate wound washing; ID 0.1 mL 2 sites days 0, 3, 7."),
    (MSF_URL, "MSF HRIG: 20 IU/kg child and adult on D0 with first vaccine; infiltrate into/around wounds; dilute 2–3-fold with 0.9% NaCl for multiple wounds; up to D7; indicated for category II and III in immunocompromised even after PrEP; AEs fever, headache, GI, joint pain, local pain, rare anaphylaxis; aspirate before injecting (shock risk); caution finger wounds (compartment pressure); separate syringes/sites with vaccines; no contraindication in pregnancy/breast-feeding; ERIG F(ab')2 40 IU/kg as substitute."),
    (ABTC_URL, "Amparo et al. 2018 PLoS ONE: only equine RIG provided by DOH (no HRIG); patients often paid out of pocket for eRIG when stocks ran out; PhilHealth ABT package PHP 3,000 covers vaccine and RIG for category III exposures."),
  ],
}
