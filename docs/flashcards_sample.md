# Auto flashcards v2: sample report

Built from this computer's cached encyclopedia: 40 diseases, 62 medicines, 96 symptoms.
**826 cards** pass the quality gates, in 57 auto decks. Cards rejected by the gates: 10 (needs 2 to 4 distractors: 1, answer appears in the question: 4, front too long: 5).

Old auto cards (`auto:` keys) are retired: no longer built, their review history is kept.

## Data coverage

| Template | Name | Entries with at least 1 card | Out of |
|---|---|---:|---:|
| `dz_picture` | Clinical picture | 35 | 40 diseases |
| `dz_vs` | Tell them apart | 40 | 40 diseases |
| `dz_mech` | Mechanism | 8 | 40 diseases |
| `dz_redflag` | Red flag | 39 | 40 diseases |
| `dz_tx` | Treatment | 39 | 40 diseases |
| `dz_feature` | Key features | 0 | 40 diseases |
| `rx_calc` | Dose calculation | 25 | 62 medicines |
| `rx_dose` | Dose recall | 61 | 62 medicines |
| `rx_class` | Drug class | 59 | 62 medicines |
| `rx_se` | Side effects | 62 | 62 medicines |
| `rx_contra` | Contraindications | 61 | 62 medicines |
| `rx_renal` | Kidney / liver dosing | 20 | 62 medicines |
| `rx_ix` | Interactions | 30 | 62 medicines |
| `sx_cause` | Causes | 96 | 96 symptoms |
| `sx_redflag` | Red flag | 0 | 96 symptoms |

## Templates skipped

- `dz_feature` (key features / criteria): **needs a diagnostic criteria field.** No authored list of key features exists, and building one from symptom links is not allowed.
- `sx_redflag`: **needs non-red-flag features of the symptom** to use as distractors. Symptoms only have causes and red flags, and red flags of unrelated conditions are not allowed.

## Sample cards

### Acute Rheumatic Fever and Rheumatic Heart Disease (disease, 7 cards)

**[dz_picture] Clinical picture** · difficulty: clinical · source: `symptoms` · key: `auto2:disease:rheumatic_fever:dz_picture`

- **Front:** A patient has fever, joint pain (arthralgia) and joint swelling. Symptoms begin about 2-4 weeks after the sore throat. Most likely diagnosis?
  - ▫️ Acute Appendicitis — _Shares fever, but not typical: joint pain (arthralgia)_
  - ▫️ Influenza — _Shares fever and joint pain (arthralgia), but not typical: joint swelling_
  - ▫️ Dengue — _Shares fever and joint pain (arthralgia), but not typical: joint swelling_
  - ✅ Acute Rheumatic Fever and Rheumatic Heart Disease — _Acute rheumatic fever (ARF) is an autoimmune inflammatory illness that follows untreated group A streptococcal throat infection, mainly in children aged 5-15 in low- and middle-income settings._
- **Answer:** Acute Rheumatic Fever and Rheumatic Heart Disease
- **Why:** Acute rheumatic fever (ARF) is an autoimmune inflammatory illness that follows untreated group A streptococcal throat infection, mainly in children aged 5-15 in low- and middle-income settings.
- **Don't confuse with:**
  - Dengue: Shares fever and joint pain (arthralgia), but not typical: joint swelling
  - Influenza: Shares fever and joint pain (arthralgia), but not typical: joint swelling
  - Acute Appendicitis: Shares fever, but not typical: joint pain (arthralgia)
- **Hint:** Think: Cardiovascular System

**[dz_vs] Tell them apart** · difficulty: clinical · source: `differential_diagnosis` · key: `auto2:disease:rheumatic_fever:dz_vs:septic-arthritis`

- **Front:** Acute Rheumatic Fever and Rheumatic Heart Disease vs Septic arthritis: what's the key difference?
- **Answer:** Usually one hot joint with high fever; organisms in joint fluid; does not migrate
- **Why:** Acute rheumatic fever (ARF) is an autoimmune inflammatory illness that follows untreated group A streptococcal throat infection, mainly in children aged 5-15 in low- and middle-income settings.

