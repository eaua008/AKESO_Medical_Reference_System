-- 036_medicines_review_04.sql  -  medicine review b04: med_ibuprofen, med_isoniazid, med_ivermectin, med_loperamide, med_losartan, med_mefenamic_acid, med_metformin, med_methimazole, med_metoprolol, med_metronidazole
-- Adds only: longer descriptions, new facts, references, disease links, and dosage
-- tables (for medicines that have none yet). Nothing is deleted or reworded.
-- Needs 030_medicine_doses.sql first. Safe to run twice (every insert is guarded).

begin;

-- ================================================ med_ibuprofen  (Ibuprofen)
update public.medicines set description = 'Ibuprofen is a non-selective, reversible inhibitor of COX-1 and COX-2 that reduces prostaglandin synthesis, producing analgesic, antipyretic and anti-inflammatory effects. It is widely used for mild-to-moderate pain, fever, dysmenorrhea and inflammatory joint conditions. In the Philippines, where dengue is endemic, NSAIDs such as ibuprofen are not recommended in suspected or confirmed dengue because they raise bleeding risk; PhilHealth''s 2026 dengue quality standards and DOH advice name paracetamol as the antipyretic of choice, and DOH advises avoiding ibuprofen until dengue is ruled out. Ibuprofen can also mask fever and pain, which may delay recognition of a worsening infection.', updated_at = now()
where id = 'med_ibuprofen' and description = 'Ibuprofen is a non-selective, reversible inhibitor of COX-1 and COX-2 that reduces prostaglandin synthesis, producing analgesic, antipyretic and anti-inflammatory effects. It is widely used for mild-to-moderate pain, fever, dysmenorrhea and inflammatory joint conditions.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'PhilHealth Dengue Quality Standards; WHO Fact Sheet - Dengue; UK SmPC (emc) - tablets; UK SmPC (emc) - suspension; Philippine National Formulary (PNF) EML' else source_attribution || '; PhilHealth Dengue Quality Standards; WHO Fact Sheet - Dengue; UK SmPC (emc) - tablets; UK SmPC (emc) - suspension; Philippine National Formulary (PNF) EML' end
where id = 'med_ibuprofen' and position('PhilHealth Dengue Quality Standards' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'indication', 'Migraine attacks (400 mg single dose)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'indication' and content = 'Migraine attacks (400 mg single dose)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'indication', 'Juvenile idiopathic (rheumatoid) arthritis, under prescription (higher mg/kg doses)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'indication' and content = 'Juvenile idiopathic (rheumatoid) arthritis, under prescription (higher mg/kg doses)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'indication', 'Post-immunisation fever in infants (limited to 2 doses)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'indication' and content = 'Post-immunisation fever in infants (limited to 2 doses)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'adverse', 'Severe skin reactions: SJS, TEN, DRESS, AGEP (mostly in the first month)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse' and content = 'Severe skin reactions: SJS, TEN, DRESS, AGEP (mostly in the first month)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'adverse', 'Interstitial nephritis, nephrotic syndrome; renal tubular acidosis and hypokalaemia with prolonged high doses', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse' and content = 'Interstitial nephritis, nephrotic syndrome; renal tubular acidosis and hypokalaemia with prolonged high doses');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'adverse', 'Rare blood dyscrasias (agranulocytosis, pancytopenia)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse' and content = 'Rare blood dyscrasias (agranulocytosis, pancytopenia)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'adverse', 'Kounis syndrome (allergic acute coronary syndrome) has been reported', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse' and content = 'Kounis syndrome (allergic acute coronary syndrome) has been reported');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'adverse', 'Masking of fever and pain, delaying treatment of infection', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'adverse' and content = 'Masking of fever and pain, delaying treatment of infection');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'contraindication', 'Suspected or confirmed dengue: NSAIDs are not recommended (PhilHealth / DOH / WHO); use paracetamol', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication' and content = 'Suspected or confirmed dengue: NSAIDs are not recommended (PhilHealth / DOH / WHO); use paracetamol');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'contraindication', 'Previous NSAID-related GI bleeding or perforation; active or recurrent peptic ulcer or haemorrhage', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication' and content = 'Previous NSAID-related GI bleeding or perforation; active or recurrent peptic ulcer or haemorrhage');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'contraindication', 'Severe heart failure (NYHA class IV)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication' and content = 'Severe heart failure (NYHA class IV)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'contraindication', 'Severe renal failure or severe hepatic failure', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication' and content = 'Severe renal failure or severe hepatic failure');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'contraindication', 'Last trimester of pregnancy', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication' and content = 'Last trimester of pregnancy');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'contraindication', 'Significant dehydration (vomiting, diarrhoea or poor fluid intake)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication' and content = 'Significant dehydration (vomiting, diarrhoea or poor fluid intake)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'contraindication', 'Cerebrovascular or other active bleeding; unexplained blood-formation disorders', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'contraindication' and content = 'Cerebrovascular or other active bleeding; unexplained blood-formation disorders');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'interaction', 'Corticosteroids and other NSAIDs (including COX-2 inhibitors): increased GI ulceration and bleeding.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction' and content = 'Corticosteroids and other NSAIDs (including COX-2 inhibitors): increased GI ulceration and bleeding.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'interaction', 'Quinolone antibiotics: possible increased risk of convulsions.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction' and content = 'Quinolone antibiotics: possible increased risk of convulsions.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'interaction', 'Ciclosporin and tacrolimus: increased nephrotoxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction' and content = 'Ciclosporin and tacrolimus: increased nephrotoxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'interaction', 'Zidovudine: increased haematological toxicity (haemarthrosis/haematoma in haemophiliacs).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction' and content = 'Zidovudine: increased haematological toxicity (haemarthrosis/haematoma in haemophiliacs).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'interaction', 'CYP2C9 inhibitors (fluconazole, voriconazole): higher ibuprofen exposure; consider dose reduction.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction' and content = 'CYP2C9 inhibitors (fluconazole, voriconazole): higher ibuprofen exposure; consider dose reduction.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'interaction', 'Digoxin and phenytoin: plasma levels may rise.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction' and content = 'Digoxin and phenytoin: plasma levels may rise.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'interaction', 'Sulfonylureas: possible enhanced hypoglycaemic effect; monitor glucose.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction' and content = 'Sulfonylureas: possible enhanced hypoglycaemic effect; monitor glucose.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ibuprofen', 'interaction', 'Mifepristone: avoid NSAIDs for 8–12 days after mifepristone.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ibuprofen' and kind = 'interaction' and content = 'Mifepristone: avoid NSAIDs for 8–12 days after mifepristone.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ibuprofen', 'PhilHealth Dengue Quality Standards', 'Philippine Health Insurance Corporation. Quality Standards on the Diagnosis and Management of Dengue (Adult and Children) as a Reference of the Corporation. PhilHealth Circular No. 2026-0009.', 'https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ibuprofen'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ibuprofen' and url = 'https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ibuprofen', 'WHO Fact Sheet - Dengue', 'World Health Organization. Dengue and severe dengue. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ibuprofen'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ibuprofen' and url = 'https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ibuprofen', 'UK SmPC (emc) - tablets', 'Ibuprofen 400 mg film-coated tablets (POM) - Summary of Product Characteristics. Milpharm Ltd. Electronic medicines compendium (emc), revised June 2026.', 'https://products.mhra.gov.uk/search/?search=ibuprofen#emc-7020', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ibuprofen'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ibuprofen' and url = 'https://products.mhra.gov.uk/search/?search=ibuprofen#emc-7020');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ibuprofen', 'UK SmPC (emc) - suspension', 'Ibuprofen 100 mg/5 ml Oral Suspension - Summary of Product Characteristics. Pinewood Laboratories Ltd. Electronic medicines compendium (emc), revised August 2024.', 'https://products.mhra.gov.uk/search/?search=ibuprofen#emc-4560', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ibuprofen'), 0)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ibuprofen' and url = 'https://products.mhra.gov.uk/search/?search=ibuprofen#emc-4560');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'cholera', 'med_ibuprofen', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'cholera'), 0), 'avoid'::condition_safety, 'UK SmPC contraindicates ibuprofen in significant dehydration from vomiting or diarrhoea, with renal risk in dehydrated children (applied to cholera by inference).'
where exists (select 1 from public.diseases where id = 'cholera')
  and exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.disease_medicines where disease_id = 'cholera' and medicine_id = 'med_ibuprofen');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'ischemic_stroke', 'med_ibuprofen', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'ischemic_stroke'), 0), 'caution'::condition_safety, 'UK SmPC: small increased risk of arterial thrombotic events such as MI and stroke, mainly at high doses (2400 mg/day); use lowest dose for shortest time.'
where exists (select 1 from public.diseases where id = 'ischemic_stroke')
  and exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.disease_medicines where disease_id = 'ischemic_stroke' and medicine_id = 'med_ibuprofen');
-- med_ibuprofen
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_ibuprofen', 'adult', 0, 'Pain, fever (≥12 y, ≥40 kg)', 'PO', '200–400 mg', 'Every 6 h as needed (3–4× a day)', 'Short term', '1,200 mg/day (OTC)', 'Label · UK SmPC', 'Not in suspected dengue: use paracetamol'),
    ('med_ibuprofen', 'adult', 1, 'Migraine', 'PO', '400 mg', 'Single dose; repeat 400 mg after ≥6 h if needed', '—', '1,200 mg/day', 'Label · UK SmPC', ''),
    ('med_ibuprofen', 'adult', 2, 'Primary dysmenorrhoea', 'PO', '200–400 mg', '1–3× a day', '—', '1,200 mg/day', 'Label · UK SmPC', ''),
    ('med_ibuprofen', 'adult', 3, 'Rheumatic disease', 'PO', '1,200–1,800 mg/day ÷ 3–4', '3–4× a day', 'Maintenance 600–1,200 mg/day', '2,400 mg/day', 'Label · UK SmPC', 'Max single dose 800 mg'),
    ('med_ibuprofen', 'child', 4, 'Pain, fever (3 mo–12 y)', 'PO', '20 mg/kg/day ÷ 3–4', 'Every 6–8 h', '≤3 days without review', '—', 'Label · UK SmPC susp', 'Not under 3 months'),
    ('med_ibuprofen', 'child', 5, 'Pain, fever, 3–6 mo (>5 kg)', 'PO', '50 mg (2.5 mL of 100 mg/5 mL)', 'Up to 3× in 24 h', 'Max 24 h', '150 mg/day', 'Label · UK SmPC susp', 'See doctor within 24 h if symptoms persist'),
    ('med_ibuprofen', 'child', 6, 'Pain, fever, 6 mo–1 y', 'PO', '50 mg (2.5 mL)', '3–4× a day', '≤3 days', '200 mg/day', 'Label · UK SmPC susp', ''),
    ('med_ibuprofen', 'child', 7, 'Pain, fever, 1–4 y', 'PO', '100 mg (5 mL)', '3× a day', '≤3 days', '300 mg/day', 'Label · UK SmPC susp', ''),
    ('med_ibuprofen', 'child', 8, 'Pain, fever, 4–7 y', 'PO', '150 mg (7.5 mL)', '3× a day', '≤3 days', '450 mg/day', 'Label · UK SmPC susp', ''),
    ('med_ibuprofen', 'child', 9, 'Pain, fever, 7–12 y', 'PO', '200 mg (10 mL)', '3× a day', '≤3 days', '600 mg/day', 'Label · UK SmPC susp', ''),
    ('med_ibuprofen', 'child', 10, 'Juvenile rheumatoid arthritis', 'PO', '30–40 mg/kg/day ÷ 3–4', '3–4× a day', '—', '—', 'Label · UK SmPC susp', 'Prescription only')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_ibuprofen');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_ibuprofen', 'renal', 0, '', 'Mild to moderate impairment: lowest dose for the shortest time and monitor renal function. Contraindicated in severe renal failure.', 'Label · UK SmPC'),
    ('med_ibuprofen', 'hepatic', 1, '', 'Mild to moderate impairment: lowest dose for the shortest time and monitor liver function. Contraindicated in severe hepatic failure.', 'Label · UK SmPC'),
    ('med_ibuprofen', 'elderly', 2, '', 'Higher risk of serious GI bleeding and perforation: lowest dose, shortest duration, review regularly.', 'Label · UK SmPC'),
    ('med_ibuprofen', 'pregnancy', 3, '', 'Avoid in the first and second trimesters unless clearly needed. From week 20, risk of oligohydramnios and ductus arteriosus constriction (consider antenatal monitoring after several days of use). Contraindicated in the third trimester. Short courses are acceptable in breastfeeding.', 'Label · UK SmPC'),
    ('med_ibuprofen', 'monitor', 4, '', 'Before giving for fever in the Philippines, consider dengue: NSAIDs (ibuprofen, celecoxib, aspirin) are not recommended; give paracetamol instead. Watch for GI bleeding signs (melena, haematemesis), blood pressure, urine output and hydration, especially in children with vomiting or diarrhoea.', 'PhilHealth 2026'),
    ('med_ibuprofen', 'administration', 5, '', 'Children from 6 months: see a doctor if needed for more than 3 days; adults: if needed for more than 10 days. Keep at least 4 h between doses.', 'Label · UK SmPC susp'),
    ('med_ibuprofen', 'forms_ph', 6, '', '200 mg and 400 mg tablet; 100 mg/5 mL syrup/suspension (60 mL); 200 mg/5 mL suspension (60 mL).', 'PNF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_ibuprofen');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_ibuprofen', 'Label · UK SmPC', 'UK SmPC (emc) - tablets', 'Ibuprofen 400 mg film-coated tablets (POM) - SmPC. Milpharm Ltd, 2026.', 'https://products.mhra.gov.uk/search/?search=ibuprofen#emc-7020', 0),
    ('med_ibuprofen', 'Label · UK SmPC susp', 'UK SmPC (emc) - suspension', 'Ibuprofen 100 mg/5 ml Oral Suspension - SmPC. Pinewood Laboratories Ltd, 2024.', 'https://products.mhra.gov.uk/search/?search=ibuprofen#emc-4560', 1),
    ('med_ibuprofen', 'PNF', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 2),
    ('med_ibuprofen', 'PhilHealth 2026', 'PhilHealth Dengue Quality Standards', 'PhilHealth Circular No. 2026-0009: Quality Standards on the Diagnosis and Management of Dengue (Adult and Children).', 'https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_ibuprofen')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_ibuprofen');


