SMPC_MDI = "https://products.mhra.gov.uk/search/?search=salbutamol#emc-850"
SMPC_NEB = "https://products.mhra.gov.uk/search/?search=salbutamol#emc-10256"
MSF_MDI = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-aerosol-16684638.html"
MSF_NEB = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-nebuliser-solution-16684649.html"
PH_KONSULTA = "https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf"

MED = {
  "id": "med_salbutamol",
  "desc_add": "For most asthma attacks a metered-dose inhaler with a spacer is easier, faster, at least as effective and better tolerated than a nebuliser, so nebulised salbutamol (with ipratropium) is reserved for severe attacks. In the Philippines, salbutamol is among the medicines of the PhilHealth Konsulta primary-care package as a metered-dose inhaler, dry powder inhaler, nebulising solution and syrup.",
  "facts": {
    "indication": [
      "Severe acute asthma attack: nebulised, combined with ipratropium (MSF)",
    ],
    "adverse": [
      "Muscle cramps; mouth and throat irritation",
      "Peripheral vasodilatation",
      "Lactic acidosis with high-dose (e.g. nebulised) therapy",
      "Myocardial ischaemia (post-marketing, frequency unknown)",
      "Hypersensitivity: angioedema, urticaria, hypotension and collapse (very rare)",
    ],
    "contraindication": [
      "Non-IV forms must not be used to stop uncomplicated premature labour or threatened abortion",
      "Nebuliser solution must never be given parenterally",
    ],
    "interaction": [
      "Xanthine derivatives and corticosteroids: may potentiate beta-2-agonist hypokalaemia.",
      "Nebulised ipratropium: acute angle-closure glaucoma reported with the combination; keep the mist out of the eyes.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (Ventolin Evohaler)", "Ventolin Evohaler 100 micrograms. Summary of Product Characteristics. electronic medicines compendium (emc).", SMPC_MDI),
    ("UK SmPC (nebuliser solution)", "Salbutamol 1 mg/ml nebuliser solution (Cipla EU Ltd). Summary of Product Characteristics. electronic medicines compendium (emc).", SMPC_NEB),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Salbutamol metered dose inhaler; Salbutamol nebuliser solution. MSF Medical Guidelines (updated June 2023).", MSF_MDI),
    ("PhilHealth Konsulta", "Philippine Health Insurance Corporation. Certification of Service Delivery Support (Medicines), Annex D2 – Konsulta Package accreditation.", PH_KONSULTA),
  ],
  "links": [
    ("type2_diabetes", "caution", "Beta-2 agonists can raise blood glucose; the SmPC advises caution in diabetes."),
    ("acute_coronary_syndrome", "caution", "Rare myocardial ischaemia reported; the SmPC advises patients with severe heart disease to seek advice for chest pain or worsening symptoms."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (Ventolin Evohaler)", "Ventolin Evohaler 100 micrograms. Summary of Product Characteristics. emc.", SMPC_MDI),
    ("Label · UK SmPC neb", "UK SmPC (nebuliser solution)", "Salbutamol 1 mg/ml nebuliser solution (Cipla EU Ltd). Summary of Product Characteristics. emc.", SMPC_NEB),
    ("MSF", "MSF Essential Drugs (MDI)", "Médecins Sans Frontières. Essential drugs – Salbutamol metered dose inhaler.", MSF_MDI),
    ("MSF neb", "MSF Essential Drugs (nebuliser)", "Médecins Sans Frontières. Essential drugs – Salbutamol nebuliser solution.", MSF_NEB),
    ("PhilHealth", "PhilHealth Konsulta medicines list", "PhilHealth. Certification of Service Delivery Support (Medicines), Annex D2 – Konsulta Package.", PH_KONSULTA),
  ],
  "doses": [
    ("adult", "Acute bronchospasm (reliever)", "Inhaled", "100–200 micrograms (1–2 puffs)", "As needed", "—", "8 puffs/24 h", "Label · UK SmPC", "MDI 100 micrograms/puff"),
    ("adult", "Exercise or allergen prevention", "Inhaled", "200 micrograms (2 puffs)", "10–15 min before challenge", "—", "8 puffs/24 h", "Label · UK SmPC", ""),
    ("adult", "Chronic therapy", "Inhaled", "200 micrograms (2 puffs)", "Up to 4× a day", "—", "8 puffs/24 h", "Label · UK SmPC", ""),
    ("adult", "Asthma attack, first hour", "Inhaled", "200–1000 micrograms (2–10 puffs)", "Every 20 min", "1 h", "—", "MSF", "Then 2–4 puffs every 4–6 h for 24–48 h; spacer advised"),
    ("adult", "Severe asthma attack", "Inhaled", "5 mg nebulised", "Every 20 min", "First hour, then taper", "—", "MSF neb", "With ipratropium; switch to MDI as symptoms improve"),
    ("adult", "Bronchospasm (nebuliser)", "Inhaled", "2.5–5 mg nebulised", "Up to 4× a day", "—", "40 mg/day (hospital only)", "Label · UK SmPC neb", "Includes elderly and ≥ 12 y"),
    ("child", "Acute bronchospasm, < 12 y", "Inhaled", "100 micrograms (1 puff)", "As needed", "—", "8 puffs/24 h", "Label · UK SmPC", "May increase to 2 puffs; licensed from 4 y"),
    ("child", "Asthma attack, first hour", "Inhaled", "200–1000 micrograms (2–10 puffs)", "Every 20 min", "1 h", "—", "MSF", "Same as adult; use a spacer (< 6 y)"),
    ("child", "Severe asthma attack, < 5 y", "Inhaled", "2.5 mg nebulised", "Every 20 min", "First hour, then taper", "—", "MSF neb", "With ipratropium"),
    ("child", "Severe asthma attack, 5–11 y", "Inhaled", "2.5–5 mg nebulised", "Every 20 min", "First hour, then taper", "—", "MSF neb", "With ipratropium"),
    ("child", "Bronchospasm (nebuliser), 4–11 y", "Inhaled", "2.5–5 mg nebulised", "Up to 4× a day", "—", "—", "Label · UK SmPC neb", "< 18 months: efficacy uncertain; transient hypoxia, consider oxygen"),
  ],
  "notes": [
    ("forms_ph", "MDI 100 micrograms/dose × 200 actuations (also breath-actuated MDI); DPI 200 micrograms/dose; nebulising solution 1 mg/mL and 2 mg/mL, 2.5 mL unit dose; syrup 2 mg/5 mL, 60 mL. Combination ipratropium + salbutamol MDI and nebule.", "", "PhilHealth"),
    ("administration", "Nebuliser: dilute with 0.9% sodium chloride to 4 mL total; stop when the reservoir is empty (about 10–15 min).", "", "MSF neb"),
    ("administration", "Use a spacer for children under 6, older patients and severe dyspnoea; clean the mouthpiece before and after use.", "", "MSF"),
    ("renal", "No renal dose adjustment is given in the SmPC; salbutamol is cleared partly renally.", "", "Label · UK SmPC neb"),
    ("elderly", "Adult dose applies, including the elderly.", "", "Label · UK SmPC neb"),
    ("pregnancy", "SmPC: use only if clearly necessary; avoid in breast-feeding unless benefit outweighs risk. MSF lists no contraindication in pregnancy or breast-feeding.", "", "Label · UK SmPC"),
    ("monitor", "Serum potassium in acute severe asthma; check for lactic acidosis if tachypnoea persists after wheeze resolves.", "", "Label · UK SmPC"),
    ("monitor", "Blood glucose in diabetes; review control if reliever is used more than twice a week or a dose gives no relief for 3 h; check inhaler technique.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (SMPC_MDI, "Ventolin Evohaler 100 micrograms SmPC: adults acute 1 inhalation, may increase to 2; prevention 2 inhalations 10–15 min before challenge; chronic 2 inhalations up to 4×/day; children <12 1 inhalation, may increase to 2; max 8 inhalations/24 h; indicated adults, adolescents, children 4–11; contraindicated non-IV for uncomplicated premature labour/threatened abortion; hypokalaemia (monitor K in acute severe asthma), lactic acidosis, thyrotoxicosis, myocardial ischaemia, diabetes caution, use >2×/week or no relief 3 h; pregnancy only if clearly necessary; breast-feeding; AEs angioedema/urticaria/hypotension/collapse, peripheral vasodilatation, mouth/throat irritation, muscle cramps, myocardial ischaemia unknown."),
    (SMPC_NEB, "Salbutamol 1 mg/ml nebuliser solution (Cipla): adults incl. elderly and ≥12 y 2.5–5 mg up to 4×/day; up to 40 mg/day in hospital; children 4–11 2.5–5 mg up to 4×/day; <18 months efficacy uncertain, transient hypoxia, consider oxygen; angle-closure glaucoma with ipratropium, keep mist from eyes; lactic acidosis with high-dose nebulised therapy; xanthines/steroids/diuretics potentiate hypokalaemia; no renal/hepatic adjustment, cleared partly renally."),
    (MSF_MDI, "MSF MDI 100 micrograms/puff: attack 2–10 puffs every 20 min first hour, then 2–4 puffs every 4–6 h for 24–48 h (or every 1–4 h if not resolved); chronic 2–4 puffs up to 4×/day; spacer for <6 y, older patients, severe dyspnoea; clean mouthpiece; no contraindication pregnancy/breast-feeding; in severe attack nebulised salbutamol + ipratropium preferred."),
    (MSF_NEB, "MSF nebuliser solution 5 mg/2.5 mL: severe asthma attack with ipratropium; every 20 min first hour: <5 y 2.5 mg, 5–11 y 2.5–5 mg, ≥12 y and adults 5 mg; dilute with 0.9% NaCl to 4 mL, ~10–15 min; never parenteral; MDI + spacer easier, faster, as or more effective, fewer AEs."),
    (PH_KONSULTA, "PhilHealth Konsulta Annex D2 medicines list: salbutamol syrup 2 mg/5 mL 60 mL; DPI 200 micrograms/dose; MDI 100 micrograms/dose × 200; breath-actuated MDI; resp. soln 1 mg/mL and 2 mg/mL 2.5 mL unit dose; ipratropium + salbutamol MDI and nebule. No brand names."),
  ],
}
