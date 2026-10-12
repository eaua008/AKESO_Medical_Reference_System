-- =====================================================================
-- 020_diseases_batch2.sql  -  5 new diseases with their symptoms and medicines
-- =====================================================================
-- Diseases: Post-Streptococcal Glomerulonephritis, Bacterial Meningitis, Hyperthyroidism (Graves' Disease), Gout, Scabies.
-- New symptoms: sym_neck_stiffness, sym_nonblanching_rash, sym_seizures, sym_hematuria, sym_periorbital_edema, sym_heat_intolerance, sym_tremor, sym_goiter, sym_proptosis, sym_podagra, sym_tophi, sym_burrows.
-- New medicines: med_vancomycin, med_dexamethasone, med_methimazole, med_propranolol, med_colchicine, med_allopurinol, med_permethrin, med_ivermectin.
-- Existing symptoms and medicines are linked by id, not copied.
--
-- Safe to run more than once: rows that already exist are left alone, and a
-- list (causes, tests, references...) is only filled in when that entry has
-- none yet, so later edits made in Content Management are kept.
-- Sources are cited per entry (Harrison's, StatPearls, WHO, KDIGO, ACG, AHA,
-- WSES, Goodman & Gilman's). Educational reference only.
-- =====================================================================

begin;

-- ===================================================== new symptoms
insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_neck_stiffness', 'Stiff neck (neck stiffness)', 'Nuchal rigidity (meningism)', 'Pain and resistance when bending the chin toward the chest, caused by irritation of the meninges. Together with fever and headache or confusion it is a classic sign of meningitis; Kernig and Brudzinski signs test the same irritation. Muscle strain and neck arthritis also cause stiffness, but usually without fever.', 'sys_nervous', true, array['meningitis', 'neurologic', 'emergency']::text[], 8, 'With fever and headache, a stiff neck strongly suggests meningitis and needs emergency assessment, although its absence does not rule meningitis out.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Bacterial Meningitis', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_neck_stiffness', 'Bacterial meningitis', 0),
    ('sym_neck_stiffness', 'Viral meningitis', 1),
    ('sym_neck_stiffness', 'Subarachnoid hemorrhage', 2),
    ('sym_neck_stiffness', 'Neck muscle strain or torticollis', 3),
    ('sym_neck_stiffness', 'Cervical spondylosis', 4),
    ('sym_neck_stiffness', 'Retropharyngeal abscess', 5)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_neck_stiffness');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_neck_stiffness', 'Fever, headache, vomiting or sensitivity to light with a stiff neck', 0),
    ('sym_neck_stiffness', 'Confusion, drowsiness or seizures', 1),
    ('sym_neck_stiffness', 'A purple rash that does not fade when pressed', 2),
    ('sym_neck_stiffness', 'Sudden, severe ''worst ever'' headache', 3)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_neck_stiffness');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_neck_stiffness', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_neck_stiffness', 'StatPearls - Bacterial Meningitis', 'Bacterial Meningitis. [Updated 2023 Aug 8]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK470351/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_neck_stiffness');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_nonblanching_rash', 'Purple rash that does not fade when pressed (non-blanching rash)', 'Non-blanching petechial or purpuric rash', 'Small red-purple spots (petechiae) or larger bruise-like patches (purpura) that stay visible when a clear glass is pressed against them, because blood has leaked into the skin. With fever it can signal meningococcal septicemia, which can progress within hours; it also occurs with low platelets, dengue and vasculitis.', 'sys_integ', true, array['rash', 'meningococcal', 'sepsis', 'emergency']::text[], 8, 'In a feverish, unwell person a non-blanching rash is a warning sign of meningococcal septicemia and needs immediate treatment.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Bacterial Meningitis; WHO Fact Sheet - Meningitis', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_nonblanching_rash', 'Meningococcal septicemia', 0),
    ('sym_nonblanching_rash', 'Other sepsis with disseminated intravascular coagulation', 1),
    ('sym_nonblanching_rash', 'Dengue and other causes of low platelets', 2),
    ('sym_nonblanching_rash', 'Immune thrombocytopenia', 3),
    ('sym_nonblanching_rash', 'Vasculitis (e.g., IgA vasculitis)', 4),
    ('sym_nonblanching_rash', 'Leukemia', 5)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_nonblanching_rash');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_nonblanching_rash', 'Fever with a rapidly spreading rash', 0),
    ('sym_nonblanching_rash', 'Cold hands and feet, rapid breathing or confusion', 1),
    ('sym_nonblanching_rash', 'Stiff neck or severe headache', 2),
    ('sym_nonblanching_rash', 'Bleeding from gums, nose or in urine or stool', 3)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_nonblanching_rash');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_nonblanching_rash', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_nonblanching_rash', 'StatPearls - Bacterial Meningitis', 'Bacterial Meningitis. [Updated 2023 Aug 8]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK470351/', false, 1),
    ('sym_nonblanching_rash', 'WHO Fact Sheet - Meningitis', 'World Health Organization. Meningitis. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/meningitis', false, 2)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_nonblanching_rash');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_seizures', 'Seizures (fits or convulsions)', 'Seizure', 'Episodes of abnormal electrical activity in the brain causing jerking movements, stiffening, staring or loss of awareness. A first seizure, a seizure with fever in an adult, or one lasting more than 5 minutes needs urgent medical assessment.', 'sys_nervous', true, array['neurologic', 'emergency']::text[], 5, 'Seizures have many causes; with fever and altered consciousness they raise concern for meningitis or encephalitis and need urgent care.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Bacterial Meningitis', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_seizures', 'Epilepsy', 0),
    ('sym_seizures', 'Meningitis or encephalitis', 1),
    ('sym_seizures', 'Febrile seizures in young children', 2),
    ('sym_seizures', 'Head injury or stroke', 3),
    ('sym_seizures', 'Low blood sugar or sodium', 4),
    ('sym_seizures', 'Alcohol or drug withdrawal', 5),
    ('sym_seizures', 'Severe high blood pressure (hypertensive encephalopathy)', 6)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_seizures');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_seizures', 'Seizure lasting more than 5 minutes or repeated without waking between', 0),
    ('sym_seizures', 'First seizure, or seizure with fever and stiff neck', 1),
    ('sym_seizures', 'Seizure after a head injury', 2),
    ('sym_seizures', 'Seizure in pregnancy', 3)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_seizures');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_seizures', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_seizures', 'StatPearls - Bacterial Meningitis', 'Bacterial Meningitis. [Updated 2023 Aug 8]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK470351/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_seizures');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_hematuria', 'Blood in urine (hematuria / cola-colored urine)', 'Hematuria', 'Red, pink or brown (cola- or tea-colored) urine caused by red blood cells, or blood found only on urine testing. Brown urine with red cell casts suggests bleeding from the glomeruli (glomerulonephritis); bright red urine with clots more often comes from the bladder or urinary tract.', 'sys_renal', false, array['kidney', 'urine', 'nephritic']::text[], 6, 'Visible blood or cola-colored urine with swelling and high blood pressure points to glomerulonephritis; isolated hematuria has many other causes.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Poststreptococcal Glomerulonephritis', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_hematuria', 'Post-streptococcal glomerulonephritis and IgA nephropathy', 0),
    ('sym_hematuria', 'Urinary tract infection', 1),
    ('sym_hematuria', 'Kidney or ureteric stones', 2),
    ('sym_hematuria', 'Bladder or kidney cancer (especially older smokers)', 3),
    ('sym_hematuria', 'Strenuous exercise or menstruation', 4),
    ('sym_hematuria', 'Anticoagulant use', 5)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hematuria');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_hematuria', 'Reduced urine output with swelling or breathlessness', 0),
    ('sym_hematuria', 'Severe headache or high blood pressure', 1),
    ('sym_hematuria', 'Painless visible blood in urine in an adult over 40', 2),
    ('sym_hematuria', 'Fever with flank pain', 3)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_hematuria');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_hematuria', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_hematuria', 'StatPearls - Poststreptococcal Glomerulonephritis', 'Poststreptococcal Glomerulonephritis. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://statpearls.com/as/renal/22287', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_hematuria');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_periorbital_edema', 'Puffy eyelids and face (periorbital edema)', 'Periorbital edema', 'Swelling around the eyes and face, usually most obvious on waking and improving during the day. In children it is often the first sign of kidney disease such as post-streptococcal glomerulonephritis or nephrotic syndrome; allergy and insect bites cause similar but usually itchy swelling.', 'sys_renal', false, array['swelling', 'kidney', 'pediatrics']::text[], 6, 'Facial and eyelid puffiness, worst in the morning, is a typical early sign of nephritic and nephrotic syndromes in children.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Poststreptococcal Glomerulonephritis', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_periorbital_edema', 'Acute glomerulonephritis', 0),
    ('sym_periorbital_edema', 'Nephrotic syndrome', 1),
    ('sym_periorbital_edema', 'Allergic reactions and angioedema', 2),
    ('sym_periorbital_edema', 'Hypothyroidism', 3),
    ('sym_periorbital_edema', 'Eye infections (periorbital cellulitis)', 4)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_periorbital_edema');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_periorbital_edema', 'Swelling of lips or tongue with breathing difficulty (angioedema)', 0),
    ('sym_periorbital_edema', 'Little urine or cola-colored urine', 1),
    ('sym_periorbital_edema', 'Painful, red, hot swelling around one eye with fever', 2)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_periorbital_edema');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_periorbital_edema', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_periorbital_edema', 'StatPearls - Poststreptococcal Glomerulonephritis', 'Poststreptococcal Glomerulonephritis. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://statpearls.com/as/renal/22287', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_periorbital_edema');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_heat_intolerance', 'Heat intolerance and excessive sweating', 'Heat intolerance', 'Feeling unusually hot, sweaty or uncomfortable in warm surroundings that others tolerate. It reflects increased heat production from a raised metabolic rate and is a classic symptom of hyperthyroidism, together with weight loss, tremor and palpitations.', 'sys_endo', false, array['thyroid', 'endocrine', 'metabolism']::text[], 6, 'Feeling hot and sweaty when others are comfortable, with weight loss and palpitations, is a characteristic pattern of hyperthyroidism.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Graves Disease', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_heat_intolerance', 'Hyperthyroidism (Graves disease, toxic nodules, thyroiditis)', 0),
    ('sym_heat_intolerance', 'Menopause', 1),
    ('sym_heat_intolerance', 'Fever and infection', 2),
    ('sym_heat_intolerance', 'Stimulant medicines or caffeine', 3),
    ('sym_heat_intolerance', 'Anxiety', 4)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_heat_intolerance');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_heat_intolerance', 'Very high fever with confusion, agitation or rapid heartbeat (possible thyroid storm)', 0),
    ('sym_heat_intolerance', 'Chest pain or fainting', 1)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_heat_intolerance');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_heat_intolerance', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_heat_intolerance', 'StatPearls - Graves Disease', 'Graves Disease. [Updated 2023 Jun 20]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK448195/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_heat_intolerance');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_tremor', 'Shaky hands (tremor)', 'Tremor', 'Rhythmic, involuntary shaking, most often of the hands. A fine, fast tremor seen with arms outstretched is typical of hyperthyroidism, anxiety and stimulants; a slower tremor at rest suggests Parkinson disease.', 'sys_nervous', false, array['neurologic', 'thyroid']::text[], 4, 'A fine tremor of outstretched hands supports hyperthyroidism when combined with other features, but tremor alone is common and nonspecific.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Graves Disease', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_tremor', 'Hyperthyroidism', 0),
    ('sym_tremor', 'Anxiety and caffeine', 1),
    ('sym_tremor', 'Essential tremor', 2),
    ('sym_tremor', 'Parkinson disease', 3),
    ('sym_tremor', 'Medicines such as salbutamol, lithium or valproate', 4),
    ('sym_tremor', 'Alcohol withdrawal', 5),
    ('sym_tremor', 'Low blood sugar', 6)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_tremor');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_tremor', 'Tremor with fever, confusion or a racing heart', 0),
    ('sym_tremor', 'Sudden tremor with weakness or slurred speech', 1)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_tremor');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_tremor', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_tremor', 'StatPearls - Graves Disease', 'Graves Disease. [Updated 2023 Jun 20]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK448195/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_tremor');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_goiter', 'Swelling at the front of the neck (goiter)', 'Goiter', 'Enlargement of the thyroid gland, seen or felt as a swelling at the front of the neck that moves up on swallowing. It may be diffuse (Graves disease, iodine deficiency, thyroiditis) or nodular, and thyroid function can be high, normal or low.', 'sys_endo', false, array['thyroid', 'neck', 'examination sign']::text[], 6, 'A diffuse, smooth goiter in a person with hyperthyroid symptoms suggests Graves disease; goiter also occurs with iodine deficiency and thyroid nodules.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Graves Disease', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_goiter', 'Graves disease', 0),
    ('sym_goiter', 'Iodine deficiency', 1),
    ('sym_goiter', 'Hashimoto thyroiditis', 2),
    ('sym_goiter', 'Multinodular goiter or thyroid nodules', 3),
    ('sym_goiter', 'Thyroid cancer (uncommon)', 4)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_goiter');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_goiter', 'Rapid growth, hard fixed lump or hoarse voice', 0),
    ('sym_goiter', 'Difficulty breathing or swallowing', 1),
    ('sym_goiter', 'Swollen lymph nodes in the neck', 2)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_goiter');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_goiter', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_goiter', 'StatPearls - Graves Disease', 'Graves Disease. [Updated 2023 Jun 20]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK448195/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_goiter');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_proptosis', 'Bulging or staring eyes (proptosis)', 'Proptosis (exophthalmos)', 'Forward displacement of one or both eyeballs, often with eyelid retraction, a staring look, gritty or watery eyes and sometimes double vision. Graves orbitopathy is the most common cause in adults; one-sided or rapidly progressive proptosis needs urgent assessment for orbital infection or tumor.', 'sys_endo', false, array['eye', 'thyroid', 'Graves']::text[], 8, 'Bulging eyes with lid retraction in a person with hyperthyroidism is highly specific for Graves disease (Graves orbitopathy).', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Graves Disease', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_proptosis', 'Graves orbitopathy', 0),
    ('sym_proptosis', 'Orbital cellulitis', 1),
    ('sym_proptosis', 'Orbital tumors', 2),
    ('sym_proptosis', 'Carotid-cavernous fistula', 3)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_proptosis');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_proptosis', 'Reduced or blurred vision or faded colors (possible optic nerve compression)', 0),
    ('sym_proptosis', 'Double vision', 1),
    ('sym_proptosis', 'Painful, red, swollen eye with fever', 2),
    ('sym_proptosis', 'Eyes that cannot close fully', 3)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_proptosis');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_proptosis', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_proptosis', 'StatPearls - Graves Disease', 'Graves Disease. [Updated 2023 Jun 20]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK448195/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_proptosis');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_podagra', 'Sudden hot, red, swollen big-toe joint (podagra)', 'Podagra', 'Acute inflammation of the joint at the base of the big toe (first metatarsophalangeal joint), with severe pain, swelling, redness and warmth that peak within 24 hours, often starting at night. It is the most typical first presentation of gout; septic arthritis must be considered if there is fever or the person is unwell.', 'sys_musculo', false, array['gout', 'joint', 'acute arthritis']::text[], 9, 'An acute, exquisitely painful, red and swollen first toe joint reaching peak within a day is the classic presentation of a gout flare.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Gout', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_podagra', 'Gout (monosodium urate crystals)', 0),
    ('sym_podagra', 'Septic arthritis', 1),
    ('sym_podagra', 'Pseudogout (calcium pyrophosphate)', 2),
    ('sym_podagra', 'Cellulitis', 3),
    ('sym_podagra', 'Trauma or fracture', 4)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_podagra');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_podagra', 'Fever, chills or feeling very unwell (possible septic arthritis)', 0),
    ('sym_podagra', 'Spreading redness up the foot or leg', 1),
    ('sym_podagra', 'Inability to bear weight after injury', 2)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_podagra');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_podagra', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_podagra', 'StatPearls - Gout', 'Gout. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK546606/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_podagra');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_tophi', 'Chalky lumps under the skin near joints or ears (tophi)', 'Tophi', 'Firm, painless, whitish or yellowish lumps formed by deposits of urate crystals, typically over the toes, fingers, elbows, Achilles tendon or ear rims. They appear after years of high uric acid and can discharge chalky material or damage joints.', 'sys_musculo', false, array['gout', 'chronic', 'examination sign']::text[], 8, 'Tophi indicate long-standing, poorly controlled gout and are an indication for urate-lowering therapy.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Gout; 2020 ACR Guideline for the Management of Gout', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_tophi', 'Chronic tophaceous gout', 0)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_tophi');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_tophi', 'Red, hot, discharging lump with fever (infection)', 0),
    ('sym_tophi', 'Rapidly enlarging lump', 1)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_tophi');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_tophi', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_tophi', 'StatPearls - Gout', 'Gout. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK546606/', false, 1),
    ('sym_tophi', '2020 ACR Guideline for the Management of Gout', 'FitzGerald JD, Dalbeth N, Mikuls T, et al. 2020 American College of Rheumatology Guideline for the Management of Gout. Arthritis Care Res (Hoboken). 2020;72(6):744-760.', 'https://pubmed.ncbi.nlm.nih.gov/32391934/', false, 2)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_tophi');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_burrows', 'Thin wavy lines between fingers or on wrists (burrows)', 'Scabies burrows', 'Short, thread-like, grey or skin-colored wavy lines a few millimetres long, made by the scabies mite tunneling in the top layer of skin. They are found mainly in the finger webs, wrists, elbows, belt line, genitals and, in infants, palms and soles, with intense itching that is worse at night.', 'sys_integ', false, array['scabies', 'skin', 'itch']::text[], 9, 'Burrows in the finger webs and wrists, with night-time itch in several household members, are almost diagnostic of scabies.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Scabies; WHO Fact Sheet - Scabies', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_burrows', 'Scabies (Sarcoptes scabiei)', 0)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_burrows');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_burrows', 'Painful, crusted or pus-filled sores (secondary bacterial infection)', 0),
    ('sym_burrows', 'Thick, crusted scaly skin in an older or immunocompromised person (crusted scabies)', 1),
    ('sym_burrows', 'Puffy face or dark urine weeks after infected sores (possible post-streptococcal glomerulonephritis)', 2)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_burrows');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_burrows', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_burrows', 'StatPearls - Scabies', 'Scabies. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK544306/', false, 1),
    ('sym_burrows', 'WHO Fact Sheet - Scabies', 'World Health Organization. Scabies. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/scabies', false, 2)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_burrows');

