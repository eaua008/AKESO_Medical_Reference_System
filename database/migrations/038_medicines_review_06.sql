-- 038_medicines_review_06.sql  -  medicine review b06: med_pyrazinamide, med_rabies_immunoglobulin, med_rabies_vaccine, med_rifampicin, med_salbutamol, med_spironolactone, med_sumatriptan, med_tenofovir, med_tld, med_vancomycin, med_warfarin, med_zinc_sulfate
-- Adds only: longer descriptions, new facts, references, disease links, and dosage
-- tables (for medicines that have none yet). Nothing is deleted or reworded.
-- Needs 030_medicine_doses.sql first. Safe to run twice (every insert is guarded).

begin;

-- ================================================ med_pyrazinamide  (Pyrazinamide)
update public.medicines set description = 'Pyrazinamide is a prodrug converted to pyrazinoic acid, which is active against semi-dormant M. tuberculosis in acidic environments; its exact mechanism is not fully understood. It is used during the 2-month intensive phase of first-line TB therapy, allowing total treatment to be shortened to 6 months. In the Philippine NTP it is given as part of the HRZE fixed-dose combination tablet in the intensive phase of Category I (2HRZE/4HR) and in the first 3 months of Category II retreatment (2HRZES/1HRZE/5HRE), with the number of tablets set by body-weight band. Single-drug pyrazinamide (including a 250 mg/5 mL suspension) is used for weight-based dosing in children who cannot take tablets.', updated_at = now()
where id = 'med_pyrazinamide' and description = 'Pyrazinamide is a prodrug converted to pyrazinoic acid, which is active against semi-dormant M. tuberculosis in acidic environments; its exact mechanism is not fully understood. It is used during the 2-month intensive phase of first-line TB therapy, allowing total treatment to be shortened to 6 months.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine NTP Manual of Procedures; Philippine National Formulary (PNF) EML; MSF Tuberculosis guideline; UK SmPC (emc)' else source_attribution || '; Philippine NTP Manual of Procedures; Philippine National Formulary (PNF) EML; MSF Tuberculosis guideline; UK SmPC (emc)' end
where id = 'med_pyrazinamide' and position('Philippine NTP Manual of Procedures' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'indication', 'Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'indication' and content = 'Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'indication', 'Drug-susceptible TB meningitis, intensive 6-month regimen (6HRZEto) at a higher dose (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'indication' and content = 'Drug-susceptible TB meningitis, intensive 6-month regimen (6HRZEto) at a higher dose (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'adverse', 'Headache, dizziness, irritability, insomnia (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'adverse' and content = 'Headache, dizziness, irritability, insomnia (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'adverse', 'Sideroblastic anaemia, angioedema, hypertension and pellagra (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'adverse' and content = 'Sideroblastic anaemia, angioedema, hypertension and pellagra (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'adverse', 'Erythema multiforme (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'adverse' and content = 'Erythema multiforme (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'adverse', 'Fever, malaise and urticaria', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'adverse' and content = 'Fever, malaise and urticaria');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'contraindication', 'Acute liver disease (e.g., hepatitis) and up to 6 months after hepatitis (UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'contraindication' and content = 'Acute liver disease (e.g., hepatitis) and up to 6 months after hepatitis (UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'contraindication', 'Acute porphyria', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'contraindication' and content = 'Acute porphyria');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'contraindication', 'Hyperuricaemia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'contraindication' and content = 'Hyperuricaemia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'contraindication', 'Breast-feeding (UK SmPC; MSF lists no contraindication)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'contraindication' and content = 'Breast-feeding (UK SmPC; MSF lists no contraindication)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'interaction', 'Blood glucose-lowering drugs: pyrazinamide may affect glucose control; monitor glucose more closely in diabetes.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction' and content = 'Blood glucose-lowering drugs: pyrazinamide may affect glucose control; monitor glucose more closely in diabetes.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'interaction', 'Rifampicin: pyrazinamide may lower rifampicin levels (UK SmPC).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction' and content = 'Rifampicin: pyrazinamide may lower rifampicin levels (UK SmPC).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'interaction', 'Oestrogen-containing contraceptives: effect may be reduced.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction' and content = 'Oestrogen-containing contraceptives: effect may be reduced.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'interaction', 'Oral typhoid vaccine: avoid pyrazinamide for 3 days before and after vaccination.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction' and content = 'Oral typhoid vaccine: avoid pyrazinamide for 3 days before and after vaccination.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_pyrazinamide', 'interaction', 'Alcohol: avoid; heavy drinking raises the risk of liver damage.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_pyrazinamide' and kind = 'interaction' and content = 'Alcohol: avoid; heavy drinking raises the risk of liver damage.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_pyrazinamide', 'Philippine NTP Manual of Procedures', 'Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.', 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_pyrazinamide'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_pyrazinamide' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_pyrazinamide', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_pyrazinamide'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_pyrazinamide' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_pyrazinamide', 'MSF Tuberculosis guideline', 'Médecins Sans Frontières. Tuberculosis - Appendix 10, TB drug information sheets: Pyrazinamide (Z). Updated January 2022.', 'https://medicalguidelines.msf.org/en/viewport/TUB/english/pyrazinamide-z-20323874.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_pyrazinamide'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_pyrazinamide' and url = 'https://medicalguidelines.msf.org/en/viewport/TUB/english/pyrazinamide-z-20323874.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_pyrazinamide', 'MSF Tuberculosis guideline', 'Médecins Sans Frontières. Tuberculosis - Appendix 13. Daily dose of TB drugs using fixed-dose combinations. Updated October 2022.', 'https://medicalguidelines.msf.org/en/node/1205', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_pyrazinamide'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_pyrazinamide' and url = 'https://medicalguidelines.msf.org/en/node/1205');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_pyrazinamide', 'UK SmPC (emc)', 'Pyrazinamide 500 mg Tablets - Summary of Product Characteristics. Morningside Healthcare Ltd. Electronic medicines compendium (emc), updated June 2025.', 'https://products.mhra.gov.uk/search/?search=pyrazinamide#emc-101051', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_pyrazinamide'), 0)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_pyrazinamide' and url = 'https://products.mhra.gov.uk/search/?search=pyrazinamide#emc-101051');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'gout', 'med_pyrazinamide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'gout'), 0), 'avoid'::condition_safety, 'Contraindicated in hyperuricaemia and acute gouty arthritis; give only if treatment is urgent, monitor uric acid and stop if acute gout develops (UK SmPC).'
where exists (select 1 from public.diseases where id = 'gout')
  and exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'gout' and medicine_id = 'med_pyrazinamide');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_pyrazinamide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'High doses may affect glucose control; monitor diabetic patients more closely (UK SmPC).'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_pyrazinamide');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_pyrazinamide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Give 25 mg/kg three times a week in renal insufficiency (MSF); UK SmPC advises reduced dose and frequency.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_pyrazinamide');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hepatitis_b', 'med_pyrazinamide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hepatitis_b'), 0), 'caution'::condition_safety, 'Contraindicated in acute hepatitis and for 6 months after (UK SmPC); applying this to hepatitis B is an inference, not stated for HBV specifically.'
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hepatitis_b' and medicine_id = 'med_pyrazinamide');
-- med_pyrazinamide
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_pyrazinamide', 'adult', 0, 'TB Cat I intensive (2HRZE), 30–37 kg', 'PO', '2 tablets HRZE FDC', 'Once a day', '2 months', '—', 'NTP MOP 2014', 'HRZE = H75/R150/Z400/E275 mg'),
    ('med_pyrazinamide', 'adult', 1, 'TB Cat I intensive (2HRZE), 38–54 kg', 'PO', '3 tablets HRZE FDC', 'Once a day', '2 months', '—', 'NTP MOP 2014', ''),
    ('med_pyrazinamide', 'adult', 2, 'TB Cat I intensive (2HRZE), 55–70 kg', 'PO', '4 tablets HRZE FDC', 'Once a day', '2 months', '—', 'NTP MOP 2014', ''),
    ('med_pyrazinamide', 'adult', 3, 'TB Cat I intensive (2HRZE), >70 kg', 'PO', '5 tablets HRZE FDC', 'Once a day', '2 months', '—', 'NTP MOP 2014', 'Cat II: HRZE months 1–3, same tablet numbers'),
    ('med_pyrazinamide', 'adult', 4, 'TB, single-drug formulation', 'PO', '25 mg/kg (range 20–30)', 'Once a day', 'Intensive phase', '2 g/day', 'NTP MOP 2014', ''),
    ('med_pyrazinamide', 'adult', 5, 'TB, standard regimen', 'PO', '1.5 g (<50 kg); 2 g (≥50 kg)', 'Once a day', '2 months', '2 g/day', 'Label · UK SmPC', ''),
    ('med_pyrazinamide', 'adult', 6, 'TB, intermittent supervised regimen', 'PO', '2 g (<50 kg); 2.5 g (≥50 kg)', '3× a week', '2 months', '—', 'Label · UK SmPC', 'Only if daily dosing is not feasible'),
    ('med_pyrazinamide', 'adult', 7, 'TB meningitis (6HRZEto)', 'PO', '40 mg/kg', 'Once a day', '6 months', '2 g/day', 'MSF TB', ''),
    ('med_pyrazinamide', 'child', 8, 'TB, single-drug formulation', 'PO', '30 mg/kg (range 20–40)', 'Once a day', 'Intensive phase', '2 g/day', 'NTP MOP 2014', 'Suspension 250 mg/5 mL dosed by weight (Table 14); newborn <4 weeks: refer'),
    ('med_pyrazinamide', 'child', 9, 'TB, child <30 kg', 'PO', '35 mg/kg (range 30–40)', 'Once a day', 'Intensive phase', '2 g/day', 'MSF TB', '150 mg dispersible tablet in 10 mL water'),
    ('med_pyrazinamide', 'child', 10, 'TB intensive phase, HRZ 50/75/150 FDC', 'PO', '4–7 kg: 1; 8–11 kg: 2; 12–15 kg: 3; 16–22 kg: 4 tablets', 'Once a day', '2 months', '—', 'MSF FDC', 'Plus ethambutol where indicated')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_pyrazinamide');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_pyrazinamide', 'renal', 0, 'Renal insufficiency', '25 mg/kg three times a week.', 'MSF TB'),
    ('med_pyrazinamide', 'renal', 1, '', 'UK label: reduce dose and frequency; use only in emergencies, given intermittently.', 'Label · UK SmPC'),
    ('med_pyrazinamide', 'hepatic', 2, '', 'Contraindicated in severe hepatic impairment, acute liver disease and for 6 months after hepatitis. If hepatocellular damage occurs, stop and do not restart. Heavy drinkers and patients on other hepatotoxic drugs are at higher risk.', 'Label · UK SmPC'),
    ('med_pyrazinamide', 'pregnancy', 3, '', 'MSF: no contraindication in pregnancy or breastfeeding. The UK SmPC states clinical data in pregnancy are insufficient (use only if benefit clearly outweighs risk) and contraindicates breastfeeding because it passes into milk.', 'MSF TB'),
    ('med_pyrazinamide', 'administration', 4, '', 'Take with or without food. For GI upset, give at bedtime or with small meals. Advise sun protection (photosensitivity).', 'NTP MOP 2014'),
    ('med_pyrazinamide', 'forms_ph', 5, '', 'Only in fixed-dose combinations (List B): isoniazid + rifampicin + pyrazinamide + ethambutol 75/150/400/275 mg tablet; isoniazid + rifampicin + pyrazinamide 50/75/150 mg dispersible tablet (pediatric). A single-ingredient pyrazinamide entry could not be read in the PNF text (it stops at ''M'').', 'PNF'),
    ('med_pyrazinamide', 'monitor', 6, '', 'LFTs (AST, ALT) before starting and every 2–4 weeks; kidney function every 3–4 weeks.', 'Label · UK SmPC'),
    ('med_pyrazinamide', 'monitor', 7, '', 'Arthralgia: give aspirin or an NSAID; if it persists, check serum uric acid and consider gout.', 'NTP MOP 2014'),
    ('med_pyrazinamide', 'monitor', 8, '', 'Blood glucose in diabetes; uric acid in patients with gout history.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_pyrazinamide');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_pyrazinamide', 'NTP MOP 2014', 'Philippine NTP Manual of Procedures', 'DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 11–15).', 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf', 0),
    ('med_pyrazinamide', 'PNF', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 1),
    ('med_pyrazinamide', 'MSF TB', 'MSF Tuberculosis guideline', 'MSF Tuberculosis, Appendix 10: Pyrazinamide (Z), 2022.', 'https://medicalguidelines.msf.org/en/viewport/TUB/english/pyrazinamide-z-20323874.html', 2),
    ('med_pyrazinamide', 'MSF FDC', 'MSF Tuberculosis guideline', 'MSF Tuberculosis, Appendix 13: daily dose of TB drugs using FDCs, 2022.', 'https://medicalguidelines.msf.org/en/node/1205', 3),
    ('med_pyrazinamide', 'Label · UK SmPC', 'UK SmPC (emc)', 'Pyrazinamide 500 mg Tablets - SmPC. Morningside Healthcare Ltd, 2025.', 'https://products.mhra.gov.uk/search/?search=pyrazinamide#emc-101051', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_pyrazinamide')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_pyrazinamide');


