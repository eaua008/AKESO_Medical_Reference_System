PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
SMPC_URL = "https://products.mhra.gov.uk/search/?search=atorvastatin#emc-4343"
SMPC2_URL = "https://products.mhra.gov.uk/search/?search=atorvastatin#emc-2588"
CPG_URL = "https://www.asean-endocrinejournal.org/index.php/JAFES/article/view/927"
DM_URL = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a60cc18b-0631-4cf0-b021-9f52224ece65"

MED = {
  "id": "med_atorvastatin",
  "desc_add": "The 2020 Philippine dyslipidemia guidelines recommend early, maximally tolerated high-intensity statin therapy after ACS, an LDL-C goal below 55 mg/dL in clinical ASCVD, and statins for CKD patients not on dialysis (lipid care of dialysis and transplant patients is referred to a nephrologist). In the Philippines it is listed in the PNF as 10, 20, 40 and 80 mg tablets.",
  "facts": {
    "indication": [
      "Heterozygous familial hypercholesterolaemia in children aged 10 years and over",
    ],
    "adverse": [
      "Constipation, flatulence, nausea",
      "Myalgia, muscle spasms, joint swelling, back pain",
      "Raised creatine kinase",
      "Interstitial lung disease (rare)",
      "Higher haemorrhagic stroke incidence with 80 mg in patients with recent stroke/TIA (SPARCL), especially prior haemorrhagic stroke or lacunar infarct",
    ],
    "contraindication": [
      "Active liver disease or unexplained persistent transaminase elevation >3× ULN",
      "Pregnancy and breastfeeding",
      "Women of childbearing potential not using appropriate contraception",
      "Concurrent glecaprevir/pibrentasvir",
    ],
    "interaction": [
      "Systemic fusidic acid: must not be co-administered (fatal rhabdomyolysis reported); stop the statin and restart 7 days after the last fusidic acid dose.",
      "Elbasvir/grazoprevir or letermovir: do not exceed 20 mg daily; letermovir with ciclosporin is not recommended.",
      "Rifampicin: give at the same time; delayed atorvastatin dosing markedly lowers its levels.",
      "Azithromycin: post-marketing rhabdomyolysis reported with statins; use with caution.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Atorvastatin 20 mg Film-coated Tablets. Summary of Product Characteristics. Sun Pharma UK Ltd; revised 2024. electronic medicines compendium (emc).", SMPC_URL),
    ("JAFES (Philippine CPG)", "Gonzalez-Santos LE, Oliva R, Jimeno C, et al. Executive Summary of the 2020 Clinical Practice Guidelines for the Management of Dyslipidemia in the Philippines. J ASEAN Fed Endocr Soc. 2021;36(1):5–11. doi:10.15605/jafes.036.01.01", CPG_URL),
    ("DailyMed (FDA label)", "LIPITOR (atorvastatin calcium) tablet, film coated. Prescribing information. Viatris Specialty LLC; updated April 2024. DailyMed, U.S. National Library of Medicine.", DM_URL),
    ("PhilHealth / DOH (PNF-EML)", "Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.", PNF_URL),
  ],
  "links": [
    ("hepatitis_a", "avoid", "Active liver disease is a contraindication (UK SmPC)."),
    ("hepatitis_b", "caution", "Use with caution in hepatic impairment; contraindicated if active liver disease or persistent transaminases >3× ULN."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Atorvastatin 20 mg Film-coated Tablets. Summary of Product Characteristics. Sun Pharma UK Ltd; revised 2024.", SMPC_URL),
    ("Label · US FDA", "DailyMed (FDA label)", "LIPITOR (atorvastatin calcium) tablets. Prescribing information. Viatris; updated April 2024.", DM_URL),
    ("PH CPG 2020", "Philippine Dyslipidemia CPG 2020", "Gonzalez-Santos LE, et al. Executive Summary of the 2020 Clinical Practice Guidelines for the Management of Dyslipidemia in the Philippines. J ASEAN Fed Endocr Soc. 2021;36(1):5–11.", CPG_URL),
    ("PNF", "Philippine National Formulary – EML", "Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.", PNF_URL),
  ],
  "doses": [
    ("adult", "Hypercholesterolaemia / mixed dyslipidaemia", "PO", "10 mg", "Once a day", "Long-term", "80 mg/day", "Label · UK SmPC", "Adjust at intervals of ≥4 weeks"),
    ("adult", "Moderate-intensity statin therapy", "PO", "10–20 mg", "Once a day", "Long-term", "—", "PH CPG 2020", "Lowers LDL-C 30–50%"),
    ("adult", "High-intensity therapy (ASCVD, ACS, FH)", "PO", "40–80 mg", "Once a day", "Long-term", "80 mg/day", "PH CPG 2020", "Start early after ACS"),
    ("adult", "With elbasvir/grazoprevir or letermovir", "PO", "≤20 mg", "Once a day", "—", "20 mg/day", "Label · UK SmPC", ""),
    ("child", "Heterozygous FH (≥10 y)", "PO", "10 mg", "Once a day", "Long-term", "80 mg/day", "Label · UK SmPC", "US label range 10–20 mg; not indicated <10 y"),
    ("child", "Homozygous FH (≥10 y)", "PO", "10–20 mg", "Once a day", "Long-term", "80 mg/day", "Label · US FDA", ""),
  ],
  "notes": [
    ("renal", "No dose adjustment; monitor for myopathy.", "", "Label · US FDA"),
    ("renal", "Patients on dialysis or after kidney transplant: lipid management by a nephrologist (no statin recommendation made).", "Dialysis", "PH CPG 2020"),
    ("hepatic", "Use with caution in hepatic impairment; contraindicated in active liver disease.", "", "Label · UK SmPC"),
    ("elderly", "Efficacy and safety in patients over 70 at recommended doses are similar to the general population.", "", "Label · UK SmPC"),
    ("pregnancy", "Contraindicated in pregnancy and breastfeeding; women of childbearing potential should use appropriate contraception.", "", "Label · UK SmPC"),
    ("administration", "Whole daily dose at once, any time of day, with or without food. Give at the same time as rifampicin.", "", "Label · UK SmPC"),
    ("forms_ph", "Tablet: 10 mg, 20 mg, 40 mg, 80 mg (as calcium).", "", "PNF"),
    ("monitor", "Liver function tests before starting and periodically thereafter.", "", "Label · UK SmPC"),
    ("monitor", "Lipid panel (LDL-C) as early as 4 weeks after starting or changing the dose.", "", "Label · US FDA"),
    ("monitor", "Ask about muscle pain/weakness; check CK if present; stop if CK >10× ULN or rhabdomyolysis suspected.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (PNF_URL, "Atorvastatin calcium Oral: 10 mg, 20 mg, 40 mg and 80 mg tablet."),
    (SMPC_URL, "Sun Pharma UK atorvastatin SmPC: adult start 10 mg, max 80 mg, adjust at intervals ≥4 weeks; HeFH children ≥10 y start 10 mg, up to 80 mg, not indicated <10 y; no renal adjustment; caution in hepatic impairment; elderly >70 similar; any time of day with/without food; elbasvir/grazoprevir and letermovir (Table 1) max 20 mg; contraindications active liver disease, pregnancy, breastfeeding, glecaprevir/pibrentasvir; fusidic acid stop, restart 7 days after; SPARCL haemorrhagic stroke; ILD; LFTs before and periodically; CK >10× ULN discontinue; rifampicin simultaneous; common AEs constipation, flatulence, nausea, myalgia, muscle spasms, joint swelling, back pain, CK increased; contraception in women of childbearing potential."),
    (SMPC2_URL, "Milpharm atorvastatin SmPC (cross-check): contraindication includes women of childbearing potential not using contraception and transaminases >3× ULN; do not start if baseline CK >5× ULN, stop if >10× ULN; letermovir with ciclosporin not recommended."),
    (CPG_URL, "2020 PH dyslipidemia CPG: atorvastatin 10–20 mg moderate intensity (30–50% LDL-C lowering), 40–80 mg high intensity; early maximally tolerated high-intensity statin in ACS; high-intensity in FH; LDL-C <55 mg/dL in clinical ASCVD; statins for CKD not on dialysis; dialysis/transplant refer to nephrologist; CK check for myalgia."),
    (DM_URL, "Lipitor US label (updated April 2024): pediatric HeFH ≥10 y 10 mg start, range 10–20 mg; pediatric HoFH 10–20 mg start, range 10–80 mg; no renal dose adjustment but monitor for myopathy; LDL-C assess as early as 4 weeks."),
    ("https://products.mhra.gov.uk/search/?search=atorvastatin#emc-1073", "Zithromax SmPC 4.5: post-marketing rhabdomyolysis reported with azithromycin + statins (atorvastatin); use caution."),
  ],
}