-- ===================================================== new medicines
insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_vancomycin', 'Vancomycin', 'Vancomycin', 'Vancocin', 'Glycopeptide antibiotic', 'Prescription', 'Vancomycin binds the D-alanyl-D-alanine ends of cell-wall precursors and blocks peptidoglycan synthesis in gram-positive bacteria. Given intravenously it treats serious infections due to MRSA and resistant pneumococci, and in suspected bacterial meningitis it is added to a third-generation cephalosporin until susceptibilities are known. Oral vancomycin is not absorbed and is used only for Clostridioides difficile colitis.', 'Adults, IV: commonly 15-20 mg/kg every 8-12 hours, with higher exposure targeted in meningitis; doses are individualised by therapeutic drug monitoring (AUC- or trough-guided) and kidney function. Infuse over at least 60 minutes. Oral (C. difficile): 125 mg four times daily for 10 days. Refer to current product labeling and local protocols.', 'Adults, IV: commonly 15-20 mg/kg every 8-12 hours, with higher exposure targeted in meningitis; doses are individualised by therapeutic drug monitoring (AUC- or trough-guided) and kidney function. Infuse over at least 60 minutes. Oral (C. difficile): 125 mg four times daily for 10 days. Refer to current product labeling and local protocols.', 'Store unreconstituted vials at 20-25 C; follow labeling for reconstituted solution stability.', 'Store unreconstituted vials at 20-25 C; follow labeling for reconstituted solution stability.', null, 'vancomycin', 'StatPearls: Vancomycin; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_vancomycin', 'brand_intl', 'Vancocin', 0),
    ('med_vancomycin', 'indication', 'Empiric therapy of bacterial meningitis (with ceftriaxone) until susceptibilities are known', 0),
    ('med_vancomycin', 'indication', 'Serious MRSA infections: bacteremia, endocarditis, pneumonia, osteomyelitis', 1),
    ('med_vancomycin', 'indication', 'Clostridioides difficile infection (oral route only)', 2),
    ('med_vancomycin', 'adverse', 'Nephrotoxicity, especially with high troughs or other nephrotoxins', 0),
    ('med_vancomycin', 'adverse', 'Vancomycin infusion reaction (flushing and itching of the upper body with rapid infusion)', 1),
    ('med_vancomycin', 'adverse', 'Ototoxicity (rare)', 2),
    ('med_vancomycin', 'adverse', 'Neutropenia and thrombocytopenia with prolonged use', 3),
    ('med_vancomycin', 'adverse', 'Phlebitis at the infusion site', 4),
    ('med_vancomycin', 'contraindication', 'Hypersensitivity to vancomycin', 0),
    ('med_vancomycin', 'interaction', 'Aminoglycosides, amphotericin B, cisplatin and loop diuretics: additive kidney or ear toxicity.', 0),
    ('med_vancomycin', 'interaction', 'Piperacillin-tazobactam: higher rates of acute kidney injury reported with the combination; monitor kidney function.', 1),
    ('med_vancomycin', 'interaction', 'NSAIDs and IV contrast: increased nephrotoxicity risk.', 2)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_vancomycin');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_vancomycin', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_vancomycin', 'StatPearls - Vancomycin', 'Vancomycin. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK459263/', false, 1)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_vancomycin');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_dexamethasone', 'Dexamethasone', 'Dexamethasone', 'Decadron', 'Corticosteroid (long-acting glucocorticoid)', 'Prescription', 'Dexamethasone is a potent, long-acting glucocorticoid with almost no mineralocorticoid effect. It suppresses inflammatory gene transcription and cytokine release. In bacterial meningitis, given just before or with the first antibiotic dose, it reduces inflammation-driven brain injury, hearing loss and death, with the clearest benefit in pneumococcal meningitis.', 'Bacterial meningitis (adults and children): 0.15 mg/kg IV every 6 hours for 2-4 days, first dose 10-20 minutes before or with the first antibiotic dose; stop if meningitis is not bacterial or the organism is not one for which benefit is shown (per local guidance). Other indications use different doses. Refer to current product labeling.', 'Bacterial meningitis (adults and children): 0.15 mg/kg IV every 6 hours for 2-4 days, first dose 10-20 minutes before or with the first antibiotic dose; stop if meningitis is not bacterial or the organism is not one for which benefit is shown (per local guidance). Other indications use different doses. Refer to current product labeling.', 'Store at 20-25 C, protected from light.', 'Store at 20-25 C, protected from light.', null, 'dexamethasone', 'StatPearls: Dexamethasone; WHO Meningitis fact sheet; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_dexamethasone', 'brand_intl', 'Decadron', 0),
    ('med_dexamethasone', 'indication', 'Adjunct in bacterial meningitis (given with the first antibiotic dose)', 0),
    ('med_dexamethasone', 'indication', 'Cerebral edema from tumors', 1),
    ('med_dexamethasone', 'indication', 'Severe asthma, croup and allergic reactions', 2),
    ('med_dexamethasone', 'indication', 'Severe COVID-19 needing oxygen', 3),
    ('med_dexamethasone', 'indication', 'Antenatal lung maturation in preterm labor', 4),
    ('med_dexamethasone', 'indication', 'Prevention of chemotherapy-induced nausea', 5),
    ('med_dexamethasone', 'adverse', 'Hyperglycemia', 0),
    ('med_dexamethasone', 'adverse', 'Insomnia, mood change and agitation', 1),
    ('med_dexamethasone', 'adverse', 'Increased infection risk and masking of fever', 2),
    ('med_dexamethasone', 'adverse', 'Gastrointestinal bleeding (especially with NSAIDs)', 3),
    ('med_dexamethasone', 'adverse', 'Adrenal suppression and osteoporosis with prolonged use', 4),
    ('med_dexamethasone', 'contraindication', 'Systemic fungal infection', 0),
    ('med_dexamethasone', 'contraindication', 'Hypersensitivity to dexamethasone', 1),
    ('med_dexamethasone', 'contraindication', 'Live vaccines during immunosuppressive doses', 2),
    ('med_dexamethasone', 'interaction', 'NSAIDs and aspirin: increased peptic ulcer and bleeding risk.', 0),
    ('med_dexamethasone', 'interaction', 'Rifampicin, phenytoin and carbamazepine: induce CYP3A4 and lower dexamethasone levels.', 1),
    ('med_dexamethasone', 'interaction', 'Insulin and oral antidiabetic drugs: corticosteroid-induced hyperglycemia may need higher doses.', 2),
    ('med_dexamethasone', 'interaction', 'Warfarin: altered INR; monitor.', 3)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_dexamethasone');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_dexamethasone', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_dexamethasone', 'StatPearls - Dexamethasone', 'Dexamethasone. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK482130/', false, 1),
    ('med_dexamethasone', 'WHO Fact Sheet - Meningitis', 'World Health Organization. Meningitis. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/meningitis', false, 2)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_dexamethasone');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_methimazole', 'Methimazole', 'Methimazole (thiamazole)', 'Tapazole', 'Thionamide antithyroid drug', 'Prescription', 'Methimazole inhibits thyroid peroxidase, blocking the iodination of thyroglobulin and the synthesis of T4 and T3. It does not stop release of hormone already stored, so improvement takes several weeks. It is the preferred antithyroid drug for Graves disease except in the first trimester of pregnancy and in thyroid storm, where propylthiouracil is used.', 'Adults, hyperthyroidism: initial dose by severity, about 5 mg three times daily for mild, 10 mg three times daily for moderate and 20 mg three times daily for severe disease (once-daily dosing is common at lower doses); after 4-6 weeks reduce to a maintenance dose of about 5-10 mg daily (range 5-30 mg). Usual course for Graves disease 12-18 months. Children: 0.4 mg/kg/day divided every 8 hours (maximum 30 mg/day). Refer to current product labeling.', 'Adults, hyperthyroidism: initial dose by severity, about 5 mg three times daily for mild, 10 mg three times daily for moderate and 20 mg three times daily for severe disease (once-daily dosing is common at lower doses); after 4-6 weeks reduce to a maintenance dose of about 5-10 mg daily (range 5-30 mg). Usual course for Graves disease 12-18 months. Children: 0.4 mg/kg/day divided every 8 hours (maximum 30 mg/day). Refer to current product labeling.', 'Store at 20-25 C, protected from light.', 'Store at 20-25 C, protected from light.', null, 'thiamazole', 'StatPearls: Methimazole; FP Notebook: Methimazole; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_methimazole', 'brand_intl', 'Tapazole', 0),
    ('med_methimazole', 'indication', 'Graves disease and other causes of hyperthyroidism', 0),
    ('med_methimazole', 'indication', 'Preparation for radioactive iodine or thyroidectomy', 1),
    ('med_methimazole', 'indication', 'Hyperthyroidism in the second and third trimesters of pregnancy', 2),
    ('med_methimazole', 'adverse', 'Agranulocytosis (about 0.2%; presents with fever and sore throat)', 0),
    ('med_methimazole', 'adverse', 'Rash, itching and joint pain', 1),
    ('med_methimazole', 'adverse', 'Cholestatic jaundice and hepatitis', 2),
    ('med_methimazole', 'adverse', 'Vasculitis and lupus-like syndrome (rare)', 3),
    ('med_methimazole', 'adverse', 'Congenital malformations with first-trimester exposure', 4),
    ('med_methimazole', 'contraindication', 'Hypersensitivity to methimazole', 0),
    ('med_methimazole', 'contraindication', 'First trimester of pregnancy (use propylthiouracil instead)', 1),
    ('med_methimazole', 'contraindication', 'Previous agranulocytosis on any thionamide', 2),
    ('med_methimazole', 'interaction', 'Warfarin: anticoagulant effect changes as thyroid status normalises; monitor INR.', 0),
    ('med_methimazole', 'interaction', 'Beta-blockers, digoxin and theophylline: doses may need reduction as the patient becomes euthyroid.', 1)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_methimazole');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_methimazole', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_methimazole', 'StatPearls - Methimazole', 'Methimazole. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK545223/', false, 1),
    ('med_methimazole', 'FP Notebook - Methimazole', 'Moses S. Methimazole. Family Practice Notebook.', 'https://fpnotebook.com/Endo/Pharm/Mthmzl.htm', false, 2)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_methimazole');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_propranolol', 'Propranolol', 'Propranolol', 'Inderal', 'Non-selective beta-adrenergic blocker', 'Prescription', 'Propranolol blocks beta-1 and beta-2 adrenergic receptors, slowing heart rate and reducing tremor, anxiety and sweating driven by excess thyroid hormone; at higher doses it also modestly reduces conversion of T4 to T3. It controls symptoms of hyperthyroidism while antithyroid treatment takes effect, and is used for hypertension, angina, migraine prevention and essential tremor.', 'Hyperthyroidism symptoms (adults): 10-40 mg orally three to four times daily, adjusted to heart rate and symptoms. Other indications use different doses. Do not stop suddenly after regular use; taper. Refer to current product labeling.', 'Hyperthyroidism symptoms (adults): 10-40 mg orally three to four times daily, adjusted to heart rate and symptoms. Other indications use different doses. Do not stop suddenly after regular use; taper. Refer to current product labeling.', 'Store at 20-25 C, protected from light and moisture.', 'Store at 20-25 C, protected from light and moisture.', 'Abrupt discontinuation can worsen angina and precipitate myocardial infarction; taper over 1-2 weeks.', 'propranolol', 'StatPearls: Propranolol; StatPearls: Graves Disease; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_propranolol', 'brand_intl', 'Inderal', 0),
    ('med_propranolol', 'indication', 'Symptom control in hyperthyroidism and thyroid storm', 0),
    ('med_propranolol', 'indication', 'Hypertension and angina', 1),
    ('med_propranolol', 'indication', 'Migraine prevention', 2),
    ('med_propranolol', 'indication', 'Essential tremor', 3),
    ('med_propranolol', 'indication', 'Prevention of variceal bleeding in portal hypertension', 4),
    ('med_propranolol', 'adverse', 'Bradycardia and hypotension', 0),
    ('med_propranolol', 'adverse', 'Fatigue, cold extremities and vivid dreams', 1),
    ('med_propranolol', 'adverse', 'Bronchospasm in asthma', 2),
    ('med_propranolol', 'adverse', 'Masking of hypoglycemia symptoms', 3),
    ('med_propranolol', 'adverse', 'Erectile dysfunction', 4),
    ('med_propranolol', 'contraindication', 'Asthma or severe bronchospasm', 0),
    ('med_propranolol', 'contraindication', 'Sinus bradycardia or second- or third-degree heart block', 1),
    ('med_propranolol', 'contraindication', 'Cardiogenic shock or decompensated heart failure', 2),
    ('med_propranolol', 'interaction', 'Verapamil and diltiazem: risk of severe bradycardia and heart block.', 0),
    ('med_propranolol', 'interaction', 'Salbutamol and other beta-agonists: effects antagonised.', 1),
    ('med_propranolol', 'interaction', 'Insulin and sulfonylureas: hypoglycemia warning signs masked.', 2),
    ('med_propranolol', 'interaction', 'Clonidine: rebound hypertension if clonidine is stopped while on propranolol.', 3)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_propranolol');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_propranolol', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_propranolol', 'StatPearls - Propranolol', 'Propranolol. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK557801/', false, 1),
    ('med_propranolol', 'StatPearls - Graves Disease', 'Graves Disease. [Updated 2023 Jun 20]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK448195/', false, 2)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_propranolol');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_colchicine', 'Colchicine', 'Colchicine', 'Colcrys', 'Anti-inflammatory (microtubule inhibitor)', 'Prescription', 'Colchicine binds tubulin and disrupts microtubules in neutrophils, reducing their migration and inflammasome activation in response to urate crystals. It treats gout flares best when started within 24-36 hours and prevents flares when urate-lowering therapy is started. It has a narrow therapeutic window, and overdose can be fatal.', 'Gout flare (adults): 1.2 mg at the first sign, then 0.6 mg one hour later (maximum 1.8 mg over 1 hour); low-dose regimens are as effective as high-dose with fewer side effects. Flare prophylaxis: 0.6 mg once or twice daily for at least 3-6 months after starting urate-lowering therapy. Reduce the dose in kidney or liver impairment and with interacting drugs. Refer to current product labeling.', 'Gout flare (adults): 1.2 mg at the first sign, then 0.6 mg one hour later (maximum 1.8 mg over 1 hour); low-dose regimens are as effective as high-dose with fewer side effects. Flare prophylaxis: 0.6 mg once or twice daily for at least 3-6 months after starting urate-lowering therapy. Reduce the dose in kidney or liver impairment and with interacting drugs. Refer to current product labeling.', 'Store at 20-25 C, protected from light.', 'Store at 20-25 C, protected from light.', 'Label warning: fatal overdoses have been reported; there is no antidote and dialysis does not remove colchicine. Keep out of the reach of children.', 'colchicine', 'StatPearls: Colchicine; 2020 ACR Gout Guideline; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_colchicine', 'brand_intl', 'Colcrys', 0),
    ('med_colchicine', 'indication', 'Treatment of gout flares', 0),
    ('med_colchicine', 'indication', 'Prevention of flares when starting urate-lowering therapy', 1),
    ('med_colchicine', 'indication', 'Familial Mediterranean fever', 2),
    ('med_colchicine', 'indication', 'Pericarditis (adjunct)', 3),
    ('med_colchicine', 'adverse', 'Diarrhea, nausea and abdominal cramps (most common)', 0),
    ('med_colchicine', 'adverse', 'Myelosuppression (neutropenia, thrombocytopenia)', 1),
    ('med_colchicine', 'adverse', 'Neuromyopathy and rhabdomyolysis, especially with statins or kidney impairment', 2),
    ('med_colchicine', 'contraindication', 'Use with strong CYP3A4 or P-glycoprotein inhibitors in people with kidney or liver impairment', 0),
    ('med_colchicine', 'contraindication', 'Severe kidney or liver impairment (avoid or use with great caution)', 1),
    ('med_colchicine', 'contraindication', 'Hypersensitivity to colchicine', 2),
    ('med_colchicine', 'interaction', 'Clarithromycin, ketoconazole, ritonavir and other strong CYP3A4 inhibitors: toxic colchicine levels; avoid or reduce dose.', 0),
    ('med_colchicine', 'interaction', 'Cyclosporine and verapamil (P-gp inhibitors): increased toxicity.', 1),
    ('med_colchicine', 'interaction', 'Statins, fibrates and digoxin: increased risk of myopathy and rhabdomyolysis.', 2),
    ('med_colchicine', 'interaction', 'Grapefruit juice: raises colchicine levels.', 3)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_colchicine');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_colchicine', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_colchicine', 'StatPearls - Colchicine', 'Colchicine. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK431102/', false, 1),
    ('med_colchicine', '2020 ACR Guideline for the Management of Gout', 'FitzGerald JD, Dalbeth N, Mikuls T, et al. 2020 American College of Rheumatology Guideline for the Management of Gout. Arthritis Care Res (Hoboken). 2020;72(6):744-760.', 'https://pubmed.ncbi.nlm.nih.gov/32391934/', false, 2)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_colchicine');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_allopurinol', 'Allopurinol', 'Allopurinol', 'Zyloprim', 'Xanthine oxidase inhibitor (urate-lowering)', 'Prescription', 'Allopurinol and its active metabolite oxypurinol inhibit xanthine oxidase, reducing production of uric acid. Lowering serum urate below 6 mg/dL dissolves urate crystals over time, preventing flares, tophi and joint damage. It is the preferred first-line urate-lowering drug in gout, including in chronic kidney disease, started at a low dose and increased gradually.', 'Gout (adults): start at 100 mg daily or less (lower, e.g., 50 mg, in moderate-to-severe CKD) and increase gradually, about every 2-5 weeks, until serum urate is below 6 mg/dL; maximum 800 mg daily. Give flare prophylaxis (e.g., colchicine) for at least 3-6 months when starting. Do not stop during a flare if already taking it. Refer to current product labeling.', 'Gout (adults): start at 100 mg daily or less (lower, e.g., 50 mg, in moderate-to-severe CKD) and increase gradually, about every 2-5 weeks, until serum urate is below 6 mg/dL; maximum 800 mg daily. Give flare prophylaxis (e.g., colchicine) for at least 3-6 months when starting. Do not stop during a flare if already taking it. Refer to current product labeling.', 'Store at 20-25 C, in a dry place.', 'Store at 20-25 C, in a dry place.', null, 'allopurinol', 'Medical Genetics Summaries: Allopurinol and HLA-B*58:01; 2020 ACR Gout Guideline; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_allopurinol', 'brand_intl', 'Zyloprim', 0),
    ('med_allopurinol', 'indication', 'Long-term urate lowering in gout (frequent flares, tophi, joint damage)', 0),
    ('med_allopurinol', 'indication', 'Prevention of tumor lysis syndrome', 1),
    ('med_allopurinol', 'indication', 'Recurrent uric acid or calcium oxalate kidney stones', 2),
    ('med_allopurinol', 'adverse', 'Gout flares when starting treatment (use prophylaxis)', 0),
    ('med_allopurinol', 'adverse', 'Rash', 1),
    ('med_allopurinol', 'adverse', 'Severe cutaneous reactions (SJS/TEN, DRESS), strongly linked to HLA-B*58:01', 2),
    ('med_allopurinol', 'adverse', 'Liver enzyme elevation', 3),
    ('med_allopurinol', 'adverse', 'Gastrointestinal upset', 4),
    ('med_allopurinol', 'contraindication', 'Previous severe allergic or skin reaction to allopurinol', 0),
    ('med_allopurinol', 'contraindication', 'HLA-B*58:01 carriers (CPIC); testing advised before starting in people of Southeast Asian or Han Chinese, Korean or Thai descent and African American patients (ACR 2020)', 1),
    ('med_allopurinol', 'interaction', 'Azathioprine and mercaptopurine: allopurinol blocks their breakdown, causing severe bone-marrow toxicity; avoid or reduce dose substantially.', 0),
    ('med_allopurinol', 'interaction', 'Amoxicillin and ampicillin: higher rate of skin rash.', 1),
    ('med_allopurinol', 'interaction', 'Thiazide diuretics and impaired kidney function: higher risk of hypersensitivity reactions.', 2),
    ('med_allopurinol', 'interaction', 'Warfarin: may increase INR; monitor.', 3)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_allopurinol', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_allopurinol', 'Medical Genetics Summaries - Allopurinol Therapy and HLA-B*58:01 Genotype', 'Dean L, Kane M. Allopurinol Therapy and HLA-B*58:01 Genotype. In: Pratt VM, et al., eds. Medical Genetics Summaries. Bethesda (MD): National Center for Biotechnology Information; updated 2020.', 'https://www.ncbi.nlm.nih.gov/books/NBK127547/', false, 1),
    ('med_allopurinol', '2020 ACR Guideline for the Management of Gout', 'FitzGerald JD, Dalbeth N, Mikuls T, et al. 2020 American College of Rheumatology Guideline for the Management of Gout. Arthritis Care Res (Hoboken). 2020;72(6):744-760.', 'https://pubmed.ncbi.nlm.nih.gov/32391934/', false, 2)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_allopurinol');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_permethrin', 'Permethrin 5% cream', 'Permethrin', 'Elimite', 'Topical pyrethroid scabicide', 'Prescription', 'Permethrin is a synthetic pyrethroid that blocks sodium channels in the nerve membranes of mites and lice, causing paralysis and death. Very little is absorbed through human skin. Permethrin 5% cream is a first-line treatment for scabies; because it may not kill all eggs, a second application about a week later is usually advised, and all close contacts are treated at the same time.', 'Scabies: apply a thin layer of 5% cream to cool, dry skin over the whole body from the neck down (including under the nails, between fingers and toes and the genitals; include the scalp, face and neck in infants and older adults), wash off after 8-14 hours, and repeat after 7 days. Approved from 2 months of age. Refer to current product labeling.', 'Scabies: apply a thin layer of 5% cream to cool, dry skin over the whole body from the neck down (including under the nails, between fingers and toes and the genitals; include the scalp, face and neck in infants and older adults), wash off after 8-14 hours, and repeat after 7 days. Approved from 2 months of age. Refer to current product labeling.', 'Store at 20-25 C.', 'Store at 20-25 C.', null, 'permethrin', 'StatPearls: Permethrin; CDC Clinical care of scabies; WHO Scabies fact sheet.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_permethrin', 'brand_intl', 'Elimite', 0),
    ('med_permethrin', 'indication', 'Scabies (first-line topical treatment)', 0),
    ('med_permethrin', 'indication', 'Crusted scabies (with oral ivermectin)', 1),
    ('med_permethrin', 'indication', 'Head lice (1% lotion)', 2),
    ('med_permethrin', 'adverse', 'Temporary burning, stinging or worsening itch after application', 0),
    ('med_permethrin', 'adverse', 'Rash or skin irritation', 1),
    ('med_permethrin', 'adverse', 'Allergic contact dermatitis (uncommon)', 2),
    ('med_permethrin', 'contraindication', 'Hypersensitivity to permethrin, pyrethroids or chrysanthemums', 0),
    ('med_permethrin', 'contraindication', 'Infants under 2 months (not FDA-approved)', 1),
    ('med_permethrin', 'interaction', 'No clinically significant drug interactions are recognised with topical use.', 0)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_permethrin');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_permethrin', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_permethrin', 'StatPearls - Permethrin', 'Nanda J, Patel P. Permethrin. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.statpearls.com/ArticleLibrary/viewarticle/27033', false, 1),
    ('med_permethrin', 'CDC - Clinical Care of Scabies', 'Centers for Disease Control and Prevention. Clinical care of scabies (for health care providers).', 'https://www.cdc.gov/scabies/hcp/clinical-care/index.html', false, 2)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_permethrin');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_ivermectin', 'Ivermectin', 'Ivermectin', 'Stromectol', 'Oral antiparasitic (macrocyclic lactone)', 'Prescription', 'Ivermectin binds glutamate-gated chloride channels in invertebrate nerve and muscle cells, causing paralysis and death of the parasite. A single oral dose is effective against scabies mites, strongyloidiasis and onchocerciasis. It does not kill mite eggs, so scabies treatment is repeated after 7-14 days. WHO recommends two-dose ivermectin for mass drug administration where scabies prevalence is 10% or more.', 'Scabies (adults and children 15 kg or more): 200 micrograms/kg orally as a single dose with food, repeated after 7-14 days. Crusted scabies: multiple doses (e.g., days 1, 2 and 8, or more) combined with topical permethrin. Not for pregnant women or children under 15 kg. Refer to current product labeling.', 'Scabies (adults and children 15 kg or more): 200 micrograms/kg orally as a single dose with food, repeated after 7-14 days. Crusted scabies: multiple doses (e.g., days 1, 2 and 8, or more) combined with topical permethrin. Not for pregnant women or children under 15 kg. Refer to current product labeling.', 'Store below 30 C.', 'Store below 30 C.', null, 'ivermectin', 'WHO Scabies fact sheet; CDC Clinical care of scabies; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_ivermectin', 'brand_intl', 'Stromectol', 0),
    ('med_ivermectin', 'indication', 'Scabies, including crusted scabies (with topical therapy)', 0),
    ('med_ivermectin', 'indication', 'Mass drug administration for scabies in high-prevalence communities', 1),
    ('med_ivermectin', 'indication', 'Strongyloidiasis', 2),
    ('med_ivermectin', 'indication', 'Onchocerciasis and lymphatic filariasis (in combination)', 3),
    ('med_ivermectin', 'adverse', 'Itching or rash (often worse in the first days)', 0),
    ('med_ivermectin', 'adverse', 'Dizziness, nausea and diarrhea', 1),
    ('med_ivermectin', 'adverse', 'Inflammatory reactions when treating heavy filarial infections', 2),
    ('med_ivermectin', 'adverse', 'Risk of severe encephalopathy in people with heavy Loa loa infection', 3),
    ('med_ivermectin', 'contraindication', 'Pregnancy', 0),
    ('med_ivermectin', 'contraindication', 'Children weighing less than 15 kg', 1),
    ('med_ivermectin', 'contraindication', 'Hypersensitivity to ivermectin', 2),
    ('med_ivermectin', 'interaction', 'Warfarin: raised INR has been reported; monitor.', 0),
    ('med_ivermectin', 'interaction', 'Strong CYP3A4 or P-glycoprotein inhibitors may raise ivermectin levels.', 1)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_ivermectin');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_ivermectin', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_ivermectin', 'WHO Fact Sheet - Scabies', 'World Health Organization. Scabies. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/scabies', false, 1),
    ('med_ivermectin', 'CDC - Clinical Care of Scabies', 'Centers for Disease Control and Prevention. Clinical care of scabies (for health care providers).', 'https://www.cdc.gov/scabies/hcp/clinical-care/index.html', false, 2)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_ivermectin');