-- ================================================ med_rabies_immunoglobulin  (Rabies Immunoglobulin (HRIG / ERIG))
update public.medicines set description = 'Rabies immunoglobulin provides ready-made rabies virus-neutralizing antibodies, prepared from the plasma of immunized human donors (HRIG) or from hyperimmunized horses as purified equine immunoglobulin or F(ab'')2 fragments (ERIG). Infiltrated into and around the wound, it neutralizes virus at the inoculation site before vaccine-induced antibodies appear. It is used with rabies vaccine for category III exposures in persons not previously vaccinated. In the Philippine public program, the DOH supplies only equine RIG to government Animal Bite Treatment Centers, and patients often pay out of pocket for it when stocks run out. Under DOH Administrative Order 2018-0013, RIG volume left after wound infiltration need not be injected IM and may be kept aseptically and fractionated for the next patient. When supply is limited, WHO gives priority to multiple or deep bites, bites to highly innervated parts of the body, severely immunodeficient patients, exposures to confirmed or probable rabid animals, and bat exposures.', updated_at = now()
where id = 'med_rabies_immunoglobulin' and description = 'Rabies immunoglobulin provides ready-made rabies virus-neutralizing antibodies, prepared from the plasma of immunized human donors (HRIG) or from hyperimmunized horses as purified equine immunoglobulin or F(ab'')2 fragments (ERIG). Infiltrated into and around the wound, it neutralizes virus at the inoculation site before vaccine-induced antibodies appear. It is used with rabies vaccine for category III exposures in persons not previously vaccinated.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'DOH Administrative Order 2018-0013; MSF Essential Drugs; WHO PEP recommendations; PLOS ONE; WHO position paper (summary)' else source_attribution || '; DOH Administrative Order 2018-0013; MSF Essential Drugs; WHO PEP recommendations; PLOS ONE; WHO position paper (summary)' end
where id = 'med_rabies_immunoglobulin' and position('DOH Administrative Order 2018-0013' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_immunoglobulin', 'indication', 'Category II exposures to the head or neck, which DOH manages as category III (vaccine plus RIG)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'indication' and content = 'Category II exposures to the head or neck, which DOH manages as category III (vaccine plus RIG)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_immunoglobulin', 'indication', 'Category II as well as category III exposures in immunocompromised patients (DOH, MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'indication' and content = 'Category II as well as category III exposures in immunocompromised patients (DOH, MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_immunoglobulin', 'indication', 'Infants born to rabid mothers, with vaccine, as early as possible after birth (DOH)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'indication' and content = 'Infants born to rabid mothers, with vaccine, as early as possible after birth (DOH)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_immunoglobulin', 'adverse', 'Fever and joint pain (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'adverse' and content = 'Fever and joint pain (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_immunoglobulin', 'contraindication', 'Finger or toe wounds: infiltrate cautiously to avoid raised compartment pressure or impaired circulation', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'contraindication' and content = 'Finger or toe wounds: infiltrate cautiously to avoid raised compartment pressure or impaired circulation');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_immunoglobulin', 'contraindication', 'Aspirate before injecting; intravascular injection risks shock (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'contraindication' and content = 'Aspirate before injecting; intravascular injection risks shock (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_immunoglobulin', 'interaction', 'Other vaccines given the same day: use separate syringes and injection sites (MSF).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_immunoglobulin' and kind = 'interaction' and content = 'Other vaccines given the same day: use separate syringes and injection sites (MSF).');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rabies_immunoglobulin', 'DOH Administrative Order 2018-0013', 'Department of Health (Philippines). Administrative Order No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 16 April 2018. (Text reproduced on LegalDex.)', 'https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rabies_immunoglobulin'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rabies_immunoglobulin' and url = 'https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rabies_immunoglobulin', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Human rabies immunoglobulin (HRIG). MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/human-rabies-immunoglobulin-hrig-16688380.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rabies_immunoglobulin'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rabies_immunoglobulin' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/human-rabies-immunoglobulin-hrig-16688380.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rabies_immunoglobulin', 'WHO PEP recommendations', 'World Health Organization. Rabies: PEP recommendations – WHO recommends the intradermal route for rabies post-exposure prophylaxis. WHO Control of Neglected Tropical Diseases.', 'https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rabies_immunoglobulin'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rabies_immunoglobulin' and url = 'https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rabies_immunoglobulin', 'PLOS ONE', 'Amparo ACB, Jayme SI, Roces MCR, et al. The evaluation of operating Animal Bite Treatment Centers in the Philippines from a health provider perspective. PLoS ONE. 2018;13(7):e0199186.', 'https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rabies_immunoglobulin'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rabies_immunoglobulin' and url = 'https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_rabies_immunoglobulin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'safe'::condition_safety, 'HIV/AIDS counts as immunocompromised: DOH gives RIG with the standard IM vaccine regimen for both category II and III exposures.'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_rabies_immunoglobulin');
-- med_rabies_immunoglobulin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_rabies_immunoglobulin', 'adult', 0, 'Category III exposure, HRIG', 'Infiltration', '20 IU/kg', 'Single dose', 'Day 0 (up to day 7)', '20 IU/kg', 'DOH AO 2018', 'Infiltrate full dose into and around wound(s); 150 IU/mL, 2 mL vial'),
    ('med_rabies_immunoglobulin', 'adult', 1, 'Category III exposure, ERIG / F(ab'')2', 'Infiltration', '40 IU/kg', 'Single dose', 'Day 0 (up to day 7)', '40 IU/kg', 'DOH AO 2018', '200 IU/mL, 5 mL vial; e.g. 50 kg = 2000 IU = 10 mL'),
    ('med_rabies_immunoglobulin', 'adult', 2, 'Category III exposure (WHO)', 'Infiltration', 'HRIG 20 IU/kg; ERIG 40 IU/kg', 'Single dose', '≤ day 7 after first vaccine dose', '20 / 40 IU/kg; no minimum', 'WHO 2018', 'As much as possible into the wound'),
    ('med_rabies_immunoglobulin', 'child', 3, 'Category III exposure, HRIG', 'Infiltration', '20 IU/kg', 'Single dose', 'Day 0 (up to day 7)', '20 IU/kg', 'MSF', 'Same dose for all ages'),
    ('med_rabies_immunoglobulin', 'child', 4, 'Category III exposure, ERIG / F(ab'')2', 'Infiltration', '40 IU/kg', 'Single dose', 'Day 0 (up to day 7)', '40 IU/kg', 'MSF', 'If HRIG unavailable')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_rabies_immunoglobulin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_rabies_immunoglobulin', 'administration', 0, '', 'If the computed dose is too small to cover all wounds, dilute it 2–3-fold with sterile 0.9% saline; never exceed the computed dose. Infiltrate even healed wounds.', 'DOH AO 2018'),
    ('med_rabies_immunoglobulin', 'administration', 1, '', 'Use a 23–24 G, 1-inch needle and avoid repeated needle punctures into the same wound. Delay suturing for at least 2 hours after RIG if suturing cannot be avoided.', 'DOH AO 2018'),
    ('med_rabies_immunoglobulin', 'administration', 2, '', 'If RIG and vaccine cannot be given on the same day, give the vaccine first; RIG is given only once per PEP course and is not indicated after day 7.', 'DOH AO 2018'),
    ('med_rabies_immunoglobulin', 'administration', 3, '', 'Leftover RIG may be fractionated aseptically for other patients; remaining volume does not need IM injection.', 'WHO 2018'),
    ('med_rabies_immunoglobulin', 'administration', 4, '', 'DOH still highly recommends an ERIG skin test, whereas WHO 2018 says skin testing is unnecessary and should be abandoned; follow the local program protocol.', 'DOH AO 2018'),
    ('med_rabies_immunoglobulin', 'pregnancy', 5, '', 'Pregnancy and infancy are not contraindications to RIG; no contraindication in breast-feeding.', 'DOH AO 2018'),
    ('med_rabies_immunoglobulin', 'monitor', 6, '', 'Observe patients for at least 1 hour after ERIG, with epinephrine available.', 'DOH AO 2018'),
    ('med_rabies_immunoglobulin', 'monitor', 7, '', 'After infiltrating fingers or toes, check circulation and signs of raised compartment pressure.', 'MSF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_rabies_immunoglobulin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_rabies_immunoglobulin', 'DOH AO 2018', 'DOH Administrative Order 2018-0013', 'Department of Health (Philippines). AO No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 2018.', 'https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures', 0),
    ('med_rabies_immunoglobulin', 'WHO 2018', 'WHO position paper (summary)', 'World Health Organization. Rabies vaccines and immunoglobulins: WHO position, April 2018 (summary).', 'https://cdn.who.int/media/docs/default-source/immunization/position_paper_documents/rabies/pp-rabies-summary-2018.pdf', 1),
    ('med_rabies_immunoglobulin', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Human rabies immunoglobulin (HRIG).', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/human-rabies-immunoglobulin-hrig-16688380.html', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_rabies_immunoglobulin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_rabies_immunoglobulin');


-- ================================================ med_rabies_vaccine  (Rabies Vaccine (PVRV / PCECV))
update public.medicines set description = 'Cell-culture rabies vaccines contain inactivated rabies virus grown in Vero cells (PVRV) or chick embryo cells (PCECV). They induce virus-neutralizing antibodies, which take time to develop, so post-exposure prophylaxis combines immediate wound washing, a vaccine course and, for category III exposures, rabies immunoglobulin to cover the gap. Because clinical rabies is almost always fatal, post-exposure prophylaxis has no contraindication. WHO recommends the intradermal route for PEP because it uses 60–80% less vaccine (1–2 vials per course versus 4–5 for intramuscular schedules) and a single vial can be shared between several patients. Philippine Animal Bite Treatment Centers (513 by July 2017) give the vaccine almost exclusively intradermally using the modified 2-site Thai Red Cross regimen, and DOH requires WHO-prequalified vaccine for PEP. Since 2016, government policy has provided all four vaccine visits free of charge, although stock-outs still force some patients to buy vaccine privately.', updated_at = now()
where id = 'med_rabies_vaccine' and description = 'Cell-culture rabies vaccines contain inactivated rabies virus grown in Vero cells (PVRV) or chick embryo cells (PCECV). They induce virus-neutralizing antibodies, which take time to develop, so post-exposure prophylaxis combines immediate wound washing, a vaccine course and, for category III exposures, rabies immunoglobulin to cover the gap. Because clinical rabies is almost always fatal, post-exposure prophylaxis has no contraindication.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'DOH Administrative Order 2018-0013; MSF Essential Drugs; PLOS ONE; WHO position paper (summary)' else source_attribution || '; DOH Administrative Order 2018-0013; MSF Essential Drugs; PLOS ONE; WHO position paper (summary)' end
where id = 'med_rabies_vaccine' and position('DOH Administrative Order 2018-0013' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_vaccine', 'indication', 'Infants born to rabid mothers: vaccine together with RIG as early as possible after birth (DOH)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'indication' and content = 'Infants born to rabid mothers: vaccine together with RIG as early as possible after birth (DOH)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_vaccine', 'indication', 'Pre-exposure prophylaxis for people in remote rabies-endemic areas with poor PEP access or dog-bite incidence above 5% per year (WHO)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'indication' and content = 'Pre-exposure prophylaxis for people in remote rabies-endemic areas with poor PEP access or dog-bite incidence above 5% per year (WHO)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_vaccine', 'contraindication', 'Nerve-tissue vaccines should be avoided: less immunogenic and more severe adverse effects than cell-culture vaccines (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'contraindication' and content = 'Nerve-tissue vaccines should be avoided: less immunogenic and more severe adverse effects than cell-culture vaccines (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_vaccine', 'contraindication', 'Intradermal route only where correct ID technique can be assured; otherwise use IM (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'contraindication' and content = 'Intradermal route only where correct ID technique can be assured; otherwise use IM (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_vaccine', 'interaction', 'Other vaccines given the same day: use separate syringes and injection sites (MSF).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'interaction' and content = 'Other vaccines given the same day: use separate syringes and injection sites (MSF).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rabies_vaccine', 'interaction', 'Chronic liver disease, chloroquine use or systemic steroids: DOH gives the standard IM regimen, without delaying vaccination.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rabies_vaccine' and kind = 'interaction' and content = 'Chronic liver disease, chloroquine use or systemic steroids: DOH gives the standard IM regimen, without delaying vaccination.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rabies_vaccine', 'DOH Administrative Order 2018-0013', 'Department of Health (Philippines). Administrative Order No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 16 April 2018. (Text reproduced on LegalDex.)', 'https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rabies_vaccine'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rabies_vaccine' and url = 'https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rabies_vaccine', 'WHO PEP recommendations', 'World Health Organization. Rabies: PEP recommendations – WHO recommends the intradermal route for rabies post-exposure prophylaxis. WHO Control of Neglected Tropical Diseases.', 'https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rabies_vaccine'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rabies_vaccine' and url = 'https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/pep-recommendations');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rabies_vaccine', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Rabies vaccine. MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/rabies-vaccine-16687811.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rabies_vaccine'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rabies_vaccine' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/rabies-vaccine-16687811.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rabies_vaccine', 'PLOS ONE', 'Amparo ACB, Jayme SI, Roces MCR, et al. The evaluation of operating Animal Bite Treatment Centers in the Philippines from a health provider perspective. PLoS ONE. 2018;13(7):e0199186.', 'https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rabies_vaccine'), 0)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rabies_vaccine' and url = 'https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199186');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_rabies_vaccine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'caution'::condition_safety, 'HIV/AIDS counts as immunocompromised: DOH uses the standard IM regimen (not the ID regimen) plus RIG for category II and III exposures; WHO adds a third PrEP dose on day 21–28.'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_rabies_vaccine');
-- med_rabies_vaccine
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_rabies_vaccine', 'adult', 0, 'PEP, category II/III (DOH ID regimen)', 'ID', '0.1 mL at 2 sites', 'Days 0, 3, 7, 28', '4 visits (2-2-2-0-2)', '—', 'DOH AO 2018', 'One dose per deltoid; day 28 may be omitted with WHO-prequalified vaccine (2-2-2-0-0)'),
    ('med_rabies_vaccine', 'adult', 1, 'PEP, category II/III (WHO 1-week ID)', 'ID', '0.1 mL at 2 sites', 'Days 0, 3, 7', '1 week', '—', 'WHO 2018', 'Category III: plus RIG'),
    ('med_rabies_vaccine', 'adult', 2, 'PEP, Zagreb (2-0-1-0-1)', 'IM', '0.5 mL PVRV or 1 mL PCECV', '2 doses day 0; 1 dose days 7, 21', '3 weeks', '—', 'DOH AO 2018', 'Day 0 dose in both deltoids'),
    ('med_rabies_vaccine', 'adult', 3, 'PEP, shortened IM (1-1-1-1-0)', 'IM', '0.5 mL PVRV or 1 mL PCECV', 'Days 0, 3, 7, 14', '2 weeks', '—', 'DOH AO 2018', 'WHO: 4th dose any day from 14 to 28'),
    ('med_rabies_vaccine', 'adult', 4, 'PEP, previously vaccinated', 'ID', '0.1 mL at 1 site', 'Days 0, 3', '2 visits', '—', 'DOH AO 2018', 'Or 0.1 mL at 4 sites on day 0; no RIG; IM boosters discouraged'),
    ('med_rabies_vaccine', 'adult', 5, 'PrEP, immunocompetent', 'ID', '0.1 mL at 2 sites', 'Days 0, 7', '1 week', '—', 'WHO 2018', 'Or 1 vial IM at 1 site on days 0, 7'),
    ('med_rabies_vaccine', 'adult', 6, 'PrEP, immunocompromised', 'IM', '1 vial (0.5 mL PVRV / 1 mL PCECV)', 'Days 0, 7, 21–28', '3–4 weeks', '—', 'DOH AO 2018', 'WHO: ID or IM plus third dose day 21–28'),
    ('med_rabies_vaccine', 'child', 7, 'PEP, category II/III (DOH ID regimen)', 'ID', '0.1 mL at 2 sites', 'Days 0, 3, 7, 28', '4 visits (2-2-2-0-2)', '—', 'DOH AO 2018', 'Same dose as adults; anterolateral thigh in infants'),
    ('med_rabies_vaccine', 'child', 8, 'PEP, IM regimens', 'IM', '0.5 mL PVRV or 1 mL PCECV', 'As adult schedule', '2–3 weeks', '—', 'MSF', 'Anterolateral thigh if < 2 y; deltoid if ≥ 2 y; never gluteal'),
    ('med_rabies_vaccine', 'child', 9, 'PrEP, immunocompetent', 'ID', '0.1 mL at 2 sites', 'Days 0, 7', '1 week', '—', 'WHO 2018', 'Schedules apply to all age groups')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_rabies_vaccine');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_rabies_vaccine', 'forms_ph', 0, '', 'DOH program vaccines: PVRV 0.5 mL/vial and PCECV 1 mL/vial (powder with diluent); ID dose 0.1 mL for both. PNF entry not readable.', 'DOH AO 2018'),
    ('med_rabies_vaccine', 'administration', 1, '', 'Each ID dose must raise a wheal of at least 3 mm (1 mL syringe, 27 G needle); repeat any dose given SC or IM by mistake.', 'DOH AO 2018'),
    ('med_rabies_vaccine', 'administration', 2, '', 'A delayed dose does not restart the schedule; changing vaccine product or route mid-course is acceptable if unavoidable.', 'DOH AO 2018'),
    ('med_rabies_vaccine', 'administration', 3, '', 'Biting dog or cat is observed for 14 days; non-WHO-prequalified PEP is stopped if the animal stays healthy. New exposure within 3 months of completed PEP needs wound care only (WHO).', 'DOH AO 2018'),
    ('med_rabies_vaccine', 'administration', 4, '', 'Start PEP as soon as possible even if the patient presents long after exposure; check national schedules (MSF).', 'MSF'),
    ('med_rabies_vaccine', 'administration', 5, '', 'DOH allows reconstituted vaccine to be kept refrigerated and used within 8 hours (enables ID vial sharing); MSF says use immediately.', 'DOH AO 2018'),
    ('med_rabies_vaccine', 'pregnancy', 6, '', 'Pregnancy and infancy are not contraindications to PVRV or PCECV; none in breast-feeding (MSF).', 'DOH AO 2018'),
    ('med_rabies_vaccine', 'monitor', 7, '', 'Anaphylaxis: epinephrine 0.1% 0.5 mL (adults) or 0.01 mL/kg, max 0.5 mL (children), repeat every 10–20 min up to 3 doses; then steroids. Record and report severe adverse events.', 'DOH AO 2018'),
    ('med_rabies_vaccine', 'monitor', 8, '', 'Routine boosters or neutralizing-antibody serology after PrEP only if exposure risk remains high.', 'WHO 2018')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_rabies_vaccine');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_rabies_vaccine', 'DOH AO 2018', 'DOH Administrative Order 2018-0013', 'Department of Health (Philippines). AO No. 2018-0013: Revised Guidelines on the Management of Rabies Exposures. 2018.', 'https://legaldex.com/laws/revised-guidelines-on-the-management-of-rabies-exposures', 0),
    ('med_rabies_vaccine', 'WHO 2018', 'WHO position paper (summary)', 'World Health Organization. Rabies vaccines and immunoglobulins: WHO position, April 2018 (summary).', 'https://cdn.who.int/media/docs/default-source/immunization/position_paper_documents/rabies/pp-rabies-summary-2018.pdf', 1),
    ('med_rabies_vaccine', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Rabies vaccine.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/rabies-vaccine-16687811.html', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_rabies_vaccine')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_rabies_vaccine');


-- ================================================ med_rifampicin  (Rifampicin)
update public.medicines set description = 'Rifampicin inhibits bacterial DNA-dependent RNA polymerase, blocking transcription, and is bactericidal against Mycobacterium tuberculosis. It is a cornerstone of first-line TB therapy (with isoniazid, pyrazinamide and ethambutol) and is a potent inducer of CYP3A4 and other drug-metabolizing enzymes, causing many drug interactions. In the Philippine NTP it is given throughout treatment in fixed-dose combinations (HRZE in the intensive phase, HR in the continuation phase of Category I 2HRZE/4HR; HRZE then HRE in Category II), with the number of tablets set by body-weight band. Single-drug rifampicin (including a 200 mg/5 mL suspension) is used for weight-based dosing in children who cannot take tablets.', updated_at = now()
where id = 'med_rifampicin' and description = 'Rifampicin inhibits bacterial DNA-dependent RNA polymerase, blocking transcription, and is bactericidal against Mycobacterium tuberculosis. It is a cornerstone of first-line TB therapy (with isoniazid, pyrazinamide and ethambutol) and is a potent inducer of CYP3A4 and other drug-metabolizing enzymes, causing many drug interactions.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine NTP Manual of Procedures; Philippine National Formulary (PNF) EML; MSF Tuberculosis guideline; MSF Essential Drugs; UK SmPC (emc)' else source_attribution || '; Philippine NTP Manual of Procedures; Philippine National Formulary (PNF) EML; MSF Tuberculosis guideline; MSF Essential Drugs; UK SmPC (emc)' end
where id = 'med_rifampicin' and position('Philippine NTP Manual of Procedures' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'indication', 'Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'indication' and content = 'Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'indication', 'Brucellosis, Legionnaires'' disease and serious staphylococcal infections, with another antibiotic', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'indication' and content = 'Brucellosis, Legionnaires'' disease and serious staphylococcal infections, with another antibiotic');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'indication', 'Chemoprophylaxis of Haemophilus influenzae: carriers and exposed children aged 4 years or younger', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'indication' and content = 'Chemoprophylaxis of Haemophilus influenzae: carriers and exposed children aged 4 years or younger');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'adverse', 'Fever and chills (very common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse' and content = 'Fever and chills (very common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'adverse', 'Paradoxical reaction: TB symptoms recur after initial improvement, usually without treatment failure', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse' and content = 'Paradoxical reaction: TB symptoms recur after initial improvement, usually without treatment failure');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'adverse', 'Thrombotic microangiopathy (TTP/HUS); stop if suspected', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse' and content = 'Thrombotic microangiopathy (TTP/HUS); stop if suspected');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'adverse', 'Interstitial lung disease / pneumonitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse' and content = 'Interstitial lung disease / pneumonitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'adverse', 'Adrenal insufficiency in patients with compromised adrenal function', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse' and content = 'Adrenal insufficiency in patients with compromised adrenal function');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'adverse', 'Tooth discolouration (may be permanent)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse' and content = 'Tooth discolouration (may be permanent)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'adverse', 'Headache and drowsiness', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'adverse' and content = 'Headache and drowsiness');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'contraindication', 'Jaundice', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'contraindication' and content = 'Jaundice');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'contraindication', 'History of severe haematological disorders (thrombocytopenia, purpura) during previous rifamycin treatment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'contraindication' and content = 'History of severe haematological disorders (thrombocytopenia, purpura) during previous rifamycin treatment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'contraindication', 'Concomitant sofosbuvir, daclatasvir or telaprevir', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'contraindication' and content = 'Concomitant sofosbuvir, daclatasvir or telaprevir');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'interaction', 'Dolutegravir: levels fall substantially; dolutegravir is given 50 mg twice daily with rifampicin.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction' and content = 'Dolutegravir: levels fall substantially; dolutegravir is given 50 mg twice daily with rifampicin.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'interaction', 'Nevirapine, lopinavir/ritonavir or atazanavir/ritonavir: use rifabutin instead of rifampicin (MSF).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction' and content = 'Nevirapine, lopinavir/ritonavir or atazanavir/ritonavir: use rifabutin instead of rifampicin (MSF).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'interaction', 'Fluconazole: give 12 hours apart (rifampicin in the morning, fluconazole in the evening).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction' and content = 'Fluconazole: give 12 hours apart (rifampicin in the morning, fluconazole in the evening).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'interaction', 'Antacids: take rifampicin at least 1 hour before the antacid.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction' and content = 'Antacids: take rifampicin at least 1 hour before the antacid.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'interaction', 'Para-aminosalicylic acid: give at least 8 hours apart.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction' and content = 'Para-aminosalicylic acid: give at least 8 hours apart.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'interaction', 'Cefazolin and other cephalosporins with an NMTT side chain: avoid (risk of severe coagulation disorders).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction' and content = 'Cefazolin and other cephalosporins with an NMTT side chain: avoid (risk of severe coagulation disorders).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'interaction', 'Paracetamol: may increase hepatotoxicity risk.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction' and content = 'Paracetamol: may increase hepatotoxicity risk.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'interaction', 'Clopidogrel: concomitant use is discouraged; halothane: avoid.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction' and content = 'Clopidogrel: concomitant use is discouraged; halothane: avoid.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_rifampicin', 'interaction', 'Phenytoin and hepatitis C direct-acting antivirals: reduced effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_rifampicin' and kind = 'interaction' and content = 'Phenytoin and hepatitis C direct-acting antivirals: reduced effect.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rifampicin', 'Philippine NTP Manual of Procedures', 'Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.', 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rifampicin'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rifampicin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rifampicin', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rifampicin'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rifampicin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rifampicin', 'MSF Tuberculosis guideline', 'Médecins Sans Frontières. Tuberculosis - Appendix 10, TB drug information sheets: Rifampicin (R). Updated January 2022.', 'https://medicalguidelines.msf.org/en/viewport/TUB/english/rifampicin-r-20323858.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rifampicin'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rifampicin' and url = 'https://medicalguidelines.msf.org/en/viewport/TUB/english/rifampicin-r-20323858.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rifampicin', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs - practical guidelines: Rifampicin (R) oral. Updated June 2021.', 'https://medicalguidelines.msf.org/en/node/570', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rifampicin'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rifampicin' and url = 'https://medicalguidelines.msf.org/en/node/570');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_rifampicin', 'UK SmPC (emc)', 'Rifadin 300 mg Capsules - Summary of Product Characteristics. Aventis Pharma Ltd (Sanofi). Electronic medicines compendium (emc), updated June 2026.', 'https://products.mhra.gov.uk/search/?search=rifampicin#emc-6384', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_rifampicin'), 0)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_rifampicin' and url = 'https://products.mhra.gov.uk/search/?search=rifampicin#emc-6384');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hepatitis_b', 'med_rifampicin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hepatitis_b'), 0), 'caution'::condition_safety, 'Hepatic impairment: do not exceed 8 mg/kg/day and monitor LFTs closely; contraindicated with jaundice (UK SmPC, MSF). Applying this to hepatitis B is an inference.'
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hepatitis_b' and medicine_id = 'med_rifampicin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_rifampicin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Rifampicin reduces the effect of antidiabetic drugs; doses may need adjusting (MSF).'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_rifampicin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_rifampicin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'No adjustment up to 600 mg/day; caution if the dose exceeds 600 mg/day (UK SmPC).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_rifampicin');
-- med_rifampicin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_rifampicin', 'adult', 0, 'TB Cat I (2HRZE/4HR), 30–37 kg', 'PO', '2 tablets HRZE, then 2 tablets HR', 'Once a day', '2 + 4 months', '—', 'NTP MOP 2014', 'Cat Ia (CNS, bones, joints): HR for 10 months'),
    ('med_rifampicin', 'adult', 1, 'TB Cat I (2HRZE/4HR), 38–54 kg', 'PO', '3 tablets HRZE, then 3 tablets HR', 'Once a day', '2 + 4 months', '—', 'NTP MOP 2014', ''),
    ('med_rifampicin', 'adult', 2, 'TB Cat I (2HRZE/4HR), 55–70 kg', 'PO', '4 tablets HRZE, then 4 tablets HR', 'Once a day', '2 + 4 months', '—', 'NTP MOP 2014', ''),
    ('med_rifampicin', 'adult', 3, 'TB Cat I (2HRZE/4HR), >70 kg', 'PO', '5 tablets HRZE, then 5 tablets HR', 'Once a day', '2 + 4 months', '—', 'NTP MOP 2014', 'Each tablet contains rifampicin 150 mg'),
    ('med_rifampicin', 'adult', 4, 'TB, single-drug formulation', 'PO', '10 mg/kg (range 8–12)', 'Once a day', 'Per regimen', '600 mg/day', 'NTP MOP 2014', 'Usually 450 mg if <50 kg, 600 mg if ≥50 kg (UK SmPC)'),
    ('med_rifampicin', 'adult', 5, 'TB meningitis (6HRZEto)', 'PO', '20 mg/kg', 'Once a day', '6 months', '600 mg/day', 'MSF TB', ''),
    ('med_rifampicin', 'adult', 6, 'Latent TB infection', 'PO', '10 mg/kg', 'Once a day', '4 months alone; 3 months with isoniazid', '600 mg/day', 'MSF', ''),
    ('med_rifampicin', 'adult', 7, 'Leprosy', 'PO', '600 mg', 'Once a month', '6 months (PB); 12 months (MB)', '—', 'MSF', 'With dapsone and clofazimine'),
    ('med_rifampicin', 'adult', 8, 'Brucellosis, Legionnaires'', serious staphylococcal infection', 'PO', '600–1200 mg/day ÷ 2–4', '2–4× a day', 'Brucellosis: 6 weeks', '1200 mg/day', 'Label · UK SmPC', 'Always with another antibiotic'),
    ('med_rifampicin', 'adult', 9, 'Meningococcal carrier eradication', 'PO', '600 mg', '2× a day', '2 days', '—', 'Label · UK SmPC', ''),
    ('med_rifampicin', 'child', 10, 'TB, single-drug formulation', 'PO', '15 mg/kg (range 10–20)', 'Once a day', 'Per regimen', '600 mg/day', 'NTP MOP 2014', 'Suspension 200 mg/5 mL dosed by weight (Table 14); newborn <4 weeks: refer'),
    ('med_rifampicin', 'child', 11, 'TB meningitis (6HRZEto)', 'PO', '20 mg/kg', 'Once a day', '6 months', '600 mg/day', 'MSF TB', ''),
    ('med_rifampicin', 'child', 12, 'Leprosy, <10 y / 10–14 y', 'PO', '10 mg/kg / 450 mg', 'Once a month', '6 months (PB); 12 months (MB)', '—', 'MSF', ''),
    ('med_rifampicin', 'child', 13, 'Meningococcal carriers, 1–12 y', 'PO', '10 mg/kg', '2× a day', '2 days', '—', 'Label · UK SmPC', 'Infants 3–12 months: 5 mg/kg'),
    ('med_rifampicin', 'child', 14, 'H. influenzae chemoprophylaxis', 'PO', '20 mg/kg', 'Once a day', '4 days', '600 mg/day', 'Label · UK SmPC', 'Neonates (1 month): 10 mg/kg')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_rifampicin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_rifampicin', 'hepatic', 0, '', 'Do not exceed 8 mg/kg/day. Contraindicated in jaundice. Monitor ALT/AST weekly for 2 weeks, then every 2 weeks for the next 6 weeks; stop if hepatocellular damage occurs.', 'Label · UK SmPC'),
    ('med_rifampicin', 'renal', 1, '', 'No adjustment up to 600 mg/day; use caution if the dose exceeds 600 mg/day.', 'Label · UK SmPC'),
    ('med_rifampicin', 'elderly', 2, '', 'Use with caution, especially if liver function is impaired.', 'Label · UK SmPC'),
    ('med_rifampicin', 'pregnancy', 3, '', 'Not contraindicated. Given in the last weeks of pregnancy it can cause bleeding in mother and newborn: give vitamin K (phytomenadione) to both. Not contraindicated in breastfeeding (MSF); passes into breast milk (UK SmPC).', 'MSF'),
    ('med_rifampicin', 'administration', 4, '', 'Take on an empty stomach, at least 30 minutes before or 2 hours after a meal; a small amount of food may be used to improve GI tolerance (MSF). Take at least 1 hour before antacids.', 'Label · UK SmPC'),
    ('med_rifampicin', 'administration', 5, '', 'Advise women on hormonal contraception to switch to injectable medroxyprogesterone or an IUD.', 'MSF'),
    ('med_rifampicin', 'forms_ph', 6, '', 'Only in fixed-dose combinations (List B): isoniazid + rifampicin 50/75 mg dispersible tablet (pediatric) and 75/150 mg tablet; isoniazid + rifampicin + ethambutol 75/150/275 mg; isoniazid + rifampicin + pyrazinamide 50/75/150 mg dispersible; isoniazid + rifampicin + pyrazinamide + ethambutol 75/150/400/275 mg. A single-ingredient rifampicin entry could not be read in the PNF text (it stops at ''M'').', 'PNF'),
    ('med_rifampicin', 'monitor', 7, '', 'Baseline LFTs, blood count and renal function in adults with TB. Stop if purpura, thrombocytopenia or signs of TMA appear.', 'Label · UK SmPC'),
    ('med_rifampicin', 'monitor', 8, '', 'Dosing less often than 2–3 times a week raises the risk of immune reactions (flu-like syndrome, anaphylaxis); monitor closely.', 'Label · UK SmPC'),
    ('med_rifampicin', 'monitor', 9, '', 'Reassure about orange-red urine and secretions; soft contact lenses can be permanently stained.', 'NTP MOP 2014')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_rifampicin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_rifampicin', 'NTP MOP 2014', 'Philippine NTP Manual of Procedures', 'DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 11–15).', 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf', 0),
    ('med_rifampicin', 'PNF', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 1),
    ('med_rifampicin', 'MSF TB', 'MSF Tuberculosis guideline', 'MSF Tuberculosis, Appendix 10: Rifampicin (R), 2022.', 'https://medicalguidelines.msf.org/en/viewport/TUB/english/rifampicin-r-20323858.html', 2),
    ('med_rifampicin', 'MSF', 'MSF Essential Drugs', 'MSF Essential drugs: Rifampicin (R) oral, 2021.', 'https://medicalguidelines.msf.org/en/node/570', 3),
    ('med_rifampicin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Rifadin 300 mg Capsules - SmPC. Sanofi, 2026.', 'https://products.mhra.gov.uk/search/?search=rifampicin#emc-6384', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_rifampicin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_rifampicin');


-- ================================================ med_salbutamol  (Salbutamol (Albuterol))
update public.medicines set description = 'Salbutamol stimulates beta-2 adrenergic receptors on bronchial smooth muscle, activating adenylyl cyclase and relaxing the airways within minutes, with effects lasting 4-6 hours. It also inhibits mediator release from mast cells. It is used for relief and prevention of bronchospasm in asthma, COPD and exercise-induced bronchoconstriction. For most asthma attacks a metered-dose inhaler with a spacer is easier, faster, at least as effective and better tolerated than a nebuliser, so nebulised salbutamol (with ipratropium) is reserved for severe attacks. In the Philippines, salbutamol is among the medicines of the PhilHealth Konsulta primary-care package as a metered-dose inhaler, dry powder inhaler, nebulising solution and syrup.', updated_at = now()
where id = 'med_salbutamol' and description = 'Salbutamol stimulates beta-2 adrenergic receptors on bronchial smooth muscle, activating adenylyl cyclase and relaxing the airways within minutes, with effects lasting 4-6 hours. It also inhibits mediator release from mast cells. It is used for relief and prevention of bronchospasm in asthma, COPD and exercise-induced bronchoconstriction.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (Ventolin Evohaler); UK SmPC (nebuliser solution); MSF Essential Drugs; PhilHealth Konsulta; MSF Essential Drugs (MDI); MSF Essential Drugs (nebuliser); PhilHealth Konsulta medicines list' else source_attribution || '; UK SmPC (Ventolin Evohaler); UK SmPC (nebuliser solution); MSF Essential Drugs; PhilHealth Konsulta; MSF Essential Drugs (MDI); MSF Essential Drugs (nebuliser); PhilHealth Konsulta medicines list' end
where id = 'med_salbutamol' and position('UK SmPC (Ventolin Evohaler)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'indication', 'Severe acute asthma attack: nebulised, combined with ipratropium (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'indication' and content = 'Severe acute asthma attack: nebulised, combined with ipratropium (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'adverse', 'Muscle cramps; mouth and throat irritation', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse' and content = 'Muscle cramps; mouth and throat irritation');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'adverse', 'Peripheral vasodilatation', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse' and content = 'Peripheral vasodilatation');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'adverse', 'Lactic acidosis with high-dose (e.g. nebulised) therapy', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse' and content = 'Lactic acidosis with high-dose (e.g. nebulised) therapy');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'adverse', 'Myocardial ischaemia (post-marketing, frequency unknown)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse' and content = 'Myocardial ischaemia (post-marketing, frequency unknown)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'adverse', 'Hypersensitivity: angioedema, urticaria, hypotension and collapse (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'adverse' and content = 'Hypersensitivity: angioedema, urticaria, hypotension and collapse (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'contraindication', 'Non-IV forms must not be used to stop uncomplicated premature labour or threatened abortion', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'contraindication' and content = 'Non-IV forms must not be used to stop uncomplicated premature labour or threatened abortion');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'contraindication', 'Nebuliser solution must never be given parenterally', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'contraindication' and content = 'Nebuliser solution must never be given parenterally');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'interaction', 'Xanthine derivatives and corticosteroids: may potentiate beta-2-agonist hypokalaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'interaction' and content = 'Xanthine derivatives and corticosteroids: may potentiate beta-2-agonist hypokalaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_salbutamol', 'interaction', 'Nebulised ipratropium: acute angle-closure glaucoma reported with the combination; keep the mist out of the eyes.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_salbutamol' and kind = 'interaction' and content = 'Nebulised ipratropium: acute angle-closure glaucoma reported with the combination; keep the mist out of the eyes.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_salbutamol', 'UK SmPC (Ventolin Evohaler)', 'Ventolin Evohaler 100 micrograms. Summary of Product Characteristics. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=salbutamol#emc-850', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_salbutamol'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_salbutamol' and url = 'https://products.mhra.gov.uk/search/?search=salbutamol#emc-850');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_salbutamol', 'UK SmPC (nebuliser solution)', 'Salbutamol 1 mg/ml nebuliser solution (Cipla EU Ltd). Summary of Product Characteristics. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=salbutamol#emc-10256', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_salbutamol'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_salbutamol' and url = 'https://products.mhra.gov.uk/search/?search=salbutamol#emc-10256');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_salbutamol', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Salbutamol metered dose inhaler; Salbutamol nebuliser solution. MSF Medical Guidelines (updated June 2023).', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-aerosol-16684638.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_salbutamol'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_salbutamol' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-aerosol-16684638.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_salbutamol', 'PhilHealth Konsulta', 'Philippine Health Insurance Corporation. Certification of Service Delivery Support (Medicines), Annex D2 – Konsulta Package accreditation.', 'https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_salbutamol'), 0)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_salbutamol' and url = 'https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_salbutamol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Beta-2 agonists can raise blood glucose; the SmPC advises caution in diabetes.'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_salbutamol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_coronary_syndrome', 'med_salbutamol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome'), 0), 'caution'::condition_safety, 'Rare myocardial ischaemia reported; the SmPC advises patients with severe heart disease to seek advice for chest pain or worsening symptoms.'
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome' and medicine_id = 'med_salbutamol');
-- med_salbutamol
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_salbutamol', 'adult', 0, 'Acute bronchospasm (reliever)', 'Inhaled', '100–200 micrograms (1–2 puffs)', 'As needed', '—', '8 puffs/24 h', 'Label · UK SmPC', 'MDI 100 micrograms/puff'),
    ('med_salbutamol', 'adult', 1, 'Exercise or allergen prevention', 'Inhaled', '200 micrograms (2 puffs)', '10–15 min before challenge', '—', '8 puffs/24 h', 'Label · UK SmPC', ''),
    ('med_salbutamol', 'adult', 2, 'Chronic therapy', 'Inhaled', '200 micrograms (2 puffs)', 'Up to 4× a day', '—', '8 puffs/24 h', 'Label · UK SmPC', ''),
    ('med_salbutamol', 'adult', 3, 'Asthma attack, first hour', 'Inhaled', '200–1000 micrograms (2–10 puffs)', 'Every 20 min', '1 h', '—', 'MSF', 'Then 2–4 puffs every 4–6 h for 24–48 h; spacer advised'),
    ('med_salbutamol', 'adult', 4, 'Severe asthma attack', 'Inhaled', '5 mg nebulised', 'Every 20 min', 'First hour, then taper', '—', 'MSF neb', 'With ipratropium; switch to MDI as symptoms improve'),
    ('med_salbutamol', 'adult', 5, 'Bronchospasm (nebuliser)', 'Inhaled', '2.5–5 mg nebulised', 'Up to 4× a day', '—', '40 mg/day (hospital only)', 'Label · UK SmPC neb', 'Includes elderly and ≥ 12 y'),
    ('med_salbutamol', 'child', 6, 'Acute bronchospasm, < 12 y', 'Inhaled', '100 micrograms (1 puff)', 'As needed', '—', '8 puffs/24 h', 'Label · UK SmPC', 'May increase to 2 puffs; licensed from 4 y'),
    ('med_salbutamol', 'child', 7, 'Asthma attack, first hour', 'Inhaled', '200–1000 micrograms (2–10 puffs)', 'Every 20 min', '1 h', '—', 'MSF', 'Same as adult; use a spacer (< 6 y)'),
    ('med_salbutamol', 'child', 8, 'Severe asthma attack, < 5 y', 'Inhaled', '2.5 mg nebulised', 'Every 20 min', 'First hour, then taper', '—', 'MSF neb', 'With ipratropium'),
    ('med_salbutamol', 'child', 9, 'Severe asthma attack, 5–11 y', 'Inhaled', '2.5–5 mg nebulised', 'Every 20 min', 'First hour, then taper', '—', 'MSF neb', 'With ipratropium'),
    ('med_salbutamol', 'child', 10, 'Bronchospasm (nebuliser), 4–11 y', 'Inhaled', '2.5–5 mg nebulised', 'Up to 4× a day', '—', '—', 'Label · UK SmPC neb', '< 18 months: efficacy uncertain; transient hypoxia, consider oxygen')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_salbutamol');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_salbutamol', 'forms_ph', 0, '', 'MDI 100 micrograms/dose × 200 actuations (also breath-actuated MDI); DPI 200 micrograms/dose; nebulising solution 1 mg/mL and 2 mg/mL, 2.5 mL unit dose; syrup 2 mg/5 mL, 60 mL. Combination ipratropium + salbutamol MDI and nebule.', 'PhilHealth'),
    ('med_salbutamol', 'administration', 1, '', 'Nebuliser: dilute with 0.9% sodium chloride to 4 mL total; stop when the reservoir is empty (about 10–15 min).', 'MSF neb'),
    ('med_salbutamol', 'administration', 2, '', 'Use a spacer for children under 6, older patients and severe dyspnoea; clean the mouthpiece before and after use.', 'MSF'),
    ('med_salbutamol', 'renal', 3, '', 'No renal dose adjustment is given in the SmPC; salbutamol is cleared partly renally.', 'Label · UK SmPC neb'),
    ('med_salbutamol', 'elderly', 4, '', 'Adult dose applies, including the elderly.', 'Label · UK SmPC neb'),
    ('med_salbutamol', 'pregnancy', 5, '', 'SmPC: use only if clearly necessary; avoid in breast-feeding unless benefit outweighs risk. MSF lists no contraindication in pregnancy or breast-feeding.', 'Label · UK SmPC'),
    ('med_salbutamol', 'monitor', 6, '', 'Serum potassium in acute severe asthma; check for lactic acidosis if tachypnoea persists after wheeze resolves.', 'Label · UK SmPC'),
    ('med_salbutamol', 'monitor', 7, '', 'Blood glucose in diabetes; review control if reliever is used more than twice a week or a dose gives no relief for 3 h; check inhaler technique.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_salbutamol');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_salbutamol', 'Label · UK SmPC', 'UK SmPC (Ventolin Evohaler)', 'Ventolin Evohaler 100 micrograms. Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=salbutamol#emc-850', 0),
    ('med_salbutamol', 'Label · UK SmPC neb', 'UK SmPC (nebuliser solution)', 'Salbutamol 1 mg/ml nebuliser solution (Cipla EU Ltd). Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=salbutamol#emc-10256', 1),
    ('med_salbutamol', 'MSF', 'MSF Essential Drugs (MDI)', 'Médecins Sans Frontières. Essential drugs – Salbutamol metered dose inhaler.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-aerosol-16684638.html', 2),
    ('med_salbutamol', 'MSF neb', 'MSF Essential Drugs (nebuliser)', 'Médecins Sans Frontières. Essential drugs – Salbutamol nebuliser solution.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/salbutamol-albuterol-nebuliser-solution-16684649.html', 3),
    ('med_salbutamol', 'PhilHealth', 'PhilHealth Konsulta medicines list', 'PhilHealth. Certification of Service Delivery Support (Medicines), Annex D2 – Konsulta Package.', 'https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_salbutamol')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_salbutamol');