**[dz_redflag] Red flag** · difficulty: clinical · source: `emergency_warning_signs` · key: `auto2:disease:rheumatic_fever:dz_redflag`

- **Front:** In Acute Rheumatic Fever and Rheumatic Heart Disease, which finding means urgent care is needed?
  - ▫️ Pink ring-shaped rash on the trunk (erythema marginatum) — _A usual symptom of the illness, not a warning sign._
  - ✅ Chest pain or a racing, irregular heartbeat — _A warning sign listed for this condition._
  - ▫️ Sore throat — _A usual symptom of the illness, not a warning sign._
  - ▫️ Fatigue & malaise — _A usual symptom of the illness, not a warning sign._
- **Answer:** Chest pain or a racing, irregular heartbeat
- **Why:** A child or young person with fever and migrating joint pain or swelling, new chorea, or a new heart murmur weeks after a sore throat needs prompt medical assessment, including echocardiography.

**[dz_tx] Treatment** · difficulty: clinical · source: `medicines` · key: `auto2:disease:rheumatic_fever:dz_tx:use`

- **Front:** Which medicine is used for Acute Rheumatic Fever and Rheumatic Heart Disease?
  - ▫️ Oseltamivir — _Listed for Influenza, not for Acute Rheumatic Fever and Rheumatic Heart Disease._
  - ▫️ Allopurinol — _Listed for Gout, not for Acute Rheumatic Fever and Rheumatic Heart Disease._
  - ✅ Benzathine Penicillin G — _Single IM dose eradicates group A strep; repeated every 3-4 weeks as secondary prophylaxis (WHO, AHA). Never give IV._
  - ▫️ Zinc Sulfate — _Listed for Acute Infectious Gastroenteritis (Acute Diarrhea), not for Acute Rheumatic Fever and Rheumatic Heart Disease._
- **Answer:** Benzathine Penicillin G
- **Why:** Single IM dose eradicates group A strep; repeated every 3-4 weeks as secondary prophylaxis (WHO, AHA). Never give IV.
- **Hint:** Think: Long-acting penicillin (beta-lactam)

### Dengue (disease, 7 cards)

**[dz_picture] Clinical picture** · difficulty: clinical · source: `symptoms` · key: `auto2:disease:dengue:dz_picture`

- **Front:** A patient has fever, muscle aches (myalgia) and retro-orbital pain (pain behind the eyes). Most likely diagnosis?
  - ▫️ Acute Infectious Gastroenteritis (Acute Diarrhea) — _Shares fever and muscle aches (myalgia), but not typical: retro-orbital pain (pain behind the eyes)_
  - ▫️ Community-Acquired Pneumonia — _Shares fever and muscle aches (myalgia), but not typical: retro-orbital pain (pain behind the eyes)_
  - ▫️ Chickenpox (Varicella) — _Shares fever and muscle aches (myalgia), but not typical: retro-orbital pain (pain behind the eyes)_
  - ✅ Dengue — _Dengue is an acute mosquito-borne viral infection caused by four antigenically distinct dengue virus serotypes and transmitted mainly by Aedes aegypti and Aedes albopictus._
- **Answer:** Dengue
- **Why:** Dengue is an acute mosquito-borne viral infection caused by four antigenically distinct dengue virus serotypes and transmitted mainly by Aedes aegypti and Aedes albopictus.
- **Don't confuse with:**
  - Acute Infectious Gastroenteritis (Acute Diarrhea): Shares fever and muscle aches (myalgia), but not typical: retro-orbital pain (pain behind the eyes)
  - Chickenpox (Varicella): Shares fever and muscle aches (myalgia), but not typical: retro-orbital pain (pain behind the eyes)
  - Community-Acquired Pneumonia: Shares fever and muscle aches (myalgia), but not typical: retro-orbital pain (pain behind the eyes)
- **Hint:** Think: Multisystem (Systemic Infection)

**[dz_vs] Tell them apart** · difficulty: clinical · source: `differential_diagnosis` · key: `auto2:disease:dengue:dz_vs:chikungunya`

