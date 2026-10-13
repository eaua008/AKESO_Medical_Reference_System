PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
PHIC_DENGUE = "https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf"
DOH_PIA = "https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf"
WHO_DENGUE = "https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue"
SMPC_TAB = "https://products.mhra.gov.uk/search/?search=ibuprofen#emc-7020"
SMPC_SUSP = "https://products.mhra.gov.uk/search/?search=ibuprofen#emc-4560"

MED = {
  "id": "med_ibuprofen",
  "desc_add": "In the Philippines, where dengue is endemic, NSAIDs such as ibuprofen are not recommended in suspected or confirmed dengue because they raise bleeding risk; PhilHealth's 2026 dengue quality standards and DOH advice name paracetamol as the antipyretic of choice, and DOH advises avoiding ibuprofen until dengue is ruled out. Ibuprofen can also mask fever and pain, which may delay recognition of a worsening infection.",
  "facts": {
    "indication": [
      "Migraine attacks (400 mg single dose)",
      "Juvenile idiopathic (rheumatoid) arthritis, under prescription (higher mg/kg doses)",
      "Post-immunisation fever in infants (limited to 2 doses)",
    ],
    "adverse": [
      "Severe skin reactions: SJS, TEN, DRESS, AGEP (mostly in the first month)",
      "Interstitial nephritis, nephrotic syndrome; renal tubular acidosis and hypokalaemia with prolonged high doses",
      "Rare blood dyscrasias (agranulocytosis, pancytopenia)",
      "Kounis syndrome (allergic acute coronary syndrome) has been reported",
      "Masking of fever and pain, delaying treatment of infection",
    ],
    "contraindication": [
      "Suspected or confirmed dengue: NSAIDs are not recommended (PhilHealth / DOH / WHO); use paracetamol",
      "Previous NSAID-related GI bleeding or perforation; active or recurrent peptic ulcer or haemorrhage",
      "Severe heart failure (NYHA class IV)",
      "Severe renal failure or severe hepatic failure",
      "Last trimester of pregnancy",
      "Significant dehydration (vomiting, diarrhoea or poor fluid intake)",
      "Cerebrovascular or other active bleeding; unexplained blood-formation disorders",
    ],
    "interaction": [
      "Corticosteroids and other NSAIDs (including COX-2 inhibitors): increased GI ulceration and bleeding.",
      "Quinolone antibiotics: possible increased risk of convulsions.",
      "Ciclosporin and tacrolimus: increased nephrotoxicity.",
      "Zidovudine: increased haematological toxicity (haemarthrosis/haematoma in haemophiliacs).",
      "CYP2C9 inhibitors (fluconazole, voriconazole): higher ibuprofen exposure; consider dose reduction.",
      "Digoxin and phenytoin: plasma levels may rise.",
      "Sulfonylureas: possible enhanced hypoglycaemic effect; monitor glucose.",
      "Mifepristone: avoid NSAIDs for 8–12 days after mifepristone.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("PhilHealth Dengue Quality Standards", "Philippine Health Insurance Corporation. Quality Standards on the Diagnosis and Management of Dengue (Adult and Children) as a Reference of the Corporation. PhilHealth Circular No. 2026-0009.", PHIC_DENGUE),
    ("WHO Fact Sheet - Dengue", "World Health Organization. Dengue and severe dengue. Fact sheet. Geneva: WHO.", WHO_DENGUE),
    ("UK SmPC (emc) - tablets", "Ibuprofen 400 mg film-coated tablets (POM) - Summary of Product Characteristics. Milpharm Ltd. Electronic medicines compendium (emc), revised June 2026.", SMPC_TAB),
    ("UK SmPC (emc) - suspension", "Ibuprofen 100 mg/5 ml Oral Suspension - Summary of Product Characteristics. Pinewood Laboratories Ltd. Electronic medicines compendium (emc), revised August 2024.", SMPC_SUSP),
  ],
  "links": [
    ("cholera", "avoid", "UK SmPC contraindicates ibuprofen in significant dehydration from vomiting or diarrhoea, with renal risk in dehydrated children (applied to cholera by inference)."),
    ("ischemic_stroke", "caution", "UK SmPC: small increased risk of arterial thrombotic events such as MI and stroke, mainly at high doses (2400 mg/day); use lowest dose for shortest time."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc) - tablets", "Ibuprofen 400 mg film-coated tablets (POM) - SmPC. Milpharm Ltd, 2026.", SMPC_TAB),
    ("Label · UK SmPC susp", "UK SmPC (emc) - suspension", "Ibuprofen 100 mg/5 ml Oral Suspension - SmPC. Pinewood Laboratories Ltd, 2024.", SMPC_SUSP),
    ("PNF", "Philippine National Formulary (PNF) EML", "Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.", PNF_URL),
    ("PhilHealth 2026", "PhilHealth Dengue Quality Standards", "PhilHealth Circular No. 2026-0009: Quality Standards on the Diagnosis and Management of Dengue (Adult and Children).", PHIC_DENGUE),
  ],
  "doses": [
    ("adult", "Pain, fever (≥12 y, ≥40 kg)", "PO", "200–400 mg", "Every 6 h as needed (3–4× a day)", "Short term", "1,200 mg/day (OTC)", "Label · UK SmPC", "Not in suspected dengue: use paracetamol"),
    ("adult", "Migraine", "PO", "400 mg", "Single dose; repeat 400 mg after ≥6 h if needed", "—", "1,200 mg/day", "Label · UK SmPC", ""),
    ("adult", "Primary dysmenorrhoea", "PO", "200–400 mg", "1–3× a day", "—", "1,200 mg/day", "Label · UK SmPC", ""),
    ("adult", "Rheumatic disease", "PO", "1,200–1,800 mg/day ÷ 3–4", "3–4× a day", "Maintenance 600–1,200 mg/day", "2,400 mg/day", "Label · UK SmPC", "Max single dose 800 mg"),
    ("child", "Pain, fever (3 mo–12 y)", "PO", "20 mg/kg/day ÷ 3–4", "Every 6–8 h", "≤3 days without review", "—", "Label · UK SmPC susp", "Not under 3 months"),
    ("child", "Pain, fever, 3–6 mo (>5 kg)", "PO", "50 mg (2.5 mL of 100 mg/5 mL)", "Up to 3× in 24 h", "Max 24 h", "150 mg/day", "Label · UK SmPC susp", "See doctor within 24 h if symptoms persist"),
    ("child", "Pain, fever, 6 mo–1 y", "PO", "50 mg (2.5 mL)", "3–4× a day", "≤3 days", "200 mg/day", "Label · UK SmPC susp", ""),
    ("child", "Pain, fever, 1–4 y", "PO", "100 mg (5 mL)", "3× a day", "≤3 days", "300 mg/day", "Label · UK SmPC susp", ""),
    ("child", "Pain, fever, 4–7 y", "PO", "150 mg (7.5 mL)", "3× a day", "≤3 days", "450 mg/day", "Label · UK SmPC susp", ""),
    ("child", "Pain, fever, 7–12 y", "PO", "200 mg (10 mL)", "3× a day", "≤3 days", "600 mg/day", "Label · UK SmPC susp", ""),
    ("child", "Juvenile rheumatoid arthritis", "PO", "30–40 mg/kg/day ÷ 3–4", "3–4× a day", "—", "—", "Label · UK SmPC susp", "Prescription only"),
  ],
  "notes": [
    ("renal", "Mild to moderate impairment: lowest dose for the shortest time and monitor renal function. Contraindicated in severe renal failure.", "", "Label · UK SmPC"),
    ("hepatic", "Mild to moderate impairment: lowest dose for the shortest time and monitor liver function. Contraindicated in severe hepatic failure.", "", "Label · UK SmPC"),
    ("elderly", "Higher risk of serious GI bleeding and perforation: lowest dose, shortest duration, review regularly.", "", "Label · UK SmPC"),
    ("pregnancy", "Avoid in the first and second trimesters unless clearly needed. From week 20, risk of oligohydramnios and ductus arteriosus constriction (consider antenatal monitoring after several days of use). Contraindicated in the third trimester. Short courses are acceptable in breastfeeding.", "", "Label · UK SmPC"),
    ("monitor", "Before giving for fever in the Philippines, consider dengue: NSAIDs (ibuprofen, celecoxib, aspirin) are not recommended; give paracetamol instead. Watch for GI bleeding signs (melena, haematemesis), blood pressure, urine output and hydration, especially in children with vomiting or diarrhoea.", "", "PhilHealth 2026"),
    ("administration", "Children from 6 months: see a doctor if needed for more than 3 days; adults: if needed for more than 10 days. Keep at least 4 h between doses.", "", "Label · UK SmPC susp"),
    ("forms_ph", "200 mg and 400 mg tablet; 100 mg/5 mL syrup/suspension (60 mL); 200 mg/5 mL suspension (60 mL).", "", "PNF"),
  ],
  "checked": [
    (PNF_URL, "Ibuprofen oral: 200 mg and 400 mg tablet; 100 mg/5 mL, 60 mL syrup/suspension; 200 mg/5 mL, 60 mL suspension."),
    (PHIC_DENGUE, "PhilHealth circular 'Quality Standards on the Diagnosis and Management of Dengue (Adult and Children)': Sec V.D.2.d use of NSAIDs such as ibuprofen, celecoxib, aspirin is not recommended; V.D.2.c paracetamol may be given for fever in adults and children."),
    (WHO_DENGUE, "Paracetamol for pain; NSAIDs such as ibuprofen and aspirin should be avoided as they can increase the risk of bleeding."),
    (DOH_PIA, "PhilHealth dengue standards: NSAIDs (ibuprofen named) are not recommended in dengue; paracetamol for fever."),
    (SMPC_TAB, "Milpharm 400 mg POM SmPC (rev 06/2026): adult pain/fever 200–400 mg every 6 h max 1200 mg/day; migraine 400 mg; dysmenorrhoea 200–400 mg 1–3×/day; rheumatic 1200–1800 mg/day, maintenance 600–1200, up to 2400 mg/day; max single 800 mg; renal/hepatic mild-moderate lowest dose + monitor, severe contraindicated; full contraindication list incl. NYHA IV, last trimester, significant dehydration, active bleeding; varicella and masking-infection warnings; interactions (quinolones, ciclosporin, tacrolimus, zidovudine, CYP2C9 inhibitors, sulphonylureas, digoxin, phenytoin, mifepristone 8–12 days, corticosteroids); pregnancy week 20 oligohydramnios/ductus; SJS/TEN/DRESS/AGEP, Kounis syndrome, agranulocytosis, interstitial nephritis, MI/stroke risk at 2400 mg/day."),
    (SMPC_SUSP, "Pinewood 100 mg/5 ml SmPC (rev 08/2024): 3–6 mo >5 kg 2.5 mL up to 3×/24 h, max 24 h; 6–12 mo 2.5 mL 3–4×; 1–4 y 5 mL 3×; 4–7 y 7.5 mL 3×; 7–12 y 10 mL 3×; 20 mg/kg/day divided; JRA 30–40 mg/kg/day in 3–4 doses; not under 3 months; children consult if >3 days, adults >10 days; post-immunisation fever max 2 doses; risk of renal impairment in dehydrated children; avoid in varicella."),
  ],
}
