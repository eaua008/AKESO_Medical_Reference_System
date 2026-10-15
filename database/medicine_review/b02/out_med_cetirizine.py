PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
TAB_URL = "https://products.mhra.gov.uk/search/?search=cetirizine#emc-12956"
SOL_URL = "https://products.mhra.gov.uk/search/?search=cetirizine#emc-6752"

MED = {
  "id": "med_cetirizine",
  "desc_add": "In the Philippines it is listed in the PNF as a 10 mg tablet and as several liquid forms (syrup, oral drops and solution) for children. UK labeling doses children aged 2–12 years twice daily, and bases renal dose reduction on eGFR, with use contraindicated below 15 mL/min.",
  "facts": {
    "indication": [],
    "adverse": [
      "Diarrhoea, rhinitis and fatigue in children",
      "Agitation, paraesthesia, pruritus, rash, asthenia (uncommon)",
      "Aggression, confusion, depression, hallucinations, insomnia (rare)",
      "Convulsions and tachycardia (rare)",
      "Abnormal liver function tests (rare); hepatitis",
      "Urinary retention",
      "Weight increase and increased appetite",
      "Angioedema, fixed drug eruption, AGEP (very rare to not known)",
      "Tics, dystonia, oculogyric crisis, blurred vision (very rare)",
      "Pruritus and/or urticaria after stopping treatment",
    ],
    "contraindication": [
      "Hypersensitivity to any piperazine derivative",
      "End-stage renal disease (eGFR <15 mL/min)",
    ],
    "interaction": [
      "Pseudoephedrine and theophylline (400 mg/day): no clinically significant interaction found.",
      "Food: slows the rate but not the extent of absorption.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Cetirizine hydrochloride 10 mg film-coated tablets. Summary of Product Characteristics. Milpharm Ltd (Aurobindo); updated February 2024. electronic medicines compendium (emc).", TAB_URL),
    ("UK SmPC (emc)", "Zirtek Allergy Solution 1 mg/ml oral solution. Summary of Product Characteristics. UCB Pharma Ltd; updated October 2023. electronic medicines compendium (emc).", SOL_URL),
    ("PhilHealth / DOH (PNF-EML)", "Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.", PNF_URL),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "Reduce dose by eGFR; contraindicated below 15 mL/min (UK SmPC)."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Cetirizine hydrochloride 10 mg film-coated tablets. Summary of Product Characteristics. Milpharm Ltd; February 2024.", TAB_URL),
    ("Label · UK SmPC sol", "UK SmPC (emc)", "Zirtek Allergy Solution 1 mg/ml oral solution. Summary of Product Characteristics. UCB Pharma Ltd; October 2023.", SOL_URL),
    ("PNF", "Philippine National Formulary – EML", "Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.", PNF_URL),
  ],
  "doses": [
    ("adult", "Allergic rhinitis, chronic urticaria", "PO", "10 mg", "Once a day", "—", "—", "Label · UK SmPC", "Also adolescents >12 y"),
    ("child", "Allergic rhinitis, urticaria (6–12 y)", "PO", "5 mg", "2× a day", "—", "—", "Label · UK SmPC", "½ tablet or 5 mL of 1 mg/mL solution"),
    ("child", "Allergic rhinitis, urticaria (2–6 y)", "PO", "2.5 mg", "2× a day", "—", "—", "Label · UK SmPC sol", "2.5 mL of 1 mg/mL solution; tablets not suitable <6 y"),
  ],
  "notes": [
    ("renal", "10 mg once a day (no change).", "eGFR ≥60", "Label · UK SmPC"),
    ("renal", "5 mg once a day.", "eGFR 30–59", "Label · UK SmPC"),
    ("renal", "5 mg once every 2 days.", "eGFR 15–29", "Label · UK SmPC"),
    ("renal", "Contraindicated.", "eGFR <15", "Label · UK SmPC"),
    ("hepatic", "No adjustment for hepatic impairment alone; adjust if renal impairment is also present.", "", "Label · UK SmPC"),
    ("elderly", "No dose reduction if renal function is normal.", "", "Label · UK SmPC"),
    ("pregnancy", "Prospective data show no excess maternal or fetal toxicity, but prescribe with caution. Passes into breast milk (25–90% of plasma levels); use with caution.", "", "Label · UK SmPC"),
    ("administration", "Stop at least 3 days before allergy skin testing (antihistamines suppress results).", "", "Label · UK SmPC"),
    ("forms_ph", "Tablet 10 mg; syrup (oral drops) 2.5 mg/mL, 10 mL; drops 10 mg/mL, 10 mL; solution 1 mg/mL, 30 mL and 60 mL; syrup 5 mg/5 mL, 30 mL.", "", "PNF"),
    ("monitor", "Ask about urinary retention in men with prostatic hyperplasia or spinal cord lesions; use caution in epilepsy.", "", "Label · UK SmPC"),
    ("monitor", "Advise against driving if drowsy; warn that itching or hives may flare on stopping.", "", "Label · UK SmPC"),
    ("monitor", "Overdose (≥5× daily dose): sedation, confusion, mydriasis, tachycardia, urinary retention; supportive care only, not removed by haemodialysis.", "", "Label · UK SmPC sol"),
  ],
  "checked": [
    (PNF_URL, "Cetirizine (as dihydrochloride) Oral: 10 mg tablet; 2.5 mg/mL syrup (oral drops) 10 mL; 10 mg/mL drops 10 mL; 1 mg/mL solution 30 and 60 mL; 5 mg/5 mL syrup 30 mL; no restriction."),
    (TAB_URL, "Cetirizine 10 mg tablets SmPC (Milpharm/Aurobindo, Feb 2024): adults/adolescents >12 y 10 mg OD; 6–12 y 5 mg BD; not for <6 y; elderly no reduction with normal renal function; hepatic alone no adjustment; eGFR table (≥60 10 mg, 30–<60 5 mg OD, 15–<30 5 mg every 2 days, <15 contraindicated); hypersensitivity to piperazine derivatives; urinary retention, epilepsy cautions; 3-day washout before skin tests; pruritus/urticaria on discontinuation; no interaction with pseudoephedrine/theophylline; food slows rate; paediatric ADRs diarrhoea, rhinitis, fatigue; rare LFT abnormalities, convulsions; hepatitis; pregnancy caution; breast milk 25–90%; driving."),
    (SOL_URL, "Zirtek Allergy Solution 1 mg/ml SmPC (UCB, Oct 2023): 2–6 y 2.5 mg BD, 6–12 y 5 mg BD, adults 10 mg OD; post-marketing ADRs (aggression, confusion, depression, hallucinations, insomnia, convulsions, tachycardia, weight increase, tics, dystonia, oculogyric crisis, blurred vision, angioedema, fixed drug eruption, AGEP, urinary retention, increased appetite, agitation, paraesthesia); overdose symptoms; haemodialysis ineffective."),
  ],
}
