# Medicine review b02: review sheet

Run `034_medicines_review_02.sql` in Supabase after you have checked this. Everything below is ADDED; the existing text stays as it is.

Every link was opened twice: by the research step (to read the fact), and again in Akeso's own browser pane on your computer in the Philippines (to make sure it opens for you, not just from the cloud). See NOTES.md in the batch folder for any link that needs attention.

UK SmPC links open the official MHRA Products search (free) for that medicine: the emc site (medicines.org.uk) now limits free page views for users outside the UK. The citation still names the exact product and PL number to pick.

## Please check (batch 02)

- **Ceftriaxone → acute gastroenteritis, *safe*:** this is for shigellosis only (MSF). The note says it is not for routine watery gastroenteritis. Drop the link if it is too broad.
- **Ceftriaxone:** the UK label says 2 g for surgical prophylaxis; the existing text (US label) says 1 g. The UK kidney limit is 2 g/day only when CrCl < 10. Many rows can be given IV or IM; the route column says IV and the note says "IV or IM".
- **Cetirizine:** the UK label says no dose change for liver disease alone; the existing text (US) says 5 mg. The UK kidney bands use eGFR.
- **Budesonide-formoterol:** the inhaler is written as delivered dose (80/4.5, 160/4.5) to match the PNF; the UK label calls the same products 100/6 and 200/6.
- **Ciprofloxacin:** links to type 2 diabetes and hypertension (caution) are readings of label warnings. Breastfeeding: the UK label says avoid; MSF lists no contraindication.
- **Clopidogrel:** the UK label says stop 7 days before surgery; the existing text says 5 days (US). Both are kept.
- **Co-amoxiclav → rabies, *safe*:** this is antibiotic cover for animal bites, not rabies treatment (the note says so). **Co-trimoxazole → rheumatic fever, *avoid*:** not recommended for strep throat; linking it to rheumatic fever is an inference.
- **Colchicine → acute coronary syndrome, *safe*:** the Lodoco label is for long-term risk reduction in heart disease, not acute ACS treatment.
- **Dapagliflozin:** the UK label says don't start below eGFR 15; the US label says 25. The UK starting dose for diabetes is 10 mg; the US is 5 mg. Both rows are shown. The PH form (10 mg tablet, PNF since April 2023) comes from PhilHealth Advisory 2024-0026.
- **Brands:** none added; no verified FDA PH page.


---

## Budesonide + Formoterol  (`med_budesonide_formoterol`)

**Description (kept)**

Budesonide is an inhaled glucocorticoid that suppresses airway inflammation, and formoterol is a long-acting beta-2 agonist with a rapid onset of bronchodilation. The combination provides maintenance control of asthma and COPD. Because formoterol acts quickly, GINA also recommends budesonide-formoterol as an as-needed anti-inflammatory reliever and for maintenance-and-reliever therapy in asthma, whereas US labeling covers maintenance use only.

**Description (added)**

UK labeling licenses the dry-powder inhaler for three asthma regimens: maintenance only, maintenance-and-reliever (12 years and older), and reliever-only in mild asthma (12 years and older). Strengths may be stated as metered dose (e.g. 200/6 mcg) or delivered dose (160/4.5 mcg); these are the same product. In the Philippines the PNF lists both a dry-powder inhaler and a metered-dose inhaler.

**Side effects**: 8 kept, 8 added

- NEW: Throat irritation, cough and hoarseness
- NEW: Anxiety, sleep disorders, aggression and psychomotor hyperactivity (uncommon)
- NEW: Dizziness, nausea, blurred vision (uncommon)
- NEW: Bruising and muscle cramps (uncommon)
- NEW: Paradoxical bronchospasm (very rare; stop and use a rapid-acting bronchodilator)
- NEW: Growth retardation in children (very rare)
- NEW: QTc prolongation, cardiac arrhythmias, angina (rare to very rare)
- NEW: Taste disturbance, depression and behavioural changes (very rare)

**Precautions**: 2 kept, 1 added

- NEW: Turbohaler: hypersensitivity to lactose (contains small amounts of milk proteins)

**Interactions**: 5 kept, 6 added

- NEW: QT-prolonging drugs (e.g., quinidine, disopyramide, phenothiazines): increased risk of ventricular arrhythmias.
- NEW: Xanthines (e.g., theophylline) and systemic corticosteroids: additive hypokalaemia.
- NEW: Digitalis glycosides: hypokalaemia raises the risk of arrhythmias.
- NEW: Halogenated hydrocarbon anaesthetics: increased arrhythmia risk.
- NEW: L-dopa, L-thyroxine, oxytocin and alcohol: may impair cardiac tolerance to beta-2 agonists.
- NEW: Strong CYP3A4 inhibitors: maintenance-and-reliever therapy is not recommended with them.

**Disease links added**

- `tuberculosis`: **caution**: Re-evaluate use in active or quiescent pulmonary TB (UK SmPC).
- `type2_diabetes`: **caution**: Beta-2 agonist can raise glucose; consider extra blood glucose checks (UK SmPC).
- `graves_disease`: **caution**: Use with caution in thyrotoxicosis (UK SmPC).
- `hypertension`: **caution**: Use with caution in severe hypertension (UK SmPC).
- `heart_failure`: **caution**: Use with caution in severe heart failure or tachyarrhythmias (UK SmPC).
- `acute_coronary_syndrome`: **caution**: Use with caution in ischaemic heart disease (UK SmPC).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Asthma, maintenance (DPI 160/4.5) (Separate reliever for rescue; UK labels this as 200/6 (metered)) | Inhaled | 1–2 inhalations | 2× a day | Long-term | 4 inhalations 2× a day | Label · UK SmPC |
| adult | Asthma, maintenance-and-reliever (DPI 160/4.5) (>8 inhalations/day: reassess) | Inhaled | 2 inhalations/day + 1 as needed | Once or 2× a day + as needed | Long-term | 6 per occasion; 12/day short-term | Label · UK SmPC |
| adult | Mild asthma, reliever only (DPI 160/4.5) (Repeat once if still symptomatic after a few minutes) | Inhaled | 1 inhalation | As needed | — | 6 per occasion; 12/day short-term | Label · UK SmPC |
| adult | Asthma, maintenance (pMDI 80/4.5 or 160/4.5) (Strength by severity and prior ICS) | Inhaled | 2 inhalations | 2× a day | Long-term | 160/4.5 strength | Label · US |
| adult | COPD (160/4.5) | Inhaled | 2 inhalations | 2× a day | Long-term | — | Label · UK SmPC |
| child | Asthma, maintenance, 12–17 y (DPI) (80/4.5 or 160/4.5) | Inhaled | 1–2 inhalations | 2× a day | Long-term | — | Label · UK SmPC |
| child | Asthma, maintenance-and-reliever, 12–17 y (DPI 80/4.5) (>8 inhalations/day: reassess) | Inhaled | 2 inhalations/day + 1 as needed | Once or 2× a day + as needed | Long-term | 6 per occasion; 12/day short-term | Label · UK SmPC 100/6 |
| child | Asthma, maintenance, 6–11 y (DPI 80/4.5) (Not recommended <6 y) | Inhaled | 1–2 inhalations | 2× a day | Long-term | — | Label · UK SmPC 100/6 |
| child | Asthma, maintenance-and-reliever, 6–11 y (DPI 80/4.5) (>4 inhalations/day: reassess) | Inhaled | 1 inhalation + 1 as needed | Once or 2× a day + as needed | Long-term | 4 per occasion; 8/day short-term | Label · UK SmPC 100/6 |
| child | Asthma, maintenance, 6–11 y (pMDI 80/4.5) | Inhaled | 2 inhalations | 2× a day | Long-term | — | Label · US |

- *renal*: No data available in renal impairment. [Label · UK SmPC]
- *hepatic*: No data; exposure may rise in severe liver cirrhosis because both drugs are cleared mainly by the liver. Monitor closely. [Label · UK SmPC]
- *elderly*: No special dosing requirements. [Label · UK SmPC]
- *pregnancy*: Use only if benefit outweighs risk, at the lowest effective budesonide dose; ~2,000 pregnancies with inhaled budesonide showed no rise in malformations; formoterol data inadequate. Budesonide passes into breast milk; no infant effects expected at therapeutic doses. [Label · UK SmPC]
- *administration*: Turbohaler: breathe in forcefully and deeply through the mouthpiece; never breathe out into it; replace cover. Patients may not taste the dose. [Label · UK SmPC 100/6]
- *administration*: pMDI: shake for 5 seconds before each spray; spray 2 test puffs before first use or if dropped or unused >7 days; take doses about 12 h apart. [Label · US]
- *administration*: Do not stop abruptly; taper the maintenance dose. Do not start during an exacerbation. [Label · UK SmPC]
- *forms_ph*: DPI 80/4.5 mcg, 160/4.5 mcg and 320/9 mcg × 60 doses; MDI 80/4.5 mcg and 160/4.5 mcg × 120 doses. [PNF]
- *monitor*: Track reliever use: rising use or >8 inhalations/day (adults) means poor control; reassess. [Label · UK SmPC]
- *monitor*: Check height regularly in children on long-term treatment. [Label · UK SmPC]
- *monitor*: Check serum potassium in acute severe asthma; check blood glucose in diabetes. [Label · UK SmPC]
- *monitor*: Check adrenal function when switching from oral steroids; watch for pneumonia in COPD. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1327): Symbicort Turbohaler 200/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd; updated March 2023. electronic medicines compendium (emc).
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1326): Symbicort Turbohaler 100/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd. electronic medicines compendium (emc).
- [PhilHealth / DOH (PNF-EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1327): Symbicort Turbohaler 200/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd; March 2023.
- Dosing source `Label · UK SmPC 100/6`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1326): Symbicort Turbohaler 100/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd.
- Dosing source `Label · US`: [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6b78d08a-e098-4188-8f7f-94fbd5f396ef): SYMBICORT (budesonide and formoterol fumarate dihydrate) inhalation aerosol. Prescribing information. AstraZeneca; revised 10/2024.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Budesonide + Formoterol inhalation: DPI 80/4.5, 160/4.5 (fumarate dihydrate) x 60 doses, 320/9 x 60 doses; MDI 80/4.5 and 160/4.5 x 120 doses; no restriction.
- https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1327: Symbicort Turbohaler 200/6 SmPC (AstraZeneca, 22 Mar 2023): delivered dose 160/4.5 = 200/6 metered; Therapy A adults 1–2 inh BD up to 4 BD, adolescents 1–2 BD; Therapy B 2 inh/day + 1 as needed, max 6/occasion, >8/day not normally needed, up to 12/day limited period; Therapy C mild asthma 1 as needed; COPD 2 inh BD; renal/hepatic no data, severe cirrhosis exposure; elderly none; pregnancy ~2000; breast milk; ADR table (throat irritation, cough, hoarseness, anxiety, aggression, sleep disorders, dizziness, blurred vision, nausea, bruising, muscle cramps, paradoxical bronchospasm, growth retardation, QTc, taste, depression, angina); interactions (QT drugs, xanthines/corticosteroids, digitalis, halogenated anaesthetics, L-dopa/L-thyroxine/oxytocin/alcohol, MART not recommended with strong CYP3A4 inhibitors); 4.3 lactose/milk proteins; 4.4 thyrotoxicosis, severe hypertension, ischaemic heart disease, severe heart failure, diabetes glucose, TB, potassium in acute severe asthma, height in children, adrenal function, pneumonia in COPD, taper.
- https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1326: Symbicort Turbohaler 100/6 SmPC: delivered 80/4.5; maintenance 6–11 y and 12–17 y 1–2 inh BD; MART 6–11 y 1 inh once/twice daily + as needed, max 4/occasion, >4/day not normally needed, up to 8/day; adolescents MART max 6/occasion, 8/day (12 short-term); not recommended <6 y; Turbohaler technique, rinse mouth.
- https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6b78d08a-e098-4188-8f7f-94fbd5f396ef: Symbicort US label (rev 10/2024): 6 to <12 y 2 inh of 80/4.5 BD; ≥12 y 2 inh 80/4.5 or 160/4.5 BD by severity; COPD 160/4.5 2 inh BD; max 160/4.5; shake 5 s, 2 test sprays, re-prime if dropped or >7 days; ~12 h apart; hepatic disease monitor closely.

---

## Ceftriaxone  (`med_ceftriaxone`)

**Description (kept)**

Ceftriaxone is a parenteral third-generation cephalosporin that binds penicillin-binding proteins and disrupts peptidoglycan cross-linking, producing bactericidal activity. Its long half-life permits once-daily dosing, and it is widely used for pneumonia, meningitis, pyelonephritis, typhoid fever, gonorrhea and sepsis.

**Description (added)**

In the Philippines, the PhilHealth CAP policy (based on the 2016 PSMID guideline) lists ceftriaxone 2 g IV once daily, combined with a macrolide or a respiratory fluoroquinolone, for moderate-risk CAP and for high-risk CAP without Pseudomonas risk. The PNF lists IM vials (reconstituted with 1% lidocaine) and IV vials.

**Uses**: 7 kept, 11 added

- NEW: Hospital-acquired pneumonia
- NEW: Acute bacterial exacerbations of COPD
- NEW: Bacterial endocarditis
- NEW: Febrile neutropenia with suspected bacterial infection
- NEW: Acute otitis media (single IM dose)
- NEW: Syphilis, including neurosyphilis
- NEW: Lyme borreliosis
- NEW: Shigellosis
- NEW: Chancroid
- NEW: Gonococcal conjunctivitis (adults and neonates)
- NEW: Tick-borne relapsing fever

**Side effects**: 7 kept, 8 added

- NEW: Eosinophilia, leucopenia, thrombocytopenia
- NEW: Raised liver enzymes and rash
- NEW: Encephalopathy (mainly elderly with severe renal impairment or CNS disorders)
- NEW: Convulsions
- NEW: Severe skin reactions: SJS/TEN, DRESS, AGEP
- NEW: Renal precipitation with oliguria
- NEW: Kernicterus in neonates
- NEW: Jarisch-Herxheimer reaction in spirochaete infections

