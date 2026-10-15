PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
NTP_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf"
WHO_TPT = "https://tbksp.who.int/en/node/43"
WHO_TPT_HB = "https://tbksp.who.int/en/node/1271"
MSF_URL = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/isoniazid-h-oral-16683911.html"
MSF_FDC = "https://medicalguidelines.msf.org/en/node/1205"
SMPC = "https://products.mhra.gov.uk/search/?search=isoniazid#emc-9139"

MED = {
  "id": "med_isoniazid",
  "desc_add": "In the Philippine NTP it is part of every first-line regimen, given as HRZE then HR fixed-dose combination tablets dosed by body-weight band (Category I 2HRZE/4HR; Category II 2HRZES/1HRZE/5HRE), and isoniazid preventive therapy (IPT) is given to household contacts under 5 years and to people living with HIV without active TB. WHO's 2024 TB preventive treatment guideline recommends 6 or 9 months of daily isoniazid, weekly isoniazid plus rifapentine for 3 months (3HP), or daily isoniazid plus rifampicin for 3 months (3HR), with 1 month of daily isoniazid plus rifapentine (1HP) as an alternative.",
  "facts": {
    "indication": [
      "Isoniazid preventive therapy for household contacts under 5 years of a TB case, after active TB is ruled out (PH NTP)",
      "Isoniazid preventive therapy for 6 months in people living with HIV without active TB (PH NTP)",
      "Short-course TB preventive treatment combined with rifapentine (3HP, 1HP) or rifampicin (3HR) (WHO)",
    ],
    "adverse": [
      "Severe skin reactions (SJS, TEN, DRESS, AGEP): never restart isoniazid",
      "Blood disorders: agranulocytosis, aplastic and haemolytic anaemia (frequency unknown)",
      "Psychotic reactions, mood changes and depression",
      "Deafness, tinnitus and vertigo",
      "Gynaecomastia, pancreatitis, hypoglycaemia; nicotinic acid deficiency secondary to pyridoxine deficiency",
      "Minor GI upset (manage by giving at bedtime or with small meals, PH NTP)",
    ],
    "contraindication": [
      "Drug-induced liver disease (UK SmPC)",
      "Severe hepatic impairment (MSF)",
    ],
    "interaction": [
      "Benzodiazepines (diazepam, triazolam): increased toxicity; diazepam may cause sedation and respiratory depression.",
      "Warfarin: increased bleeding risk; monitor closely.",
      "Itraconazole (co-administration not recommended) and ketoconazole: reduced azole levels.",
      "Primidone, disulfiram and chlorzoxazone: reduced hepatic metabolism, possible toxicity.",
      "Levodopa: effect may be reduced.",
      "Stavudine: increased risk of peripheral neuropathy.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("Philippine NTP Manual of Procedures", "Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.", NTP_URL),
    ("WHO TB guidelines - TB preventive treatment", "World Health Organization. WHO consolidated guidelines on tuberculosis. Module 1: prevention - tuberculosis preventive treatment, 2nd ed. Geneva: WHO; 2024. Section 1.4, TB preventive treatment options (WHO TB Knowledge Sharing Platform).", WHO_TPT),
    ("WHO operational handbook - TPT regimens", "World Health Organization. WHO operational handbook on tuberculosis. Module 1: prevention - TB preventive treatment. Section 5.1, Recommended TPT regimens (WHO TB Knowledge Sharing Platform).", WHO_TPT_HB),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs - practical guidelines: Isoniazid (H) oral. Updated June 2021.", MSF_URL),
    ("UK SmPC (emc)", "Isoniazid Tablets BP 100 mg - Summary of Product Characteristics. RPH Pharmaceuticals AB. Electronic medicines compendium (emc), revised August 2025.", SMPC),
  ],
  "links": [
    ("hiv_infection", "safe", "PH NTP: people living with HIV without active TB are given 6 months of IPT; give pyridoxine (HIV raises neuropathy and hepatotoxicity risk)."),
    ("hepatitis_b", "caution", "Chronic liver disease raises hepatotoxicity risk (MSF); monitor liver function and stop if jaundice develops. Contraindicated if hepatic impairment is severe."),
    ("chronic_kidney_disease", "caution", "UK SmPC advises care in renal impairment (ototoxicity reported in end-stage disease); uraemia raises neuropathy risk, so give pyridoxine. No dose change stated."),
    ("type2_diabetes", "caution", "UK SmPC: use with care in diabetes; diabetics are at higher risk of peripheral neuropathy and should get pyridoxine."),
  ],
  "sources": [
    ("NTP MOP 2014", "Philippine NTP Manual of Procedures", "DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 10–15).", NTP_URL),
    ("WHO 2024", "WHO TB guidelines - TB preventive treatment", "WHO consolidated guidelines on tuberculosis, Module 1: TB preventive treatment, 2nd ed., 2024.", WHO_TPT),
    ("MSF", "MSF Essential Drugs", "MSF Essential drugs: Isoniazid (H) oral, 2021.", MSF_URL),
    ("MSF TB", "MSF Tuberculosis guideline", "MSF Tuberculosis, Appendix 13: daily dose of TB drugs using fixed-dose combinations, 2022.", MSF_FDC),
    ("Label · UK SmPC", "UK SmPC (emc)", "Isoniazid Tablets BP 100 mg - SmPC. RPH Pharmaceuticals AB, 2025.", SMPC),
    ("PNF", "Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.", PNF_URL),
  ],
  "doses": [
    ("adult", "TB Cat I (2HRZE/4HR), 30–37 kg", "PO", "2 tablets FDC", "Once a day", "6 months", "—", "NTP MOP 2014", "HRZE 2 months then HR 4 months (HR 10 months for Cat Ia)"),
    ("adult", "TB Cat I (2HRZE/4HR), 38–54 kg", "PO", "3 tablets FDC", "Once a day", "6 months", "—", "NTP MOP 2014", ""),
    ("adult", "TB Cat I (2HRZE/4HR), 55–70 kg", "PO", "4 tablets FDC", "Once a day", "6 months", "—", "NTP MOP 2014", ""),
    ("adult", "TB Cat I (2HRZE/4HR), >70 kg", "PO", "5 tablets FDC", "Once a day", "6 months", "—", "NTP MOP 2014", ""),
    ("adult", "TB, single-drug formulation", "PO", "5 mg/kg (range 4–6)", "Once a day", "Per regimen", "400 mg/day", "NTP MOP 2014", "UK SmPC and MSF give max 300 mg/day"),
    ("adult", "TB meningitis (early phase)", "PO", "Up to 10 mg/kg", "Once a day", "Early treatment", "—", "Label · UK SmPC", ""),
    ("adult", "TB preventive treatment (6H / 9H)", "PO", "5 mg/kg (range 4–6)", "Once a day", "6 or 9 months", "300 mg/day", "MSF", "PH NTP: 6 months for PLHIV; WHO 2024 regimen"),
    ("adult", "TB preventive treatment (3HR, with rifampicin)", "PO", "5 mg/kg (range 4–6)", "Once a day", "3 months", "300 mg/day", "MSF", "WHO 2024 regimen"),
    ("adult", "TB preventive treatment (3HP, with rifapentine)", "PO", "900 mg", "Once a week", "3 months", "900 mg/week", "MSF", "Adults and children ≥30 kg"),
    ("adult", "TB preventive treatment (1HP, with rifapentine)", "PO", "300 mg", "Once a day", "1 month", "300 mg/day", "MSF", "Age 13 y and over; WHO alternative option"),
    ("child", "TB, single-drug formulation", "PO", "10 mg/kg (range 10–15)", "Once a day", "Per regimen", "300 mg/day", "NTP MOP 2014", "Newborn <4 weeks: refer to pediatrician"),
    ("child", "TB intensive phase, HZR 50/150/75 dispersible", "PO", "4–7 kg: 1 tab; 8–11 kg: 2; 12–15 kg: 3; 16–22 kg: 4", "Once a day", "2 months", "—", "MSF TB", "Then HR 50/75: 4–7 kg 1, 8–11 kg 2, 12–14 kg 3 tablets"),
    ("child", "TB preventive treatment (6H / 3HR), <30 kg", "PO", "10 mg/kg (range 7–15)", "Once a day", "6 months (6H) or 3 months (3HR)", "300 mg/day", "MSF", "PH NTP: contacts <5 y after TB ruled out"),
    ("child", "TB preventive treatment (3HP), >2 y and <30 kg", "PO", "20–30 mg/kg", "Once a week", "3 months", "—", "MSF", "With weekly rifapentine"),
  ],
  "notes": [
    ("renal", "No dose adjustment stated; use with care in renal impairment (deafness/tinnitus reported in end-stage renal disease). Renal impairment and uraemia raise neuropathy risk: give pyridoxine.", "", "Label · UK SmPC"),
    ("hepatic", "Contraindicated in drug-induced liver disease (SmPC) and severe hepatic impairment (MSF). In known liver disease monitor liver function; any deterioration is a reason to stop. Stop if jaundice appears.", "", "MSF"),
    ("elderly", "No dose reduction needed, but use caution as renal and hepatic function may be reduced; age over 35 raises hepatotoxicity risk (MSF).", "", "Label · UK SmPC"),
    ("pregnancy", "Not contraindicated in pregnancy or breastfeeding; give the mother pyridoxine 10 mg daily and the breastfed infant 5 mg daily. WHO: pregnancy alone should not exclude TB preventive treatment, but use of 1HP and 3HP in pregnancy is cautioned until more data are available.", "", "MSF"),
    ("administration", "Take once daily on an empty stomach. If GI upset occurs, PH NTP advises giving drugs at bedtime or with small meals. Avoid tyramine/histamine-rich foods (cured meats, matured cheese, tuna, mackerel).", "", "MSF"),
    ("monitor", "Pyridoxine (vitamin B6) 10 mg daily for prevention and 50–100 mg daily for treatment of peripheral neuropathy (burning feet). Baseline and regular liver tests; stop if AST rises above 3× normal or bilirubin increases (UK SmPC). Ask monthly about jaundice, nausea, numbness.", "", "NTP MOP 2014"),
    ("forms_ph", "300 mg and 400 mg tablet; 200 mg/5 mL syrup (120 mL). FDCs: isoniazid + rifampicin 50/75 mg dispersible (pediatric) and 75/150 mg tablet; + ethambutol 75/150/275 mg; isoniazid + rifampicin + pyrazinamide 50/75/150 mg dispersible (pediatric); HRZE 75/150/400/275 mg tablet.", "", "PNF"),
  ],
  "checked": [
    (PNF_URL, "Isoniazid oral 300 mg and 400 mg tablet, 200 mg/5 mL syrup 120 mL; isoniazid+rifampicin 50+75 mg dispersible (pediatric) and 75+150 mg tablet; +ethambutol 75+150+275 mg; isoniazid+rifampicin+pyrazinamide 50+75+150 mg dispersible (pediatric); HRZE 75+150+400+275 mg (List B)."),
    (NTP_URL, "NTCP MOP 5th ed 2014: Table 10 Cat I 2HRZE/4HR, Cat Ia 2HRZE/10HR, Cat II 2HRZES/1HRZE/5HRE, Cat IIa 2HRZES/1HRZE/9HRE; Table 11 FDC tablets 30–37 kg 2, 38–54 kg 3, 55–70 kg 4, >70 kg 5 (both phases); Table 13 H adults 5 (4–6) mg/kg not to exceed 400 mg daily, children 10 (10–15) mg/kg not to exceed 300 mg daily; Table 14 newborn <4 weeks refer; IPT for contacts <5 y (TST/CXR rules) and PLHIV without active TB for 6 months; Table 15 peripheral neuropathy -> pyridoxine 50–100 mg treatment, 10 mg prevention; minor GI intolerance -> give at bedtime or with small meals. (WebFetch text stopped before Chapter 4 IPT dosing and Table 18 renal.)"),
    (WHO_TPT, "WHO 2024 TPT 2nd ed Sec 1.4: Rec 19 6 or 9 months daily isoniazid, 3HP weekly, or 3HR daily, regardless of HIV status; Rec 20 alternatives 1HP or 4R."),
    (WHO_TPT_HB, "Operational handbook 5.1: regimen definitions 6H/9H/3HP/1HP/3HR/4R; pregnancy should not exclude TPT, caution with 1HP/3HP in pregnancy; pyridoxine routinely for pregnant/breastfeeding women and infants; protective pyridoxine 10–25 mg/day. (Dose table is an image; not read.)"),
    (MSF_URL, "MSF isoniazid (June 2021): TB/latent TB daily <30 kg 10 mg/kg (7–15), ≥30 kg and adults 5 mg/kg (4–6), max 300 mg; with weekly rifapentine >2 y <30 kg 20–30 mg/kg, ≥30 kg 900 mg weekly, 3 months; with daily rifapentine ≥13 y 300 mg, 1 month; with rifampicin 3 months; contraindicated severe hepatic impairment; hepatotoxicity risk (alcohol, chronic liver disease, rifampicin, >35 y); neuropathy risk factors; interactions phenytoin, carbamazepine, benzodiazepines, warfarin; pregnancy/breastfeeding not contraindicated, pyridoxine 10 mg mother, 5 mg infant; empty stomach."),
    (MSF_FDC, "Children intensive phase HZR 50/150/75: 4–7 kg 1, 8–11 kg 2, 12–13 and 14–15 kg 3, 16–17 and 18–22 kg 4 tablets; continuation HR 50/75: 4–7 kg 1, 8–11 kg 2, 12–14 kg 3."),
    (SMPC, "RPH Isoniazid 100 mg SmPC (rev 08/2025): adults 4–5 mg/kg up to 300 mg; up to 10 mg/kg early in TB meningitis; children 10–15 mg/kg from 3 months; contraindicated drug-induced liver disease; stop if AST >3× ULN or bilirubin rises; care in renal impairment, ototoxicity in ESRD; elderly no reduction; care in epilepsy, diabetes; severe skin reactions never restart; interactions diazepam/triazolam, itraconazole (not recommended), ketoconazole, primidone, chlorzoxazone, disulfiram, levodopa, stavudine; undesirable effects agranulocytosis, aplastic/haemolytic anaemia, psychotic disorder, deafness/tinnitus/vertigo, gynaecomastia, pancreatitis, hypoglycaemia, nicotinic acid deficiency."),
  ],
}