-- ================================================ med_isoniazid  (Isoniazid)
update public.medicines set description = 'Isoniazid is a prodrug activated by mycobacterial catalase-peroxidase (KatG) that inhibits mycolic acid synthesis in the cell wall, making it bactericidal against actively dividing M. tuberculosis. It is used in first-line combination therapy for active TB and as monotherapy or in combination for latent TB infection. In the Philippine NTP it is part of every first-line regimen, given as HRZE then HR fixed-dose combination tablets dosed by body-weight band (Category I 2HRZE/4HR; Category II 2HRZES/1HRZE/5HRE), and isoniazid preventive therapy (IPT) is given to household contacts under 5 years and to people living with HIV without active TB. WHO''s 2024 TB preventive treatment guideline recommends 6 or 9 months of daily isoniazid, weekly isoniazid plus rifapentine for 3 months (3HP), or daily isoniazid plus rifampicin for 3 months (3HR), with 1 month of daily isoniazid plus rifapentine (1HP) as an alternative.', updated_at = now()
where id = 'med_isoniazid' and description = 'Isoniazid is a prodrug activated by mycobacterial catalase-peroxidase (KatG) that inhibits mycolic acid synthesis in the cell wall, making it bactericidal against actively dividing M. tuberculosis. It is used in first-line combination therapy for active TB and as monotherapy or in combination for latent TB infection.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine NTP Manual of Procedures; WHO TB guidelines - TB preventive treatment; WHO operational handbook - TPT regimens; MSF Essential Drugs; UK SmPC (emc); MSF Tuberculosis guideline; Philippine National Formulary (PNF) EML' else source_attribution || '; Philippine NTP Manual of Procedures; WHO TB guidelines - TB preventive treatment; WHO operational handbook - TPT regimens; MSF Essential Drugs; UK SmPC (emc); MSF Tuberculosis guideline; Philippine National Formulary (PNF) EML' end
where id = 'med_isoniazid' and position('Philippine NTP Manual of Procedures' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'indication', 'Isoniazid preventive therapy for household contacts under 5 years of a TB case, after active TB is ruled out (PH NTP)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'indication' and content = 'Isoniazid preventive therapy for household contacts under 5 years of a TB case, after active TB is ruled out (PH NTP)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'indication', 'Isoniazid preventive therapy for 6 months in people living with HIV without active TB (PH NTP)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'indication' and content = 'Isoniazid preventive therapy for 6 months in people living with HIV without active TB (PH NTP)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'indication', 'Short-course TB preventive treatment combined with rifapentine (3HP, 1HP) or rifampicin (3HR) (WHO)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'indication' and content = 'Short-course TB preventive treatment combined with rifapentine (3HP, 1HP) or rifampicin (3HR) (WHO)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'adverse', 'Severe skin reactions (SJS, TEN, DRESS, AGEP): never restart isoniazid', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse' and content = 'Severe skin reactions (SJS, TEN, DRESS, AGEP): never restart isoniazid');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'adverse', 'Blood disorders: agranulocytosis, aplastic and haemolytic anaemia (frequency unknown)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse' and content = 'Blood disorders: agranulocytosis, aplastic and haemolytic anaemia (frequency unknown)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'adverse', 'Psychotic reactions, mood changes and depression', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse' and content = 'Psychotic reactions, mood changes and depression');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'adverse', 'Deafness, tinnitus and vertigo', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse' and content = 'Deafness, tinnitus and vertigo');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'adverse', 'Gynaecomastia, pancreatitis, hypoglycaemia; nicotinic acid deficiency secondary to pyridoxine deficiency', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse' and content = 'Gynaecomastia, pancreatitis, hypoglycaemia; nicotinic acid deficiency secondary to pyridoxine deficiency');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'adverse', 'Minor GI upset (manage by giving at bedtime or with small meals, PH NTP)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'adverse' and content = 'Minor GI upset (manage by giving at bedtime or with small meals, PH NTP)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'contraindication', 'Drug-induced liver disease (UK SmPC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'contraindication' and content = 'Drug-induced liver disease (UK SmPC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'contraindication', 'Severe hepatic impairment (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'contraindication' and content = 'Severe hepatic impairment (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'interaction', 'Benzodiazepines (diazepam, triazolam): increased toxicity; diazepam may cause sedation and respiratory depression.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction' and content = 'Benzodiazepines (diazepam, triazolam): increased toxicity; diazepam may cause sedation and respiratory depression.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'interaction', 'Warfarin: increased bleeding risk; monitor closely.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction' and content = 'Warfarin: increased bleeding risk; monitor closely.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'interaction', 'Itraconazole (co-administration not recommended) and ketoconazole: reduced azole levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction' and content = 'Itraconazole (co-administration not recommended) and ketoconazole: reduced azole levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'interaction', 'Primidone, disulfiram and chlorzoxazone: reduced hepatic metabolism, possible toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction' and content = 'Primidone, disulfiram and chlorzoxazone: reduced hepatic metabolism, possible toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'interaction', 'Levodopa: effect may be reduced.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction' and content = 'Levodopa: effect may be reduced.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_isoniazid', 'interaction', 'Stavudine: increased risk of peripheral neuropathy.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_isoniazid' and kind = 'interaction' and content = 'Stavudine: increased risk of peripheral neuropathy.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_isoniazid', 'Philippine NTP Manual of Procedures', 'Department of Health, Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed. Manila: DOH; 2014.', 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_isoniazid'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_isoniazid' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_isoniazid', 'WHO TB guidelines - TB preventive treatment', 'World Health Organization. WHO consolidated guidelines on tuberculosis. Module 1: prevention - tuberculosis preventive treatment, 2nd ed. Geneva: WHO; 2024. Section 1.4, TB preventive treatment options (WHO TB Knowledge Sharing Platform).', 'https://tbksp.who.int/en/node/43', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_isoniazid'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_isoniazid' and url = 'https://tbksp.who.int/en/node/43');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_isoniazid', 'WHO operational handbook - TPT regimens', 'World Health Organization. WHO operational handbook on tuberculosis. Module 1: prevention - TB preventive treatment. Section 5.1, Recommended TPT regimens (WHO TB Knowledge Sharing Platform).', 'https://tbksp.who.int/en/node/1271', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_isoniazid'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_isoniazid' and url = 'https://tbksp.who.int/en/node/1271');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_isoniazid', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs - practical guidelines: Isoniazid (H) oral. Updated June 2021.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/isoniazid-h-oral-16683911.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_isoniazid'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_isoniazid' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/isoniazid-h-oral-16683911.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_isoniazid', 'UK SmPC (emc)', 'Isoniazid Tablets BP 100 mg - Summary of Product Characteristics. RPH Pharmaceuticals AB. Electronic medicines compendium (emc), revised August 2025.', 'https://products.mhra.gov.uk/search/?search=isoniazid#emc-9139', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_isoniazid'), 0)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_isoniazid' and url = 'https://products.mhra.gov.uk/search/?search=isoniazid#emc-9139');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_isoniazid', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'safe'::condition_safety, 'PH NTP: people living with HIV without active TB are given 6 months of IPT; give pyridoxine (HIV raises neuropathy and hepatotoxicity risk).'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_isoniazid');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hepatitis_b', 'med_isoniazid', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hepatitis_b'), 0), 'caution'::condition_safety, 'Chronic liver disease raises hepatotoxicity risk (MSF); monitor liver function and stop if jaundice develops. Contraindicated if hepatic impairment is severe.'
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hepatitis_b' and medicine_id = 'med_isoniazid');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_isoniazid', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'UK SmPC advises care in renal impairment (ototoxicity reported in end-stage disease); uraemia raises neuropathy risk, so give pyridoxine. No dose change stated.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_isoniazid');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_isoniazid', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'UK SmPC: use with care in diabetes; diabetics are at higher risk of peripheral neuropathy and should get pyridoxine.'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_isoniazid');
-- med_isoniazid
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_isoniazid', 'adult', 0, 'TB Cat I (2HRZE/4HR), 30–37 kg', 'PO', '2 tablets FDC', 'Once a day', '6 months', '—', 'NTP MOP 2014', 'HRZE 2 months then HR 4 months (HR 10 months for Cat Ia)'),
    ('med_isoniazid', 'adult', 1, 'TB Cat I (2HRZE/4HR), 38–54 kg', 'PO', '3 tablets FDC', 'Once a day', '6 months', '—', 'NTP MOP 2014', ''),
    ('med_isoniazid', 'adult', 2, 'TB Cat I (2HRZE/4HR), 55–70 kg', 'PO', '4 tablets FDC', 'Once a day', '6 months', '—', 'NTP MOP 2014', ''),
    ('med_isoniazid', 'adult', 3, 'TB Cat I (2HRZE/4HR), >70 kg', 'PO', '5 tablets FDC', 'Once a day', '6 months', '—', 'NTP MOP 2014', ''),
    ('med_isoniazid', 'adult', 4, 'TB, single-drug formulation', 'PO', '5 mg/kg (range 4–6)', 'Once a day', 'Per regimen', '400 mg/day', 'NTP MOP 2014', 'UK SmPC and MSF give max 300 mg/day'),
    ('med_isoniazid', 'adult', 5, 'TB meningitis (early phase)', 'PO', 'Up to 10 mg/kg', 'Once a day', 'Early treatment', '—', 'Label · UK SmPC', ''),
    ('med_isoniazid', 'adult', 6, 'TB preventive treatment (6H / 9H)', 'PO', '5 mg/kg (range 4–6)', 'Once a day', '6 or 9 months', '300 mg/day', 'MSF', 'PH NTP: 6 months for PLHIV; WHO 2024 regimen'),
    ('med_isoniazid', 'adult', 7, 'TB preventive treatment (3HR, with rifampicin)', 'PO', '5 mg/kg (range 4–6)', 'Once a day', '3 months', '300 mg/day', 'MSF', 'WHO 2024 regimen'),
    ('med_isoniazid', 'adult', 8, 'TB preventive treatment (3HP, with rifapentine)', 'PO', '900 mg', 'Once a week', '3 months', '900 mg/week', 'MSF', 'Adults and children ≥30 kg'),
    ('med_isoniazid', 'adult', 9, 'TB preventive treatment (1HP, with rifapentine)', 'PO', '300 mg', 'Once a day', '1 month', '300 mg/day', 'MSF', 'Age 13 y and over; WHO alternative option'),
    ('med_isoniazid', 'child', 10, 'TB, single-drug formulation', 'PO', '10 mg/kg (range 10–15)', 'Once a day', 'Per regimen', '300 mg/day', 'NTP MOP 2014', 'Newborn <4 weeks: refer to pediatrician'),
    ('med_isoniazid', 'child', 11, 'TB intensive phase, HZR 50/150/75 dispersible', 'PO', '4–7 kg: 1 tab; 8–11 kg: 2; 12–15 kg: 3; 16–22 kg: 4', 'Once a day', '2 months', '—', 'MSF TB', 'Then HR 50/75: 4–7 kg 1, 8–11 kg 2, 12–14 kg 3 tablets'),
    ('med_isoniazid', 'child', 12, 'TB preventive treatment (6H / 3HR), <30 kg', 'PO', '10 mg/kg (range 7–15)', 'Once a day', '6 months (6H) or 3 months (3HR)', '300 mg/day', 'MSF', 'PH NTP: contacts <5 y after TB ruled out'),
    ('med_isoniazid', 'child', 13, 'TB preventive treatment (3HP), >2 y and <30 kg', 'PO', '20–30 mg/kg', 'Once a week', '3 months', '—', 'MSF', 'With weekly rifapentine')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_isoniazid');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_isoniazid', 'renal', 0, '', 'No dose adjustment stated; use with care in renal impairment (deafness/tinnitus reported in end-stage renal disease). Renal impairment and uraemia raise neuropathy risk: give pyridoxine.', 'Label · UK SmPC'),
    ('med_isoniazid', 'hepatic', 1, '', 'Contraindicated in drug-induced liver disease (SmPC) and severe hepatic impairment (MSF). In known liver disease monitor liver function; any deterioration is a reason to stop. Stop if jaundice appears.', 'MSF'),
    ('med_isoniazid', 'elderly', 2, '', 'No dose reduction needed, but use caution as renal and hepatic function may be reduced; age over 35 raises hepatotoxicity risk (MSF).', 'Label · UK SmPC'),
    ('med_isoniazid', 'pregnancy', 3, '', 'Not contraindicated in pregnancy or breastfeeding; give the mother pyridoxine 10 mg daily and the breastfed infant 5 mg daily. WHO: pregnancy alone should not exclude TB preventive treatment, but use of 1HP and 3HP in pregnancy is cautioned until more data are available.', 'MSF'),
    ('med_isoniazid', 'administration', 4, '', 'Take once daily on an empty stomach. If GI upset occurs, PH NTP advises giving drugs at bedtime or with small meals. Avoid tyramine/histamine-rich foods (cured meats, matured cheese, tuna, mackerel).', 'MSF'),
    ('med_isoniazid', 'monitor', 5, '', 'Pyridoxine (vitamin B6) 10 mg daily for prevention and 50–100 mg daily for treatment of peripheral neuropathy (burning feet). Baseline and regular liver tests; stop if AST rises above 3× normal or bilirubin increases (UK SmPC). Ask monthly about jaundice, nausea, numbness.', 'NTP MOP 2014'),
    ('med_isoniazid', 'forms_ph', 6, '', '300 mg and 400 mg tablet; 200 mg/5 mL syrup (120 mL). FDCs: isoniazid + rifampicin 50/75 mg dispersible (pediatric) and 75/150 mg tablet; + ethambutol 75/150/275 mg; isoniazid + rifampicin + pyrazinamide 50/75/150 mg dispersible (pediatric); HRZE 75/150/400/275 mg tablet.', 'PNF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_isoniazid');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_isoniazid', 'NTP MOP 2014', 'Philippine NTP Manual of Procedures', 'DOH Philippines. National Tuberculosis Control Program Manual of Procedures, 5th ed., 2014 (Tables 10–15).', 'https://www.philhealth.gov.ph/partners/providers/pdf/NTCP_MoP2014.pdf', 0),
    ('med_isoniazid', 'WHO 2024', 'WHO TB guidelines - TB preventive treatment', 'WHO consolidated guidelines on tuberculosis, Module 1: TB preventive treatment, 2nd ed., 2024.', 'https://tbksp.who.int/en/node/43', 1),
    ('med_isoniazid', 'MSF', 'MSF Essential Drugs', 'MSF Essential drugs: Isoniazid (H) oral, 2021.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/isoniazid-h-oral-16683911.html', 2),
    ('med_isoniazid', 'MSF TB', 'MSF Tuberculosis guideline', 'MSF Tuberculosis, Appendix 13: daily dose of TB drugs using fixed-dose combinations, 2022.', 'https://medicalguidelines.msf.org/en/node/1205', 3),
    ('med_isoniazid', 'Label · UK SmPC', 'UK SmPC (emc)', 'Isoniazid Tablets BP 100 mg - SmPC. RPH Pharmaceuticals AB, 2025.', 'https://products.mhra.gov.uk/search/?search=isoniazid#emc-9139', 4),
    ('med_isoniazid', 'PNF', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 5)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_isoniazid')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_isoniazid');


