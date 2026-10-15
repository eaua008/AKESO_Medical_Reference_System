PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
S200_URL = "https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1327"
S100_URL = "https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1326"
DM_URL = "https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6b78d08a-e098-4188-8f7f-94fbd5f396ef"

MED = {
  "id": "med_budesonide_formoterol",
  "desc_add": "UK labeling licenses the dry-powder inhaler for three asthma regimens: maintenance only, maintenance-and-reliever (12 years and older), and reliever-only in mild asthma (12 years and older). Strengths may be stated as metered dose (e.g. 200/6 mcg) or delivered dose (160/4.5 mcg); these are the same product. In the Philippines the PNF lists both a dry-powder inhaler and a metered-dose inhaler.",
  "facts": {
    "indication": [],
    "adverse": [
      "Throat irritation, cough and hoarseness",
      "Anxiety, sleep disorders, aggression and psychomotor hyperactivity (uncommon)",
      "Dizziness, nausea, blurred vision (uncommon)",
      "Bruising and muscle cramps (uncommon)",
      "Paradoxical bronchospasm (very rare; stop and use a rapid-acting bronchodilator)",
      "Growth retardation in children (very rare)",
      "QTc prolongation, cardiac arrhythmias, angina (rare to very rare)",
      "Taste disturbance, depression and behavioural changes (very rare)",
    ],
    "contraindication": [
      "Turbohaler: hypersensitivity to lactose (contains small amounts of milk proteins)",
    ],
    "interaction": [
      "QT-prolonging drugs (e.g., quinidine, disopyramide, phenothiazines): increased risk of ventricular arrhythmias.",
      "Xanthines (e.g., theophylline) and systemic corticosteroids: additive hypokalaemia.",
      "Digitalis glycosides: hypokalaemia raises the risk of arrhythmias.",
      "Halogenated hydrocarbon anaesthetics: increased arrhythmia risk.",
      "L-dopa, L-thyroxine, oxytocin and alcohol: may impair cardiac tolerance to beta-2 agonists.",
      "Strong CYP3A4 inhibitors: maintenance-and-reliever therapy is not recommended with them.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Symbicort Turbohaler 200/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd; updated March 2023. electronic medicines compendium (emc).", S200_URL),
    ("UK SmPC (emc)", "Symbicort Turbohaler 100/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd. electronic medicines compendium (emc).", S100_URL),
    ("PhilHealth / DOH (PNF-EML)", "Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.", PNF_URL),
  ],
  "links": [
    ("tuberculosis", "caution", "Re-evaluate use in active or quiescent pulmonary TB (UK SmPC)."),
    ("type2_diabetes", "caution", "Beta-2 agonist can raise glucose; consider extra blood glucose checks (UK SmPC)."),
    ("graves_disease", "caution", "Use with caution in thyrotoxicosis (UK SmPC)."),
    ("hypertension", "caution", "Use with caution in severe hypertension (UK SmPC)."),
    ("heart_failure", "caution", "Use with caution in severe heart failure or tachyarrhythmias (UK SmPC)."),
    ("acute_coronary_syndrome", "caution", "Use with caution in ischaemic heart disease (UK SmPC)."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Symbicort Turbohaler 200/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd; March 2023.", S200_URL),
    ("Label · UK SmPC 100/6", "UK SmPC (emc)", "Symbicort Turbohaler 100/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd.", S100_URL),
    ("Label · US", "DailyMed (FDA label)", "SYMBICORT (budesonide and formoterol fumarate dihydrate) inhalation aerosol. Prescribing information. AstraZeneca; revised 10/2024.", DM_URL),
    ("PNF", "Philippine National Formulary – EML", "Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.", PNF_URL),
  ],
  "doses": [
    ("adult", "Asthma, maintenance (DPI 160/4.5)", "Inhaled", "1–2 inhalations", "2× a day", "Long-term", "4 inhalations 2× a day", "Label · UK SmPC", "Separate reliever for rescue; UK labels this as 200/6 (metered)"),
    ("adult", "Asthma, maintenance-and-reliever (DPI 160/4.5)", "Inhaled", "2 inhalations/day + 1 as needed", "Once or 2× a day + as needed", "Long-term", "6 per occasion; 12/day short-term", "Label · UK SmPC", ">8 inhalations/day: reassess"),
    ("adult", "Mild asthma, reliever only (DPI 160/4.5)", "Inhaled", "1 inhalation", "As needed", "—", "6 per occasion; 12/day short-term", "Label · UK SmPC", "Repeat once if still symptomatic after a few minutes"),
    ("adult", "Asthma, maintenance (pMDI 80/4.5 or 160/4.5)", "Inhaled", "2 inhalations", "2× a day", "Long-term", "160/4.5 strength", "Label · US", "Strength by severity and prior ICS"),
    ("adult", "COPD (160/4.5)", "Inhaled", "2 inhalations", "2× a day", "Long-term", "—", "Label · UK SmPC", ""),
    ("child", "Asthma, maintenance, 12–17 y (DPI)", "Inhaled", "1–2 inhalations", "2× a day", "Long-term", "—", "Label · UK SmPC", "80/4.5 or 160/4.5"),
    ("child", "Asthma, maintenance-and-reliever, 12–17 y (DPI 80/4.5)", "Inhaled", "2 inhalations/day + 1 as needed", "Once or 2× a day + as needed", "Long-term", "6 per occasion; 12/day short-term", "Label · UK SmPC 100/6", ">8 inhalations/day: reassess"),
    ("child", "Asthma, maintenance, 6–11 y (DPI 80/4.5)", "Inhaled", "1–2 inhalations", "2× a day", "Long-term", "—", "Label · UK SmPC 100/6", "Not recommended <6 y"),
    ("child", "Asthma, maintenance-and-reliever, 6–11 y (DPI 80/4.5)", "Inhaled", "1 inhalation + 1 as needed", "Once or 2× a day + as needed", "Long-term", "4 per occasion; 8/day short-term", "Label · UK SmPC 100/6", ">4 inhalations/day: reassess"),
    ("child", "Asthma, maintenance, 6–11 y (pMDI 80/4.5)", "Inhaled", "2 inhalations", "2× a day", "Long-term", "—", "Label · US", ""),
  ],
  "notes": [
    ("renal", "No data available in renal impairment.", "", "Label · UK SmPC"),
    ("hepatic", "No data; exposure may rise in severe liver cirrhosis because both drugs are cleared mainly by the liver. Monitor closely.", "", "Label · UK SmPC"),
    ("elderly", "No special dosing requirements.", "", "Label · UK SmPC"),
    ("pregnancy", "Use only if benefit outweighs risk, at the lowest effective budesonide dose; ~2,000 pregnancies with inhaled budesonide showed no rise in malformations; formoterol data inadequate. Budesonide passes into breast milk; no infant effects expected at therapeutic doses.", "", "Label · UK SmPC"),
    ("administration", "Turbohaler: breathe in forcefully and deeply through the mouthpiece; never breathe out into it; replace cover. Patients may not taste the dose.", "", "Label · UK SmPC 100/6"),
    ("administration", "pMDI: shake for 5 seconds before each spray; spray 2 test puffs before first use or if dropped or unused >7 days; take doses about 12 h apart.", "", "Label · US"),
    ("administration", "Do not stop abruptly; taper the maintenance dose. Do not start during an exacerbation.", "", "Label · UK SmPC"),
    ("forms_ph", "DPI 80/4.5 mcg, 160/4.5 mcg and 320/9 mcg × 60 doses; MDI 80/4.5 mcg and 160/4.5 mcg × 120 doses.", "", "PNF"),
    ("monitor", "Track reliever use: rising use or >8 inhalations/day (adults) means poor control; reassess.", "", "Label · UK SmPC"),
    ("monitor", "Check height regularly in children on long-term treatment.", "", "Label · UK SmPC"),
    ("monitor", "Check serum potassium in acute severe asthma; check blood glucose in diabetes.", "", "Label · UK SmPC"),
    ("monitor", "Check adrenal function when switching from oral steroids; watch for pneumonia in COPD.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (PNF_URL, "Budesonide + Formoterol inhalation: DPI 80/4.5, 160/4.5 (fumarate dihydrate) x 60 doses, 320/9 x 60 doses; MDI 80/4.5 and 160/4.5 x 120 doses; no restriction."),
    (S200_URL, "Symbicort Turbohaler 200/6 SmPC (AstraZeneca, 22 Mar 2023): delivered dose 160/4.5 = 200/6 metered; Therapy A adults 1–2 inh BD up to 4 BD, adolescents 1–2 BD; Therapy B 2 inh/day + 1 as needed, max 6/occasion, >8/day not normally needed, up to 12/day limited period; Therapy C mild asthma 1 as needed; COPD 2 inh BD; renal/hepatic no data, severe cirrhosis exposure; elderly none; pregnancy ~2000; breast milk; ADR table (throat irritation, cough, hoarseness, anxiety, aggression, sleep disorders, dizziness, blurred vision, nausea, bruising, muscle cramps, paradoxical bronchospasm, growth retardation, QTc, taste, depression, angina); interactions (QT drugs, xanthines/corticosteroids, digitalis, halogenated anaesthetics, L-dopa/L-thyroxine/oxytocin/alcohol, MART not recommended with strong CYP3A4 inhibitors); 4.3 lactose/milk proteins; 4.4 thyrotoxicosis, severe hypertension, ischaemic heart disease, severe heart failure, diabetes glucose, TB, potassium in acute severe asthma, height in children, adrenal function, pneumonia in COPD, taper."),
    (S100_URL, "Symbicort Turbohaler 100/6 SmPC: delivered 80/4.5; maintenance 6–11 y and 12–17 y 1–2 inh BD; MART 6–11 y 1 inh once/twice daily + as needed, max 4/occasion, >4/day not normally needed, up to 8/day; adolescents MART max 6/occasion, 8/day (12 short-term); not recommended <6 y; Turbohaler technique, rinse mouth."),
    (DM_URL, "Symbicort US label (rev 10/2024): 6 to <12 y 2 inh of 80/4.5 BD; ≥12 y 2 inh 80/4.5 or 160/4.5 BD by severity; COPD 160/4.5 2 inh BD; max 160/4.5; shake 5 s, 2 test sprays, re-prime if dropped or >7 days; ~12 h apart; hepatic disease monitor closely."),
  ],
}