**Precautions**: 4 kept, 2 added

- NEW: Severe hypersensitivity (e.g., anaphylaxis) to any other beta-lactam
- NEW: Full-term neonates (≤28 days) with hypoalbuminaemia or acidosis

**Interactions**: 3 kept, 3 added

- NEW: Chloramphenicol: antagonism seen in vitro.
- NEW: Vancomycin, fluconazole and amsacrine: physically incompatible; do not mix.
- NEW: Lab tests: false-positive Coombs test, galactosaemia tests and non-enzymatic urine glucose; may falsely lower some glucose-meter readings.

**Disease links added**

- `chronic_kidney_disease`: **caution**: Limit to 2 g/day when CrCl <10 mL/min; not removed by dialysis (UK SmPC).
- `copd`: **safe**: Licensed for acute bacterial exacerbations of COPD (UK SmPC).
- `acute_gastroenteritis`: **safe**: Used for shigellosis (bacillary dysentery) only, not for routine watery gastroenteritis (MSF).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | CAP, cUTI/pyelonephritis, intra-abdominal infection (IV or IM; Adults and children ≥50 kg) | IV | 1–2 g | Once a day | Until 48–72 h afebrile | — | Label · UK SmPC |
| adult | CAP, moderate or high risk (PH) (With a macrolide or respiratory fluoroquinolone) | IV | 2 g | Once a day | — | — | PhilHealth CAP 2016 |
| adult | HAP, skin/soft tissue, bone and joint infection (IV or IM) | IV | 2 g | Once a day | — | — | Label · UK SmPC |
| adult | Meningitis, endocarditis, neutropenic fever (Doses >2 g/day may be split 2× a day) | IV | 2–4 g | Once a day | — | 4 g/day | Label · UK SmPC |
| adult | Typhoid fever, meningitis | IV | 2 g 2× a day or 4 g once | Every 12 h or once a day | Switch to oral when possible | 4 g/day | MSF 2023 |
| adult | Uncomplicated gonorrhoea (Plus chlamydia treatment (MSF)) | IM | 500 mg | Single dose | 1 day | — | Label · UK SmPC |
| adult | Gonococcal conjunctivitis | IM | 1 g | Single dose | 1 day | — | MSF 2023 |
| adult | Chancroid | IM | 250 mg | Single dose | 1 day | — | MSF 2023 |
| adult | Acute otitis media | IM | 1–2 g | Single dose | 1 day | — | Label · UK SmPC |
| adult | Syphilis (IV or IM) | IV | 500 mg–1 g | Once a day | 10–14 days | 2 g/day (neurosyphilis) | Label · UK SmPC |
| adult | Lyme borreliosis (IV or IM) | IV | 2 g | Once a day | 14–21 days | — | Label · UK SmPC |
| adult | Surgical prophylaxis (Give 30–90 min before surgery) | IV | 2 g | Single dose | 1 day | — | Label · UK SmPC |
| child | CAP, HAP, cUTI, intra-abdominal (15 d–12 y, <50 kg) (IV or IM; ≥50 kg: adult dose) | IV | 50–80 mg/kg | Once a day | Until 48–72 h afebrile | — | Label · UK SmPC |
| child | Skin/soft tissue, bone/joint, neutropenic fever (IV or IM) | IV | 50–100 mg/kg | Once a day | — | 4 g/day | Label · UK SmPC |
| child | Bacterial meningitis | IV | 80–100 mg/kg | Once a day | — | 4 g/day | Label · UK SmPC |
| child | Bacterial endocarditis | IV | 100 mg/kg | Once a day | — | 4 g/day | Label · UK SmPC |
| child | Severe bacterial infections (≥1 mo, <50 kg) (IV or IM) | IV | 50–100 mg/kg | Once a day | Switch to oral when possible | 4 g/day | MSF 2023 |
| child | Acute otitis media | IM | 50 mg/kg | Single dose | 1 day | — | Label · UK SmPC |
| child | Gonorrhoea, chancroid (<45 kg) | IM | 125 mg | Single dose | 1 day | — | MSF 2023 |
| child | Syphilis (IV or IM) | IV | 75–100 mg/kg | Once a day | 10–14 days | 4 g/day | Label · UK SmPC |
| child | Lyme borreliosis (IV or IM) | IV | 50–80 mg/kg | Once a day | 14–21 days | — | Label · UK SmPC |
| child | Surgical prophylaxis | IV | 50–80 mg/kg | Single dose | 1 day | — | Label · UK SmPC |
| neonate | Most infections (0–14 days) (IV or IM; Contraindicated if premature (<41 wk PMA); IV over 60 min) | IV | 20–50 mg/kg | Once a day | — | 50 mg/kg/day | Label · UK SmPC |
| neonate | Meningitis, endocarditis (0–14 days) | IV | 50 mg/kg | Once a day | — | 50 mg/kg/day | Label · UK SmPC |
| neonate | Gonococcal conjunctivitis | IM | 50 mg/kg | Single dose | 1 day | 125 mg | MSF 2023 |

