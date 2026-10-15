PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
NTP_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf"
MSF_R = "https://medicalguidelines.msf.org/en/viewport/TUB/english/rifampicin-r-20323858.html"
MSF_ED = "https://medicalguidelines.msf.org/en/node/570"
SMPC = "https://products.mhra.gov.uk/search/?search=rifampicin#emc-6384"

MED = {
  "id": "med_rifampicin",
  "desc_add": "In the Philippine NTP it is given throughout treatment in fixed-dose combinations (HRZE in the intensive phase, HR in the continuation phase of Category I 2HRZE/4HR; HRZE then HRE in Category II), with the number of tablets set by body-weight band. Single-drug rifampicin (including a 200 mg/5 mL suspension) is used for weight-based dosing in children who cannot take tablets.",
  "facts": {
    "indication": [
      "Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)",
      "Brucellosis, Legionnaires' disease and serious staphylococcal infections, with another antibiotic",
      "Chemoprophylaxis of Haemophilus influenzae: carriers and exposed children aged 4 years or younger",
    ],
    "adverse": [
      "Fever and chills (very common)",
      "Paradoxical reaction: TB symptoms recur after initial improvement, usually without treatment failure",
      "Thrombotic microangiopathy (TTP/HUS); stop if suspected",
      "Interstitial lung disease / pneumonitis",
      "Adrenal insufficiency in patients with compromised adrenal function",
      "Tooth discolouration (may be permanent)",
      "Headache and drowsiness",
    ],
    "contraindication": [
      "Jaundice",
      "History of severe haematological disorders (thrombocytopenia, purpura) during previous rifamycin treatment",
      "Concomitant sofosbuvir, daclatasvir or telaprevir",
    ],
    "interaction": [
      "Dolutegravir: levels fall substantially; dolutegravir is given 50 mg twice daily with rifampicin.",
      "Nevirapine, lopinavir/ritonavir or atazanavir/ritonavir: use rifabutin instead of rifampicin (MSF).",
      "Fluconazole: give 12 hours apart (rifampicin in the morning, fluconazole in the evening).",
      "Antacids: take rifampicin at least 1 hour before the antacid.",
      "Para-aminosalicylic acid: give at least 8 hours apart.",
      "Cefazolin and other cephalosporins with an NMTT side chain: avoid (risk of severe coagulation disorders).",
      "Paracetamol: may increase hepatotoxicity risk.",
      "Clopidogrel: concomitant use is discouraged; halothane: avoid.",
      "Phenytoin and hepatitis C direct-acting antivirals: reduced effect.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("Philippine NTP Manual of Procedures", "Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.", NTP_URL),
    ("Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.", PNF_URL),
    ("MSF Tuberculosis guideline", "Médecins Sans Frontières. Tuberculosis - Appendix 10, TB drug information sheets: Rifampicin (R). Updated January 2022.", MSF_R),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs - practical guidelines: Rifampicin (R) oral. Updated June 2021.", MSF_ED),
    ("UK SmPC (emc)", "Rifadin 300 mg Capsules - Summary of Product Characteristics. Aventis Pharma Ltd (Sanofi). Electronic medicines compendium (emc), updated June 2026.", SMPC),
  ],
  "links": [
    ("hepatitis_b", "caution", "Hepatic impairment: do not exceed 8 mg/kg/day and monitor LFTs closely; contraindicated with jaundice (UK SmPC, MSF). Applying this to hepatitis B is an inference."),
    ("type2_diabetes", "caution", "Rifampicin reduces the effect of antidiabetic drugs; doses may need adjusting (MSF)."),
    ("chronic_kidney_disease", "caution", "No adjustment up to 600 mg/day; caution if the dose exceeds 600 mg/day (UK SmPC)."),
  ],
  "sources": [
    ("NTP MOP 2014", "Philippine NTP Manual of Procedures", "DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 11–15).", NTP_URL),
    ("PNF", "Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.", PNF_URL),
    ("MSF TB", "MSF Tuberculosis guideline", "MSF Tuberculosis, Appendix 10: Rifampicin (R), 2022.", MSF_R),
    ("MSF", "MSF Essential Drugs", "MSF Essential drugs: Rifampicin (R) oral, 2021.", MSF_ED),
    ("Label · UK SmPC", "UK SmPC (emc)", "Rifadin 300 mg Capsules - SmPC. Sanofi, 2026.", SMPC),
  ],
  "doses": [
    ("adult", "TB Cat I (2HRZE/4HR), 30–37 kg", "PO", "2 tablets HRZE, then 2 tablets HR", "Once a day", "2 + 4 months", "—", "NTP MOP 2014", "Cat Ia (CNS, bones, joints): HR for 10 months"),
    ("adult", "TB Cat I (2HRZE/4HR), 38–54 kg", "PO", "3 tablets HRZE, then 3 tablets HR", "Once a day", "2 + 4 months", "—", "NTP MOP 2014", ""),
    ("adult", "TB Cat I (2HRZE/4HR), 55–70 kg", "PO", "4 tablets HRZE, then 4 tablets HR", "Once a day", "2 + 4 months", "—", "NTP MOP 2014", ""),
    ("adult", "TB Cat I (2HRZE/4HR), >70 kg", "PO", "5 tablets HRZE, then 5 tablets HR", "Once a day", "2 + 4 months", "—", "NTP MOP 2014", "Each tablet contains rifampicin 150 mg"),
    ("adult", "TB, single-drug formulation", "PO", "10 mg/kg (range 8–12)", "Once a day", "Per regimen", "600 mg/day", "NTP MOP 2014", "Usually 450 mg if <50 kg, 600 mg if ≥50 kg (UK SmPC)"),
    ("adult", "TB meningitis (6HRZEto)", "PO", "20 mg/kg", "Once a day", "6 months", "600 mg/day", "MSF TB", ""),
    ("adult", "Latent TB infection", "PO", "10 mg/kg", "Once a day", "4 months alone; 3 months with isoniazid", "600 mg/day", "MSF", ""),
    ("adult", "Leprosy", "PO", "600 mg", "Once a month", "6 months (PB); 12 months (MB)", "—", "MSF", "With dapsone and clofazimine"),
    ("adult", "Brucellosis, Legionnaires', serious staphylococcal infection", "PO", "600–1200 mg/day ÷ 2–4", "2–4× a day", "Brucellosis: 6 weeks", "1200 mg/day", "Label · UK SmPC", "Always with another antibiotic"),
    ("adult", "Meningococcal carrier eradication", "PO", "600 mg", "2× a day", "2 days", "—", "Label · UK SmPC", ""),
    ("child", "TB, single-drug formulation", "PO", "15 mg/kg (range 10–20)", "Once a day", "Per regimen", "600 mg/day", "NTP MOP 2014", "Suspension 200 mg/5 mL dosed by weight (Table 14); newborn <4 weeks: refer"),
    ("child", "TB meningitis (6HRZEto)", "PO", "20 mg/kg", "Once a day", "6 months", "600 mg/day", "MSF TB", ""),
    ("child", "Leprosy, <10 y / 10–14 y", "PO", "10 mg/kg / 450 mg", "Once a month", "6 months (PB); 12 months (MB)", "—", "MSF", ""),
    ("child", "Meningococcal carriers, 1–12 y", "PO", "10 mg/kg", "2× a day", "2 days", "—", "Label · UK SmPC", "Infants 3–12 months: 5 mg/kg"),
    ("child", "H. influenzae chemoprophylaxis", "PO", "20 mg/kg", "Once a day", "4 days", "600 mg/day", "Label · UK SmPC", "Neonates (1 month): 10 mg/kg"),
  ],
  "notes": [
    ("hepatic", "Do not exceed 8 mg/kg/day. Contraindicated in jaundice. Monitor ALT/AST weekly for 2 weeks, then every 2 weeks for the next 6 weeks; stop if hepatocellular damage occurs.", "", "Label · UK SmPC"),
    ("renal", "No adjustment up to 600 mg/day; use caution if the dose exceeds 600 mg/day.", "", "Label · UK SmPC"),
    ("elderly", "Use with caution, especially if liver function is impaired.", "", "Label · UK SmPC"),
    ("pregnancy", "Not contraindicated. Given in the last weeks of pregnancy it can cause bleeding in mother and newborn: give vitamin K (phytomenadione) to both. Not contraindicated in breastfeeding (MSF); passes into breast milk (UK SmPC).", "", "MSF"),
    ("administration", "Take on an empty stomach, at least 30 minutes before or 2 hours after a meal; a small amount of food may be used to improve GI tolerance (MSF). Take at least 1 hour before antacids.", "", "Label · UK SmPC"),
    ("administration", "Advise women on hormonal contraception to switch to injectable medroxyprogesterone or an IUD.", "", "MSF"),
    ("forms_ph", "Only in fixed-dose combinations (List B): isoniazid + rifampicin 50/75 mg dispersible tablet (pediatric) and 75/150 mg tablet; isoniazid + rifampicin + ethambutol 75/150/275 mg; isoniazid + rifampicin + pyrazinamide 50/75/150 mg dispersible; isoniazid + rifampicin + pyrazinamide + ethambutol 75/150/400/275 mg. A single-ingredient rifampicin entry could not be read in the PNF text (it stops at 'M').", "", "PNF"),
    ("monitor", "Baseline LFTs, blood count and renal function in adults with TB. Stop if purpura, thrombocytopenia or signs of TMA appear.", "", "Label · UK SmPC"),
    ("monitor", "Dosing less often than 2–3 times a week raises the risk of immune reactions (flu-like syndrome, anaphylaxis); monitor closely.", "", "Label · UK SmPC"),
    ("monitor", "Reassure about orange-red urine and secretions; soft contact lenses can be permanently stained.", "", "NTP MOP 2014"),
  ],
  "checked": [
    (PNF_URL, "Isoniazid + Rifampicin (B) 50 + 75 mg dispersible FDC (pediatric) and 75 + 150 mg tablet; Isoniazid + Rifampicin + Ethambutol (B) 75 + 150 + 275 mg; Isoniazid + Rifampicin + Pyrazinamide (B) 50 + 75 + 150 mg dispersible; Isoniazid + Rifampicin + Pyrazinamide + Ethambutol (B) 75 + 150 + 400 + 275 mg. PDF text ends at 'Multivitamins', so no standalone rifampicin entry could be checked."),
    (NTP_URL, "Table 10 regimens (Cat I 2HRZE/4HR, Ia 2HRZE/10HR, II 2HRZES/1HRZE/5HRE); Table 11 HRZE/HR tablets 30–37 kg 2, 38–54 kg 3, 55–70 kg 4, >70 kg 5, continuation same per band; Table 13 rifampicin adults 10 (8–12) mg/kg, children 15 (10–20) mg/kg, max 600 mg daily; Table 14 rifampicin 200 mg/5 ml by weight 2.1–30 kg, newborn <4 weeks refer; Table 15 orange/red urine (R): reassure; GI intolerance: bedtime or small meals."),
    (MSF_R, "MSF TB Rifampicin (Jan 2022): <30 kg 15 (10–20) mg/kg; ≥30 kg and adults 10 (8–12) mg/kg; max 600 mg; hepatic impairment max 8 mg/kg; TB meningitis 6HRZEto 20 mg/kg max 600 mg; contraindicated after severe haematologic disorders with previous rifamycin; reduces antidiabetics, phenytoin, HCV DAAs, etc.; fluconazole 12 h apart; contraception DMPA or IUD; vitamin K late pregnancy."),
    (MSF_ED, "MSF Essential drugs Rifampicin oral (June 2021): latent TB 4 months alone/3 months with isoniazid; leprosy monthly <10 y 10 mg/kg, 10–14 y 450 mg, ≥15 y 600 mg, PB 6 months, MB 12 months; brucellosis 6 weeks; contraindications jaundice, rifamycin hypersensitivity, prior severe haematological disorders; headache, drowsiness; nevirapine, LPV/r, ATV/r -> rifabutin; not contraindicated in pregnancy/breastfeeding; vitamin K."),
    (SMPC, "Rifadin 300 mg (Sanofi, June 2026): indications incl. brucellosis, Legionnaires', serious staph, meningococcal carriers, H. influenzae carriers/prophylaxis ≤4 y; TB adults 8–12 mg/kg, usually 450 mg <50 kg / 600 mg ≥50 kg; children 10–20 mg/kg max 600 mg; leprosy 600 mg monthly; brucellosis etc. 600–1200 mg/day in 2–4 doses; meningococcal adults 600 mg BD 2 days, children 1–12 y 10 mg/kg BD, infants 3–12 mo 5 mg/kg; H. influenzae 20 mg/kg OD max 600 mg 4 days, neonates 10 mg/kg; hepatic max 8 mg/kg; renal caution >600 mg/day; elderly caution; 30 min before or 2 h after meal; contraindications jaundice, saquinavir/ritonavir, lurasidone, sofosbuvir, daclatasvir, telaprevir etc.; LFT weekly ×2 then 2-weekly ×6 weeks in hepatic impairment; baseline blood count/renal; TMA; intermittent <2–3×/week immunological reactions; teeth/contact lens discolouration; interactions PAS 8 h, antacids 1 h, halothane, cefazolin/NMTT, paracetamol, clopidogrel; vitamin K late pregnancy; ADRs pyrexia/chills, paradoxical reaction, adrenal insufficiency, ILD."),
  ],
}
