# Medicine review b06: review sheet

Run `038_medicines_review_06.sql` in Supabase after you have checked this. Everything below is ADDED; the existing text stays as it is.

Every link was opened twice: by the research step (to read the fact), and again in Akeso's own browser pane on your computer in the Philippines (to make sure it opens for you, not just from the cloud). See NOTES.md in the batch folder for any link that needs attention.

UK SmPC links open the official MHRA Products search (free) for that medicine: the emc site (medicines.org.uk) now limits free page views for users outside the UK. The citation still names the exact product and PL number to pick.

## Please check (batch 06)

- **Pyrazinamide, rifampicin, rabies immunoglobulin, vancomycin, warfarin, zinc sulfate:** the research was cut off by a usage limit before the final report. The files pass all checks and the links were opened again from your computer, but please review these more carefully.
- **Rabies vaccine:** doses follow DOH AO 2018-0013 (from the LegalDex copy). The route "ID" (intradermal) is used. The DOH intradermal PrEP table is inconsistent, so PrEP follows WHO (days 0 and 7).
- **Sumatriptan:** the route "Nasal" is used. The UK oral maximum is 300 mg/24 h; the existing text says 200 mg (US).
- **TLD:** the PH form note comes from the 2021 DOST HTA summary ("not yet in the PNF" then). **TLD → chronic kidney disease, *avoid*:** from MSF.
- **Tenofovir:** PrEP doses come from the DOH interim PrEP guidelines (2021, UNAIDS-hosted copy).
- **Salbutamol:** PH forms come from the PhilHealth Konsulta list. No syrup dose rows.


---

## Pyrazinamide  (`med_pyrazinamide`)

**Description (kept)**

Pyrazinamide is a prodrug converted to pyrazinoic acid, which is active against semi-dormant M. tuberculosis in acidic environments; its exact mechanism is not fully understood. It is used during the 2-month intensive phase of first-line TB therapy, allowing total treatment to be shortened to 6 months.

**Description (added)**

In the Philippine NTP it is given as part of the HRZE fixed-dose combination tablet in the intensive phase of Category I (2HRZE/4HR) and in the first 3 months of Category II retreatment (2HRZES/1HRZE/5HRE), with the number of tablets set by body-weight band. Single-drug pyrazinamide (including a 250 mg/5 mL suspension) is used for weight-based dosing in children who cannot take tablets.

**Uses**: 1 kept, 2 added

- NEW: Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)
- NEW: Drug-susceptible TB meningitis, intensive 6-month regimen (6HRZEto) at a higher dose (MSF)

**Side effects**: 5 kept, 4 added

- NEW: Headache, dizziness, irritability, insomnia (rare)
- NEW: Sideroblastic anaemia, angioedema, hypertension and pellagra (very rare)
- NEW: Erythema multiforme (very rare)
- NEW: Fever, malaise and urticaria

**Precautions**: 3 kept, 4 added

- NEW: Acute liver disease (e.g., hepatitis) and up to 6 months after hepatitis (UK SmPC)
- NEW: Acute porphyria
- NEW: Hyperuricaemia
- NEW: Breast-feeding (UK SmPC; MSF lists no contraindication)

**Interactions**: 2 kept, 5 added

- NEW: Blood glucose-lowering drugs: pyrazinamide may affect glucose control; monitor glucose more closely in diabetes.
- NEW: Rifampicin: pyrazinamide may lower rifampicin levels (UK SmPC).
- NEW: Oestrogen-containing contraceptives: effect may be reduced.
- NEW: Oral typhoid vaccine: avoid pyrazinamide for 3 days before and after vaccination.
- NEW: Alcohol: avoid; heavy drinking raises the risk of liver damage.

**Disease links added**

- `gout`: **avoid**: Contraindicated in hyperuricaemia and acute gouty arthritis; give only if treatment is urgent, monitor uric acid and stop if acute gout develops (UK SmPC).
- `type2_diabetes`: **caution**: High doses may affect glucose control; monitor diabetic patients more closely (UK SmPC).
- `chronic_kidney_disease`: **caution**: Give 25 mg/kg three times a week in renal insufficiency (MSF); UK SmPC advises reduced dose and frequency.
- `hepatitis_b`: **caution**: Contraindicated in acute hepatitis and for 6 months after (UK SmPC); applying this to hepatitis B is an inference, not stated for HBV specifically.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | TB Cat I intensive (2HRZE), 30–37 kg (HRZE = H75/R150/Z400/E275 mg) | PO | 2 tablets HRZE FDC | Once a day | 2 months | — | NTP MOP 2014 |
| adult | TB Cat I intensive (2HRZE), 38–54 kg | PO | 3 tablets HRZE FDC | Once a day | 2 months | — | NTP MOP 2014 |
| adult | TB Cat I intensive (2HRZE), 55–70 kg | PO | 4 tablets HRZE FDC | Once a day | 2 months | — | NTP MOP 2014 |
| adult | TB Cat I intensive (2HRZE), >70 kg (Cat II: HRZE months 1–3, same tablet numbers) | PO | 5 tablets HRZE FDC | Once a day | 2 months | — | NTP MOP 2014 |
| adult | TB, single-drug formulation | PO | 25 mg/kg (range 20–30) | Once a day | Intensive phase | 2 g/day | NTP MOP 2014 |
| adult | TB, standard regimen | PO | 1.5 g (<50 kg); 2 g (≥50 kg) | Once a day | 2 months | 2 g/day | Label · UK SmPC |
| adult | TB, intermittent supervised regimen (Only if daily dosing is not feasible) | PO | 2 g (<50 kg); 2.5 g (≥50 kg) | 3× a week | 2 months | — | Label · UK SmPC |
| adult | TB meningitis (6HRZEto) | PO | 40 mg/kg | Once a day | 6 months | 2 g/day | MSF TB |
| child | TB, single-drug formulation (Suspension 250 mg/5 mL dosed by weight (Table 14); newborn <4 weeks: refer) | PO | 30 mg/kg (range 20–40) | Once a day | Intensive phase | 2 g/day | NTP MOP 2014 |
| child | TB, child <30 kg (150 mg dispersible tablet in 10 mL water) | PO | 35 mg/kg (range 30–40) | Once a day | Intensive phase | 2 g/day | MSF TB |
| child | TB intensive phase, HRZ 50/75/150 FDC (Plus ethambutol where indicated) | PO | 4–7 kg: 1; 8–11 kg: 2; 12–15 kg: 3; 16–22 kg: 4 tablets | Once a day | 2 months | — | MSF FDC |

- *renal* Renal insufficiency: 25 mg/kg three times a week. [MSF TB]
- *renal*: UK label: reduce dose and frequency; use only in emergencies, given intermittently. [Label · UK SmPC]
- *hepatic*: Contraindicated in severe hepatic impairment, acute liver disease and for 6 months after hepatitis. If hepatocellular damage occurs, stop and do not restart. Heavy drinkers and patients on other hepatotoxic drugs are at higher risk. [Label · UK SmPC]
- *pregnancy*: MSF: no contraindication in pregnancy or breastfeeding. The UK SmPC states clinical data in pregnancy are insufficient (use only if benefit clearly outweighs risk) and contraindicates breastfeeding because it passes into milk. [MSF TB]
- *administration*: Take with or without food. For GI upset, give at bedtime or with small meals. Advise sun protection (photosensitivity). [NTP MOP 2014]
- *forms_ph*: Only in fixed-dose combinations (List B): isoniazid + rifampicin + pyrazinamide + ethambutol 75/150/400/275 mg tablet; isoniazid + rifampicin + pyrazinamide 50/75/150 mg dispersible tablet (pediatric). A single-ingredient pyrazinamide entry could not be read in the PNF text (it stops at 'M'). [PNF]
- *monitor*: LFTs (AST, ALT) before starting and every 2–4 weeks; kidney function every 3–4 weeks. [Label · UK SmPC]
- *monitor*: Arthralgia: give aspirin or an NSAID; if it persists, check serum uric acid and consider gout. [NTP MOP 2014]
- *monitor*: Blood glucose in diabetes; uric acid in patients with gout history. [Label · UK SmPC]

**References added**

