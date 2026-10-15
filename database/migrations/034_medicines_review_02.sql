-- 034_medicines_review_02.sql  -  medicine review b02: med_budesonide_formoterol, med_ceftriaxone, med_cetirizine, med_ciprofloxacin, med_clarithromycin, med_clopidogrel, med_coamoxiclav, med_colchicine, med_cotrimoxazole, med_dapagliflozin
-- Adds only: longer descriptions, new facts, references, disease links, and dosage
-- tables (for medicines that have none yet). Nothing is deleted or reworded.
-- Needs 030_medicine_doses.sql first. Safe to run twice (every insert is guarded).

begin;

-- ================================================ med_budesonide_formoterol  (Budesonide + Formoterol)
update public.medicines set description = 'Budesonide is an inhaled glucocorticoid that suppresses airway inflammation, and formoterol is a long-acting beta-2 agonist with a rapid onset of bronchodilation. The combination provides maintenance control of asthma and COPD. Because formoterol acts quickly, GINA also recommends budesonide-formoterol as an as-needed anti-inflammatory reliever and for maintenance-and-reliever therapy in asthma, whereas US labeling covers maintenance use only. UK labeling licenses the dry-powder inhaler for three asthma regimens: maintenance only, maintenance-and-reliever (12 years and older), and reliever-only in mild asthma (12 years and older). Strengths may be stated as metered dose (e.g. 200/6 mcg) or delivered dose (160/4.5 mcg); these are the same product. In the Philippines the PNF lists both a dry-powder inhaler and a metered-dose inhaler.', updated_at = now()
where id = 'med_budesonide_formoterol' and description = 'Budesonide is an inhaled glucocorticoid that suppresses airway inflammation, and formoterol is a long-acting beta-2 agonist with a rapid onset of bronchodilation. The combination provides maintenance control of asthma and COPD. Because formoterol acts quickly, GINA also recommends budesonide-formoterol as an as-needed anti-inflammatory reliever and for maintenance-and-reliever therapy in asthma, whereas US labeling covers maintenance use only.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); PhilHealth / DOH (PNF-EML); DailyMed (FDA label); Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); PhilHealth / DOH (PNF-EML); DailyMed (FDA label); Philippine National Formulary – EML' end
where id = 'med_budesonide_formoterol' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'adverse', 'Throat irritation, cough and hoarseness', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse' and content = 'Throat irritation, cough and hoarseness');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'adverse', 'Anxiety, sleep disorders, aggression and psychomotor hyperactivity (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse' and content = 'Anxiety, sleep disorders, aggression and psychomotor hyperactivity (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'adverse', 'Dizziness, nausea, blurred vision (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse' and content = 'Dizziness, nausea, blurred vision (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'adverse', 'Bruising and muscle cramps (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse' and content = 'Bruising and muscle cramps (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'adverse', 'Paradoxical bronchospasm (very rare; stop and use a rapid-acting bronchodilator)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse' and content = 'Paradoxical bronchospasm (very rare; stop and use a rapid-acting bronchodilator)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'adverse', 'Growth retardation in children (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse' and content = 'Growth retardation in children (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'adverse', 'QTc prolongation, cardiac arrhythmias, angina (rare to very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse' and content = 'QTc prolongation, cardiac arrhythmias, angina (rare to very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'adverse', 'Taste disturbance, depression and behavioural changes (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'adverse' and content = 'Taste disturbance, depression and behavioural changes (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'contraindication', 'Turbohaler: hypersensitivity to lactose (contains small amounts of milk proteins)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'contraindication' and content = 'Turbohaler: hypersensitivity to lactose (contains small amounts of milk proteins)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'interaction', 'QT-prolonging drugs (e.g., quinidine, disopyramide, phenothiazines): increased risk of ventricular arrhythmias.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction' and content = 'QT-prolonging drugs (e.g., quinidine, disopyramide, phenothiazines): increased risk of ventricular arrhythmias.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'interaction', 'Xanthines (e.g., theophylline) and systemic corticosteroids: additive hypokalaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction' and content = 'Xanthines (e.g., theophylline) and systemic corticosteroids: additive hypokalaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'interaction', 'Digitalis glycosides: hypokalaemia raises the risk of arrhythmias.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction' and content = 'Digitalis glycosides: hypokalaemia raises the risk of arrhythmias.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'interaction', 'Halogenated hydrocarbon anaesthetics: increased arrhythmia risk.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction' and content = 'Halogenated hydrocarbon anaesthetics: increased arrhythmia risk.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'interaction', 'L-dopa, L-thyroxine, oxytocin and alcohol: may impair cardiac tolerance to beta-2 agonists.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction' and content = 'L-dopa, L-thyroxine, oxytocin and alcohol: may impair cardiac tolerance to beta-2 agonists.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_budesonide_formoterol', 'interaction', 'Strong CYP3A4 inhibitors: maintenance-and-reliever therapy is not recommended with them.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_budesonide_formoterol' and kind = 'interaction' and content = 'Strong CYP3A4 inhibitors: maintenance-and-reliever therapy is not recommended with them.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_budesonide_formoterol', 'UK SmPC (emc)', 'Symbicort Turbohaler 200/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd; updated March 2023. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1327', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_budesonide_formoterol'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_budesonide_formoterol' and url = 'https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1327');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_budesonide_formoterol', 'UK SmPC (emc)', 'Symbicort Turbohaler 100/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1326', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_budesonide_formoterol'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_budesonide_formoterol' and url = 'https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1326');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_budesonide_formoterol', 'PhilHealth / DOH (PNF-EML)', 'Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_budesonide_formoterol'), 0)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_budesonide_formoterol' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'tuberculosis', 'med_budesonide_formoterol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'tuberculosis'), 0), 'caution'::condition_safety, 'Re-evaluate use in active or quiescent pulmonary TB (UK SmPC).'
where exists (select 1 from public.diseases where id = 'tuberculosis')
  and exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'tuberculosis' and medicine_id = 'med_budesonide_formoterol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_budesonide_formoterol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Beta-2 agonist can raise glucose; consider extra blood glucose checks (UK SmPC).'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_budesonide_formoterol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'graves_disease', 'med_budesonide_formoterol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'graves_disease'), 0), 'caution'::condition_safety, 'Use with caution in thyrotoxicosis (UK SmPC).'
where exists (select 1 from public.diseases where id = 'graves_disease')
  and exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'graves_disease' and medicine_id = 'med_budesonide_formoterol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hypertension', 'med_budesonide_formoterol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hypertension'), 0), 'caution'::condition_safety, 'Use with caution in severe hypertension (UK SmPC).'
where exists (select 1 from public.diseases where id = 'hypertension')
  and exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hypertension' and medicine_id = 'med_budesonide_formoterol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_budesonide_formoterol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'Use with caution in severe heart failure or tachyarrhythmias (UK SmPC).'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_budesonide_formoterol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_coronary_syndrome', 'med_budesonide_formoterol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome'), 0), 'caution'::condition_safety, 'Use with caution in ischaemic heart disease (UK SmPC).'
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome' and medicine_id = 'med_budesonide_formoterol');
-- med_budesonide_formoterol
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_budesonide_formoterol', 'adult', 0, 'Asthma, maintenance (DPI 160/4.5)', 'Inhaled', '1–2 inhalations', '2× a day', 'Long-term', '4 inhalations 2× a day', 'Label · UK SmPC', 'Separate reliever for rescue; UK labels this as 200/6 (metered)'),
    ('med_budesonide_formoterol', 'adult', 1, 'Asthma, maintenance-and-reliever (DPI 160/4.5)', 'Inhaled', '2 inhalations/day + 1 as needed', 'Once or 2× a day + as needed', 'Long-term', '6 per occasion; 12/day short-term', 'Label · UK SmPC', '>8 inhalations/day: reassess'),
    ('med_budesonide_formoterol', 'adult', 2, 'Mild asthma, reliever only (DPI 160/4.5)', 'Inhaled', '1 inhalation', 'As needed', '—', '6 per occasion; 12/day short-term', 'Label · UK SmPC', 'Repeat once if still symptomatic after a few minutes'),
    ('med_budesonide_formoterol', 'adult', 3, 'Asthma, maintenance (pMDI 80/4.5 or 160/4.5)', 'Inhaled', '2 inhalations', '2× a day', 'Long-term', '160/4.5 strength', 'Label · US', 'Strength by severity and prior ICS'),
    ('med_budesonide_formoterol', 'adult', 4, 'COPD (160/4.5)', 'Inhaled', '2 inhalations', '2× a day', 'Long-term', '—', 'Label · UK SmPC', ''),
    ('med_budesonide_formoterol', 'child', 5, 'Asthma, maintenance, 12–17 y (DPI)', 'Inhaled', '1–2 inhalations', '2× a day', 'Long-term', '—', 'Label · UK SmPC', '80/4.5 or 160/4.5'),
    ('med_budesonide_formoterol', 'child', 6, 'Asthma, maintenance-and-reliever, 12–17 y (DPI 80/4.5)', 'Inhaled', '2 inhalations/day + 1 as needed', 'Once or 2× a day + as needed', 'Long-term', '6 per occasion; 12/day short-term', 'Label · UK SmPC 100/6', '>8 inhalations/day: reassess'),
    ('med_budesonide_formoterol', 'child', 7, 'Asthma, maintenance, 6–11 y (DPI 80/4.5)', 'Inhaled', '1–2 inhalations', '2× a day', 'Long-term', '—', 'Label · UK SmPC 100/6', 'Not recommended <6 y'),
    ('med_budesonide_formoterol', 'child', 8, 'Asthma, maintenance-and-reliever, 6–11 y (DPI 80/4.5)', 'Inhaled', '1 inhalation + 1 as needed', 'Once or 2× a day + as needed', 'Long-term', '4 per occasion; 8/day short-term', 'Label · UK SmPC 100/6', '>4 inhalations/day: reassess'),
    ('med_budesonide_formoterol', 'child', 9, 'Asthma, maintenance, 6–11 y (pMDI 80/4.5)', 'Inhaled', '2 inhalations', '2× a day', 'Long-term', '—', 'Label · US', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_budesonide_formoterol');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_budesonide_formoterol', 'renal', 0, '', 'No data available in renal impairment.', 'Label · UK SmPC'),
    ('med_budesonide_formoterol', 'hepatic', 1, '', 'No data; exposure may rise in severe liver cirrhosis because both drugs are cleared mainly by the liver. Monitor closely.', 'Label · UK SmPC'),
    ('med_budesonide_formoterol', 'elderly', 2, '', 'No special dosing requirements.', 'Label · UK SmPC'),
    ('med_budesonide_formoterol', 'pregnancy', 3, '', 'Use only if benefit outweighs risk, at the lowest effective budesonide dose; ~2,000 pregnancies with inhaled budesonide showed no rise in malformations; formoterol data inadequate. Budesonide passes into breast milk; no infant effects expected at therapeutic doses.', 'Label · UK SmPC'),
    ('med_budesonide_formoterol', 'administration', 4, '', 'Turbohaler: breathe in forcefully and deeply through the mouthpiece; never breathe out into it; replace cover. Patients may not taste the dose.', 'Label · UK SmPC 100/6'),
    ('med_budesonide_formoterol', 'administration', 5, '', 'pMDI: shake for 5 seconds before each spray; spray 2 test puffs before first use or if dropped or unused >7 days; take doses about 12 h apart.', 'Label · US'),
    ('med_budesonide_formoterol', 'administration', 6, '', 'Do not stop abruptly; taper the maintenance dose. Do not start during an exacerbation.', 'Label · UK SmPC'),
    ('med_budesonide_formoterol', 'forms_ph', 7, '', 'DPI 80/4.5 mcg, 160/4.5 mcg and 320/9 mcg × 60 doses; MDI 80/4.5 mcg and 160/4.5 mcg × 120 doses.', 'PNF'),
    ('med_budesonide_formoterol', 'monitor', 8, '', 'Track reliever use: rising use or >8 inhalations/day (adults) means poor control; reassess.', 'Label · UK SmPC'),
    ('med_budesonide_formoterol', 'monitor', 9, '', 'Check height regularly in children on long-term treatment.', 'Label · UK SmPC'),
    ('med_budesonide_formoterol', 'monitor', 10, '', 'Check serum potassium in acute severe asthma; check blood glucose in diabetes.', 'Label · UK SmPC'),
    ('med_budesonide_formoterol', 'monitor', 11, '', 'Check adrenal function when switching from oral steroids; watch for pneumonia in COPD.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_budesonide_formoterol');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_budesonide_formoterol', 'Label · UK SmPC', 'UK SmPC (emc)', 'Symbicort Turbohaler 200/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd; March 2023.', 'https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1327', 0),
    ('med_budesonide_formoterol', 'Label · UK SmPC 100/6', 'UK SmPC (emc)', 'Symbicort Turbohaler 100/6 Inhalation powder. Summary of Product Characteristics. AstraZeneca UK Ltd.', 'https://products.mhra.gov.uk/search/?search=budesonide+formoterol#emc-1326', 1),
    ('med_budesonide_formoterol', 'Label · US', 'DailyMed (FDA label)', 'SYMBICORT (budesonide and formoterol fumarate dihydrate) inhalation aerosol. Prescribing information. AstraZeneca; revised 10/2024.', 'https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6b78d08a-e098-4188-8f7f-94fbd5f396ef', 2),
    ('med_budesonide_formoterol', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_budesonide_formoterol')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_budesonide_formoterol');


-- ================================================ med_ceftriaxone  (Ceftriaxone)
update public.medicines set description = 'Ceftriaxone is a parenteral third-generation cephalosporin that binds penicillin-binding proteins and disrupts peptidoglycan cross-linking, producing bactericidal activity. Its long half-life permits once-daily dosing, and it is widely used for pneumonia, meningitis, pyelonephritis, typhoid fever, gonorrhea and sepsis. In the Philippines, the PhilHealth CAP policy (based on the 2016 PSMID guideline) lists ceftriaxone 2 g IV once daily, combined with a macrolide or a respiratory fluoroquinolone, for moderate-risk CAP and for high-risk CAP without Pseudomonas risk. The PNF lists IM vials (reconstituted with 1% lidocaine) and IV vials.', updated_at = now()
where id = 'med_ceftriaxone' and description = 'Ceftriaxone is a parenteral third-generation cephalosporin that binds penicillin-binding proteins and disrupts peptidoglycan cross-linking, producing bactericidal activity. Its long half-life permits once-daily dosing, and it is widely used for pneumonia, meningitis, pyelonephritis, typhoid fever, gonorrhea and sepsis.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; PhilHealth Circular 2016-0003; PhilHealth / DOH (PNF-EML); Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; PhilHealth Circular 2016-0003; PhilHealth / DOH (PNF-EML); Philippine National Formulary – EML' end
where id = 'med_ceftriaxone' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Hospital-acquired pneumonia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Hospital-acquired pneumonia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Acute bacterial exacerbations of COPD', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Acute bacterial exacerbations of COPD');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Bacterial endocarditis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Bacterial endocarditis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Febrile neutropenia with suspected bacterial infection', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Febrile neutropenia with suspected bacterial infection');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Acute otitis media (single IM dose)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Acute otitis media (single IM dose)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Syphilis, including neurosyphilis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Syphilis, including neurosyphilis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Lyme borreliosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Lyme borreliosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Shigellosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Shigellosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Chancroid', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Chancroid');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Gonococcal conjunctivitis (adults and neonates)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Gonococcal conjunctivitis (adults and neonates)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'indication', 'Tick-borne relapsing fever', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'indication' and content = 'Tick-borne relapsing fever');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'adverse', 'Eosinophilia, leucopenia, thrombocytopenia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse' and content = 'Eosinophilia, leucopenia, thrombocytopenia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'adverse', 'Raised liver enzymes and rash', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse' and content = 'Raised liver enzymes and rash');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'adverse', 'Encephalopathy (mainly elderly with severe renal impairment or CNS disorders)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse' and content = 'Encephalopathy (mainly elderly with severe renal impairment or CNS disorders)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'adverse', 'Convulsions', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse' and content = 'Convulsions');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'adverse', 'Severe skin reactions: SJS/TEN, DRESS, AGEP', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse' and content = 'Severe skin reactions: SJS/TEN, DRESS, AGEP');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'adverse', 'Renal precipitation with oliguria', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse' and content = 'Renal precipitation with oliguria');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'adverse', 'Kernicterus in neonates', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse' and content = 'Kernicterus in neonates');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'adverse', 'Jarisch-Herxheimer reaction in spirochaete infections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'adverse' and content = 'Jarisch-Herxheimer reaction in spirochaete infections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'contraindication', 'Severe hypersensitivity (e.g., anaphylaxis) to any other beta-lactam', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'contraindication' and content = 'Severe hypersensitivity (e.g., anaphylaxis) to any other beta-lactam');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'contraindication', 'Full-term neonates (≤28 days) with hypoalbuminaemia or acidosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'contraindication' and content = 'Full-term neonates (≤28 days) with hypoalbuminaemia or acidosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'interaction', 'Chloramphenicol: antagonism seen in vitro.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'interaction' and content = 'Chloramphenicol: antagonism seen in vitro.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'interaction', 'Vancomycin, fluconazole and amsacrine: physically incompatible; do not mix.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'interaction' and content = 'Vancomycin, fluconazole and amsacrine: physically incompatible; do not mix.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ceftriaxone', 'interaction', 'Lab tests: false-positive Coombs test, galactosaemia tests and non-enzymatic urine glucose; may falsely lower some glucose-meter readings.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ceftriaxone' and kind = 'interaction' and content = 'Lab tests: false-positive Coombs test, galactosaemia tests and non-enzymatic urine glucose; may falsely lower some glucose-meter readings.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ceftriaxone', 'UK SmPC (emc)', 'Ceftriaxone 2 g Powder for Solution for Injection or Infusion. Summary of Product Characteristics. Wockhardt UK Ltd; updated January 2025. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=ceftriaxone#emc-1362', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ceftriaxone'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ceftriaxone' and url = 'https://products.mhra.gov.uk/search/?search=ceftriaxone#emc-1362');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ceftriaxone', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Ceftriaxone injectable. MSF Medical Guidelines; updated September 2023.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ceftriaxone-injectable-16682532.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ceftriaxone'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ceftriaxone' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ceftriaxone-injectable-16682532.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ceftriaxone', 'PhilHealth Circular 2016-0003', 'Philippine Health Insurance Corporation. Circular No. 2016-0003: Diagnosis, empiric management and prevention of community-acquired pneumonia in immunocompetent adults (based on the 2016 Philippine CPG on CAP). PhilHealth; 2016.', 'https://www.philhealth.gov.ph/circulars/2016/circ2016-003.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ceftriaxone'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ceftriaxone' and url = 'https://www.philhealth.gov.ph/circulars/2016/circ2016-003.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ceftriaxone', 'PhilHealth / DOH (PNF-EML)', 'Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ceftriaxone'), 0)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ceftriaxone' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_ceftriaxone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Limit to 2 g/day when CrCl <10 mL/min; not removed by dialysis (UK SmPC).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_ceftriaxone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'copd', 'med_ceftriaxone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'copd'), 0), 'safe'::condition_safety, 'Licensed for acute bacterial exacerbations of COPD (UK SmPC).'
where exists (select 1 from public.diseases where id = 'copd')
  and exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'copd' and medicine_id = 'med_ceftriaxone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_gastroenteritis', 'med_ceftriaxone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis'), 0), 'safe'::condition_safety, 'Used for shigellosis (bacillary dysentery) only, not for routine watery gastroenteritis (MSF).'
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis' and medicine_id = 'med_ceftriaxone');
-- med_ceftriaxone
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_ceftriaxone', 'adult', 0, 'CAP, cUTI/pyelonephritis, intra-abdominal infection', 'IV', '1–2 g', 'Once a day', 'Until 48–72 h afebrile', '—', 'Label · UK SmPC', 'IV or IM; Adults and children ≥50 kg'),
    ('med_ceftriaxone', 'adult', 1, 'CAP, moderate or high risk (PH)', 'IV', '2 g', 'Once a day', '—', '—', 'PhilHealth CAP 2016', 'With a macrolide or respiratory fluoroquinolone'),
    ('med_ceftriaxone', 'adult', 2, 'HAP, skin/soft tissue, bone and joint infection', 'IV', '2 g', 'Once a day', '—', '—', 'Label · UK SmPC', 'IV or IM'),
    ('med_ceftriaxone', 'adult', 3, 'Meningitis, endocarditis, neutropenic fever', 'IV', '2–4 g', 'Once a day', '—', '4 g/day', 'Label · UK SmPC', 'Doses >2 g/day may be split 2× a day'),
    ('med_ceftriaxone', 'adult', 4, 'Typhoid fever, meningitis', 'IV', '2 g 2× a day or 4 g once', 'Every 12 h or once a day', 'Switch to oral when possible', '4 g/day', 'MSF 2023', ''),
    ('med_ceftriaxone', 'adult', 5, 'Uncomplicated gonorrhoea', 'IM', '500 mg', 'Single dose', '1 day', '—', 'Label · UK SmPC', 'Plus chlamydia treatment (MSF)'),
    ('med_ceftriaxone', 'adult', 6, 'Gonococcal conjunctivitis', 'IM', '1 g', 'Single dose', '1 day', '—', 'MSF 2023', ''),
    ('med_ceftriaxone', 'adult', 7, 'Chancroid', 'IM', '250 mg', 'Single dose', '1 day', '—', 'MSF 2023', ''),
    ('med_ceftriaxone', 'adult', 8, 'Acute otitis media', 'IM', '1–2 g', 'Single dose', '1 day', '—', 'Label · UK SmPC', ''),
    ('med_ceftriaxone', 'adult', 9, 'Syphilis', 'IV', '500 mg–1 g', 'Once a day', '10–14 days', '2 g/day (neurosyphilis)', 'Label · UK SmPC', 'IV or IM'),
    ('med_ceftriaxone', 'adult', 10, 'Lyme borreliosis', 'IV', '2 g', 'Once a day', '14–21 days', '—', 'Label · UK SmPC', 'IV or IM'),
    ('med_ceftriaxone', 'adult', 11, 'Surgical prophylaxis', 'IV', '2 g', 'Single dose', '1 day', '—', 'Label · UK SmPC', 'Give 30–90 min before surgery'),
    ('med_ceftriaxone', 'child', 12, 'CAP, HAP, cUTI, intra-abdominal (15 d–12 y, <50 kg)', 'IV', '50–80 mg/kg', 'Once a day', 'Until 48–72 h afebrile', '—', 'Label · UK SmPC', 'IV or IM; ≥50 kg: adult dose'),
    ('med_ceftriaxone', 'child', 13, 'Skin/soft tissue, bone/joint, neutropenic fever', 'IV', '50–100 mg/kg', 'Once a day', '—', '4 g/day', 'Label · UK SmPC', 'IV or IM'),
    ('med_ceftriaxone', 'child', 14, 'Bacterial meningitis', 'IV', '80–100 mg/kg', 'Once a day', '—', '4 g/day', 'Label · UK SmPC', ''),
    ('med_ceftriaxone', 'child', 15, 'Bacterial endocarditis', 'IV', '100 mg/kg', 'Once a day', '—', '4 g/day', 'Label · UK SmPC', ''),
    ('med_ceftriaxone', 'child', 16, 'Severe bacterial infections (≥1 mo, <50 kg)', 'IV', '50–100 mg/kg', 'Once a day', 'Switch to oral when possible', '4 g/day', 'MSF 2023', 'IV or IM'),
    ('med_ceftriaxone', 'child', 17, 'Acute otitis media', 'IM', '50 mg/kg', 'Single dose', '1 day', '—', 'Label · UK SmPC', ''),
    ('med_ceftriaxone', 'child', 18, 'Gonorrhoea, chancroid (<45 kg)', 'IM', '125 mg', 'Single dose', '1 day', '—', 'MSF 2023', ''),
    ('med_ceftriaxone', 'child', 19, 'Syphilis', 'IV', '75–100 mg/kg', 'Once a day', '10–14 days', '4 g/day', 'Label · UK SmPC', 'IV or IM'),
    ('med_ceftriaxone', 'child', 20, 'Lyme borreliosis', 'IV', '50–80 mg/kg', 'Once a day', '14–21 days', '—', 'Label · UK SmPC', 'IV or IM'),
    ('med_ceftriaxone', 'child', 21, 'Surgical prophylaxis', 'IV', '50–80 mg/kg', 'Single dose', '1 day', '—', 'Label · UK SmPC', ''),
    ('med_ceftriaxone', 'neonate', 22, 'Most infections (0–14 days)', 'IV', '20–50 mg/kg', 'Once a day', '—', '50 mg/kg/day', 'Label · UK SmPC', 'IV or IM; Contraindicated if premature (<41 wk PMA); IV over 60 min'),
    ('med_ceftriaxone', 'neonate', 23, 'Meningitis, endocarditis (0–14 days)', 'IV', '50 mg/kg', 'Once a day', '—', '50 mg/kg/day', 'Label · UK SmPC', ''),
    ('med_ceftriaxone', 'neonate', 24, 'Gonococcal conjunctivitis', 'IM', '50 mg/kg', 'Single dose', '1 day', '125 mg', 'MSF 2023', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_ceftriaxone');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_ceftriaxone', 'renal', 0, 'CrCl ≥10', 'No reduction needed if liver function is normal.', 'Label · UK SmPC'),
    ('med_ceftriaxone', 'renal', 1, 'CrCl <10', 'Do not exceed 2 g/day. Not removed by haemodialysis or peritoneal dialysis; no extra dose after dialysis.', 'Label · UK SmPC'),
    ('med_ceftriaxone', 'hepatic', 2, '', 'No adjustment in mild–moderate impairment; no data in severe impairment. Monitor closely if severe renal and hepatic impairment coexist.', 'Label · UK SmPC'),
    ('med_ceftriaxone', 'elderly', 3, '', 'No adjustment if renal and hepatic function are satisfactory; encephalopathy risk higher with severe renal impairment.', 'Label · UK SmPC'),
    ('med_ceftriaxone', 'pregnancy', 4, '', 'Crosses the placenta; use only if benefit outweighs risk, especially in the first trimester. Low levels in breast milk; watch the infant for diarrhoea or thrush.', 'Label · UK SmPC'),
    ('med_ceftriaxone', 'administration', 5, '', 'IV: infuse over ≥30 min (preferred) or slow injection over 5 min; neonates over 60 min; children ≥50 mg/kg by infusion; doses >2 g IV only.', 'Label · UK SmPC'),
    ('med_ceftriaxone', 'administration', 6, '', 'IM: reconstitute with 1% lidocaine, deep IM into a large muscle, max 1 g per site; never give the lidocaine solution IV.', 'Label · UK SmPC'),
    ('med_ceftriaxone', 'administration', 7, '', 'IV dilution volume: 5 mL/kg for children <20 kg; 100 mL bag for children ≥20 kg and adults. Use immediately after reconstitution.', 'MSF 2023'),
    ('med_ceftriaxone', 'forms_ph', 8, '', 'Powder for injection: 250 mg and 500 mg vial + 2 mL 1% lidocaine (IM); 1 g vial + 3.5 mL 1% lidocaine (IM); 250 mg vial + 5 mL diluent (IV); 1 g vial + 10 mL diluent (IV).', 'PNF'),
    ('med_ceftriaxone', 'monitor', 9, '', 'Check complete blood count during prolonged treatment; stop if haemolytic anaemia is suspected.', 'Label · UK SmPC'),
    ('med_ceftriaxone', 'monitor', 10, '', 'Watch for right upper quadrant pain (biliary sludge/pancreatitis), especially at ≥1 g/day or with TPN.', 'Label · UK SmPC'),
    ('med_ceftriaxone', 'monitor', 11, '', 'Check INR in patients on oral anticoagulants; test for C. difficile if diarrhoea develops.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_ceftriaxone');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_ceftriaxone', 'Label · UK SmPC', 'UK SmPC (emc)', 'Ceftriaxone 2 g Powder for Solution for Injection or Infusion. Summary of Product Characteristics. Wockhardt UK Ltd; January 2025.', 'https://products.mhra.gov.uk/search/?search=ceftriaxone#emc-1362', 0),
    ('med_ceftriaxone', 'MSF 2023', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Ceftriaxone injectable. Updated September 2023.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ceftriaxone-injectable-16682532.html', 1),
    ('med_ceftriaxone', 'PhilHealth CAP 2016', 'PhilHealth Circular 2016-0003', 'PhilHealth Circular 2016-0003: CAP in immunocompetent adults (2016 Philippine CPG). PhilHealth; 2016.', 'https://www.philhealth.gov.ph/circulars/2016/circ2016-003.pdf', 2),
    ('med_ceftriaxone', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_ceftriaxone')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_ceftriaxone');


-- ================================================ med_cetirizine  (Cetirizine)
update public.medicines set description = 'Cetirizine, derived from hydroxyzine, is a fast-acting, highly selective peripheral histamine H1-receptor antagonist. It crosses the blood-brain barrier only minimally, so it causes less sedation than first-generation antihistamines, and it also reduces neutrophil and eosinophil infiltration. It is used for seasonal and perennial allergic rhinitis and chronic urticaria. In the Philippines it is listed in the PNF as a 10 mg tablet and as several liquid forms (syrup, oral drops and solution) for children. UK labeling doses children aged 2–12 years twice daily, and bases renal dose reduction on eGFR, with use contraindicated below 15 mL/min.', updated_at = now()
where id = 'med_cetirizine' and description = 'Cetirizine, derived from hydroxyzine, is a fast-acting, highly selective peripheral histamine H1-receptor antagonist. It crosses the blood-brain barrier only minimally, so it causes less sedation than first-generation antihistamines, and it also reduces neutrophil and eosinophil infiltration. It is used for seasonal and perennial allergic rhinitis and chronic urticaria.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); PhilHealth / DOH (PNF-EML); Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); PhilHealth / DOH (PNF-EML); Philippine National Formulary – EML' end
where id = 'med_cetirizine' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Diarrhoea, rhinitis and fatigue in children', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Diarrhoea, rhinitis and fatigue in children');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Agitation, paraesthesia, pruritus, rash, asthenia (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Agitation, paraesthesia, pruritus, rash, asthenia (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Aggression, confusion, depression, hallucinations, insomnia (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Aggression, confusion, depression, hallucinations, insomnia (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Convulsions and tachycardia (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Convulsions and tachycardia (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Abnormal liver function tests (rare); hepatitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Abnormal liver function tests (rare); hepatitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Urinary retention', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Urinary retention');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Weight increase and increased appetite', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Weight increase and increased appetite');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Angioedema, fixed drug eruption, AGEP (very rare to not known)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Angioedema, fixed drug eruption, AGEP (very rare to not known)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Tics, dystonia, oculogyric crisis, blurred vision (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Tics, dystonia, oculogyric crisis, blurred vision (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'adverse', 'Pruritus and/or urticaria after stopping treatment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'adverse' and content = 'Pruritus and/or urticaria after stopping treatment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'contraindication', 'Hypersensitivity to any piperazine derivative', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'contraindication' and content = 'Hypersensitivity to any piperazine derivative');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'contraindication', 'End-stage renal disease (eGFR <15 mL/min)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'contraindication' and content = 'End-stage renal disease (eGFR <15 mL/min)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'interaction', 'Pseudoephedrine and theophylline (400 mg/day): no clinically significant interaction found.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'interaction' and content = 'Pseudoephedrine and theophylline (400 mg/day): no clinically significant interaction found.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cetirizine', 'interaction', 'Food: slows the rate but not the extent of absorption.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cetirizine' and kind = 'interaction' and content = 'Food: slows the rate but not the extent of absorption.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_cetirizine', 'UK SmPC (emc)', 'Cetirizine hydrochloride 10 mg film-coated tablets. Summary of Product Characteristics. Milpharm Ltd (Aurobindo); updated February 2024. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=cetirizine#emc-12956', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_cetirizine'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_cetirizine' and url = 'https://products.mhra.gov.uk/search/?search=cetirizine#emc-12956');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_cetirizine', 'UK SmPC (emc)', 'Zirtek Allergy Solution 1 mg/ml oral solution. Summary of Product Characteristics. UCB Pharma Ltd; updated October 2023. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=cetirizine#emc-6752', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_cetirizine'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_cetirizine' and url = 'https://products.mhra.gov.uk/search/?search=cetirizine#emc-6752');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_cetirizine', 'PhilHealth / DOH (PNF-EML)', 'Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_cetirizine'), 0)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_cetirizine' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_cetirizine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Reduce dose by eGFR; contraindicated below 15 mL/min (UK SmPC).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_cetirizine');
-- med_cetirizine
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_cetirizine', 'adult', 0, 'Allergic rhinitis, chronic urticaria', 'PO', '10 mg', 'Once a day', '—', '—', 'Label · UK SmPC', 'Also adolescents >12 y'),
    ('med_cetirizine', 'child', 1, 'Allergic rhinitis, urticaria (6–12 y)', 'PO', '5 mg', '2× a day', '—', '—', 'Label · UK SmPC', '½ tablet or 5 mL of 1 mg/mL solution'),
    ('med_cetirizine', 'child', 2, 'Allergic rhinitis, urticaria (2–6 y)', 'PO', '2.5 mg', '2× a day', '—', '—', 'Label · UK SmPC sol', '2.5 mL of 1 mg/mL solution; tablets not suitable <6 y')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_cetirizine');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_cetirizine', 'renal', 0, 'eGFR ≥60', '10 mg once a day (no change).', 'Label · UK SmPC'),
    ('med_cetirizine', 'renal', 1, 'eGFR 30–59', '5 mg once a day.', 'Label · UK SmPC'),
    ('med_cetirizine', 'renal', 2, 'eGFR 15–29', '5 mg once every 2 days.', 'Label · UK SmPC'),
    ('med_cetirizine', 'renal', 3, 'eGFR <15', 'Contraindicated.', 'Label · UK SmPC'),
    ('med_cetirizine', 'hepatic', 4, '', 'No adjustment for hepatic impairment alone; adjust if renal impairment is also present.', 'Label · UK SmPC'),
    ('med_cetirizine', 'elderly', 5, '', 'No dose reduction if renal function is normal.', 'Label · UK SmPC'),
    ('med_cetirizine', 'pregnancy', 6, '', 'Prospective data show no excess maternal or fetal toxicity, but prescribe with caution. Passes into breast milk (25–90% of plasma levels); use with caution.', 'Label · UK SmPC'),
    ('med_cetirizine', 'administration', 7, '', 'Stop at least 3 days before allergy skin testing (antihistamines suppress results).', 'Label · UK SmPC'),
    ('med_cetirizine', 'forms_ph', 8, '', 'Tablet 10 mg; syrup (oral drops) 2.5 mg/mL, 10 mL; drops 10 mg/mL, 10 mL; solution 1 mg/mL, 30 mL and 60 mL; syrup 5 mg/5 mL, 30 mL.', 'PNF'),
    ('med_cetirizine', 'monitor', 9, '', 'Ask about urinary retention in men with prostatic hyperplasia or spinal cord lesions; use caution in epilepsy.', 'Label · UK SmPC'),
    ('med_cetirizine', 'monitor', 10, '', 'Advise against driving if drowsy; warn that itching or hives may flare on stopping.', 'Label · UK SmPC'),
    ('med_cetirizine', 'monitor', 11, '', 'Overdose (≥5× daily dose): sedation, confusion, mydriasis, tachycardia, urinary retention; supportive care only, not removed by haemodialysis.', 'Label · UK SmPC sol')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_cetirizine');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_cetirizine', 'Label · UK SmPC', 'UK SmPC (emc)', 'Cetirizine hydrochloride 10 mg film-coated tablets. Summary of Product Characteristics. Milpharm Ltd; February 2024.', 'https://products.mhra.gov.uk/search/?search=cetirizine#emc-12956', 0),
    ('med_cetirizine', 'Label · UK SmPC sol', 'UK SmPC (emc)', 'Zirtek Allergy Solution 1 mg/ml oral solution. Summary of Product Characteristics. UCB Pharma Ltd; October 2023.', 'https://products.mhra.gov.uk/search/?search=cetirizine#emc-6752', 1),
    ('med_cetirizine', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_cetirizine')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_cetirizine');


-- ================================================ med_ciprofloxacin  (Ciprofloxacin)
update public.medicines set description = 'Ciprofloxacin is a bactericidal fluoroquinolone that inhibits bacterial DNA gyrase and topoisomerase IV, blocking DNA replication. It is especially active against Gram-negative organisms including Pseudomonas aeruginosa, but because of serious class toxicities it is reserved for infections where benefits outweigh risks. Oral bioavailability is about 70–80%, so 500 mg orally every 12 hours gives roughly the same exposure (AUC) as 400 mg IV every 12 hours; this makes early IV-to-oral switching possible. The half-life is about 4–7 hours, rising to about 12 hours in severe renal impairment, and the drug is cleared by both the kidneys and the gut. In the Philippines it is on the PNF Essential Medicines List as tablets and IV infusion. National surveillance (ARSP 2014–2018) found 8.7% of invasive non-typhoidal Salmonella isolates resistant to ciprofloxacin, and MSF notes that fluoroquinolone resistance in typhoid is endemic in Asia.', updated_at = now()
where id = 'med_ciprofloxacin' and description = 'Ciprofloxacin is a bactericidal fluoroquinolone that inhibits bacterial DNA gyrase and topoisomerase IV, blocking DNA replication. It is especially active against Gram-negative organisms including Pseudomonas aeruginosa, but because of serious class toxicities it is reserved for infections where benefits outweigh risks.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); Pfizer labeling (US); MSF Essential Drugs; Philippine National Formulary (PNF EML); Western Pacific Surveillance and Response; Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); Pfizer labeling (US); MSF Essential Drugs; Philippine National Formulary (PNF EML); Western Pacific Surveillance and Response; Philippine National Formulary – EML' end
where id = 'med_ciprofloxacin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'indication', 'Chronic suppurative otitis media and malignant external otitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication' and content = 'Chronic suppurative otitis media and malignant external otitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'indication', 'Gonococcal urethritis and cervicitis (only if the strain is known to be susceptible)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication' and content = 'Gonococcal urethritis and cervicitis (only if the strain is known to be susceptible)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'indication', 'Epididymo-orchitis and pelvic inflammatory disease (with a second agent)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication' and content = 'Epididymo-orchitis and pelvic inflammatory disease (with a second agent)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'indication', 'Gram-negative intra-abdominal infections and skin/soft tissue infections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication' and content = 'Gram-negative intra-abdominal infections and skin/soft tissue infections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'indication', 'Suspected bacterial infection in neutropenic fever (with other antibacterials)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication' and content = 'Suspected bacterial infection in neutropenic fever (with other antibacterials)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'indication', 'Prophylaxis of invasive meningococcal infection (single dose)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication' and content = 'Prophylaxis of invasive meningococcal infection (single dose)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'indication', 'Shigellosis and cholera diarrhoea', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication' and content = 'Shigellosis and cholera diarrhoea');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'indication', 'Children: Pseudomonas lung infection in cystic fibrosis; complicated UTI and pyelonephritis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'indication' and content = 'Children: Pseudomonas lung infection in cystic fibrosis; complicated UTI and pyelonephritis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'adverse', 'Headache, dizziness, sleep disorders and taste disturbance (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse' and content = 'Headache, dizziness, sleep disorders and taste disturbance (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'adverse', 'Arthralgia and musculoskeletal pain; eosinophilia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse' and content = 'Arthralgia and musculoskeletal pain; eosinophilia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'adverse', 'Tinnitus, hearing loss and vision disorders (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse' and content = 'Tinnitus, hearing loss and vision disorders (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'adverse', 'Crystalluria, interstitial nephritis and renal failure (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse' and content = 'Crystalluria, interstitial nephritis and renal failure (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'adverse', 'Haemolytic anaemia in G6PD deficiency', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse' and content = 'Haemolytic anaemia in G6PD deficiency');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'adverse', 'Stevens–Johnson syndrome, toxic epidermal necrolysis and pancreatitis (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse' and content = 'Stevens–Johnson syndrome, toxic epidermal necrolysis and pancreatitis (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'adverse', 'Fungal superinfection', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'adverse' and content = 'Fungal superinfection');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'contraindication', 'Previous serious adverse reaction to any quinolone: avoid (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication' and content = 'Previous serious adverse reaction to any quinolone: avoid (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'contraindication', 'Children and adolescents: joint (cartilage) damage seen in young animals; use only after careful benefit/risk review (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication' and content = 'Children and adolescents: joint (cartilage) damage seen in young animals; use only after careful benefit/risk review (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'contraindication', 'G6PD deficiency: risk of haemolysis; avoid unless benefit outweighs risk (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication' and content = 'G6PD deficiency: risk of haemolysis; avoid unless benefit outweighs risk (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'contraindication', 'Pregnancy: preferably avoid; breastfeeding: not to be used per UK SmPC (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication' and content = 'Pregnancy: preferably avoid; breastfeeding: not to be used per UK SmPC (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'contraindication', 'Epilepsy, older age, hypertension or heart disease: use with caution (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'contraindication' and content = 'Epilepsy, older age, hypertension or heart disease: use with caution (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'interaction', 'Dairy products and mineral-fortified drinks taken alone: reduced absorption; avoid (calcium in a normal meal has little effect).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction' and content = 'Dairy products and mineral-fortified drinks taken alone: reduced absorption; avoid (calcium in a normal meal has little effect).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'interaction', 'Probenecid: raises ciprofloxacin levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction' and content = 'Probenecid: raises ciprofloxacin levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'interaction', 'Phenytoin: levels may rise or fall; monitor phenytoin.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction' and content = 'Phenytoin: levels may rise or fall; monitor phenytoin.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'interaction', 'Ciclosporin: transient rise in serum creatinine; check creatinine about twice a week.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction' and content = 'Ciclosporin: transient rise in serum creatinine; check creatinine about twice a week.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'interaction', 'Clozapine, ropinirole, caffeine and pentoxifylline: raised levels (CYP1A2 inhibition); monitor for side effects.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction' and content = 'Clozapine, ropinirole, caffeine and pentoxifylline: raised levels (CYP1A2 inhibition); monitor for side effects.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'interaction', 'Sildenafil: exposure roughly doubled; use with caution. Zolpidem: not recommended.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction' and content = 'Sildenafil: exposure roughly doubled; use with caution. Zolpidem: not recommended.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ciprofloxacin', 'interaction', 'QT-prolonging drugs (class IA/III antiarrhythmics, tricyclics, macrolides, antipsychotics): use with caution.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ciprofloxacin' and kind = 'interaction' and content = 'QT-prolonging drugs (class IA/III antiarrhythmics, tricyclics, macrolides, antipsychotics): use with caution.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ciprofloxacin', 'UK SmPC (emc)', 'Ciprofloxacin 500 mg film-coated tablets – Summary of Product Characteristics. Sun Pharma UK Limited (PL 14894/0023). Electronic Medicines Compendium (emc), medicines.org.uk; updated May 2026.', 'https://products.mhra.gov.uk/search/?search=ciprofloxacin#emc-4346', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin' and url = 'https://products.mhra.gov.uk/search/?search=ciprofloxacin#emc-4346');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ciprofloxacin', 'Pfizer labeling (US)', 'Ciprofloxacin in Dextrose (Ciprofloxacin Injection, USP, in 5% Dextrose Injection). Prescribing information. Hospira, Inc.; revised 11/2022.', 'https://labeling.pfizer.com/ShowLabeling.aspx?id=18958', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin' and url = 'https://labeling.pfizer.com/ShowLabeling.aspx?id=18958');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ciprofloxacin', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Ciprofloxacin oral. Last updated September 2023.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ciprofloxacin-oral-16683360.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ciprofloxacin-oral-16683360.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ciprofloxacin', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ciprofloxacin', 'Western Pacific Surveillance and Response', 'Sia SB, Ablola FB, Lagrada ML, et al. Epidemiology and antimicrobial resistance profile of invasive non-typhoidal Salmonella from the Philippines Antimicrobial Resistance Surveillance Program, 2014–2018. Western Pac Surveill Response J. 2023;14(3). doi:10.5365/wpsar.2023.14.3.1030', 'https://ojs.wpro.who.int/ojs/index.php/wpsar/article/view/1030', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin'), 0)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ciprofloxacin' and url = 'https://ojs.wpro.who.int/ojs/index.php/wpsar/article/view/1030');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_ciprofloxacin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Dose reduction needed when CrCl is 60 mL/min or below; half-life up to about 12 h in severe renal impairment; keep well hydrated (crystalluria)'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_ciprofloxacin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_ciprofloxacin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Hypo- and hyperglycaemia reported; MSF advises monitoring with glibenclamide (hypoglycaemia risk)'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_ciprofloxacin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hypertension', 'med_ciprofloxacin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hypertension'), 0), 'caution'::condition_safety, 'MSF lists hypertension and heart disorders as a precaution (QT risk)'
where exists (select 1 from public.diseases where id = 'hypertension')
  and exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hypertension' and medicine_id = 'med_ciprofloxacin');
-- med_ciprofloxacin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_ciprofloxacin', 'adult', 0, 'Uncomplicated cystitis', 'PO', '250–500 mg', '2× a day', '3 days', '—', 'Label · UK SmPC', 'Pre-menopausal women: a single 500 mg dose may be used'),
    ('med_ciprofloxacin', 'adult', 1, 'Complicated cystitis, uncomplicated pyelonephritis', 'PO', '500 mg', '2× a day', '7 days', '—', 'Label · UK SmPC', ''),
    ('med_ciprofloxacin', 'adult', 2, 'Complicated pyelonephritis', 'PO', '500–750 mg', '2× a day', '≥10 days', '750 mg/dose', 'Label · UK SmPC', 'May exceed 21 days (e.g. abscesses)'),
    ('med_ciprofloxacin', 'adult', 3, 'Prostatitis', 'PO', '500–750 mg', '2× a day', '2–4 weeks (acute); 4–6 weeks (chronic)', '750 mg/dose', 'Label · UK SmPC', ''),
    ('med_ciprofloxacin', 'adult', 4, 'Lower respiratory tract infection', 'PO', '500–750 mg', '2× a day', '7–14 days', '750 mg/dose', 'Label · UK SmPC', 'Not for pneumococcal infection'),
    ('med_ciprofloxacin', 'adult', 5, 'Typhoid fever', 'PO', '500 mg', '2× a day', '7 days', '—', 'Label · UK SmPC', 'Check local resistance'),
    ('med_ciprofloxacin', 'adult', 6, 'Cholera', 'PO', '500 mg', '2× a day', '3 days', '—', 'Label · UK SmPC', ''),
    ('med_ciprofloxacin', 'adult', 7, 'Shigellosis (non-S. dysenteriae type 1)', 'PO', '500 mg', '2× a day', '1 day', '—', 'Label · UK SmPC', 'S. dysenteriae type 1: 5 days; MSF uses 3 days'),
    ('med_ciprofloxacin', 'adult', 8, 'Gonococcal urethritis/cervicitis', 'PO', '500 mg', 'Single dose', '1 day', '—', 'Label · UK SmPC', 'Only if strain susceptible'),
    ('med_ciprofloxacin', 'adult', 9, 'Meningococcal prophylaxis', 'PO', '500 mg', 'Single dose', '1 day', '—', 'Label · UK SmPC', ''),
    ('med_ciprofloxacin', 'adult', 10, 'Bone and joint infection', 'PO', '500–750 mg', '2× a day', 'Up to 3 months', '750 mg/dose', 'Label · UK SmPC', 'Combine per microbiology'),
    ('med_ciprofloxacin', 'adult', 11, 'Inhalational anthrax', 'PO', '500 mg', '2× a day', '60 days', '—', 'Label · UK SmPC', 'Start as soon as possible after exposure'),
    ('med_ciprofloxacin', 'adult', 12, 'Severe infections (skin, bone, LRTI, UTI)', 'IV', '400 mg', 'Every 8–12 h', '7–14 days', '—', 'Label · US IV', 'UTI: 200–400 mg; switch to PO when able'),
    ('med_ciprofloxacin', 'adult', 13, 'Nosocomial pneumonia', 'IV', '400 mg', 'Every 8 h', '10–14 days', '—', 'Label · US IV', ''),
    ('med_ciprofloxacin', 'adult', 14, 'Complicated intra-abdominal infection', 'IV', '400 mg', 'Every 12 h', '7–14 days', '—', 'Label · US IV', 'With metronidazole'),
    ('med_ciprofloxacin', 'adult', 15, 'Febrile neutropenia', 'IV', '400 mg', 'Every 8 h', '7–14 days', '—', 'Label · US IV', 'With piperacillin'),
    ('med_ciprofloxacin', 'child', 16, 'Shigellosis (≥1 month)', 'PO', '15 mg/kg', '2× a day', '3 days', '500 mg/dose', 'MSF 2023', ''),
    ('med_ciprofloxacin', 'child', 17, 'Complicated UTI, pyelonephritis', 'PO', '10–20 mg/kg', '2× a day', '10–21 days', '750 mg/dose', 'Label · UK SmPC', ''),
    ('med_ciprofloxacin', 'child', 18, 'Cystic fibrosis (Pseudomonas)', 'PO', '20 mg/kg', '2× a day', '10–14 days', '750 mg/dose', 'Label · UK SmPC', ''),
    ('med_ciprofloxacin', 'child', 19, 'Inhalational anthrax', 'PO', '10–15 mg/kg', '2× a day', '60 days', '500 mg/dose', 'Label · UK SmPC', ''),
    ('med_ciprofloxacin', 'child', 20, 'Complicated UTI, pyelonephritis (1–17 y)', 'IV', '6–10 mg/kg', 'Every 8 h', '10–21 days', '400 mg/dose', 'Label · US IV', ''),
    ('med_ciprofloxacin', 'child', 21, 'Inhalational anthrax', 'IV', '10 mg/kg', 'Every 12 h', '60 days', '400 mg/dose', 'Label · US IV', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_ciprofloxacin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_ciprofloxacin', 'renal', 0, 'CrCl >60', 'Usual dose.', 'Label · UK SmPC'),
    ('med_ciprofloxacin', 'renal', 1, 'CrCl 30–60', '250–500 mg PO every 12 h.', 'Label · UK SmPC'),
    ('med_ciprofloxacin', 'renal', 2, 'CrCl ≤30', '250–500 mg PO every 24 h (haemodialysis: give after dialysis).', 'Label · UK SmPC'),
    ('med_ciprofloxacin', 'renal', 3, 'CrCl 5–29', 'IV: 200–400 mg every 18–24 h.', 'Label · US IV'),
    ('med_ciprofloxacin', 'hepatic', 4, '', 'No dose adjustment needed; stop if signs of liver disease appear (hepatic necrosis reported).', 'Label · UK SmPC'),
    ('med_ciprofloxacin', 'elderly', 5, '', 'Choose dose by infection severity and creatinine clearance.', 'Label · UK SmPC'),
    ('med_ciprofloxacin', 'pregnancy', 6, '', 'Preferably avoid in pregnancy (possible cartilage effects). Excreted in breast milk: UK SmPC says not to use while breastfeeding; MSF lists no contraindication.', 'Label · UK SmPC'),
    ('med_ciprofloxacin', 'administration', 7, '', 'Swallow tablets whole with fluid, with or without meals; avoid taking with dairy or mineral-fortified juice alone.', 'Label · UK SmPC'),
    ('med_ciprofloxacin', 'administration', 8, '', 'IV: ready to use; infuse over 60 minutes. Switch to oral as soon as possible.', 'Label · US IV'),
    ('med_ciprofloxacin', 'administration', 9, '', 'Keep fluid intake high to reduce crystalluria risk.', 'MSF 2023'),
    ('med_ciprofloxacin', 'forms_ph', 10, '', 'Tablet 250 mg, 500 mg (as hydrochloride); IV infusion 2 mg/mL, 100 mL vial (as lactate); 400 mg/200 mL IV infusion.', 'PNF'),
    ('med_ciprofloxacin', 'monitor', 11, '', 'Ask about tendon pain, numbness/tingling and mood changes at each visit; stop at once if they appear.', 'Label · UK SmPC'),
    ('med_ciprofloxacin', 'monitor', 12, '', 'Check INR often with warfarin, and blood glucose in diabetics.', 'Label · UK SmPC'),
    ('med_ciprofloxacin', 'monitor', 13, '', 'Check serum creatinine about twice weekly if on ciclosporin; theophylline/phenytoin levels if co-prescribed.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_ciprofloxacin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_ciprofloxacin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Ciprofloxacin 500 mg film-coated tablets. Summary of Product Characteristics. Sun Pharma UK Ltd; 2026.', 'https://products.mhra.gov.uk/search/?search=ciprofloxacin#emc-4346', 0),
    ('med_ciprofloxacin', 'Label · US IV', 'Pfizer labeling (US)', 'Ciprofloxacin in Dextrose injection. Prescribing information. Hospira, Inc.; 11/2022.', 'https://labeling.pfizer.com/ShowLabeling.aspx?id=18958', 1),
    ('med_ciprofloxacin', 'MSF 2023', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Ciprofloxacin oral. Updated September 2023.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ciprofloxacin-oral-16683360.html', 2),
    ('med_ciprofloxacin', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_ciprofloxacin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_ciprofloxacin');


-- ================================================ med_clarithromycin  (Clarithromycin)
update public.medicines set description = 'Clarithromycin binds the 50S ribosomal subunit and inhibits bacterial protein synthesis. It covers respiratory and atypical pathogens and is a key component of H. pylori triple therapy, but it is a strong CYP3A4 inhibitor with many clinically important drug interactions. Clarithromycin is converted on first pass to 14-hydroxyclarithromycin, an active metabolite that is about twice as active as the parent drug against Haemophilus influenzae. Its kinetics are non-linear: the half-life is 2–4 hours at 250 mg twice daily and about 5 hours at 500 mg twice daily, and steady state is reached within 2 days. In the Philippines it is on the PNF Essential Medicines List as 250 mg and 500 mg tablets and as a 125 mg/5 mL or 250 mg/5 mL oral suspension.', updated_at = now()
where id = 'med_clarithromycin' and description = 'Clarithromycin binds the 50S ribosomal subunit and inhibits bacterial protein synthesis. It covers respiratory and atypical pathogens and is a key component of H. pylori triple therapy, but it is a strong CYP3A4 inhibitor with many clinically important drug interactions.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); CDC (MMWR); Philippine National Formulary (PNF EML); DailyMed (FDA label); Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); CDC (MMWR); Philippine National Formulary (PNF EML); DailyMed (FDA label); Philippine National Formulary – EML' end
where id = 'med_clarithromycin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'indication', 'Pertussis: treatment and post-exposure prophylaxis (age 1 month and over)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'indication' and content = 'Pertussis: treatment and post-exposure prophylaxis (age 1 month and over)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'indication', 'Prophylaxis of disseminated Mycobacterium avium complex infection', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'indication' and content = 'Prophylaxis of disseminated Mycobacterium avium complex infection');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'indication', 'Respiratory and skin infections in children 6 months to 12 years (oral suspension)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'indication' and content = 'Respiratory and skin infections in children 6 months to 12 years (oral suspension)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'adverse', 'Insomnia, headache and excessive sweating (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse' and content = 'Insomnia, headache and excessive sweating (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'adverse', 'Abnormal liver function tests and rash (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse' and content = 'Abnormal liver function tests and rash (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'adverse', 'Dizziness, vertigo, tinnitus and hearing impairment (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse' and content = 'Dizziness, vertigo, tinnitus and hearing impairment (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'adverse', 'Leukopenia, neutropenia and candidiasis (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse' and content = 'Leukopenia, neutropenia and candidiasis (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'adverse', 'Severe skin reactions: SJS, TEN, DRESS, AGEP (post-marketing)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse' and content = 'Severe skin reactions: SJS, TEN, DRESS, AGEP (post-marketing)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'adverse', 'Pancreatitis, hallucinations, psychotic disorder and convulsions (post-marketing)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse' and content = 'Pancreatitis, hallucinations, psychotic disorder and convulsions (post-marketing)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'adverse', 'Renal failure and interstitial nephritis; rhabdomyolysis (post-marketing)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'adverse' and content = 'Renal failure and interstitial nephritis; rhabdomyolysis (post-marketing)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'contraindication', 'Oral midazolam', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication' and content = 'Oral midazolam');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'contraindication', 'Astemizole, terfenadine or domperidone', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication' and content = 'Astemizole, terfenadine or domperidone');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'contraindication', 'Ticagrelor, ivabradine or ranolazine', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication' and content = 'Ticagrelor, ivabradine or ranolazine');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'contraindication', 'Colchicine (any patient, per UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication' and content = 'Colchicine (any patient, per UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'contraindication', 'Low potassium or magnesium (electrolyte disturbance)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication' and content = 'Low potassium or magnesium (electrolyte disturbance)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'contraindication', 'Severe hepatic failure together with renal impairment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication' and content = 'Severe hepatic failure together with renal impairment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'contraindication', 'Pregnancy: safety not established; possible higher miscarriage risk; use only if benefit outweighs risk (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication' and content = 'Pregnancy: safety not established; possible higher miscarriage risk; use only if benefit outweighs risk (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'contraindication', 'Infants under 1 month: not recommended for pertussis; azithromycin preferred (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'contraindication' and content = 'Infants under 1 month: not recommended for pertussis; azithromycin preferred (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'Rifampicin, rifabutin, rifapentine, efavirenz, nevirapine: lower clarithromycin levels; rifabutin levels rise (uveitis risk).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'Rifampicin, rifabutin, rifapentine, efavirenz, nevirapine: lower clarithromycin levels; rifabutin levels rise (uveitis risk).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'Ritonavir or atazanavir: raise clarithromycin levels; cut dose by 50% at CrCl 30–60 and 75% at CrCl <30; max 1 g/day.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'Ritonavir or atazanavir: raise clarithromycin levels; cut dose by 50% at CrCl 30–60 and 75% at CrCl <30; max 1 g/day.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'Digoxin: raised levels with toxicity and arrhythmias; monitor digoxin levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'Digoxin: raised levels with toxicity and arrhythmias; monitor digoxin levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'IV midazolam, triazolam, alprazolam: increased sedation; monitor closely.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'IV midazolam, triazolam, alprazolam: increased sedation; monitor closely.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'Direct oral anticoagulants (dabigatran, edoxaban, rivaroxaban, apixaban): higher bleeding risk; use with caution.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'Direct oral anticoagulants (dabigatran, edoxaban, rivaroxaban, apixaban): higher bleeding risk; use with caution.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'Zidovudine: reduced absorption; separate doses by 4 hours.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'Zidovudine: reduced absorption; separate doses by 4 hours.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'Sildenafil, tadalafil, vardenafil: consider dose reduction.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'Sildenafil, tadalafil, vardenafil: consider dose reduction.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'Omeprazole: omeprazole AUC up 89%.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'Omeprazole: omeprazole AUC up 89%.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'Hydroxychloroquine or chloroquine: additive QT risk; weigh risk and benefit.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'Hydroxychloroquine or chloroquine: additive QT risk; weigh risk and benefit.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clarithromycin', 'interaction', 'Phenytoin and valproate: monitor levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clarithromycin' and kind = 'interaction' and content = 'Phenytoin and valproate: monitor levels.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_clarithromycin', 'UK SmPC (emc)', 'Clarithromycin 500 mg film-coated tablets – Summary of Product Characteristics. Milpharm Limited (PL 16363/0414). Electronic Medicines Compendium (emc), medicines.org.uk; revised July 2026.', 'https://products.mhra.gov.uk/search/?search=clarithromycin#emc-7072', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_clarithromycin'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_clarithromycin' and url = 'https://products.mhra.gov.uk/search/?search=clarithromycin#emc-7072');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_clarithromycin', 'UK SmPC (emc)', 'Clarithromycin 125 mg/5 ml suspension – Summary of Product Characteristics. Sandoz Ltd. Electronic Medicines Compendium (emc), medicines.org.uk; June 2021.', 'https://products.mhra.gov.uk/search/?search=clarithromycin#emc-515', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_clarithromycin'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_clarithromycin' and url = 'https://products.mhra.gov.uk/search/?search=clarithromycin#emc-515');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_clarithromycin', 'CDC (MMWR)', 'Centers for Disease Control and Prevention. Recommended antimicrobial agents for the treatment and postexposure prophylaxis of pertussis: 2005 CDC guidelines. MMWR Recomm Rep. 2005;54(RR-14).', 'https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5414a1.htm', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_clarithromycin'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_clarithromycin' and url = 'https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5414a1.htm');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_clarithromycin', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_clarithromycin'), 0)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_clarithromycin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_clarithromycin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'CrCl <30 mL/min: halve the dose and do not treat beyond 14 days; contraindicated with severe hepatic failure plus renal impairment'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_clarithromycin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_clarithromycin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Significant hypoglycaemia reported with oral hypoglycaemics or insulin; monitor glucose'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_clarithromycin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_clarithromycin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'caution'::condition_safety, 'Used for MAC prophylaxis/treatment, but interacts with ritonavir, atazanavir, efavirenz, nevirapine and zidovudine (dose changes or spacing needed)'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_clarithromycin');
-- med_clarithromycin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_clarithromycin', 'adult', 0, 'Respiratory and skin infections (and >12 y)', 'PO', '250 mg', '2× a day', '6–14 days', '500 mg 2× a day', 'Label · UK SmPC', 'Increase to 500 mg 2× a day if severe'),
    ('med_clarithromycin', 'adult', 1, 'Community-acquired pneumonia', 'PO', '250 mg', 'Every 12 h', '7–14 days', '—', 'Label · FDA', 'H. influenzae: 500 mg for 7 days'),
    ('med_clarithromycin', 'adult', 2, 'Acute maxillary sinusitis', 'PO', '500 mg', 'Every 12 h', '14 days', '—', 'Label · FDA', ''),
    ('med_clarithromycin', 'adult', 3, 'H. pylori (triple therapy)', 'PO', '500 mg', '2× a day', '10–14 days', '—', 'Label · FDA', 'With amoxicillin 1 g and a PPI, all 2× a day'),
    ('med_clarithromycin', 'adult', 4, 'H. pylori (UK alternative)', 'PO', '500 mg', '2× a day', '6–14 days', '—', 'Label · UK SmPC', 'With a PPI plus metronidazole 400 mg 2× a day'),
    ('med_clarithromycin', 'adult', 5, 'Disseminated MAC (treatment/prophylaxis)', 'PO', '500 mg', 'Every 12 h', 'Ongoing while response lasts', '—', 'Label · FDA', 'With other antimycobacterials (e.g. ethambutol)'),
    ('med_clarithromycin', 'adult', 6, 'Pertussis (treatment or PEP)', 'PO', '500 mg', '2× a day', '7 days', '1 g/day', 'CDC 2005', ''),
    ('med_clarithromycin', 'child', 7, 'Respiratory and skin infections (6 mo–12 y)', 'PO', '7.5 mg/kg', '2× a day', '5–10 days', '—', 'Label · UK SmPC susp', 'S. pyogenes: at least 10 days'),
    ('med_clarithromycin', 'child', 8, 'Other infections', 'PO', '15 mg/kg/day ÷ 2', 'Every 12 h', '10 days', 'Adult dose', 'Label · FDA', ''),
    ('med_clarithromycin', 'child', 9, 'MAC (treatment/prophylaxis)', 'PO', '7.5 mg/kg', 'Every 12 h', 'Ongoing', '500 mg/dose', 'Label · FDA', ''),
    ('med_clarithromycin', 'child', 10, 'Pertussis (≥1 month)', 'PO', '15 mg/kg/day ÷ 2', '2× a day', '7 days', '1 g/day', 'CDC 2005', 'Not recommended <1 month')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_clarithromycin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_clarithromycin', 'renal', 0, 'CrCl <30', 'Halve the dose: 250 mg once a day (250 mg 2× a day in severe infection); children 7.5 mg/kg once a day; do not continue beyond 14 days.', 'Label · UK SmPC'),
    ('med_clarithromycin', 'renal', 1, 'CrCl 30–60', 'With ritonavir or atazanavir: reduce dose by 50%.', 'Label · FDA'),
    ('med_clarithromycin', 'renal', 2, 'CrCl <30', 'With ritonavir or atazanavir: reduce dose by 75%.', 'Label · FDA'),
    ('med_clarithromycin', 'hepatic', 3, '', 'No set dose change; use with caution. Contraindicated in severe hepatic failure with renal impairment.', 'Label · UK SmPC'),
    ('med_clarithromycin', 'elderly', 4, '', 'Same dose as adults; watch for colchicine toxicity in elderly with renal insufficiency.', 'Label · UK SmPC'),
    ('med_clarithromycin', 'pregnancy', 5, '', 'Safety not established; some studies show more first- and second-trimester miscarriage. Small amounts pass into breast milk (about 1.7% of the maternal weight-adjusted dose).', 'Label · UK SmPC'),
    ('med_clarithromycin', 'administration', 6, '', 'Tablets can be taken with or without food.', 'Label · UK SmPC'),
    ('med_clarithromycin', 'administration', 7, '', 'Suspension: shake well before each dose; food or a drink right after the dose masks the bitter aftertaste.', 'Label · UK SmPC susp'),
    ('med_clarithromycin', 'forms_ph', 8, '', 'Tablet 250 mg, 500 mg (base); granules/powder for suspension 125 mg/5 mL and 250 mg/5 mL, 50 mL.', 'PNF'),
    ('med_clarithromycin', 'monitor', 9, '', 'Check ECG, potassium and magnesium before use in patients at QT risk (heart disease, bradycardia, QT-prolonging drugs).', 'Label · UK SmPC'),
    ('med_clarithromycin', 'monitor', 10, '', 'Check INR closely with warfarin; digoxin levels with digoxin; glucose in diabetics on insulin or oral agents.', 'Label · UK SmPC'),
    ('med_clarithromycin', 'monitor', 11, '', 'Stop and check liver tests if jaundice, dark urine or abdominal pain appear; watch for diarrhoea up to 2 months after treatment (C. difficile).', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_clarithromycin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_clarithromycin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Clarithromycin 500 mg film-coated tablets. Summary of Product Characteristics. Milpharm Ltd; July 2026.', 'https://products.mhra.gov.uk/search/?search=clarithromycin#emc-7072', 0),
    ('med_clarithromycin', 'Label · UK SmPC susp', 'UK SmPC (emc)', 'Clarithromycin 125 mg/5 ml suspension. Summary of Product Characteristics. Sandoz Ltd; June 2021.', 'https://products.mhra.gov.uk/search/?search=clarithromycin#emc-515', 1),
    ('med_clarithromycin', 'Label · FDA', 'DailyMed (FDA label)', 'Clarithromycin tablet. Prescribing information. Sandoz Inc.; revised 5/2023.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=b98b02bb-2609-49a0-b29f-e5911aa0cbc1', 2),
    ('med_clarithromycin', 'CDC 2005', 'CDC (MMWR)', 'Recommended antimicrobial agents for the treatment and postexposure prophylaxis of pertussis: 2005 CDC guidelines. MMWR 2005;54(RR-14).', 'https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5414a1.htm', 3),
    ('med_clarithromycin', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_clarithromycin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_clarithromycin');


-- ================================================ med_clopidogrel  (Clopidogrel)
update public.medicines set description = 'Clopidogrel is a prodrug activated mainly by CYP2C19 to a metabolite that irreversibly blocks the platelet P2Y12 ADP receptor, preventing downstream glycoprotein IIb/IIIa activation and platelet aggregation. It is used, often with aspirin, in acute coronary syndromes and for secondary prevention after MI, stroke or peripheral arterial disease. Because the receptor block is irreversible, platelets stay affected for the rest of their lifespan (about 7–10 days); with 75 mg daily, inhibition starts on day 1 and reaches steady state between days 3 and 7, which is why a loading dose is used when a fast effect is needed. In the Philippines clopidogrel 75 mg tablets are on the PNF Essential Medicines List, and the DOST HTA Council used clopidogrel plus aspirin as the comparator when it did not recommend government financing of ticagrelor for ACS in 2025.', updated_at = now()
where id = 'med_clopidogrel' and description = 'Clopidogrel is a prodrug activated mainly by CYP2C19 to a metabolite that irreversibly blocks the platelet P2Y12 ADP receptor, preventing downstream glycoprotein IIb/IIIa activation and platelet aggregation. It is used, often with aspirin, in acute coronary syndromes and for secondary prevention after MI, stroke or peripheral arterial disease.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); Philippine National Formulary (PNF EML); DOST HTA Philippines; Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); Philippine National Formulary (PNF EML); DOST HTA Philippines; Philippine National Formulary – EML' end
where id = 'med_clopidogrel' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'indication', 'ACS patients undergoing PCI with stenting (with aspirin)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'indication' and content = 'ACS patients undergoing PCI with stenting (with aspirin)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'indication', 'Moderate- to high-risk TIA (ABCD2 ≥4) or minor ischaemic stroke (NIHSS ≤3), started within 24 h with aspirin', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'indication' and content = 'Moderate- to high-risk TIA (ABCD2 ≥4) or minor ischaemic stroke (NIHSS ≤3), started within 24 h with aspirin');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'indication', 'Atrial fibrillation with a vascular risk factor when a vitamin K antagonist is unsuitable and bleeding risk is low (with aspirin)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'indication' and content = 'Atrial fibrillation with a vascular risk factor when a vitamin K antagonist is unsuitable and bleeding risk is low (with aspirin)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'adverse', 'Haematoma, nosebleed, bruising and bleeding at puncture sites (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse' and content = 'Haematoma, nosebleed, bruising and bleeding at puncture sites (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'adverse', 'Diarrhoea, abdominal pain and dyspepsia (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse' and content = 'Diarrhoea, abdominal pain and dyspepsia (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'adverse', 'Thrombocytopenia, leucopenia and eosinophilia (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse' and content = 'Thrombocytopenia, leucopenia and eosinophilia (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'adverse', 'Headache, paraesthesia and dizziness (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse' and content = 'Headache, paraesthesia and dizziness (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'adverse', 'Gastric and duodenal ulcer, haematuria and eye bleeding (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse' and content = 'Gastric and duodenal ulcer, haematuria and eye bleeding (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'adverse', 'Acquired haemophilia (consider if isolated aPTT prolongation)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'adverse' and content = 'Acquired haemophilia (consider if isolated aPTT prolongation)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'contraindication', 'Severe hepatic impairment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication' and content = 'Severe hepatic impairment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'contraindication', 'Past hypersensitivity to ticlopidine or prasugrel: check for cross-reactivity (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication' and content = 'Past hypersensitivity to ticlopidine or prasugrel: check for cross-reactivity (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'contraindication', 'Hereditary galactose intolerance, lactase deficiency or glucose-galactose malabsorption (tablets contain lactose) (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication' and content = 'Hereditary galactose intolerance, lactase deficiency or glucose-galactose malabsorption (tablets contain lactose) (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'contraindication', 'Non-minor ischaemic stroke (NIHSS >4): dual antiplatelet therapy not recommended; start monotherapy only after the first 7 days (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication' and content = 'Non-minor ischaemic stroke (NIHSS >4): dual antiplatelet therapy not recommended; start monotherapy only after the first 7 days (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'contraindication', 'Children: not to be used (efficacy concerns) (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication' and content = 'Children: not to be used (efficacy concerns) (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'contraindication', 'Breastfeeding: stop breastfeeding during treatment (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'contraindication' and content = 'Breastfeeding: stop breastfeeding during treatment (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'interaction', 'Other CYP2C19 inhibitors (fluvoxamine, fluoxetine, moclobemide, voriconazole, fluconazole, ticlopidine, carbamazepine, efavirenz): reduce active metabolite; avoid.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction' and content = 'Other CYP2C19 inhibitors (fluvoxamine, fluoxetine, moclobemide, voriconazole, fluconazole, ticlopidine, carbamazepine, efavirenz): reduce active metabolite; avoid.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'interaction', 'Rifampicin (strong CYP2C19 inducer): avoid.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction' and content = 'Rifampicin (strong CYP2C19 inducer): avoid.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'interaction', 'Pantoprazole: can be used if a PPI is needed.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction' and content = 'Pantoprazole: can be used if a PPI is needed.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'interaction', 'Rosuvastatin: exposure about doubled after a 300 mg clopidogrel dose.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction' and content = 'Rosuvastatin: exposure about doubled after a 300 mg clopidogrel dose.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'interaction', 'Paclitaxel (CYP2C8 substrate): use with caution.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction' and content = 'Paclitaxel (CYP2C8 substrate): use with caution.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'interaction', 'Ritonavir- or cobicistat-boosted HIV therapy: concomitant use discouraged.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction' and content = 'Ritonavir- or cobicistat-boosted HIV therapy: concomitant use discouraged.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_clopidogrel', 'interaction', 'Heparin, GP IIb/IIIa inhibitors, thrombolytics and pentoxifylline: added bleeding risk; oral anticoagulants not recommended together.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_clopidogrel' and kind = 'interaction' and content = 'Heparin, GP IIb/IIIa inhibitors, thrombolytics and pentoxifylline: added bleeding risk; oral anticoagulants not recommended together.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_clopidogrel', 'UK SmPC (emc)', 'Clopidogrel 75 mg film-coated tablets – Summary of Product Characteristics. Dr. Reddy''s Laboratories (UK) Ltd (PL 08553/0766). Electronic Medicines Compendium (emc), medicines.org.uk; updated August 2024.', 'https://products.mhra.gov.uk/search/?search=clopidogrel#emc-15874', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_clopidogrel'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_clopidogrel' and url = 'https://products.mhra.gov.uk/search/?search=clopidogrel#emc-15874');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_clopidogrel', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_clopidogrel'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_clopidogrel' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_clopidogrel', 'DOST HTA Philippines', 'Health Technology Assessment Council. Call for Stakeholder Comments on the Preliminary Recommendation on Ticagrelor [90 mg film-coated tablet] as an Add-on to Aspirin for Adults with Acute Coronary Syndrome. Department of Science and Technology, HTA Philippines; 02 May 2025.', 'https://hta.dost.gov.ph/wp-content/uploads/2025/05/HTA-Council-Preliminary-Recommendation-on-Ticagrelor-90mg-film-coated-tablet-for-ACS-02-May-2025-1-2.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_clopidogrel'), 0)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_clopidogrel' and url = 'https://hta.dost.gov.ph/wp-content/uploads/2025/05/HTA-Council-Preliminary-Recommendation-on-Ticagrelor-90mg-film-coated-tablet-for-ACS-02-May-2025-1-2.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_clopidogrel', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'UK SmPC: limited experience in renal impairment; use with caution'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_clopidogrel');
-- med_clopidogrel
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_clopidogrel', 'adult', 0, 'NSTE-ACS', 'PO', '300 or 600 mg load, then 75 mg', 'Once a day', 'Up to 12 months', '—', 'Label · UK SmPC', 'With aspirin 75–100 mg; 600 mg load only if <75 y'),
    ('med_clopidogrel', 'adult', 1, 'STEMI, medically treated / fibrinolysis', 'PO', '300 mg load, then 75 mg', 'Once a day', 'At least 4 weeks', '—', 'Label · UK SmPC', 'With aspirin; >75 y: no loading dose'),
    ('med_clopidogrel', 'adult', 2, 'Primary PCI', 'PO', '600 mg load, then 75 mg', 'Once a day', 'Up to 12 months', '—', 'Label · UK SmPC', '300 mg load if PCI within 24 h of fibrinolysis; caution ≥75 y'),
    ('med_clopidogrel', 'adult', 3, 'TIA (ABCD2 ≥4) or minor stroke (NIHSS ≤3)', 'PO', '300 mg load, then 75 mg', 'Once a day', '21 days', '—', 'Label · UK SmPC', 'Start within 24 h with aspirin 75–100 mg; then single antiplatelet'),
    ('med_clopidogrel', 'adult', 4, 'Recent MI, ischaemic stroke or PAD', 'PO', '75 mg', 'Once a day', '—', '—', 'Label · UK SmPC', 'Stroke: 7 days to <6 months after event'),
    ('med_clopidogrel', 'adult', 5, 'Atrial fibrillation (VKA unsuitable)', 'PO', '75 mg', 'Once a day', '—', '—', 'Label · UK SmPC', 'With aspirin 75–100 mg')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_clopidogrel');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_clopidogrel', 'renal', 0, '', 'Limited experience; use with caution.', 'Label · UK SmPC'),
    ('med_clopidogrel', 'hepatic', 1, '', 'Contraindicated in severe hepatic impairment; otherwise limited experience, use with caution.', 'Label · UK SmPC'),
    ('med_clopidogrel', 'elderly', 2, '', 'NSTE-ACS: 600 mg load only under 75 y. STEMI medically treated over 75 y: no loading dose. Primary PCI ≥75 y: 600 mg load with caution.', 'Label · UK SmPC'),
    ('med_clopidogrel', 'pregnancy', 3, '', 'Preferably avoid (no clinical data). Stop breastfeeding during treatment.', 'Label · UK SmPC'),
    ('med_clopidogrel', 'administration', 4, '', 'Take with or without food. Missed dose: take if <12 h late; if >12 h, skip it and do not double.', 'Label · UK SmPC'),
    ('med_clopidogrel', 'administration', 5, '', 'Elective surgery: UK SmPC advises stopping 7 days before if an antiplatelet effect is not wanted.', 'Label · UK SmPC'),
    ('med_clopidogrel', 'forms_ph', 6, '', 'Tablet 75 mg.', 'PNF'),
    ('med_clopidogrel', 'monitor', 7, '', 'Watch for bleeding (black stools, bruising, nosebleeds, blood in urine), especially with aspirin, NSAIDs, SSRIs or anticoagulants.', 'Label · UK SmPC'),
    ('med_clopidogrel', 'monitor', 8, '', 'Suspected TTP (very rare, potentially fatal) needs urgent assessment and prompt treatment; check a platelet count.', 'Label · UK SmPC'),
    ('med_clopidogrel', 'monitor', 9, '', 'Unexplained isolated aPTT prolongation: test for acquired haemophilia.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_clopidogrel');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_clopidogrel', 'Label · UK SmPC', 'UK SmPC (emc)', 'Clopidogrel 75 mg film-coated tablets. Summary of Product Characteristics. Dr. Reddy''s Laboratories (UK) Ltd; 2024.', 'https://products.mhra.gov.uk/search/?search=clopidogrel#emc-15874', 0),
    ('med_clopidogrel', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 1)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_clopidogrel')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_clopidogrel');


-- ================================================ med_coamoxiclav  (Co-amoxiclav (Amoxicillin + Clavulanic acid))
update public.medicines set description = 'Amoxicillin inhibits bacterial cell-wall synthesis by binding penicillin-binding proteins, while clavulanic acid inhibits many beta-lactamases, protecting amoxicillin from degradation and extending coverage to beta-lactamase-producing organisms (e.g., H. influenzae, M. catarrhalis, many anaerobes and some Enterobacterales). It is used for sinusitis, otitis media, lower respiratory, skin, bite-wound and urinary infections. Both components are about 70% absorbed orally and have half-lives of about 1 hour, which is why it is given two or three times a day; amoxicillin does not reach adequate levels in the cerebrospinal fluid. MSF uses it as second-line treatment for otitis media and sinusitis when high-dose amoxicillin has failed, and the UK label advises switching to plain amoxicillin once an infection is shown to be amoxicillin-susceptible. In the Philippines it is on the PNF Essential Medicines List as tablets and oral suspensions.', updated_at = now()
where id = 'med_coamoxiclav' and description = 'Amoxicillin inhibits bacterial cell-wall synthesis by binding penicillin-binding proteins, while clavulanic acid inhibits many beta-lactamases, protecting amoxicillin from degradation and extending coverage to beta-lactamase-producing organisms (e.g., H. influenzae, M. catarrhalis, many anaerobes and some Enterobacterales). It is used for sinusitis, otitis media, lower respiratory, skin, bite-wound and urinary infections.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PNF EML); Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PNF EML); Philippine National Formulary – EML' end
where id = 'med_coamoxiclav' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'indication', 'Bone and joint infections, including osteomyelitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication' and content = 'Bone and joint infections, including osteomyelitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'indication', 'Severe dental abscess with spreading cellulitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication' and content = 'Severe dental abscess with spreading cellulitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'indication', 'Postpartum upper genital tract infection', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication' and content = 'Postpartum upper genital tract infection');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'indication', 'Oral step-down after IV treatment of severe infections (e.g., severe pneumonia)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication' and content = 'Oral step-down after IV treatment of severe infections (e.g., severe pneumonia)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'indication', 'Acute uncomplicated cystitis in girls over 2 years (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'indication' and content = 'Acute uncomplicated cystitis in girls over 2 years (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'adverse', 'Mucocutaneous candidosis (common); dizziness, headache and indigestion (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse' and content = 'Mucocutaneous candidosis (common); dizziness, headache and indigestion (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'adverse', 'Reversible leucopenia, neutropenia and thrombocytopenia (rare); agranulocytosis and haemolytic anaemia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse' and content = 'Reversible leucopenia, neutropenia and thrombocytopenia (rare); agranulocytosis and haemolytic anaemia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'adverse', 'Drug-induced enterocolitis syndrome (DIES), mainly in children: protracted vomiting 1–4 h after a dose', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse' and content = 'Drug-induced enterocolitis syndrome (DIES), mainly in children: protracted vomiting 1–4 h after a dose');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'adverse', 'Haemophagocytic lymphohistiocytosis (HLH)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse' and content = 'Haemophagocytic lymphohistiocytosis (HLH)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'adverse', 'Kounis syndrome (allergic acute coronary syndrome)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse' and content = 'Kounis syndrome (allergic acute coronary syndrome)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'adverse', 'Severe skin reactions: SJS, TEN, AGEP and DRESS', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse' and content = 'Severe skin reactions: SJS, TEN, AGEP and DRESS');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'adverse', 'Convulsions (with renal impairment or high doses) and aseptic meningitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse' and content = 'Convulsions (with renal impairment or high doses) and aseptic meningitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'adverse', 'Interstitial nephritis and crystalluria with acute kidney injury', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse' and content = 'Interstitial nephritis and crystalluria with acute kidney injury');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'adverse', 'Acute pancreatitis and black hairy tongue', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'adverse' and content = 'Acute pancreatitis and black hairy tongue');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'contraindication', 'Infections likely caused by penicillin-resistant S. pneumoniae or non-inhibitable beta-lactamases: not suitable (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'contraindication' and content = 'Infections likely caused by penicillin-resistant S. pneumoniae or non-inhibitable beta-lactamases: not suitable (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'contraindication', 'Children under 25 kg must not be given tablets; use suspension (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'contraindication' and content = 'Children under 25 kg must not be given tablets; use suspension (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'contraindication', 'Cephalosporin allergy: possible cross-sensitivity, use with caution (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'contraindication' and content = 'Cephalosporin allergy: possible cross-sensitivity, use with caution (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'interaction', 'Methotrexate: penicillins may reduce methotrexate excretion and increase toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'interaction' and content = 'Methotrexate: penicillins may reduce methotrexate excretion and increase toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_coamoxiclav', 'interaction', 'Mycophenolate mofetil: pre-dose mycophenolic acid levels fall by about 50%; monitor graft function closely.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_coamoxiclav' and kind = 'interaction' and content = 'Mycophenolate mofetil: pre-dose mycophenolic acid levels fall by about 50%; monitor graft function closely.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_coamoxiclav', 'UK SmPC (emc)', 'Augmentin 625 mg Tablets – Summary of Product Characteristics. GlaxoSmithKline UK; text revised 24 February 2026. Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-281', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_coamoxiclav'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_coamoxiclav' and url = 'https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-281');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_coamoxiclav', 'UK SmPC (emc)', 'Co-amoxiclav 875 mg/125 mg film-coated Tablets – Summary of Product Characteristics. Brown & Burk UK Ltd; text revised 19 September 2025. emc, medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10877', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_coamoxiclav'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_coamoxiclav' and url = 'https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10877');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_coamoxiclav', 'UK SmPC (emc)', 'Augmentin Duo 400/57 powder for oral suspension – Summary of Product Characteristics. GlaxoSmithKline UK; text revised 6 January 2026. emc, medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10038', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_coamoxiclav'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_coamoxiclav' and url = 'https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10038');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_coamoxiclav', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Amoxicillin/clavulanic acid = co-amoxiclav, oral. MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/amoxicillin-clavulanic-acid-co-amoxiclav-oral-16685119.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_coamoxiclav'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_coamoxiclav' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/amoxicillin-clavulanic-acid-co-amoxiclav-oral-16685119.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_coamoxiclav', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_coamoxiclav'), 0)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_coamoxiclav' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_coamoxiclav', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Renally cleared: reduce to 500/125 mg 2× a day (CrCl 10–30) or once a day (CrCl <10); 7:1 forms (875/125 mg) not recommended if CrCl <30; convulsion risk'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_coamoxiclav');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'rabies', 'med_coamoxiclav', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'rabies'), 0), 'safe'::condition_safety, 'Used for animal-bite wound treatment/prophylaxis (MSF, UK SmPC); it does not treat rabies itself and is given alongside rabies post-exposure care (our inference)'
where exists (select 1 from public.diseases where id = 'rabies')
  and exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.disease_medicines where disease_id = 'rabies' and medicine_id = 'med_coamoxiclav');
-- med_coamoxiclav
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_coamoxiclav', 'adult', 0, 'Most infections (4:1 tablet)', 'PO', '500/125 mg', 'Every 8 h', 'Per response; review if >14 days', '1500/375 mg/day', 'Label · UK SmPC 625', 'Also children ≥40 kg'),
    ('med_coamoxiclav', 'adult', 1, 'Most infections (7:1 tablet)', 'PO', '875/125 mg', '2× a day', 'Per response; review if >14 days', '1750/250 mg/day', 'Label · UK SmPC 875', 'Also children ≥40 kg'),
    ('med_coamoxiclav', 'adult', 2, 'Otitis media, sinusitis, LRTI, UTI (higher dose)', 'PO', '875/125 mg', 'Every 8 h', 'Per response; review if >14 days', '2625/375 mg/day', 'Label · UK SmPC 875', ''),
    ('med_coamoxiclav', 'adult', 3, 'Animal bites', 'PO', '875/125 mg', '2× a day', '5–7 days', '—', 'MSF', '8:1 form: 1000/125 mg 2× a day'),
    ('med_coamoxiclav', 'adult', 4, 'Otitis media / sinusitis after amoxicillin failure', 'PO', '875/125 mg', '2× a day', '5 days (otitis); 7–10 days (sinusitis)', '—', 'MSF', '8:1 form: 1000/125 mg 2× a day'),
    ('med_coamoxiclav', 'adult', 5, 'Postpartum upper genital tract infection', 'PO', '875/125 mg', 'Every 8 h', '7 days', '—', 'MSF', '8:1 form: 1000/125 mg every 8 h'),
    ('med_coamoxiclav', 'adult', 6, 'IV-to-oral switch, severe pneumonia', 'PO', '875/125 mg', 'Every 8 h', '10–14 days total', '—', 'MSF', '8:1 form: 1000/125 mg every 8 h'),
    ('med_coamoxiclav', 'child', 7, 'Most infections, <40 kg (4:1 forms)', 'PO', '20–60 mg/kg/day ÷ 3', 'Every 8 h', 'Per response; review if >14 days', '2400/600 mg/day', 'Label · UK SmPC 625', 'Tablets only if ≥25 kg; <2 y may need 4:1 suspension'),
    ('med_coamoxiclav', 'child', 8, 'Most infections, <40 kg (7:1 forms)', 'PO', '25–45 mg/kg/day ÷ 2', '2× a day', 'Per response; review if >14 days', '—', 'Label · UK SmPC susp', 'No data under 2 months'),
    ('med_coamoxiclav', 'child', 9, 'Otitis media, sinusitis, LRTI (higher dose, 7:1)', 'PO', '45–70 mg/kg/day ÷ 2', '2× a day', 'Per response', '70 mg/kg/day', 'Label · UK SmPC susp', 'Not >45 mg/kg/day under 2 years'),
    ('med_coamoxiclav', 'child', 10, 'Animal bites; otitis/sinusitis after amoxicillin failure', 'PO', '25 mg/kg', '2× a day', '5–7 days (bites); 5 days (otitis); 7–10 days (sinusitis)', '—', 'MSF', 'Clavulanate ≤12.5 mg/kg/day'),
    ('med_coamoxiclav', 'child', 11, 'Uncomplicated cystitis (girls >2 y)', 'PO', '12.5 mg/kg', '2× a day', '3 days', '—', 'MSF', ''),
    ('med_coamoxiclav', 'child', 12, 'IV-to-oral switch, severe infections', 'PO', '50 mg/kg', '2× a day', '10–14 days total (pneumonia)', '—', 'MSF', '7:1 or 8:1 forms; clavulanate ≤12.5 mg/kg/day')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_coamoxiclav');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_coamoxiclav', 'renal', 0, 'CrCl >30', 'No dose adjustment.', 'Label · UK SmPC 625'),
    ('med_coamoxiclav', 'renal', 1, 'CrCl 10–30', '500/125 mg 2× a day; children <40 kg 15/3.75 mg/kg 2× a day (max 500/125 mg per dose).', 'Label · UK SmPC 625'),
    ('med_coamoxiclav', 'renal', 2, 'CrCl <10', '500/125 mg once a day; children <40 kg 15/3.75 mg/kg once a day (max 500/125 mg).', 'Label · UK SmPC 625'),
    ('med_coamoxiclav', 'renal', 3, 'Haemodialysis', '500/125 mg every 24 h, plus one dose during dialysis and another at the end; children 15/3.75 mg/kg before and after dialysis.', 'Label · UK SmPC 625'),
    ('med_coamoxiclav', 'renal', 4, 'CrCl <30', '7:1 forms (875/125 mg tablet, 400/57 mg suspension) are not recommended; use a 4:1 form.', 'Label · UK SmPC 875'),
    ('med_coamoxiclav', 'hepatic', 5, '', 'Use with caution and monitor liver function regularly. Liver injury is more common in males, the elderly and with long courses, and may appear weeks after stopping.', 'Label · UK SmPC 625'),
    ('med_coamoxiclav', 'elderly', 6, '', 'No dose adjustment; check renal function and adjust if impaired.', 'Label · UK SmPC 625'),
    ('med_coamoxiclav', 'pregnancy', 7, '', 'UK label: avoid unless essential (necrotising enterocolitis reported in newborns after use for preterm premature rupture of membranes); passes into breast milk (diarrhoea, thrush in the infant). MSF: not contraindicated in pregnancy or breastfeeding.', 'Label · UK SmPC 625'),
    ('med_coamoxiclav', 'administration', 8, '', 'Tablets cannot be divided; children ≤6 years or <25 kg should get suspension. Reconstituted suspension: keep at 2–8 °C, use within 7 days, shake before each dose.', 'Label · UK SmPC susp'),
    ('med_coamoxiclav', 'forms_ph', 9, '', 'Tablets 500 mg + 125 mg, 875 mg + 125 mg; granules/powder for suspension 200 mg + 28.5 mg/5 mL (70 mL), 400 mg + 57 mg/5 mL (70 mL), 600 mg + 42.9 mg/5 mL.', 'PNF'),
    ('med_coamoxiclav', 'monitor', 10, '', 'Check liver tests, renal function and blood counts during prolonged courses.', 'Label · UK SmPC 625'),
    ('med_coamoxiclav', 'monitor', 11, '', 'On warfarin/acenocoumarol: check INR when starting and stopping; on mycophenolate: watch graft function.', 'Label · UK SmPC 625'),
    ('med_coamoxiclav', 'monitor', 12, '', 'Children: protracted vomiting 1–4 h after a dose suggests DIES; stop the drug.', 'Label · UK SmPC 625')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_coamoxiclav');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_coamoxiclav', 'Label · UK SmPC 625', 'UK SmPC (emc)', 'Augmentin 625 mg Tablets (500/125 mg). Summary of Product Characteristics. GlaxoSmithKline UK; 2026.', 'https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-281', 0),
    ('med_coamoxiclav', 'Label · UK SmPC 875', 'UK SmPC (emc)', 'Co-amoxiclav 875 mg/125 mg film-coated Tablets. Summary of Product Characteristics. Brown & Burk UK Ltd; 2025.', 'https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10877', 1),
    ('med_coamoxiclav', 'Label · UK SmPC susp', 'UK SmPC (emc)', 'Augmentin Duo 400/57 powder for oral suspension. Summary of Product Characteristics. GlaxoSmithKline UK; 2026.', 'https://products.mhra.gov.uk/search/?search=co-amoxiclav#emc-10038', 2),
    ('med_coamoxiclav', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Co-amoxiclav oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/amoxicillin-clavulanic-acid-co-amoxiclav-oral-16685119.html', 3),
    ('med_coamoxiclav', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_coamoxiclav')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_coamoxiclav');


-- ================================================ med_colchicine  (Colchicine)
update public.medicines set description = 'Colchicine binds tubulin and disrupts microtubules in neutrophils, reducing their migration and inflammasome activation in response to urate crystals. It treats gout flares best when started within 24-36 hours and prevents flares when urate-lowering therapy is started. It has a narrow therapeutic window, and overdose can be fatal. Colchicine is rapidly absorbed (peak 30–120 minutes), concentrates in leucocytes, is excreted mainly in the faeces, and has a half-life of 3–10 hours that rises to about 18.8 hours in severe renal impairment; the lethal single dose varies from about 7 to 65 mg and is generally around 20 mg in adults. A low-dose 0.5 mg once-daily regimen is now licensed in the US to reduce myocardial infarction, stroke and cardiovascular death in atherosclerotic disease. In the Philippines, colchicine is on the PNF Essential Medicines List as a 500 microgram tablet.', updated_at = now()
where id = 'med_colchicine' and description = 'Colchicine binds tubulin and disrupts microtubules in neutrophils, reducing their migration and inflammasome activation in response to urate crystals. It treats gout flares best when started within 24-36 hours and prevents flares when urate-lowering therapy is started. It has a narrow therapeutic window, and overdose can be fatal.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); DailyMed – COLCRYS; DailyMed – LODOCO; Philippine National Formulary (PNF EML)' else source_attribution || '; UK SmPC (emc); DailyMed – COLCRYS; DailyMed – LODOCO; Philippine National Formulary (PNF EML)' end
where id = 'med_colchicine' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'indication', 'Reduce the risk of myocardial infarction, stroke, coronary revascularization and cardiovascular death in adults with established atherosclerotic disease or multiple cardiovascular risk factors (low-dose 0.5 mg daily)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'indication' and content = 'Reduce the risk of myocardial infarction, stroke, coronary revascularization and cardiovascular death in adults with established atherosclerotic disease or multiple cardiovascular risk factors (low-dose 0.5 mg daily)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'indication', 'Familial Mediterranean fever in children (attack prophylaxis and prevention of amyloidosis)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'indication' and content = 'Familial Mediterranean fever in children (attack prophylaxis and prevention of amyloidosis)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'adverse', 'Agranulocytosis and aplastic anaemia (can be fatal)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse' and content = 'Agranulocytosis and aplastic anaemia (can be fatal)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'adverse', 'Vitamin B12 deficiency with long-term use (reversible malabsorption)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse' and content = 'Vitamin B12 deficiency with long-term use (reversible malabsorption)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'adverse', 'Gastrointestinal haemorrhage and hepatotoxicity', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse' and content = 'Gastrointestinal haemorrhage and hepatotoxicity');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'adverse', 'Alopecia and rash', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse' and content = 'Alopecia and rash');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'adverse', 'Amenorrhoea, dysmenorrhoea, and reversible oligospermia or azoospermia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse' and content = 'Amenorrhoea, dysmenorrhoea, and reversible oligospermia or azoospermia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'adverse', 'Myalgia (21.2% vs 18.5% with placebo in the LoDoCo2 trial)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'adverse' and content = 'Myalgia (21.2% vs 18.5% with placebo in the LoDoCo2 trial)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'contraindication', 'Pre-existing blood dyscrasias', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication' and content = 'Pre-existing blood dyscrasias');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'contraindication', 'Haemodialysis (colchicine is not removed by dialysis)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication' and content = 'Haemodialysis (colchicine is not removed by dialysis)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'contraindication', 'Renal failure with creatinine clearance below 15 mL/min (low-dose cardiovascular product)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication' and content = 'Renal failure with creatinine clearance below 15 mL/min (low-dose cardiovascular product)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'contraindication', 'Pregnancy and breastfeeding when used for gout (UK SmPC); women of childbearing potential not using effective contraception', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication' and content = 'Pregnancy and breastfeeding when used for gout (UK SmPC); women of childbearing potential not using effective contraception');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'contraindication', 'Galactose intolerance, Lapp lactase deficiency or glucose-galactose malabsorption (lactose-containing tablets; precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'contraindication' and content = 'Galactose intolerance, Lapp lactase deficiency or glucose-galactose malabsorption (lactose-containing tablets; precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'interaction', 'Itraconazole, voriconazole and HIV protease inhibitors (atazanavir, indinavir): strong CYP3A4 inhibitors; reduce colchicine dose about 4-fold.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction' and content = 'Itraconazole, voriconazole and HIV protease inhibitors (atazanavir, indinavir): strong CYP3A4 inhibitors; reduce colchicine dose about 4-fold.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'interaction', 'Diltiazem and erythromycin (moderate CYP3A4 inhibitors): reduce colchicine dose about 2-fold and monitor for toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction' and content = 'Diltiazem and erythromycin (moderate CYP3A4 inhibitors): reduce colchicine dose about 2-fold and monitor for toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'interaction', 'Fluconazole: moderate CYP3A4 inhibitor; expect higher colchicine levels and monitor.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction' and content = 'Fluconazole: moderate CYP3A4 inhibitor; expect higher colchicine levels and monitor.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'interaction', 'Quinidine, disulfiram and ranolazine (P-gp inhibitors): increased colchicine exposure.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction' and content = 'Quinidine, disulfiram and ranolazine (P-gp inhibitors): increased colchicine exposure.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'interaction', 'Azithromycin: raised colchicine levels reported; follow up during and after treatment.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction' and content = 'Azithromycin: raised colchicine levels reported; follow up during and after treatment.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'interaction', 'Cimetidine and tolbutamide: reduce colchicine metabolism.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'interaction' and content = 'Cimetidine and tolbutamide: reduce colchicine metabolism.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_colchicine', 'brand_intl', 'Lodoco', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'brand_intl'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine' and kind = 'brand_intl' and content = 'Lodoco');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_colchicine', 'UK SmPC (emc)', 'Colchicine 500 microgram Tablets – Summary of Product Characteristics. Strides Pharma UK Ltd (PL 13606/0271). Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=colchicine#emc-14362', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_colchicine'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_colchicine' and url = 'https://products.mhra.gov.uk/search/?search=colchicine#emc-14362');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_colchicine', 'DailyMed – COLCRYS', 'COLCRYS (colchicine) tablet, film coated. Prescribing information. AR Scientific Inc. DailyMed, US National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5ecaa34e-1bed-49a5-b97c-a8f8c0d885a7', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_colchicine'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_colchicine' and url = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5ecaa34e-1bed-49a5-b97c-a8f8c0d885a7');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_colchicine', 'DailyMed – LODOCO', 'LODOCO (colchicine) tablets 0.5 mg. Prescribing information. DailyMed, US National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ff06d68f-d65f-d097-e053-6294a90a7e5f', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_colchicine'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_colchicine' and url = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ff06d68f-d65f-d097-e053-6294a90a7e5f');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_colchicine', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_colchicine'), 0)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_colchicine' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_colchicine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Half-life prolonged in renal impairment; reduce dose in mild–moderate impairment; contraindicated in severe impairment and haemodialysis (UK SmPC)'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_colchicine');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_coronary_syndrome', 'med_colchicine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome'), 0), 'safe'::condition_safety, 'Low-dose 0.5 mg daily is licensed (Lodoco) for long-term risk reduction of MI, stroke and CV death in established atherosclerotic disease; not an acute ACS treatment (link inferred from the label indication)'
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome' and medicine_id = 'med_colchicine');
-- med_colchicine
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_colchicine', 'adult', 0, 'Acute gout', 'PO', '1 mg, then 500 mcg 1 h later', 'Then 500 mcg every 8 h (after a 12 h pause) if needed', 'Until relief', '6 mg per course', 'Label · UK SmPC', 'No new course within 72 h; stop if diarrhoea or vomiting'),
    ('med_colchicine', 'adult', 1, 'Gout flare (US regimen)', 'PO', '1.2 mg, then 0.6 mg 1 h later', 'Single course', '—', '1.8 mg over 1 h', 'Label · US Colcrys', 'Higher doses are not more effective'),
    ('med_colchicine', 'adult', 2, 'Gout flare prophylaxis', 'PO', '0.5–1 mg', 'Once a day (evening)', 'While starting urate-lowering therapy', '1 mg/day', 'Label · UK SmPC', 'Duration depends on flare frequency and tophi'),
    ('med_colchicine', 'adult', 3, 'Gout flare prophylaxis (US regimen)', 'PO', '0.6 mg', '1–2× a day', '—', '1.2 mg/day', 'Label · US Colcrys', 'Also adolescents >16 y'),
    ('med_colchicine', 'adult', 4, 'Familial Mediterranean fever', 'PO', '1–3 mg/day', 'Once a day or ÷ 2', 'Long-term', '3 mg/day', 'Label · UK SmPC', 'Split into 2 doses when >1 mg/day'),
    ('med_colchicine', 'adult', 5, 'Cardiovascular risk reduction', 'PO', '0.5 mg', 'Once a day', 'Long-term', '0.5 mg/day', 'Label · US Lodoco', 'Do not double a missed dose'),
    ('med_colchicine', 'child', 6, 'Familial Mediterranean fever (<5 y)', 'PO', '0.5 mg/day', 'Once a day', 'Long-term', '2 mg/day', 'Label · UK SmPC', 'Specialist supervision only'),
    ('med_colchicine', 'child', 7, 'Familial Mediterranean fever (5–10 y)', 'PO', '1 mg/day', 'Once a day or ÷ 2', 'Long-term', '2 mg/day', 'Label · UK SmPC', 'Specialist supervision only'),
    ('med_colchicine', 'child', 8, 'Familial Mediterranean fever (>10 y)', 'PO', '1.5 mg/day', 'Once a day or ÷ 2', 'Long-term', '2 mg/day', 'Label · UK SmPC', 'Up to 2 mg/day in amyloid nephropathy; not for gout in children')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_colchicine');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_colchicine', 'renal', 0, 'Mild–moderate', 'Gout: 0.5 mg/day with close monitoring. FMF: halve the starting dose (≤1 mg/day).', 'Label · UK SmPC'),
    ('med_colchicine', 'renal', 1, 'Severe', 'Contraindicated, including patients on haemodialysis.', 'Label · UK SmPC'),
    ('med_colchicine', 'renal', 2, 'CrCl <30 / dialysis', 'US label: prophylaxis start 0.3 mg/day; flare treatment no dose change but repeat courses no more than once every 2 weeks. Dialysis: prophylaxis 0.3 mg twice weekly; flare 0.6 mg single dose, repeat no more than once every 2 weeks.', 'Label · US Colcrys'),
    ('med_colchicine', 'hepatic', 3, '', 'Gout: use with caution at 0.5 mg/day. FMF: halve the starting dose (≤1 mg/day). Severe hepatic impairment: contraindicated.', 'Label · UK SmPC'),
    ('med_colchicine', 'hepatic', 4, '', 'Avoid with strong P-gp or strong/moderate CYP3A4 inhibitors in any degree of hepatic impairment.', 'Label · US Lodoco'),
    ('med_colchicine', 'elderly', 5, '', 'No specific age-based dose, but use with caution in elderly and debilitated patients.', 'Label · UK SmPC'),
    ('med_colchicine', 'pregnancy', 6, '', 'Gout: avoid unless NSAIDs and glucocorticoids are unsuitable; do not use while breastfeeding. FMF: may be considered if clinically needed. Women should use contraception during and for 3 months after treatment.', 'Label · UK SmPC'),
    ('med_colchicine', 'administration', 7, '', 'Swallow tablets whole with water. With strong CYP3A4 inhibitors (e.g. clarithromycin) the US label cuts flare treatment to 0.6 mg then 0.3 mg 1 h later, repeated no sooner than 3 days.', 'Label · US Colcrys'),
    ('med_colchicine', 'monitor', 8, '', 'Full blood count periodically (and at once if petechiae, fever, mouth ulcers, sore throat or bleeding); vitamin B12 with long-term use; muscle symptoms and CK with statins or fibrates; stop at the first diarrhoea or vomiting.', 'Label · UK SmPC'),
    ('med_colchicine', 'forms_ph', 9, '', 'Oral: 500 microgram tablet.', 'PNF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_colchicine');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_colchicine', 'Label · UK SmPC', 'UK SmPC (emc)', 'Colchicine 500 microgram Tablets – SmPC. Strides Pharma UK Ltd. emc.', 'https://products.mhra.gov.uk/search/?search=colchicine#emc-14362', 0),
    ('med_colchicine', 'Label · US Colcrys', 'DailyMed – COLCRYS', 'COLCRYS (colchicine) tablets. Prescribing information. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5ecaa34e-1bed-49a5-b97c-a8f8c0d885a7', 1),
    ('med_colchicine', 'Label · US Lodoco', 'DailyMed – LODOCO', 'LODOCO (colchicine) tablets 0.5 mg. Prescribing information. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ff06d68f-d65f-d097-e053-6294a90a7e5f', 2),
    ('med_colchicine', 'PNF', 'Philippine National Formulary (PNF EML)', 'PNF Essential Medicines List, 8th Edition, as of November 02, 2022. PhilHealth / DOH.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_colchicine')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_colchicine');


-- ================================================ med_cotrimoxazole  (Co-trimoxazole (Sulfamethoxazole + Trimethoprim))
update public.medicines set description = 'Co-trimoxazole combines sulfamethoxazole, which inhibits dihydropteroate synthase and blocks bacterial use of para-aminobenzoic acid, with trimethoprim, which inhibits dihydrofolate reductase. Sequential blockade of folate synthesis gives a synergistic, often bactericidal effect. It is used for urinary tract infections, shigellosis, traveler''s diarrhea, exacerbations of chronic bronchitis, and for treatment and prophylaxis of Pneumocystis jirovecii pneumonia and toxoplasmosis. Trimethoprim has a half-life of about 8.6–17 hours that becomes 1.5–3 times longer when creatinine clearance falls below 10 mL/min, so the dose is reduced in renal impairment. Because of resistance, the UK label keeps it for Pneumocystis pneumonia, toxoplasmosis and nocardiosis, and for urinary tract infection, bronchitis exacerbations and otitis media only when the organism is shown to be susceptible; MSF also uses it for isosporiasis, cyclosporiasis, brucellosis and susceptible typhoid fever. In the Philippines it is on the PNF Essential Medicines List as tablets, oral suspensions and an injection for IV infusion.', updated_at = now()
where id = 'med_cotrimoxazole' and description = 'Co-trimoxazole combines sulfamethoxazole, which inhibits dihydropteroate synthase and blocks bacterial use of para-aminobenzoic acid, with trimethoprim, which inhibits dihydrofolate reductase. Sequential blockade of folate synthesis gives a synergistic, often bactericidal effect. It is used for urinary tract infections, shigellosis, traveler''s diarrhea, exacerbations of chronic bronchitis, and for treatment and prophylaxis of Pneumocystis jirovecii pneumonia and toxoplasmosis.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; Merck Manual Professional; Philippine National Formulary (PNF EML); Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; Merck Manual Professional; Philippine National Formulary (PNF EML); Philippine National Formulary – EML' end
where id = 'med_cotrimoxazole' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'indication', 'Nocardiosis (treatment)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication' and content = 'Nocardiosis (treatment)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'indication', 'Isosporiasis and cyclosporiasis (treatment); isosporiasis prophylaxis in HIV', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication' and content = 'Isosporiasis and cyclosporiasis (treatment); isosporiasis prophylaxis in HIV');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'indication', 'Brucellosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication' and content = 'Brucellosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'indication', 'Uncomplicated typhoid fever, only if the strain is susceptible', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication' and content = 'Uncomplicated typhoid fever, only if the strain is susceptible');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'indication', 'Bacterial prostatitis and prophylaxis of recurrent UTI', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication' and content = 'Bacterial prostatitis and prophylaxis of recurrent UTI');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'indication', 'Oral treatment of uncomplicated community-associated MRSA infections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication' and content = 'Oral treatment of uncomplicated community-associated MRSA infections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'indication', 'Listeria monocytogenes infections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'indication' and content = 'Listeria monocytogenes infections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'adverse', 'Headache, diarrhoea and fungal overgrowth (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse' and content = 'Headache, diarrhoea and fungal overgrowth (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'adverse', 'Hyponatraemia and metabolic acidosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse' and content = 'Hyponatraemia and metabolic acidosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'adverse', 'DRESS and acute generalised exanthematous pustulosis (AGEP)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse' and content = 'DRESS and acute generalised exanthematous pustulosis (AGEP)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'adverse', 'Haemophagocytic lymphohistiocytosis (HLH), very rare', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse' and content = 'Haemophagocytic lymphohistiocytosis (HLH), very rare');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'adverse', 'Respiratory toxicity (cough, dyspnoea, lung infiltrates) that can progress to ARDS, very rare', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse' and content = 'Respiratory toxicity (cough, dyspnoea, lung infiltrates) that can progress to ARDS, very rare');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'adverse', 'Aseptic meningitis, convulsions, peripheral neuropathy, ataxia and hallucinations (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse' and content = 'Aseptic meningitis, convulsions, peripheral neuropathy, ataxia and hallucinations (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'adverse', 'Methaemoglobinaemia, pancreatitis and uveitis (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse' and content = 'Methaemoglobinaemia, pancreatitis and uveitis (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'adverse', 'Rhabdomyolysis reported in HIV patients treated for Pneumocystis pneumonia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'adverse' and content = 'Rhabdomyolysis reported in HIV patients treated for Pneumocystis pneumonia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'contraindication', 'Acute porphyria', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication' and content = 'Acute porphyria');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'contraindication', 'Group A streptococcal pharyngitis: not recommended, less effective than penicillin (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication' and content = 'Group A streptococcal pharyngitis: not recommended, less effective than penicillin (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'contraindication', 'Severe atopy or bronchial asthma: use with caution (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication' and content = 'Severe atopy or bronchial asthma: use with caution (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'contraindication', 'Pregnancy: avoid in the first trimester and near delivery unless clearly needed; give folate if used (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication' and content = 'Pregnancy: avoid in the first trimester and near delivery unless clearly needed; give folate if used (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'contraindication', 'Breastfeeding infants under 8 weeks or with jaundice: avoid (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'contraindication' and content = 'Breastfeeding infants under 8 weeks or with jaundice: avoid (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'interaction', 'Zidovudine: increased risk of haematological toxicity; monitor blood counts.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction' and content = 'Zidovudine: increased risk of haematological toxicity; monitor blood counts.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'interaction', 'Lamivudine: lamivudine exposure increased by about 40%.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction' and content = 'Lamivudine: lamivudine exposure increased by about 40%.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'interaction', 'Pyrimethamine (>25 mg weekly): risk of megaloblastic anaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction' and content = 'Pyrimethamine (>25 mg weekly): risk of megaloblastic anaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'interaction', 'Thiazide diuretics: increased risk of thrombocytopenia in the elderly.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction' and content = 'Thiazide diuretics: increased risk of thrombocytopenia in the elderly.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'interaction', 'Procainamide and amantadine: competition for renal secretion may raise levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction' and content = 'Procainamide and amantadine: competition for renal secretion may raise levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'interaction', 'Repaglinide: increased exposure and risk of hypoglycaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction' and content = 'Repaglinide: increased exposure and risk of hypoglycaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'interaction', 'Folinic acid: reduces antimicrobial efficacy, including in Pneumocystis treatment and prophylaxis.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction' and content = 'Folinic acid: reduces antimicrobial efficacy, including in Pneumocystis treatment and prophylaxis.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'interaction', 'Oral contraceptives: contraceptive failure reported; use extra barrier protection.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction' and content = 'Oral contraceptives: contraceptive failure reported; use extra barrier protection.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_cotrimoxazole', 'interaction', 'Azathioprine: conflicting reports of serious haematological abnormalities.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_cotrimoxazole' and kind = 'interaction' and content = 'Azathioprine: conflicting reports of serious haematological abnormalities.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_cotrimoxazole', 'UK SmPC (emc)', 'Co-Trimoxazole Forte 160/800 mg Tablets – Summary of Product Characteristics. Tillomed Laboratories Ltd; revised 16 August 2025. Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-11466', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole' and url = 'https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-11466');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_cotrimoxazole', 'UK SmPC (emc)', 'Co-Trimoxazole 40 mg/200 mg per 5 ml Paediatric Suspension – Summary of Product Characteristics. Aspen Pharma Trading Ltd; text revised January 2026. emc, medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-6994', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole' and url = 'https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-6994');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_cotrimoxazole', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Co-trimoxazole = sulfamethoxazole (SMX)/trimethoprim (TMP), oral. MSF Medical Guidelines; updated December 2024.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/co-trimoxazole-sulfamethoxazole-smx-trimethoprim-tmp-oral-16683418.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/co-trimoxazole-sulfamethoxazole-smx-trimethoprim-tmp-oral-16683418.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_cotrimoxazole', 'Merck Manual Professional', 'Werth BJ. Trimethoprim and Sulfamethoxazole. Merck Manual Professional Version; reviewed/revised May 2024.', 'https://www.merckmanuals.com/professional/infectious-diseases/bacteria-and-antibacterial-medications/trimethoprim-and-sulfamethoxazole', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/bacteria-and-antibacterial-medications/trimethoprim-and-sulfamethoxazole');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_cotrimoxazole', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole'), 0)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_cotrimoxazole' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'typhoid_fever', 'med_cotrimoxazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'typhoid_fever'), 0), 'safe'::condition_safety, 'MSF: for uncomplicated typhoid only if a recent susceptibility test shows the strain is susceptible'
where exists (select 1 from public.diseases where id = 'typhoid_fever')
  and exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'typhoid_fever' and medicine_id = 'med_cotrimoxazole');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'urinary_tract_infection', 'med_cotrimoxazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'urinary_tract_infection'), 0), 'safe'::condition_safety, 'UK label: acute uncomplicated UTI when susceptibility is shown; Merck: 3-day course for cystitis where resistance <15%'
where exists (select 1 from public.diseases where id = 'urinary_tract_infection')
  and exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'urinary_tract_infection' and medicine_id = 'med_cotrimoxazole');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'copd', 'med_cotrimoxazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'copd'), 0), 'safe'::condition_safety, 'UK label: acute exacerbation of chronic bronchitis when susceptibility is shown'
where exists (select 1 from public.diseases where id = 'copd')
  and exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'copd' and medicine_id = 'med_cotrimoxazole');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_cotrimoxazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Halve the dose at CrCl 15–30, not recommended <15; hyperkalaemia and false rise in serum creatinine'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_cotrimoxazole');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_cotrimoxazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Hypoglycaemia with sulfonylureas or repaglinide (UK label); Merck notes renal adverse effects are more likely in diabetes'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_cotrimoxazole');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hypertension', 'med_cotrimoxazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hypertension'), 0), 'caution'::condition_safety, 'Hyperkalaemia with ACE inhibitors, ARBs, spironolactone and other potassium-sparing diuretics; thrombocytopenia with thiazides in the elderly'
where exists (select 1 from public.diseases where id = 'hypertension')
  and exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hypertension' and medicine_id = 'med_cotrimoxazole');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'rheumatic_fever', 'med_cotrimoxazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'rheumatic_fever'), 0), 'avoid'::condition_safety, 'Not recommended for group A streptococcal pharyngitis (UK label, Merck); so not suited to rheumatic fever prevention (our inference)'
where exists (select 1 from public.diseases where id = 'rheumatic_fever')
  and exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'rheumatic_fever' and medicine_id = 'med_cotrimoxazole');
-- med_cotrimoxazole
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_cotrimoxazole', 'adult', 0, 'UTI, bronchitis exacerbation, otitis (susceptible)', 'PO', '800/160 mg', 'Every 12 h', '≥5 days; until symptom-free 2 days', '—', 'Label · UK SmPC', 'Uncomplicated lower UTI: 1–3 days. Doses as SMX/TMP'),
    ('med_cotrimoxazole', 'adult', 1, 'Pneumocystis pneumonia, treatment', 'PO', '100/20 mg/kg/day ÷ 2 or more', 'In 2+ divided doses', '14 days', '—', 'Label · UK SmPC', 'MSF: 1600/320 mg every 8 h for 21 days'),
    ('med_cotrimoxazole', 'adult', 2, 'Pneumocystis pneumonia, prophylaxis', 'PO', '800/160 mg', 'Once a day', 'As long as needed', '1600/320 mg/day', 'Label · UK SmPC', 'Or 800/160 mg 3× a week on alternate days'),
    ('med_cotrimoxazole', 'adult', 3, 'Cerebral toxoplasmosis, treatment', 'PO', '25/5 mg/kg', '2× a day', '4–6 weeks', '—', 'MSF 2024', ''),
    ('med_cotrimoxazole', 'adult', 4, 'Isosporiasis / cyclosporiasis', 'PO', '800/160 mg', '2× a day', '7–10 days / 7 days', '—', 'MSF 2024', ''),
    ('med_cotrimoxazole', 'adult', 5, 'Typhoid fever, pertussis (susceptible)', 'PO', '800/160 mg', '2× a day', '14 days', '—', 'MSF 2024', 'Typhoid only if strain susceptible'),
    ('med_cotrimoxazole', 'adult', 6, 'Brucellosis', 'PO', '800/160 mg', '2× a day', '6 weeks', '—', 'MSF 2024', ''),
    ('med_cotrimoxazole', 'child', 7, 'Acute infections, 6 weeks–5 months', 'PO', '100/20 mg (2.5 mL susp)', 'Every 12 h', '≥5 days', '—', 'Label · UK SmPC susp', '≈30/6 mg/kg/day'),
    ('med_cotrimoxazole', 'child', 8, 'Acute infections, 6 months–5 years', 'PO', '200/40 mg (5 mL susp)', 'Every 12 h', '≥5 days', '—', 'Label · UK SmPC susp', '≈30/6 mg/kg/day'),
    ('med_cotrimoxazole', 'child', 9, 'Acute infections, 6–12 years', 'PO', '400/80 mg (10 mL susp)', 'Every 12 h', '≥5 days', '—', 'Label · UK SmPC susp', '≈30/6 mg/kg/day'),
    ('med_cotrimoxazole', 'child', 10, 'Pneumocystis pneumonia, treatment', 'PO', '100/20 mg/kg/day ÷ 2 or more', 'In 2+ divided doses', '14 days', '—', 'Label · UK SmPC susp', 'Aim for peak TMP ≥5 microgram/mL'),
    ('med_cotrimoxazole', 'child', 11, 'Pneumocystis pneumonia, prophylaxis', 'PO', '750/150 mg/m²/day ÷ 2', 'Every 12 h', '3 days a week or daily', '1600/320 mg/day', 'Label · UK SmPC susp', 'Age-band volumes as for acute infections'),
    ('med_cotrimoxazole', 'child', 12, 'Cerebral toxoplasmosis (≥6 weeks)', 'PO', '25/5 mg/kg', '2× a day', '4–6 weeks', '—', 'MSF 2024', ''),
    ('med_cotrimoxazole', 'child', 13, 'Typhoid fever, pertussis, brucellosis (≥6 weeks)', 'PO', '20/4 mg/kg', '2× a day', '14 days (6 weeks brucellosis)', '800/160 mg/dose', 'MSF 2024', 'Typhoid only if strain susceptible')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_cotrimoxazole');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_cotrimoxazole', 'renal', 0, 'CrCl >30', 'Usual dose.', 'Label · UK SmPC'),
    ('med_cotrimoxazole', 'renal', 1, 'CrCl 15–30', 'Half dose (800/160 mg once a day).', 'Label · UK SmPC'),
    ('med_cotrimoxazole', 'renal', 2, 'CrCl <15', 'Not recommended; no data for children ≤12 years with renal failure.', 'Label · UK SmPC'),
    ('med_cotrimoxazole', 'hepatic', 3, '', 'No dosing data; contraindicated in severe hepatic impairment.', 'Label · UK SmPC'),
    ('med_cotrimoxazole', 'elderly', 4, '', 'Standard dose with particular care (more severe reactions, especially with renal/hepatic impairment or other drugs); monthly blood counts on long courses.', 'Label · UK SmPC'),
    ('med_cotrimoxazole', 'pregnancy', 5, '', 'Folate antagonist: avoid in the first trimester unless clearly needed (give folate) and near delivery (neonatal jaundice, kernicterus risk). MSF: for Pneumocystis prophylaxis/treatment in women with HIV the benefit outweighs the risk; watch the newborn for anaemia or jaundice if used after 36 weeks.', 'MSF 2024'),
    ('med_cotrimoxazole', 'administration', 6, '', 'Take with food or drink to reduce stomach upset; drink plenty of water to prevent crystalluria. Suspension comes with a 5 mL/2.5 mL spoon.', 'Label · UK SmPC susp'),
    ('med_cotrimoxazole', 'forms_ph', 7, '', 'Tablet/capsule 400 mg + 80 mg; tablet 800 mg + 160 mg; suspension 200 mg + 40 mg/5 mL (70 mL, 120 mL) and 400 mg + 80 mg/5 mL (60 mL); injection 400 mg + 80 mg, 5 mL ampul for IV infusion.', 'PNF'),
    ('med_cotrimoxazole', 'monitor', 8, '', 'Monthly full blood count on long courses, in the elderly or folate-deficient.', 'Label · UK SmPC'),
    ('med_cotrimoxazole', 'monitor', 9, '', 'Check potassium and sodium in patients at risk of hyperkalaemia or hyponatraemia.', 'Label · UK SmPC'),
    ('med_cotrimoxazole', 'monitor', 10, '', 'Renal impairment: plasma sulfamethoxazole every 2–3 days (12 h post-dose); stop if >150 microgram/mL until <120.', 'Label · UK SmPC'),
    ('med_cotrimoxazole', 'monitor', 11, '', 'Trimethoprim can raise serum creatinine by about 10% without a true fall in GFR.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_cotrimoxazole');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_cotrimoxazole', 'Label · UK SmPC', 'UK SmPC (emc)', 'Co-Trimoxazole Forte 160/800 mg Tablets. Summary of Product Characteristics. Tillomed Laboratories Ltd; 2025.', 'https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-11466', 0),
    ('med_cotrimoxazole', 'Label · UK SmPC susp', 'UK SmPC (emc)', 'Co-Trimoxazole 40 mg/200 mg per 5 ml Paediatric Suspension. Summary of Product Characteristics. Aspen Pharma Trading Ltd; 2026.', 'https://products.mhra.gov.uk/search/?search=co-trimoxazole#emc-6994', 1),
    ('med_cotrimoxazole', 'MSF 2024', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Co-trimoxazole oral. Updated December 2024.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/co-trimoxazole-sulfamethoxazole-smx-trimethoprim-tmp-oral-16683418.html', 2),
    ('med_cotrimoxazole', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_cotrimoxazole')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_cotrimoxazole');


-- ================================================ med_dapagliflozin  (Dapagliflozin)
update public.medicines set description = 'Dapagliflozin inhibits the sodium-glucose cotransporter 2 in the proximal renal tubule, reducing glucose reabsorption and increasing urinary glucose excretion independent of insulin. It also causes natriuresis and osmotic diuresis, lowers blood pressure and reduces intraglomerular pressure. It is used for type 2 diabetes and, independent of diabetes status, to reduce cardiovascular and kidney outcomes in heart failure and chronic kidney disease. It is more than 1,400-fold selective for SGLT2 over SGLT1, has an oral bioavailability of 78% and a terminal half-life of about 12.9 hours, and is cleared mainly by UGT1A9 glucuronidation rather than CYP enzymes. Because its glucose-lowering effect depends on blood glucose and kidney function, hypoglycaemia risk on its own is low and the glucose-lowering effect fades below an eGFR of 45, while the heart and kidney benefits persist. In the Philippines, the DOH added dapagliflozin 10 mg film-coated tablet to the Philippine National Formulary in April 2023 as add-on therapy to metformin for adults with type 2 diabetes who have, or are at high risk of, cardiovascular disease or diabetic nephropathy.', updated_at = now()
where id = 'med_dapagliflozin' and description = 'Dapagliflozin inhibits the sodium-glucose cotransporter 2 in the proximal renal tubule, reducing glucose reabsorption and increasing urinary glucose excretion independent of insulin. It also causes natriuresis and osmotic diuresis, lowers blood pressure and reduces intraglomerular pressure. It is used for type 2 diabetes and, independent of diabetes status, to reduce cardiovascular and kidney outcomes in heart failure and chronic kidney disease.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); PhilHealth Advisory No. 2024-0026; DOH Department Circular 2023-0169; HTA Philippines; DailyMed (US National Library of Medicine)' else source_attribution || '; UK SmPC (emc); PhilHealth Advisory No. 2024-0026; DOH Department Circular 2023-0169; HTA Philippines; DailyMed (US National Library of Medicine)' end
where id = 'med_dapagliflozin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'indication', 'Type 2 diabetes in children aged 10 years and above (adjunct to diet and exercise)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'indication' and content = 'Type 2 diabetes in children aged 10 years and above (adjunct to diet and exercise)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'adverse', 'Dizziness, rash, back pain and dysuria (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse' and content = 'Dizziness, rash, back pain and dysuria (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'adverse', 'Increased haematocrit and dyslipidaemia (common)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse' and content = 'Increased haematocrit and dyslipidaemia (common)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'adverse', 'Thirst, dry mouth, constipation and nocturia (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse' and content = 'Thirst, dry mouth, constipation and nocturia (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'adverse', 'Transient rise in serum creatinine and fall in creatinine clearance at the start of treatment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse' and content = 'Transient rise in serum creatinine and fall in creatinine clearance at the start of treatment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'adverse', 'Angioedema and tubulointerstitial nephritis (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse' and content = 'Angioedema and tubulointerstitial nephritis (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'adverse', 'Lower-limb amputations (mainly toes) seen more often in long-term SGLT2 inhibitor studies', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'adverse' and content = 'Lower-limb amputations (mainly toes) seen more often in long-term SGLT2 inhibitor studies');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'contraindication', 'Type 1 diabetes: should not be used', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'contraindication' and content = 'Type 1 diabetes: should not be used');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'contraindication', 'Second and third trimesters of pregnancy: not recommended; stop when pregnancy is detected', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'contraindication' and content = 'Second and third trimesters of pregnancy: not recommended; stop when pregnancy is detected');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'contraindication', 'Breastfeeding: should not be used', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'contraindication' and content = 'Breastfeeding: should not be used');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'contraindication', 'Galactose intolerance, total lactase deficiency or glucose-galactose malabsorption (contains lactose; precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'contraindication' and content = 'Galactose intolerance, total lactase deficiency or glucose-galactose malabsorption (contains lactose; precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'interaction', 'Rifampicin: lowers dapagliflozin exposure (AUC −22%); no dose adjustment needed.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'interaction' and content = 'Rifampicin: lowers dapagliflozin exposure (AUC −22%); no dose adjustment needed.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'interaction', 'Mefenamic acid (UGT1A9 inhibitor): raises dapagliflozin exposure (AUC +55%); no dose adjustment needed.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'interaction' and content = 'Mefenamic acid (UGT1A9 inhibitor): raises dapagliflozin exposure (AUC +55%); no dose adjustment needed.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_dapagliflozin', 'interaction', 'No clinically relevant effect on metformin, sitagliptin, glimepiride, valsartan, digoxin or warfarin.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_dapagliflozin' and kind = 'interaction' and content = 'No clinically relevant effect on metformin, sitagliptin, glimepiride, valsartan, digoxin or warfarin.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_dapagliflozin', 'UK SmPC (emc)', 'Forxiga 10 mg film-coated tablets – Summary of Product Characteristics. AstraZeneca UK Limited. Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=dapagliflozin#emc-7607', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_dapagliflozin'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_dapagliflozin' and url = 'https://products.mhra.gov.uk/search/?search=dapagliflozin#emc-7607');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_dapagliflozin', 'PhilHealth Advisory No. 2024-0026', 'Philippine Health Insurance Corporation. Advisory No. 2024-0026: Philippine National Formulary Essential Medicines List (8th Edition) and additional medicines as of April 25, 2024. Signed May 30, 2024.', 'https://www.philhealth.gov.ph/advisories/2024/PA2024-0026.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_dapagliflozin'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_dapagliflozin' and url = 'https://www.philhealth.gov.ph/advisories/2024/PA2024-0026.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_dapagliflozin', 'DOH Department Circular 2023-0169', 'Department of Health. Secretary of Health Decision on the HTA Council Recommendation on Dapagliflozin for Type 2 Diabetes Mellitus Patients. Department Circular No. 2023-0169, 11 April 2023.', 'https://hta.dost.gov.ph/wp-content/uploads/2025/05/DOH-DC-2023-0169-SOH-Decision-on-HTAC-Recommendation-on-Dapagliflozin-for-T2DM-Patients-11-April-2023.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_dapagliflozin'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_dapagliflozin' and url = 'https://hta.dost.gov.ph/wp-content/uploads/2025/05/DOH-DC-2023-0169-SOH-Decision-on-HTAC-Recommendation-on-Dapagliflozin-for-T2DM-Patients-11-April-2023.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_dapagliflozin', 'HTA Philippines', 'Health Technology Assessment Council (Philippines). Dapagliflozin for 2nd-line treatment of type 2 diabetes mellitus: published assessment and recommendation.', 'https://hta.dost.gov.ph/published-assessment/dapagliflozin-5mg-and-10-mg-tablet-for-2nd-line-treatment-of-type-2-diabetes-mellitus-t2dm/', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_dapagliflozin'), 0)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_dapagliflozin' and url = 'https://hta.dost.gov.ph/published-assessment/dapagliflozin-5mg-and-10-mg-tablet-for-2nd-line-treatment-of-type-2-diabetes-mellitus-t2dm/');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'urinary_tract_infection', 'med_dapagliflozin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'urinary_tract_infection'), 0), 'caution'::condition_safety, 'Glucosuria raises UTI risk; consider temporarily stopping dapagliflozin while treating pyelonephritis or urosepsis (UK SmPC)'
where exists (select 1 from public.diseases where id = 'urinary_tract_infection')
  and exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'urinary_tract_infection' and medicine_id = 'med_dapagliflozin');
-- med_dapagliflozin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_dapagliflozin', 'adult', 0, 'Type 2 diabetes', 'PO', '10 mg', 'Once a day', 'Long-term', '10 mg/day', 'Label · UK SmPC', 'Consider lower insulin or sulfonylurea dose'),
    ('med_dapagliflozin', 'adult', 1, 'Type 2 diabetes (US regimen)', 'PO', '5 mg, may increase to 10 mg', 'Once a day', 'Long-term', '10 mg/day', 'Label · US', 'Not for glycaemic control if eGFR <45'),
    ('med_dapagliflozin', 'adult', 2, 'Type 2 diabetes with CVD or nephropathy (PNF, add-on to metformin)', 'PO', '10 mg', 'Once a day', 'Long-term', '10 mg/day', 'DOH 2023', 'PH government-financed indication'),
    ('med_dapagliflozin', 'adult', 3, 'Heart failure', 'PO', '10 mg', 'Once a day', 'Long-term', '10 mg/day', 'Label · UK SmPC', 'Reduced or preserved ejection fraction'),
    ('med_dapagliflozin', 'adult', 4, 'Chronic kidney disease', 'PO', '10 mg', 'Once a day', 'Long-term', '10 mg/day', 'Label · UK SmPC', 'With or without diabetes'),
    ('med_dapagliflozin', 'child', 5, 'Type 2 diabetes (≥10 y)', 'PO', '10 mg', 'Once a day', 'Long-term', '10 mg/day', 'Label · UK SmPC', 'No data under 10 y'),
    ('med_dapagliflozin', 'child', 6, 'Type 2 diabetes (≥10 y, US regimen)', 'PO', '5 mg, may increase to 10 mg', 'Once a day', 'Long-term', '10 mg/day', 'Label · US', 'HF and CKD use not established in children')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_dapagliflozin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_dapagliflozin', 'renal', 0, 'eGFR <45', 'No dose adjustment by renal function. Initiation not recommended at eGFR <15 (UK); glucose-lowering effect reduced below 45 and likely absent in severe impairment, so add another glucose-lowering drug if needed.', 'Label · UK SmPC'),
    ('med_dapagliflozin', 'hepatic', 1, '', 'No adjustment in mild or moderate impairment. Severe impairment: start 5 mg once a day, increase to 10 mg if tolerated.', 'Label · UK SmPC'),
    ('med_dapagliflozin', 'elderly', 2, '', 'No dose adjustment by age; take extra care with volume depletion and hypotension.', 'Label · UK SmPC'),
    ('med_dapagliflozin', 'pregnancy', 3, '', 'Not recommended in the 2nd and 3rd trimesters (kidney toxicity in rats); stop when pregnancy is detected. Do not use while breastfeeding.', 'Label · UK SmPC'),
    ('med_dapagliflozin', 'administration', 4, '', 'Once a day at any time, with or without food; swallow whole. Correct volume depletion before starting.', 'Label · UK SmPC'),
    ('med_dapagliflozin', 'monitor', 5, '', 'Kidney function before starting and as needed; volume status and blood pressure; ketones (blood preferred) if unwell or around surgery, even with normal glucose; genital or perineal pain with fever (Fournier''s); foot care; haematocrit.', 'Label · UK SmPC'),
    ('med_dapagliflozin', 'forms_ph', 6, '', 'Oral: 10 mg film-coated tablet (added to the PNF on 11 April 2023 via DOH-DC No. 2023-0169).', 'PNF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_dapagliflozin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_dapagliflozin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Forxiga 10 mg film-coated tablets – SmPC. AstraZeneca UK Limited. emc.', 'https://products.mhra.gov.uk/search/?search=dapagliflozin#emc-7607', 0),
    ('med_dapagliflozin', 'Label · US', 'DailyMed (US National Library of Medicine)', 'FARXIGA (dapagliflozin) tablets. Prescribing information. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=72ad22ae-efe6-4cd6-a302-98aaee423d69', 1),
    ('med_dapagliflozin', 'PNF', 'PhilHealth Advisory No. 2024-0026', 'PhilHealth Advisory No. 2024-0026: PNF EML 8th Edition and medicines added as of April 25, 2024 (dapagliflozin added via DOH-DC No. 2023-0169).', 'https://www.philhealth.gov.ph/advisories/2024/PA2024-0026.pdf', 2),
    ('med_dapagliflozin', 'DOH 2023', 'DOH Department Circular 2023-0169', 'DOH DC No. 2023-0169: SOH Decision on HTAC Recommendation on Dapagliflozin for T2DM Patients, 11 April 2023.', 'https://hta.dost.gov.ph/wp-content/uploads/2025/05/DOH-DC-2023-0169-SOH-Decision-on-HTAC-Recommendation-on-Dapagliflozin-for-T2DM-Patients-11-April-2023.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_dapagliflozin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_dapagliflozin');


update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
