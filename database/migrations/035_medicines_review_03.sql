-- 035_medicines_review_03.sql  -  medicine review b03: med_dexamethasone, med_doxycycline, med_enalapril, med_entecavir, med_ethambutol, med_famotidine, med_ferrous_sulfate, med_furosemide, med_gliclazide, med_hydrochlorothiazide
-- Adds only: longer descriptions, new facts, references, disease links, and dosage
-- tables (for medicines that have none yet). Nothing is deleted or reworded.
-- Needs 030_medicine_doses.sql first. Safe to run twice (every insert is guarded).

begin;

-- ================================================ med_dexamethasone  (Dexamethasone)
update public.medicines set description = 'Dexamethasone is a potent, long-acting glucocorticoid with almost no mineralocorticoid effect. It suppresses inflammatory gene transcription and cytokine release. In bacterial meningitis, given just before or with the first antibiotic dose, it reduces inflammation-driven brain injury, hearing loss and death, with the clearest benefit in pneumococcal meningitis. Dexamethasone also induces CYP3A4, so it can lower levels of drugs such as indinavir, saquinavir and erythromycin. WHO recommends low-dose corticosteroids for 7–10 days only in severe or critical COVID-19 and advises against them in non-severe disease. In the Philippines, the PNF lists 500 microgram, 750 microgram, 3 mg and 4 mg tablets, 4 mg/mL and 5 mg/mL injections (as sodium phosphate, IM/IV) and 0.1% eye drops.', updated_at = now()
where id = 'med_dexamethasone' and description = 'Dexamethasone is a potent, long-acting glucocorticoid with almost no mineralocorticoid effect. It suppresses inflammatory gene transcription and cytokine release. In bacterial meningitis, given just before or with the first antibiotic dose, it reduces inflammation-driven brain injury, hearing loss and death, with the clearest benefit in pneumococcal meningitis.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc) – tablets; UK SmPC (emc) – injection; Merck Manual Professional – Acute bacterial meningitis; WHO – COVID-19 corticosteroids Q&A; Canadian Paediatric Society – Croup; Philippine National Formulary – Essential Medicines List; UK SmPC – Dexamethasone Tablets BP 2.0 mg; UK SmPC – Dexamethasone 3.3 mg/ml Solution for Injection; Merck Manual Professional – Acute Bacterial Meningitis; Merck Manual Professional – Preterm Labor; Canadian Paediatric Society – Acute management of croup; WHO – COVID-19: Corticosteroids, including dexamethasone' else source_attribution || '; UK SmPC (emc) – tablets; UK SmPC (emc) – injection; Merck Manual Professional – Acute bacterial meningitis; WHO – COVID-19 corticosteroids Q&A; Canadian Paediatric Society – Croup; Philippine National Formulary – Essential Medicines List; UK SmPC – Dexamethasone Tablets BP 2.0 mg; UK SmPC – Dexamethasone 3.3 mg/ml Solution for Injection; Merck Manual Professional – Acute Bacterial Meningitis; Merck Manual Professional – Preterm Labor; Canadian Paediatric Society – Acute management of croup; WHO – COVID-19: Corticosteroids, including dexamethasone' end
where id = 'med_dexamethasone' and position('UK SmPC (emc) – tablets' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'indication', 'Dexamethasone suppression test (investigation of Cushing''s syndrome)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'indication' and content = 'Dexamethasone suppression test (investigation of Cushing''s syndrome)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'indication', 'Adjunct in haemorrhagic, traumatic or surgical shock', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'indication' and content = 'Adjunct in haemorrhagic, traumatic or surgical shock');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'indication', 'Intra-articular and soft-tissue injection', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'indication' and content = 'Intra-articular and soft-tissue injection');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'indication', 'Palliative care (subcutaneous injection or infusion)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'indication' and content = 'Palliative care (subcutaneous injection or infusion)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'adverse', 'Severe psychiatric reactions, including psychosis, sometimes during dose tapering', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse' and content = 'Severe psychiatric reactions, including psychosis, sometimes during dose tapering');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'adverse', 'Cataract, glaucoma and central serous chorioretinopathy (blurred vision)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse' and content = 'Cataract, glaucoma and central serous chorioretinopathy (blurred vision)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'adverse', 'Growth retardation in children (dose-related, may be irreversible)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse' and content = 'Growth retardation in children (dose-related, may be irreversible)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'adverse', 'Acute adrenal insufficiency on abrupt withdrawal after prolonged use', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse' and content = 'Acute adrenal insufficiency on abrupt withdrawal after prolonged use');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'adverse', 'Hypertension and hypokalaemia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse' and content = 'Hypertension and hypokalaemia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'adverse', 'Burning or tingling in the perineal area after IV injection', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'adverse' and content = 'Burning or tingling in the perineal area after IV injection');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'contraindication', 'Systemic infection unless specific anti-infective therapy is given', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication' and content = 'Systemic infection unless specific anti-infective therapy is given');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'contraindication', 'Chickenpox or measles exposure in non-immune patients: risk of severe disease; needs immunoglobulin (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication' and content = 'Chickenpox or measles exposure in non-immune patients: risk of severe disease; needs immunoglobulin (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'contraindication', 'Amoebiasis and other parasitic infestations (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication' and content = 'Amoebiasis and other parasitic infestations (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'contraindication', 'Recent myocardial infarction: risk of myocardial rupture (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication' and content = 'Recent myocardial infarction: risk of myocardial rupture (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'contraindication', 'Phaeochromocytoma: may trigger crisis (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'contraindication' and content = 'Phaeochromocytoma: may trigger crisis (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'interaction', 'Ritonavir and cobicistat: raise corticosteroid levels and side effects; avoid unless benefit outweighs risk.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction' and content = 'Ritonavir and cobicistat: raise corticosteroid levels and side effects; avoid unless benefit outweighs risk.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'interaction', 'Indinavir, saquinavir and erythromycin: levels lowered by dexamethasone (CYP3A4 induction).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction' and content = 'Indinavir, saquinavir and erythromycin: levels lowered by dexamethasone (CYP3A4 induction).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'interaction', 'Phenobarbital, primidone, rifabutin and ephedrine: reduce dexamethasone effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction' and content = 'Phenobarbital, primidone, rifabutin and ephedrine: reduce dexamethasone effect.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'interaction', 'Loop and thiazide diuretics, acetazolamide: enhanced hypokalaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction' and content = 'Loop and thiazide diuretics, acetazolamide: enhanced hypokalaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'interaction', 'Antihypertensives and diuretics: effects antagonised.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction' and content = 'Antihypertensives and diuretics: effects antagonised.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'interaction', 'Methotrexate: increased haematological toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction' and content = 'Methotrexate: increased haematological toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'interaction', 'Salicylates: renal clearance increased; salicylate toxicity possible when the steroid is stopped.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction' and content = 'Salicylates: renal clearance increased; salicylate toxicity possible when the steroid is stopped.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'interaction', 'Antacids (especially magnesium trisilicate): reduce absorption; space doses apart.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction' and content = 'Antacids (especially magnesium trisilicate): reduce absorption; space doses apart.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dexamethasone', 'interaction', 'Anticholinesterases: effect antagonised in myasthenia gravis.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone' and kind = 'interaction' and content = 'Anticholinesterases: effect antagonised in myasthenia gravis.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_dexamethasone', 'UK SmPC (emc) – tablets', 'Dexamethasone Tablets BP 2.0 mg – Summary of Product Characteristics. Aspen Pharma Trading Limited (PL 39699/0056). Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=dexamethasone#emc-5411', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_dexamethasone'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_dexamethasone' and url = 'https://products.mhra.gov.uk/search/?search=dexamethasone#emc-5411');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_dexamethasone', 'UK SmPC (emc) – injection', 'Dexamethasone 3.3 mg/ml Solution for Injection – Summary of Product Characteristics. hameln pharma ltd (PL 01502/0079). Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=dexamethasone#emc-4659', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_dexamethasone'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_dexamethasone' and url = 'https://products.mhra.gov.uk/search/?search=dexamethasone#emc-4659');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_dexamethasone', 'Merck Manual Professional – Acute bacterial meningitis', 'Merck Manual Professional Version. Acute Bacterial Meningitis.', 'https://www.merckmanuals.com/professional/neurologic-disorders/meningitis/acute-bacterial-meningitis', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_dexamethasone'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_dexamethasone' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/meningitis/acute-bacterial-meningitis');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_dexamethasone', 'WHO – COVID-19 corticosteroids Q&A', 'World Health Organization. Coronavirus disease (COVID-19): Corticosteroids, including dexamethasone. Questions and answers.', 'https://www.who.int/news-room/questions-and-answers/item/coronavirus-disease-covid-19-dexamethasone', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_dexamethasone'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_dexamethasone' and url = 'https://www.who.int/news-room/questions-and-answers/item/coronavirus-disease-covid-19-dexamethasone');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_dexamethasone', 'Canadian Paediatric Society – Croup', 'Ortiz-Alvarez O; Canadian Paediatric Society, Acute Care Committee. Acute management of croup in the emergency department. Position statement, 2017 (updated 2026).', 'https://cps.ca/documents/position/acute-management-of-croup', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_dexamethasone'), 0)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_dexamethasone' and url = 'https://cps.ca/documents/position/acute-management-of-croup');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'covid19', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'covid19'), 0), 'safe'::condition_safety, 'WHO: recommended for severe or critical COVID-19 for 7–10 days; should not be given in non-severe COVID-19'
where exists (select 1 from public.diseases where id = 'covid19')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'covid19' and medicine_id = 'med_dexamethasone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'UK label: frequent monitoring in diabetes; antagonises insulin and oral hypoglycaemics'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_dexamethasone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hypertension', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hypertension'), 0), 'caution'::condition_safety, 'UK label: frequent monitoring in hypertension; antagonises antihypertensives'
where exists (select 1 from public.diseases where id = 'hypertension')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hypertension' and medicine_id = 'med_dexamethasone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'UK label: frequent monitoring in congestive heart failure'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_dexamethasone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'tuberculosis', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'tuberculosis'), 0), 'caution'::condition_safety, 'UK label: frequent monitoring with a history of tuberculosis'
where exists (select 1 from public.diseases where id = 'tuberculosis')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'tuberculosis' and medicine_id = 'med_dexamethasone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'peptic_ulcer_disease', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease'), 0), 'caution'::condition_safety, 'UK label: frequent monitoring in peptic ulceration'
where exists (select 1 from public.diseases where id = 'peptic_ulcer_disease')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease' and medicine_id = 'med_dexamethasone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'UK label: frequent monitoring in renal insufficiency (no dose change needed)'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_dexamethasone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'varicella', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'varicella'), 0), 'caution'::condition_safety, 'UK label: chickenpox can be fatal in immunosuppressed patients; non-immune exposed patients need VZIG within 10 days'
where exists (select 1 from public.diseases where id = 'varicella')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'varicella' and medicine_id = 'med_dexamethasone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'measles', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'measles'), 0), 'caution'::condition_safety, 'UK label: avoid exposure; exposed patients may need IM normal immunoglobulin'
where exists (select 1 from public.diseases where id = 'measles')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'measles' and medicine_id = 'med_dexamethasone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_coronary_syndrome', 'med_dexamethasone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome'), 0), 'caution'::condition_safety, 'UK label: caution after recent myocardial infarction (myocardial rupture reported)'
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome' and medicine_id = 'med_dexamethasone');
-- med_dexamethasone
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_dexamethasone', 'adult', 0, 'General glucocorticoid use', 'PO', '0.5–10 mg/day', 'Once a day or divided', 'As short as possible', '—', 'Label · UK SmPC tabs', 'Taper to lowest effective dose; stop if no response within a few days'),
    ('med_dexamethasone', 'adult', 1, 'Bacterial meningitis (adjunct)', 'IV', '10 mg', 'Every 6 h', '4 days', '—', 'Merck Manual', 'First dose just before or with the first antibiotic dose'),
    ('med_dexamethasone', 'adult', 2, 'COVID-19 needing oxygen', 'PO', '6 mg', 'Once a day', 'Up to 10 days', '—', 'Label · UK SmPC tabs', 'WHO: severe/critical only, 7–10 days'),
    ('med_dexamethasone', 'adult', 3, 'COVID-19 needing oxygen', 'IV', '6 mg', 'Once a day', 'Up to 10 days', '—', 'Label · UK SmPC inj', ''),
    ('med_dexamethasone', 'adult', 4, 'Cerebral oedema (tumour, pre-op)', 'IV', '8.3 mg, then 3.3 mg IM', 'Every 6 h (IM)', 'Reduce after 2–4 days; stop over 5–7 days', '—', 'Label · UK SmPC inj', 'Dose as dexamethasone base'),
    ('med_dexamethasone', 'adult', 5, 'Emergency use', 'IV', '3.3–16.6 mg', 'Repeat until response', 'Short term', '66.4 mg/day', 'Label · UK SmPC inj', 'IV only in shock; IM possible otherwise; dose as base'),
    ('med_dexamethasone', 'adult', 6, 'Shock (haemorrhagic, traumatic, surgical)', 'IV', '1.7–5 mg/kg', 'Single dose; repeat in 2–6 h if needed', 'Usually ≤48–72 h', '—', 'Label · UK SmPC inj', 'Adjunct to standard therapy'),
    ('med_dexamethasone', 'adult', 7, 'Palliative care', 'SC', '4–16 mg/24 h', 'Injection or continuous infusion', 'As needed', '—', 'Label · UK SmPC inj', ''),
    ('med_dexamethasone', 'adult', 8, 'Antenatal lung maturation (24–34 weeks)', 'IM', '6 mg', 'Every 12 h', '4 doses', '—', 'Merck Manual (obstetrics)', 'Repeat course may be considered if <34 weeks and ≥7 days since last'),
    ('med_dexamethasone', 'adult', 9, 'Dexamethasone suppression test (short)', 'PO', '1 mg', 'Once at 11 pm', 'Once', '—', 'Label · UK SmPC tabs', 'Measure plasma cortisol the next morning'),
    ('med_dexamethasone', 'child', 10, 'General glucocorticoid use', 'PO', '0.01–0.1 mg/kg/day', 'Once a day or divided', 'As short as possible', '—', 'Label · UK SmPC tabs', ''),
    ('med_dexamethasone', 'child', 11, 'Bacterial meningitis (adjunct)', 'IV', '0.15 mg/kg', 'Every 6 h', '4 days', '—', 'Merck Manual', 'First dose just before or with the first antibiotic dose'),
    ('med_dexamethasone', 'child', 12, 'Croup (mild to severe)', 'PO', '0.6 mg/kg', 'Single dose', 'Once', '—', 'CPS', 'IM if persistent vomiting or marked respiratory distress'),
    ('med_dexamethasone', 'child', 13, 'COVID-19 needing oxygen (≥12 y and ≥40 kg)', 'PO', '6 mg', 'Once a day', 'Up to 10 days', '—', 'Label · UK SmPC tabs', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_dexamethasone');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_dexamethasone', 'renal', 0, '', 'No dose adjustment, but monitor frequently in renal insufficiency.', 'Label · UK SmPC tabs'),
    ('med_dexamethasone', 'hepatic', 1, '', 'No dose adjustment, but monitor frequently in liver failure.', 'Label · UK SmPC tabs'),
    ('med_dexamethasone', 'elderly', 2, '', 'Osteoporosis, hypertension, hypokalaemia, diabetes, infection and skin thinning may be more serious; plan long-term use carefully under close supervision.', 'Label · UK SmPC tabs'),
    ('med_dexamethasone', 'pregnancy', 3, '', 'Crosses the placenta; no rise in birth defects seen, but prolonged or repeated use may increase intrauterine growth restriction and neonatal hypoadrenalism is possible. Infants of mothers on high, prolonged doses may have some adrenal suppression.', 'Label · UK SmPC tabs'),
    ('med_dexamethasone', 'administration', 4, '', 'After prolonged use, taper gradually; consider gradual withdrawal after repeated courses, doses over 6 mg/day, evening dosing or more than 3 weeks of treatment.', 'Label · UK SmPC tabs'),
    ('med_dexamethasone', 'administration', 5, '', 'UK injection doses are given as dexamethasone base (3.3 mg base = 4 mg dexamethasone phosphate); Philippine products are labelled as sodium phosphate, so check the label. Max 2 mL IM per site; may be added to sodium chloride or dextrose infusion; use with caution at high doses in children under 5 (propylene glycol).', 'Label · UK SmPC inj'),
    ('med_dexamethasone', 'forms_ph', 6, '', 'Oral: 500 microgram, 750 microgram, 3 mg and 4 mg tablet. Injection (IM/IV, as sodium phosphate): 4 mg/mL in 1 mL and 2 mL ampoule/vial; 5 mg/mL in 1 mL ampoule. Eye drops suspension: 0.1%, 5 mL.', 'PNF'),
    ('med_dexamethasone', 'monitor', 7, '', 'Blood glucose, blood pressure and potassium; mood and psychiatric symptoms (warn patient and carers); blurred vision (refer to eye specialist); growth in children; signs of infection, which may be masked; INR with coumarin anticoagulants.', 'Label · UK SmPC tabs')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_dexamethasone');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_dexamethasone', 'PNF', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 0),
    ('med_dexamethasone', 'Label · UK SmPC tabs', 'UK SmPC – Dexamethasone Tablets BP 2.0 mg', 'Aspen Pharma Trading Ltd. Dexamethasone Tablets BP 2.0 mg – Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=dexamethasone#emc-5411', 1),
    ('med_dexamethasone', 'Label · UK SmPC inj', 'UK SmPC – Dexamethasone 3.3 mg/ml Solution for Injection', 'hameln pharma ltd. Dexamethasone 3.3 mg/ml Solution for Injection – Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=dexamethasone#emc-4659', 2),
    ('med_dexamethasone', 'Merck Manual', 'Merck Manual Professional – Acute Bacterial Meningitis', 'Merck Manual Professional Version. Acute Bacterial Meningitis.', 'https://www.merckmanuals.com/professional/neurologic-disorders/meningitis/acute-bacterial-meningitis', 3),
    ('med_dexamethasone', 'Merck Manual (obstetrics)', 'Merck Manual Professional – Preterm Labor', 'Merck Manual Professional Version. Preterm Labor.', 'https://www.merckmanuals.com/professional/gynecology-and-obstetrics/abnormalities-and-complications-of-labor-and-delivery/preterm-labor', 4),
    ('med_dexamethasone', 'CPS', 'Canadian Paediatric Society – Acute management of croup', 'Ortiz-Alvarez O; CPS Acute Care Committee. Acute management of croup in the emergency department. 2017 (updated 2026).', 'https://cps.ca/documents/position/acute-management-of-croup', 5),
    ('med_dexamethasone', 'WHO', 'WHO – COVID-19: Corticosteroids, including dexamethasone', 'World Health Organization. Coronavirus disease (COVID-19): Corticosteroids, including dexamethasone. Q&A.', 'https://www.who.int/news-room/questions-and-answers/item/coronavirus-disease-covid-19-dexamethasone', 6)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_dexamethasone')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_dexamethasone');