-- ================================================ med_ivermectin  (Ivermectin)
update public.medicines set description = 'Ivermectin binds glutamate-gated chloride channels in invertebrate nerve and muscle cells, causing paralysis and death of the parasite. A single oral dose is effective against scabies mites, strongyloidiasis and onchocerciasis. It does not kill mite eggs, so scabies treatment is repeated after 7-14 days. WHO recommends two-dose ivermectin for mass drug administration where scabies prevalence is 10% or more. In the Philippines it is on the national formulary as 3 mg and 6 mg tablets. It is dosed by body weight (about 200 micrograms/kg for strongyloidiasis and scabies, 150 micrograms/kg for onchocerciasis), and because food increases absorption the US label advises taking it on an empty stomach with water. WHO advises that ivermectin be used to treat COVID-19 only within clinical trials.', updated_at = now()
where id = 'med_ivermectin' and description = 'Ivermectin binds glutamate-gated chloride channels in invertebrate nerve and muscle cells, causing paralysis and death of the parasite. A single oral dose is effective against scabies mites, strongyloidiasis and onchocerciasis. It does not kill mite eggs, so scabies treatment is repeated after 7-14 days. WHO recommends two-dose ivermectin for mass drug administration where scabies prevalence is 10% or more.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine National Formulary (PNF) EML; MSF Essential Drugs; FDA label (Stromectol); WHO - ivermectin and COVID-19' else source_attribution || '; Philippine National Formulary (PNF) EML; MSF Essential Drugs; FDA label (Stromectol); WHO - ivermectin and COVID-19' end
where id = 'med_ivermectin' and position('Philippine National Formulary (PNF) EML' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ivermectin', 'indication', 'Cutaneous larva migrans (200 micrograms/kg daily for 1–2 days, MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'indication' and content = 'Cutaneous larva migrans (200 micrograms/kg daily for 1–2 days, MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ivermectin', 'adverse', 'Mazzotti reactions in onchocerciasis: itching, fever, rash, joint pain, lymph node swelling, mostly in the first 4 days', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'adverse' and content = 'Mazzotti reactions in onchocerciasis: itching, fever, rash, joint pain, lymph node swelling, mostly in the first 4 days');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ivermectin', 'adverse', 'Tachycardia, peripheral oedema and orthostatic hypotension (onchocerciasis treatment)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'adverse' and content = 'Tachycardia, peripheral oedema and orthostatic hypotension (onchocerciasis treatment)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ivermectin', 'adverse', 'Raised ALT/AST; hepatitis and raised bilirubin reported after marketing', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'adverse' and content = 'Raised ALT/AST; hepatitis and raised bilirubin reported after marketing');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_ivermectin', 'adverse', 'Fatigue (strongyloidiasis treatment, ≤3%)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_ivermectin' and kind = 'adverse' and content = 'Fatigue (strongyloidiasis treatment, ≤3%)');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ivermectin', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ivermectin'), 0)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ivermectin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ivermectin', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs - practical guidelines: Ivermectin oral.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/ivermectin-oral-16683965.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ivermectin'), 0)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ivermectin' and url = 'https://medicalguidelines.msf.org/viewport/EssDr/english/ivermectin-oral-16683965.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ivermectin', 'FDA label (Stromectol)', 'Merck Sharp & Dohme Corp. STROMECTOL (ivermectin) tablets - prescribing information. U.S. Food and Drug Administration; 2009.', 'https://www.accessdata.fda.gov/drugsatfda_docs/label/2009/050742s024s025lbl.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ivermectin'), 0)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ivermectin' and url = 'https://www.accessdata.fda.gov/drugsatfda_docs/label/2009/050742s024s025lbl.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_ivermectin', 'WHO - ivermectin and COVID-19', 'World Health Organization. WHO advises that ivermectin only be used to treat COVID-19 within clinical trials. 31 March 2021.', 'https://www.who.int/news-room/feature-stories/detail/who-advises-that-ivermectin-only-be-used-to-treat-covid-19-within-clinical-trials', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_ivermectin'), 0)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_ivermectin' and url = 'https://www.who.int/news-room/feature-stories/detail/who-advises-that-ivermectin-only-be-used-to-treat-covid-19-within-clinical-trials');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'covid19', 'med_ivermectin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'covid19'), 0), 'avoid'::condition_safety, 'WHO (2021) recommends ivermectin be used to treat COVID-19 only within clinical trials.'
where exists (select 1 from public.diseases where id = 'covid19')
  and exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'covid19' and medicine_id = 'med_ivermectin');
-- med_ivermectin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_ivermectin', 'adult', 0, 'Strongyloidiasis', 'PO', '200 micrograms/kg', 'Single dose', '1 day', '—', 'Label · FDA US', '3 mg tabs: 15–24 kg 1, 25–35 kg 2, 36–50 kg 3, 51–65 kg 4, 66–79 kg 5'),
    ('med_ivermectin', 'adult', 1, 'Scabies (ordinary)', 'PO', '200 micrograms/kg', 'Single dose; repeat after 1 week', '2 doses', '—', 'MSF', 'Second dose lowers risk of failure'),
    ('med_ivermectin', 'adult', 2, 'Crusted scabies', 'PO', '200 micrograms/kg', '2 doses 1 week apart (more if needed)', '—', '—', 'MSF', 'With topical keratolytic and scabicide'),
    ('med_ivermectin', 'adult', 3, 'Onchocerciasis', 'PO', '150 micrograms/kg', 'Single dose', 'Repeat every 6–12 months', '—', 'MSF', 'Second dose at 3 months if signs persist; 3 mg tabs: 15–<25 kg 1, 25–<45 kg 2, 45–<65 kg 3, ≥65 kg 4'),
    ('med_ivermectin', 'adult', 4, 'Cutaneous larva migrans', 'PO', '200 micrograms/kg', 'Once a day', '1–2 days', '—', 'MSF', ''),
    ('med_ivermectin', 'child', 5, 'Strongyloidiasis / scabies (≥15 kg)', 'PO', '200 micrograms/kg', 'Single dose (scabies: repeat after 1 week)', '—', '—', 'MSF', 'Not under 15 kg; tablets may be crushed'),
    ('med_ivermectin', 'child', 6, 'Onchocerciasis (≥15 kg)', 'PO', '150 micrograms/kg', 'Single dose', 'Repeat every 6–12 months', '—', 'MSF', 'Not under 15 kg')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_ivermectin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_ivermectin', 'hepatic', 0, '', 'No dose adjustment given; the label advises caution in older patients with reduced hepatic function. Raised liver enzymes and hepatitis have been reported.', 'Label · FDA US'),
    ('med_ivermectin', 'pregnancy', 1, '', 'Should not be used in pregnancy (safety not established). Passes into breast milk in low amounts: treat breastfeeding mothers only when delaying treatment is riskier (US label); MSF lists no contraindication in breastfeeding.', 'Label · FDA US'),
    ('med_ivermectin', 'administration', 2, '', 'Take on an empty stomach with water (food increases bioavailability). Tablets may be crushed for small children.', 'Label · FDA US'),
    ('med_ivermectin', 'monitor', 3, '', 'Strongyloidiasis: at least three follow-up stool examinations over 3 months to confirm cure. In people from loiasis-endemic areas assess Loa loa microfilaraemia before treatment. Watch for Mazzotti reactions in onchocerciasis.', 'Label · FDA US'),
    ('med_ivermectin', 'forms_ph', 4, '', '3 mg and 6 mg tablet.', 'PNF')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_ivermectin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_ivermectin', 'Label · FDA US', 'FDA label (Stromectol)', 'STROMECTOL (ivermectin) tablets - prescribing information. Merck, 2009.', 'https://www.accessdata.fda.gov/drugsatfda_docs/label/2009/050742s024s025lbl.pdf', 0),
    ('med_ivermectin', 'MSF', 'MSF Essential Drugs', 'MSF Essential drugs: Ivermectin oral.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/ivermectin-oral-16683965.html', 1),
    ('med_ivermectin', 'PNF', 'Philippine National Formulary (PNF) EML', 'Philippine National Formulary Essential Medicines List. PhilHealth / DOH, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_ivermectin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_ivermectin');


-- ================================================ med_loperamide  (Loperamide)
update public.medicines set description = 'Loperamide is a peripherally acting synthetic mu-opioid receptor agonist that slows intestinal transit and increases anal sphincter tone, reducing stool frequency and volume. At therapeutic doses P-glycoprotein efflux keeps it out of the CNS; at very high doses it crosses the blood-brain barrier and blocks cardiac sodium and potassium channels. It is used for symptomatic control of acute non-specific diarrhea and chronic diarrhea, not as a substitute for rehydration. Systemic bioavailability is only about 0.3% because of extensive first-pass metabolism (mainly CYP3A4 and CYP2C8), and the half-life is about 11 hours; reduced first-pass clearance in liver disease can cause relative overdose. In the Philippines, the PNF lists loperamide only as a 2 mg capsule and flags it as not for children under 12 years; it is not on the WHO essential medicines list, and oral rehydration remains the core treatment of diarrhea.', updated_at = now()
where id = 'med_loperamide' and description = 'Loperamide is a peripherally acting synthetic mu-opioid receptor agonist that slows intestinal transit and increases anal sphincter tone, reducing stool frequency and volume. At therapeutic doses P-glycoprotein efflux keeps it out of the CNS; at very high doses it crosses the blood-brain barrier and blocks cardiac sodium and potassium channels. It is used for symptomatic control of acute non-specific diarrhea and chronic diarrhea, not as a substitute for rehydration.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; UK SmPC – Loperamide 2 mg Hard Capsules; MSF Essential Drugs – Loperamide oral' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; UK SmPC – Loperamide 2 mg Hard Capsules; MSF Essential Drugs – Loperamide oral' end
where id = 'med_loperamide' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'indication', 'Acute episodes of diarrhoea from irritable bowel syndrome in adults 18 years and over, after a doctor''s diagnosis (UK label)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'indication' and content = 'Acute episodes of diarrhoea from irritable bowel syndrome in adults 18 years and over, after a doctor''s diagnosis (UK label)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'indication', 'Persistent diarrhoea in adults with HIV infection, together with rehydration (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'indication' and content = 'Persistent diarrhoea in adults with HIV infection, together with rehydration (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'adverse', 'Flatulence', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse' and content = 'Flatulence');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'adverse', 'Headache', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse' and content = 'Headache');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'adverse', 'Urinary retention', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse' and content = 'Urinary retention');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'adverse', 'Miosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse' and content = 'Miosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'adverse', 'Acute pancreatitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse' and content = 'Acute pancreatitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'adverse', 'Severe skin reactions, incl. Stevens-Johnson syndrome and toxic epidermal necrolysis (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse' and content = 'Severe skin reactions, incl. Stevens-Johnson syndrome and toxic epidermal necrolysis (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'adverse', 'Anaphylactic reactions, angioedema and urticaria', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse' and content = 'Anaphylactic reactions, angioedema and urticaria');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'adverse', 'Overdose can unmask Brugada syndrome', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'adverse' and content = 'Overdose can unmask Brugada syndrome');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'contraindication', 'Children under 12 years (UK label; PNF note)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'contraindication' and content = 'Children under 12 years (UK label; PNF note)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'contraindication', 'Situations where slowing peristalsis must be avoided (risk of ileus, megacolon, toxic megacolon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'contraindication' and content = 'Situations where slowing peristalsis must be avoided (risk of ileus, megacolon, toxic megacolon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'contraindication', 'Diarrhoea due to antibiotics (MSF)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'contraindication' and content = 'Diarrhoea due to antibiotics (MSF)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'interaction', 'Ketoconazole: about 5-fold rise in loperamide levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'interaction' and content = 'Ketoconazole: about 5-fold rise in loperamide levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'interaction', 'Itraconazole plus gemfibrozil together: about 13-fold rise in loperamide AUC.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'interaction' and content = 'Itraconazole plus gemfibrozil together: about 13-fold rise in loperamide AUC.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'interaction', 'Oral desmopressin: possible about 3-fold rise in desmopressin levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'interaction' and content = 'Oral desmopressin: possible about 3-fold rise in desmopressin levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_loperamide', 'interaction', 'Anticholinergics and other drugs that slow peristalsis: loperamide effect may be enhanced.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_loperamide' and kind = 'interaction' and content = 'Anticholinergics and other drugs that slow peristalsis: loperamide effect may be enhanced.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_loperamide', 'UK SmPC (emc)', 'Loperamide 2 mg Hard Capsules – Summary of Product Characteristics. Milpharm Ltd (PL 16363/0534). Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=loperamide#emc-10420', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_loperamide'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_loperamide' and url = 'https://products.mhra.gov.uk/search/?search=loperamide#emc-10420');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_loperamide', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – practical guidelines: Loperamide oral. MSF Medical Guidelines (updated January 2024).', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/loperamide-oral-16684067.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_loperamide'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_loperamide' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/loperamide-oral-16684067.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_loperamide', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_loperamide'), 0)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_loperamide' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_loperamide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'safe'::condition_safety, 'MSF: used for persistent diarrhoea in adults with HIV with rehydration; UK label: stop at the first sign of abdominal distension in AIDS (toxic megacolon reports)'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_loperamide');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'typhoid_fever', 'med_loperamide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'typhoid_fever'), 0), 'avoid'::condition_safety, 'Our inference: the label contraindicates bacterial enterocolitis from invasive organisms such as Salmonella; typhoid is not named'
where exists (select 1 from public.diseases where id = 'typhoid_fever')
  and exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'typhoid_fever' and medicine_id = 'med_loperamide');
