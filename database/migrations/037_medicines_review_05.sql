-- 037_medicines_review_05.sql  -  medicine review b05: med_nirmatrelvir_ritonavir, med_nitrofurantoin, med_omeprazole, med_ors, med_oseltamivir, med_paracetamol, med_permethrin, med_praziquantel, med_prednisone, med_propranolol
-- Adds only: longer descriptions, new facts, references, disease links, and dosage
-- tables (for medicines that have none yet). Nothing is deleted or reworded.
-- Needs 030_medicine_doses.sql first. Safe to run twice (every insert is guarded).

begin;

-- ================================================ med_nirmatrelvir_ritonavir  (Nirmatrelvir + Ritonavir)
update public.medicines set description = 'Nirmatrelvir inhibits the SARS-CoV-2 main protease (Mpro), preventing viral polyprotein processing and replication. Ritonavir is a strong CYP3A inhibitor with no meaningful SARS-CoV-2 activity that is co-administered to raise nirmatrelvir plasma concentrations. It is used for mild-to-moderate COVID-19 in non-hospitalized patients at high risk of progression, started within 5 days of symptom onset. WHO strongly recommends it for non-severe COVID-19 in patients at highest risk of hospitalisation (such as unvaccinated, older or immunosuppressed people), where it cut hospitalisation by about 85%, but not for lower-risk patients, in whom the benefit was negligible. Because it only works early in the illness, prompt testing is essential to its use.', updated_at = now()
where id = 'med_nirmatrelvir_ritonavir' and description = 'Nirmatrelvir inhibits the SARS-CoV-2 main protease (Mpro), preventing viral polyprotein processing and replication. Ritonavir is a strong CYP3A inhibitor with no meaningful SARS-CoV-2 activity that is co-administered to raise nirmatrelvir plasma concentrations. It is used for mild-to-moderate COVID-19 in non-hospitalized patients at high risk of progression, started within 5 days of symptom onset.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); World Health Organization' else source_attribution || '; UK SmPC (emc); World Health Organization' end
where id = 'med_nirmatrelvir_ritonavir' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'indication', 'Severely immunocompromised patients: a 10-day course may be considered to reduce virological rebound (limited data)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'indication' and content = 'Severely immunocompromised patients: a 10-day course may be considered to reduce virological rebound (limited data)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'adverse', 'Headache, nausea', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'adverse' and content = 'Headache, nausea');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'adverse', 'Vomiting, abdominal pain (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'adverse' and content = 'Vomiting, abdominal pain (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'adverse', 'Malaise (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'adverse' and content = 'Malaise (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'contraindication', 'Severe hepatic impairment (Child-Pugh C)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication' and content = 'Severe hepatic impairment (Child-Pugh C)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'contraindication', 'Co-administration with colchicine (life-threatening and fatal interactions reported)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication' and content = 'Co-administration with colchicine (life-threatening and fatal interactions reported)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'contraindication', 'Co-administration with quetiapine, lurasidone, pimozide, triazolam or oral midazolam', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication' and content = 'Co-administration with quetiapine, lurasidone, pimozide, triazolam or oral midazolam');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'contraindication', 'Co-administration with alfuzosin, ranolazine, ivabradine, eplerenone, finerenone, tolvaptan or ergot derivatives', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication' and content = 'Co-administration with alfuzosin, ranolazine, ivabradine, eplerenone, finerenone, tolvaptan or ergot derivatives');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'contraindication', 'Sildenafil when used for pulmonary arterial hypertension', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'contraindication' and content = 'Sildenafil when used for pulmonary arterial hypertension');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'interaction', 'Combined hormonal contraceptives: ethinylestradiol exposure falls about 40%; use barrier/non-hormonal contraception during treatment and for one menstrual cycle after.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction' and content = 'Combined hormonal contraceptives: ethinylestradiol exposure falls about 40%; use barrier/non-hormonal contraception during treatment and for one menstrual cycle after.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'interaction', 'Sildenafil/tadalafil for erectile dysfunction: limit sildenafil to 25 mg per 48 h and tadalafil to 10 mg per 72 h.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction' and content = 'Sildenafil/tadalafil for erectile dysfunction: limit sildenafil to 25 mg per 48 h and tadalafil to 10 mg per 72 h.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'interaction', 'Salmeterol: avoid (large rise in exposure).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction' and content = 'Salmeterol: avoid (large rise in exposure).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'interaction', 'Rivaroxaban: not recommended with ritonavir.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction' and content = 'Rivaroxaban: not recommended with ritonavir.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'interaction', 'Atorvastatin/rosuvastatin: consider pausing; pravastatin or fluvastatin preferred if a statin is needed.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction' and content = 'Atorvastatin/rosuvastatin: consider pausing; pravastatin or fluvastatin preferred if a statin is needed.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'interaction', 'Levothyroxine: monitor TSH for at least the first month after starting or stopping ritonavir.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction' and content = 'Levothyroxine: monitor TSH for at least the first month after starting or stopping ritonavir.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nirmatrelvir_ritonavir', 'interaction', 'Parenteral midazolam: only in an ICU-type setting with close monitoring.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nirmatrelvir_ritonavir' and kind = 'interaction' and content = 'Parenteral midazolam: only in an ICU-type setting with close monitoring.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_nirmatrelvir_ritonavir', 'UK SmPC (emc)', 'Paxlovid 150 mg/100 mg film-coated tablets. Summary of Product Characteristics. Pfizer Ltd; revised 15 September 2026. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=nirmatrelvir#emc-13145', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_nirmatrelvir_ritonavir'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_nirmatrelvir_ritonavir' and url = 'https://products.mhra.gov.uk/search/?search=nirmatrelvir#emc-13145');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_nirmatrelvir_ritonavir', 'World Health Organization', 'WHO recommends highly successful COVID-19 therapy and calls for wide geographical distribution and transparency from originator. WHO news release, 22 April 2022.', 'https://www.who.int/news/item/22-04-2022-who-recommends-highly-successful-covid-19-therapy-and-calls-for-wide-geographical-distribution-and-transparency-from-originator', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_nirmatrelvir_ritonavir'), 0)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_nirmatrelvir_ritonavir' and url = 'https://www.who.int/news/item/22-04-2022-who-recommends-highly-successful-covid-19-therapy-and-calls-for-wide-geographical-distribution-and-transparency-from-originator');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_nirmatrelvir_ritonavir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'caution'::condition_safety, 'Risk of HIV-1 protease inhibitor resistance in uncontrolled or undiagnosed HIV; patients already on ritonavir/cobicistat regimens need no dose change (UK SmPC).'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_nirmatrelvir_ritonavir');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'gout', 'med_nirmatrelvir_ritonavir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'gout'), 0), 'caution'::condition_safety, 'Colchicine is contraindicated with it (fatal interactions reported); review gout medicines before starting (UK SmPC).'
where exists (select 1 from public.diseases where id = 'gout')
  and exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'gout' and medicine_id = 'med_nirmatrelvir_ritonavir');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'tuberculosis', 'med_nirmatrelvir_ritonavir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'tuberculosis'), 0), 'caution'::condition_safety, 'Contraindicated with rifampicin or rifapentine (loss of antiviral effect, resistance), so patients on rifamycin-based TB treatment should not take it (UK SmPC).'
where exists (select 1 from public.diseases where id = 'tuberculosis')
  and exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'tuberculosis' and medicine_id = 'med_nirmatrelvir_ritonavir');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_nirmatrelvir_ritonavir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'Several heart-failure and antiarrhythmic drugs are contraindicated with it (amiodarone, dronedarone, eplerenone, ivabradine, finerenone, tolvaptan); our inference from the SmPC interaction list.'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_nirmatrelvir_ritonavir');
-- med_nirmatrelvir_ritonavir
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_nirmatrelvir_ritonavir', 'adult', 0, 'COVID-19, high risk (eGFR ≥60)', 'PO', 'Nirmatrelvir 300 mg + ritonavir 100 mg', 'Every 12 h', '5 days', '—', 'Label · UK SmPC', 'Start within 5 days of symptoms'),
    ('med_nirmatrelvir_ritonavir', 'adult', 1, 'COVID-19, eGFR 30–59', 'PO', 'Nirmatrelvir 150 mg + ritonavir 100 mg', 'Every 12 h', '5 days', '—', 'Label · UK SmPC', ''),
    ('med_nirmatrelvir_ritonavir', 'adult', 2, 'COVID-19, eGFR <30 or haemodialysis', 'PO', '300/100 mg day 1, then 150/100 mg', 'Once a day', '5 days', '—', 'Label · UK SmPC', 'Give after dialysis on HD days'),
    ('med_nirmatrelvir_ritonavir', 'adult', 3, 'COVID-19, severely immunocompromised', 'PO', 'Nirmatrelvir 300 mg + ritonavir 100 mg', 'Every 12 h', '10 days', '—', 'Label · UK SmPC', 'May reduce rebound; limited data')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_nirmatrelvir_ritonavir');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_nirmatrelvir_ritonavir', 'renal', 0, 'eGFR ≥60', 'No dose adjustment.', 'Label · UK SmPC'),
    ('med_nirmatrelvir_ritonavir', 'renal', 1, 'eGFR 30–59', 'Nirmatrelvir 150 mg + ritonavir 100 mg twice daily for 5 days.', 'Label · UK SmPC'),
    ('med_nirmatrelvir_ritonavir', 'renal', 2, 'eGFR <30 / HD', '300/100 mg once on day 1, then 150/100 mg once daily on days 2–5; after haemodialysis on dialysis days. Discard extra tablets in the pack.', 'Label · UK SmPC'),
    ('med_nirmatrelvir_ritonavir', 'hepatic', 3, '', 'No adjustment in Child-Pugh A or B; contraindicated in Child-Pugh C. Use with caution in pre-existing liver disease or raised liver enzymes.', 'Label · UK SmPC'),
    ('med_nirmatrelvir_ritonavir', 'elderly', 4, '', 'No dose adjustment. Not established under 18 years.', 'Label · UK SmPC'),
    ('med_nirmatrelvir_ritonavir', 'pregnancy', 5, '', 'Use in pregnancy only if benefit outweighs risk (limited human data). Stop breastfeeding during treatment and for 48 h after the last dose.', 'Label · UK SmPC'),
    ('med_nirmatrelvir_ritonavir', 'administration', 6, '', 'Take the 3 tablets together, with or without food; swallow whole, do not chew, break or crush. Missed dose: take if ≤8 h late, otherwise skip. If hospitalised after starting, the 5-day course may be completed.', 'Label · UK SmPC'),
    ('med_nirmatrelvir_ritonavir', 'monitor', 7, '', 'Review every concomitant medicine (including herbal St John''s wort) before and during treatment; stop lovastatin/simvastatin ≥12 h before, during and for 5 days after.', 'Label · UK SmPC'),
    ('med_nirmatrelvir_ritonavir', 'monitor', 8, '', 'Check tacrolimus/ciclosporin/sirolimus levels closely with specialist input; check INR on warfarin.', 'Label · UK SmPC'),
    ('med_nirmatrelvir_ritonavir', 'monitor', 9, '', 'Stop at signs of anaphylaxis or severe skin reaction; check liver tests if hepatitis symptoms appear.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_nirmatrelvir_ritonavir');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_nirmatrelvir_ritonavir', 'Label · UK SmPC', 'UK SmPC (emc)', 'Paxlovid 150 mg/100 mg film-coated tablets. Summary of Product Characteristics. Pfizer Ltd; 15 September 2026.', 'https://products.mhra.gov.uk/search/?search=nirmatrelvir#emc-13145', 0),
    ('med_nirmatrelvir_ritonavir', 'WHO 2022', 'World Health Organization', 'WHO recommends highly successful COVID-19 therapy... WHO news release, 22 April 2022.', 'https://www.who.int/news/item/22-04-2022-who-recommends-highly-successful-covid-19-therapy-and-calls-for-wide-geographical-distribution-and-transparency-from-originator', 1)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_nirmatrelvir_ritonavir')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_nirmatrelvir_ritonavir');