-- ================================================ med_doxycycline  (Doxycycline)
update public.medicines set description = 'Doxycycline binds the 30S ribosomal subunit and blocks aminoacyl-tRNA binding, inhibiting bacterial protein synthesis (bacteriostatic). It is used for rickettsial infections, leptospirosis, atypical pneumonia, chlamydia, Lyme disease, acne and malaria prophylaxis. Oral doxycycline is virtually completely absorbed, and food or milk does not notably reduce absorption. About 40% is excreted in the urine over 72 hours, falling to 1–5% in severe renal failure, but its serum half-life does not change, which is why no renal dose adjustment is needed. In the Philippines it is the first-line drug for mild leptospirosis and for leptospirosis prophylaxis graded by exposure risk (PhilHealth policy recommendations), and the PNF lists it as a 100 mg capsule (as hyclate).', updated_at = now()
where id = 'med_doxycycline' and description = 'Doxycycline binds the 30S ribosomal subunit and blocks aminoacyl-tRNA binding, inhibiting bacterial protein synthesis (bacteriostatic). It is used for rickettsial infections, leptospirosis, atypical pneumonia, chlamydia, Lyme disease, acne and malaria prophylaxis.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); PhilHealth – Leptospirosis policy recommendations; CDC – Rocky Mountain spotted fever; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; UK SmPC – Doxycycline 100 mg Capsules; CDC – Clinical Care of Rocky Mountain Spotted Fever' else source_attribution || '; UK SmPC (emc); PhilHealth – Leptospirosis policy recommendations; CDC – Rocky Mountain spotted fever; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; UK SmPC – Doxycycline 100 mg Capsules; CDC – Clinical Care of Rocky Mountain Spotted Fever' end
where id = 'med_doxycycline' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'indication', 'Chloroquine-resistant falciparum malaria (treatment, with a fast-acting schizonticide such as quinine)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication' and content = 'Chloroquine-resistant falciparum malaria (treatment, with a fast-acting schizonticide such as quinine)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'indication', 'Prevention of scrub typhus', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication' and content = 'Prevention of scrub typhus');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'indication', 'Prevention of travellers'' diarrhoea', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication' and content = 'Prevention of travellers'' diarrhoea');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'indication', 'Louse- and tick-borne relapsing fever', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication' and content = 'Louse- and tick-borne relapsing fever');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'indication', 'Primary and secondary syphilis in non-pregnant patients allergic to penicillin', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication' and content = 'Primary and secondary syphilis in non-pregnant patients allergic to penicillin');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'indication', 'Epididymo-orchitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'indication' and content = 'Epididymo-orchitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'adverse', 'Anaphylaxis and angioedema', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse' and content = 'Anaphylaxis and angioedema');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'adverse', 'SJS, TEN and DRESS (stop immediately)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse' and content = 'SJS, TEN and DRESS (stop immediately)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'adverse', 'Photo-onycholysis (nail separation with sun exposure)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse' and content = 'Photo-onycholysis (nail separation with sun exposure)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'adverse', 'Pancreatitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse' and content = 'Pancreatitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'adverse', 'Haemolytic anaemia, neutropenia, thrombocytopenia and eosinophilia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse' and content = 'Haemolytic anaemia, neutropenia, thrombocytopenia and eosinophilia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'adverse', 'Jarisch-Herxheimer reaction when treating spirochaete infections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse' and content = 'Jarisch-Herxheimer reaction when treating spirochaete infections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'adverse', 'Candida overgrowth and vaginal infection', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'adverse' and content = 'Candida overgrowth and vaginal infection');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'contraindication', 'Pregnancy (UK label)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication' and content = 'Pregnancy (UK label)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'contraindication', 'Breastfeeding (passes into breast milk)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication' and content = 'Breastfeeding (passes into breast milk)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'contraindication', 'Children under 8 years, because of tooth discolouration (UK label; CDC still recommends it for rickettsial disease at all ages)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication' and content = 'Children under 8 years, because of tooth discolouration (UK label; CDC still recommends it for rickettsial disease at all ages)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'contraindication', 'Myasthenia gravis: possible weak neuromuscular blockade (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication' and content = 'Myasthenia gravis: possible weak neuromuscular blockade (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'contraindication', 'Systemic lupus erythematosus: may worsen (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'contraindication' and content = 'Systemic lupus erythematosus: may worsen (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'interaction', 'Oral zinc: impairs absorption; separate doses as much as possible.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction' and content = 'Oral zinc: impairs absorption; separate doses as much as possible.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'interaction', 'Ciclosporin: levels may rise; monitor.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction' and content = 'Ciclosporin: levels may rise; monitor.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'interaction', 'Methoxyflurane: renal failure reported with concurrent use.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction' and content = 'Methoxyflurane: renal failure reported with concurrent use.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'interaction', 'Alcohol: may shorten doxycycline half-life.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction' and content = 'Alcohol: may shorten doxycycline half-life.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_doxycycline', 'interaction', 'Lab tests: can falsely raise urinary catecholamines (fluorescence assay).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_doxycycline' and kind = 'interaction' and content = 'Lab tests: can falsely raise urinary catecholamines (fluorescence assay).');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_doxycycline', 'UK SmPC (emc)', 'Doxycycline 100 mg Capsules – Summary of Product Characteristics. Waymade Plc trading as Sovereign Medical (PL 06464/3108). Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=doxycycline#emc-13082', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_doxycycline'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_doxycycline' and url = 'https://products.mhra.gov.uk/search/?search=doxycycline#emc-13082');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_doxycycline', 'PhilHealth – Leptospirosis policy recommendations', 'Philippine Health Insurance Corporation. Policy Recommendations on the Diagnosis, Management and Prevention of Leptospirosis (based on the 2010 Leptospirosis Task Force CPG; c. 2012).', 'https://www.philhealth.gov.ph/partners/providers/pdf/Leptospirosis_Policy_Statements.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_doxycycline'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_doxycycline' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/Leptospirosis_Policy_Statements.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_doxycycline', 'CDC – Rocky Mountain spotted fever', 'Centers for Disease Control and Prevention. Clinical Care of Rocky Mountain Spotted Fever. CDC.', 'https://www.cdc.gov/rocky-mountain-spotted-fever/hcp/clinical-care/', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_doxycycline'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_doxycycline' and url = 'https://www.cdc.gov/rocky-mountain-spotted-fever/hcp/clinical-care/');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_doxycycline', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_doxycycline'), 0)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_doxycycline' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_doxycycline', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'safe'::condition_safety, 'UK label: no renal dose adjustment; half-life unchanged in severe renal impairment and by haemodialysis'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_doxycycline');
-- med_doxycycline
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_doxycycline', 'adult', 0, 'Most infections', 'PO', '200 mg on day 1, then 100 mg', 'Once a day', 'Per infection', '—', 'Label · UK SmPC', 'Also for ages 12 to under 18'),
    ('med_doxycycline', 'adult', 1, 'Severe infections', 'PO', '200 mg', 'Once a day', 'Per infection', '—', 'Label · UK SmPC', ''),
    ('med_doxycycline', 'adult', 2, 'Leptospirosis, mild (treatment)', 'PO', '100 mg', '2× a day', '—', '—', 'PhilHealth 2012', 'First-line; duration not stated in the policy'),
    ('med_doxycycline', 'adult', 3, 'Leptospirosis PEP, low risk (single wading, no wounds)', 'PO', '200 mg', 'Single dose', 'Once', '—', 'PhilHealth 2012', 'Give within 24–72 h of exposure'),
    ('med_doxycycline', 'adult', 4, 'Leptospirosis PEP, moderate risk (wounds or swallowed water)', 'PO', '200 mg', 'Once a day', '3–5 days', '—', 'PhilHealth 2012', 'Start within 24–72 h of exposure'),
    ('med_doxycycline', 'adult', 5, 'Leptospirosis PEP, high risk (continuous exposure)', 'PO', '200 mg', 'Once a week', 'Until exposure ends', '—', 'PhilHealth 2012', 'E.g. living in flooded areas, rescuers'),
    ('med_doxycycline', 'adult', 6, 'Leptospirosis pre-exposure prophylaxis', 'PO', '200 mg', 'Once a week', 'Through exposure', '—', 'PhilHealth 2012', 'Not routine; start 1–2 days before; non-pregnant, non-lactating adults'),
    ('med_doxycycline', 'adult', 7, 'Chlamydia, gonorrhoea, Ureaplasma', 'PO', '100 mg', '2× a day', '7 days', '—', 'Label · UK SmPC', ''),
    ('med_doxycycline', 'adult', 8, 'Epididymo-orchitis', 'PO', '100 mg', '2× a day', '10 days', '—', 'Label · UK SmPC', ''),
    ('med_doxycycline', 'adult', 9, 'Primary/secondary syphilis (penicillin allergy)', 'PO', '200 mg', '2× a day', '2 weeks', '—', 'Label · UK SmPC', 'Non-pregnant patients only'),
    ('med_doxycycline', 'adult', 10, 'Chloroquine-resistant falciparum malaria', 'PO', '200 mg', 'Once a day', 'At least 7 days', '—', 'Label · UK SmPC', 'With a fast-acting schizonticide such as quinine'),
    ('med_doxycycline', 'adult', 11, 'Malaria prophylaxis', 'PO', '100 mg', 'Once a day', '1–2 days before to 4 weeks after', '—', 'Label · UK SmPC', 'Also for children over 12; check current guidance'),
    ('med_doxycycline', 'adult', 12, 'Rickettsial infection (spotted fever)', 'PO', '100 mg', 'Every 12 h', 'At least 5–7 days', '—', 'CDC', 'Continue ≥3 days after fever resolves and until improvement'),
    ('med_doxycycline', 'adult', 13, 'Scrub typhus prevention', 'PO', '200 mg', 'Single dose', 'Once', '—', 'Label · UK SmPC', ''),
    ('med_doxycycline', 'adult', 14, 'Relapsing fever (louse- or tick-borne)', 'PO', '100–200 mg', 'Single dose', 'Once', '—', 'Label · UK SmPC', ''),
    ('med_doxycycline', 'adult', 15, 'Acne vulgaris', 'PO', '50 mg', 'Once a day', '6–12 weeks', '—', 'Label · UK SmPC', 'With food or fluid'),
    ('med_doxycycline', 'child', 16, 'Most infections, 8 to under 12 y, ≤45 kg', 'PO', '4.4 mg/kg on day 1, then 2.2 mg/kg', 'Once a day', 'Per infection', '4.4 mg/kg/day', 'Label · UK SmPC', 'Only if other drugs unsuitable; up to 4.4 mg/kg/day if severe; >45 kg: adult dose'),
    ('med_doxycycline', 'child', 17, 'Rickettsial infection (spotted fever), <45 kg', 'PO', '2.2 mg/kg', '2× a day', 'At least 5–7 days', '—', 'CDC', 'CDC: all ages, including under 8; ≥45 kg: adult dose')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_doxycycline');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_doxycycline', 'renal', 0, '', 'No dose adjustment; half-life is not significantly changed in severe renal impairment and is not altered by haemodialysis.', 'Label · UK SmPC'),
    ('med_doxycycline', 'hepatic', 1, '', 'Use with caution, especially with other potentially hepatotoxic drugs; rare hepatic abnormalities reported.', 'Label · UK SmPC'),
    ('med_doxycycline', 'elderly', 2, '', 'Usual doses; no special precautions.', 'Label · UK SmPC'),
    ('med_doxycycline', 'pregnancy', 3, '', 'UK label: contraindicated in pregnancy and breastfeeding (effects on teeth and skeletal development).', 'Label · UK SmPC'),
    ('med_doxycycline', 'pregnancy', 4, '', 'CDC still recommends doxycycline for presumed rickettsial disease in pregnancy after counselling on risks and benefits.', 'CDC'),
    ('med_doxycycline', 'pregnancy', 5, '', 'No leptospirosis pre-exposure prophylaxis is currently recommended as safe for pregnant or lactating women.', 'PhilHealth 2012'),
    ('med_doxycycline', 'administration', 6, '', 'Swallow with plenty of water while sitting or standing, well before bedtime. May take with food or milk if stomach upset occurs. Separate from antacids, iron, zinc and bismuth as much as possible.', 'Label · UK SmPC'),
    ('med_doxycycline', 'forms_ph', 7, '', 'Oral: 100 mg capsule (as hyclate).', 'PNF'),
    ('med_doxycycline', 'monitor', 8, '', 'Ask about headache or visual disturbance (intracranial hypertension); stop at the first sign of a serious skin reaction; watch for diarrhoea up to 2 months after the course (C. difficile); check INR with warfarin and ciclosporin levels if co-prescribed.', 'Label · UK SmPC'),
    ('med_doxycycline', 'monitor', 9, '', 'Prophylaxis is not 100% effective: people taking it should still watch for fever and flu-like symptoms after exposure.', 'PhilHealth 2012')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_doxycycline');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_doxycycline', 'PNF', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 0),
    ('med_doxycycline', 'PhilHealth 2012', 'PhilHealth – Leptospirosis policy recommendations', 'Philippine Health Insurance Corporation. Policy Recommendations on the Diagnosis, Management and Prevention of Leptospirosis (c. 2012).', 'https://www.philhealth.gov.ph/partners/providers/pdf/Leptospirosis_Policy_Statements.pdf', 1),
    ('med_doxycycline', 'Label · UK SmPC', 'UK SmPC – Doxycycline 100 mg Capsules', 'Waymade Plc (Sovereign Medical). Doxycycline 100 mg Capsules – Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=doxycycline#emc-13082', 2),
    ('med_doxycycline', 'CDC', 'CDC – Clinical Care of Rocky Mountain Spotted Fever', 'Centers for Disease Control and Prevention. Clinical Care of Rocky Mountain Spotted Fever.', 'https://www.cdc.gov/rocky-mountain-spotted-fever/hcp/clinical-care/', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_doxycycline')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_doxycycline');


