# Medicine review b05: review sheet

Run `037_medicines_review_05.sql` in Supabase after you have checked this. Everything below is ADDED; the existing text stays as it is.

Every link was opened twice: by the research step (to read the fact), and again in Akeso's own browser pane on your computer in the Philippines (to make sure it opens for you, not just from the cloud). See NOTES.md in the batch folder for any link that needs attention.

UK SmPC links open the official MHRA Products search (free) for that medicine: the emc site (medicines.org.uk) now limits free page views for users outside the UK. The citation still names the exact product and PL number to pick.

## Please check (batch 05)

- **PH forms:** the PNF list can only be read up to "M", so medicines after M have no "Forms in the Philippines" panel unless another official source had them. Prednisone and nitrofurantoin come from the PhilHealth Konsulta medicines list; ORS from the PSPGHAN 2026 guideline.
- **Nirmatrelvir-ritonavir, nitrofurantoin:** the research was cut off by a usage limit before the final report. The files pass all checks, but please review them more carefully.
- **ORS:** the table includes 2 zinc rows (MSF: <6 months 10 mg, 6 months–5 years 20 mg a day, 10–14 days).
- **Omeprazole → HIV, *caution*:** from the nelfinavir/atazanavir interactions (inference).
- **Paracetamol:** content only (it already has a table). The links to CKD and hepatitis B (*caution*) are inferred from "care in severe renal/hepatic impairment".
- **Praziquantel:** sources disagree on the youngest age (WHO 2022: from 2 years; WHO PQ label: individual decision under 4). The TB and HIV links are inferred from interactions.
- **Propranolol → COPD, *caution*:** inferred from the bronchospasm contraindication. **→ ACS, *safe*:** post-MI use from day 5–21.


---

## Nirmatrelvir + Ritonavir  (`med_nirmatrelvir_ritonavir`)

**Description (kept)**

Nirmatrelvir inhibits the SARS-CoV-2 main protease (Mpro), preventing viral polyprotein processing and replication. Ritonavir is a strong CYP3A inhibitor with no meaningful SARS-CoV-2 activity that is co-administered to raise nirmatrelvir plasma concentrations. It is used for mild-to-moderate COVID-19 in non-hospitalized patients at high risk of progression, started within 5 days of symptom onset.

**Description (added)**

WHO strongly recommends it for non-severe COVID-19 in patients at highest risk of hospitalisation (such as unvaccinated, older or immunosuppressed people), where it cut hospitalisation by about 85%, but not for lower-risk patients, in whom the benefit was negligible. Because it only works early in the illness, prompt testing is essential to its use.

**Uses**: 1 kept, 1 added

- NEW: Severely immunocompromised patients: a 10-day course may be considered to reduce virological rebound (limited data)

**Side effects**: 7 kept, 3 added

- NEW: Headache, nausea
- NEW: Vomiting, abdominal pain (uncommon)
- NEW: Malaise (rare)

**Precautions**: 3 kept, 5 added

- NEW: Severe hepatic impairment (Child-Pugh C)
- NEW: Co-administration with colchicine (life-threatening and fatal interactions reported)
- NEW: Co-administration with quetiapine, lurasidone, pimozide, triazolam or oral midazolam
- NEW: Co-administration with alfuzosin, ranolazine, ivabradine, eplerenone, finerenone, tolvaptan or ergot derivatives
- NEW: Sildenafil when used for pulmonary arterial hypertension

**Interactions**: 6 kept, 7 added

- NEW: Combined hormonal contraceptives: ethinylestradiol exposure falls about 40%; use barrier/non-hormonal contraception during treatment and for one menstrual cycle after.
- NEW: Sildenafil/tadalafil for erectile dysfunction: limit sildenafil to 25 mg per 48 h and tadalafil to 10 mg per 72 h.
- NEW: Salmeterol: avoid (large rise in exposure).
- NEW: Rivaroxaban: not recommended with ritonavir.
- NEW: Atorvastatin/rosuvastatin: consider pausing; pravastatin or fluvastatin preferred if a statin is needed.
- NEW: Levothyroxine: monitor TSH for at least the first month after starting or stopping ritonavir.
- NEW: Parenteral midazolam: only in an ICU-type setting with close monitoring.

**Disease links added**

- `hiv_infection`: **caution**: Risk of HIV-1 protease inhibitor resistance in uncontrolled or undiagnosed HIV; patients already on ritonavir/cobicistat regimens need no dose change (UK SmPC).
- `gout`: **caution**: Colchicine is contraindicated with it (fatal interactions reported); review gout medicines before starting (UK SmPC).
- `tuberculosis`: **caution**: Contraindicated with rifampicin or rifapentine (loss of antiviral effect, resistance), so patients on rifamycin-based TB treatment should not take it (UK SmPC).
- `heart_failure`: **caution**: Several heart-failure and antiarrhythmic drugs are contraindicated with it (amiodarone, dronedarone, eplerenone, ivabradine, finerenone, tolvaptan); our inference from the SmPC interaction list.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | COVID-19, high risk (eGFR ≥60) (Start within 5 days of symptoms) | PO | Nirmatrelvir 300 mg + ritonavir 100 mg | Every 12 h | 5 days | — | Label · UK SmPC |
| adult | COVID-19, eGFR 30–59 | PO | Nirmatrelvir 150 mg + ritonavir 100 mg | Every 12 h | 5 days | — | Label · UK SmPC |
| adult | COVID-19, eGFR <30 or haemodialysis (Give after dialysis on HD days) | PO | 300/100 mg day 1, then 150/100 mg | Once a day | 5 days | — | Label · UK SmPC |
| adult | COVID-19, severely immunocompromised (May reduce rebound; limited data) | PO | Nirmatrelvir 300 mg + ritonavir 100 mg | Every 12 h | 10 days | — | Label · UK SmPC |

- *renal* eGFR ≥60: No dose adjustment. [Label · UK SmPC]
- *renal* eGFR 30–59: Nirmatrelvir 150 mg + ritonavir 100 mg twice daily for 5 days. [Label · UK SmPC]
- *renal* eGFR <30 / HD: 300/100 mg once on day 1, then 150/100 mg once daily on days 2–5; after haemodialysis on dialysis days. Discard extra tablets in the pack. [Label · UK SmPC]
- *hepatic*: No adjustment in Child-Pugh A or B; contraindicated in Child-Pugh C. Use with caution in pre-existing liver disease or raised liver enzymes. [Label · UK SmPC]
- *elderly*: No dose adjustment. Not established under 18 years. [Label · UK SmPC]
- *pregnancy*: Use in pregnancy only if benefit outweighs risk (limited human data). Stop breastfeeding during treatment and for 48 h after the last dose. [Label · UK SmPC]
- *administration*: Take the 3 tablets together, with or without food; swallow whole, do not chew, break or crush. Missed dose: take if ≤8 h late, otherwise skip. If hospitalised after starting, the 5-day course may be completed. [Label · UK SmPC]
- *monitor*: Review every concomitant medicine (including herbal St John's wort) before and during treatment; stop lovastatin/simvastatin ≥12 h before, during and for 5 days after. [Label · UK SmPC]
- *monitor*: Check tacrolimus/ciclosporin/sirolimus levels closely with specialist input; check INR on warfarin. [Label · UK SmPC]
- *monitor*: Stop at signs of anaphylaxis or severe skin reaction; check liver tests if hepatitis symptoms appear. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=nirmatrelvir#emc-13145): Paxlovid 150 mg/100 mg film-coated tablets. Summary of Product Characteristics. Pfizer Ltd; revised 15 September 2026. electronic medicines compendium (emc).
- [World Health Organization](https://www.who.int/news/item/22-04-2022-who-recommends-highly-successful-covid-19-therapy-and-calls-for-wide-geographical-distribution-and-transparency-from-originator): WHO recommends highly successful COVID-19 therapy and calls for wide geographical distribution and transparency from originator. WHO news release, 22 April 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=nirmatrelvir#emc-13145): Paxlovid 150 mg/100 mg film-coated tablets. Summary of Product Characteristics. Pfizer Ltd; 15 September 2026.
- Dosing source `WHO 2022`: [World Health Organization](https://www.who.int/news/item/22-04-2022-who-recommends-highly-successful-covid-19-therapy-and-calls-for-wide-geographical-distribution-and-transparency-from-originator): WHO recommends highly successful COVID-19 therapy... WHO news release, 22 April 2022.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=nirmatrelvir#emc-13145: Paxlovid UK SmPC revised 15 Sep 2026: 300/100 mg q12h x5 days; eGFR 30–<60 150/100 mg BID; eGFR <30 incl HD 300/100 day 1 then 150/100 daily days 2–5 after dialysis; missed dose 8 h; complete course if hospitalised; 10-day course in severely immunocompromised (limited data); Child-Pugh A/B no adjustment, C contraindicated; elderly no adjustment; <18 not established; swallow whole; contraindicated list incl colchicine, quetiapine, lurasidone, pimozide, alfuzosin, ranolazine, ivabradine, eplerenone, finerenone, tolvaptan, ergots, sildenafil for PAH, triazolam, oral midazolam, amiodarone, dronedarone, rifampicin, rifapentine; HIV-1 PI resistance warning; ethinylestradiol AUC -40% and barrier contraception for one cycle; sildenafil ED 25 mg/48 h, tadalafil 10 mg/72 h; salmeterol avoid; rivaroxaban not recommended; statin advice incl stop simvastatin/lovastatin 12 h before and 5 days after, pravastatin/fluvastatin preferred; levothyroxine TSH; parenteral midazolam ICU; breastfeeding stop for 48 h; AEs: common dysgeusia, headache, diarrhoea, nausea; uncommon vomiting, abdominal pain, hypertension; rare malaise. PH forms not confirmed (PNF text ends at M).
- https://www.who.int/news/item/22-04-2022-who-recommends-highly-successful-covid-19-therapy-and-calls-for-wide-geographical-distribution-and-transparency-from-originator: WHO 22 Apr 2022: strong recommendation for non-severe COVID-19 at highest risk of hospitalisation (unvaccinated, older, immunosuppressed); 85% reduction in hospitalisation; not recommended for lower-risk patients (negligible benefit); prompt testing essential as works only early.

---

## Nitrofurantoin  (`med_nitrofurantoin`)

**Description (kept)**

Nitrofurantoin is reduced by bacterial flavoproteins to reactive intermediates that damage ribosomal proteins, DNA and other macromolecules, giving it multiple targets and low resistance rates. It concentrates in urine with low serum levels and is used for uncomplicated lower urinary tract infection (cystitis), not pyelonephritis.

**Description (added)**

WHO lists it as an Access-group antibiotic and a first-choice option for infectious cystitis, as 50 mg and 100 mg oral solids and a 25 mg/5 mL oral liquid. MSF keeps it for uncomplicated cystitis without fever or flank pain when no other antibiotic can be used.

**Uses**: 2 kept, 1 added

- NEW: Prophylaxis around urological surgery (during the procedure and for 3 days after)

**Side effects**: 7 kept, 7 added

- NEW: Dizziness and drowsiness (avoid driving if affected)
- NEW: Aplastic anaemia (rare), agranulocytosis, thrombocytopenia
- NEW: DRESS and Stevens-Johnson syndrome
- NEW: Benign intracranial hypertension
- NEW: Pancreatitis and interstitial nephritis
- NEW: Psychiatric reactions
- NEW: False-positive urine glucose tests

**Precautions**: 5 kept, 4 added

- NEW: eGFR below 45 mL/min (UK SmPC threshold)
- NEW: G6PD deficiency
- NEW: Acute porphyria
- NEW: Infants under 3 months (UK SmPC)

**Interactions**: 2 kept, 5 added

- NEW: Quinolone antibiotics: antagonise its antibacterial effect.
- NEW: Carbonic anhydrase inhibitors and urine alkalinisers: reduce antibacterial activity.
- NEW: Food or drugs that delay gastric emptying: increase absorption.
- NEW: Aluminium/magnesium hydroxide antacids: separate doses by at least 2 hours.
- NEW: Oral typhoid vaccine: inactivated by antibacterials.

**Disease links added**

- `type2_diabetes`: **caution**: SmPC advises caution in diabetes, which raises the risk of peripheral neuropathy.
- `iron_deficiency_anemia`: **caution**: SmPC advises caution in anaemia (stated for anaemia in general, not iron deficiency specifically).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Acute uncomplicated lower UTI (macrocrystals) | PO | 50 mg | 4× a day | 7 days | — | Label · UK SmPC |
| adult | Severe chronic recurrent UTI (macrocrystals) | PO | 100 mg | 4× a day | 7 days | — | Label · UK SmPC |
| adult | Acute or recurrent lower UTI (prolonged-release, ≥12 y) | PO | 100 mg | 2× a day | 7 days | — | Label · UK SmPC MR |
| adult | Uncomplicated cystitis (100 mg tablet) (Only if no other antibiotic can be used) | PO | 100 mg | Every 8 h | 5–7 days | — | MSF |
| adult | Long-term suppression | PO | 50–100 mg | Once a day | Long-term | — | Label · UK SmPC |
| adult | Surgical prophylaxis (macrocrystals) | PO | 50 mg | 4× a day | Procedure + 3 days | — | Label · UK SmPC |
| adult | Surgical prophylaxis (prolonged-release) | PO | 100 mg | 2× a day | Day of procedure + 3 days | — | Label · UK SmPC MR |
| child | Acute UTI (>3 mo) (Under 25 kg: consider suspension) | PO | 3 mg/kg/day ÷ 4 | 4× a day | 7 days | — | Label · UK SmPC |
| child | Suppression (>3 mo) | PO | 1 mg/kg | Once a day | Long-term | — | Label · UK SmPC |

- *forms_ph*: Nitrofurantoin (as macrocrystals) 50 mg and 100 mg capsules (PhilHealth Konsulta medicines list). [PhilHealth Konsulta]
- *renal* eGFR <45: Contraindicated. [Label · UK SmPC]
- *renal* eGFR 30–44: Short course only, for uncomplicated lower UTI with resistant organisms when benefit outweighs risk. [Label · UK SmPC]
- *hepatic*: Rare but potentially fatal hepatitis; use with caution in liver disease. [Label · UK SmPC]
- *elderly*: Normal adult dose if no significant renal impairment; pulmonary reactions more common in the elderly and with long-term use. [Label · UK SmPC]
- *pregnancy*: Use the lowest effective dose after careful assessment; contraindicated at term (newborn haemolysis). Breastfeeding: avoid if the infant has G6PD or other red-cell enzyme deficiency; MSF advises avoiding in the first month. [Label · UK SmPC]
- *administration*: Take with food or milk (improves absorption). Prolonged-release capsules are not suitable under 12 years. [Label · UK SmPC]
- *monitor*: Check liver tests periodically on long-term treatment. [Label · UK SmPC]
- *monitor*: Stop at first sign of paraesthesia (neuropathy), new cough/dyspnoea (pulmonary reaction) or haemolysis. [Label · UK SmPC]
- *monitor*: Recurrent or severe cases: exclude a surgical cause or a non-functioning kidney. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-428): Macrodantin / Nitrofurantoin 100 mg Capsules, Hard (macrocrystals). Summary of Product Characteristics. Mercury Pharmaceuticals (ADVANZ Pharma); updated August 2025. electronic medicines compendium (emc).
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-15362): Nitrofurantoin Mercury Pharma 100 mg Prolonged-Release Capsules (MacroBID). Summary of Product Characteristics. ADVANZ Pharma; updated August 2025. electronic medicines compendium (emc).
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/nitrofurantoin-oral-16684353.html): Médecins Sans Frontières. Essential drugs – Nitrofurantoin oral. MSF Medical Guidelines.
- [WHO eEML](https://list.essentialmeds.org/medicines/301): World Health Organization. Electronic Essential Medicines List – Nitrofurantoin (Access group antibiotic).
- Dosing source `PhilHealth Konsulta`: [PhilHealth Konsulta medicines list (Annex D2)](https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf): Philippine Health Insurance Corporation. Konsulta package: Certification of Service Delivery Support (Medicines), Annex D2.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-428): Macrodantin / Nitrofurantoin 100 mg Capsules (macrocrystals). SmPC. ADVANZ Pharma; August 2025.
- Dosing source `Label · UK SmPC MR`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-15362): Nitrofurantoin 100 mg Prolonged-Release Capsules (MacroBID). SmPC. ADVANZ Pharma; August 2025.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/nitrofurantoin-oral-16684353.html): Médecins Sans Frontières. Essential drugs – Nitrofurantoin oral.