-- ================================================ med_nitrofurantoin  (Nitrofurantoin)
update public.medicines set description = 'Nitrofurantoin is reduced by bacterial flavoproteins to reactive intermediates that damage ribosomal proteins, DNA and other macromolecules, giving it multiple targets and low resistance rates. It concentrates in urine with low serum levels and is used for uncomplicated lower urinary tract infection (cystitis), not pyelonephritis. WHO lists it as an Access-group antibiotic and a first-choice option for infectious cystitis, as 50 mg and 100 mg oral solids and a 25 mg/5 mL oral liquid. MSF keeps it for uncomplicated cystitis without fever or flank pain when no other antibiotic can be used.', updated_at = now()
where id = 'med_nitrofurantoin' and description = 'Nitrofurantoin is reduced by bacterial flavoproteins to reactive intermediates that damage ribosomal proteins, DNA and other macromolecules, giving it multiple targets and low resistance rates. It concentrates in urine with low serum levels and is used for uncomplicated lower urinary tract infection (cystitis), not pyelonephritis.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; WHO eEML; PhilHealth Konsulta medicines list (Annex D2)' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; WHO eEML; PhilHealth Konsulta medicines list (Annex D2)' end
where id = 'med_nitrofurantoin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'indication', 'Prophylaxis around urological surgery (during the procedure and for 3 days after)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'indication' and content = 'Prophylaxis around urological surgery (during the procedure and for 3 days after)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'adverse', 'Dizziness and drowsiness (avoid driving if affected)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse' and content = 'Dizziness and drowsiness (avoid driving if affected)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'adverse', 'Aplastic anaemia (rare), agranulocytosis, thrombocytopenia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse' and content = 'Aplastic anaemia (rare), agranulocytosis, thrombocytopenia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'adverse', 'DRESS and Stevens-Johnson syndrome', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse' and content = 'DRESS and Stevens-Johnson syndrome');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'adverse', 'Benign intracranial hypertension', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse' and content = 'Benign intracranial hypertension');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'adverse', 'Pancreatitis and interstitial nephritis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse' and content = 'Pancreatitis and interstitial nephritis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'adverse', 'Psychiatric reactions', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse' and content = 'Psychiatric reactions');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'adverse', 'False-positive urine glucose tests', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'adverse' and content = 'False-positive urine glucose tests');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'contraindication', 'eGFR below 45 mL/min (UK SmPC threshold)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'contraindication' and content = 'eGFR below 45 mL/min (UK SmPC threshold)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'contraindication', 'G6PD deficiency', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'contraindication' and content = 'G6PD deficiency');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'contraindication', 'Acute porphyria', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'contraindication' and content = 'Acute porphyria');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'contraindication', 'Infants under 3 months (UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'contraindication' and content = 'Infants under 3 months (UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'interaction', 'Quinolone antibiotics: antagonise its antibacterial effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction' and content = 'Quinolone antibiotics: antagonise its antibacterial effect.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'interaction', 'Carbonic anhydrase inhibitors and urine alkalinisers: reduce antibacterial activity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction' and content = 'Carbonic anhydrase inhibitors and urine alkalinisers: reduce antibacterial activity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'interaction', 'Food or drugs that delay gastric emptying: increase absorption.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction' and content = 'Food or drugs that delay gastric emptying: increase absorption.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'interaction', 'Aluminium/magnesium hydroxide antacids: separate doses by at least 2 hours.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction' and content = 'Aluminium/magnesium hydroxide antacids: separate doses by at least 2 hours.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_nitrofurantoin', 'interaction', 'Oral typhoid vaccine: inactivated by antibacterials.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_nitrofurantoin' and kind = 'interaction' and content = 'Oral typhoid vaccine: inactivated by antibacterials.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_nitrofurantoin', 'UK SmPC (emc)', 'Macrodantin / Nitrofurantoin 100 mg Capsules, Hard (macrocrystals). Summary of Product Characteristics. Mercury Pharmaceuticals (ADVANZ Pharma); updated August 2025. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-428', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_nitrofurantoin'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_nitrofurantoin' and url = 'https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-428');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_nitrofurantoin', 'UK SmPC (emc)', 'Nitrofurantoin Mercury Pharma 100 mg Prolonged-Release Capsules (MacroBID). Summary of Product Characteristics. ADVANZ Pharma; updated August 2025. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-15362', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_nitrofurantoin'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_nitrofurantoin' and url = 'https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-15362');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_nitrofurantoin', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Nitrofurantoin oral. MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/nitrofurantoin-oral-16684353.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_nitrofurantoin'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_nitrofurantoin' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/nitrofurantoin-oral-16684353.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_nitrofurantoin', 'WHO eEML', 'World Health Organization. Electronic Essential Medicines List – Nitrofurantoin (Access group antibiotic).', 'https://list.essentialmeds.org/medicines/301', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_nitrofurantoin'), 0)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_nitrofurantoin' and url = 'https://list.essentialmeds.org/medicines/301');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_nitrofurantoin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'SmPC advises caution in diabetes, which raises the risk of peripheral neuropathy.'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_nitrofurantoin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'iron_deficiency_anemia', 'med_nitrofurantoin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'iron_deficiency_anemia'), 0), 'caution'::condition_safety, 'SmPC advises caution in anaemia (stated for anaemia in general, not iron deficiency specifically).'
where exists (select 1 from public.diseases where id = 'iron_deficiency_anemia')
  and exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'iron_deficiency_anemia' and medicine_id = 'med_nitrofurantoin');