-- ================================================ med_enalapril  (Enalapril)
update public.medicines set description = 'Enalapril is a prodrug hydrolyzed to enalaprilat, which inhibits angiotensin-converting enzyme, lowering angiotensin II and aldosterone and increasing bradykinin. The result is vasodilation, reduced afterload and favorable cardiac remodeling. It is used for hypertension, heart failure with reduced ejection fraction and asymptomatic left ventricular dysfunction. Enalaprilat has an effective accumulation half-life of about 11 hours, so once-daily dosing reaches steady state after about 4 days; it is cleared mainly by the kidneys and is removed by dialysis, which is why doses are cut in renal impairment. In the Philippines, the PNF lists enalapril as 5 mg and 20 mg tablets and as a fixed tablet with hydrochlorothiazide (20 mg + 12.5 mg).', updated_at = now()
where id = 'med_enalapril' and description = 'Enalapril is a prodrug hydrolyzed to enalaprilat, which inhibits angiotensin-converting enzyme, lowering angiotensin II and aldosterone and increasing bradykinin. The result is vasodilation, reduced afterload and favorable cardiac remodeling. It is used for hypertension, heart failure with reduced ejection fraction and asymptomatic left ventricular dysfunction.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; UK SmPC – Enalapril Maleate Tablets 5 mg; MSF Essential Drugs – Enalapril oral' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; UK SmPC – Enalapril Maleate Tablets 5 mg; MSF Essential Drugs – Enalapril oral' end
where id = 'med_enalapril' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'adverse', 'Depression', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse' and content = 'Depression');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'adverse', 'Rhythm disturbances, angina and tachycardia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse' and content = 'Rhythm disturbances, angina and tachycardia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'adverse', 'Dyspnoea', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse' and content = 'Dyspnoea');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'adverse', 'Diarrhoea and abdominal pain', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse' and content = 'Diarrhoea and abdominal pain');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'adverse', 'Hyponatraemia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse' and content = 'Hyponatraemia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'adverse', 'Hypoglycaemia in people with diabetes, mainly in the first weeks', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse' and content = 'Hypoglycaemia in people with diabetes, mainly in the first weeks');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'adverse', 'Anaemia, including aplastic and haemolytic (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'adverse' and content = 'Anaemia, including aplastic and haemolytic (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'contraindication', 'Hypersensitivity to any other ACE inhibitor', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication' and content = 'Hypersensitivity to any other ACE inhibitor');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'contraindication', 'Co-administration with aliskiren when GFR is under 60 mL/min/1.73 m²', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication' and content = 'Co-administration with aliskiren when GFR is under 60 mL/min/1.73 m²');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'contraindication', 'Cardiogenic shock or haemodynamically significant left ventricular outflow obstruction (avoid)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication' and content = 'Cardiogenic shock or haemodynamically significant left ventricular outflow obstruction (avoid)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'contraindication', 'Bilateral renal artery stenosis or stenosis to a single kidney: high risk of hypotension and renal failure (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication' and content = 'Bilateral renal artery stenosis or stenosis to a single kidney: high risk of hypotension and renal failure (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'contraindication', 'Kidney transplant recipients: not recommended (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'contraindication' and content = 'Kidney transplant recipients: not recommended (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'interaction', 'mTOR inhibitors (sirolimus, everolimus), racecadotril and vildagliptin: increased angioedema risk.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction' and content = 'mTOR inhibitors (sirolimus, everolimus), racecadotril and vildagliptin: increased angioedema risk.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'interaction', 'Co-trimoxazole: hyperkalaemia; combination not recommended.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction' and content = 'Co-trimoxazole: hyperkalaemia; combination not recommended.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'interaction', 'Ciclosporin and heparin: hyperkalaemia; monitor potassium.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction' and content = 'Ciclosporin and heparin: hyperkalaemia; monitor potassium.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'interaction', 'Insulin and oral antidiabetics: increased hypoglycaemia risk, mainly early in treatment and in renal impairment.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction' and content = 'Insulin and oral antidiabetics: increased hypoglycaemia risk, mainly early in treatment and in renal impairment.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'interaction', 'Injectable gold (sodium aurothiomalate): rare nitritoid reactions (flushing, nausea, hypotension).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction' and content = 'Injectable gold (sodium aurothiomalate): rare nitritoid reactions (flushing, nausea, hypotension).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_enalapril', 'interaction', 'LDL apheresis or wasp/bee venom desensitisation: life-threatening anaphylactoid reactions; withhold enalapril before each session.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_enalapril' and kind = 'interaction' and content = 'LDL apheresis or wasp/bee venom desensitisation: life-threatening anaphylactoid reactions; withhold enalapril before each session.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_enalapril', 'UK SmPC (emc)', 'Enalapril Maleate Tablets 5 mg – Summary of Product Characteristics. Dexcel-Pharma Ltd (PL 14017/0029). Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=enalapril#emc-2671', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_enalapril'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_enalapril' and url = 'https://products.mhra.gov.uk/search/?search=enalapril#emc-2671');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_enalapril', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – practical guidelines: Enalapril oral. MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/enalapril-oral-16683529.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_enalapril'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_enalapril' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/enalapril-oral-16683529.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_enalapril', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_enalapril'), 0)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_enalapril' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_gastroenteritis', 'med_enalapril', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis'), 0), 'caution'::condition_safety, 'UK label: volume depletion from diarrhoea or vomiting makes symptomatic hypotension more likely'
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis' and medicine_id = 'med_enalapril');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'ischemic_stroke', 'med_enalapril', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'ischemic_stroke'), 0), 'caution'::condition_safety, 'UK label: in cerebrovascular disease an excessive fall in blood pressure could cause a stroke; start low'
where exists (select 1 from public.diseases where id = 'ischemic_stroke')
  and exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.disease_medicines where disease_id = 'ischemic_stroke' and medicine_id = 'med_enalapril');
-- med_enalapril
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_enalapril', 'adult', 0, 'Hypertension (starting dose)', 'PO', '5–20 mg', 'Once a day', 'Long-term', '—', 'Label · UK SmPC', '5–10 mg in mild hypertension'),
    ('med_enalapril', 'adult', 1, 'Hypertension (maintenance)', 'PO', '20 mg', 'Once a day', 'Long-term', '40 mg/day', 'Label · UK SmPC', ''),
    ('med_enalapril', 'adult', 2, 'Hypertension: renovascular, salt/volume depleted or on diuretic', 'PO', '5 mg or less', 'Once a day', 'Long-term', '—', 'Label · UK SmPC', 'Start under supervision; stop diuretic 2–3 days before if possible'),
    ('med_enalapril', 'adult', 3, 'Hypertension: elderly, on diuretic or renal impairment', 'PO', '2.5 mg', 'Once a day', 'Long-term', '40 mg/day', 'MSF', 'Then adjust to renal function'),
    ('med_enalapril', 'adult', 4, 'Heart failure / asymptomatic LV dysfunction (start)', 'PO', '2.5 mg', 'Once a day', 'Days 1–3', '—', 'Label · UK SmPC', 'Close supervision; days 4–7: 5 mg/day in 2 doses; week 2: 10 mg/day'),
    ('med_enalapril', 'adult', 5, 'Heart failure / asymptomatic LV dysfunction (target)', 'PO', '20 mg/day', 'Once a day or 2× a day', 'Long-term', '40 mg/day in 2 doses', 'Label · UK SmPC', 'Reached over 2–4 weeks'),
    ('med_enalapril', 'child', 6, 'Hypertension, 20 to under 50 kg', 'PO', '2.5 mg', 'Once a day', 'Long-term', '20 mg/day', 'Label · UK SmPC', 'Children able to swallow tablets'),
    ('med_enalapril', 'child', 7, 'Hypertension, 50 kg and over', 'PO', '5 mg', 'Once a day', 'Long-term', '40 mg/day', 'Label · UK SmPC', 'Not recommended in neonates or GFR <30 mL/min/1.73 m²')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_enalapril');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_enalapril', 'renal', 0, 'CrCl 30–80', 'Initial dose 5–10 mg a day.', 'Label · UK SmPC'),
    ('med_enalapril', 'renal', 1, 'CrCl 10–30', 'Initial dose 2.5 mg a day.', 'Label · UK SmPC'),
    ('med_enalapril', 'renal', 2, 'CrCl ≤ 10', '2.5 mg on dialysis days; on non-dialysis days adjust to blood pressure. Enalaprilat is dialysable.', 'Label · UK SmPC'),
    ('med_enalapril', 'hepatic', 3, '', 'Rare syndrome starting as cholestatic jaundice or hepatitis can progress to fulminant hepatic necrosis: stop if jaundice or marked rise in liver enzymes.', 'Label · UK SmPC'),
    ('med_enalapril', 'elderly', 4, '', 'Dose according to renal function.', 'Label · UK SmPC'),
    ('med_enalapril', 'pregnancy', 5, '', 'Not recommended in the first trimester and contraindicated in the second and third; stop as soon as pregnancy is found. If exposed from the second trimester, check fetal kidneys and skull by ultrasound; watch exposed newborns for hypotension.', 'Label · UK SmPC'),
    ('med_enalapril', 'pregnancy', 6, '', 'Breastfeeding: milk levels are very low; avoid in preterm infants and in the first weeks after birth, may be used for older infants with monitoring.', 'Label · UK SmPC'),
    ('med_enalapril', 'administration', 7, '', 'Food does not affect absorption. Increase hypertension doses every 1–2 weeks according to blood pressure.', 'MSF'),
    ('med_enalapril', 'forms_ph', 8, '', 'Oral: 5 mg and 20 mg tablet (as maleate); also enalapril 20 mg + hydrochlorothiazide 12.5 mg tablet.', 'PNF'),
    ('med_enalapril', 'monitor', 9, '', 'Blood pressure, serum creatinine and potassium before and after starting (especially with diuretics or heart failure); white cell count periodically in collagen vascular disease; blood glucose early on in diabetes.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_enalapril');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_enalapril', 'PNF', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 0),
    ('med_enalapril', 'Label · UK SmPC', 'UK SmPC – Enalapril Maleate Tablets 5 mg', 'Dexcel-Pharma Ltd. Enalapril Maleate Tablets 5 mg – Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=enalapril#emc-2671', 1),
    ('med_enalapril', 'MSF', 'MSF Essential Drugs – Enalapril oral', 'Médecins Sans Frontières. Essential drugs – practical guidelines: Enalapril oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/enalapril-oral-16683529.html', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_enalapril')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_enalapril');


