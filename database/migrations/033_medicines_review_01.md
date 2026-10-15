# Medicine review b01: review sheet

Run `033_medicines_review_01.sql` in Supabase after you have checked this. Everything below is ADDED; the existing text stays as it is.

Every link was opened twice: by the research step (to read the fact), and again in Akeso's own browser pane on your computer in the Philippines (to make sure it opens for you, not just from the cloud). See NOTES.md in the batch folder for any link that needs attention.

UK SmPC links open the official MHRA Products search (free) for that medicine: the emc site (medicines.org.uk) now limits free page views for users outside the UK. The citation still names the exact product and PL number to pick.

## Please check (batch 01)

**Links (checked from your computer, 2026-10-13):** all 37 opened, except two:

- The DOH dengue guideline PDF (`doh.gov.ph/.../ao2012-0026-1.pdf`) first shows a Cloudflare "security verification" page. A normal browser usually passes it automatically; Akeso's browser may ask you to wait or tick the box.
- The 2020 Philippine dyslipidemia CPG download link started a file download instead of opening, so it now points to the article page (`asean-endocrinejournal.org/.../article/view/927`), which opens.
- The old FDA PH insert link for amoxicillin (DRP-10727) is still 404, and is no longer used.

**Medical points to confirm:**

1. **Atorvastatin → hepatitis A, *avoid*:** the label contraindicates atorvastatin in *active liver disease*. Applying that to acute hepatitis A is a reasonable reading, but no source names hepatitis A. Change it to *caution* if you prefer.
2. **Allopurinol, "Allujen" (PH brand):** this only appears in an FDA PH recall advisory (2018-190, one lot). It is a real PH-registered brand, but the source is a recall notice. Remove it if you don't want that.
3. **Allopurinol dose rows:** these follow the US label (max 800 mg/day). The UK label allows 700–900 mg/day in severe disease. The UK label also says don't start during an attack, while Merck allows starting with anti-inflammatory cover. Both are in one "How to give it" note.
4. **Azithromycin:** typhoid, cholera, trachoma, leptospirosis and pertussis doses come from MSF Essential Drugs (2025). I found no Philippine guideline page that opened.
5. **Artemether-lumefantrine:** the CDC (US) now lists a 5-day course for falciparum. It was left out because WHO and DOH practice is the 3-day, 6-dose course. The DOH order (AO 2009-0001) is from a legal database (lawyerly.ph), because no DOH copy opened.
6. **Benzathine penicillin:** no PNF listing could be read (the PNF PDF text stops at "M"). The PH form note comes from the PhilHealth RF/RHD checklist instead (1.2 million units vial, IM). The NZ weight cut-off for prophylaxis is 20 kg (≥20 kg 1.2 MU, <20 kg 600,000 U); the existing paragraph says 27 kg (that is the US pharyngitis cut-off).
7. **No Philippine brands** could be verified for the other medicines (no FDA PH insert opened), so brands were not added.


---

## Aciclovir  (`med_aciclovir`)

**Description (kept)**

Aciclovir is a synthetic purine (guanosine) nucleoside analogue that is phosphorylated by viral and host cellular enzymes to aciclovir triphosphate, which inhibits herpesvirus DNA polymerase and terminates viral DNA chain elongation. Its selectivity for infected cells makes it active against herpes simplex virus types 1 and 2 and varicella-zoster virus. It is used for genital and mucocutaneous herpes, herpes zoster, varicella and, intravenously, herpes simplex encephalitis.

**Description (added)**

Oral bioavailability is only 10–20%, and the drug is excreted mainly unchanged by the kidneys with a half-life of about 3 hours that lengthens to about 19.5 hours in chronic renal failure, which explains the frequent oral dosing and the need for renal dose reduction. Cerebrospinal fluid levels reach about 50% of plasma levels. In the Philippines, aciclovir is on the PNF Essential Medicines List as tablets, oral suspension and an injection for IV infusion.

**Uses**: 5 kept, 2 added

- NEW: Prophylaxis of herpes simplex infections in immunocompromised patients
- NEW: Herpes simplex in people with HIV: episodic treatment and long-term suppression

**Side effects**: 7 kept, 6 added

- NEW: Pruritus and rash, including photosensitivity
- NEW: Dizziness, abdominal pain, fatigue and fever
- NEW: Urticaria and accelerated diffuse hair loss (uncommon)
- NEW: Anaphylaxis, angioedema and dyspnoea (rare)
- NEW: Reversible rises in bilirubin and liver enzymes; very rarely hepatitis and jaundice
- NEW: Anaemia, leukopenia and thrombocytopenia (very rare)

**Precautions**: 4 kept, 3 added

- NEW: Elderly patients: higher risk of neurological adverse effects; monitor closely (precaution)
- NEW: Breastfeeding: excreted in breast milk at 0.6–4.1 times plasma levels; use with caution (precaution)
- NEW: Repeated or prolonged courses in severely immunocompromised patients may select less sensitive virus strains (precaution)

**Interactions**: 4 kept, 3 added

- NEW: Cimetidine: increases aciclovir AUC by reducing its renal clearance.
- NEW: Mycophenolate mofetil: increases the AUC of aciclovir and of its inactive metabolite; no dose adjustment needed.
- NEW: Theophylline: AUC increased by about 50%; measure theophylline levels during co-therapy.

**Disease links added**

- `hiv_infection`: **safe**: CDC 2021 STI guideline gives aciclovir regimens for episodic and suppressive HSV therapy in people with HIV
- `chronic_kidney_disease`: **caution**: Renally excreted (half-life about 19.5 h in chronic renal failure); dose reduction needed and higher risk of neurotoxicity

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=aciclovir#emc-11673): Aciclovir 200 mg Tablets – Summary of Product Characteristics. Milpharm Limited (PL 16363/0556). Electronic Medicines Compendium (emc), medicines.org.uk.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- [CDC STI Treatment Guidelines](https://www.cdc.gov/std/treatment-guidelines/herpes.htm): Centers for Disease Control and Prevention. Genital Herpes. Sexually Transmitted Infections Treatment Guidelines, 2021.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=aciclovir#emc-11673: SmPC 4.1 incl. prophylaxis in immunocompromised; 4.4 elderly/renal neurological risk, resistance with prolonged courses in immunocompromised; 4.5 cimetidine, mycophenolate (no dose adjustment), theophylline AUC ~50% (measure levels); 4.6 breast milk 0.6–4.1x plasma, caution; 4.8 adverse reactions by frequency; 5.2 bioavailability 10–20%, CSF ~50%, half-life 2.8–4.1 h, ~19.5 h in chronic renal failure
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Aciclovir listed: 200/400/800 mg tablet, 200 mg/5 mL suspension, 25 mg/mL 10 mL vial (IV infusion); edition details
- https://www.cdc.gov/std/treatment-guidelines/herpes.htm: Aciclovir regimens for persons with HIV: suppressive 400–800 mg 2–3x daily; episodic 400 mg 3x daily 5–10 days; believed safe in all trimesters
- https://products.mhra.gov.uk/search/?search=aciclovir#emc-4334: Second aciclovir SmPC (Sun Pharma): confirmed same interaction list; not used as a ref

---

## Allopurinol  (`med_allopurinol`)

**Description (kept)**

Allopurinol and its active metabolite oxypurinol inhibit xanthine oxidase, reducing production of uric acid. Lowering serum urate below 6 mg/dL dissolves urate crystals over time, preventing flares, tophi and joint damage. It is the preferred first-line urate-lowering drug in gout, including in chronic kidney disease, started at a low dose and increased gradually.

**Description (added)**

Allopurinol is not a treatment for an acute gout attack and plain asymptomatic hyperuricaemia is generally not an indication for it; it is also used to prevent uric acid build-up during cancer chemotherapy and for rare 2,8-dihydroxyadenine stones. In the Philippines it is listed in the PNF Essential Medicines List as 100 mg and 300 mg tablets.

**Uses**: 3 kept, 1 added

- NEW: 2,8-dihydroxyadenine (2,8-DHA) kidney stones in adenine phosphoribosyltransferase (APRT) deficiency

**Side effects**: 5 kept, 4 added

- NEW: Raised TSH (thyroid-stimulating hormone) on long-term treatment
- NEW: Drowsiness
- NEW: Hepatitis (rare)
- NEW: Blood disorders: agranulocytosis, aplastic anaemia, thrombocytopenia, bone marrow depression (very rare)

**Interactions**: 4 kept, 9 added

- NEW: Didanosine: allopurinol roughly doubles didanosine exposure; combination generally not recommended.
- NEW: Ciclosporin: ciclosporin levels may rise; watch for toxicity.
- NEW: Theophylline: metabolism inhibited; check theophylline levels when starting or increasing allopurinol.
- NEW: Chlorpropamide: risk of prolonged hypoglycaemia, especially with poor kidney function.
- NEW: Cytotoxics (e.g., cyclophosphamide, doxorubicin): blood dyscrasias more frequent; monitor blood counts.
- NEW: ACE inhibitors: higher risk of hypersensitivity reactions, especially in kidney impairment.
- NEW: Salicylates and uricosurics (e.g., probenecid): may speed oxipurinol excretion and reduce allopurinol's effect.
- NEW: Aluminium hydroxide antacids: may reduce allopurinol's effect; separate doses by at least 3 hours.
- NEW: Vidarabine: half-life of vidarabine increased; watch for toxicity.

**Brands (PH)**: 0 kept, 1 added

- NEW: Allujen

**Brands (intl)**: 1 kept, 1 added

- NEW: Zyloric

**Disease links added**

- `chronic_kidney_disease`: **caution**: Kidney impairment raises adverse-effect risk; start low (e.g., 50 mg) and cap the dose by creatinine clearance.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Gout (starting dose) (Increase by 100 mg weekly until serum urate ≤ 6 mg/dL) | PO | 100 mg | Once a day | Long-term | — | Label · US DailyMed |
| adult | Gout, mild (maintenance) (Doses above 300 mg/day given in divided doses) | PO | 200–300 mg/day | Once a day | Long-term | 800 mg/day | Label · US DailyMed |
| adult | Gout, moderately severe tophaceous | PO | 400–600 mg/day | Divided doses | Long-term | 800 mg/day | Label · US DailyMed |
| adult | Prevention of tumour lysis (cancer therapy) (With high fluid intake) | PO | 600–800 mg/day | Divided doses | 2–3 days | 800 mg/day | Label · US DailyMed |
| adult | Recurrent calcium oxalate stones | PO | 200–300 mg/day | Once a day or divided | Long-term | — | Label · US DailyMed |
| adult | Haemodialysis (2–3× a week) (None in between dialysis sessions) | PO | 300–400 mg | After each dialysis | Long-term | — | Label · UK SmPC |
| child | Cancer therapy / hyperuricaemic states (under 15 y) (Use in children is rarely indicated) | PO | 10–20 mg/kg/day | Once a day | As needed | 400 mg/day | Label · UK SmPC |
| child | Cancer therapy, 6–10 years | PO | 300 mg/day | Once a day | As needed | — | Label · US DailyMed |
| child | Cancer therapy, under 6 years | PO | 150 mg/day | Once a day | As needed | — | Label · US DailyMed |