- [Philippine NTP Manual of Procedures](https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf): Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.
- [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.
- [MSF Tuberculosis guideline](https://medicalguidelines.msf.org/en/viewport/TUB/english/pyrazinamide-z-20323874.html): Médecins Sans Frontières. Tuberculosis - Appendix 10, TB drug information sheets: Pyrazinamide (Z). Updated January 2022.
- [MSF Tuberculosis guideline](https://medicalguidelines.msf.org/en/node/1205): Médecins Sans Frontières. Tuberculosis - Appendix 13. Daily dose of TB drugs using fixed-dose combinations. Updated October 2022.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=pyrazinamide#emc-101051): Pyrazinamide 500 mg Tablets - Summary of Product Characteristics. Morningside Healthcare Ltd. Electronic medicines compendium (emc), updated June 2025.
- Dosing source `NTP MOP 2014`: [Philippine NTP Manual of Procedures](https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf): DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 11–15).
- Dosing source `PNF`: [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.
- Dosing source `MSF TB`: [MSF Tuberculosis guideline](https://medicalguidelines.msf.org/en/viewport/TUB/english/pyrazinamide-z-20323874.html): MSF Tuberculosis, Appendix 10: Pyrazinamide (Z), 2022.
- Dosing source `MSF FDC`: [MSF Tuberculosis guideline](https://medicalguidelines.msf.org/en/node/1205): MSF Tuberculosis, Appendix 13: daily dose of TB drugs using FDCs, 2022.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=pyrazinamide#emc-101051): Pyrazinamide 500 mg Tablets - SmPC. Morningside Healthcare Ltd, 2025.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Isoniazid + Rifampicin + Pyrazinamide (B) 50 mg + 75 mg + 150 mg dispersible FDC tablet; Isoniazid + Rifampicin + Pyrazinamide + Ethambutol (B) 75 + 150 + 400 + 275 mg tablet. PDF text (65,922 chars) ends at 'Multivitamins', so no standalone pyrazinamide entry could be checked.
- https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf: Table 10: Cat I 2HRZE/4HR, Ia 2HRZE/10HR, II 2HRZES/1HRZE/5HRE, IIa; Table 11 HRZE tablets 30–37 kg 2, 38–54 kg 3, 55–70 kg 4, >70 kg 5; Table 13 pyrazinamide adults 25 (20–30) mg/kg, children 30 (20–40) mg/kg, max 2 g daily; Table 14 pyrazinamide 250 mg/5 ml by weight 2.1–30 kg, newborn <4 weeks refer; Table 15 GI intolerance (R/H/Z): bedtime or small meals; arthralgia due to hyperuricemia (Z): aspirin/NSAID, uric acid. (Text read via offsets 95000/100000; PDF text ends ~110951.)
- https://medicalguidelines.msf.org/en/viewport/TUB/english/pyrazinamide-z-20323874.html: MSF TB Pyrazinamide (Jan 2022): 400 mg tab, 150 mg dispersible; <30 kg 35 (30–40) mg/kg, ≥30 kg and adults 25 (20–30) mg/kg, max 2000 mg; renal insufficiency 25 mg/kg three times a week; TB meningitis 6HRZEto 40 mg/kg max 2000 mg; not in severe hepatic impairment or severe gout; no contraindication in pregnancy/breastfeeding; with or without food; protect skin from sun.
- https://medicalguidelines.msf.org/en/node/1205: Appendix 13 (Oct 2022): child intensive HZR 50/150/75: 4–7 kg 1, 8–11 kg 2, 12–13 kg 3, 14–15 kg 3, 16–17 kg 4, 18–22 kg 4.
- https://products.mhra.gov.uk/search/?search=pyrazinamide#emc-101051: Pyrazinamide 500 mg (Morningside, June 2025): adults <50 kg up to 1.5 g, >50 kg up to 2 g daily; intermittent 3×/week 2 g / 2.5 g; children 35 mg/kg/day max 1.5 g; contraindications incl. acute liver disease/hepatitis and up to 6 months after, acute porphyria, hyperuricaemia/gout, breast-feeding; LFTs every 2–4 weeks, liver/kidney every 3–4 weeks; diabetes monitoring; renal: emergencies, intermittent; interactions: glucose-lowering drugs, may reduce rifampicin, oestrogen contraceptives, oral typhoid vaccine 3 days, alcohol; ADRs rare headache/dizziness/irritability/insomnia; very rare erythema multiforme, tubulo-interstitial nephritis, sideroblastic anaemia, angioedema, hypertension, pellagra; not known fever, malaise, urticaria.

---

## Rabies Immunoglobulin (HRIG / ERIG)  (`med_rabies_immunoglobulin`)

**Description (kept)**

Rabies immunoglobulin provides ready-made rabies virus-neutralizing antibodies, prepared from the plasma of immunized human donors (HRIG) or from hyperimmunized horses as purified equine immunoglobulin or F(ab')2 fragments (ERIG). Infiltrated into and around the wound, it neutralizes virus at the inoculation site before vaccine-induced antibodies appear. It is used with rabies vaccine for category III exposures in persons not previously vaccinated.

**Description (added)**

In the Philippine public program, the DOH supplies only equine RIG to government Animal Bite Treatment Centers, and patients often pay out of pocket for it when stocks run out. Under DOH Administrative Order 2018-0013, RIG volume left after wound infiltration need not be injected IM and may be kept aseptically and fractionated for the next patient. When supply is limited, WHO gives priority to multiple or deep bites, bites to highly innervated parts of the body, severely immunodeficient patients, exposures to confirmed or probable rabid animals, and bat exposures.

**Uses**: 4 kept, 3 added

- NEW: Category II exposures to the head or neck, which DOH manages as category III (vaccine plus RIG)
- NEW: Category II as well as category III exposures in immunocompromised patients (DOH, MSF)
- NEW: Infants born to rabid mothers, with vaccine, as early as possible after birth (DOH)

**Side effects**: 5 kept, 1 added

- NEW: Fever and joint pain (MSF)

**Precautions**: 4 kept, 2 added

- NEW: Finger or toe wounds: infiltrate cautiously to avoid raised compartment pressure or impaired circulation
- NEW: Aspirate before injecting; intravascular injection risks shock (MSF)

**Interactions**: 4 kept, 1 added

- NEW: Other vaccines given the same day: use separate syringes and injection sites (MSF).

**Disease links added**

- `hiv_infection`: **safe**: HIV/AIDS counts as immunocompromised: DOH gives RIG with the standard IM vaccine regimen for both category II and III exposures.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Category III exposure, HRIG (Infiltrate full dose into and around wound(s); 150 IU/mL, 2 mL vial) | Infiltration | 20 IU/kg | Single dose | Day 0 (up to day 7) | 20 IU/kg | DOH AO 2018 |
| adult | Category III exposure, ERIG / F(ab')2 (200 IU/mL, 5 mL vial; e.g. 50 kg = 2000 IU = 10 mL) | Infiltration | 40 IU/kg | Single dose | Day 0 (up to day 7) | 40 IU/kg | DOH AO 2018 |
| adult | Category III exposure (WHO) (As much as possible into the wound) | Infiltration | HRIG 20 IU/kg; ERIG 40 IU/kg | Single dose | ≤ day 7 after first vaccine dose | 20 / 40 IU/kg; no minimum | WHO 2018 |
| child | Category III exposure, HRIG (Same dose for all ages) | Infiltration | 20 IU/kg | Single dose | Day 0 (up to day 7) | 20 IU/kg | MSF |
| child | Category III exposure, ERIG / F(ab')2 (If HRIG unavailable) | Infiltration | 40 IU/kg | Single dose | Day 0 (up to day 7) | 40 IU/kg | MSF |

- *administration*: If the computed dose is too small to cover all wounds, dilute it 2–3-fold with sterile 0.9% saline; never exceed the computed dose. Infiltrate even healed wounds. [DOH AO 2018]
- *administration*: Use a 23–24 G, 1-inch needle and avoid repeated needle punctures into the same wound. Delay suturing for at least 2 hours after RIG if suturing cannot be avoided. [DOH AO 2018]
- *administration*: If RIG and vaccine cannot be given on the same day, give the vaccine first; RIG is given only once per PEP course and is not indicated after day 7. [DOH AO 2018]
- *administration*: Leftover RIG may be fractionated aseptically for other patients; remaining volume does not need IM injection. [WHO 2018]
- *administration*: DOH still highly recommends an ERIG skin test, whereas WHO 2018 says skin testing is unnecessary and should be abandoned; follow the local program protocol. [DOH AO 2018]
- *pregnancy*: Pregnancy and infancy are not contraindications to RIG; no contraindication in breast-feeding. [DOH AO 2018]
- *monitor*: Observe patients for at least 1 hour after ERIG, with epinephrine available. [DOH AO 2018]
- *monitor*: After infiltrating fingers or toes, check circulation and signs of raised compartment pressure. [MSF]

**References added**

- [DOH Administrative Order 2018-0013](https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures): Department of Health (Philippines). Administrative Order No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 16 April 2018. (Text reproduced on LegalDex.)
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/human-rabies-immunoglobulin-hrig-16688380.html): Médecins Sans Frontières. Essential drugs – Human rabies immunoglobulin (HRIG). MSF Medical Guidelines.
- [WHO PEP recommendations](https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations): World Health Organization. Rabies: PEP recommendations – WHO recommends the intradermal route for rabies post-exposure prophylaxis. WHO Control of Neglected Tropical Diseases.
- [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186): Amparo ACB, Jayme SI, Roces MCR, et al. The evaluation of operating Animal Bite Treatment Centers in the Philippines from a health provider perspective. PLoS ONE. 2018;13(7):e0199186.
- Dosing source `DOH AO 2018`: [DOH Administrative Order 2018-0013](https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures): Department of Health (Philippines). AO No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 2018.
- Dosing source `WHO 2018`: [WHO position paper (summary)](https://cdn.who.int/media/docs/default-source/immunization/position_paper_documents/rabies/pp-rabies-summary-2018.pdf): World Health Organization. Rabies vaccines and immunoglobulins: WHO position, April 2018 (summary).
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/human-rabies-immunoglobulin-hrig-16688380.html): Médecins Sans Frontières. Essential drugs – Human rabies immunoglobulin (HRIG).

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: WebFetch text of the PNF-EML PDF runs only from Abacavir to Multivitamins (offset 50000 also ends at M; total 65,922 chars). No rabies immunoglobulin entry readable, so no forms_ph note written.
- https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures: DOH AO 2018-0013 (16 Apr 2018), Revised Guidelines on the Management of Rabies Exposures: HRIG 20 IU/kg max, 150 IU/mL 2 mL vial; ERIG/F(ab')2 40 IU/kg max, 200 IU/mL 5 mL vial; 50 kg example 1000 IU = 6.7 mL / 2000 IU = 10 mL; infiltrate full dose even if healed; 23–24 G 1-inch needle; leftover need not be IM, may be fractionated; dilute 2–3x saline, do not exceed dose; caution fingers/toes; delay suturing ≥2 h; give with day 0 vaccine, up to day 7; vaccine first if not same day; once per course; observe ≥1 h after ERIG; ERIG skin testing highly recommended; category II head/neck managed as category III; immunocompromised (systemic steroids, chemo, HIV/AIDS) get standard IM regimen + RIG for category II and III; pregnancy and infancy not contraindications; infants of rabid mothers get vaccine + RIG ASAP after birth.
- https://cdn.who.int/media/docs/default-source/immunization/position_paper_documents/rabies/pp-rabies-summary-2018.pdf: WHO 2018 summary: max dose 20 IU/kg hRIG, 40 IU/kg eRIG, no minimum; once, no later than day 7; infiltrate as much as possible into the wound; leftover fractionated aseptically; eRIG skin testing unnecessary; RIG prioritisation (multiple/deep bites, highly innervated parts, severe immunodeficiency, confirmed/probable rabid animal, bat exposures); vaccine never withheld for lack of RIG.
- https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations: WHO PEP recommendations page: category III gets RIG with vaccine plus immediate wound washing; ID 0.1 mL 2 sites days 0, 3, 7.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/human-rabies-immunoglobulin-hrig-16688380.html: MSF HRIG: 20 IU/kg child and adult on D0 with first vaccine; infiltrate into/around wounds; dilute 2–3-fold with 0.9% NaCl for multiple wounds; up to D7; indicated for category II and III in immunocompromised even after PrEP; AEs fever, headache, GI, joint pain, local pain, rare anaphylaxis; aspirate before injecting (shock risk); caution finger wounds (compartment pressure); separate syringes/sites with vaccines; no contraindication in pregnancy/breast-feeding; ERIG F(ab')2 40 IU/kg as substitute.
- https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186: Amparo et al. 2018 PLoS ONE: only equine RIG provided by DOH (no HRIG); patients often paid out of pocket for eRIG when stocks ran out; PhilHealth ABT package PHP 3,000 covers vaccine and RIG for category III exposures.

---

## Rabies Vaccine (PVRV / PCECV)  (`med_rabies_vaccine`)

**Description (kept)**

Cell-culture rabies vaccines contain inactivated rabies virus grown in Vero cells (PVRV) or chick embryo cells (PCECV). They induce virus-neutralizing antibodies, which take time to develop, so post-exposure prophylaxis combines immediate wound washing, a vaccine course and, for category III exposures, rabies immunoglobulin to cover the gap. Because clinical rabies is almost always fatal, post-exposure prophylaxis has no contraindication.

**Description (added)**

WHO recommends the intradermal route for PEP because it uses 60–80% less vaccine (1–2 vials per course versus 4–5 for intramuscular schedules) and a single vial can be shared between several patients. Philippine Animal Bite Treatment Centers (513 by July 2017) give the vaccine almost exclusively intradermally using the modified 2-site Thai Red Cross regimen, and DOH requires WHO-prequalified vaccine for PEP. Since 2016, government policy has provided all four vaccine visits free of charge, although stock-outs still force some patients to buy vaccine privately.

**Uses**: 4 kept, 2 added

- NEW: Infants born to rabid mothers: vaccine together with RIG as early as possible after birth (DOH)
- NEW: Pre-exposure prophylaxis for people in remote rabies-endemic areas with poor PEP access or dog-bite incidence above 5% per year (WHO)

**Precautions**: 4 kept, 2 added

- NEW: Nerve-tissue vaccines should be avoided: less immunogenic and more severe adverse effects than cell-culture vaccines (MSF)
- NEW: Intradermal route only where correct ID technique can be assured; otherwise use IM (MSF)

**Interactions**: 4 kept, 2 added

- NEW: Other vaccines given the same day: use separate syringes and injection sites (MSF).
- NEW: Chronic liver disease, chloroquine use or systemic steroids: DOH gives the standard IM regimen, without delaying vaccination.

**Disease links added**

- `hiv_infection`: **caution**: HIV/AIDS counts as immunocompromised: DOH uses the standard IM regimen (not the ID regimen) plus RIG for category II and III exposures; WHO adds a third PrEP dose on day 21–28.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | PEP, category II/III (DOH ID regimen) (One dose per deltoid; day 28 may be omitted with WHO-prequalified vaccine (2-2-2-0-0)) | ID | 0.1 mL at 2 sites | Days 0, 3, 7, 28 | 4 visits (2-2-2-0-2) | — | DOH AO 2018 |
| adult | PEP, category II/III (WHO 1-week ID) (Category III: plus RIG) | ID | 0.1 mL at 2 sites | Days 0, 3, 7 | 1 week | — | WHO 2018 |
| adult | PEP, Zagreb (2-0-1-0-1) (Day 0 dose in both deltoids) | IM | 0.5 mL PVRV or 1 mL PCECV | 2 doses day 0; 1 dose days 7, 21 | 3 weeks | — | DOH AO 2018 |
| adult | PEP, shortened IM (1-1-1-1-0) (WHO: 4th dose any day from 14 to 28) | IM | 0.5 mL PVRV or 1 mL PCECV | Days 0, 3, 7, 14 | 2 weeks | — | DOH AO 2018 |
| adult | PEP, previously vaccinated (Or 0.1 mL at 4 sites on day 0; no RIG; IM boosters discouraged) | ID | 0.1 mL at 1 site | Days 0, 3 | 2 visits | — | DOH AO 2018 |
| adult | PrEP, immunocompetent (Or 1 vial IM at 1 site on days 0, 7) | ID | 0.1 mL at 2 sites | Days 0, 7 | 1 week | — | WHO 2018 |
| adult | PrEP, immunocompromised (WHO: ID or IM plus third dose day 21–28) | IM | 1 vial (0.5 mL PVRV / 1 mL PCECV) | Days 0, 7, 21–28 | 3–4 weeks | — | DOH AO 2018 |
| child | PEP, category II/III (DOH ID regimen) (Same dose as adults; anterolateral thigh in infants) | ID | 0.1 mL at 2 sites | Days 0, 3, 7, 28 | 4 visits (2-2-2-0-2) | — | DOH AO 2018 |
| child | PEP, IM regimens (Anterolateral thigh if < 2 y; deltoid if ≥ 2 y; never gluteal) | IM | 0.5 mL PVRV or 1 mL PCECV | As adult schedule | 2–3 weeks | — | MSF |
| child | PrEP, immunocompetent (Schedules apply to all age groups) | ID | 0.1 mL at 2 sites | Days 0, 7 | 1 week | — | WHO 2018 |

- *forms_ph*: DOH program vaccines: PVRV 0.5 mL/vial and PCECV 1 mL/vial (powder with diluent); ID dose 0.1 mL for both. PNF entry not readable. [DOH AO 2018]
- *administration*: Each ID dose must raise a wheal of at least 3 mm (1 mL syringe, 27 G needle); repeat any dose given SC or IM by mistake. [DOH AO 2018]
- *administration*: A delayed dose does not restart the schedule; changing vaccine product or route mid-course is acceptable if unavoidable. [DOH AO 2018]
- *administration*: Biting dog or cat is observed for 14 days; non-WHO-prequalified PEP is stopped if the animal stays healthy. New exposure within 3 months of completed PEP needs wound care only (WHO). [DOH AO 2018]
- *administration*: Start PEP as soon as possible even if the patient presents long after exposure; check national schedules (MSF). [MSF]
- *administration*: DOH allows reconstituted vaccine to be kept refrigerated and used within 8 hours (enables ID vial sharing); MSF says use immediately. [DOH AO 2018]
- *pregnancy*: Pregnancy and infancy are not contraindications to PVRV or PCECV; none in breast-feeding (MSF). [DOH AO 2018]
- *monitor*: Anaphylaxis: epinephrine 0.1% 0.5 mL (adults) or 0.01 mL/kg, max 0.5 mL (children), repeat every 10–20 min up to 3 doses; then steroids. Record and report severe adverse events. [DOH AO 2018]
- *monitor*: Routine boosters or neutralizing-antibody serology after PrEP only if exposure risk remains high. [WHO 2018]

**References added**

- [DOH Administrative Order 2018-0013](https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures): Department of Health (Philippines). Administrative Order No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 16 April 2018. (Text reproduced on LegalDex.)
- [WHO PEP recommendations](https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations): World Health Organization. Rabies: PEP recommendations – WHO recommends the intradermal route for rabies post-exposure prophylaxis. WHO Control of Neglected Tropical Diseases.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/rabies-vaccine-16687811.html): Médecins Sans Frontières. Essential drugs – Rabies vaccine. MSF Medical Guidelines.
- [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186): Amparo ACB, Jayme SI, Roces MCR, et al. The evaluation of operating Animal Bite Treatment Centers in the Philippines from a health provider perspective. PLoS ONE. 2018;13(7):e0199186.
- Dosing source `DOH AO 2018`: [DOH Administrative Order 2018-0013](https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures): Department of Health (Philippines). AO No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 2018.
- Dosing source `WHO 2018`: [WHO position paper (summary)](https://cdn.who.int/media/docs/default-source/immunization/position_paper_documents/rabies/pp-rabies-summary-2018.pdf): World Health Organization. Rabies vaccines and immunoglobulins: WHO position, April 2018 (summary).
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/rabies-vaccine-16687811.html): Médecins Sans Frontières. Essential drugs – Rabies vaccine.

**What was checked on each page**

- https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures: DOH AO 2018-0013: Table 2 PVRV 0.5 mL/vial, PCECV 1 mL/vial, ID 0.1 mL, IM 0.5/1.0 mL; ID PEP 2-2-2-0-2 (days 0, 3, 7, 28), day 28 omissible for WHO-prequalified (2-2-2-0-0); wheal ≥3 mm, 1 mL 27G syringe, repeat if SC/IM; Zagreb 2-0-1-0-1 and 1-1-1-1-0 IM; never gluteal; PrEP ID/IM days 0, 7, 21/28 (21/28 dropped for immunocompetent with prequalified vaccine; full IM for immunocompromised); booster ID 1 site days 0, 3 or 4 sites day 0, IM boosters discouraged; immunocompromised standard IM + RIG; chronic liver disease/chloroquine/steroids standard IM no delay; pregnancy/infancy not contraindications; infants of rabid mothers vaccine + RIG; delayed dose continue; product/route change acceptable; 14-day animal observation; anaphylaxis epinephrine doses; reconstituted refrigerated use within 8 h; 2–8 °C.
- https://cdn.who.int/media/docs/default-source/immunization/position_paper_documents/rabies/pp-rabies-summary-2018.pdf: WHO 2018 summary: PrEP 2-site ID or 1-site IM days 0 and 7, all ages; IM <2 y anterolateral thigh, ≥2 y deltoid; immunocompromised PrEP third dose day 21–28 and full PEP with RIG; PEP ID 2-site days 0, 3, 7; IM 1-site days 0, 3, 7 + one dose day 14–28; Zagreb; previously immunized 1-site ID days 0, 3 or 4-site day 0, no RIG; new exposure within 3 months only wound care; delayed dose resume; booster/serology only if high risk persists; PrEP for remote areas with dog-bite incidence >5%/yr.
- https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations: WHO PEP page: ID recommended; reduces vaccine volume 60–80%; full ID course 1–2 vials vs IM 4–5 vials; one-week 2-site ID days 0, 3, 7; route/product change acceptable.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/rabies-vaccine-16687811.html: MSF rabies vaccine: CCEEV powder + diluent 0.5 or 1 mL; IM not gluteal, <2 y thigh, ≥2 y deltoid; ID 0.1 mL; Zagreb, Essen; continue schedule if delayed/route changed; start even if presenting late; check national schedules; ID only if correct technique assured else IM; separate syringes/sites with RIG or other vaccines; no contraindication in pregnancy/breast-feeding; avoid nerve-tissue vaccines; reconstituted use immediately.
- https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186: Amparo et al. 2018: 513 ABTCs by July 2017; ARV almost exclusively ID using modified 2-site Thai Red Cross regimen 2-2-2-0-2; immunocompromised/HIV get IM; only WHO pre-qualified vaccine; PVRV and PCECV; since 2016 all four ARV visits free; stock-outs force private purchase; single vial for multiple patients.

---

## Rifampicin  (`med_rifampicin`)

**Description (kept)**

Rifampicin inhibits bacterial DNA-dependent RNA polymerase, blocking transcription, and is bactericidal against Mycobacterium tuberculosis. It is a cornerstone of first-line TB therapy (with isoniazid, pyrazinamide and ethambutol) and is a potent inducer of CYP3A4 and other drug-metabolizing enzymes, causing many drug interactions.

**Description (added)**

In the Philippine NTP it is given throughout treatment in fixed-dose combinations (HRZE in the intensive phase, HR in the continuation phase of Category I 2HRZE/4HR; HRZE then HRE in Category II), with the number of tablets set by body-weight band. Single-drug rifampicin (including a 200 mg/5 mL suspension) is used for weight-based dosing in children who cannot take tablets.

**Uses**: 4 kept, 3 added

- NEW: Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)
- NEW: Brucellosis, Legionnaires' disease and serious staphylococcal infections, with another antibiotic
- NEW: Chemoprophylaxis of Haemophilus influenzae: carriers and exposed children aged 4 years or younger

**Side effects**: 7 kept, 7 added

- NEW: Fever and chills (very common)
- NEW: Paradoxical reaction: TB symptoms recur after initial improvement, usually without treatment failure
- NEW: Thrombotic microangiopathy (TTP/HUS); stop if suspected
- NEW: Interstitial lung disease / pneumonitis
- NEW: Adrenal insufficiency in patients with compromised adrenal function
- NEW: Tooth discolouration (may be permanent)
- NEW: Headache and drowsiness

**Precautions**: 3 kept, 3 added

- NEW: Jaundice
- NEW: History of severe haematological disorders (thrombocytopenia, purpura) during previous rifamycin treatment
- NEW: Concomitant sofosbuvir, daclatasvir or telaprevir

**Interactions**: 6 kept, 9 added

- NEW: Dolutegravir: levels fall substantially; dolutegravir is given 50 mg twice daily with rifampicin.
- NEW: Nevirapine, lopinavir/ritonavir or atazanavir/ritonavir: use rifabutin instead of rifampicin (MSF).
- NEW: Fluconazole: give 12 hours apart (rifampicin in the morning, fluconazole in the evening).
- NEW: Antacids: take rifampicin at least 1 hour before the antacid.
- NEW: Para-aminosalicylic acid: give at least 8 hours apart.
- NEW: Cefazolin and other cephalosporins with an NMTT side chain: avoid (risk of severe coagulation disorders).
- NEW: Paracetamol: may increase hepatotoxicity risk.
- NEW: Clopidogrel: concomitant use is discouraged; halothane: avoid.
- NEW: Phenytoin and hepatitis C direct-acting antivirals: reduced effect.

**Disease links added**

- `hepatitis_b`: **caution**: Hepatic impairment: do not exceed 8 mg/kg/day and monitor LFTs closely; contraindicated with jaundice (UK SmPC, MSF). Applying this to hepatitis B is an inference.
- `type2_diabetes`: **caution**: Rifampicin reduces the effect of antidiabetic drugs; doses may need adjusting (MSF).
- `chronic_kidney_disease`: **caution**: No adjustment up to 600 mg/day; caution if the dose exceeds 600 mg/day (UK SmPC).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | TB Cat I (2HRZE/4HR), 30–37 kg (Cat Ia (CNS, bones, joints): HR for 10 months) | PO | 2 tablets HRZE, then 2 tablets HR | Once a day | 2 + 4 months | — | NTP MOP 2014 |
| adult | TB Cat I (2HRZE/4HR), 38–54 kg | PO | 3 tablets HRZE, then 3 tablets HR | Once a day | 2 + 4 months | — | NTP MOP 2014 |
| adult | TB Cat I (2HRZE/4HR), 55–70 kg | PO | 4 tablets HRZE, then 4 tablets HR | Once a day | 2 + 4 months | — | NTP MOP 2014 |
| adult | TB Cat I (2HRZE/4HR), >70 kg (Each tablet contains rifampicin 150 mg) | PO | 5 tablets HRZE, then 5 tablets HR | Once a day | 2 + 4 months | — | NTP MOP 2014 |
| adult | TB, single-drug formulation (Usually 450 mg if <50 kg, 600 mg if ≥50 kg (UK SmPC)) | PO | 10 mg/kg (range 8–12) | Once a day | Per regimen | 600 mg/day | NTP MOP 2014 |
| adult | TB meningitis (6HRZEto) | PO | 20 mg/kg | Once a day | 6 months | 600 mg/day | MSF TB |
| adult | Latent TB infection | PO | 10 mg/kg | Once a day | 4 months alone; 3 months with isoniazid | 600 mg/day | MSF |
| adult | Leprosy (With dapsone and clofazimine) | PO | 600 mg | Once a month | 6 months (PB); 12 months (MB) | — | MSF |
| adult | Brucellosis, Legionnaires', serious staphylococcal infection (Always with another antibiotic) | PO | 600–1200 mg/day ÷ 2–4 | 2–4× a day | Brucellosis: 6 weeks | 1200 mg/day | Label · UK SmPC |
| adult | Meningococcal carrier eradication | PO | 600 mg | 2× a day | 2 days | — | Label · UK SmPC |
| child | TB, single-drug formulation (Suspension 200 mg/5 mL dosed by weight (Table 14); newborn <4 weeks: refer) | PO | 15 mg/kg (range 10–20) | Once a day | Per regimen | 600 mg/day | NTP MOP 2014 |
| child | TB meningitis (6HRZEto) | PO | 20 mg/kg | Once a day | 6 months | 600 mg/day | MSF TB |
| child | Leprosy, <10 y / 10–14 y | PO | 10 mg/kg / 450 mg | Once a month | 6 months (PB); 12 months (MB) | — | MSF |
| child | Meningococcal carriers, 1–12 y (Infants 3–12 months: 5 mg/kg) | PO | 10 mg/kg | 2× a day | 2 days | — | Label · UK SmPC |
| child | H. influenzae chemoprophylaxis (Neonates (1 month): 10 mg/kg) | PO | 20 mg/kg | Once a day | 4 days | 600 mg/day | Label · UK SmPC |

- *hepatic*: Do not exceed 8 mg/kg/day. Contraindicated in jaundice. Monitor ALT/AST weekly for 2 weeks, then every 2 weeks for the next 6 weeks; stop if hepatocellular damage occurs. [Label · UK SmPC]
- *renal*: No adjustment up to 600 mg/day; use caution if the dose exceeds 600 mg/day. [Label · UK SmPC]
- *elderly*: Use with caution, especially if liver function is impaired. [Label · UK SmPC]
- *pregnancy*: Not contraindicated. Given in the last weeks of pregnancy it can cause bleeding in mother and newborn: give vitamin K (phytomenadione) to both. Not contraindicated in breastfeeding (MSF); passes into breast milk (UK SmPC). [MSF]
- *administration*: Take on an empty stomach, at least 30 minutes before or 2 hours after a meal; a small amount of food may be used to improve GI tolerance (MSF). Take at least 1 hour before antacids. [Label · UK SmPC]
- *administration*: Advise women on hormonal contraception to switch to injectable medroxyprogesterone or an IUD. [MSF]
- *forms_ph*: Only in fixed-dose combinations (List B): isoniazid + rifampicin 50/75 mg dispersible tablet (pediatric) and 75/150 mg tablet; isoniazid + rifampicin + ethambutol 75/150/275 mg; isoniazid + rifampicin + pyrazinamide 50/75/150 mg dispersible; isoniazid + rifampicin + pyrazinamide + ethambutol 75/150/400/275 mg. A single-ingredient rifampicin entry could not be read in the PNF text (it stops at 'M'). [PNF]
- *monitor*: Baseline LFTs, blood count and renal function in adults with TB. Stop if purpura, thrombocytopenia or signs of TMA appear. [Label · UK SmPC]
- *monitor*: Dosing less often than 2–3 times a week raises the risk of immune reactions (flu-like syndrome, anaphylaxis); monitor closely. [Label · UK SmPC]
- *monitor*: Reassure about orange-red urine and secretions; soft contact lenses can be permanently stained. [NTP MOP 2014]

**References added**

- [Philippine NTP Manual of Procedures](https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf): Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.
- [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.
- [MSF Tuberculosis guideline](https://medicalguidelines.msf.org/en/viewport/TUB/english/rifampicin-r-20323858.html): Médecins Sans Frontières. Tuberculosis - Appendix 10, TB drug information sheets: Rifampicin (R). Updated January 2022.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/node/570): Médecins Sans Frontières. Essential drugs - practical guidelines: Rifampicin (R) oral. Updated June 2021.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=rifampicin#emc-6384): Rifadin 300 mg Capsules - Summary of Product Characteristics. Aventis Pharma Ltd (Sanofi). Electronic medicines compendium (emc), updated June 2026.
- Dosing source `NTP MOP 2014`: [Philippine NTP Manual of Procedures](https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf): DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 11–15).
- Dosing source `PNF`: [Philippine National Formulary (PNF) EML](https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf): Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.
- Dosing source `MSF TB`: [MSF Tuberculosis guideline](https://medicalguidelines.msf.org/en/viewport/TUB/english/rifampicin-r-20323858.html): MSF Tuberculosis, Appendix 10: Rifampicin (R), 2022.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/node/570): MSF Essential drugs: Rifampicin (R) oral, 2021.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=rifampicin#emc-6384): Rifadin 300 mg Capsules - SmPC. Sanofi, 2026.

**What was checked on each page**

- https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf: Isoniazid + Rifampicin (B) 50 + 75 mg dispersible FDC (pediatric) and 75 + 150 mg tablet; Isoniazid + Rifampicin + Ethambutol (B) 75 + 150 + 275 mg; Isoniazid + Rifampicin + Pyrazinamide (B) 50 + 75 + 150 mg dispersible; Isoniazid + Rifampicin + Pyrazinamide + Ethambutol (B) 75 + 150 + 400 + 275 mg. PDF text ends at 'Multivitamins', so no standalone rifampicin entry could be checked.
- https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf: Table 10 regimens (Cat I 2HRZE/4HR, Ia 2HRZE/10HR, II 2HRZES/1HRZE/5HRE); Table 11 HRZE/HR tablets 30–37 kg 2, 38–54 kg 3, 55–70 kg 4, >70 kg 5, continuation same per band; Table 13 rifampicin adults 10 (8–12) mg/kg, children 15 (10–20) mg/kg, max 600 mg daily; Table 14 rifampicin 200 mg/5 ml by weight 2.1–30 kg, newborn <4 weeks refer; Table 15 orange/red urine (R): reassure; GI intolerance: bedtime or small meals.
- https://medicalguidelines.msf.org/en/viewport/TUB/english/rifampicin-r-20323858.html: MSF TB Rifampicin (Jan 2022): <30 kg 15 (10–20) mg/kg; ≥30 kg and adults 10 (8–12) mg/kg; max 600 mg; hepatic impairment max 8 mg/kg; TB meningitis 6HRZEto 20 mg/kg max 600 mg; contraindicated after severe haematologic disorders with previous rifamycin; reduces antidiabetics, phenytoin, HCV DAAs, etc.; fluconazole 12 h apart; contraception DMPA or IUD; vitamin K late pregnancy.
- https://medicalguidelines.msf.org/en/node/570: MSF Essential drugs Rifampicin oral (June 2021): latent TB 4 months alone/3 months with isoniazid; leprosy monthly <10 y 10 mg/kg, 10–14 y 450 mg, ≥15 y 600 mg, PB 6 months, MB 12 months; brucellosis 6 weeks; contraindications jaundice, rifamycin hypersensitivity, prior severe haematological disorders; headache, drowsiness; nevirapine, LPV/r, ATV/r -> rifabutin; not contraindicated in pregnancy/breastfeeding; vitamin K.
- https://products.mhra.gov.uk/search/?search=rifampicin#emc-6384: Rifadin 300 mg (Sanofi, June 2026): indications incl. brucellosis, Legionnaires', serious staph, meningococcal carriers, H. influenzae carriers/prophylaxis ≤4 y; TB adults 8–12 mg/kg, usually 450 mg <50 kg / 600 mg ≥50 kg; children 10–20 mg/kg max 600 mg; leprosy 600 mg monthly; brucellosis etc. 600–1200 mg/day in 2–4 doses; meningococcal adults 600 mg BD 2 days, children 1–12 y 10 mg/kg BD, infants 3–12 mo 5 mg/kg; H. influenzae 20 mg/kg OD max 600 mg 4 days, neonates 10 mg/kg; hepatic max 8 mg/kg; renal caution >600 mg/day; elderly caution; 30 min before or 2 h after meal; contraindications jaundice, saquinavir/ritonavir, lurasidone, sofosbuvir, daclatasvir, telaprevir etc.; LFT weekly ×2 then 2-weekly ×6 weeks in hepatic impairment; baseline blood count/renal; TMA; intermittent <2–3×/week immunological reactions; teeth/contact lens discolouration; interactions PAS 8 h, antacids 1 h, halothane, cefazolin/NMTT, paracetamol, clopidogrel; vitamin K late pregnancy; ADRs pyrexia/chills, paradoxical reaction, adrenal insufficiency, ILD.

---

## Salbutamol (Albuterol)  (`med_salbutamol`)

**Description (kept)**

Salbutamol stimulates beta-2 adrenergic receptors on bronchial smooth muscle, activating adenylyl cyclase and relaxing the airways within minutes, with effects lasting 4-6 hours. It also inhibits mediator release from mast cells. It is used for relief and prevention of bronchospasm in asthma, COPD and exercise-induced bronchoconstriction.

**Description (added)**

For most asthma attacks a metered-dose inhaler with a spacer is easier, faster, at least as effective and better tolerated than a nebuliser, so nebulised salbutamol (with ipratropium) is reserved for severe attacks. In the Philippines, salbutamol is among the medicines of the PhilHealth Konsulta primary-care package as a metered-dose inhaler, dry powder inhaler, nebulising solution and syrup.

**Uses**: 2 kept, 1 added

- NEW: Severe acute asthma attack: nebulised, combined with ipratropium (MSF)

**Side effects**: 8 kept, 5 added

- NEW: Muscle cramps; mouth and throat irritation
- NEW: Peripheral vasodilatation
- NEW: Lactic acidosis with high-dose (e.g. nebulised) therapy
- NEW: Myocardial ischaemia (post-marketing, frequency unknown)
- NEW: Hypersensitivity: angioedema, urticaria, hypotension and collapse (very rare)

**Precautions**: 1 kept, 2 added

- NEW: Non-IV forms must not be used to stop uncomplicated premature labour or threatened abortion
- NEW: Nebuliser solution must never be given parenterally

**Interactions**: 4 kept, 2 added

- NEW: Xanthine derivatives and corticosteroids: may potentiate beta-2-agonist hypokalaemia.
- NEW: Nebulised ipratropium: acute angle-closure glaucoma reported with the combination; keep the mist out of the eyes.

**Disease links added**

- `type2_diabetes`: **caution**: Beta-2 agonists can raise blood glucose; the SmPC advises caution in diabetes.
- `acute_coronary_syndrome`: **caution**: Rare myocardial ischaemia reported; the SmPC advises patients with severe heart disease to seek advice for chest pain or worsening symptoms.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Acute bronchospasm (reliever) (MDI 100 micrograms/puff) | Inhaled | 100–200 micrograms (1–2 puffs) | As needed | — | 8 puffs/24 h | Label · UK SmPC |
| adult | Exercise or allergen prevention | Inhaled | 200 micrograms (2 puffs) | 10–15 min before challenge | — | 8 puffs/24 h | Label · UK SmPC |
| adult | Chronic therapy | Inhaled | 200 micrograms (2 puffs) | Up to 4× a day | — | 8 puffs/24 h | Label · UK SmPC |
| adult | Asthma attack, first hour (Then 2–4 puffs every 4–6 h for 24–48 h; spacer advised) | Inhaled | 200–1000 micrograms (2–10 puffs) | Every 20 min | 1 h | — | MSF |
| adult | Severe asthma attack (With ipratropium; switch to MDI as symptoms improve) | Inhaled | 5 mg nebulised | Every 20 min | First hour, then taper | — | MSF neb |
| adult | Bronchospasm (nebuliser) (Includes elderly and ≥ 12 y) | Inhaled | 2.5–5 mg nebulised | Up to 4× a day | — | 40 mg/day (hospital only) | Label · UK SmPC neb |
| child | Acute bronchospasm, < 12 y (May increase to 2 puffs; licensed from 4 y) | Inhaled | 100 micrograms (1 puff) | As needed | — | 8 puffs/24 h | Label · UK SmPC |
| child | Asthma attack, first hour (Same as adult; use a spacer (< 6 y)) | Inhaled | 200–1000 micrograms (2–10 puffs) | Every 20 min | 1 h | — | MSF |
| child | Severe asthma attack, < 5 y (With ipratropium) | Inhaled | 2.5 mg nebulised | Every 20 min | First hour, then taper | — | MSF neb |
| child | Severe asthma attack, 5–11 y (With ipratropium) | Inhaled | 2.5–5 mg nebulised | Every 20 min | First hour, then taper | — | MSF neb |
| child | Bronchospasm (nebuliser), 4–11 y (< 18 months: efficacy uncertain; transient hypoxia, consider oxygen) | Inhaled | 2.5–5 mg nebulised | Up to 4× a day | — | — | Label · UK SmPC neb |

- *forms_ph*: MDI 100 micrograms/dose × 200 actuations (also breath-actuated MDI); DPI 200 micrograms/dose; nebulising solution 1 mg/mL and 2 mg/mL, 2.5 mL unit dose; syrup 2 mg/5 mL, 60 mL. Combination ipratropium + salbutamol MDI and nebule. [PhilHealth]
- *administration*: Nebuliser: dilute with 0.9% sodium chloride to 4 mL total; stop when the reservoir is empty (about 10–15 min). [MSF neb]
- *administration*: Use a spacer for children under 6, older patients and severe dyspnoea; clean the mouthpiece before and after use. [MSF]
- *renal*: No renal dose adjustment is given in the SmPC; salbutamol is cleared partly renally. [Label · UK SmPC neb]
- *elderly*: Adult dose applies, including the elderly. [Label · UK SmPC neb]
- *pregnancy*: SmPC: use only if clearly necessary; avoid in breast-feeding unless benefit outweighs risk. MSF lists no contraindication in pregnancy or breast-feeding. [Label · UK SmPC]
- *monitor*: Serum potassium in acute severe asthma; check for lactic acidosis if tachypnoea persists after wheeze resolves. [Label · UK SmPC]
- *monitor*: Blood glucose in diabetes; review control if reliever is used more than twice a week or a dose gives no relief for 3 h; check inhaler technique. [Label · UK SmPC]

**References added**

- [UK SmPC (Ventolin Evohaler)](https://products.mhra.gov.uk/search/?search=salbutamol#emc-850): Ventolin Evohaler 100 micrograms. Summary of Product Characteristics. electronic medicines compendium (emc).
- [UK SmPC (nebuliser solution)](https://products.mhra.gov.uk/search/?search=salbutamol#emc-10256): Salbutamol 1 mg/ml nebuliser solution (Cipla EU Ltd). Summary of Product Characteristics. electronic medicines compendium (emc).
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-aerosol-16684638.html): Médecins Sans Frontières. Essential drugs – Salbutamol metered dose inhaler; Salbutamol nebuliser solution. MSF Medical Guidelines (updated June 2023).
- [PhilHealth Konsulta](https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf): Philippine Health Insurance Corporation. Certification of Service Delivery Support (Medicines), Annex D2 – Konsulta Package accreditation.
- Dosing source `Label · UK SmPC`: [UK SmPC (Ventolin Evohaler)](https://products.mhra.gov.uk/search/?search=salbutamol#emc-850): Ventolin Evohaler 100 micrograms. Summary of Product Characteristics. emc.
- Dosing source `Label · UK SmPC neb`: [UK SmPC (nebuliser solution)](https://products.mhra.gov.uk/search/?search=salbutamol#emc-10256): Salbutamol 1 mg/ml nebuliser solution (Cipla EU Ltd). Summary of Product Characteristics. emc.
- Dosing source `MSF`: [MSF Essential Drugs (MDI)](https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-aerosol-16684638.html): Médecins Sans Frontières. Essential drugs – Salbutamol metered dose inhaler.
- Dosing source `MSF neb`: [MSF Essential Drugs (nebuliser)](https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-nebuliser-solution-16684649.html): Médecins Sans Frontières. Essential drugs – Salbutamol nebuliser solution.
- Dosing source `PhilHealth`: [PhilHealth Konsulta medicines list](https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf): PhilHealth. Certification of Service Delivery Support (Medicines), Annex D2 – Konsulta Package.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=salbutamol#emc-850: Ventolin Evohaler 100 micrograms SmPC: adults acute 1 inhalation, may increase to 2; prevention 2 inhalations 10–15 min before challenge; chronic 2 inhalations up to 4×/day; children <12 1 inhalation, may increase to 2; max 8 inhalations/24 h; indicated adults, adolescents, children 4–11; contraindicated non-IV for uncomplicated premature labour/threatened abortion; hypokalaemia (monitor K in acute severe asthma), lactic acidosis, thyrotoxicosis, myocardial ischaemia, diabetes caution, use >2×/week or no relief 3 h; pregnancy only if clearly necessary; breast-feeding; AEs angioedema/urticaria/hypotension/collapse, peripheral vasodilatation, mouth/throat irritation, muscle cramps, myocardial ischaemia unknown.
- https://products.mhra.gov.uk/search/?search=salbutamol#emc-10256: Salbutamol 1 mg/ml nebuliser solution (Cipla): adults incl. elderly and ≥12 y 2.5–5 mg up to 4×/day; up to 40 mg/day in hospital; children 4–11 2.5–5 mg up to 4×/day; <18 months efficacy uncertain, transient hypoxia, consider oxygen; angle-closure glaucoma with ipratropium, keep mist from eyes; lactic acidosis with high-dose nebulised therapy; xanthines/steroids/diuretics potentiate hypokalaemia; no renal/hepatic adjustment, cleared partly renally.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-aerosol-16684638.html: MSF MDI 100 micrograms/puff: attack 2–10 puffs every 20 min first hour, then 2–4 puffs every 4–6 h for 24–48 h (or every 1–4 h if not resolved); chronic 2–4 puffs up to 4×/day; spacer for <6 y, older patients, severe dyspnoea; clean mouthpiece; no contraindication pregnancy/breast-feeding; in severe attack nebulised salbutamol + ipratropium preferred.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-nebuliser-solution-16684649.html: MSF nebuliser solution 5 mg/2.5 mL: severe asthma attack with ipratropium; every 20 min first hour: <5 y 2.5 mg, 5–11 y 2.5–5 mg, ≥12 y and adults 5 mg; dilute with 0.9% NaCl to 4 mL, ~10–15 min; never parenteral; MDI + spacer easier, faster, as or more effective, fewer AEs.
- https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf: PhilHealth Konsulta Annex D2 medicines list: salbutamol syrup 2 mg/5 mL 60 mL; DPI 200 micrograms/dose; MDI 100 micrograms/dose × 200; breath-actuated MDI; resp. soln 1 mg/mL and 2 mg/mL 2.5 mL unit dose; ipratropium + salbutamol MDI and nebule. No brand names.

---

## Spironolactone  (`med_spironolactone`)

**Description (kept)**

Spironolactone competitively blocks the mineralocorticoid (aldosterone) receptor in the distal nephron, increasing sodium and water excretion while retaining potassium. It also has anti-androgenic activity. It reduces mortality in heart failure with reduced ejection fraction and is used for resistant hypertension, primary hyperaldosteronism and edema from cirrhosis or nephrotic syndrome.

**Description (added)**

The 2023 Philippine clinical practice guidelines on chronic heart failure with reduced ejection fraction for primary care strongly recommend a mineralocorticoid receptor antagonist on top of standard care when eGFR is above 30 mL/min/1.73 m² and serum potassium is below 5 mEq/L; spironolactone is the only one of these drugs included in the Philippine National Formulary. It is also used in malignant ascites and as a diagnostic test for primary aldosteronism.

**Uses**: 4 kept, 2 added

- NEW: Malignant ascites
- NEW: Diagnosis of primary aldosteronism (400 mg/day test) and pre-operative preparation

**Side effects**: 6 kept, 8 added

- NEW: Confusion, dizziness, muscle spasms and malaise
- NEW: Acute kidney injury; reversible rise in blood urea
- NEW: Pruritus, rash, urticaria
- NEW: Agranulocytosis, leukopenia, thrombocytopenia (frequency not known)
- NEW: Toxic epidermal necrolysis, DRESS, pemphigoid (frequency not known)
- NEW: Hypomagnesemia, hypocalcemia, hyperglycemia and hyperuricemia
- NEW: Hyperchloraemic metabolic acidosis in decompensated cirrhosis
- NEW: Worsening hepatic encephalopathy in cirrhosis with ascites

**Precautions**: 4 kept, 4 added

- NEW: Anuria or acute renal insufficiency
- NEW: Other potassium-sparing diuretics (amiloride, triamterene) or routine potassium supplements
- NEW: Children with moderate to severe renal impairment
- NEW: Hypersensitivity to spironolactone

**Interactions**: 4 kept, 6 added

- NEW: Co-trimoxazole and low molecular weight heparin: clinically relevant hyperkalaemia.
- NEW: Potassium-containing salt substitutes or potassium-rich diet: hyperkalaemia.
- NEW: Digoxin: raised digoxin level and half-life; may interfere with digoxin assays.
- NEW: Other antihypertensives: additive blood pressure lowering; dose may need reducing.
- NEW: Carbenoxolone: sodium retention reduces the effect of spironolactone; avoid.
- NEW: Anaesthesia: reduced vascular response to noradrenaline.

**Disease links added**

- `chronic_kidney_disease`: **caution**: Contraindicated in anuria, acute renal insufficiency or significant renal compromise; higher hyperkalaemia risk in renal impairment. In heart failure with eGFR 30–50, start 25 mg every other day (US label); PH HF guideline recommends MRA only if eGFR >30.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Heart failure (HFrEF) (Start if K ≤5.0 mEq/L and eGFR >50; if hyperkalaemia, 25 mg every other day) | PO | 25 mg | Once a day | Long-term | 50 mg/day | Label · US |
| adult | Heart failure, eGFR 30–50 | PO | 25 mg | Every other day | Long-term | — | Label · US |
| adult | Hypertension (Titrate every 2 weeks; >100 mg/day usually adds no BP lowering) | PO | 25–100 mg | Once a day or divided | Long-term | — | Label · US |
| adult | Edema (heart failure, nephrotic syndrome) (Range 25–200 mg; give ≥5 days before increasing) | PO | 100 mg | Once a day or divided | — | 200 mg/day | Label · US |
| adult | Cirrhosis with ascites (Start in hospital, titrate slowly) | PO | 100 mg (urine Na/K >1); 200–400 mg (Na/K <1) | Once a day or divided | — | 400 mg/day | Label · UK SmPC |
| adult | Malignant ascites | PO | 100–200 mg | Once a day or divided | — | 400 mg/day | Label · UK SmPC |
| adult | Primary aldosteronism (diagnostic test) | PO | 400 mg | Once a day or divided | 3–4 weeks (long) or 4 days (short) | — | Label · UK SmPC |
| adult | Primary aldosteronism (before surgery) (If unfit for surgery: lowest effective dose) | PO | 100–400 mg | Once a day or divided | Until surgery | 400 mg/day | Label · US |
| child | Edema / specialist use (Only under a paediatric specialist) | PO | 1–3 mg/kg/day ÷ doses | Divided doses | — | — | Label · UK SmPC |

- *renal*: Contraindicated in anuria, acute renal insufficiency or significant renal compromise. [Label · UK SmPC]
- *renal* eGFR 30–50: Consider starting at 25 mg every other day in heart failure. [Label · US]
- *renal* eGFR >30: Philippine HF guideline recommends an MRA only when eGFR is above 30 mL/min/1.73 m² and potassium is below 5 mEq/L. [PH CPG 2023]
- *hepatic*: Cirrhosis: start in hospital at the lowest dose and titrate slowly; rapid fluid and electrolyte shifts can precipitate hepatic encephalopathy or coma. [Label · US]
- *elderly*: Start at the lowest dose and titrate; monitor renal function and electrolytes, as reduced renal function is more common. [Label · UK SmPC]
- *pregnancy*: Feminisation of male fetuses in animal studies; avoid in pregnancy or advise of the risk to a male fetus. Canrenone appears in milk in small amounts; UK labeling advises alternative infant feeding if use is essential. [Label · US]
- *administration*: Take consistently with respect to food (UK labeling suggests once daily with a meal). [Label · US]
- *monitor*: Heart failure: check potassium and creatinine at 1 week after starting or increasing the dose, monthly for 3 months, every 3 months for a year, then every 6 months. Stop or interrupt if K >5 mEq/L or creatinine >4 mg/dL. [Label · UK SmPC]
- *monitor*: Check sodium, magnesium, calcium, uric acid, glucose, volume status and blood pressure; ask men about breast swelling or pain. [Label · US]

**References added**

- [Philippine Journal of Cardiology](https://pjc.philheart.org/elib/journal/identifier/pjc.2025.0712.012034/full): Abola MTB, Punzalan FER, Magno JDA, et al. 2023 Philippine Clinical Practice Guidelines on the Diagnosis and Management of Chronic Heart Failure with Reduced Ejection Fraction for Primary Care Physicians. Philipp J Cardiol. 2025;53(2).
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=spironolactone#emc-12015): Spironolactone 12.5 mg film-coated tablets. Summary of Product Characteristics. Mercury Pharmaceuticals Ltd; revised 14 October 2025. electronic medicines compendium (emc).
- Dosing source `Label · US`: [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0fed2822-3a03-4b64-9857-c682fcd462bc): ALDACTONE (spironolactone) tablets. Prescribing information. Pfizer; revised 11/2025. DailyMed, U.S. National Library of Medicine.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=spironolactone#emc-12015): Spironolactone 12.5 mg film-coated tablets. Summary of Product Characteristics. Mercury Pharmaceuticals Ltd; revised 14 October 2025.
- Dosing source `PH CPG 2023`: [Philippine Journal of Cardiology](https://pjc.philheart.org/elib/journal/identifier/pjc.2025.0712.012034/full): Abola MTB, et al. 2023 Philippine CPG on chronic HFrEF for primary care physicians. Philipp J Cardiol. 2025;53(2).

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=spironolactone#emc-12015: Mercury spironolactone 12.5 mg SmPC (rev 14/10/2025): 4.1 CHF, cirrhosis, malignant ascites, nephrotic, primary aldosteronism; 4.2 doses incl. Na/K ratio, malignant ascites 100–200 up to 400, aldosteronism tests 400 mg 3–4 wk/4 days, children 1–3 mg/kg/day divided, elderly lowest dose, with meal; 4.3 anuria, acute renal insufficiency, other K-sparing diuretics, children mod–severe renal impairment; 4.4 K/creatinine monitoring schedule, stop K>5/creat>4, hyperchloraemic acidosis in cirrhosis; 4.5 co-trimoxazole, LMWH, salt substitutes, digoxin, carbenoxolone, noradrenaline, antihypertensives; 4.6 alternative feeding; 4.8 confusion, dizziness, muscle spasms, AKI, pruritus, agranulocytosis, TEN, DRESS, pemphigoid.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0fed2822-3a03-4b64-9857-c682fcd462bc: Aldactone label rev 11/2025: HF 25 mg daily if K ≤5.0 and eGFR >50, up to 50 mg, eGFR 30–50 25 mg every other day; HTN 25–100 mg, 2-week titration, >100 no added effect; edema 100 mg (25–200), ≥5 days, cirrhosis in hospital; aldosteronism 100–400 mg pre-surgery; food consistency; 5.3 hypomagnesemia, hypocalcemia, hyperglycemia, hyperuricemia; 8.1 male fetus risk; 8.2 canrenone low; 8.5–8.7 renal/hepatic encephalopathy; forms 25/50/100 mg (US, not PH).
- https://pjc.philheart.org/elib/journal/identifier/pjc.2025.0712.012034/full: 2023 Philippine CPG chronic HFrEF for primary care (PJC 2025;53(2)): Recommendation 11, MRA (spironolactone or eplerenone) recommended on top of standard care if eGFR >30 and K <5 mEq/L (strong, low certainty); 'only spironolactone is included in the PNF'. No dose or forms given.

---

## Sumatriptan  (`med_sumatriptan`)

**Description (kept)**

Sumatriptan is a selective serotonin 5-HT1B/1D receptor agonist that constricts dilated cranial blood vessels and inhibits release of vasoactive neuropeptides and pain transmission in the trigeminal system. It is an abortive (acute) treatment and does not prevent migraine attacks. It is used for acute migraine with or without aura and, subcutaneously, for cluster headache.

**Description (added)**

Sumatriptan is also given as a nasal spray, which UK labeling allows for adolescents aged 12–17 under specialist advice. In a 2022 survey of Filipino neurologists, NSAIDs were the most preferred acute migraine drugs and about half would not consider a triptan even for moderate to severe episodic attacks, so triptans remain little used in the Philippines.

**Uses**: 2 kept, 1 added

- NEW: Acute migraine in adolescents 12–17 years (nasal spray, specialist recommendation; UK labeling)

**Side effects**: 8 kept, 7 added

- NEW: Flushing, dyspnoea, nausea and vomiting
- NEW: Transient rise in blood pressure; hypotension, bradycardia or tachycardia
- NEW: Visual disturbance (flickering, diplopia, scotoma, reduced vision)
- NEW: Tremor, dystonia, nystagmus
- NEW: Raynaud's phenomenon and ischaemic colitis
- NEW: Hypersensitivity reactions up to anaphylaxis
- NEW: Medication overuse headache with frequent use

**Precautions**: 9 kept, 3 added

- NEW: Moderate or severe hypertension (and mild uncontrolled hypertension)
- NEW: Previous myocardial infarction
- NEW: Intravenous administration (vasospasm risk)

**Interactions**: 3 kept, 4 added

- NEW: Lithium: possible serotonin syndrome.
- NEW: St John's wort: adverse effects may be more frequent.
- NEW: After sumatriptan wait at least 6 hours before ergotamine and 24 hours before another triptan.
- NEW: No interaction with propranolol, flunarizine, pizotifen or alcohol.

**Disease links added**

- `hypertension`: **avoid**: Contraindicated in moderate or severe hypertension and in mild uncontrolled hypertension; use with caution in mild controlled hypertension (UK SmPC).
- `chronic_kidney_disease`: **caution**: UK SmPC advises caution in impaired renal function; no specific dose adjustment given.

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Acute migraine (No second dose if the first fails; use paracetamol, aspirin or an NSAID) | PO | 50 mg (some need 100 mg) | Single dose; repeat once if it recurs, ≥2 h apart | Per attack | 300 mg/24 h | Label · UK SmPC |
| adult | Acute migraine (Never IV) | SC | 6 mg | Single dose; repeat once if it recurs, ≥1 h apart | Per attack | 12 mg/24 h | Label · UK SmPC inj |
| adult | Cluster headache attack | SC | 6 mg | Per attack, ≥1 h apart | Per attack | 12 mg/24 h | Label · UK SmPC inj |
| adult | Acute migraine (Into one nostril) | Nasal | 20 mg (some respond to 10 mg) | Single dose; repeat once if it recurs, ≥2 h apart | Per attack | 40 mg/24 h | Label · UK SmPC nasal |
| child | Acute migraine, 12–17 years (Specialist recommendation only; not under 12; tablets and injection not recommended under 18) | Nasal | 10 mg | Single dose; repeat once if it recurs, ≥2 h apart | Per attack | 20 mg/24 h | Label · UK SmPC nasal |

- *renal*: No dose adjustment stated; use with caution in renal impairment. [Label · UK SmPC]
- *hepatic*: Mild to moderate impairment: consider low doses of 25–50 mg orally. Contraindicated in severe impairment. [Label · UK SmPC]
- *elderly*: Not recommended over 65 years because of limited experience. [Label · UK SmPC]
- *pregnancy*: Over 1,000 first-trimester exposures without a clear rise in birth defects, but data are insufficient; use only if benefit outweighs risk. Relative infant dose in milk is below 4%; avoid breastfeeding and discard milk for 12 hours after a dose. [Label · UK SmPC]
- *administration*: Use only when the diagnosis of migraine is clear; take at the first sign of the attack. Swallow tablets whole with water. The injection needle shield may contain latex. [Label · UK SmPC inj]
- *monitor*: Assess cardiovascular risk before first use (smokers, nicotine replacement users, men over 40, postmenopausal women with risk factors). Stop if chest symptoms suggest ischaemia. Ask about headache days per month to detect medication overuse headache. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=sumatriptan#emc-524): Sumatriptan 50 mg tablets. Summary of Product Characteristics. Milpharm Ltd; revised 9 June 2026. electronic medicines compendium (emc).
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=sumatriptan#emc-944): Imigran Injection / Imigran Subject (sumatriptan 6 mg). Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025. emc.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=sumatriptan#emc-2214): Imigran 10 mg Nasal Spray. Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025. emc.
- [Neurology Asia](https://neurology-asia.org/system/index.php/neuro/article/view/675): Roxas AA Jr, Quiles LE, Diamante PA. The practice patterns of migraine management among neurologists in the Philippines: a cross-sectional survey. Neurology Asia. 2022;27(3):717-724.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=sumatriptan#emc-524): Sumatriptan 50 mg tablets. Summary of Product Characteristics. Milpharm Ltd; revised 9 June 2026.
- Dosing source `Label · UK SmPC inj`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=sumatriptan#emc-944): Imigran Injection (sumatriptan 6 mg). Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025.
- Dosing source `Label · UK SmPC nasal`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=sumatriptan#emc-2214): Imigran 10 mg Nasal Spray. Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=sumatriptan#emc-524: Milpharm sumatriptan 50 mg SmPC (rev 09/06/2026): 50 mg, some 100 mg; no second dose for non-response; recurrence repeat ≥2 h; max 300 mg/24 h; not recommended 10–17 y or >65; hepatic 25–50 mg, severe contraindicated; renal caution (4.4); swallow whole with water; 4.3 MI, moderate/severe and mild uncontrolled hypertension; 4.4 MOH, CV evaluation risk groups, seizures, sulphonamide; 4.5 lithium, St John's wort, 6 h/24 h rules, no interaction propranolol/flunarizine/pizotifen/alcohol; 4.6 >1000 exposures, RID <4%, avoid breastfeeding 12 h; 4.8 flushing, dyspnoea, nausea, BP rise, visual effects, tremor, dystonia, nystagmus, Raynaud's, ischaemic colitis, anaphylaxis.
- https://products.mhra.gov.uk/search/?search=sumatriptan#emc-944: Imigran Injection SmPC (rev 15/10/2025): migraine 6 mg SC, repeat ≥1 h if recurrence, max 12 mg/24 h; cluster headache 6 mg per attack same limits; not <18 or >65; not IV (vasospasm); latex needle shield; injection-site pain very common.
- https://products.mhra.gov.uk/search/?search=sumatriptan#emc-2214: Imigran 10 mg Nasal Spray SmPC (rev 15/10/2025): adults 20 mg (some 10 mg) one nostril, repeat ≥2 h, max two 20 mg doses/24 h; adolescents 12–17 10 mg specialist only, max two 10 mg doses/24 h; not <12 or >65.
- https://neurology-asia.org/system/index.php/neuro/article/view/675: Roxas et al., Neurology Asia 2022;27(3):717-724: NSAIDs most preferred acute migraine class (48.26%); about half would not consider triptans for moderate–severe episodic attacks; no PH forms/availability data.

---

## Tenofovir Disoproxil Fumarate  (`med_tenofovir`)

**Description (kept)**

Tenofovir disoproxil fumarate is an oral prodrug of tenofovir, an acyclic nucleotide (adenosine monophosphate) analogue. After intracellular phosphorylation to tenofovir diphosphate it competes with natural nucleotides and terminates DNA chain elongation, inhibiting HIV-1 reverse transcriptase and the hepatitis B virus polymerase. It is used with other antiretrovirals for HIV-1 treatment, as HIV pre-exposure prophylaxis with emtricitabine, and as a first-line agent for chronic hepatitis B because of its high barrier to resistance.

**Description (added)**

In the Philippines, tenofovir disoproxil combined with emtricitabine is the drug used for oral HIV pre-exposure prophylaxis under the DOH interim PrEP guidelines (2021), taken daily by anyone at substantial risk or event-driven (2-1-1) by men who have sex with men. WHO recommends tenofovir prophylaxis from the 28th week of pregnancy for HBsAg-positive women with HBV DNA of 200,000 IU/mL or more to prevent mother-to-child transmission of hepatitis B.

**Uses**: 5 kept, 2 added

- NEW: Chronic hepatitis B with decompensated liver disease or lamivudine-resistant HBV in adults (UK SmPC)
- NEW: Event-driven (2-1-1) oral PrEP with emtricitabine for men who have sex with men (DOH interim PrEP guidelines, 2021)

**Side effects**: 6 kept, 2 added

- NEW: Dizziness
- NEW: Mild serum creatinine rises in PrEP users (mostly grade 1; renal events more frequent than with placebo)

**Precautions**: 5 kept, 3 added

- NEW: Hypersensitivity to tenofovir disoproxil or any excipient (UK SmPC)
- NEW: PrEP is not started in people who are HIV-positive, have signs of acute retroviral syndrome, weigh under 35 kg or have CrCl of 60 mL/min or less (DOH)
- NEW: Use in children with renal impairment is not recommended (UK SmPC)

**Interactions**: 5 kept, 4 added

- NEW: Other tenofovir disoproxil or tenofovir alafenamide products and adefovir dipivoxil: not co-administered.
- NEW: Tacrolimus: monitor renal function during co-administration.
- NEW: Amphotericin B and pentamidine: nephrotoxic; avoid or monitor renal function (MSF).
- NEW: Clarithromycin: may raise tenofovir levels; use with caution and close monitoring (MSF).

**Disease links added**

- `chronic_kidney_disease`: **caution**: Dosing interval is lengthened when CrCl is below 50 mL/min and renal function is monitored; MSF prefers entecavir for hepatitis B in renal impairment (UK SmPC, MSF).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | HIV-1 infection (with other ARVs) (Same dose for chronic hepatitis B) | PO | 300 mg | Once a day | Long-term | 300 mg/day | Label · US FDA |
| adult | Chronic hepatitis B (HBeAg+: at least 12 months after HBe seroconversion (UK SmPC)) | PO | 300 mg | Once a day | Usually long-term | 300 mg/day | MSF |
| adult | HBV mother-to-child prevention (pregnancy) (If HBV DNA ≥200,000 IU/mL (or HBeAg+)) | PO | 300 mg | Once a day | From week 28 until at least birth | — | WHO |
| adult | HIV PrEP, daily (with emtricitabine) (Protection after 5–7 days (anal) or 20 days (vaginal)) | PO | 1 TDF/FTC tablet | Once a day | While at risk; 28 days after last exposure | 2 tablets/day | DOH PrEP 2021 |
| adult | HIV PrEP, event-driven (MSM only) (TDF/FTC tablets) | PO | 2 tablets, then 1, then 1 | 2–24 h before sex, then 24 h and 48 h after first dose | Until 2 days after last sex | 2 tablets/day | DOH PrEP 2021 |
| child | HIV-1 or chronic hepatitis B (≥2 years, ≥10 kg) (Tablets ≥17 kg: 150 mg (17–<22 kg), 200 mg (22–<28 kg), 250 mg (28–<35 kg)) | PO | 8 mg/kg | Once a day | Long-term | 300 mg/day | Label · US FDA |
| child | HIV-1 or chronic hepatitis B (12 years and older, ≥35 kg) | PO | 300 mg | Once a day | Long-term | 300 mg/day | MSF |

- *renal* CrCl 50–80: Once-daily dosing supported by limited data. [Label · UK SmPC]
- *renal* CrCl 30–49: 300 mg every 48 hours. [MSF]
- *renal* CrCl 10–29: 300 mg every 72–96 hours; below CrCl 10 seek specialist advice. MSF prefers entecavir for hepatitis B in renal impairment. [MSF]
- *renal* Haemodialysis: Every 7 days, after a dialysis session. [Label · UK SmPC]
- *hepatic*: No dose adjustment. [Label · UK SmPC]
- *elderly*: No data in people over 65; use with caution because renal function is often reduced. [Label · UK SmPC]
- *pregnancy*: More than 1,000 pregnancy outcomes show no malformations or fetal/neonatal toxicity. Women with HBV may breastfeed; women living with HIV follow national breastfeeding advice. [Label · UK SmPC]
- *administration*: Missed dose: take within 12 hours, otherwise skip. Vomiting within 1 hour: take another dose. The UK label advises taking it with food; the oral powder is always given with food. [Label · UK SmPC]
- *monitor*: Creatinine clearance and serum phosphate before starting, after 2–4 weeks, after 3 months, then every 3–6 months if there are no renal risk factors. [Label · UK SmPC]
- *monitor*: PrEP: HIV test within 7 days before starting, after 1 month, then at least every 3 months; HBsAg at baseline; serum creatinine every 6 months; stop PrEP if CrCl falls below 60 mL/min. [DOH PrEP 2021]

**References added**

- [DOH interim PrEP guidelines](https://hivpreventioncoalition.unaids.org/sites/default/files/attachments/interim_guidelines_on_pre-exposure_prophylaxis_prep.pdf): Department of Health, Philippines. Department Memorandum: Interim Guidelines on Pre-Exposure Prophylaxis (PrEP) for the Prevention of HIV Infection in the Philippines. 4 January 2021.
- [DOST HTA Philippines](https://hta.dost.gov.ph/wp-content/uploads/2024/02/ES_Oral-PrEP-for-HIV_as-of-Nov-2021.docx-1.pdf): Health Technology Assessment Council (DOST-PCHRD / DOH). Evidence summary: Emtricitabine/tenofovir disoproxil fumarate oral PrEP for HIV. Approved by the Secretary of Health 18 January 2022.
- [World Health Organization](https://www.who.int/news-room/questions-and-answers/item/hepatitis-preventing-mother-to-child-transmission-of-the-hepatitis-b-virus): World Health Organization. Hepatitis: Preventing mother-to-child transmission of the hepatitis B virus. Questions and answers.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/tenofovir-disoproxil-fumarate-tdf-oral-38537560.html): Médecins Sans Frontières. Essential drugs - practical guidelines: Tenofovir disoproxil fumarate = TDF oral. Updated April 2026.
- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=tenofovir#emc-1615): Viread 245 mg film-coated tablets - Summary of Product Characteristics. Gilead Sciences Ltd. Electronic medicines compendium (emc), updated 15 March 2024.
- Dosing source `DOH PrEP 2021`: [DOH interim PrEP guidelines](https://hivpreventioncoalition.unaids.org/sites/default/files/attachments/interim_guidelines_on_pre-exposure_prophylaxis_prep.pdf): DOH Philippines. Interim Guidelines on Pre-Exposure Prophylaxis (PrEP) for the Prevention of HIV Infection in the Philippines, 4 January 2021.
- Dosing source `WHO`: [World Health Organization](https://www.who.int/news-room/questions-and-answers/item/hepatitis-preventing-mother-to-child-transmission-of-the-hepatitis-b-virus): WHO. Hepatitis: Preventing mother-to-child transmission of the hepatitis B virus (Q&A).
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/tenofovir-disoproxil-fumarate-tdf-oral-38537560.html): MSF Essential drugs: Tenofovir disoproxil fumarate = TDF oral, 2026.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=tenofovir#emc-1615): Viread 245 mg film-coated tablets SmPC, Gilead Sciences Ltd, updated 15 March 2024.
- Dosing source `Label · US FDA`: [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=33fd6418-fbdc-42ca-a50d-ce2a476a5418): VIREAD (tenofovir disoproxil fumarate) tablets and oral powder, Gilead Sciences. DailyMed.

**What was checked on each page**

- https://hivpreventioncoalition.unaids.org/sites/default/files/attachments/interim_guidelines_on_pre-exposure_prophylaxis_prep.pdf: DOH Department Memorandum dated 4 Jan 2021 (number illegible): daily TDF/FTC once daily, max 2 tablets/day; event-driven for MSM (2 pills 2–24 h before sex, 1 at 24 h, 1 at 48 h); lead-in 5–7 days anal / 20 days vaginal; eligibility HIV-negative, no acute retroviral syndrome, ≥35 kg, CrCl >60; HIV test within 7 days, HBsAg, creatinine; follow-up HIV test at 1 month then every 3 months, creatinine every 6 months, stop if CrCl <60; stop 28 days after last exposure (non-MSM).
- https://hta.dost.gov.ph/wp-content/uploads/2024/02/ES_Oral-PrEP-for-HIV_as-of-Nov-2021.docx-1.pdf: DOST HTA evidence summary for TDF/FTC oral PrEP, approved by SOH 18 Jan 2022; renal adverse events more frequent than placebo (RR 1.54), mostly grade-1 creatinine elevations.
- https://www.who.int/news-room/questions-and-answers/item/hepatitis-preventing-mother-to-child-transmission-of-the-hepatitis-b-virus: Tenofovir prophylaxis for HBsAg-positive pregnant women with HBV DNA ≥5.3 log10 IU/mL (≥200,000 IU/mL); HBeAg as alternative where DNA testing unavailable; from week 28 until at least birth; TDF safe.
- https://www.who.int/news-room/fact-sheets/detail/hepatitis-B: WHO hepatitis B fact sheet (28 July 2026): tenofovir in first-line HIV combinations and active against HBV; most need lifelong treatment. Used for verification only.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/tenofovir-disoproxil-fumarate-tdf-oral-38537560.html: MSF TDF page (updated Apr 2026): 300 mg once daily ≥12 years and adults; renal 300 mg every 48 h (CrCl 30–49), every 72–96 h (10–29), specialist advice <10; entecavir preferred in renal impairment; dizziness among adverse effects; avoid/monitor with aminoglycosides, amphotericin B, pentamidine, NSAIDs; caution with clarithromycin; PMTCT from second trimester until infant vaccination complete.
- https://products.mhra.gov.uk/search/?search=tenofovir#emc-1615: Viread SmPC (15 Mar 2024): indications incl. decompensated and lamivudine-resistant HBV; with food; missed dose 12 h rule; vomiting within 1 h; renal bands incl. CrCl 50–80 and HD every 7 days; no hepatic adjustment; elderly caution; not recommended in paediatric renal impairment; HBV duration; contraindication hypersensitivity; do not combine with other TDF/TAF/adefovir; tacrolimus monitoring; pregnancy >1,000 outcomes; breastfeeding; renal monitoring at 2–4 weeks, 3 months, then every 3–6 months.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=33fd6418-fbdc-42ca-a50d-ce2a476a5418: US label: 8 mg/kg once daily up to 300 mg for ≥2 years; tablets 150/200/250/300 mg by weight bands 17–<22, 22–<28, 28–<35, ≥35 kg; oral powder from 10 kg; same dose for HIV and HBV.

---

## Tenofovir + Lamivudine + Dolutegravir (TLD)  (`med_tld`)

**Description (kept)**

TLD is a once-daily fixed-dose tablet combining two nucleos(t)ide reverse transcriptase inhibitors (tenofovir disoproxil fumarate and lamivudine), which terminate viral DNA chain synthesis, with dolutegravir, an integrase strand transfer inhibitor that blocks integration of HIV DNA into the host genome. WHO recommends dolutegravir-based therapy as the preferred first- and second-line HIV treatment in all populations, and tenofovir plus lamivudine also suppress hepatitis B virus. There is no US boxed warning for this WHO-prequalified combination itself, but the US label of its tenofovir disoproxil component carries a boxed warning for severe acute exacerbation of hepatitis B after discontinuation, which applies to people with HBV co-infection. In the Philippines it is the DOH's recommended first-line antiretroviral regimen, procured nationally for people living with HIV (Philippine News Agency, July 2026).

**Description (added)**

The Philippine HTA Council recommended TLD for both treatment-naive and treatment-experienced adolescents and adults with HIV, a decision approved by the Secretary of Health on 1 September 2021, noting a monthly bottle cost (PHP 549) equal to the older tenofovir/lamivudine/efavirenz tablet. WHO's January 2026 HIV clinical management update confirms dolutegravir-based regimens as the preferred option for initial and subsequent treatment and supports reusing tenofovir in later regimens.

**Side effects**: 7 kept, 6 added

- NEW: Insomnia, abnormal dreams, anxiety and depression (common; neuropsychiatric effects were the most reported in a Zambian pharmacovigilance study)
- NEW: Dizziness, vomiting, asthenia and rash (very common)
- NEW: Raised ALT/AST and creatine phosphokinase
- NEW: Arthralgia, fatigue, fever, hair loss and pruritus
- NEW: Pancreatitis (rare); stop if suspected
- NEW: Small increased risk of neural tube defects with exposure around conception (0.19% vs 0.11% in Botswana surveillance)

**Precautions**: 5 kept, 2 added

- NEW: HIV-1 with integrase inhibitor resistance (fixed-dose tablet is for INSTI-susceptible HIV-1)
- NEW: Children weighing under 30 kg (separate formulations needed)

**Interactions**: 7 kept, 7 added

- NEW: Etravirine (without a boosted protease inhibitor): lowers dolutegravir exposure by about 71%; dolutegravir is given 50 mg twice daily.
- NEW: Efavirenz, nevirapine, oxcarbazepine and phenobarbital: expected to lower dolutegravir levels; the dolutegravir dose is doubled with enzyme inducers.
- NEW: Rifampicin and other enzyme inducers: continue the double dolutegravir dose for 2 weeks after the inducer is stopped (MSF).
- NEW: Sorbitol, mannitol and other polyols: reduce lamivudine exposure; avoid chronic co-use or monitor viral load.
- NEW: Cladribine: not recommended with lamivudine.
- NEW: Emtricitabine, adefovir dipivoxil, tenofovir alafenamide and didanosine: not co-administered.
- NEW: Metformin: MSF advises not exceeding 1 g/day with dolutegravir and monitoring blood glucose and renal function.

**Disease links added**

- `hepatitis_b`: **safe**: Tenofovir (in first-line HIV combinations) is active against HBV (WHO); in coinfection do not stop TLD without HBV cover because of flare risk (WHOPAR).
- `tuberculosis`: **caution**: Rifampicin lowers dolutegravir levels; an extra dolutegravir 50 mg tablet is added to TLD during TB treatment (DOST HTA, WHOPAR).
- `chronic_kidney_disease`: **avoid**: Fixed-dose tablet not recommended when CrCl is below 50 mL/min; use separate components with dose adjustment (WHOPAR).
- `type2_diabetes`: **caution**: Dolutegravir raises metformin levels; monitor glucose and renal function and limit metformin to 1 g/day (MSF).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | HIV-1 infection (first- or second-line) (With or without food) | PO | 1 tablet (TDF 300 mg / 3TC 300 mg / DTG 50 mg) | Once a day | Lifelong | 1 tablet/day | DOST HTA 2021 |
| adult | HIV-1 with rifampicin or other enzyme inducer (Also with efavirenz, carbamazepine (WHOPAR)) | PO | 1 tablet + dolutegravir 50 mg | TLD once a day; extra DTG about 12 h later | During inducer and 2 weeks after | — | MSF |
| child | HIV-1 infection (adolescents ≥30 kg) (Not for children under 30 kg) | PO | 1 tablet | Once a day | Lifelong | 1 tablet/day | WHOPAR |

- *renal* CrCl 50–80: No dose adjustment. [WHOPAR]
- *renal* CrCl < 50: Fixed-dose tablet not recommended; give the components separately with dose adjustment. [WHOPAR]
- *hepatic*: No adjustment in Child-Pugh A or B; use with caution in Child-Pugh C (no dolutegravir data). [WHOPAR]
- *elderly*: Use with caution. [WHOPAR]
- *pregnancy*: Counsel women of childbearing potential on neural tube defect risk and contraception; pregnancy test before starting if feasible. Folic acid in the first trimester may reduce the risk (MSF). All three components pass into breast milk. [WHOPAR]
- *administration*: Missed dose: take if less than 12 hours late, otherwise skip; never double. Vomiting within 1 hour: take another dose. [WHOPAR]
- *monitor*: Creatinine clearance before and during therapy; interrupt if confirmed CrCl < 50 mL/min or serum phosphate < 1.0 mg/dL. Test for HBV before starting. [WHOPAR]
- *monitor*: Liver enzymes and bilirubin if hypersensitivity is suspected; weight, lipids and glucose; in HBV coinfection, liver tests for at least 6 months after stopping. [WHOPAR]
- *forms_ph*: Fixed-dose tablet TDF 300 mg + 3TC 300 mg + DTG 50 mg, holding a monitored-release FDA certificate of product registration; not yet in the PNF at the time of the 2021 HTA review (components listed singly). [DOST HTA 2021]

**References added**

- [DOST HTA Philippines](https://hta.dost.gov.ph/wp-content/uploads/2021/09/ES_TLD_for_HIV_approved_by_SOH.docx.pdf): Health Technology Assessment Council (DOST / DOH). Evidence summary: Tenofovir/lamivudine/dolutegravir (TLD) for treatment-naive and treatment-experienced adolescents and adults living with HIV. Approved by the Secretary of Health 1 September 2021.
- [World Health Organization](https://www.who.int/news/item/07-01-2026-who-releases-updated-recommendations-on-hiv-clinical-management): World Health Organization. WHO releases updated recommendations on HIV clinical management. News release, 7 January 2026.
- [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/dolutegravir-dtg-oral-38537537.html): Médecins Sans Frontières. Essential drugs - practical guidelines: Dolutegravir = DTG oral. Updated October 2024.
- [World Health Organization](https://www.who.int/news-room/fact-sheets/detail/hepatitis-B): World Health Organization. Hepatitis B. Fact sheet, updated 28 July 2026.
- Dosing source `WHOPAR`: [WHO Prequalification (WHOPAR product information)](https://extranet.who.int/prequal/sites/default/files/whopar_files/HA729part4v2.pdf): WHO Prequalification. Dolutegravir/Lamivudine/Tenofovir disoproxil fumarate 50/300/300 mg tablets (HA729), SmPC, WHOPAR part 4, Oct 2022.
- Dosing source `DOST HTA 2021`: [DOST HTA Philippines](https://hta.dost.gov.ph/wp-content/uploads/2021/09/ES_TLD_for_HIV_approved_by_SOH.docx.pdf): HTA Council evidence summary: TLD for adolescents and adults living with HIV, approved by SOH 1 Sep 2021.
- Dosing source `MSF`: [MSF Essential Drugs](https://medicalguidelines.msf.org/en/viewport/EssDr/english/dolutegravir-dtg-oral-38537537.html): MSF Essential drugs: Dolutegravir = DTG oral, Oct 2024.

**What was checked on each page**

- https://hta.dost.gov.ph/wp-content/uploads/2021/09/ES_TLD_for_HIV_approved_by_SOH.docx.pdf: HTAC recommends TLD first-line (treatment-naive adolescents/adults) and second-line (treatment-experienced adults); SOH decision 1 Sep 2021; MR-CPR for the FDC tablet TDF 300/3TC 300/DTG 50; 'Currently, TLD is not listed in the PNF'; components listed singly; AO 2018-0024; one tablet daily lifelong; extra DTG 50 mg with rifampicin; PHP 549 per monthly bottle (same as TLEfv); neuropsychiatric ADEs most common in Zambian study.
- https://www.who.int/news/item/07-01-2026-who-releases-updated-recommendations-on-hiv-clinical-management: WHO news 7 Jan 2026: confirms dolutegravir-based regimens as preferred for initial and subsequent HIV treatment; supports reuse of tenofovir and abacavir in subsequent regimens.
- https://extranet.who.int/prequal/sites/default/files/whopar_files/HA729part4v2.pdf: WHOPAR HA729 part 4 (Oct 2022): ≥30 kg one tablet daily, INSTI-susceptible HIV-1; missed dose 12 h; vomiting 1 h; not for <30 kg; elderly caution; CrCl 50–80 no adjustment, <50 not recommended; Child-Pugh A/B no adjustment, C caution; inducers need DTG 50 mg twice daily via separate DTG; renal interruption CrCl <50 or phosphate <1.0 mg/dL; HBV testing; flare monitoring ≥6 months; weight/metabolic; pancreatitis; etravirine AUC -71%; nevirapine/oxcarbazepine/phenobarbital; sorbitol; cladribine; emtricitabine/adefovir/TAF/didanosine; NTD 0.19% vs 0.11%; breast milk; very common/common ADRs listed.
- https://medicalguidelines.msf.org/en/viewport/EssDr/english/dolutegravir-dtg-oral-38537537.html: MSF DTG page (Oct 2024): TLD preferred for adolescents/adults ≥30 kg; adverse effects insomnia, depression, anxiety, dizziness; metformin: monitor glucose and renal function, not exceed 1 g/day; enzyme inducers (rifampicin, carbamazepine, phenytoin, phenobarbital, efavirenz, nevirapine): double the DTG dose and continue 2 weeks after stopping the inducer; folic acid in first trimester may reduce NTD risk.
- https://www.who.int/news-room/fact-sheets/detail/hepatitis-B: Tenofovir is included in first-line HIV combinations and is active against HBV.

---

## Vancomycin  (`med_vancomycin`)

**Description (kept)**

Vancomycin binds the D-alanyl-D-alanine ends of cell-wall precursors and blocks peptidoglycan synthesis in gram-positive bacteria. Given intravenously it treats serious infections due to MRSA and resistant pneumococci, and in suspected bacterial meningitis it is added to a third-generation cephalosporin until susceptibilities are known. Oral vancomycin is not absorbed and is used only for Clostridioides difficile colitis.

**Description (added)**

UK labeling also licenses IV vancomycin for complicated skin and soft tissue infections, bone and joint infections, community- and hospital-acquired pneumonia, infective endocarditis and surgical prophylaxis in patients at high risk of endocarditis. The first IV dose is based on total body weight (a 25–30 mg/kg loading dose may be used in seriously ill patients), and later doses are guided by serum levels and kidney function. IV vancomycin is not effective for C. difficile infection, and it must never be given intramuscularly.

**Uses**: 3 kept, 3 added

- NEW: Complicated skin and soft tissue infections and bone and joint infections (IV)
- NEW: Community-acquired and hospital-acquired pneumonia, including ventilator-associated pneumonia (IV)
- NEW: Perioperative prophylaxis in patients at high risk of bacterial endocarditis undergoing major surgery (IV)

**Side effects**: 5 kept, 7 added

- NEW: Severe skin reactions: SJS, TEN, DRESS, AGEP, linear IgA bullous dermatosis (stop at first signs; never restart)
- NEW: Hypotension, shock and rarely cardiac arrest with rapid bolus infusion
- NEW: Raised ALT and AST (common)
- NEW: Interstitial nephritis and acute renal failure (rare)
- NEW: Drug fever, shivering, pain and muscle spasm of chest and back (rare)
- NEW: Kounis syndrome (allergic acute coronary syndrome)
- NEW: Haemorrhagic occlusive retinal vasculitis after intracameral or intravitreal use (not an approved route)

**Precautions**: 1 kept, 2 added

- NEW: Intramuscular injection (risk of necrosis at the injection site)
- NEW: Previous severe skin reaction (SJS, TEN, DRESS, AGEP) to vancomycin: must not be restarted

**Interactions**: 3 kept, 3 added

- NEW: Anaesthetic agents: more erythema, histamine-like flushing and anaphylactoid reactions; infuse vancomycin over 60 minutes before induction.
- NEW: Bacitracin, polymyxin B, colistin and viomycin: additive kidney or ear toxicity; monitor closely.
- NEW: Oral use for C. difficile: stop anti-motility agents and reconsider proton pump inhibitors.

**Disease links added**

- `community_acquired_pneumonia`: **safe**: Licensed IV indication, including MRSA; typical course 7–14 days (UK SmPC).
- `chronic_kidney_disease`: **caution**: Nephrotoxic and renally cleared: give the usual loading dose, then extend the interval and dose by serum levels (UK SmPC).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Serious infections (incl. ≥12 y) (Initial dose by total body weight; adjust by levels) | IV | 15–20 mg/kg | Every 8–12 h | By infection | 2 g per dose | Label · UK SmPC |
| adult | Loading dose, seriously ill (Do not reduce in renal insufficiency) | IV | 25–30 mg/kg | Once | — | — | Label · UK SmPC |
| adult | Serious infections (fixed dose) (Normal renal function) | IV | 500 mg or 1 g | Every 6 h or every 12 h | By infection | 2 g/day | Label · US |
| adult | Surgical prophylaxis, high endocarditis risk (Second dose may be needed for long surgery) | IV | 15 mg/kg | Once, before induction | — | — | Label · UK SmPC |
| adult | C. difficile, first non-severe episode | PO | 125 mg | Every 6 h | 10 days | 2 g/day | Label · UK SmPC |
| adult | C. difficile, severe or complicated | PO | 500 mg | Every 6 h | 10 days | 2 g/day | Label · UK SmPC |
| adult | C. difficile, multiple recurrences (Taper to 125 mg/day or 125–500 mg every 2–3 days) | PO | 125 mg, then taper or pulse | 4× a day | 10 days, then ≥3 weeks | — | Label · UK SmPC |
| child | Serious infections, 1 month–<12 y (Standard doses may give low levels; monitor) | IV | 10–15 mg/kg | Every 6 h | By infection | 60 mg/kg/day usually | Label · UK SmPC |
| child | Surgical prophylaxis, high endocarditis risk | IV | 15 mg/kg | Once, before induction | — | — | Label · UK SmPC |
| child | C. difficile, <12 y | PO | 10 mg/kg | Every 6 h | 10 days | 2 g/day | Label · UK SmPC |
| neonate | Serious infections, PMA <29 weeks (Seek neonatal specialist advice) | IV | 15 mg/kg | Every 24 h | By infection | — | Label · UK SmPC |
| neonate | Serious infections, PMA 29–35 weeks | IV | 15 mg/kg | Every 12 h | By infection | — | Label · UK SmPC |
| neonate | Serious infections, PMA >35 weeks | IV | 15 mg/kg | Every 8 h | By infection | — | Label · UK SmPC |

- *renal* CrCl 20–49: Usual starting dose 15–20 mg/kg every 24 h; do not reduce the first dose. [Label · UK SmPC]
- *renal* CrCl <20 or dialysis: Timing and size of later doses depend on trough levels and the dialysis method; the next dose may be withheld until levels are known. Intermittent haemodialysis removes little vancomycin; high-flux membranes and CRRT remove more. [Label · UK SmPC]
- *renal* eGFR 30–50: Children: 15 mg/kg every 12 h. [Label · UK SmPC]
- *renal* eGFR 10–29: Children: 15 mg/kg every 24 h. [Label · UK SmPC]
- *renal* eGFR <10: Children: 10–15 mg/kg once, then re-dose by levels. [Label · UK SmPC]
- *renal* Anephric: Anephric adults: 15 mg/kg, then 1.9 mg/kg every 24 h. [Label · US]
- *hepatic*: No dose adjustment needed. [Label · UK SmPC]
- *elderly*: Lower maintenance doses may be needed because kidney function declines with age; monitor kidney function. [Label · UK SmPC]
- *pregnancy*: Use only if clearly needed, with careful level monitoring; much higher doses may be needed in pregnancy. Passes into breast milk, but significant absorption by the infant is unlikely. [Label · UK SmPC]
- *administration*: Infuse over at least 60 minutes or at no more than 10 mg/min (whichever is longer), diluted to 2.5–5 mg/mL (at least 100 mL per 500 mg). Rotate infusion sites. Never give IM. [Label · UK SmPC]
- *administration*: Oral use: dissolve one 500 mg vial in 30 mL water to drink or give by nasogastric tube. [Label · UK SmPC]
- *monitor*: Trough level usually 10–20 mg/L (15–20 mg/L if MIC ≥1 mg/L); first level on day 2 before the next dose, then daily to weekly; in haemodialysis, sample before the session. [Label · UK SmPC]
- *monitor*: Kidney function, white cell count, urine and liver tests during prolonged treatment; hearing tests in older patients and with other ototoxic drugs. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=vancomycin#emc-15736): Vancomycin 500 mg powder for concentrate for solution for infusion. Summary of Product Characteristics. hameln pharma ltd; text revised 19 Jan 2026. electronic medicines compendium (emc).
- [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=0543b2b5-b1c7-4ad6-b38c-3be0086f0e06&type=display): Vancomycin Hydrochloride for Injection, USP. Prescribing information. Glenmark Pharmaceuticals Inc.; revised 12/2025. DailyMed, U.S. National Library of Medicine.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=vancomycin#emc-15736): Vancomycin 500 mg powder for concentrate for solution for infusion. Summary of Product Characteristics. hameln pharma ltd; January 2026.
- Dosing source `Label · US`: [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=0543b2b5-b1c7-4ad6-b38c-3be0086f0e06&type=display): Vancomycin Hydrochloride for Injection, USP. Prescribing information. Glenmark Pharmaceuticals Inc.; revised 12/2025.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=vancomycin#emc-15736: hameln vancomycin 500 mg SmPC (text revised 19/01/2026): 4.1 cSSTI, bone/joint, CAP, HAP/VAP, endocarditis, perioperative prophylaxis, oral CDI; 4.2 adults ≥12 y 15–20 mg/kg q8–12h max 2 g/dose, loading 25–30 mg/kg; children 1 mo–<12 y 10–15 mg/kg q6h; neonates 15 mg/kg q24/12/8h by PMA <29/29–35/>35 wk; prophylaxis 15 mg/kg; oral CDI 125 mg q6h or 500 mg q6h x10 days, max 2 g/day, recurrences taper/pulse, children 10 mg/kg q6h; renal CrCl 20–49 15–20 mg/kg q24h, <20/RRT by levels; paediatric eGFR bands; hepatic none; elderly; pregnancy higher doses; trough 10–20 (15–20) mg/L, day 2; infusion ≥60 min/≤10 mg/min, 2.5–5 mg/mL; oral reconstitution 30 mL; 4.3 not IM; 4.4 SCARs must not restart, Kounis, HORV, IV ineffective for CDI, >60 mg/kg/day not recommended in children; 4.5 anaesthetics, bacitracin/polymyxin B/colistin/viomycin, PPIs/anti-motility; 4.8 ALT/AST common, interstitial nephritis, drug fever, chest/back pain.
- https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=0543b2b5-b1c7-4ad6-b38c-3be0086f0e06&type=display: Glenmark vancomycin for injection label (rev 12/2025): adults 2 g/day as 500 mg q6h or 1 g q12h; anephric 15 mg/kg then 1.9 mg/kg/24 h; infuse ≥60 min; contraindication hypersensitivity; warnings incl. LABD, HORV, hypotension/shock/cardiac arrest with rapid infusion; geriatric renal monitoring; no brand names.

---

## Warfarin  (`med_warfarin`)

**Description (kept)**

Warfarin inhibits vitamin K epoxide reductase (VKORC1), depleting reduced vitamin K and decreasing hepatic synthesis of functional clotting factors II, VII, IX and X (and proteins C and S). It is used for prevention and treatment of venous thromboembolism and thromboembolism in atrial fibrillation and mechanical heart valves, with dosing guided by the INR.

**Description (added)**

In the Philippines warfarin is listed in the Philippine National Formulary for prophylaxis and treatment of thromboembolic disorders, and the Stroke Society of the Philippines recommends either well-controlled warfarin or a direct oral anticoagulant for at-risk patients with non-valvular atrial fibrillation. Its main practical burden is regular INR testing and the many drug and food interactions; an INR above 4.0 adds bleeding risk without added benefit for most patients.

**Uses**: 3 kept, 2 added

- NEW: Transient ischaemic attack (UK labeling)
- NEW: Systemic embolism prevention in rheumatic heart disease with atrial fibrillation

**Side effects**: 6 kept, 4 added

- NEW: Pancreatitis, diarrhoea, nausea and vomiting
- NEW: Rash, alopecia and purpura
- NEW: Unexplained fall in haematocrit or haemoglobin
- NEW: Limb ischaemia or gangrene when started too early in heparin-induced thrombocytopenia

**Precautions**: 9 kept, 5 added

- NEW: Haemorrhagic stroke
- NEW: Within 72 hours of major surgery with risk of severe bleeding
- NEW: Within 48 hours postpartum
- NEW: Initial therapy in heparin-induced thrombocytopenia (start only after platelet count normalises)
- NEW: Rare hereditary galactose intolerance or lactase deficiency (UK tablets contain lactose)

**Interactions**: 6 kept, 7 added

- NEW: Fibrinolytics (streptokinase, alteplase): contraindicated combination.
- NEW: Allopurinol, capecitabine, erlotinib, tamoxifen, fibrates, statins (mainly fluvastatin), omeprazole and sulfamethoxazole: may raise INR.
- NEW: Phenytoin, primidone, griseofulvin, azathioprine and oral contraceptives: may lower warfarin effect.
- NEW: Corticosteroids, nevirapine and ritonavir: variable effect on INR; monitor closely.
- NEW: Cholestyramine and sucralfate reduce warfarin absorption; orlistat may reduce vitamin K absorption.
- NEW: Dabigatran, rivaroxaban and fondaparinux: additive bleeding risk.
- NEW: Cranberry (avoid), grapefruit juice and glucosamine: may raise INR.

**Disease links added**

- `hypertension`: **caution**: Uncontrolled or moderate-to-severe hypertension raises bleeding risk (UK SmPC, US label); malignant hypertension is a contraindication.
- `chronic_kidney_disease`: **caution**: No dose change, but more frequent INR checks; higher risk of bleeding, anticoagulant-related nephropathy and calciphylaxis (UK SmPC, US label).
- `type2_diabetes`: **caution**: Diabetes is listed among conditions with higher warfarin risk (US label).
- `acute_coronary_syndrome`: **safe**: After high-risk MI: INR 2.0–3.0 plus low-dose aspirin for at least 3 months (US label).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| adult | Starting dose (no genotype data) (No routine loading dose; usual maintenance 2–10 mg) | PO | 2–5 mg | Once a day | Until INR in range | — | Label · US |
| adult | Elective loading (UK regimen) (Then 3–9 mg once a day by INR; no loading in protein C deficiency) | PO | 10 mg | Once a day | 2 days | — | Label · UK SmPC |
| adult | DVT / PE treatment (Overlap heparin 4–5 days and until INR in range) | PO | Dose to INR 2.0–3.0 | Once a day | 3 months if provoked; ≥3 months if unprovoked | — | Label · US |
| adult | Atrial fibrillation | PO | Dose to INR 2.0–3.0 | Once a day | Long-term | — | Label · US |
| adult | Mechanical aortic valve (bileaflet, sinus rhythm) | PO | Dose to INR 2.0–3.0 | Once a day | Long-term | — | Label · US |
| adult | Mechanical mitral or caged-ball/disk valve | PO | Dose to INR 2.5–3.5 | Once a day | Long-term | — | Label · US |
| adult | Bioprosthetic mitral valve | PO | Dose to INR 2.0–3.0 | Once a day | First 3 months | — | Label · US |
| adult | After high-risk MI (With aspirin ≤100 mg/day) | PO | Dose to INR 2.0–3.0 | Once a day | ≥3 months | — | Label · US |

- *renal*: No dose adjustment; check INR more often. Watch kidney function if INR is high with blood in the urine (anticoagulant-related nephropathy). [Label · US]
- *hepatic*: Liver impairment can increase warfarin's effect; monitor more closely for bleeding. [Label · US]
- *elderly*: Use lower starting and maintenance doses in elderly or debilitated patients and in Asian patients (US label). Age 65 or over is a bleeding risk factor. [Label · US]
- *pregnancy*: Contraindicated except in women with mechanical valves at high thrombotic risk; first-trimester exposure causes embryopathy in about 5%. Check pregnancy status and use contraception during treatment and for 1 month after. Not found in breast milk in a small study; watch the infant for bruising. [Label · US]
- *administration*: Take at the same time each day. Missed dose: take it the same day as soon as possible; do not double the next day's dose. [Label · US]
- *administration*: Surgery with severe bleeding risk: stop 3 days before; other surgery can proceed with INR <2.5. Dental extractions do not need warfarin stopped. [Label · UK SmPC]
- *administration*: High INR or bleeding: INR 6–8 with no or minor bleeding, stop and restart when INR <5; INR >8, stop and give vitamin K 0.5–1 mg IV or 5 mg orally; life-threatening bleeding, prothrombin complex concentrate 30–50 units/kg (or FFP 15 mL/kg). [Label · UK SmPC]
- *monitor*: INR daily after the first dose until stable in range, then every 1–4 weeks; recheck within 2–3 days of any dose change or when other drugs are started or stopped. [Label · US]
- *monitor*: When overlapping with heparin, check INR at least 5 h after an IV bolus, 4 h after stopping an infusion or 24 h after a SC dose. [Label · US]
- *monitor*: Check thyroid status when starting in hyper- or hypothyroidism; ask about bleeding, skin pain or purple toes at each visit. [Label · UK SmPC]

**References added**

- [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=warfarin#emc-14333): Warfarin 5 mg tablets. Summary of Product Characteristics. Strides Pharma UK Ltd; text revised 10 May 2022, updated July 2025. electronic medicines compendium (emc).
- [DOST Health Technology Assessment Council (Philippines)](https://hta.dost.gov.ph/wp-content/uploads/2026/07/ES-DOACs-for-NVAF-25-April-2023.pdf): Health Technology Assessment Council. Evidence Summary on Apixaban, Dabigatran, and Rivaroxaban for the prevention of myocardial infarction, cerebrovascular disease, and other cardiovascular events among patients with nonvalvular atrial fibrillation. HTA Division, DOST; 25 April 2023.
- Dosing source `Label · US`: [DailyMed (FDA label)](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=541c9a70-adaf-4ef3-94ba-ad4e70dfa057): Warfarin sodium tablets. Prescribing information. Amneal Pharmaceuticals; revised 7/2026. DailyMed, U.S. National Library of Medicine.
- Dosing source `Label · UK SmPC`: [UK SmPC (emc)](https://products.mhra.gov.uk/search/?search=warfarin#emc-14333): Warfarin 5 mg tablets. Summary of Product Characteristics. Strides Pharma UK Ltd; 2022/2025.

**What was checked on each page**

- https://products.mhra.gov.uk/search/?search=warfarin#emc-14333: Strides warfarin 5 mg SmPC: 4.1 RHD with AF, prosthetic valves, VTE/PE, TIA; 4.2 loading 10 mg once daily for 2 days, maintenance 3.0–9.0 mg; children no data; 4.3 haemorrhagic stroke, within 72 h of major surgery, 48 h postpartum, 1st/3rd trimester, fibrinolytics; 4.4 calciphylaxis, thyroid monitoring, protein C no loading, surgery stop 3 days/INR <2.5, dental, bleeding risk factors incl. uncontrolled hypertension & renal insufficiency, INR within 2–3 days of dose change, ARN, lactose; Asian/Afro-Caribbean statement (conflicts with US, not used); 4.5 allopurinol, capecitabine, erlotinib, tamoxifen, fibrates, fluvastatin, omeprazole, sulfamethoxazole; phenytoin, primidone, griseofulvin, azathioprine, OCs; corticosteroids/nevirapine/ritonavir variable; cholestyramine, sucralfate, orlistat, glucosamine, cranberry, grapefruit; dabigatran/rivaroxaban/fondaparinux; 4.8 pancreatitis, alopecia, purpura, haematocrit drop; 4.9 reversal thresholds and doses.
- https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=541c9a70-adaf-4ef3-94ba-ad4e70dfa057: Amneal warfarin label (rev 7/2026): target INRs and durations (VTE, AF, mechanical valves 2.0–3.0 / 2.5–3.5, bioprosthetic mitral 3 months, post-MI + aspirin ≥3 months), INR >4 no benefit; initial 2–5 mg, maintenance 2–10 mg, no routine loading; lower doses elderly/debilitated/Asian; INR daily then 1–4 weeks; heparin overlap 4–5 days and INR timing; missed dose; 8.1 embryopathy ~5%, contraception 1 month; 8.2 not detected in milk (15 mothers); 8.6 renal no adjustment; 8.7 hepatic; warnings HIT, hypertension, diabetes, calciphylaxis.
- https://hta.dost.gov.ph/wp-content/uploads/2026/07/ES-DOACs-for-NVAF-25-April-2023.pdf: HTAC evidence summary (25 Apr 2023): 'Warfarin is currently listed in the Philippine National Formulary for prophylaxis and treatment of thromboembolic disorders'; Stroke Society of the Philippines recommends well-controlled warfarin or DOACs in at-risk NVAF; no forms/strengths given.

---

## Zinc Sulfate  (`med_zinc_sulfate`)

**Description (kept)**

Zinc is an essential trace element that serves as a cofactor for many enzymes and transcription factors involved in immunity, epithelial repair and growth. In acute diarrhea it inhibits several intracellular pathways of intestinal ion secretion (cAMP, calcium and nitric oxide) and supports mucosal recovery; WHO and UNICEF have recommended zinc with oral rehydration salts for all childhood diarrhea episodes since 2004. It is also used to correct zinc deficiency and, as zinc salts, in Wilson disease.

**Description (added)**

Besides shortening and easing the current episode, a 10–14 day zinc course lowers the incidence of diarrhoea in the following 2–3 months (WHO/UNICEF 2004). In the Philippines, DOH Administrative Order No. 2007-0045 (17 December 2007) adopted zinc supplementation together with reformulated ORS for the management of diarrhoea in children. WHO-prequalified products include 20 mg dispersible tablets and a 10 mg/5 mL oral solution.

**Uses**: 5 kept, 1 added

- NEW: Bloody diarrhoea (dysentery) in children, given as for watery diarrhoea alongside antibiotics

**Side effects**: 5 kept, 2 added

- NEW: Headache, irritability and lethargy (frequency not known)
- NEW: Gastric irritation and gastritis

**Precautions**: 4 kept, 2 added

- NEW: Copper deficiency
- NEW: Hereditary fructose intolerance with sorbitol-containing oral solutions

**Interactions**: 6 kept, 2 added

- NEW: Calcium salts, oral iron and trientine: mutual reduction in absorption; separate doses.
- NEW: Copper: zinc inhibits copper absorption.

**Disease links added**

- `acute_gastroenteritis`: **safe**: Zinc with low-osmolarity ORS is recommended for all children with acute diarrhoea (WHO/UNICEF 2004).
- `chronic_kidney_disease`: **caution**: Zinc may accumulate in renal failure (WHO-prequalified product information).

**Dosage table**

| Group | Indication | Route | Dose | Frequency | Duration | Max | Source |
|---|---|---|---|---|---|---|---|
| child | Acute or persistent diarrhoea, <6 months (= ½ × 20 mg tablet or 5 mL of 10 mg/5 mL solution) | PO | 10 mg elemental zinc | Once a day | 10–14 days | — | WHO/UNICEF 2004 |
| child | Acute or persistent diarrhoea, 6 months–5 y (= 1 × 20 mg tablet or 10 mL of 10 mg/5 mL solution) | PO | 20 mg elemental zinc | Once a day | 10–14 days | — | WHO/UNICEF 2004 |
| child | Dysentery (bloody diarrhoea) (Give antibiotic for Shigella separately) | PO | Same as acute diarrhoea by age | Once a day | 10–14 days | — | MOST 2005 |

- *renal*: Zinc may accumulate in renal failure. [Label · WHO PQ]
- *pregnancy*: Limited human data; animal studies show no reproductive toxicity at the therapeutic dose. Zinc is present in breast milk. [Label · WHO PQ]
- *administration*: Give between meals. If the child vomits within 30 minutes, repeat the dose. Missed dose: give as soon as possible unless the next is due within 6 hours. [Label · WHO PQ]
- *administration*: Dispersible tablet: dissolve in about 5 mL of expressed breast milk, ORS or clean water on a small spoon for infants; older children may chew it. Finish all 10–14 days even after diarrhoea stops. [MOST 2005]
- *administration*: Oral solution excipients: aspartame (avoid in phenylketonuria), sodium benzoate (may worsen newborn jaundice) and sorbitol (mild laxative effect). Discard 28 days after opening. [Label · WHO PQ]
- *monitor*: Ask about vomiting after doses; if the child vomits ORS, food and fluids, bring to a health facility rather than continuing zinc at home. [MOST 2005]

**References added**

- [WHO/UNICEF Joint Statement](https://stg.nutritioncluster.net/sites/nutritioncluster.com/files/2019-12/WHO_FCH_CAH_04.71.pdf): World Health Organization, UNICEF. Clinical Management of Acute Diarrhoea: WHO/UNICEF Joint Statement. WHO/FCH/CAH/04.7; May 2004.
- [WHO eLENA](https://www.who.int/tools/elena/bbc/zinc-diarrhoea): Khan WU, Sellen DW. Zinc supplementation in the management of diarrhoea: biological, behavioural and contextual rationale. WHO e-Library of Evidence for Nutrition Actions (eLENA); April 2011.
- [WHO Prequalification (WHOPAR product information)](https://extranet.who.int/prequal/sites/default/files/whopar_files/DI010part4v2.pdf): World Health Organization Prequalification Unit. Zinc (as sulfate monohydrate) 10 mg/5 mL oral solution, PharmEvo (DI010): Summary of Product Characteristics, WHOPAR part 4; revised June 2025.
- [Department of Health (Philippines)](https://elibrary.judiciary.gov.ph/thebookshelf/showdocsfriendly/10/52204): Department of Health. Administrative Order No. 2007-0045: Zinc Supplementation and Reformulated Oral Rehydration Salt in the Management of Diarrhea Among Children. Adopted 17 December 2007. National Administrative Register Vol. 19 No. 1 (Jan–Mar 2008), Supreme Court E-Library.
- [MOST / USAID](https://cdn.who.int/media/docs/default-source/2021-dha-docs/pnadk428.pdf): MOST, the USAID Micronutrient Program. Diarrhoea Treatment Guidelines including new recommendations for the use of ORS and zinc supplementation for clinic-based healthcare workers. Arlington, VA; January 2005.
- Dosing source `WHO/UNICEF 2004`: [WHO/UNICEF Joint Statement](https://stg.nutritioncluster.net/sites/nutritioncluster.com/files/2019-12/WHO_FCH_CAH_04.71.pdf): World Health Organization, UNICEF. Clinical Management of Acute Diarrhoea. WHO/FCH/CAH/04.7; 2004.
- Dosing source `Label · WHO PQ`: [WHO Prequalification (WHOPAR)](https://extranet.who.int/prequal/sites/default/files/whopar_files/DI010part4v2.pdf): Zinc (as sulfate monohydrate) 10 mg/5 mL oral solution (DI010), SmPC; June 2025.
- Dosing source `MOST 2005`: [MOST / USAID](https://cdn.who.int/media/docs/default-source/2021-dha-docs/pnadk428.pdf): Diarrhoea Treatment Guidelines including new recommendations for the use of ORS and zinc supplementation. MOST, USAID Micronutrient Program; 2005.

**What was checked on each page**

- https://stg.nutritioncluster.net/sites/nutritioncluster.com/files/2019-12/WHO_FCH_CAH_04.71.pdf: WHO/UNICEF joint statement WHO/FCH/CAH/04.7 (May 2004): 20 mg/day zinc for 10–14 days, 10 mg/day under 6 months; reduces duration and severity and lowers incidence of diarrhoea in the following 2–3 months; low-osmolarity ORS composition.
- https://www.who.int/tools/elena/bbc/zinc-diarrhoea: WHO eLENA rationale page (Khan & Sellen, April 2011): 20 mg/day >6 months, 10 mg/day <6 months, 10–14 days; reduces duration/severity and later infections for 2–3 months.
- https://extranet.who.int/prequal/sites/default/files/whopar_files/DI010part4v2.pdf: WHOPAR DI010 (PharmEvo 10 mg/5 mL oral solution, rev June 2025): <6 mo 5 mL (10 mg), 6 mo–5 y 10 mL (20 mg) once daily 10–14 days; between meals, repeat if vomit within 30 min, missed dose rule; 4.3 copper deficiency; 4.4 renal accumulation, aspartame, sodium benzoate, sorbitol/fructose intolerance; 4.5 calcium, iron, trientine, copper; 4.6 pregnancy/breast milk; 4.8 headache, irritability, lethargy, gastritis; discard 28 days after opening.
- https://elibrary.judiciary.gov.ph/thebookshelf/showdocsfriendly/10/52204: Supreme Court E-Library, NAR Vol 19 No 1: DOH Administrative Order No. 2007-0045 'Zinc Supplementation and Reformulated Oral Rehydration Salt in the Management of Diarrhea Among Children', adopted 17 Dec 2007 (title and date only; full text not on page).
- https://cdn.who.int/media/docs/default-source/2021-dha-docs/pnadk428.pdf: MOST/USAID 2005 diarrhoea treatment guidelines: <6 mo ½ tablet, ≥6 mo 1 tablet for 10/14 days; dissolve in ~5 mL breast milk/ORS/water; complete course; zinc for dysentery as for watery diarrhoea with separate Shigella antibiotic; vomiting ORS/food/fluids -> health facility.

---