-- ================================================ med_entecavir  (Entecavir)
update public.medicines set description = 'Entecavir is a guanosine nucleoside analogue that is phosphorylated intracellularly to its active triphosphate, which competes with deoxyguanosine triphosphate and inhibits all three activities of the hepatitis B virus polymerase (base priming, reverse transcription of the negative strand and synthesis of the positive strand). It is a preferred first-line oral agent for chronic hepatitis B because of its potency and high barrier to resistance in nucleoside-naive patients. Resistance is rare in nucleoside-naive patients but becomes common after lamivudine resistance (rtM204V/rtL180M substitutions), with cumulative entecavir resistance of about 51% by year 5 in lamivudine-refractory studies, so adding a second antiviral is considered in that setting. WHO lists tenofovir or entecavir as the oral treatments for chronic hepatitis B, and most people who start treatment continue it for life. In the Philippines the PNF lists 0.5 mg and 1 mg tablets and a 0.05 mg/mL oral solution.', updated_at = now()
where id = 'med_entecavir' and description = 'Entecavir is a guanosine nucleoside analogue that is phosphorylated intracellularly to its active triphosphate, which competes with deoxyguanosine triphosphate and inhibits all three activities of the hepatitis B virus polymerase (base priming, reverse transcription of the negative strand and synthesis of the positive strand). It is a preferred first-line oral agent for chronic hepatitis B because of its potency and high barrier to resistance in nucleoside-naive patients.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine National Formulary (PNF) EML; UK SmPC (emc); WHO' else source_attribution || '; Philippine National Formulary (PNF) EML; UK SmPC (emc); WHO' end
where id = 'med_entecavir' and position('Philippine National Formulary (PNF) EML' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_entecavir', 'adverse', 'Insomnia and somnolence (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse' and content = 'Insomnia and somnolence (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_entecavir', 'adverse', 'Vomiting, diarrhoea and dyspepsia (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse' and content = 'Vomiting, diarrhoea and dyspepsia (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_entecavir', 'adverse', 'Raised transaminases during treatment (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse' and content = 'Raised transaminases during treatment (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_entecavir', 'adverse', 'Rash and alopecia (uncommon); anaphylactoid reaction (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse' and content = 'Rash and alopecia (uncommon); anaphylactoid reaction (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_entecavir', 'adverse', 'Neutropenia (very common in paediatric patients)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'adverse' and content = 'Neutropenia (very common in paediatric patients)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_entecavir', 'contraindication', 'Hypersensitivity to entecavir or any excipient (UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'contraindication' and content = 'Hypersensitivity to entecavir or any excipient (UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_entecavir', 'contraindication', 'Rare hereditary galactose intolerance, Lapp lactase deficiency or glucose-galactose malabsorption (tablets contain lactose)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'contraindication' and content = 'Rare hereditary galactose intolerance, Lapp lactase deficiency or glucose-galactose malabsorption (tablets contain lactose)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_entecavir', 'interaction', 'Not a substrate, inducer or inhibitor of CYP450 enzymes: CYP-mediated interactions are unlikely.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'interaction' and content = 'Not a substrate, inducer or inhibitor of CYP450 enzymes: CYP-mediated interactions are unlikely.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_entecavir', 'interaction', 'Lamivudine, adefovir or tenofovir: no pharmacokinetic interaction was seen.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_entecavir' and kind = 'interaction' and content = 'Lamivudine, adefovir or tenofovir: no pharmacokinetic interaction was seen.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_entecavir', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_entecavir'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_entecavir' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_entecavir', 'UK SmPC (emc)', 'Baraclude 0.5 mg film-coated tablets - Summary of Product Characteristics. Bristol-Myers Squibb Pharma EEIG. Electronic medicines compendium (emc), updated May 2021.', 'https://products.mhra.gov.uk/search/?search=entecavir#emc-213', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_entecavir'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_entecavir' and url = 'https://products.mhra.gov.uk/search/?search=entecavir#emc-213');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_entecavir', 'UK SmPC (emc)', 'Baraclude 0.05 mg/ml oral solution - Summary of Product Characteristics. Bristol-Myers Squibb. Electronic medicines compendium (emc), updated May 2021.', 'https://products.mhra.gov.uk/search/?search=entecavir#emc-2089', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_entecavir'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_entecavir' and url = 'https://products.mhra.gov.uk/search/?search=entecavir#emc-2089');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_entecavir', 'WHO', 'World Health Organization. Hepatitis B fact sheet. Geneva: WHO; 2026.', 'https://www.who.int/news-room/fact-sheets/detail/hepatitis-b', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_entecavir'), 0)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_entecavir' and url = 'https://www.who.int/news-room/fact-sheets/detail/hepatitis-b');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_entecavir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'caution'::condition_safety, 'Not used for HBV in HIV/HBV coinfection unless on fully suppressive antiretroviral therapy (risk of HIV resistance).'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_entecavir');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_entecavir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Renally cleared: dose reduced or interval extended when CrCl < 50 mL/min, including dialysis.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_entecavir');
-- med_entecavir
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_entecavir', 'adult', 0, 'Chronic hepatitis B, nucleoside-naive, compensated', 'PO', '0.5 mg', 'Once a day', 'Long term (see stopping rules)', '—', 'Label · UK SmPC', 'With or without food'),
    ('med_entecavir', 'adult', 1, 'Lamivudine-refractory chronic hepatitis B', 'PO', '1 mg', 'Once a day', 'Long term', '—', 'Label · UK SmPC', 'Empty stomach (>2 h before and after a meal)'),
    ('med_entecavir', 'adult', 2, 'Decompensated liver disease', 'PO', '1 mg', 'Once a day', 'Do not stop', '—', 'Label · UK SmPC', 'Empty stomach; stopping not advised in decompensated disease or cirrhosis'),
    ('med_entecavir', 'child', 3, 'Chronic hepatitis B, nucleoside-naive, 2–<18 y, ≥32.6 kg', 'PO', '0.5 mg (1 tablet or 10 mL solution)', 'Once a day', 'Long term', '—', 'Label · UK SmPC', ''),
    ('med_entecavir', 'child', 4, 'Chronic hepatitis B, nucleoside-naive, 2–<18 y, 10–32.5 kg', 'PO', '4–9.5 mL of 0.05 mg/mL solution by weight band', 'Once a day', 'Long term', '10 mL', 'Label · UK SmPC (soln)', '10–14.1 kg 4 mL; 20.9–22.5 kg 6.5 mL; 30.9–32.5 kg 9.5 mL (0.5 mL steps per band)')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_entecavir');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_entecavir', 'renal', 0, 'CrCl 30–49', 'Naive: 0.25 mg once a day or 0.5 mg every 48 h. Lamivudine-refractory/decompensated: 0.5 mg once a day.', 'Label · UK SmPC'),
    ('med_entecavir', 'renal', 1, 'CrCl 10–29', 'Naive: 0.15 mg once a day or 0.5 mg every 72 h. Lamivudine-refractory/decompensated: 0.3 mg once a day or 0.5 mg every 48 h.', 'Label · UK SmPC'),
    ('med_entecavir', 'renal', 2, 'CrCl <10, HD, CAPD', 'Naive: 0.05 mg once a day or 0.5 mg every 5–7 days. Lamivudine-refractory/decompensated: 0.1 mg once a day or 0.5 mg every 72 h. Doses extrapolated from limited data: monitor virological response closely.', 'Label · UK SmPC'),
    ('med_entecavir', 'hepatic', 3, '', 'No dose adjustment in hepatic impairment; serious hepatic events are more frequent in decompensated (Child-Pugh C) disease.', 'Label · UK SmPC'),
    ('med_entecavir', 'elderly', 4, '', 'No age-based adjustment; dose by renal function.', 'Label · UK SmPC'),
    ('med_entecavir', 'pregnancy', 5, '', 'Not recommended in pregnancy unless clearly necessary; women of childbearing potential use effective contraception. Breastfeeding should stop during treatment.', 'Label · UK SmPC'),
    ('med_entecavir', 'monitor', 6, '', 'HBV DNA and ALT during treatment; liver function for at least 6 months after stopping (risk of flare); renal function, especially with cyclosporine or tacrolimus after liver transplant.', 'Label · UK SmPC'),
    ('med_entecavir', 'administration', 7, '', 'Duration: HBeAg-positive, at least 12 months after HBe seroconversion (or until HBs seroconversion/loss of efficacy); HBeAg-negative, at least until HBs seroconversion or loss of efficacy.', 'Label · UK SmPC'),
    ('med_entecavir', 'forms_ph', 8, '', '500 mcg and 1 mg tablet/film-coated tablet; 0.05 mg/mL oral solution.', 'PNF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_entecavir');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_entecavir', 'Label · UK SmPC', 'UK SmPC (emc)', 'Baraclude 0.5 mg film-coated tablets - SmPC. Bristol-Myers Squibb Pharma EEIG, 2021.', 'https://products.mhra.gov.uk/search/?search=entecavir#emc-213', 0),
    ('med_entecavir', 'Label · UK SmPC (soln)', 'UK SmPC (emc)', 'Baraclude 0.05 mg/ml oral solution - SmPC. Bristol-Myers Squibb, 2021.', 'https://products.mhra.gov.uk/search/?search=entecavir#emc-2089', 1),
    ('med_entecavir', 'PNF', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_entecavir')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_entecavir');


-- ================================================ med_ethambutol  (Ethambutol)
update public.medicines set description = 'Ethambutol inhibits mycobacterial arabinosyltransferases, interfering with arabinogalactan synthesis in the cell wall; it is bacteriostatic. It is included in the intensive phase of first-line TB therapy to protect against resistance while drug-susceptibility results are pending. In the Philippine NTP it is given in the HRZE fixed-dose combination for the 2-month intensive phase of Category I (2HRZE/4HR) and through all 8 months of Category II retreatment (2HRZES/1HRZE/5HRE), with the number of tablets set by body-weight band. MSF notes that ethambutol is not routinely given to all children, and that young children (under 5) need particular care because visual changes are hard to detect at that age.', updated_at = now()
where id = 'med_ethambutol' and description = 'Ethambutol inhibits mycobacterial arabinosyltransferases, interfering with arabinogalactan synthesis in the cell wall; it is bacteriostatic. It is included in the intensive phase of first-line TB therapy to protect against resistance while drug-susceptibility results are pending.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine NTP Manual of Procedures; Philippine National Formulary (PNF) EML; MSF Essential Drugs; MSF Tuberculosis guideline; UK SmPC (emc)' else source_attribution || '; Philippine NTP Manual of Procedures; Philippine National Formulary (PNF) EML; MSF Essential Drugs; MSF Tuberculosis guideline; UK SmPC (emc)' end
where id = 'med_ethambutol' and position('Philippine NTP Manual of Procedures' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ethambutol', 'indication', 'Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'indication' and content = 'Previously treated drug-susceptible TB (PH NTP Category II: 2HRZES/1HRZE/5HRE)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ethambutol', 'indication', 'Extrapulmonary TB of the CNS, bones or joints (PH NTP Category Ia: 2HRZE/10HR)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'indication' and content = 'Extrapulmonary TB of the CNS, bones or joints (PH NTP Category Ia: 2HRZE/10HR)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ethambutol', 'adverse', 'Very rare skin reactions: photosensitive lichenoid eruptions, bullous dermatitis, Stevens-Johnson syndrome', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'adverse' and content = 'Very rare skin reactions: photosensitive lichenoid eruptions, bullous dermatitis, Stevens-Johnson syndrome');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ethambutol', 'adverse', 'Numbness and paraesthesia of the extremities (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'adverse' and content = 'Numbness and paraesthesia of the extremities (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ethambutol', 'contraindication', 'Pre-existing eye disease such as diabetic retinopathy (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'contraindication' and content = 'Pre-existing eye disease such as diabetic retinopathy (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ethambutol', 'contraindication', 'Severe renal impairment (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'contraindication' and content = 'Severe renal impairment (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ethambutol', 'contraindication', 'Retrobulbar neuritis (UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ethambutol' and kind = 'contraindication' and content = 'Retrobulbar neuritis (UK SmPC)');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ethambutol', 'Philippine NTP Manual of Procedures', 'Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.', 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ethambutol'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ethambutol' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ethambutol', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ethambutol'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ethambutol' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ethambutol', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs - practical guidelines: Ethambutol (E) oral. Updated August 2022.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ethambutol-e-oral-16683637.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ethambutol'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ethambutol' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ethambutol-e-oral-16683637.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ethambutol', 'MSF Tuberculosis guideline', 'Médecins Sans Frontières. Tuberculosis - Appendix 13. Daily dose of TB drugs using fixed-dose combinations. Updated October 2022.', 'https://medicalguidelines.msf.org/en/node/1205', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ethambutol'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ethambutol' and url = 'https://medicalguidelines.msf.org/en/node/1205');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ethambutol', 'UK SmPC (emc)', 'Ethambutol 400 mg Tablets - Summary of Product Characteristics. Esteve Pharmaceuticals Ltd. Electronic medicines compendium (emc), updated July 2024.', 'https://products.mhra.gov.uk/search/?search=ethambutol#emc-9346', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ethambutol'), 0)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ethambutol' and url = 'https://products.mhra.gov.uk/search/?search=ethambutol#emc-9346');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_ethambutol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Dose given three times a week in renal impairment; optic toxicity is more common when renal function is reduced; MSF advises against use in severe renal impairment.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_ethambutol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_ethambutol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'MSF lists pre-existing eye disease such as diabetic retinopathy as a contraindication; check eyes before treatment in diabetics (applies only with retinopathy).'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_ethambutol');
-- med_ethambutol
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_ethambutol', 'adult', 0, 'TB Cat I intensive (2HRZE), 30–37 kg', 'PO', '2 tablets HRZE FDC', 'Once a day', '2 months', '—', 'NTP MOP 2014', 'Then HR 2 tablets for 4 months (10 months for Cat Ia)'),
    ('med_ethambutol', 'adult', 1, 'TB Cat I intensive (2HRZE), 38–54 kg', 'PO', '3 tablets HRZE FDC', 'Once a day', '2 months', '—', 'NTP MOP 2014', 'Then HR 3 tablets'),
    ('med_ethambutol', 'adult', 2, 'TB Cat I intensive (2HRZE), 55–70 kg', 'PO', '4 tablets HRZE FDC', 'Once a day', '2 months', '—', 'NTP MOP 2014', 'Then HR 4 tablets'),
    ('med_ethambutol', 'adult', 3, 'TB Cat I intensive (2HRZE), >70 kg', 'PO', '5 tablets HRZE FDC', 'Once a day', '2 months', '—', 'NTP MOP 2014', 'Then HR 5 tablets'),
    ('med_ethambutol', 'adult', 4, 'TB Cat II retreatment (2HRZES/1HRZE/5HRE)', 'PO', 'Same tablet number per weight band (2/3/4/5)', 'Once a day', '8 months', '—', 'NTP MOP 2014', 'HRZE months 1–3 (+ streptomycin months 1–2), then HRE months 4–8'),
    ('med_ethambutol', 'adult', 5, 'TB, single-drug formulation', 'PO', '15 mg/kg (range 15–20)', 'Once a day', 'Per regimen', '1.2 g/day', 'NTP MOP 2014', ''),
    ('med_ethambutol', 'child', 6, 'TB, single-drug formulation', 'PO', '20 mg/kg (range 15–25)', 'Once a day', 'Per regimen', '1.2 g/day', 'NTP MOP 2014', 'Newborn <4 weeks: refer to pediatrician (streptomycin instead of ethambutol)'),
    ('med_ethambutol', 'child', 7, 'TB intensive phase, 4–7 kg / 8–11 kg (with HRZ 50/75/150)', 'PO', '1 / 2 tablets E 100 mg', 'Once a day', '2 months', '—', 'MSF TB', 'Not routinely given to all children')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_ethambutol');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_ethambutol', 'renal', 0, '', '15–25 mg/kg three times a week in renal impairment; MSF advises not to give in severe renal impairment. Toxic effects are more common when renal function is impaired.', 'MSF'),
    ('med_ethambutol', 'pregnancy', 1, '', 'MSF: no contraindication in pregnancy or breastfeeding. The UK SmPC states it is not recommended in pregnancy or breastfeeding.', 'MSF'),
    ('med_ethambutol', 'monitor', 2, '', 'Full eye examination before starting (UK SmPC). Teach patients to stop the drug and seek care at once for blurred vision, reduced acuity or difficulty telling red from green (MSF; usually reverses within weeks).', 'MSF'),
    ('med_ethambutol', 'administration', 3, '', 'Dose carefully by body weight. HRZE FDC tablet = isoniazid 75 mg + rifampicin 150 mg + pyrazinamide 400 mg + ethambutol 275 mg.', 'PNF'),
    ('med_ethambutol', 'forms_ph', 4, '', '100 mg tablet (pediatric); 200 mg and 400 mg tablet. FDCs: isoniazid + rifampicin + ethambutol 75/150/275 mg tablet; isoniazid + rifampicin + pyrazinamide + ethambutol 75/150/400/275 mg tablet.', 'PNF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_ethambutol');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_ethambutol', 'NTP MOP 2014', 'Philippine NTP Manual of Procedures', 'DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 11–14).', 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf', 0),
    ('med_ethambutol', 'PNF', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 1),
    ('med_ethambutol', 'MSF', 'MSF Essential Drugs', 'MSF Essential drugs: Ethambutol (E) oral, 2022.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ethambutol-e-oral-16683637.html', 2),
    ('med_ethambutol', 'MSF TB', 'MSF Tuberculosis guideline', 'MSF Tuberculosis, Appendix 13: daily dose of TB drugs using FDCs, 2022.', 'https://medicalguidelines.msf.org/en/node/1205', 3),
    ('med_ethambutol', 'Label · UK SmPC', 'UK SmPC (emc)', 'Ethambutol 400 mg Tablets - SmPC. Esteve Pharmaceuticals Ltd, 2024.', 'https://products.mhra.gov.uk/search/?search=ethambutol#emc-9346', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_ethambutol')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_ethambutol');


-- ================================================ med_famotidine  (Famotidine)
update public.medicines set description = 'Famotidine competitively blocks histamine H2 receptors on gastric parietal cells, reducing basal, nocturnal and stimulated gastric acid secretion. It relieves heartburn and heals peptic ulcers and esophagitis, but is less potent than proton pump inhibitors; it is useful for on-demand symptom control and as a bedtime add-on for nighttime reflux. A single 40 mg bedtime dose suppresses gastric acid for more than 12 hours, and famotidine does not affect the cytochrome P450 system, so it has few clinically important interactions apart from drugs that need gastric acid for absorption. In the Philippines the PNF lists a 20 mg tablet and a 20 mg injection, the latter used intravenously in hospitalised patients until oral therapy is possible.', updated_at = now()
where id = 'med_famotidine' and description = 'Famotidine competitively blocks histamine H2 receptors on gastric parietal cells, reducing basal, nocturnal and stimulated gastric acid secretion. It relieves heartburn and heals peptic ulcers and esophagitis, but is less potent than proton pump inhibitors; it is useful for on-demand symptom control and as a bedtime add-on for nighttime reflux.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine National Formulary (PNF) EML; UK SmPC (emc); DailyMed (FDA label)' else source_attribution || '; Philippine National Formulary (PNF) EML; UK SmPC (emc); DailyMed (FDA label)' end
where id = 'med_famotidine' and position('Philippine National Formulary (PNF) EML' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'indication', 'Prevention of duodenal ulcer relapse (20 mg at night)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'indication' and content = 'Prevention of duodenal ulcer relapse (20 mg at night)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'indication', 'Hospitalised patients who cannot take oral therapy (IV 20 mg every 12 h)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'indication' and content = 'Hospitalised patients who cannot take oral therapy (IV 20 mg every 12 h)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'adverse', 'Taste disorder, dry mouth, nausea, flatulence and loss of appetite (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'adverse' and content = 'Taste disorder, dry mouth, nausea, flatulence and loss of appetite (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'adverse', 'Rash, itching and urticaria (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'adverse' and content = 'Rash, itching and urticaria (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'adverse', 'Very rare: agranulocytosis or pancytopenia, anaphylaxis, hepatitis or cholestatic jaundice, convulsions', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'adverse' and content = 'Very rare: agranulocytosis or pancytopenia, anaphylaxis, hepatitis or cholestatic jaundice, convulsions');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'adverse', 'Very rare: QT prolongation and arrhythmias', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'adverse' and content = 'Very rare: QT prolongation and arrhythmias');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'contraindication', 'Gastric malignancy must be excluded before treating a gastric ulcer', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'contraindication' and content = 'Gastric malignancy must be excluded before treating a gastric ulcer');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'contraindication', 'Multiple-dose vials containing benzyl alcohol: not for neonates (gasping syndrome)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'contraindication' and content = 'Multiple-dose vials containing benzyl alcohol: not for neonates (gasping syndrome)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'interaction', 'Ketoconazole or itraconazole: absorption reduced; give ketoconazole 2 hours before famotidine.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction' and content = 'Ketoconazole or itraconazole: absorption reduced; give ketoconazole 2 hours before famotidine.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'interaction', 'Atazanavir and posaconazole oral suspension: absorption reduced by higher gastric pH; avoid where possible.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction' and content = 'Atazanavir and posaconazole oral suspension: absorption reduced by higher gastric pH; avoid where possible.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'interaction', 'Erlotinib, gefitinib or pazopanib: co-administration not recommended.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction' and content = 'Erlotinib, gefitinib or pazopanib: co-administration not recommended.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'interaction', 'Probenecid: raises famotidine levels by about 50%; avoid.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction' and content = 'Probenecid: raises famotidine levels by about 50%; avoid.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'interaction', 'Antacids: take famotidine 1–2 hours before the antacid; sucralfate should not be given within 2 hours of famotidine.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction' and content = 'Antacids: take famotidine 1–2 hours before the antacid; sucralfate should not be given within 2 hours of famotidine.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_famotidine', 'interaction', 'Calcium carbonate phosphate binders in haemodialysis patients: may lose efficacy.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine' and kind = 'interaction' and content = 'Calcium carbonate phosphate binders in haemodialysis patients: may lose efficacy.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_famotidine', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_famotidine'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_famotidine' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_famotidine', 'UK SmPC (emc)', 'Famotidine 20mg Tablets - Summary of Product Characteristics. Tillomed Laboratories Ltd. Electronic medicines compendium (emc), updated January 2025.', 'https://products.mhra.gov.uk/search/?search=famotidine#emc-11523', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_famotidine'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_famotidine' and url = 'https://products.mhra.gov.uk/search/?search=famotidine#emc-11523');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_famotidine', 'DailyMed (FDA label)', 'Famotidine Injection, USP 10 mg/mL - prescribing information. Hikma Pharmaceuticals USA Inc. DailyMed, U.S. National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1fdf16e5-145d-4c19-a318-fc6c10794b50', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_famotidine'), 0)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_famotidine' and url = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1fdf16e5-145d-4c19-a318-fc6c10794b50');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'peptic_ulcer_disease', 'med_famotidine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease'), 0), 'safe'::condition_safety, 'Licensed for duodenal and benign gastric ulcer healing and relapse prevention; exclude gastric malignancy first.'
where exists (select 1 from public.diseases where id = 'peptic_ulcer_disease')
  and exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease' and medicine_id = 'med_famotidine');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_famotidine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Daily dose halved when CrCl < 30 mL/min; CNS adverse effects reported in moderate to severe renal insufficiency.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_famotidine');
-- med_famotidine
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_famotidine', 'adult', 0, 'Duodenal ulcer', 'PO', '40 mg', 'Once a day (at night)', '4–8 weeks', '—', 'Label · UK SmPC', 'Continue 4 more weeks if not healed at 4 weeks'),
    ('med_famotidine', 'adult', 1, 'Duodenal ulcer relapse prevention', 'PO', '20 mg', 'Once a day (at night)', '—', '—', 'Label · UK SmPC', ''),
    ('med_famotidine', 'adult', 2, 'Benign gastric ulcer', 'PO', '40 mg', 'Once a day (at night)', '4–8 weeks', '—', 'Label · UK SmPC', 'Exclude malignancy first'),
    ('med_famotidine', 'adult', 3, 'Reflux oesophagitis, mild', 'PO', '20 mg', '2× a day', '6–12 weeks', '—', 'Label · UK SmPC', ''),
    ('med_famotidine', 'adult', 4, 'Reflux oesophagitis, mild to moderate', 'PO', '40 mg', '2× a day', '6–12 weeks', '—', 'Label · UK SmPC', ''),
    ('med_famotidine', 'adult', 5, 'Zollinger-Ellison syndrome', 'PO', '20 mg, then adjust', 'Every 6 h', 'As needed', '800 mg/day', 'Label · UK SmPC', 'Up to 800 mg/day used for up to 1 year'),
    ('med_famotidine', 'adult', 6, 'Hospitalised / unable to take oral', 'IV', '20 mg', 'Every 12 h', 'Until oral possible', '—', 'Label · US (inj)', 'Push over ≥2 min or infuse over 15–30 min'),
    ('med_famotidine', 'child', 7, '1–16 y, IV acid suppression', 'IV', '0.25 mg/kg', 'Every 12 h', '—', '40 mg/day', 'Label · US (inj)', 'Up to 0.5 mg/kg every 12 h used in studies; oral use in children not established (UK SmPC)')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_famotidine');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_famotidine', 'renal', 0, 'CrCl <30', 'Reduce the daily dose by 50%.', 'Label · UK SmPC'),
    ('med_famotidine', 'renal', 1, 'CrCl <10', 'Consider 20 mg at night.', 'Label · UK SmPC'),
    ('med_famotidine', 'renal', 2, 'Dialysis', 'Reduce dose by 50%; give at the end of or after dialysis.', 'Label · UK SmPC'),
    ('med_famotidine', 'elderly', 3, '', 'Same dose as adults.', 'Label · UK SmPC'),
    ('med_famotidine', 'pregnancy', 4, '', 'Not recommended in pregnancy unless clearly needed. Excreted in breast milk: stop famotidine or stop breastfeeding.', 'Label · UK SmPC'),
    ('med_famotidine', 'monitor', 5, '', 'Blood count and liver function during long-term high-dose treatment; avoid abrupt withdrawal after long-standing ulcer disease; watch for confusion in renal impairment.', 'Label · UK SmPC'),
    ('med_famotidine', 'administration', 6, '', 'IV push: dilute 20 mg (2 mL) to 5 or 10 mL and inject over at least 2 minutes. Infusion: dilute 2 mL in 100 mL dextrose 5% and run over 15–30 minutes.', 'Label · US (inj)'),
    ('med_famotidine', 'forms_ph', 7, '', '20 mg tablet; 20 mg powder/lyophilized powder for injection (ampule/vial).', 'PNF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_famotidine');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_famotidine', 'Label · UK SmPC', 'UK SmPC (emc)', 'Famotidine 20mg Tablets - SmPC. Tillomed Laboratories Ltd, 2024.', 'https://products.mhra.gov.uk/search/?search=famotidine#emc-11523', 0),
    ('med_famotidine', 'Label · US (inj)', 'DailyMed (FDA label)', 'Famotidine Injection, USP 10 mg/mL - prescribing information. Hikma Pharmaceuticals USA Inc.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1fdf16e5-145d-4c19-a318-fc6c10794b50', 1),
    ('med_famotidine', 'PNF', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_famotidine')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_famotidine');


-- ================================================ med_ferrous_sulfate  (Ferrous Sulfate)
update public.medicines set description = 'Ferrous sulfate supplies ferrous iron, which is absorbed mainly in the duodenum and used to rebuild body iron stores and hemoglobin. It is first-line treatment for iron-deficiency anemia. A 200 mg ferrous sulfate tablet contains about 65 mg of elemental iron; hemoglobin usually rises within about a month, and treatment continues for about 3 months to refill stores. Doses are written as elemental iron because content differs by salt (hydrated ferrous sulfate is about 20% iron, dried ferrous sulfate about 32%). In the Philippines, the DOH antenatal program gives daily iron-folic acid tablets (60 mg elemental iron + 0.4 mg folic acid) for at least 180 days, covering pregnancy and up to 3 months after delivery. WHO likewise recommends 30–60 mg elemental iron with 400 µg folic acid every day in pregnancy.', updated_at = now()
where id = 'med_ferrous_sulfate' and description = 'Ferrous sulfate supplies ferrous iron, which is absorbed mainly in the duodenum and used to rebuild body iron stores and hemoglobin. It is first-line treatment for iron-deficiency anemia. A 200 mg ferrous sulfate tablet contains about 65 mg of elemental iron; hemoglobin usually rises within about a month, and treatment continues for about 3 months to refill stores.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC - Ferrous Sulfate Tablets 200mg (Sandoz); WHO guideline - Daily iron and folic acid supplementation in pregnant women; Nutrients 2021 - IFA compliance in the Philippines; DOH Administrative Order No. 2010-0010; WHO guideline - Daily iron supplementation in infants and children; PH DOH IFA policy (as reported in Nutrients 2021); WHO guideline (pregnancy iron); Philippine National Formulary EML' else source_attribution || '; UK SmPC - Ferrous Sulfate Tablets 200mg (Sandoz); WHO guideline - Daily iron and folic acid supplementation in pregnant women; Nutrients 2021 - IFA compliance in the Philippines; DOH Administrative Order No. 2010-0010; WHO guideline - Daily iron supplementation in infants and children; PH DOH IFA policy (as reported in Nutrients 2021); WHO guideline (pregnancy iron); Philippine National Formulary EML' end
where id = 'med_ferrous_sulfate' and position('UK SmPC - Ferrous Sulfate Tablets 200mg (Sandoz)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'indication', 'Iron-folic acid supplementation in pregnancy and up to 3 months postpartum (PH DOH program)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'indication' and content = 'Iron-folic acid supplementation in pregnancy and up to 3 months postpartum (PH DOH program)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'adverse', 'Mouth ulceration if tablets are chewed, sucked or held in the mouth', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'adverse' and content = 'Mouth ulceration if tablets are chewed, sucked or held in the mouth');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'adverse', 'Oesophageal injury or bronchial necrosis if a tablet is aspirated (elderly, swallowing problems)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'adverse' and content = 'Oesophageal injury or bronchial necrosis if a tablet is aspirated (elderly, swallowing problems)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'adverse', 'Hypersensitivity rash, rarely anaphylaxis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'adverse' and content = 'Hypersensitivity rash, rarely anaphylaxis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'adverse', 'Faecal impaction with long-term use in older patients', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'adverse' and content = 'Faecal impaction with long-term use in older patients');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'contraindication', 'Concomitant parenteral (injectable) iron', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'contraindication' and content = 'Concomitant parenteral (injectable) iron');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'contraindication', 'Hypersensitivity to any ingredient of the product', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'contraindication' and content = 'Hypersensitivity to any ingredient of the product');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'interaction', 'Bisphosphonates, penicillamine, norfloxacin and ofloxacin: iron reduces their absorption.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction' and content = 'Bisphosphonates, penicillamine, norfloxacin and ofloxacin: iron reduces their absorption.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'interaction', 'Levothyroxine: separate doses by at least 2 hours.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction' and content = 'Levothyroxine: separate doses by at least 2 hours.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'interaction', 'Methyldopa: reduced bioavailability; cholestyramine binds iron in the gut.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction' and content = 'Methyldopa: reduced bioavailability; cholestyramine binds iron in the gut.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'interaction', 'Calcium, trientine, tea, coffee, milk, eggs and whole grains: reduced iron absorption; avoid from 1 hour before to 2 hours after the iron dose.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction' and content = 'Calcium, trientine, tea, coffee, milk, eggs and whole grains: reduced iron absorption; avoid from 1 hour before to 2 hours after the iron dose.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ferrous_sulfate', 'interaction', 'Dimercaprol: avoid, as it forms a toxic complex with iron.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate' and kind = 'interaction' and content = 'Dimercaprol: avoid, as it forms a toxic complex with iron.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ferrous_sulfate', 'UK SmPC - Ferrous Sulfate Tablets 200mg (Sandoz)', 'Sandoz Limited. Ferrous Sulfate Tablets 200mg - Summary of Product Characteristics. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=ferrous+sulfate#emc-4231', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate' and url = 'https://products.mhra.gov.uk/search/?search=ferrous+sulfate#emc-4231');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ferrous_sulfate', 'WHO guideline - Daily iron and folic acid supplementation in pregnant women', 'World Health Organization. e-Library of Evidence for Nutrition Actions (eLENA): Daily iron and folic acid supplementation during pregnancy. Updated 26 July 2024.', 'https://www.who.int/publications/i/item/9789241501996', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate' and url = 'https://www.who.int/publications/i/item/9789241501996');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ferrous_sulfate', 'Nutrients 2021 - IFA compliance in the Philippines', 'Felipe-Dimog EB, Yu CH, Ho CH, Liang FW. Factors Influencing the Compliance of Pregnant Women with Iron and Folic Acid Supplementation in the Philippines: 2017 Philippine Demographic and Health Survey Analysis. Nutrients. 2021;13(9):3060. doi:10.3390/nu13093060', 'https://www.mdpi.com/2072-6643/13/9/3060', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate' and url = 'https://www.mdpi.com/2072-6643/13/9/3060');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ferrous_sulfate', 'DOH Administrative Order No. 2010-0010', 'Department of Health (Philippines). Administrative Order No. 2010-0010: Revised Policy on Micronutrient Supplementation to Support Achievement of 2015 MDG Targets to Reduce Underfive and Maternal Deaths and Address Micronutrient Needs of Other Population Groups. 19 April 2010.', 'https://dev.lawyerly.ph/laws/55982', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate' and url = 'https://dev.lawyerly.ph/laws/55982');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ferrous_sulfate', 'WHO guideline - Daily iron supplementation in infants and children', 'World Health Organization. e-Library of Evidence for Nutrition Actions (eLENA): Daily iron supplementation in children 6-23 months of age. Updated 9 August 2023.', 'https://www.who.int/publications/i/item/9789241549523', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate'), 0)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate' and url = 'https://www.who.int/publications/i/item/9789241549523');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'peptic_ulcer_disease', 'med_ferrous_sulfate', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease'), 0), 'caution'::condition_safety, 'Label advises caution in existing gastrointestinal disease and GI irritation is common (applying this to peptic ulcer is an inference).'
where exists (select 1 from public.diseases where id = 'peptic_ulcer_disease')
  and exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease' and medicine_id = 'med_ferrous_sulfate');
-- med_ferrous_sulfate
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_ferrous_sulfate', 'adult', 0, 'Iron-deficiency anaemia (treatment)', 'PO', '65 mg elemental iron (1 × 200 mg tab)', '2–3× a day', '3 months', '—', 'MSF', 'Also for children ≥12 years'),
    ('med_ferrous_sulfate', 'adult', 1, 'Prevention (risk periods)', 'PO', '65 mg elemental iron', 'Once a day', 'During risk period', '—', 'MSF', 'Also for children ≥12 years'),
    ('med_ferrous_sulfate', 'adult', 2, 'Pregnancy (PH DOH program)', 'PO', '60 mg elemental iron + 0.4 mg folic acid', 'Once a day', '≥180 days (pregnancy to 3 months postpartum)', '—', 'PH DOH', 'Iron-folic acid tablet'),
    ('med_ferrous_sulfate', 'adult', 3, 'Pregnancy (WHO)', 'PO', '30–60 mg elemental iron + 400 µg folic acid', 'Once a day', 'Throughout pregnancy', '—', 'WHO 2024', ''),
    ('med_ferrous_sulfate', 'child', 4, 'Iron-deficiency anaemia, 6 to <12 y', 'PO', '65 mg elemental iron', '2× a day', '3 months', '—', 'MSF', ''),
    ('med_ferrous_sulfate', 'child', 5, 'Iron-deficiency anaemia, 6–12 y (tablets)', 'PO', '>22 kg: 1 tab; >44 kg: 1 tab 2×; >66 kg: 1 tab 3×', 'Daily', '—', '—', 'Label · UK SmPC', '200 mg tablets not recommended <6 y or <22 kg'),
    ('med_ferrous_sulfate', 'child', 6, 'Iron-deficiency anaemia, 1 month to <6 y', 'PO', '1.5–3 mg/kg elemental iron', '2× a day', '3 months', '—', 'MSF', 'Use syrup/drops'),
    ('med_ferrous_sulfate', 'child', 7, 'Prevention, 1 month to <12 y', 'PO', '1–2 mg/kg elemental iron', 'Once a day', 'During risk period', '65 mg/day', 'MSF', ''),
    ('med_ferrous_sulfate', 'neonate', 8, 'Iron-deficiency anaemia', 'PO', '1–2 mg/kg elemental iron', '2× a day', '3 months', '—', 'MSF', ''),
    ('med_ferrous_sulfate', 'neonate', 9, 'Prevention', 'PO', '4.5 mg elemental iron', 'Once a day', 'During risk period', '—', 'MSF', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_ferrous_sulfate');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_ferrous_sulfate', 'forms_ph', 0, '', 'Ferrous salt tablet (equiv. to 60 mg elemental iron); solution 15 mg elemental iron/0.6 mL drops (15 mL, 30 mL); solution 30 mg elemental iron/5 mL syrup (60 mL). Also ferrous salt + folic acid: 60 mg elemental iron + 400 µg folic acid tablet/capsule.', 'PNF'),
    ('med_ferrous_sulfate', 'pregnancy', 1, '', 'Recommended in pregnancy and lactation; for prevention in pregnancy prefer the combined iron + folic acid tablet (PH DOH: 60 mg + 0.4 mg daily for at least 180 days).', 'PH DOH'),
    ('med_ferrous_sulfate', 'administration', 2, '', 'Swallow tablets whole with water; do not chew, suck or hold in the mouth. Take with or before meals; with meals if GI upset.', 'Label · UK SmPC'),
    ('med_ferrous_sulfate', 'administration', 3, '', 'Rinse mouth or drink water after syrup to avoid tooth staining; increase the dose gradually if poorly tolerated.', 'MSF'),
    ('med_ferrous_sulfate', 'elderly', 4, '', 'Usual adult dose. Check swallowing/aspiration risk first (tablet aspiration can cause bronchial necrosis); watch for constipation and faecal impaction.', 'Label · UK SmPC'),
    ('med_ferrous_sulfate', 'monitor', 5, '', 'Before starting, look for an underlying cause of anaemia (e.g. GI blood loss). Check haemoglobin response. In homes with young children, store safely: 20 mg/kg elemental iron is toxic.', 'MSF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_ferrous_sulfate');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_ferrous_sulfate', 'MSF', 'MSF Essential Drugs', 'Medecins Sans Frontieres. Essential drugs - practical guidelines: Ferrous salts, oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ferrous-salts-16683659.html', 0),
    ('med_ferrous_sulfate', 'Label · UK SmPC', 'UK SmPC - Ferrous Sulfate Tablets 200mg (Sandoz)', 'Sandoz Limited. Ferrous Sulfate Tablets 200mg - Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=ferrous+sulfate#emc-4231', 1),
    ('med_ferrous_sulfate', 'PH DOH', 'PH DOH IFA policy (as reported in Nutrients 2021)', 'Felipe-Dimog EB, et al. Nutrients. 2021;13(9):3060, citing DOH AO 2010-0010 and AO 119 s. 2003.', 'https://www.mdpi.com/2072-6643/13/9/3060', 2),
    ('med_ferrous_sulfate', 'WHO 2024', 'WHO guideline (pregnancy iron)', 'World Health Organization. Guideline: daily iron and folic acid supplementation in pregnant women. Geneva: WHO; 2012 (dosing as summarised in WHO eLENA, July 2024).', 'https://www.who.int/publications/i/item/9789241501996', 3),
    ('med_ferrous_sulfate', 'PNF', 'Philippine National Formulary EML', 'Philippine National Formulary - Essential Medicines List, 8th ed. PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_ferrous_sulfate')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_ferrous_sulfate');


-- ================================================ med_furosemide  (Furosemide)
update public.medicines set description = 'Furosemide inhibits the Na+/K+/2Cl- cotransporter in the thick ascending limb of the loop of Henle, producing a potent, short-acting diuresis with loss of sodium, chloride, potassium, magnesium and water. It remains effective at low GFR. It is used for edema from heart failure, cirrhosis and renal disease, and for hypertension, particularly when renal function is reduced. In the Philippines, furosemide is on the PNF as 20 mg and 40 mg tablets (bioequivalence list B) and a 10 mg/mL injection. Injections are used only when oral dosing is not possible or not working, or when a fast effect is needed; patients are switched back to tablets as soon as possible. A loop diuretic is not the right treatment for nutritional (kwashiorkor) oedema or for oedema from pre-eclampsia.', updated_at = now()
where id = 'med_furosemide' and description = 'Furosemide inhibits the Na+/K+/2Cl- cotransporter in the thick ascending limb of the loop of Henle, producing a potent, short-acting diuresis with loss of sodium, chloride, potassium, magnesium and water. It remains effective at low GFR. It is used for edema from heart failure, cirrhosis and renal disease, and for hypertension, particularly when renal function is reduced.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC - Furosemide 40 mg tablets; UK SmPC - Furosemide 10 mg/ml Solution for Injection (Baxter); MSF Essential Drugs - Furosemide oral; MSF Essential Drugs - Furosemide injectable; Philippine National Formulary EML; UK SmPC - Furosemide 10 mg/ml Solution for Injection; DailyMed - LASIX tablets; MSF Essential Drugs' else source_attribution || '; UK SmPC - Furosemide 40 mg tablets; UK SmPC - Furosemide 10 mg/ml Solution for Injection (Baxter); MSF Essential Drugs - Furosemide oral; MSF Essential Drugs - Furosemide injectable; Philippine National Formulary EML; UK SmPC - Furosemide 10 mg/ml Solution for Injection; DailyMed - LASIX tablets; MSF Essential Drugs' end
where id = 'med_furosemide' and position('UK SmPC - Furosemide 40 mg tablets' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'indication', 'Peripheral oedema due to mechanical obstruction or venous insufficiency', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'indication' and content = 'Peripheral oedema due to mechanical obstruction or venous insufficiency');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'indication', 'Hypertensive crisis, emergency IV use (not in pregnancy)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'indication' and content = 'Hypertensive crisis, emergency IV use (not in pregnancy)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'adverse', 'Hypocalcaemia and hypochloraemic alkalosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'adverse' and content = 'Hypocalcaemia and hypochloraemic alkalosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'adverse', 'Acute renal failure', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'adverse' and content = 'Acute renal failure');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'adverse', 'Anaphylactic reactions', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'adverse' and content = 'Anaphylactic reactions');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'adverse', 'Nephrocalcinosis in premature infants', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'adverse' and content = 'Nephrocalcinosis in premature infants');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'contraindication', 'Hypersensitivity to sulphonamides or amiloride', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication' and content = 'Hypersensitivity to sulphonamides or amiloride');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'contraindication', 'Severe renal impairment (CrCl <30 mL/min/1.73 m²) or renal failure from nephrotoxic/hepatotoxic poisoning (UK label)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication' and content = 'Severe renal impairment (CrCl <30 mL/min/1.73 m²) or renal failure from nephrotoxic/hepatotoxic poisoning (UK label)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'contraindication', 'Severe hyponatraemia, severe hypokalaemia, hypovolaemia, dehydration or hypotension', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication' and content = 'Severe hyponatraemia, severe hypokalaemia, hypovolaemia, dehydration or hypotension');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'contraindication', 'Hepatic pre-coma or coma, hepatic encephalopathy', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication' and content = 'Hepatic pre-coma or coma, hepatic encephalopathy');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'contraindication', 'Addison''s disease; digitalis intoxication', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication' and content = 'Addison''s disease; digitalis intoxication');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'contraindication', 'Taking potassium supplements or potassium-sparing diuretics (UK label)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication' and content = 'Taking potassium supplements or potassium-sparing diuretics (UK label)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'contraindication', 'Breastfeeding', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication' and content = 'Breastfeeding');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'contraindication', 'Kwashiorkor (nutritional) oedema or oedema from pre-eclampsia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'contraindication' and content = 'Kwashiorkor (nutritional) oedema or oedema from pre-eclampsia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'Digoxin: diuretic-induced hypokalaemia increases digoxin toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'Digoxin: diuretic-induced hypokalaemia increases digoxin toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'Cisplatin: increased ototoxicity and possible nephrotoxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'Cisplatin: increased ototoxicity and possible nephrotoxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'Risperidone: higher mortality in elderly patients with dementia; weigh risks and benefits.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'Risperidone: higher mortality in elderly patients with dementia; weigh risks and benefits.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'High-dose cephalosporins: risk of renal impairment.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'High-dose cephalosporins: risk of renal impairment.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'Methotrexate: competition for renal tubular secretion; more toxicity at high doses.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'Methotrexate: competition for renal tubular secretion; more toxicity at high doses.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'Chloral hydrate: avoid; IV furosemide within 24 hours can cause flushing, sweating and tachycardia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'Chloral hydrate: avoid; IV furosemide within 24 hours can cause flushing, sweating and tachycardia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'Ciclosporin: increased risk of gouty arthritis.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'Ciclosporin: increased risk of gouty arthritis.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'Colestyramine or colestipol: give 2–3 hours apart.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'Colestyramine or colestipol: give 2–3 hours apart.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'Radiocontrast: more renal function decline in high-risk patients.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'Radiocontrast: more renal function decline in high-risk patients.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_furosemide', 'interaction', 'Insulin and oral antidiabetics: hyperglycaemia may reduce their effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_furosemide' and kind = 'interaction' and content = 'Insulin and oral antidiabetics: hyperglycaemia may reduce their effect.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_furosemide', 'UK SmPC - Furosemide 40 mg tablets', 'Furosemide 40 mg tablets - Summary of Product Characteristics. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=furosemide#emc-12129', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_furosemide'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_furosemide' and url = 'https://products.mhra.gov.uk/search/?search=furosemide#emc-12129');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_furosemide', 'UK SmPC - Furosemide 10 mg/ml Solution for Injection (Baxter)', 'Baxter Healthcare Limited. Furosemide 10 mg/ml Solution for Injection - Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=furosemide#emc-11522', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_furosemide'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_furosemide' and url = 'https://products.mhra.gov.uk/search/?search=furosemide#emc-11522');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_furosemide', 'MSF Essential Drugs - Furosemide oral', 'Medecins Sans Frontieres. Essential drugs - practical guidelines: Furosemide, oral.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-oral-16683798.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_furosemide'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_furosemide' and url = 'https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-oral-16683798.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_furosemide', 'MSF Essential Drugs - Furosemide injectable', 'Medecins Sans Frontieres. Essential drugs - practical guidelines: Furosemide, injectable.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-injectable-16682724.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_furosemide'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_furosemide' and url = 'https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-injectable-16682724.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_furosemide', 'Philippine National Formulary EML', 'Philippine National Formulary - Essential Medicines List, 8th ed. PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_furosemide'), 0)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_furosemide' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_furosemide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Can raise blood glucose; labels advise caution in diabetes and possible adjustment of antidiabetic doses.'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_furosemide');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_gastroenteritis', 'med_furosemide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis'), 0), 'avoid'::condition_safety, 'Dehydration and hypovolaemia are label contraindications (applying this to gastroenteritis is an inference).'
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis' and medicine_id = 'med_furosemide');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'cholera', 'med_furosemide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'cholera'), 0), 'avoid'::condition_safety, 'Dehydration and hypovolaemia are label contraindications (applying this to cholera is an inference).'
where exists (select 1 from public.diseases where id = 'cholera')
  and exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'cholera' and medicine_id = 'med_furosemide');
-- med_furosemide
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_furosemide', 'adult', 0, 'Oedema', 'PO', '40 mg', 'Once a day (morning)', '—', '80 mg/day (resistant oedema)', 'Label · UK SmPC', 'Maintenance 20 mg daily or 40 mg on alternate days'),
    ('med_furosemide', 'adult', 1, 'Hypertension', 'PO', '20–40 mg', '2× a day', 'Long-term', '40 mg 2× a day', 'Label · UK SmPC', 'If not enough, add another antihypertensive'),
    ('med_furosemide', 'adult', 2, 'Oedema', 'IV', '20–50 mg', 'Increase by 20 mg, not more often than every 2 h', 'Switch to oral ASAP', '1500 mg/day', 'Label · UK SmPC inj', 'Same dose IM; >50 mg as slow IV infusion'),
    ('med_furosemide', 'adult', 3, 'Acute pulmonary oedema', 'IV', '40 mg slow IV', '80 mg if no response within 1 h', 'Per response', '—', 'MSF', 'IM not suitable'),
    ('med_furosemide', 'child', 4, 'Oedema', 'PO', '2 mg/kg', 'Single dose; +1–2 mg/kg after ≥6–8 h', 'Per response', '6 mg/kg/dose', 'Label · DailyMed', ''),
    ('med_furosemide', 'child', 5, 'Oedema', 'IV', '0.5–1.5 mg/kg/day', 'Daily', 'Per response', '20 mg/day', 'Label · UK SmPC inj', 'IV or IM')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_furosemide');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_furosemide', 'renal', 0, 'CrCl <30', 'Contraindicated (UK label); for IV infusion with serum creatinine >5 mg/dL, max rate 2.5 mg/min.', 'Label · UK SmPC'),
    ('med_furosemide', 'hepatic', 1, '', 'Dose may need adjusting in liver congestion or dysfunction, with monitoring; contraindicated in hepatic pre-coma/coma and hepatic encephalopathy. Hypokalaemia is more likely in cirrhosis.', 'Label · UK SmPC'),
    ('med_furosemide', 'elderly', 2, '', 'Slower elimination: start at the low end and titrate to response.', 'Label · UK SmPC'),
    ('med_furosemide', 'pregnancy', 3, '', 'Do not use in pregnancy unless there are compelling reasons; monitor fetal growth. Not for hypertension of pregnancy or pre-eclampsia oedema. Breastfeeding: contraindicated (passes into milk, may suppress lactation).', 'Label · UK SmPC'),
    ('med_furosemide', 'administration', 4, '', 'IV infusion max 4 mg/min; doses >50 mg by slow infusion. Continuous infusion or small doses about every 4 h are preferred over large boluses. Take tablets in the morning.', 'Label · UK SmPC inj'),
    ('med_furosemide', 'forms_ph', 5, '', 'Oral: 20 mg and 40 mg tablet (List B, bioequivalence required). Injection: 10 mg/mL, 2 mL ampul (IM, IV); 10 mg/mL, 25 mL ampul (IV infusion).', 'PNF'),
    ('med_furosemide', 'monitor', 6, '', 'Serum sodium, potassium, creatinine and BUN (often in the first months, then periodically); blood pressure including orthostatic; urine output (watch for retention with prostatic enlargement); glucose in diabetes; FBC for blood dyscrasias. Correct hypovolaemia and electrolytes before starting.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_furosemide');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_furosemide', 'Label · UK SmPC', 'UK SmPC - Furosemide 40 mg tablets', 'Furosemide 40 mg tablets - SmPC. emc.', 'https://products.mhra.gov.uk/search/?search=furosemide#emc-12129', 0),
    ('med_furosemide', 'Label · UK SmPC inj', 'UK SmPC - Furosemide 10 mg/ml Solution for Injection', 'Baxter Healthcare Limited. Furosemide 10 mg/ml Solution for Injection - SmPC. emc.', 'https://products.mhra.gov.uk/search/?search=furosemide#emc-11522', 1),
    ('med_furosemide', 'Label · DailyMed', 'DailyMed - LASIX tablets', 'LASIX (furosemide) tablets. Prescribing information. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2c9b4d8f-0770-482d-a9e6-9c616a440b1a', 2),
    ('med_furosemide', 'MSF', 'MSF Essential Drugs', 'Medecins Sans Frontieres. Essential drugs: Furosemide oral / injectable.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/furosemide-injectable-16682724.html', 3),
    ('med_furosemide', 'PNF', 'Philippine National Formulary EML', 'Philippine National Formulary - Essential Medicines List, 8th ed. PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_furosemide')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_furosemide');


