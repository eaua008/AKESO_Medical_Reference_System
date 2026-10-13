HTA_TLD = "https://hta.dost.gov.ph/wp-content/uploads/2021/09/ES_TLD_for_HIV_approved_by_SOH.docx.pdf"
WHO_2026 = "https://www.who.int/news/item/07-01-2026-who-releases-updated-recommendations-on-hiv-clinical-management"
WHOPAR = "https://extranet.who.int/prequal/sites/default/files/whopar_files/HA729part4v2.pdf"
MSF_DTG = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/dolutegravir-dtg-oral-38537537.html"
WHO_FS = "https://www.who.int/news-room/fact-sheets/detail/hepatitis-B"

MED = {
  "id": "med_tld",
  "desc_add": "The Philippine HTA Council recommended TLD for both treatment-naive and treatment-experienced adolescents and adults with HIV, a decision approved by the Secretary of Health on 1 September 2021, noting a monthly bottle cost (PHP 549) equal to the older tenofovir/lamivudine/efavirenz tablet. WHO's January 2026 HIV clinical management update confirms dolutegravir-based regimens as the preferred option for initial and subsequent treatment and supports reusing tenofovir in later regimens.",
  "facts": {
    "indication": [],
    "adverse": [
      "Insomnia, abnormal dreams, anxiety and depression (common; neuropsychiatric effects were the most reported in a Zambian pharmacovigilance study)",
      "Dizziness, vomiting, asthenia and rash (very common)",
      "Raised ALT/AST and creatine phosphokinase",
      "Arthralgia, fatigue, fever, hair loss and pruritus",
      "Pancreatitis (rare); stop if suspected",
      "Small increased risk of neural tube defects with exposure around conception (0.19% vs 0.11% in Botswana surveillance)",
    ],
    "contraindication": [
      "HIV-1 with integrase inhibitor resistance (fixed-dose tablet is for INSTI-susceptible HIV-1)",
      "Children weighing under 30 kg (separate formulations needed)",
    ],
    "interaction": [
      "Etravirine (without a boosted protease inhibitor): lowers dolutegravir exposure by about 71%; dolutegravir is given 50 mg twice daily.",
      "Efavirenz, nevirapine, oxcarbazepine and phenobarbital: expected to lower dolutegravir levels; the dolutegravir dose is doubled with enzyme inducers.",
      "Rifampicin and other enzyme inducers: continue the double dolutegravir dose for 2 weeks after the inducer is stopped (MSF).",
      "Sorbitol, mannitol and other polyols: reduce lamivudine exposure; avoid chronic co-use or monitor viral load.",
      "Cladribine: not recommended with lamivudine.",
      "Emtricitabine, adefovir dipivoxil, tenofovir alafenamide and didanosine: not co-administered.",
      "Metformin: MSF advises not exceeding 1 g/day with dolutegravir and monitoring blood glucose and renal function.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("DOST HTA Philippines", "Health Technology Assessment Council (DOST / DOH). Evidence summary: Tenofovir/lamivudine/dolutegravir (TLD) for treatment-naive and treatment-experienced adolescents and adults living with HIV. Approved by the Secretary of Health 1 September 2021.", HTA_TLD),
    ("World Health Organization", "World Health Organization. WHO releases updated recommendations on HIV clinical management. News release, 7 January 2026.", WHO_2026),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs - practical guidelines: Dolutegravir = DTG oral. Updated October 2024.", MSF_DTG),
    ("World Health Organization", "World Health Organization. Hepatitis B. Fact sheet, updated 28 July 2026.", WHO_FS),
  ],
  "links": [
    ("hepatitis_b", "safe", "Tenofovir (in first-line HIV combinations) is active against HBV (WHO); in coinfection do not stop TLD without HBV cover because of flare risk (WHOPAR)."),
    ("tuberculosis", "caution", "Rifampicin lowers dolutegravir levels; an extra dolutegravir 50 mg tablet is added to TLD during TB treatment (DOST HTA, WHOPAR)."),
    ("chronic_kidney_disease", "avoid", "Fixed-dose tablet not recommended when CrCl is below 50 mL/min; use separate components with dose adjustment (WHOPAR)."),
    ("type2_diabetes", "caution", "Dolutegravir raises metformin levels; monitor glucose and renal function and limit metformin to 1 g/day (MSF)."),
  ],
  "sources": [
    ("WHOPAR", "WHO Prequalification (WHOPAR product information)", "WHO Prequalification. Dolutegravir/Lamivudine/Tenofovir disoproxil fumarate 50/300/300 mg tablets (HA729), SmPC, WHOPAR part 4, Oct 2022.", WHOPAR),
    ("DOST HTA 2021", "DOST HTA Philippines", "HTA Council evidence summary: TLD for adolescents and adults living with HIV, approved by SOH 1 Sep 2021.", HTA_TLD),
    ("MSF", "MSF Essential Drugs", "MSF Essential drugs: Dolutegravir = DTG oral, Oct 2024.", MSF_DTG),
  ],
  "doses": [
    ("adult", "HIV-1 infection (first- or second-line)", "PO", "1 tablet (TDF 300 mg / 3TC 300 mg / DTG 50 mg)", "Once a day", "Lifelong", "1 tablet/day", "DOST HTA 2021", "With or without food"),
    ("adult", "HIV-1 with rifampicin or other enzyme inducer", "PO", "1 tablet + dolutegravir 50 mg", "TLD once a day; extra DTG about 12 h later", "During inducer and 2 weeks after", "—", "MSF", "Also with efavirenz, carbamazepine (WHOPAR)"),
    ("child", "HIV-1 infection (adolescents ≥30 kg)", "PO", "1 tablet", "Once a day", "Lifelong", "1 tablet/day", "WHOPAR", "Not for children under 30 kg"),
  ],
  "notes": [
    ("renal", "No dose adjustment.", "CrCl 50–80", "WHOPAR"),
    ("renal", "Fixed-dose tablet not recommended; give the components separately with dose adjustment.", "CrCl < 50", "WHOPAR"),
    ("hepatic", "No adjustment in Child-Pugh A or B; use with caution in Child-Pugh C (no dolutegravir data).", "", "WHOPAR"),
    ("elderly", "Use with caution.", "", "WHOPAR"),
    ("pregnancy", "Counsel women of childbearing potential on neural tube defect risk and contraception; pregnancy test before starting if feasible. Folic acid in the first trimester may reduce the risk (MSF). All three components pass into breast milk.", "", "WHOPAR"),
    ("administration", "Missed dose: take if less than 12 hours late, otherwise skip; never double. Vomiting within 1 hour: take another dose.", "", "WHOPAR"),
    ("monitor", "Creatinine clearance before and during therapy; interrupt if confirmed CrCl < 50 mL/min or serum phosphate < 1.0 mg/dL. Test for HBV before starting.", "", "WHOPAR"),
    ("monitor", "Liver enzymes and bilirubin if hypersensitivity is suspected; weight, lipids and glucose; in HBV coinfection, liver tests for at least 6 months after stopping.", "", "WHOPAR"),
    ("forms_ph", "Fixed-dose tablet TDF 300 mg + 3TC 300 mg + DTG 50 mg, holding a monitored-release FDA certificate of product registration; not yet in the PNF at the time of the 2021 HTA review (components listed singly).", "", "DOST HTA 2021"),
  ],
  "checked": [
    (HTA_TLD, "HTAC recommends TLD first-line (treatment-naive adolescents/adults) and second-line (treatment-experienced adults); SOH decision 1 Sep 2021; MR-CPR for the FDC tablet TDF 300/3TC 300/DTG 50; 'Currently, TLD is not listed in the PNF'; components listed singly; AO 2018-0024; one tablet daily lifelong; extra DTG 50 mg with rifampicin; PHP 549 per monthly bottle (same as TLEfv); neuropsychiatric ADEs most common in Zambian study."),
    (WHO_2026, "WHO news 7 Jan 2026: confirms dolutegravir-based regimens as preferred for initial and subsequent HIV treatment; supports reuse of tenofovir and abacavir in subsequent regimens."),
    (WHOPAR, "WHOPAR HA729 part 4 (Oct 2022): ≥30 kg one tablet daily, INSTI-susceptible HIV-1; missed dose 12 h; vomiting 1 h; not for <30 kg; elderly caution; CrCl 50–80 no adjustment, <50 not recommended; Child-Pugh A/B no adjustment, C caution; inducers need DTG 50 mg twice daily via separate DTG; renal interruption CrCl <50 or phosphate <1.0 mg/dL; HBV testing; flare monitoring ≥6 months; weight/metabolic; pancreatitis; etravirine AUC -71%; nevirapine/oxcarbazepine/phenobarbital; sorbitol; cladribine; emtricitabine/adefovir/TAF/didanosine; NTD 0.19% vs 0.11%; breast milk; very common/common ADRs listed."),
    (MSF_DTG, "MSF DTG page (Oct 2024): TLD preferred for adolescents/adults ≥30 kg; adverse effects insomnia, depression, anxiety, dizziness; metformin: monitor glucose and renal function, not exceed 1 g/day; enzyme inducers (rifampicin, carbamazepine, phenytoin, phenobarbital, efavirenz, nevirapine): double the DTG dose and continue 2 weeks after stopping the inducer; folic acid in first trimester may reduce NTD risk."),
    (WHO_FS, "Tenofovir is included in first-line HIV combinations and is active against HBV."),
  ],
}