- *renal* CrCl ≥10: No reduction needed if liver function is normal. [Label · UK SmPC]
- *renal* CrCl <10: Do not exceed 2 g/day. Not removed by haemodialysis or peritoneal dialysis; no extra dose after dialysis. [Label · UK SmPC]
- *hepatic*: No adjustment in mild–moderate impairment; no data in severe impairment. Monitor closely if severe renal and hepatic impairment coexist. [Label · UK SmPC]
- *elderly*: No adjustment if renal and hepatic function are satisfactory; encephalopathy risk higher with severe renal impairment. [Label · UK SmPC]
- *pregnancy*: Crosses the placenta; use only if benefit outweighs risk, especially in the first trimester. Low levels in breast milk; watch the infant for diarrhoea or thrush. [Label · UK SmPC]
- *administration*: IV: infuse over ≥30 min (preferred) or slow injection over 5 min; neonates over 60 min; children ≥50 mg/kg by infusion; doses >2 g IV only. [Label · UK SmPC]
- *administration*: IM: reconstitute with 1% lidocaine, deep IM into a large muscle, max 1 g per site; never give the lidocaine solution IV. [Label · UK SmPC]
- *administration*: IV dilution volume: 5 mL/kg for children <20 kg; 100 mL bag for children ≥20 kg and adults. Use immediately after reconstitution. [MSF 2023]
- *forms_ph*: Powder for injection: 250 mg and 500 mg vial + 2 mL 1% lidocaine (IM); 1 g vial + 3.5 mL 1% lidocaine (IM); 250 mg vial + 5 mL diluent (IV); 1 g vial + 10 mL diluent (IV). [PNF]
- *monitor*: Check complete blood count during prolonged treatment; stop if haemolytic anaemia is suspected. [Label · UK SmPC]
- *monitor*: Watch for right upper quadrant pain (biliary sludge/pancreatitis), especially at ≥1 g/day or with TPN. [Label · UK SmPC]
- *monitor*: Check INR in patients on oral anticoagulants; test for C. difficile if diarrhoea develops. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=ceftriaxone#emc-1362): Ceftriaxone 2 g Powder for Solution for Injection or Infusion. Summary of Product Characteristics. Wockhardt UK Ltd; updated January 2025. electronic medicines compendium (emc).
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/ceftriaxone-injectable-16682532.html): Médecins Sans Frontières. Essential drugs – Ceftriaxone injectable. MSF Medical Guidelines; updated September 2023.
- [PhilHealth Circular 2016-0003](https://www.philhealth.gov.ph/circulars/2016/circ2016-003.pdf): Philippine Health Insurance Corporation. Circular No. 2016-0003: Diagnosis, empiric management and prevention of community-acquired pneumonia in immunocompetent adults (based on the 2016 Philippine CPG on CAP). PhilHealth; 2016.
- [PhilHealth / DOH (PNF-EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=ceftriaxone#emc-1362): Ceftriaxone 2 g Powder for Solution for Injection or Infusion. Summary of Product Characteristics. Wockhardt UK Ltd; January 2025.
- Dosing source `MSF 2023`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/ceftriaxone-injectable-16682532.html): Médecins Sans Frontières. Essential drugs – Ceftriaxone injectable. Updated September 2023.
- Dosing source `PhilHealth CAP 2016`: [PhilHealth Circular 2016-0003](https://www.philhealth.gov.ph/circulars/2016/circ2016-003.pdf): PhilHealth Circular 2016-0003: CAP in immunocompetent adults (2016 Philippine CPG). PhilHealth; 2016.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Ceftriaxone (as disodium/sodium salt) Inj.: 250 mg and 500 mg vial + 2 mL 1% lidocaine (IM); 250 mg vial + 5 mL diluent (IV); 1 g vial + 3.5 mL 1% lidocaine (IM); 1 g vial + 10 mL diluent (IV); no restriction.
- https://products.mhra.gov.uk/search/?search=ceftriaxone#emc-1362: Ceftriaxone 2 g SmPC (Wockhardt UK, 30 Jan 2025): adult/≥50 kg dosing by indication (1–2 g CAP/AECOPD/IAI/cUTI; 2 g HAP/skin/bone; 2–4 g neutropenic fever/endocarditis/meningitis; AOM 1–2 g IM; prophylaxis 2 g; gonorrhoea 500 mg IM; syphilis 500 mg–1 g 10–14 d, 2 g neurosyphilis; Lyme 2 g 14–21 d); paediatric 15 d–12 y mg/kg with 4 g max; neonates 20–50 mg/kg, 50 mg/kg meningitis/endocarditis, max 50 mg/kg; contraindicated premature <41 wk PMA; duration 48–72 h afebrile; CrCl <10 max 2 g/day, not dialysed; hepatic mild–moderate no change; IV ≥30 min or 5 min, neonates 60 min; IM lidocaine max 1 g/site; contraindications incl. severe beta-lactam allergy, neonates with hyperbilirubinaemia/hypoalbuminaemia/acidosis; interactions chloramphenicol, incompatible vancomycin/fluconazole/amsacrine, lab interference; ADRs eosinophilia, leucopenia, thrombocytopenia, LFTs, rash, encephalopathy, convulsion, SJS/TEN/DRESS/AGEP, renal precipitation, kernicterus, Jarisch-Herxheimer; CBC monitoring; pregnancy/breastfeeding.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/ceftriaxone-injectable-16682532.html: MSF ceftriaxone injectable (Sept 2023): indications incl. typhoid, shigellosis, leptospirosis, tick-borne relapsing fever, neurosyphilis, chancroid, gonococcal conjunctivitis; child ≥1 mo 50–100 mg/kg max 4 g OD; adult 1–2 g OD, meningitis/typhoid up to 2 g BD or 4 g OD; gonorrhoea child <45 kg 125 mg IM, adult 500 mg IM (with chlamydia treatment); chancroid 250 mg IM; gonococcal conjunctivitis neonate 50 mg/kg max 125 mg, adult 1 g IM; dilution 5 mL/kg <20 kg, 100 mL ≥20 kg; severe renal impairment max 2 g/day.
- https://www.philhealth.gov.ph/circulars/2016/circ2016-003.pdf: PhilHealth circular (2016 PSMID CAP guideline, immunocompetent adults): Table 1 lists ceftriaxone 2 g OD IV for moderate-risk CAP (with extended macrolide or oral respiratory fluoroquinolone) and for high-risk CAP without Pseudomonas risk. PDF text partly garbled.

---

## Cetirizine  (`med_cetirizine`)

**Description (kept)**

Cetirizine, derived from hydroxyzine, is a fast-acting, highly selective peripheral histamine H1-receptor antagonist. It crosses the blood-brain barrier only minimally, so it causes less sedation than first-generation antihistamines, and it also reduces neutrophil and eosinophil infiltration. It is used for seasonal and perennial allergic rhinitis and chronic urticaria.

**Description (added)**

In the Philippines it is listed in the PNF as a 10 mg tablet and as several liquid forms (syrup, oral drops and solution) for children. UK labeling doses children aged 2–12 years twice daily, and bases renal dose reduction on eGFR, with use contraindicated below 15 mL/min.

**Side effects**: 5 kept, 10 added

- NEW: Diarrhoea, rhinitis and fatigue in children
- NEW: Agitation, paraesthesia, pruritus, rash, asthenia (uncommon)
- NEW: Aggression, confusion, depression, hallucinations, insomnia (rare)
- NEW: Convulsions and tachycardia (rare)
- NEW: Abnormal liver function tests (rare); hepatitis
- NEW: Urinary retention
- NEW: Weight increase and increased appetite
- NEW: Angioedema, fixed drug eruption, AGEP (very rare to not known)
- NEW: Tics, dystonia, oculogyric crisis, blurred vision (very rare)
- NEW: Pruritus and/or urticaria after stopping treatment

**Precautions**: 4 kept, 2 added

- NEW: Hypersensitivity to any piperazine derivative
- NEW: End-stage renal disease (eGFR <15 mL/min)

**Interactions**: 4 kept, 2 added

- NEW: Pseudoephedrine and theophylline (400 mg/day): no clinically significant interaction found.
- NEW: Food: slows the rate but not the extent of absorption.

**Disease links added**

- `chronic_kidney_disease`: **caution**: Reduce dose by eGFR; contraindicated below 15 mL/min (UK SmPC).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Allergic rhinitis, chronic urticaria (Also adolescents >12 y) | PO | 10 mg | Once a day | — | — | Label · UK SmPC |
| child | Allergic rhinitis, urticaria (6–12 y) (½ tablet or 5 mL of 1 mg/mL solution) | PO | 5 mg | 2× a day | — | — | Label · UK SmPC |
| child | Allergic rhinitis, urticaria (2–6 y) (2.5 mL of 1 mg/mL solution; tablets not suitable <6 y) | PO | 2.5 mg | 2× a day | — | — | Label · UK SmPC sol |

- *renal* eGFR ≥60: 10 mg once a day (no change). [Label · UK SmPC]
- *renal* eGFR 30–59: 5 mg once a day. [Label · UK SmPC]
- *renal* eGFR 15–29: 5 mg once every 2 days. [Label · UK SmPC]
- *renal* eGFR <15: Contraindicated. [Label · UK SmPC]
- *hepatic*: No adjustment for hepatic impairment alone; adjust if renal impairment is also present. [Label · UK SmPC]
- *elderly*: No dose reduction if renal function is normal. [Label · UK SmPC]
- *pregnancy*: Prospective data show no excess maternal or fetal toxicity, but prescribe with caution. Passes into breast milk (25–90% of plasma levels); use with caution. [Label · UK SmPC]
- *administration*: Stop at least 3 days before allergy skin testing (antihistamines suppress results). [Label · UK SmPC]
- *forms_ph*: Tablet 10 mg; syrup (oral drops) 2.5 mg/mL, 10 mL; drops 10 mg/mL, 10 mL; solution 1 mg/mL, 30 mL and 60 mL; syrup 5 mg/5 mL, 30 mL. [PNF]
- *monitor*: Ask about urinary retention in men with prostatic hyperplasia or spinal cord lesions; use caution in epilepsy. [Label · UK SmPC]
- *monitor*: Advise against driving if drowsy; warn that itching or hives may flare on stopping. [Label · UK SmPC]
- *monitor*: Overdose (≥5× daily dose): sedation, confusion, mydriasis, tachycardia, urinary retention; supportive care only, not removed by haemodialysis. [Label · UK SmPC sol]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=cetirizine#emc-12956): Cetirizine hydrochloride 10 mg film-coated tablets. Summary of Product Characteristics. Milpharm Ltd (Aurobindo); updated February 2024. electronic medicines compendium (emc).
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=cetirizine#emc-6752): Zirtek Allergy Solution 1 mg/ml oral solution. Summary of Product Characteristics. UCB Pharma Ltd; updated October 2023. electronic medicines compendium (emc).
- [PhilHealth / DOH (PNF-EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=cetirizine#emc-12956): Cetirizine hydrochloride 10 mg film-coated tablets. Summary of Product Characteristics. Milpharm Ltd; February 2024.
- Dosing source `Label · UK SmPC sol`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=cetirizine#emc-6752): Zirtek Allergy Solution 1 mg/ml oral solution. Summary of Product Characteristics. UCB Pharma Ltd; October 2023.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Cetirizine (as dihydrochloride) Oral: 10 mg tablet; 2.5 mg/mL syrup (oral drops) 10 mL; 10 mg/mL drops 10 mL; 1 mg/mL solution 30 and 60 mL; 5 mg/5 mL syrup 30 mL; no restriction.
- https://products.mhra.gov.uk/search/?search=cetirizine#emc-12956: Cetirizine 10 mg tablets SmPC (Milpharm/Aurobindo, Feb 2024): adults/adolescents >12 y 10 mg OD; 6–12 y 5 mg BD; not for <6 y; elderly no reduction with normal renal function; hepatic alone no adjustment; eGFR table (≥60 10 mg, 30–<60 5 mg OD, 15–<30 5 mg every 2 days, <15 contraindicated); hypersensitivity to piperazine derivatives; urinary retention, epilepsy cautions; 3-day washout before skin tests; pruritus/urticaria on discontinuation; no interaction with pseudoephedrine/theophylline; food slows rate; paediatric ADRs diarrhoea, rhinitis, fatigue; rare LFT abnormalities, convulsions; hepatitis; pregnancy caution; breast milk 25–90%; driving.
- https://products.mhra.gov.uk/search/?search=cetirizine#emc-6752: Zirtek Allergy Solution 1 mg/ml SmPC (UCB, Oct 2023): 2–6 y 2.5 mg BD, 6–12 y 5 mg BD, adults 10 mg OD; post-marketing ADRs (aggression, confusion, depression, hallucinations, insomnia, convulsions, tachycardia, weight increase, tics, dystonia, oculogyric crisis, blurred vision, angioedema, fixed drug eruption, AGEP, urinary retention, increased appetite, agitation, paraesthesia); overdose symptoms; haemodialysis ineffective.

---

## Ciprofloxacin  (`med_ciprofloxacin`)

**Description (kept)**

Ciprofloxacin is a bactericidal fluoroquinolone that inhibits bacterial DNA gyrase and topoisomerase IV, blocking DNA replication. It is especially active against Gram-negative organisms including Pseudomonas aeruginosa, but because of serious class toxicities it is reserved for infections where benefits outweigh risks.

**Description (added)**

Oral bioavailability is about 70–80%, so 500 mg orally every 12 hours gives roughly the same exposure (AUC) as 400 mg IV every 12 hours; this makes early IV-to-oral switching possible. The half-life is about 4–7 hours, rising to about 12 hours in severe renal impairment, and the drug is cleared by both the kidneys and the gut. In the Philippines it is on the PNF Essential Medicines List as tablets and IV infusion. National surveillance (ARSP 2014–2018) found 8.7% of invasive non-typhoidal Salmonella isolates resistant to ciprofloxacin, and MSF notes that fluoroquinolone resistance in typhoid is endemic in Asia.

**Uses**: 6 kept, 8 added

- NEW: Chronic suppurative otitis media and malignant external otitis
- NEW: Gonococcal urethritis and cervicitis (only if the strain is known to be susceptible)
- NEW: Epididymo-orchitis and pelvic inflammatory disease (with a second agent)
- NEW: Gram-negative intra-abdominal infections and skin/soft tissue infections
- NEW: Suspected bacterial infection in neutropenic fever (with other antibacterials)
- NEW: Prophylaxis of invasive meningococcal infection (single dose)
- NEW: Shigellosis and cholera diarrhoea
- NEW: Children: Pseudomonas lung infection in cystic fibrosis; complicated UTI and pyelonephritis

**Side effects**: 9 kept, 7 added

- NEW: Headache, dizziness, sleep disorders and taste disturbance (uncommon)
- NEW: Arthralgia and musculoskeletal pain; eosinophilia
- NEW: Tinnitus, hearing loss and vision disorders (rare)
- NEW: Crystalluria, interstitial nephritis and renal failure (rare)
- NEW: Haemolytic anaemia in G6PD deficiency
- NEW: Stevens–Johnson syndrome, toxic epidermal necrolysis and pancreatitis (very rare)
- NEW: Fungal superinfection

**Precautions**: 2 kept, 5 added

- NEW: Previous serious adverse reaction to any quinolone: avoid (precaution)
- NEW: Children and adolescents: joint (cartilage) damage seen in young animals; use only after careful benefit/risk review (precaution)
- NEW: G6PD deficiency: risk of haemolysis; avoid unless benefit outweighs risk (precaution)
- NEW: Pregnancy: preferably avoid; breastfeeding: not to be used per UK SmPC (precaution)
- NEW: Epilepsy, older age, hypertension or heart disease: use with caution (precaution)

**Interactions**: 6 kept, 7 added

- NEW: Dairy products and mineral-fortified drinks taken alone: reduced absorption; avoid (calcium in a normal meal has little effect).
- NEW: Probenecid: raises ciprofloxacin levels.
- NEW: Phenytoin: levels may rise or fall; monitor phenytoin.
- NEW: Ciclosporin: transient rise in serum creatinine; check creatinine about twice a week.
- NEW: Clozapine, ropinirole, caffeine and pentoxifylline: raised levels (CYP1A2 inhibition); monitor for side effects.
- NEW: Sildenafil: exposure roughly doubled; use with caution. Zolpidem: not recommended.
- NEW: QT-prolonging drugs (class IA/III antiarrhythmics, tricyclics, macrolides, antipsychotics): use with caution.

**Disease links added**

- `chronic_kidney_disease`: **caution**: Dose reduction needed when CrCl is 60 mL/min or below; half-life up to about 12 h in severe renal impairment; keep well hydrated (crystalluria)
- `type2_diabetes`: **caution**: Hypo- and hyperglycaemia reported; MSF advises monitoring with glibenclamide (hypoglycaemia risk)
- `hypertension`: **caution**: MSF lists hypertension and heart disorders as a precaution (QT risk)

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Uncomplicated cystitis (Pre-menopausal women: a single 500 mg dose may be used) | PO | 250–500 mg | 2× a day | 3 days | — | Label · UK SmPC |
| adult | Complicated cystitis, uncomplicated pyelonephritis | PO | 500 mg | 2× a day | 7 days | — | Label · UK SmPC |
| adult | Complicated pyelonephritis (May exceed 21 days (e.g. abscesses)) | PO | 500–750 mg | 2× a day | ≥10 days | 750 mg/dose | Label · UK SmPC |
| adult | Prostatitis | PO | 500–750 mg | 2× a day | 2–4 weeks (acute); 4–6 weeks (chronic) | 750 mg/dose | Label · UK SmPC |
| adult | Lower respiratory tract infection (Not for pneumococcal infection) | PO | 500–750 mg | 2× a day | 7–14 days | 750 mg/dose | Label · UK SmPC |
| adult | Typhoid fever (Check local resistance) | PO | 500 mg | 2× a day | 7 days | — | Label · UK SmPC |
| adult | Cholera | PO | 500 mg | 2× a day | 3 days | — | Label · UK SmPC |
| adult | Shigellosis (non-S. dysenteriae type 1) (S. dysenteriae type 1: 5 days; MSF uses 3 days) | PO | 500 mg | 2× a day | 1 day | — | Label · UK SmPC |
| adult | Gonococcal urethritis/cervicitis (Only if strain susceptible) | PO | 500 mg | Single dose | 1 day | — | Label · UK SmPC |
| adult | Meningococcal prophylaxis | PO | 500 mg | Single dose | 1 day | — | Label · UK SmPC |
| adult | Bone and joint infection (Combine per microbiology) | PO | 500–750 mg | 2× a day | Up to 3 months | 750 mg/dose | Label · UK SmPC |
| adult | Inhalational anthrax (Start as soon as possible after exposure) | PO | 500 mg | 2× a day | 60 days | — | Label · UK SmPC |
| adult | Severe infections (skin, bone, LRTI, UTI) (UTI: 200–400 mg; switch to PO when able) | IV | 400 mg | Every 8–12 h | 7–14 days | — | Label · US IV |
| adult | Nosocomial pneumonia | IV | 400 mg | Every 8 h | 10–14 days | — | Label · US IV |
| adult | Complicated intra-abdominal infection (With metronidazole) | IV | 400 mg | Every 12 h | 7–14 days | — | Label · US IV |
| adult | Febrile neutropenia (With piperacillin) | IV | 400 mg | Every 8 h | 7–14 days | — | Label · US IV |
| child | Shigellosis (≥1 month) | PO | 15 mg/kg | 2× a day | 3 days | 500 mg/dose | MSF 2023 |
| child | Complicated UTI, pyelonephritis | PO | 10–20 mg/kg | 2× a day | 10–21 days | 750 mg/dose | Label · UK SmPC |
| child | Cystic fibrosis (Pseudomonas) | PO | 20 mg/kg | 2× a day | 10–14 days | 750 mg/dose | Label · UK SmPC |
| child | Inhalational anthrax | PO | 10–15 mg/kg | 2× a day | 60 days | 500 mg/dose | Label · UK SmPC |
| child | Complicated UTI, pyelonephritis (1–17 y) | IV | 6–10 mg/kg | Every 8 h | 10–21 days | 400 mg/dose | Label · US IV |
| child | Inhalational anthrax | IV | 10 mg/kg | Every 12 h | 60 days | 400 mg/dose | Label · US IV |

- *renal* CrCl >60: Usual dose. [Label · UK SmPC]
- *renal* CrCl 30–60: 250–500 mg PO every 12 h. [Label · UK SmPC]
- *renal* CrCl ≤30: 250–500 mg PO every 24 h (haemodialysis: give after dialysis). [Label · UK SmPC]
- *renal* CrCl 5–29: IV: 200–400 mg every 18–24 h. [Label · US IV]
- *hepatic*: No dose adjustment needed; stop if signs of liver disease appear (hepatic necrosis reported). [Label · UK SmPC]
- *elderly*: Choose dose by infection severity and creatinine clearance. [Label · UK SmPC]
- *pregnancy*: Preferably avoid in pregnancy (possible cartilage effects). Excreted in breast milk: UK SmPC says not to use while breastfeeding; MSF lists no contraindication. [Label · UK SmPC]
- *administration*: Swallow tablets whole with fluid, with or without meals; avoid taking with dairy or mineral-fortified juice alone. [Label · UK SmPC]
- *administration*: IV: ready to use; infuse over 60 minutes. Switch to oral as soon as possible. [Label · US IV]
- *administration*: Keep fluid intake high to reduce crystalluria risk. [MSF 2023]
- *forms_ph*: Tablet 250 mg, 500 mg (as hydrochloride); IV infusion 2 mg/mL, 100 mL vial (as lactate); 400 mg/200 mL IV infusion. [PNF]
- *monitor*: Ask about tendon pain, numbness/tingling and mood changes at each visit; stop at once if they appear. [Label · UK SmPC]
- *monitor*: Check INR often with warfarin, and blood glucose in diabetics. [Label · UK SmPC]
- *monitor*: Check serum creatinine about twice weekly if on ciclosporin; theophylline/phenytoin levels if co-prescribed. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=ciprofloxacin#emc-4346): Ciprofloxacin 500 mg film-coated tablets – Summary of Product Characteristics. Sun Pharma UK Limited (PL 14894/0023). Electronic Medicines Compendium (emc), medicines.org.uk; updated May 2026.
- [Pfizer labeling (US)](https://labeling.pfizer.com/ShowLabeling.aspx?id=18958): Ciprofloxacin in Dextrose (Ciprofloxacin Injection, USP, in 5% Dextrose Injection). Prescribing information. Hospira, Inc.; revised 11/2022.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/ciprofloxacin-oral-16683360.html): Médecins Sans Frontières. Essential drugs – Ciprofloxacin oral. Last updated September 2023.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- [Western Pacific Surveillance and Response](https://ojs.wpro.who.int/ojs/index.php/wpsar/article/view/1030): Sia SB, Ablola FB, Lagrada ML, et al. Epidemiology and antimicrobial resistance profile of invasive non-typhoidal Salmonella from the Philippines Antimicrobial Resistance Surveillance Program, 2014–2018. Western Pac Surveill Response J. 2023;14(3). doi:10.5365/wpsar.2023.14.3.1030
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=ciprofloxacin#emc-4346): Ciprofloxacin 500 mg film-coated tablets. Summary of Product Characteristics. Sun Pharma UK Ltd; 2026.
- Dosing source `Label · US IV`: [Pfizer labeling (US)](https://labeling.pfizer.com/ShowLabeling.aspx?id=18958): Ciprofloxacin in Dextrose injection. Prescribing information. Hospira, Inc.; 11/2022.
- Dosing source `MSF 2023`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/ciprofloxacin-oral-16683360.html): Médecins Sans Frontières. Essential drugs – Ciprofloxacin oral. Updated September 2023.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=ciprofloxacin#emc-4346: 4.2 adult and paediatric dosing tables, renal table (CrCl >60/30–60/≤30/HD/PD), hepatic no adjustment, elderly, administration; 4.3; 4.4 (prior quinolone reaction, children arthropathy, G6PD, hydration/crystalluria, liver); 4.5 (dairy, probenecid, phenytoin, ciclosporin creatinine 2x/week, ropinirole, clozapine, sildenafil ~2x, zolpidem, caffeine/pentoxifylline, QT drugs); 4.6 pregnancy avoid, breastfeeding not to be used; 4.8 frequencies; 5.2 bioavailability 70–80%, 500 mg PO q12h ≈ 400 mg IV q12h AUC, t½ 4–7 h, up to 12 h severe renal
- https://labeling.pfizer.com/ShowLabeling.aspx?id=18958: Hospira Ciprofloxacin in Dextrose label rev 11/2022: adult IV table (400 mg q8–12h; nosocomial pneumonia q8h 10–14 d; intra-abdominal q12h with metronidazole; febrile neutropenia q8h with piperacillin; UTI 200–400 mg); paediatric cUTI 6–10 mg/kg q8h max 400 mg, anthrax 10 mg/kg q12h; renal CrCl 5–29 200–400 mg q18–24h; infuse over 60 min
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/ciprofloxacin-oral-16683360.html: Shigellosis child ≥1 mo 15 mg/kg BID max 500 mg/dose, 3 days; precautions epilepsy, elderly, hypertension/heart disorders; monitor with glibenclamide; high fluid intake; breastfeeding no contraindication; fluoroquinolone resistance endemic in Asia (typhoid); updated Sept 2023
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Ciprofloxacin: 250 mg and 500 mg tablet (as hydrochloride); 2 mg/mL 100 mL vial IV infusion (as lactate); 400 mg/200 mL IV infusion; no restriction note
- https://ojs.wpro.who.int/ojs/index.php/wpsar/article/view/1030: WPSAR 2023;14(3), ARSP 2014–2018: 8.7% of invasive non-typhoidal Salmonella isolates resistant to ciprofloxacin; authors and DOI
- https://assets.hpra.ie/products/Human/20262/LicenseSPC_PA0711-168-001_14022014115044.pdf: Irish SmPC for IV ciprofloxacin (2014) opened; not used (older; US IV label used instead)

---

## Clarithromycin  (`med_clarithromycin`)

**Description (kept)**

Clarithromycin binds the 50S ribosomal subunit and inhibits bacterial protein synthesis. It covers respiratory and atypical pathogens and is a key component of H. pylori triple therapy, but it is a strong CYP3A4 inhibitor with many clinically important drug interactions.

**Description (added)**

Clarithromycin is converted on first pass to 14-hydroxyclarithromycin, an active metabolite that is about twice as active as the parent drug against Haemophilus influenzae. Its kinetics are non-linear: the half-life is 2–4 hours at 250 mg twice daily and about 5 hours at 500 mg twice daily, and steady state is reached within 2 days. In the Philippines it is on the PNF Essential Medicines List as 250 mg and 500 mg tablets and as a 125 mg/5 mL or 250 mg/5 mL oral suspension.

**Uses**: 6 kept, 3 added

- NEW: Pertussis: treatment and post-exposure prophylaxis (age 1 month and over)
- NEW: Prophylaxis of disseminated Mycobacterium avium complex infection
- NEW: Respiratory and skin infections in children 6 months to 12 years (oral suspension)

**Side effects**: 7 kept, 7 added

- NEW: Insomnia, headache and excessive sweating (common)
- NEW: Abnormal liver function tests and rash (common)
- NEW: Dizziness, vertigo, tinnitus and hearing impairment (uncommon)
- NEW: Leukopenia, neutropenia and candidiasis (uncommon)
- NEW: Severe skin reactions: SJS, TEN, DRESS, AGEP (post-marketing)
- NEW: Pancreatitis, hallucinations, psychotic disorder and convulsions (post-marketing)
- NEW: Renal failure and interstitial nephritis; rhabdomyolysis (post-marketing)

**Precautions**: 6 kept, 8 added

- NEW: Oral midazolam
- NEW: Astemizole, terfenadine or domperidone
- NEW: Ticagrelor, ivabradine or ranolazine
- NEW: Colchicine (any patient, per UK SmPC)
- NEW: Low potassium or magnesium (electrolyte disturbance)
- NEW: Severe hepatic failure together with renal impairment
- NEW: Pregnancy: safety not established; possible higher miscarriage risk; use only if benefit outweighs risk (precaution)
- NEW: Infants under 1 month: not recommended for pertussis; azithromycin preferred (precaution)

**Interactions**: 6 kept, 10 added

- NEW: Rifampicin, rifabutin, rifapentine, efavirenz, nevirapine: lower clarithromycin levels; rifabutin levels rise (uveitis risk).
- NEW: Ritonavir or atazanavir: raise clarithromycin levels; cut dose by 50% at CrCl 30–60 and 75% at CrCl <30; max 1 g/day.
- NEW: Digoxin: raised levels with toxicity and arrhythmias; monitor digoxin levels.
- NEW: IV midazolam, triazolam, alprazolam: increased sedation; monitor closely.
- NEW: Direct oral anticoagulants (dabigatran, edoxaban, rivaroxaban, apixaban): higher bleeding risk; use with caution.
- NEW: Zidovudine: reduced absorption; separate doses by 4 hours.
- NEW: Sildenafil, tadalafil, vardenafil: consider dose reduction.
- NEW: Omeprazole: omeprazole AUC up 89%.
- NEW: Hydroxychloroquine or chloroquine: additive QT risk; weigh risk and benefit.
- NEW: Phenytoin and valproate: monitor levels.

**Disease links added**

- `chronic_kidney_disease`: **caution**: CrCl <30 mL/min: halve the dose and do not treat beyond 14 days; contraindicated with severe hepatic failure plus renal impairment
- `type2_diabetes`: **caution**: Significant hypoglycaemia reported with oral hypoglycaemics or insulin; monitor glucose
- `hiv_infection`: **caution**: Used for MAC prophylaxis/treatment, but interacts with ritonavir, atazanavir, efavirenz, nevirapine and zidovudine (dose changes or spacing needed)

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Respiratory and skin infections (and >12 y) (Increase to 500 mg 2× a day if severe) | PO | 250 mg | 2× a day | 6–14 days | 500 mg 2× a day | Label · UK SmPC |
| adult | Community-acquired pneumonia (H. influenzae: 500 mg for 7 days) | PO | 250 mg | Every 12 h | 7–14 days | — | Label · FDA |
| adult | Acute maxillary sinusitis | PO | 500 mg | Every 12 h | 14 days | — | Label · FDA |
| adult | H. pylori (triple therapy) (With amoxicillin 1 g and a PPI, all 2× a day) | PO | 500 mg | 2× a day | 10–14 days | — | Label · FDA |
| adult | H. pylori (UK alternative) (With a PPI plus metronidazole 400 mg 2× a day) | PO | 500 mg | 2× a day | 6–14 days | — | Label · UK SmPC |
| adult | Disseminated MAC (treatment/prophylaxis) (With other antimycobacterials (e.g. ethambutol)) | PO | 500 mg | Every 12 h | Ongoing while response lasts | — | Label · FDA |
| adult | Pertussis (treatment or PEP) | PO | 500 mg | 2× a day | 7 days | 1 g/day | CDC 2005 |
| child | Respiratory and skin infections (6 mo–12 y) (S. pyogenes: at least 10 days) | PO | 7.5 mg/kg | 2× a day | 5–10 days | — | Label · UK SmPC susp |
| child | Other infections | PO | 15 mg/kg/day ÷ 2 | Every 12 h | 10 days | Adult dose | Label · FDA |
| child | MAC (treatment/prophylaxis) | PO | 7.5 mg/kg | Every 12 h | Ongoing | 500 mg/dose | Label · FDA |
| child | Pertussis (≥1 month) (Not recommended <1 month) | PO | 15 mg/kg/day ÷ 2 | 2× a day | 7 days | 1 g/day | CDC 2005 |

- *renal* CrCl <30: Halve the dose: 250 mg once a day (250 mg 2× a day in severe infection); children 7.5 mg/kg once a day; do not continue beyond 14 days. [Label · UK SmPC]
- *renal* CrCl 30–60: With ritonavir or atazanavir: reduce dose by 50%. [Label · FDA]
- *renal* CrCl <30: With ritonavir or atazanavir: reduce dose by 75%. [Label · FDA]
- *hepatic*: No set dose change; use with caution. Contraindicated in severe hepatic failure with renal impairment. [Label · UK SmPC]
- *elderly*: Same dose as adults; watch for colchicine toxicity in elderly with renal insufficiency. [Label · UK SmPC]
- *pregnancy*: Safety not established; some studies show more first- and second-trimester miscarriage. Small amounts pass into breast milk (about 1.7% of the maternal weight-adjusted dose). [Label · UK SmPC]
- *administration*: Tablets can be taken with or without food. [Label · UK SmPC]
- *administration*: Suspension: shake well before each dose; food or a drink right after the dose masks the bitter aftertaste. [Label · UK SmPC susp]
- *forms_ph*: Tablet 250 mg, 500 mg (base); granules/powder for suspension 125 mg/5 mL and 250 mg/5 mL, 50 mL. [PNF]
- *monitor*: Check ECG, potassium and magnesium before use in patients at QT risk (heart disease, bradycardia, QT-prolonging drugs). [Label · UK SmPC]
- *monitor*: Check INR closely with warfarin; digoxin levels with digoxin; glucose in diabetics on insulin or oral agents. [Label · UK SmPC]
- *monitor*: Stop and check liver tests if jaundice, dark urine or abdominal pain appear; watch for diarrhoea up to 2 months after treatment (C. difficile). [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=clarithromycin#emc-7072): Clarithromycin 500 mg film-coated tablets – Summary of Product Characteristics. Milpharm Limited (PL 16363/0414). Electronic Medicines Compendium (emc), medicines.org.uk; revised July 2026.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=clarithromycin#emc-515): Clarithromycin 125 mg/5 ml suspension – Summary of Product Characteristics. Sandoz Ltd. Electronic Medicines Compendium (emc), medicines.org.uk; June 2021.
- [CDC (MMWR)](https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5414a1.htm): Centers for Disease Control and Prevention. Recommended antimicrobial agents for the treatment and postexposure prophylaxis of pertussis: 2005 CDC guidelines. MMWR Recomm Rep. 2005;54(RR-14).
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=clarithromycin#emc-7072): Clarithromycin 500 mg film-coated tablets. Summary of Product Characteristics. Milpharm Ltd; July 2026.
- Dosing source `Label · UK SmPC susp`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=clarithromycin#emc-515): Clarithromycin 125 mg/5 ml suspension. Summary of Product Characteristics. Sandoz Ltd; June 2021.
- Dosing source `Label · FDA`: [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=b98b02bb-2609-49a0-b29f-e5911aa0cbc1): Clarithromycin tablet. Prescribing information. Sandoz Inc.; revised 5/2023.
- Dosing source `CDC 2005`: [CDC (MMWR)](https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5414a1.htm): Recommended antimicrobial agents for the treatment and postexposure prophylaxis of pertussis: 2005 CDC guidelines. MMWR 2005;54(RR-14).
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=clarithromycin#emc-7072: Milpharm SmPC rev 07/2026: 4.2 adult 250 mg BID up to 500 mg BID 6–14 d, H. pylori regimens (incl. metronidazole 400 mg), renal CrCl <30 halve to 250 mg OD/BID max 14 d, hepatic caution, elderly as adults, with/without food; 4.3 full list (oral midazolam, astemizole/terfenadine/domperidone, ticagrelor/ivabradine/ranolazine, colchicine, hypoK/hypoMg, severe hepatic failure + renal impairment); 4.4; 4.5 (rifamycins/efavirenz/nevirapine, ritonavir/atazanavir renal reductions, digoxin, midazolam, DOACs, zidovudine 4 h, PDE5, omeprazole AUC +89%, HCQ/chloroquine, phenytoin/valproate); 4.6 miscarriage, 1.7% milk; 4.8; 5.1 14-OH 2x vs H. influenzae; 5.2 non-linear, steady state 2 days
- https://products.mhra.gov.uk/search/?search=clarithromycin#emc-515: Sandoz suspension SmPC: 7.5 mg/kg BID 6 mo–12 y, 5–10 days (≥10 d S. pyogenes), renal 7.5 mg/kg OD max 14 d; shake, bitter aftertaste; adult t½ 2–4 h (250 BID), ~5 h (500 BID)
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=b98b02bb-2609-49a0-b29f-e5911aa0cbc1: Sandoz clarithromycin label rev 5/2023: adult table (CAP 250 mg q12h 7–14 d, H. influenzae 500 mg 7 d; sinusitis 500 mg 14 d), H. pylori triple 10–14 d, MAC 500 mg q12h with ethambutol, paediatric 15 mg/kg/day ÷ q12h 10 d up to adult dose, MAC 7.5 mg/kg q12h max 500 mg; renal with atazanavir/ritonavir 50%/75%
- https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5414a1.htm: 2005 CDC pertussis guideline: clarithromycin 15 mg/kg/day ÷ 2 (max 1 g/day) 7 days for >1 month; adults 1 g/day ÷ 2 for 7 days; not recommended <1 month
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Clarithromycin: 250 mg and 500 mg base tablet; 125 mg/5 mL and 250 mg/5 mL granules/powder for suspension, 50 mL
- https://www.cdc.gov/pertussis/hcp/clinical-care/index.html: Clarithromycin listed among macrolides for pertussis treatment/PEP; no doses (not used)

---

## Clopidogrel  (`med_clopidogrel`)

**Description (kept)**

Clopidogrel is a prodrug activated mainly by CYP2C19 to a metabolite that irreversibly blocks the platelet P2Y12 ADP receptor, preventing downstream glycoprotein IIb/IIIa activation and platelet aggregation. It is used, often with aspirin, in acute coronary syndromes and for secondary prevention after MI, stroke or peripheral arterial disease.

**Description (added)**

Because the receptor block is irreversible, platelets stay affected for the rest of their lifespan (about 7–10 days); with 75 mg daily, inhibition starts on day 1 and reaches steady state between days 3 and 7, which is why a loading dose is used when a fast effect is needed. In the Philippines clopidogrel 75 mg tablets are on the PNF Essential Medicines List, and the DOST HTA Council used clopidogrel plus aspirin as the comparator when it did not recommend government financing of ticagrelor for ACS in 2025.

**Uses**: 4 kept, 3 added

- NEW: ACS patients undergoing PCI with stenting (with aspirin)
- NEW: Moderate- to high-risk TIA (ABCD2 ≥4) or minor ischaemic stroke (NIHSS ≤3), started within 24 h with aspirin
- NEW: Atrial fibrillation with a vascular risk factor when a vitamin K antagonist is unsuitable and bleeding risk is low (with aspirin)

**Side effects**: 4 kept, 6 added

- NEW: Haematoma, nosebleed, bruising and bleeding at puncture sites (common)
- NEW: Diarrhoea, abdominal pain and dyspepsia (common)
- NEW: Thrombocytopenia, leucopenia and eosinophilia (uncommon)
- NEW: Headache, paraesthesia and dizziness (uncommon)
- NEW: Gastric and duodenal ulcer, haematuria and eye bleeding (uncommon)
- NEW: Acquired haemophilia (consider if isolated aPTT prolongation)

**Precautions**: 2 kept, 6 added

- NEW: Severe hepatic impairment
- NEW: Past hypersensitivity to ticlopidine or prasugrel: check for cross-reactivity (precaution)
- NEW: Hereditary galactose intolerance, lactase deficiency or glucose-galactose malabsorption (tablets contain lactose) (precaution)
- NEW: Non-minor ischaemic stroke (NIHSS >4): dual antiplatelet therapy not recommended; start monotherapy only after the first 7 days (precaution)
- NEW: Children: not to be used (efficacy concerns) (precaution)
- NEW: Breastfeeding: stop breastfeeding during treatment (precaution)

**Interactions**: 5 kept, 7 added

- NEW: Other CYP2C19 inhibitors (fluvoxamine, fluoxetine, moclobemide, voriconazole, fluconazole, ticlopidine, carbamazepine, efavirenz): reduce active metabolite; avoid.
- NEW: Rifampicin (strong CYP2C19 inducer): avoid.
- NEW: Pantoprazole: can be used if a PPI is needed.
- NEW: Rosuvastatin: exposure about doubled after a 300 mg clopidogrel dose.
- NEW: Paclitaxel (CYP2C8 substrate): use with caution.
- NEW: Ritonavir- or cobicistat-boosted HIV therapy: concomitant use discouraged.
- NEW: Heparin, GP IIb/IIIa inhibitors, thrombolytics and pentoxifylline: added bleeding risk; oral anticoagulants not recommended together.

**Disease links added**

- `chronic_kidney_disease`: **caution**: UK SmPC: limited experience in renal impairment; use with caution

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | NSTE-ACS (With aspirin 75–100 mg; 600 mg load only if <75 y) | PO | 300 or 600 mg load, then 75 mg | Once a day | Up to 12 months | — | Label · UK SmPC |
| adult | STEMI, medically treated / fibrinolysis (With aspirin; >75 y: no loading dose) | PO | 300 mg load, then 75 mg | Once a day | At least 4 weeks | — | Label · UK SmPC |
| adult | Primary PCI (300 mg load if PCI within 24 h of fibrinolysis; caution ≥75 y) | PO | 600 mg load, then 75 mg | Once a day | Up to 12 months | — | Label · UK SmPC |
| adult | TIA (ABCD2 ≥4) or minor stroke (NIHSS ≤3) (Start within 24 h with aspirin 75–100 mg; then single antiplatelet) | PO | 300 mg load, then 75 mg | Once a day | 21 days | — | Label · UK SmPC |
| adult | Recent MI, ischaemic stroke or PAD (Stroke: 7 days to <6 months after event) | PO | 75 mg | Once a day | — | — | Label · UK SmPC |
| adult | Atrial fibrillation (VKA unsuitable) (With aspirin 75–100 mg) | PO | 75 mg | Once a day | — | — | Label · UK SmPC |

- *renal*: Limited experience; use with caution. [Label · UK SmPC]
- *hepatic*: Contraindicated in severe hepatic impairment; otherwise limited experience, use with caution. [Label · UK SmPC]
- *elderly*: NSTE-ACS: 600 mg load only under 75 y. STEMI medically treated over 75 y: no loading dose. Primary PCI ≥75 y: 600 mg load with caution. [Label · UK SmPC]
- *pregnancy*: Preferably avoid (no clinical data). Stop breastfeeding during treatment. [Label · UK SmPC]
- *administration*: Take with or without food. Missed dose: take if <12 h late; if >12 h, skip it and do not double. [Label · UK SmPC]
- *administration*: Elective surgery: UK SmPC advises stopping 7 days before if an antiplatelet effect is not wanted. [Label · UK SmPC]
- *forms_ph*: Tablet 75 mg. [PNF]
- *monitor*: Watch for bleeding (black stools, bruising, nosebleeds, blood in urine), especially with aspirin, NSAIDs, SSRIs or anticoagulants. [Label · UK SmPC]
- *monitor*: Suspected TTP (very rare, potentially fatal) needs urgent assessment and prompt treatment; check a platelet count. [Label · UK SmPC]
- *monitor*: Unexplained isolated aPTT prolongation: test for acquired haemophilia. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=clopidogrel#emc-15874): Clopidogrel 75 mg film-coated tablets – Summary of Product Characteristics. Dr. Reddy's Laboratories (UK) Ltd (PL 08553/0766). Electronic Medicines Compendium (emc), medicines.org.uk; updated August 2024.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- [DOST HTA Philippines](https://hta.dost.gov.ph/wp-content/uploads/2025/05/HTA-Council-Preliminary-Recommendation-on-Ticagrelor-90mg-film-coated-tablet-for-ACS-02-May-2025-1-2.pdf): Health Technology Assessment Council. Call for Stakeholder Comments on the Preliminary Recommendation on Ticagrelor [90 mg film-coated tablet] as an Add-on to Aspirin for Adults with Acute Coronary Syndrome. Department of Science and Technology, HTA Philippines; 02 May 2025.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=clopidogrel#emc-15874): Clopidogrel 75 mg film-coated tablets. Summary of Product Characteristics. Dr. Reddy's Laboratories (UK) Ltd; 2024.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=clopidogrel#emc-15874: Dr. Reddy's SmPC (updated 12-Aug-2024): 4.1 incl. TIA/minor IS and AF; 4.2 NSTE-ACS 300/600 mg load up to 12 months, aspirin ≤100 mg, STEMI 300 mg load ≥4 weeks, primary PCI 600 mg (300 mg after fibrinolysis), TIA 21 days, AF, elderly loading rules, paediatrics not to be used, renal/hepatic limited experience caution, with/without food, missed dose 12 h; 4.3 severe hepatic impairment; 4.4 stop 7 days pre-surgery, NIHSS >4, acquired haemophilia/aPTT, TTP, thienopyridine cross-reactivity, lactose; 4.5 CYP2C19 inhibitors list, rifampicin, pantoprazole OK, rosuvastatin ~2x, paclitaxel/repaglinide, ritonavir/cobicistat, heparin/GP IIb/IIIa/thrombolytics/pentoxifylline; 4.6; 4.8 common/uncommon; 5.1 platelet lifespan 7–10 days, steady state day 3–7
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Clopidogrel: Oral 75 mg tablet; no restriction note
- https://hta.dost.gov.ph/wp-content/uploads/2025/05/HTA-Council-Preliminary-Recommendation-on-Ticagrelor-90mg-film-coated-tablet-for-ACS-02-May-2025-1-2.pdf: DOST HTA Council preliminary recommendation (02 May 2025): aspirin and clopidogrel already on PNF; clopidogrel + aspirin comparator; ticagrelor not recommended for government financing for ACS

---

## Co-amoxiclav (Amoxicillin + Clavulanic acid)  (`med_coamoxiclav`)

**Description (kept)**

Amoxicillin inhibits bacterial cell-wall synthesis by binding penicillin-binding proteins, while clavulanic acid inhibits many beta-lactamases, protecting amoxicillin from degradation and extending coverage to beta-lactamase-producing organisms (e.g., H. influenzae, M. catarrhalis, many anaerobes and some Enterobacterales). It is used for sinusitis, otitis media, lower respiratory, skin, bite-wound and urinary infections.

**Description (added)**

Both components are about 70% absorbed orally and have half-lives of about 1 hour, which is why it is given two or three times a day; amoxicillin does not reach adequate levels in the cerebrospinal fluid. MSF uses it as second-line treatment for otitis media and sinusitis when high-dose amoxicillin has failed, and the UK label advises switching to plain amoxicillin once an infection is shown to be amoxicillin-susceptible. In the Philippines it is on the PNF Essential Medicines List as tablets and oral suspensions.

**Uses**: 5 kept, 5 added

- NEW: Bone and joint infections, including osteomyelitis
- NEW: Severe dental abscess with spreading cellulitis
- NEW: Postpartum upper genital tract infection
- NEW: Oral step-down after IV treatment of severe infections (e.g., severe pneumonia)
- NEW: Acute uncomplicated cystitis in girls over 2 years (MSF)

**Side effects**: 6 kept, 9 added

- NEW: Mucocutaneous candidosis (common); dizziness, headache and indigestion (uncommon)
- NEW: Reversible leucopenia, neutropenia and thrombocytopenia (rare); agranulocytosis and haemolytic anaemia
- NEW: Drug-induced enterocolitis syndrome (DIES), mainly in children: protracted vomiting 1–4 h after a dose
- NEW: Haemophagocytic lymphohistiocytosis (HLH)
- NEW: Kounis syndrome (allergic acute coronary syndrome)
- NEW: Severe skin reactions: SJS, TEN, AGEP and DRESS
- NEW: Convulsions (with renal impairment or high doses) and aseptic meningitis
- NEW: Interstitial nephritis and crystalluria with acute kidney injury
- NEW: Acute pancreatitis and black hairy tongue

**Precautions**: 2 kept, 3 added

- NEW: Infections likely caused by penicillin-resistant S. pneumoniae or non-inhibitable beta-lactamases: not suitable (precaution)
- NEW: Children under 25 kg must not be given tablets; use suspension (precaution)
- NEW: Cephalosporin allergy: possible cross-sensitivity, use with caution (precaution)

**Interactions**: 4 kept, 2 added

- NEW: Methotrexate: penicillins may reduce methotrexate excretion and increase toxicity.
- NEW: Mycophenolate mofetil: pre-dose mycophenolic acid levels fall by about 50%; monitor graft function closely.

**Disease links added**

- `chronic_kidney_disease`: **caution**: Renally cleared: reduce to 500/125 mg 2× a day (CrCl 10–30) or once a day (CrCl <10); 7:1 forms (875/125 mg) not recommended if CrCl <30; convulsion risk
- `rabies`: **safe**: Used for animal-bite wound treatment/prophylaxis (MSF, UK SmPC); it does not treat rabies itself and is given alongside rabies post-exposure care (our inference)

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Most infections (4:1 tablet) (Also children ≥40 kg) | PO | 500/125 mg | Every 8 h | Per response; review if >14 days | 1500/375 mg/day | Label · UK SmPC 625 |
| adult | Most infections (7:1 tablet) (Also children ≥40 kg) | PO | 875/125 mg | 2× a day | Per response; review if >14 days | 1750/250 mg/day | Label · UK SmPC 875 |
| adult | Otitis media, sinusitis, LRTI, UTI (higher dose) | PO | 875/125 mg | Every 8 h | Per response; review if >14 days | 2625/375 mg/day | Label · UK SmPC 875 |
| adult | Animal bites (8:1 form: 1000/125 mg 2× a day) | PO | 875/125 mg | 2× a day | 5–7 days | — | MSF |
| adult | Otitis media / sinusitis after amoxicillin failure (8:1 form: 1000/125 mg 2× a day) | PO | 875/125 mg | 2× a day | 5 days (otitis); 7–10 days (sinusitis) | — | MSF |
| adult | Postpartum upper genital tract infection (8:1 form: 1000/125 mg every 8 h) | PO | 875/125 mg | Every 8 h | 7 days | — | MSF |
| adult | IV-to-oral switch, severe pneumonia (8:1 form: 1000/125 mg every 8 h) | PO | 875/125 mg | Every 8 h | 10–14 days total | — | MSF |
| child | Most infections, <40 kg (4:1 forms) (Tablets only if ≥25 kg; <2 y may need 4:1 suspension) | PO | 20–60 mg/kg/day ÷ 3 | Every 8 h | Per response; review if >14 days | 2400/600 mg/day | Label · UK SmPC 625 |
| child | Most infections, <40 kg (7:1 forms) (No data under 2 months) | PO | 25–45 mg/kg/day ÷ 2 | 2× a day | Per response; review if >14 days | — | Label · UK SmPC susp |
| child | Otitis media, sinusitis, LRTI (higher dose, 7:1) (Not >45 mg/kg/day under 2 years) | PO | 45–70 mg/kg/day ÷ 2 | 2× a day | Per response | 70 mg/kg/day | Label · UK SmPC susp |
| child | Animal bites; otitis/sinusitis after amoxicillin failure (Clavulanate ≤12.5 mg/kg/day) | PO | 25 mg/kg | 2× a day | 5–7 days (bites); 5 days (otitis); 7–10 days (sinusitis) | — | MSF |
| child | Uncomplicated cystitis (girls >2 y) | PO | 12.5 mg/kg | 2× a day | 3 days | — | MSF |
| child | IV-to-oral switch, severe infections (7:1 or 8:1 forms; clavulanate ≤12.5 mg/kg/day) | PO | 50 mg/kg | 2× a day | 10–14 days total (pneumonia) | — | MSF |

- *renal* CrCl >30: No dose adjustment. [Label · UK SmPC 625]
- *renal* CrCl 10–30: 500/125 mg 2× a day; children <40 kg 15/3.75 mg/kg 2× a day (max 500/125 mg per dose). [Label · UK SmPC 625]
- *renal* CrCl <10: 500/125 mg once a day; children <40 kg 15/3.75 mg/kg once a day (max 500/125 mg). [Label · UK SmPC 625]
- *renal* Haemodialysis: 500/125 mg every 24 h, plus one dose during dialysis and another at the end; children 15/3.75 mg/kg before and after dialysis. [Label · UK SmPC 625]
- *renal* CrCl <30: 7:1 forms (875/125 mg tablet, 400/57 mg suspension) are not recommended; use a 4:1 form. [Label · UK SmPC 875]
- *hepatic*: Use with caution and monitor liver function regularly. Liver injury is more common in males, the elderly and with long courses, and may appear weeks after stopping. [Label · UK SmPC 625]
- *elderly*: No dose adjustment; check renal function and adjust if impaired. [Label · UK SmPC 625]
- *pregnancy*: UK label: avoid unless essential (necrotising enterocolitis reported in newborns after use for preterm premature rupture of membranes); passes into breast milk (diarrhoea, thrush in the infant). MSF: not contraindicated in pregnancy or breastfeeding. [Label · UK SmPC 625]
- *administration*: Tablets cannot be divided; children ≤6 years or <25 kg should get suspension. Reconstituted suspension: keep at 2–8 °C, use within 7 days, shake before each dose. [Label · UK SmPC susp]
- *forms_ph*: Tablets 500 mg + 125 mg, 875 mg + 125 mg; granules/powder for suspension 200 mg + 28.5 mg/5 mL (70 mL), 400 mg + 57 mg/5 mL (70 mL), 600 mg + 42.9 mg/5 mL. [PNF]
- *monitor*: Check liver tests, renal function and blood counts during prolonged courses. [Label · UK SmPC 625]
- *monitor*: On warfarin/acenocoumarol: check INR when starting and stopping; on mycophenolate: watch graft function. [Label · UK SmPC 625]
- *monitor*: Children: protracted vomiting 1–4 h after a dose suggests DIES; stop the drug. [Label · UK SmPC 625]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-281): Augmentin 625 mg Tablets – Summary of Product Characteristics. GlaxoSmithKline UK; text revised 24 February 2026. Electronic Medicines Compendium (emc), medicines.org.uk.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10877): Co-amoxiclav 875 mg/125 mg film-coated Tablets – Summary of Product Characteristics. Brown & Burk UK Ltd; text revised 19 September 2025. emc, medicines.org.uk.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10038): Augmentin Duo 400/57 powder for oral suspension – Summary of Product Characteristics. GlaxoSmithKline UK; text revised 6 January 2026. emc, medicines.org.uk.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/amoxicillin-clavulanic-acid-co-amoxiclav-oral-16685119.html): Médecins Sans Frontières. Essential drugs – Amoxicillin/clavulanic acid = co-amoxiclav, oral. MSF Medical Guidelines.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `Label · UK SmPC 625`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-281): Augmentin 625 mg Tablets (500/125 mg). Summary of Product Characteristics. GlaxoSmithKline UK; 2026.
- Dosing source `Label · UK SmPC 875`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10877): Co-amoxiclav 875 mg/125 mg film-coated Tablets. Summary of Product Characteristics. Brown & Burk UK Ltd; 2025.
- Dosing source `Label · UK SmPC susp`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10038): Augmentin Duo 400/57 powder for oral suspension. Summary of Product Characteristics. GlaxoSmithKline UK; 2026.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/amoxicillin-clavulanic-acid-co-amoxiclav-oral-16685119.html): Médecins Sans Frontières. Essential drugs – Co-amoxiclav oral.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-281: Augmentin 625 (GSK, text rev. 24 Feb 2026): 4.1 incl. bone/joint, dental abscess with cellulitis; 4.2 500/125 mg 3× daily, max 1500/375; children <40 kg 20–60 mg/kg/day ÷3, max 2400/600; tablets not <25 kg; renal table (10–30 2× daily, <10 once daily, HD regimen, paediatric 15/3.75 mg/kg); hepatic caution; 4.4 DIES, HLH, Kounis, AGEP, convulsions, hepatic events (males/elderly/prolonged, weeks after), switch to amoxicillin, not for PRSP, periodic renal/hepatic/haematological monitoring; 4.5 methotrexate, mycophenolate ~50% fall, anticoagulant INR, probenecid; 4.6 NEC in PPROM, breast milk; 4.8 frequencies incl. pancreatitis, black hairy tongue, interstitial nephritis, crystalluria, aseptic meningitis; 5.2 ~70% bioavailability, t½ ~1 h, poor CSF penetration
- https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10877: Co-amoxiclav 875/125 (Brown & Burk, rev. 19 Sep 2025): adults 875/125 2× daily (max 1750/250), higher dose 3× daily for otitis/sinusitis/LRTI/UTI (max 2625/375); children 25–45 mg/kg/day ÷2, up to 70 mg/kg/day; 7:1 not recommended CrCl <30; take with a meal
- https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10038: Augmentin Duo 400/57 (GSK, rev. 6 Jan 2026): children 25–45 mg/kg/day ÷2, higher 45–70 mg/kg/day ÷2 for otitis/sinusitis/LRTI; under 2 y not >45 mg/kg/day; no data <2 months; ≤6 y prefer suspension; reconstituted at 2–8 °C, 7 days
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/amoxicillin-clavulanic-acid-co-amoxiclav-oral-16685119.html: MSF co-amoxiclav oral: indications (animal bites, 2nd-line AOM/sinusitis after high-dose amoxicillin, cystitis girls >2 y, postpartum upper genital infection, IV-to-oral switch); doses 25/12.5/50 mg/kg 2× daily, adult 875/125 2× or 3× daily (8:1: 2 × 500/62.5); durations; clavulanate ≤12.5 mg/kg/day or 375 mg/day; cephalosporin cross-sensitivity; not contraindicated in pregnancy/breastfeeding
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF EML lists co-amoxiclav 500+125 mg and 875+125 mg tablets; 200+28.5 mg/5 mL (70 mL), 400+57 mg/5 mL (70 mL), 600+42.9 mg/5 mL suspensions; no IV form listed

