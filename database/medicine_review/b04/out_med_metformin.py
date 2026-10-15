SMPC_IR = "https://products.mhra.gov.uk/search/?search=metformin#emc-15731"
SMPC_PR = "https://products.mhra.gov.uk/search/?search=metformin#emc-5263"
MSF = "https://medicalguidelines.msf.org/viewport/EssDr/english/metformin-oral-27983919.html"
PNF = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
WHOEML = "https://list.essentialmeds.org/medicines/191"

MED = {
  "id": "med_metformin",
  "desc_add": "In the Philippines it is listed in the PNF Essential Medicines List as 500 mg tablets/film-coated tablets and 850 mg tablets, and it has been on the WHO Model List of Essential Medicines since 1997. In the UKPDS, overweight patients started on metformin after diet failure had fewer diabetes-related complications, lower diabetes-related and all-cause mortality, and fewer myocardial infarctions than those on diet alone. It is not metabolised and is excreted unchanged in the urine (half-life about 6.5 h), so clearance falls in step with kidney function.",
  "facts": {
    "indication": [
      "Type 2 diabetes in combination with insulin (adults)",
    ],
    "adverse": [
      "Abnormal liver tests or hepatitis (very rare; resolves on stopping)",
      "Skin reactions: erythema, pruritus, urticaria (very rare)",
    ],
    "contraindication": [
      "Diabetic pre-coma",
      "Acute conditions that can affect kidney function: dehydration, severe infection, shock",
      "Conditions causing tissue hypoxia: decompensated heart failure, respiratory failure, recent myocardial infarction",
      "Hepatic insufficiency, acute alcohol intoxication, alcoholism",
      "Not recommended in mitochondrial disease (MELAS, MIDD)",
    ],
    "interaction": [
      "NSAIDs (incl. COX-2 inhibitors), ACE inhibitors, ARBs and diuretics (especially loop): may impair kidney function; monitor renal function.",
      "Glucocorticoids, sympathomimetics (e.g., salbutamol), hydrochlorothiazide, chlorpromazine: raise blood glucose; check glucose more often and adjust dose.",
      "Verapamil (OCT1 inhibitor) may reduce metformin efficacy; rifampicin (OCT1 inducer) may increase its absorption and effect.",
      "Trimethoprim, isavuconazole, crizotinib, olaparib: may raise metformin levels or alter its renal elimination.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Metformin 500 mg Tablets. Summary of Product Characteristics. Medley Pharma Ltd. electronic medicines compendium (emc); text revised 04/2025.", SMPC_IR),
    ("UK SmPC (emc)", "Metformin hydrochloride 500 mg prolonged release tablets. Summary of Product Characteristics. Genus Pharmaceuticals (STADA). emc; text revised 04/2025.", SMPC_PR),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Metformin oral. In: Essential Drugs – practical guidelines. MSF Medical Guidelines; updated 09/2023.", MSF),
    ("Philippine National Formulary (PhilHealth)", "Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.", PNF),
    ("WHO Model List of Essential Medicines", "World Health Organization. eEML – Electronic Essential Medicines List: Metformin (first added 1997, TRS 882).", WHOEML),
  ],
  "links": [
    ("heart_failure", "caution", "Can be used in stable chronic heart failure with regular monitoring of heart and kidney function; contraindicated in acute or unstable (decompensated) heart failure."),
    ("acute_coronary_syndrome", "avoid", "Recent myocardial infarction is a contraindication (tissue hypoxia raises lactic acidosis risk)."),
    ("acute_gastroenteritis", "caution", "Dehydration is a contraindication in the label; withholding metformin during gastroenteritis with significant dehydration is an inference from this, not a direct label statement."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Metformin 500 mg Tablets SmPC, Medley Pharma Ltd; text revised 04/2025.", SMPC_IR),
    ("Label · UK SmPC PR", "UK SmPC (emc)", "Metformin hydrochloride 500 mg prolonged release tablets SmPC, Genus Pharmaceuticals (STADA); text revised 04/2025.", SMPC_PR),
    ("MSF", "MSF Essential Drugs", "Médecins Sans Frontières. Metformin oral. Essential Drugs – practical guidelines; updated 09/2023.", MSF),
    ("PNF", "Philippine National Formulary (PhilHealth)", "PNF Essential Medicines List, 2022.", PNF),
  ],
  "doses": [
    ("adult", "Type 2 diabetes (IR tablet)", "PO", "500 mg or 850 mg", "2–3× a day", "Long-term", "3 g/day", "Label · UK SmPC", "With or after meals; adjust after 10–15 days by blood glucose"),
    ("adult", "Type 2 diabetes (IR tablet, MSF schedule)", "PO", "500 mg, then 500 mg 2× a day", "Once a day (week 1)", "Long-term", "2 g/day", "MSF", "Week 2: 500 mg 2× a day; then +500 mg/week as needed (1 g morning and evening max)"),
    ("adult", "Type 2 diabetes (prolonged-release)", "PO", "500 mg", "Once a day", "Long-term", "2000 mg/day", "Label · UK SmPC PR", "With evening meal; +500 mg every 10–15 days; if not controlled at 2000 mg once daily, try 1000 mg 2× a day"),
    ("child", "Type 2 diabetes, 10 years and older (IR tablet)", "PO", "500 mg or 850 mg", "Once a day", "Long-term", "2 g/day", "Label · UK SmPC", "Above starting dose give in 2–3 divided doses; PR tablets not for children"),
  ],
  "notes": [
    ("renal", "Max 3 g/day (IR) or 2000 mg/day (PR); consider dose reduction as function declines.", "GFR 60–89", "Label · UK SmPC"),
    ("renal", "Max 2 g/day; review lactic acidosis risk factors before starting; starting dose at most half the maximum.", "GFR 45–59", "Label · UK SmPC"),
    ("renal", "Max 1 g/day (MSF: max 1 g/day in moderate renal impairment).", "GFR 30–44", "Label · UK SmPC"),
    ("renal", "Contraindicated.", "GFR <30", "Label · UK SmPC"),
    ("hepatic", "Hepatic insufficiency is a contraindication; no separate hepatic dosing is given.", "", "Label · UK SmPC"),
    ("elderly", "Base the dose on kidney function; check GFR every 3–6 months.", "", "Label · UK SmPC"),
    ("pregnancy", "Crosses the placenta; data from more than 1,000 exposed pregnancies show no rise in malformations, so it may be considered as add-on or alternative to insulin (UK SmPC), although MSF names insulin the drug of choice in pregnancy. Breastfeeding: excreted in milk; UK SmPC advises against it because data are limited, while MSF lists no contraindication.", "", "Label · UK SmPC"),
    ("administration", "Take with or after meals and titrate slowly (dividing doses 2–3× a day reduces GI upset). Stop at the time of surgery under general, spinal or epidural anaesthesia and restart no earlier than 48 h after, once kidney function is stable. Switching IR to PR: same total daily dose; not advised above 2000 mg/day.", "", "Label · UK SmPC"),
    ("forms_ph", "Metformin (as hydrochloride) 500 mg oral tablet/film-coated tablet; 850 mg oral tablet.", "", "PNF"),
    ("monitor", "GFR before starting and at least yearly (every 3–6 months if at risk or elderly); vitamin B12 if anaemia or neuropathy; if symptoms suggest lactic acidosis, stop metformin and seek urgent care. Use particular caution in children aged 10–12 (few trial data). Overdose: lactic acidosis is an emergency; haemodialysis removes lactate and metformin.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (PNF, "PNF-EML lists 'Metformin (as hydrochloride) Oral: 500 mg tablet/film coated tablet, 850 mg tablet'."),
    (SMPC_IR, "Metformin 500 mg Tablets SmPC (Medley, rev 15/04/2025): adults 500/850 mg 2–3× daily with/after meals, adjust after 10–15 days, max 3 g/day; children ≥10 y 500/850 mg once daily, max 2 g/day in 2–3 doses; elderly by renal function; GFR bands 60–89 max 3 g, 45–59 max 2 g (start ≤ half), 30–44 max 1 g, <30 contraindicated; GFR yearly, 3–6 monthly if at risk/elderly; contraindications incl. diabetic pre-coma, dehydration/severe infection/shock, decompensated HF, respiratory failure, recent MI, hepatic insufficiency, alcohol intoxication/alcoholism; MELAS/MIDD not recommended; stable chronic HF OK with monitoring; surgery/contrast stop and restart ≥48 h; B12 monitoring; caution age 10–12; interactions NSAIDs/ACEi/ARB/diuretics, glucocorticoids/sympathomimetics, verapamil, rifampicin, OCT2 inhibitors incl. trimethoprim & isavuconazole, crizotinib, olaparib; pregnancy >1000 pregnancies, may be considered; breastfeeding not recommended; ADRs very rare hepatitis/LFT abnormalities, erythema/pruritus/urticaria; overdose haemodialysis; UKPDS outcomes (complications, diabetes mortality, all-cause mortality, MI); excreted unchanged, t½ ~6.5 h."),
    (SMPC_PR, "Metformin 500 mg PR SmPC (STADA, rev 15/04/2025): 500 mg once daily, +500 mg every 10–15 days, max 2000 mg once daily with evening meal; 1000 mg twice daily if inadequate; IR→PR same total dose, not if >2000 mg; with insulin start 500 mg; GFR 60–89 and 45–59 max 2000 mg, 30–44 max 1000 mg, <30 contraindicated; not for children."),
    (MSF, "MSF Metformin oral (updated 09/2023): first-line T2D; 500 mg od week 1, 500 mg bd week 2, +500 mg/week to max 2 g/day; contraindicated in ketoacidosis, cardiac/respiratory/hepatic/severe renal impairment; moderate renal impairment max 1 g/day; stop before surgery/iodinated contrast, restart 48 h after renal check; corticosteroids, HCTZ, salbutamol, chlorpromazine raise glucose; insulin drug of choice in pregnancy; breastfeeding no contraindication; 500 mg and 1 g tablets."),
    (WHOEML, "WHO eEML: metformin, hypoglycaemic agents, oral solid 500 mg, first added 1997 (TRS 882), type 2 diabetes."),
  ],
}