-- ================================================ med_spironolactone  (Spironolactone)
update public.medicines set description = 'Spironolactone competitively blocks the mineralocorticoid (aldosterone) receptor in the distal nephron, increasing sodium and water excretion while retaining potassium. It also has anti-androgenic activity. It reduces mortality in heart failure with reduced ejection fraction and is used for resistant hypertension, primary hyperaldosteronism and edema from cirrhosis or nephrotic syndrome. The 2023 Philippine clinical practice guidelines on chronic heart failure with reduced ejection fraction for primary care strongly recommend a mineralocorticoid receptor antagonist on top of standard care when eGFR is above 30 mL/min/1.73 m² and serum potassium is below 5 mEq/L; spironolactone is the only one of these drugs included in the Philippine National Formulary. It is also used in malignant ascites and as a diagnostic test for primary aldosteronism.', updated_at = now()
where id = 'med_spironolactone' and description = 'Spironolactone competitively blocks the mineralocorticoid (aldosterone) receptor in the distal nephron, increasing sodium and water excretion while retaining potassium. It also has anti-androgenic activity. It reduces mortality in heart failure with reduced ejection fraction and is used for resistant hypertension, primary hyperaldosteronism and edema from cirrhosis or nephrotic syndrome.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine Journal of Cardiology; UK SmPC (emc); DailyMed (FDA label)' else source_attribution || '; Philippine Journal of Cardiology; UK SmPC (emc); DailyMed (FDA label)' end
where id = 'med_spironolactone' and position('Philippine Journal of Cardiology' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'indication', 'Malignant ascites', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'indication' and content = 'Malignant ascites');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'indication', 'Diagnosis of primary aldosteronism (400 mg/day test) and pre-operative preparation', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'indication' and content = 'Diagnosis of primary aldosteronism (400 mg/day test) and pre-operative preparation');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'adverse', 'Confusion, dizziness, muscle spasms and malaise', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse' and content = 'Confusion, dizziness, muscle spasms and malaise');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'adverse', 'Acute kidney injury; reversible rise in blood urea', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse' and content = 'Acute kidney injury; reversible rise in blood urea');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'adverse', 'Pruritus, rash, urticaria', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse' and content = 'Pruritus, rash, urticaria');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'adverse', 'Agranulocytosis, leukopenia, thrombocytopenia (frequency not known)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse' and content = 'Agranulocytosis, leukopenia, thrombocytopenia (frequency not known)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'adverse', 'Toxic epidermal necrolysis, DRESS, pemphigoid (frequency not known)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse' and content = 'Toxic epidermal necrolysis, DRESS, pemphigoid (frequency not known)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'adverse', 'Hypomagnesemia, hypocalcemia, hyperglycemia and hyperuricemia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse' and content = 'Hypomagnesemia, hypocalcemia, hyperglycemia and hyperuricemia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'adverse', 'Hyperchloraemic metabolic acidosis in decompensated cirrhosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse' and content = 'Hyperchloraemic metabolic acidosis in decompensated cirrhosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'adverse', 'Worsening hepatic encephalopathy in cirrhosis with ascites', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'adverse' and content = 'Worsening hepatic encephalopathy in cirrhosis with ascites');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'contraindication', 'Anuria or acute renal insufficiency', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'contraindication' and content = 'Anuria or acute renal insufficiency');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'contraindication', 'Other potassium-sparing diuretics (amiloride, triamterene) or routine potassium supplements', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'contraindication' and content = 'Other potassium-sparing diuretics (amiloride, triamterene) or routine potassium supplements');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'contraindication', 'Children with moderate to severe renal impairment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'contraindication' and content = 'Children with moderate to severe renal impairment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'contraindication', 'Hypersensitivity to spironolactone', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'contraindication' and content = 'Hypersensitivity to spironolactone');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'interaction', 'Co-trimoxazole and low molecular weight heparin: clinically relevant hyperkalaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction' and content = 'Co-trimoxazole and low molecular weight heparin: clinically relevant hyperkalaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'interaction', 'Potassium-containing salt substitutes or potassium-rich diet: hyperkalaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction' and content = 'Potassium-containing salt substitutes or potassium-rich diet: hyperkalaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'interaction', 'Digoxin: raised digoxin level and half-life; may interfere with digoxin assays.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction' and content = 'Digoxin: raised digoxin level and half-life; may interfere with digoxin assays.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'interaction', 'Other antihypertensives: additive blood pressure lowering; dose may need reducing.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction' and content = 'Other antihypertensives: additive blood pressure lowering; dose may need reducing.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'interaction', 'Carbenoxolone: sodium retention reduces the effect of spironolactone; avoid.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction' and content = 'Carbenoxolone: sodium retention reduces the effect of spironolactone; avoid.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_spironolactone', 'interaction', 'Anaesthesia: reduced vascular response to noradrenaline.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_spironolactone' and kind = 'interaction' and content = 'Anaesthesia: reduced vascular response to noradrenaline.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_spironolactone', 'Philippine Journal of Cardiology', 'Abola MTB, Punzalan FER, Magno JDA, et al. 2023 Philippine Clinical Practice Guidelines on the Diagnosis and Management of Chronic Heart Failure with Reduced Ejection Fraction for Primary Care Physicians. Philipp J Cardiol. 2025;53(2).', 'https://pjc.philheart.org/elib/journal/identifier/pjc.2025.0712.012034/full', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_spironolactone'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_spironolactone' and url = 'https://pjc.philheart.org/elib/journal/identifier/pjc.2025.0712.012034/full');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_spironolactone', 'UK SmPC (emc)', 'Spironolactone 12.5 mg film-coated tablets. Summary of Product Characteristics. Mercury Pharmaceuticals Ltd; revised 14 October 2025. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=spironolactone#emc-12015', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_spironolactone'), 0)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_spironolactone' and url = 'https://products.mhra.gov.uk/search/?search=spironolactone#emc-12015');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_spironolactone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Contraindicated in anuria, acute renal insufficiency or significant renal compromise; higher hyperkalaemia risk in renal impairment. In heart failure with eGFR 30–50, start 25 mg every other day (US label); PH HF guideline recommends MRA only if eGFR >30.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_spironolactone');
-- med_spironolactone
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_spironolactone', 'adult', 0, 'Heart failure (HFrEF)', 'PO', '25 mg', 'Once a day', 'Long-term', '50 mg/day', 'Label · US', 'Start if K ≤5.0 mEq/L and eGFR >50; if hyperkalaemia, 25 mg every other day'),
    ('med_spironolactone', 'adult', 1, 'Heart failure, eGFR 30–50', 'PO', '25 mg', 'Every other day', 'Long-term', '—', 'Label · US', ''),
    ('med_spironolactone', 'adult', 2, 'Hypertension', 'PO', '25–100 mg', 'Once a day or divided', 'Long-term', '—', 'Label · US', 'Titrate every 2 weeks; >100 mg/day usually adds no BP lowering'),
    ('med_spironolactone', 'adult', 3, 'Edema (heart failure, nephrotic syndrome)', 'PO', '100 mg', 'Once a day or divided', '—', '200 mg/day', 'Label · US', 'Range 25–200 mg; give ≥5 days before increasing'),
    ('med_spironolactone', 'adult', 4, 'Cirrhosis with ascites', 'PO', '100 mg (urine Na/K >1); 200–400 mg (Na/K <1)', 'Once a day or divided', '—', '400 mg/day', 'Label · UK SmPC', 'Start in hospital, titrate slowly'),
    ('med_spironolactone', 'adult', 5, 'Malignant ascites', 'PO', '100–200 mg', 'Once a day or divided', '—', '400 mg/day', 'Label · UK SmPC', ''),
    ('med_spironolactone', 'adult', 6, 'Primary aldosteronism (diagnostic test)', 'PO', '400 mg', 'Once a day or divided', '3–4 weeks (long) or 4 days (short)', '—', 'Label · UK SmPC', ''),
    ('med_spironolactone', 'adult', 7, 'Primary aldosteronism (before surgery)', 'PO', '100–400 mg', 'Once a day or divided', 'Until surgery', '400 mg/day', 'Label · US', 'If unfit for surgery: lowest effective dose'),
    ('med_spironolactone', 'child', 8, 'Edema / specialist use', 'PO', '1–3 mg/kg/day ÷ doses', 'Divided doses', '—', '—', 'Label · UK SmPC', 'Only under a paediatric specialist')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_spironolactone');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_spironolactone', 'renal', 0, '', 'Contraindicated in anuria, acute renal insufficiency or significant renal compromise.', 'Label · UK SmPC'),
    ('med_spironolactone', 'renal', 1, 'eGFR 30–50', 'Consider starting at 25 mg every other day in heart failure.', 'Label · US'),
    ('med_spironolactone', 'renal', 2, 'eGFR >30', 'Philippine HF guideline recommends an MRA only when eGFR is above 30 mL/min/1.73 m² and potassium is below 5 mEq/L.', 'PH CPG 2023'),
    ('med_spironolactone', 'hepatic', 3, '', 'Cirrhosis: start in hospital at the lowest dose and titrate slowly; rapid fluid and electrolyte shifts can precipitate hepatic encephalopathy or coma.', 'Label · US'),
    ('med_spironolactone', 'elderly', 4, '', 'Start at the lowest dose and titrate; monitor renal function and electrolytes, as reduced renal function is more common.', 'Label · UK SmPC'),
    ('med_spironolactone', 'pregnancy', 5, '', 'Feminisation of male fetuses in animal studies; avoid in pregnancy or advise of the risk to a male fetus. Canrenone appears in milk in small amounts; UK labeling advises alternative infant feeding if use is essential.', 'Label · US'),
    ('med_spironolactone', 'administration', 6, '', 'Take consistently with respect to food (UK labeling suggests once daily with a meal).', 'Label · US'),
    ('med_spironolactone', 'monitor', 7, '', 'Heart failure: check potassium and creatinine at 1 week after starting or increasing the dose, monthly for 3 months, every 3 months for a year, then every 6 months. Stop or interrupt if K >5 mEq/L or creatinine >4 mg/dL.', 'Label · UK SmPC'),
    ('med_spironolactone', 'monitor', 8, '', 'Check sodium, magnesium, calcium, uric acid, glucose, volume status and blood pressure; ask men about breast swelling or pain.', 'Label · US')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_spironolactone');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_spironolactone', 'Label · US', 'DailyMed (FDA label)', 'ALDACTONE (spironolactone) tablets. Prescribing information. Pfizer; revised 11/2025. DailyMed, U.S. National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0fed2822-3a03-4b64-9857-c682fcd462bc', 0),
    ('med_spironolactone', 'Label · UK SmPC', 'UK SmPC (emc)', 'Spironolactone 12.5 mg film-coated tablets. Summary of Product Characteristics. Mercury Pharmaceuticals Ltd; revised 14 October 2025.', 'https://products.mhra.gov.uk/search/?search=spironolactone#emc-12015', 1),
    ('med_spironolactone', 'PH CPG 2023', 'Philippine Journal of Cardiology', 'Abola MTB, et al. 2023 Philippine CPG on chronic HFrEF for primary care physicians. Philipp J Cardiol. 2025;53(2).', 'https://pjc.philheart.org/elib/journal/identifier/pjc.2025.0712.012034/full', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_spironolactone')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_spironolactone');