---

## Colchicine  (`med_colchicine`)

**Description (kept)**

Colchicine binds tubulin and disrupts microtubules in neutrophils, reducing their migration and inflammasome activation in response to urate crystals. It treats gout flares best when started within 24-36 hours and prevents flares when urate-lowering therapy is started. It has a narrow therapeutic window, and overdose can be fatal.

**Description (added)**

Colchicine is rapidly absorbed (peak 30–120 minutes), concentrates in leucocytes, is excreted mainly in the faeces, and has a half-life of 3–10 hours that rises to about 18.8 hours in severe renal impairment; the lethal single dose varies from about 7 to 65 mg and is generally around 20 mg in adults. A low-dose 0.5 mg once-daily regimen is now licensed in the US to reduce myocardial infarction, stroke and cardiovascular death in atherosclerotic disease. In the Philippines, colchicine is on the PNF Essential Medicines List as a 500 microgram tablet.

**Uses**: 4 kept, 2 added

- NEW: Reduce the risk of myocardial infarction, stroke, coronary revascularization and cardiovascular death in adults with established atherosclerotic disease or multiple cardiovascular risk factors (low-dose 0.5 mg daily)
- NEW: Familial Mediterranean fever in children (attack prophylaxis and prevention of amyloidosis)

**Side effects**: 3 kept, 6 added

