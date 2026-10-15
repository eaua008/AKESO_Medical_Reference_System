SMPC_URL = "https://products.mhra.gov.uk/search/?search=omeprazole#emc-15127"
MSF_URL = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/omeprazole-oral-16684375.html"
EML_URL = "https://list.essentialmeds.org/medicines/178"

MED = {
  "id": "med_omeprazole",
  "desc_add": "WHO keeps omeprazole on the Essential Medicines List as an antiulcer medicine for GERD, peptic ulcer and gastrointestinal bleeding, in oral (10, 20, 40 mg; oral liquid) and 40 mg IV forms. The UK label also licenses it to treat and prevent NSAID-associated ulcers and, in children from 1 year (at least 10 kg), for reflux oesophagitis.",
  "facts": {
    "indication": [
      "Treatment of NSAID-associated gastric and duodenal ulcers, and prevention in at-risk patients (over 60, previous ulcer or upper GI bleed)",
      "Children from 1 year and at least 10 kg: reflux oesophagitis and symptomatic GERD",
      "Children over 4 years: H. pylori-associated duodenal ulcer (with antibiotics, specialist-supervised)",
    ],
    "adverse": [
      "Constipation",
      "Dizziness, paraesthesia, somnolence, insomnia",
      "Hyponatraemia (rare)",
      "Blurred vision and taste disturbance (rare)",
      "Hepatitis with or without jaundice (rare); hepatic encephalopathy in pre-existing liver disease (very rare)",
      "Microscopic colitis",
      "Severe skin reactions: SJS, TEN, DRESS, AGEP",
      "Leukopenia, thrombocytopenia (rare); agranulocytosis, pancytopenia (very rare)",
      "Gynaecomastia (very rare)",
      "Slightly increased risk of Salmonella and Campylobacter gut infections",
    ],
    "contraindication": [
      "Co-administration with nelfinavir",
    ],
    "interaction": [
      "Atazanavir: exposure markedly reduced; not recommended (if unavoidable, atazanavir/ritonavir 400/100 mg and omeprazole no more than 20 mg).",
      "Posaconazole, erlotinib, ketoconazole and itraconazole: absorption reduced by the higher gastric pH.",
      "Phenytoin, diazepam and cilostazol: levels may rise (CYP2C19); monitor phenytoin in the first 2 weeks and after stopping.",
      "Digoxin: bioavailability rises about 10%; take care at high doses in the elderly.",
      "Saquinavir/ritonavir: saquinavir levels raised up to about 70%.",
      "Voriconazole and clarithromycin: raise omeprazole exposure (voriconazole more than doubles it).",
      "Chromogranin A tests: stop omeprazole at least 5 days before testing (falsely raised CgA).",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Omeprazole 20 mg gastro-resistant capsules, hard. Summary of Product Characteristics. Zentiva Pharma UK Ltd; revised August 2025. electronic medicines compendium (emc).", SMPC_URL),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Omeprazole oral. MSF Medical Guidelines.", MSF_URL),
    ("WHO eEML", "World Health Organization. Electronic Essential Medicines List – Omeprazole (antiulcer medicines).", EML_URL),
  ],
  "links": [
    ("hiv_infection", "caution", "Contraindicated with nelfinavir and not recommended with atazanavir (UK SmPC); check the antiretroviral regimen."),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Omeprazole 20 mg gastro-resistant capsules. SmPC. Zentiva; August 2025.", SMPC_URL),
    ("MSF", "MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Omeprazole oral.", MSF_URL),
  ],
  "doses": [
    ("adult", "Duodenal ulcer", "PO", "20 mg", "Once a day", "2–4 weeks", "40 mg/day in poor responders", "Label · UK SmPC", ""),
    ("adult", "Gastric ulcer", "PO", "20 mg", "Once a day", "4–8 weeks", "40 mg/day in poor responders", "Label · UK SmPC", ""),
    ("adult", "Ulcer relapse prevention", "PO", "10–20 mg", "Once a day", "Long-term", "40 mg/day", "Label · UK SmPC", "H. pylori-negative or eradication not possible"),
    ("adult", "H. pylori eradication (with clarithromycin + amoxicillin or metronidazole)", "PO", "20 mg", "2× a day", "7 days", "—", "Label · UK SmPC", "Choose antibiotics by local resistance; repeat if still positive"),
    ("adult", "NSAID-associated ulcer, treatment", "PO", "20 mg", "Once a day", "4–8 weeks", "—", "Label · UK SmPC", ""),
    ("adult", "NSAID-associated ulcer, prevention (at-risk)", "PO", "20 mg", "Once a day", "While on NSAID", "—", "Label · UK SmPC", ""),
    ("adult", "Reflux oesophagitis", "PO", "20 mg", "Once a day", "4–8 weeks", "40 mg/day if severe", "Label · UK SmPC", ""),
    ("adult", "Healed reflux oesophagitis, maintenance", "PO", "10 mg", "Once a day", "Long-term", "20–40 mg/day", "Label · UK SmPC", ""),
    ("adult", "Symptomatic GERD", "PO", "10–20 mg", "Once a day", "4 weeks", "—", "Label · UK SmPC", "Investigate if not controlled after 4 weeks"),
    ("adult", "Zollinger-Ellison syndrome", "PO", "60 mg initially", "Once a day", "As needed", "Usual 20–120 mg/day", "Label · UK SmPC", "Split doses above 80 mg/day into 2"),
    ("child", "Reflux oesophagitis / GERD (≥1 y, 10–20 kg)", "PO", "10 mg", "Once a day", "4–8 weeks (GERD symptoms 2–4 weeks)", "20 mg/day", "Label · UK SmPC", ""),
    ("child", "Reflux oesophagitis / GERD (≥2 y, >20 kg)", "PO", "20 mg", "Once a day", "4–8 weeks (GERD symptoms 2–4 weeks)", "40 mg/day", "Label · UK SmPC", ""),
    ("child", "GERD (<5 kg)", "PO", "0.7–1.4 mg/kg", "Once a day", "3 days–8 weeks", "2.8 mg/kg/day", "MSF", "From dispersible 10 mg tablet as 1 mg/mL"),
    ("child", "GERD (5–10 kg)", "PO", "5 mg", "Once a day", "3 days–8 weeks", "—", "MSF", ""),
    ("child", "H. pylori duodenal ulcer (>4 y, 15–30 kg)", "PO", "10 mg", "2× a day", "7 days (up to 14)", "—", "Label · UK SmPC", "With amoxicillin 25 mg/kg + clarithromycin 7.5 mg/kg 2× a day"),
    ("child", "H. pylori duodenal ulcer (>4 y, 31–40 kg)", "PO", "20 mg", "2× a day", "7 days (up to 14)", "—", "Label · UK SmPC", "With amoxicillin 750 mg + clarithromycin 7.5 mg/kg 2× a day"),
    ("child", "H. pylori duodenal ulcer (>4 y, >40 kg)", "PO", "20 mg", "2× a day", "7 days (up to 14)", "—", "Label · UK SmPC", "With amoxicillin 1 g + clarithromycin 500 mg 2× a day"),
  ],
  "notes": [
    ("renal", "No dose adjustment needed.", "", "Label · UK SmPC"),
    ("hepatic", "10–20 mg daily may be sufficient.", "", "Label · UK SmPC"),
    ("hepatic", "Severe hepatic impairment: do not exceed 0.7 mg/kg daily (max 20 mg daily).", "Severe", "MSF"),
    ("elderly", "No dose adjustment needed.", "", "Label · UK SmPC"),
    ("pregnancy", "Over 1,000 exposed pregnancies showed no adverse effects; can be used in pregnancy. Passes into breast milk but unlikely to affect the infant at therapeutic doses.", "", "Label · UK SmPC"),
    ("administration", "Take in the morning, swallowed whole with half a glass of water; do not chew or crush. If swallowing is difficult, open the capsule and mix the pellets with water or a slightly acidic liquid (fruit juice, applesauce); take within 30 minutes.", "", "Label · UK SmPC"),
    ("monitor", "Exclude malignancy first if there are alarm features (weight loss, recurrent vomiting, dysphagia, haematemesis, melaena).", "", "Label · UK SmPC"),
    ("monitor", "Long-term use (especially beyond 1 year): review regularly; consider magnesium levels (more so with digoxin or diuretics), vitamin B12, and calcium/vitamin D in patients at fracture risk.", "", "Label · UK SmPC"),
    ("monitor", "Stop if acute tubulointerstitial nephritis is suspected, or if SCLE-type skin lesions with joint pain appear.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (SMPC_URL, "Zentiva omeprazole 20 mg capsules SmPC (rev. 29 Aug 2025): indications incl. NSAID ulcers, children ≥1 y ≥10 kg reflux oesophagitis/GERD, >4 y H. pylori DU; all adult doses/durations above; child weight-band doses and H. pylori combos; renal/elderly no adjustment, hepatic 10–20 mg; administration (morning, whole, capsule opening, 30 min); contraindicated with nelfinavir; atazanavir not recommended (max 20 mg); posaconazole/erlotinib/keto-/itraconazole absorption reduced; digoxin +10%; phenytoin monitor 2 weeks; diazepam, cilostazol; saquinavir +70%; voriconazole doubles exposure; CgA stop 5 days; Salmonella/Campylobacter risk; hypomagnesaemia, B12, fractures, SCLE, AIN; AEs constipation, dizziness, paraesthesia, somnolence, insomnia, hyponatraemia, blurred vision, taste disturbance, hepatitis, microscopic colitis, SJS/TEN/DRESS/AGEP, leukopenia, thrombocytopenia, agranulocytosis, gynaecomastia; pregnancy >1,000 outcomes can be used; breastfeeding unlikely to affect infant."),
    (MSF_URL, "MSF omeprazole oral: 10 mg dispersible tablet, 20 mg capsule; GORD child <5 kg 0.7–1.4 mg/kg (max 2.8 mg/kg/day), 5–10 kg 5 mg, 10–20 kg 10 mg, >20 kg and adult 20 mg once daily; durations 3 days to 4–8 weeks; severe hepatic impairment max 0.7 mg/kg/day (max 20 mg)."),
    (EML_URL, "WHO eEML omeprazole: antiulcer medicines; oral liquid 1 mg/mL and 4 mg/mL powder, oral solid 10/20/40 mg, 40 mg IV vial; indications GERD, peptic ulcer, GI bleeding; added 2009."),
    ("https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf", "Read with offset 64000: text covers Midazolam to Moxifloxacin only; omeprazole entry not readable, so no forms_ph note."),
  ],
}
