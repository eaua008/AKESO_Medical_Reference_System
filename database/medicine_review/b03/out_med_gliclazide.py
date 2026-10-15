SMPC_MR = "https://products.mhra.gov.uk/search/?search=gliclazide#emc-1321"
SMPC_IR = "https://products.mhra.gov.uk/search/?search=gliclazide#emc-13676"
MSF = "https://medicalguidelines.msf.org/viewport/EssDr/english/gliclazide-oral-27983946.html"
PNF = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
WHOEML = "https://list.essentialmeds.org/medicines/194"

MED = {
  "id": "med_gliclazide",
  "desc_add": "In the Philippines it is listed in the PNF Essential Medicines List as 30 mg and 60 mg modified-release tablets and an 80 mg tablet, and it has been on the WHO Model List of Essential Medicines since 2013. MSF guidance places it second line, alone when metformin is not tolerated or added to metformin when control is inadequate. It is cleared mainly by hepatic metabolism (under 1% excreted unchanged in urine) and is about 95% protein-bound, so dialysis does not help in overdose.",
  "facts": {
    "indication": [
      "Add-on to metformin when glycaemic control is inadequate on metformin alone",
    ],
    "adverse": [
      "Cholestatic jaundice (stop treatment)",
      "DRESS (very rare)",
      "Hyponatraemia, allergic vasculitis, agranulocytosis and pancytopenia (sulfonylurea class effects)",
      "Acute porphyria reported with other sulfonylureas in patients with porphyria",
    ],
    "contraindication": [],
    "interaction": [
      "H2 antagonists, MAOIs, sulfonamides (e.g., co-trimoxazole), trimethoprim, anabolic steroids: increased hypoglycaemia risk.",
      "Macrolides (clarithromycin, erythromycin): increased hypoglycaemia risk; monitor glucose.",
      "IV salbutamol, terbutaline or ritodrine, and tetracosactide: raised blood glucose.",
      "Rifampicin and St John's wort: reduced gliclazide effect or exposure.",
      "Hydrochlorothiazide: may raise blood glucose and reduce control.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Gliclazide 80 mg Tablets. Summary of Product Characteristics. Flamingo Pharma (UK) Ltd. electronic medicines compendium (emc); text revised 01/2025.", SMPC_IR),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Gliclazide oral. In: Essential Drugs – practical guidelines. MSF Medical Guidelines.", MSF),
    ("Philippine National Formulary (PhilHealth)", "Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.", PNF),
    ("WHO Model List of Essential Medicines", "World Health Organization. eEML – Electronic Essential Medicines List: Gliclazide (first added 2013, TRS 985).", WHOEML),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "Mild–moderate renal impairment: usual dose with careful monitoring; contraindicated in severe renal insufficiency (use insulin)."),
  ],
  "sources": [
    ("Label · UK SmPC MR", "UK SmPC (emc)", "Diamicron 30 mg MR Tablets SmPC, Servier; text revised 02/2020.", SMPC_MR),
    ("Label · UK SmPC", "UK SmPC (emc)", "Gliclazide 80 mg Tablets SmPC, Flamingo Pharma (UK) Ltd; text revised 01/2025.", SMPC_IR),
    ("MSF", "MSF Essential Drugs", "Médecins Sans Frontières. Gliclazide oral. Essential Drugs – practical guidelines.", MSF),
    ("PNF", "Philippine National Formulary (PhilHealth)", "PNF Essential Medicines List, 2022.", PNF),
  ],
  "doses": [
    ("adult", "Type 2 diabetes (MR tablet)", "PO", "30 mg", "Once a day", "Long-term", "120 mg/day", "Label · UK SmPC MR", "With breakfast; step up to 60, 90, 120 mg at ≥1-month intervals (2 weeks if glucose not falling)"),
    ("adult", "Type 2 diabetes (80 mg tablet)", "PO", "40–80 mg", "Once a day", "Long-term", "320 mg/day", "Label · UK SmPC", "Max 160 mg per dose; above 160 mg/day give 2× a day with main meals"),
    ("adult", "Type 2 diabetes, second line (80 mg tablet)", "PO", "40 mg, then 80–160 mg/day", "Once a day", "Long-term", "240 mg/day", "MSF", "Morning dose; increase by 40 mg every 2 weeks; split doses above 80 mg/day into 2"),
  ],
  "notes": [
    ("renal", "Mild–moderate impairment: same regimen with careful monitoring. Severe renal insufficiency: contraindicated (insulin recommended). Not removed by dialysis (strongly protein-bound).", "", "Label · UK SmPC MR"),
    ("hepatic", "Severe hepatic insufficiency: contraindicated (insulin recommended). Stop if cholestatic jaundice develops.", "", "Label · UK SmPC MR"),
    ("elderly", "Same regimen as under 65. Start at the minimum dose (30 mg MR / 40–80 mg) in high-risk patients: malnourished, poorly controlled endocrine disease (hypopituitarism, hypothyroidism, adrenal insufficiency), after stopping long-term/high-dose steroids, or severe vascular disease.", "", "Label · UK SmPC MR"),
    ("pregnancy", "Avoid in pregnancy; switch to insulin before conception or as soon as pregnancy is found. Contraindicated in breastfeeding (risk of neonatal hypoglycaemia).", "", "Label · UK SmPC MR"),
    ("administration", "MR tablet: swallow whole as one dose at breakfast; do not double a missed dose. One 80 mg tablet ≈ one 30 mg MR tablet when switching (monitor glucose). After a long half-life sulfonylurea, a few drug-free days may be needed. Not for children (no data).", "", "Label · UK SmPC MR"),
    ("forms_ph", "Gliclazide 30 mg and 60 mg modified-release (MR) oral tablets; 80 mg oral tablet.", "", "PNF"),
    ("monitor", "Blood glucose/HbA1c; teach patient and family hypoglycaemia symptoms and risk factors (missed meals, alcohol, exercise); close glucose checks with fluoroquinolones, illness or surgery; consider an alternative in G6PD deficiency. Hypoglycaemic coma: 50 mL 20–30% glucose IV, then 10% glucose infusion with close monitoring.", "", "Label · UK SmPC MR"),
  ],
  "checked": [
    (PNF, "PNF-EML lists Gliclazide 'Oral: 30 mg and 60 mg MR tablet' and '80 mg tablet'."),
    (SMPC_MR, "Diamicron 30 mg MR SmPC (Servier, text rev 02/2020): 30 mg od at breakfast, titration 60/90/120 mg at ≥1 month (2 weeks if no fall), max 120 mg; 80 mg IR ≈ 30 mg MR; elderly same; mild-moderate renal careful monitoring, severe renal/hepatic contraindicated; high-risk start 30 mg; no paediatric data; pregnancy avoid/insulin; lactation contraindicated (neonatal hypoglycaemia); ADRs incl. DRESS, cholestatic jaundice, class effects (hyponatraemia, vasculitis, agranulocytosis, pancytopenia); porphyria; interactions incl. H2 antagonists, MAOIs, sulfonamides, clarithromycin, IV salbutamol/terbutaline/ritodrine, tetracosactide, St John's wort; overdose 50 mL 20–30% glucose then 10% infusion; dialysis not beneficial (protein-bound); <1% unchanged in urine, ~95% protein binding."),
    (SMPC_IR, "Gliclazide 80 mg Tablets SmPC (Flamingo, rev 30/01/2025): 40–80 mg/day start, 40–320 mg/day, single dose max 160 mg, >160 mg/day twice daily with main meals; interactions incl. trimethoprim and anabolic steroids (hypoglycaemia)."),
    (MSF, "MSF Gliclazide oral: second-line T2D (>60 y) monotherapy if metformin not tolerated or with metformin; 40 mg od weeks 1–2, +40 mg every 2 weeks, usual 80–160 mg/day, max 240 mg/day; split >80 mg/day into 2 doses; interactions: erythromycin, co-trimoxazole, ciprofloxacin (hypoglycaemia), rifampicin (reduced effect), hydrochlorothiazide raises glucose."),
    (WHOEML, "WHO eEML: gliclazide, hypoglycaemic agents section, oral solid 30/60/80 mg, first added 2013 (TRS 985) for type 2 diabetes."),
  ],
}