- NEW: Agranulocytosis and aplastic anaemia (can be fatal)
- NEW: Vitamin B12 deficiency with long-term use (reversible malabsorption)
- NEW: Gastrointestinal haemorrhage and hepatotoxicity
- NEW: Alopecia and rash
- NEW: Amenorrhoea, dysmenorrhoea, and reversible oligospermia or azoospermia
- NEW: Myalgia (21.2% vs 18.5% with placebo in the LoDoCo2 trial)

**Precautions**: 3 kept, 5 added

- NEW: Pre-existing blood dyscrasias
- NEW: Haemodialysis (colchicine is not removed by dialysis)
- NEW: Renal failure with creatinine clearance below 15 mL/min (low-dose cardiovascular product)
- NEW: Pregnancy and breastfeeding when used for gout (UK SmPC); women of childbearing potential not using effective contraception
- NEW: Galactose intolerance, Lapp lactase deficiency or glucose-galactose malabsorption (lactose-containing tablets; precaution)

**Interactions**: 4 kept, 6 added

- NEW: Itraconazole, voriconazole and HIV protease inhibitors (atazanavir, indinavir): strong CYP3A4 inhibitors; reduce colchicine dose about 4-fold.
- NEW: Diltiazem and erythromycin (moderate CYP3A4 inhibitors): reduce colchicine dose about 2-fold and monitor for toxicity.
- NEW: Fluconazole: moderate CYP3A4 inhibitor; expect higher colchicine levels and monitor.
- NEW: Quinidine, disulfiram and ranolazine (P-gp inhibitors): increased colchicine exposure.
- NEW: Azithromycin: raised colchicine levels reported; follow up during and after treatment.
- NEW: Cimetidine and tolbutamide: reduce colchicine metabolism.