- **Front:** Dengue vs Chikungunya: what's the key difference?
- **Answer:** Arthralgia more prominent. Bleeding and marked thrombocytopenia are relatively more specific for dengue
- **Why:** Dengue is an acute mosquito-borne viral infection caused by four antigenically distinct dengue virus serotypes and transmitted mainly by Aedes aegypti and Aedes albopictus. Chikungunya is an acute mosquito-borne viral illness caused by chikungunya virus, an alphavirus transmitted mainly by Aedes aegypti and Aedes albopictus, the same vectors that spread dengue.

**[dz_redflag] Red flag** · difficulty: clinical · source: `emergency_warning_signs` · key: `auto2:disease:dengue:dz_redflag`

- **Front:** In Dengue, which finding means urgent care is needed?
  - ✅ Cold, pale, clammy skin or other signs of shock — _A warning sign listed for this condition._
  - ▫️ Skin rash — _A usual symptom of the illness, not a warning sign._
  - ▫️ Chills / rigors — _A usual symptom of the illness, not a warning sign._
  - ▫️ Dizziness / lightheadedness — _A usual symptom of the illness, not a warning sign._
- **Answer:** Cold, pale, clammy skin or other signs of shock
- **Why:** Acute febrile illness compatible with dengue without warning signs warrants prompt clinical review with CBC. Any warning sign (severe abdominal pain, persistent vomiting, mucosal bleeding, lethargy/restlessness, fluid accumulation, rising hematocrit with falling platelets) or signs of shock, severe bleeding or organ impairment place the presentation in the EMERGENCY tier.

**[dz_tx] Treatment** · difficulty: clinical · source: `medicines` · key: `auto2:disease:dengue:dz_tx:use`

- **Front:** Which medicine is used for Dengue?
  - ▫️ Doxycycline — _Listed for Cholera, not for Dengue._
  - ✅ Oral Rehydration Salts (reduced osmolarity) — _Oral fluids such as ORS support hydration in outpatient dengue without warning signs._
  - ▫️ Colchicine — _Listed for Gout, not for Dengue._
  - ▫️ Prednisone — _Listed for Gout, not for Dengue._
- **Answer:** Oral Rehydration Salts (reduced osmolarity)
- **Why:** Oral fluids such as ORS support hydration in outpatient dengue without warning signs.
- **Hint:** Think: Oral rehydration solution

### Acute Appendicitis (disease, 8 cards)

**[dz_picture] Clinical picture** · difficulty: clinical · source: `symptoms` · key: `auto2:disease:acute_appendicitis:dz_picture`

- **Front:** A patient has right lower abdominal pain (right lower quadrant) and abdominal pain. Most likely diagnosis?
  - ▫️ Hepatitis A — _Shares abdominal pain, but not typical: right lower abdominal pain (right lower quadrant)_
  - ▫️ Dengue — _Shares abdominal pain, but not typical: right lower abdominal pain (right lower quadrant)_
  - ✅ Acute Appendicitis — _Acute appendicitis is inflammation of the vermiform appendix, usually triggered by obstruction of its lumen._
  - ▫️ Acute Infectious Gastroenteritis (Acute Diarrhea) — _Shares abdominal pain, but not typical: right lower abdominal pain (right lower quadrant)_
- **Answer:** Acute Appendicitis
- **Why:** Acute appendicitis is inflammation of the vermiform appendix, usually triggered by obstruction of its lumen.
- **Don't confuse with:**
  - Acute Infectious Gastroenteritis (Acute Diarrhea): Shares abdominal pain, but not typical: right lower abdominal pain (right lower quadrant)
  - Dengue: Shares abdominal pain, but not typical: right lower abdominal pain (right lower quadrant)
  - Hepatitis A: Shares abdominal pain, but not typical: right lower abdominal pain (right lower quadrant)
- **Hint:** Think: Digestive System

**[dz_vs] Tell them apart** · difficulty: clinical · source: `differential_diagnosis` · key: `auto2:disease:acute_appendicitis:dz_vs:mesenteric-adenitis`

- **Front:** Acute Appendicitis vs Mesenteric adenitis: what's the key difference?
- **Answer:** Usually children with a recent viral illness; enlarged mesenteric nodes with a normal appendix on imaging
- **Why:** Acute appendicitis is inflammation of the vermiform appendix, usually triggered by obstruction of its lumen.