-- med_loperamide
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_loperamide', 'adult', 0, 'Acute diarrhoea', 'PO', '4 mg, then 2 mg after each loose stool', 'As needed', 'Stop if no improvement in 48 h', '12 mg/day', 'Label · UK SmPC', 'Usual 6–8 mg/day; keep rehydrating'),
    ('med_loperamide', 'adult', 1, 'Acute diarrhoea of IBS (18 years and over, diagnosed)', 'PO', '4 mg, then 2 mg after each loose stool', 'As needed', 'Stop if no improvement in 48 h', '12 mg/day', 'Label · UK SmPC', 'See doctor if episodes persist beyond 2 weeks'),
    ('med_loperamide', 'adult', 2, 'Persistent diarrhoea in HIV infection', 'PO', '4 mg, then 2 mg after each loose stool', 'As needed', 'By clinical response', '16 mg/day', 'MSF', 'With rehydration'),
    ('med_loperamide', 'child', 3, 'Acute diarrhoea, 12 years and over', 'PO', '4 mg, then 2 mg after each loose stool', 'As needed', 'Stop if no improvement in 48 h', '12 mg/day', 'Label · UK SmPC', 'Contraindicated under 12 years')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_loperamide');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_loperamide', 'renal', 0, '', 'No dose adjustment needed.', 'Label · UK SmPC'),
    ('med_loperamide', 'hepatic', 1, '', 'No pharmacokinetic data; use with caution, as reduced first-pass metabolism can cause relative overdose and CNS toxicity.', 'Label · UK SmPC'),
    ('med_loperamide', 'elderly', 2, '', 'No dose adjustment; fluid and electrolyte replacement is the priority in frail and elderly patients.', 'Label · UK SmPC'),
    ('med_loperamide', 'pregnancy', 3, '', 'Avoid in the first trimester if possible (one study suggested a possible moderate rise in hypospadias); may be considered in the second and third trimesters. Not recommended while breastfeeding (UK label); MSF lists no contraindication in pregnancy or breastfeeding.', 'Label · UK SmPC'),
    ('med_loperamide', 'administration', 4, '', 'Swallow capsules with liquid. Do not use for long periods before the cause of persistent diarrhoea is found. Overdose: naloxone.', 'Label · UK SmPC'),
    ('med_loperamide', 'forms_ph', 5, '', 'Oral: 2 mg capsule (as hydrochloride). PNF note: not for infants and children under 12 years.', 'PNF'),
    ('med_loperamide', 'monitor', 6, '', 'Stool frequency and hydration status; stop at constipation, abdominal distension or ileus, and if no improvement after 48 h. Ask about misuse in patients with a drug-abuse history (cardiac toxicity at high doses).', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_loperamide');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_loperamide', 'PNF', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 0),
    ('med_loperamide', 'Label · UK SmPC', 'UK SmPC – Loperamide 2 mg Hard Capsules', 'Milpharm Ltd. Loperamide 2 mg Hard Capsules – Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=loperamide#emc-10420', 1),
    ('med_loperamide', 'MSF', 'MSF Essential Drugs – Loperamide oral', 'Médecins Sans Frontières. Essential drugs – practical guidelines: Loperamide oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/loperamide-oral-16684067.html', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_loperamide')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_loperamide');


-- ================================================ med_losartan  (Losartan)
update public.medicines set description = 'Losartan selectively blocks the angiotensin II type 1 (AT1) receptor, preventing angiotensin II-mediated vasoconstriction and aldosterone release. This lowers blood pressure and reduces intraglomerular pressure and proteinuria. It is used for hypertension (including with left ventricular hypertrophy) and diabetic nephropathy in type 2 diabetes, and does not cause the bradykinin-related cough typical of ACE inhibitors. Losartan is partly converted to an active carboxylic acid metabolite (E-3174) that is 10–40 times more potent; losartan''s half-life is about 2 hours but the metabolite''s is 6–9 hours, which allows once-daily dosing, and full blood-pressure effect takes 3–6 weeks. In the Philippine national primary-care hypertension protocol, losartan 50 mg is added to amlodipine 5 mg at step 2 and both are raised (losartan 100 mg, amlodipine 10 mg) at step 3, but it should not be given to women who are or could become pregnant. The PNF lists 50 mg and 100 mg tablets and a losartan + hydrochlorothiazide 50 mg/12.5 mg tablet.', updated_at = now()
where id = 'med_losartan' and description = 'Losartan selectively blocks the angiotensin II type 1 (AT1) receptor, preventing angiotensin II-mediated vasoconstriction and aldosterone release. This lowers blood pressure and reduces intraglomerular pressure and proteinuria. It is used for hypertension (including with left ventricular hypertrophy) and diabetic nephropathy in type 2 diabetes, and does not cause the bradykinin-related cough typical of ACE inhibitors.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); Philippine hypertension protocol; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; Philippine primary-care hypertension protocol; UK SmPC – Losartan potassium 50 mg film-coated tablets; COZAAR (losartan potassium) – US prescribing information' else source_attribution || '; UK SmPC (emc); Philippine hypertension protocol; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; Philippine primary-care hypertension protocol; UK SmPC – Losartan potassium 50 mg film-coated tablets; COZAAR (losartan potassium) – US prescribing information' end
where id = 'med_losartan' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'indication', 'Chronic heart failure (LVEF ≤40%) when ACE inhibitors are unsuitable, e.g. because of cough (UK label)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'indication' and content = 'Chronic heart failure (LVEF ≤40%) when ACE inhibitors are unsuitable, e.g. because of cough (UK label)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'indication', 'Hypertension in children and adolescents aged 6–18 years', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'indication' and content = 'Hypertension in children and adolescents aged 6–18 years');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'adverse', 'Vertigo', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse' and content = 'Vertigo');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'adverse', 'Anaemia (heart failure trials)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse' and content = 'Anaemia (heart failure trials)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'adverse', 'Hypoglycaemia (diabetic renal disease trials)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse' and content = 'Hypoglycaemia (diabetic renal disease trials)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'adverse', 'Intestinal angioedema (abdominal pain, vomiting, diarrhoea)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse' and content = 'Intestinal angioedema (abdominal pain, vomiting, diarrhoea)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'adverse', 'Hepatitis and raised ALT (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse' and content = 'Hepatitis and raised ALT (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'adverse', 'Thrombocytopenia, hyponatraemia, pancreatitis, rhabdomyolysis (frequency not known)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'adverse' and content = 'Thrombocytopenia, hyponatraemia, pancreatitis, rhabdomyolysis (frequency not known)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'contraindication', 'Severe hepatic impairment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'contraindication' and content = 'Severe hepatic impairment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'contraindication', 'Co-administration with aliskiren when GFR is under 60 mL/min/1.73 m²', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'contraindication' and content = 'Co-administration with aliskiren when GFR is under 60 mL/min/1.73 m²');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'contraindication', 'Primary hyperaldosteronism: not recommended (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'contraindication' and content = 'Primary hyperaldosteronism: not recommended (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'interaction', 'Fluconazole (CYP2C9 inhibitor): about 50% lower active-metabolite exposure.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction' and content = 'Fluconazole (CYP2C9 inhibitor): about 50% lower active-metabolite exposure.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'interaction', 'Rifampicin (CYP2C9 inducer): about 40% lower active-metabolite levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction' and content = 'Rifampicin (CYP2C9 inducer): about 40% lower active-metabolite levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'interaction', 'Trimethoprim (incl. co-trimoxazole) and heparin: hyperkalaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction' and content = 'Trimethoprim (incl. co-trimoxazole) and heparin: hyperkalaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'interaction', 'Tricyclic antidepressants, antipsychotics, baclofen, amifostine: added hypotension.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction' and content = 'Tricyclic antidepressants, antipsychotics, baclofen, amifostine: added hypotension.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_losartan', 'interaction', 'Grapefruit juice: may lower active-metabolite levels; avoid.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_losartan' and kind = 'interaction' and content = 'Grapefruit juice: may lower active-metabolite levels; avoid.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_losartan', 'UK SmPC (emc)', 'Losartan potassium 50 mg film-coated tablets – Summary of Product Characteristics. Milpharm Ltd (PL 16363/0421). Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=losartan#emc-7061', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_losartan'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_losartan' and url = 'https://products.mhra.gov.uk/search/?search=losartan#emc-7061');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_losartan', 'Philippine hypertension protocol', 'National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Hosted by Resolve to Save Lives, 2023.', 'https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_losartan'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_losartan' and url = 'https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_losartan', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_losartan'), 0)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_losartan' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_gastroenteritis', 'med_losartan', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis'), 0), 'caution'::condition_safety, 'UK label: correct volume/sodium depletion first or start lower; check renal function with fever or dehydration'
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis' and medicine_id = 'med_losartan');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_coronary_syndrome', 'med_losartan', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome'), 0), 'caution'::condition_safety, 'UK label: in coronary disease an excessive fall in blood pressure could cause myocardial infarction'
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome' and medicine_id = 'med_losartan');
-- med_losartan
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_losartan', 'adult', 0, 'Hypertension (PH protocol step 2, with amlodipine 5 mg)', 'PO', '50 mg', 'Once a day', 'Long-term', '—', 'PH HTN protocol', 'Recheck BP after 1 month'),
    ('med_losartan', 'adult', 1, 'Hypertension (PH protocol step 3, with amlodipine 10 mg)', 'PO', '100 mg', 'Once a day', 'Long-term', '100 mg/day', 'PH HTN protocol', 'Step 4: add HCTZ 25 mg or refer'),
    ('med_losartan', 'adult', 2, 'Hypertension', 'PO', '50 mg', 'Once a day', 'Long-term', '100 mg/day', 'Label · UK SmPC', 'Full effect in 3–6 weeks; 25 mg if volume depleted or over 75 y'),
    ('med_losartan', 'adult', 3, 'Chronic heart failure (start)', 'PO', '12.5 mg', 'Once a day', 'Titrate weekly', '150 mg/day', 'Label · UK SmPC', '12.5 → 25 → 50 → 100 mg weekly as tolerated'),
    ('med_losartan', 'adult', 4, 'Hypertensive LVH (stroke risk reduction)', 'PO', '50 mg', 'Once a day', 'Long-term', '100 mg/day', 'Label · UK SmPC', 'Add low-dose HCTZ and/or raise to 100 mg'),
    ('med_losartan', 'child', 5, 'Hypertension, 6–18 y, >20 to <50 kg', 'PO', '25 mg', 'Once a day', 'Long-term', '50 mg/day', 'Label · UK SmPC', 'Up to 50 mg only exceptionally'),
    ('med_losartan', 'child', 6, 'Hypertension, 6–18 y, ≥50 kg', 'PO', '50 mg', 'Once a day', 'Long-term', '100 mg/day', 'Label · UK SmPC', 'Up to 100 mg only exceptionally'),
    ('med_losartan', 'child', 7, 'Hypertension, 6 y and over (weight-based)', 'PO', '0.7 mg/kg', 'Once a day', 'Long-term', '50 mg start', 'Label · US', '>1.4 mg/kg or >100 mg/day not studied; not under 6 y or eGFR <30')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_losartan');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_losartan', 'renal', 0, '', 'No initial dose adjustment, including haemodialysis; neither losartan nor its metabolite is removed by dialysis. Not recommended in children with GFR <30 mL/min/1.73 m².', 'Label · UK SmPC'),
    ('med_losartan', 'renal', 1, 'CrCl 30–50', 'Monitor potassium and creatinine clearance closely.', 'Label · UK SmPC'),
    ('med_losartan', 'hepatic', 2, '', 'Plasma levels are much higher in cirrhosis (about 5-fold): use a lower dose if there is a history of hepatic impairment; contraindicated in severe impairment; not recommended in children with hepatic impairment.', 'Label · UK SmPC'),
    ('med_losartan', 'elderly', 3, '', 'Usually no adjustment; consider 25 mg to start in those over 75 years.', 'Label · UK SmPC'),
    ('med_losartan', 'pregnancy', 4, '', 'Do not start in pregnancy; not recommended in the first trimester, contraindicated in the second and third. PH protocol: do not give to women who are or could become pregnant. Not recommended while breastfeeding.', 'Label · UK SmPC'),
    ('med_losartan', 'administration', 5, '', 'Swallow whole with water, with or without food. In the PH protocol amlodipine and losartan are taken together, and adherence is confirmed before stepping up.', 'PH HTN protocol'),
    ('med_losartan', 'forms_ph', 6, '', 'Oral: 50 mg and 100 mg tablet (as potassium salt); losartan 50 mg + hydrochlorothiazide 12.5 mg tablet.', 'PNF'),
    ('med_losartan', 'monitor', 7, '', 'BP monthly while titrating (target <130/80 if diabetes, CKD, prior MI or stroke); serum potassium and creatinine, especially in heart failure, renal impairment, diabetes and during fever or dehydration.', 'PH HTN protocol')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_losartan');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_losartan', 'PNF', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 0),
    ('med_losartan', 'PH HTN protocol', 'Philippine primary-care hypertension protocol', 'National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives, 2023.', 'https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf', 1),
    ('med_losartan', 'Label · UK SmPC', 'UK SmPC – Losartan potassium 50 mg film-coated tablets', 'Milpharm Ltd. Losartan potassium 50 mg film-coated tablets – Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=losartan#emc-7061', 2),
    ('med_losartan', 'Label · US', 'COZAAR (losartan potassium) – US prescribing information', 'COZAAR (losartan potassium) tablets. Prescribing information. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9949448f-c3b9-44ee-94ed-c1aca8c90f39', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_losartan')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_losartan');


