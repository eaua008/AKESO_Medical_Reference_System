UK_URL = "https://products.mhra.gov.uk/search/?search=vancomycin#emc-15736"
US_URL = "https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=0543b2b5-b1c7-4ad6-b38c-3be0086f0e06&type=display"

MED = {
  "id": "med_vancomycin",
  "desc_add": "UK labeling also licenses IV vancomycin for complicated skin and soft tissue infections, bone and joint infections, community- and hospital-acquired pneumonia, infective endocarditis and surgical prophylaxis in patients at high risk of endocarditis. The first IV dose is based on total body weight (a 25–30 mg/kg loading dose may be used in seriously ill patients), and later doses are guided by serum levels and kidney function. IV vancomycin is not effective for C. difficile infection, and it must never be given intramuscularly.",
  "facts": {
    "indication": [
      "Complicated skin and soft tissue infections and bone and joint infections (IV)",
      "Community-acquired and hospital-acquired pneumonia, including ventilator-associated pneumonia (IV)",
      "Perioperative prophylaxis in patients at high risk of bacterial endocarditis undergoing major surgery (IV)",
    ],
    "adverse": [
      "Severe skin reactions: SJS, TEN, DRESS, AGEP, linear IgA bullous dermatosis (stop at first signs; never restart)",
      "Hypotension, shock and rarely cardiac arrest with rapid bolus infusion",
      "Raised ALT and AST (common)",
      "Interstitial nephritis and acute renal failure (rare)",
      "Drug fever, shivering, pain and muscle spasm of chest and back (rare)",
      "Kounis syndrome (allergic acute coronary syndrome)",
      "Haemorrhagic occlusive retinal vasculitis after intracameral or intravitreal use (not an approved route)",
    ],
    "contraindication": [
      "Intramuscular injection (risk of necrosis at the injection site)",
      "Previous severe skin reaction (SJS, TEN, DRESS, AGEP) to vancomycin: must not be restarted",
    ],
    "interaction": [
      "Anaesthetic agents: more erythema, histamine-like flushing and anaphylactoid reactions; infuse vancomycin over 60 minutes before induction.",
      "Bacitracin, polymyxin B, colistin and viomycin: additive kidney or ear toxicity; monitor closely.",
      "Oral use for C. difficile: stop anti-motility agents and reconsider proton pump inhibitors.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Vancomycin 500 mg powder for concentrate for solution for infusion. Summary of Product Characteristics. hameln pharma ltd; text revised 19 Jan 2026. electronic medicines compendium (emc).", UK_URL),
    ("DailyMed (FDA label)", "Vancomycin Hydrochloride for Injection, USP. Prescribing information. Glenmark Pharmaceuticals Inc.; revised 12/2025. DailyMed, U.S. National Library of Medicine.", US_URL),
  ],
  "links": [
    ("community_acquired_pneumonia", "safe", "Licensed IV indication, including MRSA; typical course 7–14 days (UK SmPC)."),
    ("chronic_kidney_disease", "caution", "Nephrotoxic and renally cleared: give the usual loading dose, then extend the interval and dose by serum levels (UK SmPC)."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Vancomycin 500 mg powder for concentrate for solution for infusion. Summary of Product Characteristics. hameln pharma ltd; January 2026.", UK_URL),
    ("Label · US", "DailyMed (FDA label)", "Vancomycin Hydrochloride for Injection, USP. Prescribing information. Glenmark Pharmaceuticals Inc.; revised 12/2025.", US_URL),
  ],
  "doses": [
    ("adult", "Serious infections (incl. ≥12 y)", "IV", "15–20 mg/kg", "Every 8–12 h", "By infection", "2 g per dose", "Label · UK SmPC", "Initial dose by total body weight; adjust by levels"),
    ("adult", "Loading dose, seriously ill", "IV", "25–30 mg/kg", "Once", "—", "—", "Label · UK SmPC", "Do not reduce in renal insufficiency"),
    ("adult", "Serious infections (fixed dose)", "IV", "500 mg or 1 g", "Every 6 h or every 12 h", "By infection", "2 g/day", "Label · US", "Normal renal function"),
    ("adult", "Surgical prophylaxis, high endocarditis risk", "IV", "15 mg/kg", "Once, before induction", "—", "—", "Label · UK SmPC", "Second dose may be needed for long surgery"),
    ("adult", "C. difficile, first non-severe episode", "PO", "125 mg", "Every 6 h", "10 days", "2 g/day", "Label · UK SmPC", ""),
    ("adult", "C. difficile, severe or complicated", "PO", "500 mg", "Every 6 h", "10 days", "2 g/day", "Label · UK SmPC", ""),
    ("adult", "C. difficile, multiple recurrences", "PO", "125 mg, then taper or pulse", "4× a day", "10 days, then ≥3 weeks", "—", "Label · UK SmPC", "Taper to 125 mg/day or 125–500 mg every 2–3 days"),
    ("child", "Serious infections, 1 month–<12 y", "IV", "10–15 mg/kg", "Every 6 h", "By infection", "60 mg/kg/day usually", "Label · UK SmPC", "Standard doses may give low levels; monitor"),
    ("child", "Surgical prophylaxis, high endocarditis risk", "IV", "15 mg/kg", "Once, before induction", "—", "—", "Label · UK SmPC", ""),
    ("child", "C. difficile, <12 y", "PO", "10 mg/kg", "Every 6 h", "10 days", "2 g/day", "Label · UK SmPC", ""),
    ("neonate", "Serious infections, PMA <29 weeks", "IV", "15 mg/kg", "Every 24 h", "By infection", "—", "Label · UK SmPC", "Seek neonatal specialist advice"),
    ("neonate", "Serious infections, PMA 29–35 weeks", "IV", "15 mg/kg", "Every 12 h", "By infection", "—", "Label · UK SmPC", ""),
    ("neonate", "Serious infections, PMA >35 weeks", "IV", "15 mg/kg", "Every 8 h", "By infection", "—", "Label · UK SmPC", ""),
  ],
  "notes": [
    ("renal", "Usual starting dose 15–20 mg/kg every 24 h; do not reduce the first dose.", "CrCl 20–49", "Label · UK SmPC"),
    ("renal", "Timing and size of later doses depend on trough levels and the dialysis method; the next dose may be withheld until levels are known. Intermittent haemodialysis removes little vancomycin; high-flux membranes and CRRT remove more.", "CrCl <20 or dialysis", "Label · UK SmPC"),
    ("renal", "Children: 15 mg/kg every 12 h.", "eGFR 30–50", "Label · UK SmPC"),
    ("renal", "Children: 15 mg/kg every 24 h.", "eGFR 10–29", "Label · UK SmPC"),
    ("renal", "Children: 10–15 mg/kg once, then re-dose by levels.", "eGFR <10", "Label · UK SmPC"),
    ("renal", "Anephric adults: 15 mg/kg, then 1.9 mg/kg every 24 h.", "Anephric", "Label · US"),
    ("hepatic", "No dose adjustment needed.", "", "Label · UK SmPC"),
    ("elderly", "Lower maintenance doses may be needed because kidney function declines with age; monitor kidney function.", "", "Label · UK SmPC"),
    ("pregnancy", "Use only if clearly needed, with careful level monitoring; much higher doses may be needed in pregnancy. Passes into breast milk, but significant absorption by the infant is unlikely.", "", "Label · UK SmPC"),
    ("administration", "Infuse over at least 60 minutes or at no more than 10 mg/min (whichever is longer), diluted to 2.5–5 mg/mL (at least 100 mL per 500 mg). Rotate infusion sites. Never give IM.", "", "Label · UK SmPC"),
    ("administration", "Oral use: dissolve one 500 mg vial in 30 mL water to drink or give by nasogastric tube.", "", "Label · UK SmPC"),
    ("monitor", "Trough level usually 10–20 mg/L (15–20 mg/L if MIC ≥1 mg/L); first level on day 2 before the next dose, then daily to weekly; in haemodialysis, sample before the session.", "", "Label · UK SmPC"),
    ("monitor", "Kidney function, white cell count, urine and liver tests during prolonged treatment; hearing tests in older patients and with other ototoxic drugs.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (UK_URL, "hameln vancomycin 500 mg SmPC (text revised 19/01/2026): 4.1 cSSTI, bone/joint, CAP, HAP/VAP, endocarditis, perioperative prophylaxis, oral CDI; 4.2 adults ≥12 y 15–20 mg/kg q8–12h max 2 g/dose, loading 25–30 mg/kg; children 1 mo–<12 y 10–15 mg/kg q6h; neonates 15 mg/kg q24/12/8h by PMA <29/29–35/>35 wk; prophylaxis 15 mg/kg; oral CDI 125 mg q6h or 500 mg q6h x10 days, max 2 g/day, recurrences taper/pulse, children 10 mg/kg q6h; renal CrCl 20–49 15–20 mg/kg q24h, <20/RRT by levels; paediatric eGFR bands; hepatic none; elderly; pregnancy higher doses; trough 10–20 (15–20) mg/L, day 2; infusion ≥60 min/≤10 mg/min, 2.5–5 mg/mL; oral reconstitution 30 mL; 4.3 not IM; 4.4 SCARs must not restart, Kounis, HORV, IV ineffective for CDI, >60 mg/kg/day not recommended in children; 4.5 anaesthetics, bacitracin/polymyxin B/colistin/viomycin, PPIs/anti-motility; 4.8 ALT/AST common, interstitial nephritis, drug fever, chest/back pain."),
    (US_URL, "Glenmark vancomycin for injection label (rev 12/2025): adults 2 g/day as 500 mg q6h or 1 g q12h; anephric 15 mg/kg then 1.9 mg/kg/24 h; infuse ≥60 min; contraindication hypersensitivity; warnings incl. LABD, HORV, hypotension/shock/cardiac arrest with rapid infusion; geriatric renal monitoring; no brand names."),
  ],
}
