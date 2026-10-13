MSF_ORS_URL = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/oral-rehydration-salts-ors-16684387.html"
MSF_ZN_URL = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/zinc-sulfate-oral-16684806.html"
PSPGHAN_URL = "https://pps.org.ph/wp-content/uploads/PSPGHAN-GUIDELINES-ON-THE-TREATMENT-OF-ACUTE-GASTROENTERITIS-WITH-NO-SIGNS-OF-DEHYDRATION-April-2026-1.pdf"
PHIC_URL = "https://www.philhealth.gov.ph/circulars/2022/circ2022-0026.pdf"
WHO_FS_URL = "https://www.who.int/news-room/fact-sheets/detail/diarrhoeal-disease"

MED = {
  "id": "med_ors",
  "desc_add": "In the Philippines, PhilHealth's quality policy on acute infectious gastroenteritis names ORS and IV fluids as the standard treatment for dehydration, with routine zinc 20 mg/day for 10–14 days as an adjunct in children. The Philippine Society for Pediatric Gastroenterology, Hepatology and Nutrition (PSPGHAN, 2026) recommends WHO low-osmolarity ORS plus zinc for children with no signs of dehydration, and advises against soft drinks, sports drinks and electrolyte drinks that do not meet the WHO low-osmolarity formula. WHO notes that a 10–14 day zinc course shortens a diarrhoea episode by about 25% and cuts stool volume by about 30%.",
  "facts": {
    "indication": [
      "Given alongside IV therapy in severe dehydration (WHO Plan C), once the patient is conscious and able to drink",
    ],
    "adverse": [],
    "contraindication": [
      "Severe acute malnutrition: use ReSoMal (special ORS) under medical supervision instead, except in cholera, where standard ORS is used (MSF)",
    ],
    "interaction": [
      "Zinc given with ORS: separate zinc from iron (ferrous) salts by at least 2 hours (MSF).",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("PSPGHAN (Philippine Pediatric Society)", "Philippine Society for Pediatric Gastroenterology, Hepatology and Nutrition. Guidelines for Health Care Professionals on the Treatment of Acute Gastroenteritis with No Signs of Dehydration. April 2026.", PSPGHAN_URL),
    ("PhilHealth", "Philippine Health Insurance Corporation. Quality Policy on the Diagnosis and Management of Acute Infectious Gastroenteritis as Reference of the Corporation. PhilHealth Circular 2022-0026.", PHIC_URL),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Oral rehydration salts (ORS). MSF Medical Guidelines.", MSF_ORS_URL),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Zinc sulfate oral. MSF Medical Guidelines.", MSF_ZN_URL),
    ("World Health Organization", "WHO. Diarrhoeal disease. Fact sheet, 7 March 2024.", WHO_FS_URL),
  ],
  "links": [],
  "sources": [
    ("MSF", "MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Oral rehydration salts (ORS).", MSF_ORS_URL),
    ("MSF zinc", "MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Zinc sulfate oral.", MSF_ZN_URL),
    ("PSPGHAN 2026", "PSPGHAN (Philippine Pediatric Society)", "PSPGHAN. Treatment of Acute Gastroenteritis with No Signs of Dehydration. April 2026.", PSPGHAN_URL),
    ("PhilHealth", "PhilHealth", "PhilHealth Circular 2022-0026. Quality Policy on Acute Infectious Gastroenteritis.", PHIC_URL),
  ],
  "doses": [
    ("adult", "No dehydration (Plan A), >10 y and adults", "PO", "200–400 mL after each loose stool", "After each stool", "While diarrhoea lasts", "About 2000 mL/day", "MSF", ""),
    ("adult", "Moderate dehydration (Plan B), ≥15 y / ≥30 kg", "PO", "2200–4000 mL", "Over 4 h", "4 h, then reassess", "—", "MSF", "Then Plan A, repeat Plan B, or start IV (Plan C)"),
    ("adult", "Severe dehydration (Plan C), with IV fluids", "PO", "5 mL/kg/h", "Continuous", "Reassess after 3 h", "—", "MSF", "Only if conscious"),
    ("child", "No dehydration (Plan A), <2 y", "PO", "50–100 mL after each loose stool", "After each stool", "While diarrhoea lasts", "About 500 mL/day", "MSF", "PSPGHAN: 50–100 mL (¼–½ cup)"),
    ("child", "No dehydration (Plan A), 2–10 y", "PO", "100–200 mL after each loose stool", "After each stool", "While diarrhoea lasts", "About 1000 mL/day", "MSF", "PSPGHAN: 100 mL (½ cup)"),
    ("child", "No dehydration, >10 y (PH)", "PO", "As much as tolerated", "After each stool", "While diarrhoea lasts", "—", "PSPGHAN 2026", ""),
    ("child", "Moderate dehydration (Plan B), <4 mo / <5 kg", "PO", "200–400 mL", "Over 4 h", "4 h, then reassess", "—", "MSF", ""),
    ("child", "Moderate dehydration (Plan B), 4–11 mo / 5–7.9 kg", "PO", "400–600 mL", "Over 4 h", "4 h, then reassess", "—", "MSF", ""),
    ("child", "Moderate dehydration (Plan B), 12–23 mo / 8–10.9 kg", "PO", "600–800 mL", "Over 4 h", "4 h, then reassess", "—", "MSF", ""),
    ("child", "Moderate dehydration (Plan B), 2–4 y / 11–15.9 kg", "PO", "800–1200 mL", "Over 4 h", "4 h, then reassess", "—", "MSF", ""),
    ("child", "Moderate dehydration (Plan B), 5–14 y / 16–29.9 kg", "PO", "1200–2200 mL", "Over 4 h", "4 h, then reassess", "—", "MSF", ""),
    ("child", "Severe dehydration (Plan C), with IV fluids", "PO", "5 mL/kg/h", "Continuous", "Reassess after 3 h (6 h in infants)", "—", "MSF", "Only if conscious"),
    ("child", "Adjunct zinc with ORS, <6 mo", "PO", "10 mg zinc", "Once a day", "10 days", "—", "MSF zinc", "Half a 20 mg dispersible tablet"),
    ("child", "Adjunct zinc with ORS, 6 mo–5 y", "PO", "20 mg zinc", "Once a day", "10–14 days", "—", "MSF zinc", "PSPGHAN/PhilHealth: 20 mg/day; PSPGHAN gives 14 days"),
  ],
  "notes": [
    ("forms_ph", "PSPGHAN describes WHO low-osmolarity ORS in the Philippines as flavoured sachets made up with 100 mL, unflavoured or flavoured sachets made up with 200 mL of cool boiled water, and a flavoured ready-to-drink solution. Zinc for diarrhoea: drops 10 mg/mL (2 mL daily) or syrup 20 mg/5 mL (5 mL daily), as a single preparation, not a multivitamin.", "", "PSPGHAN 2026"),
    ("pregnancy", "No contraindication in pregnancy or breastfeeding.", "", "MSF"),
    ("administration", "Make up only with the volume of cool boiled water stated for that sachet size (100 mL or 200 mL sachets in PH).", "", "PSPGHAN 2026"),
    ("administration", "If the child vomits, stop for 10 minutes, then restart with very small, frequent amounts; do not stop rehydration.", "", "MSF"),
    ("administration", "Continue diet for age and breastfeeding during the episode.", "", "PSPGHAN 2026"),
    ("administration", "Zinc dispersible tablet: dissolve in a teaspoon of water; repeat the dose if vomited within 30 minutes. Zinc never replaces ORS.", "", "MSF zinc"),
    ("monitor", "Reassess hydration after 4 hours of Plan B (3 h on Plan C, 6 h in infants) and choose Plan A, B or C again.", "", "MSF"),
    ("monitor", "Puffy eyelids: stop ORS, give plain water, and resume Plan A once the puffiness settles.", "", "MSF"),
    ("monitor", "Children with no dehydration: see the doctor again if symptoms persist or do not improve within 3 days.", "", "PSPGHAN 2026"),
  ],
  "checked": [
    (MSF_ORS_URL, "MSF ORS: sachet for 1 L; Plan A per stool <24 mo 50–100 mL (~500 mL/day), 2–10 y 100–200 mL (~1000 mL/day), >10 y and adult 200–400 mL (~2000 mL/day); Plan B 4-h volumes by age/weight (<4 mo 200–400 ... ≥15 y 2200–4000 mL); Plan C ORS 5 mL/kg/h with IV if conscious, reassess 3 h (6 h infants); puffy eyelids and vomiting management; ReSoMal for severe malnutrition except cholera (standard ORS); no contraindication in pregnancy/breastfeeding; use solution within 24 h."),
    (MSF_ZN_URL, "MSF zinc sulfate: 20 mg dispersible tablet; <6 mo 10 mg, 6 mo–5 y 20 mg once daily for 10 days; dissolve in teaspoon of water; repeat if vomited within 30 min; separate from ferrous salts by 2 h; never replaces ORS."),
    (PSPGHAN_URL, "PSPGHAN (Philippine Pediatric Society component) April 2026, AGE with no signs of dehydration: WHO low-osmolarity ORS; flavoured sachet in 100 mL, unflavoured/flavoured sachet in 200 mL cool boiled water, flavoured ready-to-drink; per stool <2 y 50–100 mL, >2 y 100 mL, >10 y ad libitum; zinc ≥6 mo drops 10 mg/mL 2 mL daily x14 days or syrup 20 mg/5 mL 5 mL daily x14 days, single preparation; avoid carbonated/sports/non-WHO electrolyte drinks; follow up if not improved in 3 days; references 2019 PH CPG on acute infectious diarrhea (with DOH)."),
    (PHIC_URL, "PhilHealth quality policy on acute infectious gastroenteritis (updates Circular 2016-0001, based on DOH/IDSA): ORS and IV fluids are the standard of treatment for dehydration; IV preferred for severe dehydration in children; zinc 20 mg/day for 10–14 days routinely as adjunct in children (age range garbled in text). Circular number taken from the URL/search title; the number in the PDF text itself was garbled."),
    (WHO_FS_URL, "WHO diarrhoeal disease fact sheet (7 March 2024): ORS; 10–14 day zinc course reduces episode duration by 25% and stool volume by 30%; IV for severe dehydration/shock; continue feeding and breastfeeding."),
    ("https://www.who.int/publications/i/item/9241594217", "WHO 2006 'Implementing the new recommendations on the clinical management of diarrhoea': new low-osmolarity ORS and zinc for 10–14 days; page does not give zinc mg doses (not used as a ref)."),
    ("https://actamedicaphilippina.upm.edu.ph/index.php/acta/article/view/7513", "Acta Med Philipp 2024 adherence study: 2019 PH CPG strongly recommends low-osmolarity ORS and zinc; only 52% got ORS (not used as a ref)."),
    ("https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf", "Read with offset 64000: text covers Midazolam to Moxifloxacin only; ORS entry not readable, so the forms_ph note uses PSPGHAN instead of the PNF."),
  ],
}