-- ================================================ med_mefenamic_acid  (Mefenamic Acid)
update public.medicines set description = 'Mefenamic acid is an anthranilic acid (fenamate) NSAID that inhibits cyclooxygenase and prostaglandin synthesis. It is used for short-term relief of mild-to-moderate pain and for primary dysmenorrhea. It is metabolised mainly by hepatic CYP2C9 and has a short plasma half-life of about 2 hours, so it is given three times a day; besides pain it is also used for menorrhagia and, in other countries, arthritis. In the Philippines it is widely available (PNF: 250 mg and 500 mg tablets/capsules), but PhilHealth''s dengue quality standards state that NSAIDs are not recommended in dengue and that paracetamol is the drug for fever.', updated_at = now()
where id = 'med_mefenamic_acid' and description = 'Mefenamic acid is an anthranilic acid (fenamate) NSAID that inhibits cyclooxygenase and prostaglandin synthesis. It is used for short-term relief of mild-to-moderate pain and for primary dysmenorrhea.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); UK SmPC (emc) – suspension; PhilHealth dengue quality standards; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; UK SmPC – Mefenamic Acid 500 mg Tablets; UK SmPC – Mefenamic Acid 50 mg/5 ml Suspension' else source_attribution || '; UK SmPC (emc); UK SmPC (emc) – suspension; PhilHealth dengue quality standards; Philippine National Formulary (PNF EML); Philippine National Formulary – Essential Medicines List; UK SmPC – Mefenamic Acid 500 mg Tablets; UK SmPC – Mefenamic Acid 50 mg/5 ml Suspension' end
where id = 'med_mefenamic_acid' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'indication', 'Rheumatoid arthritis (including Still''s disease) and osteoarthritis (UK label)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'indication' and content = 'Rheumatoid arthritis (including Still''s disease) and osteoarthritis (UK label)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'indication', 'Menorrhagia from dysfunctional causes or an IUD, after other pelvic pathology is excluded', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'indication' and content = 'Menorrhagia from dysfunctional causes or an IUD, after other pelvic pathology is excluded');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'indication', 'Dental, traumatic, muscular, post-operative and post-partum pain; headache', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'indication' and content = 'Dental, traumatic, muscular, post-operative and post-partum pain; headache');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'adverse', 'Diarrhoea that can be severe, with proctocolitis: stop and do not re-use', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse' and content = 'Diarrhoea that can be severe, with proctocolitis: stop and do not re-use');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'adverse', 'Reversible haemolytic anaemia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse' and content = 'Reversible haemolytic anaemia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'adverse', 'Agranulocytosis, aplastic anaemia, thrombocytopenia (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse' and content = 'Agranulocytosis, aplastic anaemia, thrombocytopenia (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'adverse', 'Stevens-Johnson syndrome and toxic epidermal necrolysis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse' and content = 'Stevens-Johnson syndrome and toxic epidermal necrolysis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'adverse', 'Aseptic meningitis (higher risk in SLE or mixed connective tissue disease)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse' and content = 'Aseptic meningitis (higher risk in SLE or mixed connective tissue disease)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'adverse', 'Convulsions (especially in overdose)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse' and content = 'Convulsions (especially in overdose)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'adverse', 'Interstitial nephritis and renal papillary necrosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse' and content = 'Interstitial nephritis and renal papillary necrosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'adverse', 'Reversible loss of colour vision', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse' and content = 'Reversible loss of colour vision');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'adverse', 'False-positive urine bile test', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'adverse' and content = 'False-positive urine bile test');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'contraindication', 'Inflammatory bowel disease', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication' and content = 'Inflammatory bowel disease');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'contraindication', 'History of GI bleeding or perforation with previous NSAIDs', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication' and content = 'History of GI bleeding or perforation with previous NSAIDs');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'contraindication', 'Active or recurrent peptic ulcer or haemorrhage', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication' and content = 'Active or recurrent peptic ulcer or haemorrhage');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'contraindication', 'Severe heart, liver or kidney failure', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication' and content = 'Severe heart, liver or kidney failure');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'contraindication', 'Third trimester of pregnancy', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'contraindication' and content = 'Third trimester of pregnancy');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'interaction', 'Corticosteroids: increased GI ulceration and bleeding.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction' and content = 'Corticosteroids: increased GI ulceration and bleeding.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'interaction', 'Sulfonylureas: longer half-life and more hypoglycaemia.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction' and content = 'Sulfonylureas: longer half-life and more hypoglycaemia.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'interaction', 'Ciclosporin, tacrolimus and aminoglycosides: increased nephrotoxicity (aminoglycoside levels rise).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction' and content = 'Ciclosporin, tacrolimus and aminoglycosides: increased nephrotoxicity (aminoglycoside levels rise).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'interaction', 'Digoxin and other cardiac glycosides: higher glycoside levels and worse heart failure.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction' and content = 'Digoxin and other cardiac glycosides: higher glycoside levels and worse heart failure.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'interaction', 'Quinolone antibiotics: increased convulsion risk.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction' and content = 'Quinolone antibiotics: increased convulsion risk.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'interaction', 'Mifepristone: avoid NSAIDs for 8–12 days after.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction' and content = 'Mifepristone: avoid NSAIDs for 8–12 days after.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_mefenamic_acid', 'interaction', 'Zidovudine: increased haematological toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_mefenamic_acid' and kind = 'interaction' and content = 'Zidovudine: increased haematological toxicity.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_mefenamic_acid', 'UK SmPC (emc)', 'Mefenamic Acid 500 mg Tablets – Summary of Product Characteristics. Chemidex Pharma Ltd (PL 17736/0005). Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-12891', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_mefenamic_acid'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_mefenamic_acid' and url = 'https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-12891');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_mefenamic_acid', 'UK SmPC (emc) – suspension', 'Mefenamic Acid 50 mg/5 ml Suspension – Summary of Product Characteristics. Chemidex Pharma Ltd (PL 17736/0146). emc.', 'https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-13316', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_mefenamic_acid'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_mefenamic_acid' and url = 'https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-13316');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_mefenamic_acid', 'PhilHealth dengue quality standards', 'PhilHealth. Quality Standards on the Diagnosis and Management of Dengue (Adult and Children) as a Reference of the Corporation. PhilHealth Circular 2026-0009.', 'https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_mefenamic_acid'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_mefenamic_acid' and url = 'https://www.philhealth.gov.ph/circulars/2026/PC2026-0009.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_mefenamic_acid', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_mefenamic_acid'), 0)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_mefenamic_acid' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'migraine', 'med_mefenamic_acid', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'migraine'), 0), 'caution'::condition_safety, 'UK label lists headache of most causes as an indication, but warns that frequent painkiller use causes medication-overuse headache'
where exists (select 1 from public.diseases where id = 'migraine')
  and exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.disease_medicines where disease_id = 'migraine' and medicine_id = 'med_mefenamic_acid');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'type2_diabetes', 'med_mefenamic_acid', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'type2_diabetes'), 0), 'caution'::condition_safety, 'UK label: prolongs sulfonylurea action (hypoglycaemia) and can cause glucose intolerance in diabetics'
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.disease_medicines where disease_id = 'type2_diabetes' and medicine_id = 'med_mefenamic_acid');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_gastroenteritis', 'med_mefenamic_acid', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis'), 0), 'caution'::condition_safety, 'UK label: higher risk of renal failure with dehydration; can itself cause diarrhoea (stop if it occurs)'
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis' and medicine_id = 'med_mefenamic_acid');
-- med_mefenamic_acid
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_mefenamic_acid', 'adult', 0, 'Pain; rheumatoid arthritis and osteoarthritis', 'PO', '500 mg', '3× a day', 'Shortest possible', '1500 mg/day', 'Label · UK SmPC', 'With or after food'),
    ('med_mefenamic_acid', 'adult', 1, 'Primary dysmenorrhoea', 'PO', '500 mg', '3× a day', 'From onset of pain', '1500 mg/day', 'Label · UK SmPC', ''),
    ('med_mefenamic_acid', 'adult', 2, 'Menorrhagia', 'PO', '500 mg', '3× a day', 'From first day of heavy bleeding', '1500 mg/day', 'Label · UK SmPC', 'Investigate if no response'),
    ('med_mefenamic_acid', 'child', 3, 'Pain or fever, over 6 months', 'PO', '25 mg/kg/day ÷ 3', 'Up to 3× a day', 'Max 7 days', '—', 'Label · UK SmPC susp', 'Fever: use paracetamol if dengue possible'),
    ('med_mefenamic_acid', 'child', 4, '6 months to <2 years', 'PO', '50 mg (5 mL)', 'Up to 3× a day', 'Max 7 days', '150 mg/day', 'Label · UK SmPC susp', '50 mg/5 mL suspension'),
    ('med_mefenamic_acid', 'child', 5, '2 to <5 years', 'PO', '100 mg (10 mL)', 'Up to 3× a day', 'Max 7 days', '300 mg/day', 'Label · UK SmPC susp', ''),
    ('med_mefenamic_acid', 'child', 6, '5 to <9 years', 'PO', '150 mg (15 mL)', 'Up to 3× a day', 'Max 7 days', '450 mg/day', 'Label · UK SmPC susp', ''),
    ('med_mefenamic_acid', 'child', 7, '9 to 12 years', 'PO', '200 mg (20 mL)', 'Up to 3× a day', 'Max 7 days', '600 mg/day', 'Label · UK SmPC susp', 'Longer only in Still''s disease')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_mefenamic_acid');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_mefenamic_acid', 'renal', 0, '', 'Contraindicated in severe renal failure; caution in renal disease, dehydration, diuretic use and old age; monitor renal function. Haemodialysis removes little drug.', 'Label · UK SmPC'),
    ('med_mefenamic_acid', 'hepatic', 1, '', 'Contraindicated in hepatic failure; check liver function on prolonged therapy and stop if dysfunction appears.', 'Label · UK SmPC'),
    ('med_mefenamic_acid', 'elderly', 2, '', 'Same dose as adults but lowest effective dose for the shortest time, with monitoring for GI bleeding (more often fatal in the elderly).', 'Label · UK SmPC'),
    ('med_mefenamic_acid', 'pregnancy', 3, '', 'Avoid in the first and second trimesters unless clearly needed (low dose, short course); from week 20 can cause oligohydramnios and ductus constriction; contraindicated in the third trimester. Do not use while breastfeeding. May impair female fertility.', 'Label · UK SmPC'),
    ('med_mefenamic_acid', 'administration', 4, '', 'Take with or after food. Use caution in CYP2C9 poor metabolisers and in epilepsy; avoid alcohol.', 'Label · UK SmPC'),
    ('med_mefenamic_acid', 'forms_ph', 5, '', 'Oral: 250 mg and 500 mg tablet/capsule.', 'PNF'),
    ('med_mefenamic_acid', 'monitor', 6, '', 'On prolonged use: blood count (haemolytic anaemia, dyscrasias), liver function, renal function, rash and diarrhoea — stop if any occur. Check for dengue before giving for fever in the Philippines.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_mefenamic_acid');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_mefenamic_acid', 'PNF', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List, 8th ed., as of 02 Nov 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 0),
    ('med_mefenamic_acid', 'Label · UK SmPC', 'UK SmPC – Mefenamic Acid 500 mg Tablets', 'Chemidex Pharma Ltd. Mefenamic Acid 500 mg Tablets – Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-12891', 1),
    ('med_mefenamic_acid', 'Label · UK SmPC susp', 'UK SmPC – Mefenamic Acid 50 mg/5 ml Suspension', 'Chemidex Pharma Ltd. Mefenamic Acid 50 mg/5 ml Suspension – Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=mefenamic+acid#emc-13316', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_mefenamic_acid')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_mefenamic_acid');