**[dz_mech] Mechanism** · difficulty: advanced · source: `pathophysiology` · key: `auto2:disease:acute_appendicitis:dz_mech:1`

- **Front:** Acute Appendicitis: Obstruction of the appendiceal lumen by an appendicolith ([ … ]), lymphoid hyperplasia (most common in children), parasites or tumor raises intraluminal and wall pressure.
- **Full sentence:** Acute Appendicitis: Obstruction of the appendiceal lumen by an appendicolith (fecalith), lymphoid hyperplasia (most common in children), parasites or tumor raises intraluminal and wall pressure.
- **Answer:** fecalith
- **Why:** Venous and lymphatic outflow are blocked, the appendix distends and becomes ischemic, and bacteria such as Escherichia coli, Bacteroides, Peptostreptococcus and Pseudomonas overgrow and invade the wall.
- **Hint:** Starts with “F”

**[dz_redflag] Red flag** · difficulty: clinical · source: `emergency_warning_signs` · key: `auto2:disease:acute_appendicitis:dz_redflag`

- **Front:** In Acute Appendicitis, which finding means urgent care is needed?
  - ✅ High fever with chills — _A warning sign listed for this condition._
  - ▫️ Diarrhea — _A usual symptom of the illness, not a warning sign._
  - ▫️ Epigastric pain — _A usual symptom of the illness, not a warning sign._
  - ▫️ Urinary frequency & urgency — _A usual symptom of the illness, not a warning sign._
- **Answer:** High fever with chills
- **Why:** Suspected appendicitis (abdominal pain migrating to the right lower quadrant with anorexia, nausea or fever) needs same-day emergency assessment for surgical evaluation. Signs of perforation or peritonitis (rigid abdomen, high fever, rapid pulse, low blood pressure) need immediate care.

### Typhoid Fever (disease, 7 cards)

**[dz_picture] Clinical picture** · difficulty: clinical · source: `symptoms` · key: `auto2:disease:typhoid_fever:dz_picture`

- **Front:** A patient has fever, abdominal pain and headache. Most likely diagnosis?
  - ▫️ Acute Appendicitis — _Shares fever and abdominal pain, but not typical: headache_
  - ✅ Typhoid Fever — _Typhoid fever is a systemic infection caused by the exclusively human pathogen Salmonella enterica serovar Typhi._
  - ▫️ Acute Infectious Gastroenteritis (Acute Diarrhea) — _Shares fever and abdominal pain, but not typical: headache_
  - ▫️ Bacterial Meningitis — _Shares fever and headache, but not typical: abdominal pain_
- **Answer:** Typhoid Fever
- **Why:** Typhoid fever is a systemic infection caused by the exclusively human pathogen Salmonella enterica serovar Typhi.
- **Don't confuse with:**
  - Acute Appendicitis: Shares fever and abdominal pain, but not typical: headache
  - Acute Infectious Gastroenteritis (Acute Diarrhea): Shares fever and abdominal pain, but not typical: headache
  - Bacterial Meningitis: Shares fever and headache, but not typical: abdominal pain
- **Hint:** Think: Multisystem (Systemic Infection)

**[dz_vs] Tell them apart** · difficulty: clinical · source: `differential_diagnosis` · key: `auto2:disease:typhoid_fever:dz_vs:malaria`

- **Front:** Typhoid Fever vs Malaria: what's the key difference?
- **Answer:** Paroxysmal fever with rigors after exposure in an endemic area. Parasites on smear or positive RDT
- **Why:** Typhoid fever is a systemic infection caused by the exclusively human pathogen Salmonella enterica serovar Typhi.

**[dz_redflag] Red flag** · difficulty: clinical · source: `emergency_warning_signs` · key: `auto2:disease:typhoid_fever:dz_redflag`

- **Front:** In Typhoid Fever, which finding means urgent care is needed?
  - ▫️ Constipation — _A usual symptom of the illness, not a warning sign._
  - ▫️ Skin rash — _A usual symptom of the illness, not a warning sign._
  - ▫️ Diarrhea — _A usual symptom of the illness, not a warning sign._
  - ✅ Sudden severe abdominal pain, rigidity or distension (possible intestinal perforation) — _A warning sign listed for this condition._
