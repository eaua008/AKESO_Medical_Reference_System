PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
NTP_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf"
MSF_Z = "https://medicalguidelines.msf.org/en/viewport/TUB/english/pyrazinamide-z-20323874.html"
MSF_FDC = "https://medicalguidelines.msf.org/en/node/1205"
SMPC = "https://products.mhra.gov.uk/search/?search=pyrazinamide#emc-101051"

MED = {
  "id": "med_pyrazinamide",
  "desc_add": "In the Philippine NTP it is given as part of the HRZE fixed-dose combination tablet in the intensive phase of Category I (2HRZE/4HR) and in the first 3 months of Category II retreatment (2HRZES/1HRZE/5HRE), with the number of tablets set by body-weight band. Single-drug pyrazinamide (including a 250 mg/5 mL suspension) is used for weight-based dosing in children who cannot take tablets.",
  "facts": {
    "indication": [
      "Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)",
      "Drug-susceptible TB meningitis, intensive 6-month regimen (6HRZEto) at a higher dose (MSF)",
    ],
    "adverse": [
      "Headache, dizziness, irritability, insomnia (rare)",
      "Sideroblastic anaemia, angioedema, hypertension and pellagra (very rare)",
      "Erythema multiforme (very rare)",
      "Fever, malaise and urticaria",
    ],
    "contraindication": [
      "Acute liver disease (e.g., hepatitis) and up to 6 months after hepatitis (UK SmPC)",
      "Acute porphyria",
      "Hyperuricaemia",
      "Breast-feeding (UK SmPC; MSF lists no contraindication)",
    ],
    "interaction": [
      "Blood glucose-lowering drugs: pyrazinamide may affect glucose control; monitor glucose more closely in diabetes.",
      "Rifampicin: pyrazinamide may lower rifampicin levels (UK SmPC).",
      "Oestrogen-containing contraceptives: effect may be reduced.",
      "Oral typhoid vaccine: avoid pyrazinamide for 3 days before and after vaccination.",
      "Alcohol: avoid; heavy drinking raises the risk of liver damage.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("Philippine NTP Manual of Procedures", "Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.", NTP_URL),
    ("Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.", PNF_URL),
    ("MSF Tuberculosis guideline", "Médecins Sans Frontières. Tuberculosis - Appendix 10, TB drug information sheets: Pyrazinamide (Z). Updated January 2022.", MSF_Z),
    ("MSF Tuberculosis guideline", "Médecins Sans Frontières. Tuberculosis - Appendix 13. Daily dose of TB drugs using fixed-dose combinations. Updated October 2022.", MSF_FDC),
    ("UK SmPC (emc)", "Pyrazinamide 500 mg Tablets - Summary of Product Characteristics. Morningside Healthcare Ltd. Electronic medicines compendium (emc), updated June 2025.", SMPC),
  ],
  "links": [
    ("gout", "avoid", "Contraindicated in hyperuricaemia and acute gouty arthritis; give only if treatment is urgent, monitor uric acid and stop if acute gout develops (UK SmPC)."),
    ("type2_diabetes", "caution", "High doses may affect glucose control; monitor diabetic patients more closely (UK SmPC)."),
    ("chronic_kidney_disease", "caution", "Give 25 mg/kg three times a week in renal insufficiency (MSF); UK SmPC advises reduced dose and frequency."),
    ("hepatitis_b", "caution", "Contraindicated in acute hepatitis and for 6 months after (UK SmPC); applying this to hepatitis B is an inference, not stated for HBV specifically."),
  ],
  "sources": [
    ("NTP MOP 2014", "Philippine NTP Manual of Procedures", "DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 11–15).", NTP_URL),
    ("PNF", "Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.", PNF_URL),
    ("MSF TB", "MSF Tuberculosis guideline", "MSF Tuberculosis, Appendix 10: Pyrazinamide (Z), 2022.", MSF_Z),
    ("MSF FDC", "MSF Tuberculosis guideline", "MSF Tuberculosis, Appendix 13: daily dose of TB drugs using FDCs, 2022.", MSF_FDC),
    ("Label · UK SmPC", "UK SmPC (emc)", "Pyrazinamide 500 mg Tablets - SmPC. Morningside Healthcare Ltd, 2025.", SMPC),
  ],
  "doses": [
    ("adult", "TB Cat I intensive (2HRZE), 30–37 kg", "PO", "2 tablets HRZE FDC", "Once a day", "2 months", "—", "NTP MOP 2014", "HRZE = H75/R150/Z400/E275 mg"),
    ("adult", "TB Cat I intensive (2HRZE), 38–54 kg", "PO", "3 tablets HRZE FDC", "Once a day", "2 months", "—", "NTP MOP 2014", ""),
    ("adult", "TB Cat I intensive (2HRZE), 55–70 kg", "PO", "4 tablets HRZE FDC", "Once a day", "2 months", "—", "NTP MOP 2014", ""),
    ("adult", "TB Cat I intensive (2HRZE), >70 kg", "PO", "5 tablets HRZE FDC", "Once a day", "2 months", "—", "NTP MOP 2014", "Cat II: HRZE months 1–3, same tablet numbers"),
    ("adult", "TB, single-drug formulation", "PO", "25 mg/kg (range 20–30)", "Once a day", "Intensive phase", "2 g/day", "NTP MOP 2014", ""),
    ("adult", "TB, standard regimen", "PO", "1.5 g (<50 kg); 2 g (≥50 kg)", "Once a day", "2 months", "2 g/day", "Label · UK SmPC", ""),
    ("adult", "TB, intermittent supervised regimen", "PO", "2 g (<50 kg); 2.5 g (≥50 kg)", "3× a week", "2 months", "—", "Label · UK SmPC", "Only if daily dosing is not feasible"),
    ("adult", "TB meningitis (6HRZEto)", "PO", "40 mg/kg", "Once a day", "6 months", "2 g/day", "MSF TB", ""),
    ("child", "TB, single-drug formulation", "PO", "30 mg/kg (range 20–40)", "Once a day", "Intensive phase", "2 g/day", "NTP MOP 2014", "Suspension 250 mg/5 mL dosed by weight (Table 14); newborn <4 weeks: refer"),
    ("child", "TB, child <30 kg", "PO", "35 mg/kg (range 30–40)", "Once a day", "Intensive phase", "2 g/day", "MSF TB", "150 mg dispersible tablet in 10 mL water"),
    ("child", "TB intensive phase, HRZ 50/75/150 FDC", "PO", "4–7 kg: 1; 8–11 kg: 2; 12–15 kg: 3; 16–22 kg: 4 tablets", "Once a day", "2 months", "—", "MSF FDC", "Plus ethambutol where indicated"),
  ],
  "notes": [
    ("renal", "25 mg/kg three times a week.", "Renal insufficiency", "MSF TB"),
    ("renal", "UK label: reduce dose and frequency; use only in emergencies, given intermittently.", "", "Label · UK SmPC"),
    ("hepatic", "Contraindicated in severe hepatic impairment, acute liver disease and for 6 months after hepatitis. If hepatocellular damage occurs, stop and do not restart. Heavy drinkers and patients on other hepatotoxic drugs are at higher risk.", "", "Label · UK SmPC"),
    ("pregnancy", "MSF: no contraindication in pregnancy or breastfeeding. The UK SmPC states clinical data in pregnancy are insufficient (use only if benefit clearly outweighs risk) and contraindicates breastfeeding because it passes into milk.", "", "MSF TB"),
    ("administration", "Take with or without food. For GI upset, give at bedtime or with small meals. Advise sun protection (photosensitivity).", "", "NTP MOP 2014"),
    ("forms_ph", "Only in fixed-dose combinations (List B): isoniazid + rifampicin + pyrazinamide + ethambutol 75/150/400/275 mg tablet; isoniazid + rifampicin + pyrazinamide 50/75/150 mg dispersible tablet (pediatric). A single-ingredient pyrazinamide entry could not be read in the PNF text (it stops at 'M').", "", "PNF"),
    ("monitor", "LFTs (AST, ALT) before starting and every 2–4 weeks; kidney function every 3–4 weeks.", "", "Label · UK SmPC"),
    ("monitor", "Arthralgia: give aspirin or an NSAID; if it persists, check serum uric acid and consider gout.", "", "NTP MOP 2014"),
    ("monitor", "Blood glucose in diabetes; uric acid in patients with gout history.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (PNF_URL, "Isoniazid + Rifampicin + Pyrazinamide (B) 50 mg + 75 mg + 150 mg dispersible FDC tablet; Isoniazid + Rifampicin + Pyrazinamide + Ethambutol (B) 75 + 150 + 400 + 275 mg tablet. PDF text (65,922 chars) ends at 'Multivitamins', so no standalone pyrazinamide entry could be checked."),
    (NTP_URL, "Table 10: Cat I 2HRZE/4HR, Ia 2HRZE/10HR, II 2HRZES/1HRZE/5HRE, IIa; Table 11 HRZE tablets 30–37 kg 2, 38–54 kg 3, 55–70 kg 4, >70 kg 5; Table 13 pyrazinamide adults 25 (20–30) mg/kg, children 30 (20–40) mg/kg, max 2 g daily; Table 14 pyrazinamide 250 mg/5 ml by weight 2.1–30 kg, newborn <4 weeks refer; Table 15 GI intolerance (R/H/Z): bedtime or small meals; arthralgia due to hyperuricemia (Z): aspirin/NSAID, uric acid. (Text read via offsets 95000/100000; PDF text ends ~110951.)"),
    (MSF_Z, "MSF TB Pyrazinamide (Jan 2022): 400 mg tab, 150 mg dispersible; <30 kg 35 (30–40) mg/kg, ≥30 kg and adults 25 (20–30) mg/kg, max 2000 mg; renal insufficiency 25 mg/kg three times a week; TB meningitis 6HRZEto 40 mg/kg max 2000 mg; not in severe hepatic impairment or severe gout; no contraindication in pregnancy/breastfeeding; with or without food; protect skin from sun."),
    (MSF_FDC, "Appendix 13 (Oct 2022): child intensive HZR 50/150/75: 4–7 kg 1, 8–11 kg 2, 12–13 kg 3, 14–15 kg 3, 16–17 kg 4, 18–22 kg 4."),
    (SMPC, "Pyrazinamide 500 mg (Morningside, June 2025): adults <50 kg up to 1.5 g, >50 kg up to 2 g daily; intermittent 3×/week 2 g / 2.5 g; children 35 mg/kg/day max 1.5 g; contraindications incl. acute liver disease/hepatitis and up to 6 months after, acute porphyria, hyperuricaemia/gout, breast-feeding; LFTs every 2–4 weeks, liver/kidney every 3–4 weeks; diabetes monitoring; renal: emergencies, intermittent; interactions: glucose-lowering drugs, may reduce rifampicin, oestrogen contraceptives, oral typhoid vaccine 3 days, alcohol; ADRs rare headache/dizziness/irritability/insomnia; very rare erythema multiforme, tubulo-interstitial nephritis, sideroblastic anaemia, angioedema, hypertension, pellagra; not known fever, malaise, urticaria."),
  ],
}