-- med_nitrofurantoin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_nitrofurantoin', 'adult', 0, 'Acute uncomplicated lower UTI (macrocrystals)', 'PO', '50 mg', '4× a day', '7 days', '—', 'Label · UK SmPC', ''),
    ('med_nitrofurantoin', 'adult', 1, 'Severe chronic recurrent UTI (macrocrystals)', 'PO', '100 mg', '4× a day', '7 days', '—', 'Label · UK SmPC', ''),
    ('med_nitrofurantoin', 'adult', 2, 'Acute or recurrent lower UTI (prolonged-release, ≥12 y)', 'PO', '100 mg', '2× a day', '7 days', '—', 'Label · UK SmPC MR', ''),
    ('med_nitrofurantoin', 'adult', 3, 'Uncomplicated cystitis (100 mg tablet)', 'PO', '100 mg', 'Every 8 h', '5–7 days', '—', 'MSF', 'Only if no other antibiotic can be used'),
    ('med_nitrofurantoin', 'adult', 4, 'Long-term suppression', 'PO', '50–100 mg', 'Once a day', 'Long-term', '—', 'Label · UK SmPC', ''),
    ('med_nitrofurantoin', 'adult', 5, 'Surgical prophylaxis (macrocrystals)', 'PO', '50 mg', '4× a day', 'Procedure + 3 days', '—', 'Label · UK SmPC', ''),
    ('med_nitrofurantoin', 'adult', 6, 'Surgical prophylaxis (prolonged-release)', 'PO', '100 mg', '2× a day', 'Day of procedure + 3 days', '—', 'Label · UK SmPC MR', ''),
    ('med_nitrofurantoin', 'child', 7, 'Acute UTI (>3 mo)', 'PO', '3 mg/kg/day ÷ 4', '4× a day', '7 days', '—', 'Label · UK SmPC', 'Under 25 kg: consider suspension'),
    ('med_nitrofurantoin', 'child', 8, 'Suppression (>3 mo)', 'PO', '1 mg/kg', 'Once a day', 'Long-term', '—', 'Label · UK SmPC', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_nitrofurantoin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_nitrofurantoin', 'forms_ph', 0, '', 'Nitrofurantoin (as macrocrystals) 50 mg and 100 mg capsules (PhilHealth Konsulta medicines list).', 'PhilHealth Konsulta'),
    ('med_nitrofurantoin', 'renal', 1, 'eGFR <45', 'Contraindicated.', 'Label · UK SmPC'),
    ('med_nitrofurantoin', 'renal', 2, 'eGFR 30–44', 'Short course only, for uncomplicated lower UTI with resistant organisms when benefit outweighs risk.', 'Label · UK SmPC'),
    ('med_nitrofurantoin', 'hepatic', 3, '', 'Rare but potentially fatal hepatitis; use with caution in liver disease.', 'Label · UK SmPC'),
    ('med_nitrofurantoin', 'elderly', 4, '', 'Normal adult dose if no significant renal impairment; pulmonary reactions more common in the elderly and with long-term use.', 'Label · UK SmPC'),
    ('med_nitrofurantoin', 'pregnancy', 5, '', 'Use the lowest effective dose after careful assessment; contraindicated at term (newborn haemolysis). Breastfeeding: avoid if the infant has G6PD or other red-cell enzyme deficiency; MSF advises avoiding in the first month.', 'Label · UK SmPC'),
    ('med_nitrofurantoin', 'administration', 6, '', 'Take with food or milk (improves absorption). Prolonged-release capsules are not suitable under 12 years.', 'Label · UK SmPC'),
    ('med_nitrofurantoin', 'monitor', 7, '', 'Check liver tests periodically on long-term treatment.', 'Label · UK SmPC'),
    ('med_nitrofurantoin', 'monitor', 8, '', 'Stop at first sign of paraesthesia (neuropathy), new cough/dyspnoea (pulmonary reaction) or haemolysis.', 'Label · UK SmPC'),
    ('med_nitrofurantoin', 'monitor', 9, '', 'Recurrent or severe cases: exclude a surgical cause or a non-functioning kidney.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_nitrofurantoin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_nitrofurantoin', 'PhilHealth Konsulta', 'PhilHealth Konsulta medicines list (Annex D2)', 'Philippine Health Insurance Corporation. Konsulta package: Certification of Service Delivery Support (Medicines), Annex D2.', 'https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf', 0),
    ('med_nitrofurantoin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Macrodantin / Nitrofurantoin 100 mg Capsules (macrocrystals). SmPC. ADVANZ Pharma; August 2025.', 'https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-428', 1),
    ('med_nitrofurantoin', 'Label · UK SmPC MR', 'UK SmPC (emc)', 'Nitrofurantoin 100 mg Prolonged-Release Capsules (MacroBID). SmPC. ADVANZ Pharma; August 2025.', 'https://products.mhra.gov.uk/search/?search=nitrofurantoin#emc-15362', 2),
    ('med_nitrofurantoin', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Nitrofurantoin oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/nitrofurantoin-oral-16684353.html', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_nitrofurantoin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_nitrofurantoin');


-- ================================================ med_omeprazole  (Omeprazole)
update public.medicines set description = 'Omeprazole irreversibly inhibits the parietal cell H+/K+-ATPase (proton pump), the final step of gastric acid secretion. Onset is within about an hour and acid suppression persists for up to 72 hours because new pumps must be synthesized. It is used for peptic ulcer disease, GERD and erosive esophagitis, Helicobacter pylori eradication regimens and hypersecretory states such as Zollinger-Ellison syndrome. WHO keeps omeprazole on the Essential Medicines List as an antiulcer medicine for GERD, peptic ulcer and gastrointestinal bleeding, in oral (10, 20, 40 mg; oral liquid) and 40 mg IV forms. The UK label also licenses it to treat and prevent NSAID-associated ulcers and, in children from 1 year (at least 10 kg), for reflux oesophagitis.', updated_at = now()
where id = 'med_omeprazole' and description = 'Omeprazole irreversibly inhibits the parietal cell H+/K+-ATPase (proton pump), the final step of gastric acid secretion. Onset is within about an hour and acid suppression persists for up to 72 hours because new pumps must be synthesized. It is used for peptic ulcer disease, GERD and erosive esophagitis, Helicobacter pylori eradication regimens and hypersecretory states such as Zollinger-Ellison syndrome.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; WHO eEML' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; WHO eEML' end
where id = 'med_omeprazole' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'indication', 'Treatment of NSAID-associated gastric and duodenal ulcers, and prevention in at-risk patients (over 60, previous ulcer or upper GI bleed)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'indication' and content = 'Treatment of NSAID-associated gastric and duodenal ulcers, and prevention in at-risk patients (over 60, previous ulcer or upper GI bleed)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'indication', 'Children from 1 year and at least 10 kg: reflux oesophagitis and symptomatic GERD', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'indication' and content = 'Children from 1 year and at least 10 kg: reflux oesophagitis and symptomatic GERD');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'indication', 'Children over 4 years: H. pylori-associated duodenal ulcer (with antibiotics, specialist-supervised)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'indication' and content = 'Children over 4 years: H. pylori-associated duodenal ulcer (with antibiotics, specialist-supervised)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Constipation', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Constipation');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Dizziness, paraesthesia, somnolence, insomnia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Dizziness, paraesthesia, somnolence, insomnia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Hyponatraemia (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Hyponatraemia (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Blurred vision and taste disturbance (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Blurred vision and taste disturbance (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Hepatitis with or without jaundice (rare); hepatic encephalopathy in pre-existing liver disease (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Hepatitis with or without jaundice (rare); hepatic encephalopathy in pre-existing liver disease (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Microscopic colitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Microscopic colitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Severe skin reactions: SJS, TEN, DRESS, AGEP', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Severe skin reactions: SJS, TEN, DRESS, AGEP');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Leukopenia, thrombocytopenia (rare); agranulocytosis, pancytopenia (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Leukopenia, thrombocytopenia (rare); agranulocytosis, pancytopenia (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Gynaecomastia (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Gynaecomastia (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'adverse', 'Slightly increased risk of Salmonella and Campylobacter gut infections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'adverse' and content = 'Slightly increased risk of Salmonella and Campylobacter gut infections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'contraindication', 'Co-administration with nelfinavir', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'contraindication' and content = 'Co-administration with nelfinavir');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'interaction', 'Atazanavir: exposure markedly reduced; not recommended (if unavoidable, atazanavir/ritonavir 400/100 mg and omeprazole no more than 20 mg).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction' and content = 'Atazanavir: exposure markedly reduced; not recommended (if unavoidable, atazanavir/ritonavir 400/100 mg and omeprazole no more than 20 mg).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'interaction', 'Posaconazole, erlotinib, ketoconazole and itraconazole: absorption reduced by the higher gastric pH.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction' and content = 'Posaconazole, erlotinib, ketoconazole and itraconazole: absorption reduced by the higher gastric pH.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'interaction', 'Phenytoin, diazepam and cilostazol: levels may rise (CYP2C19); monitor phenytoin in the first 2 weeks and after stopping.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction' and content = 'Phenytoin, diazepam and cilostazol: levels may rise (CYP2C19); monitor phenytoin in the first 2 weeks and after stopping.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'interaction', 'Digoxin: bioavailability rises about 10%; take care at high doses in the elderly.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction' and content = 'Digoxin: bioavailability rises about 10%; take care at high doses in the elderly.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'interaction', 'Saquinavir/ritonavir: saquinavir levels raised up to about 70%.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction' and content = 'Saquinavir/ritonavir: saquinavir levels raised up to about 70%.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'interaction', 'Voriconazole and clarithromycin: raise omeprazole exposure (voriconazole more than doubles it).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction' and content = 'Voriconazole and clarithromycin: raise omeprazole exposure (voriconazole more than doubles it).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_omeprazole', 'interaction', 'Chromogranin A tests: stop omeprazole at least 5 days before testing (falsely raised CgA).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_omeprazole' and kind = 'interaction' and content = 'Chromogranin A tests: stop omeprazole at least 5 days before testing (falsely raised CgA).');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_omeprazole', 'UK SmPC (emc)', 'Omeprazole 20 mg gastro-resistant capsules, hard. Summary of Product Characteristics. Zentiva Pharma UK Ltd; revised August 2025. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=omeprazole#emc-15127', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_omeprazole'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_omeprazole' and url = 'https://products.mhra.gov.uk/search/?search=omeprazole#emc-15127');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_omeprazole', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Omeprazole oral. MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/omeprazole-oral-16684375.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_omeprazole'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_omeprazole' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/omeprazole-oral-16684375.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_omeprazole', 'WHO eEML', 'World Health Organization. Electronic Essential Medicines List – Omeprazole (antiulcer medicines).', 'https://list.essentialmeds.org/medicines/178', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_omeprazole'), 0)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_omeprazole' and url = 'https://list.essentialmeds.org/medicines/178');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_omeprazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'caution'::condition_safety, 'Contraindicated with nelfinavir and not recommended with atazanavir (UK SmPC); check the antiretroviral regimen.'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_omeprazole');
-- med_omeprazole
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_omeprazole', 'adult', 0, 'Duodenal ulcer', 'PO', '20 mg', 'Once a day', '2–4 weeks', '40 mg/day in poor responders', 'Label · UK SmPC', ''),
    ('med_omeprazole', 'adult', 1, 'Gastric ulcer', 'PO', '20 mg', 'Once a day', '4–8 weeks', '40 mg/day in poor responders', 'Label · UK SmPC', ''),
    ('med_omeprazole', 'adult', 2, 'Ulcer relapse prevention', 'PO', '10–20 mg', 'Once a day', 'Long-term', '40 mg/day', 'Label · UK SmPC', 'H. pylori-negative or eradication not possible'),
    ('med_omeprazole', 'adult', 3, 'H. pylori eradication (with clarithromycin + amoxicillin or metronidazole)', 'PO', '20 mg', '2× a day', '7 days', '—', 'Label · UK SmPC', 'Choose antibiotics by local resistance; repeat if still positive'),
    ('med_omeprazole', 'adult', 4, 'NSAID-associated ulcer, treatment', 'PO', '20 mg', 'Once a day', '4–8 weeks', '—', 'Label · UK SmPC', ''),
    ('med_omeprazole', 'adult', 5, 'NSAID-associated ulcer, prevention (at-risk)', 'PO', '20 mg', 'Once a day', 'While on NSAID', '—', 'Label · UK SmPC', ''),
    ('med_omeprazole', 'adult', 6, 'Reflux oesophagitis', 'PO', '20 mg', 'Once a day', '4–8 weeks', '40 mg/day if severe', 'Label · UK SmPC', ''),
    ('med_omeprazole', 'adult', 7, 'Healed reflux oesophagitis, maintenance', 'PO', '10 mg', 'Once a day', 'Long-term', '20–40 mg/day', 'Label · UK SmPC', ''),
    ('med_omeprazole', 'adult', 8, 'Symptomatic GERD', 'PO', '10–20 mg', 'Once a day', '4 weeks', '—', 'Label · UK SmPC', 'Investigate if not controlled after 4 weeks'),
    ('med_omeprazole', 'adult', 9, 'Zollinger-Ellison syndrome', 'PO', '60 mg initially', 'Once a day', 'As needed', 'Usual 20–120 mg/day', 'Label · UK SmPC', 'Split doses above 80 mg/day into 2'),
    ('med_omeprazole', 'child', 10, 'Reflux oesophagitis / GERD (≥1 y, 10–20 kg)', 'PO', '10 mg', 'Once a day', '4–8 weeks (GERD symptoms 2–4 weeks)', '20 mg/day', 'Label · UK SmPC', ''),
    ('med_omeprazole', 'child', 11, 'Reflux oesophagitis / GERD (≥2 y, >20 kg)', 'PO', '20 mg', 'Once a day', '4–8 weeks (GERD symptoms 2–4 weeks)', '40 mg/day', 'Label · UK SmPC', ''),
    ('med_omeprazole', 'child', 12, 'GERD (<5 kg)', 'PO', '0.7–1.4 mg/kg', 'Once a day', '3 days–8 weeks', '2.8 mg/kg/day', 'MSF', 'From dispersible 10 mg tablet as 1 mg/mL'),
    ('med_omeprazole', 'child', 13, 'GERD (5–10 kg)', 'PO', '5 mg', 'Once a day', '3 days–8 weeks', '—', 'MSF', ''),
    ('med_omeprazole', 'child', 14, 'H. pylori duodenal ulcer (>4 y, 15–30 kg)', 'PO', '10 mg', '2× a day', '7 days (up to 14)', '—', 'Label · UK SmPC', 'With amoxicillin 25 mg/kg + clarithromycin 7.5 mg/kg 2× a day'),
    ('med_omeprazole', 'child', 15, 'H. pylori duodenal ulcer (>4 y, 31–40 kg)', 'PO', '20 mg', '2× a day', '7 days (up to 14)', '—', 'Label · UK SmPC', 'With amoxicillin 750 mg + clarithromycin 7.5 mg/kg 2× a day'),
    ('med_omeprazole', 'child', 16, 'H. pylori duodenal ulcer (>4 y, >40 kg)', 'PO', '20 mg', '2× a day', '7 days (up to 14)', '—', 'Label · UK SmPC', 'With amoxicillin 1 g + clarithromycin 500 mg 2× a day')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_omeprazole');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_omeprazole', 'renal', 0, '', 'No dose adjustment needed.', 'Label · UK SmPC'),
    ('med_omeprazole', 'hepatic', 1, '', '10–20 mg daily may be sufficient.', 'Label · UK SmPC'),
    ('med_omeprazole', 'hepatic', 2, 'Severe', 'Severe hepatic impairment: do not exceed 0.7 mg/kg daily (max 20 mg daily).', 'MSF'),
    ('med_omeprazole', 'elderly', 3, '', 'No dose adjustment needed.', 'Label · UK SmPC'),
    ('med_omeprazole', 'pregnancy', 4, '', 'Over 1,000 exposed pregnancies showed no adverse effects; can be used in pregnancy. Passes into breast milk but unlikely to affect the infant at therapeutic doses.', 'Label · UK SmPC'),
    ('med_omeprazole', 'administration', 5, '', 'Take in the morning, swallowed whole with half a glass of water; do not chew or crush. If swallowing is difficult, open the capsule and mix the pellets with water or a slightly acidic liquid (fruit juice, applesauce); take within 30 minutes.', 'Label · UK SmPC'),
    ('med_omeprazole', 'monitor', 6, '', 'Exclude malignancy first if there are alarm features (weight loss, recurrent vomiting, dysphagia, haematemesis, melaena).', 'Label · UK SmPC'),
    ('med_omeprazole', 'monitor', 7, '', 'Long-term use (especially beyond 1 year): review regularly; consider magnesium levels (more so with digoxin or diuretics), vitamin B12, and calcium/vitamin D in patients at fracture risk.', 'Label · UK SmPC'),
    ('med_omeprazole', 'monitor', 8, '', 'Stop if acute tubulointerstitial nephritis is suspected, or if SCLE-type skin lesions with joint pain appear.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_omeprazole');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_omeprazole', 'Label · UK SmPC', 'UK SmPC (emc)', 'Omeprazole 20 mg gastro-resistant capsules. SmPC. Zentiva; August 2025.', 'https://products.mhra.gov.uk/search/?search=omeprazole#emc-15127', 0),
    ('med_omeprazole', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Omeprazole oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/omeprazole-oral-16684375.html', 1)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_omeprazole')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_omeprazole');


-- ================================================ med_ors  (Oral Rehydration Salts (reduced osmolarity))
update public.medicines set description = 'Reduced-osmolarity ORS (245 mOsm/L) contains glucose and sodium in equimolar amounts (75 mmol/L each), exploiting sodium-glucose co-transport in the small intestine to drive water absorption even during secretory diarrhea. It also replaces potassium and corrects acidosis with citrate. Compared with the older standard ORS it reduces stool output, vomiting and the need for unscheduled IV therapy; it is the cornerstone of treatment for dehydration from acute diarrhea. In the Philippines, PhilHealth''s quality policy on acute infectious gastroenteritis names ORS and IV fluids as the standard treatment for dehydration, with routine zinc 20 mg/day for 10–14 days as an adjunct in children. The Philippine Society for Pediatric Gastroenterology, Hepatology and Nutrition (PSPGHAN, 2026) recommends WHO low-osmolarity ORS plus zinc for children with no signs of dehydration, and advises against soft drinks, sports drinks and electrolyte drinks that do not meet the WHO low-osmolarity formula. WHO notes that a 10–14 day zinc course shortens a diarrhoea episode by about 25% and cuts stool volume by about 30%.', updated_at = now()
where id = 'med_ors' and description = 'Reduced-osmolarity ORS (245 mOsm/L) contains glucose and sodium in equimolar amounts (75 mmol/L each), exploiting sodium-glucose co-transport in the small intestine to drive water absorption even during secretory diarrhea. It also replaces potassium and corrects acidosis with citrate. Compared with the older standard ORS it reduces stool output, vomiting and the need for unscheduled IV therapy; it is the cornerstone of treatment for dehydration from acute diarrhea.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'PSPGHAN (Philippine Pediatric Society); PhilHealth; MSF Essential Drugs; World Health Organization' else source_attribution || '; PSPGHAN (Philippine Pediatric Society); PhilHealth; MSF Essential Drugs; World Health Organization' end
where id = 'med_ors' and position('PSPGHAN (Philippine Pediatric Society)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ors', 'indication', 'Given alongside IV therapy in severe dehydration (WHO Plan C), once the patient is conscious and able to drink', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ors' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ors' and kind = 'indication' and content = 'Given alongside IV therapy in severe dehydration (WHO Plan C), once the patient is conscious and able to drink');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ors', 'contraindication', 'Severe acute malnutrition: use ReSoMal (special ORS) under medical supervision instead, except in cholera, where standard ORS is used (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ors' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ors' and kind = 'contraindication' and content = 'Severe acute malnutrition: use ReSoMal (special ORS) under medical supervision instead, except in cholera, where standard ORS is used (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ors', 'interaction', 'Zinc given with ORS: separate zinc from iron (ferrous) salts by at least 2 hours (MSF).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ors' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ors' and kind = 'interaction' and content = 'Zinc given with ORS: separate zinc from iron (ferrous) salts by at least 2 hours (MSF).');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ors', 'PSPGHAN (Philippine Pediatric Society)', 'Philippine Society for Pediatric Gastroenterology, Hepatology and Nutrition. Guidelines for Health Care Professionals on the Treatment of Acute Gastroenteritis with No Signs of Dehydration. April 2026.', 'https://pps.org.ph/wp-content/uploads/PSPGHAN-GUIDELINES-ON-THE-TREATMENT-OF-ACUTE-GASTROENTERITIS-WITH-NO-SIGNS-OF-DEHYDRATION-April-2026-1.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ors'), 0)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ors' and url = 'https://pps.org.ph/wp-content/uploads/PSPGHAN-GUIDELINES-ON-THE-TREATMENT-OF-ACUTE-GASTROENTERITIS-WITH-NO-SIGNS-OF-DEHYDRATION-April-2026-1.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ors', 'PhilHealth', 'Philippine Health Insurance Corporation. Quality Policy on the Diagnosis and Management of Acute Infectious Gastroenteritis as Reference of the Corporation. PhilHealth Circular 2022-0026.', 'https://www.philhealth.gov.ph/circulars/2022/circ2022-0026.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ors'), 0)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ors' and url = 'https://www.philhealth.gov.ph/circulars/2022/circ2022-0026.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ors', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Oral rehydration salts (ORS). MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/oral-rehydration-salts-ors-16684387.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ors'), 0)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ors' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/oral-rehydration-salts-ors-16684387.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ors', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Zinc sulfate oral. MSF Medical Guidelines.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/zinc-sulfate-oral-16684806.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ors'), 0)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ors' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/zinc-sulfate-oral-16684806.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ors', 'World Health Organization', 'WHO. Diarrhoeal disease. Fact sheet, 7 March 2024.', 'https://www.who.int/news-room/fact-sheets/detail/diarrhoeal-disease', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ors'), 0)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ors' and url = 'https://www.who.int/news-room/fact-sheets/detail/diarrhoeal-disease');
-- med_ors
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_ors', 'adult', 0, 'No dehydration (Plan A), >10 y and adults', 'PO', '200–400 mL after each loose stool', 'After each stool', 'While diarrhoea lasts', 'About 2000 mL/day', 'MSF', ''),
    ('med_ors', 'adult', 1, 'Moderate dehydration (Plan B), ≥15 y / ≥30 kg', 'PO', '2200–4000 mL', 'Over 4 h', '4 h, then reassess', '—', 'MSF', 'Then Plan A, repeat Plan B, or start IV (Plan C)'),
    ('med_ors', 'adult', 2, 'Severe dehydration (Plan C), with IV fluids', 'PO', '5 mL/kg/h', 'Continuous', 'Reassess after 3 h', '—', 'MSF', 'Only if conscious'),
    ('med_ors', 'child', 3, 'No dehydration (Plan A), <2 y', 'PO', '50–100 mL after each loose stool', 'After each stool', 'While diarrhoea lasts', 'About 500 mL/day', 'MSF', 'PSPGHAN: 50–100 mL (¼–½ cup)'),
    ('med_ors', 'child', 4, 'No dehydration (Plan A), 2–10 y', 'PO', '100–200 mL after each loose stool', 'After each stool', 'While diarrhoea lasts', 'About 1000 mL/day', 'MSF', 'PSPGHAN: 100 mL (½ cup)'),
    ('med_ors', 'child', 5, 'No dehydration, >10 y (PH)', 'PO', 'As much as tolerated', 'After each stool', 'While diarrhoea lasts', '—', 'PSPGHAN 2026', ''),
    ('med_ors', 'child', 6, 'Moderate dehydration (Plan B), <4 mo / <5 kg', 'PO', '200–400 mL', 'Over 4 h', '4 h, then reassess', '—', 'MSF', ''),
    ('med_ors', 'child', 7, 'Moderate dehydration (Plan B), 4–11 mo / 5–7.9 kg', 'PO', '400–600 mL', 'Over 4 h', '4 h, then reassess', '—', 'MSF', ''),
    ('med_ors', 'child', 8, 'Moderate dehydration (Plan B), 12–23 mo / 8–10.9 kg', 'PO', '600–800 mL', 'Over 4 h', '4 h, then reassess', '—', 'MSF', ''),
    ('med_ors', 'child', 9, 'Moderate dehydration (Plan B), 2–4 y / 11–15.9 kg', 'PO', '800–1200 mL', 'Over 4 h', '4 h, then reassess', '—', 'MSF', ''),
    ('med_ors', 'child', 10, 'Moderate dehydration (Plan B), 5–14 y / 16–29.9 kg', 'PO', '1200–2200 mL', 'Over 4 h', '4 h, then reassess', '—', 'MSF', ''),
    ('med_ors', 'child', 11, 'Severe dehydration (Plan C), with IV fluids', 'PO', '5 mL/kg/h', 'Continuous', 'Reassess after 3 h (6 h in infants)', '—', 'MSF', 'Only if conscious'),
    ('med_ors', 'child', 12, 'Adjunct zinc with ORS, <6 mo', 'PO', '10 mg zinc', 'Once a day', '10 days', '—', 'MSF zinc', 'Half a 20 mg dispersible tablet'),
    ('med_ors', 'child', 13, 'Adjunct zinc with ORS, 6 mo–5 y', 'PO', '20 mg zinc', 'Once a day', '10–14 days', '—', 'MSF zinc', 'PSPGHAN/PhilHealth: 20 mg/day; PSPGHAN gives 14 days')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_ors');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_ors', 'forms_ph', 0, '', 'PSPGHAN describes WHO low-osmolarity ORS in the Philippines as flavoured sachets made up with 100 mL, unflavoured or flavoured sachets made up with 200 mL of cool boiled water, and a flavoured ready-to-drink solution. Zinc for diarrhoea: drops 10 mg/mL (2 mL daily) or syrup 20 mg/5 mL (5 mL daily), as a single preparation, not a multivitamin.', 'PSPGHAN 2026'),
    ('med_ors', 'pregnancy', 1, '', 'No contraindication in pregnancy or breastfeeding.', 'MSF'),
    ('med_ors', 'administration', 2, '', 'Make up only with the volume of cool boiled water stated for that sachet size (100 mL or 200 mL sachets in PH).', 'PSPGHAN 2026'),
    ('med_ors', 'administration', 3, '', 'If the child vomits, stop for 10 minutes, then restart with very small, frequent amounts; do not stop rehydration.', 'MSF'),
    ('med_ors', 'administration', 4, '', 'Continue diet for age and breastfeeding during the episode.', 'PSPGHAN 2026'),
    ('med_ors', 'administration', 5, '', 'Zinc dispersible tablet: dissolve in a teaspoon of water; repeat the dose if vomited within 30 minutes. Zinc never replaces ORS.', 'MSF zinc'),
    ('med_ors', 'monitor', 6, '', 'Reassess hydration after 4 hours of Plan B (3 h on Plan C, 6 h in infants) and choose Plan A, B or C again.', 'MSF'),
    ('med_ors', 'monitor', 7, '', 'Puffy eyelids: stop ORS, give plain water, and resume Plan A once the puffiness settles.', 'MSF'),
    ('med_ors', 'monitor', 8, '', 'Children with no dehydration: see the doctor again if symptoms persist or do not improve within 3 days.', 'PSPGHAN 2026')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_ors');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_ors', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Oral rehydration salts (ORS).', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/oral-rehydration-salts-ors-16684387.html', 0),
    ('med_ors', 'MSF zinc', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Zinc sulfate oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/zinc-sulfate-oral-16684806.html', 1),
    ('med_ors', 'PSPGHAN 2026', 'PSPGHAN (Philippine Pediatric Society)', 'PSPGHAN. Treatment of Acute Gastroenteritis with No Signs of Dehydration. April 2026.', 'https://pps.org.ph/wp-content/uploads/PSPGHAN-GUIDELINES-ON-THE-TREATMENT-OF-ACUTE-GASTROENTERITIS-WITH-NO-SIGNS-OF-DEHYDRATION-April-2026-1.pdf', 2),
    ('med_ors', 'PhilHealth', 'PhilHealth', 'PhilHealth Circular 2022-0026. Quality Policy on Acute Infectious Gastroenteritis.', 'https://www.philhealth.gov.ph/circulars/2022/circ2022-0026.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_ors')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_ors');


-- ================================================ med_oseltamivir  (Oseltamivir)
update public.medicines set description = 'Oseltamivir is an oral prodrug converted to oseltamivir carboxylate, a competitive inhibitor of influenza A and B neuraminidase that prevents release of new virions from infected cells. Started ideally within 48 hours of symptom onset, it shortens illness duration and is recommended for hospitalized and high-risk patients; it is also used for post-exposure prophylaxis. WHO lists oseltamivir on the complementary Essential Medicines List (30, 45 and 75 mg capsules; 6 mg/mL powder for oral liquid for children), limited to severe confirmed or suspected influenza in critically ill hospitalized patients. CDC advises starting it without waiting for test results in hospitalized, severely ill or high-risk patients, and in hospitalized patients even when more than 48 hours have passed since symptom onset. It is the preferred antiviral in pregnancy and does not replace influenza vaccination.', updated_at = now()
where id = 'med_oseltamivir' and description = 'Oseltamivir is an oral prodrug converted to oseltamivir carboxylate, a competitive inhibitor of influenza A and B neuraminidase that prevents release of new virions from infected cells. Started ideally within 48 hours of symptom onset, it shortens illness duration and is recommended for hospitalized and high-risk patients; it is also used for post-exposure prophylaxis.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); CDC; WHO eEML' else source_attribution || '; UK SmPC (emc); CDC; WHO eEML' end
where id = 'med_oseltamivir' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'indication', 'Treatment of influenza in hospitalized or severe, complicated or progressive illness, even if started more than 48 hours after onset (CDC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'indication' and content = 'Treatment of influenza in hospitalized or severe, complicated or progressive illness, even if started more than 48 hours after onset (CDC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'indication', 'Treatment of influenza in infants under 1 year, including full-term neonates', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'indication' and content = 'Treatment of influenza in infants under 1 year, including full-term neonates');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'indication', 'Seasonal prophylaxis in exceptional situations (e.g., vaccine-strain mismatch or pandemic); post-exposure prophylaxis in infants under 1 year only during a pandemic (UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'indication' and content = 'Seasonal prophylaxis in exceptional situations (e.g., vaccine-strain mismatch or pandemic); post-exposure prophylaxis in infants under 1 year only during a pandemic (UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'adverse', 'Vomiting is the most common effect in children; also conjunctivitis, earache, otitis media, cough and nasal congestion', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse' and content = 'Vomiting is the most common effect in children; also conjunctivitis, earache, otitis media, cough and nasal congestion');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'adverse', 'Hepatitis, jaundice and hepatic failure (rare, some fatal)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse' and content = 'Hepatitis, jaundice and hepatic failure (rare, some fatal)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'adverse', 'Gastrointestinal bleeding (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse' and content = 'Gastrointestinal bleeding (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'adverse', 'Angioedema', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse' and content = 'Angioedema');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'adverse', 'Convulsions', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse' and content = 'Convulsions');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'adverse', 'Thrombocytopenia, visual disturbance and cardiac arrhythmia (listed in the UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'adverse' and content = 'Thrombocytopenia, visual disturbance and cardiac arrhythmia (listed in the UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'interaction', 'Probenecid: roughly doubles exposure to the active metabolite; no dose change with normal renal function.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'interaction' and content = 'Probenecid: roughly doubles exposure to the active metabolite; no dose change with normal renal function.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'interaction', 'Renally excreted drugs with a narrow margin (e.g., chlorpropamide, methotrexate, phenylbutazone): use with caution.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'interaction' and content = 'Renally excreted drugs with a narrow margin (e.g., chlorpropamide, methotrexate, phenylbutazone): use with caution.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_oseltamivir', 'interaction', 'No interactions reported with paracetamol, aspirin, cimetidine, antacids, warfarin or amoxicillin.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_oseltamivir' and kind = 'interaction' and content = 'No interactions reported with paracetamol, aspirin, cimetidine, antacids, warfarin or amoxicillin.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_oseltamivir', 'UK SmPC (emc)', 'Tamiflu 30 mg, 45 mg and 75 mg hard capsules. Summary of Product Characteristics. Roche Products Ltd; revised January 2021. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=oseltamivir#emc-1194', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_oseltamivir'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_oseltamivir' and url = 'https://products.mhra.gov.uk/search/?search=oseltamivir#emc-1194');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_oseltamivir', 'CDC', 'Centers for Disease Control and Prevention. Influenza Antiviral Medications: Summary for Clinicians. Last reviewed 10 March 2026.', 'https://www.cdc.gov/flu/hcp/antivirals/summary-clinicians.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_oseltamivir'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_oseltamivir' and url = 'https://www.cdc.gov/flu/hcp/antivirals/summary-clinicians.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_oseltamivir', 'WHO eEML', 'World Health Organization. Electronic Essential Medicines List – Oseltamivir (complementary list, section 6.4.3).', 'https://list.essentialmeds.org/recommendations/511', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_oseltamivir'), 0)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_oseltamivir' and url = 'https://list.essentialmeds.org/recommendations/511');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_oseltamivir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Dose must be reduced when CrCl is 60 mL/min or less; not recommended at CrCl 10 or below without dialysis (UK SmPC, CDC).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_oseltamivir');
-- med_oseltamivir
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_oseltamivir', 'adult', 0, 'Treatment (≥13 y, >40 kg)', 'PO', '75 mg', '2× a day', '5 days (10 days if immunocompromised)', '—', 'Label · UK SmPC', 'Start within 2 days of onset'),
    ('med_oseltamivir', 'adult', 1, 'Post-exposure prophylaxis', 'PO', '75 mg', 'Once a day', '10 days', '—', 'Label · UK SmPC', 'Start within 2 days of exposure; CDC: 7 days after last exposure'),
    ('med_oseltamivir', 'adult', 2, 'Prophylaxis during a community epidemic', 'PO', '75 mg', 'Once a day', 'Up to 6 weeks (12 weeks if immunocompromised)', '—', 'Label · UK SmPC', ''),
    ('med_oseltamivir', 'adult', 3, 'Institutional outbreak prophylaxis', 'PO', '75 mg', 'Once a day', '≥2 weeks, until 1 week after last case', '—', 'CDC', ''),
    ('med_oseltamivir', 'child', 4, 'Treatment (≥1 y, ≤15 kg)', 'PO', '30 mg', '2× a day', '5 days', '—', 'Label · UK SmPC', 'UK SmPC band 10–15 kg'),
    ('med_oseltamivir', 'child', 5, 'Treatment (≥1 y, >15–23 kg)', 'PO', '45 mg', '2× a day', '5 days', '—', 'Label · UK SmPC', ''),
    ('med_oseltamivir', 'child', 6, 'Treatment (≥1 y, >23–40 kg)', 'PO', '60 mg', '2× a day', '5 days', '—', 'Label · UK SmPC', ''),
    ('med_oseltamivir', 'child', 7, 'Treatment (≥1 y, >40 kg)', 'PO', '75 mg', '2× a day', '5 days', '—', 'Label · UK SmPC', ''),
    ('med_oseltamivir', 'child', 8, 'Prophylaxis (≥1 y)', 'PO', 'Same weight-band dose as treatment', 'Once a day', '10 days', '75 mg', 'Label · UK SmPC', 'CDC: 7 days after last exposure'),
    ('med_oseltamivir', 'child', 9, 'Treatment (<1 y)', 'PO', '3 mg/kg', '2× a day', '5 days (10 days if immunocompromised)', '—', 'Label · UK SmPC', 'AAP (via CDC): 3.5 mg/kg for 9–11 months'),
    ('med_oseltamivir', 'child', 10, 'Prophylaxis (3 mo to <1 y)', 'PO', '3 mg/kg', 'Once a day', '10 days', '—', 'Label · UK SmPC', 'UK: pandemic only; CDC: not under 3 months unless critical'),
    ('med_oseltamivir', 'neonate', 11, 'Treatment, preterm (PMA <38 wk)', 'PO', '1 mg/kg', '2× a day', '5 days', '—', 'CDC', 'Not licensed below 36 weeks post-conceptual age (UK)'),
    ('med_oseltamivir', 'neonate', 12, 'Treatment, preterm (PMA 38–40 wk)', 'PO', '1.5 mg/kg', '2× a day', '5 days', '—', 'CDC', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_oseltamivir');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_oseltamivir', 'renal', 0, 'CrCl 30–60', 'Treatment 30 mg 2× a day; prophylaxis 30 mg once a day.', 'Label · UK SmPC'),
    ('med_oseltamivir', 'renal', 1, 'CrCl 10–30', 'Treatment 30 mg once a day; prophylaxis 30 mg every second day.', 'Label · UK SmPC'),
    ('med_oseltamivir', 'renal', 2, 'CrCl ≤10', 'Not recommended (no data) unless on dialysis.', 'Label · UK SmPC'),
    ('med_oseltamivir', 'renal', 3, 'Haemodialysis', 'Haemodialysis: treatment 30 mg after each session; prophylaxis 30 mg after every second session. CDC: treatment no longer than 5 days.', 'Label · UK SmPC'),
    ('med_oseltamivir', 'renal', 4, 'Peritoneal dialysis', 'Peritoneal dialysis: treatment 30 mg single dose; prophylaxis 30 mg once a week.', 'Label · UK SmPC'),
    ('med_oseltamivir', 'renal', 5, 'Children', 'No dosing data for children 12 years and under with renal impairment.', 'Label · UK SmPC'),
    ('med_oseltamivir', 'hepatic', 6, '', 'No dose adjustment needed.', 'Label · UK SmPC'),
    ('med_oseltamivir', 'elderly', 7, '', 'No dose adjustment unless moderate or severe renal impairment.', 'Label · UK SmPC'),
    ('med_oseltamivir', 'pregnancy', 8, '', 'Preferred antiviral in pregnancy, at the same dose as in non-pregnant adults (CDC). Over 1,000 first-trimester exposures showed no malformative toxicity (UK SmPC). Passes into breast milk in small amounts; may be used when there is clear benefit.', 'CDC'),
    ('med_oseltamivir', 'administration', 9, '', 'Can be taken with or without food (food does not change levels); taking it with food may reduce nausea and vomiting. If capsules cannot be swallowed, use the oral suspension; a pharmacy-made 6 mg/mL suspension is preferred, otherwise mix capsule contents with no more than a teaspoon of sweetened food and swallow at once.', 'Label · UK SmPC'),
    ('med_oseltamivir', 'administration', 10, '', 'Critically ill adults: standard doses are adequately absorbed by mouth or feeding tube; doubling to 150 mg 2× a day may not add benefit. Extend beyond 5 days if still severely ill.', 'CDC'),
    ('med_oseltamivir', 'monitor', 11, '', 'Watch behaviour closely, especially in children and adolescents, for neuropsychiatric events (delirium, self-injury, convulsions).', 'Label · UK SmPC'),
    ('med_oseltamivir', 'monitor', 12, '', 'Check creatinine clearance before dosing and adjust for renal function.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_oseltamivir');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_oseltamivir', 'Label · UK SmPC', 'UK SmPC (emc)', 'Tamiflu hard capsules. SmPC. Roche; January 2021.', 'https://products.mhra.gov.uk/search/?search=oseltamivir#emc-1194', 0),
    ('med_oseltamivir', 'CDC', 'CDC', 'CDC. Influenza Antiviral Medications: Summary for Clinicians. March 2026.', 'https://www.cdc.gov/flu/hcp/antivirals/summary-clinicians.html', 1)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_oseltamivir')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_oseltamivir');


-- ================================================ med_paracetamol  (Paracetamol)
update public.medicines set description = 'Paracetamol is thought to act mainly centrally, reducing prostaglandin synthesis via inhibition of cyclooxygenase pathways in the CNS, with a possible contribution from its metabolite AM404 acting on cannabinoid and TRPV1 systems. It has analgesic and antipyretic effects but minimal peripheral anti-inflammatory activity, and is a first-line agent for mild-to-moderate pain and fever. A small fraction is converted by hepatic cytochrome P-450 to the toxic metabolite NAPQI, normally detoxified by glutathione; an acute ingestion of at least 150 mg/kg (about 7.5–10 g in adults) can deplete glutathione and cause hepatocellular necrosis, and N-acetylcysteine is most effective within 8 hours of ingestion. In the Philippines, paracetamol is in the PhilHealth Konsulta primary-care medicines list as 300 mg and 500 mg tablets, 100 mg/mL drops, 120 mg/5 mL (125 mg/5 mL) and 250 mg/5 mL syrup/suspension, and 125 mg and 250 mg suppositories.', updated_at = now()
where id = 'med_paracetamol' and description = 'Paracetamol is thought to act mainly centrally, reducing prostaglandin synthesis via inhibition of cyclooxygenase pathways in the CNS, with a possible contribution from its metabolite AM404 acting on cannabinoid and TRPV1 systems. It has analgesic and antipyretic effects but minimal peripheral anti-inflammatory activity, and is a first-line agent for mild-to-moderate pain and fever.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC; Merck Manual Professional; PhilHealth Konsulta' else source_attribution || '; UK SmPC; Merck Manual Professional; PhilHealth Konsulta' end
where id = 'med_paracetamol' and position('UK SmPC' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_paracetamol', 'adverse', 'Blood dyscrasias including thrombocytopenia and agranulocytosis (frequency not known)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'adverse' and content = 'Blood dyscrasias including thrombocytopenia and agranulocytosis (frequency not known)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_paracetamol', 'adverse', 'High anion gap metabolic acidosis, mainly in sepsis, malnutrition or glutathione deficiency (e.g. chronic alcoholism)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'adverse' and content = 'High anion gap metabolic acidosis, mainly in sepsis, malnutrition or glutathione deficiency (e.g. chronic alcoholism)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_paracetamol', 'contraindication', 'Use with care in severe renal impairment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'contraindication' and content = 'Use with care in severe renal impairment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_paracetamol', 'contraindication', 'Overdose hazard greater in non-cirrhotic alcoholic liver disease', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'contraindication' and content = 'Overdose hazard greater in non-cirrhotic alcoholic liver disease');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_paracetamol', 'interaction', 'Metoclopramide or domperidone: may speed paracetamol absorption.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'interaction' and content = 'Metoclopramide or domperidone: may speed paracetamol absorption.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_paracetamol', 'interaction', 'Cholestyramine: reduces paracetamol absorption.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'interaction' and content = 'Cholestyramine: reduces paracetamol absorption.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_paracetamol', 'interaction', 'Flucloxacillin: combined (especially prolonged) use raises the risk of high anion gap metabolic acidosis; use with caution.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_paracetamol' and kind = 'interaction' and content = 'Flucloxacillin: combined (especially prolonged) use raises the risk of high anion gap metabolic acidosis; use with caution.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_paracetamol', 'UK SmPC', 'Paracetamol 500 mg Tablets (P), Zentiva Pharma UK Ltd. Summary of Product Characteristics (updated 25 February 2025). electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=paracetamol#emc-9128', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_paracetamol'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_paracetamol' and url = 'https://products.mhra.gov.uk/search/?search=paracetamol#emc-9128');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_paracetamol', 'Merck Manual Professional', 'O''Malley GF, O''Malley R. Acetaminophen Poisoning. Merck Manual Professional Edition (reviewed Apr 2025).', 'https://www.merckmanuals.com/professional/injuries-poisoning/poisoning/acetaminophen-poisoning', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_paracetamol'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_paracetamol' and url = 'https://www.merckmanuals.com/professional/injuries-poisoning/poisoning/acetaminophen-poisoning');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_paracetamol', 'PhilHealth Konsulta', 'Philippine Health Insurance Corporation. Certification of Service Delivery Support (Medicines), Annex D2 – Konsulta Package accreditation.', 'https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_paracetamol'), 0)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_paracetamol' and url = 'https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_paracetamol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'SmPC advises care in severe renal impairment (applies to advanced CKD).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_paracetamol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hepatitis_b', 'med_paracetamol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hepatitis_b'), 0), 'caution'::condition_safety, 'Own inference: SmPC advises care in severe hepatic impairment, which can occur in chronic hepatitis B; not stated for hepatitis B specifically.'
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hepatitis_b' and medicine_id = 'med_paracetamol');

-- ================================================ med_permethrin  (Permethrin 5% cream)
update public.medicines set description = 'Permethrin is a synthetic pyrethroid that blocks sodium channels in the nerve membranes of mites and lice, causing paralysis and death. Very little is absorbed through human skin. Permethrin 5% cream is a first-line treatment for scabies; because it may not kill all eggs, a second application about a week later is usually advised, and all close contacts are treated at the same time. WHO lists 5% permethrin cream as a whole-body topical scabicide and as the topical option for community mass treatment when oral ivermectin is contraindicated or unavailable (ivermectin is not given in pregnancy or to children under 15 kg). About 90% of patients are cured by one application; itching can last up to 4 weeks from an allergic reaction to dead mites and is not by itself a reason to re-treat. Clothes and bed linen are decontaminated after each treatment (wash at 60 °C or more and sun-dry, or seal in a plastic bag for 72 hours).', updated_at = now()
where id = 'med_permethrin' and description = 'Permethrin is a synthetic pyrethroid that blocks sodium channels in the nerve membranes of mites and lice, causing paralysis and death. Very little is absorbed through human skin. Permethrin 5% cream is a first-line treatment for scabies; because it may not kill all eggs, a second application about a week later is usually advised, and all close contacts are treated at the same time.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'MSF Essential Drugs - Permethrin 5% cream; UK SmPC - Permethrin 5% w/w Cream (Sandoz); WHO - Scabies fact sheet' else source_attribution || '; MSF Essential Drugs - Permethrin 5% cream; UK SmPC - Permethrin 5% w/w Cream (Sandoz); WHO - Scabies fact sheet' end
where id = 'med_permethrin' and position('MSF Essential Drugs - Permethrin 5% cream' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_permethrin', 'adverse', 'Paraesthesia (tingling) and dry skin', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'adverse' and content = 'Paraesthesia (tingling) and dry skin');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_permethrin', 'adverse', 'Oedema and hypersensitivity reactions (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'adverse' and content = 'Oedema and hypersensitivity reactions (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_permethrin', 'adverse', 'Itching that persists up to 4 weeks after treatment (reaction to dead mites, not necessarily treatment failure)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'adverse' and content = 'Itching that persists up to 4 weeks after treatment (reaction to dead mites, not necessarily treatment failure)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_permethrin', 'contraindication', 'Application to the face, mucous membranes or broken skin (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'contraindication' and content = 'Application to the face, mucous membranes or broken skin (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_permethrin', 'contraindication', 'Hypersensitivity to any excipient (e.g., benzyl alcohol, cetostearyl alcohol in some creams)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'contraindication' and content = 'Hypersensitivity to any excipient (e.g., benzyl alcohol, cetostearyl alcohol in some creams)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_permethrin', 'interaction', 'Topical corticosteroids for eczema-like reactions: withhold before treatment, as they may reduce the immune response to the mite and worsen the infestation.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_permethrin' and kind = 'interaction' and content = 'Topical corticosteroids for eczema-like reactions: withhold before treatment, as they may reduce the immune response to the mite and worsen the infestation.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_permethrin', 'MSF Essential Drugs - Permethrin 5% cream', 'Medecins Sans Frontieres. Essential drugs - practical guidelines: Permethrin 5%, cream.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/permethrin-5-cream-16687201.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_permethrin'), 0)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_permethrin' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/permethrin-5-cream-16687201.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_permethrin', 'UK SmPC - Permethrin 5% w/w Cream (Sandoz)', 'Sandoz Limited. Permethrin 5% w/w Cream - Summary of Product Characteristics. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=permethrin#emc-6540', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_permethrin'), 0)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_permethrin' and url = 'https://products.mhra.gov.uk/search/?search=permethrin#emc-6540');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_permethrin', 'WHO - Scabies fact sheet', 'World Health Organization. Scabies. Fact sheet.', 'https://www.who.int/news-room/fact-sheets/detail/scabies', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_permethrin'), 0)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_permethrin' and url = 'https://www.who.int/news-room/fact-sheets/detail/scabies');
-- med_permethrin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_permethrin', 'adult', 0, 'Scabies', 'Topical', 'Up to 30 g (1 tube)', 'Single application; wash off after 8–12 h', 'Repeat once ≥7 days later if needed', '60 g per application', 'Label · UK SmPC', 'Also adolescents >12 y and elderly'),
    ('med_permethrin', 'adult', 1, 'Scabies', 'Topical', 'Thin layer, whole body', 'Leave on ≥8 h, then rinse', 'Repeat after 7 days', '—', 'MSF', 'Include scalp, behind ears, palms, soles'),
    ('med_permethrin', 'child', 2, 'Scabies (6–12 y)', 'Topical', 'Up to 15 g (½ tube)', 'Single application; wash off after 8–12 h', 'Repeat once ≥7 days later if needed', '15 g per application', 'Label · UK SmPC', ''),
    ('med_permethrin', 'child', 3, 'Scabies (1–5 y)', 'Topical', 'Up to 7.5 g (¼ tube)', 'Single application; wash off after 8–12 h', 'Repeat once ≥7 days later if needed', '7.5 g per application', 'Label · UK SmPC', 'Under 2 y: medical supervision'),
    ('med_permethrin', 'child', 4, 'Scabies (2 mo–1 y)', 'Topical', 'Up to 3.75 g (⅛ tube)', 'Single application; wash off after 8–12 h', 'Repeat once ≥7 days later if needed', '3.75 g per application', 'Label · UK SmPC', 'Not under 2 months')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_permethrin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_permethrin', 'pregnancy', 0, '', 'Limited data show no sign of fetal risk; systemic absorption is very low, though some permethrin may cross the placenta. Breastfeeding: risk to the infant considered unlikely; do not apply the cream to the breasts (MSF).', 'Label · UK SmPC'),
    ('med_permethrin', 'administration', 1, '', 'Apply to clean, dry, cool skin (not straight after a hot bath) and rub in gently. Reapply to the hands if they are washed within 8 hours. Carers applying it should wear gloves. Keep out of the eyes (rinse with water or saline if contact). Fabric soaked with cream ignites easily: keep away from flames.', 'Label · UK SmPC'),
    ('med_permethrin', 'administration', 2, '', 'In children under 2 years, wrap the hands to prevent swallowing the cream and getting it in the eyes.', 'MSF'),
    ('med_permethrin', 'monitor', 3, '', 'Give a second application (not sooner than 7 days) if original lesions are not healing or new lesions appear. Persistent itching alone within 4 weeks is not treatment failure; re-treat only if burrows are still present after that time. Treat all close contacts at the same time.', 'MSF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_permethrin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_permethrin', 'Label · UK SmPC', 'UK SmPC - Permethrin 5% w/w Cream (Sandoz)', 'Sandoz Limited. Permethrin 5% w/w Cream - SmPC. emc.', 'https://products.mhra.gov.uk/search/?search=permethrin#emc-6540', 0),
    ('med_permethrin', 'MSF', 'MSF Essential Drugs - Permethrin 5% cream', 'Medecins Sans Frontieres. Essential drugs: Permethrin 5%, cream.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/permethrin-5-cream-16687201.html', 1)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_permethrin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_permethrin');


-- ================================================ med_praziquantel  (Praziquantel)
update public.medicines set description = 'Praziquantel is a synthetic pyrazinoisoquinoline anthelmintic that increases the permeability of the helminth tegument to calcium, producing rapid muscle contraction, spastic paralysis and tegumental damage that exposes the parasite to host defenses. It is the drug of choice for all Schistosoma species, including S. japonicum endemic in the Philippines, and for the liver flukes Clonorchis and Opisthorchis, and is also active against tapeworms and cysticercosis. WHO''s 2022 schistosomiasis guideline extends preventive chemotherapy to adults and preschool children, considers praziquantel safe from age 2 years and in pregnancy after the first trimester, and recommends one annual dose where prevalence is 10% or more. In mass campaigns the dose is read from the person''s height (dose pole) instead of weight.', updated_at = now()
where id = 'med_praziquantel' and description = 'Praziquantel is a synthetic pyrazinoisoquinoline anthelmintic that increases the permeability of the helminth tegument to calcium, producing rapid muscle contraction, spastic paralysis and tegumental damage that exposes the parasite to host defenses. It is the drug of choice for all Schistosoma species, including S. japonicum endemic in the Philippines, and for the liver flukes Clonorchis and Opisthorchis, and is also active against tapeworms and cysticercosis.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'MSF Essential Drugs - Praziquantel oral; WHO Prequalification - Praziquantel 600 mg tablets SmPC (NT004); WHO - Guideline on control and elimination of human schistosomiasis (2022); BIGG (PAHO/BVS) - WHO schistosomiasis recommendation; DailyMed - BILTRICIDE; WHO guideline on control and elimination of human schistosomiasis (2022), via BIGG' else source_attribution || '; MSF Essential Drugs - Praziquantel oral; WHO Prequalification - Praziquantel 600 mg tablets SmPC (NT004); WHO - Guideline on control and elimination of human schistosomiasis (2022); BIGG (PAHO/BVS) - WHO schistosomiasis recommendation; DailyMed - BILTRICIDE; WHO guideline on control and elimination of human schistosomiasis (2022), via BIGG' end
where id = 'med_praziquantel' and position('MSF Essential Drugs - Praziquantel oral' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'indication', 'Intestinal flukes (Fasciolopsis buski, Heterophyes heterophyes, Metagonimus yokogawai)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'indication' and content = 'Intestinal flukes (Fasciolopsis buski, Heterophyes heterophyes, Metagonimus yokogawai)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'adverse', 'Vomiting and fatigue (very common in mass treatment)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse' and content = 'Vomiting and fatigue (very common in mass treatment)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'adverse', 'Diarrhoea, sometimes bloody', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse' and content = 'Diarrhoea, sometimes bloody');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'adverse', 'Eosinophilia and polyserositis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse' and content = 'Eosinophilia and polyserositis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'adverse', 'Raised liver function tests', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse' and content = 'Raised liver function tests');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'adverse', 'Side effects more frequent and severe with heavy worm burden', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'adverse' and content = 'Side effects more frequent and severe with heavy worm burden');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'contraindication', 'Avoid in epilepsy or signs of CNS involvement from schistosomiasis, paragonimiasis or T. solium cysticercosis (WHO-prequalified label)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'contraindication' and content = 'Avoid in epilepsy or signs of CNS involvement from schistosomiasis, paragonimiasis or T. solium cysticercosis (WHO-prequalified label)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'contraindication', 'Not active against Fasciola hepatica or F. gigantica (use triclabendazole)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'contraindication' and content = 'Not active against Fasciola hepatica or F. gigantica (use triclabendazole)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'interaction', 'Phenytoin, phenobarbital, carbamazepine and dexamethasone: lower praziquantel levels; concomitant use not recommended.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'interaction' and content = 'Phenytoin, phenobarbital, carbamazepine and dexamethasone: lower praziquantel levels; concomitant use not recommended.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'interaction', 'Chloroquine: may lower praziquantel blood concentrations (mechanism unclear).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'interaction' and content = 'Chloroquine: may lower praziquantel blood concentrations (mechanism unclear).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_praziquantel', 'interaction', 'Digoxin: monitor patients with arrhythmias or heart failure on digoxin during treatment.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_praziquantel' and kind = 'interaction' and content = 'Digoxin: monitor patients with arrhythmias or heart failure on digoxin during treatment.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_praziquantel', 'MSF Essential Drugs - Praziquantel oral', 'Medecins Sans Frontieres. Essential drugs - practical guidelines: Praziquantel, oral.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/praziquantel-oral-16684480.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_praziquantel'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_praziquantel' and url = 'https://medicalguidelines.msf.org/viewport/EssDr/english/praziquantel-oral-16684480.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_praziquantel', 'WHO Prequalification - Praziquantel 600 mg tablets SmPC (NT004)', 'World Health Organization Prequalification. WHOPAR NT004 Part 4: Summary of product characteristics, Praziquantel Tablets 600 mg (Macleods Pharmaceuticals Ltd).', 'https://extranet.who.int/prequal/sites/default/files/whopar_files/NT004part4.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_praziquantel'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_praziquantel' and url = 'https://extranet.who.int/prequal/sites/default/files/whopar_files/NT004part4.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_praziquantel', 'WHO - Guideline on control and elimination of human schistosomiasis (2022)', 'World Health Organization. WHO launches new guideline for the control and elimination of human schistosomiasis. News release, 22 February 2022.', 'https://www.who.int/news/item/22-02-2022-who-launches-new-guideline-for-the-control-and-elimination-of-human-schistosomiasis', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_praziquantel'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_praziquantel' and url = 'https://www.who.int/news/item/22-02-2022-who-launches-new-guideline-for-the-control-and-elimination-of-human-schistosomiasis');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_praziquantel', 'BIGG (PAHO/BVS) - WHO schistosomiasis recommendation', 'WHO guideline on control and elimination of human schistosomiasis (2022): annual single-dose praziquantel preventive chemotherapy where prevalence >=10%, incl. pregnant women after the first trimester. BIGG international database of GRADE guidelines.', 'https://bigg-rec.bvsalud.org/en/recommendations/db797c50ffffecd0187f631260baf6e5d402b92e', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_praziquantel'), 0)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_praziquantel' and url = 'https://bigg-rec.bvsalud.org/en/recommendations/db797c50ffffecd0187f631260baf6e5d402b92e');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_praziquantel', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'WHO-prequalified label: monitor patients with arrhythmias or heart failure taking digoxin.'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_praziquantel');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'tuberculosis', 'med_praziquantel', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'tuberculosis'), 0), 'caution'::condition_safety, 'Rifampicin is contraindicated with praziquantel; stop it 4 weeks before and restart 1 day after (applying this to TB treatment is an inference from the rifampicin interaction).'
where exists (select 1 from public.diseases where id = 'tuberculosis')
  and exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.disease_medicines where disease_id = 'tuberculosis' and medicine_id = 'med_praziquantel');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_praziquantel', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'caution'::condition_safety, 'Efavirenz lowers and ritonavir raises praziquantel levels per the US label (applying this to HIV treatment is an inference).'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_praziquantel');