-- ===================================================== Post-Streptococcal Glomerulonephritis
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('post_strep_glomerulonephritis', 'Post-Streptococcal Glomerulonephritis', 'Acute post-streptococcal glomerulonephritis (APSGN)', 'Post-streptococcal glomerulonephritis is an immune-mediated inflammation of the kidney''s filtering units (glomeruli) that follows infection of the throat or skin with nephritogenic strains of group A Streptococcus. It is the most common cause of acute nephritic syndrome in children worldwide, mainly at ages 5-12, and is linked to crowding and to impetigo complicating scabies. Most children recover fully, but adults and those with severe disease can develop lasting kidney damage.', 'sys_renal', 'Moderate', 'SEE_DOCTOR_SOON', 'A child with puffy eyes or face, cola-colored urine or reduced urine 1-6 weeks after a sore throat or infected skin sores needs prompt medical review with blood pressure, urinalysis and kidney tests. Severe headache, seizures, vision changes, breathlessness or very little urine (possible hypertensive encephalopathy, pulmonary edema or kidney failure) need emergency care.', false, 'Nephritogenic streptococcal antigens deposit in the glomeruli or form circulating immune complexes. These activate complement, mainly through the alternative pathway, lowering serum C3. Neutrophils and monocytes infiltrate the glomerular capillaries, producing a diffuse proliferative (endocapillary) glomerulonephritis with subepithelial ''hump'' deposits on electron microscopy (a type III hypersensitivity reaction). The inflamed glomeruli filter less, causing salt and water retention, and leak red cells and some protein into the urine.', 'Reduced filtration with continued sodium reabsorption expands extracellular volume, causing periorbital and leg edema, hypertension and, in severe cases, pulmonary edema or hypertensive encephalopathy. Damaged glomerular capillaries allow red cells into the urine, giving cola- or tea-colored urine with dysmorphic red cells and red cell casts. Low C3 with normal C4, and raised antistreptolysin O or anti-DNase B (the latter especially after skin infection), reflect the post-infectious immune mechanism.', 'Monitor blood pressure, weight, urine output, creatinine and electrolytes during the acute phase. Recheck C3 at 6-8 weeks: persistently low C3 suggests another diagnosis (C3 glomerulopathy, lupus) and may need kidney biopsy. Follow urinalysis and blood pressure until hematuria and proteinuria resolve, and longer in adults, because a minority develop hypertension or chronic kidney disease years later.', 'StatPearls: Poststreptococcal Glomerulonephritis; Lecturio; WHO Scabies fact sheet; Nelson Textbook of Pediatrics, 21st ed.', 'Begins after a latent period of about 1-3 weeks after pharyngitis or 3-6 weeks after skin infection (impetigo). Onset is abrupt with edema, dark urine and hypertension. Diuresis usually starts within a week, C3 returns to normal within about 6-8 weeks, proteinuria usually clears within months, and microscopic hematuria can persist for 6 months to a year.', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('post_strep_glomerulonephritis', 0, 'Immune reaction to nephritogenic strains of group A Streptococcus (Streptococcus pyogenes)'),
    ('post_strep_glomerulonephritis', 1, 'Preceding streptococcal pharyngitis (sore throat)'),
    ('post_strep_glomerulonephritis', 2, 'Preceding streptococcal skin infection (impetigo), often complicating scabies'),
    ('post_strep_glomerulonephritis', 3, 'Immune-complex deposition and complement activation in the glomeruli')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('post_strep_glomerulonephritis', 0, 'Age 5-12 years (also adults over 60)'),
    ('post_strep_glomerulonephritis', 1, 'Male sex'),
    ('post_strep_glomerulonephritis', 2, 'Crowded living conditions and poor hygiene'),
    ('post_strep_glomerulonephritis', 3, 'Scabies and impetigo in the household or community'),
    ('post_strep_glomerulonephritis', 4, 'Untreated streptococcal throat or skin infection')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('post_strep_glomerulonephritis', 0, 'Urinalysis: hematuria with dysmorphic red cells and red cell casts, variable proteinuria'),
    ('post_strep_glomerulonephritis', 1, 'Serum creatinine, BUN and electrolytes (potassium)'),
    ('post_strep_glomerulonephritis', 2, 'Serum complement: low C3 (and CH50) with normal C4'),
    ('post_strep_glomerulonephritis', 3, 'Evidence of streptococcal infection: ASO titer (after pharyngitis), anti-DNase B (after skin infection), throat or skin culture'),
    ('post_strep_glomerulonephritis', 4, 'Blood pressure monitoring and daily weight'),
    ('post_strep_glomerulonephritis', 5, 'Chest X-ray if breathless (pulmonary edema)'),
    ('post_strep_glomerulonephritis', 6, 'Kidney biopsy only if atypical: low C3 beyond 8 weeks, rapidly rising creatinine or nephrotic-range proteinuria')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('post_strep_glomerulonephritis', 0, 'Supportive care: most patients recover spontaneously'),
    ('post_strep_glomerulonephritis', 1, 'Restrict salt and fluid intake while edema, hypertension or oliguria persist'),
    ('post_strep_glomerulonephritis', 2, 'Loop diuretics (e.g., furosemide) for edema and volume overload'),
    ('post_strep_glomerulonephritis', 3, 'Antihypertensives (e.g., calcium channel blockers) if blood pressure stays high despite diuretics; ACE inhibitors are used cautiously because of hyperkalemia during the acute phase'),
    ('post_strep_glomerulonephritis', 4, 'Antibiotics (penicillin, or erythromycin if allergic) if streptococcal infection is still present, and to protect close contacts during outbreaks'),
    ('post_strep_glomerulonephritis', 5, 'Treat scabies and impetigo in the household to stop further streptococcal skin infection'),
    ('post_strep_glomerulonephritis', 6, 'Dialysis for severe fluid overload, refractory hyperkalemia, uremia or rapidly worsening kidney function')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('post_strep_glomerulonephritis', 0, 'Follow the salt and fluid limits advised by the doctor until swelling and blood pressure settle'),
    ('post_strep_glomerulonephritis', 1, 'Weigh daily and keep a record of urine output if asked'),
    ('post_strep_glomerulonephritis', 2, 'Take blood pressure and water pills exactly as prescribed'),
    ('post_strep_glomerulonephritis', 3, 'Finish any antibiotic course and have sore throats and skin sores in the family treated'),
    ('post_strep_glomerulonephritis', 4, 'Avoid painkillers such as ibuprofen and mefenamic acid during the illness')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('post_strep_glomerulonephritis', 0, 'Severe headache, vomiting, blurred vision, confusion or seizures (possible hypertensive encephalopathy)'),
    ('post_strep_glomerulonephritis', 1, 'Shortness of breath or cough with frothy sputum (fluid in the lungs)'),
    ('post_strep_glomerulonephritis', 2, 'Very little or no urine for 12 hours or more'),
    ('post_strep_glomerulonephritis', 3, 'Rapidly increasing swelling of the face, legs or abdomen'),
    ('post_strep_glomerulonephritis', 4, 'Chest pain or an irregular heartbeat (possible high potassium)')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('post_strep_glomerulonephritis', 0, 'Prompt treatment of streptococcal sore throat and impetigo, control of scabies, handwashing and reduced household crowding.', 'primary'::public.prevention_tier),
    ('post_strep_glomerulonephritis', 1, 'Urine and blood pressure checks in children with recent streptococcal infection or in outbreak households, and penicillin for close contacts during community outbreaks.', 'secondary'::public.prevention_tier),
    ('post_strep_glomerulonephritis', 2, 'Careful fluid, blood pressure and electrolyte management, dialysis when needed, and long-term follow-up to detect hypertension or chronic kidney disease.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('post_strep_glomerulonephritis', 0, 'IgA nephropathy', 'Hematuria within 1-5 days of an upper respiratory infection (synpharyngitic), recurrent episodes, normal C3'),
    ('post_strep_glomerulonephritis', 1, 'C3 glomerulopathy', 'Low C3 and urine abnormalities persisting beyond 6-8 weeks'),
    ('post_strep_glomerulonephritis', 2, 'Lupus nephritis', 'Both C3 and C4 low, positive ANA and anti-dsDNA, multisystem features'),
    ('post_strep_glomerulonephritis', 3, 'IgA vasculitis (Henoch-Schonlein purpura)', 'Palpable purpura on legs, abdominal pain and arthritis; normal complement'),
    ('post_strep_glomerulonephritis', 4, 'Nephrotic syndrome (minimal change disease)', 'Heavy proteinuria and marked edema with little hematuria or hypertension')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('post_strep_glomerulonephritis', 'nephritic syndrome'),
    ('post_strep_glomerulonephritis', 'group A Streptococcus'),
    ('post_strep_glomerulonephritis', 'pediatrics'),
    ('post_strep_glomerulonephritis', 'low C3'),
    ('post_strep_glomerulonephritis', 'cola-colored urine')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('post_strep_glomerulonephritis', 'sym_periorbital_edema', 7::smallint, true, 1.4::numeric),
    ('post_strep_glomerulonephritis', 'sym_hematuria', 7::smallint, true, 1.5::numeric),
    ('post_strep_glomerulonephritis', 'sym_edema', 6::smallint, false, 1.0::numeric),
    ('post_strep_glomerulonephritis', 'sym_decreased_urine', 5::smallint, false, 1.1::numeric),
    ('post_strep_glomerulonephritis', 'sym_dark_urine', 5::smallint, false, 1.0::numeric),
    ('post_strep_glomerulonephritis', 'sym_headache', 4::smallint, false, 0.6::numeric),
    ('post_strep_glomerulonephritis', 'sym_sore_throat', 2::smallint, false, 0.6::numeric),
    ('post_strep_glomerulonephritis', 'sym_fatigue', 3::smallint, false, 0.4::numeric),
    ('post_strep_glomerulonephritis', 'sym_dyspnea', 2::smallint, false, 0.6::numeric),
    ('post_strep_glomerulonephritis', 'sym_nausea_vomiting', 2::smallint, false, 0.4::numeric),
    ('post_strep_glomerulonephritis', 'sym_seizures', 1::smallint, false, 0.6::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('post_strep_glomerulonephritis', 'med_furosemide', 0, 'safe'::public.condition_safety, 'Loop diuretic for edema and fluid overload, the mainstay of treating volume-driven hypertension in PSGN.'),
    ('post_strep_glomerulonephritis', 'med_amlodipine', 1, 'safe'::public.condition_safety, 'Calcium channel blocker for persistent hypertension once volume is being controlled.'),
    ('post_strep_glomerulonephritis', 'med_benzathine_penicillin', 2, 'safe'::public.condition_safety, 'Eradicates remaining group A strep and is used for close contacts during outbreaks; it does not alter the course of the nephritis itself.'),
    ('post_strep_glomerulonephritis', 'med_amoxicillin', 3, 'safe'::public.condition_safety, 'Oral alternative to treat an ongoing streptococcal throat infection.'),
    ('post_strep_glomerulonephritis', 'med_enalapril', 4, 'caution'::public.condition_safety, 'ACE inhibitors can raise potassium and creatinine during acute nephritis; used later for persistent proteinuria or hypertension.'),
    ('post_strep_glomerulonephritis', 'med_losartan', 5, 'caution'::public.condition_safety, 'Same hyperkalemia concern as ACE inhibitors during the acute phase.'),
    ('post_strep_glomerulonephritis', 'med_ibuprofen', 6, 'avoid'::public.condition_safety, 'NSAIDs reduce kidney blood flow and worsen salt and water retention in acute nephritis.'),
    ('post_strep_glomerulonephritis', 'med_mefenamic_acid', 7, 'avoid'::public.condition_safety, 'NSAID; nephrotoxic risk during acute glomerulonephritis.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'post_strep_glomerulonephritis');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_post_strep_glomerulonephritis_1', 'post_strep_glomerulonephritis', 0, 'Nelson Textbook of Pediatrics', 'Kliegman RM, St Geme JW, Blum NJ, Shah SS, Tasker RC, Wilson KM, eds. Nelson Textbook of Pediatrics. 21st ed. Philadelphia: Elsevier; 2020.', null, 'Pediatrics', true),
    ('ref_post_strep_glomerulonephritis_2', 'post_strep_glomerulonephritis', 1, 'StatPearls - Poststreptococcal Glomerulonephritis', 'Poststreptococcal Glomerulonephritis. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://statpearls.com/as/renal/22287', 'Nephrology / Pediatrics', false),
    ('ref_post_strep_glomerulonephritis_3', 'post_strep_glomerulonephritis', 2, 'Lecturio - Postinfectious (Poststreptococcal) Glomerulonephritis', 'Lecturio Medical Concept Library. Postinfectious glomerulonephritis.', 'https://lecturio.com/concepts/poststreptococcal-glomerulonephritis', 'Nephrology', false),
    ('ref_post_strep_glomerulonephritis_4', 'post_strep_glomerulonephritis', 3, 'WHO Fact Sheet - Scabies', 'World Health Organization. Scabies. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/scabies', 'Public Health', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'post_strep_glomerulonephritis');

-- ===================================================== Bacterial Meningitis
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('bacterial_meningitis', 'Bacterial Meningitis', 'Acute bacterial meningitis', 'Bacterial meningitis is infection and inflammation of the meninges and cerebrospinal fluid surrounding the brain and spinal cord. The main causes are Streptococcus pneumoniae, Neisseria meningitidis, Haemophilus influenzae type b and, in newborns, group B Streptococcus. It can kill within hours: about 1 in 6 patients die and 1 in 5 survivors have lasting complications such as hearing loss, seizures or cognitive impairment (WHO). Vaccines and immediate antibiotics are the key defences.', 'sys_nervous', 'Critical', 'EMERGENCY', 'Suspected bacterial meningitis is a medical emergency: fever with severe headache, stiff neck, confusion, seizures, a non-blanching rash, or, in infants, poor feeding, lethargy, high-pitched cry or bulging fontanelle, needs immediate hospital care. Antibiotics must not be delayed for tests.', true, 'Bacteria that colonise the nasopharynx invade the bloodstream and cross the blood-brain barrier, or spread directly from sinusitis, otitis media or skull defects. In the subarachnoid space, where host defences are limited, bacterial products trigger an intense cytokine-driven neutrophilic inflammation. This increases blood-brain barrier permeability, causing vasogenic and cytotoxic cerebral edema, raised intracranial pressure, reduced cerebral blood flow, vasculitis and thrombosis. Meningococcal septicemia adds endotoxin-driven shock and disseminated intravascular coagulation.', 'Meningeal inflammation produces headache, neck stiffness, photophobia and positive Kernig and Brudzinski signs; raised intracranial pressure and cortical involvement cause vomiting, confusion, seizures and coma. The full triad of fever, neck stiffness and altered mental status is present in fewer than half of patients. Cerebrospinal fluid shows a high neutrophil count, high protein and low glucose relative to blood. A rapidly spreading petechial or purpuric rash reflects meningococcal septicemia with coagulopathy.', 'Monitor neurological status, vital signs, fluid balance and sodium closely in hospital, and narrow antibiotics once cultures and sensitivities return. Arrange a formal hearing test before or soon after discharge (ideally within 4 weeks) and follow-up for seizures, developmental or cognitive problems, especially in children. Notify public health about meningococcal and Hib cases so close contacts receive chemoprophylaxis.', 'WHO Meningitis fact sheet; StatPearls: Bacterial Meningitis (2023); Harrison''s Principles of Internal Medicine, 21st ed.', 'Usually acute, developing over hours to 1-2 days, and sometimes fulminant within hours (meningococcal disease). It may follow a few days of upper respiratory symptoms, sinusitis or ear infection. Infants and older adults may present only with fever or hypothermia, irritability, poor feeding or confusion.', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('bacterial_meningitis', 0, 'Streptococcus pneumoniae (most common in most age groups)'),
    ('bacterial_meningitis', 1, 'Neisseria meningitidis (meningococcus), most common in adolescents and young adults'),
    ('bacterial_meningitis', 2, 'Group B Streptococcus (most common in infants under 2 months)'),
    ('bacterial_meningitis', 3, 'Haemophilus influenzae type b in unvaccinated children'),
    ('bacterial_meningitis', 4, 'Listeria monocytogenes in newborns, adults over 50 and immunocompromised people'),
    ('bacterial_meningitis', 5, 'Staphylococcus aureus and gram-negative bacilli after neurosurgery or head trauma')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'bacterial_meningitis');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('bacterial_meningitis', 0, 'Age under 5 or over 60'),
    ('bacterial_meningitis', 1, 'Lack of vaccination (pneumococcal, meningococcal, Hib)'),
    ('bacterial_meningitis', 2, 'Crowded living (dormitories, military barracks, mass gatherings)'),
    ('bacterial_meningitis', 3, 'Immunosuppression, HIV, splenectomy or sickle cell disease'),
    ('bacterial_meningitis', 4, 'Recent sinusitis, otitis media, skull fracture, CSF leak or cochlear implant'),
    ('bacterial_meningitis', 5, 'Close contact with a person with meningococcal disease')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'bacterial_meningitis');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('bacterial_meningitis', 0, 'Blood cultures immediately, before antibiotics when this causes no delay'),
    ('bacterial_meningitis', 1, 'Lumbar puncture with CSF opening pressure, cell count, glucose (with paired blood glucose), protein, Gram stain, culture and PCR'),
    ('bacterial_meningitis', 2, 'CT head before lumbar puncture only if there are signs of raised pressure or a mass (papilledema, focal deficit, new seizures, reduced consciousness, immunocompromise)'),
    ('bacterial_meningitis', 3, 'CBC, CRP or procalcitonin, electrolytes, kidney function and coagulation screen'),
    ('bacterial_meningitis', 4, 'Typical CSF in bacterial meningitis: neutrophilic pleocytosis, high protein, low CSF-to-blood glucose ratio')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'bacterial_meningitis');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('bacterial_meningitis', 0, 'Start empiric IV antibiotics immediately; do not wait for lumbar puncture or CT (each hour of delay raises mortality)'),
    ('bacterial_meningitis', 1, 'Adults and children beyond the newborn period: ceftriaxone plus vancomycin; add ampicillin for adults over 50 or immunocompromised patients (Listeria cover)'),
    ('bacterial_meningitis', 2, 'Neonates: ampicillin plus cefotaxime or an aminoglycoside, per local protocols'),
    ('bacterial_meningitis', 3, 'Dexamethasone given just before or with the first antibiotic dose in non-epidemic settings, continued if pneumococcal meningitis is confirmed'),
    ('bacterial_meningitis', 4, 'Supportive care: fluids, oxygen, treatment of shock, seizures and raised intracranial pressure, often in intensive care'),
    ('bacterial_meningitis', 5, 'Narrow antibiotics to the identified organism; usual duration 7-21 days depending on the bacterium'),
    ('bacterial_meningitis', 6, 'Droplet precautions for suspected meningococcal disease until 24 hours of effective antibiotics; chemoprophylaxis for close contacts')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'bacterial_meningitis');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('bacterial_meningitis', 0, 'Meningitis is treated in hospital; there is no home treatment'),
    ('bacterial_meningitis', 1, 'After discharge, attend hearing tests and follow-up visits, and report seizures, headaches or learning problems'),
    ('bacterial_meningitis', 2, 'Close contacts of a meningococcal case should take the preventive antibiotic exactly as advised'),
    ('bacterial_meningitis', 3, 'Keep everyone in the household up to date with pneumococcal, meningococcal and Hib vaccines')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'bacterial_meningitis');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('bacterial_meningitis', 0, 'Fever with severe headache and stiff neck'),
    ('bacterial_meningitis', 1, 'Purple or red rash that does not fade when pressed with a glass'),
    ('bacterial_meningitis', 2, 'Confusion, drowsiness or difficulty waking'),
    ('bacterial_meningitis', 3, 'Seizures'),
    ('bacterial_meningitis', 4, 'Cold hands and feet, mottled skin or rapid breathing (sepsis)'),
    ('bacterial_meningitis', 5, 'Infant with bulging soft spot, high-pitched cry, floppiness or refusal to feed')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'bacterial_meningitis');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('bacterial_meningitis', 0, 'Vaccination against pneumococcus, meningococcus and Hib; intrapartum antibiotics for mothers colonised with group B Streptococcus.', 'primary'::public.prevention_tier),
    ('bacterial_meningitis', 1, 'Antibiotic chemoprophylaxis (rifampicin, ciprofloxacin or ceftriaxone) for close contacts of meningococcal and Hib cases, and early recognition and treatment of suspected cases.', 'secondary'::public.prevention_tier),
    ('bacterial_meningitis', 2, 'Immediate antibiotics with dexamethasone, intensive care, hearing assessment and rehabilitation to reduce death and long-term disability.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'bacterial_meningitis');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('bacterial_meningitis', 0, 'Viral meningitis', 'Milder illness; CSF lymphocytic with normal glucose and modestly raised protein'),
    ('bacterial_meningitis', 1, 'Herpes simplex encephalitis', 'Behavioral change, focal deficits or seizures; temporal lobe changes on MRI; CSF HSV PCR positive'),
    ('bacterial_meningitis', 2, 'Tuberculous meningitis', 'Subacute onset over weeks, cranial nerve palsies; CSF lymphocytic with very high protein and low glucose'),
    ('bacterial_meningitis', 3, 'Subarachnoid hemorrhage', 'Sudden thunderclap headache; blood on CT or xanthochromia in CSF'),
    ('bacterial_meningitis', 4, 'Cerebral malaria', 'Travel to or residence in an endemic area; positive blood smear or RDT'),
    ('bacterial_meningitis', 5, 'Dengue with neurological involvement', 'Thrombocytopenia, hemoconcentration and positive dengue NS1 or IgM')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'bacterial_meningitis');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('bacterial_meningitis', 'neurological emergency'),
    ('bacterial_meningitis', 'meningococcus'),
    ('bacterial_meningitis', 'pneumococcus'),
    ('bacterial_meningitis', 'lumbar puncture'),
    ('bacterial_meningitis', 'vaccine-preventable')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'bacterial_meningitis');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('bacterial_meningitis', 'sym_fever', 9::smallint, true, 1.0::numeric),
    ('bacterial_meningitis', 'sym_headache', 8::smallint, true, 1.1::numeric),
    ('bacterial_meningitis', 'sym_neck_stiffness', 8::smallint, true, 1.5::numeric),
    ('bacterial_meningitis', 'sym_confusion', 6::smallint, false, 1.2::numeric),
    ('bacterial_meningitis', 'sym_photophobia', 6::smallint, false, 1.1::numeric),
    ('bacterial_meningitis', 'sym_nausea_vomiting', 6::smallint, false, 0.8::numeric),
    ('bacterial_meningitis', 'sym_nonblanching_rash', 3::smallint, false, 1.5::numeric),
    ('bacterial_meningitis', 'sym_seizures', 3::smallint, false, 1.0::numeric),
    ('bacterial_meningitis', 'sym_chills', 4::smallint, false, 0.6::numeric),
    ('bacterial_meningitis', 'sym_rash', 3::smallint, false, 0.6::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'bacterial_meningitis');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('bacterial_meningitis', 'med_ceftriaxone', 0, 'safe'::public.condition_safety, 'Backbone of empiric therapy, given IV immediately at meningitic doses (2 g every 12 hours in adults per IDSA).'),
    ('bacterial_meningitis', 'med_vancomycin', 1, 'safe'::public.condition_safety, 'Added to ceftriaxone empirically to cover resistant pneumococci until susceptibilities are known.'),
    ('bacterial_meningitis', 'med_dexamethasone', 2, 'safe'::public.condition_safety, 'Given just before or with the first antibiotic dose in non-epidemic settings; reduces death and hearing loss, especially in pneumococcal meningitis.'),
    ('bacterial_meningitis', 'med_rifampicin', 3, 'safe'::public.condition_safety, 'Chemoprophylaxis for close contacts of meningococcal or Hib cases; turns urine and tears orange.'),
    ('bacterial_meningitis', 'med_ciprofloxacin', 4, 'safe'::public.condition_safety, 'Single-dose chemoprophylaxis option for adult close contacts of meningococcal disease.'),
    ('bacterial_meningitis', 'med_paracetamol', 5, 'safe'::public.condition_safety, 'For fever and headache alongside antibiotics; never a substitute for urgent treatment.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'bacterial_meningitis');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_bacterial_meningitis_1', 'bacterial_meningitis', 0, 'Harrison''s Principles of Internal Medicine', 'Loscalzo J, Fauci A, Kasper D, Hauser S, Longo D, Jameson JL, eds. Harrison''s Principles of Internal Medicine, 21st ed. New York: McGraw Hill; 2022.', null, 'Internal Medicine', true),
    ('ref_bacterial_meningitis_2', 'bacterial_meningitis', 1, 'WHO Fact Sheet - Meningitis', 'World Health Organization. Meningitis. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/meningitis', 'Public Health / Infectious Disease', false),
    ('ref_bacterial_meningitis_3', 'bacterial_meningitis', 2, 'StatPearls - Bacterial Meningitis', 'Bacterial Meningitis. [Updated 2023 Aug 8]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK470351/', 'Infectious Disease / Neurology', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'bacterial_meningitis');

