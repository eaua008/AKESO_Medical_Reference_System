PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
SMPC_TAB = "https://products.mhra.gov.uk/search/?search=entecavir#emc-213"
SMPC_SOL = "https://products.mhra.gov.uk/search/?search=entecavir#emc-2089"
WHO_FS = "https://www.who.int/news-room/fact-sheets/detail/hepatitis-b"

MED = {
  "id": "med_entecavir",
  "desc_add": "Resistance is rare in nucleoside-naive patients but becomes common after lamivudine resistance (rtM204V/rtL180M substitutions), with cumulative entecavir resistance of about 51% by year 5 in lamivudine-refractory studies, so adding a second antiviral is considered in that setting. WHO lists tenofovir or entecavir as the oral treatments for chronic hepatitis B, and most people who start treatment continue it for life. In the Philippines the PNF lists 0.5 mg and 1 mg tablets and a 0.05 mg/mL oral solution.",
  "facts": {
    "indication": [],
    "adverse": [
      "Insomnia and somnolence (common)",
      "Vomiting, diarrhoea and dyspepsia (common)",
      "Raised transaminases during treatment (common)",
      "Rash and alopecia (uncommon); anaphylactoid reaction (rare)",
      "Neutropenia (very common in paediatric patients)",
    ],
    "contraindication": [
      "Hypersensitivity to entecavir or any excipient (UK SmPC)",
      "Rare hereditary galactose intolerance, Lapp lactase deficiency or glucose-galactose malabsorption (tablets contain lactose)",
    ],
    "interaction": [
      "Not a substrate, inducer or inhibitor of CYP450 enzymes: CYP-mediated interactions are unlikely.",
      "Lamivudine, adefovir or tenofovir: no pharmacokinetic interaction was seen.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.", PNF_URL),
    ("UK SmPC (emc)", "Baraclude 0.5 mg film-coated tablets - Summary of Product Characteristics. Bristol-Myers Squibb Pharma EEIG. Electronic medicines compendium (emc), updated May 2021.", SMPC_TAB),
    ("UK SmPC (emc)", "Baraclude 0.05 mg/ml oral solution - Summary of Product Characteristics. Bristol-Myers Squibb. Electronic medicines compendium (emc), updated May 2021.", SMPC_SOL),
    ("WHO", "World Health Organization. Hepatitis B fact sheet. Geneva: WHO; 2026.", WHO_FS),
  ],
  "links": [
    ("hiv_infection", "caution", "Not used for HBV in HIV/HBV coinfection unless on fully suppressive antiretroviral therapy (risk of HIV resistance)."),
    ("chronic_kidney_disease", "caution", "Renally cleared: dose reduced or interval extended when CrCl < 50 mL/min, including dialysis."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Baraclude 0.5 mg film-coated tablets - SmPC. Bristol-Myers Squibb Pharma EEIG, 2021.", SMPC_TAB),
    ("Label · UK SmPC (soln)", "UK SmPC (emc)", "Baraclude 0.05 mg/ml oral solution - SmPC. Bristol-Myers Squibb, 2021.", SMPC_SOL),
    ("PNF", "Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.", PNF_URL),
  ],
  "doses": [
    ("adult", "Chronic hepatitis B, nucleoside-naive, compensated", "PO", "0.5 mg", "Once a day", "Long term (see stopping rules)", "—", "Label · UK SmPC", "With or without food"),
    ("adult", "Lamivudine-refractory chronic hepatitis B", "PO", "1 mg", "Once a day", "Long term", "—", "Label · UK SmPC", "Empty stomach (>2 h before and after a meal)"),
    ("adult", "Decompensated liver disease", "PO", "1 mg", "Once a day", "Do not stop", "—", "Label · UK SmPC", "Empty stomach; stopping not advised in decompensated disease or cirrhosis"),
    ("child", "Chronic hepatitis B, nucleoside-naive, 2–<18 y, ≥32.6 kg", "PO", "0.5 mg (1 tablet or 10 mL solution)", "Once a day", "Long term", "—", "Label · UK SmPC", ""),
    ("child", "Chronic hepatitis B, nucleoside-naive, 2–<18 y, 10–32.5 kg", "PO", "4–9.5 mL of 0.05 mg/mL solution by weight band", "Once a day", "Long term", "10 mL", "Label · UK SmPC (soln)", "10–14.1 kg 4 mL; 20.9–22.5 kg 6.5 mL; 30.9–32.5 kg 9.5 mL (0.5 mL steps per band)"),
  ],
  "notes": [
    ("renal", "Naive: 0.25 mg once a day or 0.5 mg every 48 h. Lamivudine-refractory/decompensated: 0.5 mg once a day.", "CrCl 30–49", "Label · UK SmPC"),
    ("renal", "Naive: 0.15 mg once a day or 0.5 mg every 72 h. Lamivudine-refractory/decompensated: 0.3 mg once a day or 0.5 mg every 48 h.", "CrCl 10–29", "Label · UK SmPC"),
    ("renal", "Naive: 0.05 mg once a day or 0.5 mg every 5–7 days. Lamivudine-refractory/decompensated: 0.1 mg once a day or 0.5 mg every 72 h. Doses extrapolated from limited data: monitor virological response closely.", "CrCl <10, HD, CAPD", "Label · UK SmPC"),
    ("hepatic", "No dose adjustment in hepatic impairment; serious hepatic events are more frequent in decompensated (Child-Pugh C) disease.", "", "Label · UK SmPC"),
    ("elderly", "No age-based adjustment; dose by renal function.", "", "Label · UK SmPC"),
    ("pregnancy", "Not recommended in pregnancy unless clearly necessary; women of childbearing potential use effective contraception. Breastfeeding should stop during treatment.", "", "Label · UK SmPC"),
    ("monitor", "HBV DNA and ALT during treatment; liver function for at least 6 months after stopping (risk of flare); renal function, especially with cyclosporine or tacrolimus after liver transplant.", "", "Label · UK SmPC"),
    ("administration", "Duration: HBeAg-positive, at least 12 months after HBe seroconversion (or until HBs seroconversion/loss of efficacy); HBeAg-negative, at least until HBs seroconversion or loss of efficacy.", "", "Label · UK SmPC"),
    ("forms_ph", "500 mcg and 1 mg tablet/film-coated tablet; 0.05 mg/mL oral solution.", "", "PNF"),
  ],
  "checked": [
    (PNF_URL, "Entecavir: oral 500 mcg and 1 mg tablet/film-coated tablet; 0.05 mg/mL oral solution."),
    (SMPC_TAB, "Baraclude 0.5 mg SmPC: adult doses (0.5 mg naive with/without food; 1 mg lamivudine-refractory and decompensated on empty stomach), stopping rules, ≥32.6 kg child dose, renal table incl. lamivudine-refractory/decompensated column, hepatic/elderly, contraindication, lactose, resistance ~51% at year 5, rtM204V/rtL180M, CYP450 and lamivudine/adefovir/tenofovir interactions, pregnancy/breastfeeding, adverse reactions incl. insomnia, somnolence, dyspepsia, rash, alopecia, anaphylactoid, paediatric neutropenia, monitoring LFT ≥6 months after stopping, transplant renal monitoring, HIV coinfection."),
    (SMPC_SOL, "Baraclude 0.05 mg/ml oral solution: paediatric weight-band table 10.0–14.1 kg 4.0 mL up to ≥32.6 kg 10.0 mL; minimum age 2 years."),
    (WHO_FS, "Chronic hepatitis B can be treated with oral tenofovir or entecavir; most who start treatment continue for life."),
  ],
}
