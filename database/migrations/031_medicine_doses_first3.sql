-- 031_medicine_doses_first3.sql  -  dosage table rows for: med_aciclovir, med_amoxicillin, med_paracetamol
-- Needs 030_medicine_doses.sql first. Fills a medicine only if it has no rows yet;
-- medicines.dosage_text is not touched. Safe to run twice.

begin;

-- med_aciclovir
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_aciclovir', 'adult', 0, 'Herpes simplex, treatment', 'PO', '200 mg', '5× a day, about every 4 h, skip the night dose', '5 days; longer for a severe first episode', '400 mg/dose if severely immunocompromised', 'Label · UK SmPC', 'Cold sores, first or recurrent genital herpes'),
    ('med_aciclovir', 'adult', 1, 'Herpes simplex, suppression', 'PO', '400 mg', '2× a day (or 200 mg 4× a day)', 'Pause every 6–12 months to review', '', 'Label · UK SmPC', 'Frequent recurrences, immunocompetent'),
    ('med_aciclovir', 'adult', 2, 'Herpes simplex, prophylaxis', 'PO', '200 mg', '4× a day, about every 6 h', 'While at risk', '400 mg/dose if severe', 'Label · UK SmPC', 'Immunocompromised'),
    ('med_aciclovir', 'adult', 3, 'Varicella and herpes zoster', 'PO', '800 mg', '5× a day, about every 4 h, skip the night dose', '7 days', '800 mg/dose', 'Label · UK SmPC', ''),
    ('med_aciclovir', 'child', 4, 'Herpes simplex, treatment', 'PO', '≥ 2 y: 200 mg
< 2 y: 100 mg', '5× a day', '5 days', 'Adult dose', 'Label · UK SmPC', 'Neonatal herpes: IV only'),
    ('med_aciclovir', 'child', 5, 'Varicella', 'PO', '20 mg/kg', '4× a day', '5 days', '800 mg/dose', 'Label · UK SmPC', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_aciclovir');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_aciclovir', 'renal', 0, 'CrCl 10–25', 'Zoster: 800 mg every 8 h', 'Label · UK SmPC'),
    ('med_aciclovir', 'renal', 1, 'CrCl < 10', 'Zoster: 800 mg every 12 h. Herpes simplex: 200 mg every 12 h', 'Label · UK SmPC'),
    ('med_aciclovir', 'elderly', 2, '', 'Adjust for kidney function and keep well hydrated.', 'Label · UK SmPC'),
    ('med_aciclovir', 'monitor', 3, '', 'Kidney function in older adults and in kidney disease', ''),
    ('med_aciclovir', 'monitor', 4, '', 'Fluid intake: keep the patient hydrated', '')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_aciclovir');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_aciclovir', 'Label · UK SmPC', 'Aciclovir 400 mg Tablets – Summary of Product Characteristics', 'Aciclovir 400 mg Tablets. Summary of Product Characteristics, section 4.2 Posology. electronic medicines compendium (emc), UK.', 'https://www.medicines.org.uk/emc/product/2352/smpc/print', 0)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_aciclovir');