-- ================================================ med_metformin  (Metformin)
update public.medicines set description = 'Metformin lowers blood glucose mainly by decreasing hepatic gluconeogenesis, and also reduces intestinal glucose absorption and improves peripheral insulin sensitivity. It does not stimulate insulin secretion, so it rarely causes hypoglycemia alone and is weight-neutral. It is the usual first-line oral agent for type 2 diabetes. In the Philippines it is listed in the PNF Essential Medicines List as 500 mg tablets/film-coated tablets and 850 mg tablets, and it has been on the WHO Model List of Essential Medicines since 1997. In the UKPDS, overweight patients started on metformin after diet failure had fewer diabetes-related complications, lower diabetes-related and all-cause mortality, and fewer myocardial infarctions than those on diet alone. It is not metabolised and is excreted unchanged in the urine (half-life about 6.5 h), so clearance falls in step with kidney function.', updated_at = now()
where id = 'med_metformin' and description = 'Metformin lowers blood glucose mainly by decreasing hepatic gluconeogenesis, and also reduces intestinal glucose absorption and improves peripheral insulin sensitivity. It does not stimulate insulin secretion, so it rarely causes hypoglycemia alone and is weight-neutral. It is the usual first-line oral agent for type 2 diabetes.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PhilHealth); WHO Model List of Essential Medicines' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PhilHealth); WHO Model List of Essential Medicines' end
where id = 'med_metformin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'indication', 'Type 2 diabetes in combination with insulin (adults)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'indication' and content = 'Type 2 diabetes in combination with insulin (adults)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'adverse', 'Abnormal liver tests or hepatitis (very rare; resolves on stopping)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'adverse' and content = 'Abnormal liver tests or hepatitis (very rare; resolves on stopping)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'adverse', 'Skin reactions: erythema, pruritus, urticaria (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'adverse' and content = 'Skin reactions: erythema, pruritus, urticaria (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'contraindication', 'Diabetic pre-coma', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication' and content = 'Diabetic pre-coma');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'contraindication', 'Acute conditions that can affect kidney function: dehydration, severe infection, shock', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication' and content = 'Acute conditions that can affect kidney function: dehydration, severe infection, shock');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'contraindication', 'Conditions causing tissue hypoxia: decompensated heart failure, respiratory failure, recent myocardial infarction', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication' and content = 'Conditions causing tissue hypoxia: decompensated heart failure, respiratory failure, recent myocardial infarction');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'contraindication', 'Hepatic insufficiency, acute alcohol intoxication, alcoholism', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication' and content = 'Hepatic insufficiency, acute alcohol intoxication, alcoholism');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'contraindication', 'Not recommended in mitochondrial disease (MELAS, MIDD)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'contraindication' and content = 'Not recommended in mitochondrial disease (MELAS, MIDD)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'interaction', 'NSAIDs (incl. COX-2 inhibitors), ACE inhibitors, ARBs and diuretics (especially loop): may impair kidney function; monitor renal function.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'interaction' and content = 'NSAIDs (incl. COX-2 inhibitors), ACE inhibitors, ARBs and diuretics (especially loop): may impair kidney function; monitor renal function.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'interaction', 'Glucocorticoids, sympathomimetics (e.g., salbutamol), hydrochlorothiazide, chlorpromazine: raise blood glucose; check glucose more often and adjust dose.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'interaction' and content = 'Glucocorticoids, sympathomimetics (e.g., salbutamol), hydrochlorothiazide, chlorpromazine: raise blood glucose; check glucose more often and adjust dose.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'interaction', 'Verapamil (OCT1 inhibitor) may reduce metformin efficacy; rifampicin (OCT1 inducer) may increase its absorption and effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'interaction' and content = 'Verapamil (OCT1 inhibitor) may reduce metformin efficacy; rifampicin (OCT1 inducer) may increase its absorption and effect.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metformin', 'interaction', 'Trimethoprim, isavuconazole, crizotinib, olaparib: may raise metformin levels or alter its renal elimination.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metformin' and kind = 'interaction' and content = 'Trimethoprim, isavuconazole, crizotinib, olaparib: may raise metformin levels or alter its renal elimination.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metformin', 'UK SmPC (emc)', 'Metformin 500 mg Tablets. Summary of Product Characteristics. Medley Pharma Ltd. electronic medicines compendium (emc); text revised 04/2025.', 'https://products.mhra.gov.uk/search/?search=metformin#emc-15731', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metformin'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metformin' and url = 'https://products.mhra.gov.uk/search/?search=metformin#emc-15731');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metformin', 'UK SmPC (emc)', 'Metformin hydrochloride 500 mg prolonged release tablets. Summary of Product Characteristics. Genus Pharmaceuticals (STADA). emc; text revised 04/2025.', 'https://products.mhra.gov.uk/search/?search=metformin#emc-5263', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metformin'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metformin' and url = 'https://products.mhra.gov.uk/search/?search=metformin#emc-5263');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metformin', 'MSF Essential Drugs', 'Médecins Sans Frontières. Metformin oral. In: Essential Drugs – practical guidelines. MSF Medical Guidelines; updated 09/2023.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/metformin-oral-27983919.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metformin'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metformin' and url = 'https://medicalguidelines.msf.org/viewport/EssDr/english/metformin-oral-27983919.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metformin', 'Philippine National Formulary (PhilHealth)', 'Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metformin'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metformin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metformin', 'WHO Model List of Essential Medicines', 'World Health Organization. eEML – Electronic Essential Medicines List: Metformin (first added 1997, TRS 882).', 'https://list.essentialmeds.org/medicines/191', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metformin'), 0)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metformin' and url = 'https://list.essentialmeds.org/medicines/191');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_metformin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'Can be used in stable chronic heart failure with regular monitoring of heart and kidney function; contraindicated in acute or unstable (decompensated) heart failure.'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_metformin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_coronary_syndrome', 'med_metformin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome'), 0), 'avoid'::condition_safety, 'Recent myocardial infarction is a contraindication (tissue hypoxia raises lactic acidosis risk).'
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome' and medicine_id = 'med_metformin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_gastroenteritis', 'med_metformin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis'), 0), 'caution'::condition_safety, 'Dehydration is a contraindication in the label; withholding metformin during gastroenteritis with significant dehydration is an inference from this, not a direct label statement.'
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis' and medicine_id = 'med_metformin');
-- med_metformin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_metformin', 'adult', 0, 'Type 2 diabetes (IR tablet)', 'PO', '500 mg or 850 mg', '2–3× a day', 'Long-term', '3 g/day', 'Label · UK SmPC', 'With or after meals; adjust after 10–15 days by blood glucose'),
    ('med_metformin', 'adult', 1, 'Type 2 diabetes (IR tablet, MSF schedule)', 'PO', '500 mg, then 500 mg 2× a day', 'Once a day (week 1)', 'Long-term', '2 g/day', 'MSF', 'Week 2: 500 mg 2× a day; then +500 mg/week as needed (1 g morning and evening max)'),
    ('med_metformin', 'adult', 2, 'Type 2 diabetes (prolonged-release)', 'PO', '500 mg', 'Once a day', 'Long-term', '2000 mg/day', 'Label · UK SmPC PR', 'With evening meal; +500 mg every 10–15 days; if not controlled at 2000 mg once daily, try 1000 mg 2× a day'),
    ('med_metformin', 'child', 3, 'Type 2 diabetes, 10 years and older (IR tablet)', 'PO', '500 mg or 850 mg', 'Once a day', 'Long-term', '2 g/day', 'Label · UK SmPC', 'Above starting dose give in 2–3 divided doses; PR tablets not for children')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_metformin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_metformin', 'renal', 0, 'GFR 60–89', 'Max 3 g/day (IR) or 2000 mg/day (PR); consider dose reduction as function declines.', 'Label · UK SmPC'),
    ('med_metformin', 'renal', 1, 'GFR 45–59', 'Max 2 g/day; review lactic acidosis risk factors before starting; starting dose at most half the maximum.', 'Label · UK SmPC'),
    ('med_metformin', 'renal', 2, 'GFR 30–44', 'Max 1 g/day (MSF: max 1 g/day in moderate renal impairment).', 'Label · UK SmPC'),
    ('med_metformin', 'renal', 3, 'GFR <30', 'Contraindicated.', 'Label · UK SmPC'),
    ('med_metformin', 'hepatic', 4, '', 'Hepatic insufficiency is a contraindication; no separate hepatic dosing is given.', 'Label · UK SmPC'),
    ('med_metformin', 'elderly', 5, '', 'Base the dose on kidney function; check GFR every 3–6 months.', 'Label · UK SmPC'),
    ('med_metformin', 'pregnancy', 6, '', 'Crosses the placenta; data from more than 1,000 exposed pregnancies show no rise in malformations, so it may be considered as add-on or alternative to insulin (UK SmPC), although MSF names insulin the drug of choice in pregnancy. Breastfeeding: excreted in milk; UK SmPC advises against it because data are limited, while MSF lists no contraindication.', 'Label · UK SmPC'),
    ('med_metformin', 'administration', 7, '', 'Take with or after meals and titrate slowly (dividing doses 2–3× a day reduces GI upset). Stop at the time of surgery under general, spinal or epidural anaesthesia and restart no earlier than 48 h after, once kidney function is stable. Switching IR to PR: same total daily dose; not advised above 2000 mg/day.', 'Label · UK SmPC'),
    ('med_metformin', 'forms_ph', 8, '', 'Metformin (as hydrochloride) 500 mg oral tablet/film-coated tablet; 850 mg oral tablet.', 'PNF'),
    ('med_metformin', 'monitor', 9, '', 'GFR before starting and at least yearly (every 3–6 months if at risk or elderly); vitamin B12 if anaemia or neuropathy; if symptoms suggest lactic acidosis, stop metformin and seek urgent care. Use particular caution in children aged 10–12 (few trial data). Overdose: lactic acidosis is an emergency; haemodialysis removes lactate and metformin.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_metformin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_metformin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Metformin 500 mg Tablets SmPC, Medley Pharma Ltd; text revised 04/2025.', 'https://products.mhra.gov.uk/search/?search=metformin#emc-15731', 0),
    ('med_metformin', 'Label · UK SmPC PR', 'UK SmPC (emc)', 'Metformin hydrochloride 500 mg prolonged release tablets SmPC, Genus Pharmaceuticals (STADA); text revised 04/2025.', 'https://products.mhra.gov.uk/search/?search=metformin#emc-5263', 1),
    ('med_metformin', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Metformin oral. Essential Drugs – practical guidelines; updated 09/2023.', 'https://medicalguidelines.msf.org/viewport/EssDr/english/metformin-oral-27983919.html', 2),
    ('med_metformin', 'PNF', 'Philippine National Formulary (PhilHealth)', 'PNF Essential Medicines List, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_metformin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_metformin');


-- ================================================ med_methimazole  (Methimazole)
update public.medicines set description = 'Methimazole inhibits thyroid peroxidase, blocking the iodination of thyroglobulin and the synthesis of T4 and T3. It does not stop release of hormone already stored, so improvement takes several weeks. It is the preferred antithyroid drug for Graves disease except in the first trimester of pregnancy and in thyroid storm, where propylthiouracil is used. In the Philippines it is listed in the PNF Essential Medicines List as 5 mg and 10 mg tablets, and it was added to the WHO Model List of Essential Medicines in 2019 for thyrotoxicosis. It is the preferred antithyroid drug in children because propylthiouracil has caused severe liver injury in children. It is well absorbed (bioavailability about 93%) with a plasma half-life of 3–5 hours that lengthens in liver or kidney impairment, yet the maintenance dose can be taken once daily.', updated_at = now()
where id = 'med_methimazole' and description = 'Methimazole inhibits thyroid peroxidase, blocking the iodination of thyroglobulin and the synthesis of T4 and T3. It does not stop release of hormone already stored, so improvement takes several weeks. It is the preferred antithyroid drug for Graves disease except in the first trimester of pregnancy and in thyroid storm, where propylthiouracil is used.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'DailyMed (US National Library of Medicine); Swedish Medical Products Agency (Läkemedelsverket); Philippine National Formulary (PhilHealth); WHO Model List of Essential Medicines' else source_attribution || '; DailyMed (US National Library of Medicine); Swedish Medical Products Agency (Läkemedelsverket); Philippine National Formulary (PhilHealth); WHO Model List of Essential Medicines' end
where id = 'med_methimazole' and position('DailyMed (US National Library of Medicine)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'indication', 'Hyperthyroidism in children from 3 years of age (EU label)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'indication' and content = 'Hyperthyroidism in children from 3 years of age (EU label)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'adverse', 'Aplastic anaemia, thrombocytopenia, leukopenia and pancytopenia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse' and content = 'Aplastic anaemia, thrombocytopenia, leukopenia and pancytopenia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'adverse', 'Insulin autoimmune syndrome (marked hypoglycaemia, can cause coma)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse' and content = 'Insulin autoimmune syndrome (marked hypoglycaemia, can cause coma)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'adverse', 'Acute pancreatitis (postmarketing; recurs faster on re-exposure)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse' and content = 'Acute pancreatitis (postmarketing; recurs faster on re-exposure)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'adverse', 'Hypoprothrombinaemia with bleeding risk', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse' and content = 'Hypoprothrombinaemia with bleeding risk');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'adverse', 'Loss or change of taste, hair loss, salivary gland swelling, lymphadenopathy', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse' and content = 'Loss or change of taste, hair loss, salivary gland swelling, lymphadenopathy');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'adverse', 'Drug fever, neuritis/polyneuropathy, nephritis (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse' and content = 'Drug fever, neuritis/polyneuropathy, nephritis (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'adverse', 'Hypothyroidism if the dose is too high', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'adverse' and content = 'Hypothyroidism if the dose is too high');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'contraindication', 'Severe hypersensitivity to other thionamides (carbimazole, propylthiouracil)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication' and content = 'Severe hypersensitivity to other thionamides (carbimazole, propylthiouracil)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'contraindication', 'Moderate to severe granulocytopenia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication' and content = 'Moderate to severe granulocytopenia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'contraindication', 'Pre-existing cholestasis not caused by hyperthyroidism', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication' and content = 'Pre-existing cholestasis not caused by hyperthyroidism');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'contraindication', 'Previous acute pancreatitis after thiamazole or carbimazole', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication' and content = 'Previous acute pancreatitis after thiamazole or carbimazole');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'contraindication', 'Combination with thyroid hormone (levothyroxine) during pregnancy', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'contraindication' and content = 'Combination with thyroid hormone (levothyroxine) during pregnancy');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_methimazole', 'interaction', 'Other drugs known to cause agranulocytosis: use with particular care.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole' and kind = 'interaction' and content = 'Other drugs known to cause agranulocytosis: use with particular care.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_methimazole', 'DailyMed (US National Library of Medicine)', 'Methimazole tablets, USP. Prescribing information. Upsher-Smith Laboratories, LLC; revised 12/2023. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2185e6e0-7c21-4348-a7b4-d898f50a0184', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_methimazole'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_methimazole' and url = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2185e6e0-7c21-4348-a7b4-d898f50a0184');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_methimazole', 'Swedish Medical Products Agency (Läkemedelsverket)', 'Thiamazole Uni-Pharma 5 mg tablets. Summary of Product Characteristics. Uni-Pharma Kleon Tsetis Pharmaceutical Laboratories S.A.; text revised 2022-10-04.', 'https://docetp.mpa.se/LMF/Thiamazole%20Uni-Pharma%20tablet%20SmPC_09001bee807a75ba.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_methimazole'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_methimazole' and url = 'https://docetp.mpa.se/LMF/Thiamazole%20Uni-Pharma%20tablet%20SmPC_09001bee807a75ba.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_methimazole', 'Philippine National Formulary (PhilHealth)', 'Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_methimazole'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_methimazole' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_methimazole', 'WHO Model List of Essential Medicines', 'World Health Organization. eEML – Electronic Essential Medicines List: Methimazole (first added 2019, TRS 1021).', 'https://list.essentialmeds.org/medicines/506', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_methimazole'), 0)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_methimazole' and url = 'https://list.essentialmeds.org/medicines/506');
-- med_methimazole
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_methimazole', 'adult', 0, 'Hyperthyroidism, mild (initial)', 'PO', '15 mg/day ÷ 3', 'Every 8 h', 'Until euthyroid', '—', 'Label · DailyMed', ''),
    ('med_methimazole', 'adult', 1, 'Hyperthyroidism, moderately severe (initial)', 'PO', '30–40 mg/day ÷ 3', 'Every 8 h', 'Until euthyroid', '—', 'Label · DailyMed', ''),
    ('med_methimazole', 'adult', 2, 'Hyperthyroidism, severe (initial)', 'PO', '60 mg/day ÷ 3', 'Every 8 h', 'Until euthyroid', '—', 'Label · DailyMed', ''),
    ('med_methimazole', 'adult', 3, 'Hyperthyroidism (maintenance)', 'PO', '5–15 mg/day', 'Once a day or divided', 'Long-term', '—', 'Label · DailyMed', 'Lower the dose if TSH rises'),
    ('med_methimazole', 'adult', 4, 'Hyperthyroidism, mild (initial)', 'PO', '10–20 mg/day', 'Once or 2× a day', 'Until euthyroid', '—', 'Label · EU SmPC', ''),
    ('med_methimazole', 'adult', 5, 'Hyperthyroidism, severe (initial)', 'PO', '30–40 mg/day', 'Divided doses', 'Until euthyroid', '—', 'Label · EU SmPC', 'Higher start may be needed with large goitre or after iodine exposure'),
    ('med_methimazole', 'adult', 6, 'Hyperthyroidism (maintenance)', 'PO', '5–10 mg', 'Once a day', 'Long-term', '—', 'Label · EU SmPC', 'Morning, with or after breakfast; levothyroxine may be added'),
    ('med_methimazole', 'child', 7, 'Hyperthyroidism (initial)', 'PO', '0.4 mg/kg/day ÷ 3', 'Every 8 h', 'Until euthyroid', '—', 'Label · DailyMed', 'Maintenance about half the initial dose'),
    ('med_methimazole', 'child', 8, 'Hyperthyroidism, 3–17 years (initial)', 'PO', '0.5 mg/kg/day ÷ 2–3', '2–3× a day', 'Until euthyroid', '40 mg/day', 'Label · EU SmPC', 'Not recommended at 2 years or younger')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_methimazole');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_methimazole', 'renal', 0, '', 'Half-life is prolonged; individualise the dose, use the lowest effective dose and follow up closely.', 'Label · EU SmPC'),
    ('med_methimazole', 'hepatic', 1, '', 'Clearance is reduced; use the lowest possible dose with close monitoring.', 'Label · EU SmPC'),
    ('med_methimazole', 'pregnancy', 2, '', 'Women of childbearing potential should use effective contraception. If used in pregnancy, give the lowest effective dose without added thyroid hormone; excess dosing can cause fetal goitre and hypothyroidism. Reported first-trimester defects include aplasia cutis, craniofacial malformations, omphalocele and oesophageal atresia. Breastfeeding: possible at up to 10 mg/day without added thyroid hormone, checking the infant''s thyroid function regularly.', 'Label · EU SmPC'),
    ('med_methimazole', 'administration', 3, '', 'Swallow with fluid; do not chew (bitter). High starting doses can be spread over the day; give the maintenance dose once in the morning. Do not stop methimazole and continue levothyroxine alone.', 'Label · EU SmPC'),
    ('med_methimazole', 'forms_ph', 4, '', 'Methimazole (thiamazole) 5 mg and 10 mg oral tablet.', 'PNF'),
    ('med_methimazole', 'monitor', 5, '', 'Blood count before and after starting, and at once if fever, sore throat or mouth ulcers appear (stop if agranulocytosis); liver tests if anorexia, itching or right upper abdominal pain (stop if transaminases exceed 3× the upper limit of normal); TSH and free T4 regularly to avoid hypothyroidism; prothrombin time/INR especially before surgery. (Blood count before/after start from EU SmPC; rest from DailyMed label.)', '')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_methimazole');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_methimazole', 'Label · DailyMed', 'DailyMed (US National Library of Medicine)', 'Methimazole tablets, USP. Upsher-Smith Laboratories; revised 12/2023.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2185e6e0-7c21-4348-a7b4-d898f50a0184', 0),
    ('med_methimazole', 'Label · EU SmPC', 'Swedish Medical Products Agency (Läkemedelsverket)', 'Thiamazole Uni-Pharma 5 mg tablets SmPC; text revised 2022-10-04.', 'https://docetp.mpa.se/LMF/Thiamazole%20Uni-Pharma%20tablet%20SmPC_09001bee807a75ba.pdf', 1),
    ('med_methimazole', 'PNF', 'Philippine National Formulary (PhilHealth)', 'PNF Essential Medicines List, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_methimazole')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_methimazole');