**Brands (intl)**: 1 kept, 1 added

- NEW: Lodoco

**Disease links added**

- `chronic_kidney_disease`: **caution**: Half-life prolonged in renal impairment; reduce dose in mild–moderate impairment; contraindicated in severe impairment and haemodialysis (UK SmPC)
- `acute_coronary_syndrome`: **safe**: Low-dose 0.5 mg daily is licensed (Lodoco) for long-term risk reduction of MI, stroke and CV death in established atherosclerotic disease; not an acute ACS treatment (link inferred from the label indication)

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Acute gout (No new course within 72 h; stop if diarrhoea or vomiting) | PO | 1 mg, then 500 mcg 1 h later | Then 500 mcg every 8 h (after a 12 h pause) if needed | Until relief | 6 mg per course | Label · UK SmPC |
| adult | Gout flare (US regimen) (Higher doses are not more effective) | PO | 1.2 mg, then 0.6 mg 1 h later | Single course | — | 1.8 mg over 1 h | Label · US Colcrys |
| adult | Gout flare prophylaxis (Duration depends on flare frequency and tophi) | PO | 0.5–1 mg | Once a day (evening) | While starting urate-lowering therapy | 1 mg/day | Label · UK SmPC |
| adult | Gout flare prophylaxis (US regimen) (Also adolescents >16 y) | PO | 0.6 mg | 1–2× a day | — | 1.2 mg/day | Label · US Colcrys |
| adult | Familial Mediterranean fever (Split into 2 doses when >1 mg/day) | PO | 1–3 mg/day | Once a day or ÷ 2 | Long-term | 3 mg/day | Label · UK SmPC |
| adult | Cardiovascular risk reduction (Do not double a missed dose) | PO | 0.5 mg | Once a day | Long-term | 0.5 mg/day | Label · US Lodoco |
| child | Familial Mediterranean fever (<5 y) (Specialist supervision only) | PO | 0.5 mg/day | Once a day | Long-term | 2 mg/day | Label · UK SmPC |
| child | Familial Mediterranean fever (5–10 y) (Specialist supervision only) | PO | 1 mg/day | Once a day or ÷ 2 | Long-term | 2 mg/day | Label · UK SmPC |
| child | Familial Mediterranean fever (>10 y) (Up to 2 mg/day in amyloid nephropathy; not for gout in children) | PO | 1.5 mg/day | Once a day or ÷ 2 | Long-term | 2 mg/day | Label · UK SmPC |