-- med_amoxicillin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_amoxicillin', 'adult', 0, 'Acute bacterial sinusitis', 'PO', '250–500 mg', 'Every 8 h (or 750 mg – 1 g every 12 h)', 'As short as possible; follow guidelines', '', 'Label · UK SmPC', 'Also asymptomatic bacteriuria in pregnancy. Adults and children 40 kg and over'),
    ('med_amoxicillin', 'adult', 1, 'Acute otitis media', 'PO', '500 mg', 'Every 8 h (or 750 mg – 1 g every 12 h)', 'As short as possible; follow guidelines', '', 'Label · UK SmPC', ''),
    ('med_amoxicillin', 'adult', 2, 'Streptococcal tonsillitis or pharyngitis; acute exacerbation of chronic bronchitis', 'PO', '750 mg – 1 g', 'Every 8 h', '10 days', '', 'Label · UK SmPC', 'Severe infections'),
    ('med_amoxicillin', 'adult', 3, 'Community-acquired pneumonia', 'PO', '500 mg – 1 g', 'Every 8 h', 'As short as possible; follow guidelines', '', 'Label · UK SmPC', ''),
    ('med_amoxicillin', 'adult', 4, 'Acute pyelonephritis; dental abscess with spreading cellulitis', 'PO', '750 mg – 1 g', 'Every 8 h', 'As short as possible; follow guidelines', '', 'Label · UK SmPC', 'Severe infections'),
    ('med_amoxicillin', 'adult', 5, 'Acute cystitis', 'PO', '3 g', '2× a day', '1 day', '', 'Label · UK SmPC', ''),
    ('med_amoxicillin', 'adult', 6, 'Typhoid and paratyphoid fever', 'PO', '500 mg – 2 g', 'Every 8 h', 'Follow guidelines', '', 'Label · UK SmPC', ''),
    ('med_amoxicillin', 'adult', 7, 'Endocarditis prophylaxis', 'PO', '2 g', 'Once, 30–60 min before the procedure', 'Single dose', '', 'Label · UK SmPC', ''),
    ('med_amoxicillin', 'adult', 8, 'H. pylori eradication', 'PO', '750 mg – 1 g', '2× a day', '7 days', '', 'Label · UK SmPC', 'With a proton pump inhibitor and another antibiotic'),
    ('med_amoxicillin', 'adult', 9, 'Lyme disease, early stage', 'PO', '500 mg – 1 g', 'Every 8 h', '14 days (10–21)', '4 g/day', 'Label · UK SmPC', ''),
    ('med_amoxicillin', 'child', 10, 'Sinusitis, otitis media, pneumonia, cystitis, pyelonephritis, dental abscess', 'PO', '20–90 mg/kg/day, divided', 'Divided doses; 2× a day only at the upper range', 'As short as possible; follow guidelines', '', 'Label · UK SmPC', 'Under 40 kg (40 kg and over: adult dose)'),
    ('med_amoxicillin', 'child', 11, 'Streptococcal tonsillitis or pharyngitis', 'PO', '40–90 mg/kg/day, divided', 'Divided doses; 2× a day only at the upper range', 'As short as possible; follow guidelines', '', 'Label · UK SmPC', ''),
    ('med_amoxicillin', 'child', 12, 'Typhoid and paratyphoid fever', 'PO', '100 mg/kg/day ÷ 3', 'Every 8 h', 'Follow guidelines', '', 'Label · UK SmPC', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_amoxicillin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_amoxicillin', 'renal', 0, 'GFR > 30', 'No change', 'Label · UK SmPC'),
    ('med_amoxicillin', 'renal', 1, 'GFR 10–30', '40 kg and over: at most 500 mg 2× a day. Under 40 kg: 15 mg/kg 2× a day', 'Label · UK SmPC'),
    ('med_amoxicillin', 'renal', 2, 'GFR < 10', '40 kg and over: at most 500 mg a day. Under 40 kg: 15 mg/kg once a day', 'Label · UK SmPC'),
    ('med_amoxicillin', 'renal', 3, 'Haemodialysis', '40 kg and over: 500 mg every 24 h, plus 500 mg before and 500 mg after each session. Under 40 kg: 15 mg/kg once a day (max 500 mg), plus 15 mg/kg before and after', 'Label · UK SmPC'),
    ('med_amoxicillin', 'renal', 4, 'Peritoneal dialysis', 'At most 500 mg a day', 'Label · UK SmPC'),
    ('med_amoxicillin', 'hepatic', 5, '', 'Dose with caution and check liver function regularly.', 'Label · UK SmPC'),
    ('med_amoxicillin', 'elderly', 6, '', 'No dose change needed.', 'Label · UK SmPC'),
    ('med_amoxicillin', 'administration', 7, '', 'Can be taken with or without food; food does not affect absorption.', 'Label · UK SmPC'),
    ('med_amoxicillin', 'forms_ph', 8, '', 'Powder for suspension 250 mg/5 mL, 60 mL bottle (add 41 mL water)', 'Label · FDA PH'),
    ('med_amoxicillin', 'monitor', 9, '', 'Ask about penicillin allergy before the first dose', ''),
    ('med_amoxicillin', 'monitor', 10, '', 'Rash or diarrhoea during treatment', ''),
    ('med_amoxicillin', 'monitor', 11, '', 'Avoid if infectious mononucleosis is suspected (it can cause a rash)', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_amoxicillin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_amoxicillin', 'Label · UK SmPC', 'Amoxicillin 250 mg/5 ml Powder for Oral Suspension – SmPC', 'Amoxicillin 250 mg/5 ml Powder for Oral Suspension Sugar Free (Flamingo Pharma UK Ltd). Summary of Product Characteristics, section 4.2 Posology. electronic medicines compendium (emc), UK.', 'https://www.medicines.org.uk/emc/product/14145/smpc/print', 0),
    ('med_amoxicillin', 'Label · FDA PH', 'FDA Philippines Verification Portal – amoxicillin 250 mg/5 mL', 'Amoxicillin (as trihydrate) 250 mg/5 mL powder for oral suspension, registration DRP-10727. Search the registration number on the FDA Philippines Verification Portal (the direct PDF link no longer opens).', 'https://verification.fda.gov.ph/', 1)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_amoxicillin');

-- med_paracetamol
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_paracetamol', 'adult', 0, 'Fever, mild to moderate pain', 'PO', '500 mg – 1 g', 'Every 4–6 h as needed, at least 4 h apart', 'As needed', '1 g/dose · 4 g/day', 'bpac NZ 2018', ''),
    ('med_paracetamol', 'adult', 1, 'Same, with a risk factor', 'PO', 'Up to 60 mg/kg/day', 'Every 4–6 h', 'As needed', '2 g/day', 'Label · HPRA', 'Under 50 kg, liver disease, Gilbert''s, dehydration, malnutrition, chronic alcohol use'),
    ('med_paracetamol', 'child', 2, 'Fever, mild to moderate pain', 'PO', '15 mg/kg', 'Every 4–6 h as needed', 'As needed', '1 g/dose · 60 mg/kg/day, not over 4 g', 'bpac NZ 2018', '1 month to 18 years'),
    ('med_paracetamol', 'child', 3, 'Underweight or malnourished child', 'PO', '10 mg/kg', 'Every 4–6 h, or longer apart', 'As needed', '60 mg/kg/day', 'bpac NZ 2018', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_paracetamol');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_paracetamol', 'renal', 0, 'GFR 10–50', '500 mg every 6 h', 'Label · HPRA'),
    ('med_paracetamol', 'renal', 1, 'GFR < 10', '500 mg every 8 h; at least 6 h between doses', 'Label · HPRA'),
    ('med_paracetamol', 'monitor', 2, '', 'Add up paracetamol from every product taken, including cold and flu mixes', ''),
    ('med_paracetamol', 'monitor', 3, '', 'Liver risk in malnourished or acutely unwell young children', 'bpac NZ 2018')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_paracetamol');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_paracetamol', 'bpac NZ 2018', 'bpac NZ – Paracetamol dosing for children', 'Best Practice Advocacy Centre New Zealand. Paracetamol dosing. bpac NZ; 2018.', 'https://bpac.org.nz/2018/docs/paracetamol.pdf', 0),
    ('med_paracetamol', 'Label · HPRA', 'Paracetamol 500 mg tablets – SmPC (HPRA)', 'Paralief 500 mg film-coated tablets. Summary of Product Characteristics, section 4.2. Health Products Regulatory Authority, Ireland.', 'https://assets.hpra.ie/products/Human/37091/Licence_PA0126-020-008_24022025151042.pdf', 1)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_paracetamol')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_paracetamol');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
