MSF = "https://medicalguidelines.msf.org/viewport/EssDr/english/hydrochlorothiazide-oral-16683854.html"
DM = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=7b38ac8a-4540-4eb2-aedd-9aa966d22190"
PNF = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
PHHTN = "https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf"
MHRA = "https://www.gov.uk/drug-safety-update/hydrochlorothiazide-risk-of-non-melanoma-skin-cancer-particularly-in-long-term-use"
WHOEML = "https://list.essentialmeds.org/medicines/139"

MED = {
  "id": "med_hydrochlorothiazide",
  "desc_add": "In the Philippines it is listed in the PNF Essential Medicines List as 12.5 mg and 25 mg tablets and in fixed combinations with losartan, enalapril and irbesartan. In the national primary-care hypertension protocol, hydrochlorothiazide 25 mg once daily is the step-4 add-on to amlodipine plus losartan (or the patient is referred). Long-term use carries a dose-dependent risk of non-melanoma skin cancer, thought to relate to its photosensitising effect.",
  "facts": {
    "indication": [],
    "adverse": [
      "Dehydration and hypotension, including orthostatic hypotension",
      "Headache, dizziness, vertigo, paraesthesia",
      "Impotence",
      "Non-melanoma skin cancer (basal cell and squamous cell carcinoma, lip cancer) with high cumulative long-term use",
      "Interstitial nephritis, renal dysfunction",
      "Sialadenitis",
      "Hypersensitivity: anaphylaxis, necrotising angiitis, pneumonitis, pulmonary oedema",
      "Exacerbation or activation of systemic lupus erythematosus",
      "Transient blurred vision, xanthopsia",
    ],
    "contraindication": [
      "Severe renal failure",
    ],
    "interaction": [
      "Cholestyramine and colestipol: reduce hydrochlorothiazide absorption (by up to 85% and 43%).",
      "Drugs that cause hypotension (e.g., haloperidol, amitriptyline) and other antihypertensives: additive hypotension.",
      "SSRIs, carbamazepine: added risk of hyponatraemia.",
      "Laxatives, amphotericin B: added potassium loss.",
      "Calcium or vitamin D (ergocalciferol): risk of hypercalcaemia.",
      "Pressor amines (e.g., noradrenaline): possibly reduced response.",
      "Nondepolarising muscle relaxants: possibly increased response.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("MSF Essential Drugs", "Médecins Sans Frontières. Hydrochlorothiazide oral. In: Essential Drugs – practical guidelines. MSF Medical Guidelines.", MSF),
    ("Philippine National Formulary (PhilHealth)", "Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.", PNF),
    ("National Protocol for Hypertension Management (Philippines)", "National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives; 2021 (rev. 2023).", PHHTN),
    ("MHRA Drug Safety Update", "Medicines and Healthcare products Regulatory Agency. Hydrochlorothiazide: risk of non-melanoma skin cancer, particularly in long-term use. Drug Safety Update 2018;12(4).", MHRA),
    ("WHO Model List of Essential Medicines", "World Health Organization. eEML – Electronic Essential Medicines List: Hydrochlorothiazide (first added 1977).", WHOEML),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "Use with caution in severe renal disease (may precipitate azotemia; stop if impairment progresses); MSF advises not to give in severe renal failure."),
    ("type2_diabetes", "caution", "Can raise blood glucose; doses of oral antidiabetics or insulin may need adjusting."),
  ],
  "sources": [
    ("MSF", "MSF Essential Drugs", "Médecins Sans Frontières. Hydrochlorothiazide oral. Essential Drugs – practical guidelines.", MSF),
    ("Label · DailyMed", "DailyMed (US National Library of Medicine)", "Hydrochlorothiazide Tablets USP 25 mg and 50 mg. Prescribing information. Caraco Pharmaceutical Laboratories; 2007.", DM),
    ("PH HTN protocol", "National Protocol for Hypertension Management (Philippines)", "National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives.", PHHTN),
    ("PNF", "Philippine National Formulary (PhilHealth)", "PNF Essential Medicines List, 2022.", PNF),
    ("MHRA 2018", "MHRA Drug Safety Update", "Hydrochlorothiazide: risk of non-melanoma skin cancer, particularly in long-term use. Drug Safety Update, November 2018.", MHRA),
  ],
  "doses": [
    ("adult", "Hypertension", "PO", "12.5–25 mg", "Once a day", "Long-term", "25 mg/day", "MSF", "Morning dose"),
    ("adult", "Hypertension (PH primary care, step 4)", "PO", "25 mg", "Once a day", "Long-term", "—", "PH HTN protocol", "Added to amlodipine 10 mg + losartan 100 mg if BP still high after 1 month (or refer)"),
    ("adult", "Hypertension", "PO", "25 mg, up to 50 mg/day", "Once a day or 2× a day", "Long-term", "50 mg/day", "Label · DailyMed", "Doses above 50 mg/day cause marked potassium loss"),
    ("adult", "Oedema (renal, hepatic, heart failure)", "PO", "25 mg", "Once a day or 2× a day", "By response", "100 mg/day", "MSF", "Morning dose"),
    ("adult", "Oedema", "PO", "25–100 mg/day", "Once a day or divided", "By response", "100 mg/day", "Label · DailyMed", "Intermittent dosing (alternate days or 3–5 days a week) lowers electrolyte risk"),
    ("child", "Oedema / hypertension", "PO", "1–2 mg/kg/day ÷ 1–2", "Once a day or 2× a day", "By response", "37.5 mg/day (<2 y); 100 mg/day (2–12 y)", "Label · DailyMed", "Infants <6 months may need up to 3 mg/kg/day ÷ 2"),
  ],
  "notes": [
    ("renal", "Do not give in severe renal failure.", "Severe", "MSF"),
    ("renal", "Use with caution in severe renal disease: may precipitate azotemia and accumulate; withhold or stop if renal impairment progresses.", "", "Label · DailyMed"),
    ("hepatic", "Use with caution in hepatic impairment or progressive liver disease: small fluid/electrolyte shifts may precipitate hepatic coma.", "", "Label · DailyMed"),
    ("elderly", "Use with caution.", "", "MSF"),
    ("pregnancy", "MSF lists pregnancy and breastfeeding as contraindications. Thiazides cross the placenta (risk of fetal/neonatal jaundice and thrombocytopenia) and pass into breast milk; routine use in normal pregnancy is inappropriate.", "", "MSF"),
    ("administration", "Take in the morning. Recommend a potassium-rich diet; give a sustained-release potassium supplement if K+ < 3.5 mmol/L. Not indicated for nutritional oedema. Stop before parathyroid function tests.", "", "MSF"),
    ("forms_ph", "Hydrochlorothiazide 12.5 mg and 25 mg oral tablets. Fixed combinations: losartan 50 mg + HCTZ 12.5 mg, enalapril 20 mg + HCTZ 12.5 mg, irbesartan 150 mg + HCTZ 12.5 mg tablets.", "", "PNF"),
    ("monitor", "Serum electrolytes (K+, Na+, Mg2+, Ca2+), renal function, glucose, uric acid and lipids periodically; BP including orthostatic drop; confirm adherence before stepping up.", "", "Label · DailyMed"),
    ("monitor", "Long-term use: advise regular skin self-checks and sun/UV protection; examine new or changing lesions; reconsider HCTZ in patients with previous skin cancer.", "", "MHRA 2018"),
  ],
  "checked": [
    (PNF, "PNF-EML lists Hydrochlorothiazide 'Oral: 12.5 mg and 25 mg tablet' and combinations: enalapril 20 mg + HCTZ 12.5 mg, irbesartan 150 mg + HCTZ 12.5 mg, losartan 50 mg + HCTZ 12.5 mg tablets."),
    (MSF, "MSF Hydrochlorothiazide oral: hypertension 12.5–25 mg od morning max 25 mg/day; oedema 25 mg od or bid max 100 mg/day; contraindicated severe renal failure, pregnancy, breastfeeding; caution elderly; ADRs dehydration, hypotension, headache, dizziness, impotence, photosensitivity; interactions haloperidol/amitriptyline, corticosteroids/laxatives/amphotericin B, SSRIs/carbamazepine, calcium/ergocalciferol, antidiabetics; potassium-rich diet, SR K if <3.5 mmol/L; not for nutritional oedema."),
    (DM, "DailyMed Caraco HCTZ label (2007; already in refs, used only as a dose-table source): adult edema 25–100 mg/day, intermittent dosing; hypertension 25 mg up to 50 mg/day; children 1–2 mg/kg/day, max 37.5 mg (<2 y) / 100 mg (2–12 y), infants <6 mo up to 3 mg/kg/day in 2 doses; caution severe renal disease (azotemia) and hepatic disease (hepatic coma); SLE; cholestyramine 85%/colestipol 43%; pressor amines; muscle relaxants; ADRs sialadenitis, interstitial nephritis, anaphylaxis, pneumonitis, xanthopsia; stop before parathyroid tests; placenta/neonatal jaundice/thrombocytopenia."),
    (PHHTN, "PH primary-care protocol: step 4 'Add hydrochlorothiazide 25 mg once daily' OR refer, after 1 month if BP still high; check adherence before stepping up."),
    (MHRA, "MHRA DSU Nov 2018: dose-dependent NMSC (BCC, SCC, lip) risk with cumulative HCTZ; inform patients, skin self-checks, limit sun/UV, examine lesions, reconsider in previous skin cancer; photosensitising mechanism."),
    (WHOEML, "WHO eEML: hydrochlorothiazide first added 1977 (hypertension, oedema), heart failure 1997; oral solid 12.5/25 mg, oral liquid 50 mg/5 mL."),
  ],
}