-- ================================================ med_sumatriptan  (Sumatriptan)
update public.medicines set description = 'Sumatriptan is a selective serotonin 5-HT1B/1D receptor agonist that constricts dilated cranial blood vessels and inhibits release of vasoactive neuropeptides and pain transmission in the trigeminal system. It is an abortive (acute) treatment and does not prevent migraine attacks. It is used for acute migraine with or without aura and, subcutaneously, for cluster headache. Sumatriptan is also given as a nasal spray, which UK labeling allows for adolescents aged 12–17 under specialist advice. In a 2022 survey of Filipino neurologists, NSAIDs were the most preferred acute migraine drugs and about half would not consider a triptan even for moderate to severe episodic attacks, so triptans remain little used in the Philippines.', updated_at = now()
where id = 'med_sumatriptan' and description = 'Sumatriptan is a selective serotonin 5-HT1B/1D receptor agonist that constricts dilated cranial blood vessels and inhibits release of vasoactive neuropeptides and pain transmission in the trigeminal system. It is an abortive (acute) treatment and does not prevent migraine attacks. It is used for acute migraine with or without aura and, subcutaneously, for cluster headache.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); Neurology Asia' else source_attribution || '; UK SmPC (emc); Neurology Asia' end
where id = 'med_sumatriptan' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'indication', 'Acute migraine in adolescents 12–17 years (nasal spray, specialist recommendation; UK labeling)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'indication' and content = 'Acute migraine in adolescents 12–17 years (nasal spray, specialist recommendation; UK labeling)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'adverse', 'Flushing, dyspnoea, nausea and vomiting', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse' and content = 'Flushing, dyspnoea, nausea and vomiting');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'adverse', 'Transient rise in blood pressure; hypotension, bradycardia or tachycardia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse' and content = 'Transient rise in blood pressure; hypotension, bradycardia or tachycardia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'adverse', 'Visual disturbance (flickering, diplopia, scotoma, reduced vision)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse' and content = 'Visual disturbance (flickering, diplopia, scotoma, reduced vision)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'adverse', 'Tremor, dystonia, nystagmus', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse' and content = 'Tremor, dystonia, nystagmus');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'adverse', 'Raynaud''s phenomenon and ischaemic colitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse' and content = 'Raynaud''s phenomenon and ischaemic colitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'adverse', 'Hypersensitivity reactions up to anaphylaxis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse' and content = 'Hypersensitivity reactions up to anaphylaxis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'adverse', 'Medication overuse headache with frequent use', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'adverse' and content = 'Medication overuse headache with frequent use');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'contraindication', 'Moderate or severe hypertension (and mild uncontrolled hypertension)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'contraindication' and content = 'Moderate or severe hypertension (and mild uncontrolled hypertension)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'contraindication', 'Previous myocardial infarction', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'contraindication' and content = 'Previous myocardial infarction');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'contraindication', 'Intravenous administration (vasospasm risk)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'contraindication' and content = 'Intravenous administration (vasospasm risk)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'interaction', 'Lithium: possible serotonin syndrome.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'interaction' and content = 'Lithium: possible serotonin syndrome.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'interaction', 'St John''s wort: adverse effects may be more frequent.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'interaction' and content = 'St John''s wort: adverse effects may be more frequent.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'interaction', 'After sumatriptan wait at least 6 hours before ergotamine and 24 hours before another triptan.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'interaction' and content = 'After sumatriptan wait at least 6 hours before ergotamine and 24 hours before another triptan.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_sumatriptan', 'interaction', 'No interaction with propranolol, flunarizine, pizotifen or alcohol.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_sumatriptan' and kind = 'interaction' and content = 'No interaction with propranolol, flunarizine, pizotifen or alcohol.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_sumatriptan', 'UK SmPC (emc)', 'Sumatriptan 50 mg tablets. Summary of Product Characteristics. Milpharm Ltd; revised 9 June 2026. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=sumatriptan#emc-524', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_sumatriptan'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_sumatriptan' and url = 'https://products.mhra.gov.uk/search/?search=sumatriptan#emc-524');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_sumatriptan', 'UK SmPC (emc)', 'Imigran Injection / Imigran Subject (sumatriptan 6 mg). Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025. emc.', 'https://products.mhra.gov.uk/search/?search=sumatriptan#emc-944', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_sumatriptan'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_sumatriptan' and url = 'https://products.mhra.gov.uk/search/?search=sumatriptan#emc-944');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_sumatriptan', 'UK SmPC (emc)', 'Imigran 10 mg Nasal Spray. Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025. emc.', 'https://products.mhra.gov.uk/search/?search=sumatriptan#emc-2214', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_sumatriptan'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_sumatriptan' and url = 'https://products.mhra.gov.uk/search/?search=sumatriptan#emc-2214');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_sumatriptan', 'Neurology Asia', 'Roxas AA Jr, Quiles LE, Diamante PA. The practice patterns of migraine management among neurologists in the Philippines: a cross-sectional survey. Neurology Asia. 2022;27(3):717-724.', 'https://neurology-asia.org/system/index.php/neuro/article/view/675', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_sumatriptan'), 0)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_sumatriptan' and url = 'https://neurology-asia.org/system/index.php/neuro/article/view/675');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hypertension', 'med_sumatriptan', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hypertension'), 0), 'avoid'::condition_safety, 'Contraindicated in moderate or severe hypertension and in mild uncontrolled hypertension; use with caution in mild controlled hypertension (UK SmPC).'
where exists (select 1 from public.diseases where id = 'hypertension')
  and exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hypertension' and medicine_id = 'med_sumatriptan');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_sumatriptan', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'UK SmPC advises caution in impaired renal function; no specific dose adjustment given.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_sumatriptan');
