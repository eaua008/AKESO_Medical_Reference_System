# Medicine review b04: review sheet

Run `036_medicines_review_04.sql` in Supabase after you have checked this. Everything below is ADDED; the existing text stays as it is.

Every link was opened twice: by the research step (to read the fact), and again in Akeso's own browser pane on your computer in the Philippines (to make sure it opens for you, not just from the cloud). See NOTES.md in the batch folder for any link that needs attention.

UK SmPC links open the official MHRA Products search (free) for that medicine: the emc site (medicines.org.uk) now limits free page views for users outside the UK. The citation still names the exact product and PL number to pick.

## Please check (batch 04)

- **Ibuprofen, isoniazid, ivermectin:** the research for these three was cut off by a usage limit just before its final report. The files were complete and pass all checks, and the links were opened again from your computer, but please review these three more carefully.
- **Loperamide → typhoid, *avoid*:** inferred from "invasive Salmonella" in the label. **→ HIV, *safe*:** MSF use; the UK label says stop at the first sign of abdominal distension in AIDS.
- **Mefenamic acid:** the adult maximum (1,500 mg/day) and child maximums are worked out from the dose × 3 a day; the label gives no explicit maximum. Dengue: PhilHealth 2026 dengue standards say no NSAIDs.
- **Metformin → acute gastroenteritis, *caution*:** inferred from the dehydration contraindication.
- **Methimazole:** the child maximum is 40 mg/day (EU label) vs 30 mg/day in the existing text. The EU label is a PDF from the Swedish agency.
- **Metronidazole:** the UK child tables were garbled, so child doses come from MSF. Alcohol: the UK label says 48 h; the existing fact says 3 days (unchanged).
- **Metoprolol:** hypertension maximum 200 mg/day (UK) vs 450 mg/day in the existing text (US).


---

## Ibuprofen  (`med_ibuprofen`)

**Description (kept)**

Ibuprofen is a non-selective, reversible inhibitor of COX-1 and COX-2 that reduces prostaglandin synthesis, producing analgesic, antipyretic and anti-inflammatory effects. It is widely used for mild-to-moderate pain, fever, dysmenorrhea and inflammatory joint conditions.

**Description (added)**

In the Philippines, where dengue is endemic, NSAIDs such as ibuprofen are not recommended in suspected or confirmed dengue because they raise bleeding risk; PhilHealth's 2026 dengue quality standards and DOH advice name paracetamol as the antipyretic of choice, and DOH advises avoiding ibuprofen until dengue is ruled out. Ibuprofen can also mask fever and pain, which may delay recognition of a worsening infection.

**Uses**: 4 kept, 3 added

- NEW: Migraine attacks (400 mg single dose)
- NEW: Juvenile idiopathic (rheumatoid) arthritis, under prescription (higher mg/kg doses)
- NEW: Post-immunisation fever in infants (limited to 2 doses)

**Side effects**: 8 kept, 5 added

- NEW: Severe skin reactions: SJS, TEN, DRESS, AGEP (mostly in the first month)
- NEW: Interstitial nephritis, nephrotic syndrome; renal tubular acidosis and hypokalaemia with prolonged high doses
- NEW: Rare blood dyscrasias (agranulocytosis, pancytopenia)
- NEW: Kounis syndrome (allergic acute coronary syndrome) has been reported
- NEW: Masking of fever and pain, delaying treatment of infection

**Precautions**: 3 kept, 7 added

- NEW: Suspected or confirmed dengue: NSAIDs are not recommended (PhilHealth / DOH / WHO); use paracetamol
- NEW: Previous NSAID-related GI bleeding or perforation; active or recurrent peptic ulcer or haemorrhage
- NEW: Severe heart failure (NYHA class IV)
- NEW: Severe renal failure or severe hepatic failure
- NEW: Last trimester of pregnancy
- NEW: Significant dehydration (vomiting, diarrhoea or poor fluid intake)
- NEW: Cerebrovascular or other active bleeding; unexplained blood-formation disorders

**Interactions**: 6 kept, 8 added

- NEW: Corticosteroids and other NSAIDs (including COX-2 inhibitors): increased GI ulceration and bleeding.
- NEW: Quinolone antibiotics: possible increased risk of convulsions.
- NEW: Ciclosporin and tacrolimus: increased nephrotoxicity.
- NEW: Zidovudine: increased haematological toxicity (haemarthrosis/haematoma in haemophiliacs).
- NEW: CYP2C9 inhibitors (fluconazole, voriconazole): higher ibuprofen exposure; consider dose reduction.
- NEW: Digoxin and phenytoin: plasma levels may rise.
- NEW: Sulfonylureas: possible enhanced hypoglycaemic effect; monitor glucose.
- NEW: Mifepristone: avoid NSAIDs for 8–12 days after mifepristone.

**Disease links added**

- `cholera`: **avoid**: UK SmPC contraindicates ibuprofen in significant dehydration from vomiting or diarrhoea, with renal risk in dehydrated children (applied to cholera by inference).
- `ischemic_stroke`: **caution**: UK SmPC: small increased risk of arterial thrombotic events such as MI and stroke, mainly at high doses (2400 mg/day); use lowest dose for shortest time.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Pain, fever (≥12 y, ≥40 kg) (Not in suspected dengue: use paracetamol) | PO | 200–400 mg | Every 6 h as needed (3–4× a day) | Short term | 1,200 mg/day (OTC) | Label · UK SmPC |
| adult | Migraine | PO | 400 mg | Single dose; repeat 400 mg after ≥6 h if needed | — | 1,200 mg/day | Label · UK SmPC |
| adult | Primary dysmenorrhoea | PO | 200–400 mg | 1–3× a day | — | 1,200 mg/day | Label · UK SmPC |
| adult | Rheumatic disease (Max single dose 800 mg) | PO | 1,200–1,800 mg/day ÷ 3–4 | 3–4× a day | Maintenance 600–1,200 mg/day | 2,400 mg/day | Label · UK SmPC |
| child | Pain, fever (3 mo–12 y) (Not under 3 months) | PO | 20 mg/kg/day ÷ 3–4 | Every 6–8 h | ≤3 days without review | — | Label · UK SmPC susp |
| child | Pain, fever, 3–6 mo (>5 kg) (See doctor within 24 h if symptoms persist) | PO | 50 mg (2.5 mL of 100 mg/5 mL) | Up to 3× in 24 h | Max 24 h | 150 mg/day | Label · UK SmPC susp |
| child | Pain, fever, 6 mo–1 y | PO | 50 mg (2.5 mL) | 3–4× a day | ≤3 days | 200 mg/day | Label · UK SmPC susp |
| child | Pain, fever, 1–4 y | PO | 100 mg (5 mL) | 3× a day | ≤3 days | 300 mg/day | Label · UK SmPC susp |
| child | Pain, fever, 4–7 y | PO | 150 mg (7.5 mL) | 3× a day | ≤3 days | 450 mg/day | Label · UK SmPC susp |
| child | Pain, fever, 7–12 y | PO | 200 mg (10 mL) | 3× a day | ≤3 days | 600 mg/day | Label · UK SmPC susp |
| child | Juvenile rheumatoid arthritis (Prescription only) | PO | 30–40 mg/kg/day ÷ 3–4 | 3–4× a day | — | — | Label · UK SmPC susp |

- *renal*: Mild to moderate impairment: lowest dose for the shortest time and monitor renal function. Contraindicated in severe renal failure. [Label · UK SmPC]
- *hepatic*: Mild to moderate impairment: lowest dose for the shortest time and monitor liver function. Contraindicated in severe hepatic failure. [Label · UK SmPC]
- *elderly*: Higher risk of serious GI bleeding and perforation: lowest dose, shortest duration, review regularly. [Label · UK SmPC]
- *pregnancy*: Avoid in the first and second trimesters unless clearly needed. From week 20, risk of oligohydramnios and ductus arteriosus constriction (consider antenatal monitoring after several days of use). Contraindicated in the third trimester. Short courses are acceptable in breastfeeding. [Label · UK SmPC]
- *monitor*: Before giving for fever in the Philippines, consider dengue: NSAIDs (ibuprofen, celecoxib, aspirin) are not recommended; give paracetamol instead. Watch for GI bleeding signs (melena, haematemesis), blood pressure, urine output and hydration, especially in children with vomiting or diarrhoea. [PhilHealth 2026]
- *administration*: Children from 6 months: see a doctor if needed for more than 3 days; adults: if needed for more than 10 days. Keep at least 4 h between doses. [Label · UK SmPC susp]
- *forms_ph*: 200 mg and 400 mg tablet; 100 mg/5 mL syrup/suspension (60 mL); 200 mg/5 mL suspension (60 mL). [PNF]

**References added**