- **Answer:** Sudden severe abdominal pain, rigidity or distension (possible intestinal perforation)
- **Why:** A prolonged or stepwise-rising fever with abdominal symptoms in someone exposed to unsafe water or food warrants prompt evaluation with blood culture. The EMERGENCY tier applies to severe abdominal pain or peritonism (possible perforation), gastrointestinal bleeding, delirium or other altered mental status, or hemodynamic instability, typically in the 2nd-3rd week.

**[dz_tx] Treatment** · difficulty: clinical · source: `medicines` · key: `auto2:disease:typhoid_fever:dz_tx:use`

- **Front:** Which medicine is used for Typhoid Fever?
  - ✅ Ceftriaxone — _IV therapy of choice for severe typhoid or where fluoroquinolone resistance prevails (ineffective against XDR strains)._
  - ▫️ Aspirin (low-dose) — _Listed for Acute Ischemic Stroke, not for Typhoid Fever._
  - ▫️ Oral Rehydration Salts (reduced osmolarity) — _Listed for Acute Infectious Gastroenteritis (Acute Diarrhea), not for Typhoid Fever._
  - ▫️ Propranolol — _Listed for Essential Hypertension, not for Typhoid Fever._
- **Answer:** Ceftriaxone
- **Why:** IV therapy of choice for severe typhoid or where fluoroquinolone resistance prevails (ineffective against XDR strains).
- **Hint:** Think: Antibiotic (third-generation cephalosporin)

### Amoxicillin (medicine, 8 cards)

**[rx_calc] Dose calculation** · difficulty: clinical · source: `doses` · key: `auto2:medicine:med_amoxicillin:rx_calc:typhoid-and-paratyphoid-fever:20`

- **Front:** Child, 20 kg, Typhoid and paratyphoid fever: Amoxicillin dose per intake?
- **Answer:** 667 mg every 8 h (13 mL)
- **Steps:**
    1. 100 mg/kg/day × 20 kg = 2,000 mg a day
    2. ÷ 3 doses = 667 mg per dose
    3. No maximum is listed in Akeso for this row
    4. As 250 mg/5 mL liquid: 13 mL per dose
    5. Practice calculation: always check the prescriber and product insert.
- **Hint:** Work out mg per kg × weight first, then split into the doses.

**[rx_dose] Dose recall** · difficulty: basic · source: `doses` · key: `auto2:medicine:med_amoxicillin:rx_dose:acute-bacterial-sinusitis`

- **Front:** Amoxicillin for Acute bacterial sinusitis (adult): dose and how often?
- **Answer:** 250–500 mg every 8 h (or 750 mg – 1 g every 12 h)
- **Why:** Duration: As short as possible; follow guidelines Also asymptomatic bacteriuria in pregnancy. Adults and children 40 kg and over
- **Hint:** Route: PO

**[rx_class] Drug class** · difficulty: basic · source: `drug_class` · key: `auto2:medicine:med_amoxicillin:rx_class`

- **Front:** Amoxicillin belongs to which drug class?
  - ▫️ Potassium-sparing diuretic (mineralocorticoid receptor antagonist) — _Another drug class in Akeso._
  - ✅ Antibiotic (aminopenicillin) — _Amoxicillin: Antibiotic (aminopenicillin)._
  - ▫️ SGLT2 inhibitor — _Another drug class in Akeso._
  - ▫️ Antiviral (neuraminidase inhibitor) — _Another drug class in Akeso._
- **Answer:** Antibiotic (aminopenicillin)
- **Why:** Used for: infections of the ear, nose and throat (including streptococcal pharyngitis, otitis media).

**[rx_se] Side effects** · difficulty: clinical · source: `adverse` · key: `auto2:medicine:med_amoxicillin:rx_se`

- **Front:** Which is NOT an adverse effect of Amoxicillin?
  - ▫️ Rash (maculopapular rash common in infectious mononucleosis) — _A listed adverse effect of Amoxicillin._
  - ▫️ Diarrhea, nausea, vomiting — _A listed adverse effect of Amoxicillin._
  - ✅ Hypophosphatemia with prolonged high-dose aluminium use — _Listed for Aluminium hydroxide + Magnesium hydroxide, not for Amoxicillin._
  - ▫️ Anaphylaxis and serious hypersensitivity — _A listed adverse effect of Amoxicillin._