**What was checked on each page**

- https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf: Konsulta Annex D2 lists the forms in the forms_ph note.
- https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-428: Macrodantin/nitrofurantoin 100 mg macrocrystal capsules SmPC (Aug 2025): adults acute 50 mg QDS 7 d; severe chronic recurrent 100 mg QDS 7 d; suppression 50–100 mg once daily; prophylaxis 50 mg QDS procedure + 3 d; children >3 mo 3 mg/kg/day in 4 doses 7 d, suppression 1 mg/kg daily, <25 kg consider suspension; elderly normal dose; contraindicated eGFR <45, G6PD, acute porphyria, infants <3 mo, term pregnancy; eGFR 30–44 short course; caution in anaemia, diabetes etc.; pulmonary/hepatic/neuropathy warnings and periodic LFTs; false-positive urine glucose; interactions: delayed gastric emptying, magnesium trisilicate, probenecid, carbonic anhydrase inhibitors/urine alkalinisation, quinolones, oral typhoid vaccine; pregnancy lowest dose; breastfeeding infant G6PD; dizziness/drowsiness; AEs aplastic anaemia, agranulocytosis, thrombocytopenia, DRESS, SJS, benign intracranial hypertension, pancreatitis, interstitial nephritis, psychiatric reactions; take with food or milk.
- https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-15362: Nitrofurantoin 100 mg prolonged-release (MacroBID) SmPC (Aug 2025): adults/children >12 y 100 mg BID 7 d; surgical prophylaxis 100 mg BID day of procedure + 3 d; not for <12 y; eGFR <45 contraindicated, 30–44 caution.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/nitrofurantoin-oral-16684353.html: MSF nitrofurantoin oral: 100 mg tablet; uncomplicated cystitis when no other antibiotic; adult 100 mg TDS 5–7 d; contraindicated renal impairment, G6PD; separate from Al/Mg hydroxide antacids by 2 h; avoid last month of pregnancy, avoid breastfeeding first month; take with meals; do not use for prevention.
- https://list.essentialmeds.org/medicines/301: WHO eEML: nitrofurantoin, Access group; oral liquid 25 mg/5 mL; oral solid 50 mg, 100 mg; first choice for infectious cystitis.
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Opened, but WebFetch text ends at 'Multivitamins' (65,922 chars); nitrofurantoin entry not readable, so no forms_ph note.

---

## Omeprazole  (`med_omeprazole`)

**Description (kept)**

Omeprazole irreversibly inhibits the parietal cell H+/K+-ATPase (proton pump), the final step of gastric acid secretion. Onset is within about an hour and acid suppression persists for up to 72 hours because new pumps must be synthesized. It is used for peptic ulcer disease, GERD and erosive esophagitis, Helicobacter pylori eradication regimens and hypersecretory states such as Zollinger-Ellison syndrome.

**Description (added)**

WHO keeps omeprazole on the Essential Medicines List as an antiulcer medicine for GERD, peptic ulcer and gastrointestinal bleeding, in oral (10, 20, 40 mg; oral liquid) and 40 mg IV forms. The UK label also licenses it to treat and prevent NSAID-associated ulcers and, in children from 1 year (at least 10 kg), for reflux oesophagitis.

**Uses**: 4 kept, 3 added

- NEW: Treatment of NSAID-associated gastric and duodenal ulcers, and prevention in at-risk patients (over 60, previous ulcer or upper GI bleed)
- NEW: Children from 1 year and at least 10 kg: reflux oesophagitis and symptomatic GERD
- NEW: Children over 4 years: H. pylori-associated duodenal ulcer (with antibiotics, specialist-supervised)

**Side effects**: 8 kept, 10 added

- NEW: Constipation
- NEW: Dizziness, paraesthesia, somnolence, insomnia
- NEW: Hyponatraemia (rare)
- NEW: Blurred vision and taste disturbance (rare)
- NEW: Hepatitis with or without jaundice (rare); hepatic encephalopathy in pre-existing liver disease (very rare)
- NEW: Microscopic colitis
- NEW: Severe skin reactions: SJS, TEN, DRESS, AGEP
- NEW: Leukopenia, thrombocytopenia (rare); agranulocytosis, pancytopenia (very rare)
- NEW: Gynaecomastia (very rare)
- NEW: Slightly increased risk of Salmonella and Campylobacter gut infections

**Precautions**: 2 kept, 1 added

- NEW: Co-administration with nelfinavir

**Interactions**: 6 kept, 7 added

- NEW: Atazanavir: exposure markedly reduced; not recommended (if unavoidable, atazanavir/ritonavir 400/100 mg and omeprazole no more than 20 mg).
- NEW: Posaconazole, erlotinib, ketoconazole and itraconazole: absorption reduced by the higher gastric pH.
- NEW: Phenytoin, diazepam and cilostazol: levels may rise (CYP2C19); monitor phenytoin in the first 2 weeks and after stopping.
- NEW: Digoxin: bioavailability rises about 10%; take care at high doses in the elderly.
- NEW: Saquinavir/ritonavir: saquinavir levels raised up to about 70%.
- NEW: Voriconazole and clarithromycin: raise omeprazole exposure (voriconazole more than doubles it).
- NEW: Chromogranin A tests: stop omeprazole at least 5 days before testing (falsely raised CgA).

**Disease links added**

- `hiv_infection`: **caution**: Contraindicated with nelfinavir and not recommended with atazanavir (UK SmPC); check the antiretroviral regimen.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Duodenal ulcer | PO | 20 mg | Once a day | 2–4 weeks | 40 mg/day in poor responders | Label · UK SmPC |
| adult | Gastric ulcer | PO | 20 mg | Once a day | 4–8 weeks | 40 mg/day in poor responders | Label · UK SmPC |
| adult | Ulcer relapse prevention (H. pylori-negative or eradication not possible) | PO | 10–20 mg | Once a day | Long-term | 40 mg/day | Label · UK SmPC |
| adult | H. pylori eradication (with clarithromycin + amoxicillin or metronidazole) (Choose antibiotics by local resistance; repeat if still positive) | PO | 20 mg | 2× a day | 7 days | — | Label · UK SmPC |
| adult | NSAID-associated ulcer, treatment | PO | 20 mg | Once a day | 4–8 weeks | — | Label · UK SmPC |
| adult | NSAID-associated ulcer, prevention (at-risk) | PO | 20 mg | Once a day | While on NSAID | — | Label · UK SmPC |
| adult | Reflux oesophagitis | PO | 20 mg | Once a day | 4–8 weeks | 40 mg/day if severe | Label · UK SmPC |
| adult | Healed reflux oesophagitis, maintenance | PO | 10 mg | Once a day | Long-term | 20–40 mg/day | Label · UK SmPC |
| adult | Symptomatic GERD (Investigate if not controlled after 4 weeks) | PO | 10–20 mg | Once a day | 4 weeks | — | Label · UK SmPC |
| adult | Zollinger-Ellison syndrome (Split doses above 80 mg/day into 2) | PO | 60 mg initially | Once a day | As needed | Usual 20–120 mg/day | Label · UK SmPC |
| child | Reflux oesophagitis / GERD (≥1 y, 10–20 kg) | PO | 10 mg | Once a day | 4–8 weeks (GERD symptoms 2–4 weeks) | 20 mg/day | Label · UK SmPC |
| child | Reflux oesophagitis / GERD (≥2 y, >20 kg) | PO | 20 mg | Once a day | 4–8 weeks (GERD symptoms 2–4 weeks) | 40 mg/day | Label · UK SmPC |
| child | GERD (<5 kg) (From dispersible 10 mg tablet as 1 mg/mL) | PO | 0.7–1.4 mg/kg | Once a day | 3 days–8 weeks | 2.8 mg/kg/day | MSF |
| child | GERD (5–10 kg) | PO | 5 mg | Once a day | 3 days–8 weeks | — | MSF |
| child | H. pylori duodenal ulcer (>4 y, 15–30 kg) (With amoxicillin 25 mg/kg + clarithromycin 7.5 mg/kg 2× a day) | PO | 10 mg | 2× a day | 7 days (up to 14) | — | Label · UK SmPC |
| child | H. pylori duodenal ulcer (>4 y, 31–40 kg) (With amoxicillin 750 mg + clarithromycin 7.5 mg/kg 2× a day) | PO | 20 mg | 2× a day | 7 days (up to 14) | — | Label · UK SmPC |
| child | H. pylori duodenal ulcer (>4 y, >40 kg) (With amoxicillin 1 g + clarithromycin 500 mg 2× a day) | PO | 20 mg | 2× a day | 7 days (up to 14) | — | Label · UK SmPC |