-- ===================================================== Hyperthyroidism (Graves' Disease)
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('graves_disease', 'Hyperthyroidism (Graves'' Disease)', 'Graves disease (autoimmune hyperthyroidism)', 'Graves disease is an autoimmune disorder in which antibodies stimulate the thyroid gland to grow and produce excess thyroid hormone. It is the most common cause of hyperthyroidism, accounting for about 60-80% of cases, and mainly affects women aged 20-50. Besides symptoms of a raised metabolic rate, it can affect the eyes (Graves orbitopathy) and, rarely, the skin (pretibial myxedema). It is treatable with antithyroid drugs, radioactive iodine or surgery.', 'sys_endo', 'Moderate', 'SEE_DOCTOR_SOON', 'Symptoms of an overactive thyroid (weight loss despite good appetite, heat intolerance, palpitations, tremor, goiter or bulging eyes) need medical review and thyroid function tests. Very high fever with agitation, confusion, vomiting or a very fast or irregular heartbeat (possible thyroid storm), fever or sore throat while on antithyroid drugs (possible agranulocytosis), or loss of vision need urgent care.', false, 'Thyroid-stimulating immunoglobulins (TSH receptor antibodies) bind and activate the TSH receptor on thyroid follicular cells, mimicking TSH. This drives uncontrolled synthesis and release of T4 and T3 and diffuse thyroid hyperplasia, while pituitary TSH is suppressed by negative feedback. The same antibodies act on TSH receptors in orbital fibroblasts and adipocytes, causing inflammation, glycosaminoglycan deposition and expansion of orbital fat and extraocular muscles (orbitopathy). Genetic susceptibility, female sex, smoking, stress and the postpartum period are triggers.', 'Excess thyroid hormone raises metabolic rate and sensitivity to catecholamines, causing heat intolerance, sweating, weight loss with increased appetite, palpitations, tachycardia or atrial fibrillation, tremor, anxiety, frequent bowel movements and menstrual changes. Continuous TSH-receptor stimulation produces a diffuse, often bruit-bearing goiter. Orbital tissue expansion causes proptosis, lid retraction, gritty eyes and diplopia. Laboratory findings are suppressed TSH, raised free T4 and/or T3, and positive TSH receptor antibodies.', 'Check free T4 and T3 about 4-6 weeks after starting methimazole, then every 4-8 weeks while adjusting the dose and every 2-3 months once stable; TSH can stay suppressed for months. Baseline CBC and liver tests are recommended, and patients must report fever or sore throat at once. After 12-18 months of treatment, measure TSH receptor antibodies to decide whether to stop; relapse is common, so monitor thyroid function after stopping. After radioactive iodine or surgery, monitor for hypothyroidism and start levothyroxine. Refer moderate-to-severe eye disease to ophthalmology.', 'StatPearls: Graves Disease (2023); StatPearls: Methimazole; Harrison''s Principles of Internal Medicine, 21st ed.', 'Usually develops gradually over weeks to months, although onset can be abrupt after stress or childbirth. Older adults may have few classic symptoms and present with weight loss, fatigue or new atrial fibrillation (apathetic hyperthyroidism). Eye disease can begin before, with or after the hyperthyroidism.', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('graves_disease', 0, 'Autoimmune production of TSH receptor-stimulating antibodies (thyroid-stimulating immunoglobulins)'),
    ('graves_disease', 1, 'Genetic susceptibility (family history of autoimmune thyroid disease)'),
    ('graves_disease', 2, 'Triggers: smoking, stress, infection, high iodine intake and the postpartum period')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'graves_disease');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('graves_disease', 0, 'Female sex (several times more common than in men)'),
    ('graves_disease', 1, 'Age 20-50 years'),
    ('graves_disease', 2, 'Family history of Graves or Hashimoto disease'),
    ('graves_disease', 3, 'Other autoimmune diseases (type 1 diabetes, vitiligo, pernicious anemia)'),
    ('graves_disease', 4, 'Smoking (also worsens eye disease)'),
    ('graves_disease', 5, 'Postpartum period')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'graves_disease');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('graves_disease', 0, 'TSH (suppressed) with free T4 and T3 (raised)'),
    ('graves_disease', 1, 'TSH receptor antibodies (TRAb or TSI) to confirm Graves disease'),
    ('graves_disease', 2, 'Radioactive iodine uptake scan (diffuse high uptake) or thyroid Doppler ultrasound (increased flow) when the cause is unclear'),
    ('graves_disease', 3, 'Baseline CBC and liver function tests before antithyroid drugs'),
    ('graves_disease', 4, 'ECG for tachycardia or atrial fibrillation'),
    ('graves_disease', 5, 'Pregnancy test in women of reproductive age before choosing treatment')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'graves_disease');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('graves_disease', 0, 'Beta-blocker (e.g., propranolol) for palpitations, tremor and anxiety while definitive treatment takes effect'),
    ('graves_disease', 1, 'Methimazole as the preferred antithyroid drug, usually for 12-18 months, titrated to free T4 and T3'),
    ('graves_disease', 2, 'Propylthiouracil instead of methimazole in the first trimester of pregnancy and in thyroid storm'),
    ('graves_disease', 3, 'Radioactive iodine ablation (not in pregnancy, breastfeeding or active moderate-to-severe eye disease), usually followed by lifelong levothyroxine'),
    ('graves_disease', 4, 'Total thyroidectomy for large goiters, suspicious nodules, pregnancy needing surgery, or patient preference'),
    ('graves_disease', 5, 'Graves orbitopathy: stop smoking, lubricating eye drops and selenium for mild disease; IV glucocorticoids or other therapies for active moderate-to-severe disease'),
    ('graves_disease', 6, 'Thyroid storm: intensive care with beta-blocker, propylthiouracil, iodine (after the thionamide), glucocorticoids and supportive care')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'graves_disease');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('graves_disease', 0, 'Take antithyroid tablets daily as prescribed and keep follow-up blood tests'),
    ('graves_disease', 1, 'Stop treatment and seek care at once if fever, sore throat or mouth ulcers develop (check for agranulocytosis)'),
    ('graves_disease', 2, 'Stop smoking, which worsens eye disease and lowers the chance of remission'),
    ('graves_disease', 3, 'Protect the eyes with sunglasses and lubricating drops, and raise the head of the bed if eyes are puffy'),
    ('graves_disease', 4, 'Avoid iodine supplements and excess seaweed while hyperthyroid, and limit caffeine if palpitations')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'graves_disease');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('graves_disease', 0, 'Very high fever with agitation, confusion or delirium (possible thyroid storm)'),
    ('graves_disease', 1, 'Chest pain, fainting or a very fast or irregular heartbeat'),
    ('graves_disease', 2, 'Fever, sore throat or mouth ulcers while taking methimazole or propylthiouracil'),
    ('graves_disease', 3, 'Yellow skin or eyes, dark urine or severe abdominal pain on antithyroid drugs'),
    ('graves_disease', 4, 'Sudden loss or dimming of vision or new double vision')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'graves_disease');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('graves_disease', 0, 'No proven way to prevent Graves disease; not smoking lowers the risk of disease and especially of eye involvement.', 'primary'::public.prevention_tier),
    ('graves_disease', 1, 'Thyroid function testing for people with suggestive symptoms, new atrial fibrillation, unexplained weight loss or a family history, so it is treated before complications develop.', 'secondary'::public.prevention_tier),
    ('graves_disease', 2, 'Definitive treatment and monitoring to prevent atrial fibrillation, heart failure, osteoporosis, thyroid storm and vision-threatening eye disease, and lifelong levothyroxine after ablation.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'graves_disease');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('graves_disease', 0, 'Toxic multinodular goiter or toxic adenoma', 'Nodular gland with patchy or focal uptake on scan; no eye disease; TRAb negative'),
    ('graves_disease', 1, 'Subacute (de Quervain) thyroiditis', 'Painful, tender thyroid after a viral illness, high ESR, low radioiodine uptake; resolves spontaneously'),
    ('graves_disease', 2, 'Painless or postpartum thyroiditis', 'Transient hyperthyroidism with low uptake, often followed by hypothyroidism'),
    ('graves_disease', 3, 'Exogenous thyroid hormone intake', 'Low thyroglobulin and low uptake; history of levothyroxine or ''slimming'' products'),
    ('graves_disease', 4, 'Anxiety disorder', 'Palpitations and tremor with normal thyroid function tests'),
    ('graves_disease', 5, 'Pheochromocytoma', 'Episodic headache, sweating and hypertension; raised metanephrines; normal thyroid tests')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'graves_disease');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('graves_disease', 'thyroid'),
    ('graves_disease', 'autoimmune'),
    ('graves_disease', 'hyperthyroidism'),
    ('graves_disease', 'orbitopathy'),
    ('graves_disease', 'endocrinology')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'graves_disease');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('graves_disease', 'sym_weight_loss', 7::smallint, true, 1.0::numeric),
    ('graves_disease', 'sym_palpitations', 7::smallint, true, 1.0::numeric),
    ('graves_disease', 'sym_heat_intolerance', 7::smallint, true, 1.4::numeric),
    ('graves_disease', 'sym_tremor', 6::smallint, false, 1.1::numeric),
    ('graves_disease', 'sym_goiter', 6::smallint, false, 1.4::numeric),
    ('graves_disease', 'sym_diaphoresis', 6::smallint, false, 0.8::numeric),
    ('graves_disease', 'sym_proptosis', 4::smallint, false, 1.5::numeric),
    ('graves_disease', 'sym_fatigue', 5::smallint, false, 0.5::numeric),
    ('graves_disease', 'sym_agitation', 4::smallint, false, 0.6::numeric),
    ('graves_disease', 'sym_diarrhea', 3::smallint, false, 0.5::numeric),
    ('graves_disease', 'sym_dyspnea', 2::smallint, false, 0.4::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'graves_disease');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('graves_disease', 'med_methimazole', 0, 'safe'::public.condition_safety, 'Preferred antithyroid drug except in the first trimester and thyroid storm; report fever or sore throat at once.'),
    ('graves_disease', 'med_propranolol', 1, 'safe'::public.condition_safety, 'Controls palpitations, tremor and anxiety within hours; avoid in asthma.'),
    ('graves_disease', 'med_metoprolol', 2, 'safe'::public.condition_safety, 'Cardioselective beta-blocker alternative when propranolol is unsuitable.'),
    ('graves_disease', 'med_prednisone', 3, 'caution'::public.condition_safety, 'Glucocorticoids are used for active moderate-to-severe orbitopathy or around radioactive iodine in eye disease, under specialist care.'),
    ('graves_disease', 'med_salbutamol', 4, 'caution'::public.condition_safety, 'Beta-agonists can worsen tachycardia and tremor in untreated hyperthyroidism; use when needed for asthma but seek thyroid control.'),
    ('graves_disease', 'med_warfarin', 5, 'caution'::public.condition_safety, 'Hyperthyroidism increases warfarin sensitivity, and needs change as thyroid levels normalise; monitor INR closely.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'graves_disease');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_graves_disease_1', 'graves_disease', 0, 'Harrison''s Principles of Internal Medicine', 'Loscalzo J, Fauci A, Kasper D, Hauser S, Longo D, Jameson JL, eds. Harrison''s Principles of Internal Medicine, 21st ed. New York: McGraw Hill; 2022.', null, 'Internal Medicine', true),
    ('ref_graves_disease_2', 'graves_disease', 1, 'StatPearls - Graves Disease', 'Graves Disease. [Updated 2023 Jun 20]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK448195/', 'Endocrinology', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'graves_disease');

