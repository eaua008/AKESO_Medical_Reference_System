PREP_URL = "https://hivpreventioncoalition.unaids.org/sites/default/files/attachments/interim_guidelines_on_pre-exposure_prophylaxis_prep.pdf"
HTA_PREP = "https://hta.dost.gov.ph/wp-content/uploads/2024/02/ES_Oral-PrEP-for-HIV_as-of-Nov-2021.docx-1.pdf"
WHO_MTCT = "https://www.who.int/news-room/questions-and-answers/item/hepatitis-preventing-mother-to-child-transmission-of-the-hepatitis-b-virus"
WHO_FS = "https://www.who.int/news-room/fact-sheets/detail/hepatitis-B"
MSF_TDF = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/tenofovir-disoproxil-fumarate-tdf-oral-38537560.html"
SMPC = "https://products.mhra.gov.uk/search/?search=tenofovir#emc-1615"
DM = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=33fd6418-fbdc-42ca-a50d-ce2a476a5418"

MED = {
  "id": "med_tenofovir",
  "desc_add": "In the Philippines, tenofovir disoproxil combined with emtricitabine is the drug used for oral HIV pre-exposure prophylaxis under the DOH interim PrEP guidelines (2021), taken daily by anyone at substantial risk or event-driven (2-1-1) by men who have sex with men. WHO recommends tenofovir prophylaxis from the 28th week of pregnancy for HBsAg-positive women with HBV DNA of 200,000 IU/mL or more to prevent mother-to-child transmission of hepatitis B.",
  "facts": {
    "indication": [
      "Chronic hepatitis B with decompensated liver disease or lamivudine-resistant HBV in adults (UK SmPC)",
      "Event-driven (2-1-1) oral PrEP with emtricitabine for men who have sex with men (DOH interim PrEP guidelines, 2021)",
    ],
    "adverse": [
      "Dizziness",
      "Mild serum creatinine rises in PrEP users (mostly grade 1; renal events more frequent than with placebo)",
    ],
    "contraindication": [
      "Hypersensitivity to tenofovir disoproxil or any excipient (UK SmPC)",
      "PrEP is not started in people who are HIV-positive, have signs of acute retroviral syndrome, weigh under 35 kg or have CrCl of 60 mL/min or less (DOH)",
      "Use in children with renal impairment is not recommended (UK SmPC)",
    ],
    "interaction": [
      "Other tenofovir disoproxil or tenofovir alafenamide products and adefovir dipivoxil: not co-administered.",
      "Tacrolimus: monitor renal function during co-administration.",
      "Amphotericin B and pentamidine: nephrotoxic; avoid or monitor renal function (MSF).",
      "Clarithromycin: may raise tenofovir levels; use with caution and close monitoring (MSF).",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("DOH interim PrEP guidelines", "Department of Health, Philippines. Department Memorandum: Interim Guidelines on Pre-Exposure Prophylaxis (PrEP) for the Prevention of HIV Infection in the Philippines. 4 January 2021.", PREP_URL),
    ("DOST HTA Philippines", "Health Technology Assessment Council (DOST-PCHRD / DOH). Evidence summary: Emtricitabine/tenofovir disoproxil fumarate oral PrEP for HIV. Approved by the Secretary of Health 18 January 2022.", HTA_PREP),
    ("World Health Organization", "World Health Organization. Hepatitis: Preventing mother-to-child transmission of the hepatitis B virus. Questions and answers.", WHO_MTCT),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs - practical guidelines: Tenofovir disoproxil fumarate = TDF oral. Updated April 2026.", MSF_TDF),
    ("UK SmPC (emc)", "Viread 245 mg film-coated tablets - Summary of Product Characteristics. Gilead Sciences Ltd. Electronic medicines compendium (emc), updated 15 March 2024.", SMPC),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "Dosing interval is lengthened when CrCl is below 50 mL/min and renal function is monitored; MSF prefers entecavir for hepatitis B in renal impairment (UK SmPC, MSF)."),
  ],
  "sources": [
    ("DOH PrEP 2021", "DOH interim PrEP guidelines", "DOH Philippines. Interim Guidelines on Pre-Exposure Prophylaxis (PrEP) for the Prevention of HIV Infection in the Philippines, 4 January 2021.", PREP_URL),
    ("WHO", "World Health Organization", "WHO. Hepatitis: Preventing mother-to-child transmission of the hepatitis B virus (Q&A).", WHO_MTCT),
    ("MSF", "MSF Essential Drugs", "MSF Essential drugs: Tenofovir disoproxil fumarate = TDF oral, 2026.", MSF_TDF),
    ("Label · UK SmPC", "UK SmPC (emc)", "Viread 245 mg film-coated tablets SmPC, Gilead Sciences Ltd, updated 15 March 2024.", SMPC),
    ("Label · US FDA", "DailyMed (FDA label)", "VIREAD (tenofovir disoproxil fumarate) tablets and oral powder, Gilead Sciences. DailyMed.", DM),
  ],
  "doses": [
    ("adult", "HIV-1 infection (with other ARVs)", "PO", "300 mg", "Once a day", "Long-term", "300 mg/day", "Label · US FDA", "Same dose for chronic hepatitis B"),
    ("adult", "Chronic hepatitis B", "PO", "300 mg", "Once a day", "Usually long-term", "300 mg/day", "MSF", "HBeAg+: at least 12 months after HBe seroconversion (UK SmPC)"),
    ("adult", "HBV mother-to-child prevention (pregnancy)", "PO", "300 mg", "Once a day", "From week 28 until at least birth", "—", "WHO", "If HBV DNA ≥200,000 IU/mL (or HBeAg+)"),
    ("adult", "HIV PrEP, daily (with emtricitabine)", "PO", "1 TDF/FTC tablet", "Once a day", "While at risk; 28 days after last exposure", "2 tablets/day", "DOH PrEP 2021", "Protection after 5–7 days (anal) or 20 days (vaginal)"),
    ("adult", "HIV PrEP, event-driven (MSM only)", "PO", "2 tablets, then 1, then 1", "2–24 h before sex, then 24 h and 48 h after first dose", "Until 2 days after last sex", "2 tablets/day", "DOH PrEP 2021", "TDF/FTC tablets"),
    ("child", "HIV-1 or chronic hepatitis B (≥2 years, ≥10 kg)", "PO", "8 mg/kg", "Once a day", "Long-term", "300 mg/day", "Label · US FDA", "Tablets ≥17 kg: 150 mg (17–<22 kg), 200 mg (22–<28 kg), 250 mg (28–<35 kg)"),
    ("child", "HIV-1 or chronic hepatitis B (12 years and older, ≥35 kg)", "PO", "300 mg", "Once a day", "Long-term", "300 mg/day", "MSF", ""),
  ],
  "notes": [
    ("renal", "Once-daily dosing supported by limited data.", "CrCl 50–80", "Label · UK SmPC"),
    ("renal", "300 mg every 48 hours.", "CrCl 30–49", "MSF"),
    ("renal", "300 mg every 72–96 hours; below CrCl 10 seek specialist advice. MSF prefers entecavir for hepatitis B in renal impairment.", "CrCl 10–29", "MSF"),
    ("renal", "Every 7 days, after a dialysis session.", "Haemodialysis", "Label · UK SmPC"),
    ("hepatic", "No dose adjustment.", "", "Label · UK SmPC"),
    ("elderly", "No data in people over 65; use with caution because renal function is often reduced.", "", "Label · UK SmPC"),
    ("pregnancy", "More than 1,000 pregnancy outcomes show no malformations or fetal/neonatal toxicity. Women with HBV may breastfeed; women living with HIV follow national breastfeeding advice.", "", "Label · UK SmPC"),
    ("administration", "Missed dose: take within 12 hours, otherwise skip. Vomiting within 1 hour: take another dose. The UK label advises taking it with food; the oral powder is always given with food.", "", "Label · UK SmPC"),
    ("monitor", "Creatinine clearance and serum phosphate before starting, after 2–4 weeks, after 3 months, then every 3–6 months if there are no renal risk factors.", "", "Label · UK SmPC"),
    ("monitor", "PrEP: HIV test within 7 days before starting, after 1 month, then at least every 3 months; HBsAg at baseline; serum creatinine every 6 months; stop PrEP if CrCl falls below 60 mL/min.", "", "DOH PrEP 2021"),
  ],
  "checked": [
    (PREP_URL, "DOH Department Memorandum dated 4 Jan 2021 (number illegible): daily TDF/FTC once daily, max 2 tablets/day; event-driven for MSM (2 pills 2–24 h before sex, 1 at 24 h, 1 at 48 h); lead-in 5–7 days anal / 20 days vaginal; eligibility HIV-negative, no acute retroviral syndrome, ≥35 kg, CrCl >60; HIV test within 7 days, HBsAg, creatinine; follow-up HIV test at 1 month then every 3 months, creatinine every 6 months, stop if CrCl <60; stop 28 days after last exposure (non-MSM)."),
    (HTA_PREP, "DOST HTA evidence summary for TDF/FTC oral PrEP, approved by SOH 18 Jan 2022; renal adverse events more frequent than placebo (RR 1.54), mostly grade-1 creatinine elevations."),
    (WHO_MTCT, "Tenofovir prophylaxis for HBsAg-positive pregnant women with HBV DNA ≥5.3 log10 IU/mL (≥200,000 IU/mL); HBeAg as alternative where DNA testing unavailable; from week 28 until at least birth; TDF safe."),
    (WHO_FS, "WHO hepatitis B fact sheet (28 July 2026): tenofovir in first-line HIV combinations and active against HBV; most need lifelong treatment. Used for verification only."),
    (MSF_TDF, "MSF TDF page (updated Apr 2026): 300 mg once daily ≥12 years and adults; renal 300 mg every 48 h (CrCl 30–49), every 72–96 h (10–29), specialist advice <10; entecavir preferred in renal impairment; dizziness among adverse effects; avoid/monitor with aminoglycosides, amphotericin B, pentamidine, NSAIDs; caution with clarithromycin; PMTCT from second trimester until infant vaccination complete."),
    (SMPC, "Viread SmPC (15 Mar 2024): indications incl. decompensated and lamivudine-resistant HBV; with food; missed dose 12 h rule; vomiting within 1 h; renal bands incl. CrCl 50–80 and HD every 7 days; no hepatic adjustment; elderly caution; not recommended in paediatric renal impairment; HBV duration; contraindication hypersensitivity; do not combine with other TDF/TAF/adefovir; tacrolimus monitoring; pregnancy >1,000 outcomes; breastfeeding; renal monitoring at 2–4 weeks, 3 months, then every 3–6 months."),
    (DM, "US label: 8 mg/kg once daily up to 300 mg for ≥2 years; tablets 150/200/250/300 mg by weight bands 17–<22, 22–<28, 28–<35, ≥35 kg; oral powder from 10 kg; same dose for HIV and HBV."),
  ],
}
