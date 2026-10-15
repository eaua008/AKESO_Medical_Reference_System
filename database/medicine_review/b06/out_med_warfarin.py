UK_URL = "https://products.mhra.gov.uk/search/?search=warfarin#emc-14333"
US_URL = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=541c9a70-adaf-4ef3-94ba-ad4e70dfa057"
HTA_URL = "https://hta.dost.gov.ph/wp-content/uploads/2026/07/ES-DOACs-for-NVAF-25-April-2023.pdf"

MED = {
  "id": "med_warfarin",
  "desc_add": "In the Philippines warfarin is listed in the Philippine National Formulary for prophylaxis and treatment of thromboembolic disorders, and the Stroke Society of the Philippines recommends either well-controlled warfarin or a direct oral anticoagulant for at-risk patients with non-valvular atrial fibrillation. Its main practical burden is regular INR testing and the many drug and food interactions; an INR above 4.0 adds bleeding risk without added benefit for most patients.",
  "facts": {
    "indication": [
      "Transient ischaemic attack (UK labeling)",
      "Systemic embolism prevention in rheumatic heart disease with atrial fibrillation",
    ],
    "adverse": [
      "Pancreatitis, diarrhoea, nausea and vomiting",
      "Rash, alopecia and purpura",
      "Unexplained fall in haematocrit or haemoglobin",
      "Limb ischaemia or gangrene when started too early in heparin-induced thrombocytopenia",
    ],
    "contraindication": [
      "Haemorrhagic stroke",
      "Within 72 hours of major surgery with risk of severe bleeding",
      "Within 48 hours postpartum",
      "Initial therapy in heparin-induced thrombocytopenia (start only after platelet count normalises)",
      "Rare hereditary galactose intolerance or lactase deficiency (UK tablets contain lactose)",
    ],
    "interaction": [
      "Fibrinolytics (streptokinase, alteplase): contraindicated combination.",
      "Allopurinol, capecitabine, erlotinib, tamoxifen, fibrates, statins (mainly fluvastatin), omeprazole and sulfamethoxazole: may raise INR.",
      "Phenytoin, primidone, griseofulvin, azathioprine and oral contraceptives: may lower warfarin effect.",
      "Corticosteroids, nevirapine and ritonavir: variable effect on INR; monitor closely.",
      "Cholestyramine and sucralfate reduce warfarin absorption; orlistat may reduce vitamin K absorption.",
      "Dabigatran, rivaroxaban and fondaparinux: additive bleeding risk.",
      "Cranberry (avoid), grapefruit juice and glucosamine: may raise INR.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Warfarin 5 mg tablets. Summary of Product Characteristics. Strides Pharma UK Ltd; text revised 10 May 2022, updated July 2025. electronic medicines compendium (emc).", UK_URL),
    ("DOST Health Technology Assessment Council (Philippines)", "Health Technology Assessment Council. Evidence Summary on Apixaban, Dabigatran, and Rivaroxaban for the prevention of myocardial infarction, cerebrovascular disease, and other cardiovascular events among patients with nonvalvular atrial fibrillation. HTA Division, DOST; 25 April 2023.", HTA_URL),
  ],
  "links": [
    ("hypertension", "caution", "Uncontrolled or moderate-to-severe hypertension raises bleeding risk (UK SmPC, US label); malignant hypertension is a contraindication."),
    ("chronic_kidney_disease", "caution", "No dose change, but more frequent INR checks; higher risk of bleeding, anticoagulant-related nephropathy and calciphylaxis (UK SmPC, US label)."),
    ("type2_diabetes", "caution", "Diabetes is listed among conditions with higher warfarin risk (US label)."),
    ("acute_coronary_syndrome", "safe", "After high-risk MI: INR 2.0–3.0 plus low-dose aspirin for at least 3 months (US label)."),
  ],
  "sources": [
    ("Label · US", "DailyMed (FDA label)", "Warfarin sodium tablets. Prescribing information. Amneal Pharmaceuticals; revised 7/2026. DailyMed, U.S. National Library of Medicine.", US_URL),
    ("Label · UK SmPC", "UK SmPC (emc)", "Warfarin 5 mg tablets. Summary of Product Characteristics. Strides Pharma UK Ltd; 2022/2025.", UK_URL),
  ],
  "doses": [
    ("adult", "Starting dose (no genotype data)", "PO", "2–5 mg", "Once a day", "Until INR in range", "—", "Label · US", "No routine loading dose; usual maintenance 2–10 mg"),
    ("adult", "Elective loading (UK regimen)", "PO", "10 mg", "Once a day", "2 days", "—", "Label · UK SmPC", "Then 3–9 mg once a day by INR; no loading in protein C deficiency"),
    ("adult", "DVT / PE treatment", "PO", "Dose to INR 2.0–3.0", "Once a day", "3 months if provoked; ≥3 months if unprovoked", "—", "Label · US", "Overlap heparin 4–5 days and until INR in range"),
    ("adult", "Atrial fibrillation", "PO", "Dose to INR 2.0–3.0", "Once a day", "Long-term", "—", "Label · US", ""),
    ("adult", "Mechanical aortic valve (bileaflet, sinus rhythm)", "PO", "Dose to INR 2.0–3.0", "Once a day", "Long-term", "—", "Label · US", ""),
    ("adult", "Mechanical mitral or caged-ball/disk valve", "PO", "Dose to INR 2.5–3.5", "Once a day", "Long-term", "—", "Label · US", ""),
    ("adult", "Bioprosthetic mitral valve", "PO", "Dose to INR 2.0–3.0", "Once a day", "First 3 months", "—", "Label · US", ""),
    ("adult", "After high-risk MI", "PO", "Dose to INR 2.0–3.0", "Once a day", "≥3 months", "—", "Label · US", "With aspirin ≤100 mg/day"),
  ],
  "notes": [
    ("renal", "No dose adjustment; check INR more often. Watch kidney function if INR is high with blood in the urine (anticoagulant-related nephropathy).", "", "Label · US"),
    ("hepatic", "Liver impairment can increase warfarin's effect; monitor more closely for bleeding.", "", "Label · US"),
    ("elderly", "Use lower starting and maintenance doses in elderly or debilitated patients and in Asian patients (US label). Age 65 or over is a bleeding risk factor.", "", "Label · US"),
    ("pregnancy", "Contraindicated except in women with mechanical valves at high thrombotic risk; first-trimester exposure causes embryopathy in about 5%. Check pregnancy status and use contraception during treatment and for 1 month after. Not found in breast milk in a small study; watch the infant for bruising.", "", "Label · US"),
    ("administration", "Take at the same time each day. Missed dose: take it the same day as soon as possible; do not double the next day's dose.", "", "Label · US"),
    ("administration", "Surgery with severe bleeding risk: stop 3 days before; other surgery can proceed with INR <2.5. Dental extractions do not need warfarin stopped.", "", "Label · UK SmPC"),
    ("administration", "High INR or bleeding: INR 6–8 with no or minor bleeding, stop and restart when INR <5; INR >8, stop and give vitamin K 0.5–1 mg IV or 5 mg orally; life-threatening bleeding, prothrombin complex concentrate 30–50 units/kg (or FFP 15 mL/kg).", "", "Label · UK SmPC"),
    ("monitor", "INR daily after the first dose until stable in range, then every 1–4 weeks; recheck within 2–3 days of any dose change or when other drugs are started or stopped.", "", "Label · US"),
    ("monitor", "When overlapping with heparin, check INR at least 5 h after an IV bolus, 4 h after stopping an infusion or 24 h after a SC dose.", "", "Label · US"),
    ("monitor", "Check thyroid status when starting in hyper- or hypothyroidism; ask about bleeding, skin pain or purple toes at each visit.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (UK_URL, "Strides warfarin 5 mg SmPC: 4.1 RHD with AF, prosthetic valves, VTE/PE, TIA; 4.2 loading 10 mg once daily for 2 days, maintenance 3.0–9.0 mg; children no data; 4.3 haemorrhagic stroke, within 72 h of major surgery, 48 h postpartum, 1st/3rd trimester, fibrinolytics; 4.4 calciphylaxis, thyroid monitoring, protein C no loading, surgery stop 3 days/INR <2.5, dental, bleeding risk factors incl. uncontrolled hypertension & renal insufficiency, INR within 2–3 days of dose change, ARN, lactose; Asian/Afro-Caribbean statement (conflicts with US, not used); 4.5 allopurinol, capecitabine, erlotinib, tamoxifen, fibrates, fluvastatin, omeprazole, sulfamethoxazole; phenytoin, primidone, griseofulvin, azathioprine, OCs; corticosteroids/nevirapine/ritonavir variable; cholestyramine, sucralfate, orlistat, glucosamine, cranberry, grapefruit; dabigatran/rivaroxaban/fondaparinux; 4.8 pancreatitis, alopecia, purpura, haematocrit drop; 4.9 reversal thresholds and doses."),
    (US_URL, "Amneal warfarin label (rev 7/2026): target INRs and durations (VTE, AF, mechanical valves 2.0–3.0 / 2.5–3.5, bioprosthetic mitral 3 months, post-MI + aspirin ≥3 months), INR >4 no benefit; initial 2–5 mg, maintenance 2–10 mg, no routine loading; lower doses elderly/debilitated/Asian; INR daily then 1–4 weeks; heparin overlap 4–5 days and INR timing; missed dose; 8.1 embryopathy ~5%, contraception 1 month; 8.2 not detected in milk (15 mothers); 8.6 renal no adjustment; 8.7 hepatic; warnings HIT, hypertension, diabetes, calciphylaxis."),
    (HTA_URL, "HTAC evidence summary (25 Apr 2023): 'Warfarin is currently listed in the Philippine National Formulary for prophylaxis and treatment of thromboembolic disorders'; Stroke Society of the Philippines recommends well-controlled warfarin or DOACs in at-risk NVAF; no forms/strengths given."),
  ],
}
