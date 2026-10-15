# Medicine review b03: review sheet

Run `035_medicines_review_03.sql` in Supabase after you have checked this. Everything below is ADDED; the existing text stays as it is.

Every link was opened twice: by the research step (to read the fact), and again in Akeso's own browser pane on your computer in the Philippines (to make sure it opens for you, not just from the cloud). See NOTES.md in the batch folder for any link that needs attention.

UK SmPC links open the official MHRA Products search (free) for that medicine: the emc site (medicines.org.uk) now limits free page views for users outside the UK. The citation still names the exact product and PL number to pick.

## Please check (batch 03)

- **Dexamethasone:** the UK injection label gives doses as dexamethasone *base* (3.3 mg base = 4 mg phosphate); PH products say "as sodium phosphate". This is explained in a note. Most caution links (diabetes, hypertension, TB, ulcers…) come from the label's "monitor closely" list. Meningitis doses come from Merck (4 days).
- **Doxycycline:** the UK label says not under 8 years or in pregnancy; the CDC uses it at any age for rickettsial disease. Both are noted. PhilHealth's leptospirosis table gives no treatment duration.
- **Enalapril:** no Philippine or WHO guideline that names drugs could be opened.
- **Ethambutol:** PH weight bands are from the NTP Manual 5th ed. (2014); a newer manual may differ but couldn't be opened. The **type 2 diabetes** link applies only when there is retinopathy (inference, noted).
- **Famotidine:** no oral child dose (the US label couldn't be read); only the IV child dose.
- **Ferrous sulfate:** the PH DOH pregnancy dose (60 mg iron + 0.4 mg folic acid, ≥180 days) is quoted from a 2021 peer-reviewed paper citing DOH AO 2010-0010, because no DOH page opened.
- **Furosemide:** ⚠ the existing link *chronic kidney disease: safe* conflicts with the UK label (contraindicated at CrCl < 30). Please review that old link. The new *avoid* links to gastroenteritis and cholera are inferred from the "dehydration/hypovolaemia" contraindication.
- **Hydrochlorothiazide:** the child dose comes from an old (2007) US label already in its refs. Pregnancy: MSF says contraindicated; the US label says "not routine".
- **Gliclazide:** maximum 240 mg/day (MSF) vs 320 mg/day (UK) – separate rows.


---

## Dexamethasone  (`med_dexamethasone`)

**Description (kept)**

Dexamethasone is a potent, long-acting glucocorticoid with almost no mineralocorticoid effect. It suppresses inflammatory gene transcription and cytokine release. In bacterial meningitis, given just before or with the first antibiotic dose, it reduces inflammation-driven brain injury, hearing loss and death, with the clearest benefit in pneumococcal meningitis.

**Description (added)**

Dexamethasone also induces CYP3A4, so it can lower levels of drugs such as indinavir, saquinavir and erythromycin. WHO recommends low-dose corticosteroids for 7–10 days only in severe or critical COVID-19 and advises against them in non-severe disease. In the Philippines, the PNF lists 500 microgram, 750 microgram, 3 mg and 4 mg tablets, 4 mg/mL and 5 mg/mL injections (as sodium phosphate, IM/IV) and 0.1% eye drops.

**Uses**: 6 kept, 4 added

- NEW: Dexamethasone suppression test (investigation of Cushing's syndrome)
- NEW: Adjunct in haemorrhagic, traumatic or surgical shock
- NEW: Intra-articular and soft-tissue injection
- NEW: Palliative care (subcutaneous injection or infusion)

**Side effects**: 5 kept, 6 added

- NEW: Severe psychiatric reactions, including psychosis, sometimes during dose tapering
- NEW: Cataract, glaucoma and central serous chorioretinopathy (blurred vision)
- NEW: Growth retardation in children (dose-related, may be irreversible)
- NEW: Acute adrenal insufficiency on abrupt withdrawal after prolonged use
- NEW: Hypertension and hypokalaemia
- NEW: Burning or tingling in the perineal area after IV injection

**Precautions**: 3 kept, 5 added

- NEW: Systemic infection unless specific anti-infective therapy is given
- NEW: Chickenpox or measles exposure in non-immune patients: risk of severe disease; needs immunoglobulin (precaution)
- NEW: Amoebiasis and other parasitic infestations (precaution)
- NEW: Recent myocardial infarction: risk of myocardial rupture (precaution)
- NEW: Phaeochromocytoma: may trigger crisis (precaution)

**Interactions**: 4 kept, 9 added

- NEW: Ritonavir and cobicistat: raise corticosteroid levels and side effects; avoid unless benefit outweighs risk.
- NEW: Indinavir, saquinavir and erythromycin: levels lowered by dexamethasone (CYP3A4 induction).
- NEW: Phenobarbital, primidone, rifabutin and ephedrine: reduce dexamethasone effect.
- NEW: Loop and thiazide diuretics, acetazolamide: enhanced hypokalaemia.
- NEW: Antihypertensives and diuretics: effects antagonised.
- NEW: Methotrexate: increased haematological toxicity.
- NEW: Salicylates: renal clearance increased; salicylate toxicity possible when the steroid is stopped.
- NEW: Antacids (especially magnesium trisilicate): reduce absorption; space doses apart.
- NEW: Anticholinesterases: effect antagonised in myasthenia gravis.

**Disease links added**

- `covid19`: **safe**: WHO: recommended for severe or critical COVID-19 for 7–10 days; should not be given in non-severe COVID-19
- `type2_diabetes`: **caution**: UK label: frequent monitoring in diabetes; antagonises insulin and oral hypoglycaemics
- `hypertension`: **caution**: UK label: frequent monitoring in hypertension; antagonises antihypertensives
- `heart_failure`: **caution**: UK label: frequent monitoring in congestive heart failure
- `tuberculosis`: **caution**: UK label: frequent monitoring with a history of tuberculosis
- `peptic_ulcer_disease`: **caution**: UK label: frequent monitoring in peptic ulceration
- `chronic_kidney_disease`: **caution**: UK label: frequent monitoring in renal insufficiency (no dose change needed)
- `varicella`: **caution**: UK label: chickenpox can be fatal in immunosuppressed patients; non-immune exposed patients need VZIG within 10 days
- `measles`: **caution**: UK label: avoid exposure; exposed patients may need IM normal immunoglobulin
- `acute_coronary_syndrome`: **caution**: UK label: caution after recent myocardial infarction (myocardial rupture reported)

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | General glucocorticoid use (Taper to lowest effective dose; stop if no response within a few days) | PO | 0.5–10 mg/day | Once a day or divided | As short as possible | — | Label · UK SmPC tabs |
| adult | Bacterial meningitis (adjunct) (First dose just before or with the first antibiotic dose) | IV | 10 mg | Every 6 h | 4 days | — | Merck Manual |
| adult | COVID-19 needing oxygen (WHO: severe/critical only, 7–10 days) | PO | 6 mg | Once a day | Up to 10 days | — | Label · UK SmPC tabs |
| adult | COVID-19 needing oxygen | IV | 6 mg | Once a day | Up to 10 days | — | Label · UK SmPC inj |
| adult | Cerebral oedema (tumour, pre-op) (Dose as dexamethasone base) | IV | 8.3 mg, then 3.3 mg IM | Every 6 h (IM) | Reduce after 2–4 days; stop over 5–7 days | — | Label · UK SmPC inj |
| adult | Emergency use (IV only in shock; IM possible otherwise; dose as base) | IV | 3.3–16.6 mg | Repeat until response | Short term | 66.4 mg/day | Label · UK SmPC inj |
| adult | Shock (haemorrhagic, traumatic, surgical) (Adjunct to standard therapy) | IV | 1.7–5 mg/kg | Single dose; repeat in 2–6 h if needed | Usually ≤48–72 h | — | Label · UK SmPC inj |
| adult | Palliative care | SC | 4–16 mg/24 h | Injection or continuous infusion | As needed | — | Label · UK SmPC inj |
| adult | Antenatal lung maturation (24–34 weeks) (Repeat course may be considered if <34 weeks and ≥7 days since last) | IM | 6 mg | Every 12 h | 4 doses | — | Merck Manual (obstetrics) |
| adult | Dexamethasone suppression test (short) (Measure plasma cortisol the next morning) | PO | 1 mg | Once at 11 pm | Once | — | Label · UK SmPC tabs |
| child | General glucocorticoid use | PO | 0.01–0.1 mg/kg/day | Once a day or divided | As short as possible | — | Label · UK SmPC tabs |
| child | Bacterial meningitis (adjunct) (First dose just before or with the first antibiotic dose) | IV | 0.15 mg/kg | Every 6 h | 4 days | — | Merck Manual |
| child | Croup (mild to severe) (IM if persistent vomiting or marked respiratory distress) | PO | 0.6 mg/kg | Single dose | Once | — | CPS |
| child | COVID-19 needing oxygen (≥12 y and ≥40 kg) | PO | 6 mg | Once a day | Up to 10 days | — | Label · UK SmPC tabs |

- *renal*: No dose adjustment, but monitor frequently in renal insufficiency. [Label · UK SmPC tabs]
- *hepatic*: No dose adjustment, but monitor frequently in liver failure. [Label · UK SmPC tabs]
- *elderly*: Osteoporosis, hypertension, hypokalaemia, diabetes, infection and skin thinning may be more serious; plan long-term use carefully under close supervision. [Label · UK SmPC tabs]
- *pregnancy*: Crosses the placenta; no rise in birth defects seen, but prolonged or repeated use may increase intrauterine growth restriction and neonatal hypoadrenalism is possible. Infants of mothers on high, prolonged doses may have some adrenal suppression. [Label · UK SmPC tabs]
- *administration*: After prolonged use, taper gradually; consider gradual withdrawal after repeated courses, doses over 6 mg/day, evening dosing or more than 3 weeks of treatment. [Label · UK SmPC tabs]
- *administration*: UK injection doses are given as dexamethasone base (3.3 mg base = 4 mg dexamethasone phosphate); Philippine products are labelled as sodium phosphate, so check the label. Max 2 mL IM per site; may be added to sodium chloride or dextrose infusion; use with caution at high doses in children under 5 (propylene glycol). [Label · UK SmPC inj]
- *forms_ph*: Oral: 500 microgram, 750 microgram, 3 mg and 4 mg tablet. Injection (IM/IV, as sodium phosphate): 4 mg/mL in 1 mL and 2 mL ampoule/vial; 5 mg/mL in 1 mL ampoule. Eye drops suspension: 0.1%, 5 mL. [PNF]
- *monitor*: Blood glucose, blood pressure and potassium; mood and psychiatric symptoms (warn patient and carers); blurred vision (refer to eye specialist); growth in children; signs of infection, which may be masked; INR with coumarin anticoagulants. [Label · UK SmPC tabs]

**References added**

- [UK SmPC (emc) – tablets](https://products.mhra.gov.uk/search/?search=dexamethasone#emc-5411): Dexamethasone Tablets BP 2.0 mg – Summary of Product Characteristics. Aspen Pharma Trading Limited (PL 39699/0056). Electronic Medicines Compendium (emc), medicines.org.uk.
- [UK SmPC (emc) – injection](https://products.mhra.gov.uk/search/?search=dexamethasone#emc-4659): Dexamethasone 3.3 mg/ml Solution for Injection – Summary of Product Characteristics. hameln pharma ltd (PL 01502/0079). Electronic Medicines Compendium (emc), medicines.org.uk.
- [Merck Manual Professional – Acute bacterial meningitis](https://www.merckmanuals.com/professional/neurologic-disorders/meningitis/acute-bacterial-meningitis): Merck Manual Professional Version. Acute Bacterial Meningitis.
- [WHO – COVID-19 corticosteroids Q&A](https://www.who.int/news-room/questions-and-answers/item/coronavirus-disease-covid-19-dexamethasone): World Health Organization. Coronavirus disease (COVID-19): Corticosteroids, including dexamethasone. Questions and answers.
- [Canadian Paediatric Society – Croup](https://cps.ca/documents/position/acute-management-of-croup): Ortiz-Alvarez O; Canadian Paediatric Society, Acute Care Committee. Acute management of croup in the emergency department. Position statement, 2017 (updated 2026).
- Dosing source `PNF`: [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.
- Dosing source `Label · UK SmPC tabs`: [UK SmPC – Dexamethasone Tablets BP 2.0 mg](https://products.mhra.gov.uk/search/?search=dexamethasone#emc-5411): Aspen Pharma Trading Ltd. Dexamethasone Tablets BP 2.0 mg – Summary of Product Characteristics. emc.
- Dosing source `Label · UK SmPC inj`: [UK SmPC – Dexamethasone 3.3 mg/ml Solution for Injection](https://products.mhra.gov.uk/search/?search=dexamethasone#emc-4659): hameln pharma ltd. Dexamethasone 3.3 mg/ml Solution for Injection – Summary of Product Characteristics. emc.
- Dosing source `Merck Manual`: [Merck Manual Professional – Acute Bacterial Meningitis](https://www.merckmanuals.com/professional/neurologic-disorders/meningitis/acute-bacterial-meningitis): Merck Manual Professional Version. Acute Bacterial Meningitis.
- Dosing source `Merck Manual (obstetrics)`: [Merck Manual Professional – Preterm Labor](https://www.merckmanuals.com/professional/gynecology-and-obstetrics/abnormalities-and-complications-of-labor-and-delivery/preterm-labor): Merck Manual Professional Version. Preterm Labor.
- Dosing source `CPS`: [Canadian Paediatric Society – Acute management of croup](https://cps.ca/documents/position/acute-management-of-croup): Ortiz-Alvarez O; CPS Acute Care Committee. Acute management of croup in the emergency department. 2017 (updated 2026).
- Dosing source `WHO`: [WHO – COVID-19: Corticosteroids, including dexamethasone](https://www.who.int/news-room/questions-and-answers/item/coronavirus-disease-covid-19-dexamethasone): World Health Organization. Coronavirus disease (COVID-19): Corticosteroids, including dexamethasone. Q&A.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=dexamethasone#emc-5411: Aspen dexamethasone 2 mg tablets SmPC: 4.1 cerebral oedema adjunct, COVID-19 ≥12 y ≥40 kg on oxygen; 4.2 adult 0.5–10 mg/day, child 0.01–0.1 mg/kg/day, COVID 6 mg once daily up to 10 days, suppression test 1 mg 11 pm, no adjustment elderly/renal/hepatic; 4.3 systemic infection, live vaccines; 4.4 withdrawal rules (>6 mg/day, 3 weeks), chickenpox/VZIG within 10 days, measles, psychiatric, eye (cataract, glaucoma, CSCR), phaeochromocytoma, recent MI, growth retardation, frequent monitoring list (osteoporosis, hypertension/CHF, diabetes, TB history, glaucoma, liver failure, renal insufficiency, epilepsy, peptic ulceration), amoebiasis; 4.5 inducers incl. phenobarbital/primidone/rifabutin/ephedrine, ritonavir/cobicistat, indinavir/saquinavir/erythromycin lowered, antihypertensives/hypoglycaemics/diuretics antagonised, K-depleting agents, anticholinesterases, coumarins, methotrexate, salicylates, antacids; 4.6 pregnancy/lactation; elderly statement
- https://products.mhra.gov.uk/search/?search=dexamethasone#emc-4659: hameln dexamethasone 3.3 mg/ml injection SmPC: doses as base (3.32 mg base = 4 mg phosphate); emergency 3.3–16.6 mg, max 66.4 mg/day; COVID 6 mg IV daily up to 10 days; shock 1.7–5 mg/kg IV, ≤48–72 h; cerebral oedema 8.3 mg IV then 3.3 mg IM q6h, reduce after 2–4 days, stop over 5–7 days; SC palliative 4–16 mg/24 h; intra-articular doses; max 2 mL IM per site; propylene glycol caution <5 y; perineal burning after IV (4.8)
- https://www.merckmanuals.com/professional/neurologic-disorders/meningitis/acute-bacterial-meningitis: Dexamethasone adults 10 mg IV, children 0.15 mg/kg IV, immediately before or with first antibiotic dose and every 6 h for 4 days; best established in pneumococcal meningitis
- https://www.merckmanuals.com/professional/gynecology-and-obstetrics/abnormalities-and-complications-of-labor-and-delivery/preterm-labor: Dexamethasone 6 mg IM every 12 h for 4 doses at 24–34 weeks; repeat course if <34 weeks and last course ≥7 days prior
- https://cps.ca/documents/position/acute-management-of-croup: Dexamethasone 0.6 mg/kg oral single dose for all croup severities; IM if persistent vomiting or significant distress; no mg maximum stated
- https://www.who.int/news-room/questions-and-answers/item/coronavirus-disease-covid-19-dexamethasone: Corticosteroids recommended for severe/critical COVID-19, low dose for 7–10 days; should not be given in non-severe COVID-19
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Dexamethasone 500 mcg, 750 mcg, 3 mg, 4 mg tablet; 4 mg/mL 1 and 2 mL and 5 mg/mL 1 mL ampul/vial IM/IV (as sodium phosphate); 0.1% eye drops 5 mL
- https://www.who.int/publications/i/item/9789240108042: WHO 2025 meningitis guideline landing page; no dexamethasone detail on page and PDF did not load - not used

---

## Doxycycline  (`med_doxycycline`)

**Description (kept)**

Doxycycline binds the 30S ribosomal subunit and blocks aminoacyl-tRNA binding, inhibiting bacterial protein synthesis (bacteriostatic). It is used for rickettsial infections, leptospirosis, atypical pneumonia, chlamydia, Lyme disease, acne and malaria prophylaxis.

**Description (added)**

Oral doxycycline is virtually completely absorbed, and food or milk does not notably reduce absorption. About 40% is excreted in the urine over 72 hours, falling to 1–5% in severe renal failure, but its serum half-life does not change, which is why no renal dose adjustment is needed. In the Philippines it is the first-line drug for mild leptospirosis and for leptospirosis prophylaxis graded by exposure risk (PhilHealth policy recommendations), and the PNF lists it as a 100 mg capsule (as hyclate).

**Uses**: 7 kept, 6 added

- NEW: Chloroquine-resistant falciparum malaria (treatment, with a fast-acting schizonticide such as quinine)
- NEW: Prevention of scrub typhus
- NEW: Prevention of travellers' diarrhoea
- NEW: Louse- and tick-borne relapsing fever
- NEW: Primary and secondary syphilis in non-pregnant patients allergic to penicillin
- NEW: Epididymo-orchitis

**Side effects**: 7 kept, 7 added

- NEW: Anaphylaxis and angioedema
- NEW: SJS, TEN and DRESS (stop immediately)
- NEW: Photo-onycholysis (nail separation with sun exposure)
- NEW: Pancreatitis
- NEW: Haemolytic anaemia, neutropenia, thrombocytopenia and eosinophilia
- NEW: Jarisch-Herxheimer reaction when treating spirochaete infections
- NEW: Candida overgrowth and vaginal infection

**Precautions**: 1 kept, 5 added

- NEW: Pregnancy (UK label)
- NEW: Breastfeeding (passes into breast milk)
- NEW: Children under 8 years, because of tooth discolouration (UK label; CDC still recommends it for rickettsial disease at all ages)
- NEW: Myasthenia gravis: possible weak neuromuscular blockade (precaution)
- NEW: Systemic lupus erythematosus: may worsen (precaution)

**Interactions**: 6 kept, 5 added

- NEW: Oral zinc: impairs absorption; separate doses as much as possible.
- NEW: Ciclosporin: levels may rise; monitor.
- NEW: Methoxyflurane: renal failure reported with concurrent use.
- NEW: Alcohol: may shorten doxycycline half-life.
- NEW: Lab tests: can falsely raise urinary catecholamines (fluorescence assay).

**Disease links added**

- `chronic_kidney_disease`: **safe**: UK label: no renal dose adjustment; half-life unchanged in severe renal impairment and by haemodialysis

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Most infections (Also for ages 12 to under 18) | PO | 200 mg on day 1, then 100 mg | Once a day | Per infection | — | Label · UK SmPC |
| adult | Severe infections | PO | 200 mg | Once a day | Per infection | — | Label · UK SmPC |
| adult | Leptospirosis, mild (treatment) (First-line; duration not stated in the policy) | PO | 100 mg | 2× a day | — | — | PhilHealth 2012 |
| adult | Leptospirosis PEP, low risk (single wading, no wounds) (Give within 24–72 h of exposure) | PO | 200 mg | Single dose | Once | — | PhilHealth 2012 |
| adult | Leptospirosis PEP, moderate risk (wounds or swallowed water) (Start within 24–72 h of exposure) | PO | 200 mg | Once a day | 3–5 days | — | PhilHealth 2012 |
| adult | Leptospirosis PEP, high risk (continuous exposure) (E.g. living in flooded areas, rescuers) | PO | 200 mg | Once a week | Until exposure ends | — | PhilHealth 2012 |
| adult | Leptospirosis pre-exposure prophylaxis (Not routine; start 1–2 days before; non-pregnant, non-lactating adults) | PO | 200 mg | Once a week | Through exposure | — | PhilHealth 2012 |
| adult | Chlamydia, gonorrhoea, Ureaplasma | PO | 100 mg | 2× a day | 7 days | — | Label · UK SmPC |
| adult | Epididymo-orchitis | PO | 100 mg | 2× a day | 10 days | — | Label · UK SmPC |
| adult | Primary/secondary syphilis (penicillin allergy) (Non-pregnant patients only) | PO | 200 mg | 2× a day | 2 weeks | — | Label · UK SmPC |
| adult | Chloroquine-resistant falciparum malaria (With a fast-acting schizonticide such as quinine) | PO | 200 mg | Once a day | At least 7 days | — | Label · UK SmPC |
| adult | Malaria prophylaxis (Also for children over 12; check current guidance) | PO | 100 mg | Once a day | 1–2 days before to 4 weeks after | — | Label · UK SmPC |
| adult | Rickettsial infection (spotted fever) (Continue ≥3 days after fever resolves and until improvement) | PO | 100 mg | Every 12 h | At least 5–7 days | — | CDC |
| adult | Scrub typhus prevention | PO | 200 mg | Single dose | Once | — | Label · UK SmPC |
| adult | Relapsing fever (louse- or tick-borne) | PO | 100–200 mg | Single dose | Once | — | Label · UK SmPC |
| adult | Acne vulgaris (With food or fluid) | PO | 50 mg | Once a day | 6–12 weeks | — | Label · UK SmPC |
| child | Most infections, 8 to under 12 y, ≤45 kg (Only if other drugs unsuitable; up to 4.4 mg/kg/day if severe; >45 kg: adult dose) | PO | 4.4 mg/kg on day 1, then 2.2 mg/kg | Once a day | Per infection | 4.4 mg/kg/day | Label · UK SmPC |
| child | Rickettsial infection (spotted fever), <45 kg (CDC: all ages, including under 8; ≥45 kg: adult dose) | PO | 2.2 mg/kg | 2× a day | At least 5–7 days | — | CDC |

- *renal*: No dose adjustment; half-life is not significantly changed in severe renal impairment and is not altered by haemodialysis. [Label · UK SmPC]
- *hepatic*: Use with caution, especially with other potentially hepatotoxic drugs; rare hepatic abnormalities reported. [Label · UK SmPC]
- *elderly*: Usual doses; no special precautions. [Label · UK SmPC]
- *pregnancy*: UK label: contraindicated in pregnancy and breastfeeding (effects on teeth and skeletal development). [Label · UK SmPC]
- *pregnancy*: CDC still recommends doxycycline for presumed rickettsial disease in pregnancy after counselling on risks and benefits. [CDC]
- *pregnancy*: No leptospirosis pre-exposure prophylaxis is currently recommended as safe for pregnant or lactating women. [PhilHealth 2012]
- *administration*: Swallow with plenty of water while sitting or standing, well before bedtime. May take with food or milk if stomach upset occurs. Separate from antacids, iron, zinc and bismuth as much as possible. [Label · UK SmPC]
- *forms_ph*: Oral: 100 mg capsule (as hyclate). [PNF]
- *monitor*: Ask about headache or visual disturbance (intracranial hypertension); stop at the first sign of a serious skin reaction; watch for diarrhoea up to 2 months after the course (C. difficile); check INR with warfarin and ciclosporin levels if co-prescribed. [Label · UK SmPC]
- *monitor*: Prophylaxis is not 100% effective: people taking it should still watch for fever and flu-like symptoms after exposure. [PhilHealth 2012]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=doxycycline#emc-13082): Doxycycline 100 mg Capsules – Summary of Product Characteristics. Waymade Plc trading as Sovereign Medical (PL 06464/3108). Electronic Medicines Compendium (emc), medicines.org.uk.
- [PhilHealth – Leptospirosis policy recommendations](https://www.philhealth.gov.ph/partners/providers/pdf/Leptospirosis_Policy_Statements.pdf): Philippine Health Insurance Corporation. Policy Recommendations on the Diagnosis, Management and Prevention of Leptospirosis (based on the 2010 Leptospirosis Task Force CPG; c. 2012).
- [CDC – Rocky Mountain spotted fever](https://www.cdc.gov/rocky-mountain-spotted-fever/hcp/clinical-care/): Centers for Disease Control and Prevention. Clinical Care of Rocky Mountain Spotted Fever. CDC.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `PNF`: [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.
- Dosing source `PhilHealth 2012`: [PhilHealth – Leptospirosis policy recommendations](https://www.philhealth.gov.ph/partners/providers/pdf/Leptospirosis_Policy_Statements.pdf): Philippine Health Insurance Corporation. Policy Recommendations on the Diagnosis, Management and Prevention of Leptospirosis (c. 2012).
- Dosing source `Label · UK SmPC`: [UK SmPC – Doxycycline 100 mg Capsules](https://products.mhra.gov.uk/search/?search=doxycycline#emc-13082): Waymade Plc (Sovereign Medical). Doxycycline 100 mg Capsules – Summary of Product Characteristics. emc.
- Dosing source `CDC`: [CDC – Clinical Care of Rocky Mountain Spotted Fever](https://www.cdc.gov/rocky-mountain-spotted-fever/hcp/clinical-care/): Centers for Disease Control and Prevention. Clinical Care of Rocky Mountain Spotted Fever.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=doxycycline#emc-13082: Sovereign Medical doxycycline 100 mg caps SmPC: 4.2 all regimens (200 mg day 1 then 100 mg; severe 200 mg; acne 50 mg 6–12 wk; STI 100 mg bd 7 d; epididymo-orchitis 10 d; syphilis 200 mg bd 2 wk; CQ-resistant falciparum 200 mg daily ≥7 d with quinine; malaria prophylaxis 100 mg; scrub typhus 200 mg single; travellers' diarrhoea; relapsing fever 100–200 mg single; RMSF; children 8–<12 4.4/2.2 mg/kg; <8 should not be used; renal no adjustment; hepatic caution; elderly usual dose; administration); 4.3 pregnancy/breastfeeding contraindicated; 4.4 myasthenia, SLE, SJS/TEN/DRESS; 4.5 zinc, ciclosporin, methoxyflurane, alcohol, urinary catecholamines; 4.8 photo-onycholysis, pancreatitis, blood disorders, Jarisch-Herxheimer, candida; 5.2 absorption, ~40% urinary excretion falling to 1–5% in CrCl <10, half-life unchanged
- https://www.philhealth.gov.ph/partners/providers/pdf/Leptospirosis_Policy_Statements.pdf: Doxycycline first-line for mild leptospirosis 100 mg bid PO (no duration given); PrEP 200 mg weekly starting 1–2 days before (non-pregnant, non-lactating adults); PEP low risk 200 mg single dose within 24–72 h, moderate 200 mg daily 3–5 days, high 200 mg weekly until end of exposure; no safe PrEP for pregnant/lactating women; prophylaxis not 100% effective
- https://www.cdc.gov/rocky-mountain-spotted-fever/hcp/clinical-care/: Adults 100 mg every 12 h; children <45 kg 2.2 mg/kg twice daily; ≥3 days after fever resolves, minimum 5–7 days; recommended for all ages incl. under 8; recommended in pregnancy with counselling
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Doxycycline Oral: 100 mg capsule (as hyclate); no restriction marker

---

## Enalapril  (`med_enalapril`)

**Description (kept)**

Enalapril is a prodrug hydrolyzed to enalaprilat, which inhibits angiotensin-converting enzyme, lowering angiotensin II and aldosterone and increasing bradykinin. The result is vasodilation, reduced afterload and favorable cardiac remodeling. It is used for hypertension, heart failure with reduced ejection fraction and asymptomatic left ventricular dysfunction.

**Description (added)**

Enalaprilat has an effective accumulation half-life of about 11 hours, so once-daily dosing reaches steady state after about 4 days; it is cleared mainly by the kidneys and is removed by dialysis, which is why doses are cut in renal impairment. In the Philippines, the PNF lists enalapril as 5 mg and 20 mg tablets and as a fixed tablet with hydrochlorothiazide (20 mg + 12.5 mg).

**Side effects**: 8 kept, 7 added

- NEW: Depression
- NEW: Rhythm disturbances, angina and tachycardia
- NEW: Dyspnoea
- NEW: Diarrhoea and abdominal pain
- NEW: Hyponatraemia
- NEW: Hypoglycaemia in people with diabetes, mainly in the first weeks
- NEW: Anaemia, including aplastic and haemolytic (uncommon)

**Precautions**: 5 kept, 5 added

- NEW: Hypersensitivity to any other ACE inhibitor
- NEW: Co-administration with aliskiren when GFR is under 60 mL/min/1.73 m²
- NEW: Cardiogenic shock or haemodynamically significant left ventricular outflow obstruction (avoid)
- NEW: Bilateral renal artery stenosis or stenosis to a single kidney: high risk of hypotension and renal failure (precaution)
- NEW: Kidney transplant recipients: not recommended (precaution)

**Interactions**: 6 kept, 6 added

- NEW: mTOR inhibitors (sirolimus, everolimus), racecadotril and vildagliptin: increased angioedema risk.
- NEW: Co-trimoxazole: hyperkalaemia; combination not recommended.
- NEW: Ciclosporin and heparin: hyperkalaemia; monitor potassium.
- NEW: Insulin and oral antidiabetics: increased hypoglycaemia risk, mainly early in treatment and in renal impairment.
- NEW: Injectable gold (sodium aurothiomalate): rare nitritoid reactions (flushing, nausea, hypotension).
- NEW: LDL apheresis or wasp/bee venom desensitisation: life-threatening anaphylactoid reactions; withhold enalapril before each session.

**Disease links added**

- `acute_gastroenteritis`: **caution**: UK label: volume depletion from diarrhoea or vomiting makes symptomatic hypotension more likely
- `ischemic_stroke`: **caution**: UK label: in cerebrovascular disease an excessive fall in blood pressure could cause a stroke; start low

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Hypertension (starting dose) (5–10 mg in mild hypertension) | PO | 5–20 mg | Once a day | Long-term | — | Label · UK SmPC |
| adult | Hypertension (maintenance) | PO | 20 mg | Once a day | Long-term | 40 mg/day | Label · UK SmPC |
| adult | Hypertension: renovascular, salt/volume depleted or on diuretic (Start under supervision; stop diuretic 2–3 days before if possible) | PO | 5 mg or less | Once a day | Long-term | — | Label · UK SmPC |
| adult | Hypertension: elderly, on diuretic or renal impairment (Then adjust to renal function) | PO | 2.5 mg | Once a day | Long-term | 40 mg/day | MSF |
| adult | Heart failure / asymptomatic LV dysfunction (start) (Close supervision; days 4–7: 5 mg/day in 2 doses; week 2: 10 mg/day) | PO | 2.5 mg | Once a day | Days 1–3 | — | Label · UK SmPC |
| adult | Heart failure / asymptomatic LV dysfunction (target) (Reached over 2–4 weeks) | PO | 20 mg/day | Once a day or 2× a day | Long-term | 40 mg/day in 2 doses | Label · UK SmPC |
| child | Hypertension, 20 to under 50 kg (Children able to swallow tablets) | PO | 2.5 mg | Once a day | Long-term | 20 mg/day | Label · UK SmPC |
| child | Hypertension, 50 kg and over (Not recommended in neonates or GFR <30 mL/min/1.73 m²) | PO | 5 mg | Once a day | Long-term | 40 mg/day | Label · UK SmPC |

- *renal* CrCl 30–80: Initial dose 5–10 mg a day. [Label · UK SmPC]
- *renal* CrCl 10–30: Initial dose 2.5 mg a day. [Label · UK SmPC]
- *renal* CrCl ≤ 10: 2.5 mg on dialysis days; on non-dialysis days adjust to blood pressure. Enalaprilat is dialysable. [Label · UK SmPC]
- *hepatic*: Rare syndrome starting as cholestatic jaundice or hepatitis can progress to fulminant hepatic necrosis: stop if jaundice or marked rise in liver enzymes. [Label · UK SmPC]
- *elderly*: Dose according to renal function. [Label · UK SmPC]
- *pregnancy*: Not recommended in the first trimester and contraindicated in the second and third; stop as soon as pregnancy is found. If exposed from the second trimester, check fetal kidneys and skull by ultrasound; watch exposed newborns for hypotension. [Label · UK SmPC]
- *pregnancy*: Breastfeeding: milk levels are very low; avoid in preterm infants and in the first weeks after birth, may be used for older infants with monitoring. [Label · UK SmPC]
- *administration*: Food does not affect absorption. Increase hypertension doses every 1–2 weeks according to blood pressure. [MSF]
- *forms_ph*: Oral: 5 mg and 20 mg tablet (as maleate); also enalapril 20 mg + hydrochlorothiazide 12.5 mg tablet. [PNF]
- *monitor*: Blood pressure, serum creatinine and potassium before and after starting (especially with diuretics or heart failure); white cell count periodically in collagen vascular disease; blood glucose early on in diabetes. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=enalapril#emc-2671): Enalapril Maleate Tablets 5 mg – Summary of Product Characteristics. Dexcel-Pharma Ltd (PL 14017/0029). Electronic Medicines Compendium (emc), medicines.org.uk.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/enalapril-oral-16683529.html): Médecins Sans Frontières. Essential drugs – practical guidelines: Enalapril oral. MSF Medical Guidelines.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `PNF`: [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC – Enalapril Maleate Tablets 5 mg](https://products.mhra.gov.uk/search/?search=enalapril#emc-2671): Dexcel-Pharma Ltd. Enalapril Maleate Tablets 5 mg – Summary of Product Characteristics. emc.
- Dosing source `MSF`: [MSF Essential Drugs – Enalapril oral](https://medicalguidelines.msf.org/en/viewport/EssDr/english/enalapril-oral-16683529.html): Médecins Sans Frontières. Essential drugs – practical guidelines: Enalapril oral.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=enalapril#emc-2671: Dexcel enalapril 5 mg SmPC: 4.2 hypertension 5–20 mg start, 20 mg maintenance, max 40 mg; renovascular/diuretic 5 mg or lower, stop diuretic 2–3 days before; HF titration table 2.5 mg -> 20 mg target, max 40 mg in 2 doses; renal table CrCl 30–80 5–10 mg, 10–30 2.5 mg, ≤10 2.5 mg dialysis days; elderly by renal function; paediatric 2.5 mg (20–<50 kg, max 20) / 5 mg (≥50 kg, max 40), not neonates or GFR<30; 4.3 other ACEi hypersensitivity, aliskiren with GFR<60, 2nd/3rd trimester; 4.4 outflow obstruction, renal artery stenosis, LDL apheresis, desensitisation, hepatic failure, transplant, volume depletion incl. diarrhoea/vomiting, ischaemic heart/cerebrovascular disease, WBC monitoring in collagen vascular disease; 4.5 mTOR inhibitors, racecadotril, vildagliptin, co-trimoxazole, ciclosporin, heparin, gold, antidiabetics; 4.6 pregnancy/lactation; 4.8 depression, rhythm disturbances, angina, dyspnoea, diarrhoea, anaemia; 5.2 effective half-life 11 h, steady state ~4 days, renal elimination
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/enalapril-oral-16683529.html: Elderly/diuretic/renal impairment start 2.5 mg once daily; increase every 1–2 weeks; max 40 mg/day; adverse effects incl. hyponatraemia, hypoglycaemia; forms 5 and 20 mg tablets
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Enalapril (as maleate) Oral: 5 mg and 20 mg tablet; Enalapril + Hydrochlorothiazide 20 mg + 12.5 mg tablet
- https://www.who.int/publications/i/item/9789240033986: WHO 2021 hypertension guideline landing page; no drug-class detail on the page (full PDF not readable) - not used
- https://doaj.org/article/ebdc3ab0c7dd464bba849e90bb337ee5: 2020 Philippine hypertension CPG executive summary abstract (J Clin Hypertens 2021;23:1637-50); abstract has no ACE inhibitor detail and Wiley full text failed to load - not used

---

## Entecavir  (`med_entecavir`)

**Description (kept)**

Entecavir is a guanosine nucleoside analogue that is phosphorylated intracellularly to its active triphosphate, which competes with deoxyguanosine triphosphate and inhibits all three activities of the hepatitis B virus polymerase (base priming, reverse transcription of the negative strand and synthesis of the positive strand). It is a preferred first-line oral agent for chronic hepatitis B because of its potency and high barrier to resistance in nucleoside-naive patients.

**Description (added)**

Resistance is rare in nucleoside-naive patients but becomes common after lamivudine resistance (rtM204V/rtL180M substitutions), with cumulative entecavir resistance of about 51% by year 5 in lamivudine-refractory studies, so adding a second antiviral is considered in that setting. WHO lists tenofovir or entecavir as the oral treatments for chronic hepatitis B, and most people who start treatment continue it for life. In the Philippines the PNF lists 0.5 mg and 1 mg tablets and a 0.05 mg/mL oral solution.

**Side effects**: 4 kept, 5 added

- NEW: Insomnia and somnolence (common)
- NEW: Vomiting, diarrhoea and dyspepsia (common)
- NEW: Raised transaminases during treatment (common)
- NEW: Rash and alopecia (uncommon); anaphylactoid reaction (rare)
- NEW: Neutropenia (very common in paediatric patients)

**Precautions**: 4 kept, 2 added

- NEW: Hypersensitivity to entecavir or any excipient (UK SmPC)
- NEW: Rare hereditary galactose intolerance, Lapp lactase deficiency or glucose-galactose malabsorption (tablets contain lactose)

**Interactions**: 4 kept, 2 added

- NEW: Not a substrate, inducer or inhibitor of CYP450 enzymes: CYP-mediated interactions are unlikely.
- NEW: Lamivudine, adefovir or tenofovir: no pharmacokinetic interaction was seen.

**Disease links added**

- `hiv_infection`: **caution**: Not used for HBV in HIV/HBV coinfection unless on fully suppressive antiretroviral therapy (risk of HIV resistance).
- `chronic_kidney_disease`: **caution**: Renally cleared: dose reduced or interval extended when CrCl < 50 mL/min, including dialysis.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Chronic hepatitis B, nucleoside-naive, compensated (With or without food) | PO | 0.5 mg | Once a day | Long term (see stopping rules) | — | Label · UK SmPC |
| adult | Lamivudine-refractory chronic hepatitis B (Empty stomach (>2 h before and after a meal)) | PO | 1 mg | Once a day | Long term | — | Label · UK SmPC |
| adult | Decompensated liver disease (Empty stomach; stopping not advised in decompensated disease or cirrhosis) | PO | 1 mg | Once a day | Do not stop | — | Label · UK SmPC |
| child | Chronic hepatitis B, nucleoside-naive, 2–<18 y, ≥32.6 kg | PO | 0.5 mg (1 tablet or 10 mL solution) | Once a day | Long term | — | Label · UK SmPC |
| child | Chronic hepatitis B, nucleoside-naive, 2–<18 y, 10–32.5 kg (10–14.1 kg 4 mL; 20.9–22.5 kg 6.5 mL; 30.9–32.5 kg 9.5 mL (0.5 mL steps per band)) | PO | 4–9.5 mL of 0.05 mg/mL solution by weight band | Once a day | Long term | 10 mL | Label · UK SmPC (soln) |

- *renal* CrCl 30–49: Naive: 0.25 mg once a day or 0.5 mg every 48 h. Lamivudine-refractory/decompensated: 0.5 mg once a day. [Label · UK SmPC]
- *renal* CrCl 10–29: Naive: 0.15 mg once a day or 0.5 mg every 72 h. Lamivudine-refractory/decompensated: 0.3 mg once a day or 0.5 mg every 48 h. [Label · UK SmPC]
- *renal* CrCl <10, HD, CAPD: Naive: 0.05 mg once a day or 0.5 mg every 5–7 days. Lamivudine-refractory/decompensated: 0.1 mg once a day or 0.5 mg every 72 h. Doses extrapolated from limited data: monitor virological response closely. [Label · UK SmPC]
- *hepatic*: No dose adjustment in hepatic impairment; serious hepatic events are more frequent in decompensated (Child-Pugh C) disease. [Label · UK SmPC]
- *elderly*: No age-based adjustment; dose by renal function. [Label · UK SmPC]
- *pregnancy*: Not recommended in pregnancy unless clearly necessary; women of childbearing potential use effective contraception. Breastfeeding should stop during treatment. [Label · UK SmPC]
- *monitor*: HBV DNA and ALT during treatment; liver function for at least 6 months after stopping (risk of flare); renal function, especially with cyclosporine or tacrolimus after liver transplant. [Label · UK SmPC]
- *administration*: Duration: HBeAg-positive, at least 12 months after HBe seroconversion (or until HBs seroconversion/loss of efficacy); HBeAg-negative, at least until HBs seroconversion or loss of efficacy. [Label · UK SmPC]
- *forms_ph*: 500 mcg and 1 mg tablet/film-coated tablet; 0.05 mg/mL oral solution. [PNF]

**References added**

- [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=entecavir#emc-213): Baraclude 0.5 mg film-coated tablets - Summary of Product Characteristics. Bristol-Myers Squibb Pharma EEIG. Electronic medicines compendium (emc), updated May 2021.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=entecavir#emc-2089): Baraclude 0.05 mg/ml oral solution - Summary of Product Characteristics. Bristol-Myers Squibb. Electronic medicines compendium (emc), updated May 2021.
- [WHO](https://www.who.int/news-room/fact-sheets/detail/hepatitis-b): World Health Organization. Hepatitis B fact sheet. Geneva: WHO; 2026.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=entecavir#emc-213): Baraclude 0.5 mg film-coated tablets - SmPC. Bristol-Myers Squibb Pharma EEIG, 2021.
- Dosing source `Label · UK SmPC (soln)`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=entecavir#emc-2089): Baraclude 0.05 mg/ml oral solution - SmPC. Bristol-Myers Squibb, 2021.
- Dosing source `PNF`: [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Entecavir: oral 500 mcg and 1 mg tablet/film-coated tablet; 0.05 mg/mL oral solution.
- https://products.mhra.gov.uk/search/?search=entecavir#emc-213: Baraclude 0.5 mg SmPC: adult doses (0.5 mg naive with/without food; 1 mg lamivudine-refractory and decompensated on empty stomach), stopping rules, ≥32.6 kg child dose, renal table incl. lamivudine-refractory/decompensated column, hepatic/elderly, contraindication, lactose, resistance ~51% at year 5, rtM204V/rtL180M, CYP450 and lamivudine/adefovir/tenofovir interactions, pregnancy/breastfeeding, adverse reactions incl. insomnia, somnolence, dyspepsia, rash, alopecia, anaphylactoid, paediatric neutropenia, monitoring LFT ≥6 months after stopping, transplant renal monitoring, HIV coinfection.
- https://products.mhra.gov.uk/search/?search=entecavir#emc-2089: Baraclude 0.05 mg/ml oral solution: paediatric weight-band table 10.0–14.1 kg 4.0 mL up to ≥32.6 kg 10.0 mL; minimum age 2 years.
- https://www.who.int/news-room/fact-sheets/detail/hepatitis-b: Chronic hepatitis B can be treated with oral tenofovir or entecavir; most who start treatment continue for life.

---

## Ethambutol  (`med_ethambutol`)

**Description (kept)**

Ethambutol inhibits mycobacterial arabinosyltransferases, interfering with arabinogalactan synthesis in the cell wall; it is bacteriostatic. It is included in the intensive phase of first-line TB therapy to protect against resistance while drug-susceptibility results are pending.

**Description (added)**

In the Philippine NTP it is given in the HRZE fixed-dose combination for the 2-month intensive phase of Category I (2HRZE/4HR) and through all 8 months of Category II retreatment (2HRZES/1HRZE/5HRE), with the number of tablets set by body-weight band. MSF notes that ethambutol is not routinely given to all children, and that young children (under 5) need particular care because visual changes are hard to detect at that age.

**Uses**: 2 kept, 2 added

- NEW: Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)
- NEW: Extrapulmonary TB of the CNS, bones or joints (PH NTP Category Ia: 2HRZE/10HR)

**Side effects**: 6 kept, 2 added

- NEW: Very rare skin reactions: photosensitive lichenoid eruptions, bullous dermatitis, Stevens-Johnson syndrome
- NEW: Numbness and paraesthesia of the extremities (rare)

**Precautions**: 3 kept, 3 added

- NEW: Pre-existing eye disease such as diabetic retinopathy (MSF)
- NEW: Severe renal impairment (MSF)
- NEW: Retrobulbar neuritis (UK SmPC)

**Disease links added**

- `chronic_kidney_disease`: **caution**: Dose given three times a week in renal impairment; optic toxicity is more common when renal function is reduced; MSF advises against use in severe renal impairment.
- `type2_diabetes`: **caution**: MSF lists pre-existing eye disease such as diabetic retinopathy as a contraindication; check eyes before treatment in diabetics (applies only with retinopathy).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | TB Cat I intensive (2HRZE), 30–37 kg (Then HR 2 tablets for 4 months (10 months for Cat Ia)) | PO | 2 tablets HRZE FDC | Once a day | 2 months | — | NTP MOP 2014 |
| adult | TB Cat I intensive (2HRZE), 38–54 kg (Then HR 3 tablets) | PO | 3 tablets HRZE FDC | Once a day | 2 months | — | NTP MOP 2014 |
| adult | TB Cat I intensive (2HRZE), 55–70 kg (Then HR 4 tablets) | PO | 4 tablets HRZE FDC | Once a day | 2 months | — | NTP MOP 2014 |
| adult | TB Cat I intensive (2HRZE), >70 kg (Then HR 5 tablets) | PO | 5 tablets HRZE FDC | Once a day | 2 months | — | NTP MOP 2014 |
| adult | TB Cat II retreatment (2HRZES/1HRZE/5HRE) (HRZE months 1–3 (+ streptomycin months 1–2), then HRE months 4–8) | PO | Same tablet number per weight band (2/3/4/5) | Once a day | 8 months | — | NTP MOP 2014 |
| adult | TB, single-drug formulation | PO | 15 mg/kg (range 15–20) | Once a day | Per regimen | 1.2 g/day | NTP MOP 2014 |
| child | TB, single-drug formulation (Newborn <4 weeks: refer to pediatrician (streptomycin instead of ethambutol)) | PO | 20 mg/kg (range 15–25) | Once a day | Per regimen | 1.2 g/day | NTP MOP 2014 |
| child | TB intensive phase, 4–7 kg / 8–11 kg (with HRZ 50/75/150) (Not routinely given to all children) | PO | 1 / 2 tablets E 100 mg | Once a day | 2 months | — | MSF TB |

- *renal*: 15–25 mg/kg three times a week in renal impairment; MSF advises not to give in severe renal impairment. Toxic effects are more common when renal function is impaired. [MSF]
- *pregnancy*: MSF: no contraindication in pregnancy or breastfeeding. The UK SmPC states it is not recommended in pregnancy or breastfeeding. [MSF]
- *monitor*: Full eye examination before starting (UK SmPC). Teach patients to stop the drug and seek care at once for blurred vision, reduced acuity or difficulty telling red from green (MSF; usually reverses within weeks). [MSF]
- *administration*: Dose carefully by body weight. HRZE FDC tablet = isoniazid 75 mg + rifampicin 150 mg + pyrazinamide 400 mg + ethambutol 275 mg. [PNF]
- *forms_ph*: 100 mg tablet (pediatric); 200 mg and 400 mg tablet. FDCs: isoniazid + rifampicin + ethambutol 75/150/275 mg tablet; isoniazid + rifampicin + pyrazinamide + ethambutol 75/150/400/275 mg tablet. [PNF]

**References added**

- [Philippine NTP Manual of Procedures](https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf): Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.
- [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/ethambutol-e-oral-16683637.html): Médecins Sans Frontières. Essential drugs - practical guidelines: Ethambutol (E) oral. Updated August 2022.
- [MSF Tuberculosis guideline](https://medicalguidelines.msf.org/en/node/1205): Médecins Sans Frontières. Tuberculosis - Appendix 13. Daily dose of TB drugs using fixed-dose combinations. Updated October 2022.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=ethambutol#emc-9346): Ethambutol 400 mg Tablets - Summary of Product Characteristics. Esteve Pharmaceuticals Ltd. Electronic medicines compendium (emc), updated July 2024.
- Dosing source `NTP MOP 2014`: [Philippine NTP Manual of Procedures](https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf): DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 11–14).
- Dosing source `PNF`: [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/ethambutol-e-oral-16683637.html): MSF Essential drugs: Ethambutol (E) oral, 2022.
- Dosing source `MSF TB`: [MSF Tuberculosis guideline](https://medicalguidelines.msf.org/en/node/1205): MSF Tuberculosis, Appendix 13: daily dose of TB drugs using FDCs, 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=ethambutol#emc-9346): Ethambutol 400 mg Tablets - SmPC. Esteve Pharmaceuticals Ltd, 2024.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Ethambutol oral 100 mg tablet (pediatric), 200 mg and 400 mg tablet; isoniazid+rifampicin+ethambutol 75+150+275 mg; isoniazid+rifampicin+pyrazinamide+ethambutol 75+150+400+275 mg (List B).
- https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf: NTCP MOP 5th ed 2014: Cat I 2HRZE/4HR (Cat Ia 2HRZE/10HR for CNS/bones/joints); Cat II 2HRZES/1HRZE/5HRE; Table 11/12 tablets per day 30–37 kg 2, 38–54 kg 3, 55–70 kg 4, >70 kg 5; Table 13 E adults 15 (15–20) mg/kg, children 20 (15–25) mg/kg, max 1.2 g daily; Table 14 newborn <4 weeks refer, streptomycin instead of ethambutol.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/ethambutol-e-oral-16683637.html: 15–25 mg/kg once daily, max 1200 mg; renal impairment 15–25 mg/kg three times weekly; do not give in severe renal impairment or pre-existing optic neuritis incl. diabetic retinopathy; children <5 particular care; no contraindication in pregnancy/breastfeeding; stop for visual symptoms, usually reversible.
- https://medicalguidelines.msf.org/en/node/1205: Children intensive phase HZR 50/150/75 + E 100 mg: 4–7 kg 1 tablet E, 8–11 kg 2 tablets E; ethambutol not routinely given to all children.
- https://products.mhra.gov.uk/search/?search=ethambutol#emc-9346: Contraindicated in optic or retrobulbar neuritis; full ophthalmic exam before starting; toxic effects more common in renal impairment; not recommended in pregnancy/breastfeeding; very rare photosensitive lichenoid eruptions, bullous dermatitis, SJS; rare peripheral neuropathy, numbness, paraesthesia.

---

## Famotidine  (`med_famotidine`)

**Description (kept)**

Famotidine competitively blocks histamine H2 receptors on gastric parietal cells, reducing basal, nocturnal and stimulated gastric acid secretion. It relieves heartburn and heals peptic ulcers and esophagitis, but is less potent than proton pump inhibitors; it is useful for on-demand symptom control and as a bedtime add-on for nighttime reflux.

**Description (added)**

A single 40 mg bedtime dose suppresses gastric acid for more than 12 hours, and famotidine does not affect the cytochrome P450 system, so it has few clinically important interactions apart from drugs that need gastric acid for absorption. In the Philippines the PNF lists a 20 mg tablet and a 20 mg injection, the latter used intravenously in hospitalised patients until oral therapy is possible.

**Uses**: 4 kept, 2 added

- NEW: Prevention of duodenal ulcer relapse (20 mg at night)
- NEW: Hospitalised patients who cannot take oral therapy (IV 20 mg every 12 h)

**Side effects**: 5 kept, 4 added

- NEW: Taste disorder, dry mouth, nausea, flatulence and loss of appetite (uncommon)
- NEW: Rash, itching and urticaria (uncommon)
- NEW: Very rare: agranulocytosis or pancytopenia, anaphylaxis, hepatitis or cholestatic jaundice, convulsions
- NEW: Very rare: QT prolongation and arrhythmias

**Precautions**: 2 kept, 2 added

- NEW: Gastric malignancy must be excluded before treating a gastric ulcer
- NEW: Multiple-dose vials containing benzyl alcohol: not for neonates (gasping syndrome)

**Interactions**: 2 kept, 6 added

- NEW: Ketoconazole or itraconazole: absorption reduced; give ketoconazole 2 hours before famotidine.
- NEW: Atazanavir and posaconazole oral suspension: absorption reduced by higher gastric pH; avoid where possible.
- NEW: Erlotinib, gefitinib or pazopanib: co-administration not recommended.
- NEW: Probenecid: raises famotidine levels by about 50%; avoid.
- NEW: Antacids: take famotidine 1–2 hours before the antacid; sucralfate should not be given within 2 hours of famotidine.
- NEW: Calcium carbonate phosphate binders in haemodialysis patients: may lose efficacy.

**Disease links added**

- `peptic_ulcer_disease`: **safe**: Licensed for duodenal and benign gastric ulcer healing and relapse prevention; exclude gastric malignancy first.
- `chronic_kidney_disease`: **caution**: Daily dose halved when CrCl < 30 mL/min; CNS adverse effects reported in moderate to severe renal insufficiency.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Duodenal ulcer (Continue 4 more weeks if not healed at 4 weeks) | PO | 40 mg | Once a day (at night) | 4–8 weeks | — | Label · UK SmPC |
| adult | Duodenal ulcer relapse prevention | PO | 20 mg | Once a day (at night) | — | — | Label · UK SmPC |
| adult | Benign gastric ulcer (Exclude malignancy first) | PO | 40 mg | Once a day (at night) | 4–8 weeks | — | Label · UK SmPC |
| adult | Reflux oesophagitis, mild | PO | 20 mg | 2× a day | 6–12 weeks | — | Label · UK SmPC |
| adult | Reflux oesophagitis, mild to moderate | PO | 40 mg | 2× a day | 6–12 weeks | — | Label · UK SmPC |
| adult | Zollinger-Ellison syndrome (Up to 800 mg/day used for up to 1 year) | PO | 20 mg, then adjust | Every 6 h | As needed | 800 mg/day | Label · UK SmPC |
| adult | Hospitalised / unable to take oral (Push over ≥2 min or infuse over 15–30 min) | IV | 20 mg | Every 12 h | Until oral possible | — | Label · US (inj) |
| child | 1–16 y, IV acid suppression (Up to 0.5 mg/kg every 12 h used in studies; oral use in children not established (UK SmPC)) | IV | 0.25 mg/kg | Every 12 h | — | 40 mg/day | Label · US (inj) |

- *renal* CrCl <30: Reduce the daily dose by 50%. [Label · UK SmPC]
- *renal* CrCl <10: Consider 20 mg at night. [Label · UK SmPC]
- *renal* Dialysis: Reduce dose by 50%; give at the end of or after dialysis. [Label · UK SmPC]
- *elderly*: Same dose as adults. [Label · UK SmPC]
- *pregnancy*: Not recommended in pregnancy unless clearly needed. Excreted in breast milk: stop famotidine or stop breastfeeding. [Label · UK SmPC]
- *monitor*: Blood count and liver function during long-term high-dose treatment; avoid abrupt withdrawal after long-standing ulcer disease; watch for confusion in renal impairment. [Label · UK SmPC]
- *administration*: IV push: dilute 20 mg (2 mL) to 5 or 10 mL and inject over at least 2 minutes. Infusion: dilute 2 mL in 100 mL dextrose 5% and run over 15–30 minutes. [Label · US (inj)]
- *forms_ph*: 20 mg tablet; 20 mg powder/lyophilized powder for injection (ampule/vial). [PNF]

**References added**

- [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=famotidine#emc-11523): Famotidine 20mg Tablets - Summary of Product Characteristics. Tillomed Laboratories Ltd. Electronic medicines compendium (emc), updated January 2025.
- [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1fdf16e5-145d-4c19-a318-fc6c10794b50): Famotidine Injection, USP 10 mg/mL - prescribing information. Hikma Pharmaceuticals USA Inc. DailyMed, U.S. National Library of Medicine.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=famotidine#emc-11523): Famotidine 20mg Tablets - SmPC. Tillomed Laboratories Ltd, 2024.
- Dosing source `Label · US (inj)`: [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1fdf16e5-145d-4c19-a318-fc6c10794b50): Famotidine Injection, USP 10 mg/mL - prescribing information. Hikma Pharmaceuticals USA Inc.
- Dosing source `PNF`: [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Famotidine: oral 20 mg tablet; inj. 20 mg powder/lyophilized powder for injection, ampule/vial.
- https://products.mhra.gov.uk/search/?search=famotidine#emc-11523: Tillomed Famotidine 20 mg SmPC: DU 40 mg nocte 4(+4) weeks; relapse 20 mg nocte; GU 40 mg nocte 4–8 weeks; ZES 20 mg q6h up to 800 mg/day for 1 year; oesophagitis 20 mg bd mild / 40 mg bd mild-moderate, 6+6 weeks; CrCl <30 reduce 50%, dialysis 50% after dialysis, <10 consider 20 mg nocte; elderly as adults; children not established; exclude gastric malignancy; monitor blood count/LFT long-term high dose; avoid abrupt withdrawal; interactions ketoconazole/itraconazole, atazanavir, probenecid +50%, antacids 1–2 h, sucralfate 2 h, posaconazole suspension, dasatinib/erlotinib/gefitinib/pazopanib, calcium carbonate phosphate binders; no CYP450 effect; pregnancy not recommended, excreted in breast milk; adverse effects list incl. taste disorder, dry mouth, very rare agranulocytosis, pancytopenia, hepatitis, convulsions, QT prolongation; 40 mg at 9 pm effective >12 h.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1fdf16e5-145d-4c19-a318-fc6c10794b50: Hikma Famotidine Injection 10 mg/mL: adult 20 mg IV q12h until oral possible; IV push diluted to 5 or 10 mL over ≥2 min; infusion in 100 mL D5W over 15–30 min; paediatric 1–16 y 0.25 mg/kg IV q12h up to 40 mg/day (up to 0.5 mg/kg used); CNS adverse effects in moderate/severe renal insufficiency; benzyl alcohol multi-dose vials and gasping syndrome in neonates.

---

## Ferrous Sulfate  (`med_ferrous_sulfate`)

**Description (kept)**

Ferrous sulfate supplies ferrous iron, which is absorbed mainly in the duodenum and used to rebuild body iron stores and hemoglobin. It is first-line treatment for iron-deficiency anemia. A 200 mg ferrous sulfate tablet contains about 65 mg of elemental iron; hemoglobin usually rises within about a month, and treatment continues for about 3 months to refill stores.

**Description (added)**

Doses are written as elemental iron because content differs by salt (hydrated ferrous sulfate is about 20% iron, dried ferrous sulfate about 32%). In the Philippines, the DOH antenatal program gives daily iron-folic acid tablets (60 mg elemental iron + 0.4 mg folic acid) for at least 180 days, covering pregnancy and up to 3 months after delivery. WHO likewise recommends 30–60 mg elemental iron with 400 µg folic acid every day in pregnancy.

**Uses**: 2 kept, 1 added

- NEW: Iron-folic acid supplementation in pregnancy and up to 3 months postpartum (PH DOH program)

**Side effects**: 4 kept, 4 added

- NEW: Mouth ulceration if tablets are chewed, sucked or held in the mouth
- NEW: Oesophageal injury or bronchial necrosis if a tablet is aspirated (elderly, swallowing problems)
- NEW: Hypersensitivity rash, rarely anaphylaxis
- NEW: Faecal impaction with long-term use in older patients

**Precautions**: 3 kept, 2 added

- NEW: Concomitant parenteral (injectable) iron
- NEW: Hypersensitivity to any ingredient of the product

**Interactions**: 4 kept, 5 added

- NEW: Bisphosphonates, penicillamine, norfloxacin and ofloxacin: iron reduces their absorption.
- NEW: Levothyroxine: separate doses by at least 2 hours.
- NEW: Methyldopa: reduced bioavailability; cholestyramine binds iron in the gut.
- NEW: Calcium, trientine, tea, coffee, milk, eggs and whole grains: reduced iron absorption; avoid from 1 hour before to 2 hours after the iron dose.
- NEW: Dimercaprol: avoid, as it forms a toxic complex with iron.

**Disease links added**

- `peptic_ulcer_disease`: **caution**: Label advises caution in existing gastrointestinal disease and GI irritation is common (applying this to peptic ulcer is an inference).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Iron-deficiency anaemia (treatment) (Also for children ≥12 years) | PO | 65 mg elemental iron (1 × 200 mg tab) | 2–3× a day | 3 months | — | MSF |
| adult | Prevention (risk periods) (Also for children ≥12 years) | PO | 65 mg elemental iron | Once a day | During risk period | — | MSF |
| adult | Pregnancy (PH DOH program) (Iron-folic acid tablet) | PO | 60 mg elemental iron + 0.4 mg folic acid | Once a day | ≥180 days (pregnancy to 3 months postpartum) | — | PH DOH |
| adult | Pregnancy (WHO) | PO | 30–60 mg elemental iron + 400 µg folic acid | Once a day | Throughout pregnancy | — | WHO 2024 |
| child | Iron-deficiency anaemia, 6 to <12 y | PO | 65 mg elemental iron | 2× a day | 3 months | — | MSF |
| child | Iron-deficiency anaemia, 6–12 y (tablets) (200 mg tablets not recommended <6 y or <22 kg) | PO | >22 kg: 1 tab; >44 kg: 1 tab 2×; >66 kg: 1 tab 3× | Daily | — | — | Label · UK SmPC |
| child | Iron-deficiency anaemia, 1 month to <6 y (Use syrup/drops) | PO | 1.5–3 mg/kg elemental iron | 2× a day | 3 months | — | MSF |
| child | Prevention, 1 month to <12 y | PO | 1–2 mg/kg elemental iron | Once a day | During risk period | 65 mg/day | MSF |
| neonate | Iron-deficiency anaemia | PO | 1–2 mg/kg elemental iron | 2× a day | 3 months | — | MSF |
| neonate | Prevention | PO | 4.5 mg elemental iron | Once a day | During risk period | — | MSF |

- *forms_ph*: Ferrous salt tablet (equiv. to 60 mg elemental iron); solution 15 mg elemental iron/0.6 mL drops (15 mL, 30 mL); solution 30 mg elemental iron/5 mL syrup (60 mL). Also ferrous salt + folic acid: 60 mg elemental iron + 400 µg folic acid tablet/capsule. [PNF]
- *pregnancy*: Recommended in pregnancy and lactation; for prevention in pregnancy prefer the combined iron + folic acid tablet (PH DOH: 60 mg + 0.4 mg daily for at least 180 days). [PH DOH]
- *administration*: Swallow tablets whole with water; do not chew, suck or hold in the mouth. Take with or before meals; with meals if GI upset. [Label · UK SmPC]
- *administration*: Rinse mouth or drink water after syrup to avoid tooth staining; increase the dose gradually if poorly tolerated. [MSF]
- *elderly*: Usual adult dose. Check swallowing/aspiration risk first (tablet aspiration can cause bronchial necrosis); watch for constipation and faecal impaction. [Label · UK SmPC]
- *monitor*: Before starting, look for an underlying cause of anaemia (e.g. GI blood loss). Check haemoglobin response. In homes with young children, store safely: 20 mg/kg elemental iron is toxic. [MSF]

**References added**

- [UK SmPC - Ferrous Sulfate Tablets 200mg (Sandoz)](https://products.mhra.gov.uk/search/?search=ferrous+sulfate#emc-4231): Sandoz Limited. Ferrous Sulfate Tablets 200mg - Summary of Product Characteristics. electronic medicines compendium (emc).
- [WHO guideline - Daily iron and folic acid supplementation in pregnant women](https://www.who.int/publications/i/item/9789241501996): World Health Organization. e-Library of Evidence for Nutrition Actions (eLENA): Daily iron and folic acid supplementation during pregnancy. Updated 26 July 2024.
- [Nutrients 2021 - IFA compliance in the Philippines](https://www.mdpi.com/2072-6643/13/9/3060): Felipe-Dimog EB, Yu CH, Ho CH, Liang FW. Factors Influencing the Compliance of Pregnant Women with Iron and Folic Acid Supplementation in the Philippines: 2017 Philippine Demographic and Health Survey Analysis. Nutrients. 2021;13(9):3060. doi:10.3390/nu13093060
- [DOH Administrative Order No. 2010-0010](https://dev.lawyerly.ph/laws/55982): Department of Health (Philippines). Administrative Order No. 2010-0010: Revised Policy on Micronutrient Supplementation to Support Achievement of 2015 MDG Targets to Reduce Underfive and Maternal Deaths and Address Micronutrient Needs of Other Population Groups. 19 April 2010.
- [WHO guideline - Daily iron supplementation in infants and children](https://www.who.int/publications/i/item/9789241549523): World Health Organization. e-Library of Evidence for Nutrition Actions (eLENA): Daily iron supplementation in children 6-23 months of age. Updated 9 August 2023.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/ferrous-salts-16683659.html): Medecins Sans Frontieres. Essential drugs - practical guidelines: Ferrous salts, oral.
- Dosing source `Label · UK SmPC`: [UK SmPC - Ferrous Sulfate Tablets 200mg (Sandoz)](https://products.mhra.gov.uk/search/?search=ferrous+sulfate#emc-4231): Sandoz Limited. Ferrous Sulfate Tablets 200mg - Summary of Product Characteristics. emc.
- Dosing source `PH DOH`: [PH DOH IFA policy (as reported in Nutrients 2021)](https://www.mdpi.com/2072-6643/13/9/3060): Felipe-Dimog EB, et al. Nutrients. 2021;13(9):3060, citing DOH AO 2010-0010 and AO 119 s. 2003.
- Dosing source `WHO 2024`: [WHO guideline (pregnancy iron)](https://www.who.int/publications/i/item/9789241501996): World Health Organization. Guideline: daily iron and folic acid supplementation in pregnant women. Geneva: WHO; 2012 (dosing as summarised in WHO eLENA, July 2024).
- Dosing source `PNF`: [Philippine National Formulary EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary - Essential Medicines List, 8th ed. PhilHealth; 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF EML p.20: Ferrous salt tablet equiv. 60 mg elemental iron; solution 15 mg/0.6 mL drops 15 & 30 mL; solution 30 mg/5 mL syrup 60 mL; ferrous sulfate hydrated 20%, dried 32% iron; ferrous salt + folic acid 60 mg + 400 µg.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/ferrous-salts-16683659.html: Prevention/treatment doses by age (neonate 4.5 mg; 1–2 mg/kg max 65 mg/day; 1.5–3 mg/kg 2×; 65 mg 2×; 65 mg 2–3×), 3-month treatment, 20 mg/kg toxic, rinse mouth after syrup, take with meals, prefer iron+folic acid in pregnancy.
- https://products.mhra.gov.uk/search/?search=ferrous+sulfate#emc-4231: Sandoz SmPC: adult/child 6–12 y weight-band dosing, not <6 y/<22 kg; contraindications incl. parenteral iron; interactions (bisphosphonates, penicillamine, nor/ofloxacin, methyldopa, cholestyramine, calcium, trientine, tea, coffee, milk, eggs, whole grains 1 h before–2 h after, levothyroxine ≥2 h, dimercaprol); caution in GI disease; mouth ulceration, aspiration/bronchial necrosis, anaphylaxis, faecal impaction; recommended in pregnancy and lactation.
- https://www.who.int/publications/i/item/9789241501996: WHO: daily 30–60 mg elemental iron + 400 µg folic acid in pregnancy; updated 26 July 2024.
- https://www.mdpi.com/2072-6643/13/9/3060: Philippine health authorities recommend 60 mg elemental iron + 0.4 mg folic acid daily for at least 180 days, covering pregnancy and up to 3 months postpartum; cites DOH AO 2010-0010 and AO 119 s. 2003.
- https://dev.lawyerly.ph/laws/55982: Text of DOH AO 2010-0010 (Revised Policy on Micronutrient Supplementation), 19 April 2010; priority groups 0–59 months, pregnant and lactating women, WRA 15–49. No doses in the text.
- https://www.who.int/publications/i/item/9789241549523: WHO recommends daily iron supplementation for children 6–23 months where anaemia prevalence ≥40%; updated 9 Aug 2023 (dose not shown on page).

---

## Furosemide  (`med_furosemide`)

**Description (kept)**

Furosemide inhibits the Na+/K+/2Cl- cotransporter in the thick ascending limb of the loop of Henle, producing a potent, short-acting diuresis with loss of sodium, chloride, potassium, magnesium and water. It remains effective at low GFR. It is used for edema from heart failure, cirrhosis and renal disease, and for hypertension, particularly when renal function is reduced.

**Description (added)**

In the Philippines, furosemide is on the PNF as 20 mg and 40 mg tablets (bioequivalence list B) and a 10 mg/mL injection. Injections are used only when oral dosing is not possible or not working, or when a fast effect is needed; patients are switched back to tablets as soon as possible. A loop diuretic is not the right treatment for nutritional (kwashiorkor) oedema or for oedema from pre-eclampsia.

**Uses**: 3 kept, 2 added

- NEW: Peripheral oedema due to mechanical obstruction or venous insufficiency
- NEW: Hypertensive crisis, emergency IV use (not in pregnancy)

**Side effects**: 6 kept, 4 added

- NEW: Hypocalcaemia and hypochloraemic alkalosis
- NEW: Acute renal failure
- NEW: Anaphylactic reactions
- NEW: Nephrocalcinosis in premature infants

**Precautions**: 2 kept, 8 added

- NEW: Hypersensitivity to sulphonamides or amiloride
- NEW: Severe renal impairment (CrCl <30 mL/min/1.73 m²) or renal failure from nephrotoxic/hepatotoxic poisoning (UK label)
- NEW: Severe hyponatraemia, severe hypokalaemia, hypovolaemia, dehydration or hypotension
- NEW: Hepatic pre-coma or coma, hepatic encephalopathy
- NEW: Addison's disease; digitalis intoxication
- NEW: Taking potassium supplements or potassium-sparing diuretics (UK label)
- NEW: Breastfeeding
- NEW: Kwashiorkor (nutritional) oedema or oedema from pre-eclampsia

**Interactions**: 6 kept, 10 added

- NEW: Digoxin: diuretic-induced hypokalaemia increases digoxin toxicity.
- NEW: Cisplatin: increased ototoxicity and possible nephrotoxicity.
- NEW: Risperidone: higher mortality in elderly patients with dementia; weigh risks and benefits.
- NEW: High-dose cephalosporins: risk of renal impairment.
- NEW: Methotrexate: competition for renal tubular secretion; more toxicity at high doses.
- NEW: Chloral hydrate: avoid; IV furosemide within 24 hours can cause flushing, sweating and tachycardia.
- NEW: Ciclosporin: increased risk of gouty arthritis.
- NEW: Colestyramine or colestipol: give 2–3 hours apart.
- NEW: Radiocontrast: more renal function decline in high-risk patients.
- NEW: Insulin and oral antidiabetics: hyperglycaemia may reduce their effect.

**Disease links added**

- `type2_diabetes`: **caution**: Can raise blood glucose; labels advise caution in diabetes and possible adjustment of antidiabetic doses.
- `acute_gastroenteritis`: **avoid**: Dehydration and hypovolaemia are label contraindications (applying this to gastroenteritis is an inference).
- `cholera`: **avoid**: Dehydration and hypovolaemia are label contraindications (applying this to cholera is an inference).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Oedema (Maintenance 20 mg daily or 40 mg on alternate days) | PO | 40 mg | Once a day (morning) | — | 80 mg/day (resistant oedema) | Label · UK SmPC |
| adult | Hypertension (If not enough, add another antihypertensive) | PO | 20–40 mg | 2× a day | Long-term | 40 mg 2× a day | Label · UK SmPC |
| adult | Oedema (Same dose IM; >50 mg as slow IV infusion) | IV | 20–50 mg | Increase by 20 mg, not more often than every 2 h | Switch to oral ASAP | 1500 mg/day | Label · UK SmPC inj |
| adult | Acute pulmonary oedema (IM not suitable) | IV | 40 mg slow IV | 80 mg if no response within 1 h | Per response | — | MSF |
| child | Oedema | PO | 2 mg/kg | Single dose; +1–2 mg/kg after ≥6–8 h | Per response | 6 mg/kg/dose | Label · DailyMed |
| child | Oedema (IV or IM) | IV | 0.5–1.5 mg/kg/day | Daily | Per response | 20 mg/day | Label · UK SmPC inj |

- *renal* CrCl <30: Contraindicated (UK label); for IV infusion with serum creatinine >5 mg/dL, max rate 2.5 mg/min. [Label · UK SmPC]
- *hepatic*: Dose may need adjusting in liver congestion or dysfunction, with monitoring; contraindicated in hepatic pre-coma/coma and hepatic encephalopathy. Hypokalaemia is more likely in cirrhosis. [Label · UK SmPC]
- *elderly*: Slower elimination: start at the low end and titrate to response. [Label · UK SmPC]
- *pregnancy*: Do not use in pregnancy unless there are compelling reasons; monitor fetal growth. Not for hypertension of pregnancy or pre-eclampsia oedema. Breastfeeding: contraindicated (passes into milk, may suppress lactation). [Label · UK SmPC]
- *administration*: IV infusion max 4 mg/min; doses >50 mg by slow infusion. Continuous infusion or small doses about every 4 h are preferred over large boluses. Take tablets in the morning. [Label · UK SmPC inj]
- *forms_ph*: Oral: 20 mg and 40 mg tablet (List B, bioequivalence required). Injection: 10 mg/mL, 2 mL ampul (IM, IV); 10 mg/mL, 25 mL ampul (IV infusion). [PNF]
- *monitor*: Serum sodium, potassium, creatinine and BUN (often in the first months, then periodically); blood pressure including orthostatic; urine output (watch for retention with prostatic enlargement); glucose in diabetes; FBC for blood dyscrasias. Correct hypovolaemia and electrolytes before starting. [Label · UK SmPC]

**References added**

- [UK SmPC - Furosemide 40 mg tablets](https://products.mhra.gov.uk/search/?search=furosemide#emc-12129): Furosemide 40 mg tablets - Summary of Product Characteristics. electronic medicines compendium (emc).
- [UK SmPC - Furosemide 10 mg/ml Solution for Injection (Baxter)](https://products.mhra.gov.uk/search/?search=furosemide#emc-11522): Baxter Healthcare Limited. Furosemide 10 mg/ml Solution for Injection - Summary of Product Characteristics. emc.
- [MSF Essential Drugs - Furosemide oral](https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-oral-16683798.html): Medecins Sans Frontieres. Essential drugs - practical guidelines: Furosemide, oral.
- [MSF Essential Drugs - Furosemide injectable](https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-injectable-16682724.html): Medecins Sans Frontieres. Essential drugs - practical guidelines: Furosemide, injectable.
- [Philippine National Formulary EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary - Essential Medicines List, 8th ed. PhilHealth; 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC - Furosemide 40 mg tablets](https://products.mhra.gov.uk/search/?search=furosemide#emc-12129): Furosemide 40 mg tablets - SmPC. emc.
- Dosing source `Label · UK SmPC inj`: [UK SmPC - Furosemide 10 mg/ml Solution for Injection](https://products.mhra.gov.uk/search/?search=furosemide#emc-11522): Baxter Healthcare Limited. Furosemide 10 mg/ml Solution for Injection - SmPC. emc.
- Dosing source `Label · DailyMed`: [DailyMed - LASIX tablets](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2c9b4d8f-0770-482d-a9e6-9c616a440b1a): LASIX (furosemide) tablets. Prescribing information. DailyMed.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-injectable-16682724.html): Medecins Sans Frontieres. Essential drugs: Furosemide oral / injectable.
- Dosing source `PNF`: [Philippine National Formulary EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary - Essential Medicines List, 8th ed. PhilHealth; 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF EML p.22: furosemide oral 20 mg and 40 mg tablet (B); inj. 10 mg/mL 2 mL ampul (IM, IV); 10 mg/mL 25 mL ampul (IV infusion). (B) = List B, in vivo bioequivalence.
- https://products.mhra.gov.uk/search/?search=furosemide#emc-12129: Oral posology (oedema 40 mg, maintenance 20 mg/40 mg alt days, 80 mg resistant; HTN 20–40 mg 2×), elderly, CrCl <30 contraindication, hepatic adjustment, full contraindication list, interactions (risperidone, cisplatin, digoxin, cephalosporins, methotrexate, colestyramine 2–3 h), pregnancy/breastfeeding, monitoring (BUN, electrolytes, blood dyscrasias), adverse effects incl. hypocalcaemia, acute renal failure, anaphylaxis, premature infant nephrocalcinosis.
- https://products.mhra.gov.uk/search/?search=furosemide#emc-11522: Baxter injection SmPC: adult IV/IM 20–50 mg, +20 mg steps ≥2 h apart, >50 mg by infusion, max 1500 mg/day; max 4 mg/min (2.5 mg/min if creatinine >5 mg/dL); children 0.5–1.5 mg/kg/day max 20 mg/day; continuous infusion preferred; IM unsuitable for pulmonary oedema; monitoring Na/K/creatinine, urinary output, diabetes.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2c9b4d8f-0770-482d-a9e6-9c616a440b1a: Pediatric oral 2 mg/kg, +1–2 mg/kg after ≥6–8 h, >6 mg/kg not recommended; interactions chloral hydrate, cyclosporine (gout), radiocontrast, methotrexate.
- https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-oral-16683798.html: Oral 20 mg start, max 160 mg/day; take in morning; not for nutritional or pre-eclampsia oedema; breastfeeding contraindicated; hyperglycaemia with antidiabetics.
- https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-injectable-16682724.html: Acute pulmonary oedema 40 mg IV, 80 mg if no response in 1 h; hypertensive crisis (not in pregnancy); not for kwashiorkor oedema or hepatic encephalopathy; digoxin toxicity.

---

## Gliclazide  (`med_gliclazide`)

**Description (kept)**

Gliclazide is a second-generation sulfonylurea that binds the SUR1 subunit of ATP-sensitive potassium channels on pancreatic beta cells, causing depolarization, calcium influx and insulin release regardless of blood glucose level. Hypoglycemia and weight gain are the main drawbacks. It is used in type 2 diabetes when metformin alone is insufficient or not tolerated; it is not marketed in the United States.

**Description (added)**

In the Philippines it is listed in the PNF Essential Medicines List as 30 mg and 60 mg modified-release tablets and an 80 mg tablet, and it has been on the WHO Model List of Essential Medicines since 2013. MSF guidance places it second line, alone when metformin is not tolerated or added to metformin when control is inadequate. It is cleared mainly by hepatic metabolism (under 1% excreted unchanged in urine) and is about 95% protein-bound, so dialysis does not help in overdose.

**Uses**: 1 kept, 1 added

- NEW: Add-on to metformin when glycaemic control is inadequate on metformin alone

**Side effects**: 7 kept, 4 added

- NEW: Cholestatic jaundice (stop treatment)
- NEW: DRESS (very rare)
- NEW: Hyponatraemia, allergic vasculitis, agranulocytosis and pancytopenia (sulfonylurea class effects)
- NEW: Acute porphyria reported with other sulfonylureas in patients with porphyria

**Interactions**: 5 kept, 5 added

- NEW: H2 antagonists, MAOIs, sulfonamides (e.g., co-trimoxazole), trimethoprim, anabolic steroids: increased hypoglycaemia risk.
- NEW: Macrolides (clarithromycin, erythromycin): increased hypoglycaemia risk; monitor glucose.
- NEW: IV salbutamol, terbutaline or ritodrine, and tetracosactide: raised blood glucose.
- NEW: Rifampicin and St John's wort: reduced gliclazide effect or exposure.
- NEW: Hydrochlorothiazide: may raise blood glucose and reduce control.

**Disease links added**

- `chronic_kidney_disease`: **caution**: Mild–moderate renal impairment: usual dose with careful monitoring; contraindicated in severe renal insufficiency (use insulin).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Type 2 diabetes (MR tablet) (With breakfast; step up to 60, 90, 120 mg at ≥1-month intervals (2 weeks if glucose not falling)) | PO | 30 mg | Once a day | Long-term | 120 mg/day | Label · UK SmPC MR |
| adult | Type 2 diabetes (80 mg tablet) (Max 160 mg per dose; above 160 mg/day give 2× a day with main meals) | PO | 40–80 mg | Once a day | Long-term | 320 mg/day | Label · UK SmPC |
| adult | Type 2 diabetes, second line (80 mg tablet) (Morning dose; increase by 40 mg every 2 weeks; split doses above 80 mg/day into 2) | PO | 40 mg, then 80–160 mg/day | Once a day | Long-term | 240 mg/day | MSF |

- *renal*: Mild–moderate impairment: same regimen with careful monitoring. Severe renal insufficiency: contraindicated (insulin recommended). Not removed by dialysis (strongly protein-bound). [Label · UK SmPC MR]
- *hepatic*: Severe hepatic insufficiency: contraindicated (insulin recommended). Stop if cholestatic jaundice develops. [Label · UK SmPC MR]
- *elderly*: Same regimen as under 65. Start at the minimum dose (30 mg MR / 40–80 mg) in high-risk patients: malnourished, poorly controlled endocrine disease (hypopituitarism, hypothyroidism, adrenal insufficiency), after stopping long-term/high-dose steroids, or severe vascular disease. [Label · UK SmPC MR]
- *pregnancy*: Avoid in pregnancy; switch to insulin before conception or as soon as pregnancy is found. Contraindicated in breastfeeding (risk of neonatal hypoglycaemia). [Label · UK SmPC MR]
- *administration*: MR tablet: swallow whole as one dose at breakfast; do not double a missed dose. One 80 mg tablet ≈ one 30 mg MR tablet when switching (monitor glucose). After a long half-life sulfonylurea, a few drug-free days may be needed. Not for children (no data). [Label · UK SmPC MR]
- *forms_ph*: Gliclazide 30 mg and 60 mg modified-release (MR) oral tablets; 80 mg oral tablet. [PNF]
- *monitor*: Blood glucose/HbA1c; teach patient and family hypoglycaemia symptoms and risk factors (missed meals, alcohol, exercise); close glucose checks with fluoroquinolones, illness or surgery; consider an alternative in G6PD deficiency. Hypoglycaemic coma: 50 mL 20–30% glucose IV, then 10% glucose infusion with close monitoring. [Label · UK SmPC MR]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=gliclazide#emc-13676): Gliclazide 80 mg Tablets. Summary of Product Characteristics. Flamingo Pharma (UK) Ltd. electronic medicines compendium (emc); text revised 01/2025.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/gliclazide-oral-27983946.html): Médecins Sans Frontières. Gliclazide oral. In: Essential Drugs – practical guidelines. MSF Medical Guidelines.
- [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.
- [WHO Model List of Essential Medicines](https://list.essentialmeds.org/medicines/194): World Health Organization. eEML – Electronic Essential Medicines List: Gliclazide (first added 2013, TRS 985).
- Dosing source `Label · UK SmPC MR`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=gliclazide#emc-1321): Diamicron 30 mg MR Tablets SmPC, Servier; text revised 02/2020.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=gliclazide#emc-13676): Gliclazide 80 mg Tablets SmPC, Flamingo Pharma (UK) Ltd; text revised 01/2025.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/gliclazide-oral-27983946.html): Médecins Sans Frontières. Gliclazide oral. Essential Drugs – practical guidelines.
- Dosing source `PNF`: [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): PNF Essential Medicines List, 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF-EML lists Gliclazide 'Oral: 30 mg and 60 mg MR tablet' and '80 mg tablet'.
- https://products.mhra.gov.uk/search/?search=gliclazide#emc-1321: Diamicron 30 mg MR SmPC (Servier, text rev 02/2020): 30 mg od at breakfast, titration 60/90/120 mg at ≥1 month (2 weeks if no fall), max 120 mg; 80 mg IR ≈ 30 mg MR; elderly same; mild-moderate renal careful monitoring, severe renal/hepatic contraindicated; high-risk start 30 mg; no paediatric data; pregnancy avoid/insulin; lactation contraindicated (neonatal hypoglycaemia); ADRs incl. DRESS, cholestatic jaundice, class effects (hyponatraemia, vasculitis, agranulocytosis, pancytopenia); porphyria; interactions incl. H2 antagonists, MAOIs, sulfonamides, clarithromycin, IV salbutamol/terbutaline/ritodrine, tetracosactide, St John's wort; overdose 50 mL 20–30% glucose then 10% infusion; dialysis not beneficial (protein-bound); <1% unchanged in urine, ~95% protein binding.
- https://products.mhra.gov.uk/search/?search=gliclazide#emc-13676: Gliclazide 80 mg Tablets SmPC (Flamingo, rev 30/01/2025): 40–80 mg/day start, 40–320 mg/day, single dose max 160 mg, >160 mg/day twice daily with main meals; interactions incl. trimethoprim and anabolic steroids (hypoglycaemia).
- https://medicalguidelines.msf.org/viewport/EssDr/english/gliclazide-oral-27983946.html: MSF Gliclazide oral: second-line T2D (>60 y) monotherapy if metformin not tolerated or with metformin; 40 mg od weeks 1–2, +40 mg every 2 weeks, usual 80–160 mg/day, max 240 mg/day; split >80 mg/day into 2 doses; interactions: erythromycin, co-trimoxazole, ciprofloxacin (hypoglycaemia), rifampicin (reduced effect), hydrochlorothiazide raises glucose.
- https://list.essentialmeds.org/medicines/194: WHO eEML: gliclazide, hypoglycaemic agents section, oral solid 30/60/80 mg, first added 2013 (TRS 985) for type 2 diabetes.

---

## Hydrochlorothiazide  (`med_hydrochlorothiazide`)

**Description (kept)**

Hydrochlorothiazide inhibits the Na+/Cl- cotransporter in the distal convoluted tubule, increasing sodium and water excretion. Blood pressure falls initially from volume reduction and long-term from reduced peripheral vascular resistance. It is used alone or in combination for hypertension and for edema, and is less effective when renal function is severely reduced.

**Description (added)**

In the Philippines it is listed in the PNF Essential Medicines List as 12.5 mg and 25 mg tablets and in fixed combinations with losartan, enalapril and irbesartan. In the national primary-care hypertension protocol, hydrochlorothiazide 25 mg once daily is the step-4 add-on to amlodipine plus losartan (or the patient is referred). Long-term use carries a dose-dependent risk of non-melanoma skin cancer, thought to relate to its photosensitising effect.

**Side effects**: 8 kept, 9 added

- NEW: Dehydration and hypotension, including orthostatic hypotension
- NEW: Headache, dizziness, vertigo, paraesthesia
- NEW: Impotence
- NEW: Non-melanoma skin cancer (basal cell and squamous cell carcinoma, lip cancer) with high cumulative long-term use
- NEW: Interstitial nephritis, renal dysfunction
- NEW: Sialadenitis
- NEW: Hypersensitivity: anaphylaxis, necrotising angiitis, pneumonitis, pulmonary oedema
- NEW: Exacerbation or activation of systemic lupus erythematosus
- NEW: Transient blurred vision, xanthopsia

**Precautions**: 2 kept, 1 added

- NEW: Severe renal failure

**Interactions**: 5 kept, 7 added

- NEW: Cholestyramine and colestipol: reduce hydrochlorothiazide absorption (by up to 85% and 43%).
- NEW: Drugs that cause hypotension (e.g., haloperidol, amitriptyline) and other antihypertensives: additive hypotension.
- NEW: SSRIs, carbamazepine: added risk of hyponatraemia.
- NEW: Laxatives, amphotericin B: added potassium loss.
- NEW: Calcium or vitamin D (ergocalciferol): risk of hypercalcaemia.
- NEW: Pressor amines (e.g., noradrenaline): possibly reduced response.
- NEW: Nondepolarising muscle relaxants: possibly increased response.

**Disease links added**

- `chronic_kidney_disease`: **caution**: Use with caution in severe renal disease (may precipitate azotemia; stop if impairment progresses); MSF advises not to give in severe renal failure.
- `type2_diabetes`: **caution**: Can raise blood glucose; doses of oral antidiabetics or insulin may need adjusting.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Hypertension (Morning dose) | PO | 12.5–25 mg | Once a day | Long-term | 25 mg/day | MSF |
| adult | Hypertension (PH primary care, step 4) (Added to amlodipine 10 mg + losartan 100 mg if BP still high after 1 month (or refer)) | PO | 25 mg | Once a day | Long-term | — | PH HTN protocol |
| adult | Hypertension (Doses above 50 mg/day cause marked potassium loss) | PO | 25 mg, up to 50 mg/day | Once a day or 2× a day | Long-term | 50 mg/day | Label · DailyMed |
| adult | Oedema (renal, hepatic, heart failure) (Morning dose) | PO | 25 mg | Once a day or 2× a day | By response | 100 mg/day | MSF |
| adult | Oedema (Intermittent dosing (alternate days or 3–5 days a week) lowers electrolyte risk) | PO | 25–100 mg/day | Once a day or divided | By response | 100 mg/day | Label · DailyMed |
| child | Oedema / hypertension (Infants <6 months may need up to 3 mg/kg/day ÷ 2) | PO | 1–2 mg/kg/day ÷ 1–2 | Once a day or 2× a day | By response | 37.5 mg/day (<2 y); 100 mg/day (2–12 y) | Label · DailyMed |

- *renal* Severe: Do not give in severe renal failure. [MSF]
- *renal*: Use with caution in severe renal disease: may precipitate azotemia and accumulate; withhold or stop if renal impairment progresses. [Label · DailyMed]
- *hepatic*: Use with caution in hepatic impairment or progressive liver disease: small fluid/electrolyte shifts may precipitate hepatic coma. [Label · DailyMed]
- *elderly*: Use with caution. [MSF]
- *pregnancy*: MSF lists pregnancy and breastfeeding as contraindications. Thiazides cross the placenta (risk of fetal/neonatal jaundice and thrombocytopenia) and pass into breast milk; routine use in normal pregnancy is inappropriate. [MSF]
- *administration*: Take in the morning. Recommend a potassium-rich diet; give a sustained-release potassium supplement if K+ < 3.5 mmol/L. Not indicated for nutritional oedema. Stop before parathyroid function tests. [MSF]
- *forms_ph*: Hydrochlorothiazide 12.5 mg and 25 mg oral tablets. Fixed combinations: losartan 50 mg + HCTZ 12.5 mg, enalapril 20 mg + HCTZ 12.5 mg, irbesartan 150 mg + HCTZ 12.5 mg tablets. [PNF]
- *monitor*: Serum electrolytes (K+, Na+, Mg2+, Ca2+), renal function, glucose, uric acid and lipids periodically; BP including orthostatic drop; confirm adherence before stepping up. [Label · DailyMed]
- *monitor*: Long-term use: advise regular skin self-checks and sun/UV protection; examine new or changing lesions; reconsider HCTZ in patients with previous skin cancer. [MHRA 2018]

**References added**

- [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/hydrochlorothiazide-oral-16683854.html): Médecins Sans Frontières. Hydrochlorothiazide oral. In: Essential Drugs – practical guidelines. MSF Medical Guidelines.
- [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.
- [National Protocol for Hypertension Management (Philippines)](https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf): National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives; 2021 (rev. 2023).
- [MHRA Drug Safety Update](https://www.gov.uk/drug-safety-update/hydrochlorothiazide-risk-of-non-melanoma-skin-cancer-particularly-in-long-term-use): Medicines and Healthcare products Regulatory Agency. Hydrochlorothiazide: risk of non-melanoma skin cancer, particularly in long-term use. Drug Safety Update 2018;12(4).
- [WHO Model List of Essential Medicines](https://list.essentialmeds.org/medicines/139): World Health Organization. eEML – Electronic Essential Medicines List: Hydrochlorothiazide (first added 1977).
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/hydrochlorothiazide-oral-16683854.html): Médecins Sans Frontières. Hydrochlorothiazide oral. Essential Drugs – practical guidelines.
- Dosing source `Label · DailyMed`: [DailyMed (US National Library of Medicine)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=7b38ac8a-4540-4eb2-aedd-9aa966d22190): Hydrochlorothiazide Tablets USP 25 mg and 50 mg. Prescribing information. Caraco Pharmaceutical Laboratories; 2007.
- Dosing source `PH HTN protocol`: [National Protocol for Hypertension Management (Philippines)](https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf): National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives.
- Dosing source `PNF`: [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): PNF Essential Medicines List, 2022.
- Dosing source `MHRA 2018`: [MHRA Drug Safety Update](https://www.gov.uk/drug-safety-update/hydrochlorothiazide-risk-of-non-melanoma-skin-cancer-particularly-in-long-term-use): Hydrochlorothiazide: risk of non-melanoma skin cancer, particularly in long-term use. Drug Safety Update, November 2018.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF-EML lists Hydrochlorothiazide 'Oral: 12.5 mg and 25 mg tablet' and combinations: enalapril 20 mg + HCTZ 12.5 mg, irbesartan 150 mg + HCTZ 12.5 mg, losartan 50 mg + HCTZ 12.5 mg tablets.
- https://medicalguidelines.msf.org/viewport/EssDr/english/hydrochlorothiazide-oral-16683854.html: MSF Hydrochlorothiazide oral: hypertension 12.5–25 mg od morning max 25 mg/day; oedema 25 mg od or bid max 100 mg/day; contraindicated severe renal failure, pregnancy, breastfeeding; caution elderly; ADRs dehydration, hypotension, headache, dizziness, impotence, photosensitivity; interactions haloperidol/amitriptyline, corticosteroids/laxatives/amphotericin B, SSRIs/carbamazepine, calcium/ergocalciferol, antidiabetics; potassium-rich diet, SR K if <3.5 mmol/L; not for nutritional oedema.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=7b38ac8a-4540-4eb2-aedd-9aa966d22190: DailyMed Caraco HCTZ label (2007; already in refs, used only as a dose-table source): adult edema 25–100 mg/day, intermittent dosing; hypertension 25 mg up to 50 mg/day; children 1–2 mg/kg/day, max 37.5 mg (<2 y) / 100 mg (2–12 y), infants <6 mo up to 3 mg/kg/day in 2 doses; caution severe renal disease (azotemia) and hepatic disease (hepatic coma); SLE; cholestyramine 85%/colestipol 43%; pressor amines; muscle relaxants; ADRs sialadenitis, interstitial nephritis, anaphylaxis, pneumonitis, xanthopsia; stop before parathyroid tests; placenta/neonatal jaundice/thrombocytopenia.
- https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf: PH primary-care protocol: step 4 'Add hydrochlorothiazide 25 mg once daily' OR refer, after 1 month if BP still high; check adherence before stepping up.
- https://www.gov.uk/drug-safety-update/hydrochlorothiazide-risk-of-non-melanoma-skin-cancer-particularly-in-long-term-use: MHRA DSU Nov 2018: dose-dependent NMSC (BCC, SCC, lip) risk with cumulative HCTZ; inform patients, skin self-checks, limit sun/UV, examine lesions, reconsider in previous skin cancer; photosensitising mechanism.
- https://list.essentialmeds.org/medicines/139: WHO eEML: hydrochlorothiazide first added 1977 (hypertension, oedema), heart failure 1997; oral solid 12.5/25 mg, oral liquid 50 mg/5 mL.

---