-- med_sumatriptan
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_sumatriptan', 'adult', 0, 'Acute migraine', 'PO', '50 mg (some need 100 mg)', 'Single dose; repeat once if it recurs, ≥2 h apart', 'Per attack', '300 mg/24 h', 'Label · UK SmPC', 'No second dose if the first fails; use paracetamol, aspirin or an NSAID'),
    ('med_sumatriptan', 'adult', 1, 'Acute migraine', 'SC', '6 mg', 'Single dose; repeat once if it recurs, ≥1 h apart', 'Per attack', '12 mg/24 h', 'Label · UK SmPC inj', 'Never IV'),
    ('med_sumatriptan', 'adult', 2, 'Cluster headache attack', 'SC', '6 mg', 'Per attack, ≥1 h apart', 'Per attack', '12 mg/24 h', 'Label · UK SmPC inj', ''),
    ('med_sumatriptan', 'adult', 3, 'Acute migraine', 'Nasal', '20 mg (some respond to 10 mg)', 'Single dose; repeat once if it recurs, ≥2 h apart', 'Per attack', '40 mg/24 h', 'Label · UK SmPC nasal', 'Into one nostril'),
    ('med_sumatriptan', 'child', 4, 'Acute migraine, 12–17 years', 'Nasal', '10 mg', 'Single dose; repeat once if it recurs, ≥2 h apart', 'Per attack', '20 mg/24 h', 'Label · UK SmPC nasal', 'Specialist recommendation only; not under 12; tablets and injection not recommended under 18')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_sumatriptan');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_sumatriptan', 'renal', 0, '', 'No dose adjustment stated; use with caution in renal impairment.', 'Label · UK SmPC'),
    ('med_sumatriptan', 'hepatic', 1, '', 'Mild to moderate impairment: consider low doses of 25–50 mg orally. Contraindicated in severe impairment.', 'Label · UK SmPC'),
    ('med_sumatriptan', 'elderly', 2, '', 'Not recommended over 65 years because of limited experience.', 'Label · UK SmPC'),
    ('med_sumatriptan', 'pregnancy', 3, '', 'Over 1,000 first-trimester exposures without a clear rise in birth defects, but data are insufficient; use only if benefit outweighs risk. Relative infant dose in milk is below 4%; avoid breastfeeding and discard milk for 12 hours after a dose.', 'Label · UK SmPC'),
    ('med_sumatriptan', 'administration', 4, '', 'Use only when the diagnosis of migraine is clear; take at the first sign of the attack. Swallow tablets whole with water. The injection needle shield may contain latex.', 'Label · UK SmPC inj'),
    ('med_sumatriptan', 'monitor', 5, '', 'Assess cardiovascular risk before first use (smokers, nicotine replacement users, men over 40, postmenopausal women with risk factors). Stop if chest symptoms suggest ischaemia. Ask about headache days per month to detect medication overuse headache.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_sumatriptan');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_sumatriptan', 'Label · UK SmPC', 'UK SmPC (emc)', 'Sumatriptan 50 mg tablets. Summary of Product Characteristics. Milpharm Ltd; revised 9 June 2026.', 'https://products.mhra.gov.uk/search/?search=sumatriptan#emc-524', 0),
    ('med_sumatriptan', 'Label · UK SmPC inj', 'UK SmPC (emc)', 'Imigran Injection (sumatriptan 6 mg). Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025.', 'https://products.mhra.gov.uk/search/?search=sumatriptan#emc-944', 1),
    ('med_sumatriptan', 'Label · UK SmPC nasal', 'UK SmPC (emc)', 'Imigran 10 mg Nasal Spray. Summary of Product Characteristics. GlaxoSmithKline UK; revised 15 October 2025.', 'https://products.mhra.gov.uk/search/?search=sumatriptan#emc-2214', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_sumatriptan')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_sumatriptan');