- **Answer:** Hypophosphatemia with prolonged high-dose aluminium use
- **Why:** “Hypophosphatemia with prolonged high-dose aluminium use” comes from Aluminium hydroxide + Magnesium hydroxide's list.

### Paracetamol (medicine, 8 cards)

**[rx_calc] Dose calculation** · difficulty: clinical · source: `doses` · key: `auto2:medicine:med_paracetamol:rx_calc:underweight-or-malnourished-child:20`

- **Front:** Child, 20 kg, Underweight or malnourished child: Paracetamol dose per intake?
- **Answer:** 200 mg every 4–6 h, or longer apart
- **Steps:**
    1. 10 mg/kg × 20 kg = 200 mg per dose
    2. Max 60 mg/kg/day = 1,200 mg/day: keep the day's total under it
    3. Practice calculation: always check the prescriber and product insert.
- **Hint:** Work out mg per kg × weight first, then split into the doses.

**[rx_dose] Dose recall** · difficulty: basic · source: `doses` · key: `auto2:medicine:med_paracetamol:rx_dose:fever-mild-to-moderate-pain`

- **Front:** Paracetamol for Fever, mild to moderate pain (adult): dose and how often?
- **Answer:** 500 mg – 1 g every 4–6 h as needed, at least 4 h apart
- **Why:** Duration: As needed Max: 1 g/dose · 4 g/day
- **Hint:** Route: PO

**[rx_class] Drug class** · difficulty: basic · source: `drug_class` · key: `auto2:medicine:med_paracetamol:rx_class`

- **Front:** Paracetamol belongs to which drug class?
  - ▫️ Antiviral (SARS-CoV-2 protease inhibitor, ritonavir-boosted) — _Another drug class in Akeso._
  - ▫️ Antibiotic (aminopenicillin) — _Another drug class in Akeso._
  - ▫️ Mineral supplement (zinc) — _Another drug class in Akeso._
  - ✅ Analgesic / antipyretic (para-aminophenol) — _Paracetamol: Analgesic / antipyretic (para-aminophenol)._
- **Answer:** Analgesic / antipyretic (para-aminophenol)
- **Why:** Used for: mild-to-moderate pain (headache, musculoskeletal pain, dysmenorrhea, toothache).

**[rx_se] Side effects** · difficulty: clinical · source: `adverse` · key: `auto2:medicine:med_paracetamol:rx_se`

- **Front:** Which is NOT an adverse effect of Paracetamol?
  - ✅ Pharyngitis — _Listed for Cetirizine, not for Paracetamol._
  - ▫️ Generally well tolerated at therapeutic doses — _A listed adverse effect of Paracetamol._
  - ▫️ Anaphylaxis and hypersensitivity reactions — _A listed adverse effect of Paracetamol._
  - ▫️ Hepatotoxicity / acute liver failure (overdose, chronic excess, alcohol use) — _A listed adverse effect of Paracetamol._
- **Answer:** Pharyngitis
- **Why:** “Pharyngitis” comes from Cetirizine's list.

### Ciprofloxacin (medicine, 8 cards)

**[rx_calc] Dose calculation** · difficulty: clinical · source: `doses` · key: `auto2:medicine:med_ciprofloxacin:rx_calc:shigellosis-1-month:20`

- **Front:** Child, 20 kg, Shigellosis (≥1 month): Ciprofloxacin dose per intake?
- **Answer:** 300 mg 2× a day (150 mL)
- **Steps:**
    1. 15 mg/kg × 20 kg = 300 mg per dose
    2. 2 doses a day = 600 mg a day
    3. Max 500 mg/dose: within the limit
    4. As 400 mg/200 mL liquid: 150 mL per dose
    5. Practice calculation: always check the prescriber and product insert.
- **Hint:** Work out mg per kg × weight first, then split into the doses.