-- ===================================================== Gout
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('gout', 'Gout', 'Monosodium urate crystal arthropathy', 'Gout is an inflammatory arthritis caused by deposition of monosodium urate crystals in and around joints when serum uric acid stays high (hyperuricemia). It typically causes sudden, intensely painful flares, classically in the big toe, that settle over days to weeks. Without urate-lowering treatment flares become more frequent and can lead to tophi, chronic joint damage and kidney stones. It is the most common inflammatory arthritis in adult men and is closely linked to obesity, hypertension, kidney disease and metabolic syndrome.', 'sys_musculo', 'Moderate', 'SEE_DOCTOR_SOON', 'A sudden, very painful, red, swollen joint (often the big toe) should be assessed promptly and treated early, ideally within 24 hours. Fever, chills or feeling very unwell with a hot joint needs same-day care to rule out septic arthritis.', false, 'Uric acid is the end product of purine metabolism, cleared mainly by the kidneys. Under-excretion (most cases) or overproduction raises serum urate above its saturation point of about 6.8 mg/dL, and crystals form in cooler, peripheral joints and soft tissues. When crystals are shed into the joint they are engulfed by macrophages and activate the NLRP3 inflammasome, releasing interleukin-1 beta and recruiting neutrophils, which produces an intense acute synovitis. Long-standing deposition forms tophi and erodes cartilage and bone.', 'Neutrophil-driven synovitis causes the sudden, severe pain, swelling, warmth and redness of a flare, peaking within 24 hours, most often in the first metatarsophalangeal joint (podagra), midfoot, ankle or knee. Joint fluid shows needle-shaped, negatively birefringent urate crystals. Serum urate may be normal during a flare. Chronic deposition produces tophi on the ears, fingers, elbows and Achilles tendons, punched-out erosions with overhanging edges on X-ray, a double-contour sign on ultrasound, and uric acid kidney stones.', 'Once urate-lowering therapy starts, check serum urate every 2-5 weeks while titrating to below 6 mg/dL (below 5 mg/dL with tophi), then every 6-12 months. Continue flare prophylaxis for at least 3-6 months. Monitor kidney function, blood pressure, glucose and lipids because of associated cardiometabolic disease, and review medicines that raise urate.', '2020 ACR Guideline for the Management of Gout; StatPearls: Gout; Harrison''s Principles of Internal Medicine, 21st ed.', 'A flare begins suddenly, often at night or early morning, after triggers such as alcohol, a large meat or seafood meal, dehydration, surgery or starting diuretics, and resolves within 1-2 weeks even untreated. Symptom-free intervals between flares shorten over years without urate-lowering therapy, progressing to chronic tophaceous gout.', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('gout', 0, 'Persistent hyperuricemia with urate crystal deposition (serum urate above about 6.8 mg/dL)'),
    ('gout', 1, 'Reduced kidney excretion of uric acid (most common), including chronic kidney disease'),
    ('gout', 2, 'Increased urate production (high purine turnover, myeloproliferative disorders, tumor lysis)'),
    ('gout', 3, 'Medicines that raise urate: thiazide and loop diuretics, low-dose aspirin, cyclosporine, pyrazinamide')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'gout');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('gout', 0, 'Male sex and older age (women mainly after menopause)'),
    ('gout', 1, 'Obesity and metabolic syndrome'),
    ('gout', 2, 'Alcohol, especially beer and spirits'),
    ('gout', 3, 'Diet rich in red meat, organ meats and seafood, and sugar-sweetened drinks high in fructose'),
    ('gout', 4, 'Hypertension, chronic kidney disease and heart failure'),
    ('gout', 5, 'Family history of gout')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'gout');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('gout', 0, 'Joint aspiration with polarized microscopy: needle-shaped, negatively birefringent urate crystals (gold standard); also excludes infection'),
    ('gout', 1, 'Serum uric acid (may be normal during a flare; recheck 2 weeks after it settles)'),
    ('gout', 2, 'CBC, CRP or ESR and kidney function'),
    ('gout', 3, 'Ultrasound (double-contour sign, tophi) or dual-energy CT when aspiration is not possible'),
    ('gout', 4, 'X-ray of affected joints in long-standing disease (punched-out erosions with overhanging edges)'),
    ('gout', 5, 'HLA-B*58:01 testing before allopurinol in people of Southeast Asian or Han Chinese, Korean or Thai descent and African American patients')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'gout');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('gout', 0, 'Treat flares early with low-dose colchicine, an NSAID or a glucocorticoid (oral, intra-articular or intramuscular), chosen by comorbidities'),
    ('gout', 1, 'Rest, elevation and ice on the affected joint during a flare'),
    ('gout', 2, 'Urate-lowering therapy for 2 or more flares a year, tophi, joint damage on imaging or kidney stones; allopurinol is first line, started low and titrated to serum urate below 6 mg/dL'),
    ('gout', 3, 'Febuxostat or uricosurics as alternatives when allopurinol is not tolerated or contraindicated'),
    ('gout', 4, 'Flare prophylaxis (colchicine, NSAID or low-dose prednisone) for at least 3-6 months when starting urate-lowering therapy'),
    ('gout', 5, 'Continue urate-lowering therapy during flares if already taking it'),
    ('gout', 6, 'Address contributors: switch thiazides to another antihypertensive where possible (losartan lowers urate), limit alcohol, lose weight')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'gout');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('gout', 0, 'Rest and raise the painful joint, apply ice wrapped in a cloth, and keep bedclothes off the toe'),
    ('gout', 1, 'Start flare medicine as soon as symptoms begin, as instructed'),
    ('gout', 2, 'Drink plenty of water and limit beer, spirits and sugary drinks'),
    ('gout', 3, 'Cut down on organ meats, red meat and shellfish; aim for a healthy weight'),
    ('gout', 4, 'Keep taking allopurinol every day even during a flare, unless told otherwise')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'gout');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('gout', 0, 'Hot, swollen joint with fever, chills or feeling very unwell (possible septic arthritis)'),
    ('gout', 1, 'Spreading redness up the foot or leg'),
    ('gout', 2, 'Severe flank pain with blood in urine (possible kidney stone)'),
    ('gout', 3, 'Widespread rash, blistering, mouth sores or fever after starting allopurinol (possible severe drug reaction)')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'gout');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('gout', 0, 'Healthy weight, limited alcohol and sugar-sweetened drinks, and a diet lower in red meat and seafood reduce hyperuricemia.', 'primary'::public.prevention_tier),
    ('gout', 1, 'Treat-to-target urate-lowering therapy after recurrent flares, with HLA-B*58:01 screening in high-risk groups, to prevent further flares and tophi.', 'secondary'::public.prevention_tier),
    ('gout', 2, 'Sustained urate control, management of tophi, kidney stones and cardiovascular and kidney disease to prevent joint destruction and disability.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'gout');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('gout', 0, 'Septic arthritis', 'Fever and a hot joint; organisms and very high white cells in joint fluid; may coexist with gout'),
    ('gout', 1, 'Pseudogout (calcium pyrophosphate deposition)', 'Often knee or wrist in older adults; rhomboid, positively birefringent crystals; chondrocalcinosis on X-ray'),
    ('gout', 2, 'Cellulitis', 'Spreading skin redness without a joint effusion; joint movement less painful'),
    ('gout', 3, 'Reactive arthritis', 'Follows gastrointestinal or genitourinary infection; asymmetric oligoarthritis with conjunctivitis or urethritis'),
    ('gout', 4, 'Rheumatoid arthritis', 'Symmetric small-joint polyarthritis with morning stiffness; rheumatoid factor or anti-CCP positive'),
    ('gout', 5, 'Trauma or fracture', 'Clear history of injury; fracture on X-ray')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'gout');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('gout', 'inflammatory arthritis'),
    ('gout', 'uric acid'),
    ('gout', 'podagra'),
    ('gout', 'treat-to-target'),
    ('gout', 'lifestyle')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'gout');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('gout', 'sym_podagra', 9::smallint, true, 1.5::numeric),
    ('gout', 'sym_arthralgia', 8::smallint, true, 1.1::numeric),
    ('gout', 'sym_joint_swelling', 8::smallint, true, 1.2::numeric),
    ('gout', 'sym_tophi', 2::smallint, false, 1.5::numeric),
    ('gout', 'sym_fever', 3::smallint, false, 0.5::numeric),
    ('gout', 'sym_flank_pain', 1::smallint, false, 0.3::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'gout');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('gout', 'med_colchicine', 0, 'safe'::public.condition_safety, 'Low-dose regimen for flares and 0.6 mg once or twice daily as prophylaxis; reduce dose in CKD and avoid with strong CYP3A4 inhibitors.'),
    ('gout', 'med_allopurinol', 1, 'safe'::public.condition_safety, 'First-line urate-lowering therapy; start low, titrate to urate below 6 mg/dL, screen HLA-B*58:01 in high-risk groups.'),
    ('gout', 'med_prednisone', 2, 'safe'::public.condition_safety, 'Short oral course for flares when NSAIDs or colchicine are unsuitable, e.g., in kidney disease.'),
    ('gout', 'med_ibuprofen', 3, 'caution'::public.condition_safety, 'Effective for flares in people without kidney disease, peptic ulcer, heart failure or anticoagulation.'),
    ('gout', 'med_losartan', 4, 'safe'::public.condition_safety, 'Preferred antihypertensive in gout because it modestly increases uric acid excretion (ACR 2020).'),
    ('gout', 'med_hydrochlorothiazide', 5, 'caution'::public.condition_safety, 'Thiazides raise serum urate; consider switching to another antihypertensive where possible.'),
    ('gout', 'med_furosemide', 6, 'caution'::public.condition_safety, 'Loop diuretics raise serum urate and can trigger flares; do not stop when needed for heart failure.'),
    ('gout', 'med_aspirin', 7, 'caution'::public.condition_safety, 'Low-dose aspirin slightly raises urate, but should not be stopped if needed for heart protection.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'gout');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_gout_1', 'gout', 0, 'Harrison''s Principles of Internal Medicine', 'Loscalzo J, Fauci A, Kasper D, Hauser S, Longo D, Jameson JL, eds. Harrison''s Principles of Internal Medicine, 21st ed. New York: McGraw Hill; 2022.', null, 'Internal Medicine', true),
    ('ref_gout_2', 'gout', 1, '2020 ACR Guideline for the Management of Gout', 'FitzGerald JD, Dalbeth N, Mikuls T, et al. 2020 American College of Rheumatology Guideline for the Management of Gout. Arthritis Care Res (Hoboken). 2020;72(6):744-760.', 'https://pubmed.ncbi.nlm.nih.gov/32391934/', 'Rheumatology', false),
    ('ref_gout_3', 'gout', 2, 'StatPearls - Gout', 'Gout. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK546606/', 'Rheumatology', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'gout');