-- ================================================ med_tenofovir  (Tenofovir Disoproxil Fumarate)
update public.medicines set description = 'Tenofovir disoproxil fumarate is an oral prodrug of tenofovir, an acyclic nucleotide (adenosine monophosphate) analogue. After intracellular phosphorylation to tenofovir diphosphate it competes with natural nucleotides and terminates DNA chain elongation, inhibiting HIV-1 reverse transcriptase and the hepatitis B virus polymerase. It is used with other antiretrovirals for HIV-1 treatment, as HIV pre-exposure prophylaxis with emtricitabine, and as a first-line agent for chronic hepatitis B because of its high barrier to resistance. In the Philippines, tenofovir disoproxil combined with emtricitabine is the drug used for oral HIV pre-exposure prophylaxis under the DOH interim PrEP guidelines (2021), taken daily by anyone at substantial risk or event-driven (2-1-1) by men who have sex with men. WHO recommends tenofovir prophylaxis from the 28th week of pregnancy for HBsAg-positive women with HBV DNA of 200,000 IU/mL or more to prevent mother-to-child transmission of hepatitis B.', updated_at = now()
where id = 'med_tenofovir' and description = 'Tenofovir disoproxil fumarate is an oral prodrug of tenofovir, an acyclic nucleotide (adenosine monophosphate) analogue. After intracellular phosphorylation to tenofovir diphosphate it competes with natural nucleotides and terminates DNA chain elongation, inhibiting HIV-1 reverse transcriptase and the hepatitis B virus polymerase. It is used with other antiretrovirals for HIV-1 treatment, as HIV pre-exposure prophylaxis with emtricitabine, and as a first-line agent for chronic hepatitis B because of its high barrier to resistance.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'DOH interim PrEP guidelines; DOST HTA Philippines; World Health Organization; MSF Essential Drugs; UK SmPC (emc); DailyMed (FDA label)' else source_attribution || '; DOH interim PrEP guidelines; DOST HTA Philippines; World Health Organization; MSF Essential Drugs; UK SmPC (emc); DailyMed (FDA label)' end
where id = 'med_tenofovir' and position('DOH interim PrEP guidelines' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'indication', 'Chronic hepatitis B with decompensated liver disease or lamivudine-resistant HBV in adults (UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'indication' and content = 'Chronic hepatitis B with decompensated liver disease or lamivudine-resistant HBV in adults (UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'indication', 'Event-driven (2-1-1) oral PrEP with emtricitabine for men who have sex with men (DOH interim PrEP guidelines, 2021)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'indication' and content = 'Event-driven (2-1-1) oral PrEP with emtricitabine for men who have sex with men (DOH interim PrEP guidelines, 2021)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'adverse', 'Dizziness', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'adverse' and content = 'Dizziness');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'adverse', 'Mild serum creatinine rises in PrEP users (mostly grade 1; renal events more frequent than with placebo)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'adverse' and content = 'Mild serum creatinine rises in PrEP users (mostly grade 1; renal events more frequent than with placebo)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'contraindication', 'Hypersensitivity to tenofovir disoproxil or any excipient (UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'contraindication' and content = 'Hypersensitivity to tenofovir disoproxil or any excipient (UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'contraindication', 'PrEP is not started in people who are HIV-positive, have signs of acute retroviral syndrome, weigh under 35 kg or have CrCl of 60 mL/min or less (DOH)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'contraindication' and content = 'PrEP is not started in people who are HIV-positive, have signs of acute retroviral syndrome, weigh under 35 kg or have CrCl of 60 mL/min or less (DOH)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'contraindication', 'Use in children with renal impairment is not recommended (UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'contraindication' and content = 'Use in children with renal impairment is not recommended (UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'interaction', 'Other tenofovir disoproxil or tenofovir alafenamide products and adefovir dipivoxil: not co-administered.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'interaction' and content = 'Other tenofovir disoproxil or tenofovir alafenamide products and adefovir dipivoxil: not co-administered.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'interaction', 'Tacrolimus: monitor renal function during co-administration.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'interaction' and content = 'Tacrolimus: monitor renal function during co-administration.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'interaction', 'Amphotericin B and pentamidine: nephrotoxic; avoid or monitor renal function (MSF).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'interaction' and content = 'Amphotericin B and pentamidine: nephrotoxic; avoid or monitor renal function (MSF).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tenofovir', 'interaction', 'Clarithromycin: may raise tenofovir levels; use with caution and close monitoring (MSF).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tenofovir' and kind = 'interaction' and content = 'Clarithromycin: may raise tenofovir levels; use with caution and close monitoring (MSF).');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_tenofovir', 'DOH interim PrEP guidelines', 'Department of Health, Philippines. Department Memorandum: Interim Guidelines on Pre-Exposure Prophylaxis (PrEP) for the Prevention of HIV Infection in the Philippines. 4 January 2021.', 'https://hivpreventioncoalition.unaids.org/sites/default/files/attachments/interim_guidelines_on_pre-exposure_prophylaxis_prep.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_tenofovir'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_tenofovir' and url = 'https://hivpreventioncoalition.unaids.org/sites/default/files/attachments/interim_guidelines_on_pre-exposure_prophylaxis_prep.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_tenofovir', 'DOST HTA Philippines', 'Health Technology Assessment Council (DOST-PCHRD / DOH). Evidence summary: Emtricitabine/tenofovir disoproxil fumarate oral PrEP for HIV. Approved by the Secretary of Health 18 January 2022.', 'https://hta.dost.gov.ph/wp-content/uploads/2024/02/ES_Oral-PrEP-for-HIV_as-of-Nov-2021.docx-1.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_tenofovir'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_tenofovir' and url = 'https://hta.dost.gov.ph/wp-content/uploads/2024/02/ES_Oral-PrEP-for-HIV_as-of-Nov-2021.docx-1.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_tenofovir', 'World Health Organization', 'World Health Organization. Hepatitis: Preventing mother-to-child transmission of the hepatitis B virus. Questions and answers.', 'https://www.who.int/news-room/questions-and-answers/item/hepatitis-preventing-mother-to-child-transmission-of-the-hepatitis-b-virus', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_tenofovir'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_tenofovir' and url = 'https://www.who.int/news-room/questions-and-answers/item/hepatitis-preventing-mother-to-child-transmission-of-the-hepatitis-b-virus');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_tenofovir', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs - practical guidelines: Tenofovir disoproxil fumarate = TDF oral. Updated April 2026.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/tenofovir-disoproxil-fumarate-tdf-oral-38537560.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_tenofovir'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_tenofovir' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/tenofovir-disoproxil-fumarate-tdf-oral-38537560.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_tenofovir', 'UK SmPC (emc)', 'Viread 245 mg film-coated tablets - Summary of Product Characteristics. Gilead Sciences Ltd. Electronic medicines compendium (emc), updated 15 March 2024.', 'https://products.mhra.gov.uk/search/?search=tenofovir#emc-1615', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_tenofovir'), 0)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_tenofovir' and url = 'https://products.mhra.gov.uk/search/?search=tenofovir#emc-1615');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_tenofovir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Dosing interval is lengthened when CrCl is below 50 mL/min and renal function is monitored; MSF prefers entecavir for hepatitis B in renal impairment (UK SmPC, MSF).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_tenofovir');
-- med_tenofovir
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_tenofovir', 'adult', 0, 'HIV-1 infection (with other ARVs)', 'PO', '300 mg', 'Once a day', 'Long-term', '300 mg/day', 'Label · US FDA', 'Same dose for chronic hepatitis B'),
    ('med_tenofovir', 'adult', 1, 'Chronic hepatitis B', 'PO', '300 mg', 'Once a day', 'Usually long-term', '300 mg/day', 'MSF', 'HBeAg+: at least 12 months after HBe seroconversion (UK SmPC)'),
    ('med_tenofovir', 'adult', 2, 'HBV mother-to-child prevention (pregnancy)', 'PO', '300 mg', 'Once a day', 'From week 28 until at least birth', '—', 'WHO', 'If HBV DNA ≥200,000 IU/mL (or HBeAg+)'),
    ('med_tenofovir', 'adult', 3, 'HIV PrEP, daily (with emtricitabine)', 'PO', '1 TDF/FTC tablet', 'Once a day', 'While at risk; 28 days after last exposure', '2 tablets/day', 'DOH PrEP 2021', 'Protection after 5–7 days (anal) or 20 days (vaginal)'),
    ('med_tenofovir', 'adult', 4, 'HIV PrEP, event-driven (MSM only)', 'PO', '2 tablets, then 1, then 1', '2–24 h before sex, then 24 h and 48 h after first dose', 'Until 2 days after last sex', '2 tablets/day', 'DOH PrEP 2021', 'TDF/FTC tablets'),
    ('med_tenofovir', 'child', 5, 'HIV-1 or chronic hepatitis B (≥2 years, ≥10 kg)', 'PO', '8 mg/kg', 'Once a day', 'Long-term', '300 mg/day', 'Label · US FDA', 'Tablets ≥17 kg: 150 mg (17–<22 kg), 200 mg (22–<28 kg), 250 mg (28–<35 kg)'),
    ('med_tenofovir', 'child', 6, 'HIV-1 or chronic hepatitis B (12 years and older, ≥35 kg)', 'PO', '300 mg', 'Once a day', 'Long-term', '300 mg/day', 'MSF', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_tenofovir');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_tenofovir', 'renal', 0, 'CrCl 50–80', 'Once-daily dosing supported by limited data.', 'Label · UK SmPC'),
    ('med_tenofovir', 'renal', 1, 'CrCl 30–49', '300 mg every 48 hours.', 'MSF'),
    ('med_tenofovir', 'renal', 2, 'CrCl 10–29', '300 mg every 72–96 hours; below CrCl 10 seek specialist advice. MSF prefers entecavir for hepatitis B in renal impairment.', 'MSF'),
    ('med_tenofovir', 'renal', 3, 'Haemodialysis', 'Every 7 days, after a dialysis session.', 'Label · UK SmPC'),
    ('med_tenofovir', 'hepatic', 4, '', 'No dose adjustment.', 'Label · UK SmPC'),
    ('med_tenofovir', 'elderly', 5, '', 'No data in people over 65; use with caution because renal function is often reduced.', 'Label · UK SmPC'),
    ('med_tenofovir', 'pregnancy', 6, '', 'More than 1,000 pregnancy outcomes show no malformations or fetal/neonatal toxicity. Women with HBV may breastfeed; women living with HIV follow national breastfeeding advice.', 'Label · UK SmPC'),
    ('med_tenofovir', 'administration', 7, '', 'Missed dose: take within 12 hours, otherwise skip. Vomiting within 1 hour: take another dose. The UK label advises taking it with food; the oral powder is always given with food.', 'Label · UK SmPC'),
    ('med_tenofovir', 'monitor', 8, '', 'Creatinine clearance and serum phosphate before starting, after 2–4 weeks, after 3 months, then every 3–6 months if there are no renal risk factors.', 'Label · UK SmPC'),
    ('med_tenofovir', 'monitor', 9, '', 'PrEP: HIV test within 7 days before starting, after 1 month, then at least every 3 months; HBsAg at baseline; serum creatinine every 6 months; stop PrEP if CrCl falls below 60 mL/min.', 'DOH PrEP 2021')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_tenofovir');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_tenofovir', 'DOH PrEP 2021', 'DOH interim PrEP guidelines', 'DOH Philippines. Interim Guidelines on Pre-Exposure Prophylaxis (PrEP) for the Prevention of HIV Infection in the Philippines, 4 January 2021.', 'https://hivpreventioncoalition.unaids.org/sites/default/files/attachments/interim_guidelines_on_pre-exposure_prophylaxis_prep.pdf', 0),
    ('med_tenofovir', 'WHO', 'World Health Organization', 'WHO. Hepatitis: Preventing mother-to-child transmission of the hepatitis B virus (Q&A).', 'https://www.who.int/news-room/questions-and-answers/item/hepatitis-preventing-mother-to-child-transmission-of-the-hepatitis-b-virus', 1),
    ('med_tenofovir', 'MSF', 'MSF Essential Drugs', 'MSF Essential drugs: Tenofovir disoproxil fumarate = TDF oral, 2026.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/tenofovir-disoproxil-fumarate-tdf-oral-38537560.html', 2),
    ('med_tenofovir', 'Label · UK SmPC', 'UK SmPC (emc)', 'Viread 245 mg film-coated tablets SmPC, Gilead Sciences Ltd, updated 15 March 2024.', 'https://products.mhra.gov.uk/search/?search=tenofovir#emc-1615', 3),
    ('med_tenofovir', 'Label · US FDA', 'DailyMed (FDA label)', 'VIREAD (tenofovir disoproxil fumarate) tablets and oral powder, Gilead Sciences. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=33fd6418-fbdc-42ca-a50d-ce2a476a5418', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_tenofovir')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_tenofovir');


-- ================================================ med_tld  (Tenofovir + Lamivudine + Dolutegravir (TLD))
update public.medicines set description = 'TLD is a once-daily fixed-dose tablet combining two nucleos(t)ide reverse transcriptase inhibitors (tenofovir disoproxil fumarate and lamivudine), which terminate viral DNA chain synthesis, with dolutegravir, an integrase strand transfer inhibitor that blocks integration of HIV DNA into the host genome. WHO recommends dolutegravir-based therapy as the preferred first- and second-line HIV treatment in all populations, and tenofovir plus lamivudine also suppress hepatitis B virus. There is no US boxed warning for this WHO-prequalified combination itself, but the US label of its tenofovir disoproxil component carries a boxed warning for severe acute exacerbation of hepatitis B after discontinuation, which applies to people with HBV co-infection. In the Philippines it is the DOH''s recommended first-line antiretroviral regimen, procured nationally for people living with HIV (Philippine News Agency, July 2026). The Philippine HTA Council recommended TLD for both treatment-naive and treatment-experienced adolescents and adults with HIV, a decision approved by the Secretary of Health on 1 September 2021, noting a monthly bottle cost (PHP 549) equal to the older tenofovir/lamivudine/efavirenz tablet. WHO''s January 2026 HIV clinical management update confirms dolutegravir-based regimens as the preferred option for initial and subsequent treatment and supports reusing tenofovir in later regimens.', updated_at = now()
where id = 'med_tld' and description = 'TLD is a once-daily fixed-dose tablet combining two nucleos(t)ide reverse transcriptase inhibitors (tenofovir disoproxil fumarate and lamivudine), which terminate viral DNA chain synthesis, with dolutegravir, an integrase strand transfer inhibitor that blocks integration of HIV DNA into the host genome. WHO recommends dolutegravir-based therapy as the preferred first- and second-line HIV treatment in all populations, and tenofovir plus lamivudine also suppress hepatitis B virus. There is no US boxed warning for this WHO-prequalified combination itself, but the US label of its tenofovir disoproxil component carries a boxed warning for severe acute exacerbation of hepatitis B after discontinuation, which applies to people with HBV co-infection. In the Philippines it is the DOH''s recommended first-line antiretroviral regimen, procured nationally for people living with HIV (Philippine News Agency, July 2026).';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'DOST HTA Philippines; World Health Organization; MSF Essential Drugs; WHO Prequalification (WHOPAR product information)' else source_attribution || '; DOST HTA Philippines; World Health Organization; MSF Essential Drugs; WHO Prequalification (WHOPAR product information)' end
where id = 'med_tld' and position('DOST HTA Philippines' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'adverse', 'Insomnia, abnormal dreams, anxiety and depression (common; neuropsychiatric effects were the most reported in a Zambian pharmacovigilance study)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse' and content = 'Insomnia, abnormal dreams, anxiety and depression (common; neuropsychiatric effects were the most reported in a Zambian pharmacovigilance study)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'adverse', 'Dizziness, vomiting, asthenia and rash (very common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse' and content = 'Dizziness, vomiting, asthenia and rash (very common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'adverse', 'Raised ALT/AST and creatine phosphokinase', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse' and content = 'Raised ALT/AST and creatine phosphokinase');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'adverse', 'Arthralgia, fatigue, fever, hair loss and pruritus', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse' and content = 'Arthralgia, fatigue, fever, hair loss and pruritus');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'adverse', 'Pancreatitis (rare); stop if suspected', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse' and content = 'Pancreatitis (rare); stop if suspected');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'adverse', 'Small increased risk of neural tube defects with exposure around conception (0.19% vs 0.11% in Botswana surveillance)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'adverse' and content = 'Small increased risk of neural tube defects with exposure around conception (0.19% vs 0.11% in Botswana surveillance)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'contraindication', 'HIV-1 with integrase inhibitor resistance (fixed-dose tablet is for INSTI-susceptible HIV-1)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'contraindication' and content = 'HIV-1 with integrase inhibitor resistance (fixed-dose tablet is for INSTI-susceptible HIV-1)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'contraindication', 'Children weighing under 30 kg (separate formulations needed)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'contraindication' and content = 'Children weighing under 30 kg (separate formulations needed)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'interaction', 'Etravirine (without a boosted protease inhibitor): lowers dolutegravir exposure by about 71%; dolutegravir is given 50 mg twice daily.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction' and content = 'Etravirine (without a boosted protease inhibitor): lowers dolutegravir exposure by about 71%; dolutegravir is given 50 mg twice daily.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'interaction', 'Efavirenz, nevirapine, oxcarbazepine and phenobarbital: expected to lower dolutegravir levels; the dolutegravir dose is doubled with enzyme inducers.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction' and content = 'Efavirenz, nevirapine, oxcarbazepine and phenobarbital: expected to lower dolutegravir levels; the dolutegravir dose is doubled with enzyme inducers.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'interaction', 'Rifampicin and other enzyme inducers: continue the double dolutegravir dose for 2 weeks after the inducer is stopped (MSF).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction' and content = 'Rifampicin and other enzyme inducers: continue the double dolutegravir dose for 2 weeks after the inducer is stopped (MSF).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'interaction', 'Sorbitol, mannitol and other polyols: reduce lamivudine exposure; avoid chronic co-use or monitor viral load.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction' and content = 'Sorbitol, mannitol and other polyols: reduce lamivudine exposure; avoid chronic co-use or monitor viral load.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'interaction', 'Cladribine: not recommended with lamivudine.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction' and content = 'Cladribine: not recommended with lamivudine.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'interaction', 'Emtricitabine, adefovir dipivoxil, tenofovir alafenamide and didanosine: not co-administered.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction' and content = 'Emtricitabine, adefovir dipivoxil, tenofovir alafenamide and didanosine: not co-administered.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_tld', 'interaction', 'Metformin: MSF advises not exceeding 1 g/day with dolutegravir and monitoring blood glucose and renal function.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_tld' and kind = 'interaction' and content = 'Metformin: MSF advises not exceeding 1 g/day with dolutegravir and monitoring blood glucose and renal function.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_tld', 'DOST HTA Philippines', 'Health Technology Assessment Council (DOST / DOH). Evidence summary: Tenofovir/lamivudine/dolutegravir (TLD) for treatment-naive and treatment-experienced adolescents and adults living with HIV. Approved by the Secretary of Health 1 September 2021.', 'https://hta.dost.gov.ph/wp-content/uploads/2021/09/ES_TLD_for_HIV_approved_by_SOH.docx.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_tld'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_tld' and url = 'https://hta.dost.gov.ph/wp-content/uploads/2021/09/ES_TLD_for_HIV_approved_by_SOH.docx.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_tld', 'World Health Organization', 'World Health Organization. WHO releases updated recommendations on HIV clinical management. News release, 7 January 2026.', 'https://www.who.int/news/item/07-01-2026-who-releases-updated-recommendations-on-hiv-clinical-management', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_tld'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_tld' and url = 'https://www.who.int/news/item/07-01-2026-who-releases-updated-recommendations-on-hiv-clinical-management');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_tld', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs - practical guidelines: Dolutegravir = DTG oral. Updated October 2024.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/dolutegravir-dtg-oral-38537537.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_tld'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_tld' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/dolutegravir-dtg-oral-38537537.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_tld', 'World Health Organization', 'World Health Organization. Hepatitis B. Fact sheet, updated 28 July 2026.', 'https://www.who.int/news-room/fact-sheets/detail/hepatitis-B', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_tld'), 0)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_tld' and url = 'https://www.who.int/news-room/fact-sheets/detail/hepatitis-B');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hepatitis_b', 'med_tld', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hepatitis_b'), 0), 'safe'::condition_safety, 'Tenofovir (in first-line HIV combinations) is active against HBV (WHO); in coinfection do not stop TLD without HBV cover because of flare risk (WHOPAR).'
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hepatitis_b' and medicine_id = 'med_tld');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'tuberculosis', 'med_tld', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'tuberculosis'), 0), 'caution'::condition_safety, 'Rifampicin lowers dolutegravir levels; an extra dolutegravir 50 mg tablet is added to TLD during TB treatment (DOST HTA, WHOPAR).'
where exists (select 1 from public.diseases where id = 'tuberculosis')
  and exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.disease_medicines where disease_id = 'tuberculosis' and medicine_id = 'med_tld');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_tld', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'avoid'::condition_safety, 'Fixed-dose tablet not recommended when CrCl is below 50 mL/min; use separate components with dose adjustment (WHOPAR).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_tld');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_tld', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Dolutegravir raises metformin levels; monitor glucose and renal function and limit metformin to 1 g/day (MSF).'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_tld');
-- med_tld
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_tld', 'adult', 0, 'HIV-1 infection (first- or second-line)', 'PO', '1 tablet (TDF 300 mg / 3TC 300 mg / DTG 50 mg)', 'Once a day', 'Lifelong', '1 tablet/day', 'DOST HTA 2021', 'With or without food'),
    ('med_tld', 'adult', 1, 'HIV-1 with rifampicin or other enzyme inducer', 'PO', '1 tablet + dolutegravir 50 mg', 'TLD once a day; extra DTG about 12 h later', 'During inducer and 2 weeks after', '—', 'MSF', 'Also with efavirenz, carbamazepine (WHOPAR)'),
    ('med_tld', 'child', 2, 'HIV-1 infection (adolescents ≥30 kg)', 'PO', '1 tablet', 'Once a day', 'Lifelong', '1 tablet/day', 'WHOPAR', 'Not for children under 30 kg')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_tld');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_tld', 'renal', 0, 'CrCl 50–80', 'No dose adjustment.', 'WHOPAR'),
    ('med_tld', 'renal', 1, 'CrCl < 50', 'Fixed-dose tablet not recommended; give the components separately with dose adjustment.', 'WHOPAR'),
    ('med_tld', 'hepatic', 2, '', 'No adjustment in Child-Pugh A or B; use with caution in Child-Pugh C (no dolutegravir data).', 'WHOPAR'),
    ('med_tld', 'elderly', 3, '', 'Use with caution.', 'WHOPAR'),
    ('med_tld', 'pregnancy', 4, '', 'Counsel women of childbearing potential on neural tube defect risk and contraception; pregnancy test before starting if feasible. Folic acid in the first trimester may reduce the risk (MSF). All three components pass into breast milk.', 'WHOPAR'),
    ('med_tld', 'administration', 5, '', 'Missed dose: take if less than 12 hours late, otherwise skip; never double. Vomiting within 1 hour: take another dose.', 'WHOPAR'),
    ('med_tld', 'monitor', 6, '', 'Creatinine clearance before and during therapy; interrupt if confirmed CrCl < 50 mL/min or serum phosphate < 1.0 mg/dL. Test for HBV before starting.', 'WHOPAR'),
    ('med_tld', 'monitor', 7, '', 'Liver enzymes and bilirubin if hypersensitivity is suspected; weight, lipids and glucose; in HBV coinfection, liver tests for at least 6 months after stopping.', 'WHOPAR'),
    ('med_tld', 'forms_ph', 8, '', 'Fixed-dose tablet TDF 300 mg + 3TC 300 mg + DTG 50 mg, holding a monitored-release FDA certificate of product registration; not yet in the PNF at the time of the 2021 HTA review (components listed singly).', 'DOST HTA 2021')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_tld');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_tld', 'WHOPAR', 'WHO Prequalification (WHOPAR product information)', 'WHO Prequalification. Dolutegravir/Lamivudine/Tenofovir disoproxil fumarate 50/300/300 mg tablets (HA729), SmPC, WHOPAR part 4, Oct 2022.', 'https://extranet.who.int/prequal/sites/default/files/whopar_files/HA729part4v2.pdf', 0),
    ('med_tld', 'DOST HTA 2021', 'DOST HTA Philippines', 'HTA Council evidence summary: TLD for adolescents and adults living with HIV, approved by SOH 1 Sep 2021.', 'https://hta.dost.gov.ph/wp-content/uploads/2021/09/ES_TLD_for_HIV_approved_by_SOH.docx.pdf', 1),
    ('med_tld', 'MSF', 'MSF Essential Drugs', 'MSF Essential drugs: Dolutegravir = DTG oral, Oct 2024.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/dolutegravir-dtg-oral-38537537.html', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_tld')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_tld');


