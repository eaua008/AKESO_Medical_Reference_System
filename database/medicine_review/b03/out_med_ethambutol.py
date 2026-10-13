PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
NTP_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf"
MSF_URL = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/ethambutol-e-oral-16683637.html"
MSF_FDC = "https://medicalguidelines.msf.org/en/node/1205"
SMPC = "https://products.mhra.gov.uk/search/?search=ethambutol#emc-9346"

MED = {
  "id": "med_ethambutol",
  "desc_add": "In the Philippine NTP it is given in the HRZE fixed-dose combination for the 2-month intensive phase of Category I (2HRZE/4HR) and through all 8 months of Category II retreatment (2HRZES/1HRZE/5HRE), with the number of tablets set by body-weight band. MSF notes that ethambutol is not routinely given to all children, and that young children (under 5) need particular care because visual changes are hard to detect at that age.",
  "facts": {
    "indication": [
      "Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)",
      "Extrapulmonary TB of the CNS, bones or joints (PH NTP Category Ia: 2HRZE/10HR)",
    ],
    "adverse": [
      "Very rare skin reactions: photosensitive lichenoid eruptions, bullous dermatitis, Stevens-Johnson syndrome",
      "Numbness and paraesthesia of the extremities (rare)",
    ],
    "contraindication": [
      "Pre-existing eye disease such as diabetic retinopathy (MSF)",
      "Severe renal impairment (MSF)",
      "Retrobulbar neuritis (UK SmPC)",
    ],
    "interaction": [],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("Philippine NTP Manual of Procedures", "Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.", NTP_URL),
    ("Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.", PNF_URL),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs - practical guidelines: Ethambutol (E) oral. Updated August 2022.", MSF_URL),
    ("MSF Tuberculosis guideline", "Médecins Sans Frontières. Tuberculosis - Appendix 13. Daily dose of TB drugs using fixed-dose combinations. Updated October 2022.", MSF_FDC),
    ("UK SmPC (emc)", "Ethambutol 400 mg Tablets - Summary of Product Characteristics. Esteve Pharmaceuticals Ltd. Electronic medicines compendium (emc), updated July 2024.", SMPC),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "Dose given three times a week in renal impairment; optic toxicity is more common when renal function is reduced; MSF advises against use in severe renal impairment."),
    ("type2_diabetes", "caution", "MSF lists pre-existing eye disease such as diabetic retinopathy as a contraindication; check eyes before treatment in diabetics (applies only with retinopathy)."),
  ],
  "sources": [
    ("NTP MOP 2014", "Philippine NTP Manual of Procedures", "DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 11–14).", NTP_URL),
    ("PNF", "Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.", PNF_URL),
    ("MSF", "MSF Essential Drugs", "MSF Essential drugs: Ethambutol (E) oral, 2022.", MSF_URL),
    ("MSF TB", "MSF Tuberculosis guideline", "MSF Tuberculosis, Appendix 13: daily dose of TB drugs using FDCs, 2022.", MSF_FDC),
    ("Label · UK SmPC", "UK SmPC (emc)", "Ethambutol 400 mg Tablets - SmPC. Esteve Pharmaceuticals Ltd, 2024.", SMPC),
  ],
  "doses": [
    ("adult", "TB Cat I intensive (2HRZE), 30–37 kg", "PO", "2 tablets HRZE FDC", "Once a day", "2 months", "—", "NTP MOP 2014", "Then HR 2 tablets for 4 months (10 months for Cat Ia)"),
    ("adult", "TB Cat I intensive (2HRZE), 38–54 kg", "PO", "3 tablets HRZE FDC", "Once a day", "2 months", "—", "NTP MOP 2014", "Then HR 3 tablets"),
    ("adult", "TB Cat I intensive (2HRZE), 55–70 kg", "PO", "4 tablets HRZE FDC", "Once a day", "2 months", "—", "NTP MOP 2014", "Then HR 4 tablets"),
    ("adult", "TB Cat I intensive (2HRZE), >70 kg", "PO", "5 tablets HRZE FDC", "Once a day", "2 months", "—", "NTP MOP 2014", "Then HR 5 tablets"),
    ("adult", "TB Cat II retreatment (2HRZES/1HRZE/5HRE)", "PO", "Same tablet number per weight band (2/3/4/5)", "Once a day", "8 months", "—", "NTP MOP 2014", "HRZE months 1–3 (+ streptomycin months 1–2), then HRE months 4–8"),
    ("adult", "TB, single-drug formulation", "PO", "15 mg/kg (range 15–20)", "Once a day", "Per regimen", "1.2 g/day", "NTP MOP 2014", ""),
    ("child", "TB, single-drug formulation", "PO", "20 mg/kg (range 15–25)", "Once a day", "Per regimen", "1.2 g/day", "NTP MOP 2014", "Newborn <4 weeks: refer to pediatrician (streptomycin instead of ethambutol)"),
    ("child", "TB intensive phase, 4–7 kg / 8–11 kg (with HRZ 50/75/150)", "PO", "1 / 2 tablets E 100 mg", "Once a day", "2 months", "—", "MSF TB", "Not routinely given to all children"),
  ],
  "notes": [
    ("renal", "15–25 mg/kg three times a week in renal impairment; MSF advises not to give in severe renal impairment. Toxic effects are more common when renal function is impaired.", "", "MSF"),
    ("pregnancy", "MSF: no contraindication in pregnancy or breastfeeding. The UK SmPC states it is not recommended in pregnancy or breastfeeding.", "", "MSF"),
    ("monitor", "Full eye examination before starting (UK SmPC). Teach patients to stop the drug and seek care at once for blurred vision, reduced acuity or difficulty telling red from green (MSF; usually reverses within weeks).", "", "MSF"),
    ("administration", "Dose carefully by body weight. HRZE FDC tablet = isoniazid 75 mg + rifampicin 150 mg + pyrazinamide 400 mg + ethambutol 275 mg.", "", "PNF"),
    ("forms_ph", "100 mg tablet (pediatric); 200 mg and 400 mg tablet. FDCs: isoniazid + rifampicin + ethambutol 75/150/275 mg tablet; isoniazid + rifampicin + pyrazinamide + ethambutol 75/150/400/275 mg tablet.", "", "PNF"),
  ],
  "checked": [
    (PNF_URL, "Ethambutol oral 100 mg tablet (pediatric), 200 mg and 400 mg tablet; isoniazid+rifampicin+ethambutol 75+150+275 mg; isoniazid+rifampicin+pyrazinamide+ethambutol 75+150+400+275 mg (List B)."),
    (NTP_URL, "NTCP MOP 5th ed 2014: Cat I 2HRZE/4HR (Cat Ia 2HRZE/10HR for CNS/bones/joints); Cat II 2HRZES/1HRZE/5HRE; Table 11/12 tablets per day 30–37 kg 2, 38–54 kg 3, 55–70 kg 4, >70 kg 5; Table 13 E adults 15 (15–20) mg/kg, children 20 (15–25) mg/kg, max 1.2 g daily; Table 14 newborn <4 weeks refer, streptomycin instead of ethambutol."),
    (MSF_URL, "15–25 mg/kg once daily, max 1200 mg; renal impairment 15–25 mg/kg three times weekly; do not give in severe renal impairment or pre-existing optic neuritis incl. diabetic retinopathy; children <5 particular care; no contraindication in pregnancy/breastfeeding; stop for visual symptoms, usually reversible."),
    (MSF_FDC, "Children intensive phase HZR 50/150/75 + E 100 mg: 4–7 kg 1 tablet E, 8–11 kg 2 tablets E; ethambutol not routinely given to all children."),
    (SMPC, "Contraindicated in optic or retrobulbar neuritis; full ophthalmic exam before starting; toxic effects more common in renal impairment; not recommended in pregnancy/breastfeeding; very rare photosensitive lichenoid eruptions, bullous dermatitis, SJS; rare peripheral neuropathy, numbness, paraesthesia."),
  ],
}