-- med_praziquantel
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_praziquantel', 'adult', 0, 'Schistosomiasis (S. haematobium, S. mansoni, S. intercalatum)', 'PO', '40 mg/kg', 'Single dose (or 20 mg/kg × 2, 4 h apart)', '1 day', '—', 'MSF', ''),
    ('med_praziquantel', 'adult', 1, 'Schistosomiasis (S. japonicum, S. mekongi)', 'PO', '20 mg/kg', '3 doses 4 h apart (or 30 mg/kg × 2)', '1 day', '—', 'MSF', 'S. japonicum is the PH species'),
    ('med_praziquantel', 'adult', 2, 'Schistosomiasis, mass treatment', 'PO', '600–3000 mg by height (dose pole)', 'Single dose', 'Yearly in high-risk areas', '3000 mg (≥178 cm)', 'WHO PQ label', '160–177 cm: 2400 mg'),
    ('med_praziquantel', 'adult', 3, 'Clonorchiasis / opisthorchiasis', 'PO', '25 mg/kg', '3× a day (4–6 h apart)', '1 day', '—', 'Label · DailyMed', ''),
    ('med_praziquantel', 'adult', 4, 'Lung and liver flukes (incl. paragonimiasis)', 'PO', '25 mg/kg', '3× a day', '2 days', '—', 'MSF', ''),
    ('med_praziquantel', 'adult', 5, 'Intestinal flukes', 'PO', '25 mg/kg', '3× a day', '1 day', '—', 'MSF', ''),
    ('med_praziquantel', 'adult', 6, 'Taeniasis (T. saginata, T. solium, D. latum)', 'PO', '5–10 mg/kg', 'Single dose', '1 day', '—', 'MSF', ''),
    ('med_praziquantel', 'adult', 7, 'Taeniasis (H. nana)', 'PO', '15–25 mg/kg', 'Single dose', '1 day', '—', 'MSF', ''),
    ('med_praziquantel', 'child', 8, 'Schistosomiasis (S. haematobium, S. mansoni, S. intercalatum)', 'PO', '40 mg/kg', 'Single dose (or 20 mg/kg × 2, 4 h apart)', '1 day', '—', 'MSF', 'MSF: from 4 years'),
    ('med_praziquantel', 'child', 9, 'Schistosomiasis (S. japonicum, S. mekongi)', 'PO', '20 mg/kg', '3 doses 4 h apart', '1 day', '—', 'Label · DailyMed', 'US label: from 1 year (4–6 h apart)'),
    ('med_praziquantel', 'child', 10, 'Schistosomiasis, mass treatment', 'PO', '600 mg (94–109 cm); 900 mg (110–124 cm); 1200 mg (125–137 cm); 1500 mg (138–149 cm)', 'Single dose', 'Yearly in high-risk areas', '—', 'WHO PQ label', '<94 cm/<4 y: individual medical decision'),
    ('med_praziquantel', 'child', 11, 'Taeniasis (H. nana)', 'PO', '15–25 mg/kg', 'Single dose', '1 day', '—', 'MSF', 'From 4 years')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_praziquantel');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_praziquantel', 'hepatic', 0, 'Child-Pugh B–C', 'Moderate–severe impairment (Child-Pugh B/C): much higher exposure (AUC up to about 15-fold in Child-Pugh C); use with caution and watch for adverse effects.', 'WHO PQ label'),
    ('med_praziquantel', 'elderly', 1, '', 'No special precautions required.', 'WHO PQ label'),
    ('med_praziquantel', 'pregnancy', 2, '', 'WHO recommends annual single-dose preventive chemotherapy for pregnant women after the first trimester and for lactating women where prevalence is 10% or more.', 'WHO 2022'),
    ('med_praziquantel', 'pregnancy', 3, '', 'No contraindication for schistosomiasis or taeniasis; for fluke infections, delay until after delivery unless treatment is essential now. Breastfeeding: no contraindication (MSF), but the WHO-prequalified label advises not breastfeeding on the treatment day and for the next 24 hours.', 'MSF'),
    ('med_praziquantel', 'administration', 4, '', 'Swallow whole with water during or after a meal; do not chew or hold in the mouth (bitter, may cause gagging or vomiting). The 600 mg tablet is scored into four 150 mg segments. For children under 6, tablets may be crushed or dispersed in semi-solid food or liquid and used within 1 hour.', 'Label · DailyMed'),
    ('med_praziquantel', 'monitor', 5, '', 'Watch for dizziness, somnolence and seizures on the treatment day (no driving if they occur). Monitor patients with known arrhythmias and patients with heart failure on digoxin. New neurological symptoms may unmask undiagnosed neurocysticercosis. Expect more side effects with heavy worm burden.', 'WHO PQ label')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_praziquantel');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_praziquantel', 'MSF', 'MSF Essential Drugs - Praziquantel oral', 'Medecins Sans Frontieres. Essential drugs: Praziquantel, oral.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/praziquantel-oral-16684480.html', 0),
    ('med_praziquantel', 'WHO PQ label', 'WHO Prequalification - Praziquantel 600 mg tablets SmPC (NT004)', 'WHOPAR NT004 Part 4: SmPC, Praziquantel Tablets 600 mg (Macleods).', 'https://extranet.who.int/prequal/sites/default/files/whopar_files/NT004part4.pdf', 1),
    ('med_praziquantel', 'Label · DailyMed', 'DailyMed - BILTRICIDE', 'BILTRICIDE (praziquantel) tablets, film coated. Prescribing information. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=34ce1cdd-648e-4f1e-8512-bf3d4cc22eb9', 2),
    ('med_praziquantel', 'WHO 2022', 'WHO guideline on control and elimination of human schistosomiasis (2022), via BIGG', 'WHO 2022 recommendation: annual single-dose praziquantel preventive chemotherapy where prevalence >=10%.', 'https://bigg-rec.bvsalud.org/en/recommendations/db797c50ffffecd0187f631260baf6e5d402b92e', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_praziquantel')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_praziquantel');


