SMPC = "https://products.mhra.gov.uk/search/?search=paracetamol#emc-9128"
MERCK = "https://www.merckmanuals.com/professional/injuries-poisoning/poisoning/acetaminophen-poisoning"
PH_KONSULTA = "https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf"

MED = {
  "id": "med_paracetamol",
  "desc_add": "A small fraction is converted by hepatic cytochrome P-450 to the toxic metabolite NAPQI, normally detoxified by glutathione; an acute ingestion of at least 150 mg/kg (about 7.5–10 g in adults) can deplete glutathione and cause hepatocellular necrosis, and N-acetylcysteine is most effective within 8 hours of ingestion. In the Philippines, paracetamol is in the PhilHealth Konsulta primary-care medicines list as 300 mg and 500 mg tablets, 100 mg/mL drops, 120 mg/5 mL (125 mg/5 mL) and 250 mg/5 mL syrup/suspension, and 125 mg and 250 mg suppositories.",
  "facts": {
    "indication": [],
    "adverse": [
      "Blood dyscrasias including thrombocytopenia and agranulocytosis (frequency not known)",
      "High anion gap metabolic acidosis, mainly in sepsis, malnutrition or glutathione deficiency (e.g. chronic alcoholism)",
    ],
    "contraindication": [
      "Use with care in severe renal impairment",
      "Overdose hazard greater in non-cirrhotic alcoholic liver disease",
    ],
    "interaction": [
      "Metoclopramide or domperidone: may speed paracetamol absorption.",
      "Cholestyramine: reduces paracetamol absorption.",
      "Flucloxacillin: combined (especially prolonged) use raises the risk of high anion gap metabolic acidosis; use with caution.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC", "Paracetamol 500 mg Tablets (P), Zentiva Pharma UK Ltd. Summary of Product Characteristics (updated 25 February 2025). electronic medicines compendium (emc).", SMPC),
    ("Merck Manual Professional", "O'Malley GF, O'Malley R. Acetaminophen Poisoning. Merck Manual Professional Edition (reviewed Apr 2025).", MERCK),
    ("PhilHealth Konsulta", "Philippine Health Insurance Corporation. Certification of Service Delivery Support (Medicines), Annex D2 – Konsulta Package accreditation.", PH_KONSULTA),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "SmPC advises care in severe renal impairment (applies to advanced CKD)."),
    ("hepatitis_b", "caution", "Own inference: SmPC advises care in severe hepatic impairment, which can occur in chronic hepatitis B; not stated for hepatitis B specifically."),
  ],
  "checked": [
    (SMPC, "Zentiva Paracetamol 500 mg SmPC: care in severe renal or severe hepatic impairment; overdose hazard greater in non-cirrhotic alcoholic liver disease; HAGMA with sepsis, malnutrition, glutathione deficiency (chronic alcoholism), and with flucloxacillin; metoclopramide/domperidone increase absorption speed; cholestyramine reduces absorption; warfarin prolonged use; blood dyscrasias incl. thrombocytopenia and agranulocytosis (not known); NAC up to 24 h, maximal within 8 h."),
    (MERCK, "Merck Manual Professional, Acetaminophen Poisoning: toxicity requires ≥150 mg/kg within 24 h (~7.5–10 g adults); NAPQI formed by hepatic CYP450, detoxified by glutathione; overdose depletes glutathione causing hepatocellular necrosis; NAC most effective within 8 h."),
    (PH_KONSULTA, "PhilHealth Konsulta Annex D2 medicines list: paracetamol 300 mg and 500 mg tablets; 100 mg/mL drops 15 mL; 120 mg/5 mL (125 mg/5 mL) syrup/suspension 30/60/120 mL; 250 mg/5 mL syrup/suspension 30/60/120 mL; 125 mg and 250 mg suppositories. No brands."),
  ],
}
