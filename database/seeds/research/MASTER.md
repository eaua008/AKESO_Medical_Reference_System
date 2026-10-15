# Akeso seed data — shared master lists (read this first)

Akeso is a medical REFERENCE platform for medical/health students in the
Philippines (desktop app). This data feeds: Disease Encyclopedia, Symptom
Encyclopedia, Medicine Reference, a Symptom Checker (scores reported symptoms
against disease_symptoms links) and a Drug Interaction Checker (drug x drug
pairs, drug x patient-condition safety, multi-drug rules).

Write in neutral reference voice ("Reference urgency", "is associated with"),
never advice addressed to a patient. Adult content unless stated.

## HARD RULES for research
- Use only WebSearch / WebFetch for the web. If a site is blocked or fails,
  do NOT use curl/wget/python to fetch it; pick another source.
- Every `url` you output must be one you actually opened with WebFetch and
  that loaded the right page. No guessed URLs. If unverified, leave url "".
- Prefer: NCBI Bookshelf StatPearls (https://www.ncbi.nlm.nih.gov/books/NBK...),
  WHO fact sheets, CDC, MedlinePlus, DailyMed / FDA labels, NICE, DOH
  Philippines, PSMID/PCP guidelines, GINA/GOLD/ADA/ESC/AHA guideline pages.
- Tier 1 "mother book" (is_mother_book=true): one standard textbook per
  disease, e.g. "Harrison's Principles of Internal Medicine, 21st ed.
  (Loscalzo et al., McGraw Hill, 2022)". Only name a chapter title/number if
  you verified it. Its url is always "" (a publisher press release is not
  the book). build_sql.py refuses a mother book with a url.
- Drug labels (DailyMed / FDA prescribing information) are cited on the
  MEDICINE they describe, never on a disease or symptom. build_sql.py
  refuses them on diseases and symptoms.
- Accuracy over volume. If unsure of a fact, leave it out.

## Enums
severity: Mild | Moderate | Severe | Critical
urgency (reference attribute): SELF_CARE | SEE_DOCTOR_SOON | SEEK_URGENT_CARE | EMERGENCY
safety: safe | caution | avoid
prevention tier: primary | secondary | tertiary
medicine category: OTC | Prescription

## Body systems (use these exact names)
Cardiovascular System; Respiratory System; Digestive System; Urinary System;
Endocrine System; Nervous System; Immune & Lymphatic System;
Musculoskeletal System; Integumentary System; Hematologic System;
Multisystem (Systemic Infection); Systemic / General (symptoms only)

## Diseases (id — name)
dengue — Dengue
typhoid_fever — Typhoid Fever
leptospirosis — Leptospirosis
tuberculosis — Pulmonary Tuberculosis
malaria — Malaria (Plasmodium falciparum / vivax)
community_acquired_pneumonia — Community-Acquired Pneumonia
influenza — Influenza
covid19 — COVID-19
measles — Measles
acute_gastroenteritis — Acute Infectious Gastroenteritis (Acute Diarrhea)
urinary_tract_infection — Urinary Tract Infection (Cystitis / Pyelonephritis)
peptic_ulcer_disease — Peptic Ulcer Disease
hypertension — Essential Hypertension
type2_diabetes — Type 2 Diabetes Mellitus
asthma — Bronchial Asthma
copd — Chronic Obstructive Pulmonary Disease
acute_coronary_syndrome — Acute Coronary Syndrome (incl. Myocardial Infarction)
heart_failure — Heart Failure
ischemic_stroke — Acute Ischemic Stroke
migraine — Migraine

## Symptoms (id — name). Link diseases ONLY to these ids.
sym_fever — Fever
sym_chills — Chills / rigors
sym_headache — Headache
sym_retroorbital_pain — Retro-orbital pain (pain behind the eyes)
sym_myalgia — Muscle aches (myalgia)
sym_calf_pain — Calf muscle pain / tenderness
sym_arthralgia — Joint pain (arthralgia)
sym_rash — Skin rash
sym_bleeding — Mucosal bleeding / petechiae (gum bleeding, nosebleed)
sym_abdominal_pain — Abdominal pain
sym_epigastric_pain — Epigastric pain
sym_heartburn — Heartburn
sym_nausea_vomiting — Nausea & vomiting
sym_diarrhea — Diarrhea
sym_constipation — Constipation
sym_melena — Black, tarry stools (melena)
sym_hematemesis — Vomiting blood (hematemesis)
sym_anorexia — Loss of appetite
sym_fatigue — Fatigue & malaise
sym_weight_loss — Unintentional weight loss
sym_night_sweats — Night sweats
sym_cough — Cough
sym_productive_cough — Productive cough (sputum)
sym_hemoptysis — Coughing up blood (hemoptysis)
sym_dyspnea — Shortness of breath (dyspnea)
sym_wheezing — Wheezing
sym_chest_tightness — Chest tightness
sym_pleuritic_chest_pain — Pleuritic chest pain
sym_chest_pain — Chest pain or pressure (angina-like)
sym_sore_throat — Sore throat
sym_rhinorrhea — Runny nose (coryza)
sym_conjunctivitis — Red eyes (conjunctivitis / conjunctival suffusion)
sym_koplik_spots — Koplik spots
sym_anosmia — Loss of smell or taste
sym_jaundice — Jaundice
sym_dark_urine — Dark urine
sym_decreased_urine — Decreased urine output (oliguria)
sym_dysuria — Painful urination (dysuria)
sym_urinary_frequency — Urinary frequency & urgency
sym_flank_pain — Flank pain
sym_suprapubic_pain — Suprapubic pain
sym_polyuria — Excessive urination (polyuria)
sym_polydipsia — Excessive thirst (polydipsia)
sym_blurred_vision — Blurred vision
sym_palpitations — Palpitations
sym_orthopnea — Breathlessness lying flat (orthopnea)
sym_edema — Leg swelling (edema)
sym_diaphoresis — Sweating (diaphoresis)
sym_dizziness — Dizziness / lightheadedness
sym_hemiparesis — One-sided weakness or numbness
sym_facial_droop — Facial droop
sym_speech_difficulty — Slurred or difficult speech
sym_confusion — Confusion / altered mental status
sym_photophobia — Sensitivity to light (photophobia)
sym_visual_aura — Visual aura

## Medicines (id — name — drug_class, use the drug_class EXACTLY)
med_paracetamol — Paracetamol — Analgesic / antipyretic (para-aminophenol)
med_ibuprofen — Ibuprofen — NSAID (propionic acid derivative)
med_mefenamic_acid — Mefenamic Acid — NSAID (fenamate)
med_aspirin — Aspirin (low-dose) — Antiplatelet (salicylate)
med_clopidogrel — Clopidogrel — Antiplatelet (P2Y12 inhibitor)
med_warfarin — Warfarin — Anticoagulant (vitamin K antagonist)
med_amoxicillin — Amoxicillin — Antibiotic (aminopenicillin)
med_coamoxiclav — Co-amoxiclav (Amoxicillin + Clavulanic acid) — Antibiotic (aminopenicillin + beta-lactamase inhibitor)
med_azithromycin — Azithromycin — Antibiotic (macrolide)
med_clarithromycin — Clarithromycin — Antibiotic (macrolide)
med_ceftriaxone — Ceftriaxone — Antibiotic (third-generation cephalosporin)
med_ciprofloxacin — Ciprofloxacin — Antibiotic (fluoroquinolone)
med_nitrofurantoin — Nitrofurantoin — Antibiotic (nitrofuran)
med_doxycycline — Doxycycline — Antibiotic (tetracycline)
med_rifampicin — Rifampicin — Antituberculosis agent (rifamycin)
med_isoniazid — Isoniazid — Antituberculosis agent
med_pyrazinamide — Pyrazinamide — Antituberculosis agent
med_ethambutol — Ethambutol — Antituberculosis agent
med_artemether_lumefantrine — Artemether + Lumefantrine — Antimalarial (artemisinin-based combination)
med_oseltamivir — Oseltamivir — Antiviral (neuraminidase inhibitor)
med_nirmatrelvir_ritonavir — Nirmatrelvir + Ritonavir — Antiviral (SARS-CoV-2 protease inhibitor, ritonavir-boosted)
med_ors — Oral Rehydration Salts (reduced osmolarity) — Oral rehydration solution
med_loperamide — Loperamide — Antidiarrheal (opioid receptor agonist)
med_omeprazole — Omeprazole — Proton pump inhibitor
med_amlodipine — Amlodipine — Calcium channel blocker (dihydropyridine)
med_losartan — Losartan — Angiotensin receptor blocker (RAAS blocker)
med_enalapril — Enalapril — ACE inhibitor (RAAS blocker)
med_hydrochlorothiazide — Hydrochlorothiazide — Thiazide diuretic
med_furosemide — Furosemide — Loop diuretic
med_spironolactone — Spironolactone — Potassium-sparing diuretic (mineralocorticoid receptor antagonist)
med_metoprolol — Metoprolol — Beta-blocker (beta-1 selective)
med_atorvastatin — Atorvastatin — Statin (HMG-CoA reductase inhibitor)
med_dapagliflozin — Dapagliflozin — SGLT2 inhibitor
med_metformin — Metformin — Biguanide antidiabetic
med_gliclazide — Gliclazide — Sulfonylurea antidiabetic
med_salbutamol — Salbutamol (Albuterol) — Short-acting beta-2 agonist (bronchodilator)
med_budesonide_formoterol — Budesonide + Formoterol — Inhaled corticosteroid + long-acting beta-2 agonist
med_prednisone — Prednisone — Corticosteroid (systemic glucocorticoid)
med_sumatriptan — Sumatriptan — Triptan (5-HT1B/1D agonist)

## Patient conditions (Drug Interaction Checker), condition_id — label
hypertension — Hypertension
diabetes — Diabetes Mellitus
pregnant — Pregnancy
asthma — Asthma / Reactive Airway (also COPD)
peptic_ulcer — Peptic Ulcer / GI Bleed
renal_impairment — Chronic Kidney Disease
liver_disease — Liver Disease
autoimmune — Autoimmune Condition (lupus, RA, on biologics)

## Changelog
- 2026-09-26: removed 5 drug-label citations from diseases (ibuprofen on ACS
  and heart failure, sumatriptan on stroke and migraine, Paxlovid on COVID-19;
  each medicine keeps its own label) and the press-release URL from 10
  Harrison's citations. Existing databases: seeds/patches/001_fix_disease_citations.sql.

## Batch 2 (2026-09-27): 10 more conditions common in the Philippines
Everything above still applies. Batch 2 files: diseases_E/F/G.json,
symptoms_B.json, medicines_C.json, interactions_B.json.

### New diseases (id — name)
chikungunya — Chikungunya
hepatitis_b — Hepatitis B (Acute and Chronic)
hepatitis_a — Hepatitis A
cholera — Cholera
rabies — Rabies
schistosomiasis — Schistosomiasis (Schistosoma japonicum)
pertussis — Pertussis (Whooping Cough)
hfmd — Hand, Foot and Mouth Disease
varicella — Chickenpox (Varicella)
hiv_infection — HIV Infection

### New symptoms (id — name). Diseases may link to these AND the batch-1 list.
sym_joint_swelling — Joint swelling
sym_ruq_pain — Right upper abdominal pain (right upper quadrant)
sym_pale_stool — Pale or clay-colored stools
sym_pruritus — Itching (pruritus)
sym_watery_diarrhea — Profuse watery ("rice-water") diarrhea
sym_dehydration — Signs of dehydration (sunken eyes, dry mouth, intense thirst)
sym_muscle_cramps — Muscle cramps
sym_bite_site_paresthesia — Pain or tingling at an animal-bite site
sym_hydrophobia — Fear of water / throat spasms on swallowing (hydrophobia)
sym_hypersalivation — Excessive salivation / drooling
sym_agitation — Agitation, anxiety or hallucinations
sym_abdominal_swelling — Abdominal swelling (distension or ascites)
sym_bloody_stool — Blood in stool (hematochezia)
sym_paroxysmal_cough — Coughing fits with a "whoop" (paroxysmal cough)
sym_posttussive_vomiting — Vomiting after coughing fits (post-tussive vomiting)
sym_mouth_sores — Painful mouth sores or ulcers
sym_vesicular_rash — Blister-like rash (vesicles)
sym_lymphadenopathy — Swollen lymph nodes (lymphadenopathy)
sym_oral_thrush — White patches in the mouth (oral thrush)

### New medicines (id — name — drug_class, use the drug_class EXACTLY)
med_tenofovir — Tenofovir Disoproxil Fumarate — Antiviral (nucleotide reverse transcriptase inhibitor)
med_entecavir — Entecavir — Antiviral (nucleoside analogue, HBV polymerase inhibitor)
med_tld — Tenofovir + Lamivudine + Dolutegravir (TLD) — Antiretroviral (NRTI + integrase inhibitor fixed-dose combination)
med_cotrimoxazole — Co-trimoxazole (Sulfamethoxazole + Trimethoprim) — Antibiotic (sulfonamide + dihydrofolate reductase inhibitor)
med_praziquantel — Praziquantel — Anthelmintic (pyrazinoisoquinoline)
med_aciclovir — Aciclovir — Antiviral (nucleoside analogue, herpesvirus DNA polymerase inhibitor)
med_rabies_vaccine — Rabies Vaccine (PVRV / PCECV) — Vaccine (inactivated rabies)
med_rabies_immunoglobulin — Rabies Immunoglobulin (HRIG / ERIG) — Passive immunization (immunoglobulin)
med_cetirizine — Cetirizine — Antihistamine (second-generation H1 antagonist)
med_zinc_sulfate — Zinc Sulfate — Mineral supplement (zinc)

### Batch 2 rules
- Philippine brand names (brands_ph) only when verified on a Philippine
  source (PH FDA verification portal, DOH, a PH pharmacy listing). Otherwise
  leave the list empty. Never guess a brand.
- Pediatric conditions (pertussis, hfmd, varicella) may use Nelson Textbook
  of Pediatrics, 22nd ed. (Kliegman et al., Elsevier, 2024) as the mother book.
- Philippine context is valued: DOH programs (e.g. Animal Bite Treatment
  Centers, the Schistosomiasis Control Program, the National HIV/AIDS & STI
  Program, PhilHealth packages) when verified.
- 2026-09-27: batch 2 added (10 diseases, 19 symptoms, 10 medicines, 26
  interaction pairs, 3 rules) and cross-links dengue<->chikungunya,
  acute_gastroenteritis<->cholera, tuberculosis<->hiv_infection,
  measles<->varicella. Existing databases: re-run split/part1..part4 in order
  (the seed is idempotent; tested against a database at the 001 state).
- 2026-09-27: DOH pages sit behind a Cloudflare bot check, so three facts were
  confirmed from other official or peer-reviewed sources: TLD as DOH's
  first-line ARV regimen (PNA, 2 Jul 2026, quoting DOH); pentavalent DPT-HepB-Hib
  at 6/10/14 weeks (PIDS Research Paper 2022-04); Davao del Norte and Davao de
  Oro as low-prevalence schistosomiasis-endemic provinces (Belizario et al.,
  Parasitol Int 2024).