-- ================================================ med_prednisone  (Prednisone)
update public.medicines set description = 'Prednisone is an oral synthetic glucocorticoid prodrug converted in the liver to prednisolone. It binds glucocorticoid receptors and alters gene transcription, producing potent anti-inflammatory and immunosuppressive effects. It is used across endocrine, rheumatic, collagen-vascular, dermatologic, allergic (including asthma exacerbations), respiratory, hematologic, neoplastic and gastrointestinal inflammatory disorders. Prednisone is an intermediate-acting corticosteroid: 5 mg has about the same anti-inflammatory activity as 0.75 mg dexamethasone or 20 mg hydrocortisone. MSF lists prednisone and prednisolone together as essential drugs for the symptomatic treatment of allergic and inflammatory diseases, dosed by body weight. Short oral courses are a standard part of treating acute asthma exacerbations in adults and children.', updated_at = now()
where id = 'med_prednisone' and description = 'Prednisone is an oral synthetic glucocorticoid prodrug converted in the liver to prednisolone. It binds glucocorticoid receptors and alters gene transcription, producing potent anti-inflammatory and immunosuppressive effects. It is used across endocrine, rheumatic, collagen-vascular, dermatologic, allergic (including asthma exacerbations), respiratory, hematologic, neoplastic and gastrointestinal inflammatory disorders.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'MSF Essential Drugs - Prednisolone and prednisone, oral; Merck Manual Professional - Treatment of Acute Asthma Exacerbations; PhilHealth Konsulta medicines list (Annex D2); DailyMed - Prednisone tablets USP (Par); MSF Essential Drugs; Merck Manual Professional' else source_attribution || '; MSF Essential Drugs - Prednisolone and prednisone, oral; Merck Manual Professional - Treatment of Acute Asthma Exacerbations; PhilHealth Konsulta medicines list (Annex D2); DailyMed - Prednisone tablets USP (Par); MSF Essential Drugs; Merck Manual Professional' end
where id = 'med_prednisone' and position('MSF Essential Drugs - Prednisolone and prednisone, oral' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'indication', 'Acute exacerbations of multiple sclerosis (label dosing section)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'indication' and content = 'Acute exacerbations of multiple sclerosis (label dosing section)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'adverse', 'Pancreatitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse' and content = 'Pancreatitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'adverse', 'Thromboembolism', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse' and content = 'Thromboembolism');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'adverse', 'Kaposi''s sarcoma (may improve when the steroid is stopped)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse' and content = 'Kaposi''s sarcoma (may improve when the steroid is stopped)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'adverse', 'Aseptic necrosis of the femoral and humeral heads', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse' and content = 'Aseptic necrosis of the femoral and humeral heads');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'adverse', 'Benign intracranial hypertension', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse' and content = 'Benign intracranial hypertension');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'adverse', 'Growth retardation in children on prolonged treatment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse' and content = 'Growth retardation in children on prolonged treatment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'adverse', 'Reactivation of latent tuberculosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse' and content = 'Reactivation of latent tuberculosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'adverse', 'Strongyloides hyperinfection and activation of latent amoebiasis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'adverse' and content = 'Strongyloides hyperinfection and activation of latent amoebiasis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'contraindication', 'Active ocular herpes simplex (risk of corneal perforation)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'contraindication' and content = 'Active ocular herpes simplex (risk of corneal perforation)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'contraindication', 'Cerebral malaria (label: avoid)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'contraindication' and content = 'Cerebral malaria (label: avoid)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'contraindication', 'Active peptic ulcer unless the ulcer is being treated (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'contraindication' and content = 'Active peptic ulcer unless the ulcer is being treated (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Anticholinesterases: may cause severe weakness in myasthenia gravis.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Anticholinesterases: may cause severe weakness in myasthenia gravis.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Isoniazid: serum isoniazid levels may fall.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Isoniazid: serum isoniazid levels may fall.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Colestyramine: may increase corticosteroid clearance.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Colestyramine: may increase corticosteroid clearance.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Ciclosporin: activity of both drugs may increase.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Ciclosporin: activity of both drugs may increase.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Digoxin and other digitalis glycosides: higher arrhythmia risk from hypokalaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Digoxin and other digitalis glycosides: higher arrhythmia risk from hypokalaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Oestrogens, including oral contraceptives: reduced hepatic metabolism, stronger steroid effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Oestrogens, including oral contraceptives: reduced hepatic metabolism, stronger steroid effect.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Fluoroquinolones: higher risk of tendon rupture.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Fluoroquinolones: higher risk of tendon rupture.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Quetiapine: higher quetiapine doses may be needed.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Quetiapine: higher quetiapine doses may be needed.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Thalidomide: use cautiously; toxic epidermal necrolysis reported.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Thalidomide: use cautiously; toxic epidermal necrolysis reported.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_prednisone', 'interaction', 'Skin tests: reactions may be suppressed.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_prednisone' and kind = 'interaction' and content = 'Skin tests: reactions may be suppressed.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_prednisone', 'MSF Essential Drugs - Prednisolone and prednisone, oral', 'Medecins Sans Frontieres. Essential drugs - practical guidelines: Prednisolone and prednisone, oral.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/prednisolone-and-prednisone-oral-16684491.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_prednisone'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_prednisone' and url = 'https://medicalguidelines.msf.org/viewport/EssDr/english/prednisolone-and-prednisone-oral-16684491.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_prednisone', 'Merck Manual Professional - Treatment of Acute Asthma Exacerbations', 'Merck Manual Professional Version. Treatment of Acute Asthma Exacerbations. Merck & Co.', 'https://www.merckmanuals.com/professional/pulmonary-disorders/asthma-and-related-disorders/treatment-of-acute-asthma-exacerbations', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_prednisone'), 0)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_prednisone' and url = 'https://www.merckmanuals.com/professional/pulmonary-disorders/asthma-and-related-disorders/treatment-of-acute-asthma-exacerbations');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'malaria', 'med_prednisone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'malaria'), 0), 'caution'::condition_safety, 'Label says to avoid corticosteroids in cerebral malaria.'
where exists (select 1 from public.diseases where id = 'malaria')
  and exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'malaria' and medicine_id = 'med_prednisone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'measles', 'med_prednisone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'measles'), 0), 'caution'::condition_safety, 'Measles can take a serious or fatal course in non-immune patients on corticosteroids (label).'