-- ===================================================== Scabies
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('scabies', 'Scabies', 'Sarcoptes scabiei var. hominis infestation', 'Scabies is a contagious skin infestation by the human itch mite Sarcoptes scabiei var. hominis, which burrows into the top layer of the skin. WHO estimates at least 200 million people have it at any time, mostly in hot, crowded, low-resource settings, where 5-50% of children may be affected. It causes intense itching and rash; scratching opens the skin to streptococcal and staphylococcal infection, which can lead to sepsis, post-streptococcal glomerulonephritis and rheumatic heart disease. WHO lists it as a neglected tropical disease.', 'sys_integ', 'Mild', 'SEE_DOCTOR_SOON', 'Intense itching, worse at night, with burrows or a rash in the finger webs, wrists, waist or genitals, especially if household members itch too, should be seen by a health worker for diagnosis and treatment of the whole household. Infected sores with fever, puffy face or dark urine, or thick crusted skin in an older or immunocompromised person, need prompt care.', true, 'Fertilized female mites burrow into the stratum corneum and lay eggs, which hatch in 3-4 days; the life cycle takes about 2 weeks and most people carry only 10-15 mites. A delayed (type IV) hypersensitivity reaction to mites, eggs and feces develops after about 4-6 weeks in a first infestation, causing itching and an inflammatory papular rash, much faster on reinfestation. In people with weakened immunity, mites multiply unchecked into thousands to millions, producing crusted (Norwegian) scabies.', 'Burrows appear as short, wavy grey lines in the finger webs, wrists, elbows and genitals, while the hypersensitivity reaction produces an intensely itchy, widespread papular rash, typically worse at night and sparing the head in adults. Infants may have lesions on the palms, soles and scalp. Scratching causes excoriations and impetigo. Crusted scabies shows thick, scaly crusts with little itch and is highly contagious. Diagnosis is mainly clinical, supported by dermoscopy or microscopy of skin scrapings.', 'Review 2-4 weeks after treatment. Persistent itch alone is common and does not mean failure, but new burrows or lesions mean retreatment and checking that all contacts were treated at the same time. Treat secondary bacterial infection, and check blood pressure and urine in children with infected sores who develop swelling or dark urine. Crusted scabies needs specialist, repeated combined treatment and infection control.', 'WHO Scabies fact sheet; CDC Clinical care of scabies; StatPearls: Scabies and Permethrin; Fitzpatrick''s Dermatology, 9th ed.', 'Itching starts about 4-6 weeks after a first infestation (1-3 days after reinfestation), so a person can spread it before noticing symptoms. Untreated, it persists for months. After effective treatment, itching can continue for 2-4 weeks while the skin reaction settles (post-scabietic itch).', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('scabies', 0, 'Infestation with the mite Sarcoptes scabiei var. hominis'),
    ('scabies', 1, 'Transmission through prolonged skin-to-skin contact, mainly within households'),
    ('scabies', 2, 'Contaminated bedding and clothing (mainly with crusted scabies)')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'scabies');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('scabies', 0, 'Crowded living conditions (households, dormitories, evacuation and refugee camps)'),
    ('scabies', 1, 'Young children and older adults'),
    ('scabies', 2, 'Residents and staff of nursing homes and other institutions'),
    ('scabies', 3, 'Weakened immunity (HIV, older age, immunosuppressive drugs) for crusted scabies'),
    ('scabies', 4, 'Hot, tropical climates and limited access to health care')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'scabies');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('scabies', 0, 'Clinical diagnosis from the itch pattern, distribution of lesions and affected contacts'),
    ('scabies', 1, 'Dermoscopy: the mite at the end of a burrow (''delta-wing jet'' sign)'),
    ('scabies', 2, 'Skin scraping from a burrow examined under the microscope for mites, eggs or feces'),
    ('scabies', 3, 'Swab and culture of infected sores if impetigo or cellulitis is suspected'),
    ('scabies', 4, 'Urinalysis and blood pressure in children with infected sores who develop swelling or dark urine')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'scabies');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('scabies', 0, 'Permethrin 5% cream to the whole body from the neck down (including the head in infants and older adults), washed off after 8-14 hours and repeated after 7 days'),
    ('scabies', 1, 'Oral ivermectin 200 micrograms/kg, repeated after 7-14 days, as an alternative (not in pregnancy or children under 15 kg)'),
    ('scabies', 2, 'Treat all household members and close contacts at the same time, even if they have no symptoms'),
    ('scabies', 3, 'Wash clothing, towels and bedding used in the previous 3 days in hot water and dry in the sun or a hot dryer; seal unwashable items in a plastic bag for about a week'),
    ('scabies', 4, 'Treat itching with antihistamines and emollients; itch may persist 2-4 weeks after cure'),
    ('scabies', 5, 'Treat secondary bacterial infection (impetigo) with appropriate antibiotics'),
    ('scabies', 6, 'Crusted scabies: repeated oral ivermectin combined with topical permethrin and keratolytics, with isolation precautions'),
    ('scabies', 7, 'Mass drug administration with ivermectin in communities where prevalence is 10% or more (WHO)')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'scabies');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('scabies', 0, 'Apply the cream to cool, dry skin and reapply to hands after each handwashing during the treatment period'),
    ('scabies', 1, 'Make sure everyone in the household is treated on the same day'),
    ('scabies', 2, 'Trim fingernails and avoid scratching to prevent infected sores'),
    ('scabies', 3, 'Wash bedding and clothes in hot water, or seal them in a plastic bag for a week'),
    ('scabies', 4, 'Expect itching to continue for a few weeks after treatment; see a health worker if new spots appear')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'scabies');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('scabies', 0, 'Infected sores with fever, spreading redness or pus'),
    ('scabies', 1, 'Puffy face or eyes, dark or cola-colored urine, or very little urine weeks after infected sores'),
    ('scabies', 2, 'Joint pain with fever or breathlessness weeks after infected sores'),
    ('scabies', 3, 'Thick, crusted, widespread scaly skin in an older or immunocompromised person')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'scabies');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('scabies', 0, 'Avoid prolonged skin contact with infested people, treat all household contacts together, and reduce crowding.', 'primary'::public.prevention_tier),
    ('scabies', 1, 'Early diagnosis and simultaneous treatment of cases and contacts, outbreak control in institutions, and mass drug administration in high-prevalence communities.', 'secondary'::public.prevention_tier),
    ('scabies', 2, 'Treat secondary skin infections promptly and screen for kidney and heart complications to prevent post-streptococcal glomerulonephritis, rheumatic heart disease and sepsis.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'scabies');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('scabies', 0, 'Atopic dermatitis (eczema)', 'Chronic flexural eczema with personal or family atopy; no burrows; contacts unaffected'),
    ('scabies', 1, 'Insect bites (papular urticaria)', 'Exposed skin, seasonal, no burrows or finger-web involvement'),
    ('scabies', 2, 'Contact dermatitis', 'Rash at the site of an irritant or allergen; resolves when it is removed'),
    ('scabies', 3, 'Impetigo', 'Honey-colored crusts; may complicate scabies'),
    ('scabies', 4, 'Dermatitis herpetiformis', 'Grouped vesicles on extensor surfaces; associated with celiac disease'),
    ('scabies', 5, 'Chickenpox (varicella)', 'Fever with crops of vesicles in different stages, including the scalp and mouth')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'scabies');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('scabies', 'skin infestation'),
    ('scabies', 'itch'),
    ('scabies', 'neglected tropical disease'),
    ('scabies', 'household treatment'),
    ('scabies', 'contagious')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'scabies');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('scabies', 'sym_pruritus', 9::smallint, true, 1.3::numeric),
    ('scabies', 'sym_burrows', 6::smallint, true, 1.5::numeric),
    ('scabies', 'sym_rash', 7::smallint, true, 1.0::numeric),
    ('scabies', 'sym_vesicular_rash', 2::smallint, false, 0.4::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'scabies');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('scabies', 'med_permethrin', 0, 'safe'::public.condition_safety, 'First-line topical treatment: whole body, wash off after 8-14 hours, repeat after 7 days; treat contacts at the same time.'),
    ('scabies', 'med_ivermectin', 1, 'safe'::public.condition_safety, 'Oral alternative (200 micrograms/kg, repeated after 7-14 days) and for crusted scabies with permethrin; not in pregnancy or under 15 kg.'),
    ('scabies', 'med_cetirizine', 2, 'safe'::public.condition_safety, 'Non-sedating antihistamine to ease itching during and after treatment.'),
    ('scabies', 'med_coamoxiclav', 3, 'safe'::public.condition_safety, 'Covers streptococci and staphylococci when scabies is complicated by impetigo or cellulitis, per local guidance.'),
    ('scabies', 'med_prednisone', 4, 'avoid'::public.condition_safety, 'Systemic steroids suppress the inflammatory signs and itch, delaying diagnosis and allowing spread; treat the mites instead.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'scabies');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_scabies_1', 'scabies', 0, 'Fitzpatrick''s Dermatology', 'Kang S, Amagai M, Bruckner AL, et al., eds. Fitzpatrick''s Dermatology. 9th ed. New York: McGraw Hill; 2019.', null, 'Dermatology', true),
    ('ref_scabies_2', 'scabies', 1, 'WHO Fact Sheet - Scabies', 'World Health Organization. Scabies. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/scabies', 'Public Health / Dermatology', false),
    ('ref_scabies_3', 'scabies', 2, 'CDC - Clinical Care of Scabies', 'Centers for Disease Control and Prevention. Clinical care of scabies (for health care providers).', 'https://www.cdc.gov/scabies/hcp/clinical-care/index.html', 'Dermatology / Infectious Disease', false),
    ('ref_scabies_4', 'scabies', 3, 'StatPearls - Scabies', 'Scabies. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK544306/', 'Dermatology', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'scabies');

