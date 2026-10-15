SMPC = "https://products.mhra.gov.uk/search/?search=aspirin#emc-107619"
PNF = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
DOH = "https://doh.gov.ph/wp-content/uploads/2023/08/ao2012-0026-1.pdf"
WHO = "https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue"

MED = {
  "id": "med_aspirin",
  "desc_add": "In the Philippines, the DOH dengue case-management guidelines tell patients not to take aspirin, mefenamic acid or other NSAIDs during dengue and to use paracetamol instead, because these drugs raise bleeding risk. It is not recommended for children and adolescents under 16 except on medical advice (Reye's syndrome), and low-dose aspirin is not used as an analgesic, antipyretic or anti-inflammatory.",
  "facts": {
    "indication": [
      "Stable angina and history of unstable angina (prevention of cardiovascular events)",
      "Prevention of graft occlusion after coronary artery bypass grafting",
      "Coronary angioplasty (outside the acute phase)",
    ],
    "adverse": [
      "Tinnitus and reduced hearing",
      "Hyperuricaemia (low doses reduce uric acid excretion; may trigger gout)",
      "Kounis syndrome (allergic acute coronary syndrome)",
      "Thrombocytopenia, agranulocytosis, aplastic anaemia (rare)",
      "Severe skin reactions: Stevens-Johnson syndrome, Lyell's syndrome (rare)",
      "Renal impairment and acute renal failure",
      "Menorrhagia",
    ],
    "contraindication": [
      "Acute or recurrent peptic ulcer, or history of NSAID-related GI bleeding/perforation",
      "Severe hepatic, renal or cardiac insufficiency",
      "Doses above 100 mg/day in the third trimester of pregnancy",
      "Methotrexate above 15 mg/week",
      "Suspected or confirmed dengue (DOH/WHO: avoid aspirin and NSAIDs; use paracetamol)",
    ],
    "interaction": [
      "Alteplase: do not start aspirin within 24 h after thrombolysis for acute stroke.",
      "Probenecid and sulfinpyrazone: salicylates reverse their uricosuric effect (not recommended).",
      "Sulfonylureas and insulin: enhanced hypoglycaemic effect; dose adjustment may be needed.",
      "Digoxin and lithium: reduced renal excretion; monitor plasma levels.",
      "Acetazolamide: severe acidosis and CNS toxicity.",
      "Metamizole: may reduce the antiplatelet effect of aspirin.",
      "Valproate and phenytoin: altered protein binding and free drug levels.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Aspirin 75 mg Tablets. Summary of Product Characteristics. G.L. Pharma GmbH. electronic medicines compendium (emc); revised 03/08/2026.", SMPC),
    ("Philippine National Formulary (PhilHealth)", "Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.", PNF),
    ("Department of Health (Philippines)", "Department of Health. Administrative Order: Revised Dengue Clinical Case Management Guidelines 2011. Manila: DOH; 2012.", DOH),
    ("World Health Organization", "World Health Organization. Dengue and severe dengue. Fact sheet; 21 August 2025.", WHO),
  ],
  "links": [
    ("heart_failure", "caution", "Contraindicated in severe cardiac insufficiency."),
    ("chronic_kidney_disease", "caution", "Contraindicated in severe renal insufficiency; caution in moderate impairment and with diuretics/ACE inhibitors."),
    ("hypertension", "caution", "Caution in uncontrolled hypertension; may reduce the effect of antihypertensives."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Aspirin 75 mg Tablets SmPC, G.L. Pharma GmbH; revised 03/08/2026.", SMPC),
    ("PNF", "Philippine National Formulary (PhilHealth)", "PNF Essential Medicines List, 2022.", PNF),
    ("DOH 2012", "Department of Health (Philippines)", "Revised Dengue Clinical Case Management Guidelines 2011 (Administrative Order, 2012).", DOH),
  ],
  "doses": [
    ("adult", "Secondary prevention of MI, stable angina, post-CABG", "PO", "75–160 mg", "Once a day", "Long-term", "300 mg/day", "Label · UK SmPC", ""),
    ("adult", "Secondary prevention of TIA / ischaemic stroke", "PO", "75–300 mg", "Once a day", "Long-term", "300 mg/day", "Label · UK SmPC", "Start only after intracerebral haemorrhage is excluded"),
    ("adult", "Acute myocardial infarction", "PO", "150–300 mg loading, then 75–160 mg", "Once a day", "Long-term", "300 mg/day", "Label · UK SmPC", ""),
    ("child", "Under 16 years", "PO", "Not recommended", "—", "—", "—", "Label · UK SmPC", "Reye's syndrome risk; only on medical advice"),
  ],
  "notes": [
    ("renal", "Contraindicated in severe renal insufficiency; use with caution in moderate impairment or dehydration.", "", "Label · UK SmPC"),
    ("hepatic", "Contraindicated in severe hepatic insufficiency; in mild–moderate impairment use with caution and check liver function regularly.", "", "Label · UK SmPC"),
    ("elderly", "More prone to adverse effects; usual adult dose if no severe renal or hepatic insufficiency; review treatment regularly.", "", "Label · UK SmPC"),
    ("pregnancy", "Up to 100 mg/day appears safe for restricted obstetric use under specialist monitoring; higher doses contraindicated in the third trimester. Breastfeeding: short-term use acceptable; stop with long-term or high-dose use.", "", "Label · UK SmPC"),
    ("administration", "Swallow with about half a glass of water. Bleeding risk persists 4–8 days after stopping; temporary withdrawal may be needed before surgery, including tooth extraction.", "", "Label · UK SmPC"),
    ("administration", "Dengue: patients should not take aspirin, mefenamic acid or other NSAIDs; use paracetamol (max 4 g/day in adults). Those already on these drugs should consult their doctor.", "", "DOH 2012"),
    ("forms_ph", "Aspirin oral tablets 80 mg, 100 mg, 300 mg and 325 mg.", "", "PNF"),
    ("monitor", "Signs of GI bleeding (black stools, haematemesis) and anaemia; gout flares; renal function when combined with diuretics, ACE inhibitors or ARBs; blood glucose with sulfonylureas or insulin.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (PNF, "PNF-EML lists 'Aspirin Oral: 80 mg, 100 mg tablet, 300 mg tablet and 325mg tablet'."),
    (SMPC, "Aspirin 75 mg Tablets SmPC (G.L. Pharma, rev 03/08/2026): indications incl. CABG graft occlusion, angioplasty, stable/unstable angina; doses 75–160 mg od, TIA/CVA 75–300 mg, acute MI 150–300 mg load then 75–160 mg, not exceed 300 mg/day; not under 16 (Reye's); contraindications (ulcers, severe hepatic/renal/cardiac insufficiency, >100 mg/day 3rd trimester, MTX >15 mg/week); interactions (alteplase 24 h, probenecid, antidiabetics, digoxin/lithium, acetazolamide, metamizole, valproate/phenytoin); ADRs incl. tinnitus, hyperuricaemia, Kounis syndrome, blood dyscrasias, SJS/Lyell, renal failure, menorrhagia; bleeding effect 4–8 days; caution uncontrolled hypertension."),
    (DOH, "DOH AO 'Revised Dengue Clinical Case Management Guidelines 2011' (signed Sec. Enrique T. Ona; AO number garbled in text): Home Care Card 'Do not take NSAIDs, e.g. acetylsalicylic acid (aspirin)/mefenamic acid or steroids'; paracetamol not more than 4 g/day in adults; 'If you are already taking these medications, please consult your doctor'."),
    (WHO, "WHO dengue fact sheet (21 Aug 2025): 'Non-steroidal anti-inflammatory medicines such as ibuprofen and aspirin should be avoided as they can increase the risk of bleeding'; paracetamol for pain."),
  ],
}