**[rx_dose] Dose recall** · difficulty: basic · source: `doses` · key: `auto2:medicine:med_ciprofloxacin:rx_dose:uncomplicated-cystitis`

- **Front:** Ciprofloxacin for Uncomplicated cystitis (adult): dose and how often?
- **Answer:** 250–500 mg 2× a day
- **Why:** Duration: 3 days Pre-menopausal women: a single 500 mg dose may be used
- **Hint:** Route: PO

**[rx_class] Drug class** · difficulty: basic · source: `drug_class` · key: `auto2:medicine:med_ciprofloxacin:rx_class`

- **Front:** Ciprofloxacin belongs to which drug class?
  - ▫️ Antiplatelet (salicylate) — _Another drug class in Akeso._
  - ▫️ Antidiarrheal (opioid receptor agonist) — _Another drug class in Akeso._
  - ▫️ Biguanide antidiabetic — _Another drug class in Akeso._
  - ✅ Antibiotic (fluoroquinolone) — _Ciprofloxacin: Antibiotic (fluoroquinolone)._
- **Answer:** Antibiotic (fluoroquinolone)
- **Why:** Used for: complicated urinary tract infections and pyelonephritis.

**[rx_se] Side effects** · difficulty: clinical · source: `adverse` · key: `auto2:medicine:med_ciprofloxacin:rx_se`

- **Front:** Which is NOT an adverse effect of Ciprofloxacin?
  - ✅ Acute kidney injury from crystal nephropathy (mainly high-dose IV therapy, dehydration or pre-existing renal impairment) — _Listed for Aciclovir, not for Ciprofloxacin._
  - ▫️ Nausea, diarrhea, vomiting, rash; abnormal liver function tests — _A listed adverse effect of Ciprofloxacin._
  - ▫️ Peripheral neuropathy (boxed) — _A listed adverse effect of Ciprofloxacin._
- **Answer:** Acute kidney injury from crystal nephropathy (mainly high-dose IV therapy, dehydration or pre-existing renal impairment)
- **Why:** “Acute kidney injury from crystal nephropathy (mainly high-dose IV therapy, dehydration or pre-existing renal impairment)” comes from Aciclovir's list.

### Azithromycin (medicine, 8 cards)

**[rx_calc] Dose calculation** · difficulty: clinical · source: `doses` · key: `auto2:medicine:med_azithromycin:rx_calc:acute-otitis-media-6-mo:20`

- **Front:** Child, 20 kg, Acute otitis media (≥6 mo): Azithromycin dose per intake?
- **Answer:** 600 mg single dose (15 mL)
- **Steps:**
    1. 30 mg/kg × 20 kg = 600 mg per dose
    2. 1 dose a day = 600 mg a day
    3. Max 1,500 mg/dose: within the limit
    4. As 200 mg/5 mL liquid: 15 mL per dose
    5. Practice calculation: always check the prescriber and product insert.
- **Hint:** Work out mg per kg × weight first, then split into the doses.

**[rx_dose] Dose recall** · difficulty: basic · source: `doses` · key: `auto2:medicine:med_azithromycin:rx_dose:cap-sinusitis-pharyngitis-skin-infection`

- **Front:** Azithromycin for CAP, sinusitis, pharyngitis, skin infections (adult): dose and how often?
- **Answer:** 500 mg once a day
- **Why:** Duration: 3 days Max: 1.5 g/course Or 500 mg day 1, then 250 mg days 2–5
- **Hint:** Route: PO

**[rx_class] Drug class** · difficulty: basic · source: `drug_class` · key: `auto2:medicine:med_azithromycin:rx_class`

- **Front:** Azithromycin belongs to which drug class?
  - ▫️ Oral iron replacement — _Another drug class in Akeso._
  - ✅ Antibiotic (macrolide) — _Azithromycin: Antibiotic (macrolide)._
  - ▫️ Biguanide antidiabetic — _Another drug class in Akeso._
  - ▫️ Antiplatelet (P2Y12 inhibitor) — _Another drug class in Akeso._
- **Answer:** Antibiotic (macrolide)
- **Why:** Used for: community-acquired pneumonia (including atypical pathogens).

