PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
SMPC = "https://products.mhra.gov.uk/search/?search=famotidine#emc-11523"
INJ = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1fdf16e5-145d-4c19-a318-fc6c10794b50"

MED = {
  "id": "med_famotidine",
  "desc_add": "A single 40 mg bedtime dose suppresses gastric acid for more than 12 hours, and famotidine does not affect the cytochrome P450 system, so it has few clinically important interactions apart from drugs that need gastric acid for absorption. In the Philippines the PNF lists a 20 mg tablet and a 20 mg injection, the latter used intravenously in hospitalised patients until oral therapy is possible.",
  "facts": {
    "indication": [
      "Prevention of duodenal ulcer relapse (20 mg at night)",
      "Hospitalised patients who cannot take oral therapy (IV 20 mg every 12 h)",
    ],
    "adverse": [
      "Taste disorder, dry mouth, nausea, flatulence and loss of appetite (uncommon)",
      "Rash, itching and urticaria (uncommon)",
      "Very rare: agranulocytosis or pancytopenia, anaphylaxis, hepatitis or cholestatic jaundice, convulsions",
      "Very rare: QT prolongation and arrhythmias",
    ],
    "contraindication": [
      "Gastric malignancy must be excluded before treating a gastric ulcer",
      "Multiple-dose vials containing benzyl alcohol: not for neonates (gasping syndrome)",
    ],
    "interaction": [
      "Ketoconazole or itraconazole: absorption reduced; give ketoconazole 2 hours before famotidine.",
      "Atazanavir and posaconazole oral suspension: absorption reduced by higher gastric pH; avoid where possible.",
      "Erlotinib, gefitinib or pazopanib: co-administration not recommended.",
      "Probenecid: raises famotidine levels by about 50%; avoid.",
      "Antacids: take famotidine 1–2 hours before the antacid; sucralfate should not be given within 2 hours of famotidine.",
      "Calcium carbonate phosphate binders in haemodialysis patients: may lose efficacy.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.", PNF_URL),
    ("UK SmPC (emc)", "Famotidine 20mg Tablets - Summary of Product Characteristics. Tillomed Laboratories Ltd. Electronic medicines compendium (emc), updated January 2025.", SMPC),
    ("DailyMed (FDA label)", "Famotidine Injection, USP 10 mg/mL - prescribing information. Hikma Pharmaceuticals USA Inc. DailyMed, U.S. National Library of Medicine.", INJ),
  ],
  "links": [
    ("peptic_ulcer_disease", "safe", "Licensed for duodenal and benign gastric ulcer healing and relapse prevention; exclude gastric malignancy first."),
    ("chronic_kidney_disease", "caution", "Daily dose halved when CrCl < 30 mL/min; CNS adverse effects reported in moderate to severe renal insufficiency."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Famotidine 20mg Tablets - SmPC. Tillomed Laboratories Ltd, 2024.", SMPC),
    ("Label · US (inj)", "DailyMed (FDA label)", "Famotidine Injection, USP 10 mg/mL - prescribing information. Hikma Pharmaceuticals USA Inc.", INJ),
    ("PNF", "Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.", PNF_URL),
  ],
  "doses": [
    ("adult", "Duodenal ulcer", "PO", "40 mg", "Once a day (at night)", "4–8 weeks", "—", "Label · UK SmPC", "Continue 4 more weeks if not healed at 4 weeks"),
    ("adult", "Duodenal ulcer relapse prevention", "PO", "20 mg", "Once a day (at night)", "—", "—", "Label · UK SmPC", ""),
    ("adult", "Benign gastric ulcer", "PO", "40 mg", "Once a day (at night)", "4–8 weeks", "—", "Label · UK SmPC", "Exclude malignancy first"),
    ("adult", "Reflux oesophagitis, mild", "PO", "20 mg", "2× a day", "6–12 weeks", "—", "Label · UK SmPC", ""),
    ("adult", "Reflux oesophagitis, mild to moderate", "PO", "40 mg", "2× a day", "6–12 weeks", "—", "Label · UK SmPC", ""),
    ("adult", "Zollinger-Ellison syndrome", "PO", "20 mg, then adjust", "Every 6 h", "As needed", "800 mg/day", "Label · UK SmPC", "Up to 800 mg/day used for up to 1 year"),
    ("adult", "Hospitalised / unable to take oral", "IV", "20 mg", "Every 12 h", "Until oral possible", "—", "Label · US (inj)", "Push over ≥2 min or infuse over 15–30 min"),
    ("child", "1–16 y, IV acid suppression", "IV", "0.25 mg/kg", "Every 12 h", "—", "40 mg/day", "Label · US (inj)", "Up to 0.5 mg/kg every 12 h used in studies; oral use in children not established (UK SmPC)"),
  ],
  "notes": [
    ("renal", "Reduce the daily dose by 50%.", "CrCl <30", "Label · UK SmPC"),
    ("renal", "Consider 20 mg at night.", "CrCl <10", "Label · UK SmPC"),
    ("renal", "Reduce dose by 50%; give at the end of or after dialysis.", "Dialysis", "Label · UK SmPC"),
    ("elderly", "Same dose as adults.", "", "Label · UK SmPC"),
    ("pregnancy", "Not recommended in pregnancy unless clearly needed. Excreted in breast milk: stop famotidine or stop breastfeeding.", "", "Label · UK SmPC"),
    ("monitor", "Blood count and liver function during long-term high-dose treatment; avoid abrupt withdrawal after long-standing ulcer disease; watch for confusion in renal impairment.", "", "Label · UK SmPC"),
    ("administration", "IV push: dilute 20 mg (2 mL) to 5 or 10 mL and inject over at least 2 minutes. Infusion: dilute 2 mL in 100 mL dextrose 5% and run over 15–30 minutes.", "", "Label · US (inj)"),
    ("forms_ph", "20 mg tablet; 20 mg powder/lyophilized powder for injection (ampule/vial).", "", "PNF"),
  ],
  "checked": [
    (PNF_URL, "Famotidine: oral 20 mg tablet; inj. 20 mg powder/lyophilized powder for injection, ampule/vial."),
    (SMPC, "Tillomed Famotidine 20 mg SmPC: DU 40 mg nocte 4(+4) weeks; relapse 20 mg nocte; GU 40 mg nocte 4–8 weeks; ZES 20 mg q6h up to 800 mg/day for 1 year; oesophagitis 20 mg bd mild / 40 mg bd mild-moderate, 6+6 weeks; CrCl <30 reduce 50%, dialysis 50% after dialysis, <10 consider 20 mg nocte; elderly as adults; children not established; exclude gastric malignancy; monitor blood count/LFT long-term high dose; avoid abrupt withdrawal; interactions ketoconazole/itraconazole, atazanavir, probenecid +50%, antacids 1–2 h, sucralfate 2 h, posaconazole suspension, dasatinib/erlotinib/gefitinib/pazopanib, calcium carbonate phosphate binders; no CYP450 effect; pregnancy not recommended, excreted in breast milk; adverse effects list incl. taste disorder, dry mouth, very rare agranulocytosis, pancytopenia, hepatitis, convulsions, QT prolongation; 40 mg at 9 pm effective >12 h."),
    (INJ, "Hikma Famotidine Injection 10 mg/mL: adult 20 mg IV q12h until oral possible; IV push diluted to 5 or 10 mL over ≥2 min; infusion in 100 mL D5W over 15–30 min; paediatric 1–16 y 0.25 mg/kg IV q12h up to 40 mg/day (up to 0.5 mg/kg used); CNS adverse effects in moderate/severe renal insufficiency; benzyl alcohol multi-dose vials and gasping syndrome in neonates."),
  ],
}