- *renal* CrCl 10–20: 200 mg a day is suitable. [Label · US DailyMed]
- *renal* CrCl < 10: Do not exceed 100 mg a day. [Label · US DailyMed]
- *renal* CrCl < 3: The dosing interval may also need to be lengthened. [Label · US DailyMed]
- *renal* CrCl < 60: Some clinicians start at 50 mg once a day; supporting data are limited. [Merck Manual]
- *hepatic*: Use reduced doses in hepatic impairment; do periodic liver function tests early in treatment. [Label · UK SmPC]
- *elderly*: Use the lowest dose that gives satisfactory urate reduction. [Label · UK SmPC]
- *pregnancy*: Inadequate evidence of safety in human pregnancy; use only when no safer alternative exists. Use during breastfeeding is not recommended (allopurinol and oxipurinol pass into breast milk). [Label · UK SmPC]
- *administration*: Take once daily after a meal; split the dose if over 300 mg/day causes stomach upset. Drink enough fluid for at least 2 L of urine a day. [Label · UK SmPC]
- *administration*: The UK label advises waiting until an acute attack has fully subsided before starting; Merck notes it can be started during a flare if anti-inflammatory cover is given. [Merck Manual]
- *forms_ph*: Oral: 100 mg and 300 mg tablet. [PNF]
- *monitor*: Serum urate to guide dose titration; liver function tests in the early months; BUN and serum creatinine in kidney impairment; blood counts with cytotoxics or azathioprine; TSH on long-term use; stop at the first sign of rash. [Label · UK SmPC]

**References added**

