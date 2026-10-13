SMPC = "https://products.mhra.gov.uk/search/?search=amlodipine#emc-2743"
PNF = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
PHHTN = "https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf"

MED = {
  "id": "med_amlodipine",
  "desc_add": "In the Philippines it is listed in the PNF Essential Medicines List (5 mg and 10 mg tablets) and is the first drug in the national primary-care hypertension protocol, with losartan added if blood pressure stays above target. Amlodipine is not removed by dialysis, and the usual dose is used in renal impairment.",
  "facts": {
    "indication": [],
    "adverse": [
      "Abdominal pain and nausea",
      "Gingival hyperplasia (very rare)",
      "Hepatitis, jaundice and raised liver enzymes, mostly cholestatic (very rare)",
      "Extrapyramidal disorder (exceptional reports)",
      "Angioedema, Stevens-Johnson syndrome and erythema multiforme (very rare)",
      "Overdose: marked prolonged hypotension and non-cardiogenic pulmonary oedema (may appear 24–48 h after ingestion)",
    ],
    "contraindication": [
      "Hypersensitivity to other dihydropyridines",
      "Severe hypotension",
      "Shock, including cardiogenic shock",
      "Left ventricular outflow obstruction (e.g., high-grade aortic stenosis)",
      "Haemodynamically unstable heart failure after acute myocardial infarction",
    ],
    "interaction": [
      "Diltiazem and verapamil (CYP3A4 inhibitors): increased amlodipine exposure and hypotension risk, especially in the elderly.",
      "CYP3A4 inducers (rifampicin, St John's wort): may alter amlodipine levels; monitor blood pressure during and after co-administration.",
      "Grapefruit or grapefruit juice: not recommended (may increase blood-pressure lowering).",
      "IV dantrolene: avoid calcium channel blockers in patients susceptible to or treated for malignant hyperthermia (hyperkalaemia risk).",
      "mTOR inhibitors (sirolimus, temsirolimus, everolimus): amlodipine may increase their exposure.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Amlodipine 5 mg Tablets. Summary of Product Characteristics. Generics UK Ltd t/a Mylan (Viatris). electronic medicines compendium (emc); text revised 07/2022.", SMPC),
    ("Philippine National Formulary (PhilHealth)", "Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.", PNF),
    ("National Protocol for Hypertension Management (Philippines)", "National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives; 2021 (rev. 2023).", PHHTN),
  ],
  "links": [
    ("heart_failure", "caution", "Use with caution: more pulmonary oedema in NYHA III–IV trial; contraindicated in unstable heart failure after acute MI."),
    ("acute_coronary_syndrome", "caution", "Contraindicated in haemodynamically unstable heart failure after acute MI and in cardiogenic shock."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Amlodipine 5 mg Tablets SmPC, Generics UK Ltd t/a Mylan; text revised 07/2022.", SMPC),
    ("PNF", "Philippine National Formulary (PhilHealth)", "PNF Essential Medicines List, 2022.", PNF),
    ("PH HTN protocol", "National Protocol for Hypertension Management (Philippines)", "National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives.", PHHTN),
  ],
  "doses": [
    ("adult", "Hypertension", "PO", "5 mg", "Once a day", "Long-term", "10 mg/day", "Label · UK SmPC", "Increase by response"),
    ("adult", "Chronic stable or vasospastic angina", "PO", "5 mg", "Once a day", "Long-term", "10 mg/day", "Label · UK SmPC", ""),
    ("adult", "Hypertension (PH primary care)", "PO", "5 mg, then 10 mg", "Once a day", "Long-term", "10 mg/day", "PH HTN protocol", "Step 1: 5 mg; step 2: add losartan 50 mg; step 3: amlodipine 10 mg + losartan 100 mg (1-month intervals)"),
    ("child", "Hypertension (6–17 years)", "PO", "2.5 mg", "Once a day", "Long-term", "5 mg/day", "Label · UK SmPC", "May increase to 5 mg after 4 weeks; no data under 6 years"),
  ],
  "notes": [
    ("renal", "Usual dose. Amlodipine is not removed by dialysis.", "", "Label · UK SmPC"),
    ("hepatic", "Mild–moderate impairment: start at the low end of the dose range. Severe impairment: start at the lowest dose and titrate slowly (prolonged half-life, higher AUC).", "", "Label · UK SmPC"),
    ("elderly", "Usual doses apply; increase the dose with care.", "", "Label · UK SmPC"),
    ("pregnancy", "Safety in pregnancy not established; use only when there is no safer alternative. Excreted in breast milk (infant dose about 3–7% of maternal dose, max 15%).", "", "Label · UK SmPC"),
    ("administration", "Can be combined with thiazide diuretics, beta-blockers, alpha-blockers or ACE inhibitors. In the PH protocol, amlodipine and losartan are taken together; confirm adherence before stepping up.", "", "PH HTN protocol"),
    ("forms_ph", "Amlodipine (as besilate/camsylate) 5 mg and 10 mg oral tablets.", "", "PNF"),
    ("monitor", "Blood pressure and symptoms of hypotension; ankle/peripheral oedema; heart-failure symptoms; slow titration with close monitoring in hepatic impairment.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (PNF, "PNF-EML lists 'Amlodipine (as besilate/camsylate) Oral: 5 mg and 10 mg tablet'."),
    (SMPC, "Amlodipine 5 mg Tablets SmPC (Mylan/Viatris, rev 07/2022): adult 5 mg od max 10 mg; paediatric 6–17 y 2.5 mg od up to 5 mg after 4 weeks; elderly/hepatic/renal guidance; not dialysable; contraindications (dihydropyridine hypersensitivity, severe hypotension, shock, LVOT obstruction, unstable HF post-MI); interactions (CYP3A4 inhibitors incl. diltiazem/verapamil, inducers rifampicin/St John's wort, grapefruit, dantrolene, tacrolimus, mTOR inhibitors); pregnancy/lactation 3–7%; ADRs incl. gingival hyperplasia, hepatitis/jaundice, extrapyramidal, SJS; overdose non-cardiogenic pulmonary oedema 24–48 h."),
    (PHHTN, "National Protocol for Hypertension Management in Primary Health Care Settings: step 1 amlodipine 5 mg od; step 2 add losartan 50 mg; step 3 amlodipine 10 mg + losartan 100 mg; step 4 add HCTZ 25 mg or refer; take together; check adherence. (Issuing body not printed in the text; hosted by Resolve to Save Lives.)"),
  ],
}