- [PhilHealth Dengue Quality Standards](https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf): Philippine Health Insurance Corporation. Quality Standards on the Diagnosis and Management of Dengue (Adult and Children) as a Reference of the Corporation. PhilHealth Circular No. 2026-0009.
- [WHO Fact Sheet - Dengue](https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue): World Health Organization. Dengue and severe dengue. Fact sheet. Geneva: WHO.
- [UK SmPC (emc) - tablets](https://products.mhra.gov.uk/search/?search=ibuprofen#emc-7020): Ibuprofen 400 mg film-coated tablets (POM) - Summary of Product Characteristics. Milpharm Ltd. Electronic medicines compendium (emc), revised June 2026.
- [UK SmPC (emc) - suspension](https://products.mhra.gov.uk/search/?search=ibuprofen#emc-4560): Ibuprofen 100 mg/5 ml Oral Suspension - Summary of Product Characteristics. Pinewood Laboratories Ltd. Electronic medicines compendium (emc), revised August 2024.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc) - tablets](https://products.mhra.gov.uk/search/?search=ibuprofen#emc-7020): Ibuprofen 400 mg film-coated tablets (POM) - SmPC. Milpharm Ltd, 2026.
- Dosing source `Label · UK SmPC susp`: [UK SmPC (emc) - suspension](https://products.mhra.gov.uk/search/?search=ibuprofen#emc-4560): Ibuprofen 100 mg/5 ml Oral Suspension - SmPC. Pinewood Laboratories Ltd, 2024.
- Dosing source `PNF`: [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.
- Dosing source `PhilHealth 2026`: [PhilHealth Dengue Quality Standards](https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf): PhilHealth Circular No. 2026-0009: Quality Standards on the Diagnosis and Management of Dengue (Adult and Children).

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Ibuprofen oral: 200 mg and 400 mg tablet; 100 mg/5 mL, 60 mL syrup/suspension; 200 mg/5 mL, 60 mL suspension.
- https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf: PhilHealth circular 'Quality Standards on the Diagnosis and Management of Dengue (Adult and Children)': Sec V.D.2.d use of NSAIDs such as ibuprofen, celecoxib, aspirin is not recommended; V.D.2.c paracetamol may be given for fever in adults and children.
- https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue: Paracetamol for pain; NSAIDs such as ibuprofen and aspirin should be avoided as they can increase the risk of bleeding.
- https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf: PhilHealth dengue standards: NSAIDs (ibuprofen named) are not recommended in dengue; paracetamol for fever.
- https://products.mhra.gov.uk/search/?search=ibuprofen#emc-7020: Milpharm 400 mg POM SmPC (rev 06/2026): adult pain/fever 200–400 mg every 6 h max 1200 mg/day; migraine 400 mg; dysmenorrhoea 200–400 mg 1–3×/day; rheumatic 1200–1800 mg/day, maintenance 600–1200, up to 2400 mg/day; max single 800 mg; renal/hepatic mild-moderate lowest dose + monitor, severe contraindicated; full contraindication list incl. NYHA IV, last trimester, significant dehydration, active bleeding; varicella and masking-infection warnings; interactions (quinolones, ciclosporin, tacrolimus, zidovudine, CYP2C9 inhibitors, sulphonylureas, digoxin, phenytoin, mifepristone 8–12 days, corticosteroids); pregnancy week 20 oligohydramnios/ductus; SJS/TEN/DRESS/AGEP, Kounis syndrome, agranulocytosis, interstitial nephritis, MI/stroke risk at 2400 mg/day.
- https://products.mhra.gov.uk/search/?search=ibuprofen#emc-4560: Pinewood 100 mg/5 ml SmPC (rev 08/2024): 3–6 mo >5 kg 2.5 mL up to 3×/24 h, max 24 h; 6–12 mo 2.5 mL 3–4×; 1–4 y 5 mL 3×; 4–7 y 7.5 mL 3×; 7–12 y 10 mL 3×; 20 mg/kg/day divided; JRA 30–40 mg/kg/day in 3–4 doses; not under 3 months; children consult if >3 days, adults >10 days; post-immunisation fever max 2 doses; risk of renal impairment in dehydrated children; avoid in varicella.

---

## Isoniazid  (`med_isoniazid`)

**Description (kept)**

Isoniazid is a prodrug activated by mycobacterial catalase-peroxidase (KatG) that inhibits mycolic acid synthesis in the cell wall, making it bactericidal against actively dividing M. tuberculosis. It is used in first-line combination therapy for active TB and as monotherapy or in combination for latent TB infection.

**Description (added)**

In the Philippine NTP it is part of every first-line regimen, given as HRZE then HR fixed-dose combination tablets dosed by body-weight band (Category I 2HRZE/4HR; Category II 2HRZES/1HRZE/5HRE), and isoniazid preventive therapy (IPT) is given to household contacts under 5 years and to people living with HIV without active TB. WHO's 2024 TB preventive treatment guideline recommends 6 or 9 months of daily isoniazid, weekly isoniazid plus rifapentine for 3 months (3HP), or daily isoniazid plus rifampicin for 3 months (3HR), with 1 month of daily isoniazid plus rifapentine (1HP) as an alternative.

**Uses**: 2 kept, 3 added

- NEW: Isoniazid preventive therapy for household contacts under 5 years of a TB case, after active TB is ruled out (PH NTP)
- NEW: Isoniazid preventive therapy for 6 months in people living with HIV without active TB (PH NTP)
- NEW: Short-course TB preventive treatment combined with rifapentine (3HP, 1HP) or rifampicin (3HR) (WHO)

**Side effects**: 6 kept, 6 added

- NEW: Severe skin reactions (SJS, TEN, DRESS, AGEP): never restart isoniazid
- NEW: Blood disorders: agranulocytosis, aplastic and haemolytic anaemia (frequency unknown)
- NEW: Psychotic reactions, mood changes and depression
- NEW: Deafness, tinnitus and vertigo
- NEW: Gynaecomastia, pancreatitis, hypoglycaemia; nicotinic acid deficiency secondary to pyridoxine deficiency
- NEW: Minor GI upset (manage by giving at bedtime or with small meals, PH NTP)

**Precautions**: 3 kept, 2 added

- NEW: Drug-induced liver disease (UK SmPC)
- NEW: Severe hepatic impairment (MSF)

**Interactions**: 5 kept, 6 added

- NEW: Benzodiazepines (diazepam, triazolam): increased toxicity; diazepam may cause sedation and respiratory depression.
- NEW: Warfarin: increased bleeding risk; monitor closely.
- NEW: Itraconazole (co-administration not recommended) and ketoconazole: reduced azole levels.
- NEW: Primidone, disulfiram and chlorzoxazone: reduced hepatic metabolism, possible toxicity.
- NEW: Levodopa: effect may be reduced.
- NEW: Stavudine: increased risk of peripheral neuropathy.

**Disease links added**

- `hiv_infection`: **safe**: PH NTP: people living with HIV without active TB are given 6 months of IPT; give pyridoxine (HIV raises neuropathy and hepatotoxicity risk).
- `hepatitis_b`: **caution**: Chronic liver disease raises hepatotoxicity risk (MSF); monitor liver function and stop if jaundice develops. Contraindicated if hepatic impairment is severe.
- `chronic_kidney_disease`: **caution**: UK SmPC advises care in renal impairment (ototoxicity reported in end-stage disease); uraemia raises neuropathy risk, so give pyridoxine. No dose change stated.
- `type2_diabetes`: **caution**: UK SmPC: use with care in diabetes; diabetics are at higher risk of peripheral neuropathy and should get pyridoxine.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | TB Cat I (2HRZE/4HR), 30–37 kg (HRZE 2 months then HR 4 months (HR 10 months for Cat Ia)) | PO | 2 tablets FDC | Once a day | 6 months | — | NTP MOP 2014 |
| adult | TB Cat I (2HRZE/4HR), 38–54 kg | PO | 3 tablets FDC | Once a day | 6 months | — | NTP MOP 2014 |
| adult | TB Cat I (2HRZE/4HR), 55–70 kg | PO | 4 tablets FDC | Once a day | 6 months | — | NTP MOP 2014 |
| adult | TB Cat I (2HRZE/4HR), >70 kg | PO | 5 tablets FDC | Once a day | 6 months | — | NTP MOP 2014 |
| adult | TB, single-drug formulation (UK SmPC and MSF give max 300 mg/day) | PO | 5 mg/kg (range 4–6) | Once a day | Per regimen | 400 mg/day | NTP MOP 2014 |
| adult | TB meningitis (early phase) | PO | Up to 10 mg/kg | Once a day | Early treatment | — | Label · UK SmPC |
| adult | TB preventive treatment (6H / 9H) (PH NTP: 6 months for PLHIV; WHO 2024 regimen) | PO | 5 mg/kg (range 4–6) | Once a day | 6 or 9 months | 300 mg/day | MSF |
| adult | TB preventive treatment (3HR, with rifampicin) (WHO 2024 regimen) | PO | 5 mg/kg (range 4–6) | Once a day | 3 months | 300 mg/day | MSF |
| adult | TB preventive treatment (3HP, with rifapentine) (Adults and children ≥30 kg) | PO | 900 mg | Once a week | 3 months | 900 mg/week | MSF |
| adult | TB preventive treatment (1HP, with rifapentine) (Age 13 y and over; WHO alternative option) | PO | 300 mg | Once a day | 1 month | 300 mg/day | MSF |
| child | TB, single-drug formulation (Newborn <4 weeks: refer to pediatrician) | PO | 10 mg/kg (range 10–15) | Once a day | Per regimen | 300 mg/day | NTP MOP 2014 |
| child | TB intensive phase, HZR 50/150/75 dispersible (Then HR 50/75: 4–7 kg 1, 8–11 kg 2, 12–14 kg 3 tablets) | PO | 4–7 kg: 1 tab; 8–11 kg: 2; 12–15 kg: 3; 16–22 kg: 4 | Once a day | 2 months | — | MSF TB |
| child | TB preventive treatment (6H / 3HR), <30 kg (PH NTP: contacts <5 y after TB ruled out) | PO | 10 mg/kg (range 7–15) | Once a day | 6 months (6H) or 3 months (3HR) | 300 mg/day | MSF |
| child | TB preventive treatment (3HP), >2 y and <30 kg (With weekly rifapentine) | PO | 20–30 mg/kg | Once a week | 3 months | — | MSF |

- *renal*: No dose adjustment stated; use with care in renal impairment (deafness/tinnitus reported in end-stage renal disease). Renal impairment and uraemia raise neuropathy risk: give pyridoxine. [Label · UK SmPC]
- *hepatic*: Contraindicated in drug-induced liver disease (SmPC) and severe hepatic impairment (MSF). In known liver disease monitor liver function; any deterioration is a reason to stop. Stop if jaundice appears. [MSF]
- *elderly*: No dose reduction needed, but use caution as renal and hepatic function may be reduced; age over 35 raises hepatotoxicity risk (MSF). [Label · UK SmPC]
- *pregnancy*: Not contraindicated in pregnancy or breastfeeding; give the mother pyridoxine 10 mg daily and the breastfed infant 5 mg daily. WHO: pregnancy alone should not exclude TB preventive treatment, but use of 1HP and 3HP in pregnancy is cautioned until more data are available. [MSF]
- *administration*: Take once daily on an empty stomach. If GI upset occurs, PH NTP advises giving drugs at bedtime or with small meals. Avoid tyramine/histamine-rich foods (cured meats, matured cheese, tuna, mackerel). [MSF]
- *monitor*: Pyridoxine (vitamin B6) 10 mg daily for prevention and 50–100 mg daily for treatment of peripheral neuropathy (burning feet). Baseline and regular liver tests; stop if AST rises above 3× normal or bilirubin increases (UK SmPC). Ask monthly about jaundice, nausea, numbness. [NTP MOP 2014]
- *forms_ph*: 300 mg and 400 mg tablet; 200 mg/5 mL syrup (120 mL). FDCs: isoniazid + rifampicin 50/75 mg dispersible (pediatric) and 75/150 mg tablet; + ethambutol 75/150/275 mg; isoniazid + rifampicin + pyrazinamide 50/75/150 mg dispersible (pediatric); HRZE 75/150/400/275 mg tablet. [PNF]

**References added**

- [Philippine NTP Manual of Procedures](https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf): Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.
- [WHO TB guidelines - TB preventive treatment](https://tbksp.who.int/en/node/43): World Health Organization. WHO consolidated guidelines on tuberculosis. Module 1: prevention - tuberculosis preventive treatment, 2nd ed. Geneva: WHO; 2024. Section 1.4, TB preventive treatment options (WHO TB Knowledge Sharing Platform).
- [WHO operational handbook - TPT regimens](https://tbksp.who.int/en/node/1271): World Health Organization. WHO operational handbook on tuberculosis. Module 1: prevention - TB preventive treatment. Section 5.1, Recommended TPT regimens (WHO TB Knowledge Sharing Platform).
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/isoniazid-h-oral-16683911.html): Médecins Sans Frontières. Essential drugs - practical guidelines: Isoniazid (H) oral. Updated June 2021.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=isoniazid#emc-9139): Isoniazid Tablets BP 100 mg - Summary of Product Characteristics. RPH Pharmaceuticals AB. Electronic medicines compendium (emc), revised August 2025.
- Dosing source `NTP MOP 2014`: [Philippine NTP Manual of Procedures](https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf): DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 10–15).
- Dosing source `WHO 2024`: [WHO TB guidelines - TB preventive treatment](https://tbksp.who.int/en/node/43): WHO consolidated guidelines on tuberculosis, Module 1: TB preventive treatment, 2nd ed., 2024.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/isoniazid-h-oral-16683911.html): MSF Essential drugs: Isoniazid (H) oral, 2021.
- Dosing source `MSF TB`: [MSF Tuberculosis guideline](https://medicalguidelines.msf.org/en/node/1205): MSF Tuberculosis, Appendix 13: daily dose of TB drugs using fixed-dose combinations, 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=isoniazid#emc-9139): Isoniazid Tablets BP 100 mg - SmPC. RPH Pharmaceuticals AB, 2025.
- Dosing source `PNF`: [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Isoniazid oral 300 mg and 400 mg tablet, 200 mg/5 mL syrup 120 mL; isoniazid+rifampicin 50+75 mg dispersible (pediatric) and 75+150 mg tablet; +ethambutol 75+150+275 mg; isoniazid+rifampicin+pyrazinamide 50+75+150 mg dispersible (pediatric); HRZE 75+150+400+275 mg (List B).
- https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf: NTCP MOP 5th ed 2014: Table 10 Cat I 2HRZE/4HR, Cat Ia 2HRZE/10HR, Cat II 2HRZES/1HRZE/5HRE, Cat IIa 2HRZES/1HRZE/9HRE; Table 11 FDC tablets 30–37 kg 2, 38–54 kg 3, 55–70 kg 4, >70 kg 5 (both phases); Table 13 H adults 5 (4–6) mg/kg not to exceed 400 mg daily, children 10 (10–15) mg/kg not to exceed 300 mg daily; Table 14 newborn <4 weeks refer; IPT for contacts <5 y (TST/CXR rules) and PLHIV without active TB for 6 months; Table 15 peripheral neuropathy -> pyridoxine 50–100 mg treatment, 10 mg prevention; minor GI intolerance -> give at bedtime or with small meals. (WebFetch text stopped before Chapter 4 IPT dosing and Table 18 renal.)
- https://tbksp.who.int/en/node/43: WHO 2024 TPT 2nd ed Sec 1.4: Rec 19 6 or 9 months daily isoniazid, 3HP weekly, or 3HR daily, regardless of HIV status; Rec 20 alternatives 1HP or 4R.
- https://tbksp.who.int/en/node/1271: Operational handbook 5.1: regimen definitions 6H/9H/3HP/1HP/3HR/4R; pregnancy should not exclude TPT, caution with 1HP/3HP in pregnancy; pyridoxine routinely for pregnant/breastfeeding women and infants; protective pyridoxine 10–25 mg/day. (Dose table is an image; not read.)
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/isoniazid-h-oral-16683911.html: MSF isoniazid (June 2021): TB/latent TB daily <30 kg 10 mg/kg (7–15), ≥30 kg and adults 5 mg/kg (4–6), max 300 mg; with weekly rifapentine >2 y <30 kg 20–30 mg/kg, ≥30 kg 900 mg weekly, 3 months; with daily rifapentine ≥13 y 300 mg, 1 month; with rifampicin 3 months; contraindicated severe hepatic impairment; hepatotoxicity risk (alcohol, chronic liver disease, rifampicin, >35 y); neuropathy risk factors; interactions phenytoin, carbamazepine, benzodiazepines, warfarin; pregnancy/breastfeeding not contraindicated, pyridoxine 10 mg mother, 5 mg infant; empty stomach.
- https://medicalguidelines.msf.org/en/node/1205: Children intensive phase HZR 50/150/75: 4–7 kg 1, 8–11 kg 2, 12–13 and 14–15 kg 3, 16–17 and 18–22 kg 4 tablets; continuation HR 50/75: 4–7 kg 1, 8–11 kg 2, 12–14 kg 3.
- https://products.mhra.gov.uk/search/?search=isoniazid#emc-9139: RPH Isoniazid 100 mg SmPC (rev 08/2025): adults 4–5 mg/kg up to 300 mg; up to 10 mg/kg early in TB meningitis; children 10–15 mg/kg from 3 months; contraindicated drug-induced liver disease; stop if AST >3× ULN or bilirubin rises; care in renal impairment, ototoxicity in ESRD; elderly no reduction; care in epilepsy, diabetes; severe skin reactions never restart; interactions diazepam/triazolam, itraconazole (not recommended), ketoconazole, primidone, chlorzoxazone, disulfiram, levodopa, stavudine; undesirable effects agranulocytosis, aplastic/haemolytic anaemia, psychotic disorder, deafness/tinnitus/vertigo, gynaecomastia, pancreatitis, hypoglycaemia, nicotinic acid deficiency.

---

## Ivermectin  (`med_ivermectin`)

**Description (kept)**

Ivermectin binds glutamate-gated chloride channels in invertebrate nerve and muscle cells, causing paralysis and death of the parasite. A single oral dose is effective against scabies mites, strongyloidiasis and onchocerciasis. It does not kill mite eggs, so scabies treatment is repeated after 7-14 days. WHO recommends two-dose ivermectin for mass drug administration where scabies prevalence is 10% or more.

**Description (added)**

In the Philippines it is on the national formulary as 3 mg and 6 mg tablets. It is dosed by body weight (about 200 micrograms/kg for strongyloidiasis and scabies, 150 micrograms/kg for onchocerciasis), and because food increases absorption the US label advises taking it on an empty stomach with water. WHO advises that ivermectin be used to treat COVID-19 only within clinical trials.

**Uses**: 4 kept, 1 added

- NEW: Cutaneous larva migrans (200 micrograms/kg daily for 1–2 days, MSF)

**Side effects**: 4 kept, 4 added

- NEW: Mazzotti reactions in onchocerciasis: itching, fever, rash, joint pain, lymph node swelling, mostly in the first 4 days
- NEW: Tachycardia, peripheral oedema and orthostatic hypotension (onchocerciasis treatment)
- NEW: Raised ALT/AST; hepatitis and raised bilirubin reported after marketing
- NEW: Fatigue (strongyloidiasis treatment, ≤3%)

**Disease links added**

- `covid19`: **avoid**: WHO (2021) recommends ivermectin be used to treat COVID-19 only within clinical trials.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Strongyloidiasis (3 mg tabs: 15–24 kg 1, 25–35 kg 2, 36–50 kg 3, 51–65 kg 4, 66–79 kg 5) | PO | 200 micrograms/kg | Single dose | 1 day | — | Label · FDA US |
| adult | Scabies (ordinary) (Second dose lowers risk of failure) | PO | 200 micrograms/kg | Single dose; repeat after 1 week | 2 doses | — | MSF |
| adult | Crusted scabies (With topical keratolytic and scabicide) | PO | 200 micrograms/kg | 2 doses 1 week apart (more if needed) | — | — | MSF |
| adult | Onchocerciasis (Second dose at 3 months if signs persist; 3 mg tabs: 15–<25 kg 1, 25–<45 kg 2, 45–<65 kg 3, ≥65 kg 4) | PO | 150 micrograms/kg | Single dose | Repeat every 6–12 months | — | MSF |
| adult | Cutaneous larva migrans | PO | 200 micrograms/kg | Once a day | 1–2 days | — | MSF |
| child | Strongyloidiasis / scabies (≥15 kg) (Not under 15 kg; tablets may be crushed) | PO | 200 micrograms/kg | Single dose (scabies: repeat after 1 week) | — | — | MSF |
| child | Onchocerciasis (≥15 kg) (Not under 15 kg) | PO | 150 micrograms/kg | Single dose | Repeat every 6–12 months | — | MSF |

- *hepatic*: No dose adjustment given; the label advises caution in older patients with reduced hepatic function. Raised liver enzymes and hepatitis have been reported. [Label · FDA US]
- *pregnancy*: Should not be used in pregnancy (safety not established). Passes into breast milk in low amounts: treat breastfeeding mothers only when delaying treatment is riskier (US label); MSF lists no contraindication in breastfeeding. [Label · FDA US]
- *administration*: Take on an empty stomach with water (food increases bioavailability). Tablets may be crushed for small children. [Label · FDA US]
- *monitor*: Strongyloidiasis: at least three follow-up stool examinations over 3 months to confirm cure. In people from loiasis-endemic areas assess Loa loa microfilaraemia before treatment. Watch for Mazzotti reactions in onchocerciasis. [Label · FDA US]
- *forms_ph*: 3 mg and 6 mg tablet. [PNF]

**References added**

- [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/ivermectin-oral-16683965.html): Médecins Sans Frontières. Essential drugs - practical guidelines: Ivermectin oral.
- [FDA label (Stromectol)](https://www.accessdata.fda.gov/drugsatfda_docs/label/2009/050742s024s025lbl.pdf): Merck Sharp & Dohme Corp. STROMECTOL (ivermectin) tablets - prescribing information. U.S. Food and Drug Administration; 2009.
- [WHO - ivermectin and COVID-19](https://www.who.int/news-room/feature-stories/detail/who-advises-that-ivermectin-only-be-used-to-treat-covid-19-within-clinical-trials): World Health Organization. WHO advises that ivermectin only be used to treat COVID-19 within clinical trials. 31 March 2021.
- Dosing source `Label · FDA US`: [FDA label (Stromectol)](https://www.accessdata.fda.gov/drugsatfda_docs/label/2009/050742s024s025lbl.pdf): STROMECTOL (ivermectin) tablets - prescribing information. Merck, 2009.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/ivermectin-oral-16683965.html): MSF Essential drugs: Ivermectin oral.
- Dosing source `PNF`: [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Ivermectin oral: 3 mg and 6 mg tablet.
- https://medicalguidelines.msf.org/viewport/EssDr/english/ivermectin-oral-16683965.html: Onchocerciasis 150 micrograms/kg single dose, second dose at 3 months, repeat 6–12 monthly, weight bands 15–<25 kg 1, 25–<45 2, 45–<65 3, ≥65 4 tablets of 3 mg, <15 kg do not give; ordinary scabies 200 micrograms/kg single dose, second dose 1 week later; crusted scabies two doses a week apart with keratolytic + topical scabicide; strongyloidiasis 200 micrograms/kg single; cutaneous larva migrans 200 micrograms/kg daily 1–2 days; pregnancy avoid; breastfeeding no contraindication; empty stomach; tablets may be crushed.
- https://www.accessdata.fda.gov/drugsatfda_docs/label/2009/050742s024s025lbl.pdf: Stromectol label 2009: strongyloidiasis ~200 mcg/kg single dose, ≥3 stool exams over 3 months; onchocerciasis ~150 mcg/kg, retreat as early as 3 months; empty stomach with water, food increases bioavailability; weight bands 15–24 kg 1, 25–35 2, 36–50 3, 51–65 4, 66–79 5; <15 kg not established; not in pregnancy; low amounts in milk; Mazzotti reactions, tachycardia, peripheral oedema, orthostatic hypotension; fatigue; ALT/AST elevation, post-marketing hepatitis and raised bilirubin; caution in older patients with reduced hepatic function; increased INR with warfarin.
- https://www.who.int/news-room/feature-stories/detail/who-advises-that-ivermectin-only-be-used-to-treat-covid-19-within-clinical-trials: 31 March 2021: until more data is available, WHO recommends that ivermectin only be used within clinical trials (for COVID-19).

---

## Loperamide  (`med_loperamide`)

**Description (kept)**

Loperamide is a peripherally acting synthetic mu-opioid receptor agonist that slows intestinal transit and increases anal sphincter tone, reducing stool frequency and volume. At therapeutic doses P-glycoprotein efflux keeps it out of the CNS; at very high doses it crosses the blood-brain barrier and blocks cardiac sodium and potassium channels. It is used for symptomatic control of acute non-specific diarrhea and chronic diarrhea, not as a substitute for rehydration.

**Description (added)**

Systemic bioavailability is only about 0.3% because of extensive first-pass metabolism (mainly CYP3A4 and CYP2C8), and the half-life is about 11 hours; reduced first-pass clearance in liver disease can cause relative overdose. In the Philippines, the PNF lists loperamide only as a 2 mg capsule and flags it as not for children under 12 years; it is not on the WHO essential medicines list, and oral rehydration remains the core treatment of diarrhea.

**Uses**: 4 kept, 2 added

- NEW: Acute episodes of diarrhoea from irritable bowel syndrome in adults 18 years and over, after a doctor's diagnosis (UK label)
- NEW: Persistent diarrhoea in adults with HIV infection, together with rehydration (MSF)

**Side effects**: 7 kept, 8 added

- NEW: Flatulence
- NEW: Headache
- NEW: Urinary retention
- NEW: Miosis
- NEW: Acute pancreatitis
- NEW: Severe skin reactions, incl. Stevens-Johnson syndrome and toxic epidermal necrolysis (rare)
- NEW: Anaphylactic reactions, angioedema and urticaria
- NEW: Overdose can unmask Brugada syndrome

**Precautions**: 7 kept, 3 added

- NEW: Children under 12 years (UK label; PNF note)
- NEW: Situations where slowing peristalsis must be avoided (risk of ileus, megacolon, toxic megacolon)
- NEW: Diarrhoea due to antibiotics (MSF)

**Interactions**: 4 kept, 4 added

- NEW: Ketoconazole: about 5-fold rise in loperamide levels.
- NEW: Itraconazole plus gemfibrozil together: about 13-fold rise in loperamide AUC.
- NEW: Oral desmopressin: possible about 3-fold rise in desmopressin levels.
- NEW: Anticholinergics and other drugs that slow peristalsis: loperamide effect may be enhanced.

**Disease links added**

- `hiv_infection`: **safe**: MSF: used for persistent diarrhoea in adults with HIV with rehydration; UK label: stop at the first sign of abdominal distension in AIDS (toxic megacolon reports)
- `typhoid_fever`: **avoid**: Our inference: the label contraindicates bacterial enterocolitis from invasive organisms such as Salmonella; typhoid is not named

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Acute diarrhoea (Usual 6–8 mg/day; keep rehydrating) | PO | 4 mg, then 2 mg after each loose stool | As needed | Stop if no improvement in 48 h | 12 mg/day | Label · UK SmPC |
| adult | Acute diarrhoea of IBS (18 years and over, diagnosed) (See doctor if episodes persist beyond 2 weeks) | PO | 4 mg, then 2 mg after each loose stool | As needed | Stop if no improvement in 48 h | 12 mg/day | Label · UK SmPC |
| adult | Persistent diarrhoea in HIV infection (With rehydration) | PO | 4 mg, then 2 mg after each loose stool | As needed | By clinical response | 16 mg/day | MSF |
| child | Acute diarrhoea, 12 years and over (Contraindicated under 12 years) | PO | 4 mg, then 2 mg after each loose stool | As needed | Stop if no improvement in 48 h | 12 mg/day | Label · UK SmPC |

- *renal*: No dose adjustment needed. [Label · UK SmPC]
- *hepatic*: No pharmacokinetic data; use with caution, as reduced first-pass metabolism can cause relative overdose and CNS toxicity. [Label · UK SmPC]
- *elderly*: No dose adjustment; fluid and electrolyte replacement is the priority in frail and elderly patients. [Label · UK SmPC]
- *pregnancy*: Avoid in the first trimester if possible (one study suggested a possible moderate rise in hypospadias); may be considered in the second and third trimesters. Not recommended while breastfeeding (UK label); MSF lists no contraindication in pregnancy or breastfeeding. [Label · UK SmPC]
- *administration*: Swallow capsules with liquid. Do not use for long periods before the cause of persistent diarrhoea is found. Overdose: naloxone. [Label · UK SmPC]
- *forms_ph*: Oral: 2 mg capsule (as hydrochloride). PNF note: not for infants and children under 12 years. [PNF]
- *monitor*: Stool frequency and hydration status; stop at constipation, abdominal distension or ileus, and if no improvement after 48 h. Ask about misuse in patients with a drug-abuse history (cardiac toxicity at high doses). [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=loperamide#emc-10420): Loperamide 2 mg Hard Capsules – Summary of Product Characteristics. Milpharm Ltd (PL 16363/0534). Electronic Medicines Compendium (emc), medicines.org.uk.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/loperamide-oral-16684067.html): Médecins Sans Frontières. Essential drugs – practical guidelines: Loperamide oral. MSF Medical Guidelines (updated January 2024).
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `PNF`: [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC – Loperamide 2 mg Hard Capsules](https://products.mhra.gov.uk/search/?search=loperamide#emc-10420): Milpharm Ltd. Loperamide 2 mg Hard Capsules – Summary of Product Characteristics. emc.
- Dosing source `MSF`: [MSF Essential Drugs – Loperamide oral](https://medicalguidelines.msf.org/en/viewport/EssDr/english/loperamide-oral-16684067.html): Médecins Sans Frontières. Essential drugs – practical guidelines: Loperamide oral.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=loperamide#emc-10420: Milpharm loperamide 2 mg SmPC: 4.1 acute diarrhoea ≥12 y, IBS ≥18 y; 4.2 4 mg then 2 mg per loose stool, usual 6–8 mg, max 12 mg/day, <12 contraindicated, no renal/elderly adjustment, hepatic caution; 4.3 incl. avoid peristalsis inhibition; 4.4 48 h stop, AIDS distension, Brugada with overdose, abuse; 4.5 ketoconazole 5-fold, itraconazole+gemfibrozil 13-fold AUC, desmopressin ~3-fold, anticholinergics; 4.6 avoid 1st trimester, hypospadias signal, not in breastfeeding; 4.8 flatulence, headache, urinary retention, miosis, pancreatitis, SJS/TEN, anaphylaxis; 5.2 bioavailability 0.3%, CYP3A4/2C8, t½ ~11 h
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/loperamide-oral-16684067.html: Indication persistent diarrhoea in adults with HIV with rehydration; 4 mg then 2 mg per loose stool, max 16 mg/day; do not give to children; not for bloody diarrhoea, UC, antibiotic diarrhoea; no contraindication in pregnancy/breastfeeding; naloxone for overdose; not on WHO EML
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Loperamide (as hydrochloride) Oral: 2 mg capsule; N.B. not for infants and children less than 12 years old

---

## Losartan  (`med_losartan`)

**Description (kept)**

Losartan selectively blocks the angiotensin II type 1 (AT1) receptor, preventing angiotensin II-mediated vasoconstriction and aldosterone release. This lowers blood pressure and reduces intraglomerular pressure and proteinuria. It is used for hypertension (including with left ventricular hypertrophy) and diabetic nephropathy in type 2 diabetes, and does not cause the bradykinin-related cough typical of ACE inhibitors.

**Description (added)**

Losartan is partly converted to an active carboxylic acid metabolite (E-3174) that is 10–40 times more potent; losartan's half-life is about 2 hours but the metabolite's is 6–9 hours, which allows once-daily dosing, and full blood-pressure effect takes 3–6 weeks. In the Philippine national primary-care hypertension protocol, losartan 50 mg is added to amlodipine 5 mg at step 2 and both are raised (losartan 100 mg, amlodipine 10 mg) at step 3, but it should not be given to women who are or could become pregnant. The PNF lists 50 mg and 100 mg tablets and a losartan + hydrochlorothiazide 50 mg/12.5 mg tablet.

**Uses**: 3 kept, 2 added

- NEW: Chronic heart failure (LVEF ≤40%) when ACE inhibitors are unsuitable, e.g. because of cough (UK label)
- NEW: Hypertension in children and adolescents aged 6–18 years

**Side effects**: 8 kept, 6 added

- NEW: Vertigo
- NEW: Anaemia (heart failure trials)
- NEW: Hypoglycaemia (diabetic renal disease trials)
- NEW: Intestinal angioedema (abdominal pain, vomiting, diarrhoea)
- NEW: Hepatitis and raised ALT (rare)
- NEW: Thrombocytopenia, hyponatraemia, pancreatitis, rhabdomyolysis (frequency not known)

**Precautions**: 3 kept, 3 added

- NEW: Severe hepatic impairment
- NEW: Co-administration with aliskiren when GFR is under 60 mL/min/1.73 m²
- NEW: Primary hyperaldosteronism: not recommended (precaution)

**Interactions**: 4 kept, 5 added

- NEW: Fluconazole (CYP2C9 inhibitor): about 50% lower active-metabolite exposure.
- NEW: Rifampicin (CYP2C9 inducer): about 40% lower active-metabolite levels.
- NEW: Trimethoprim (incl. co-trimoxazole) and heparin: hyperkalaemia.
- NEW: Tricyclic antidepressants, antipsychotics, baclofen, amifostine: added hypotension.
- NEW: Grapefruit juice: may lower active-metabolite levels; avoid.

**Disease links added**

- `acute_gastroenteritis`: **caution**: UK label: correct volume/sodium depletion first or start lower; check renal function with fever or dehydration
- `acute_coronary_syndrome`: **caution**: UK label: in coronary disease an excessive fall in blood pressure could cause myocardial infarction

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Hypertension (PH protocol step 2, with amlodipine 5 mg) (Recheck BP after 1 month) | PO | 50 mg | Once a day | Long-term | — | PH HTN protocol |
| adult | Hypertension (PH protocol step 3, with amlodipine 10 mg) (Step 4: add HCTZ 25 mg or refer) | PO | 100 mg | Once a day | Long-term | 100 mg/day | PH HTN protocol |
| adult | Hypertension (Full effect in 3–6 weeks; 25 mg if volume depleted or over 75 y) | PO | 50 mg | Once a day | Long-term | 100 mg/day | Label · UK SmPC |
| adult | Chronic heart failure (start) (12.5 → 25 → 50 → 100 mg weekly as tolerated) | PO | 12.5 mg | Once a day | Titrate weekly | 150 mg/day | Label · UK SmPC |
| adult | Hypertensive LVH (stroke risk reduction) (Add low-dose HCTZ and/or raise to 100 mg) | PO | 50 mg | Once a day | Long-term | 100 mg/day | Label · UK SmPC |
| child | Hypertension, 6–18 y, >20 to <50 kg (Up to 50 mg only exceptionally) | PO | 25 mg | Once a day | Long-term | 50 mg/day | Label · UK SmPC |
| child | Hypertension, 6–18 y, ≥50 kg (Up to 100 mg only exceptionally) | PO | 50 mg | Once a day | Long-term | 100 mg/day | Label · UK SmPC |
| child | Hypertension, 6 y and over (weight-based) (>1.4 mg/kg or >100 mg/day not studied; not under 6 y or eGFR <30) | PO | 0.7 mg/kg | Once a day | Long-term | 50 mg start | Label · US |

- *renal*: No initial dose adjustment, including haemodialysis; neither losartan nor its metabolite is removed by dialysis. Not recommended in children with GFR <30 mL/min/1.73 m². [Label · UK SmPC]
- *renal* CrCl 30–50: Monitor potassium and creatinine clearance closely. [Label · UK SmPC]
- *hepatic*: Plasma levels are much higher in cirrhosis (about 5-fold): use a lower dose if there is a history of hepatic impairment; contraindicated in severe impairment; not recommended in children with hepatic impairment. [Label · UK SmPC]
- *elderly*: Usually no adjustment; consider 25 mg to start in those over 75 years. [Label · UK SmPC]
- *pregnancy*: Do not start in pregnancy; not recommended in the first trimester, contraindicated in the second and third. PH protocol: do not give to women who are or could become pregnant. Not recommended while breastfeeding. [Label · UK SmPC]
- *administration*: Swallow whole with water, with or without food. In the PH protocol amlodipine and losartan are taken together, and adherence is confirmed before stepping up. [PH HTN protocol]
- *forms_ph*: Oral: 50 mg and 100 mg tablet (as potassium salt); losartan 50 mg + hydrochlorothiazide 12.5 mg tablet. [PNF]
- *monitor*: BP monthly while titrating (target <130/80 if diabetes, CKD, prior MI or stroke); serum potassium and creatinine, especially in heart failure, renal impairment, diabetes and during fever or dehydration. [PH HTN protocol]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=losartan#emc-7061): Losartan potassium 50 mg film-coated tablets – Summary of Product Characteristics. Milpharm Ltd (PL 16363/0421). Electronic Medicines Compendium (emc), medicines.org.uk.
- [Philippine hypertension protocol](https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf): National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Hosted by Resolve to Save Lives, 2023.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `PNF`: [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.
- Dosing source `PH HTN protocol`: [Philippine primary-care hypertension protocol](https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf): National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives, 2023.
- Dosing source `Label · UK SmPC`: [UK SmPC – Losartan potassium 50 mg film-coated tablets](https://products.mhra.gov.uk/search/?search=losartan#emc-7061): Milpharm Ltd. Losartan potassium 50 mg film-coated tablets – Summary of Product Characteristics. emc.
- Dosing source `Label · US`: [COZAAR (losartan potassium) – US prescribing information](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9949448f-c3b9-44ee-94ed-c1aca8c90f39): COZAAR (losartan potassium) tablets. Prescribing information. DailyMed.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=losartan#emc-7061: Milpharm losartan 50 mg SmPC: 4.1 HF LVEF ≤40% when ACEi unsuitable, children 6–18; 4.2 HTN 50→100 mg, effect 3–6 wk; HF 12.5 mg weekly titration to max 150 mg; LVH 50 mg + HCTZ/100 mg; volume depletion 25 mg; renal/HD no adjustment; hepatic lower dose, contraindicated severe; children 25 mg (>20–<50 kg, max 50) and 50 mg (≥50 kg, max 100); >75 y consider 25 mg; 4.3 aliskiren with diabetes or GFR<60, severe hepatic; 4.4 primary hyperaldosteronism, coronary disease, volume depletion, fever/dehydration renal monitoring, CrCl 30–50 K monitoring; 4.5 fluconazole −50%, rifampicin −40%, trimethoprim, heparin, TCAs/antipsychotics/baclofen/amifostine, grapefruit; 4.6; 4.8 vertigo, anaemia, hypoglycaemia, intestinal angioedema, hepatitis, thrombocytopenia, hyponatraemia, pancreatitis, rhabdomyolysis; 5.2 E-3174 10–40× potency, t½ 2 h / 6–9 h, cirrhosis ~5×, not dialysed
- https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf: National Protocol for Hypertension Management in Primary Health Care Settings: step 1 amlodipine 5 mg; step 2 add losartan 50 mg; step 3 amlodipine 10 mg + losartan 100 mg; step 4 add HCTZ 25 mg or refer; recheck after 1 month; target <130/80 for high-risk; losartan not for women who are or could become pregnant; take together. Issuer/date not printed on the page; no K/creatinine instructions
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Losartan (as potassium salt) Oral: 50 mg and 100 mg tablet; Losartan + Hydrochlorothiazide 50 mg + 12.5 mg tablet
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9949448f-c3b9-44ee-94ed-c1aca8c90f39: COZAAR label: pediatric ≥6 y start 0.7 mg/kg once daily (up to 50 mg); >1.4 mg/kg or >100 mg not studied; not <6 y or eGFR <30 (used only as a dose-table source; already in refs)

---

## Mefenamic Acid  (`med_mefenamic_acid`)

**Description (kept)**

Mefenamic acid is an anthranilic acid (fenamate) NSAID that inhibits cyclooxygenase and prostaglandin synthesis. It is used for short-term relief of mild-to-moderate pain and for primary dysmenorrhea.

**Description (added)**

It is metabolised mainly by hepatic CYP2C9 and has a short plasma half-life of about 2 hours, so it is given three times a day; besides pain it is also used for menorrhagia and, in other countries, arthritis. In the Philippines it is widely available (PNF: 250 mg and 500 mg tablets/capsules), but PhilHealth's dengue quality standards state that NSAIDs are not recommended in dengue and that paracetamol is the drug for fever.

**Uses**: 2 kept, 3 added

- NEW: Rheumatoid arthritis (including Still's disease) and osteoarthritis (UK label)
- NEW: Menorrhagia from dysfunctional causes or an IUD, after other pelvic pathology is excluded
- NEW: Dental, traumatic, muscular, post-operative and post-partum pain; headache

**Side effects**: 7 kept, 9 added

- NEW: Diarrhoea that can be severe, with proctocolitis: stop and do not re-use
- NEW: Reversible haemolytic anaemia
- NEW: Agranulocytosis, aplastic anaemia, thrombocytopenia (rare)
- NEW: Stevens-Johnson syndrome and toxic epidermal necrolysis
- NEW: Aseptic meningitis (higher risk in SLE or mixed connective tissue disease)
- NEW: Convulsions (especially in overdose)
- NEW: Interstitial nephritis and renal papillary necrosis
- NEW: Reversible loss of colour vision
- NEW: False-positive urine bile test

**Precautions**: 3 kept, 5 added

- NEW: Inflammatory bowel disease
- NEW: History of GI bleeding or perforation with previous NSAIDs
- NEW: Active or recurrent peptic ulcer or haemorrhage
- NEW: Severe heart, liver or kidney failure
- NEW: Third trimester of pregnancy

**Interactions**: 5 kept, 7 added

- NEW: Corticosteroids: increased GI ulceration and bleeding.
- NEW: Sulfonylureas: longer half-life and more hypoglycaemia.
- NEW: Ciclosporin, tacrolimus and aminoglycosides: increased nephrotoxicity (aminoglycoside levels rise).
- NEW: Digoxin and other cardiac glycosides: higher glycoside levels and worse heart failure.
- NEW: Quinolone antibiotics: increased convulsion risk.
- NEW: Mifepristone: avoid NSAIDs for 8–12 days after.
- NEW: Zidovudine: increased haematological toxicity.

**Disease links added**

- `migraine`: **caution**: UK label lists headache of most causes as an indication, but warns that frequent painkiller use causes medication-overuse headache
- `type2_diabetes`: **caution**: UK label: prolongs sulfonylurea action (hypoglycaemia) and can cause glucose intolerance in diabetics
- `acute_gastroenteritis`: **caution**: UK label: higher risk of renal failure with dehydration; can itself cause diarrhoea (stop if it occurs)

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Pain; rheumatoid arthritis and osteoarthritis (With or after food) | PO | 500 mg | 3× a day | Shortest possible | 1500 mg/day | Label · UK SmPC |
| adult | Primary dysmenorrhoea | PO | 500 mg | 3× a day | From onset of pain | 1500 mg/day | Label · UK SmPC |
| adult | Menorrhagia (Investigate if no response) | PO | 500 mg | 3× a day | From first day of heavy bleeding | 1500 mg/day | Label · UK SmPC |
| child | Pain or fever, over 6 months (Fever: use paracetamol if dengue possible) | PO | 25 mg/kg/day ÷ 3 | Up to 3× a day | Max 7 days | — | Label · UK SmPC susp |
| child | 6 months to <2 years (50 mg/5 mL suspension) | PO | 50 mg (5 mL) | Up to 3× a day | Max 7 days | 150 mg/day | Label · UK SmPC susp |
| child | 2 to <5 years | PO | 100 mg (10 mL) | Up to 3× a day | Max 7 days | 300 mg/day | Label · UK SmPC susp |
| child | 5 to <9 years | PO | 150 mg (15 mL) | Up to 3× a day | Max 7 days | 450 mg/day | Label · UK SmPC susp |
| child | 9 to 12 years (Longer only in Still's disease) | PO | 200 mg (20 mL) | Up to 3× a day | Max 7 days | 600 mg/day | Label · UK SmPC susp |

- *renal*: Contraindicated in severe renal failure; caution in renal disease, dehydration, diuretic use and old age; monitor renal function. Haemodialysis removes little drug. [Label · UK SmPC]
- *hepatic*: Contraindicated in hepatic failure; check liver function on prolonged therapy and stop if dysfunction appears. [Label · UK SmPC]
- *elderly*: Same dose as adults but lowest effective dose for the shortest time, with monitoring for GI bleeding (more often fatal in the elderly). [Label · UK SmPC]
- *pregnancy*: Avoid in the first and second trimesters unless clearly needed (low dose, short course); from week 20 can cause oligohydramnios and ductus constriction; contraindicated in the third trimester. Do not use while breastfeeding. May impair female fertility. [Label · UK SmPC]
- *administration*: Take with or after food. Use caution in CYP2C9 poor metabolisers and in epilepsy; avoid alcohol. [Label · UK SmPC]
- *forms_ph*: Oral: 250 mg and 500 mg tablet/capsule. [PNF]
- *monitor*: On prolonged use: blood count (haemolytic anaemia, dyscrasias), liver function, renal function, rash and diarrhoea — stop if any occur. Check for dengue before giving for fever in the Philippines. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-12891): Mefenamic Acid 500 mg Tablets – Summary of Product Characteristics. Chemidex Pharma Ltd (PL 17736/0005). Electronic Medicines Compendium (emc), medicines.org.uk.
- [UK SmPC (emc) – suspension](https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-13316): Mefenamic Acid 50 mg/5 ml Suspension – Summary of Product Characteristics. Chemidex Pharma Ltd (PL 17736/0146). emc.
- [PhilHealth dengue quality standards](https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf): PhilHealth. Quality Standards on the Diagnosis and Management of Dengue (Adult and Children) as a Reference of the Corporation. PhilHealth Circular 2026-0009.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `PNF`: [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC – Mefenamic Acid 500 mg Tablets](https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-12891): Chemidex Pharma Ltd. Mefenamic Acid 500 mg Tablets – Summary of Product Characteristics. emc.
- Dosing source `Label · UK SmPC susp`: [UK SmPC – Mefenamic Acid 50 mg/5 ml Suspension](https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-13316): Chemidex Pharma Ltd. Mefenamic Acid 50 mg/5 ml Suspension – Summary of Product Characteristics. emc.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-12891: Chemidex mefenamic 500 mg SmPC: 4.1 RA/OA, pain types, dysmenorrhoea, menorrhagia; 4.2 500 mg TDS with food, elderly lowest dose; 4.3 IBD, prior NSAID GI bleed, active/recurrent PU, severe heart/liver/renal failure, 3rd trimester; 4.4 diarrhoea/proctocolitis, haemolytic anaemia, monitoring LFT/blood/rash, SLE aseptic meningitis, fertility, epilepsy, medication-overuse headache, CYP2C9 poor metabolisers, dehydration renal risk; 4.5 corticosteroids, aminoglycosides, glycosides, ciclosporin/tacrolimus, sulfonylureas, mifepristone 8–12 d, quinolones, zidovudine; 4.6 week 20 oligohydramnios, no breastfeeding; 4.8 colour vision, interstitial nephritis, papillary necrosis, glucose intolerance, urine bile test; 5.2 CYP2C9, t½ ~2 h, HD of little value
- https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-13316: Chemidex suspension 50 mg/5 ml SmPC: infants >6 mo 25 mg/kg/day divided; 6 mo–<2 y 5 ml, 2–<5 y 10 ml, 5–<9 y 15 ml, 9–12 y 20 ml; up to 3× daily; max 7 days except Still's; pyrexia in children indication
- https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf: PhilHealth 'Quality Standards on the Diagnosis and Management of Dengue (Adult and Children)': V.D.2.d use of NSAIDs (ibuprofen, celecoxib, aspirin) not recommended; V.D.2.c paracetamol for fever in adults and children. Mefenamic acid not named; circular number/date garbled in text (number taken from URL)
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Mefenamic Acid Oral: 250 mg and 500 mg tablet/capsule

---

## Metformin  (`med_metformin`)

**Description (kept)**

Metformin lowers blood glucose mainly by decreasing hepatic gluconeogenesis, and also reduces intestinal glucose absorption and improves peripheral insulin sensitivity. It does not stimulate insulin secretion, so it rarely causes hypoglycemia alone and is weight-neutral. It is the usual first-line oral agent for type 2 diabetes.

**Description (added)**

In the Philippines it is listed in the PNF Essential Medicines List as 500 mg tablets/film-coated tablets and 850 mg tablets, and it has been on the WHO Model List of Essential Medicines since 1997. In the UKPDS, overweight patients started on metformin after diet failure had fewer diabetes-related complications, lower diabetes-related and all-cause mortality, and fewer myocardial infarctions than those on diet alone. It is not metabolised and is excreted unchanged in the urine (half-life about 6.5 h), so clearance falls in step with kidney function.

**Uses**: 2 kept, 1 added

- NEW: Type 2 diabetes in combination with insulin (adults)

**Side effects**: 5 kept, 2 added

- NEW: Abnormal liver tests or hepatitis (very rare; resolves on stopping)
- NEW: Skin reactions: erythema, pruritus, urticaria (very rare)

**Precautions**: 3 kept, 5 added

- NEW: Diabetic pre-coma
- NEW: Acute conditions that can affect kidney function: dehydration, severe infection, shock
- NEW: Conditions causing tissue hypoxia: decompensated heart failure, respiratory failure, recent myocardial infarction
- NEW: Hepatic insufficiency, acute alcohol intoxication, alcoholism
- NEW: Not recommended in mitochondrial disease (MELAS, MIDD)

**Interactions**: 5 kept, 4 added

- NEW: NSAIDs (incl. COX-2 inhibitors), ACE inhibitors, ARBs and diuretics (especially loop): may impair kidney function; monitor renal function.
- NEW: Glucocorticoids, sympathomimetics (e.g., salbutamol), hydrochlorothiazide, chlorpromazine: raise blood glucose; check glucose more often and adjust dose.
- NEW: Verapamil (OCT1 inhibitor) may reduce metformin efficacy; rifampicin (OCT1 inducer) may increase its absorption and effect.
- NEW: Trimethoprim, isavuconazole, crizotinib, olaparib: may raise metformin levels or alter its renal elimination.

**Disease links added**

- `heart_failure`: **caution**: Can be used in stable chronic heart failure with regular monitoring of heart and kidney function; contraindicated in acute or unstable (decompensated) heart failure.
- `acute_coronary_syndrome`: **avoid**: Recent myocardial infarction is a contraindication (tissue hypoxia raises lactic acidosis risk).
- `acute_gastroenteritis`: **caution**: Dehydration is a contraindication in the label; withholding metformin during gastroenteritis with significant dehydration is an inference from this, not a direct label statement.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Type 2 diabetes (IR tablet) (With or after meals; adjust after 10–15 days by blood glucose) | PO | 500 mg or 850 mg | 2–3× a day | Long-term | 3 g/day | Label · UK SmPC |
| adult | Type 2 diabetes (IR tablet, MSF schedule) (Week 2: 500 mg 2× a day; then +500 mg/week as needed (1 g morning and evening max)) | PO | 500 mg, then 500 mg 2× a day | Once a day (week 1) | Long-term | 2 g/day | MSF |
| adult | Type 2 diabetes (prolonged-release) (With evening meal; +500 mg every 10–15 days; if not controlled at 2000 mg once daily, try 1000 mg 2× a day) | PO | 500 mg | Once a day | Long-term | 2000 mg/day | Label · UK SmPC PR |
| child | Type 2 diabetes, 10 years and older (IR tablet) (Above starting dose give in 2–3 divided doses; PR tablets not for children) | PO | 500 mg or 850 mg | Once a day | Long-term | 2 g/day | Label · UK SmPC |

- *renal* GFR 60–89: Max 3 g/day (IR) or 2000 mg/day (PR); consider dose reduction as function declines. [Label · UK SmPC]
- *renal* GFR 45–59: Max 2 g/day; review lactic acidosis risk factors before starting; starting dose at most half the maximum. [Label · UK SmPC]
- *renal* GFR 30–44: Max 1 g/day (MSF: max 1 g/day in moderate renal impairment). [Label · UK SmPC]
- *renal* GFR <30: Contraindicated. [Label · UK SmPC]
- *hepatic*: Hepatic insufficiency is a contraindication; no separate hepatic dosing is given. [Label · UK SmPC]
- *elderly*: Base the dose on kidney function; check GFR every 3–6 months. [Label · UK SmPC]
- *pregnancy*: Crosses the placenta; data from more than 1,000 exposed pregnancies show no rise in malformations, so it may be considered as add-on or alternative to insulin (UK SmPC), although MSF names insulin the drug of choice in pregnancy. Breastfeeding: excreted in milk; UK SmPC advises against it because data are limited, while MSF lists no contraindication. [Label · UK SmPC]
- *administration*: Take with or after meals and titrate slowly (dividing doses 2–3× a day reduces GI upset). Stop at the time of surgery under general, spinal or epidural anaesthesia and restart no earlier than 48 h after, once kidney function is stable. Switching IR to PR: same total daily dose; not advised above 2000 mg/day. [Label · UK SmPC]
- *forms_ph*: Metformin (as hydrochloride) 500 mg oral tablet/film-coated tablet; 850 mg oral tablet. [PNF]
- *monitor*: GFR before starting and at least yearly (every 3–6 months if at risk or elderly); vitamin B12 if anaemia or neuropathy; if symptoms suggest lactic acidosis, stop metformin and seek urgent care. Use particular caution in children aged 10–12 (few trial data). Overdose: lactic acidosis is an emergency; haemodialysis removes lactate and metformin. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metformin#emc-15731): Metformin 500 mg Tablets. Summary of Product Characteristics. Medley Pharma Ltd. electronic medicines compendium (emc); text revised 04/2025.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metformin#emc-5263): Metformin hydrochloride 500 mg prolonged release tablets. Summary of Product Characteristics. Genus Pharmaceuticals (STADA). emc; text revised 04/2025.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/metformin-oral-27983919.html): Médecins Sans Frontières. Metformin oral. In: Essential Drugs – practical guidelines. MSF Medical Guidelines; updated 09/2023.
- [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.
- [WHO Model List of Essential Medicines](https://list.essentialmeds.org/medicines/191): World Health Organization. eEML – Electronic Essential Medicines List: Metformin (first added 1997, TRS 882).
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metformin#emc-15731): Metformin 500 mg Tablets SmPC, Medley Pharma Ltd; text revised 04/2025.
- Dosing source `Label · UK SmPC PR`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metformin#emc-5263): Metformin hydrochloride 500 mg prolonged release tablets SmPC, Genus Pharmaceuticals (STADA); text revised 04/2025.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/metformin-oral-27983919.html): Médecins Sans Frontières. Metformin oral. Essential Drugs – practical guidelines; updated 09/2023.
- Dosing source `PNF`: [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): PNF Essential Medicines List, 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF-EML lists 'Metformin (as hydrochloride) Oral: 500 mg tablet/film coated tablet, 850 mg tablet'.
- https://products.mhra.gov.uk/search/?search=metformin#emc-15731: Metformin 500 mg Tablets SmPC (Medley, rev 15/04/2025): adults 500/850 mg 2–3× daily with/after meals, adjust after 10–15 days, max 3 g/day; children ≥10 y 500/850 mg once daily, max 2 g/day in 2–3 doses; elderly by renal function; GFR bands 60–89 max 3 g, 45–59 max 2 g (start ≤ half), 30–44 max 1 g, <30 contraindicated; GFR yearly, 3–6 monthly if at risk/elderly; contraindications incl. diabetic pre-coma, dehydration/severe infection/shock, decompensated HF, respiratory failure, recent MI, hepatic insufficiency, alcohol intoxication/alcoholism; MELAS/MIDD not recommended; stable chronic HF OK with monitoring; surgery/contrast stop and restart ≥48 h; B12 monitoring; caution age 10–12; interactions NSAIDs/ACEi/ARB/diuretics, glucocorticoids/sympathomimetics, verapamil, rifampicin, OCT2 inhibitors incl. trimethoprim & isavuconazole, crizotinib, olaparib; pregnancy >1000 pregnancies, may be considered; breastfeeding not recommended; ADRs very rare hepatitis/LFT abnormalities, erythema/pruritus/urticaria; overdose haemodialysis; UKPDS outcomes (complications, diabetes mortality, all-cause mortality, MI); excreted unchanged, t½ ~6.5 h.
- https://products.mhra.gov.uk/search/?search=metformin#emc-5263: Metformin 500 mg PR SmPC (STADA, rev 15/04/2025): 500 mg once daily, +500 mg every 10–15 days, max 2000 mg once daily with evening meal; 1000 mg twice daily if inadequate; IR→PR same total dose, not if >2000 mg; with insulin start 500 mg; GFR 60–89 and 45–59 max 2000 mg, 30–44 max 1000 mg, <30 contraindicated; not for children.
- https://medicalguidelines.msf.org/viewport/EssDr/english/metformin-oral-27983919.html: MSF Metformin oral (updated 09/2023): first-line T2D; 500 mg od week 1, 500 mg bd week 2, +500 mg/week to max 2 g/day; contraindicated in ketoacidosis, cardiac/respiratory/hepatic/severe renal impairment; moderate renal impairment max 1 g/day; stop before surgery/iodinated contrast, restart 48 h after renal check; corticosteroids, HCTZ, salbutamol, chlorpromazine raise glucose; insulin drug of choice in pregnancy; breastfeeding no contraindication; 500 mg and 1 g tablets.
- https://list.essentialmeds.org/medicines/191: WHO eEML: metformin, hypoglycaemic agents, oral solid 500 mg, first added 1997 (TRS 882), type 2 diabetes.

---

## Methimazole  (`med_methimazole`)

**Description (kept)**

Methimazole inhibits thyroid peroxidase, blocking the iodination of thyroglobulin and the synthesis of T4 and T3. It does not stop release of hormone already stored, so improvement takes several weeks. It is the preferred antithyroid drug for Graves disease except in the first trimester of pregnancy and in thyroid storm, where propylthiouracil is used.

**Description (added)**

In the Philippines it is listed in the PNF Essential Medicines List as 5 mg and 10 mg tablets, and it was added to the WHO Model List of Essential Medicines in 2019 for thyrotoxicosis. It is the preferred antithyroid drug in children because propylthiouracil has caused severe liver injury in children. It is well absorbed (bioavailability about 93%) with a plasma half-life of 3–5 hours that lengthens in liver or kidney impairment, yet the maintenance dose can be taken once daily.

**Uses**: 3 kept, 1 added

- NEW: Hyperthyroidism in children from 3 years of age (EU label)

**Side effects**: 5 kept, 7 added

- NEW: Aplastic anaemia, thrombocytopenia, leukopenia and pancytopenia
- NEW: Insulin autoimmune syndrome (marked hypoglycaemia, can cause coma)
- NEW: Acute pancreatitis (postmarketing; recurs faster on re-exposure)
- NEW: Hypoprothrombinaemia with bleeding risk
- NEW: Loss or change of taste, hair loss, salivary gland swelling, lymphadenopathy
- NEW: Drug fever, neuritis/polyneuropathy, nephritis (very rare)
- NEW: Hypothyroidism if the dose is too high

**Precautions**: 3 kept, 5 added

- NEW: Severe hypersensitivity to other thionamides (carbimazole, propylthiouracil)
- NEW: Moderate to severe granulocytopenia
- NEW: Pre-existing cholestasis not caused by hyperthyroidism
- NEW: Previous acute pancreatitis after thiamazole or carbimazole
- NEW: Combination with thyroid hormone (levothyroxine) during pregnancy

**Interactions**: 2 kept, 1 added

- NEW: Other drugs known to cause agranulocytosis: use with particular care.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Hyperthyroidism, mild (initial) | PO | 15 mg/day ÷ 3 | Every 8 h | Until euthyroid | — | Label · DailyMed |
| adult | Hyperthyroidism, moderately severe (initial) | PO | 30–40 mg/day ÷ 3 | Every 8 h | Until euthyroid | — | Label · DailyMed |
| adult | Hyperthyroidism, severe (initial) | PO | 60 mg/day ÷ 3 | Every 8 h | Until euthyroid | — | Label · DailyMed |
| adult | Hyperthyroidism (maintenance) (Lower the dose if TSH rises) | PO | 5–15 mg/day | Once a day or divided | Long-term | — | Label · DailyMed |
| adult | Hyperthyroidism, mild (initial) | PO | 10–20 mg/day | Once or 2× a day | Until euthyroid | — | Label · EU SmPC |
| adult | Hyperthyroidism, severe (initial) (Higher start may be needed with large goitre or after iodine exposure) | PO | 30–40 mg/day | Divided doses | Until euthyroid | — | Label · EU SmPC |
| adult | Hyperthyroidism (maintenance) (Morning, with or after breakfast; levothyroxine may be added) | PO | 5–10 mg | Once a day | Long-term | — | Label · EU SmPC |
| child | Hyperthyroidism (initial) (Maintenance about half the initial dose) | PO | 0.4 mg/kg/day ÷ 3 | Every 8 h | Until euthyroid | — | Label · DailyMed |
| child | Hyperthyroidism, 3–17 years (initial) (Not recommended at 2 years or younger) | PO | 0.5 mg/kg/day ÷ 2–3 | 2–3× a day | Until euthyroid | 40 mg/day | Label · EU SmPC |

- *renal*: Half-life is prolonged; individualise the dose, use the lowest effective dose and follow up closely. [Label · EU SmPC]
- *hepatic*: Clearance is reduced; use the lowest possible dose with close monitoring. [Label · EU SmPC]
- *pregnancy*: Women of childbearing potential should use effective contraception. If used in pregnancy, give the lowest effective dose without added thyroid hormone; excess dosing can cause fetal goitre and hypothyroidism. Reported first-trimester defects include aplasia cutis, craniofacial malformations, omphalocele and oesophageal atresia. Breastfeeding: possible at up to 10 mg/day without added thyroid hormone, checking the infant's thyroid function regularly. [Label · EU SmPC]
- *administration*: Swallow with fluid; do not chew (bitter). High starting doses can be spread over the day; give the maintenance dose once in the morning. Do not stop methimazole and continue levothyroxine alone. [Label · EU SmPC]
- *forms_ph*: Methimazole (thiamazole) 5 mg and 10 mg oral tablet. [PNF]
- *monitor*: Blood count before and after starting, and at once if fever, sore throat or mouth ulcers appear (stop if agranulocytosis); liver tests if anorexia, itching or right upper abdominal pain (stop if transaminases exceed 3× the upper limit of normal); TSH and free T4 regularly to avoid hypothyroidism; prothrombin time/INR especially before surgery. (Blood count before/after start from EU SmPC; rest from DailyMed label.)

**References added**

- [DailyMed (US National Library of Medicine)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2185e6e0-7c21-4348-a7b4-d898f50a0184): Methimazole tablets, USP. Prescribing information. Upsher-Smith Laboratories, LLC; revised 12/2023. DailyMed.
- [Swedish Medical Products Agency (Läkemedelsverket)](https://docetp.mpa.se/LMF/Thiamazole%20Uni-Pharma%20tablet%20SmPC_09001bee807a75ba.pdf): Thiamazole Uni-Pharma 5 mg tablets. Summary of Product Characteristics. Uni-Pharma Kleon Tsetis Pharmaceutical Laboratories S.A.; text revised 2022-10-04.
- [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.
- [WHO Model List of Essential Medicines](https://list.essentialmeds.org/medicines/506): World Health Organization. eEML – Electronic Essential Medicines List: Methimazole (first added 2019, TRS 1021).
- Dosing source `Label · DailyMed`: [DailyMed (US National Library of Medicine)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2185e6e0-7c21-4348-a7b4-d898f50a0184): Methimazole tablets, USP. Upsher-Smith Laboratories; revised 12/2023.
- Dosing source `Label · EU SmPC`: [Swedish Medical Products Agency (Läkemedelsverket)](https://docetp.mpa.se/LMF/Thiamazole%20Uni-Pharma%20tablet%20SmPC_09001bee807a75ba.pdf): Thiamazole Uni-Pharma 5 mg tablets SmPC; text revised 2022-10-04.
- Dosing source `PNF`: [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): PNF Essential Medicines List, 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF-EML lists 'Methimazole (thiamazole) Oral: 5 mg and 10 mg tablet'.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2185e6e0-7c21-4348-a7b4-d898f50a0184: Upsher-Smith methimazole label (rev 12/2023): adults initial 15 mg/day mild, 30–40 mg moderately severe, 60 mg severe, in 3 doses ~8 h apart; maintenance 5–15 mg/day; pediatric 0.4 mg/kg/day ÷3, maintenance ~half; agranulocytosis warning; stop if transaminases >3× ULN; hepatotoxicity lower than PTU; TSH/FT4 monitoring; prothrombin time before surgery (hypoprothrombinaemia); vasculitis ANCA-positive; preferred in pediatrics over PTU; ADRs incl. aplastic anaemia, thrombocytopenia, insulin autoimmune syndrome (hypoglycaemic coma), periarteritis, hypoprothrombinaemia, nephritis, loss of taste, hair loss, sialadenopathy, lymphadenopathy, drug fever; postmarketing acute pancreatitis; nursing: monitor mother's thyroid every 1–2 weeks.
- https://docetp.mpa.se/LMF/Thiamazole%20Uni-Pharma%20tablet%20SmPC_09001bee807a75ba.pdf: Thiamazole Uni-Pharma 5 mg SmPC (MPA Sweden, rev 2022-10-04): adults ≥3 y indication; severe 30–40 mg/day divided, mild 10–20 mg/day (1–2 doses), maintenance 5–10 mg/day once in morning; higher start with large goitre/prior iodine; children 3–17 y 0.5 mg/kg/day in 2–3 doses, max 40 mg/day; ≤2 y not recommended; hepatic/renal lowest dose; contraindications: thionamide hypersensitivity, moderate–severe granulocytopenia, pre-existing cholestasis, previous bone marrow damage or pancreatitis after thiamazole/carbimazole, thyroid hormone combination in pregnancy; agranulocytosis 0.3–0.6%, blood count before/after start; pancreatitis recurrence on re-exposure; contraception; don't stop thiamazole and continue levothyroxine alone; malformations list; breastfeeding up to 10 mg/day; ADRs neuritis, polyneuropathy, nephritis, autoimmune insulin syndrome; bioavailability 93%, t½ 3–5 h, longer in hepatic/renal impairment; swallow with fluid, don't chew.
- https://list.essentialmeds.org/medicines/506: WHO eEML: methimazole (thiamazole), thyroid/antithyroid section, oral tablet 5 mg and 10 mg, first added 2019 (TRS 1021), thyrotoxicosis.

---

## Metoprolol  (`med_metoprolol`)

**Description (kept)**

Metoprolol is a relatively cardioselective beta-1 adrenergic receptor antagonist that reduces heart rate, contractility and blood pressure and lowers myocardial oxygen demand. Selectivity is dose-dependent and is lost at higher doses. It is used for hypertension, angina, secondary prevention after myocardial infarction, and (as the succinate extended-release form) heart failure with reduced ejection fraction.

**Description (added)**

Oral bioavailability is about 50% after a single dose, rising to about 70% with repeated dosing; the half-life is short (about 3.5 hours, range 1–9 hours), so the immediate-release tartrate is usually given two or more times a day. It is cleared mainly by hepatic CYP2D6, and poor metabolisers can have several-fold higher blood levels. In the Philippines the PNF Essential Medicines List includes only metoprolol tartrate 50 mg and 100 mg tablets (no extended-release succinate or injection).

**Uses**: 4 kept, 3 added

- NEW: Cardiac arrhythmias, especially supraventricular tachyarrhythmias
- NEW: Adjunct in thyrotoxicosis
- NEW: Migraine prophylaxis

**Side effects**: 7 kept, 8 added

- NEW: Orthostatic hypotension, occasionally with syncope
- NEW: Headache, nausea, vomiting and abdominal pain
- NEW: Nightmares, insomnia or somnolence
- NEW: Raynaud's phenomenon and cold extremities; gangrene in severe peripheral arterial disease (very rare)
- NEW: Visual disturbance, dry eyes, tinnitus
- NEW: Worsening of psoriasis, alopecia, photosensitivity
- NEW: Sexual dysfunction
- NEW: Retroperitoneal fibrosis and Peyronie's disease (frequency not known)

**Precautions**: 7 kept, 6 added

- NEW: Severe asthma or history of severe bronchospasm
- NEW: Severe peripheral arterial disease
- NEW: Untreated phaeochromocytoma
- NEW: Metabolic acidosis
- NEW: Suspected MI with heart rate <45/min or significant first-degree heart block (PR ≥0.24 s)
- NEW: Prinzmetal's (variant) angina: use only with great care (precaution)

**Interactions**: 5 kept, 8 added

- NEW: IV verapamil must never be given to a patient taking metoprolol.
- NEW: Class I antiarrhythmics and amiodarone: added slowing of heart rate and AV conduction.
- NEW: Insulin and sulfonylureas: altered hypoglycaemia risk; warning signs may be masked.
- NEW: NSAIDs (e.g., indometacin): reduce the blood-pressure-lowering effect.
- NEW: Rifampicin and other enzyme inducers: lower metoprolol levels.
- NEW: Bupropion and cimetidine: raise metoprolol levels (CYP2D6 inhibition).
- NEW: Other beta-blockers, including eye drops: additive beta-blockade.
- NEW: Inhalational anaesthetics and lidocaine: additive cardiac depression; tell the anaesthetist.

**Disease links added**

- `chronic_kidney_disease`: **safe**: UK SmPC: dose adjustment usually not needed in renal impairment

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Hypertension (Raise by 100 mg/day at weekly intervals) | PO | 100 mg/day to start | Once a day or ÷ 2 | Long term | 200 mg/day | Label · UK SmPC |
| adult | Hypertension (extended-release succinate) (Adjust at weekly or longer intervals) | PO | 25–100 mg | Once a day | Long term | >400 mg/day not studied | Label · US XL |
| adult | Angina | PO | 50–100 mg | 2–3× a day | Long term | 400 mg/day | Label · UK SmPC |
| adult | Angina (extended-release succinate) (Increase weekly) | PO | 100 mg | Once a day | Long term | >400 mg/day not studied | Label · US XL |
| adult | Arrhythmias | PO | 50 mg | 2–3× a day | Long term | 300 mg/day | Label · UK SmPC |
| adult | Hyperthyroidism (adjunct) (Reduce as euthyroid state is reached) | PO | 50 mg | 4× a day | Until euthyroid | — | Label · UK SmPC |
| adult | Acute MI, early (Coronary care unit; monitor ECG, BP, HR) | IV | 5 mg | Every 2 min × 3 doses | Once (15 mg total) | 15 mg | Label · US IV |
| adult | Acute MI, early (after IV) (Start 15 min after last IV dose; 25 mg if not tolerated) | PO | 50 mg | Every 6 h | 48 h | — | Label · US |
| adult | Acute MI, early (oral only) (Ideally within 12 h of chest pain onset) | PO | 50 mg | Every 6 h | 48 h | — | Label · UK SmPC |
| adult | Post-MI maintenance (US label: 100 mg 2× a day) | PO | 200 mg/day ÷ 2 | 2× a day | ≥3 months | — | Label · UK SmPC |
| adult | Migraine prophylaxis | PO | 100–200 mg/day | Divided doses | Long term | 200 mg/day | Label · UK SmPC |
| adult | Heart failure (extended-release succinate) (Double every 2 weeks to highest tolerated dose) | PO | 25 mg (NYHA II); 12.5 mg (more severe) | Once a day | Long term | 200 mg/day | Label · US XL |
| child | Hypertension, ≥6 y (extended-release succinate) (>2 mg/kg or >200 mg/day not studied; not for <6 y) | PO | 1 mg/kg | Once a day | Long term | 50 mg starting dose | Label · US XL |

- *renal*: Dose adjustment usually not needed. [Label · UK SmPC]
- *hepatic*: Significant liver dysfunction: consider lower doses (levels may rise substantially); start low and titrate gradually. [Label · UK SmPC]
- *elderly*: No special dose needed in healthy older adults; watch for excessive falls in blood pressure or pulse. [Label · UK SmPC]
- *pregnancy*: Avoid unless benefit outweighs risk (may reduce placental perfusion); has been used for hypertension after 20 weeks under close supervision. Stop 2–3 days before delivery if possible. Watch newborns for bradycardia, hypotension and hypoglycaemia. [Label · UK SmPC]
- *pregnancy*: Breastfeeding: small amounts in milk (0.5–2% of maternal weight-adjusted dose); monitor the infant for slow heart rate and listlessness. [Label · US XL]
- *administration*: Tartrate: take with a drink of water; US label advises with or right after meals. [Label · UK SmPC]
- *administration*: Extended-release succinate tablets can be split at the score line but must not be crushed or chewed. [Label · US XL]
- *administration*: Stopping: taper over about 10 days, using 25 mg for the last 6 days. For surgery, if stopping, stop at least 24 h before and tell the anaesthetist. [Label · UK SmPC]
- *administration*: Poor CYP2D6 metabolisers may need lower doses. [Label · UK SmPC]
- *forms_ph*: Metoprolol (as tartrate) tablet 50 mg, 100 mg. [PNF]
- *monitor*: Check pulse and blood pressure at each visit; reduce dose or stop if heart rate falls below 50–55/min. [Label · UK SmPC]
- *monitor*: Diabetics: check blood glucose more often (masked hypoglycaemia, especially with sulfonylureas). Thyrotoxicosis: monitor thyroid and cardiac function. [Label · UK SmPC]
- *monitor*: During IV dosing in MI: continuous ECG, blood pressure and heart rate. [Label · US IV]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metoprolol#emc-12971): Metoprolol Tartrate 25 mg Tablets – Summary of Product Characteristics. Zentiva Pharma UK Limited. Electronic Medicines Compendium (emc), medicines.org.uk; updated August 2026.
- [US FDA label (Drugs@FDA)](https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/019962s050s052lbl.pdf): TOPROL-XL (metoprolol succinate) extended-release tablets. Prescribing information. Revised 03/2023. US Food and Drug Administration.
- [Pfizer labeling (US)](https://labeling.pfizer.com/ShowLabeling.aspx?id=4523): Metoprolol Tartrate Injection, USP, 5 mg/5 mL. Prescribing information. Hospira, Inc.; revised 5/2024.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metoprolol#emc-12971): Metoprolol Tartrate 25 mg Tablets. Summary of Product Characteristics. Zentiva Pharma UK Ltd; 2026.
- Dosing source `Label · US XL`: [US FDA label](https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/019962s050s052lbl.pdf): TOPROL-XL (metoprolol succinate) extended-release tablets. Prescribing information; 03/2023.
- Dosing source `Label · US IV`: [Pfizer labeling (US)](https://labeling.pfizer.com/ShowLabeling.aspx?id=4523): Metoprolol Tartrate Injection, USP. Prescribing information. Hospira, Inc.; 5/2024.
- Dosing source `Label · US`: [DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0283bc9d-6998-493a-824a-d4c85f704111): LOPRESSOR (metoprolol tartrate) tablets. Prescribing information. Validus Pharmaceuticals; 9/2023.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=metoprolol#emc-12971: Zentiva metoprolol tartrate 25 mg SmPC, updated 04-Aug-2026: 4.1 (arrhythmias, thyrotoxicosis adjunct, migraine prophylaxis); 4.2 (HTN 100 mg/day +100 mg weekly to max 200 mg/day; angina 50–100 mg BID/TID; arrhythmias 50 mg BID/TID up to 300 mg/day; hyperthyroidism 50 mg QID; MI 50 mg q6h 48 h within 12 h then 200 mg/day divided ≥3 months; migraine 100–200 mg/day; max 400 mg/day; taper 10 days with 25 mg last 6 days; elderly; hepatic lower doses; renal usually no adjustment; CYP2D6 poor metabolisers; children not recommended; take with water); 4.3 (severe asthma, severe PAD, untreated phaeo, metabolic acidosis, MI first-degree block); 4.4 (Prinzmetal, HR <50–55, diabetes, thyrotoxicosis, anaesthesia stop ≥24 h); 4.5 (IV verapamil never, class I/amiodarone, insulin/SU, NSAIDs/indometacin, rifampicin, bupropion, cimetidine, other beta-blockers incl eye drops, lignocaine, inhalational anaesthetics); 4.6 (avoid; used after 20 weeks; stop 2–3 days before delivery); 4.8 frequencies; 5.2 bioavailability ~50% to ~70%, t½ 3.5 h (1–9 h), CYP2D6 several-fold
- https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/019962s050s052lbl.pdf: Toprol-XL label rev 03/2023: HTN 25–100 mg OD; paediatric ≥6 y 1 mg/kg OD, max initial 50 mg, >2 mg/kg or 200 mg not studied; angina 100 mg OD; HF 25 mg OD (NYHA II) or 12.5 mg OD, double every 2 weeks to 200 mg; scored, do not crush/chew; hepatic start low; 8.1 neonatal hypotension/hypoglycaemia/bradycardia; 8.2 infant dose 0.5–2%, monitor bradycardia/listlessness
- https://labeling.pfizer.com/ShowLabeling.aspx?id=4523: Hospira metoprolol tartrate injection rev 5/2024: three 5 mg IV boluses ~2 min apart in CCU; monitor BP, HR, ECG; MI contraindications HR <45, PR ≥0.24 s, SBP <100
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0283bc9d-6998-493a-824a-d4c85f704111: Lopressor tablets (already in refs; used as dose-table source only): after IV, 50 mg q6h starting 15 min after last IV dose for 48 h, 25 mg if not tolerated; maintenance 100 mg BID ≥3 months; take with or right after meals
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Metoprolol (as tartrate) Oral: 50 mg and 100 mg tablet; no injection or modified-release form; no restriction note

---

## Metronidazole  (`med_metronidazole`)

**Description (kept)**

Metronidazole is a nitroimidazole that enters anaerobic bacteria and protozoa by diffusion and is activated by intracellular reduction to cytotoxic free radicals that break DNA strands, causing cell death. Its antibacterial activity is limited to anaerobes, so in mixed intra-abdominal infections it is combined with an agent active against aerobic gram-negative bacteria.

**Description (added)**

Oral metronidazole is rapidly and almost completely absorbed (peak levels in 20 minutes to 3 hours; half-life about 8.5 hours), so oral and IV routes are equally effective and patients should be switched to tablets as soon as they can swallow. It is also used for surgical prophylaxis against anaerobes and for dental and gum infections. In the Philippines it is on the PNF Essential Medicines List as 250 mg and 500 mg tablets, an oral suspension and a 5 mg/mL IV infusion.

**Uses**: 5 kept, 4 added

- NEW: Prevention of post-operative anaerobic infection (surgical prophylaxis)
- NEW: Anaerobic septicaemia, peritonitis, brain abscess, pneumonia, osteomyelitis and pelvic infections
- NEW: Acute ulcerative gingivitis and acute dental infections
- NEW: Anaerobically infected leg ulcers and pressure sores

**Side effects**: 5 kept, 8 added

- NEW: Dark or brownish urine (harmless)
- NEW: Encephalopathy, subacute cerebellar syndrome, ataxia and seizures (very rare)
- NEW: Optic neuropathy, hearing impairment and tinnitus
- NEW: Hepatitis, jaundice and reversible pancreatitis (very rare)
- NEW: Severe skin reactions: SJS/TEN, AGEP, fixed drug eruption
- NEW: QT prolongation, especially with other QT-prolonging drugs
- NEW: Agranulocytosis, thrombocytopenia and pancytopenia (very rare)
- NEW: Anaphylaxis, angioedema and urticaria (rare)

**Precautions**: 4 kept, 3 added

- NEW: Cockayne syndrome: severe, sometimes fatal liver failure reported; avoid unless no alternative (precaution)
- NEW: Active or chronic severe CNS or peripheral nerve disease: use with caution (precaution)
- NEW: Severe hepatic impairment or hepatic encephalopathy: drug accumulates; reduce the dose (precaution)

**Interactions**: 4 kept, 6 added

- NEW: Phenytoin and phenobarbital: shorten metronidazole half-life to about 3 hours.
- NEW: 5-fluorouracil: reduced clearance and more toxicity.
- NEW: Ciclosporin: raised ciclosporin levels; monitor levels and creatinine.
- NEW: Busulfan: raised busulfan levels, risk of severe toxicity.
- NEW: QT-prolonging drugs: QT prolongation reported in combination.
- NEW: Ergometrine and phenytoin: their plasma levels may rise (MSF).

**Disease links added**

- `peptic_ulcer_disease`: **safe**: Part of H. pylori eradication combination therapy (UK SmPC gives a paediatric H. pylori dose)
- `chronic_kidney_disease`: **safe**: No routine dose change in renal failure, including peritoneal dialysis; removed by haemodialysis, so re-dose right after each session
- `acute_gastroenteritis`: **safe**: Treats parasitic causes of dysentery/diarrhoea (amoebiasis, giardiasis); our note: not for routine watery or viral gastroenteritis

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Anaerobic infection (treatment) | PO | 800 mg first dose, then 400 mg | Every 8 h | About 7 days | — | Label · UK SmPC |
| adult | Anaerobic infection (treatment) (Or 1–1.5 g once a day; switch to PO when able) | IV | 500 mg | Every 8 h | 7–10 days | — | Label · UK IV |
| adult | Surgical prophylaxis (Or 1–1.5 g single dose 30–60 min before surgery) | IV | 500 mg | Before/during/after surgery, then every 8 h | ≤24 h (never >48 h) | — | Label · UK IV |
| adult | Surgical prophylaxis (Then IV/rectal until oral possible) | PO | 400 mg | Every 8 h | 24 h before surgery | — | Label · UK SmPC |
| adult | Trichomoniasis (Or 200 mg 3× a day for 7 days; treat partner) | PO | 400 mg | 2× a day | 5–7 days | — | Label · UK SmPC |
| adult | Bacterial vaginosis (Or 2 g single dose) | PO | 400 mg | 2× a day | 5–7 days | — | Label · UK SmPC |
| adult | Invasive intestinal amoebiasis (MSF: 500 mg 3× a day, 5 days (5–10 days hepatic)) | PO | 800 mg | 3× a day | 5 days | — | Label · UK SmPC |
| adult | Intestinal amoebiasis (less susceptible), chronic amoebic hepatitis | PO | 400 mg | 3× a day | 5–10 days | — | Label · UK SmPC |
| adult | Symptomless amoebic cyst passers | PO | 400–800 mg | 3× a day | 5–10 days | — | Label · UK SmPC |
| adult | Giardiasis (Or 400 mg 3× a day 5 days, or 500 mg 2× a day 7–10 days) | PO | 2 g | Once a day | 3 days | — | Label · UK SmPC |
| adult | Acute ulcerative gingivitis | PO | 200 mg | 3× a day | 3 days | — | Label · UK SmPC |
| adult | Acute dental infection | PO | 200 mg | 3× a day | 3–7 days | — | Label · UK SmPC |
| adult | Infected leg ulcers, pressure sores | PO | 400 mg | 3× a day | 7 days | — | Label · UK SmPC |
| child | Anaerobic infection (8 weeks–12 y) (Or 20–30 mg/kg once a day) | PO | 7.5 mg/kg | Every 8 h | Usually 7 days | 40 mg/kg/day | Label · UK SmPC |
| child | Anaerobic infection (≥1 month) (Infuse over 30 min) | IV | 10 mg/kg | Every 8 h | By indication | 1,500 mg/day | MSF · IV |
| child | Surgical prophylaxis (<12 y) | PO | 20–30 mg/kg | Single dose | 1–2 h before surgery | — | Label · UK SmPC |
| child | Amoebiasis | PO | 15 mg/kg | 3× a day | 5 days (intestinal); 5–10 days (hepatic) | — | MSF |
| child | Giardiasis | PO | 30 mg/kg | Once a day | 3 days | — | MSF |
| child | Trichomoniasis (Or 15–30 mg/kg/day ÷ 2–3) | PO | 40 mg/kg | Single dose | 1 day | 2 g/dose | Label · UK SmPC |
| child | H. pylori eradication (with other drugs) | PO | 20 mg/kg/day ÷ 2 | 2× a day | 7–14 days | 500 mg/dose | Label · UK SmPC |
| neonate | Anaerobic infection (<8 weeks) (Or 7.5 mg/kg every 12 h; check levels in preterm babies) | PO | 15 mg/kg | Once a day | Usually 7 days | — | Label · UK SmPC |
| neonate | Surgical prophylaxis (<40 weeks gestation) | IV | 10 mg/kg | Single dose | Before surgery | — | Label · UK IV |

- *renal*: No routine dose change in renal failure, including peritoneal dialysis. [Label · UK IV]
- *renal* Haemodialysis: Removed by haemodialysis: give the dose again immediately after each session. [Label · UK IV]
- *hepatic*: Advanced hepatic insufficiency or hepatic encephalopathy: drug accumulates (more CNS effects); reduce the dose and monitor serum levels. [Label · UK IV]
- *hepatic*: Severe hepatic impairment: give one third of the total daily dose, once a day. [MSF]
- *elderly*: Usually well tolerated; use caution with high-dose regimens. [Label · UK SmPC]
- *pregnancy*: UK SmPC: give in pregnancy or breastfeeding only if essential; short high-dose regimens not recommended. MSF: no contraindication in pregnancy, but split into smaller doses and avoid prolonged use; passes into breast milk (infant GI upset). [Label · UK SmPC]
- *administration*: Swallow tablets whole with water, during or after a meal. [Label · UK SmPC]
- *administration*: IV: infuse about 5 mL/min (one 100 mL bag over 20–60 min); do not add other drugs to the bag; switch to oral as soon as possible. Contains 13.5 mmol (310 mg) sodium per 100 mL. [Label · UK IV]
- *forms_ph*: Tablet 250 mg, 500 mg; suspension 125 mg base/5 mL (200 mg/5 mL as benzoate), 60 mL; IV infusion 5 mg/mL, 100 mL vial. [PNF]
- *monitor*: Courses longer than 10 days: check white cell count and watch for numbness, tingling, unsteadiness or fits; stop if they appear. [Label · UK SmPC]
- *monitor*: Check INR/prothrombin time with warfarin; lithium, creatinine and electrolytes with lithium; ciclosporin levels if co-prescribed. [Label · UK SmPC]
- *monitor*: Cockayne syndrome: liver tests before, during and after treatment; stop if markedly raised. [Label · UK SmPC]
- *monitor*: Preterm neonates: check serum levels after a few days (accumulation in week one). [Label · UK IV]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metronidazole#emc-12817): Metronidazole Tablets BP 400 mg – Summary of Product Characteristics. Milpharm Limited (PL 16363/0026). Electronic Medicines Compendium (emc), medicines.org.uk; updated April 2025.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metronidazole#emc-1842): Metronidazole 500 mg/100 ml Intravenous Infusion – Summary of Product Characteristics. Baxter Healthcare Ltd. Electronic Medicines Compendium (emc), medicines.org.uk; updated April 2026.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-oral-16684146.html): Médecins Sans Frontières. Essential drugs – Metronidazole oral. medicalguidelines.msf.org.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-injectable-16682959.html): Médecins Sans Frontières. Essential drugs – Metronidazole injectable. medicalguidelines.msf.org.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metronidazole#emc-12817): Metronidazole Tablets BP 400 mg. Summary of Product Characteristics. Milpharm Ltd; 2025.
- Dosing source `Label · UK IV`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=metronidazole#emc-1842): Metronidazole 500 mg/100 ml Intravenous Infusion. Summary of Product Characteristics. Baxter Healthcare Ltd; 2026.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-oral-16684146.html): Médecins Sans Frontières. Essential drugs – Metronidazole oral.
- Dosing source `MSF · IV`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-injectable-16682959.html): Médecins Sans Frontières. Essential drugs – Metronidazole injectable.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=metronidazole#emc-12817: Milpharm 400 mg SmPC, rev 04/2025: 4.1 indications incl. prophylaxis, brain abscess, gingivitis, dental, leg ulcers; 4.2 adult doses (anaerobic 800 mg then 400 mg q8h ~7 d; prophylaxis 400 mg q8h 24 h pre-op; trich 2 g / 200 mg TDS 7 d / 400 mg BID 5–7 d; BV 400 mg BID 5–7 d or 2 g; amoebiasis 800 mg TDS 5 d, 400 mg TDS 5–10 d, cyst passers 400–800 mg TDS 5–10 d; giardiasis 2 g OD 3 d / 400 mg TDS 5 d / 500 mg BID 7–10 d; gingivitis 200 mg TDS 3 d; dental 200 mg TDS 3–7 d; leg ulcers 400 mg TDS 7 d); children anaerobic 20–30 mg/kg/day or 7.5 mg/kg q8h up to 40 mg/kg/day, <8 wk 15 mg/kg OD or 7.5 mg/kg q12h, prophylaxis <12 y 20–30 mg/kg; trich child 40 mg/kg single or 15–30 mg/kg/day ÷2–3 (max text reads '2000 mg/kg dose', taken as 2 g); H. pylori child 20 mg/kg/day max 500 mg BID 7–14 d; elderly caution high dose; with/after meal; 4.3; 4.4 (neuropathy >10 days leucocyte monitoring, CNS disease caution, Cockayne LFTs, SJS/TEN/AGEP, dark urine); 4.5 (phenytoin/phenobarbital t½ ~3 h, 5-FU, ciclosporin, busulfan, QT, warfarin, lithium); 4.6; 4.8 frequencies; 5.2 almost complete absorption, peak 20 min–3 h, t½ 8.5 h, dialysable, used in CRF. Adult/children table columns were garbled, so child age-band tablet doses were not used.
- https://products.mhra.gov.uk/search/?search=metronidazole#emc-1842: Baxter 500 mg/100 mL IV SmPC, updated 16-Apr-2026: infuse ~5 mL/min or 20–60 min; prophylaxis 1–1.5 g single or 500 mg then q8h, ≤24 h never >48 h; treatment 1–1.5 g daily or 500 mg q8h 7–10 d; children doses; neonate <40 wk prophylaxis 10 mg/kg, check levels; elderly caution; renal no adjustment incl PD, re-dose after HD; hepatic reduce dose/monitor; hepatic encephalopathy caution; sodium 13.5 mmol/100 mL
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-oral-16684146.html: Forms 250/500 mg tab, 200 mg/5 mL susp; amoebiasis child 15 mg/kg TDS, adult 500 mg TDS, 5 d intestinal / 5–10 d hepatic; giardiasis child 30 mg/kg OD, adult 2 g OD 3 d; precautions anticoagulants, lithium, phenytoin, ergometrine; severe hepatic impairment one third of daily dose once daily; pregnancy no contraindication, smaller doses, avoid prolonged use; breastfeeding excreted, infant GI upset
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-injectable-16682959.html: 500 mg/100 mL; child ≥1 month 10 mg/kg q8h max 1,500 mg/day; adult 500 mg q8h; infuse over 30 min; no other drugs in the vial; switch to oral asap, routes equally effective
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Metronidazole: Oral 250 mg and 500 mg tablet; 125 mg base/5 mL (200 mg/5 mL as benzoate) suspension, 60 mL; Inj. 5 mg/mL, 100 mL vial (IV infusion); no restriction note

---

