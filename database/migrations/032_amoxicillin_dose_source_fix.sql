-- 032_amoxicillin_dose_source_fix.sql  -  amoxicillin dosage rows from a working, verified source
-- Needs 030 (and 031). The old FDA PH PDF link gave 404, so amoxicillin's rows now
-- follow the UK SmPC (medicines.org.uk/emc/product/14145, section 4.2).
-- Replaces the rows only while they are still the untouched old sample; otherwise
-- only the dead link is fixed. Safe to run twice.

begin;

create temporary table _amox_old on commit drop as
select exists (select 1 from public.medicine_dose_sources
               where medicine_id = 'med_amoxicillin' and url = 'https://verification.fda.gov.ph/files/DRP-10727_PI_01.pdf')
   and not exists (select 1 from public.medicine_doses
                   where medicine_id = 'med_amoxicillin' and source <> 'Label · FDA PH') as untouched;

delete from public.medicine_doses      where medicine_id = 'med_amoxicillin' and (select untouched from _amox_old);
delete from public.medicine_dose_notes where medicine_id = 'med_amoxicillin' and (select untouched from _amox_old);
delete from public.medicine_dose_sources where medicine_id = 'med_amoxicillin' and (select untouched from _amox_old);

-- Edited by an admin: keep their rows, just fix the dead link.
update public.medicine_dose_sources
   set url = 'https://verification.fda.gov.ph/', source_name = 'FDA Philippines Verification Portal – amoxicillin 250 mg/5 mL', updated_at = now()
 where medicine_id = 'med_amoxicillin' and url = 'https://verification.fda.gov.ph/files/DRP-10727_PI_01.pdf';

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

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