-- ================================================ med_metoprolol  (Metoprolol)
update public.medicines set description = 'Metoprolol is a relatively cardioselective beta-1 adrenergic receptor antagonist that reduces heart rate, contractility and blood pressure and lowers myocardial oxygen demand. Selectivity is dose-dependent and is lost at higher doses. It is used for hypertension, angina, secondary prevention after myocardial infarction, and (as the succinate extended-release form) heart failure with reduced ejection fraction. Oral bioavailability is about 50% after a single dose, rising to about 70% with repeated dosing; the half-life is short (about 3.5 hours, range 1–9 hours), so the immediate-release tartrate is usually given two or more times a day. It is cleared mainly by hepatic CYP2D6, and poor metabolisers can have several-fold higher blood levels. In the Philippines the PNF Essential Medicines List includes only metoprolol tartrate 50 mg and 100 mg tablets (no extended-release succinate or injection).', updated_at = now()
where id = 'med_metoprolol' and description = 'Metoprolol is a relatively cardioselective beta-1 adrenergic receptor antagonist that reduces heart rate, contractility and blood pressure and lowers myocardial oxygen demand. Selectivity is dose-dependent and is lost at higher doses. It is used for hypertension, angina, secondary prevention after myocardial infarction, and (as the succinate extended-release form) heart failure with reduced ejection fraction.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); US FDA label (Drugs@FDA); Pfizer labeling (US); Philippine National Formulary (PNF EML); US FDA label; Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); US FDA label (Drugs@FDA); Pfizer labeling (US); Philippine National Formulary (PNF EML); US FDA label; Philippine National Formulary – EML' end
where id = 'med_metoprolol' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'indication', 'Cardiac arrhythmias, especially supraventricular tachyarrhythmias', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'indication' and content = 'Cardiac arrhythmias, especially supraventricular tachyarrhythmias');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'indication', 'Adjunct in thyrotoxicosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'indication' and content = 'Adjunct in thyrotoxicosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'indication', 'Migraine prophylaxis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'indication' and content = 'Migraine prophylaxis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'adverse', 'Orthostatic hypotension, occasionally with syncope', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse' and content = 'Orthostatic hypotension, occasionally with syncope');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'adverse', 'Headache, nausea, vomiting and abdominal pain', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse' and content = 'Headache, nausea, vomiting and abdominal pain');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'adverse', 'Nightmares, insomnia or somnolence', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse' and content = 'Nightmares, insomnia or somnolence');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'adverse', 'Raynaud''s phenomenon and cold extremities; gangrene in severe peripheral arterial disease (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse' and content = 'Raynaud''s phenomenon and cold extremities; gangrene in severe peripheral arterial disease (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'adverse', 'Visual disturbance, dry eyes, tinnitus', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse' and content = 'Visual disturbance, dry eyes, tinnitus');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'adverse', 'Worsening of psoriasis, alopecia, photosensitivity', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse' and content = 'Worsening of psoriasis, alopecia, photosensitivity');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'adverse', 'Sexual dysfunction', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse' and content = 'Sexual dysfunction');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'adverse', 'Retroperitoneal fibrosis and Peyronie''s disease (frequency not known)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'adverse' and content = 'Retroperitoneal fibrosis and Peyronie''s disease (frequency not known)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'contraindication', 'Severe asthma or history of severe bronchospasm', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication' and content = 'Severe asthma or history of severe bronchospasm');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'contraindication', 'Severe peripheral arterial disease', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication' and content = 'Severe peripheral arterial disease');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'contraindication', 'Untreated phaeochromocytoma', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication' and content = 'Untreated phaeochromocytoma');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'contraindication', 'Metabolic acidosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication' and content = 'Metabolic acidosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'contraindication', 'Suspected MI with heart rate <45/min or significant first-degree heart block (PR ≥0.24 s)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication' and content = 'Suspected MI with heart rate <45/min or significant first-degree heart block (PR ≥0.24 s)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'contraindication', 'Prinzmetal''s (variant) angina: use only with great care (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'contraindication' and content = 'Prinzmetal''s (variant) angina: use only with great care (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'interaction', 'IV verapamil must never be given to a patient taking metoprolol.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction' and content = 'IV verapamil must never be given to a patient taking metoprolol.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'interaction', 'Class I antiarrhythmics and amiodarone: added slowing of heart rate and AV conduction.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction' and content = 'Class I antiarrhythmics and amiodarone: added slowing of heart rate and AV conduction.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'interaction', 'Insulin and sulfonylureas: altered hypoglycaemia risk; warning signs may be masked.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction' and content = 'Insulin and sulfonylureas: altered hypoglycaemia risk; warning signs may be masked.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'interaction', 'NSAIDs (e.g., indometacin): reduce the blood-pressure-lowering effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction' and content = 'NSAIDs (e.g., indometacin): reduce the blood-pressure-lowering effect.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'interaction', 'Rifampicin and other enzyme inducers: lower metoprolol levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction' and content = 'Rifampicin and other enzyme inducers: lower metoprolol levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'interaction', 'Bupropion and cimetidine: raise metoprolol levels (CYP2D6 inhibition).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction' and content = 'Bupropion and cimetidine: raise metoprolol levels (CYP2D6 inhibition).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'interaction', 'Other beta-blockers, including eye drops: additive beta-blockade.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction' and content = 'Other beta-blockers, including eye drops: additive beta-blockade.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metoprolol', 'interaction', 'Inhalational anaesthetics and lidocaine: additive cardiac depression; tell the anaesthetist.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metoprolol' and kind = 'interaction' and content = 'Inhalational anaesthetics and lidocaine: additive cardiac depression; tell the anaesthetist.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metoprolol', 'UK SmPC (emc)', 'Metoprolol Tartrate 25 mg Tablets – Summary of Product Characteristics. Zentiva Pharma UK Limited. Electronic Medicines Compendium (emc), medicines.org.uk; updated August 2026.', 'https://products.mhra.gov.uk/search/?search=metoprolol#emc-12971', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metoprolol'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metoprolol' and url = 'https://products.mhra.gov.uk/search/?search=metoprolol#emc-12971');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metoprolol', 'US FDA label (Drugs@FDA)', 'TOPROL-XL (metoprolol succinate) extended-release tablets. Prescribing information. Revised 03/2023. US Food and Drug Administration.', 'https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/019962s050s052lbl.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metoprolol'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metoprolol' and url = 'https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/019962s050s052lbl.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metoprolol', 'Pfizer labeling (US)', 'Metoprolol Tartrate Injection, USP, 5 mg/5 mL. Prescribing information. Hospira, Inc.; revised 5/2024.', 'https://labeling.pfizer.com/ShowLabeling.aspx?id=4523', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metoprolol'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metoprolol' and url = 'https://labeling.pfizer.com/ShowLabeling.aspx?id=4523');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metoprolol', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metoprolol'), 0)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metoprolol' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_metoprolol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'safe'::condition_safety, 'UK SmPC: dose adjustment usually not needed in renal impairment'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_metoprolol');
-- med_metoprolol
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_metoprolol', 'adult', 0, 'Hypertension', 'PO', '100 mg/day to start', 'Once a day or ÷ 2', 'Long term', '200 mg/day', 'Label · UK SmPC', 'Raise by 100 mg/day at weekly intervals'),
    ('med_metoprolol', 'adult', 1, 'Hypertension (extended-release succinate)', 'PO', '25–100 mg', 'Once a day', 'Long term', '>400 mg/day not studied', 'Label · US XL', 'Adjust at weekly or longer intervals'),
    ('med_metoprolol', 'adult', 2, 'Angina', 'PO', '50–100 mg', '2–3× a day', 'Long term', '400 mg/day', 'Label · UK SmPC', ''),
    ('med_metoprolol', 'adult', 3, 'Angina (extended-release succinate)', 'PO', '100 mg', 'Once a day', 'Long term', '>400 mg/day not studied', 'Label · US XL', 'Increase weekly'),
    ('med_metoprolol', 'adult', 4, 'Arrhythmias', 'PO', '50 mg', '2–3× a day', 'Long term', '300 mg/day', 'Label · UK SmPC', ''),
    ('med_metoprolol', 'adult', 5, 'Hyperthyroidism (adjunct)', 'PO', '50 mg', '4× a day', 'Until euthyroid', '—', 'Label · UK SmPC', 'Reduce as euthyroid state is reached'),
    ('med_metoprolol', 'adult', 6, 'Acute MI, early', 'IV', '5 mg', 'Every 2 min × 3 doses', 'Once (15 mg total)', '15 mg', 'Label · US IV', 'Coronary care unit; monitor ECG, BP, HR'),
    ('med_metoprolol', 'adult', 7, 'Acute MI, early (after IV)', 'PO', '50 mg', 'Every 6 h', '48 h', '—', 'Label · US', 'Start 15 min after last IV dose; 25 mg if not tolerated'),
    ('med_metoprolol', 'adult', 8, 'Acute MI, early (oral only)', 'PO', '50 mg', 'Every 6 h', '48 h', '—', 'Label · UK SmPC', 'Ideally within 12 h of chest pain onset'),
    ('med_metoprolol', 'adult', 9, 'Post-MI maintenance', 'PO', '200 mg/day ÷ 2', '2× a day', '≥3 months', '—', 'Label · UK SmPC', 'US label: 100 mg 2× a day'),
    ('med_metoprolol', 'adult', 10, 'Migraine prophylaxis', 'PO', '100–200 mg/day', 'Divided doses', 'Long term', '200 mg/day', 'Label · UK SmPC', ''),
    ('med_metoprolol', 'adult', 11, 'Heart failure (extended-release succinate)', 'PO', '25 mg (NYHA II); 12.5 mg (more severe)', 'Once a day', 'Long term', '200 mg/day', 'Label · US XL', 'Double every 2 weeks to highest tolerated dose'),
    ('med_metoprolol', 'child', 12, 'Hypertension, ≥6 y (extended-release succinate)', 'PO', '1 mg/kg', 'Once a day', 'Long term', '50 mg starting dose', 'Label · US XL', '>2 mg/kg or >200 mg/day not studied; not for <6 y')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_metoprolol');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_metoprolol', 'renal', 0, '', 'Dose adjustment usually not needed.', 'Label · UK SmPC'),
    ('med_metoprolol', 'hepatic', 1, '', 'Significant liver dysfunction: consider lower doses (levels may rise substantially); start low and titrate gradually.', 'Label · UK SmPC'),
    ('med_metoprolol', 'elderly', 2, '', 'No special dose needed in healthy older adults; watch for excessive falls in blood pressure or pulse.', 'Label · UK SmPC'),
    ('med_metoprolol', 'pregnancy', 3, '', 'Avoid unless benefit outweighs risk (may reduce placental perfusion); has been used for hypertension after 20 weeks under close supervision. Stop 2–3 days before delivery if possible. Watch newborns for bradycardia, hypotension and hypoglycaemia.', 'Label · UK SmPC'),
    ('med_metoprolol', 'pregnancy', 4, '', 'Breastfeeding: small amounts in milk (0.5–2% of maternal weight-adjusted dose); monitor the infant for slow heart rate and listlessness.', 'Label · US XL'),
    ('med_metoprolol', 'administration', 5, '', 'Tartrate: take with a drink of water; US label advises with or right after meals.', 'Label · UK SmPC'),
    ('med_metoprolol', 'administration', 6, '', 'Extended-release succinate tablets can be split at the score line but must not be crushed or chewed.', 'Label · US XL'),
    ('med_metoprolol', 'administration', 7, '', 'Stopping: taper over about 10 days, using 25 mg for the last 6 days. For surgery, if stopping, stop at least 24 h before and tell the anaesthetist.', 'Label · UK SmPC'),
    ('med_metoprolol', 'administration', 8, '', 'Poor CYP2D6 metabolisers may need lower doses.', 'Label · UK SmPC'),
    ('med_metoprolol', 'forms_ph', 9, '', 'Metoprolol (as tartrate) tablet 50 mg, 100 mg.', 'PNF'),
    ('med_metoprolol', 'monitor', 10, '', 'Check pulse and blood pressure at each visit; reduce dose or stop if heart rate falls below 50–55/min.', 'Label · UK SmPC'),
    ('med_metoprolol', 'monitor', 11, '', 'Diabetics: check blood glucose more often (masked hypoglycaemia, especially with sulfonylureas). Thyrotoxicosis: monitor thyroid and cardiac function.', 'Label · UK SmPC'),
    ('med_metoprolol', 'monitor', 12, '', 'During IV dosing in MI: continuous ECG, blood pressure and heart rate.', 'Label · US IV')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_metoprolol');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_metoprolol', 'Label · UK SmPC', 'UK SmPC (emc)', 'Metoprolol Tartrate 25 mg Tablets. Summary of Product Characteristics. Zentiva Pharma UK Ltd; 2026.', 'https://products.mhra.gov.uk/search/?search=metoprolol#emc-12971', 0),
    ('med_metoprolol', 'Label · US XL', 'US FDA label', 'TOPROL-XL (metoprolol succinate) extended-release tablets. Prescribing information; 03/2023.', 'https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/019962s050s052lbl.pdf', 1),
    ('med_metoprolol', 'Label · US IV', 'Pfizer labeling (US)', 'Metoprolol Tartrate Injection, USP. Prescribing information. Hospira, Inc.; 5/2024.', 'https://labeling.pfizer.com/ShowLabeling.aspx?id=4523', 2),
    ('med_metoprolol', 'Label · US', 'DailyMed', 'LOPRESSOR (metoprolol tartrate) tablets. Prescribing information. Validus Pharmaceuticals; 9/2023.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0283bc9d-6998-493a-824a-d4c85f704111', 3),
    ('med_metoprolol', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_metoprolol')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_metoprolol');