where exists (select 1 from public.diseases where id = 'measles')
  and exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'measles' and medicine_id = 'med_prednisone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_prednisone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'Sodium and fluid retention; label advises caution in congestive heart failure.'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_prednisone');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_prednisone', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Label advises caution in renal insufficiency (fluid retention, hypertension).'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_prednisone');
-- med_prednisone
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_prednisone', 'adult', 0, 'Inflammatory/allergic disease', 'PO', '5–60 mg/day', 'Once a day (morning, before 9 am)', 'Until response, then taper to lowest effective dose', '—', 'Label · DailyMed', 'Starting dose depends on disease and severity'),
    ('med_prednisone', 'adult', 1, 'Inflammatory/allergic disease', 'PO', '0.5–2 mg/kg/day', 'Once a day or ÷ 2', 'Per indication; taper if >3 weeks', '80 mg/day', 'MSF', 'If >10 days, cut high starting dose to lowest effective dose fast'),
    ('med_prednisone', 'adult', 2, 'Asthma exacerbation', 'PO', '40–60 mg/day', 'Once a day or ÷ 2', '3–10 days', '—', 'Merck', '50–60 mg for severe attacks; 5–7 days usually enough'),
    ('med_prednisone', 'child', 3, 'Inflammatory/allergic disease', 'PO', '0.5–2 mg/kg/day', 'Once a day or ÷ 2', 'Per indication; taper if >3 weeks', '80 mg/day', 'MSF', ''),
    ('med_prednisone', 'child', 4, 'Asthma exacerbation', 'PO', '1–2 mg/kg/day', 'Once a day', '5 days', '<2 y 20 mg; 3–5 y 30 mg; 6–11 y 40 mg per day', 'Merck', '3–5 days usually enough in children')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_prednisone');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_prednisone', 'forms_ph', 0, '', 'Prednisone 5 mg, 10 mg and 20 mg tablets; 10 mg/5 mL suspension, 60 mL (PhilHealth Konsulta medicines list).', 'PhilHealth Konsulta'),
    ('med_prednisone', 'renal', 1, '', 'Use with caution in renal insufficiency (sodium and fluid retention); no specific dose change given.', 'Label · DailyMed'),
    ('med_prednisone', 'hepatic', 2, '', 'Effect is enhanced in cirrhosis because corticosteroid metabolism is reduced.', 'Label · DailyMed'),
    ('med_prednisone', 'elderly', 3, '', 'Start at the low end of the dose range.', 'Label · DailyMed'),
    ('med_prednisone', 'pregnancy', 4, '', 'US label: use only if benefit justifies risk (cleft palate in animal studies). MSF: no contraindication in pregnancy or breastfeeding; use the lowest effective dose, and for >40 mg/day beyond 7 days give just after a feed and wait about 4 h before the next feed.', 'MSF'),
    ('med_prednisone', 'administration', 5, '', 'Give in the morning before 9 am, with or right after food or milk to reduce stomach upset. Alternate-day therapy: twice the usual daily dose every other morning. Do not stop suddenly; taper after more than 3 weeks of treatment.', 'Label · DailyMed'),
    ('med_prednisone', 'monitor', 6, '', 'Blood pressure, weight and oedema, serum potassium, blood glucose; intraocular pressure if treatment lasts >6 weeks; growth in children; signs of infection and TB reactivation; mood and sleep changes.', 'Label · DailyMed')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_prednisone');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_prednisone', 'PhilHealth Konsulta', 'PhilHealth Konsulta medicines list (Annex D2)', 'Philippine Health Insurance Corporation. Konsulta package: Certification of Service Delivery Support (Medicines), Annex D2.', 'https://www.philhealth.gov.ph/downloads/accreditation/konsulta/AnnexD2_CertificationServiceDeliverySupportMedicines.pdf', 0),
    ('med_prednisone', 'Label · DailyMed', 'DailyMed - Prednisone tablets USP (Par)', 'Prednisone tablets, USP. Prescribing information. Par Health USA. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=10fe5a3b-84dc-4600-87c2-b80c97ce18cf', 1),
    ('med_prednisone', 'MSF', 'MSF Essential Drugs', 'Medecins Sans Frontieres. Essential drugs: Prednisolone and prednisone, oral.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/prednisolone-and-prednisone-oral-16684491.html', 2),
    ('med_prednisone', 'Merck', 'Merck Manual Professional', 'Merck Manual Professional Version. Treatment of Acute Asthma Exacerbations.', 'https://www.merckmanuals.com/professional/pulmonary-disorders/asthma-and-related-disorders/treatment-of-acute-asthma-exacerbations', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_prednisone')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_prednisone');