-- ================================================ med_gliclazide  (Gliclazide)
update public.medicines set description = 'Gliclazide is a second-generation sulfonylurea that binds the SUR1 subunit of ATP-sensitive potassium channels on pancreatic beta cells, causing depolarization, calcium influx and insulin release regardless of blood glucose level. Hypoglycemia and weight gain are the main drawbacks. It is used in type 2 diabetes when metformin alone is insufficient or not tolerated; it is not marketed in the United States. In the Philippines it is listed in the PNF Essential Medicines List as 30 mg and 60 mg modified-release tablets and an 80 mg tablet, and it has been on the WHO Model List of Essential Medicines since 2013. MSF guidance places it second line, alone when metformin is not tolerated or added to metformin when control is inadequate. It is cleared mainly by hepatic metabolism (under 1% excreted unchanged in urine) and is about 95% protein-bound, so dialysis does not help in overdose.', updated_at = now()
where id = 'med_gliclazide' and description = 'Gliclazide is a second-generation sulfonylurea that binds the SUR1 subunit of ATP-sensitive potassium channels on pancreatic beta cells, causing depolarization, calcium influx and insulin release regardless of blood glucose level. Hypoglycemia and weight gain are the main drawbacks. It is used in type 2 diabetes when metformin alone is insufficient or not tolerated; it is not marketed in the United States.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PhilHealth); WHO Model List of Essential Medicines' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PhilHealth); WHO Model List of Essential Medicines' end
where id = 'med_gliclazide' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'indication', 'Add-on to metformin when glycaemic control is inadequate on metformin alone', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'indication' and content = 'Add-on to metformin when glycaemic control is inadequate on metformin alone');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'adverse', 'Cholestatic jaundice (stop treatment)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'adverse' and content = 'Cholestatic jaundice (stop treatment)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'adverse', 'DRESS (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'adverse' and content = 'DRESS (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'adverse', 'Hyponatraemia, allergic vasculitis, agranulocytosis and pancytopenia (sulfonylurea class effects)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'adverse' and content = 'Hyponatraemia, allergic vasculitis, agranulocytosis and pancytopenia (sulfonylurea class effects)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'adverse', 'Acute porphyria reported with other sulfonylureas in patients with porphyria', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'adverse' and content = 'Acute porphyria reported with other sulfonylureas in patients with porphyria');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'interaction', 'H2 antagonists, MAOIs, sulfonamides (e.g., co-trimoxazole), trimethoprim, anabolic steroids: increased hypoglycaemia risk.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction' and content = 'H2 antagonists, MAOIs, sulfonamides (e.g., co-trimoxazole), trimethoprim, anabolic steroids: increased hypoglycaemia risk.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'interaction', 'Macrolides (clarithromycin, erythromycin): increased hypoglycaemia risk; monitor glucose.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction' and content = 'Macrolides (clarithromycin, erythromycin): increased hypoglycaemia risk; monitor glucose.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'interaction', 'IV salbutamol, terbutaline or ritodrine, and tetracosactide: raised blood glucose.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction' and content = 'IV salbutamol, terbutaline or ritodrine, and tetracosactide: raised blood glucose.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'interaction', 'Rifampicin and St John''s wort: reduced gliclazide effect or exposure.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction' and content = 'Rifampicin and St John''s wort: reduced gliclazide effect or exposure.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_gliclazide', 'interaction', 'Hydrochlorothiazide: may raise blood glucose and reduce control.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_gliclazide' and kind = 'interaction' and content = 'Hydrochlorothiazide: may raise blood glucose and reduce control.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_gliclazide', 'UK SmPC (emc)', 'Gliclazide 80 mg Tablets. Summary of Product Characteristics. Flamingo Pharma (UK) Ltd. electronic medicines compendium (emc); text revised 01/2025.', 'https://products.mhra.gov.uk/search/?search=gliclazide#emc-13676', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_gliclazide'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_gliclazide' and url = 'https://products.mhra.gov.uk/search/?search=gliclazide#emc-13676');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_gliclazide', 'MSF Essential Drugs', 'Médecins Sans Frontières. Gliclazide oral. In: Essential Drugs – practical guidelines. MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/gliclazide-oral-27983946.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_gliclazide'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_gliclazide' and url = 'https://medicalguidelines.msf.org/viewport/EssDr/english/gliclazide-oral-27983946.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_gliclazide', 'Philippine National Formulary (PhilHealth)', 'Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_gliclazide'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_gliclazide' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_gliclazide', 'WHO Model List of Essential Medicines', 'World Health Organization. eEML – Electronic Essential Medicines List: Gliclazide (first added 2013, TRS 985).', 'https://list.essentialmeds.org/medicines/194', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_gliclazide'), 0)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_gliclazide' and url = 'https://list.essentialmeds.org/medicines/194');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_gliclazide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Mild–moderate renal impairment: usual dose with careful monitoring; contraindicated in severe renal insufficiency (use insulin).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_gliclazide');
-- med_gliclazide
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_gliclazide', 'adult', 0, 'Type 2 diabetes (MR tablet)', 'PO', '30 mg', 'Once a day', 'Long-term', '120 mg/day', 'Label · UK SmPC MR', 'With breakfast; step up to 60, 90, 120 mg at ≥1-month intervals (2 weeks if glucose not falling)'),
    ('med_gliclazide', 'adult', 1, 'Type 2 diabetes (80 mg tablet)', 'PO', '40–80 mg', 'Once a day', 'Long-term', '320 mg/day', 'Label · UK SmPC', 'Max 160 mg per dose; above 160 mg/day give 2× a day with main meals'),
    ('med_gliclazide', 'adult', 2, 'Type 2 diabetes, second line (80 mg tablet)', 'PO', '40 mg, then 80–160 mg/day', 'Once a day', 'Long-term', '240 mg/day', 'MSF', 'Morning dose; increase by 40 mg every 2 weeks; split doses above 80 mg/day into 2')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_gliclazide');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_gliclazide', 'renal', 0, '', 'Mild–moderate impairment: same regimen with careful monitoring. Severe renal insufficiency: contraindicated (insulin recommended). Not removed by dialysis (strongly protein-bound).', 'Label · UK SmPC MR'),
    ('med_gliclazide', 'hepatic', 1, '', 'Severe hepatic insufficiency: contraindicated (insulin recommended). Stop if cholestatic jaundice develops.', 'Label · UK SmPC MR'),
    ('med_gliclazide', 'elderly', 2, '', 'Same regimen as under 65. Start at the minimum dose (30 mg MR / 40–80 mg) in high-risk patients: malnourished, poorly controlled endocrine disease (hypopituitarism, hypothyroidism, adrenal insufficiency), after stopping long-term/high-dose steroids, or severe vascular disease.', 'Label · UK SmPC MR'),
    ('med_gliclazide', 'pregnancy', 3, '', 'Avoid in pregnancy; switch to insulin before conception or as soon as pregnancy is found. Contraindicated in breastfeeding (risk of neonatal hypoglycaemia).', 'Label · UK SmPC MR'),
    ('med_gliclazide', 'administration', 4, '', 'MR tablet: swallow whole as one dose at breakfast; do not double a missed dose. One 80 mg tablet ≈ one 30 mg MR tablet when switching (monitor glucose). After a long half-life sulfonylurea, a few drug-free days may be needed. Not for children (no data).', 'Label · UK SmPC MR'),
    ('med_gliclazide', 'forms_ph', 5, '', 'Gliclazide 30 mg and 60 mg modified-release (MR) oral tablets; 80 mg oral tablet.', 'PNF'),
    ('med_gliclazide', 'monitor', 6, '', 'Blood glucose/HbA1c; teach patient and family hypoglycaemia symptoms and risk factors (missed meals, alcohol, exercise); close glucose checks with fluoroquinolones, illness or surgery; consider an alternative in G6PD deficiency. Hypoglycaemic coma: 50 mL 20–30% glucose IV, then 10% glucose infusion with close monitoring.', 'Label · UK SmPC MR')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_gliclazide');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_gliclazide', 'Label · UK SmPC MR', 'UK SmPC (emc)', 'Diamicron 30 mg MR Tablets SmPC, Servier; text revised 02/2020.', 'https://products.mhra.gov.uk/search/?search=gliclazide#emc-1321', 0),
    ('med_gliclazide', 'Label · UK SmPC', 'UK SmPC (emc)', 'Gliclazide 80 mg Tablets SmPC, Flamingo Pharma (UK) Ltd; text revised 01/2025.', 'https://products.mhra.gov.uk/search/?search=gliclazide#emc-13676', 1),
    ('med_gliclazide', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Gliclazide oral. Essential Drugs – practical guidelines.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/gliclazide-oral-27983946.html', 2),
    ('med_gliclazide', 'PNF', 'Philippine National Formulary (PhilHealth)', 'PNF Essential Medicines List, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_gliclazide')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_gliclazide');


-- ================================================ med_hydrochlorothiazide  (Hydrochlorothiazide)
update public.medicines set description = 'Hydrochlorothiazide inhibits the Na+/Cl- cotransporter in the distal convoluted tubule, increasing sodium and water excretion. Blood pressure falls initially from volume reduction and long-term from reduced peripheral vascular resistance. It is used alone or in combination for hypertension and for edema, and is less effective when renal function is severely reduced. In the Philippines it is listed in the PNF Essential Medicines List as 12.5 mg and 25 mg tablets and in fixed combinations with losartan, enalapril and irbesartan. In the national primary-care hypertension protocol, hydrochlorothiazide 25 mg once daily is the step-4 add-on to amlodipine plus losartan (or the patient is referred). Long-term use carries a dose-dependent risk of non-melanoma skin cancer, thought to relate to its photosensitising effect.', updated_at = now()
where id = 'med_hydrochlorothiazide' and description = 'Hydrochlorothiazide inhibits the Na+/Cl- cotransporter in the distal convoluted tubule, increasing sodium and water excretion. Blood pressure falls initially from volume reduction and long-term from reduced peripheral vascular resistance. It is used alone or in combination for hypertension and for edema, and is less effective when renal function is severely reduced.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'MSF Essential Drugs; Philippine National Formulary (PhilHealth); National Protocol for Hypertension Management (Philippines); MHRA Drug Safety Update; WHO Model List of Essential Medicines; DailyMed (US National Library of Medicine)' else source_attribution || '; MSF Essential Drugs; Philippine National Formulary (PhilHealth); National Protocol for Hypertension Management (Philippines); MHRA Drug Safety Update; WHO Model List of Essential Medicines; DailyMed (US National Library of Medicine)' end
where id = 'med_hydrochlorothiazide' and position('MSF Essential Drugs' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'adverse', 'Dehydration and hypotension, including orthostatic hypotension', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse' and content = 'Dehydration and hypotension, including orthostatic hypotension');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'adverse', 'Headache, dizziness, vertigo, paraesthesia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse' and content = 'Headache, dizziness, vertigo, paraesthesia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'adverse', 'Impotence', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse' and content = 'Impotence');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'adverse', 'Non-melanoma skin cancer (basal cell and squamous cell carcinoma, lip cancer) with high cumulative long-term use', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse' and content = 'Non-melanoma skin cancer (basal cell and squamous cell carcinoma, lip cancer) with high cumulative long-term use');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'adverse', 'Interstitial nephritis, renal dysfunction', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse' and content = 'Interstitial nephritis, renal dysfunction');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'adverse', 'Sialadenitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse' and content = 'Sialadenitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'adverse', 'Hypersensitivity: anaphylaxis, necrotising angiitis, pneumonitis, pulmonary oedema', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse' and content = 'Hypersensitivity: anaphylaxis, necrotising angiitis, pneumonitis, pulmonary oedema');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'adverse', 'Exacerbation or activation of systemic lupus erythematosus', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse' and content = 'Exacerbation or activation of systemic lupus erythematosus');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'adverse', 'Transient blurred vision, xanthopsia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'adverse' and content = 'Transient blurred vision, xanthopsia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'contraindication', 'Severe renal failure', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'contraindication' and content = 'Severe renal failure');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'interaction', 'Cholestyramine and colestipol: reduce hydrochlorothiazide absorption (by up to 85% and 43%).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction' and content = 'Cholestyramine and colestipol: reduce hydrochlorothiazide absorption (by up to 85% and 43%).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'interaction', 'Drugs that cause hypotension (e.g., haloperidol, amitriptyline) and other antihypertensives: additive hypotension.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction' and content = 'Drugs that cause hypotension (e.g., haloperidol, amitriptyline) and other antihypertensives: additive hypotension.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'interaction', 'SSRIs, carbamazepine: added risk of hyponatraemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction' and content = 'SSRIs, carbamazepine: added risk of hyponatraemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'interaction', 'Laxatives, amphotericin B: added potassium loss.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction' and content = 'Laxatives, amphotericin B: added potassium loss.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'interaction', 'Calcium or vitamin D (ergocalciferol): risk of hypercalcaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction' and content = 'Calcium or vitamin D (ergocalciferol): risk of hypercalcaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'interaction', 'Pressor amines (e.g., noradrenaline): possibly reduced response.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction' and content = 'Pressor amines (e.g., noradrenaline): possibly reduced response.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_hydrochlorothiazide', 'interaction', 'Nondepolarising muscle relaxants: possibly increased response.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_hydrochlorothiazide' and kind = 'interaction' and content = 'Nondepolarising muscle relaxants: possibly increased response.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_hydrochlorothiazide', 'MSF Essential Drugs', 'Médecins Sans Frontières. Hydrochlorothiazide oral. In: Essential Drugs – practical guidelines. MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/hydrochlorothiazide-oral-16683854.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide' and url = 'https://medicalguidelines.msf.org/viewport/EssDr/english/hydrochlorothiazide-oral-16683854.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_hydrochlorothiazide', 'Philippine National Formulary (PhilHealth)', 'Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_hydrochlorothiazide', 'National Protocol for Hypertension Management (Philippines)', 'National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives; 2021 (rev. 2023).', 'https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide' and url = 'https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_hydrochlorothiazide', 'MHRA Drug Safety Update', 'Medicines and Healthcare products Regulatory Agency. Hydrochlorothiazide: risk of non-melanoma skin cancer, particularly in long-term use. Drug Safety Update 2018;12(4).', 'https://www.gov.uk/drug-safety-update/hydrochlorothiazide-risk-of-non-melanoma-skin-cancer-particularly-in-long-term-use', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide' and url = 'https://www.gov.uk/drug-safety-update/hydrochlorothiazide-risk-of-non-melanoma-skin-cancer-particularly-in-long-term-use');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_hydrochlorothiazide', 'WHO Model List of Essential Medicines', 'World Health Organization. eEML – Electronic Essential Medicines List: Hydrochlorothiazide (first added 1977).', 'https://list.essentialmeds.org/medicines/139', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide'), 0)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_hydrochlorothiazide' and url = 'https://list.essentialmeds.org/medicines/139');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_hydrochlorothiazide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Use with caution in severe renal disease (may precipitate azotemia; stop if impairment progresses); MSF advises not to give in severe renal failure.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_hydrochlorothiazide');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_hydrochlorothiazide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Can raise blood glucose; doses of oral antidiabetics or insulin may need adjusting.'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_hydrochlorothiazide');
-- med_hydrochlorothiazide
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_hydrochlorothiazide', 'adult', 0, 'Hypertension', 'PO', '12.5–25 mg', 'Once a day', 'Long-term', '25 mg/day', 'MSF', 'Morning dose'),
    ('med_hydrochlorothiazide', 'adult', 1, 'Hypertension (PH primary care, step 4)', 'PO', '25 mg', 'Once a day', 'Long-term', '—', 'PH HTN protocol', 'Added to amlodipine 10 mg + losartan 100 mg if BP still high after 1 month (or refer)'),
    ('med_hydrochlorothiazide', 'adult', 2, 'Hypertension', 'PO', '25 mg, up to 50 mg/day', 'Once a day or 2× a day', 'Long-term', '50 mg/day', 'Label · DailyMed', 'Doses above 50 mg/day cause marked potassium loss'),
    ('med_hydrochlorothiazide', 'adult', 3, 'Oedema (renal, hepatic, heart failure)', 'PO', '25 mg', 'Once a day or 2× a day', 'By response', '100 mg/day', 'MSF', 'Morning dose'),
    ('med_hydrochlorothiazide', 'adult', 4, 'Oedema', 'PO', '25–100 mg/day', 'Once a day or divided', 'By response', '100 mg/day', 'Label · DailyMed', 'Intermittent dosing (alternate days or 3–5 days a week) lowers electrolyte risk'),
    ('med_hydrochlorothiazide', 'child', 5, 'Oedema / hypertension', 'PO', '1–2 mg/kg/day ÷ 1–2', 'Once a day or 2× a day', 'By response', '37.5 mg/day (<2 y); 100 mg/day (2–12 y)', 'Label · DailyMed', 'Infants <6 months may need up to 3 mg/kg/day ÷ 2')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_hydrochlorothiazide');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_hydrochlorothiazide', 'renal', 0, 'Severe', 'Do not give in severe renal failure.', 'MSF'),
    ('med_hydrochlorothiazide', 'renal', 1, '', 'Use with caution in severe renal disease: may precipitate azotemia and accumulate; withhold or stop if renal impairment progresses.', 'Label · DailyMed'),
    ('med_hydrochlorothiazide', 'hepatic', 2, '', 'Use with caution in hepatic impairment or progressive liver disease: small fluid/electrolyte shifts may precipitate hepatic coma.', 'Label · DailyMed'),
    ('med_hydrochlorothiazide', 'elderly', 3, '', 'Use with caution.', 'MSF'),
    ('med_hydrochlorothiazide', 'pregnancy', 4, '', 'MSF lists pregnancy and breastfeeding as contraindications. Thiazides cross the placenta (risk of fetal/neonatal jaundice and thrombocytopenia) and pass into breast milk; routine use in normal pregnancy is inappropriate.', 'MSF'),
    ('med_hydrochlorothiazide', 'administration', 5, '', 'Take in the morning. Recommend a potassium-rich diet; give a sustained-release potassium supplement if K+ < 3.5 mmol/L. Not indicated for nutritional oedema. Stop before parathyroid function tests.', 'MSF'),
    ('med_hydrochlorothiazide', 'forms_ph', 6, '', 'Hydrochlorothiazide 12.5 mg and 25 mg oral tablets. Fixed combinations: losartan 50 mg + HCTZ 12.5 mg, enalapril 20 mg + HCTZ 12.5 mg, irbesartan 150 mg + HCTZ 12.5 mg tablets.', 'PNF'),
    ('med_hydrochlorothiazide', 'monitor', 7, '', 'Serum electrolytes (K+, Na+, Mg2+, Ca2+), renal function, glucose, uric acid and lipids periodically; BP including orthostatic drop; confirm adherence before stepping up.', 'Label · DailyMed'),
    ('med_hydrochlorothiazide', 'monitor', 8, '', 'Long-term use: advise regular skin self-checks and sun/UV protection; examine new or changing lesions; reconsider HCTZ in patients with previous skin cancer.', 'MHRA 2018')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_hydrochlorothiazide');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_hydrochlorothiazide', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Hydrochlorothiazide oral. Essential Drugs – practical guidelines.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/hydrochlorothiazide-oral-16683854.html', 0),
    ('med_hydrochlorothiazide', 'Label · DailyMed', 'DailyMed (US National Library of Medicine)', 'Hydrochlorothiazide Tablets USP 25 mg and 50 mg. Prescribing information. Caraco Pharmaceutical Laboratories; 2007.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=7b38ac8a-4540-4eb2-aedd-9aa966d22190', 1),
    ('med_hydrochlorothiazide', 'PH HTN protocol', 'National Protocol for Hypertension Management (Philippines)', 'National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives.', 'https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf', 2),
    ('med_hydrochlorothiazide', 'PNF', 'Philippine National Formulary (PhilHealth)', 'PNF Essential Medicines List, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 3),
    ('med_hydrochlorothiazide', 'MHRA 2018', 'MHRA Drug Safety Update', 'Hydrochlorothiazide: risk of non-melanoma skin cancer, particularly in long-term use. Drug Safety Update, November 2018.', 'https://www.gov.uk/drug-safety-update/hydrochlorothiazide-risk-of-non-melanoma-skin-cancer-particularly-in-long-term-use', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_hydrochlorothiazide')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_hydrochlorothiazide');


update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
