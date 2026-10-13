T625_URL = "https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-281"
T875_URL = "https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10877"
SUSP_URL = "https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10038"
MSF_URL = "https://medicalguidelines.msf.org/en/viewport/EssDr/english/amoxicillin-clavulanic-acid-co-amoxiclav-oral-16685119.html"
PNF_URL = "https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf"

MED = {
  "id": "med_coamoxiclav",
  "desc_add": "Both components are about 70% absorbed orally and have half-lives of about 1 hour, which is why it is given two or three times a day; amoxicillin does not reach adequate levels in the cerebrospinal fluid. MSF uses it as second-line treatment for otitis media and sinusitis when high-dose amoxicillin has failed, and the UK label advises switching to plain amoxicillin once an infection is shown to be amoxicillin-susceptible. In the Philippines it is on the PNF Essential Medicines List as tablets and oral suspensions.",
  "facts": {
    "indication": [
      "Bone and joint infections, including osteomyelitis",
      "Severe dental abscess with spreading cellulitis",
      "Postpartum upper genital tract infection",
      "Oral step-down after IV treatment of severe infections (e.g., severe pneumonia)",
      "Acute uncomplicated cystitis in girls over 2 years (MSF)",
    ],
    "adverse": [
      "Mucocutaneous candidosis (common); dizziness, headache and indigestion (uncommon)",
      "Reversible leucopenia, neutropenia and thrombocytopenia (rare); agranulocytosis and haemolytic anaemia",
      "Drug-induced enterocolitis syndrome (DIES), mainly in children: protracted vomiting 1–4 h after a dose",
      "Haemophagocytic lymphohistiocytosis (HLH)",
      "Kounis syndrome (allergic acute coronary syndrome)",
      "Severe skin reactions: SJS, TEN, AGEP and DRESS",
      "Convulsions (with renal impairment or high doses) and aseptic meningitis",
      "Interstitial nephritis and crystalluria with acute kidney injury",
      "Acute pancreatitis and black hairy tongue",
    ],
    "contraindication": [
      "Infections likely caused by penicillin-resistant S. pneumoniae or non-inhibitable beta-lactamases: not suitable (precaution)",
      "Children under 25 kg must not be given tablets; use suspension (precaution)",
      "Cephalosporin allergy: possible cross-sensitivity, use with caution (precaution)",
    ],
    "interaction": [
      "Methotrexate: penicillins may reduce methotrexate excretion and increase toxicity.",
      "Mycophenolate mofetil: pre-dose mycophenolic acid levels fall by about 50%; monitor graft function closely.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("UK SmPC (emc)", "Augmentin 625 mg Tablets – Summary of Product Characteristics. GlaxoSmithKline UK; text revised 24 February 2026. Electronic Medicines Compendium (emc), medicines.org.uk.", T625_URL),
    ("UK SmPC (emc)", "Co-amoxiclav 875 mg/125 mg film-coated Tablets – Summary of Product Characteristics. Brown & Burk UK Ltd; text revised 19 September 2025. emc, medicines.org.uk.", T875_URL),
    ("UK SmPC (emc)", "Augmentin Duo 400/57 powder for oral suspension – Summary of Product Characteristics. GlaxoSmithKline UK; text revised 6 January 2026. emc, medicines.org.uk.", SUSP_URL),
    ("MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Amoxicillin/clavulanic acid = co-amoxiclav, oral. MSF Medical Guidelines.", MSF_URL),
    ("Philippine National Formulary (PNF EML)", "Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.", PNF_URL),
  ],
  "links": [
    ("chronic_kidney_disease", "caution", "Renally cleared: reduce to 500/125 mg 2× a day (CrCl 10–30) or once a day (CrCl <10); 7:1 forms (875/125 mg) not recommended if CrCl <30; convulsion risk"),
    ("rabies", "safe", "Used for animal-bite wound treatment/prophylaxis (MSF, UK SmPC); it does not treat rabies itself and is given alongside rabies post-exposure care (our inference)"),
  ],
  "sources": [
    ("Label · UK SmPC 625", "UK SmPC (emc)", "Augmentin 625 mg Tablets (500/125 mg). Summary of Product Characteristics. GlaxoSmithKline UK; 2026.", T625_URL),
    ("Label · UK SmPC 875", "UK SmPC (emc)", "Co-amoxiclav 875 mg/125 mg film-coated Tablets. Summary of Product Characteristics. Brown & Burk UK Ltd; 2025.", T875_URL),
    ("Label · UK SmPC susp", "UK SmPC (emc)", "Augmentin Duo 400/57 powder for oral suspension. Summary of Product Characteristics. GlaxoSmithKline UK; 2026.", SUSP_URL),
    ("MSF", "MSF Essential Drugs", "Médecins Sans Frontières. Essential drugs – Co-amoxiclav oral.", MSF_URL),
    ("PNF", "Philippine National Formulary – EML", "Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.", PNF_URL),
  ],
  "doses": [
    ("adult", "Most infections (4:1 tablet)", "PO", "500/125 mg", "Every 8 h", "Per response; review if >14 days", "1500/375 mg/day", "Label · UK SmPC 625", "Also children ≥40 kg"),
    ("adult", "Most infections (7:1 tablet)", "PO", "875/125 mg", "2× a day", "Per response; review if >14 days", "1750/250 mg/day", "Label · UK SmPC 875", "Also children ≥40 kg"),
    ("adult", "Otitis media, sinusitis, LRTI, UTI (higher dose)", "PO", "875/125 mg", "Every 8 h", "Per response; review if >14 days", "2625/375 mg/day", "Label · UK SmPC 875", ""),
    ("adult", "Animal bites", "PO", "875/125 mg", "2× a day", "5–7 days", "—", "MSF", "8:1 form: 1000/125 mg 2× a day"),
    ("adult", "Otitis media / sinusitis after amoxicillin failure", "PO", "875/125 mg", "2× a day", "5 days (otitis); 7–10 days (sinusitis)", "—", "MSF", "8:1 form: 1000/125 mg 2× a day"),
    ("adult", "Postpartum upper genital tract infection", "PO", "875/125 mg", "Every 8 h", "7 days", "—", "MSF", "8:1 form: 1000/125 mg every 8 h"),
    ("adult", "IV-to-oral switch, severe pneumonia", "PO", "875/125 mg", "Every 8 h", "10–14 days total", "—", "MSF", "8:1 form: 1000/125 mg every 8 h"),
    ("child", "Most infections, <40 kg (4:1 forms)", "PO", "20–60 mg/kg/day ÷ 3", "Every 8 h", "Per response; review if >14 days", "2400/600 mg/day", "Label · UK SmPC 625", "Tablets only if ≥25 kg; <2 y may need 4:1 suspension"),
    ("child", "Most infections, <40 kg (7:1 forms)", "PO", "25–45 mg/kg/day ÷ 2", "2× a day", "Per response; review if >14 days", "—", "Label · UK SmPC susp", "No data under 2 months"),
    ("child", "Otitis media, sinusitis, LRTI (higher dose, 7:1)", "PO", "45–70 mg/kg/day ÷ 2", "2× a day", "Per response", "70 mg/kg/day", "Label · UK SmPC susp", "Not >45 mg/kg/day under 2 years"),
    ("child", "Animal bites; otitis/sinusitis after amoxicillin failure", "PO", "25 mg/kg", "2× a day", "5–7 days (bites); 5 days (otitis); 7–10 days (sinusitis)", "—", "MSF", "Clavulanate ≤12.5 mg/kg/day"),
    ("child", "Uncomplicated cystitis (girls >2 y)", "PO", "12.5 mg/kg", "2× a day", "3 days", "—", "MSF", ""),
    ("child", "IV-to-oral switch, severe infections", "PO", "50 mg/kg", "2× a day", "10–14 days total (pneumonia)", "—", "MSF", "7:1 or 8:1 forms; clavulanate ≤12.5 mg/kg/day"),
  ],
  "notes": [
    ("renal", "No dose adjustment.", "CrCl >30", "Label · UK SmPC 625"),
    ("renal", "500/125 mg 2× a day; children <40 kg 15/3.75 mg/kg 2× a day (max 500/125 mg per dose).", "CrCl 10–30", "Label · UK SmPC 625"),
    ("renal", "500/125 mg once a day; children <40 kg 15/3.75 mg/kg once a day (max 500/125 mg).", "CrCl <10", "Label · UK SmPC 625"),
    ("renal", "500/125 mg every 24 h, plus one dose during dialysis and another at the end; children 15/3.75 mg/kg before and after dialysis.", "Haemodialysis", "Label · UK SmPC 625"),
    ("renal", "7:1 forms (875/125 mg tablet, 400/57 mg suspension) are not recommended; use a 4:1 form.", "CrCl <30", "Label · UK SmPC 875"),
    ("hepatic", "Use with caution and monitor liver function regularly. Liver injury is more common in males, the elderly and with long courses, and may appear weeks after stopping.", "", "Label · UK SmPC 625"),
    ("elderly", "No dose adjustment; check renal function and adjust if impaired.", "", "Label · UK SmPC 625"),
    ("pregnancy", "UK label: avoid unless essential (necrotising enterocolitis reported in newborns after use for preterm premature rupture of membranes); passes into breast milk (diarrhoea, thrush in the infant). MSF: not contraindicated in pregnancy or breastfeeding.", "", "Label · UK SmPC 625"),
    ("administration", "Tablets cannot be divided; children ≤6 years or <25 kg should get suspension. Reconstituted suspension: keep at 2–8 °C, use within 7 days, shake before each dose.", "", "Label · UK SmPC susp"),
    ("forms_ph", "Tablets 500 mg + 125 mg, 875 mg + 125 mg; granules/powder for suspension 200 mg + 28.5 mg/5 mL (70 mL), 400 mg + 57 mg/5 mL (70 mL), 600 mg + 42.9 mg/5 mL.", "", "PNF"),
    ("monitor", "Check liver tests, renal function and blood counts during prolonged courses.", "", "Label · UK SmPC 625"),
    ("monitor", "On warfarin/acenocoumarol: check INR when starting and stopping; on mycophenolate: watch graft function.", "", "Label · UK SmPC 625"),
    ("monitor", "Children: protracted vomiting 1–4 h after a dose suggests DIES; stop the drug.", "", "Label · UK SmPC 625"),
  ],
  "checked": [
    (T625_URL, "Augmentin 625 (GSK, text rev. 24 Feb 2026): 4.1 incl. bone/joint, dental abscess with cellulitis; 4.2 500/125 mg 3× daily, max 1500/375; children <40 kg 20–60 mg/kg/day ÷3, max 2400/600; tablets not <25 kg; renal table (10–30 2× daily, <10 once daily, HD regimen, paediatric 15/3.75 mg/kg); hepatic caution; 4.4 DIES, HLH, Kounis, AGEP, convulsions, hepatic events (males/elderly/prolonged, weeks after), switch to amoxicillin, not for PRSP, periodic renal/hepatic/haematological monitoring; 4.5 methotrexate, mycophenolate ~50% fall, anticoagulant INR, probenecid; 4.6 NEC in PPROM, breast milk; 4.8 frequencies incl. pancreatitis, black hairy tongue, interstitial nephritis, crystalluria, aseptic meningitis; 5.2 ~70% bioavailability, t½ ~1 h, poor CSF penetration"),
    (T875_URL, "Co-amoxiclav 875/125 (Brown & Burk, rev. 19 Sep 2025): adults 875/125 2× daily (max 1750/250), higher dose 3× daily for otitis/sinusitis/LRTI/UTI (max 2625/375); children 25–45 mg/kg/day ÷2, up to 70 mg/kg/day; 7:1 not recommended CrCl <30; take with a meal"),
    (SUSP_URL, "Augmentin Duo 400/57 (GSK, rev. 6 Jan 2026): children 25–45 mg/kg/day ÷2, higher 45–70 mg/kg/day ÷2 for otitis/sinusitis/LRTI; under 2 y not >45 mg/kg/day; no data <2 months; ≤6 y prefer suspension; reconstituted at 2–8 °C, 7 days"),
    (MSF_URL, "MSF co-amoxiclav oral: indications (animal bites, 2nd-line AOM/sinusitis after high-dose amoxicillin, cystitis girls >2 y, postpartum upper genital infection, IV-to-oral switch); doses 25/12.5/50 mg/kg 2× daily, adult 875/125 2× or 3× daily (8:1: 2 × 500/62.5); durations; clavulanate ≤12.5 mg/kg/day or 375 mg/day; cephalosporin cross-sensitivity; not contraindicated in pregnancy/breastfeeding"),
    (PNF_URL, "PNF EML lists co-amoxiclav 500+125 mg and 875+125 mg tablets; 200+28.5 mg/5 mL (70 mL), 400+57 mg/5 mL (70 mL), 600+42.9 mg/5 mL suspensions; no IV form listed"),
  ],
}