-- ================================================ med_vancomycin  (Vancomycin)
update public.medicines set description = 'Vancomycin binds the D-alanyl-D-alanine ends of cell-wall precursors and blocks peptidoglycan synthesis in gram-positive bacteria. Given intravenously it treats serious infections due to MRSA and resistant pneumococci, and in suspected bacterial meningitis it is added to a third-generation cephalosporin until susceptibilities are known. Oral vancomycin is not absorbed and is used only for Clostridioides difficile colitis. UK labeling also licenses IV vancomycin for complicated skin and soft tissue infections, bone and joint infections, community- and hospital-acquired pneumonia, infective endocarditis and surgical prophylaxis in patients at high risk of endocarditis. The first IV dose is based on total body weight (a 25–30 mg/kg loading dose may be used in seriously ill patients), and later doses are guided by serum levels and kidney function. IV vancomycin is not effective for C. difficile infection, and it must never be given intramuscularly.', updated_at = now()
where id = 'med_vancomycin' and description = 'Vancomycin binds the D-alanyl-D-alanine ends of cell-wall precursors and blocks peptidoglycan synthesis in gram-positive bacteria. Given intravenously it treats serious infections due to MRSA and resistant pneumococci, and in suspected bacterial meningitis it is added to a third-generation cephalosporin until susceptibilities are known. Oral vancomycin is not absorbed and is used only for Clostridioides difficile colitis.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); DailyMed (FDA label)' else source_attribution || '; UK SmPC (emc); DailyMed (FDA label)' end
where id = 'med_vancomycin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'indication', 'Complicated skin and soft tissue infections and bone and joint infections (IV)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'indication' and content = 'Complicated skin and soft tissue infections and bone and joint infections (IV)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'indication', 'Community-acquired and hospital-acquired pneumonia, including ventilator-associated pneumonia (IV)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'indication' and content = 'Community-acquired and hospital-acquired pneumonia, including ventilator-associated pneumonia (IV)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'indication', 'Perioperative prophylaxis in patients at high risk of bacterial endocarditis undergoing major surgery (IV)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'indication' and content = 'Perioperative prophylaxis in patients at high risk of bacterial endocarditis undergoing major surgery (IV)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'adverse', 'Severe skin reactions: SJS, TEN, DRESS, AGEP, linear IgA bullous dermatosis (stop at first signs; never restart)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse' and content = 'Severe skin reactions: SJS, TEN, DRESS, AGEP, linear IgA bullous dermatosis (stop at first signs; never restart)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'adverse', 'Hypotension, shock and rarely cardiac arrest with rapid bolus infusion', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse' and content = 'Hypotension, shock and rarely cardiac arrest with rapid bolus infusion');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'adverse', 'Raised ALT and AST (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse' and content = 'Raised ALT and AST (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'adverse', 'Interstitial nephritis and acute renal failure (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse' and content = 'Interstitial nephritis and acute renal failure (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'adverse', 'Drug fever, shivering, pain and muscle spasm of chest and back (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse' and content = 'Drug fever, shivering, pain and muscle spasm of chest and back (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'adverse', 'Kounis syndrome (allergic acute coronary syndrome)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse' and content = 'Kounis syndrome (allergic acute coronary syndrome)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'adverse', 'Haemorrhagic occlusive retinal vasculitis after intracameral or intravitreal use (not an approved route)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'adverse' and content = 'Haemorrhagic occlusive retinal vasculitis after intracameral or intravitreal use (not an approved route)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'contraindication', 'Intramuscular injection (risk of necrosis at the injection site)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'contraindication' and content = 'Intramuscular injection (risk of necrosis at the injection site)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'contraindication', 'Previous severe skin reaction (SJS, TEN, DRESS, AGEP) to vancomycin: must not be restarted', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'contraindication' and content = 'Previous severe skin reaction (SJS, TEN, DRESS, AGEP) to vancomycin: must not be restarted');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'interaction', 'Anaesthetic agents: more erythema, histamine-like flushing and anaphylactoid reactions; infuse vancomycin over 60 minutes before induction.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'interaction' and content = 'Anaesthetic agents: more erythema, histamine-like flushing and anaphylactoid reactions; infuse vancomycin over 60 minutes before induction.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'interaction', 'Bacitracin, polymyxin B, colistin and viomycin: additive kidney or ear toxicity; monitor closely.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'interaction' and content = 'Bacitracin, polymyxin B, colistin and viomycin: additive kidney or ear toxicity; monitor closely.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_vancomycin', 'interaction', 'Oral use for C. difficile: stop anti-motility agents and reconsider proton pump inhibitors.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin' and kind = 'interaction' and content = 'Oral use for C. difficile: stop anti-motility agents and reconsider proton pump inhibitors.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_vancomycin', 'UK SmPC (emc)', 'Vancomycin 500 mg powder for concentrate for solution for infusion. Summary of Product Characteristics. hameln pharma ltd; text revised 19 Jan 2026. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=vancomycin#emc-15736', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_vancomycin'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_vancomycin' and url = 'https://products.mhra.gov.uk/search/?search=vancomycin#emc-15736');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_vancomycin', 'DailyMed (FDA label)', 'Vancomycin Hydrochloride for Injection, USP. Prescribing information. Glenmark Pharmaceuticals Inc.; revised 12/2025. DailyMed, U.S. National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=0543b2b5-b1c7-4ad6-b38c-3be0086f0e06&type=display', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_vancomycin'), 0)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_vancomycin' and url = 'https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=0543b2b5-b1c7-4ad6-b38c-3be0086f0e06&type=display');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'community_acquired_pneumonia', 'med_vancomycin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'community_acquired_pneumonia'), 0), 'safe'::condition_safety, 'Licensed IV indication, including MRSA; typical course 7–14 days (UK SmPC).'
where exists (select 1 from public.diseases where id = 'community_acquired_pneumonia')
  and exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'community_acquired_pneumonia' and medicine_id = 'med_vancomycin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_vancomycin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Nephrotoxic and renally cleared: give the usual loading dose, then extend the interval and dose by serum levels (UK SmPC).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_vancomycin');
-- med_vancomycin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_vancomycin', 'adult', 0, 'Serious infections (incl. ≥12 y)', 'IV', '15–20 mg/kg', 'Every 8–12 h', 'By infection', '2 g per dose', 'Label · UK SmPC', 'Initial dose by total body weight; adjust by levels'),
    ('med_vancomycin', 'adult', 1, 'Loading dose, seriously ill', 'IV', '25–30 mg/kg', 'Once', '—', '—', 'Label · UK SmPC', 'Do not reduce in renal insufficiency'),
    ('med_vancomycin', 'adult', 2, 'Serious infections (fixed dose)', 'IV', '500 mg or 1 g', 'Every 6 h or every 12 h', 'By infection', '2 g/day', 'Label · US', 'Normal renal function'),
    ('med_vancomycin', 'adult', 3, 'Surgical prophylaxis, high endocarditis risk', 'IV', '15 mg/kg', 'Once, before induction', '—', '—', 'Label · UK SmPC', 'Second dose may be needed for long surgery'),
    ('med_vancomycin', 'adult', 4, 'C. difficile, first non-severe episode', 'PO', '125 mg', 'Every 6 h', '10 days', '2 g/day', 'Label · UK SmPC', ''),
    ('med_vancomycin', 'adult', 5, 'C. difficile, severe or complicated', 'PO', '500 mg', 'Every 6 h', '10 days', '2 g/day', 'Label · UK SmPC', ''),
    ('med_vancomycin', 'adult', 6, 'C. difficile, multiple recurrences', 'PO', '125 mg, then taper or pulse', '4× a day', '10 days, then ≥3 weeks', '—', 'Label · UK SmPC', 'Taper to 125 mg/day or 125–500 mg every 2–3 days'),
    ('med_vancomycin', 'child', 7, 'Serious infections, 1 month–<12 y', 'IV', '10–15 mg/kg', 'Every 6 h', 'By infection', '60 mg/kg/day usually', 'Label · UK SmPC', 'Standard doses may give low levels; monitor'),
    ('med_vancomycin', 'child', 8, 'Surgical prophylaxis, high endocarditis risk', 'IV', '15 mg/kg', 'Once, before induction', '—', '—', 'Label · UK SmPC', ''),
    ('med_vancomycin', 'child', 9, 'C. difficile, <12 y', 'PO', '10 mg/kg', 'Every 6 h', '10 days', '2 g/day', 'Label · UK SmPC', ''),
    ('med_vancomycin', 'neonate', 10, 'Serious infections, PMA <29 weeks', 'IV', '15 mg/kg', 'Every 24 h', 'By infection', '—', 'Label · UK SmPC', 'Seek neonatal specialist advice'),
    ('med_vancomycin', 'neonate', 11, 'Serious infections, PMA 29–35 weeks', 'IV', '15 mg/kg', 'Every 12 h', 'By infection', '—', 'Label · UK SmPC', ''),
    ('med_vancomycin', 'neonate', 12, 'Serious infections, PMA >35 weeks', 'IV', '15 mg/kg', 'Every 8 h', 'By infection', '—', 'Label · UK SmPC', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_vancomycin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_vancomycin', 'renal', 0, 'CrCl 20–49', 'Usual starting dose 15–20 mg/kg every 24 h; do not reduce the first dose.', 'Label · UK SmPC'),
    ('med_vancomycin', 'renal', 1, 'CrCl <20 or dialysis', 'Timing and size of later doses depend on trough levels and the dialysis method; the next dose may be withheld until levels are known. Intermittent haemodialysis removes little vancomycin; high-flux membranes and CRRT remove more.', 'Label · UK SmPC'),
    ('med_vancomycin', 'renal', 2, 'eGFR 30–50', 'Children: 15 mg/kg every 12 h.', 'Label · UK SmPC'),
    ('med_vancomycin', 'renal', 3, 'eGFR 10–29', 'Children: 15 mg/kg every 24 h.', 'Label · UK SmPC'),
    ('med_vancomycin', 'renal', 4, 'eGFR <10', 'Children: 10–15 mg/kg once, then re-dose by levels.', 'Label · UK SmPC'),
    ('med_vancomycin', 'renal', 5, 'Anephric', 'Anephric adults: 15 mg/kg, then 1.9 mg/kg every 24 h.', 'Label · US'),
    ('med_vancomycin', 'hepatic', 6, '', 'No dose adjustment needed.', 'Label · UK SmPC'),
    ('med_vancomycin', 'elderly', 7, '', 'Lower maintenance doses may be needed because kidney function declines with age; monitor kidney function.', 'Label · UK SmPC'),
    ('med_vancomycin', 'pregnancy', 8, '', 'Use only if clearly needed, with careful level monitoring; much higher doses may be needed in pregnancy. Passes into breast milk, but significant absorption by the infant is unlikely.', 'Label · UK SmPC'),
    ('med_vancomycin', 'administration', 9, '', 'Infuse over at least 60 minutes or at no more than 10 mg/min (whichever is longer), diluted to 2.5–5 mg/mL (at least 100 mL per 500 mg). Rotate infusion sites. Never give IM.', 'Label · UK SmPC'),
    ('med_vancomycin', 'administration', 10, '', 'Oral use: dissolve one 500 mg vial in 30 mL water to drink or give by nasogastric tube.', 'Label · UK SmPC'),
    ('med_vancomycin', 'monitor', 11, '', 'Trough level usually 10–20 mg/L (15–20 mg/L if MIC ≥1 mg/L); first level on day 2 before the next dose, then daily to weekly; in haemodialysis, sample before the session.', 'Label · UK SmPC'),
    ('med_vancomycin', 'monitor', 12, '', 'Kidney function, white cell count, urine and liver tests during prolonged treatment; hearing tests in older patients and with other ototoxic drugs.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_vancomycin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_vancomycin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Vancomycin 500 mg powder for concentrate for solution for infusion. Summary of Product Characteristics. hameln pharma ltd; January 2026.', 'https://products.mhra.gov.uk/search/?search=vancomycin#emc-15736', 0),
    ('med_vancomycin', 'Label · US', 'DailyMed (FDA label)', 'Vancomycin Hydrochloride for Injection, USP. Prescribing information. Glenmark Pharmaceuticals Inc.; revised 12/2025.', 'https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=0543b2b5-b1c7-4ad6-b38c-3be0086f0e06&type=display', 1)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_vancomycin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_vancomycin');


-- ================================================ med_warfarin  (Warfarin)
update public.medicines set description = 'Warfarin inhibits vitamin K epoxide reductase (VKORC1), depleting reduced vitamin K and decreasing hepatic synthesis of functional clotting factors II, VII, IX and X (and proteins C and S). It is used for prevention and treatment of venous thromboembolism and thromboembolism in atrial fibrillation and mechanical heart valves, with dosing guided by the INR. In the Philippines warfarin is listed in the Philippine National Formulary for prophylaxis and treatment of thromboembolic disorders, and the Stroke Society of the Philippines recommends either well-controlled warfarin or a direct oral anticoagulant for at-risk patients with non-valvular atrial fibrillation. Its main practical burden is regular INR testing and the many drug and food interactions; an INR above 4.0 adds bleeding risk without added benefit for most patients.', updated_at = now()
where id = 'med_warfarin' and description = 'Warfarin inhibits vitamin K epoxide reductase (VKORC1), depleting reduced vitamin K and decreasing hepatic synthesis of functional clotting factors II, VII, IX and X (and proteins C and S). It is used for prevention and treatment of venous thromboembolism and thromboembolism in atrial fibrillation and mechanical heart valves, with dosing guided by the INR.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); DOST Health Technology Assessment Council (Philippines); DailyMed (FDA label)' else source_attribution || '; UK SmPC (emc); DOST Health Technology Assessment Council (Philippines); DailyMed (FDA label)' end
where id = 'med_warfarin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'indication', 'Transient ischaemic attack (UK labeling)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'indication' and content = 'Transient ischaemic attack (UK labeling)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'indication', 'Systemic embolism prevention in rheumatic heart disease with atrial fibrillation', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'indication' and content = 'Systemic embolism prevention in rheumatic heart disease with atrial fibrillation');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'adverse', 'Pancreatitis, diarrhoea, nausea and vomiting', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'adverse' and content = 'Pancreatitis, diarrhoea, nausea and vomiting');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'adverse', 'Rash, alopecia and purpura', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'adverse' and content = 'Rash, alopecia and purpura');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'adverse', 'Unexplained fall in haematocrit or haemoglobin', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'adverse' and content = 'Unexplained fall in haematocrit or haemoglobin');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'adverse', 'Limb ischaemia or gangrene when started too early in heparin-induced thrombocytopenia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'adverse' and content = 'Limb ischaemia or gangrene when started too early in heparin-induced thrombocytopenia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'contraindication', 'Haemorrhagic stroke', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication' and content = 'Haemorrhagic stroke');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'contraindication', 'Within 72 hours of major surgery with risk of severe bleeding', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication' and content = 'Within 72 hours of major surgery with risk of severe bleeding');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'contraindication', 'Within 48 hours postpartum', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication' and content = 'Within 48 hours postpartum');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'contraindication', 'Initial therapy in heparin-induced thrombocytopenia (start only after platelet count normalises)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication' and content = 'Initial therapy in heparin-induced thrombocytopenia (start only after platelet count normalises)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'contraindication', 'Rare hereditary galactose intolerance or lactase deficiency (UK tablets contain lactose)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'contraindication' and content = 'Rare hereditary galactose intolerance or lactase deficiency (UK tablets contain lactose)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'interaction', 'Fibrinolytics (streptokinase, alteplase): contraindicated combination.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction' and content = 'Fibrinolytics (streptokinase, alteplase): contraindicated combination.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'interaction', 'Allopurinol, capecitabine, erlotinib, tamoxifen, fibrates, statins (mainly fluvastatin), omeprazole and sulfamethoxazole: may raise INR.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction' and content = 'Allopurinol, capecitabine, erlotinib, tamoxifen, fibrates, statins (mainly fluvastatin), omeprazole and sulfamethoxazole: may raise INR.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'interaction', 'Phenytoin, primidone, griseofulvin, azathioprine and oral contraceptives: may lower warfarin effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction' and content = 'Phenytoin, primidone, griseofulvin, azathioprine and oral contraceptives: may lower warfarin effect.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'interaction', 'Corticosteroids, nevirapine and ritonavir: variable effect on INR; monitor closely.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction' and content = 'Corticosteroids, nevirapine and ritonavir: variable effect on INR; monitor closely.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'interaction', 'Cholestyramine and sucralfate reduce warfarin absorption; orlistat may reduce vitamin K absorption.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction' and content = 'Cholestyramine and sucralfate reduce warfarin absorption; orlistat may reduce vitamin K absorption.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'interaction', 'Dabigatran, rivaroxaban and fondaparinux: additive bleeding risk.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction' and content = 'Dabigatran, rivaroxaban and fondaparinux: additive bleeding risk.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_warfarin', 'interaction', 'Cranberry (avoid), grapefruit juice and glucosamine: may raise INR.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_warfarin' and kind = 'interaction' and content = 'Cranberry (avoid), grapefruit juice and glucosamine: may raise INR.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_warfarin', 'UK SmPC (emc)', 'Warfarin 5 mg tablets. Summary of Product Characteristics. Strides Pharma UK Ltd; text revised 10 May 2022, updated July 2025. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=warfarin#emc-14333', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_warfarin'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_warfarin' and url = 'https://products.mhra.gov.uk/search/?search=warfarin#emc-14333');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_warfarin', 'DOST Health Technology Assessment Council (Philippines)', 'Health Technology Assessment Council. Evidence Summary on Apixaban, Dabigatran, and Rivaroxaban for the prevention of myocardial infarction, cerebrovascular disease, and other cardiovascular events among patients with nonvalvular atrial fibrillation. HTA Division, DOST; 25 April 2023.', 'https://hta.dost.gov.ph/wp-content/uploads/2026/07/ES-DOACs-for-NVAF-25-April-2023.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_warfarin'), 0)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_warfarin' and url = 'https://hta.dost.gov.ph/wp-content/uploads/2026/07/ES-DOACs-for-NVAF-25-April-2023.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hypertension', 'med_warfarin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hypertension'), 0), 'caution'::condition_safety, 'Uncontrolled or moderate-to-severe hypertension raises bleeding risk (UK SmPC, US label); malignant hypertension is a contraindication.'
where exists (select 1 from public.diseases where id = 'hypertension')
  and exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hypertension' and medicine_id = 'med_warfarin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_warfarin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'No dose change, but more frequent INR checks; higher risk of bleeding, anticoagulant-related nephropathy and calciphylaxis (UK SmPC, US label).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_warfarin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_warfarin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Diabetes is listed among conditions with higher warfarin risk (US label).'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_warfarin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_coronary_syndrome', 'med_warfarin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome'), 0), 'safe'::condition_safety, 'After high-risk MI: INR 2.0–3.0 plus low-dose aspirin for at least 3 months (US label).'
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome' and medicine_id = 'med_warfarin');
-- med_warfarin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_warfarin', 'adult', 0, 'Starting dose (no genotype data)', 'PO', '2–5 mg', 'Once a day', 'Until INR in range', '—', 'Label · US', 'No routine loading dose; usual maintenance 2–10 mg'),
    ('med_warfarin', 'adult', 1, 'Elective loading (UK regimen)', 'PO', '10 mg', 'Once a day', '2 days', '—', 'Label · UK SmPC', 'Then 3–9 mg once a day by INR; no loading in protein C deficiency'),
    ('med_warfarin', 'adult', 2, 'DVT / PE treatment', 'PO', 'Dose to INR 2.0–3.0', 'Once a day', '3 months if provoked; ≥3 months if unprovoked', '—', 'Label · US', 'Overlap heparin 4–5 days and until INR in range'),
    ('med_warfarin', 'adult', 3, 'Atrial fibrillation', 'PO', 'Dose to INR 2.0–3.0', 'Once a day', 'Long-term', '—', 'Label · US', ''),
    ('med_warfarin', 'adult', 4, 'Mechanical aortic valve (bileaflet, sinus rhythm)', 'PO', 'Dose to INR 2.0–3.0', 'Once a day', 'Long-term', '—', 'Label · US', ''),
    ('med_warfarin', 'adult', 5, 'Mechanical mitral or caged-ball/disk valve', 'PO', 'Dose to INR 2.5–3.5', 'Once a day', 'Long-term', '—', 'Label · US', ''),
    ('med_warfarin', 'adult', 6, 'Bioprosthetic mitral valve', 'PO', 'Dose to INR 2.0–3.0', 'Once a day', 'First 3 months', '—', 'Label · US', ''),
    ('med_warfarin', 'adult', 7, 'After high-risk MI', 'PO', 'Dose to INR 2.0–3.0', 'Once a day', '≥3 months', '—', 'Label · US', 'With aspirin ≤100 mg/day')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_warfarin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_warfarin', 'renal', 0, '', 'No dose adjustment; check INR more often. Watch kidney function if INR is high with blood in the urine (anticoagulant-related nephropathy).', 'Label · US'),
    ('med_warfarin', 'hepatic', 1, '', 'Liver impairment can increase warfarin''s effect; monitor more closely for bleeding.', 'Label · US'),
    ('med_warfarin', 'elderly', 2, '', 'Use lower starting and maintenance doses in elderly or debilitated patients and in Asian patients (US label). Age 65 or over is a bleeding risk factor.', 'Label · US'),
    ('med_warfarin', 'pregnancy', 3, '', 'Contraindicated except in women with mechanical valves at high thrombotic risk; first-trimester exposure causes embryopathy in about 5%. Check pregnancy status and use contraception during treatment and for 1 month after. Not found in breast milk in a small study; watch the infant for bruising.', 'Label · US'),
    ('med_warfarin', 'administration', 4, '', 'Take at the same time each day. Missed dose: take it the same day as soon as possible; do not double the next day''s dose.', 'Label · US'),
    ('med_warfarin', 'administration', 5, '', 'Surgery with severe bleeding risk: stop 3 days before; other surgery can proceed with INR <2.5. Dental extractions do not need warfarin stopped.', 'Label · UK SmPC'),
    ('med_warfarin', 'administration', 6, '', 'High INR or bleeding: INR 6–8 with no or minor bleeding, stop and restart when INR <5; INR >8, stop and give vitamin K 0.5–1 mg IV or 5 mg orally; life-threatening bleeding, prothrombin complex concentrate 30–50 units/kg (or FFP 15 mL/kg).', 'Label · UK SmPC'),
    ('med_warfarin', 'monitor', 7, '', 'INR daily after the first dose until stable in range, then every 1–4 weeks; recheck within 2–3 days of any dose change or when other drugs are started or stopped.', 'Label · US'),
    ('med_warfarin', 'monitor', 8, '', 'When overlapping with heparin, check INR at least 5 h after an IV bolus, 4 h after stopping an infusion or 24 h after a SC dose.', 'Label · US'),
    ('med_warfarin', 'monitor', 9, '', 'Check thyroid status when starting in hyper- or hypothyroidism; ask about bleeding, skin pain or purple toes at each visit.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_warfarin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_warfarin', 'Label · US', 'DailyMed (FDA label)', 'Warfarin sodium tablets. Prescribing information. Amneal Pharmaceuticals; revised 7/2026. DailyMed, U.S. National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=541c9a70-adaf-4ef3-94ba-ad4e70dfa057', 0),
    ('med_warfarin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Warfarin 5 mg tablets. Summary of Product Characteristics. Strides Pharma UK Ltd; 2022/2025.', 'https://products.mhra.gov.uk/search/?search=warfarin#emc-14333', 1)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_warfarin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_warfarin');