-- ================================================ med_propranolol  (Propranolol)
update public.medicines set description = 'Propranolol blocks beta-1 and beta-2 adrenergic receptors, slowing heart rate and reducing tremor, anxiety and sweating driven by excess thyroid hormone; at higher doses it also modestly reduces conversion of T4 to T3. It controls symptoms of hyperthyroidism while antithyroid treatment takes effect, and is used for hypertension, angina, migraine prevention and essential tremor. Propranolol is on the WHO Essential Medicines List for migraine prophylaxis (10 mg and 40 mg tablets). In thyroid storm it lowers heart rate within 2–3 hours when given orally and within minutes when given IV. An oral solution is approved for proliferating infantile haemangioma, started between 5 weeks and 5 months of age.', updated_at = now()
where id = 'med_propranolol' and description = 'Propranolol blocks beta-1 and beta-2 adrenergic receptors, slowing heart rate and reducing tremor, anxiety and sweating driven by excess thyroid hormone; at higher doses it also modestly reduces conversion of T4 to T3. It controls symptoms of hyperthyroidism while antithyroid treatment takes effect, and is used for hypertension, angina, migraine prevention and essential tremor.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC - Propranolol 40 mg film-coated tablets; Merck Manual Professional - Hyperthyroidism; US FDA label - HEMANGEOL (propranolol oral solution); WHO Electronic Essential Medicines List - Propranolol; US FDA label - HEMANGEOL' else source_attribution || '; UK SmPC - Propranolol 40 mg film-coated tablets; Merck Manual Professional - Hyperthyroidism; US FDA label - HEMANGEOL (propranolol oral solution); WHO Electronic Essential Medicines List - Propranolol; US FDA label - HEMANGEOL' end
where id = 'med_propranolol' and position('UK SmPC - Propranolol 40 mg film-coated tablets' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'indication', 'Secondary prevention after myocardial infarction', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication' and content = 'Secondary prevention after myocardial infarction');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'indication', 'Cardiac arrhythmias and anxiety-related tachycardia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication' and content = 'Cardiac arrhythmias and anxiety-related tachycardia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'indication', 'Somatic symptoms of situational and generalised anxiety', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication' and content = 'Somatic symptoms of situational and generalised anxiety');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'indication', 'Phaeochromocytoma (only together with an alpha-blocker)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication' and content = 'Phaeochromocytoma (only together with an alpha-blocker)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'indication', 'Hypertrophic obstructive cardiomyopathy; Fallot''s tetralogy in children', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication' and content = 'Hypertrophic obstructive cardiomyopathy; Fallot''s tetralogy in children');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'indication', 'Proliferating infantile haemangioma needing systemic therapy (oral solution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'indication' and content = 'Proliferating infantile haemangioma needing systemic therapy (oral solution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'adverse', 'Raynaud''s phenomenon', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse' and content = 'Raynaud''s phenomenon');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'adverse', 'Hallucinations, psychosis, confusion and depression', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse' and content = 'Hallucinations, psychosis, confusion and depression');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'adverse', 'Worsening heart failure, heart block and postural hypotension', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse' and content = 'Worsening heart failure, heart block and postural hypotension');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'adverse', 'Thrombocytopenia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse' and content = 'Thrombocytopenia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'adverse', 'Hypoglycaemia, sometimes with seizures (especially in infants)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse' and content = 'Hypoglycaemia, sometimes with seizures (especially in infants)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'adverse', 'Myasthenia gravis-like syndrome or worsening of myasthenia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse' and content = 'Myasthenia gravis-like syndrome or worsening of myasthenia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'adverse', 'More severe anaphylaxis with poor response to usual adrenaline doses', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'adverse' and content = 'More severe anaphylaxis with poor response to usual adrenaline doses');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'contraindication', 'Hypotension or metabolic acidosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication' and content = 'Hypotension or metabolic acidosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'contraindication', 'Prolonged fasting or proneness to hypoglycaemia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication' and content = 'Prolonged fasting or proneness to hypoglycaemia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'contraindication', 'Severe peripheral arterial circulatory disease', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication' and content = 'Severe peripheral arterial circulatory disease');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'contraindication', 'Sick sinus syndrome', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication' and content = 'Sick sinus syndrome');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'contraindication', 'Untreated phaeochromocytoma', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication' and content = 'Untreated phaeochromocytoma');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'contraindication', 'Prinzmetal''s angina', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication' and content = 'Prinzmetal''s angina');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'contraindication', 'Infants under 2 kg or with corrected age under 5 weeks (oral solution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'contraindication' and content = 'Infants under 2 kg or with corrected age under 5 weeks (oral solution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'interaction', 'Rizatriptan: levels rise by about 70–80%; use rizatriptan 5 mg.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction' and content = 'Rizatriptan: levels rise by about 70–80%; use rizatriptan 5 mg.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'interaction', 'Nifedipine and other dihydropyridines: more hypotension; heart failure in latent cardiac insufficiency.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction' and content = 'Nifedipine and other dihydropyridines: more hypotension; heart failure in latent cardiac insufficiency.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'interaction', 'Class I antiarrhythmics, amiodarone and digoxin: additive effects on conduction and contractility.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction' and content = 'Class I antiarrhythmics, amiodarone and digoxin: additive effects on conduction and contractility.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'interaction', 'Lidocaine: levels rise by about 30%; avoid the combination.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction' and content = 'Lidocaine: levels rise by about 30%; avoid the combination.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'interaction', 'Adrenaline and other sympathomimetics: may counteract beta-blockade; give parenteral adrenaline with care.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction' and content = 'Adrenaline and other sympathomimetics: may counteract beta-blockade; give parenteral adrenaline with care.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'interaction', 'Cimetidine, hydralazine, alcohol and chlorpromazine: raise propranolol levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction' and content = 'Cimetidine, hydralazine, alcohol and chlorpromazine: raise propranolol levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'interaction', 'Ergotamine and related drugs: risk of vasospastic reactions.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction' and content = 'Ergotamine and related drugs: risk of vasospastic reactions.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'interaction', 'NSAIDs (ibuprofen, indometacin): may blunt the blood-pressure-lowering effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction' and content = 'NSAIDs (ibuprofen, indometacin): may blunt the blood-pressure-lowering effect.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'interaction', 'Rifampicin, theophylline, warfarin, thioridazine, quinidine and propafenone: altered levels; dose adjustment may be needed.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'interaction' and content = 'Rifampicin, theophylline, warfarin, thioridazine, quinidine and propafenone: altered levels; dose adjustment may be needed.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_propranolol', 'brand_intl', 'Hemangeol', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'brand_intl'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol' and kind = 'brand_intl' and content = 'Hemangeol');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_propranolol', 'UK SmPC - Propranolol 40 mg film-coated tablets', 'Ipca Laboratories UK Ltd. Propranolol 40 mg film-coated tablets - Summary of Product Characteristics. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=propranolol#emc-101996', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_propranolol'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_propranolol' and url = 'https://products.mhra.gov.uk/search/?search=propranolol#emc-101996');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_propranolol', 'Merck Manual Professional - Hyperthyroidism', 'Merck Manual Professional Version. Hyperthyroidism. Merck & Co.', 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/hyperthyroidism', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_propranolol'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_propranolol' and url = 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/hyperthyroidism');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_propranolol', 'US FDA label - HEMANGEOL (propranolol oral solution)', 'Pierre Fabre. HEMANGEOL (propranolol hydrochloride) oral solution. Prescribing information. US FDA; 2021.', 'https://www.accessdata.fda.gov/drugsatfda_docs/label/2021/205410s006lbl.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_propranolol'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_propranolol' and url = 'https://www.accessdata.fda.gov/drugsatfda_docs/label/2021/205410s006lbl.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_propranolol', 'WHO Electronic Essential Medicines List - Propranolol', 'World Health Organization. eEML - Electronic Essential Medicines List: Propranolol.', 'https://list.essentialmeds.org/medicines/392', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_propranolol'), 0)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_propranolol' and url = 'https://list.essentialmeds.org/medicines/392');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hypertension', 'med_propranolol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hypertension'), 0), 'safe'::condition_safety, 'Licensed indication (usual 160–320 mg/day).'
where exists (select 1 from public.diseases where id = 'hypertension')
  and exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hypertension' and medicine_id = 'med_propranolol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'migraine', 'med_propranolol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'migraine'), 0), 'safe'::condition_safety, 'Licensed for migraine prophylaxis; on the WHO EML for this use.'
