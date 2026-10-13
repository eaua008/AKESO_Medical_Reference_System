MC_URL = "https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-428"
MR_URL = "https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-15362"
MSF_URL = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/nitrofurantoin-oral-16684353.html"
EML_URL = "https://list.essentialmeds.org/medicines/301"

MED = {
  "id": "med_nitrofurantoin",
  "desc_add": "WHO lists it as an Access-group antibiotic and a first-choice option for infectious cystitis, as 50 mg and 100 mg oral solids and a 25 mg/5 mL oral liquid. MSF keeps it for uncomplicated cystitis without fever or flank pain when no other antibiotic can be used.",
  "facts": {
    "indication": [
      "Prophylaxis around urological surgery (during the procedure and for 3 days after)",
    ],
    "adverse": [
      "Dizziness and drowsiness (avoid driving if affected)",
      "Aplastic anaemia (rare), agranulocytosis, thrombocytopenia",
      "DRESS and Stevens-Johnson syndrome",
      "Benign intracranial hypertension",
      "Pancreatitis and interstitial nephritis",
      "Psychiatric reactions",
      "False-positive urine glucose tests",
    ],
    "contraindication": [
      "eGFR below 45 mL/min (UK SmPC threshold)",
      "G6PD deficiency",
      "Acute porphyria",
      "Infants under 3 months (UK SmPC)",
    ],
    "interaction": [
      "Quinolone antibiotics: antagonise its antibacterial effect.",
      "Carbonic anhydrase inhibitors and urine alkalinisers: reduce antibacterial activity.",
      "Food or drugs that delay gastric emptying: increase absorption.",
      "Aluminium/magnesium hydroxide antacids: separate doses by at least 2 hours.",
      "Oral typhoid vaccine: inactivated by antibacterials.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Macrodantin / Nitrofurantoin 100 mg Capsules, Hard (macrocrystals). Summary of Product Characteristics. Mercury Pharmaceuticals (ADVANZ Pharma); updated August 2025. electronic medicines compendium (emc).", MC_URL),
    ("UK SmPC (emc)", "Nitrofurantoin Mercury Pharma 100 mg Prolonged-Release Capsules (MacroBID). Summary of Product Characteristics. ADVANZ Pharma; updated August 2025. electronic medicines compendium (emc).", MR_URL),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Nitrofurantoin oral. MSF Medical Guidelines.", MSF_URL),
    ("WHO eEML", "World Health Organization. Electronic Essential Medicines List – Nitrofurantoin (Access group antibiotic).", EML_URL),
  ],
  "links": [
    ("type2_diabetes", "caution", "SmPC advises caution in diabetes, which raises the risk of peripheral neuropathy."),
    ("iron_deficiency_anemia", "caution", "SmPC advises caution in anaemia (stated for anaemia in general, not iron deficiency specifically)."),
  ],
  "sources": [
    ("PhilHealth Konsulta", "PhilHealth Konsulta medicines list (Annex D2)", "Philippine Health Insurance Corporation. Konsulta package: Certification of Service Delivery Support (Medicines), Annex D2.", "https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf"),
    ("Label · UK SmPC", "UK SmPC (emc)", "Macrodantin / Nitrofurantoin 100 mg Capsules (macrocrystals). SmPC. ADVANZ Pharma; August 2025.", MC_URL),
    ("Label · UK SmPC MR", "UK SmPC (emc)", "Nitrofurantoin 100 mg Prolonged-Release Capsules (MacroBID). SmPC. ADVANZ Pharma; August 2025.", MR_URL),
    ("MSF", "MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Nitrofurantoin oral.", MSF_URL),
  ],
  "doses": [
    ("adult", "Acute uncomplicated lower UTI (macrocrystals)", "PO", "50 mg", "4× a day", "7 days", "—", "Label · UK SmPC", ""),
    ("adult", "Severe chronic recurrent UTI (macrocrystals)", "PO", "100 mg", "4× a day", "7 days", "—", "Label · UK SmPC", ""),
    ("adult", "Acute or recurrent lower UTI (prolonged-release, ≥12 y)", "PO", "100 mg", "2× a day", "7 days", "—", "Label · UK SmPC MR", ""),
    ("adult", "Uncomplicated cystitis (100 mg tablet)", "PO", "100 mg", "Every 8 h", "5–7 days", "—", "MSF", "Only if no other antibiotic can be used"),
    ("adult", "Long-term suppression", "PO", "50–100 mg", "Once a day", "Long-term", "—", "Label · UK SmPC", ""),
    ("adult", "Surgical prophylaxis (macrocrystals)", "PO", "50 mg", "4× a day", "Procedure + 3 days", "—", "Label · UK SmPC", ""),
    ("adult", "Surgical prophylaxis (prolonged-release)", "PO", "100 mg", "2× a day", "Day of procedure + 3 days", "—", "Label · UK SmPC MR", ""),
    ("child", "Acute UTI (>3 mo)", "PO", "3 mg/kg/day ÷ 4", "4× a day", "7 days", "—", "Label · UK SmPC", "Under 25 kg: consider suspension"),
    ("child", "Suppression (>3 mo)", "PO", "1 mg/kg", "Once a day", "Long-term", "—", "Label · UK SmPC", ""),
  ],
  "notes": [
    ("forms_ph", "Nitrofurantoin (as macrocrystals) 50 mg and 100 mg capsules (PhilHealth Konsulta medicines list).", "", "PhilHealth Konsulta"),
    ("renal", "Contraindicated.", "eGFR <45", "Label · UK SmPC"),
    ("renal", "Short course only, for uncomplicated lower UTI with resistant organisms when benefit outweighs risk.", "eGFR 30–44", "Label · UK SmPC"),
    ("hepatic", "Rare but potentially fatal hepatitis; use with caution in liver disease.", "", "Label · UK SmPC"),
    ("elderly", "Normal adult dose if no significant renal impairment; pulmonary reactions more common in the elderly and with long-term use.", "", "Label · UK SmPC"),
    ("pregnancy", "Use the lowest effective dose after careful assessment; contraindicated at term (newborn haemolysis). Breastfeeding: avoid if the infant has G6PD or other red-cell enzyme deficiency; MSF advises avoiding in the first month.", "", "Label · UK SmPC"),
    ("administration", "Take with food or milk (improves absorption). Prolonged-release capsules are not suitable under 12 years.", "", "Label · UK SmPC"),
    ("monitor", "Check liver tests periodically on long-term treatment.", "", "Label · UK SmPC"),
    ("monitor", "Stop at first sign of paraesthesia (neuropathy), new cough/dyspnoea (pulmonary reaction) or haemolysis.", "", "Label · UK SmPC"),
    ("monitor", "Recurrent or severe cases: exclude a surgical cause or a non-functioning kidney.", "", "Label · UK SmPC"),
  ],
  "checked": [
    ("https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf", "Konsulta Annex D2 lists the forms in the forms_ph note."),
    (MC_URL, "Macrodantin/nitrofurantoin 100 mg macrocrystal capsules SmPC (Aug 2025): adults acute 50 mg QDS 7 d; severe chronic recurrent 100 mg QDS 7 d; suppression 50–100 mg once daily; prophylaxis 50 mg QDS procedure + 3 d; children >3 mo 3 mg/kg/day in 4 doses 7 d, suppression 1 mg/kg daily, <25 kg consider suspension; elderly normal dose; contraindicated eGFR <45, G6PD, acute porphyria, infants <3 mo, term pregnancy; eGFR 30–44 short course; caution in anaemia, diabetes etc.; pulmonary/hepatic/neuropathy warnings and periodic LFTs; false-positive urine glucose; interactions: delayed gastric emptying, magnesium trisilicate, probenecid, carbonic anhydrase inhibitors/urine alkalinisation, quinolones, oral typhoid vaccine; pregnancy lowest dose; breastfeeding infant G6PD; dizziness/drowsiness; AEs aplastic anaemia, agranulocytosis, thrombocytopenia, DRESS, SJS, benign intracranial hypertension, pancreatitis, interstitial nephritis, psychiatric reactions; take with food or milk."),
    (MR_URL, "Nitrofurantoin 100 mg prolonged-release (MacroBID) SmPC (Aug 2025): adults/children >12 y 100 mg BID 7 d; surgical prophylaxis 100 mg BID day of procedure + 3 d; not for <12 y; eGFR <45 contraindicated, 30–44 caution."),
    (MSF_URL, "MSF nitrofurantoin oral: 100 mg tablet; uncomplicated cystitis when no other antibiotic; adult 100 mg TDS 5–7 d; contraindicated renal impairment, G6PD; separate from Al/Mg hydroxide antacids by 2 h; avoid last month of pregnancy, avoid breastfeeding first month; take with meals; do not use for prevention."),
    (EML_URL, "WHO eEML: nitrofurantoin, Access group; oral liquid 25 mg/5 mL; oral solid 50 mg, 100 mg; first choice for infectious cystitis."),
    ("https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf", "Opened, but WebFetch text ends at 'Multivitamins' (65,922 chars); nitrofurantoin entry not readable, so no forms_ph note."),
  ],
}