- *renal* Mild–moderate: Gout: 0.5 mg/day with close monitoring. FMF: halve the starting dose (≤1 mg/day). [Label · UK SmPC]
- *renal* Severe: Contraindicated, including patients on haemodialysis. [Label · UK SmPC]
- *renal* CrCl <30 / dialysis: US label: prophylaxis start 0.3 mg/day; flare treatment no dose change but repeat courses no more than once every 2 weeks. Dialysis: prophylaxis 0.3 mg twice weekly; flare 0.6 mg single dose, repeat no more than once every 2 weeks. [Label · US Colcrys]
- *hepatic*: Gout: use with caution at 0.5 mg/day. FMF: halve the starting dose (≤1 mg/day). Severe hepatic impairment: contraindicated. [Label · UK SmPC]
- *hepatic*: Avoid with strong P-gp or strong/moderate CYP3A4 inhibitors in any degree of hepatic impairment. [Label · US Lodoco]
- *elderly*: No specific age-based dose, but use with caution in elderly and debilitated patients. [Label · UK SmPC]
- *pregnancy*: Gout: avoid unless NSAIDs and glucocorticoids are unsuitable; do not use while breastfeeding. FMF: may be considered if clinically needed. Women should use contraception during and for 3 months after treatment. [Label · UK SmPC]
- *administration*: Swallow tablets whole with water. With strong CYP3A4 inhibitors (e.g. clarithromycin) the US label cuts flare treatment to 0.6 mg then 0.3 mg 1 h later, repeated no sooner than 3 days. [Label · US Colcrys]
- *monitor*: Full blood count periodically (and at once if petechiae, fever, mouth ulcers, sore throat or bleeding); vitamin B12 with long-term use; muscle symptoms and CK with statins or fibrates; stop at the first diarrhoea or vomiting. [Label · UK SmPC]
- *forms_ph*: Oral: 500 microgram tablet. [PNF]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=colchicine#emc-14362): Colchicine 500 microgram Tablets – Summary of Product Characteristics. Strides Pharma UK Ltd (PL 13606/0271). Electronic Medicines Compendium (emc), medicines.org.uk.
- [DailyMed – COLCRYS](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5ecaa34e-1bed-49a5-b97c-a8f8c0d885a7): COLCRYS (colchicine) tablet, film coated. Prescribing information. AR Scientific Inc. DailyMed, US National Library of Medicine.
- [DailyMed – LODOCO](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ff06d68f-d65f-d097-e053-6294a90a7e5f): LODOCO (colchicine) tablets 0.5 mg. Prescribing information. DailyMed, US National Library of Medicine.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=colchicine#emc-14362): Colchicine 500 microgram Tablets – SmPC. Strides Pharma UK Ltd. emc.
- Dosing source `Label · US Colcrys`: [DailyMed – COLCRYS](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5ecaa34e-1bed-49a5-b97c-a8f8c0d885a7): COLCRYS (colchicine) tablets. Prescribing information. DailyMed.
- Dosing source `Label · US Lodoco`: [DailyMed – LODOCO](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ff06d68f-d65f-d097-e053-6294a90a7e5f): LODOCO (colchicine) tablets 0.5 mg. Prescribing information. DailyMed.
- Dosing source `PNF`: [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): PNF Essential Medicines List, 8th Edition, as of November 02, 2022. PhilHealth / DOH.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=colchicine#emc-14362: Strides colchicine 500 mcg SmPC: 4.1 (acute gout, prophylaxis, FMF adults/children incl. amyloidosis prevention); 4.2 gout 1 mg then 0.5 mg 1 h later, no more for 12 h, then 0.5 mg every 8 h, max 6 mg/course, 72 h between courses; prophylaxis 0.5–1 mg evening; FMF adults 1–3 mg/day max 3; children <5 y 0.5, 5–10 y 1, >10 y 1.5 mg/day, max 2 mg/day; renal/hepatic dosing; 4.3 blood dyscrasias, pregnancy/breastfeeding, contraception, haemodialysis; 4.4 B12, lactose, contraception 3/6 months; 4.5 itraconazole/voriconazole/protease inhibitors (4-fold), diltiazem (2-fold), quinidine/disulfiram/erythromycin, azithromycin, cimetidine/tolbutamide; 4.6; 4.8 adverse list; 4.9 lethal 7–65 mg, ~20 mg; 5.2 Tmax 30–120 min, t½ 3–10 h, 18.8 h severe renal, ~80% faecal, leucocyte accumulation
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5ecaa34e-1bed-49a5-b97c-a8f8c0d885a7: Colcrys label: flare 1.2 mg then 0.6 mg 1 h later (max 1.8 mg/1 h); prophylaxis 0.6 mg 1–2× daily max 1.2 mg/day (adults and >16 y); FMF dosing; renal (severe start 0.3 mg/day; dialysis 0.3 mg twice weekly; flare repeat ≤ once per 2 weeks) and hepatic adjustments; strong CYP3A4 inhibitor table (flare 0.6 then 0.3 mg, repeat ≥3 days)
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ff06d68f-d65f-d097-e053-6294a90a7e5f: Lodoco 0.5 mg label: indication (MI, stroke, revascularization, CV death in atherosclerotic disease/multiple risk factors); 0.5 mg once daily; contraindicated with strong CYP3A4/P-gp inhibitors, CrCl <15, severe hepatic impairment, blood dyscrasias; myalgia 21.2% vs 18.5% (LoDoCo2); fluconazole moderate inhibitor, ranolazine P-gp; hepatic impairment + inhibitors avoid
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Colchicine Oral: 500 microgram tablet listed
- https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query=lodoco: Search used only to find the Lodoco setid; not cited
- https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query=colcrys: Search used only to find the Colcrys setid; not cited

---

## Co-trimoxazole (Sulfamethoxazole + Trimethoprim)  (`med_cotrimoxazole`)

**Description (kept)**

Co-trimoxazole combines sulfamethoxazole, which inhibits dihydropteroate synthase and blocks bacterial use of para-aminobenzoic acid, with trimethoprim, which inhibits dihydrofolate reductase. Sequential blockade of folate synthesis gives a synergistic, often bactericidal effect. It is used for urinary tract infections, shigellosis, traveler's diarrhea, exacerbations of chronic bronchitis, and for treatment and prophylaxis of Pneumocystis jirovecii pneumonia and toxoplasmosis.

**Description (added)**

Trimethoprim has a half-life of about 8.6–17 hours that becomes 1.5–3 times longer when creatinine clearance falls below 10 mL/min, so the dose is reduced in renal impairment. Because of resistance, the UK label keeps it for Pneumocystis pneumonia, toxoplasmosis and nocardiosis, and for urinary tract infection, bronchitis exacerbations and otitis media only when the organism is shown to be susceptible; MSF also uses it for isosporiasis, cyclosporiasis, brucellosis and susceptible typhoid fever. In the Philippines it is on the PNF Essential Medicines List as tablets, oral suspensions and an injection for IV infusion.

**Uses**: 7 kept, 7 added

- NEW: Nocardiosis (treatment)
- NEW: Isosporiasis and cyclosporiasis (treatment); isosporiasis prophylaxis in HIV
- NEW: Brucellosis
- NEW: Uncomplicated typhoid fever, only if the strain is susceptible
- NEW: Bacterial prostatitis and prophylaxis of recurrent UTI
- NEW: Oral treatment of uncomplicated community-associated MRSA infections
- NEW: Listeria monocytogenes infections

**Side effects**: 8 kept, 8 added

- NEW: Headache, diarrhoea and fungal overgrowth (common)
- NEW: Hyponatraemia and metabolic acidosis
- NEW: DRESS and acute generalised exanthematous pustulosis (AGEP)
- NEW: Haemophagocytic lymphohistiocytosis (HLH), very rare
- NEW: Respiratory toxicity (cough, dyspnoea, lung infiltrates) that can progress to ARDS, very rare
- NEW: Aseptic meningitis, convulsions, peripheral neuropathy, ataxia and hallucinations (very rare)
- NEW: Methaemoglobinaemia, pancreatitis and uveitis (very rare)
- NEW: Rhabdomyolysis reported in HIV patients treated for Pneumocystis pneumonia

**Precautions**: 7 kept, 5 added

- NEW: Acute porphyria
- NEW: Group A streptococcal pharyngitis: not recommended, less effective than penicillin (precaution)
- NEW: Severe atopy or bronchial asthma: use with caution (precaution)
- NEW: Pregnancy: avoid in the first trimester and near delivery unless clearly needed; give folate if used (precaution)
- NEW: Breastfeeding infants under 8 weeks or with jaundice: avoid (precaution)

**Interactions**: 8 kept, 9 added

- NEW: Zidovudine: increased risk of haematological toxicity; monitor blood counts.
- NEW: Lamivudine: lamivudine exposure increased by about 40%.
- NEW: Pyrimethamine (>25 mg weekly): risk of megaloblastic anaemia.
- NEW: Thiazide diuretics: increased risk of thrombocytopenia in the elderly.
- NEW: Procainamide and amantadine: competition for renal secretion may raise levels.
- NEW: Repaglinide: increased exposure and risk of hypoglycaemia.
- NEW: Folinic acid: reduces antimicrobial efficacy, including in Pneumocystis treatment and prophylaxis.
- NEW: Oral contraceptives: contraceptive failure reported; use extra barrier protection.
- NEW: Azathioprine: conflicting reports of serious haematological abnormalities.

**Disease links added**

- `typhoid_fever`: **safe**: MSF: for uncomplicated typhoid only if a recent susceptibility test shows the strain is susceptible
- `urinary_tract_infection`: **safe**: UK label: acute uncomplicated UTI when susceptibility is shown; Merck: 3-day course for cystitis where resistance <15%
- `copd`: **safe**: UK label: acute exacerbation of chronic bronchitis when susceptibility is shown
- `chronic_kidney_disease`: **caution**: Halve the dose at CrCl 15–30, not recommended <15; hyperkalaemia and false rise in serum creatinine
- `type2_diabetes`: **caution**: Hypoglycaemia with sulfonylureas or repaglinide (UK label); Merck notes renal adverse effects are more likely in diabetes
- `hypertension`: **caution**: Hyperkalaemia with ACE inhibitors, ARBs, spironolactone and other potassium-sparing diuretics; thrombocytopenia with thiazides in the elderly
- `rheumatic_fever`: **avoid**: Not recommended for group A streptococcal pharyngitis (UK label, Merck); so not suited to rheumatic fever prevention (our inference)

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | UTI, bronchitis exacerbation, otitis (susceptible) (Uncomplicated lower UTI: 1–3 days. Doses as SMX/TMP) | PO | 800/160 mg | Every 12 h | ≥5 days; until symptom-free 2 days | — | Label · UK SmPC |
| adult | Pneumocystis pneumonia, treatment (MSF: 1600/320 mg every 8 h for 21 days) | PO | 100/20 mg/kg/day ÷ 2 or more | In 2+ divided doses | 14 days | — | Label · UK SmPC |
| adult | Pneumocystis pneumonia, prophylaxis (Or 800/160 mg 3× a week on alternate days) | PO | 800/160 mg | Once a day | As long as needed | 1600/320 mg/day | Label · UK SmPC |
| adult | Cerebral toxoplasmosis, treatment | PO | 25/5 mg/kg | 2× a day | 4–6 weeks | — | MSF 2024 |
| adult | Isosporiasis / cyclosporiasis | PO | 800/160 mg | 2× a day | 7–10 days / 7 days | — | MSF 2024 |
| adult | Typhoid fever, pertussis (susceptible) (Typhoid only if strain susceptible) | PO | 800/160 mg | 2× a day | 14 days | — | MSF 2024 |
| adult | Brucellosis | PO | 800/160 mg | 2× a day | 6 weeks | — | MSF 2024 |
| child | Acute infections, 6 weeks–5 months (≈30/6 mg/kg/day) | PO | 100/20 mg (2.5 mL susp) | Every 12 h | ≥5 days | — | Label · UK SmPC susp |
| child | Acute infections, 6 months–5 years (≈30/6 mg/kg/day) | PO | 200/40 mg (5 mL susp) | Every 12 h | ≥5 days | — | Label · UK SmPC susp |
| child | Acute infections, 6–12 years (≈30/6 mg/kg/day) | PO | 400/80 mg (10 mL susp) | Every 12 h | ≥5 days | — | Label · UK SmPC susp |
| child | Pneumocystis pneumonia, treatment (Aim for peak TMP ≥5 microgram/mL) | PO | 100/20 mg/kg/day ÷ 2 or more | In 2+ divided doses | 14 days | — | Label · UK SmPC susp |
| child | Pneumocystis pneumonia, prophylaxis (Age-band volumes as for acute infections) | PO | 750/150 mg/m²/day ÷ 2 | Every 12 h | 3 days a week or daily | 1600/320 mg/day | Label · UK SmPC susp |
| child | Cerebral toxoplasmosis (≥6 weeks) | PO | 25/5 mg/kg | 2× a day | 4–6 weeks | — | MSF 2024 |
| child | Typhoid fever, pertussis, brucellosis (≥6 weeks) (Typhoid only if strain susceptible) | PO | 20/4 mg/kg | 2× a day | 14 days (6 weeks brucellosis) | 800/160 mg/dose | MSF 2024 |