where exists (select 1 from public.diseases where id = 'migraine')
  and exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'migraine' and medicine_id = 'med_propranolol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_coronary_syndrome', 'med_propranolol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome'), 0), 'safe'::condition_safety, 'Licensed for secondary prevention after MI, started 5–21 days after the infarct; contraindicated in cardiogenic shock.'
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome' and medicine_id = 'med_propranolol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'asthma', 'med_propranolol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'asthma'), 0), 'avoid'::condition_safety, 'Contraindicated with a history of bronchial asthma or bronchospasm; fatal bronchospasm reported.'
where exists (select 1 from public.diseases where id = 'asthma')
  and exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'asthma' and medicine_id = 'med_propranolol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_propranolol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'Contraindicated in uncontrolled heart failure; controlled heart failure only with caution.'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_propranolol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_propranolol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'Masks hypoglycaemia (tachycardia) and may prolong insulin-induced hypoglycaemia.'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_propranolol');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'copd', 'med_propranolol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'copd'), 0), 'caution'::condition_safety, 'Bronchospasm risk (label contraindicates asthma/bronchospasm history; applying caution to COPD is an inference).'
where exists (select 1 from public.diseases where id = 'copd')
  and exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'copd' and medicine_id = 'med_propranolol');
-- med_propranolol
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_propranolol', 'adult', 0, 'Hypertension', 'PO', '80 mg', '2× a day', 'Long-term', '320 mg/day (usual 160–320 mg)', 'Label · UK SmPC', 'Increase at weekly intervals'),
    ('med_propranolol', 'adult', 1, 'Angina', 'PO', '40 mg', '2–3× a day', 'Long-term', '—', 'Label · UK SmPC', 'Usual 120–240 mg/day; increase weekly'),
    ('med_propranolol', 'adult', 2, 'Migraine prophylaxis / essential tremor', 'PO', '40 mg', '2–3× a day', 'Long-term', '—', 'Label · UK SmPC', 'Usual 80–160 mg/day'),
    ('med_propranolol', 'adult', 3, 'Arrhythmia, thyrotoxicosis, HOCM', 'PO', '10–40 mg', '3–4× a day', 'Per response', '—', 'Label · UK SmPC', ''),
    ('med_propranolol', 'adult', 4, 'Anxiety', 'PO', '40 mg', 'Once a day (situational); 2–3× a day (generalised)', 'Review at 6–12 months', '—', 'Label · UK SmPC', ''),
    ('med_propranolol', 'adult', 5, 'After myocardial infarction', 'PO', '40 mg, then 80 mg', '4× a day for 2–3 days, then 2× a day', 'Long-term', '—', 'Label · UK SmPC', 'Start 5–21 days after the infarct'),
    ('med_propranolol', 'adult', 6, 'Portal hypertension', 'PO', '40 mg, up to 80 mg', '2× a day', 'Long-term', '160 mg 2× a day', 'Label · UK SmPC', 'Aim for ~25% fall in resting heart rate'),
    ('med_propranolol', 'adult', 7, 'Thyroid storm', 'PO', '60–80 mg', 'Every 4–6 h', 'Until controlled', '—', 'Merck', 'Adjust to heart rate and blood pressure'),
    ('med_propranolol', 'adult', 8, 'Thyroid storm', 'IV', '0.5–1 mg over 10–15 min', 'Every 4 h', 'Until oral possible', '1 mg/min rate', 'Merck', 'Close monitoring'),
    ('med_propranolol', 'child', 9, 'Arrhythmia, thyrotoxicosis, phaeochromocytoma', 'PO', '0.25–0.5 mg/kg', '3–4× a day', 'Per response', '—', 'Label · UK SmPC', ''),
    ('med_propranolol', 'child', 10, 'Migraine prophylaxis (<12 y)', 'PO', '20 mg', '2–3× a day', 'Long-term', '—', 'Label · UK SmPC', '≥12 y: adult dose'),
    ('med_propranolol', 'child', 11, 'Fallot''s tetralogy', 'PO', 'Up to 1 mg/kg', '3–4× a day', 'Per response', '—', 'Label · UK SmPC', ''),
    ('med_propranolol', 'child', 12, 'Infantile haemangioma (age 5 wk–5 mo)', 'PO', '0.6 mg/kg → 1.1 mg/kg (wk 2) → 1.7 mg/kg (from wk 3)', '2× a day, ≥9 h apart', '6 months', '1.7 mg/kg 2× a day', 'Label · US FDA', 'Oral solution; give during or right after a feed')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_propranolol');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_propranolol', 'renal', 0, '', 'Half-life may be prolonged: take care when starting and choosing the first dose. No specific dose change given.', 'Label · UK SmPC'),
    ('med_propranolol', 'hepatic', 1, '', 'Half-life may be prolonged: start carefully; caution in decompensated cirrhosis. May worsen hepatic encephalopathy in portal hypertension.', 'Label · UK SmPC'),
    ('med_propranolol', 'elderly', 2, '', 'Start at the lowest dose and adjust to response.', 'Label · UK SmPC'),
    ('med_propranolol', 'pregnancy', 3, '', 'Avoid unless essential: reduced placental perfusion, risk of fetal death, premature delivery, and neonatal hypoglycaemia and bradycardia. Breastfeeding not recommended.', 'Label · UK SmPC'),
    ('med_propranolol', 'administration', 4, '', 'Taper over 7–14 days when stopping. If beta-blockade is to be stopped before surgery, stop at least 24 h beforehand. Infant oral solution: give during or right after a feed and skip the dose if the child is not eating or is vomiting.', 'Label · UK SmPC'),
    ('med_propranolol', 'monitor', 5, '', 'Heart rate and blood pressure (stop if severe or symptomatic bradycardia/hypotension); signs of heart failure; blood glucose in diabetes and in infants; wheeze. Infants: check heart rate and blood pressure for 2 h after starting or increasing the dose. Note it may mask thyrotoxicosis signs and interferes with bilirubin and catecholamine assays.', 'Label · US FDA')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_propranolol');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_propranolol', 'Label · UK SmPC', 'UK SmPC - Propranolol 40 mg film-coated tablets', 'Ipca Laboratories UK Ltd. Propranolol 40 mg film-coated tablets - SmPC. emc.', 'https://products.mhra.gov.uk/search/?search=propranolol#emc-101996', 0),
    ('med_propranolol', 'Merck', 'Merck Manual Professional - Hyperthyroidism', 'Merck Manual Professional Version. Hyperthyroidism.', 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/hyperthyroidism', 1),
    ('med_propranolol', 'Label · US FDA', 'US FDA label - HEMANGEOL', 'HEMANGEOL (propranolol hydrochloride) oral solution. Prescribing information. US FDA; 2021.', 'https://www.accessdata.fda.gov/drugsatfda_docs/label/2021/205410s006lbl.pdf', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_propranolol')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_propranolol');


update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