-- ================================================ med_metronidazole  (Metronidazole)
update public.medicines set description = 'Metronidazole is a nitroimidazole that enters anaerobic bacteria and protozoa by diffusion and is activated by intracellular reduction to cytotoxic free radicals that break DNA strands, causing cell death. Its antibacterial activity is limited to anaerobes, so in mixed intra-abdominal infections it is combined with an agent active against aerobic gram-negative bacteria. Oral metronidazole is rapidly and almost completely absorbed (peak levels in 20 minutes to 3 hours; half-life about 8.5 hours), so oral and IV routes are equally effective and patients should be switched to tablets as soon as they can swallow. It is also used for surgical prophylaxis against anaerobes and for dental and gum infections. In the Philippines it is on the PNF Essential Medicines List as 250 mg and 500 mg tablets, an oral suspension and a 5 mg/mL IV infusion.', updated_at = now()
where id = 'med_metronidazole' and description = 'Metronidazole is a nitroimidazole that enters anaerobic bacteria and protozoa by diffusion and is activated by intracellular reduction to cytotoxic free radicals that break DNA strands, causing cell death. Its antibacterial activity is limited to anaerobes, so in mixed intra-abdominal infections it is combined with an agent active against aerobic gram-negative bacteria.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PNF EML); Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); MSF Essential Drugs; Philippine National Formulary (PNF EML); Philippine National Formulary – EML' end
where id = 'med_metronidazole' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'indication', 'Prevention of post-operative anaerobic infection (surgical prophylaxis)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'indication' and content = 'Prevention of post-operative anaerobic infection (surgical prophylaxis)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'indication', 'Anaerobic septicaemia, peritonitis, brain abscess, pneumonia, osteomyelitis and pelvic infections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'indication' and content = 'Anaerobic septicaemia, peritonitis, brain abscess, pneumonia, osteomyelitis and pelvic infections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'indication', 'Acute ulcerative gingivitis and acute dental infections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'indication' and content = 'Acute ulcerative gingivitis and acute dental infections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'indication', 'Anaerobically infected leg ulcers and pressure sores', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'indication' and content = 'Anaerobically infected leg ulcers and pressure sores');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'adverse', 'Dark or brownish urine (harmless)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse' and content = 'Dark or brownish urine (harmless)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'adverse', 'Encephalopathy, subacute cerebellar syndrome, ataxia and seizures (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse' and content = 'Encephalopathy, subacute cerebellar syndrome, ataxia and seizures (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'adverse', 'Optic neuropathy, hearing impairment and tinnitus', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse' and content = 'Optic neuropathy, hearing impairment and tinnitus');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'adverse', 'Hepatitis, jaundice and reversible pancreatitis (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse' and content = 'Hepatitis, jaundice and reversible pancreatitis (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'adverse', 'Severe skin reactions: SJS/TEN, AGEP, fixed drug eruption', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse' and content = 'Severe skin reactions: SJS/TEN, AGEP, fixed drug eruption');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'adverse', 'QT prolongation, especially with other QT-prolonging drugs', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse' and content = 'QT prolongation, especially with other QT-prolonging drugs');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'adverse', 'Agranulocytosis, thrombocytopenia and pancytopenia (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse' and content = 'Agranulocytosis, thrombocytopenia and pancytopenia (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'adverse', 'Anaphylaxis, angioedema and urticaria (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'adverse' and content = 'Anaphylaxis, angioedema and urticaria (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'contraindication', 'Cockayne syndrome: severe, sometimes fatal liver failure reported; avoid unless no alternative (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'contraindication' and content = 'Cockayne syndrome: severe, sometimes fatal liver failure reported; avoid unless no alternative (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'contraindication', 'Active or chronic severe CNS or peripheral nerve disease: use with caution (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'contraindication' and content = 'Active or chronic severe CNS or peripheral nerve disease: use with caution (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'contraindication', 'Severe hepatic impairment or hepatic encephalopathy: drug accumulates; reduce the dose (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'contraindication' and content = 'Severe hepatic impairment or hepatic encephalopathy: drug accumulates; reduce the dose (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'interaction', 'Phenytoin and phenobarbital: shorten metronidazole half-life to about 3 hours.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction' and content = 'Phenytoin and phenobarbital: shorten metronidazole half-life to about 3 hours.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'interaction', '5-fluorouracil: reduced clearance and more toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction' and content = '5-fluorouracil: reduced clearance and more toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'interaction', 'Ciclosporin: raised ciclosporin levels; monitor levels and creatinine.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction' and content = 'Ciclosporin: raised ciclosporin levels; monitor levels and creatinine.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'interaction', 'Busulfan: raised busulfan levels, risk of severe toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction' and content = 'Busulfan: raised busulfan levels, risk of severe toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'interaction', 'QT-prolonging drugs: QT prolongation reported in combination.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction' and content = 'QT-prolonging drugs: QT prolongation reported in combination.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_metronidazole', 'interaction', 'Ergometrine and phenytoin: their plasma levels may rise (MSF).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole' and kind = 'interaction' and content = 'Ergometrine and phenytoin: their plasma levels may rise (MSF).');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metronidazole', 'UK SmPC (emc)', 'Metronidazole Tablets BP 400 mg – Summary of Product Characteristics. Milpharm Limited (PL 16363/0026). Electronic Medicines Compendium (emc), medicines.org.uk; updated April 2025.', 'https://products.mhra.gov.uk/search/?search=metronidazole#emc-12817', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metronidazole'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metronidazole' and url = 'https://products.mhra.gov.uk/search/?search=metronidazole#emc-12817');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metronidazole', 'UK SmPC (emc)', 'Metronidazole 500 mg/100 ml Intravenous Infusion – Summary of Product Characteristics. Baxter Healthcare Ltd. Electronic Medicines Compendium (emc), medicines.org.uk; updated April 2026.', 'https://products.mhra.gov.uk/search/?search=metronidazole#emc-1842', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metronidazole'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metronidazole' and url = 'https://products.mhra.gov.uk/search/?search=metronidazole#emc-1842');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metronidazole', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Metronidazole oral. medicalguidelines.msf.org.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-oral-16684146.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metronidazole'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metronidazole' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-oral-16684146.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metronidazole', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Metronidazole injectable. medicalguidelines.msf.org.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-injectable-16682959.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metronidazole'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metronidazole' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-injectable-16682959.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_metronidazole', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_metronidazole'), 0)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_metronidazole' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'peptic_ulcer_disease', 'med_metronidazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease'), 0), 'safe'::condition_safety, 'Part of H. pylori eradication combination therapy (UK SmPC gives a paediatric H. pylori dose)'
where exists (select 1 from public.diseases where id = 'peptic_ulcer_disease')
  and exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease' and medicine_id = 'med_metronidazole');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_metronidazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'safe'::condition_safety, 'No routine dose change in renal failure, including peritoneal dialysis; removed by haemodialysis, so re-dose right after each session'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_metronidazole');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_gastroenteritis', 'med_metronidazole', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis'), 0), 'safe'::condition_safety, 'Treats parasitic causes of dysentery/diarrhoea (amoebiasis, giardiasis); our note: not for routine watery or viral gastroenteritis'
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_gastroenteritis' and medicine_id = 'med_metronidazole');
-- med_metronidazole
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_metronidazole', 'adult', 0, 'Anaerobic infection (treatment)', 'PO', '800 mg first dose, then 400 mg', 'Every 8 h', 'About 7 days', '—', 'Label · UK SmPC', ''),
    ('med_metronidazole', 'adult', 1, 'Anaerobic infection (treatment)', 'IV', '500 mg', 'Every 8 h', '7–10 days', '—', 'Label · UK IV', 'Or 1–1.5 g once a day; switch to PO when able'),
    ('med_metronidazole', 'adult', 2, 'Surgical prophylaxis', 'IV', '500 mg', 'Before/during/after surgery, then every 8 h', '≤24 h (never >48 h)', '—', 'Label · UK IV', 'Or 1–1.5 g single dose 30–60 min before surgery'),
    ('med_metronidazole', 'adult', 3, 'Surgical prophylaxis', 'PO', '400 mg', 'Every 8 h', '24 h before surgery', '—', 'Label · UK SmPC', 'Then IV/rectal until oral possible'),
    ('med_metronidazole', 'adult', 4, 'Trichomoniasis', 'PO', '400 mg', '2× a day', '5–7 days', '—', 'Label · UK SmPC', 'Or 200 mg 3× a day for 7 days; treat partner'),
    ('med_metronidazole', 'adult', 5, 'Bacterial vaginosis', 'PO', '400 mg', '2× a day', '5–7 days', '—', 'Label · UK SmPC', 'Or 2 g single dose'),
    ('med_metronidazole', 'adult', 6, 'Invasive intestinal amoebiasis', 'PO', '800 mg', '3× a day', '5 days', '—', 'Label · UK SmPC', 'MSF: 500 mg 3× a day, 5 days (5–10 days hepatic)'),
    ('med_metronidazole', 'adult', 7, 'Intestinal amoebiasis (less susceptible), chronic amoebic hepatitis', 'PO', '400 mg', '3× a day', '5–10 days', '—', 'Label · UK SmPC', ''),
    ('med_metronidazole', 'adult', 8, 'Symptomless amoebic cyst passers', 'PO', '400–800 mg', '3× a day', '5–10 days', '—', 'Label · UK SmPC', ''),
    ('med_metronidazole', 'adult', 9, 'Giardiasis', 'PO', '2 g', 'Once a day', '3 days', '—', 'Label · UK SmPC', 'Or 400 mg 3× a day 5 days, or 500 mg 2× a day 7–10 days'),
    ('med_metronidazole', 'adult', 10, 'Acute ulcerative gingivitis', 'PO', '200 mg', '3× a day', '3 days', '—', 'Label · UK SmPC', ''),
    ('med_metronidazole', 'adult', 11, 'Acute dental infection', 'PO', '200 mg', '3× a day', '3–7 days', '—', 'Label · UK SmPC', ''),
    ('med_metronidazole', 'adult', 12, 'Infected leg ulcers, pressure sores', 'PO', '400 mg', '3× a day', '7 days', '—', 'Label · UK SmPC', ''),
    ('med_metronidazole', 'child', 13, 'Anaerobic infection (8 weeks–12 y)', 'PO', '7.5 mg/kg', 'Every 8 h', 'Usually 7 days', '40 mg/kg/day', 'Label · UK SmPC', 'Or 20–30 mg/kg once a day'),
    ('med_metronidazole', 'child', 14, 'Anaerobic infection (≥1 month)', 'IV', '10 mg/kg', 'Every 8 h', 'By indication', '1,500 mg/day', 'MSF · IV', 'Infuse over 30 min'),
    ('med_metronidazole', 'child', 15, 'Surgical prophylaxis (<12 y)', 'PO', '20–30 mg/kg', 'Single dose', '1–2 h before surgery', '—', 'Label · UK SmPC', ''),
    ('med_metronidazole', 'child', 16, 'Amoebiasis', 'PO', '15 mg/kg', '3× a day', '5 days (intestinal); 5–10 days (hepatic)', '—', 'MSF', ''),
    ('med_metronidazole', 'child', 17, 'Giardiasis', 'PO', '30 mg/kg', 'Once a day', '3 days', '—', 'MSF', ''),
    ('med_metronidazole', 'child', 18, 'Trichomoniasis', 'PO', '40 mg/kg', 'Single dose', '1 day', '2 g/dose', 'Label · UK SmPC', 'Or 15–30 mg/kg/day ÷ 2–3'),
    ('med_metronidazole', 'child', 19, 'H. pylori eradication (with other drugs)', 'PO', '20 mg/kg/day ÷ 2', '2× a day', '7–14 days', '500 mg/dose', 'Label · UK SmPC', ''),
    ('med_metronidazole', 'neonate', 20, 'Anaerobic infection (<8 weeks)', 'PO', '15 mg/kg', 'Once a day', 'Usually 7 days', '—', 'Label · UK SmPC', 'Or 7.5 mg/kg every 12 h; check levels in preterm babies'),
    ('med_metronidazole', 'neonate', 21, 'Surgical prophylaxis (<40 weeks gestation)', 'IV', '10 mg/kg', 'Single dose', 'Before surgery', '—', 'Label · UK IV', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_metronidazole');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_metronidazole', 'renal', 0, '', 'No routine dose change in renal failure, including peritoneal dialysis.', 'Label · UK IV'),
    ('med_metronidazole', 'renal', 1, 'Haemodialysis', 'Removed by haemodialysis: give the dose again immediately after each session.', 'Label · UK IV'),
    ('med_metronidazole', 'hepatic', 2, '', 'Advanced hepatic insufficiency or hepatic encephalopathy: drug accumulates (more CNS effects); reduce the dose and monitor serum levels.', 'Label · UK IV'),
    ('med_metronidazole', 'hepatic', 3, '', 'Severe hepatic impairment: give one third of the total daily dose, once a day.', 'MSF'),
    ('med_metronidazole', 'elderly', 4, '', 'Usually well tolerated; use caution with high-dose regimens.', 'Label · UK SmPC'),
    ('med_metronidazole', 'pregnancy', 5, '', 'UK SmPC: give in pregnancy or breastfeeding only if essential; short high-dose regimens not recommended. MSF: no contraindication in pregnancy, but split into smaller doses and avoid prolonged use; passes into breast milk (infant GI upset).', 'Label · UK SmPC'),
    ('med_metronidazole', 'administration', 6, '', 'Swallow tablets whole with water, during or after a meal.', 'Label · UK SmPC'),
    ('med_metronidazole', 'administration', 7, '', 'IV: infuse about 5 mL/min (one 100 mL bag over 20–60 min); do not add other drugs to the bag; switch to oral as soon as possible. Contains 13.5 mmol (310 mg) sodium per 100 mL.', 'Label · UK IV'),
    ('med_metronidazole', 'forms_ph', 8, '', 'Tablet 250 mg, 500 mg; suspension 125 mg base/5 mL (200 mg/5 mL as benzoate), 60 mL; IV infusion 5 mg/mL, 100 mL vial.', 'PNF'),
    ('med_metronidazole', 'monitor', 9, '', 'Courses longer than 10 days: check white cell count and watch for numbness, tingling, unsteadiness or fits; stop if they appear.', 'Label · UK SmPC'),
    ('med_metronidazole', 'monitor', 10, '', 'Check INR/prothrombin time with warfarin; lithium, creatinine and electrolytes with lithium; ciclosporin levels if co-prescribed.', 'Label · UK SmPC'),
    ('med_metronidazole', 'monitor', 11, '', 'Cockayne syndrome: liver tests before, during and after treatment; stop if markedly raised.', 'Label · UK SmPC'),
    ('med_metronidazole', 'monitor', 12, '', 'Preterm neonates: check serum levels after a few days (accumulation in week one).', 'Label · UK IV')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_metronidazole');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_metronidazole', 'Label · UK SmPC', 'UK SmPC (emc)', 'Metronidazole Tablets BP 400 mg. Summary of Product Characteristics. Milpharm Ltd; 2025.', 'https://products.mhra.gov.uk/search/?search=metronidazole#emc-12817', 0),
    ('med_metronidazole', 'Label · UK IV', 'UK SmPC (emc)', 'Metronidazole 500 mg/100 ml Intravenous Infusion. Summary of Product Characteristics. Baxter Healthcare Ltd; 2026.', 'https://products.mhra.gov.uk/search/?search=metronidazole#emc-1842', 1),
    ('med_metronidazole', 'MSF', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Metronidazole oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-oral-16684146.html', 2),
    ('med_metronidazole', 'MSF · IV', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Metronidazole injectable.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/metronidazole-injectable-16682959.html', 3),
    ('med_metronidazole', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_metronidazole')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_metronidazole');


update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