- *renal* CrCl >30: Usual dose. [Label · UK SmPC]
- *renal* CrCl 15–30: Half dose (800/160 mg once a day). [Label · UK SmPC]
- *renal* CrCl <15: Not recommended; no data for children ≤12 years with renal failure. [Label · UK SmPC]
- *hepatic*: No dosing data; contraindicated in severe hepatic impairment. [Label · UK SmPC]
- *elderly*: Standard dose with particular care (more severe reactions, especially with renal/hepatic impairment or other drugs); monthly blood counts on long courses. [Label · UK SmPC]
- *pregnancy*: Folate antagonist: avoid in the first trimester unless clearly needed (give folate) and near delivery (neonatal jaundice, kernicterus risk). MSF: for Pneumocystis prophylaxis/treatment in women with HIV the benefit outweighs the risk; watch the newborn for anaemia or jaundice if used after 36 weeks. [MSF 2024]
- *administration*: Take with food or drink to reduce stomach upset; drink plenty of water to prevent crystalluria. Suspension comes with a 5 mL/2.5 mL spoon. [Label · UK SmPC susp]
- *forms_ph*: Tablet/capsule 400 mg + 80 mg; tablet 800 mg + 160 mg; suspension 200 mg + 40 mg/5 mL (70 mL, 120 mL) and 400 mg + 80 mg/5 mL (60 mL); injection 400 mg + 80 mg, 5 mL ampul for IV infusion. [PNF]
- *monitor*: Monthly full blood count on long courses, in the elderly or folate-deficient. [Label · UK SmPC]
- *monitor*: Check potassium and sodium in patients at risk of hyperkalaemia or hyponatraemia. [Label · UK SmPC]
- *monitor*: Renal impairment: plasma sulfamethoxazole every 2–3 days (12 h post-dose); stop if >150 microgram/mL until <120. [Label · UK SmPC]
- *monitor*: Trimethoprim can raise serum creatinine by about 10% without a true fall in GFR. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-11466): Co-Trimoxazole Forte 160/800 mg Tablets – Summary of Product Characteristics. Tillomed Laboratories Ltd; revised 16 August 2025. Electronic Medicines Compendium (emc), medicines.org.uk.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-6994): Co-Trimoxazole 40 mg/200 mg per 5 ml Paediatric Suspension – Summary of Product Characteristics. Aspen Pharma Trading Ltd; text revised January 2026. emc, medicines.org.uk.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/co-trimoxazole-sulfamethoxazole-smx-trimethoprim-tmp-oral-16683418.html): Médecins Sans Frontières. Essential drugs – Co-trimoxazole = sulfamethoxazole (SMX)/trimethoprim (TMP), oral. MSF Medical Guidelines; updated December 2024.
- [Merck Manual Professional](https://www.merckmanuals.com/professional/infectious-diseases/bacteria-and-antibacterial-medications/trimethoprim-and-sulfamethoxazole): Werth BJ. Trimethoprim and Sulfamethoxazole. Merck Manual Professional Version; reviewed/revised May 2024.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-11466): Co-Trimoxazole Forte 160/800 mg Tablets. Summary of Product Characteristics. Tillomed Laboratories Ltd; 2025.
- Dosing source `Label · UK SmPC susp`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-6994): Co-Trimoxazole 40 mg/200 mg per 5 ml Paediatric Suspension. Summary of Product Characteristics. Aspen Pharma Trading Ltd; 2026.
- Dosing source `MSF 2024`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/co-trimoxazole-sulfamethoxazole-smx-trimethoprim-tmp-oral-16683418.html): Médecins Sans Frontières. Essential drugs – Co-trimoxazole oral. Updated December 2024.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-11466: Co-Trimoxazole Forte (Tillomed, rev. 16 Aug 2025): 4.1 PJP, toxoplasmosis, nocardiosis; UTI/AECB/otitis when susceptible; 4.2 1 tab every 12 h, ≥5 days, UTI 1–3 days; renal table (>30 usual, 15–30 once daily, <15 not recommended), SMX level monitoring 150/120; PJP 20/100 mg/kg/day for 2 weeks; prophylaxis regimens, max 320/1600; hepatic no data; 4.3 acute porphyria, first 6 weeks; 4.4 DRESS, AGEP, HLH, respiratory toxicity/ARDS, monthly blood counts, K/Na, metabolic acidosis, asthma/atopy, not for GABHS pharyngitis; 4.5 zidovudine, lamivudine +40%, pyrimethamine, thiazides, procainamide/amantadine, repaglinide, folinic acid, OCs, azathioprine, creatinine +10%; 4.6 pregnancy/breastfeeding; 4.8 frequencies; 5.2 TMP t½ 8.6–17 h, ×1.5–3 if CrCl <10
- https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-6994: Paediatric suspension (Aspen, text rev. Jan 2026): age-band doses 2.5/5/10 mL every 12 h (≈6/30 mg/kg/day); PJP treatment 20/100 mg/kg/day ≥2 divided doses 2 weeks, peak TMP ≥5; prophylaxis ≈150/750 mg/m²/day, schedules, max 320/1600; with food; measuring spoon; not in first 6 weeks
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/co-trimoxazole-sulfamethoxazole-smx-trimethoprim-tmp-oral-16683418.html: MSF co-trimoxazole oral (updated Dec 2024): indications incl. isosporiasis, cyclosporiasis, brucellosis, susceptible typhoid, 2nd-line pertussis; doses toxoplasmosis 25/5 mg/kg 2×, adult PJP 1600/320 mg 3× daily, 800/160 2× daily for isospora/cyclospora/typhoid/pertussis/brucellosis, child 20/4 mg/kg 2× (max 800/160); durations; pregnancy/HIV benefit statement, observe newborn after 36 weeks; plenty of water. (Child prophylaxis 50/10 mg/kg once daily seen but not used as it could not be double-checked.)
- https://www.merckmanuals.com/professional/infectious-diseases/bacteria-and-antibacterial-medications/trimethoprim-and-sulfamethoxazole: Merck Manual (Werth, May 2024): indications prostatitis, recurrent UTI prophylaxis, 3-day cystitis if resistance <15%, Nocardia, Listeria, CA-MRSA oral; not effective for GAS pharyngitis; renal adverse effects more likely with renal insufficiency or diabetes; creatinine rise from tubular secretion block
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF EML lists cotrimoxazole 400/80 mg tablet/capsule, 800/160 mg tablet, 200/40 mg per 5 mL (70, 120 mL) and 400/80 mg per 5 mL (60 mL) suspensions, 400/80 mg 5 mL ampul for IV infusion

---

## Dapagliflozin  (`med_dapagliflozin`)

**Description (kept)**

Dapagliflozin inhibits the sodium-glucose cotransporter 2 in the proximal renal tubule, reducing glucose reabsorption and increasing urinary glucose excretion independent of insulin. It also causes natriuresis and osmotic diuresis, lowers blood pressure and reduces intraglomerular pressure. It is used for type 2 diabetes and, independent of diabetes status, to reduce cardiovascular and kidney outcomes in heart failure and chronic kidney disease.

**Description (added)**

It is more than 1,400-fold selective for SGLT2 over SGLT1, has an oral bioavailability of 78% and a terminal half-life of about 12.9 hours, and is cleared mainly by UGT1A9 glucuronidation rather than CYP enzymes. Because its glucose-lowering effect depends on blood glucose and kidney function, hypoglycaemia risk on its own is low and the glucose-lowering effect fades below an eGFR of 45, while the heart and kidney benefits persist. In the Philippines, the DOH added dapagliflozin 10 mg film-coated tablet to the Philippine National Formulary in April 2023 as add-on therapy to metformin for adults with type 2 diabetes who have, or are at high risk of, cardiovascular disease or diabetic nephropathy.

**Uses**: 4 kept, 1 added

- NEW: Type 2 diabetes in children aged 10 years and above (adjunct to diet and exercise)

**Side effects**: 6 kept, 6 added

- NEW: Dizziness, rash, back pain and dysuria (common)
- NEW: Increased haematocrit and dyslipidaemia (common)
- NEW: Thirst, dry mouth, constipation and nocturia (uncommon)
- NEW: Transient rise in serum creatinine and fall in creatinine clearance at the start of treatment
- NEW: Angioedema and tubulointerstitial nephritis (very rare)
- NEW: Lower-limb amputations (mainly toes) seen more often in long-term SGLT2 inhibitor studies

**Precautions**: 1 kept, 4 added

- NEW: Type 1 diabetes: should not be used
- NEW: Second and third trimesters of pregnancy: not recommended; stop when pregnancy is detected
- NEW: Breastfeeding: should not be used
- NEW: Galactose intolerance, total lactase deficiency or glucose-galactose malabsorption (contains lactose; precaution)

**Interactions**: 4 kept, 3 added

- NEW: Rifampicin: lowers dapagliflozin exposure (AUC −22%); no dose adjustment needed.
- NEW: Mefenamic acid (UGT1A9 inhibitor): raises dapagliflozin exposure (AUC +55%); no dose adjustment needed.
- NEW: No clinically relevant effect on metformin, sitagliptin, glimepiride, valsartan, digoxin or warfarin.

**Disease links added**

- `urinary_tract_infection`: **caution**: Glucosuria raises UTI risk; consider temporarily stopping dapagliflozin while treating pyelonephritis or urosepsis (UK SmPC)

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Type 2 diabetes (Consider lower insulin or sulfonylurea dose) | PO | 10 mg | Once a day | Long-term | 10 mg/day | Label · UK SmPC |
| adult | Type 2 diabetes (US regimen) (Not for glycaemic control if eGFR <45) | PO | 5 mg, may increase to 10 mg | Once a day | Long-term | 10 mg/day | Label · US |
| adult | Type 2 diabetes with CVD or nephropathy (PNF, add-on to metformin) (PH government-financed indication) | PO | 10 mg | Once a day | Long-term | 10 mg/day | DOH 2023 |
| adult | Heart failure (Reduced or preserved ejection fraction) | PO | 10 mg | Once a day | Long-term | 10 mg/day | Label · UK SmPC |
| adult | Chronic kidney disease (With or without diabetes) | PO | 10 mg | Once a day | Long-term | 10 mg/day | Label · UK SmPC |
| child | Type 2 diabetes (≥10 y) (No data under 10 y) | PO | 10 mg | Once a day | Long-term | 10 mg/day | Label · UK SmPC |
| child | Type 2 diabetes (≥10 y, US regimen) (HF and CKD use not established in children) | PO | 5 mg, may increase to 10 mg | Once a day | Long-term | 10 mg/day | Label · US |

- *renal* eGFR <45: No dose adjustment by renal function. Initiation not recommended at eGFR <15 (UK); glucose-lowering effect reduced below 45 and likely absent in severe impairment, so add another glucose-lowering drug if needed. [Label · UK SmPC]
- *hepatic*: No adjustment in mild or moderate impairment. Severe impairment: start 5 mg once a day, increase to 10 mg if tolerated. [Label · UK SmPC]
- *elderly*: No dose adjustment by age; take extra care with volume depletion and hypotension. [Label · UK SmPC]
- *pregnancy*: Not recommended in the 2nd and 3rd trimesters (kidney toxicity in rats); stop when pregnancy is detected. Do not use while breastfeeding. [Label · UK SmPC]
- *administration*: Once a day at any time, with or without food; swallow whole. Correct volume depletion before starting. [Label · UK SmPC]
- *monitor*: Kidney function before starting and as needed; volume status and blood pressure; ketones (blood preferred) if unwell or around surgery, even with normal glucose; genital or perineal pain with fever (Fournier's); foot care; haematocrit. [Label · UK SmPC]
- *forms_ph*: Oral: 10 mg film-coated tablet (added to the PNF on 11 April 2023 via DOH-DC No. 2023-0169). [PNF]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=dapagliflozin#emc-7607): Forxiga 10 mg film-coated tablets – Summary of Product Characteristics. AstraZeneca UK Limited. Electronic Medicines Compendium (emc), medicines.org.uk.
- [PhilHealth Advisory No. 2024-0026](https://www.philhealth.gov.ph/advisories/2024/PA2024-0026.pdf): Philippine Health Insurance Corporation. Advisory No. 2024-0026: Philippine National Formulary Essential Medicines List (8th Edition) and additional medicines as of April 25, 2024. Signed May 30, 2024.
- [DOH Department Circular 2023-0169](https://hta.dost.gov.ph/wp-content/uploads/2025/05/DOH-DC-2023-0169-SOH-Decision-on-HTAC-Recommendation-on-Dapagliflozin-for-T2DM-Patients-11-April-2023.pdf): Department of Health. Secretary of Health Decision on the HTA Council Recommendation on Dapagliflozin for Type 2 Diabetes Mellitus Patients. Department Circular No. 2023-0169, 11 April 2023.
- [HTA Philippines](https://hta.dost.gov.ph/published-assessment/dapagliflozin-5mg-and-10-mg-tablet-for-2nd-line-treatment-of-type-2-diabetes-mellitus-t2dm/): Health Technology Assessment Council (Philippines). Dapagliflozin for 2nd-line treatment of type 2 diabetes mellitus: published assessment and recommendation.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=dapagliflozin#emc-7607): Forxiga 10 mg film-coated tablets – SmPC. AstraZeneca UK Limited. emc.
- Dosing source `Label · US`: [DailyMed (US National Library of Medicine)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=72ad22ae-efe6-4cd6-a302-98aaee423d69): FARXIGA (dapagliflozin) tablets. Prescribing information. DailyMed.
- Dosing source `PNF`: [PhilHealth Advisory No. 2024-0026](https://www.philhealth.gov.ph/advisories/2024/PA2024-0026.pdf): PhilHealth Advisory No. 2024-0026: PNF EML 8th Edition and medicines added as of April 25, 2024 (dapagliflozin added via DOH-DC No. 2023-0169).
- Dosing source `DOH 2023`: [DOH Department Circular 2023-0169](https://hta.dost.gov.ph/wp-content/uploads/2025/05/DOH-DC-2023-0169-SOH-Decision-on-HTAC-Recommendation-on-Dapagliflozin-for-T2DM-Patients-11-April-2023.pdf): DOH DC No. 2023-0169: SOH Decision on HTAC Recommendation on Dapagliflozin for T2DM Patients, 11 April 2023.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=dapagliflozin#emc-7607: Forxiga SmPC (AstraZeneca UK, updated July 2026): 4.1 incl. T2DM children ≥10 y; 4.2 10 mg once daily all indications, renal (initiation not recommended eGFR <15, efficacy reduced <45), severe hepatic start 5 mg, elderly, administration; 4.4 DKA/type 1 diabetes, volume, Fournier, UTI interruption for pyelonephritis/urosepsis, haematocrit, amputation, lactose; 4.5 rifampicin −22%, mefenamic acid +55%, no relevant effect on metformin etc., UGT1A9; 4.6 not in 2nd/3rd trimester, not breastfeeding; 4.8 frequencies; 5.1 >1400-fold selectivity. (Section 5.2 could not be read via WebFetch.)
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=72ad22ae-efe6-4cd6-a302-98aaee423d69: Farxiga US label: 5 mg start up to 10 mg for glycaemic control in adults and children ≥10 y; 10 mg for HF/CKD; eGFR thresholds; peds HF/CKD not established; bioavailability 78%; t½ ~12.9 h (already an existing ref; used as dose-table source only)
- https://www.philhealth.gov.ph/advisories/2024/PA2024-0026.pdf: PhilHealth Advisory 2024-0026 (signed May 30, 2024): Dapagliflozin 10 mg film-coated tablet added to PNF April 11, 2023 under DOH-DC No. 2023-0169
- https://hta.dost.gov.ph/wp-content/uploads/2025/05/DOH-DC-2023-0169-SOH-Decision-on-HTAC-Recommendation-on-Dapagliflozin-for-T2DM-Patients-11-April-2023.pdf: DOH circular 11 April 2023: SOH approved inclusion of dapagliflozin 10 mg film-coated tablet in PNF as add-on to metformin for adults with T2DM with or at high risk of CVD and/or diabetic nephropathy
- https://hta.dost.gov.ph/published-assessment/dapagliflozin-5mg-and-10-mg-tablet-for-2nd-line-treatment-of-type-2-diabetes-mellitus-t2dm/: HTA Council page: recommendation for PNF inclusion, 10 mg tablet, add-on to metformin (2nd line), SOH approval April 11, 2023
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Dapagliflozin NOT in the Nov 2022 PNF EML text (D entries Dacarbazine–Dapsone–Deferiprone); hence the 2024 advisory is used

---