- [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List. 2022.
- [UK SmPC – Allopurinol Tablets BP 100mg](https://products.mhra.gov.uk/search/?search=allopurinol#emc-7004): Milpharm Ltd. Allopurinol Tablets BP 100mg – Summary of Product Characteristics. electronic medicines compendium (emc).
- [DailyMed – Zyloprim (allopurinol) tablet label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=342832b5-1a32-4bea-bc49-ab0fd152154e): ZYLOPRIM (allopurinol) tablet – prescribing information. DailyMed, U.S. National Library of Medicine.
- [Merck Manual Professional – Gout](https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout): Merck Manual Professional Version. Gout. Musculoskeletal and Connective Tissue Disorders: Crystal-Induced Arthritides.
- [FDA Philippines Advisory No. 2018-190](https://www.fda.gov.ph/?p=1608): Food and Drug Administration Philippines. FDA Advisory No. 2018-190: recall of one lot of Allopurinol 300 mg tablet (Allujen).
- Dosing source `PNF`: [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List. 2022.
- Dosing source `Label · US DailyMed`: [DailyMed – Zyloprim (allopurinol) tablet label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=342832b5-1a32-4bea-bc49-ab0fd152154e): ZYLOPRIM (allopurinol) tablet – prescribing information. DailyMed, U.S. National Library of Medicine.
- Dosing source `Label · UK SmPC`: [UK SmPC – Allopurinol Tablets BP 100mg](https://products.mhra.gov.uk/search/?search=allopurinol#emc-7004): Milpharm Ltd. Allopurinol Tablets BP 100mg – Summary of Product Characteristics. emc.
- Dosing source `Merck Manual`: [Merck Manual Professional – Gout](https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout): Merck Manual Professional Version. Gout.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Allopurinol listed: Oral 100 mg and 300 mg tablet; no restrictions noted.
- https://products.mhra.gov.uk/search/?search=allopurinol#emc-7004: Indications incl. 2,8-DHA stones; start 100 mg/day; children <15 y 10–20 mg/kg/day max 400 mg; elderly lowest dose; severe renal <100 mg/day; reduced dose in hepatic impairment + LFTs; haemodialysis 300–400 mg after each dialysis; once daily after meal; do not start until acute attack subsided; asymptomatic hyperuricaemia not an indication; TSH rise; interactions (didanosine, ciclosporin, theophylline, chlorpropamide, cytotoxics, ACE inhibitors, salicylates/probenecid, aluminium hydroxide 3 h, vidarabine); pregnancy inadequate evidence, breastfeeding not recommended; ADRs (raised TSH, hepatitis, agranulocytosis/aplastic anaemia/thrombocytopenia).
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=342832b5-1a32-4bea-bc49-ab0fd152154e: Zyloprim: start 100 mg, increase weekly by 100 mg to urate ≤6 mg/dL; mild 200–300 mg/day, moderately severe tophaceous 400–600 mg/day; max 800 mg; >300 mg divided; cancer therapy 600–800 mg/day 2–3 days with fluids; children 6–10 y 300 mg, <6 y 150 mg; calcium oxalate stones 200–300 mg/day; CrCl 10–20: 200 mg, <10: ≤100 mg, <3: lengthen interval; urine output ≥2 L; drowsiness; bone marrow depression; LFTs early; BUN/creatinine in renal impairment; present in breast milk.
- https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout: Start 50–100 mg once daily, up to 800 mg; 50 mg if CrCl <60 (limited data); adverse effects more common in renal dysfunction; can start during flare with anti-inflammatory therapy.
- https://www.fda.gov.ph/?p=1608: FDA PH Advisory 2018-190 names 'ALLOPURINOL 300 MG TABLET (ALLUJEN)' (lot recall) - brand present in PH.
- https://www.hpra.ie/find-a-medicine/for-human-use/authorised-medicines/details/24619: Zyloric 100 mg tablets, allopurinol, Aspen Pharma Trading Ltd (brand_intl).

---

## Aluminium hydroxide + Magnesium hydroxide  (`med_aluminium_magnesium_hydroxide`)

**Description (kept)**

A combination antacid that neutralizes gastric acid already secreted, giving fast but short-lived relief of heartburn and dyspepsia. Aluminium hydroxide also inhibits pepsin and tends to constipate, while magnesium hydroxide tends to loosen the stool, so combining them balances the effect on bowel habit. Antacids are suited to mild, intermittent reflux symptoms.

**Description (added)**

It is a local, non-absorbed treatment for symptoms and does not heal ulcers or treat their cause, so persistent symptoms beyond about 2 weeks call for medical review. Its main practical problem is binding many other oral drugs in the gut, which reduces their absorption. In the Philippines it is on the PNF Essential Medicines List as a suspension (225 mg + 200 mg per 5 mL) and a tablet (200 mg + 100 mg).

**Uses**: 3 kept, 1 added

- NEW: Gastritis and gastric hyperacidity

**Side effects**: 3 kept, 2 added

- NEW: Abdominal pain
- NEW: Hypermagnesaemia in young children, especially with kidney impairment or dehydration

**Precautions**: 2 kept, 2 added

- NEW: Severely debilitated patients
- NEW: Hereditary fructose intolerance (sorbitol-containing suspensions)

**Interactions**: 4 kept, 5 added

- NEW: Chloroquine, digoxin, gabapentin, itraconazole and atazanavir: reduced absorption; separate by at least 2 hours.
- NEW: Velpatasvir: reduced absorption; separate by 4 hours.
- NEW: Allopurinol: aluminium hydroxide may reduce its effect; separate by at least 3 hours.
- NEW: Salicylates: urine alkalinisation by magnesium hydroxide increases salicylate excretion.
- NEW: Vitamins: absorption reduced; do not take at the same time.

**Brands (intl)**: 2 kept, 1 added

- NEW: Mucogel

**Disease links added**

- `peptic_ulcer_disease`: **safe**: Symptomatic relief of ulcer and gastritis pain (adjunct; does not heal the ulcer).
- `hiv_infection`: **caution**: Reduces absorption of dolutegravir and atazanavir; time doses apart.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Dyspepsia, heartburn, ulcer/gastritis pain (suspension ~220 mg + 195 mg/5 mL) (20 min–1 h after meals, or as required; also for ages 12+) | PO | 10–20 mL | 3× a day + at bedtime | As needed | — | Label · UK SmPC |
| adult | Acid indigestion, heartburn (suspension 200 mg + 200 mg/5 mL) (Also for ages 12+) | PO | 10–20 mL | 4× a day | ≤ 2 weeks at max dose | 80 mL/day | Label · US DailyMed |
| adult | Gastritis / peptic ulcer pain (chewable tablet 400 mg + 400 mg) (Or 1 tablet during painful episodes) | PO | 1–2 tablets | 3× a day | By clinical response | — | MSF |
| child | Gastritis / peptic ulcer pain, over 5 years (tablet 400 mg + 400 mg) (Rarely indicated) | PO | ½ tablet | 3× a day | By clinical response | — | MSF |

- *renal*: Ask a doctor before use with kidney disease or a magnesium-restricted diet. [Label · US DailyMed]
- *elderly*: Same dose as adults. [Label · UK SmPC]
- *pregnancy*: MSF lists no contraindication in pregnancy or breastfeeding; the UK label notes no clinical data for its product and advises caution in pregnancy. [MSF]
- *administration*: Shake suspension well; chew tablets thoroughly. Strengths differ between products, so dose by the product's own label. [MSF]
- *administration*: Children under 12: not recommended for some suspensions (UK label) or only on a doctor's advice (US OTC label). [Label · UK SmPC]
- *forms_ph*: Oral: 225 mg aluminium hydroxide + 200 mg magnesium hydroxide per 5 mL suspension (60 mL, 120 mL); 200 mg aluminium hydroxide + 100 mg magnesium hydroxide tablet. [PNF]
- *monitor*: Symptom relief; refer if symptoms last more than 2 weeks. Check the timing of other oral medicines (antibiotics, iron, antiretrovirals, levothyroxine). [Label · US DailyMed]

**References added**

- [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List. 2022.
- [UK SmPC – Mucogel Suspension](https://products.mhra.gov.uk/search/?search=aluminium+hydroxide#emc-13356): Rosemont Pharmaceuticals Ltd. Mucogel Suspension – Summary of Product Characteristics. electronic medicines compendium (emc); updated 01-Mar-2022.
- [MSF Essential Drugs – Aluminium hydroxide/Magnesium hydroxide oral](https://medicalguidelines.msf.org/en/viewport/EssDr/english/aluminium-hydroxide-magnesium-hydroxide-oral-16685025.html): Médecins Sans Frontières. Essential drugs – practical guidelines: Aluminium hydroxide/Magnesium hydroxide, oral.
- [DailyMed – Kesin Mag-Al suspension (OTC label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42df2198-14dc-da1c-e063-6394a90a1ae6): KESIN MAG-AL (aluminum and magnesium hydroxide suspension) – OTC drug label. DailyMed, U.S. National Library of Medicine.
- Dosing source `PNF`: [Philippine National Formulary – Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List. 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC – Mucogel Suspension](https://products.mhra.gov.uk/search/?search=aluminium+hydroxide#emc-13356): Rosemont Pharmaceuticals Ltd. Mucogel Suspension (220 mg dried aluminium hydroxide + 195 mg magnesium hydroxide per 5 mL) – SmPC. emc.
- Dosing source `MSF`: [MSF Essential Drugs – Aluminium hydroxide/Magnesium hydroxide oral](https://medicalguidelines.msf.org/en/viewport/EssDr/english/aluminium-hydroxide-magnesium-hydroxide-oral-16685025.html): Médecins Sans Frontières. Essential drugs – practical guidelines: Aluminium hydroxide/Magnesium hydroxide, oral (400 mg + 400 mg chewable tablet).
- Dosing source `Label · US DailyMed`: [DailyMed – Kesin Mag-Al suspension (OTC label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42df2198-14dc-da1c-e063-6394a90a1ae6): KESIN MAG-AL (200 mg aluminum hydroxide + 200 mg magnesium hydroxide per 5 mL) – OTC drug label. DailyMed.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Aluminum hydroxide + magnesium hydroxide: oral suspension 225 mg + 200 mg per 5 mL (60 mL, 120 mL); tablet 200 mg + 100 mg.
- https://products.mhra.gov.uk/search/?search=aluminium+hydroxide#emc-13356: Mucogel: 44 mg dried Al(OH)3 + 39 mg Mg(OH)2 per mL; indications incl. gastric/duodenal ulcer, gastritis, hyperacidity, heartburn, reflux; adults and elderly 10–20 mL 3× daily 20 min–1 h after meals and at bedtime or as required; not under 12 y; not in severely debilitated or kidney failure; hypermagnesaemia in young children (renal impairment/dehydration); sorbitol – hereditary fructose intolerance; tetracyclines and vitamins absorption reduced; salicylate excretion increased; no pregnancy data, caution; abdominal pain (frequency not known).
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/aluminium-hydroxide-magnesium-hydroxide-oral-16685025.html: 400/400 mg chewable tablet; adults 1–2 tab 3× daily after meals or 1 tab in painful episodes; children >5 y ½ tab 3× daily (rarely indicated); interactions: atazanavir, chloroquine, digoxin, doxycycline, iron, gabapentin, itraconazole, levothyroxine 2 h; ciprofloxacin; dolutegravir 2 h before/6 h after; velpatasvir 4 h; no contraindication in pregnancy/breastfeeding; tablets chewed.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42df2198-14dc-da1c-e063-6394a90a1ae6: 200 mg + 200 mg per 5 mL; adults/children 12+ 2–4 tsp 4× daily; max 16 tsp (80 mL)/24 h; max dose not >2 weeks; ask doctor if kidney disease or magnesium-restricted diet; stop if symptoms >2 weeks; under 12 consult physician; shake well.
- https://products.mhra.gov.uk/search/?search=aluminium+hydroxide#emc-7004: Allopurinol SmPC: aluminium hydroxide may reduce allopurinol effect; separate by at least 3 hours.

---

## Amlodipine  (`med_amlodipine`)

**Description (kept)**

Amlodipine is a long-acting dihydropyridine calcium channel blocker that inhibits L-type calcium channels in vascular smooth muscle, causing arterial vasodilation and a fall in peripheral resistance and blood pressure. Its long half-life allows once-daily dosing. It is a first-line antihypertensive and is also used for chronic stable and vasospastic angina.

**Description (added)**

In the Philippines it is listed in the PNF Essential Medicines List (5 mg and 10 mg tablets) and is the first drug in the national primary-care hypertension protocol, with losartan added if blood pressure stays above target. Amlodipine is not removed by dialysis, and the usual dose is used in renal impairment.

**Side effects**: 8 kept, 6 added

- NEW: Abdominal pain and nausea
- NEW: Gingival hyperplasia (very rare)
- NEW: Hepatitis, jaundice and raised liver enzymes, mostly cholestatic (very rare)
- NEW: Extrapyramidal disorder (exceptional reports)
- NEW: Angioedema, Stevens-Johnson syndrome and erythema multiforme (very rare)
- NEW: Overdose: marked prolonged hypotension and non-cardiogenic pulmonary oedema (may appear 24–48 h after ingestion)

**Precautions**: 1 kept, 5 added

- NEW: Hypersensitivity to other dihydropyridines
- NEW: Severe hypotension
- NEW: Shock, including cardiogenic shock
- NEW: Left ventricular outflow obstruction (e.g., high-grade aortic stenosis)
- NEW: Haemodynamically unstable heart failure after acute myocardial infarction

**Interactions**: 4 kept, 5 added

- NEW: Diltiazem and verapamil (CYP3A4 inhibitors): increased amlodipine exposure and hypotension risk, especially in the elderly.
- NEW: CYP3A4 inducers (rifampicin, St John's wort): may alter amlodipine levels; monitor blood pressure during and after co-administration.
- NEW: Grapefruit or grapefruit juice: not recommended (may increase blood-pressure lowering).
- NEW: IV dantrolene: avoid calcium channel blockers in patients susceptible to or treated for malignant hyperthermia (hyperkalaemia risk).
- NEW: mTOR inhibitors (sirolimus, temsirolimus, everolimus): amlodipine may increase their exposure.

**Disease links added**

- `heart_failure`: **caution**: Use with caution: more pulmonary oedema in NYHA III–IV trial; contraindicated in unstable heart failure after acute MI.
- `acute_coronary_syndrome`: **caution**: Contraindicated in haemodynamically unstable heart failure after acute MI and in cardiogenic shock.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Hypertension (Increase by response) | PO | 5 mg | Once a day | Long-term | 10 mg/day | Label · UK SmPC |
| adult | Chronic stable or vasospastic angina | PO | 5 mg | Once a day | Long-term | 10 mg/day | Label · UK SmPC |
| adult | Hypertension (PH primary care) (Step 1: 5 mg; step 2: add losartan 50 mg; step 3: amlodipine 10 mg + losartan 100 mg (1-month intervals)) | PO | 5 mg, then 10 mg | Once a day | Long-term | 10 mg/day | PH HTN protocol |
| child | Hypertension (6–17 years) (May increase to 5 mg after 4 weeks; no data under 6 years) | PO | 2.5 mg | Once a day | Long-term | 5 mg/day | Label · UK SmPC |

- *renal*: Usual dose. Amlodipine is not removed by dialysis. [Label · UK SmPC]
- *hepatic*: Mild–moderate impairment: start at the low end of the dose range. Severe impairment: start at the lowest dose and titrate slowly (prolonged half-life, higher AUC). [Label · UK SmPC]
- *elderly*: Usual doses apply; increase the dose with care. [Label · UK SmPC]
- *pregnancy*: Safety in pregnancy not established; use only when there is no safer alternative. Excreted in breast milk (infant dose about 3–7% of maternal dose, max 15%). [Label · UK SmPC]
- *administration*: Can be combined with thiazide diuretics, beta-blockers, alpha-blockers or ACE inhibitors. In the PH protocol, amlodipine and losartan are taken together; confirm adherence before stepping up. [PH HTN protocol]
- *forms_ph*: Amlodipine (as besilate/camsylate) 5 mg and 10 mg oral tablets. [PNF]
- *monitor*: Blood pressure and symptoms of hypotension; ankle/peripheral oedema; heart-failure symptoms; slow titration with close monitoring in hepatic impairment. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=amlodipine#emc-2743): Amlodipine 5 mg Tablets. Summary of Product Characteristics. Generics UK Ltd t/a Mylan (Viatris). electronic medicines compendium (emc); text revised 07/2022.
- [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.
- [National Protocol for Hypertension Management (Philippines)](https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf): National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives; 2021 (rev. 2023).
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=amlodipine#emc-2743): Amlodipine 5 mg Tablets SmPC, Generics UK Ltd t/a Mylan; text revised 07/2022.
- Dosing source `PNF`: [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): PNF Essential Medicines List, 2022.
- Dosing source `PH HTN protocol`: [National Protocol for Hypertension Management (Philippines)](https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf): National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF-EML lists 'Amlodipine (as besilate/camsylate) Oral: 5 mg and 10 mg tablet'.
- https://products.mhra.gov.uk/search/?search=amlodipine#emc-2743: Amlodipine 5 mg Tablets SmPC (Mylan/Viatris, rev 07/2022): adult 5 mg od max 10 mg; paediatric 6–17 y 2.5 mg od up to 5 mg after 4 weeks; elderly/hepatic/renal guidance; not dialysable; contraindications (dihydropyridine hypersensitivity, severe hypotension, shock, LVOT obstruction, unstable HF post-MI); interactions (CYP3A4 inhibitors incl. diltiazem/verapamil, inducers rifampicin/St John's wort, grapefruit, dantrolene, tacrolimus, mTOR inhibitors); pregnancy/lactation 3–7%; ADRs incl. gingival hyperplasia, hepatitis/jaundice, extrapyramidal, SJS; overdose non-cardiogenic pulmonary oedema 24–48 h.
- https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf: National Protocol for Hypertension Management in Primary Health Care Settings: step 1 amlodipine 5 mg od; step 2 add losartan 50 mg; step 3 amlodipine 10 mg + losartan 100 mg; step 4 add HCTZ 25 mg or refer; take together; check adherence. (Issuing body not printed in the text; hosted by Resolve to Save Lives.)

---

## Amoxicillin  (`med_amoxicillin`)

**Description (kept)**

Amoxicillin is a bactericidal beta-lactam that binds penicillin-binding proteins and inhibits transpeptidation in bacterial cell-wall synthesis, leading to cell lysis. It is a first-line agent for many respiratory, ENT, skin and urinary infections and a component of H. pylori eradication regimens.

**Description (added)**

Oral bioavailability is about 70% and is not affected by food; the half-life is about 1 hour with mainly renal excretion, and the time the drug level stays above the MIC is the main driver of efficacy. CDC names penicillin or amoxicillin as the antibiotic of choice for group A streptococcal pharyngitis. In the Philippines, amoxicillin is on the PNF Essential Medicines List as 250 mg and 500 mg capsules, paediatric drops and oral suspension.

**Uses**: 6 kept, 6 added

- NEW: Typhoid and paratyphoid fevers
- NEW: Acute pyelonephritis and asymptomatic bacteriuria in pregnancy
- NEW: Dental abscess with spreading cellulitis
- NEW: Lyme disease
- NEW: Prosthetic joint infections
- NEW: Prophylaxis of endocarditis

**Side effects**: 6 kept, 7 added

- NEW: Mucocutaneous candidiasis
- NEW: Blood disorders (very rare): reversible leucopenia, neutropenia, agranulocytosis, thrombocytopenia, haemolytic anaemia
- NEW: Convulsions, more likely with renal impairment, high doses or a seizure history
- NEW: Crystalluria with acute kidney injury (mainly high-dose parenteral use)
- NEW: Jarisch-Herxheimer reaction during Lyme disease treatment
- NEW: Kounis syndrome and drug-induced enterocolitis syndrome (mainly in children)
- NEW: Black hairy tongue

**Precautions**: 1 kept, 3 added

- NEW: Suspected infectious mononucleosis: avoid because of the high risk of rash (precaution)
- NEW: Previous acute generalised exanthematous pustulosis (AGEP) with amoxicillin: do not re-administer
- NEW: Renal impairment: dose adjustment required (precaution)

**Interactions**: 5 kept, 2 added

- NEW: Methotrexate: penicillins may reduce methotrexate excretion and increase its toxicity.
- NEW: Urine glucose tests: false-positive results with chemical methods; use enzymatic glucose oxidase tests.

**Disease links added**

- `typhoid_fever`: **safe**: UK SmPC lists typhoid and paratyphoid fevers as an approved indication (use where the organism is susceptible)
- `chronic_kidney_disease`: **caution**: Mainly renally excreted; dose reduction needed and seizure/crystalluria risk is higher with impaired renal function

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=amoxicillin#emc-526): Amoxicillin 500 mg Capsules – Summary of Product Characteristics. Milpharm Limited (PL 16363/0045). Electronic Medicines Compendium (emc), medicines.org.uk; last updated April 2025.
- [Philippine National Formulary (PNF EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.
- [CDC](https://www.cdc.gov/group-a-strep/hcp/clinical-guidance/strep-throat.html): Centers for Disease Control and Prevention. Clinical Guidance for Group A Streptococcal Pharyngitis. Updated November 18, 2025.
- [Merck Manual Professional](https://www.merckmanuals.com/professional/infectious-diseases/bacteria-and-antibacterial-medications/penicillins): Werth BJ. Penicillins. Merck Manual Professional Edition. Reviewed May 2024.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=amoxicillin#emc-526: SmPC 4.1 incl. typhoid/paratyphoid, pyelonephritis, bacteriuria in pregnancy, dental abscess, prosthetic joint infection, Lyme, endocarditis prophylaxis; 4.4 mononucleosis, AGEP, convulsions, crystalluria, Jarisch-Herxheimer, Kounis, renal adjustment, urine glucose interference; 4.5 methotrexate; 4.8 frequencies; 5.1 time above MIC; 5.2 bioavailability ~70%, food no effect, half-life ~1 h, renal
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Amoxicillin (as trihydrate): 250/500 mg capsule, 100 mg/mL drops 15 mL, 250 mg/5 mL suspension 60 mL
- https://www.cdc.gov/group-a-strep/hcp/clinical-guidance/strep-throat.html: 'Penicillin or amoxicillin is the antibiotic of choice to treat group A strep pharyngitis'; amoxicillin 50 mg/kg once daily (max 1000 mg) x10 days
- https://www.merckmanuals.com/professional/infectious-diseases/bacteria-and-antibacterial-medications/penicillins: Amoxicillin absorption not affected by food, has largely replaced oral ampicillin; penicillin doses must be reduced in severe renal insufficiency

---

## Artemether + Lumefantrine  (`med_artemether_lumefantrine`)

**Description (kept)**

Artemether (and its metabolite dihydroartemisinin) rapidly reduces parasite biomass, while the long-acting lumefantrine eliminates residual parasites; both are thought to interfere with parasite heme detoxification and nucleic acid/protein synthesis. This fixed-dose artemisinin-based combination therapy is a WHO-recommended first-line treatment for uncomplicated P. falciparum malaria.

**Description (added)**

In the Philippines, DOH Administrative Order No. 2009-0001 made artemether-lumefantrine the first-line medicine for confirmed P. falciparum malaria, replacing chloroquine plus sulfadoxine-pyrimethamine, and allows an ACT for all Plasmodium species and mixed infections. It acts on the blood stages of P. vivax but not on the liver hypnozoites, so vivax and ovale infections still need an anti-relapse drug (primaquine or tafenoquine, after G6PD testing).

**Uses**: 2 kept, 2 added

- NEW: Uncomplicated P. malariae and P. knowlesi malaria (CDC treatment tables)
- NEW: Oral follow-on course after IV artesunate for severe malaria, once the patient can take oral medicines (CDC)

**Side effects**: 5 kept, 5 added

- NEW: Palpitations and sleep disorders
- NEW: Rash and pruritus
- NEW: Cough (very common in children)
- NEW: Raised liver function tests (children)
- NEW: Delayed haemolytic anaemia, reported up to a few weeks after treatment

**Precautions**: 2 kept, 5 added

- NEW: Severe malaria (WHO definition), including cerebral malaria: not evaluated
- NEW: Family history of sudden death or congenital QTc prolongation, or other conditions known to prolong QTc
- NEW: Symptomatic arrhythmia, clinically relevant bradycardia or heart failure with reduced ejection fraction
- NEW: Electrolyte disturbances such as hypokalaemia or hypomagnesaemia
- NEW: Use with drugs metabolised by CYP2D6 (e.g., metoprolol, imipramine, amitriptyline, clomipramine)

**Interactions**: 5 kept, 4 added

- NEW: CYP2D6 substrates (e.g., flecainide, metoprolol, imipramine, amitriptyline): contraindicated with artemether-lumefantrine.
- NEW: Lopinavir/ritonavir: raises lumefantrine exposure about 2.3-fold.
- NEW: Nevirapine and efavirenz: markedly reduce artemether exposure; use cautiously with antiretrovirals.
- NEW: Other antimalarials: should not be given concurrently unless no other option exists.

**Disease links added**

- `hiv_infection`: **caution**: Antiretrovirals change exposure (lopinavir/ritonavir raises lumefantrine; nevirapine/efavirenz lower artemether); may reduce efficacy.
- `tuberculosis`: **avoid**: Rifampicin (strong CYP3A4 inducer) sharply lowers artemether/lumefantrine levels; combination is contraindicated.
- `heart_failure`: **avoid**: Contraindicated in heart failure with reduced ejection fraction because of QT/arrhythmia risk.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Uncomplicated malaria (≥35 kg or ≥12 y) (Take with food or a milky drink) | PO | 4 tablets (80/480 mg) | At 0 h and 8 h, then 2× a day | 3 days (6 doses) | 24 tablets/course | WHO PQ |
| child | Uncomplicated malaria, 5 to <15 kg (Tablet may be crushed) | PO | 1 tablet (20/120 mg) | At 0 h and 8 h, then 2× a day | 3 days (6 doses) | 6 tablets/course | WHO PQ |
| child | Uncomplicated malaria, 15 to <25 kg | PO | 2 tablets (40/240 mg) | At 0 h and 8 h, then 2× a day | 3 days (6 doses) | 12 tablets/course | WHO PQ |
| child | Uncomplicated malaria, 25 to <35 kg | PO | 3 tablets (60/360 mg) | At 0 h and 8 h, then 2× a day | 3 days (6 doses) | 18 tablets/course | WHO PQ |
| child | Uncomplicated malaria, ≥35 kg (Same as adult dose) | PO | 4 tablets (80/480 mg) | At 0 h and 8 h, then 2× a day | 3 days (6 doses) | 24 tablets/course | WHO PQ |

- *renal*: No dose adjustment recommended; in severe renal impairment use with caution and monitor ECG and blood potassium. [Label · UK SmPC]
- *hepatic*: No dose adjustment in mild to moderate hepatic impairment; in severe impairment use with caution and monitor ECG and blood potassium. [Label · UK SmPC]
- *elderly*: No information suggesting the dose should differ in patients over 65 years. [Label · UK SmPC]
- *pregnancy*: CDC states artemether-lumefantrine can be used in all trimesters of pregnancy, per WHO evidence review and policy (older labels still advise against first-trimester use if alternatives exist). Primaquine and tafenoquine must not be given in pregnancy. [CDC]
- *pregnancy*: Breastfeeding: the UK label advises not breastfeeding during treatment and for at least one week after the last dose; CDC advises against use in women breastfeeding infants <5 kg. [Label · UK SmPC]
- *administration*: Tablets may be crushed for infants and children; dispersible tablets exist for paediatric use and are not recommended for adults. [WHO PQ]
- *administration* <5 kg: Infants <5 kg: the standard tablet is not established below 5 kg; the September 2026 WHO malaria guidelines add a new artemether-lumefantrine formulation for children under 5 kg. [WHO 2026]
- *administration* Radical cure: P. vivax / P. ovale: after the blood-stage course, give primaquine 0.5 mg/kg base (adults 30 mg base) once a day for 14 days, or tafenoquine 300 mg once (≥16 y), only after quantitative G6PD testing shows normal activity. [CDC]
- *administration*: Philippine policy: antimalarials used must be WHO-prequalified or GMP-certified; quinine plus tetracycline, doxycycline or clindamycin for 7 days is the second-line option if AL fails or is unavailable. [DOH AO 2009-0001]
- *forms_ph*: Oral tablet, 20 mg artemether + 120 mg lumefantrine. Listed as a List B medicine (needs in vivo bioequivalence studies). [PNF]
- *monitor*: Watch for QT prolongation: check ECG and correct potassium/magnesium if the patient deteriorates, has severe hepatic or renal impairment, or takes other QT-prolonging drugs. [Label · UK SmPC]
- *monitor*: Check haemoglobin if the patient becomes pale or tired in the weeks after treatment (delayed haemolytic anaemia has been reported). [Label · UK SmPC]
- *monitor*: Overdose: symptomatic and supportive care with ECG and blood potassium monitoring. [Label · UK SmPC]

**References added**

- [UK SmPC (emc) - Riamet](https://products.mhra.gov.uk/search/?search=artemether#emc-1628): Riamet 20 mg/120 mg tablets - Summary of Product Characteristics. Novartis Pharmaceuticals UK Ltd. electronic medicines compendium (emc).
- [WHO Prequalification - WHOPAR MA026](https://extranet.who.int/prequal/sites/default/files/whopar_files/MA026part4v3.pdf): Riamet (artemether/lumefantrine 20 mg/120 mg tablets), Novartis Pharma Schweiz AG. WHO Public Assessment Report, Part 4: Summary of Product Characteristics. World Health Organization Prequalification Unit.
- [CDC - Malaria treatment tables](https://www.cdc.gov/malaria/hcp/clinical-guidance/appendix-a-treatment-tables.html): Centers for Disease Control and Prevention. Appendix A: Malaria in the United States - Treatment Tables. Clinical guidance for healthcare providers.
- [WHO guidelines for malaria](https://www.who.int/publications/i/item/guidelines-for-malaria): World Health Organization. WHO guidelines for malaria. Geneva: WHO; latest version 10 September 2026.
- [DOH AO 2009-0001](https://dev.lawyerly.ph/laws/46597): Department of Health (Philippines). Administrative Order No. 2009-0001: Revised Policy and Guidelines on the Diagnosis and Treatment for Malaria. 13 January 2009.
- Dosing source `WHO PQ`: [WHO Prequalification - WHOPAR MA026 (Riamet SmPC)](https://extranet.who.int/prequal/sites/default/files/whopar_files/MA026part4v3.pdf): Riamet (artemether/lumefantrine 20 mg/120 mg tablets). WHO Public Assessment Report, Part 4: Summary of Product Characteristics. WHO Prequalification Unit.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc) - Riamet](https://products.mhra.gov.uk/search/?search=artemether#emc-1628): Riamet 20 mg/120 mg tablets - Summary of Product Characteristics. Novartis Pharmaceuticals UK Ltd. emc.
- Dosing source `CDC`: [CDC - Malaria treatment tables](https://www.cdc.gov/malaria/hcp/clinical-guidance/appendix-a-treatment-tables.html): Centers for Disease Control and Prevention. Appendix A: Malaria in the United States - Treatment Tables.
- Dosing source `WHO 2026`: [WHO guidelines for malaria](https://www.who.int/publications/i/item/guidelines-for-malaria): World Health Organization. WHO guidelines for malaria. Geneva: WHO; 10 September 2026.
- Dosing source `PNF`: [Philippine National Formulary - Essential Medicines List](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health; 2022.
- Dosing source `DOH AO 2009-0001`: [DOH Administrative Order No. 2009-0001](https://dev.lawyerly.ph/laws/46597): Department of Health (Philippines). Revised Policy and Guidelines on the Diagnosis and Treatment for Malaria. 13 January 2009.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF entry: 'Artemether + Lumefantrin (B) Oral: 20 mg artemether + 120 mg lumefantrin tablet'; (B) = List B medicines requiring in vivo bioequivalence studies.
- https://extranet.who.int/prequal/sites/default/files/whopar_files/MA026part4v3.pdf: WHOPAR Riamet SmPC: weight bands 5-<15 kg 1 tab, 15-<25 kg 2 tabs, 25-<35 kg 3 tabs, >=35 kg or >=12 y 4 tabs; dose at diagnosis, again after 8 h, then twice daily for 2 days (6/12/18/24 tablets); tablets may be crushed; dispersible tablets for paediatrics, not adults.
- https://products.mhra.gov.uk/search/?search=artemether#emc-1628: UK SmPC: 6 doses over 60 h; <5 kg not established; elderly no change; renal/mild-moderate hepatic no adjustment, caution + ECG/potassium in severe; take with food or milky drink; contraindications (severe malaria, family history sudden death/congenital QTc, arrhythmia/bradycardia/HFrEF, hypokalaemia/hypomagnesaemia, CYP2D6 substrates metoprolol/imipramine/amitriptyline/clomipramine, strong CYP3A4 inducers incl. rifampin); not active against hypnozoites (5.1); lopinavir/ritonavir ~2.3-fold lumefantrine; nevirapine/efavirenz reduce artemether; no concurrent antimalarials; breastfeeding stop until 1 week after last dose; ADRs palpitations, sleep disorders, rash, pruritus, cough (children), raised LFTs (children), delayed haemolytic anaemia; overdose supportive with ECG and potassium.
- https://www.cdc.gov/malaria/hcp/clinical-guidance/appendix-a-treatment-tables.html: CDC tables: AL listed for P. malariae/P. knowlesi (Table 3) and as oral option/follow-on after IV artesunate (Table 5); 'can be used in all trimesters in pregnancy per WHO evidence review and policy'; not recommended in women breastfeeding infants <5 kg; primaquine 30 mg base daily x14 d (child 0.5 mg/kg base), tafenoquine 300 mg once (>=16 y), quantitative G6PD testing required; neither in pregnancy.
- https://www.who.int/publications/i/item/guidelines-for-malaria: WHO guidelines for malaria, latest version 10 September 2026; adds a new formulation of artemether-lumefantrine for treating malaria in children less than 5 kg bw.
- https://dev.lawyerly.ph/laws/46597: DOH AO 2009-0001 (13 Jan 2009), Sec. VII 2.1 AL first-line for confirmed P. falciparum, replacing CQ+SP; 2.2 quinine + tetracycline/doxycycline/clindamycin x7 days second-line; 2.4 ACT may be used for all Plasmodium species and mixed infections; 2.5 WHO prequalification or GMP certification.

---

## Aspirin (low-dose)  (`med_aspirin`)

**Description (kept)**

Aspirin irreversibly acetylates platelet cyclooxygenase-1, blocking thromboxane A2 synthesis for the life of the platelet and thereby inhibiting platelet aggregation. At low doses it is used for acute coronary syndromes and secondary prevention of cardiovascular and cerebrovascular events.

**Description (added)**

In the Philippines, the DOH dengue case-management guidelines tell patients not to take aspirin, mefenamic acid or other NSAIDs during dengue and to use paracetamol instead, because these drugs raise bleeding risk. It is not recommended for children and adolescents under 16 except on medical advice (Reye's syndrome), and low-dose aspirin is not used as an analgesic, antipyretic or anti-inflammatory.

**Uses**: 4 kept, 3 added

- NEW: Stable angina and history of unstable angina (prevention of cardiovascular events)
- NEW: Prevention of graft occlusion after coronary artery bypass grafting
- NEW: Coronary angioplasty (outside the acute phase)

**Side effects**: 5 kept, 7 added

- NEW: Tinnitus and reduced hearing
- NEW: Hyperuricaemia (low doses reduce uric acid excretion; may trigger gout)
- NEW: Kounis syndrome (allergic acute coronary syndrome)
- NEW: Thrombocytopenia, agranulocytosis, aplastic anaemia (rare)
- NEW: Severe skin reactions: Stevens-Johnson syndrome, Lyell's syndrome (rare)
- NEW: Renal impairment and acute renal failure
- NEW: Menorrhagia

**Precautions**: 4 kept, 5 added

- NEW: Acute or recurrent peptic ulcer, or history of NSAID-related GI bleeding/perforation
- NEW: Severe hepatic, renal or cardiac insufficiency
- NEW: Doses above 100 mg/day in the third trimester of pregnancy
- NEW: Methotrexate above 15 mg/week
- NEW: Suspected or confirmed dengue (DOH/WHO: avoid aspirin and NSAIDs; use paracetamol)

**Interactions**: 6 kept, 7 added

- NEW: Alteplase: do not start aspirin within 24 h after thrombolysis for acute stroke.
- NEW: Probenecid and sulfinpyrazone: salicylates reverse their uricosuric effect (not recommended).
- NEW: Sulfonylureas and insulin: enhanced hypoglycaemic effect; dose adjustment may be needed.
- NEW: Digoxin and lithium: reduced renal excretion; monitor plasma levels.
- NEW: Acetazolamide: severe acidosis and CNS toxicity.
- NEW: Metamizole: may reduce the antiplatelet effect of aspirin.
- NEW: Valproate and phenytoin: altered protein binding and free drug levels.

**Disease links added**

- `heart_failure`: **caution**: Contraindicated in severe cardiac insufficiency.
- `chronic_kidney_disease`: **caution**: Contraindicated in severe renal insufficiency; caution in moderate impairment and with diuretics/ACE inhibitors.
- `hypertension`: **caution**: Caution in uncontrolled hypertension; may reduce the effect of antihypertensives.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Secondary prevention of MI, stable angina, post-CABG | PO | 75–160 mg | Once a day | Long-term | 300 mg/day | Label · UK SmPC |
| adult | Secondary prevention of TIA / ischaemic stroke (Start only after intracerebral haemorrhage is excluded) | PO | 75–300 mg | Once a day | Long-term | 300 mg/day | Label · UK SmPC |
| adult | Acute myocardial infarction | PO | 150–300 mg loading, then 75–160 mg | Once a day | Long-term | 300 mg/day | Label · UK SmPC |
| child | Under 16 years (Reye's syndrome risk; only on medical advice) | PO | Not recommended | — | — | — | Label · UK SmPC |

- *renal*: Contraindicated in severe renal insufficiency; use with caution in moderate impairment or dehydration. [Label · UK SmPC]
- *hepatic*: Contraindicated in severe hepatic insufficiency; in mild–moderate impairment use with caution and check liver function regularly. [Label · UK SmPC]
- *elderly*: More prone to adverse effects; usual adult dose if no severe renal or hepatic insufficiency; review treatment regularly. [Label · UK SmPC]
- *pregnancy*: Up to 100 mg/day appears safe for restricted obstetric use under specialist monitoring; higher doses contraindicated in the third trimester. Breastfeeding: short-term use acceptable; stop with long-term or high-dose use. [Label · UK SmPC]
- *administration*: Swallow with about half a glass of water. Bleeding risk persists 4–8 days after stopping; temporary withdrawal may be needed before surgery, including tooth extraction. [Label · UK SmPC]
- *administration*: Dengue: patients should not take aspirin, mefenamic acid or other NSAIDs; use paracetamol (max 4 g/day in adults). Those already on these drugs should consult their doctor. [DOH 2012]
- *forms_ph*: Aspirin oral tablets 80 mg, 100 mg, 300 mg and 325 mg. [PNF]
- *monitor*: Signs of GI bleeding (black stools, haematemesis) and anaemia; gout flares; renal function when combined with diuretics, ACE inhibitors or ARBs; blood glucose with sulfonylureas or insulin. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=aspirin#emc-107619): Aspirin 75 mg Tablets. Summary of Product Characteristics. G.L. Pharma GmbH. electronic medicines compendium (emc); revised 03/08/2026.
- [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.
- [Department of Health (Philippines)](https://doh.gov.ph/wp-content/uploads/2023/08/ao2012-0026-1.pdf): Department of Health. Administrative Order: Revised Dengue Clinical Case Management Guidelines 2011. Manila: DOH; 2012.
- [World Health Organization](https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue): World Health Organization. Dengue and severe dengue. Fact sheet; 21 August 2025.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=aspirin#emc-107619): Aspirin 75 mg Tablets SmPC, G.L. Pharma GmbH; revised 03/08/2026.
- Dosing source `PNF`: [Philippine National Formulary (PhilHealth)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): PNF Essential Medicines List, 2022.
- Dosing source `DOH 2012`: [Department of Health (Philippines)](https://doh.gov.ph/wp-content/uploads/2023/08/ao2012-0026-1.pdf): Revised Dengue Clinical Case Management Guidelines 2011 (Administrative Order, 2012).

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: PNF-EML lists 'Aspirin Oral: 80 mg, 100 mg tablet, 300 mg tablet and 325mg tablet'.
- https://products.mhra.gov.uk/search/?search=aspirin#emc-107619: Aspirin 75 mg Tablets SmPC (G.L. Pharma, rev 03/08/2026): indications incl. CABG graft occlusion, angioplasty, stable/unstable angina; doses 75–160 mg od, TIA/CVA 75–300 mg, acute MI 150–300 mg load then 75–160 mg, not exceed 300 mg/day; not under 16 (Reye's); contraindications (ulcers, severe hepatic/renal/cardiac insufficiency, >100 mg/day 3rd trimester, MTX >15 mg/week); interactions (alteplase 24 h, probenecid, antidiabetics, digoxin/lithium, acetazolamide, metamizole, valproate/phenytoin); ADRs incl. tinnitus, hyperuricaemia, Kounis syndrome, blood dyscrasias, SJS/Lyell, renal failure, menorrhagia; bleeding effect 4–8 days; caution uncontrolled hypertension.
- https://doh.gov.ph/wp-content/uploads/2023/08/ao2012-0026-1.pdf: DOH AO 'Revised Dengue Clinical Case Management Guidelines 2011' (signed Sec. Enrique T. Ona; AO number garbled in text): Home Care Card 'Do not take NSAIDs, e.g. acetylsalicylic acid (aspirin)/mefenamic acid or steroids'; paracetamol not more than 4 g/day in adults; 'If you are already taking these medications, please consult your doctor'.
- https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue: WHO dengue fact sheet (21 Aug 2025): 'Non-steroidal anti-inflammatory medicines such as ibuprofen and aspirin should be avoided as they can increase the risk of bleeding'; paracetamol for pain.

---

## Atorvastatin  (`med_atorvastatin`)

**Description (kept)**

Atorvastatin competitively inhibits HMG-CoA reductase, the rate-limiting enzyme of hepatic cholesterol synthesis, which up-regulates hepatic LDL receptors and lowers LDL-cholesterol. Moderate-intensity doses (10-20 mg) lower LDL-C by about 30-50% and high-intensity doses (40-80 mg) by more than 50%. It reduces the risk of MI, stroke and revascularization in primary and secondary prevention.

**Description (added)**

The 2020 Philippine dyslipidemia guidelines recommend early, maximally tolerated high-intensity statin therapy after ACS, an LDL-C goal below 55 mg/dL in clinical ASCVD, and statins for CKD patients not on dialysis (lipid care of dialysis and transplant patients is referred to a nephrologist). In the Philippines it is listed in the PNF as 10, 20, 40 and 80 mg tablets.

**Uses**: 4 kept, 1 added

- NEW: Heterozygous familial hypercholesterolaemia in children aged 10 years and over

**Side effects**: 8 kept, 5 added

- NEW: Constipation, flatulence, nausea
- NEW: Myalgia, muscle spasms, joint swelling, back pain
- NEW: Raised creatine kinase
- NEW: Interstitial lung disease (rare)
- NEW: Higher haemorrhagic stroke incidence with 80 mg in patients with recent stroke/TIA (SPARCL), especially prior haemorrhagic stroke or lacunar infarct

**Precautions**: 2 kept, 4 added

- NEW: Active liver disease or unexplained persistent transaminase elevation >3× ULN
- NEW: Pregnancy and breastfeeding
- NEW: Women of childbearing potential not using appropriate contraception
- NEW: Concurrent glecaprevir/pibrentasvir

**Interactions**: 5 kept, 4 added

- NEW: Systemic fusidic acid: must not be co-administered (fatal rhabdomyolysis reported); stop the statin and restart 7 days after the last fusidic acid dose.
- NEW: Elbasvir/grazoprevir or letermovir: do not exceed 20 mg daily; letermovir with ciclosporin is not recommended.
- NEW: Rifampicin: give at the same time; delayed atorvastatin dosing markedly lowers its levels.
- NEW: Azithromycin: post-marketing rhabdomyolysis reported with statins; use with caution.

**Disease links added**

- `hepatitis_a`: **avoid**: Active liver disease is a contraindication (UK SmPC).
- `hepatitis_b`: **caution**: Use with caution in hepatic impairment; contraindicated if active liver disease or persistent transaminases >3× ULN.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Hypercholesterolaemia / mixed dyslipidaemia (Adjust at intervals of ≥4 weeks) | PO | 10 mg | Once a day | Long-term | 80 mg/day | Label · UK SmPC |
| adult | Moderate-intensity statin therapy (Lowers LDL-C 30–50%) | PO | 10–20 mg | Once a day | Long-term | — | PH CPG 2020 |
| adult | High-intensity therapy (ASCVD, ACS, FH) (Start early after ACS) | PO | 40–80 mg | Once a day | Long-term | 80 mg/day | PH CPG 2020 |
| adult | With elbasvir/grazoprevir or letermovir | PO | ≤20 mg | Once a day | — | 20 mg/day | Label · UK SmPC |
| child | Heterozygous FH (≥10 y) (US label range 10–20 mg; not indicated <10 y) | PO | 10 mg | Once a day | Long-term | 80 mg/day | Label · UK SmPC |
| child | Homozygous FH (≥10 y) | PO | 10–20 mg | Once a day | Long-term | 80 mg/day | Label · US FDA |

- *renal*: No dose adjustment; monitor for myopathy. [Label · US FDA]
- *renal* Dialysis: Patients on dialysis or after kidney transplant: lipid management by a nephrologist (no statin recommendation made). [PH CPG 2020]
- *hepatic*: Use with caution in hepatic impairment; contraindicated in active liver disease. [Label · UK SmPC]
- *elderly*: Efficacy and safety in patients over 70 at recommended doses are similar to the general population. [Label · UK SmPC]
- *pregnancy*: Contraindicated in pregnancy and breastfeeding; women of childbearing potential should use appropriate contraception. [Label · UK SmPC]
- *administration*: Whole daily dose at once, any time of day, with or without food. Give at the same time as rifampicin. [Label · UK SmPC]
- *forms_ph*: Tablet: 10 mg, 20 mg, 40 mg, 80 mg (as calcium). [PNF]
- *monitor*: Liver function tests before starting and periodically thereafter. [Label · UK SmPC]
- *monitor*: Lipid panel (LDL-C) as early as 4 weeks after starting or changing the dose. [Label · US FDA]
- *monitor*: Ask about muscle pain/weakness; check CK if present; stop if CK >10× ULN or rhabdomyolysis suspected. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=atorvastatin#emc-4343): Atorvastatin 20 mg Film-coated Tablets. Summary of Product Characteristics. Sun Pharma UK Ltd; revised 2024. electronic medicines compendium (emc).
- [JAFES (Philippine CPG)](https://www.asean-endocrinejournal.org/index.php/JAFES/article/view/927): Gonzalez-Santos LE, Oliva R, Jimeno C, et al. Executive Summary of the 2020 Clinical Practice Guidelines for the Management of Dyslipidemia in the Philippines. J ASEAN Fed Endocr Soc. 2021;36(1):5–11. doi:10.15605/jafes.036.01.01
- [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a60cc18b-0631-4cf0-b021-9f52224ece65): LIPITOR (atorvastatin calcium) tablet, film coated. Prescribing information. Viatris Specialty LLC; updated April 2024. DailyMed, U.S. National Library of Medicine.
- [PhilHealth / DOH (PNF-EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=atorvastatin#emc-4343): Atorvastatin 20 mg Film-coated Tablets. Summary of Product Characteristics. Sun Pharma UK Ltd; revised 2024.
- Dosing source `Label · US FDA`: [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a60cc18b-0631-4cf0-b021-9f52224ece65): LIPITOR (atorvastatin calcium) tablets. Prescribing information. Viatris; updated April 2024.
- Dosing source `PH CPG 2020`: [Philippine Dyslipidemia CPG 2020](https://www.asean-endocrinejournal.org/index.php/JAFES/article/view/927): Gonzalez-Santos LE, et al. Executive Summary of the 2020 Clinical Practice Guidelines for the Management of Dyslipidemia in the Philippines. J ASEAN Fed Endocr Soc. 2021;36(1):5–11.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Atorvastatin calcium Oral: 10 mg, 20 mg, 40 mg and 80 mg tablet.
- https://products.mhra.gov.uk/search/?search=atorvastatin#emc-4343: Sun Pharma UK atorvastatin SmPC: adult start 10 mg, max 80 mg, adjust at intervals ≥4 weeks; HeFH children ≥10 y start 10 mg, up to 80 mg, not indicated <10 y; no renal adjustment; caution in hepatic impairment; elderly >70 similar; any time of day with/without food; elbasvir/grazoprevir and letermovir (Table 1) max 20 mg; contraindications active liver disease, pregnancy, breastfeeding, glecaprevir/pibrentasvir; fusidic acid stop, restart 7 days after; SPARCL haemorrhagic stroke; ILD; LFTs before and periodically; CK >10× ULN discontinue; rifampicin simultaneous; common AEs constipation, flatulence, nausea, myalgia, muscle spasms, joint swelling, back pain, CK increased; contraception in women of childbearing potential.
- https://products.mhra.gov.uk/search/?search=atorvastatin#emc-2588: Milpharm atorvastatin SmPC (cross-check): contraindication includes women of childbearing potential not using contraception and transaminases >3× ULN; do not start if baseline CK >5× ULN, stop if >10× ULN; letermovir with ciclosporin not recommended.
- https://www.asean-endocrinejournal.org/index.php/JAFES/article/view/927: 2020 PH dyslipidemia CPG: atorvastatin 10–20 mg moderate intensity (30–50% LDL-C lowering), 40–80 mg high intensity; early maximally tolerated high-intensity statin in ACS; high-intensity in FH; LDL-C <55 mg/dL in clinical ASCVD; statins for CKD not on dialysis; dialysis/transplant refer to nephrologist; CK check for myalgia.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a60cc18b-0631-4cf0-b021-9f52224ece65: Lipitor US label (updated April 2024): pediatric HeFH ≥10 y 10 mg start, range 10–20 mg; pediatric HoFH 10–20 mg start, range 10–80 mg; no renal dose adjustment but monitor for myopathy; LDL-C assess as early as 4 weeks.
- https://products.mhra.gov.uk/search/?search=atorvastatin#emc-1073: Zithromax SmPC 4.5: post-marketing rhabdomyolysis reported with azithromycin + statins (atorvastatin); use caution.

---

## Azithromycin  (`med_azithromycin`)

**Description (kept)**

Azithromycin is an azalide macrolide that binds the 23S rRNA of the 50S ribosomal subunit and inhibits bacterial protein synthesis; it is mainly bacteriostatic. Its long tissue half-life allows short once-daily courses for respiratory infections, atypical pneumonia and sexually transmitted infections.

**Description (added)**

In the Philippines it is listed in the PNF as capsules, tablets, oral suspension and a vial for IV infusion. Beyond respiratory and sexually transmitted infections, it is used as a single-dose treatment for cholera and trachoma and as a 7-day oral option for typhoid fever.

**Uses**: 7 kept, 10 added

- NEW: Acute otitis media
- NEW: Gonococcal urethritis/cervicitis (together with a second agent such as ceftriaxone)
- NEW: Pelvic inflammatory disease (IV then oral)
- NEW: Typhoid fever
- NEW: Cholera (single dose, susceptible strains)
- NEW: Pertussis
- NEW: Leptospirosis
- NEW: Trachoma (single dose)
- NEW: Yaws (single dose)
- NEW: Shigellosis (second-line)

**Side effects**: 7 kept, 6 added

- NEW: Vomiting, headache
- NEW: Deafness and tinnitus (hearing disorders usually reversible)
- NEW: Dizziness, drowsiness, convulsions
- NEW: Visual impairment (uncommon)
- NEW: Decreased lymphocytes and bicarbonate; increased eosinophils
- NEW: Electrolyte disturbances

**Precautions**: 2 kept, 1 added

- NEW: Severe hepatic impairment

**Interactions**: 4 kept, 6 added

- NEW: Ergot derivatives: do not co-administer (risk of ergotism).
- NEW: Ciclosporin: peak levels rise about 24%; monitor and adjust.
- NEW: Statins (e.g., atorvastatin): rhabdomyolysis reported; use with caution.
- NEW: Dabigatran: possible increased bleeding risk.
- NEW: Antimalarials with QT effect (artemether-lumefantrine, chloroquine, mefloquine, quinine), amiodarone, fluconazole, ondansetron: avoid combining (QT prolongation).
- NEW: Aluminium/magnesium hydroxide antacids: separate doses by 2 hours.

**Disease links added**

- `heart_failure`: **caution**: QT/arrhythmia risk; use with caution in severe cardiac insufficiency (UK SmPC).
- `malaria`: **caution**: Avoid combining with QT-prolonging antimalarials (artemether-lumefantrine, quinine, mefloquine, chloroquine).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | CAP, sinusitis, pharyngitis, skin infections (Or 500 mg day 1, then 250 mg days 2–5) | PO | 500 mg | Once a day | 3 days | 1.5 g/course | Label · UK SmPC |
| adult | Chlamydial urethritis/cervicitis | PO | 1 g | Single dose | 1 day | — | Label · UK SmPC |
| adult | Gonorrhoea (with ceftriaxone) (Give with a second antibacterial) | PO | 1–2 g | Single dose | 1 day | — | Label · UK SmPC |
| adult | CAP (hospitalised) (Switch to 500 mg PO once a day) | IV | 500 mg | Once a day | ≥2 days, then PO to 7–10 days | — | Label · US IV |
| adult | Pelvic inflammatory disease (Then 250 mg PO once a day) | IV | 500 mg | Once a day | 1–2 days, then PO to 7 days | — | Label · US IV |
| adult | Typhoid fever (Or 1 g day 1, then 500 mg days 2–7) | PO | 500 mg–1 g | Once a day | 7 days | 1 g/day | MSF 2025 |
| adult | Cholera (If strain susceptible) | PO | 1 g | Single dose | 1 day | — | MSF 2025 |
| adult | Leptospirosis | PO | 1 g day 1, then 500 mg | Once a day | 3 days | — | MSF 2025 |
| adult | Trachoma | PO | 1 g | Single dose | 1 day | — | MSF 2025 |
| child | CAP, sinusitis, skin infections (≥6 mo) (Or 10 mg/kg day 1, then 5 mg/kg days 2–5) | PO | 10 mg/kg | Once a day | 3 days | 500 mg/day; 1.5 g/course | Label · UK SmPC susp |
| child | Acute otitis media (≥6 mo) (Or a 3- or 5-day regimen) | PO | 30 mg/kg | Single dose | 1 day | 1.5 g | Label · UK SmPC susp |
| child | Streptococcal pharyngitis (≥2 y) (Or 12 mg/kg once a day for 5 days) | PO | 20 mg/kg | Once a day | 3 days | 500 mg/day | Label · UK SmPC susp |
| child | Typhoid fever | PO | 10–20 mg/kg | Once a day | 7 days | 1 g/day | MSF 2025 |
| child | Cholera (If strain susceptible) | PO | 20 mg/kg | Single dose | 1 day | 1 g | MSF 2025 |
| child | Leptospirosis | PO | 10 mg/kg day 1, then 5 mg/kg | Once a day | 3 days | 500 mg day 1; 250 mg/day | MSF 2025 |
| child | Pertussis (<6 mo) (Caution <6 weeks (pyloric stenosis)) | PO | 10 mg/kg | Once a day | 5 days | — | MSF 2025 |
| child | Pertussis (≥6 mo) | PO | 10 mg/kg day 1, then 5 mg/kg | Once a day | 5 days | 500 mg day 1; 250 mg/day | MSF 2025 |

- *renal* GFR ≥10: No dose adjustment. [Label · UK SmPC]
- *renal* GFR <10: Use with caution. [Label · UK SmPC]
- *hepatic*: No adjustment in mild–moderate impairment; use with caution in severe impairment (no data). [Label · UK SmPC]
- *elderly*: No dose adjustment, but extra caution because of arrhythmia/QT risk. [Label · UK SmPC]
- *pregnancy*: Use only if clinically needed; >7000 exposed pregnancies showed no clear rise in major malformations. Excreted substantially in breast milk. [Label · UK SmPC]
- *administration*: Capsules: swallow whole at least 1 h before or 2 h after a meal. Suspension: with or without food; shake before each dose. [Label · UK SmPC susp]
- *administration*: IV: infuse 1 mg/mL over 3 h or 2 mg/mL over 1 h; never as IV bolus or IM. [Label · US IV]
- *administration*: Missed dose: take if ≤12 h late, otherwise wait for the next scheduled dose. [Label · UK SmPC]
- *forms_ph*: Capsule 250 mg; tablet 250 mg, 500 mg; powder for suspension 200 mg/5 mL (15 mL, 60 mL); powder for IV infusion 500 mg vial. [PNF]
- *monitor*: Check ECG and K/Mg in patients with QT risk (bradycardia, arrhythmia, heart failure, QT-prolonging drugs). [Label · UK SmPC]
- *monitor*: Stop and check liver tests if jaundice, dark urine or other hepatitis symptoms appear. [Label · UK SmPC]
- *monitor*: Infants in the first 42 days: watch for projectile vomiting or feeding irritability (pyloric stenosis). [Label · UK SmPC susp]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=azithromycin#emc-1073): Zithromax 250 mg Capsules. Summary of Product Characteristics. Pfizer Ltd; updated July 2026. electronic medicines compendium (emc).
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=azithromycin#emc-3006): Zithromax 200 mg/5 ml Powder for Oral Suspension. Summary of Product Characteristics. Pfizer Ltd; updated July 2026. electronic medicines compendium (emc).
- [Pfizer labeling (US)](https://labeling.pfizer.com/ShowLabeling.aspx?id=1181): ZITHROMAX (azithromycin dihydrate) injection, powder, lyophilized, for solution. Prescribing information. Pfizer Inc; revised 2026.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/azithromycin-oral-16685286.html): Médecins Sans Frontières. Essential drugs – Azithromycin oral. MSF Medical Guidelines; updated June 2025.
- [PhilHealth / DOH (PNF-EML)](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=azithromycin#emc-1073): Zithromax 250 mg Capsules / 200 mg/5 ml Powder for Oral Suspension. Summary of Product Characteristics. Pfizer Ltd; July 2026.
- Dosing source `Label · UK SmPC susp`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=azithromycin#emc-3006): Zithromax 200 mg/5 ml Powder for Oral Suspension. Summary of Product Characteristics. Pfizer Ltd; July 2026.
- Dosing source `Label · US IV`: [Pfizer labeling (US)](https://labeling.pfizer.com/ShowLabeling.aspx?id=1181): ZITHROMAX (azithromycin) for injection. Prescribing information. Pfizer Inc; 2026.
- Dosing source `MSF 2025`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/azithromycin-oral-16685286.html): Médecins Sans Frontières. Essential drugs – Azithromycin oral. Updated June 2025.
- Dosing source `PNF`: [Philippine National Formulary – EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Azithromycin Oral: 250 mg capsule; 250 mg and 500 mg (B) tablet; 200 mg/5 mL powder for suspension 15 mL and 60 mL; Inj.: 500 mg powder, vial (IV infusion).
- https://products.mhra.gov.uk/search/?search=azithromycin#emc-1073: Zithromax 250 mg capsules SmPC (Pfizer, July 2026): indications incl. AOM, gonococcal urethritis/cervicitis with second agent e.g. ceftriaxone; 500 mg/day x3 days (1500 mg total) or 500 mg then 250 mg days 2–5; chlamydia 1 g; gonorrhoea 1 g or 2 g; missed dose ≤12 h; GFR ≥10 no adjustment, <10 caution; hepatic mild–moderate no adjustment, severe caution; elderly caution; 1 h before/2 h after meal; ergot avoid; QT cautions; ciclosporin +24%; statins rhabdomyolysis; dabigatran; pregnancy >7000 exposures; breast milk; AEs vomiting, headache, lymphocytes/bicarbonate decreased, eosinophils increased, visual impairment, dizziness, deafness, tinnitus, convulsions.
- https://products.mhra.gov.uk/search/?search=azithromycin#emc-3006: Zithromax 200 mg/5 ml suspension SmPC: children ≥6 mo <45 kg 10 mg/kg x3 days or 10 then 5 mg/kg days 2–5; AOM single 30 mg/kg; strep pharyngitis ≥2 y 20 mg/kg x3 days or 12 mg/kg x5 days; daily max 500 mg (except AOM single dose), total max 1500 mg; with or without meal, shake; IHPS within first 42 days.
- https://labeling.pfizer.com/ShowLabeling.aspx?id=1181: Zithromax IV label: CAP 500 mg IV daily ≥2 days then oral 500 mg to complete 7–10 days; PID 500 mg IV 1–2 days then 250 mg oral to complete 7 days; 1 mg/mL over 3 h or 2 mg/mL over 1 h; no bolus or IM; pediatric IV safety not established.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/azithromycin-oral-16685286.html: MSF azithromycin oral (June 2025): typhoid adult 500 mg–1 g OD x7 days (or 1 g then 500 mg), child 10–20 mg/kg max 1 g x7 d; cholera 1 g / 20 mg/kg max 1 g single; trachoma 1 g / 20 mg/kg; leptospirosis adult 1 g then 500 mg days 2–3, child 10 then 5 mg/kg; pertussis <6 mo 10 mg/kg x5 d, ≥6 mo 10 then 5 mg/kg; yaws; shigellosis second-line; contraindicated in severe hepatic impairment; antacids separate 2 h; avoid with QT drugs incl. co-artemether, chloroquine, mefloquine, quinine, amiodarone, fluconazole, ondansetron; reversible hearing disorders, electrolyte disturbances.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=330a082d-57b2-2bf5-e054-00144ff88e88: Zithromax US tablet label (oral only, no IV dosing); pediatric AOM 30 mg/kg single dose capped at 1500 mg (cross-check).

---

## Benzathine Penicillin G  (`med_benzathine_penicillin`)

**Description (kept)**

Benzathine penicillin G is a depot form of penicillin G that is released slowly from the intramuscular injection site, giving low but prolonged blood levels for 3-4 weeks. Like other penicillins it inhibits bacterial cell-wall synthesis and is bactericidal. A single injection eradicates group A streptococcal pharyngitis, and repeated injections every 3-4 weeks are the most effective secondary prophylaxis against recurrent rheumatic fever.

**Description (added)**

In the Philippines, the PhilHealth outpatient benefit package for rheumatic fever/rheumatic heart disease covers benzathine benzylpenicillin 1.2 million units IM every 28 days for rheumatic fever, and every 21 days once rheumatic heart disease is present, with injections tracked against the schedule. The American Heart Association calls injectable BPG secondary prophylaxis the cornerstone of RHD prevention and management, while noting that uptake has been sub-optimal.

**Uses**: 4 kept, 3 added

- NEW: Prophylaxis of rheumatic chorea and of glomerulonephritis after an acute attack
- NEW: Congenital syphilis (children under 2 years, weight-based dose)
- NEW: Late (tertiary) syphilis: three weekly injections

**Side effects**: 4 kept, 5 added

- NEW: Severe cutaneous reactions (Stevens-Johnson syndrome, DRESS): stop immediately
- NEW: Hoigne syndrome (agitation, confusion, hallucinations)
- NEW: Nicolau syndrome and injection-site necrosis
- NEW: Quadriceps fibrosis and atrophy after repeated anterolateral thigh injections
- NEW: Clostridioides difficile-associated diarrhoea

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Secondary prophylaxis: rheumatic fever (PhilHealth RF/RHD package) | IM | 1.2 million units | Every 28 days | Long-term (see notes) | — | PhilHealth |
| adult | Secondary prophylaxis: rheumatic heart disease (PhilHealth RF/RHD package) | IM | 1.2 million units | Every 21 days | Long-term (see notes) | — | PhilHealth |
| adult | Group A strep pharyngitis | IM | 1.2 million units | Once | Single dose | — | Label · US |
| adult | Syphilis: primary, secondary, latent | IM | 2.4 million units | Once | Single dose | — | Label · US |
| adult | Syphilis: late (tertiary) | IM | 2.4 million units | Every 7 days | 3 doses | — | Label · US |
| adult | Yaws, bejel, pinta | IM | 1.2 million units | Once | Single dose | — | Label · US |
| child | Secondary prophylaxis, ≥20 kg (Every 3 weeks if high risk) | IM | 1.2 million units | Every 4 weeks | Long-term (see notes) | — | Label · NZ |
| child | Secondary prophylaxis, <20 kg (Every 3 weeks if high risk) | IM | 600,000 units | Every 4 weeks | Long-term (see notes) | — | Label · NZ |
| child | Group A strep pharyngitis, older children | IM | 900,000 units | Once | Single dose | — | Label · NZ |
| child | Group A strep pharyngitis, <27 kg | IM | 300,000–600,000 units | Once | Single dose | — | Label · NZ |
| child | Congenital syphilis, <2 years (Ages 2–12: adult schedule) | IM | 50,000 units/kg | — | — | — | Label · US |

- *forms_ph*: Benzathine benzylpenicillin (penicillin G benzathine) 1.2 million units, vial, for IM injection (PhilHealth RF/RHD package). [PhilHealth]
- *renal*: Substantially excreted by the kidney; toxic reactions may be more likely in impaired renal function. Select doses cautiously and consider monitoring renal function. [Label · US]
- *elderly*: Older patients more often have reduced renal function: choose the dose carefully and monitor renal function. [Label · US]
- *pregnancy*: No harm in animal studies but no adequate human studies; use if clearly needed. Penicillin G passes into breast milk, so use caution when breastfeeding. [Label · US]
- *administration* Injection site: Give deep IM into the upper outer quadrant of the buttock or the ventrogluteal site; in neonates, infants and small children the midlateral thigh may be preferable. The anterolateral thigh is not recommended. [Label · US]
- *administration*: Inject at a slow, steady rate (the thick suspension can block the needle) and vary the site with repeat doses. [Label · US]
- *administration* Duration: Duration of secondary prophylaxis: RF without carditis, 5 years or until age 21 (whichever is longer); carditis without residual heart disease, 10 years or until age 21; carditis with residual valve disease, more than 10 years (many experts: until age 40 or lifelong). [Merck]
- *administration* Alternatives: If injections are refused or the patient is allergic: daily oral penicillin V (or sulfadiazine); if allergic to both penicillin and sulfa, daily oral erythromycin or azithromycin. [Merck]
- *monitor*: Keep epinephrine and resuscitation equipment ready: serious, sometimes fatal anaphylaxis can occur. [Label · US]
- *monitor*: Track adherence to the injection schedule (doses due every 21 or 28 days) and follow RHD patients with yearly 2D echo, ASO/ESR/CRP as needed, and dental clearance. [PhilHealth RF/RHD form]

**References added**

- [Bicillin L-A US prescribing information (Pfizer)](https://labeling.pfizer.com/ShowLabeling.aspx?id=691): BICILLIN L-A (penicillin G benzathine injectable suspension) - prescribing information. Pfizer Laboratories.
- [AHA science news - BPG reactions in severe RHD](https://professional.heart.org/en/science-news/penicillin-reactions-in-patients-with-severe-rheumatic-heart-disease): American Heart Association. Penicillin reactions in patients with severe rheumatic heart disease (advisory in J Am Heart Assoc, doi:10.1161/JAHA.121.024517). Updated 20 Jan 2022.
- [PhilHealth RF/RHD benefit package - Annex C1](https://www.philhealth.gov.ph/downloads/rf-rhd/RF-RHD_AnnexC1_MandatoryChecklist_010319.pdf): Philippine Health Insurance Corporation. Annex C1 - RF/RHD: Checklist of mandatory services (Tranche 1). January 2019.
- [WHO guideline on RF and RHD (2024)](https://www.who.int/publications/i/item/9789240100077): World Health Organization. WHO guideline on the prevention and diagnosis of rheumatic fever and rheumatic heart disease. Geneva: WHO; 29 October 2024. ISBN 9789240100077.
- [Merck Manual Professional - Rheumatic fever](https://www.merckmanuals.com/professional/pediatrics/miscellaneous-bacterial-infections-in-infants-and-children/rheumatic-fever): Rheumatic Fever. Merck Manual Professional Version. Merck & Co., Inc.
- Dosing source `PhilHealth`: [PhilHealth RF/RHD benefit package - Annex C1](https://www.philhealth.gov.ph/downloads/rf-rhd/RF-RHD_AnnexC1_MandatoryChecklist_010319.pdf): Philippine Health Insurance Corporation. Annex C1 - RF/RHD: Checklist of mandatory services (Tranche 1). January 2019.
- Dosing source `Label · US`: [Bicillin L-A US prescribing information (Pfizer)](https://labeling.pfizer.com/ShowLabeling.aspx?id=691): BICILLIN L-A (penicillin G benzathine injectable suspension) - prescribing information. Pfizer Laboratories.
- Dosing source `Label · NZ`: [Medsafe data sheet - Bicillin L-A](https://www.Medsafe.govt.nz/profs/Datasheet/b/BicillinLAinj.pdf): Bicillin L-A (benzathine benzylpenicillin) injection - New Zealand data sheet. Medsafe.
- Dosing source `Merck`: [Merck Manual Professional - Rheumatic fever](https://www.merckmanuals.com/professional/pediatrics/miscellaneous-bacterial-infections-in-infants-and-children/rheumatic-fever): Rheumatic Fever. Merck Manual Professional Version. Merck & Co., Inc.
- Dosing source `PhilHealth RF/RHD form`: [PhilHealth RF/RHD benefit package - Annex N](https://www.philhealth.gov.ph/downloads/rf-rhd/RF-RHD_AnnexN_OutpatientAssessmentForm_010319.pdf): Philippine Health Insurance Corporation. Annex N - RF/RHD: Systematic clinical assessment and follow-up form. January 2019.

**What was checked on each page**

- https://www.philhealth.gov.ph/downloads/rf-rhd/RF-RHD_AnnexC1_MandatoryChecklist_010319.pdf: Annex C1 RF/RHD checklist (Jan 2019): 'penicillin G benzathine (benzathine benzylpenicillin), 1.2M units, vial (MR) (IM) every 28 days' for RF (Section A) and 'every 21 days' for RF/RHD (Section B); oral phenoxymethylpenicillin or erythromycin as alternatives.
- https://www.philhealth.gov.ph/downloads/rf-rhd/RF-RHD_AnnexN_OutpatientAssessmentForm_010319.pdf: Annex N: PhilHealth Outpatient Benefit Package for RF/RHD follow-up form; 'IM BPN 1.2 M Units', intervals 28/21 days, compliance 'Total scheduled q 21 days'; yearly 2D echo for years 1-5, ASO/CBC/ESR/CRP, dental clearance.
- https://labeling.pfizer.com/ShowLabeling.aspx?id=691: Bicillin L-A US label: boxed IV warning; GAS URTI adult 1,200,000 units single; syphilis primary/secondary/latent 2,400,000 units (1 dose), late (tertiary and neurosyphilis) 2,400,000 units at 7-day intervals x3, congenital <2 y 50,000 units/kg, 2-12 y adult schedule; yaws/bejel/pinta 1,200,000 units; RF and glomerulonephritis prophylaxis 1,200,000 units monthly or 600,000 every 2 weeks; injection sites (dorsogluteal/ventrogluteal; midlateral thigh in small children; anterolateral thigh not recommended; quadriceps fibrosis/atrophy); slow steady rate, vary site; SCAR (SJS, DRESS); CDAD; Hoigne syndrome; Nicolau syndrome; renal excretion caution; pregnancy 'if clearly needed'; excreted in milk; anaphylaxis needs epinephrine.
- https://www.Medsafe.govt.nz/profs/Datasheet/b/BicillinLAinj.pdf: NZ data sheet 4.2: secondary prophylaxis 1,200,000 units for patients weighing [>=]20 kg and 600,000 units for <20 kg, every 4 weeks, 3-weekly if high risk; pharyngitis 1,200,000 adults, 900,000 older children, 300,000-600,000 units for infants/children under 27 kg.
- https://www.merckmanuals.com/professional/pediatrics/miscellaneous-bacterial-infections-in-infants-and-children/rheumatic-fever: Merck: BPG IM every 3-4 weeks (3-weekly superior in high-endemic areas); duration 5 y or to age 21 (no carditis), 10 y or to 21 (carditis without residual damage), >10 y / until 40 or lifelong (residual damage); alternatives oral penicillin V or sulfadiazine; erythromycin/azithromycin if allergic to penicillin and sulfa.
- https://www.who.int/publications/i/item/9789240100077: WHO guideline on prevention and diagnosis of RF and RHD, 29 Oct 2024, ISBN 9789240100077; scope includes secondary prevention with long-term antibiotic prophylaxis and treatment of GAS pharyngitis (page itself names no drug; PDF on iris would not load).
- https://professional.heart.org/en/science-news/penicillin-reactions-in-patients-with-severe-rheumatic-heart-disease: AHA science news (Jan 2022, JAHA advisory): secondary prophylaxis with injectable BPG is 'the cornerstone of RHD prevention and management'; 'adoption of BPG has been sub-optimal'. Supports desc_add sentence.
- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Could NOT confirm a benzathine entry: the fetched text (~66k chars) is truncated around 'M' and the entry is likely under 'P' (penicillin G benzathine). No forms_ph note added.

---

