SMPC_URL = "https://products.mhra.gov.uk/search/?search=clopidogrel#emc-15874"
PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"
HTA_URL = "https://hta.dost.gov.ph/wp-content/uploads/2025/05/HTA-Council-Preliminary-Recommendation-on-Ticagrelor-90mg-film-coated-tablet-for-ACS-02-May-2025-1-2.pdf"

MED = {
  "id": "med_clopidogrel",
  "desc_add": "Because the receptor block is irreversible, platelets stay affected for the rest of their lifespan (about 7–10 days); with 75 mg daily, inhibition starts on day 1 and reaches steady state between days 3 and 7, which is why a loading dose is used when a fast effect is needed. In the Philippines clopidogrel 75 mg tablets are on the PNF Essential Medicines List, and the DOST HTA Council used clopidogrel plus aspirin as the comparator when it did not recommend government financing of ticagrelor for ACS in 2025.",
  "facts": {
    "indication": [
      "ACS patients undergoing PCI with stenting (with aspirin)",
      "Moderate- to high-risk TIA (ABCD2 ≥4) or minor ischaemic stroke (NIHSS ≤3), started within 24 h with aspirin",
      "Atrial fibrillation with a vascular risk factor when a vitamin K antagonist is unsuitable and bleeding risk is low (with aspirin)",
    ],
    "adverse": [
      "Haematoma, nosebleed, bruising and bleeding at puncture sites (common)",
      "Diarrhoea, abdominal pain and dyspepsia (common)",
      "Thrombocytopenia, leucopenia and eosinophilia (uncommon)",
      "Headache, paraesthesia and dizziness (uncommon)",
      "Gastric and duodenal ulcer, haematuria and eye bleeding (uncommon)",
      "Acquired haemophilia (consider if isolated aPTT prolongation)",
    ],
    "contraindication": [
      "Severe hepatic impairment",
      "Past hypersensitivity to ticlopidine or prasugrel: check for cross-reactivity (precaution)",
      "Hereditary galactose intolerance, lactase deficiency or glucose-galactose malabsorption (tablets contain lactose) (precaution)",
      "Non-minor ischaemic stroke (NIHSS >4): dual antiplatelet therapy not recommended; start monotherapy only after the first 7 days (precaution)",
      "Children: not to be used (efficacy concerns) (precaution)",
      "Breastfeeding: stop breastfeeding during treatment (precaution)",
    ],
    "interaction": [
      "Other CYP2C19 inhibitors (fluvoxamine, fluoxetine, moclobemide, voriconazole, fluconazole, ticlopidine, carbamazepine, efavirenz): reduce active metabolite; avoid.",
      "Rifampicin (strong CYP2C19 inducer): avoid.",
      "Pantoprazole: can be used if a PPI is needed.",
      "Rosuvastatin: exposure about doubled after a 300 mg clopidogrel dose.",
      "Paclitaxel (CYP2C8 substrate): use with caution.",
      "Ritonavir- or cobicistat-boosted HIV therapy: concomitant use discouraged.",
      "Heparin, GP IIb/IIIa inhibitors, thrombolytics and pentoxifylline: added bleeding risk; oral anticoagulants not recommended together.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Clopidogrel 75 mg film-coated tablets – Summary of Product Characteristics. Dr. Reddy's Laboratories (UK) Ltd (PL 08553/0766). Electronic Medicines Compendium (emc), medicines.org.uk; updated August 2024.", SMPC_URL),
    ("Philippine National Formulary (PNF EML)", "Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.", PNF_URL),
    ("DOST HTA Philippines", "Health Technology Assessment Council. Call for Stakeholder Comments on the Preliminary Recommendation on Ticagrelor [90 mg film-coated tablet] as an Add-on to Aspirin for Adults with Acute Coronary Syndrome. Department of Science and Technology, HTA Philippines; 02 May 2025.", HTA_URL),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "UK SmPC: limited experience in renal impairment; use with caution"),
  ],
  "sources": [
    ("Label · UK SmPC", "UK SmPC (emc)", "Clopidogrel 75 mg film-coated tablets. Summary of Product Characteristics. Dr. Reddy's Laboratories (UK) Ltd; 2024.", SMPC_URL),
    ("PNF", "Philippine National Formulary – EML", "Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.", PNF_URL),
  ],
  "doses": [
    ("adult", "NSTE-ACS", "PO", "300 or 600 mg load, then 75 mg", "Once a day", "Up to 12 months", "—", "Label · UK SmPC", "With aspirin 75–100 mg; 600 mg load only if <75 y"),
    ("adult", "STEMI, medically treated / fibrinolysis", "PO", "300 mg load, then 75 mg", "Once a day", "At least 4 weeks", "—", "Label · UK SmPC", "With aspirin; >75 y: no loading dose"),
    ("adult", "Primary PCI", "PO", "600 mg load, then 75 mg", "Once a day", "Up to 12 months", "—", "Label · UK SmPC", "300 mg load if PCI within 24 h of fibrinolysis; caution ≥75 y"),
    ("adult", "TIA (ABCD2 ≥4) or minor stroke (NIHSS ≤3)", "PO", "300 mg load, then 75 mg", "Once a day", "21 days", "—", "Label · UK SmPC", "Start within 24 h with aspirin 75–100 mg; then single antiplatelet"),
    ("adult", "Recent MI, ischaemic stroke or PAD", "PO", "75 mg", "Once a day", "—", "—", "Label · UK SmPC", "Stroke: 7 days to <6 months after event"),
    ("adult", "Atrial fibrillation (VKA unsuitable)", "PO", "75 mg", "Once a day", "—", "—", "Label · UK SmPC", "With aspirin 75–100 mg"),
  ],
  "notes": [
    ("renal", "Limited experience; use with caution.", "", "Label · UK SmPC"),
    ("hepatic", "Contraindicated in severe hepatic impairment; otherwise limited experience, use with caution.", "", "Label · UK SmPC"),
    ("elderly", "NSTE-ACS: 600 mg load only under 75 y. STEMI medically treated over 75 y: no loading dose. Primary PCI ≥75 y: 600 mg load with caution.", "", "Label · UK SmPC"),
    ("pregnancy", "Preferably avoid (no clinical data). Stop breastfeeding during treatment.", "", "Label · UK SmPC"),
    ("administration", "Take with or without food. Missed dose: take if <12 h late; if >12 h, skip it and do not double.", "", "Label · UK SmPC"),
    ("administration", "Elective surgery: UK SmPC advises stopping 7 days before if an antiplatelet effect is not wanted.", "", "Label · UK SmPC"),
    ("forms_ph", "Tablet 75 mg.", "", "PNF"),
    ("monitor", "Watch for bleeding (black stools, bruising, nosebleeds, blood in urine), especially with aspirin, NSAIDs, SSRIs or anticoagulants.", "", "Label · UK SmPC"),
    ("monitor", "Suspected TTP (very rare, potentially fatal) needs urgent assessment and prompt treatment; check a platelet count.", "", "Label · UK SmPC"),
    ("monitor", "Unexplained isolated aPTT prolongation: test for acquired haemophilia.", "", "Label · UK SmPC"),
  ],
  "checked": [
    (SMPC_URL, "Dr. Reddy's SmPC (updated 12-Aug-2024): 4.1 incl. TIA/minor IS and AF; 4.2 NSTE-ACS 300/600 mg load up to 12 months, aspirin ≤100 mg, STEMI 300 mg load ≥4 weeks, primary PCI 600 mg (300 mg after fibrinolysis), TIA 21 days, AF, elderly loading rules, paediatrics not to be used, renal/hepatic limited experience caution, with/without food, missed dose 12 h; 4.3 severe hepatic impairment; 4.4 stop 7 days pre-surgery, NIHSS >4, acquired haemophilia/aPTT, TTP, thienopyridine cross-reactivity, lactose; 4.5 CYP2C19 inhibitors list, rifampicin, pantoprazole OK, rosuvastatin ~2x, paclitaxel/repaglinide, ritonavir/cobicistat, heparin/GP IIb/IIIa/thrombolytics/pentoxifylline; 4.6; 4.8 common/uncommon; 5.1 platelet lifespan 7–10 days, steady state day 3–7"),
    (PNF_URL, "Clopidogrel: Oral 75 mg tablet; no restriction note"),
    (HTA_URL, "DOST HTA Council preliminary recommendation (02 May 2025): aspirin and clopidogrel already on PNF; clopidogrel + aspirin comparator; ticagrelor not recommended for government financing for ACS"),
  ],
}