- *renal*: No dose adjustment needed. [Label · UK SmPC]
- *hepatic*: 10–20 mg daily may be sufficient. [Label · UK SmPC]
- *hepatic* Severe: Severe hepatic impairment: do not exceed 0.7 mg/kg daily (max 20 mg daily). [MSF]
- *elderly*: No dose adjustment needed. [Label · UK SmPC]
- *pregnancy*: Over 1,000 exposed pregnancies showed no adverse effects; can be used in pregnancy. Passes into breast milk but unlikely to affect the infant at therapeutic doses. [Label · UK SmPC]
- *administration*: Take in the morning, swallowed whole with half a glass of water; do not chew or crush. If swallowing is difficult, open the capsule and mix the pellets with water or a slightly acidic liquid (fruit juice, applesauce); take within 30 minutes. [Label · UK SmPC]
- *monitor*: Exclude malignancy first if there are alarm features (weight loss, recurrent vomiting, dysphagia, haematemesis, melaena). [Label · UK SmPC]
- *monitor*: Long-term use (especially beyond 1 year): review regularly; consider magnesium levels (more so with digoxin or diuretics), vitamin B12, and calcium/vitamin D in patients at fracture risk. [Label · UK SmPC]
- *monitor*: Stop if acute tubulointerstitial nephritis is suspected, or if SCLE-type skin lesions with joint pain appear. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=omeprazole#emc-15127): Omeprazole 20 mg gastro-resistant capsules, hard. Summary of Product Characteristics. Zentiva Pharma UK Ltd; revised August 2025. electronic medicines compendium (emc).
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/omeprazole-oral-16684375.html): Médecins Sans Frontières. Essential drugs – Omeprazole oral. MSF Medical Guidelines.
- [WHO eEML](https://list.essentialmeds.org/medicines/178): World Health Organization. Electronic Essential Medicines List – Omeprazole (antiulcer medicines).
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=omeprazole#emc-15127): Omeprazole 20 mg gastro-resistant capsules. SmPC. Zentiva; August 2025.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/omeprazole-oral-16684375.html): Médecins Sans Frontières. Essential drugs – Omeprazole oral.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=omeprazole#emc-15127: Zentiva omeprazole 20 mg capsules SmPC (rev. 29 Aug 2025): indications incl. NSAID ulcers, children ≥1 y ≥10 kg reflux oesophagitis/GERD, >4 y H. pylori DU; all adult doses/durations above; child weight-band doses and H. pylori combos; renal/elderly no adjustment, hepatic 10–20 mg; administration (morning, whole, capsule opening, 30 min); contraindicated with nelfinavir; atazanavir not recommended (max 20 mg); posaconazole/erlotinib/keto-/itraconazole absorption reduced; digoxin +10%; phenytoin monitor 2 weeks; diazepam, cilostazol; saquinavir +70%; voriconazole doubles exposure; CgA stop 5 days; Salmonella/Campylobacter risk; hypomagnesaemia, B12, fractures, SCLE, AIN; AEs constipation, dizziness, paraesthesia, somnolence, insomnia, hyponatraemia, blurred vision, taste disturbance, hepatitis, microscopic colitis, SJS/TEN/DRESS/AGEP, leukopenia, thrombocytopenia, agranulocytosis, gynaecomastia; pregnancy >1,000 outcomes can be used; breastfeeding unlikely to affect infant.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/omeprazole-oral-16684375.html: MSF omeprazole oral: 10 mg dispersible tablet, 20 mg capsule; GORD child <5 kg 0.7–1.4 mg/kg (max 2.8 mg/kg/day), 5–10 kg 5 mg, 10–20 kg 10 mg, >20 kg and adult 20 mg once daily; durations 3 days to 4–8 weeks; severe hepatic impairment max 0.7 mg/kg/day (max 20 mg).
- https://list.essentialmeds.org/medicines/178: WHO eEML omeprazole: antiulcer medicines; oral liquid 1 mg/mL and 4 mg/mL powder, oral solid 10/20/40 mg, 40 mg IV vial; indications GERD, peptic ulcer, GI bleeding; added 2009.
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Read with offset 64000: text covers Midazolam to Moxifloxacin only; omeprazole entry not readable, so no forms_ph note.

---

## Oral Rehydration Salts (reduced osmolarity)  (`med_ors`)

**Description (kept)**

Reduced-osmolarity ORS (245 mOsm/L) contains glucose and sodium in equimolar amounts (75 mmol/L each), exploiting sodium-glucose co-transport in the small intestine to drive water absorption even during secretory diarrhea. It also replaces potassium and corrects acidosis with citrate. Compared with the older standard ORS it reduces stool output, vomiting and the need for unscheduled IV therapy; it is the cornerstone of treatment for dehydration from acute diarrhea.

**Description (added)**

In the Philippines, PhilHealth's quality policy on acute infectious gastroenteritis names ORS and IV fluids as the standard treatment for dehydration, with routine zinc 20 mg/day for 10–14 days as an adjunct in children. The Philippine Society for Pediatric Gastroenterology, Hepatology and Nutrition (PSPGHAN, 2026) recommends WHO low-osmolarity ORS plus zinc for children with no signs of dehydration, and advises against soft drinks, sports drinks and electrolyte drinks that do not meet the WHO low-osmolarity formula. WHO notes that a 10–14 day zinc course shortens a diarrhoea episode by about 25% and cuts stool volume by about 30%.

**Uses**: 2 kept, 1 added

- NEW: Given alongside IV therapy in severe dehydration (WHO Plan C), once the patient is conscious and able to drink

**Precautions**: 3 kept, 1 added

- NEW: Severe acute malnutrition: use ReSoMal (special ORS) under medical supervision instead, except in cholera, where standard ORS is used (MSF)

**Interactions**: 3 kept, 1 added

- NEW: Zinc given with ORS: separate zinc from iron (ferrous) salts by at least 2 hours (MSF).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | No dehydration (Plan A), >10 y and adults | PO | 200–400 mL after each loose stool | After each stool | While diarrhoea lasts | About 2000 mL/day | MSF |
| adult | Moderate dehydration (Plan B), ≥15 y / ≥30 kg (Then Plan A, repeat Plan B, or start IV (Plan C)) | PO | 2200–4000 mL | Over 4 h | 4 h, then reassess | — | MSF |
| adult | Severe dehydration (Plan C), with IV fluids (Only if conscious) | PO | 5 mL/kg/h | Continuous | Reassess after 3 h | — | MSF |
| child | No dehydration (Plan A), <2 y (PSPGHAN: 50–100 mL (¼–½ cup)) | PO | 50–100 mL after each loose stool | After each stool | While diarrhoea lasts | About 500 mL/day | MSF |
| child | No dehydration (Plan A), 2–10 y (PSPGHAN: 100 mL (½ cup)) | PO | 100–200 mL after each loose stool | After each stool | While diarrhoea lasts | About 1000 mL/day | MSF |
| child | No dehydration, >10 y (PH) | PO | As much as tolerated | After each stool | While diarrhoea lasts | — | PSPGHAN 2026 |
| child | Moderate dehydration (Plan B), <4 mo / <5 kg | PO | 200–400 mL | Over 4 h | 4 h, then reassess | — | MSF |
| child | Moderate dehydration (Plan B), 4–11 mo / 5–7.9 kg | PO | 400–600 mL | Over 4 h | 4 h, then reassess | — | MSF |
| child | Moderate dehydration (Plan B), 12–23 mo / 8–10.9 kg | PO | 600–800 mL | Over 4 h | 4 h, then reassess | — | MSF |
| child | Moderate dehydration (Plan B), 2–4 y / 11–15.9 kg | PO | 800–1200 mL | Over 4 h | 4 h, then reassess | — | MSF |
| child | Moderate dehydration (Plan B), 5–14 y / 16–29.9 kg | PO | 1200–2200 mL | Over 4 h | 4 h, then reassess | — | MSF |
| child | Severe dehydration (Plan C), with IV fluids (Only if conscious) | PO | 5 mL/kg/h | Continuous | Reassess after 3 h (6 h in infants) | — | MSF |
| child | Adjunct zinc with ORS, <6 mo (Half a 20 mg dispersible tablet) | PO | 10 mg zinc | Once a day | 10 days | — | MSF zinc |
| child | Adjunct zinc with ORS, 6 mo–5 y (PSPGHAN/PhilHealth: 20 mg/day; PSPGHAN gives 14 days) | PO | 20 mg zinc | Once a day | 10–14 days | — | MSF zinc |

- *forms_ph*: PSPGHAN describes WHO low-osmolarity ORS in the Philippines as flavoured sachets made up with 100 mL, unflavoured or flavoured sachets made up with 200 mL of cool boiled water, and a flavoured ready-to-drink solution. Zinc for diarrhoea: drops 10 mg/mL (2 mL daily) or syrup 20 mg/5 mL (5 mL daily), as a single preparation, not a multivitamin. [PSPGHAN 2026]
- *pregnancy*: No contraindication in pregnancy or breastfeeding. [MSF]
- *administration*: Make up only with the volume of cool boiled water stated for that sachet size (100 mL or 200 mL sachets in PH). [PSPGHAN 2026]
- *administration*: If the child vomits, stop for 10 minutes, then restart with very small, frequent amounts; do not stop rehydration. [MSF]
- *administration*: Continue diet for age and breastfeeding during the episode. [PSPGHAN 2026]
- *administration*: Zinc dispersible tablet: dissolve in a teaspoon of water; repeat the dose if vomited within 30 minutes. Zinc never replaces ORS. [MSF zinc]
- *monitor*: Reassess hydration after 4 hours of Plan B (3 h on Plan C, 6 h in infants) and choose Plan A, B or C again. [MSF]
- *monitor*: Puffy eyelids: stop ORS, give plain water, and resume Plan A once the puffiness settles. [MSF]
- *monitor*: Children with no dehydration: see the doctor again if symptoms persist or do not improve within 3 days. [PSPGHAN 2026]

**References added**

- [PSPGHAN (Philippine Pediatric Society)](https://pps.org.ph/wp-content/uploads/PSPGHAN-GUIDELINES-ON-THE-TREATMENT-OF-ACUTE-GASTROENTERITIS-WITH-NO-SIGNS-OF-DEHYDRATION-April-2026-1.pdf): Philippine Society for Pediatric Gastroenterology, Hepatology and Nutrition. Guidelines for Health Care Professionals on the Treatment of Acute Gastroenteritis with No Signs of Dehydration. April 2026.
- [PhilHealth](https://www.philhealth.gov.ph/circulars/2022/circ2022-0026.pdf): Philippine Health Insurance Corporation. Quality Policy on the Diagnosis and Management of Acute Infectious Gastroenteritis as Reference of the Corporation. PhilHealth Circular 2022-0026.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/oral-rehydration-salts-ors-16684387.html): Médecins Sans Frontières. Essential drugs – Oral rehydration salts (ORS). MSF Medical Guidelines.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/zinc-sulfate-oral-16684806.html): Médecins Sans Frontières. Essential drugs – Zinc sulfate oral. MSF Medical Guidelines.
- [World Health Organization](https://www.who.int/news-room/fact-sheets/detail/diarrhoeal-disease): WHO. Diarrhoeal disease. Fact sheet, 7 March 2024.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/oral-rehydration-salts-ors-16684387.html): Médecins Sans Frontières. Essential drugs – Oral rehydration salts (ORS).
- Dosing source `MSF zinc`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/zinc-sulfate-oral-16684806.html): Médecins Sans Frontières. Essential drugs – Zinc sulfate oral.
- Dosing source `PSPGHAN 2026`: [PSPGHAN (Philippine Pediatric Society)](https://pps.org.ph/wp-content/uploads/PSPGHAN-GUIDELINES-ON-THE-TREATMENT-OF-ACUTE-GASTROENTERITIS-WITH-NO-SIGNS-OF-DEHYDRATION-April-2026-1.pdf): PSPGHAN. Treatment of Acute Gastroenteritis with No Signs of Dehydration. April 2026.
- Dosing source `PhilHealth`: [PhilHealth](https://www.philhealth.gov.ph/circulars/2022/circ2022-0026.pdf): PhilHealth Circular 2022-0026. Quality Policy on Acute Infectious Gastroenteritis.

**What was checked on each page**

- https://medicalguidelines.msf.org/en/viewport/EssDr/english/oral-rehydration-salts-ors-16684387.html: MSF ORS: sachet for 1 L; Plan A per stool <24 mo 50–100 mL (~500 mL/day), 2–10 y 100–200 mL (~1000 mL/day), >10 y and adult 200–400 mL (~2000 mL/day); Plan B 4-h volumes by age/weight (<4 mo 200–400 ... ≥15 y 2200–4000 mL); Plan C ORS 5 mL/kg/h with IV if conscious, reassess 3 h (6 h infants); puffy eyelids and vomiting management; ReSoMal for severe malnutrition except cholera (standard ORS); no contraindication in pregnancy/breastfeeding; use solution within 24 h.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/zinc-sulfate-oral-16684806.html: MSF zinc sulfate: 20 mg dispersible tablet; <6 mo 10 mg, 6 mo–5 y 20 mg once daily for 10 days; dissolve in teaspoon of water; repeat if vomited within 30 min; separate from ferrous salts by 2 h; never replaces ORS.
- https://pps.org.ph/wp-content/uploads/PSPGHAN-GUIDELINES-ON-THE-TREATMENT-OF-ACUTE-GASTROENTERITIS-WITH-NO-SIGNS-OF-DEHYDRATION-April-2026-1.pdf: PSPGHAN (Philippine Pediatric Society component) April 2026, AGE with no signs of dehydration: WHO low-osmolarity ORS; flavoured sachet in 100 mL, unflavoured/flavoured sachet in 200 mL cool boiled water, flavoured ready-to-drink; per stool <2 y 50–100 mL, >2 y 100 mL, >10 y ad libitum; zinc ≥6 mo drops 10 mg/mL 2 mL daily x14 days or syrup 20 mg/5 mL 5 mL daily x14 days, single preparation; avoid carbonated/sports/non-WHO electrolyte drinks; follow up if not improved in 3 days; references 2019 PH CPG on acute infectious diarrhea (with DOH).
- https://www.philhealth.gov.ph/circulars/2022/circ2022-0026.pdf: PhilHealth quality policy on acute infectious gastroenteritis (updates Circular 2016-0001, based on DOH/IDSA): ORS and IV fluids are the standard of treatment for dehydration; IV preferred for severe dehydration in children; zinc 20 mg/day for 10–14 days routinely as adjunct in children (age range garbled in text). Circular number taken from the URL/search title; the number in the PDF text itself was garbled.
- https://www.who.int/news-room/fact-sheets/detail/diarrhoeal-disease: WHO diarrhoeal disease fact sheet (7 March 2024): ORS; 10–14 day zinc course reduces episode duration by 25% and stool volume by 30%; IV for severe dehydration/shock; continue feeding and breastfeeding.
- https://www.who.int/publications/i/item/9241594217: WHO 2006 'Implementing the new recommendations on the clinical management of diarrhoea': new low-osmolarity ORS and zinc for 10–14 days; page does not give zinc mg doses (not used as a ref).
- https://actamedicaphilippina.upm.edu.ph/index.php/acta/article/view/7513: Acta Med Philipp 2024 adherence study: 2019 PH CPG strongly recommends low-osmolarity ORS and zinc; only 52% got ORS (not used as a ref).
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Read with offset 64000: text covers Midazolam to Moxifloxacin only; ORS entry not readable, so the forms_ph note uses PSPGHAN instead of the PNF.

---

## Oseltamivir  (`med_oseltamivir`)

**Description (kept)**

Oseltamivir is an oral prodrug converted to oseltamivir carboxylate, a competitive inhibitor of influenza A and B neuraminidase that prevents release of new virions from infected cells. Started ideally within 48 hours of symptom onset, it shortens illness duration and is recommended for hospitalized and high-risk patients; it is also used for post-exposure prophylaxis.

**Description (added)**

WHO lists oseltamivir on the complementary Essential Medicines List (30, 45 and 75 mg capsules; 6 mg/mL powder for oral liquid for children), limited to severe confirmed or suspected influenza in critically ill hospitalized patients. CDC advises starting it without waiting for test results in hospitalized, severely ill or high-risk patients, and in hospitalized patients even when more than 48 hours have passed since symptom onset. It is the preferred antiviral in pregnancy and does not replace influenza vaccination.

**Uses**: 2 kept, 3 added

- NEW: Treatment of influenza in hospitalized or severe, complicated or progressive illness, even if started more than 48 hours after onset (CDC)
- NEW: Treatment of influenza in infants under 1 year, including full-term neonates
- NEW: Seasonal prophylaxis in exceptional situations (e.g., vaccine-strain mismatch or pandemic); post-exposure prophylaxis in infants under 1 year only during a pandemic (UK SmPC)

**Side effects**: 4 kept, 6 added

- NEW: Vomiting is the most common effect in children; also conjunctivitis, earache, otitis media, cough and nasal congestion
- NEW: Hepatitis, jaundice and hepatic failure (rare, some fatal)
- NEW: Gastrointestinal bleeding (rare)
- NEW: Angioedema
- NEW: Convulsions
- NEW: Thrombocytopenia, visual disturbance and cardiac arrhythmia (listed in the UK SmPC)

**Interactions**: 2 kept, 3 added

- NEW: Probenecid: roughly doubles exposure to the active metabolite; no dose change with normal renal function.
- NEW: Renally excreted drugs with a narrow margin (e.g., chlorpropamide, methotrexate, phenylbutazone): use with caution.
- NEW: No interactions reported with paracetamol, aspirin, cimetidine, antacids, warfarin or amoxicillin.

**Disease links added**

- `chronic_kidney_disease`: **caution**: Dose must be reduced when CrCl is 60 mL/min or less; not recommended at CrCl 10 or below without dialysis (UK SmPC, CDC).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Treatment (≥13 y, >40 kg) (Start within 2 days of onset) | PO | 75 mg | 2× a day | 5 days (10 days if immunocompromised) | — | Label · UK SmPC |
| adult | Post-exposure prophylaxis (Start within 2 days of exposure; CDC: 7 days after last exposure) | PO | 75 mg | Once a day | 10 days | — | Label · UK SmPC |
| adult | Prophylaxis during a community epidemic | PO | 75 mg | Once a day | Up to 6 weeks (12 weeks if immunocompromised) | — | Label · UK SmPC |
| adult | Institutional outbreak prophylaxis | PO | 75 mg | Once a day | ≥2 weeks, until 1 week after last case | — | CDC |
| child | Treatment (≥1 y, ≤15 kg) (UK SmPC band 10–15 kg) | PO | 30 mg | 2× a day | 5 days | — | Label · UK SmPC |
| child | Treatment (≥1 y, >15–23 kg) | PO | 45 mg | 2× a day | 5 days | — | Label · UK SmPC |
| child | Treatment (≥1 y, >23–40 kg) | PO | 60 mg | 2× a day | 5 days | — | Label · UK SmPC |
| child | Treatment (≥1 y, >40 kg) | PO | 75 mg | 2× a day | 5 days | — | Label · UK SmPC |
| child | Prophylaxis (≥1 y) (CDC: 7 days after last exposure) | PO | Same weight-band dose as treatment | Once a day | 10 days | 75 mg | Label · UK SmPC |
| child | Treatment (<1 y) (AAP (via CDC): 3.5 mg/kg for 9–11 months) | PO | 3 mg/kg | 2× a day | 5 days (10 days if immunocompromised) | — | Label · UK SmPC |
| child | Prophylaxis (3 mo to <1 y) (UK: pandemic only; CDC: not under 3 months unless critical) | PO | 3 mg/kg | Once a day | 10 days | — | Label · UK SmPC |
| neonate | Treatment, preterm (PMA <38 wk) (Not licensed below 36 weeks post-conceptual age (UK)) | PO | 1 mg/kg | 2× a day | 5 days | — | CDC |
| neonate | Treatment, preterm (PMA 38–40 wk) | PO | 1.5 mg/kg | 2× a day | 5 days | — | CDC |

- *renal* CrCl 30–60: Treatment 30 mg 2× a day; prophylaxis 30 mg once a day. [Label · UK SmPC]
- *renal* CrCl 10–30: Treatment 30 mg once a day; prophylaxis 30 mg every second day. [Label · UK SmPC]
- *renal* CrCl ≤10: Not recommended (no data) unless on dialysis. [Label · UK SmPC]
- *renal* Haemodialysis: Haemodialysis: treatment 30 mg after each session; prophylaxis 30 mg after every second session. CDC: treatment no longer than 5 days. [Label · UK SmPC]
- *renal* Peritoneal dialysis: Peritoneal dialysis: treatment 30 mg single dose; prophylaxis 30 mg once a week. [Label · UK SmPC]
- *renal* Children: No dosing data for children 12 years and under with renal impairment. [Label · UK SmPC]
- *hepatic*: No dose adjustment needed. [Label · UK SmPC]
- *elderly*: No dose adjustment unless moderate or severe renal impairment. [Label · UK SmPC]
- *pregnancy*: Preferred antiviral in pregnancy, at the same dose as in non-pregnant adults (CDC). Over 1,000 first-trimester exposures showed no malformative toxicity (UK SmPC). Passes into breast milk in small amounts; may be used when there is clear benefit. [CDC]
- *administration*: Can be taken with or without food (food does not change levels); taking it with food may reduce nausea and vomiting. If capsules cannot be swallowed, use the oral suspension; a pharmacy-made 6 mg/mL suspension is preferred, otherwise mix capsule contents with no more than a teaspoon of sweetened food and swallow at once. [Label · UK SmPC]
- *administration*: Critically ill adults: standard doses are adequately absorbed by mouth or feeding tube; doubling to 150 mg 2× a day may not add benefit. Extend beyond 5 days if still severely ill. [CDC]
- *monitor*: Watch behaviour closely, especially in children and adolescents, for neuropsychiatric events (delirium, self-injury, convulsions). [Label · UK SmPC]
- *monitor*: Check creatinine clearance before dosing and adjust for renal function. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=oseltamivir#emc-1194): Tamiflu 30 mg, 45 mg and 75 mg hard capsules. Summary of Product Characteristics. Roche Products Ltd; revised January 2021. electronic medicines compendium (emc).
- [CDC](https://www.cdc.gov/flu/hcp/antivirals/summary-clinicians.html): Centers for Disease Control and Prevention. Influenza Antiviral Medications: Summary for Clinicians. Last reviewed 10 March 2026.
- [WHO eEML](https://list.essentialmeds.org/recommendations/511): World Health Organization. Electronic Essential Medicines List – Oseltamivir (complementary list, section 6.4.3).
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=oseltamivir#emc-1194): Tamiflu hard capsules. SmPC. Roche; January 2021.
- Dosing source `CDC`: [CDC](https://www.cdc.gov/flu/hcp/antivirals/summary-clinicians.html): CDC. Influenza Antiviral Medications: Summary for Clinicians. March 2026.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=oseltamivir#emc-1194: Tamiflu 30/45/75 mg capsules SmPC (Roche, rev. Jan 2021): treatment incl. full-term neonates; seasonal prophylaxis in exceptional situations; infants <1 y PEP pandemic only; adult 75 mg BID 5 d (10 d immunocompromised), PEP 75 mg OD 10 d, epidemic up to 6 wk (12 wk immunocompromised); child weight bands 10–15/15–23/23–40/>40 kg 30/45/60/75 mg BID 5 d, same OD 10 d prophylaxis; infants 3 mg/kg BID 5 d, PEP 3 mg/kg OD 10 d; not for <36 wk PCA; renal treatment and prophylaxis tables incl. HD, PD, ≤10 not recommended; no child renal data; hepatic none; elderly; suspension/6 mg/mL compounded/teaspoon sweetened food; food no effect on levels; neuropsychiatric monitoring; probenecid doubles exposure; caution chlorpropamide/methotrexate/phenylbutazone; no interaction with paracetamol, aspirin, cimetidine, antacids, rimantadine, warfarin, amoxicillin; pregnancy >1,000 exposures, breastfeeding; AEs children vomiting, conjunctivitis, earache, otitis media; hepatitis/hepatic failure, angioedema, GI bleeding, convulsions; thrombocytopenia, visual disturbance, arrhythmia in table (frequency unclear).
- https://www.cdc.gov/flu/hcp/antivirals/summary-clinicians.html: CDC Summary for Clinicians (last reviewed 10 Mar 2026): treat hospitalized/severe/high-risk without waiting for confirmation, benefit even >48 h in hospitalized; dosing tables incl. AAP 3.5 mg/kg for 9–11 mo, preterm 1.0 mg/kg (<38 wk PMA), 1.5 mg/kg (38–40 wk), 3.0 mg/kg (>40 wk); prophylaxis 7 days after last exposure, infants 3 mo–<1 y 3 mg/kg OD, <3 mo not unless critical, institutional ≥2 wk to 1 wk after last case; critically ill standard doses absorbed, 150 mg BID may not add benefit, extend if severely ill; renal HD treatment not more than 5 days; pregnancy preferred, same dose; GI AEs less likely with food.
- https://list.essentialmeds.org/recommendations/511: WHO eEML oseltamivir: section 6.4.3, complementary list; 6 mg/mL powder for oral liquid (children), 30/45/75 mg capsules; limited to severe confirmed/suspected influenza in critically ill hospitalized patients; added 2011, changed 2025.
- https://www.who.int/publications/i/item/9789240097759: WHO Clinical practice guidelines for influenza (Sept 2024): landing page opened but recommendation text was not readable (nor on the MagicApp summary), so not cited.
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Read with offset 64000: text covers Midazolam to Moxifloxacin only; oseltamivir entry not readable, so no forms_ph note.

---

## Paracetamol  (`med_paracetamol`)

**Description (kept)**

Paracetamol is thought to act mainly centrally, reducing prostaglandin synthesis via inhibition of cyclooxygenase pathways in the CNS, with a possible contribution from its metabolite AM404 acting on cannabinoid and TRPV1 systems. It has analgesic and antipyretic effects but minimal peripheral anti-inflammatory activity, and is a first-line agent for mild-to-moderate pain and fever.

**Description (added)**

A small fraction is converted by hepatic cytochrome P-450 to the toxic metabolite NAPQI, normally detoxified by glutathione; an acute ingestion of at least 150 mg/kg (about 7.5–10 g in adults) can deplete glutathione and cause hepatocellular necrosis, and N-acetylcysteine is most effective within 8 hours of ingestion. In the Philippines, paracetamol is in the PhilHealth Konsulta primary-care medicines list as 300 mg and 500 mg tablets, 100 mg/mL drops, 120 mg/5 mL (125 mg/5 mL) and 250 mg/5 mL syrup/suspension, and 125 mg and 250 mg suppositories.

**Side effects**: 5 kept, 2 added

- NEW: Blood dyscrasias including thrombocytopenia and agranulocytosis (frequency not known)
- NEW: High anion gap metabolic acidosis, mainly in sepsis, malnutrition or glutathione deficiency (e.g. chronic alcoholism)

**Precautions**: 3 kept, 2 added

- NEW: Use with care in severe renal impairment
- NEW: Overdose hazard greater in non-cirrhotic alcoholic liver disease

**Interactions**: 4 kept, 3 added

- NEW: Metoclopramide or domperidone: may speed paracetamol absorption.
- NEW: Cholestyramine: reduces paracetamol absorption.
- NEW: Flucloxacillin: combined (especially prolonged) use raises the risk of high anion gap metabolic acidosis; use with caution.

**Disease links added**

- `chronic_kidney_disease`: **caution**: SmPC advises care in severe renal impairment (applies to advanced CKD).
- `hepatitis_b`: **caution**: Own inference: SmPC advises care in severe hepatic impairment, which can occur in chronic hepatitis B; not stated for hepatitis B specifically.

**References added**

- [UK SmPC](https://products.mhra.gov.uk/search/?search=paracetamol#emc-9128): Paracetamol 500 mg Tablets (P), Zentiva Pharma UK Ltd. Summary of Product Characteristics (updated 25 February 2025). electronic medicines compendium (emc).
- [Merck Manual Professional](https://www.merckmanuals.com/professional/injuries-poisoning/poisoning/acetaminophen-poisoning): O'Malley GF, O'Malley R. Acetaminophen Poisoning. Merck Manual Professional Edition (reviewed Apr 2025).
- [PhilHealth Konsulta](https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf): Philippine Health Insurance Corporation. Certification of Service Delivery Support (Medicines), Annex D2 – Konsulta Package accreditation.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=paracetamol#emc-9128: Zentiva Paracetamol 500 mg SmPC: care in severe renal or severe hepatic impairment; overdose hazard greater in non-cirrhotic alcoholic liver disease; HAGMA with sepsis, malnutrition, glutathione deficiency (chronic alcoholism), and with flucloxacillin; metoclopramide/domperidone increase absorption speed; cholestyramine reduces absorption; warfarin prolonged use; blood dyscrasias incl. thrombocytopenia and agranulocytosis (not known); NAC up to 24 h, maximal within 8 h.
- https://www.merckmanuals.com/professional/injuries-poisoning/poisoning/acetaminophen-poisoning: Merck Manual Professional, Acetaminophen Poisoning: toxicity requires ≥150 mg/kg within 24 h (~7.5–10 g adults); NAPQI formed by hepatic CYP450, detoxified by glutathione; overdose depletes glutathione causing hepatocellular necrosis; NAC most effective within 8 h.
- https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf: PhilHealth Konsulta Annex D2 medicines list: paracetamol 300 mg and 500 mg tablets; 100 mg/mL drops 15 mL; 120 mg/5 mL (125 mg/5 mL) syrup/suspension 30/60/120 mL; 250 mg/5 mL syrup/suspension 30/60/120 mL; 125 mg and 250 mg suppositories. No brands.

---

## Permethrin 5% cream  (`med_permethrin`)

**Description (kept)**

Permethrin is a synthetic pyrethroid that blocks sodium channels in the nerve membranes of mites and lice, causing paralysis and death. Very little is absorbed through human skin. Permethrin 5% cream is a first-line treatment for scabies; because it may not kill all eggs, a second application about a week later is usually advised, and all close contacts are treated at the same time.

**Description (added)**

WHO lists 5% permethrin cream as a whole-body topical scabicide and as the topical option for community mass treatment when oral ivermectin is contraindicated or unavailable (ivermectin is not given in pregnancy or to children under 15 kg). About 90% of patients are cured by one application; itching can last up to 4 weeks from an allergic reaction to dead mites and is not by itself a reason to re-treat. Clothes and bed linen are decontaminated after each treatment (wash at 60 °C or more and sun-dry, or seal in a plastic bag for 72 hours).

**Side effects**: 3 kept, 3 added

- NEW: Paraesthesia (tingling) and dry skin
- NEW: Oedema and hypersensitivity reactions (rare)
- NEW: Itching that persists up to 4 weeks after treatment (reaction to dead mites, not necessarily treatment failure)

**Precautions**: 2 kept, 2 added

- NEW: Application to the face, mucous membranes or broken skin (MSF)
- NEW: Hypersensitivity to any excipient (e.g., benzyl alcohol, cetostearyl alcohol in some creams)

**Interactions**: 1 kept, 1 added

- NEW: Topical corticosteroids for eczema-like reactions: withhold before treatment, as they may reduce the immune response to the mite and worsen the infestation.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Scabies (Also adolescents >12 y and elderly) | Topical | Up to 30 g (1 tube) | Single application; wash off after 8–12 h | Repeat once ≥7 days later if needed | 60 g per application | Label · UK SmPC |
| adult | Scabies (Include scalp, behind ears, palms, soles) | Topical | Thin layer, whole body | Leave on ≥8 h, then rinse | Repeat after 7 days | — | MSF |
| child | Scabies (6–12 y) | Topical | Up to 15 g (½ tube) | Single application; wash off after 8–12 h | Repeat once ≥7 days later if needed | 15 g per application | Label · UK SmPC |
| child | Scabies (1–5 y) (Under 2 y: medical supervision) | Topical | Up to 7.5 g (¼ tube) | Single application; wash off after 8–12 h | Repeat once ≥7 days later if needed | 7.5 g per application | Label · UK SmPC |
| child | Scabies (2 mo–1 y) (Not under 2 months) | Topical | Up to 3.75 g (⅛ tube) | Single application; wash off after 8–12 h | Repeat once ≥7 days later if needed | 3.75 g per application | Label · UK SmPC |

- *pregnancy*: Limited data show no sign of fetal risk; systemic absorption is very low, though some permethrin may cross the placenta. Breastfeeding: risk to the infant considered unlikely; do not apply the cream to the breasts (MSF). [Label · UK SmPC]
- *administration*: Apply to clean, dry, cool skin (not straight after a hot bath) and rub in gently. Reapply to the hands if they are washed within 8 hours. Carers applying it should wear gloves. Keep out of the eyes (rinse with water or saline if contact). Fabric soaked with cream ignites easily: keep away from flames. [Label · UK SmPC]
- *administration*: In children under 2 years, wrap the hands to prevent swallowing the cream and getting it in the eyes. [MSF]
- *monitor*: Give a second application (not sooner than 7 days) if original lesions are not healing or new lesions appear. Persistent itching alone within 4 weeks is not treatment failure; re-treat only if burrows are still present after that time. Treat all close contacts at the same time. [MSF]

**References added**

- [MSF Essential Drugs - Permethrin 5% cream](https://medicalguidelines.msf.org/en/viewport/EssDr/english/permethrin-5-cream-16687201.html): Medecins Sans Frontieres. Essential drugs - practical guidelines: Permethrin 5%, cream.
- [UK SmPC - Permethrin 5% w/w Cream (Sandoz)](https://products.mhra.gov.uk/search/?search=permethrin#emc-6540): Sandoz Limited. Permethrin 5% w/w Cream - Summary of Product Characteristics. electronic medicines compendium (emc).
- [WHO - Scabies fact sheet](https://www.who.int/news-room/fact-sheets/detail/scabies): World Health Organization. Scabies. Fact sheet.
- Dosing source `Label · UK SmPC`: [UK SmPC - Permethrin 5% w/w Cream (Sandoz)](https://products.mhra.gov.uk/search/?search=permethrin#emc-6540): Sandoz Limited. Permethrin 5% w/w Cream - SmPC. emc.
- Dosing source `MSF`: [MSF Essential Drugs - Permethrin 5% cream](https://medicalguidelines.msf.org/en/viewport/EssDr/english/permethrin-5-cream-16687201.html): Medecins Sans Frontieres. Essential drugs: Permethrin 5%, cream.

**What was checked on each page**

- https://medicalguidelines.msf.org/en/viewport/EssDr/english/permethrin-5-cream-16687201.html: MSF permethrin 5% cream: whole body incl. scalp/behind ears/palms/soles, leave >=8 h, repeat after 7 days, from 2 months; wrap hands <2 y; contraindicated <2 months and on face/mucosa/broken skin; AEs paraesthesia, pruritus, redness, burning, dry skin, rarely oedema/hypersensitivity; breastfeeding: do not apply to breasts; linen 60 °C/sun/sealed bag 72 h; itching up to 4 weeks, re-treat only if burrows persist; store below 25 °C.
- https://products.mhra.gov.uk/search/?search=permethrin#emc-6540: Sandoz Permethrin 5% w/w Cream SmPC: up to 30 g adults/elderly/>12 y (max 60 g), 6–12 y 15 g, 1–5 y 7.5 g, 2 mo–1 y 3.75 g; wash off 8–12 h; ~90% cured after one application; second application not sooner than 7 days; reapply to hands if washed within 8 h; gloves for carers; avoid eyes/mucosa/wounds; chrysanthemum caution; flammable fabric; benzyl alcohol, cetostearyl alcohol excipients; corticosteroids withheld before treatment; pregnancy/breastfeeding statements; itching up to 4 weeks; <2 y under medical supervision.
- https://www.who.int/news-room/fact-sheets/detail/scabies: WHO scabies fact sheet: 5% permethrin cream as whole-body topical treatment; ivermectin not for pregnant women or children <15 kg; permethrin 5% cream for MDA when ivermectin contraindicated/unavailable.
- https://medicalguidelines.msf.org/en/node/1011: Same MSF permethrin 5% cream monograph (redirects/canonical to the viewport URL above); not cited directly.
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Fetched with offset 60000: text ends in the M entries (Multivitamins); permethrin entry not reachable, so no forms_ph note.

---

## Praziquantel  (`med_praziquantel`)

**Description (kept)**

Praziquantel is a synthetic pyrazinoisoquinoline anthelmintic that increases the permeability of the helminth tegument to calcium, producing rapid muscle contraction, spastic paralysis and tegumental damage that exposes the parasite to host defenses. It is the drug of choice for all Schistosoma species, including S. japonicum endemic in the Philippines, and for the liver flukes Clonorchis and Opisthorchis, and is also active against tapeworms and cysticercosis.

**Description (added)**

WHO's 2022 schistosomiasis guideline extends preventive chemotherapy to adults and preschool children, considers praziquantel safe from age 2 years and in pregnancy after the first trimester, and recommends one annual dose where prevalence is 10% or more. In mass campaigns the dose is read from the person's height (dose pole) instead of weight.

**Uses**: 6 kept, 1 added

- NEW: Intestinal flukes (Fasciolopsis buski, Heterophyes heterophyes, Metagonimus yokogawai)

**Side effects**: 6 kept, 5 added

- NEW: Vomiting and fatigue (very common in mass treatment)
- NEW: Diarrhoea, sometimes bloody
- NEW: Eosinophilia and polyserositis
- NEW: Raised liver function tests
- NEW: Side effects more frequent and severe with heavy worm burden

**Precautions**: 4 kept, 2 added

- NEW: Avoid in epilepsy or signs of CNS involvement from schistosomiasis, paragonimiasis or T. solium cysticercosis (WHO-prequalified label)
- NEW: Not active against Fasciola hepatica or F. gigantica (use triclabendazole)

**Interactions**: 4 kept, 3 added

- NEW: Phenytoin, phenobarbital, carbamazepine and dexamethasone: lower praziquantel levels; concomitant use not recommended.
- NEW: Chloroquine: may lower praziquantel blood concentrations (mechanism unclear).
- NEW: Digoxin: monitor patients with arrhythmias or heart failure on digoxin during treatment.

**Disease links added**

- `heart_failure`: **caution**: WHO-prequalified label: monitor patients with arrhythmias or heart failure taking digoxin.
- `tuberculosis`: **caution**: Rifampicin is contraindicated with praziquantel; stop it 4 weeks before and restart 1 day after (applying this to TB treatment is an inference from the rifampicin interaction).
- `hiv_infection`: **caution**: Efavirenz lowers and ritonavir raises praziquantel levels per the US label (applying this to HIV treatment is an inference).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Schistosomiasis (S. haematobium, S. mansoni, S. intercalatum) | PO | 40 mg/kg | Single dose (or 20 mg/kg × 2, 4 h apart) | 1 day | — | MSF |
| adult | Schistosomiasis (S. japonicum, S. mekongi) (S. japonicum is the PH species) | PO | 20 mg/kg | 3 doses 4 h apart (or 30 mg/kg × 2) | 1 day | — | MSF |
| adult | Schistosomiasis, mass treatment (160–177 cm: 2400 mg) | PO | 600–3000 mg by height (dose pole) | Single dose | Yearly in high-risk areas | 3000 mg (≥178 cm) | WHO PQ label |
| adult | Clonorchiasis / opisthorchiasis | PO | 25 mg/kg | 3× a day (4–6 h apart) | 1 day | — | Label · DailyMed |
| adult | Lung and liver flukes (incl. paragonimiasis) | PO | 25 mg/kg | 3× a day | 2 days | — | MSF |
| adult | Intestinal flukes | PO | 25 mg/kg | 3× a day | 1 day | — | MSF |
| adult | Taeniasis (T. saginata, T. solium, D. latum) | PO | 5–10 mg/kg | Single dose | 1 day | — | MSF |
| adult | Taeniasis (H. nana) | PO | 15–25 mg/kg | Single dose | 1 day | — | MSF |
| child | Schistosomiasis (S. haematobium, S. mansoni, S. intercalatum) (MSF: from 4 years) | PO | 40 mg/kg | Single dose (or 20 mg/kg × 2, 4 h apart) | 1 day | — | MSF |
| child | Schistosomiasis (S. japonicum, S. mekongi) (US label: from 1 year (4–6 h apart)) | PO | 20 mg/kg | 3 doses 4 h apart | 1 day | — | Label · DailyMed |
| child | Schistosomiasis, mass treatment (<94 cm/<4 y: individual medical decision) | PO | 600 mg (94–109 cm); 900 mg (110–124 cm); 1200 mg (125–137 cm); 1500 mg (138–149 cm) | Single dose | Yearly in high-risk areas | — | WHO PQ label |
| child | Taeniasis (H. nana) (From 4 years) | PO | 15–25 mg/kg | Single dose | 1 day | — | MSF |

- *hepatic* Child-Pugh B–C: Moderate–severe impairment (Child-Pugh B/C): much higher exposure (AUC up to about 15-fold in Child-Pugh C); use with caution and watch for adverse effects. [WHO PQ label]
- *elderly*: No special precautions required. [WHO PQ label]
- *pregnancy*: WHO recommends annual single-dose preventive chemotherapy for pregnant women after the first trimester and for lactating women where prevalence is 10% or more. [WHO 2022]
- *pregnancy*: No contraindication for schistosomiasis or taeniasis; for fluke infections, delay until after delivery unless treatment is essential now. Breastfeeding: no contraindication (MSF), but the WHO-prequalified label advises not breastfeeding on the treatment day and for the next 24 hours. [MSF]
- *administration*: Swallow whole with water during or after a meal; do not chew or hold in the mouth (bitter, may cause gagging or vomiting). The 600 mg tablet is scored into four 150 mg segments. For children under 6, tablets may be crushed or dispersed in semi-solid food or liquid and used within 1 hour. [Label · DailyMed]
- *monitor*: Watch for dizziness, somnolence and seizures on the treatment day (no driving if they occur). Monitor patients with known arrhythmias and patients with heart failure on digoxin. New neurological symptoms may unmask undiagnosed neurocysticercosis. Expect more side effects with heavy worm burden. [WHO PQ label]

**References added**

- [MSF Essential Drugs - Praziquantel oral](https://medicalguidelines.msf.org/viewport/EssDr/english/praziquantel-oral-16684480.html): Medecins Sans Frontieres. Essential drugs - practical guidelines: Praziquantel, oral.
- [WHO Prequalification - Praziquantel 600 mg tablets SmPC (NT004)](https://extranet.who.int/prequal/sites/default/files/whopar_files/NT004part4.pdf): World Health Organization Prequalification. WHOPAR NT004 Part 4: Summary of product characteristics, Praziquantel Tablets 600 mg (Macleods Pharmaceuticals Ltd).
- [WHO - Guideline on control and elimination of human schistosomiasis (2022)](https://www.who.int/news/item/22-02-2022-who-launches-new-guideline-for-the-control-and-elimination-of-human-schistosomiasis): World Health Organization. WHO launches new guideline for the control and elimination of human schistosomiasis. News release, 22 February 2022.
- [BIGG (PAHO/BVS) - WHO schistosomiasis recommendation](https://bigg-rec.bvsalud.org/en/recommendations/db797c50ffffecd0187f631260baf6e5d402b92e): WHO guideline on control and elimination of human schistosomiasis (2022): annual single-dose praziquantel preventive chemotherapy where prevalence >=10%, incl. pregnant women after the first trimester. BIGG international database of GRADE guidelines.
- Dosing source `MSF`: [MSF Essential Drugs - Praziquantel oral](https://medicalguidelines.msf.org/viewport/EssDr/english/praziquantel-oral-16684480.html): Medecins Sans Frontieres. Essential drugs: Praziquantel, oral.
- Dosing source `WHO PQ label`: [WHO Prequalification - Praziquantel 600 mg tablets SmPC (NT004)](https://extranet.who.int/prequal/sites/default/files/whopar_files/NT004part4.pdf): WHOPAR NT004 Part 4: SmPC, Praziquantel Tablets 600 mg (Macleods).
- Dosing source `Label · DailyMed`: [DailyMed - BILTRICIDE](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=34ce1cdd-648e-4f1e-8512-bf3d4cc22eb9): BILTRICIDE (praziquantel) tablets, film coated. Prescribing information. DailyMed.
- Dosing source `WHO 2022`: [WHO guideline on control and elimination of human schistosomiasis (2022), via BIGG](https://bigg-rec.bvsalud.org/en/recommendations/db797c50ffffecd0187f631260baf6e5d402b92e): WHO 2022 recommendation: annual single-dose praziquantel preventive chemotherapy where prevalence >=10%.

**What was checked on each page**

- https://medicalguidelines.msf.org/viewport/EssDr/english/praziquantel-oral-16684480.html: MSF: 600 mg breakable tablet; child >=4 y and adults: S. haematobium/mansoni/intercalatum 40 mg/kg single or 2×20 mg/kg 4 h apart; S. japonicum/mekongi 2×30 mg/kg or 3×20 mg/kg 4 h apart; taeniasis 5–10 mg/kg single; H. nana 15–25 mg/kg single; lung/hepatobiliary flukes 25 mg/kg 3×/day 2 days; intestinal flukes (F. buski, H. heterophyes, M. yokogawai) 25 mg/kg 3×/day 1 day; ocular cysticercosis CI; pregnancy no CI for schisto/taeniasis, delay for flukes; breastfeeding no CI; not active vs Fasciola (triclabendazole); with meals, don't chew.
- https://extranet.who.int/prequal/sites/default/files/whopar_files/NT004part4.pdf: WHO PQ SmPC Praziquantel 600 mg (Macleods, NT004): height-based dosing 94–109 cm 600 mg ... 160–177 cm 2400 mg, >=178 cm 3000 mg; high-risk yearly; <4 y/<94 cm individual; hepatic Child-Pugh B/C AUC up to ~15-fold; renal no adjustment; elderly no precautions; avoid in epilepsy/CNS involvement; monitor arrhythmia/heart failure on digoxin; rifampicin stop 4 weeks before, restart 1 day after; phenytoin/phenobarbital/carbamazepine/dexamethasone not recommended; chloroquine lowers levels; no breastfeeding on treatment day + 24 h; AEs incl. vomiting, fatigue, eosinophilia, polyserositis, bloody diarrhoea, raised LFTs; heavier worm burden more AEs.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=34ce1cdd-648e-4f1e-8512-bf3d4cc22eb9: Biltricide: 20 mg/kg 3× in one day 4–6 h apart (schisto), 25 mg/kg (clonorchiasis/opisthorchiasis); ages >=1 y; swallow with water during meals, don't chew; scored into four 150 mg segments; crush/disperse for <6 y and use within 1 h; hepatic B/C monitor; monitor arrhythmias; avoid efavirenz.
- https://www.who.int/news/item/22-02-2022-who-launches-new-guideline-for-the-control-and-elimination-of-human-schistosomiasis: WHO 2022 guideline news: PC expanded to adults and preschool-aged children; single prevalence threshold; praziquantel safety for children >=2 y, adults, pregnant women after first trimester (and lactating women).
- https://bigg-rec.bvsalud.org/en/recommendations/db797c50ffffecd0187f631260baf6e5d402b92e: WHO 2022 schistosomiasis guideline recommendation: annual single-dose praziquantel PC where prevalence >=10%, incl. pregnant women after first trimester and lactating/postpartum women.
- https://www.who.int/publications/i/item/9789240041608: WHO guideline publication page (14 Feb 2022); recommendations not in page text, PDF did not load - not cited.
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Fetched with offset 60000: text ends in M entries; praziquantel entry not reachable. WHO-hosted 2017 PNF PDF also truncated at O. No forms_ph note.

---

## Prednisone  (`med_prednisone`)

**Description (kept)**

Prednisone is an oral synthetic glucocorticoid prodrug converted in the liver to prednisolone. It binds glucocorticoid receptors and alters gene transcription, producing potent anti-inflammatory and immunosuppressive effects. It is used across endocrine, rheumatic, collagen-vascular, dermatologic, allergic (including asthma exacerbations), respiratory, hematologic, neoplastic and gastrointestinal inflammatory disorders.

**Description (added)**

Prednisone is an intermediate-acting corticosteroid: 5 mg has about the same anti-inflammatory activity as 0.75 mg dexamethasone or 20 mg hydrocortisone. MSF lists prednisone and prednisolone together as essential drugs for the symptomatic treatment of allergic and inflammatory diseases, dosed by body weight. Short oral courses are a standard part of treating acute asthma exacerbations in adults and children.

**Uses**: 6 kept, 1 added

- NEW: Acute exacerbations of multiple sclerosis (label dosing section)

**Side effects**: 8 kept, 8 added

- NEW: Pancreatitis
- NEW: Thromboembolism
- NEW: Kaposi's sarcoma (may improve when the steroid is stopped)
- NEW: Aseptic necrosis of the femoral and humeral heads
- NEW: Benign intracranial hypertension
- NEW: Growth retardation in children on prolonged treatment
- NEW: Reactivation of latent tuberculosis
- NEW: Strongyloides hyperinfection and activation of latent amoebiasis

**Precautions**: 3 kept, 3 added

- NEW: Active ocular herpes simplex (risk of corneal perforation)
- NEW: Cerebral malaria (label: avoid)
- NEW: Active peptic ulcer unless the ulcer is being treated (MSF)

**Interactions**: 6 kept, 10 added

- NEW: Anticholinesterases: may cause severe weakness in myasthenia gravis.
- NEW: Isoniazid: serum isoniazid levels may fall.
- NEW: Colestyramine: may increase corticosteroid clearance.
- NEW: Ciclosporin: activity of both drugs may increase.
- NEW: Digoxin and other digitalis glycosides: higher arrhythmia risk from hypokalaemia.
- NEW: Oestrogens, including oral contraceptives: reduced hepatic metabolism, stronger steroid effect.
- NEW: Fluoroquinolones: higher risk of tendon rupture.
- NEW: Quetiapine: higher quetiapine doses may be needed.
- NEW: Thalidomide: use cautiously; toxic epidermal necrolysis reported.
- NEW: Skin tests: reactions may be suppressed.

**Disease links added**

- `malaria`: **caution**: Label says to avoid corticosteroids in cerebral malaria.
- `measles`: **caution**: Measles can take a serious or fatal course in non-immune patients on corticosteroids (label).
- `heart_failure`: **caution**: Sodium and fluid retention; label advises caution in congestive heart failure.
- `chronic_kidney_disease`: **caution**: Label advises caution in renal insufficiency (fluid retention, hypertension).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Inflammatory/allergic disease (Starting dose depends on disease and severity) | PO | 5–60 mg/day | Once a day (morning, before 9 am) | Until response, then taper to lowest effective dose | — | Label · DailyMed |
| adult | Inflammatory/allergic disease (If >10 days, cut high starting dose to lowest effective dose fast) | PO | 0.5–2 mg/kg/day | Once a day or ÷ 2 | Per indication; taper if >3 weeks | 80 mg/day | MSF |
| adult | Asthma exacerbation (50–60 mg for severe attacks; 5–7 days usually enough) | PO | 40–60 mg/day | Once a day or ÷ 2 | 3–10 days | — | Merck |
| child | Inflammatory/allergic disease | PO | 0.5–2 mg/kg/day | Once a day or ÷ 2 | Per indication; taper if >3 weeks | 80 mg/day | MSF |
| child | Asthma exacerbation (3–5 days usually enough in children) | PO | 1–2 mg/kg/day | Once a day | 5 days | <2 y 20 mg; 3–5 y 30 mg; 6–11 y 40 mg per day | Merck |

- *forms_ph*: Prednisone 5 mg, 10 mg and 20 mg tablets; 10 mg/5 mL suspension, 60 mL (PhilHealth Konsulta medicines list). [PhilHealth Konsulta]
- *renal*: Use with caution in renal insufficiency (sodium and fluid retention); no specific dose change given. [Label · DailyMed]
- *hepatic*: Effect is enhanced in cirrhosis because corticosteroid metabolism is reduced. [Label · DailyMed]
- *elderly*: Start at the low end of the dose range. [Label · DailyMed]
- *pregnancy*: US label: use only if benefit justifies risk (cleft palate in animal studies). MSF: no contraindication in pregnancy or breastfeeding; use the lowest effective dose, and for >40 mg/day beyond 7 days give just after a feed and wait about 4 h before the next feed. [MSF]
- *administration*: Give in the morning before 9 am, with or right after food or milk to reduce stomach upset. Alternate-day therapy: twice the usual daily dose every other morning. Do not stop suddenly; taper after more than 3 weeks of treatment. [Label · DailyMed]
- *monitor*: Blood pressure, weight and oedema, serum potassium, blood glucose; intraocular pressure if treatment lasts >6 weeks; growth in children; signs of infection and TB reactivation; mood and sleep changes. [Label · DailyMed]

**References added**

- [MSF Essential Drugs - Prednisolone and prednisone, oral](https://medicalguidelines.msf.org/viewport/EssDr/english/prednisolone-and-prednisone-oral-16684491.html): Medecins Sans Frontieres. Essential drugs - practical guidelines: Prednisolone and prednisone, oral.
- [Merck Manual Professional - Treatment of Acute Asthma Exacerbations](https://www.merckmanuals.com/professional/pulmonary-disorders/asthma-and-related-disorders/treatment-of-acute-asthma-exacerbations): Merck Manual Professional Version. Treatment of Acute Asthma Exacerbations. Merck & Co.
- Dosing source `PhilHealth Konsulta`: [PhilHealth Konsulta medicines list (Annex D2)](https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf): Philippine Health Insurance Corporation. Konsulta package: Certification of Service Delivery Support (Medicines), Annex D2.
- Dosing source `Label · DailyMed`: [DailyMed - Prednisone tablets USP (Par)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=10fe5a3b-84dc-4600-87c2-b80c97ce18cf): Prednisone tablets, USP. Prescribing information. Par Health USA. DailyMed.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/viewport/EssDr/english/prednisolone-and-prednisone-oral-16684491.html): Medecins Sans Frontieres. Essential drugs: Prednisolone and prednisone, oral.
- Dosing source `Merck`: [Merck Manual Professional](https://www.merckmanuals.com/professional/pulmonary-disorders/asthma-and-related-disorders/treatment-of-acute-asthma-exacerbations): Merck Manual Professional Version. Treatment of Acute Asthma Exacerbations.

**What was checked on each page**

- https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf: Konsulta Annex D2 lists the forms in the forms_ph note.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=10fe5a3b-84dc-4600-87c2-b80c97ce18cf: Par prednisone label: 5–60 mg/day, morning before 9 am, with food/milk, alternate-day = twice daily dose every other morning, MS exacerbation dosing; caution in CHF/hypertension/renal insufficiency; enhanced effect in cirrhosis and hypothyroidism; elderly low-end start; pregnancy cat C cleft palate; interactions (anticholinesterases, isoniazid, cholestyramine, cyclosporine, digitalis, estrogens, fluoroquinolones tendon rupture, quetiapine, skin tests, thalidomide TEN); warnings TB reactivation, varicella/measles serious course, Strongyloides, latent amebiasis, avoid in cerebral malaria, ocular herpes simplex; IOP monitoring >6 weeks; salt restriction/potassium; Kaposi's sarcoma, pancreatitis, thromboembolism, aseptic necrosis, benign intracranial hypertension; pediatric growth monitoring, titrate to lowest dose.
- https://medicalguidelines.msf.org/viewport/EssDr/english/prednisolone-and-prednisone-oral-16684491.html: Intermediate-acting corticosteroid; adults and children 0.5–2 mg/kg once daily (morning) or ÷2, max 80 mg/day; reduce quickly if >10 days, taper if >3 weeks; not in active peptic ulcer unless treated; growth retardation; pregnancy/breastfeeding no contraindication, >40 mg/day >7 days dose after feed, wait 4 h; take with food; 5 mg = 0.75 mg dexamethasone = 20 mg hydrocortisone.
- https://www.merckmanuals.com/professional/pulmonary-disorders/asthma-and-related-disorders/treatment-of-acute-asthma-exacerbations: Drug table: prednisone adults 40–60 mg/day single or ÷ q12h for 3–10 days; children 1–2 mg/kg daily for 5 days; max <2 y 20 mg, 3–5 y 30 mg, 6–11 y 40 mg (prednisone row); 50–60 mg for severe; 3–5 days children, 5–7 days adults adequate.
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: NOT USED: WebFetch text ends at 'Multivitamins' (65,922 chars; offset 60000 covers Medroxyprogesterone–Multivitamins), so the prednisone entry could not be read. No forms_ph note written.

---

## Propranolol  (`med_propranolol`)

**Description (kept)**

Propranolol blocks beta-1 and beta-2 adrenergic receptors, slowing heart rate and reducing tremor, anxiety and sweating driven by excess thyroid hormone; at higher doses it also modestly reduces conversion of T4 to T3. It controls symptoms of hyperthyroidism while antithyroid treatment takes effect, and is used for hypertension, angina, migraine prevention and essential tremor.

**Description (added)**

Propranolol is on the WHO Essential Medicines List for migraine prophylaxis (10 mg and 40 mg tablets). In thyroid storm it lowers heart rate within 2–3 hours when given orally and within minutes when given IV. An oral solution is approved for proliferating infantile haemangioma, started between 5 weeks and 5 months of age.

**Uses**: 5 kept, 6 added

- NEW: Secondary prevention after myocardial infarction
- NEW: Cardiac arrhythmias and anxiety-related tachycardia
- NEW: Somatic symptoms of situational and generalised anxiety
- NEW: Phaeochromocytoma (only together with an alpha-blocker)
- NEW: Hypertrophic obstructive cardiomyopathy; Fallot's tetralogy in children
- NEW: Proliferating infantile haemangioma needing systemic therapy (oral solution)

**Side effects**: 5 kept, 7 added

- NEW: Raynaud's phenomenon
- NEW: Hallucinations, psychosis, confusion and depression
- NEW: Worsening heart failure, heart block and postural hypotension
- NEW: Thrombocytopenia
- NEW: Hypoglycaemia, sometimes with seizures (especially in infants)
- NEW: Myasthenia gravis-like syndrome or worsening of myasthenia
- NEW: More severe anaphylaxis with poor response to usual adrenaline doses

**Precautions**: 3 kept, 7 added

- NEW: Hypotension or metabolic acidosis
- NEW: Prolonged fasting or proneness to hypoglycaemia
- NEW: Severe peripheral arterial circulatory disease
- NEW: Sick sinus syndrome
- NEW: Untreated phaeochromocytoma
- NEW: Prinzmetal's angina
- NEW: Infants under 2 kg or with corrected age under 5 weeks (oral solution)

**Interactions**: 4 kept, 9 added

- NEW: Rizatriptan: levels rise by about 70–80%; use rizatriptan 5 mg.
- NEW: Nifedipine and other dihydropyridines: more hypotension; heart failure in latent cardiac insufficiency.
- NEW: Class I antiarrhythmics, amiodarone and digoxin: additive effects on conduction and contractility.
- NEW: Lidocaine: levels rise by about 30%; avoid the combination.
- NEW: Adrenaline and other sympathomimetics: may counteract beta-blockade; give parenteral adrenaline with care.
- NEW: Cimetidine, hydralazine, alcohol and chlorpromazine: raise propranolol levels.
- NEW: Ergotamine and related drugs: risk of vasospastic reactions.
- NEW: NSAIDs (ibuprofen, indometacin): may blunt the blood-pressure-lowering effect.
- NEW: Rifampicin, theophylline, warfarin, thioridazine, quinidine and propafenone: altered levels; dose adjustment may be needed.

**Brands (intl)**: 1 kept, 1 added

- NEW: Hemangeol

**Disease links added**

- `hypertension`: **safe**: Licensed indication (usual 160–320 mg/day).
- `migraine`: **safe**: Licensed for migraine prophylaxis; on the WHO EML for this use.
- `acute_coronary_syndrome`: **safe**: Licensed for secondary prevention after MI, started 5–21 days after the infarct; contraindicated in cardiogenic shock.
- `asthma`: **avoid**: Contraindicated with a history of bronchial asthma or bronchospasm; fatal bronchospasm reported.
- `heart_failure`: **caution**: Contraindicated in uncontrolled heart failure; controlled heart failure only with caution.
- `type2_diabetes`: **caution**: Masks hypoglycaemia (tachycardia) and may prolong insulin-induced hypoglycaemia.
- `copd`: **caution**: Bronchospasm risk (label contraindicates asthma/bronchospasm history; applying caution to COPD is an inference).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Hypertension (Increase at weekly intervals) | PO | 80 mg | 2× a day | Long-term | 320 mg/day (usual 160–320 mg) | Label · UK SmPC |
| adult | Angina (Usual 120–240 mg/day; increase weekly) | PO | 40 mg | 2–3× a day | Long-term | — | Label · UK SmPC |
| adult | Migraine prophylaxis / essential tremor (Usual 80–160 mg/day) | PO | 40 mg | 2–3× a day | Long-term | — | Label · UK SmPC |
| adult | Arrhythmia, thyrotoxicosis, HOCM | PO | 10–40 mg | 3–4× a day | Per response | — | Label · UK SmPC |
| adult | Anxiety | PO | 40 mg | Once a day (situational); 2–3× a day (generalised) | Review at 6–12 months | — | Label · UK SmPC |
| adult | After myocardial infarction (Start 5–21 days after the infarct) | PO | 40 mg, then 80 mg | 4× a day for 2–3 days, then 2× a day | Long-term | — | Label · UK SmPC |
| adult | Portal hypertension (Aim for ~25% fall in resting heart rate) | PO | 40 mg, up to 80 mg | 2× a day | Long-term | 160 mg 2× a day | Label · UK SmPC |
| adult | Thyroid storm (Adjust to heart rate and blood pressure) | PO | 60–80 mg | Every 4–6 h | Until controlled | — | Merck |
| adult | Thyroid storm (Close monitoring) | IV | 0.5–1 mg over 10–15 min | Every 4 h | Until oral possible | 1 mg/min rate | Merck |
| child | Arrhythmia, thyrotoxicosis, phaeochromocytoma | PO | 0.25–0.5 mg/kg | 3–4× a day | Per response | — | Label · UK SmPC |
| child | Migraine prophylaxis (<12 y) (≥12 y: adult dose) | PO | 20 mg | 2–3× a day | Long-term | — | Label · UK SmPC |
| child | Fallot's tetralogy | PO | Up to 1 mg/kg | 3–4× a day | Per response | — | Label · UK SmPC |
| child | Infantile haemangioma (age 5 wk–5 mo) (Oral solution; give during or right after a feed) | PO | 0.6 mg/kg → 1.1 mg/kg (wk 2) → 1.7 mg/kg (from wk 3) | 2× a day, ≥9 h apart | 6 months | 1.7 mg/kg 2× a day | Label · US FDA |

- *renal*: Half-life may be prolonged: take care when starting and choosing the first dose. No specific dose change given. [Label · UK SmPC]
- *hepatic*: Half-life may be prolonged: start carefully; caution in decompensated cirrhosis. May worsen hepatic encephalopathy in portal hypertension. [Label · UK SmPC]
- *elderly*: Start at the lowest dose and adjust to response. [Label · UK SmPC]
- *pregnancy*: Avoid unless essential: reduced placental perfusion, risk of fetal death, premature delivery, and neonatal hypoglycaemia and bradycardia. Breastfeeding not recommended. [Label · UK SmPC]
- *administration*: Taper over 7–14 days when stopping. If beta-blockade is to be stopped before surgery, stop at least 24 h beforehand. Infant oral solution: give during or right after a feed and skip the dose if the child is not eating or is vomiting. [Label · UK SmPC]
- *monitor*: Heart rate and blood pressure (stop if severe or symptomatic bradycardia/hypotension); signs of heart failure; blood glucose in diabetes and in infants; wheeze. Infants: check heart rate and blood pressure for 2 h after starting or increasing the dose. Note it may mask thyrotoxicosis signs and interferes with bilirubin and catecholamine assays. [Label · US FDA]

**References added**

- [UK SmPC - Propranolol 40 mg film-coated tablets](https://products.mhra.gov.uk/search/?search=propranolol#emc-101996): Ipca Laboratories UK Ltd. Propranolol 40 mg film-coated tablets - Summary of Product Characteristics. electronic medicines compendium (emc).
- [Merck Manual Professional - Hyperthyroidism](https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/hyperthyroidism): Merck Manual Professional Version. Hyperthyroidism. Merck & Co.
- [US FDA label - HEMANGEOL (propranolol oral solution)](https://www.accessdata.fda.gov/drugsatfda_docs/label/2021/205410s006lbl.pdf): Pierre Fabre. HEMANGEOL (propranolol hydrochloride) oral solution. Prescribing information. US FDA; 2021.
- [WHO Electronic Essential Medicines List - Propranolol](https://list.essentialmeds.org/medicines/392): World Health Organization. eEML - Electronic Essential Medicines List: Propranolol.
- Dosing source `Label · UK SmPC`: [UK SmPC - Propranolol 40 mg film-coated tablets](https://products.mhra.gov.uk/search/?search=propranolol#emc-101996): Ipca Laboratories UK Ltd. Propranolol 40 mg film-coated tablets - SmPC. emc.
- Dosing source `Merck`: [Merck Manual Professional - Hyperthyroidism](https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/hyperthyroidism): Merck Manual Professional Version. Hyperthyroidism.
- Dosing source `Label · US FDA`: [US FDA label - HEMANGEOL](https://www.accessdata.fda.gov/drugsatfda_docs/label/2021/205410s006lbl.pdf): HEMANGEOL (propranolol hydrochloride) oral solution. Prescribing information. US FDA; 2021.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=propranolol#emc-101996: Ipca propranolol 40 mg SmPC: posology for hypertension (80 mg 2×, 160–320), angina (40 mg 2–3×, 120–240), migraine/tremor (80–160), anxiety, arrhythmia/thyrotoxicosis/HOCM 10–40 mg 3–4×, post-MI 40 mg 4× then 80 mg 2× from day 5–21, portal HTN 40→80 mg 2× max 160 mg 2× (25% HR fall), phaeo with alpha-blocker; children 0.25–0.5 mg/kg 3–4×, migraine <12 y 20 mg 2–3×, Fallot up to 1 mg/kg 3–4×; elderly; renal/hepatic half-life prolonged, decompensated cirrhosis; contraindications (asthma/bronchospasm, hypotension, metabolic acidosis, fasting/hypoglycaemia, severe PAD, sick sinus, untreated phaeo, uncontrolled HF, Prinzmetal); warnings (taper 7–14 days, stop 24 h before surgery, masks hypoglycaemia/thyrotoxicosis, anaphylaxis/adrenaline, hepatic encephalopathy, assay interference); interactions (rizatriptan, verapamil/diltiazem, dihydropyridines, antiarrhythmics, lidocaine, adrenaline, cimetidine/hydralazine/alcohol/chlorpromazine, clonidine, ergotamine, NSAIDs, metabolic list); pregnancy/breastfeeding; ADRs (Raynaud, hallucinations/psychosis, HF, heart block, thrombocytopenia, myasthenia, hypoglycaemia seizures, depression).
- https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/hyperthyroidism: Thyroid storm: propranolol 60–80 mg PO every 4–6 h adjusted to HR/BP; 0.5–1 mg IV over 10–15 min every 4 h (≤1 mg/min) under close monitoring; HR falls within 2–3 h oral, minutes IV.
- https://www.accessdata.fda.gov/drugsatfda_docs/label/2021/205410s006lbl.pdf: HEMANGEOL: proliferating infantile hemangioma; start age 5 wk–5 mo; 0.6 mg/kg 2× (≥9 h apart), 1.1 mg/kg after 1 week, 1.7 mg/kg after 2 weeks for 6 months; give during/after feeding, skip if not eating/vomiting; HR/BP monitoring 2 h after start/increase; contraindications <2 kg, corrected age <5 wk, asthma, HR <80, BP <50/30, pheochromocytoma; hypoglycemia with seizures.
- https://list.essentialmeds.org/medicines/392: WHO eEML propranolol: migraine prophylaxis, tablets 10 mg and 40 mg (added 1989). Page also shows cardiovascular listings with confusing 'removed 1997' history, so only the migraine listing is cited.
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: NOT USED: WebFetch text ends at 'Multivitamins' (65,922 chars), so the propranolol entry could not be read. No forms_ph note written.

---