-- ===================================================== related diseases (after all exist)
insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('post_strep_glomerulonephritis', 'chronic_kidney_disease'),
    ('post_strep_glomerulonephritis', 'rheumatic_fever'),
    ('post_strep_glomerulonephritis', 'scabies'),
    ('post_strep_glomerulonephritis', 'urinary_tract_infection')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'post_strep_glomerulonephritis');

insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('bacterial_meningitis', 'community_acquired_pneumonia'),
    ('bacterial_meningitis', 'ischemic_stroke'),
    ('bacterial_meningitis', 'malaria'),
    ('bacterial_meningitis', 'dengue'),
    ('bacterial_meningitis', 'hiv_infection')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'bacterial_meningitis');

insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('graves_disease', 'heart_failure'),
    ('graves_disease', 'type2_diabetes')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'graves_disease');

insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('gout', 'chronic_kidney_disease'),
    ('gout', 'hypertension'),
    ('gout', 'type2_diabetes'),
    ('gout', 'heart_failure')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'gout');

insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('scabies', 'post_strep_glomerulonephritis'),
    ('scabies', 'rheumatic_fever'),
    ('scabies', 'varicella'),
    ('scabies', 'hiv_infection')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'scabies');

-- every running Akeso downloads the new entries on its next sync
update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
