UK_URL = "https://products.mhra.gov.uk/search/?search=spironolactone#emc-12015"
US_URL = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0fed2822-3a03-4b64-9857-c682fcd462bc"
PH_HF_URL = "https://pjc.philheart.org/elib/journal/identifier/pjc.2025.0712.012034/full"

MED = {
  "id": "med_spironolactone",
  "desc_add": "The 2023 Philippine clinical practice guidelines on chronic heart failure with reduced ejection fraction for primary care strongly recommend a mineralocorticoid receptor antagonist on top of standard care when eGFR is above 30 mL/min/1.73 m² and serum potassium is below 5 mEq/L; spironolactone is the only one of these drugs included in the Philippine National Formulary. It is also used in malignant ascites and as a diagnostic test for primary aldosteronism.",
  "facts": {
    "indication": [
      "Malignant ascites",
      "Diagnosis of primary aldosteronism (400 mg/day test) and pre-operative preparation",
    ],
    "adverse": [
      "Confusion, dizziness, muscle spasms and malaise",
      "Acute kidney injury; reversible rise in blood urea",
      "Pruritus, rash, urticaria",
      "Agranulocytosis, leukopenia, thrombocytopenia (frequency not known)",
      "Toxic epidermal necrolysis, DRESS, pemphigoid (frequency not known)",
      "Hypomagnesemia, hypocalcemia, hyperglycemia and hyperuricemia",
      "Hyperchloraemic metabolic acidosis in decompensated cirrhosis",
      "Worsening hepatic encephalopathy in cirrhosis with ascites",
    ],
    "contraindication": [
      "Anuria or acute renal insufficiency",
      "Other potassium-sparing diuretics (amiloride, triamterene) or routine potassium supplements",
      "Children with moderate to severe renal impairment",
      "Hypersensitivity to spironolactone",
    ],
    "interaction": [
      "Co-trimoxazole and low molecular weight heparin: clinically relevant hyperkalaemia.",
      "Potassium-containing salt substitutes or potassium-rich diet: hyperkalaemia.",
      "Digoxin: raised digoxin level and half-life; may interfere with digoxin assays.",
      "Other antihypertensives: additive blood pressure lowering; dose may need reducing.",
      "Carbenoxolone: sodium retention reduces the effect of spironolactone; avoid.",
      "Anaesthesia: reduced vascular response to noradrenaline.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("Philippine Journal of Cardiology", "Abola MTB, Punzalan FER, Magno JDA, et al. 2023 Philippine Clinical Practice Guidelines on the Diagnosis and Management of Chronic Heart Failure with Reduced Ejection Fraction for Primary Care Physicians. Philipp J Cardiol. 2025;53(2).", PH_HF_URL),
    ("UK SmPC (emc)", "Spironolactone 12.5 mg film-coated tablets. Summary of Product Characteristics. Mercury Pharmaceuticals Ltd; revised 14 October 2025. electronic medicines compendium (emc).", UK_URL),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "Contraindicated in anuria, acute renal insufficiency or significant renal compromise; higher hyperkalaemia risk in renal impairment. In heart failure with eGFR 30–50, start 25 mg every other day (US label); PH HF guideline recommends MRA only if eGFR >30."),
  ],
  "sources": [
    ("Label · US", "DailyMed (FDA label)", "ALDACTONE (spironolactone) tablets. Prescribing information. Pfizer; revised 11/2025. DailyMed, U.S. National Library of Medicine.", US_URL),
    ("Label · UK SmPC", "UK SmPC (emc)", "Spironolactone 12.5 mg film-coated tablets. Summary of Product Characteristics. Mercury Pharmaceuticals Ltd; revised 14 October 2025.", UK_URL),
    ("PH CPG 2023", "Philippine Journal of Cardiology", "Abola MTB, et al. 2023 Philippine CPG on chronic HFrEF for primary care physicians. Philipp J Cardiol. 2025;53(2).", PH_HF_URL),
  ],
  "doses": [
    ("adult", "Heart failure (HFrEF)", "PO", "25 mg", "Once a day", "Long-term", "50 mg/day", "Label · US", "Start if K ≤5.0 mEq/L and eGFR >50; if hyperkalaemia, 25 mg every other day"),
    ("adult", "Heart failure, eGFR 30–50", "PO", "25 mg", "Every other day", "Long-term", "—", "Label · US", ""),
    ("adult", "Hypertension", "PO", "25–100 mg", "Once a day or divided", "Long-term", "—", "Label · US", "Titrate every 2 weeks; >100 mg/day usually adds no BP lowering"),
    ("adult", "Edema (heart failure, nephrotic syndrome)", "PO", "100 mg", "Once a day or divided", "—", "200 mg/day", "Label · US", "Range 25–200 mg; give ≥5 days before increasing"),
    ("adult", "Cirrhosis with ascites", "PO", "100 mg (urine Na/K >1); 200–400 mg (Na/K <1)", "Once a day or divided", "—", "400 mg/day", "Label · UK SmPC", "Start in hospital, titrate slowly"),
    ("adult", "Malignant ascites", "PO", "100–200 mg", "Once a day or divided", "—", "400 mg/day", "Label · UK SmPC", ""),
    ("adult", "Primary aldosteronism (diagnostic test)", "PO", "400 mg", "Once a day or divided", "3–4 weeks (long) or 4 days (short)", "—", "Label · UK SmPC", ""),
    ("adult", "Primary aldosteronism (before surgery)", "PO", "100–400 mg", "Once a day or divided", "Until surgery", "400 mg/day", "Label · US", "If unfit for surgery: lowest effective dose"),
    ("child", "Edema / specialist use", "PO", "1–3 mg/kg/day ÷ doses", "Divided doses", "—", "—", "Label · UK SmPC", "Only under a paediatric specialist"),
  ],
  "notes": [
    ("renal", "Contraindicated in anuria, acute renal insufficiency or significant renal compromise.", "", "Label · UK SmPC"),
    ("renal", "Consider starting at 25 mg every other day in heart failure.", "eGFR 30–50", "Label · US"),
    ("renal", "Philippine HF guideline recommends an MRA only when eGFR is above 30 mL/min/1.73 m² and potassium is below 5 mEq/L.", "eGFR >30", "PH CPG 2023"),
    ("hepatic", "Cirrhosis: start in hospital at the lowest dose and titrate slowly; rapid fluid and electrolyte shifts can precipitate hepatic encephalopathy or coma.", "", "Label · US"),
    ("elderly", "Start at the lowest dose and titrate; monitor renal function and electrolytes, as reduced renal function is more common.", "", "Label · UK SmPC"),
    ("pregnancy", "Feminisation of male fetuses in animal studies; avoid in pregnancy or advise of the risk to a male fetus. Canrenone appears in milk in small amounts; UK labeling advises alternative infant feeding if use is essential.", "", "Label · US"),
    ("administration", "Take consistently with respect to food (UK labeling suggests once daily with a meal).", "", "Label · US"),
    ("monitor", "Heart failure: check potassium and creatinine at 1 week after starting or increasing the dose, monthly for 3 months, every 3 months for a year, then every 6 months. Stop or interrupt if K >5 mEq/L or creatinine >4 mg/dL.", "", "Label · UK SmPC"),
    ("monitor", "Check sodium, magnesium, calcium, uric acid, glucose, volume status and blood pressure; ask men about breast swelling or pain.", "", "Label · US"),
  ],
  "checked": [
    (UK_URL, "Mercury spironolactone 12.5 mg SmPC (rev 14/10/2025): 4.1 CHF, cirrhosis, malignant ascites, nephrotic, primary aldosteronism; 4.2 doses incl. Na/K ratio, malignant ascites 100–200 up to 400, aldosteronism tests 400 mg 3–4 wk/4 days, children 1–3 mg/kg/day divided, elderly lowest dose, with meal; 4.3 anuria, acute renal insufficiency, other K-sparing diuretics, children mod–severe renal impairment; 4.4 K/creatinine monitoring schedule, stop K>5/creat>4, hyperchloraemic acidosis in cirrhosis; 4.5 co-trimoxazole, LMWH, salt substitutes, digoxin, carbenoxolone, noradrenaline, antihypertensives; 4.6 alternative feeding; 4.8 confusion, dizziness, muscle spasms, AKI, pruritus, agranulocytosis, TEN, DRESS, pemphigoid."),
    (US_URL, "Aldactone label rev 11/2025: HF 25 mg daily if K ≤5.0 and eGFR >50, up to 50 mg, eGFR 30–50 25 mg every other day; HTN 25–100 mg, 2-week titration, >100 no added effect; edema 100 mg (25–200), ≥5 days, cirrhosis in hospital; aldosteronism 100–400 mg pre-surgery; food consistency; 5.3 hypomagnesemia, hypocalcemia, hyperglycemia, hyperuricemia; 8.1 male fetus risk; 8.2 canrenone low; 8.5–8.7 renal/hepatic encephalopathy; forms 25/50/100 mg (US, not PH)."),
    (PH_HF_URL, "2023 Philippine CPG chronic HFrEF for primary care (PJC 2025;53(2)): Recommendation 11, MRA (spironolactone or eplerenone) recommended on top of standard care if eGFR >30 and K <5 mEq/L (strong, low certainty); 'only spironolactone is included in the PNF'. No dose or forms given."),
  ],
}