**[rx_se] Side effects** · difficulty: clinical · source: `adverse` · key: `auto2:medicine:med_azithromycin:rx_se`

- **Front:** Which is NOT an adverse effect of Azithromycin?
  - ▫️ Diarrhea, nausea, abdominal pain — _A listed adverse effect of Azithromycin._
  - ✅ GI ulceration, bleeding and perforation — _Listed for Ibuprofen, not for Azithromycin._
  - ▫️ Exacerbation of myasthenia gravis — _A listed adverse effect of Azithromycin._
  - ▫️ QT prolongation and torsades de pointes — _A listed adverse effect of Azithromycin._
- **Answer:** GI ulceration, bleeding and perforation
- **Why:** “GI ulceration, bleeding and perforation” comes from Ibuprofen's list.

### Abdominal pain (symptom, 1 cards)

**[sx_cause] Causes** · difficulty: basic · source: `causes` · key: `auto2:symptom:sym_abdominal_pain:sx_cause`

- **Front:** Which is a common cause of abdominal pain?
  - ✅ Acute pancreatitis — _Listed as a cause of abdominal pain._
  - ▫️ Migraine aura — _A cause of blurred vision, not listed for abdominal pain._
  - ▫️ Cluster headache — _A cause of headache, not listed for abdominal pain._
  - ▫️ Hematuria — _A cause of dark urine, not listed for abdominal pain._
- **Answer:** Acute pancreatitis
- **Why:** Other causes listed: gastroenteritis, constipation or gas and peptic ulcer disease or gastritis.
- **Hint:** Think: Digestive System

### Cough (symptom, 1 cards)

**[sx_cause] Causes** · difficulty: basic · source: `causes` · key: `auto2:symptom:sym_cough:sx_cause`

- **Front:** Which is a common cause of cough?
  - ▫️ Metastatic cancer — _A cause of swollen lymph nodes (lymphadenopathy), not listed for cough._
  - ▫️ Meckel's diverticulum (children) — _A cause of blood in stool (hematochezia), not listed for cough._
  - ▫️ Appendicitis — _A cause of abdominal pain, not listed for cough._
  - ✅ Heart failure — _Listed as a cause of cough._
- **Answer:** Heart failure
- **Why:** Other causes listed: upper respiratory tract infection, acute bronchitis or pneumonia and asthma.
- **Hint:** Think: Respiratory System

## Content gaps (for a content batch)

- Diseases with **no differential distinguishing features** (no tell-apart cards): 0
- Diseases with **no mechanism cloze** (no short mechanism sentence or no clear term): 32 of 40
- Diseases with **no "avoid" medicine link**: 17 of 40
- Diseases with **no red-flag card** (no red flags, or fewer than 2 symptoms that are clearly not red flags): 1 of 40
- Medicines with weight-based child doses but **no calculation card** (ambiguous strings such as "40–90 mg/kg/day, divided", frequency ranges, or complex maximums): 14: Benzathine Penicillin G, Co-trimoxazole (Sulfamethoxazole + Trimethoprim), Ethambutol, Ferrous Sulfate, Hydrochlorothiazide, Ibuprofen, Ivermectin, Losartan, Metoprolol, Oral Rehydration Salts (reduced osmolarity), Prednisone, Pyrazinamide, Rabies Immunoglobulin (HRIG / ERIG), Spironolactone
- **No diagnostic criteria field** on diseases (e.g. Jones criteria), which `dz_feature` needs.
- Medicines have **no description field**: `rx_class` explains with the first indication instead.

## Things to decide

- **Dose calculation without a listed maximum:** the spec asks for rows "with a parseable max". Many child rows (e.g. amoxicillin for typhoid) list none. These cards are built and say "No maximum is listed in Akeso for this row". Say if you'd rather skip them.
- `dz_picture` adds one context sentence when the clinicopathologic text has a timing or trigger (e.g. "Symptoms begin about 2-4 weeks after the sore throat."), and only if it doesn't name the disease.
- Distractors are filtered more strictly than the spec asks: a distractor that shares a key word with a true fact ("Leg swelling" vs the red flag "Swelling of the legs") is dropped, and treatment distractors never come from the same drug family as this disease's medicines.

_34 sample cards shown._