-- ================================================ med_zinc_sulfate  (Zinc Sulfate)
update public.medicines set description = 'Zinc is an essential trace element that serves as a cofactor for many enzymes and transcription factors involved in immunity, epithelial repair and growth. In acute diarrhea it inhibits several intracellular pathways of intestinal ion secretion (cAMP, calcium and nitric oxide) and supports mucosal recovery; WHO and UNICEF have recommended zinc with oral rehydration salts for all childhood diarrhea episodes since 2004. It is also used to correct zinc deficiency and, as zinc salts, in Wilson disease. Besides shortening and easing the current episode, a 10–14 day zinc course lowers the incidence of diarrhoea in the following 2–3 months (WHO/UNICEF 2004). In the Philippines, DOH Administrative Order No. 2007-0045 (17 December 2007) adopted zinc supplementation together with reformulated ORS for the management of diarrhoea in children. WHO-prequalified products include 20 mg dispersible tablets and a 10 mg/5 mL oral solution.', updated_at = now()
where id = 'med_zinc_sulfate' and description = 'Zinc is an essential trace element that serves as a cofactor for many enzymes and transcription factors involved in immunity, epithelial repair and growth. In acute diarrhea it inhibits several intracellular pathways of intestinal ion secretion (cAMP, calcium and nitric oxide) and supports mucosal recovery; WHO and UNICEF have recommended zinc with oral rehydration salts for all childhood diarrhea episodes since 2004. It is also used to correct zinc deficiency and, as zinc salts, in Wilson disease.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'WHO/UNICEF Joint Statement; WHO eLENA; WHO Prequalification (WHOPAR product information); Department of Health (Philippines); MOST / USAID; WHO Prequalification (WHOPAR)' else source_attribution || '; WHO/UNICEF Joint Statement; WHO eLENA; WHO Prequalification (WHOPAR product information); Department of Health (Philippines); MOST / USAID; WHO Prequalification (WHOPAR)' end
where id = 'med_zinc_sulfate' and position('WHO/UNICEF Joint Statement' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_zinc_sulfate', 'indication', 'Bloody diarrhoea (dysentery) in children, given as for watery diarrhoea alongside antibiotics', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'indication' and content = 'Bloody diarrhoea (dysentery) in children, given as for watery diarrhoea alongside antibiotics');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_zinc_sulfate', 'adverse', 'Headache, irritability and lethargy (frequency not known)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'adverse' and content = 'Headache, irritability and lethargy (frequency not known)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_zinc_sulfate', 'adverse', 'Gastric irritation and gastritis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'adverse' and content = 'Gastric irritation and gastritis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_zinc_sulfate', 'contraindication', 'Copper deficiency', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'contraindication' and content = 'Copper deficiency');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_zinc_sulfate', 'contraindication', 'Hereditary fructose intolerance with sorbitol-containing oral solutions', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'contraindication' and content = 'Hereditary fructose intolerance with sorbitol-containing oral solutions');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_zinc_sulfate', 'interaction', 'Calcium salts, oral iron and trientine: mutual reduction in absorption; separate doses.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'interaction' and content = 'Calcium salts, oral iron and trientine: mutual reduction in absorption; separate doses.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_zinc_sulfate', 'interaction', 'Copper: zinc inhibits copper absorption.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_zinc_sulfate' and kind = 'interaction' and content = 'Copper: zinc inhibits copper absorption.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_zinc_sulfate', 'WHO/UNICEF Joint Statement', 'World Health Organization, UNICEF. Clinical Management of Acute Diarrhoea: WHO/UNICEF Joint Statement. WHO/FCH/CAH/04.7; May 2004.', 'https://stg.nutritioncluster.net/sites/nutritioncluster.com/files/2019-12/WHO_FCH_CAH_04.71.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate' and url = 'https://stg.nutritioncluster.net/sites/nutritioncluster.com/files/2019-12/WHO_FCH_CAH_04.71.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_zinc_sulfate', 'WHO eLENA', 'Khan WU, Sellen DW. Zinc supplementation in the management of diarrhoea: biological, behavioural and contextual rationale. WHO e-Library of Evidence for Nutrition Actions (eLENA); April 2011.', 'https://www.who.int/tools/elena/bbc/zinc-diarrhoea', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate' and url = 'https://www.who.int/tools/elena/bbc/zinc-diarrhoea');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_zinc_sulfate', 'WHO Prequalification (WHOPAR product information)', 'World Health Organization Prequalification Unit. Zinc (as sulfate monohydrate) 10 mg/5 mL oral solution, PharmEvo (DI010): Summary of Product Characteristics, WHOPAR part 4; revised June 2025.', 'https://extranet.who.int/prequal/sites/default/files/whopar_files/DI010part4v2.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate' and url = 'https://extranet.who.int/prequal/sites/default/files/whopar_files/DI010part4v2.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_zinc_sulfate', 'Department of Health (Philippines)', 'Department of Health. Administrative Order No. 2007-0045: Zinc Supplementation and Reformulated Oral Rehydration Salt in the Management of Diarrhea Among Children. Adopted 17 December 2007. National Administrative Register Vol. 19 No. 1 (Jan–Mar 2008), Supreme Court E-Library.', 'https://elibrary.judiciary.gov.ph/thebookshelf/showdocsfriendly/10/52204', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate' and url = 'https://elibrary.judiciary.gov.ph/thebookshelf/showdocsfriendly/10/52204');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_zinc_sulfate', 'MOST / USAID', 'MOST, the USAID Micronutrient Program. Diarrhoea Treatment Guidelines including new recommendations for the use of ORS and zinc supplementation for clinic-based healthcare workers. Arlington, VA; January 2005.', 'https://cdn.who.int/media/docs/default-source/2021-dha-docs/pnadk428.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_zinc_sulfate' and url = 'https://cdn.who.int/media/docs/default-source/2021-dha-docs/pnadk428.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_gastroenteritis', 'med_zinc_sulfate', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis'), 0), 'safe'::condition_safety, 'Zinc with low-osmolarity ORS is recommended for all children with acute diarrhoea (WHO/UNICEF 2004).'
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis' and medicine_id = 'med_zinc_sulfate');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_zinc_sulfate', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Zinc may accumulate in renal failure (WHO-prequalified product information).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_zinc_sulfate');
-- med_zinc_sulfate
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_zinc_sulfate', 'child', 0, 'Acute or persistent diarrhoea, <6 months', 'PO', '10 mg elemental zinc', 'Once a day', '10–14 days', '—', 'WHO/UNICEF 2004', '= ½ × 20 mg tablet or 5 mL of 10 mg/5 mL solution'),
    ('med_zinc_sulfate', 'child', 1, 'Acute or persistent diarrhoea, 6 months–5 y', 'PO', '20 mg elemental zinc', 'Once a day', '10–14 days', '—', 'WHO/UNICEF 2004', '= 1 × 20 mg tablet or 10 mL of 10 mg/5 mL solution'),
    ('med_zinc_sulfate', 'child', 2, 'Dysentery (bloody diarrhoea)', 'PO', 'Same as acute diarrhoea by age', 'Once a day', '10–14 days', '—', 'MOST 2005', 'Give antibiotic for Shigella separately')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_zinc_sulfate');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_zinc_sulfate', 'renal', 0, '', 'Zinc may accumulate in renal failure.', 'Label · WHO PQ'),
    ('med_zinc_sulfate', 'pregnancy', 1, '', 'Limited human data; animal studies show no reproductive toxicity at the therapeutic dose. Zinc is present in breast milk.', 'Label · WHO PQ'),
    ('med_zinc_sulfate', 'administration', 2, '', 'Give between meals. If the child vomits within 30 minutes, repeat the dose. Missed dose: give as soon as possible unless the next is due within 6 hours.', 'Label · WHO PQ'),
    ('med_zinc_sulfate', 'administration', 3, '', 'Dispersible tablet: dissolve in about 5 mL of expressed breast milk, ORS or clean water on a small spoon for infants; older children may chew it. Finish all 10–14 days even after diarrhoea stops.', 'MOST 2005'),
    ('med_zinc_sulfate', 'administration', 4, '', 'Oral solution excipients: aspartame (avoid in phenylketonuria), sodium benzoate (may worsen newborn jaundice) and sorbitol (mild laxative effect). Discard 28 days after opening.', 'Label · WHO PQ'),
    ('med_zinc_sulfate', 'monitor', 5, '', 'Ask about vomiting after doses; if the child vomits ORS, food and fluids, bring to a health facility rather than continuing zinc at home.', 'MOST 2005')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_zinc_sulfate');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_zinc_sulfate', 'WHO/UNICEF 2004', 'WHO/UNICEF Joint Statement', 'World Health Organization, UNICEF. Clinical Management of Acute Diarrhoea. WHO/FCH/CAH/04.7; 2004.', 'https://stg.nutritioncluster.net/sites/nutritioncluster.com/files/2019-12/WHO_FCH_CAH_04.71.pdf', 0),
    ('med_zinc_sulfate', 'Label · WHO PQ', 'WHO Prequalification (WHOPAR)', 'Zinc (as sulfate monohydrate) 10 mg/5 mL oral solution (DI010), SmPC; June 2025.', 'https://extranet.who.int/prequal/sites/default/files/whopar_files/DI010part4v2.pdf', 1),
    ('med_zinc_sulfate', 'MOST 2005', 'MOST / USAID', 'Diarrhoea Treatment Guidelines including new recommendations for the use of ORS and zinc supplementation. MOST, USAID Micronutrient Program; 2005.', 'https://cdn.who.int/media/docs/default-source/2021-dha-docs/pnadk428.pdf', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_zinc_sulfate')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_zinc_sulfate');


update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
