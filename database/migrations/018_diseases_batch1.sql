-- =====================================================================
-- 018_diseases_batch1.sql  -  5 new diseases with their symptoms and medicines
-- =====================================================================
-- Diseases: Acute Appendicitis, Gastroesophageal Reflux Disease (GERD), Iron-Deficiency Anemia, Chronic Kidney Disease, Acute Rheumatic Fever and Rheumatic Heart Disease.
-- New symptoms: sym_rlq_pain, sym_regurgitation, sym_dysphagia, sym_pallor, sym_pica, sym_koilonychia, sym_foamy_urine, sym_nocturia, sym_chorea, sym_erythema_marginatum.
-- New medicines: med_metronidazole, med_famotidine, med_aluminium_magnesium_hydroxide, med_ferrous_sulfate, med_benzathine_penicillin.
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
values ('sym_rlq_pain', 'Right lower abdominal pain (right lower quadrant)', 'Right lower quadrant abdominal pain', 'Pain felt in the right lower part of the abdomen, below the navel and toward the hip bone. In acute appendicitis it typically begins as vague pain around the navel and moves to the right lower quadrant (McBurney point) over 12-24 hours as the inflamed appendix irritates the overlying peritoneum. Ovarian, tubal, urinary tract and bowel conditions can cause pain in the same area.', 'sys_digest', true, array['abdomen', 'pain', 'appendicitis', 'surgical']::text[], 7, 'Pain that starts around the navel and settles in the right lower abdomen is the classic pattern of acute appendicitis and points strongly toward it, although gynecologic, urinary and bowel causes must be excluded.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Appendicitis', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_rlq_pain', 'Acute appendicitis', 0),
    ('sym_rlq_pain', 'Mesenteric adenitis', 1),
    ('sym_rlq_pain', 'Ectopic pregnancy', 2),
    ('sym_rlq_pain', 'Ovarian cyst rupture or ovarian torsion', 3),
    ('sym_rlq_pain', 'Pelvic inflammatory disease', 4),
    ('sym_rlq_pain', 'Right ureteric stone (renal colic)', 5),
    ('sym_rlq_pain', 'Crohn disease of the terminal ileum', 6),
    ('sym_rlq_pain', 'Infectious ileitis (Yersinia, Campylobacter)', 7)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_rlq_pain');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_rlq_pain', 'Pain that worsens with walking, coughing or jolting (peritoneal irritation)', 0),
    ('sym_rlq_pain', 'Fever with persistent vomiting', 1),
    ('sym_rlq_pain', 'Rigid or board-like abdomen', 2),
    ('sym_rlq_pain', 'Missed period or positive pregnancy test with pain or vaginal bleeding', 3),
    ('sym_rlq_pain', 'Fainting, low blood pressure or rapid heart rate', 4)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_rlq_pain');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_rlq_pain', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_rlq_pain', 'StatPearls - Appendicitis', 'Lotfollahzadeh S, Lopez RA, Deppen JG. Appendicitis. [Updated 2024 Feb 12]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026 Jan-.', 'https://www.ncbi.nlm.nih.gov/books/NBK493193/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_rlq_pain');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_regurgitation', 'Acid regurgitation (sour fluid or food coming back up)', 'Regurgitation', 'Effortless backflow of sour or bitter stomach contents into the throat or mouth, without the retching of vomiting. It is, with heartburn, one of the two typical symptoms of gastroesophageal reflux disease and is often worse after large meals, when bending over or when lying down.', 'sys_digest', false, array['GERD', 'esophagus', 'reflux']::text[], 7, 'Heartburn and regurgitation are the two typical symptoms of GERD; together, without alarm features, they support a presumptive diagnosis.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Gastroesophageal Reflux Disease', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_regurgitation', 'Gastroesophageal reflux disease', 0),
    ('sym_regurgitation', 'Hiatal hernia', 1),
    ('sym_regurgitation', 'Achalasia', 2),
    ('sym_regurgitation', 'Rumination syndrome', 3),
    ('sym_regurgitation', 'Gastroparesis', 4),
    ('sym_regurgitation', 'Pregnancy', 5)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_regurgitation');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_regurgitation', 'Difficulty or pain on swallowing', 0),
    ('sym_regurgitation', 'Unintentional weight loss', 1),
    ('sym_regurgitation', 'Vomiting blood or black stools', 2),
    ('sym_regurgitation', 'Choking or coughing at night with recurrent chest infections', 3)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_regurgitation');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_regurgitation', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_regurgitation', 'StatPearls - Gastroesophageal Reflux Disease', 'Antunes C, Aleem A, Curtis SA. Gastroesophageal Reflux Disease. [Updated 2023 Jul 3]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK441938/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_regurgitation');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_dysphagia', 'Difficulty swallowing (dysphagia)', 'Dysphagia', 'A sensation that food or liquid sticks or passes slowly on the way from the mouth to the stomach. Oropharyngeal dysphagia (trouble starting a swallow, coughing or choking) usually has a neurologic or muscular cause, while esophageal dysphagia (food sticking behind the breastbone) suggests a stricture, ring, motility disorder or tumor. In GERD it is an alarm feature.', 'sys_digest', true, array['esophagus', 'swallowing', 'alarm feature']::text[], 5, 'Dysphagia is not specific to one disease, but it is an alarm feature: in reflux it suggests stricture or malignancy and calls for endoscopy.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Gastroesophageal Reflux Disease', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_dysphagia', 'Peptic stricture from long-standing GERD', 0),
    ('sym_dysphagia', 'Esophageal or gastric cancer', 1),
    ('sym_dysphagia', 'Eosinophilic esophagitis', 2),
    ('sym_dysphagia', 'Achalasia and other motility disorders', 3),
    ('sym_dysphagia', 'Stroke and other neurologic disease', 4),
    ('sym_dysphagia', 'Esophageal rings or webs (e.g., Plummer-Vinson syndrome)', 5)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dysphagia');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_dysphagia', 'Food stuck with inability to swallow saliva', 0),
    ('sym_dysphagia', 'Progressive difficulty from solids to liquids', 1),
    ('sym_dysphagia', 'Unintentional weight loss', 2),
    ('sym_dysphagia', 'Vomiting blood or black stools', 3),
    ('sym_dysphagia', 'Sudden onset with facial droop, slurred speech or weakness', 4)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dysphagia');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_dysphagia', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_dysphagia', 'StatPearls - Gastroesophageal Reflux Disease', 'Antunes C, Aleem A, Curtis SA. Gastroesophageal Reflux Disease. [Updated 2023 Jul 3]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK441938/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_dysphagia');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_pallor', 'Pale skin, lips or inner eyelids (pallor)', 'Pallor', 'Unusual paleness of the skin and mucous membranes, best seen in the inner lower eyelids (conjunctivae), palms, nail beds and lips. It most often reflects a reduced hemoglobin concentration (anemia) but can also occur with shock or reduced skin blood flow.', 'bs_hematologic', false, array['anemia', 'skin', 'examination sign']::text[], 5, 'Pallor of the conjunctivae, palms and nail beds is a useful bedside sign of anemia, but it does not identify the cause.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Iron-Deficiency Anemia', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_pallor', 'Iron-deficiency anemia', 0),
    ('sym_pallor', 'Anemia of chronic kidney disease or chronic inflammation', 1),
    ('sym_pallor', 'Acute or chronic blood loss', 2),
    ('sym_pallor', 'Thalassemia and other hemoglobin disorders', 3),
    ('sym_pallor', 'Vitamin B12 or folate deficiency', 4),
    ('sym_pallor', 'Shock or fainting', 5)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_pallor');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_pallor', 'Shortness of breath at rest or chest pain', 0),
    ('sym_pallor', 'Fainting or near-fainting', 1),
    ('sym_pallor', 'Vomiting blood, black stools or heavy bleeding', 2),
    ('sym_pallor', 'Pallor with fever, easy bruising or bleeding gums', 3)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_pallor');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_pallor', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_pallor', 'StatPearls - Iron-Deficiency Anemia', 'Jogu P, Kamran MT. Iron-Deficiency Anemia. [Updated 2026 Feb 15]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026 Jan-.', 'https://www.ncbi.nlm.nih.gov/books/NBK448065/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_pallor');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_pica', 'Craving ice, soil or other non-food items (pica)', 'Pica', 'Persistent craving for and eating of non-food substances such as ice (pagophagia), clay or soil (geophagia), starch or chalk. Pica is a recognised feature of iron deficiency, with or without anemia, and is also seen in pregnancy, young children and some developmental conditions.', 'bs_hematologic', false, array['iron deficiency', 'behavior', 'anemia']::text[], 7, 'Pica, especially pagophagia (craving ice), is a fairly specific clue to iron deficiency and often improves quickly with iron replacement.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Iron-Deficiency Anemia', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_pica', 'Iron deficiency', 0),
    ('sym_pica', 'Pregnancy', 1),
    ('sym_pica', 'Developmental disorders and autism spectrum disorder', 2),
    ('sym_pica', 'Zinc deficiency', 3),
    ('sym_pica', 'Cultural practices', 4)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_pica');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_pica', 'Eating soil or paint chips (risk of parasites and lead poisoning)', 0),
    ('sym_pica', 'Abdominal pain, constipation or vomiting suggesting bowel obstruction', 1),
    ('sym_pica', 'Pica in a young child with irritability or developmental delay', 2)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_pica');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_pica', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_pica', 'StatPearls - Iron-Deficiency Anemia', 'Jogu P, Kamran MT. Iron-Deficiency Anemia. [Updated 2026 Feb 15]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026 Jan-.', 'https://www.ncbi.nlm.nih.gov/books/NBK448065/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_pica');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_koilonychia', 'Spoon-shaped, brittle nails (koilonychia)', 'Koilonychia', 'Thin, brittle nails that become flat and then concave, so that the nail can hold a drop of water (spoon nails). It is classically linked to chronic iron deficiency, and can be normal in infants or follow trauma and occupational exposure.', 'bs_hematologic', false, array['nails', 'iron deficiency', 'examination sign']::text[], 6, 'Koilonychia is uncommon but, when present, strongly suggests long-standing iron deficiency.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Iron-Deficiency Anemia', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_koilonychia', 'Chronic iron deficiency', 0),
    ('sym_koilonychia', 'Normal finding in infancy', 1),
    ('sym_koilonychia', 'Trauma or occupational exposure to oils and solvents', 2),
    ('sym_koilonychia', 'Hemochromatosis', 3),
    ('sym_koilonychia', 'Hypothyroidism', 4)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_koilonychia');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_koilonychia', 'Accompanied by difficulty swallowing (possible Plummer-Vinson syndrome)', 0),
    ('sym_koilonychia', 'Accompanied by fatigue, breathlessness or pallor', 1)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_koilonychia');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_koilonychia', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_koilonychia', 'StatPearls - Iron-Deficiency Anemia', 'Jogu P, Kamran MT. Iron-Deficiency Anemia. [Updated 2026 Feb 15]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026 Jan-.', 'https://www.ncbi.nlm.nih.gov/books/NBK448065/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_koilonychia');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_foamy_urine', 'Foamy or bubbly urine', 'Proteinuria (foamy urine)', 'Urine that repeatedly forms a frothy layer that does not settle. Occasional foam is normal (forceful stream, concentrated urine), but persistent foaminess can reflect large amounts of protein in the urine (proteinuria), a marker of glomerular kidney damage in diabetes, hypertension and glomerulonephritis.', 'sys_renal', false, array['kidney', 'urine', 'proteinuria']::text[], 5, 'Persistently foamy urine can indicate significant proteinuria, an important marker of kidney damage, but it needs urine testing to confirm.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Chronic Kidney Disease', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_foamy_urine', 'Diabetic kidney disease', 0),
    ('sym_foamy_urine', 'Hypertensive kidney disease', 1),
    ('sym_foamy_urine', 'Glomerulonephritis and nephrotic syndrome', 2),
    ('sym_foamy_urine', 'Concentrated urine or dehydration', 3),
    ('sym_foamy_urine', 'Forceful urine stream (benign)', 4)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_foamy_urine');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_foamy_urine', 'Swelling of the face, legs or abdomen', 0),
    ('sym_foamy_urine', 'Reduced urine output', 1),
    ('sym_foamy_urine', 'Blood-colored or cola-colored urine', 2),
    ('sym_foamy_urine', 'High blood pressure with headache or breathlessness', 3)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_foamy_urine');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_foamy_urine', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_foamy_urine', 'StatPearls - Chronic Kidney Disease', 'Vaidya SR, Aeddula NR. Chronic Kidney Disease. [Updated 2024 Jul 31]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK535404/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_foamy_urine');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_nocturia', 'Waking at night to urinate (nocturia)', 'Nocturia', 'Waking from sleep one or more times to pass urine. Causes include high evening fluid or caffeine intake, bladder and prostate problems, diabetes (high urine volume), heart failure (fluid shifted at night) and chronic kidney disease, in which the kidneys lose the ability to concentrate urine.', 'sys_renal', false, array['urination', 'kidney', 'nonspecific']::text[], 3, 'Nocturia is common and nonspecific; in chronic kidney disease it reflects loss of urine-concentrating ability, but it is more often due to fluid intake, prostate disease or diabetes.', 'Bates'' Guide to Physical Examination and History Taking; StatPearls - Chronic Kidney Disease', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_nocturia', 'Evening fluid, caffeine or alcohol intake', 0),
    ('sym_nocturia', 'Benign prostatic hyperplasia', 1),
    ('sym_nocturia', 'Diabetes mellitus', 2),
    ('sym_nocturia', 'Chronic kidney disease', 3),
    ('sym_nocturia', 'Heart failure', 4),
    ('sym_nocturia', 'Diuretic medicines taken late in the day', 5),
    ('sym_nocturia', 'Urinary tract infection', 6)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_nocturia');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_nocturia', 'Excessive thirst and weight loss (possible uncontrolled diabetes)', 0),
    ('sym_nocturia', 'Leg swelling or breathlessness when lying flat', 1),
    ('sym_nocturia', 'Fever, flank pain or blood in the urine', 2)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_nocturia');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_nocturia', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_nocturia', 'StatPearls - Chronic Kidney Disease', 'Vaidya SR, Aeddula NR. Chronic Kidney Disease. [Updated 2024 Jul 31]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK535404/', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_nocturia');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_chorea', 'Involuntary jerky movements (chorea)', 'Chorea', 'Brief, irregular, purposeless movements that flow from one body part to another, often with clumsiness, facial grimacing and emotional lability. In children and adolescents the most common acquired cause is Sydenham chorea, a late manifestation of acute rheumatic fever that can appear months after the streptococcal infection.', 'sys_nervous', true, array['movement disorder', 'rheumatic fever', 'neurologic']::text[], 8, 'In a child or adolescent, new chorea is a major Jones criterion and is strongly suggestive of acute rheumatic fever (Sydenham chorea), even without other features.', 'Bates'' Guide to Physical Examination and History Taking; AHA Scientific Statement - Revision of the Jones Criteria (2015); WHO Fact Sheet - Rheumatic heart disease', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_chorea', 'Sydenham chorea (acute rheumatic fever)', 0),
    ('sym_chorea', 'Medicines (e.g., levodopa, antipsychotic withdrawal)', 1),
    ('sym_chorea', 'Huntington disease', 2),
    ('sym_chorea', 'Systemic lupus erythematosus and antiphospholipid syndrome', 3),
    ('sym_chorea', 'Hyperthyroidism', 4),
    ('sym_chorea', 'Pregnancy (chorea gravidarum)', 5),
    ('sym_chorea', 'Stroke involving the basal ganglia', 6)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chorea');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_chorea', 'Sudden one-sided movements in an adult (possible stroke)', 0),
    ('sym_chorea', 'Chest pain, breathlessness or a new heart murmur', 1),
    ('sym_chorea', 'Movements that prevent eating, walking or self-care', 2)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_chorea');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_chorea', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_chorea', 'AHA Scientific Statement - Revision of the Jones Criteria (2015)', 'Gewitz MH, Baltimore RS, Tani LY, et al. Revision of the Jones Criteria for the diagnosis of acute rheumatic fever in the era of Doppler echocardiography: a scientific statement from the American Heart Association. Circulation. 2015;131(20):1806-1818.', '', false, 1),
    ('sym_chorea', 'WHO Fact Sheet - Rheumatic heart disease', 'World Health Organization. Rheumatic heart disease. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/rheumatic-heart-disease', false, 2)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_chorea');

insert into public.symptoms (id, name, scientific_name, description, body_system_id, is_red_flag, tags, diagnostic_weight, weight_rationale, source_attribution, is_published)
values ('sym_erythema_marginatum', 'Pink ring-shaped rash on the trunk (erythema marginatum)', 'Erythema marginatum', 'A faint pink, non-itchy rash of rings or arcs with pale centres and sharp, raised edges, appearing mainly on the trunk and upper limbs and sparing the face. It comes and goes, may be brought out by heat, and is a rare but specific sign of acute rheumatic fever.', 'sys_integ', false, array['rash', 'rheumatic fever', 'skin']::text[], 9, 'Erythema marginatum is rare but highly specific; it is a major Jones criterion for acute rheumatic fever.', 'Bates'' Guide to Physical Examination and History Taking; AHA Scientific Statement - Revision of the Jones Criteria (2015)', true)
on conflict (id) do nothing;
insert into public.symptom_causes (symptom_id, content, position)
select * from (values
    ('sym_erythema_marginatum', 'Acute rheumatic fever', 0),
    ('sym_erythema_marginatum', 'Hereditary angioedema (prodromal rash)', 1)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_causes where symptom_id = 'sym_erythema_marginatum');

insert into public.symptom_red_flags (symptom_id, content, position)
select * from (values
    ('sym_erythema_marginatum', 'Accompanied by joint pain, fever or a new heart murmur', 0),
    ('sym_erythema_marginatum', 'Breathlessness, chest pain or leg swelling', 1)
) v(symptom_id, content, position)
where not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_erythema_marginatum');

insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('sym_erythema_marginatum', 'Bates'' Guide to Physical Examination and History Taking', 'Bickley LS, Szilagyi PG, Hoffman RM, Soriano RP. Bates'' Guide to Physical Examination and History Taking. 13th ed. Philadelphia: Wolters Kluwer; 2021.', '', true, 0),
    ('sym_erythema_marginatum', 'AHA Scientific Statement - Revision of the Jones Criteria (2015)', 'Gewitz MH, Baltimore RS, Tani LY, et al. Revision of the Jones Criteria for the diagnosis of acute rheumatic fever in the era of Doppler echocardiography: a scientific statement from the American Heart Association. Circulation. 2015;131(20):1806-1818.', '', false, 1)
) v(symptom_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.symptom_references where symptom_id = 'sym_erythema_marginatum');

-- ===================================================== new medicines
insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_metronidazole', 'Metronidazole', 'Metronidazole', 'Flagyl', 'Nitroimidazole antibacterial / antiprotozoal', 'Prescription', 'Metronidazole is a nitroimidazole that enters anaerobic bacteria and protozoa by diffusion and is activated by intracellular reduction to cytotoxic free radicals that break DNA strands, causing cell death. Its antibacterial activity is limited to anaerobes, so in mixed intra-abdominal infections it is combined with an agent active against aerobic gram-negative bacteria.', 'Adults, intra-abdominal infection (e.g., appendicitis, with a cephalosporin): 500 mg IV or orally every 8 hours. Bacterial vaginosis: 500 mg orally twice daily for 7 days. Trichomoniasis: 2 g orally as a single dose or 500 mg twice daily for 7 days. Giardiasis: 250 mg three times daily or 500 mg twice daily for 5-7 days. Amebiasis: 500-750 mg every 8 hours for 7-10 days, then a luminal agent. Refer to current product labeling.', 'Adults, intra-abdominal infection (e.g., appendicitis, with a cephalosporin): 500 mg IV or orally every 8 hours. Bacterial vaginosis: 500 mg orally twice daily for 7 days. Trichomoniasis: 2 g orally as a single dose or 500 mg twice daily for 7 days. Giardiasis: 250 mg three times daily or 500 mg twice daily for 5-7 days. Amebiasis: 500-750 mg every 8 hours for 7-10 days, then a luminal agent. Refer to current product labeling.', 'Store at 20-25 C, protected from light.', 'Store at 20-25 C, protected from light.', 'Carcinogenic in mice and rats. The risk to humans is considered low, but unnecessary use should be avoided and it should be reserved for approved indications.', 'metronidazole', 'StatPearls: Metronidazole; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_metronidazole', 'brand_intl', 'Flagyl', 0),
    ('med_metronidazole', 'indication', 'Anaerobic and mixed intra-abdominal infections (with an aerobic agent)', 0),
    ('med_metronidazole', 'indication', 'Bacterial vaginosis and trichomoniasis', 1),
    ('med_metronidazole', 'indication', 'Amebiasis and giardiasis', 2),
    ('med_metronidazole', 'indication', 'Part of Helicobacter pylori eradication regimens', 3),
    ('med_metronidazole', 'indication', 'Clostridioides difficile infection when vancomycin or fidaxomicin are unavailable', 4),
    ('med_metronidazole', 'adverse', 'Metallic taste, nausea, vomiting and diarrhea', 0),
    ('med_metronidazole', 'adverse', 'Headache', 1),
    ('med_metronidazole', 'adverse', 'Peripheral neuropathy and other neurotoxicity with prolonged courses', 2),
    ('med_metronidazole', 'adverse', 'Transient leukopenia or neutropenia', 3),
    ('med_metronidazole', 'adverse', 'Vaginal or oral candidiasis (superinfection)', 4),
    ('med_metronidazole', 'contraindication', 'Hypersensitivity to metronidazole or other nitroimidazoles', 0),
    ('med_metronidazole', 'contraindication', 'Disulfiram use within the past 2 weeks', 1),
    ('med_metronidazole', 'contraindication', 'Alcohol or propylene glycol products during and for at least 3 days after therapy', 2),
    ('med_metronidazole', 'contraindication', 'First trimester of pregnancy (avoid where possible)', 3),
    ('med_metronidazole', 'interaction', 'Alcohol and alcohol-containing syrups: disulfiram-like reaction (flushing, palpitations, vomiting).', 0),
    ('med_metronidazole', 'interaction', 'Disulfiram: acute psychosis and confusion; avoid within 2 weeks.', 1),
    ('med_metronidazole', 'interaction', 'Warfarin: enhanced anticoagulant effect; monitor INR closely.', 2),
    ('med_metronidazole', 'interaction', 'Lithium: raised lithium levels; monitor levels and kidney function.', 3)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_metronidazole');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_metronidazole', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_metronidazole', 'StatPearls - Metronidazole', 'Metronidazole. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; updated 2023 Jun 26.', 'https://www.statpearls.com/point-of-care/25091', false, 1)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_metronidazole');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_famotidine', 'Famotidine', 'Famotidine', 'Pepcid', 'Histamine H2-receptor antagonist', 'OTC', 'Famotidine competitively blocks histamine H2 receptors on gastric parietal cells, reducing basal, nocturnal and stimulated gastric acid secretion. It relieves heartburn and heals peptic ulcers and esophagitis, but is less potent than proton pump inhibitors; it is useful for on-demand symptom control and as a bedtime add-on for nighttime reflux.', 'Adults, non-erosive GERD: 20 mg orally twice daily for up to 6 weeks. Erosive esophagitis: 20-40 mg twice daily for up to 12 weeks. OTC heartburn products (10-20 mg): one tablet 10-60 minutes before trigger food or drink; do not use for more than 2 weeks without medical advice. Creatinine clearance below 50 mL/min: halve the dose or extend the interval to 36-48 hours. Refer to current product labeling.', 'Adults, non-erosive GERD: 20 mg orally twice daily for up to 6 weeks. Erosive esophagitis: 20-40 mg twice daily for up to 12 weeks. OTC heartburn products (10-20 mg): one tablet 10-60 minutes before trigger food or drink; do not use for more than 2 weeks without medical advice. Creatinine clearance below 50 mL/min: halve the dose or extend the interval to 36-48 hours. Refer to current product labeling.', 'Store at 20-25 C.', 'Store at 20-25 C.', null, 'famotidine', 'StatPearls: Famotidine; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_famotidine', 'brand_intl', 'Pepcid', 0),
    ('med_famotidine', 'indication', 'Gastroesophageal reflux disease and erosive esophagitis', 0),
    ('med_famotidine', 'indication', 'Duodenal and gastric ulcers', 1),
    ('med_famotidine', 'indication', 'Prevention and relief of heartburn (OTC)', 2),
    ('med_famotidine', 'indication', 'Pathological hypersecretory conditions (e.g., Zollinger-Ellison syndrome)', 3),
    ('med_famotidine', 'adverse', 'Headache', 0),
    ('med_famotidine', 'adverse', 'Diarrhea or constipation', 1),
    ('med_famotidine', 'adverse', 'Dizziness', 2),
    ('med_famotidine', 'adverse', 'Confusion or agitation, especially in older adults and kidney impairment', 3),
    ('med_famotidine', 'adverse', 'Thrombocytopenia (rare)', 4),
    ('med_famotidine', 'contraindication', 'Hypersensitivity to famotidine or other H2-receptor antagonists', 0),
    ('med_famotidine', 'contraindication', 'OTC use with swallowing difficulty, vomiting blood or black stools (needs medical review)', 1),
    ('med_famotidine', 'interaction', 'Drugs needing gastric acid for absorption (e.g., dasatinib, cefuroxime, risedronate): reduced absorption; avoid combination.', 0),
    ('med_famotidine', 'interaction', 'Tizanidine: famotidine mildly inhibits CYP1A2 and can raise tizanidine levels (hypotension, drowsiness).', 1)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_famotidine');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_famotidine', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_famotidine', 'StatPearls - Famotidine', 'Patel P, Ahlawat R. Famotidine. [Updated 2025 Sep 14]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026 Jan-.', 'https://www.ncbi.nlm.nih.gov/books/NBK534778/', false, 1)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_famotidine');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_aluminium_magnesium_hydroxide', 'Aluminium hydroxide + Magnesium hydroxide', 'Aluminium hydroxide + Magnesium hydroxide', 'Maalox', 'Antacid', 'OTC', 'A combination antacid that neutralizes gastric acid already secreted, giving fast but short-lived relief of heartburn and dyspepsia. Aluminium hydroxide also inhibits pepsin and tends to constipate, while magnesium hydroxide tends to loosen the stool, so combining them balances the effect on bowel habit. Antacids are suited to mild, intermittent reflux symptoms.', 'Adults: take as directed on the product label, usually after meals and at bedtime or when symptoms occur. Do not exceed the labeled maximum daily dose or use for more than 2 weeks without medical advice. Separate from other oral medicines by at least 2 hours. Refer to current product labeling.', 'Adults: take as directed on the product label, usually after meals and at bedtime or when symptoms occur. Do not exceed the labeled maximum daily dose or use for more than 2 weeks without medical advice. Separate from other oral medicines by at least 2 hours. Refer to current product labeling.', 'Store below 25 C; do not freeze suspensions.', 'Store below 25 C; do not freeze suspensions.', null, 'aluminium hydroxide; magnesium hydroxide', 'StatPearls: Antacids; MSF Essential Drugs; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_aluminium_magnesium_hydroxide', 'brand_intl', 'Maalox', 0),
    ('med_aluminium_magnesium_hydroxide', 'brand_intl', 'Mylanta', 1),
    ('med_aluminium_magnesium_hydroxide', 'indication', 'Mild, intermittent heartburn and gastroesophageal reflux symptoms', 0),
    ('med_aluminium_magnesium_hydroxide', 'indication', 'Dyspepsia and acid indigestion', 1),
    ('med_aluminium_magnesium_hydroxide', 'indication', 'Adjunct relief of peptic ulcer pain', 2),
    ('med_aluminium_magnesium_hydroxide', 'adverse', 'Constipation (aluminium) or diarrhea (magnesium)', 0),
    ('med_aluminium_magnesium_hydroxide', 'adverse', 'Hypophosphatemia with prolonged high-dose aluminium use', 1),
    ('med_aluminium_magnesium_hydroxide', 'adverse', 'Aluminium and magnesium accumulation in kidney failure (osteomalacia, encephalopathy, hypermagnesemia)', 2),
    ('med_aluminium_magnesium_hydroxide', 'contraindication', 'Hypersensitivity to any component', 0),
    ('med_aluminium_magnesium_hydroxide', 'contraindication', 'Severe kidney impairment (risk of aluminium and magnesium accumulation)', 1),
    ('med_aluminium_magnesium_hydroxide', 'interaction', 'Tetracyclines, doxycycline and fluoroquinolones (e.g., ciprofloxacin): chelation reduces antibiotic absorption; separate by at least 2 hours.', 0),
    ('med_aluminium_magnesium_hydroxide', 'interaction', 'Iron salts: reduced iron absorption; separate by at least 2 hours.', 1),
    ('med_aluminium_magnesium_hydroxide', 'interaction', 'Dolutegravir and other integrase inhibitors: reduced absorption; take the antiretroviral 2 hours before or 6 hours after.', 2),
    ('med_aluminium_magnesium_hydroxide', 'interaction', 'Levothyroxine: reduced absorption; separate by 4 hours.', 3)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_aluminium_magnesium_hydroxide', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_aluminium_magnesium_hydroxide', 'StatPearls - Antacids', 'Salisbury BH, Terrell JM. Antacids. [Updated 2023 Aug 8]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK526049/', false, 1),
    ('med_aluminium_magnesium_hydroxide', 'MSF Essential Drugs - Ferrous salts (oral)', 'Medecins Sans Frontieres. Essential drugs - practical guidelines: Ferrous salts, oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ferrous-salts-16683659.html', false, 2)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_aluminium_magnesium_hydroxide');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_ferrous_sulfate', 'Ferrous Sulfate', 'Ferrous sulfate', 'Feosol', 'Oral iron replacement', 'OTC', 'Ferrous sulfate supplies ferrous iron, which is absorbed mainly in the duodenum and used to rebuild body iron stores and hemoglobin. It is first-line treatment for iron-deficiency anemia. A 200 mg ferrous sulfate tablet contains about 65 mg of elemental iron; hemoglobin usually rises within about a month, and treatment continues for about 3 months to refill stores.', 'Adults and children 12 years and over, treatment: 65 mg elemental iron (one 200 mg tablet) 2-3 times daily; lower or alternate-day dosing may be better tolerated and absorbed. Children 1 month to under 6 years: 1.5-3 mg/kg elemental iron twice daily; 6 to under 12 years: 65 mg twice daily. Prevention (adults): 65 mg once daily. Usual course about 3 months. Refer to current product labeling.', 'Adults and children 12 years and over, treatment: 65 mg elemental iron (one 200 mg tablet) 2-3 times daily; lower or alternate-day dosing may be better tolerated and absorbed. Children 1 month to under 6 years: 1.5-3 mg/kg elemental iron twice daily; 6 to under 12 years: 65 mg twice daily. Prevention (adults): 65 mg once daily. Usual course about 3 months. Refer to current product labeling.', 'Store below 25 C, out of the reach of children.', 'Store below 25 C, out of the reach of children.', 'Label warning (not a boxed warning): accidental overdose of iron-containing products is a leading cause of fatal poisoning in children under 6. Keep out of the reach of children.', 'ferrous sulfate', 'StatPearls: Iron-Deficiency Anemia; MSF Essential Drugs: Ferrous salts; Goodman & Gilman''s 14th ed.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_ferrous_sulfate', 'brand_intl', 'Feosol', 0),
    ('med_ferrous_sulfate', 'indication', 'Treatment of iron-deficiency anemia', 0),
    ('med_ferrous_sulfate', 'indication', 'Prevention of iron deficiency in pregnancy, infancy and other periods of high demand', 1),
    ('med_ferrous_sulfate', 'adverse', 'Nausea, abdominal pain and epigastric discomfort', 0),
    ('med_ferrous_sulfate', 'adverse', 'Constipation or diarrhea', 1),
    ('med_ferrous_sulfate', 'adverse', 'Black stools (harmless)', 2),
    ('med_ferrous_sulfate', 'adverse', 'Tooth staining with liquid preparations', 3),
    ('med_ferrous_sulfate', 'contraindication', 'Anemia not caused by iron deficiency (e.g., thalassemia without iron deficiency)', 0),
    ('med_ferrous_sulfate', 'contraindication', 'Iron overload (hemochromatosis, hemosiderosis)', 1),
    ('med_ferrous_sulfate', 'contraindication', 'Repeated blood transfusions without documented iron deficiency', 2),
    ('med_ferrous_sulfate', 'interaction', 'Antacids (aluminium or magnesium hydroxide): reduced iron absorption; separate by at least 2 hours.', 0),
    ('med_ferrous_sulfate', 'interaction', 'Doxycycline, tetracyclines and ciprofloxacin: mutual chelation; separate by at least 2 hours.', 1),
    ('med_ferrous_sulfate', 'interaction', 'Dolutegravir, levodopa and zinc: reduced absorption; separate by at least 2 hours.', 2),
    ('med_ferrous_sulfate', 'interaction', 'Vitamin C (ascorbic acid): increases iron absorption.', 3)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_ferrous_sulfate');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_ferrous_sulfate', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_ferrous_sulfate', 'StatPearls - Iron-Deficiency Anemia', 'Jogu P, Kamran MT. Iron-Deficiency Anemia. [Updated 2026 Feb 15]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026 Jan-.', 'https://www.ncbi.nlm.nih.gov/books/NBK448065/', false, 1),
    ('med_ferrous_sulfate', 'MSF Essential Drugs - Ferrous salts (oral)', 'Medecins Sans Frontieres. Essential drugs - practical guidelines: Ferrous salts, oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/ferrous-salts-16683659.html', false, 2)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_ferrous_sulfate');

insert into public.medicines (id, name, generic_name, trade_name, drug_class, category, description, dosage_info, dosage_text, storage_instructions, storage, black_box_warning, international_generic_name, source_attribution, is_published)
values ('med_benzathine_penicillin', 'Benzathine Penicillin G', 'Benzathine benzylpenicillin', 'Bicillin L-A', 'Long-acting penicillin (beta-lactam)', 'Prescription', 'Benzathine penicillin G is a depot form of penicillin G that is released slowly from the intramuscular injection site, giving low but prolonged blood levels for 3-4 weeks. Like other penicillins it inhibits bacterial cell-wall synthesis and is bactericidal. A single injection eradicates group A streptococcal pharyngitis, and repeated injections every 3-4 weeks are the most effective secondary prophylaxis against recurrent rheumatic fever.', 'Deep intramuscular injection only. Streptococcal pharyngitis: 1.2 million units once (600,000 units for children under 27 kg). Secondary prophylaxis of rheumatic fever: 1.2 million units every 4 weeks, or every 3 weeks in high-risk patients (600,000 units for children under 27 kg). Early syphilis: 2.4 million units once. Refer to current product labeling.', 'Deep intramuscular injection only. Streptococcal pharyngitis: 1.2 million units once (600,000 units for children under 27 kg). Secondary prophylaxis of rheumatic fever: 1.2 million units every 4 weeks, or every 3 weeks in high-risk patients (600,000 units for children under 27 kg). Early syphilis: 2.4 million units once. Refer to current product labeling.', 'Refrigerate at 2-8 C. Do not freeze. Bring to room temperature before injection.', 'Refrigerate at 2-8 C. Do not freeze. Bring to room temperature before injection.', 'For deep intramuscular use only. Never inject intravenously or mix with intravenous solutions: inadvertent intravenous or intra-arterial injection has caused cardiorespiratory arrest, gangrene and death.', 'benzathine benzylpenicillin', 'StatPearls: Benzathine Penicillin; WHO Rheumatic heart disease fact sheet; AHA 2009 statement on prevention of rheumatic fever.', true)
on conflict (id) do nothing;
insert into public.medicine_facts (medicine_id, kind, content, position)
select * from (values
    ('med_benzathine_penicillin', 'brand_intl', 'Bicillin L-A', 0),
    ('med_benzathine_penicillin', 'indication', 'Secondary prophylaxis of rheumatic fever and rheumatic heart disease', 0),
    ('med_benzathine_penicillin', 'indication', 'Group A streptococcal pharyngitis (primary prevention of rheumatic fever)', 1),
    ('med_benzathine_penicillin', 'indication', 'Syphilis (primary, secondary and latent)', 2),
    ('med_benzathine_penicillin', 'indication', 'Yaws, bejel and pinta', 3),
    ('med_benzathine_penicillin', 'adverse', 'Pain and induration at the injection site (most common)', 0),
    ('med_benzathine_penicillin', 'adverse', 'Hypersensitivity reactions, including anaphylaxis', 1),
    ('med_benzathine_penicillin', 'adverse', 'Jarisch-Herxheimer reaction when treating syphilis', 2),
    ('med_benzathine_penicillin', 'adverse', 'Nerve or vascular injury if injected near a nerve or artery', 3),
    ('med_benzathine_penicillin', 'contraindication', 'Previous anaphylaxis or severe skin reaction to any penicillin', 0),
    ('med_benzathine_penicillin', 'contraindication', 'Intravenous administration (never)', 1),
    ('med_benzathine_penicillin', 'interaction', 'Probenecid: reduces kidney excretion and raises penicillin levels.', 0),
    ('med_benzathine_penicillin', 'interaction', 'Tetracyclines and other bacteriostatic antibiotics: may antagonise the bactericidal effect.', 1)
) v(medicine_id, kind, content, position)
where not exists (select 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin');

insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select * from (values
    ('med_benzathine_penicillin', 'Goodman & Gilman''s The Pharmacological Basis of Therapeutics', 'Brunton LL, Knollmann BC, eds. Goodman & Gilman''s The Pharmacological Basis of Therapeutics. 14th ed. New York: McGraw Hill; 2023.', '', true, 0),
    ('med_benzathine_penicillin', 'StatPearls - Benzathine Penicillin', 'Benzathine Penicillin. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.statpearls.com/sp/md/81/18217/', false, 1),
    ('med_benzathine_penicillin', 'WHO Fact Sheet - Rheumatic heart disease', 'World Health Organization. Rheumatic heart disease. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/rheumatic-heart-disease', false, 2),
    ('med_benzathine_penicillin', 'AHA Scientific Statement - Prevention of Rheumatic Fever (2009)', 'Gerber MA, Baltimore RS, Eaton CB, et al. Prevention of rheumatic fever and diagnosis and treatment of acute streptococcal pharyngitis. Circulation. 2009;119(11):1541-1551.', '', false, 3)
) v(medicine_id, source_name, citation_text, url, is_mother_book, position)
where not exists (select 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin');

-- ===================================================== Acute Appendicitis
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('acute_appendicitis', 'Acute Appendicitis', 'Acute inflammation of the vermiform appendix', 'Acute appendicitis is inflammation of the vermiform appendix, usually triggered by obstruction of its lumen. It is the most common cause of acute abdominal pain needing emergency surgery, with a lifetime risk of about 7-9% and a peak between ages 5 and 45. Untreated, the appendix can become gangrenous and perforate, causing abscess or generalised peritonitis, so early recognition and treatment matter.', 'sys_digest', 'Severe', 'EMERGENCY', 'Suspected appendicitis (abdominal pain migrating to the right lower quadrant with anorexia, nausea or fever) needs same-day emergency assessment for surgical evaluation. Signs of perforation or peritonitis (rigid abdomen, high fever, rapid pulse, low blood pressure) need immediate care.', false, 'Obstruction of the appendiceal lumen by an appendicolith (fecalith), lymphoid hyperplasia (most common in children), parasites or tumor raises intraluminal and wall pressure. Venous and lymphatic outflow are blocked, the appendix distends and becomes ischemic, and bacteria such as Escherichia coli, Bacteroides, Peptostreptococcus and Pseudomonas overgrow and invade the wall. Continued ischemia leads to necrosis and perforation, with localized abscess or diffuse peritonitis.', 'Early distension stimulates visceral afferents entering the spinal cord at T8-T10, so pain is first vague and periumbilical. When inflammation reaches the parietal peritoneum, pain localizes to the right lower quadrant over McBurney point, with guarding, rebound tenderness and Rovsing, psoas or Dunphy signs. Leukocytosis and raised CRP reflect the inflammatory response; very high WBC or CRP suggest complicated (gangrenous or perforated) disease.', 'After appendectomy, monitor pain control, temperature, wound and return of bowel function; uncomplicated cases usually recover within 24-48 hours and resume normal activity within 1-2 weeks. Persistent fever, ileus or worsening pain after surgery suggests intra-abdominal abscess and needs imaging. Patients treated with antibiotics alone need follow-up because about a quarter need appendectomy within a year, and older adults treated non-operatively should be assessed to exclude an underlying tumor.', 'StatPearls: Appendicitis (2024); WSES Jerusalem guidelines 2020; Schwartz''s Principles of Surgery, 11th ed.', 'Symptoms usually build over 12-24 hours: vague periumbilical pain, then anorexia and nausea or vomiting, then migration of pain to the right lower quadrant, often with low-grade fever. About 75% of patients present within 24 hours. The risk of rupture is about 2% at 36 hours and rises by about 5% for every further 12 hours without treatment.', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('acute_appendicitis', 0, 'Obstruction of the appendiceal lumen by an appendicolith (fecalith)'),
    ('acute_appendicitis', 1, 'Lymphoid hyperplasia, often after a viral or bacterial infection (most common cause in children)'),
    ('acute_appendicitis', 2, 'Parasites, foreign bodies or, rarely, tumors (carcinoid, adenocarcinoma, mucocele)'),
    ('acute_appendicitis', 3, 'Secondary bacterial invasion of the ischemic appendiceal wall (E. coli, Bacteroides and other gut flora)')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'acute_appendicitis');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('acute_appendicitis', 0, 'Age 5-45 years (mean age at presentation about 28)'),
    ('acute_appendicitis', 1, 'Male sex (slightly higher lifetime risk)'),
    ('acute_appendicitis', 2, 'Family history of appendicitis'),
    ('acute_appendicitis', 3, 'Recent gastrointestinal or respiratory infection (lymphoid hyperplasia)')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'acute_appendicitis');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('acute_appendicitis', 0, 'CBC with differential (leukocytosis in about two-thirds; WBC 17,000/mm3 or more suggests complicated appendicitis)'),
    ('acute_appendicitis', 1, 'C-reactive protein (normal WBC and CRP together make appendicitis unlikely)'),
    ('acute_appendicitis', 2, 'Urinalysis to look for urinary tract infection or stones'),
    ('acute_appendicitis', 3, 'Pregnancy test in all women of reproductive age'),
    ('acute_appendicitis', 4, 'Ultrasound of the right lower quadrant, first choice in children and pregnancy (appendix diameter over 6 mm, appendicolith)'),
    ('acute_appendicitis', 5, 'CT abdomen and pelvis with IV contrast, preferred in adults (over 95% accurate)'),
    ('acute_appendicitis', 6, 'Clinical scores such as the Alvarado score (7 or more points strongly supports appendicitis)')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'acute_appendicitis');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('acute_appendicitis', 0, 'Nil by mouth, IV crystalloid fluids and adequate analgesia (analgesia does not hide the diagnosis)'),
    ('acute_appendicitis', 1, 'IV antibiotics covering gut gram-negatives and anaerobes, e.g., a third-generation cephalosporin (ceftriaxone) plus metronidazole, adjusted to local resistance'),
    ('acute_appendicitis', 2, 'Appendectomy is the standard treatment; the laparoscopic approach is preferred (less wound infection and pain, shorter stay)'),
    ('acute_appendicitis', 3, 'Selected adults with uncomplicated, imaging-confirmed appendicitis may be treated with antibiotics alone after shared decision-making; about 1 in 4 later need surgery'),
    ('acute_appendicitis', 4, 'Periappendiceal abscess: percutaneous drainage and antibiotics, with interval appendectomy considered later'),
    ('acute_appendicitis', 5, 'Perforation with generalized peritonitis: urgent surgery, source control and a full antibiotic course')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'acute_appendicitis');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('acute_appendicitis', 0, 'Do not eat, drink or take laxatives or enemas while appendicitis is suspected; go to the emergency department'),
    ('acute_appendicitis', 1, 'Avoid heat packs on the abdomen and do not wait for the pain to settle'),
    ('acute_appendicitis', 2, 'After surgery, walk early, keep the wound clean and dry, and avoid heavy lifting for about 2 weeks (longer after open surgery)'),
    ('acute_appendicitis', 3, 'Finish the full antibiotic course if one was prescribed')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'acute_appendicitis');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('acute_appendicitis', 0, 'Severe, constant abdominal pain that worsens with movement or coughing'),
    ('acute_appendicitis', 1, 'Rigid, board-like abdomen'),
    ('acute_appendicitis', 2, 'High fever with chills'),
    ('acute_appendicitis', 3, 'Persistent vomiting or inability to keep fluids down'),
    ('acute_appendicitis', 4, 'Rapid heartbeat, low blood pressure, confusion or fainting (possible sepsis)'),
    ('acute_appendicitis', 5, 'Abdominal pain with a missed period or vaginal bleeding (rule out ectopic pregnancy)')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'acute_appendicitis');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('acute_appendicitis', 0, 'No proven way to prevent appendicitis; a fiber-rich diet has been associated with lower rates but is not a reliable preventive measure.', 'primary'::public.prevention_tier),
    ('acute_appendicitis', 1, 'Early assessment of migrating right lower quadrant pain, with clinical scoring, labs and imaging, so the diagnosis is made before perforation.', 'secondary'::public.prevention_tier),
    ('acute_appendicitis', 2, 'Prompt appendectomy or source control and appropriate antibiotics to prevent abscess, peritonitis, sepsis and death.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'acute_appendicitis');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('acute_appendicitis', 0, 'Mesenteric adenitis', 'Usually children with a recent viral illness; enlarged mesenteric nodes with a normal appendix on imaging'),
    ('acute_appendicitis', 1, 'Ectopic pregnancy', 'Positive pregnancy test, missed period, vaginal bleeding; may present with shock'),
    ('acute_appendicitis', 2, 'Ovarian torsion or ruptured ovarian cyst', 'Sudden severe unilateral pelvic pain; diagnosis by pelvic ultrasound'),
    ('acute_appendicitis', 3, 'Pelvic inflammatory disease', 'Bilateral lower abdominal pain, vaginal discharge, cervical motion tenderness'),
    ('acute_appendicitis', 4, 'Right ureteric stone / urinary tract infection', 'Colicky loin-to-groin pain, hematuria or pyuria; stone on imaging'),
    ('acute_appendicitis', 5, 'Acute gastroenteritis', 'Diarrhea and vomiting usually precede or accompany diffuse pain; no localized peritonism'),
    ('acute_appendicitis', 6, 'Crohn disease (terminal ileitis)', 'Chronic diarrhea, weight loss and recurrent pain; thickened terminal ileum on imaging')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'acute_appendicitis');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('acute_appendicitis', 'surgical emergency'),
    ('acute_appendicitis', 'acute abdomen'),
    ('acute_appendicitis', 'right lower quadrant'),
    ('acute_appendicitis', 'McBurney point'),
    ('acute_appendicitis', 'Alvarado score')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'acute_appendicitis');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('acute_appendicitis', 'sym_rlq_pain', 9::smallint, true, 1.5::numeric),
    ('acute_appendicitis', 'sym_abdominal_pain', 8::smallint, true, 1.1::numeric),
    ('acute_appendicitis', 'sym_anorexia', 6::smallint, false, 1.0::numeric),
    ('acute_appendicitis', 'sym_nausea_vomiting', 6::smallint, false, 0.9::numeric),
    ('acute_appendicitis', 'sym_fever', 4::smallint, false, 0.8::numeric),
    ('acute_appendicitis', 'sym_diarrhea', 2::smallint, false, 0.3::numeric),
    ('acute_appendicitis', 'sym_urinary_frequency', 2::smallint, false, 0.3::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'acute_appendicitis');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('acute_appendicitis', 'med_ceftriaxone', 0, 'safe'::public.condition_safety, 'Third-generation cephalosporin used IV with metronidazole for gram-negative and anaerobic cover (StatPearls, WSES).'),
    ('acute_appendicitis', 'med_metronidazole', 1, 'safe'::public.condition_safety, 'Adds anaerobic cover to ceftriaxone in appendicitis; avoid alcohol during and for 3 days after the course.'),
    ('acute_appendicitis', 'med_coamoxiclav', 2, 'safe'::public.condition_safety, 'Oral option to complete antibiotic therapy after complicated appendicitis, guided by local protocols.'),
    ('acute_appendicitis', 'med_paracetamol', 3, 'safe'::public.condition_safety, 'Early analgesia is recommended and does not mask the diagnosis; observe the maximum daily dose.'),
    ('acute_appendicitis', 'med_loperamide', 4, 'avoid'::public.condition_safety, 'Antimotility agents are inappropriate when an acute surgical abdomen is suspected and can delay diagnosis.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'acute_appendicitis');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_acute_appendicitis_1', 'acute_appendicitis', 0, 'Schwartz''s Principles of Surgery', 'Brunicardi FC, Andersen DK, Billiar TR, et al., eds. Schwartz''s Principles of Surgery. 11th ed. New York: McGraw Hill; 2019.', null, 'General Surgery', true),
    ('ref_acute_appendicitis_2', 'acute_appendicitis', 1, 'StatPearls - Appendicitis', 'Lotfollahzadeh S, Lopez RA, Deppen JG. Appendicitis. [Updated 2024 Feb 12]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026 Jan-.', 'https://www.ncbi.nlm.nih.gov/books/NBK493193/', 'General Surgery / Emergency Medicine', false),
    ('ref_acute_appendicitis_3', 'acute_appendicitis', 2, 'WSES Jerusalem guidelines - Acute appendicitis (2020)', 'Di Saverio S, Podda M, De Simone B, et al. Diagnosis and treatment of acute appendicitis: 2020 update of the WSES Jerusalem guidelines. World J Emerg Surg. 2020;15(1):27.', null, 'General Surgery', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'acute_appendicitis');

-- ===================================================== Gastroesophageal Reflux Disease (GERD)
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('gerd', 'Gastroesophageal Reflux Disease (GERD)', 'Gastroesophageal reflux disease', 'Gastroesophageal reflux disease (GERD) is a chronic condition in which stomach contents flow back into the esophagus often enough to cause troublesome symptoms or injury to the esophageal lining. It affects roughly one in five adults in Western populations. Most patients have non-erosive disease; others develop erosive esophagitis, peptic strictures or Barrett esophagus, a precursor of esophageal adenocarcinoma.', 'sys_digest', 'Mild', 'SELF_CARE', 'Typical heartburn and regurgitation without alarm features can be managed with lifestyle measures and short-term acid suppression, with medical review if symptoms persist beyond 2 weeks of OTC treatment. Alarm features (difficulty or pain on swallowing, weight loss, vomiting blood, black stools, anemia) need prompt medical evaluation and endoscopy. Chest pain needs cardiac causes excluded first.', false, 'The lower esophageal sphincter (LES) and the crural diaphragm normally form an anti-reflux barrier. GERD results mainly from transient LES relaxations not triggered by swallowing, a hypotensive LES, and hiatal hernia, which separates the LES from the crura. Obesity and pregnancy raise intra-abdominal pressure, while impaired esophageal peristalsis and delayed gastric emptying prolong acid contact. Acid, pepsin and sometimes bile injure the squamous epithelium, causing inflammation and, with chronic injury, metaplasia to columnar epithelium (Barrett esophagus).', 'Acid exposure of the distal esophagus produces heartburn, a retrosternal burning that rises toward the throat, and regurgitation of sour fluid, typically after meals or when lying down. Refluxate reaching the larynx and airways can cause chronic cough, hoarseness and asthma-like symptoms. Erosions graded by the Los Angeles classification (A-D) reflect mucosal injury, and fibrosis from chronic esophagitis can narrow the lumen into a peptic stricture that presents with dysphagia.', 'Review response after an 8-week once-daily PPI trial, then try to step down to the lowest effective dose or on-demand use if there is no erosive esophagitis or Barrett esophagus. Endoscopy is done for alarm features, lack of response, or recurrence, ideally after stopping PPIs for 2-4 weeks. Severe (LA grade C or D) esophagitis needs long-term maintenance therapy, and Barrett esophagus needs periodic surveillance endoscopy.', 'ACG Clinical Guideline for GERD (Katz et al., 2022); StatPearls: Gastroesophageal Reflux Disease; Harrison''s Principles of Internal Medicine, 21st ed.', 'Usually a chronic, relapsing course with intermittent symptoms over months to years, worse after large or fatty meals, alcohol, bending over and at night. Symptoms often respond within days to weeks of acid suppression but commonly recur after stopping treatment.', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('gerd', 0, 'Transient relaxations of the lower esophageal sphincter (most common mechanism)'),
    ('gerd', 1, 'Weak (hypotensive) lower esophageal sphincter'),
    ('gerd', 2, 'Hiatal hernia'),
    ('gerd', 3, 'Raised intra-abdominal pressure (obesity, pregnancy)'),
    ('gerd', 4, 'Impaired esophageal clearance and delayed gastric emptying')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'gerd');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('gerd', 0, 'Overweight or obesity'),
    ('gerd', 1, 'Large or late evening meals and lying down soon after eating'),
    ('gerd', 2, 'Smoking and excess alcohol'),
    ('gerd', 3, 'Pregnancy'),
    ('gerd', 4, 'Medicines that relax the LES or irritate the esophagus (NSAIDs, aspirin, calcium channel blockers, nitrates, anticholinergics, benzodiazepines)'),
    ('gerd', 5, 'Connective tissue disorders such as systemic sclerosis')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'gerd');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('gerd', 0, 'Clinical diagnosis with an 8-week empiric PPI trial for typical symptoms without alarm features'),
    ('gerd', 1, 'Upper endoscopy (EGD) for alarm features, non-response, Barrett risk factors or before long-term therapy decisions'),
    ('gerd', 2, 'Ambulatory esophageal pH or pH-impedance monitoring off PPI for refractory or atypical symptoms, and before anti-reflux surgery'),
    ('gerd', 3, 'Esophageal manometry before surgery to exclude achalasia and other motility disorders'),
    ('gerd', 4, 'ECG and cardiac evaluation when chest pain could be cardiac')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'gerd');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('gerd', 0, 'Lifestyle measures: weight loss if overweight, avoid meals within 2-3 hours of bedtime, elevate the head of the bed for nighttime symptoms, stop smoking, limit personal trigger foods'),
    ('gerd', 1, 'Proton pump inhibitor once daily 30-60 minutes before the first meal for 8 weeks, then step down to the lowest effective dose or on-demand use'),
    ('gerd', 2, 'H2-receptor antagonists (e.g., famotidine) for milder symptoms, on-demand use, or as a bedtime add-on for nighttime symptoms'),
    ('gerd', 3, 'Antacids for quick relief of mild, intermittent heartburn'),
    ('gerd', 4, 'Long-term PPI maintenance for LA grade C or D esophagitis or Barrett esophagus'),
    ('gerd', 5, 'Anti-reflux surgery (laparoscopic fundoplication) or magnetic sphincter augmentation for selected patients with confirmed, refractory or volume reflux')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'gerd');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('gerd', 0, 'Eat smaller meals and finish eating at least 2-3 hours before lying down'),
    ('gerd', 1, 'Raise the head of the bed by 15-20 cm (blocks under the bed legs) for nighttime symptoms'),
    ('gerd', 2, 'Lose weight if overweight and avoid tight belts or waistbands'),
    ('gerd', 3, 'Stop smoking and limit alcohol and personal trigger foods'),
    ('gerd', 4, 'Take PPIs before breakfast, not at bedtime, and do not use OTC acid reducers for more than 2 weeks without medical advice')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'gerd');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('gerd', 0, 'Chest pain with sweating, breathlessness or pain spreading to the arm or jaw (rule out heart attack)'),
    ('gerd', 1, 'Vomiting blood or material that looks like coffee grounds'),
    ('gerd', 2, 'Black, tarry stools'),
    ('gerd', 3, 'Food stuck in the throat or chest with inability to swallow saliva'),
    ('gerd', 4, 'Progressive difficulty swallowing with unintentional weight loss')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'gerd');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('gerd', 0, 'Healthy body weight, not smoking, moderate alcohol, and avoiding large late-night meals reduce reflux episodes.', 'primary'::public.prevention_tier),
    ('gerd', 1, 'Endoscopy for alarm features or long-standing symptoms with Barrett risk factors (older men, obesity, smoking, family history) to detect esophagitis, Barrett esophagus or cancer early.', 'secondary'::public.prevention_tier),
    ('gerd', 2, 'Maintenance acid suppression for severe esophagitis, dilation of strictures, and surveillance endoscopy in Barrett esophagus to prevent complications and detect dysplasia.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'gerd');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('gerd', 0, 'Acute coronary syndrome / stable angina', 'Exertional chest pain, risk factors, ECG and troponin changes; must be excluded first'),
    ('gerd', 1, 'Peptic ulcer disease', 'Epigastric pain related to meals, NSAID use or H. pylori; ulcer seen on endoscopy'),
    ('gerd', 2, 'Eosinophilic esophagitis', 'Young adults with atopy and food impaction; rings and furrows with eosinophils on biopsy'),
    ('gerd', 3, 'Achalasia', 'Dysphagia to solids and liquids with regurgitation of undigested food; diagnosed by manometry'),
    ('gerd', 4, 'Functional heartburn / dyspepsia', 'Typical symptoms with normal endoscopy and normal acid exposure on pH monitoring'),
    ('gerd', 5, 'Esophageal or gastric cancer', 'Older age, progressive dysphagia, weight loss and anemia')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'gerd');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('gerd', 'acid reflux'),
    ('gerd', 'heartburn'),
    ('gerd', 'PPI'),
    ('gerd', 'Barrett esophagus'),
    ('gerd', 'lifestyle')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'gerd');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('gerd', 'sym_heartburn', 8::smallint, true, 1.5::numeric),
    ('gerd', 'sym_regurgitation', 7::smallint, true, 1.4::numeric),
    ('gerd', 'sym_epigastric_pain', 4::smallint, false, 0.8::numeric),
    ('gerd', 'sym_chest_pain', 3::smallint, false, 0.5::numeric),
    ('gerd', 'sym_cough', 3::smallint, false, 0.5::numeric),
    ('gerd', 'sym_sore_throat', 2::smallint, false, 0.4::numeric),
    ('gerd', 'sym_dysphagia', 2::smallint, false, 0.6::numeric),
    ('gerd', 'sym_nausea_vomiting', 2::smallint, false, 0.4::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'gerd');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('gerd', 'med_omeprazole', 0, 'safe'::public.condition_safety, 'First-line PPI: once daily 30-60 minutes before breakfast for 8 weeks, then the lowest effective dose (ACG 2022).'),
    ('gerd', 'med_famotidine', 1, 'safe'::public.condition_safety, 'H2-receptor antagonist for milder or on-demand symptoms, or at bedtime for nighttime reflux; reduce the dose in kidney impairment.'),
    ('gerd', 'med_aluminium_magnesium_hydroxide', 2, 'safe'::public.condition_safety, 'Antacid for quick relief of mild, intermittent heartburn; separate from other oral medicines by 2 hours.'),
    ('gerd', 'med_ibuprofen', 3, 'caution'::public.condition_safety, 'NSAIDs can worsen reflux symptoms and esophageal injury; use the lowest dose for the shortest time or choose paracetamol.'),
    ('gerd', 'med_mefenamic_acid', 4, 'caution'::public.condition_safety, 'NSAID; can aggravate reflux and dyspepsia.'),
    ('gerd', 'med_aspirin', 5, 'caution'::public.condition_safety, 'Aspirin can injure the esophageal and gastric mucosa; do not stop prescribed cardiac aspirin without medical advice.'),
    ('gerd', 'med_amlodipine', 6, 'caution'::public.condition_safety, 'Calcium channel blockers lower LES pressure and may worsen reflux in some patients; do not stop without medical advice.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'gerd');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_gerd_1', 'gerd', 0, 'Harrison''s Principles of Internal Medicine', 'Loscalzo J, Fauci A, Kasper D, Hauser S, Longo D, Jameson JL, eds. Harrison''s Principles of Internal Medicine, 21st ed. New York: McGraw Hill; 2022.', null, 'Internal Medicine', true),
    ('ref_gerd_2', 'gerd', 1, 'ACG Clinical Guideline - Diagnosis and Management of GERD (2022)', 'Katz PO, Dunbar KB, Schnoll-Sussman FH, Greer KB, Yadlapati R, Spechler SJ. ACG Clinical Guideline for the Diagnosis and Management of Gastroesophageal Reflux Disease. Am J Gastroenterol. 2022;117(1):27-56.', null, 'Gastroenterology', false),
    ('ref_gerd_3', 'gerd', 2, 'StatPearls - Gastroesophageal Reflux Disease', 'Antunes C, Aleem A, Curtis SA. Gastroesophageal Reflux Disease. [Updated 2023 Jul 3]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK441938/', 'Gastroenterology', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'gerd');

-- ===================================================== Iron-Deficiency Anemia
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('iron_deficiency_anemia', 'Iron-Deficiency Anemia', 'Microcytic hypochromic anemia due to iron deficiency', 'Iron-deficiency anemia is a reduction in hemoglobin caused by too little iron for red cell production. It is the most common cause of anemia worldwide and is especially frequent in young children, adolescent girls, women of reproductive age and pregnant women. It results from inadequate intake, poor absorption or chronic blood loss, so the underlying cause must always be found, particularly gastrointestinal bleeding in men and postmenopausal women.', 'bs_hematologic', 'Moderate', 'SEE_DOCTOR_SOON', 'Suspected anemia (fatigue, pallor, breathlessness on exertion) warrants a CBC and ferritin and a search for the cause, especially in men, postmenopausal women and anyone with gastrointestinal symptoms. Chest pain, breathlessness at rest, fainting, or ongoing heavy bleeding need emergency care.', false, 'When iron loss or demand exceeds absorption, iron stores (ferritin) are used up first. Serum iron and transferrin saturation then fall and total iron-binding capacity rises. Iron-starved erythroblasts make less hemoglobin and divide more, producing small (microcytic), pale (hypochromic) red cells of varying size (raised RDW). Hepcidin is suppressed, maximising intestinal iron absorption. Iron is also needed by tissue enzymes, explaining epithelial changes and neurocognitive effects even before anemia develops.', 'Reduced oxygen-carrying capacity causes fatigue, exertional breathlessness, palpitations, dizziness and pallor, with compensatory tachycardia and sometimes a flow murmur. Depletion of iron-dependent epithelial enzymes produces glossitis, angular cheilitis and koilonychia, and rarely an esophageal web (Plummer-Vinson syndrome). Pica, particularly craving ice, and restless legs are characteristic. Laboratory findings are low hemoglobin, low MCV and MCH, high RDW and, most specifically, low ferritin.', 'Recheck hemoglobin about 2-4 weeks after starting oral iron; a rise of about 1-2 g/dL within a month indicates response. Continue iron for about 3 months after correction to refill stores, then check ferritin. No response suggests non-adherence, malabsorption (e.g., celiac disease, H. pylori, atrophic gastritis), ongoing blood loss or a wrong diagnosis, and calls for further investigation or IV iron. Monitor high-risk groups (pregnancy, heavy menstrual bleeding, CKD) periodically.', 'StatPearls: Iron-Deficiency Anemia (2026); WHO Guideline on haemoglobin cutoffs (2024); Harrison''s Principles of Internal Medicine, 21st ed.', 'Develops gradually over weeks to months, so many people adapt and have few symptoms until hemoglobin is quite low. Iron stores are depleted before anemia appears. Acute blood loss can cause rapid symptoms.', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('iron_deficiency_anemia', 0, 'Chronic blood loss: heavy menstrual bleeding, gastrointestinal bleeding (peptic ulcer, NSAIDs, colorectal cancer, angiodysplasia)'),
    ('iron_deficiency_anemia', 1, 'Increased demand: pregnancy, infancy, rapid growth in adolescence'),
    ('iron_deficiency_anemia', 2, 'Inadequate dietary intake (low intake of meat and iron-rich foods)'),
    ('iron_deficiency_anemia', 3, 'Reduced absorption: celiac disease, atrophic gastritis, H. pylori infection, gastric or bariatric surgery'),
    ('iron_deficiency_anemia', 4, 'Hookworm and other intestinal parasites, and schistosomiasis in endemic areas'),
    ('iron_deficiency_anemia', 5, 'Frequent blood donation')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'iron_deficiency_anemia');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('iron_deficiency_anemia', 0, 'Women of reproductive age and pregnancy'),
    ('iron_deficiency_anemia', 1, 'Infants and toddlers, especially with early cow''s milk'),
    ('iron_deficiency_anemia', 2, 'Adolescent girls'),
    ('iron_deficiency_anemia', 3, 'Vegetarian or low-meat diets'),
    ('iron_deficiency_anemia', 4, 'Long-term NSAID, aspirin or anticoagulant use'),
    ('iron_deficiency_anemia', 5, 'Chronic kidney disease and heart failure'),
    ('iron_deficiency_anemia', 6, 'Living in areas with poor sanitation and soil-transmitted helminths')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'iron_deficiency_anemia');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('iron_deficiency_anemia', 0, 'CBC: low hemoglobin (WHO anemia cutoffs, e.g., below 13 g/dL in men and 12 g/dL in non-pregnant women), low MCV and MCH, raised RDW'),
    ('iron_deficiency_anemia', 1, 'Serum ferritin, the most useful single test (below 45 ng/mL supports iron deficiency per AGA/ASH; ferritin is falsely raised by inflammation)'),
    ('iron_deficiency_anemia', 2, 'Serum iron, total iron-binding capacity and transferrin saturation (low saturation, high TIBC)'),
    ('iron_deficiency_anemia', 3, 'Peripheral blood smear (microcytic, hypochromic cells, pencil cells) and reticulocyte count'),
    ('iron_deficiency_anemia', 4, 'Search for the cause: stool tests for occult blood and parasites, celiac serology, H. pylori testing'),
    ('iron_deficiency_anemia', 5, 'Upper endoscopy and colonoscopy in men and postmenopausal women without an obvious cause')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'iron_deficiency_anemia');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('iron_deficiency_anemia', 0, 'Treat the underlying cause (e.g., heavy menses, ulcer, NSAID use, parasites); iron alone fails if losses continue'),
    ('iron_deficiency_anemia', 1, 'Oral iron (e.g., ferrous sulfate) first line; once-daily or alternate-day dosing improves tolerance and absorption'),
    ('iron_deficiency_anemia', 2, 'Continue oral iron for about 3 months after hemoglobin normalises to replenish stores'),
    ('iron_deficiency_anemia', 3, 'IV iron for intolerance or failure of oral iron, malabsorption, chronic inflammatory disease (CKD, IBD), ongoing losses or need for rapid repletion (late pregnancy, before surgery)'),
    ('iron_deficiency_anemia', 4, 'Red cell transfusion only for severe, symptomatic anemia with hemodynamic instability or active bleeding'),
    ('iron_deficiency_anemia', 5, 'Deworming (e.g., albendazole) where intestinal helminths are the cause')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'iron_deficiency_anemia');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('iron_deficiency_anemia', 0, 'Take iron on an empty stomach if tolerated, or with a small meal if it upsets the stomach'),
    ('iron_deficiency_anemia', 1, 'Take iron with vitamin C-rich foods or juice; avoid tea, coffee, milk and antacids within 2 hours of the dose'),
    ('iron_deficiency_anemia', 2, 'Expect dark or black stools; seek care if stools are tarry with abdominal pain or dizziness'),
    ('iron_deficiency_anemia', 3, 'Eat iron-rich foods: meat, liver, fish, legumes (monggo), dark green leafy vegetables (malunggay, kangkong) and iron-fortified foods'),
    ('iron_deficiency_anemia', 4, 'Keep iron tablets locked away from children; overdose is dangerous')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'iron_deficiency_anemia');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('iron_deficiency_anemia', 0, 'Chest pain or breathlessness at rest'),
    ('iron_deficiency_anemia', 1, 'Fainting or near-fainting'),
    ('iron_deficiency_anemia', 2, 'Vomiting blood or passing black, tarry or bloody stools'),
    ('iron_deficiency_anemia', 3, 'Very heavy menstrual bleeding soaking a pad every hour'),
    ('iron_deficiency_anemia', 4, 'Rapid heartbeat with confusion or cold, clammy skin')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'iron_deficiency_anemia');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('iron_deficiency_anemia', 0, 'Iron-rich and fortified foods, delayed cord clamping, iron supplementation in pregnancy and for at-risk infants, and deworming in endemic areas.', 'primary'::public.prevention_tier),
    ('iron_deficiency_anemia', 1, 'Screening high-risk groups (pregnant women, infants at 9-12 months, adolescent girls) with hemoglobin and ferritin, and investigating the cause of any iron deficiency.', 'secondary'::public.prevention_tier),
    ('iron_deficiency_anemia', 2, 'Adequate iron repletion with follow-up of hemoglobin and ferritin, and treatment of the bleeding source, to prevent relapse, heart strain and impaired child development.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'iron_deficiency_anemia');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('iron_deficiency_anemia', 0, 'Thalassemia trait', 'Microcytosis with normal or high ferritin, high RBC count, normal RDW; Mentzer index below 13; hemoglobin electrophoresis'),
    ('iron_deficiency_anemia', 1, 'Anemia of chronic disease (inflammation)', 'Chronic inflammatory illness; normal or high ferritin, low TIBC'),
    ('iron_deficiency_anemia', 2, 'Sideroblastic anemia', 'Ring sideroblasts on bone marrow; often alcohol, lead or isoniazid related'),
    ('iron_deficiency_anemia', 3, 'Lead poisoning', 'Basophilic stippling, abdominal pain, neurologic symptoms; raised blood lead'),
    ('iron_deficiency_anemia', 4, 'Anemia of chronic kidney disease', 'Reduced eGFR; normocytic anemia from low erythropoietin, often with coexisting iron deficiency')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'iron_deficiency_anemia');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('iron_deficiency_anemia', 'anemia'),
    ('iron_deficiency_anemia', 'microcytic'),
    ('iron_deficiency_anemia', 'ferritin'),
    ('iron_deficiency_anemia', 'women''s health'),
    ('iron_deficiency_anemia', 'nutrition')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'iron_deficiency_anemia');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('iron_deficiency_anemia', 'sym_fatigue', 8::smallint, true, 1.0::numeric),
    ('iron_deficiency_anemia', 'sym_pallor', 7::smallint, true, 1.4::numeric),
    ('iron_deficiency_anemia', 'sym_dyspnea', 4::smallint, false, 0.7::numeric),
    ('iron_deficiency_anemia', 'sym_palpitations', 4::smallint, false, 0.7::numeric),
    ('iron_deficiency_anemia', 'sym_dizziness', 4::smallint, false, 0.6::numeric),
    ('iron_deficiency_anemia', 'sym_headache', 3::smallint, false, 0.4::numeric),
    ('iron_deficiency_anemia', 'sym_pica', 3::smallint, false, 1.3::numeric),
    ('iron_deficiency_anemia', 'sym_koilonychia', 2::smallint, false, 1.3::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'iron_deficiency_anemia');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('iron_deficiency_anemia', 'med_ferrous_sulfate', 0, 'safe'::public.condition_safety, 'First-line oral iron; about 3 months of treatment is needed to refill stores after hemoglobin normalises.'),
    ('iron_deficiency_anemia', 'med_omeprazole', 1, 'caution'::public.condition_safety, 'Long-term acid suppression reduces dietary and oral iron absorption; review the need for a PPI.'),
    ('iron_deficiency_anemia', 'med_aluminium_magnesium_hydroxide', 2, 'caution'::public.condition_safety, 'Antacids reduce oral iron absorption; separate doses by at least 2 hours.'),
    ('iron_deficiency_anemia', 'med_ibuprofen', 3, 'caution'::public.condition_safety, 'NSAIDs can cause gastrointestinal blood loss that worsens iron deficiency.'),
    ('iron_deficiency_anemia', 'med_aspirin', 4, 'caution'::public.condition_safety, 'Gastrointestinal bleeding risk; review the indication, but do not stop prescribed cardiac aspirin without advice.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'iron_deficiency_anemia');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_iron_deficiency_anemia_1', 'iron_deficiency_anemia', 0, 'Harrison''s Principles of Internal Medicine', 'Loscalzo J, Fauci A, Kasper D, Hauser S, Longo D, Jameson JL, eds. Harrison''s Principles of Internal Medicine, 21st ed. New York: McGraw Hill; 2022.', null, 'Internal Medicine', true),
    ('ref_iron_deficiency_anemia_2', 'iron_deficiency_anemia', 1, 'StatPearls - Iron-Deficiency Anemia', 'Jogu P, Kamran MT. Iron-Deficiency Anemia. [Updated 2026 Feb 15]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026 Jan-.', 'https://www.ncbi.nlm.nih.gov/books/NBK448065/', 'Hematology', false),
    ('ref_iron_deficiency_anemia_3', 'iron_deficiency_anemia', 2, 'WHO Guideline - Haemoglobin cutoffs to define anaemia (2024)', 'World Health Organization. Guideline on haemoglobin cutoffs to define anaemia in individuals and populations. Geneva: WHO; 2024.', null, 'Hematology / Public Health', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'iron_deficiency_anemia');

-- ===================================================== Chronic Kidney Disease
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('chronic_kidney_disease', 'Chronic Kidney Disease', 'Chronic kidney disease (CKD)', 'Chronic kidney disease is kidney damage or a reduced glomerular filtration rate (eGFR below 60 mL/min/1.73 m2) lasting more than 3 months, regardless of cause. It is staged by eGFR (G1-G5) and albuminuria (A1-A3). Diabetes and hypertension are the leading causes. CKD is usually silent until advanced, raises cardiovascular risk sharply, and can progress to kidney failure needing dialysis or transplantation.', 'sys_renal', 'Severe', 'SEE_DOCTOR_SOON', 'People with diabetes, hypertension or other risk factors should have regular eGFR and urine albumin testing; newly reduced eGFR or albuminuria needs medical review. Shortness of breath, chest pain, confusion, very low urine output, severe vomiting or muscle weakness (possible hyperkalemia, fluid overload or uremia) need emergency care.', false, 'Diabetic, hypertensive, glomerular, cystic or obstructive injury reduces the number of functioning nephrons. Remaining nephrons hyperfilter through glomerular hypertension and hypertrophy, which, together with proteinuria and angiotensin II-driven inflammation, causes progressive glomerulosclerosis, tubulointerstitial fibrosis and vascular sclerosis. Falling filtration leads to retention of urea and other uremic toxins, salt and water, potassium, phosphate and acid, and reduced production of erythropoietin and active vitamin D.', 'Early stages are usually asymptomatic and detected by a reduced eGFR or albuminuria (foamy urine). Salt and water retention cause hypertension and edema; loss of concentrating ability causes nocturia. Low erythropoietin causes normocytic anemia, phosphate retention and low calcitriol drive secondary hyperparathyroidism and mineral bone disorder, and accumulation of uremic toxins causes anorexia, nausea, itching, cramps, fatigue and, in advanced disease, pericarditis, encephalopathy and bleeding.', 'Monitor eGFR and urine albumin-creatinine ratio at a frequency set by the CKD stage and albuminuria category (at least yearly, more often in advanced stages), together with blood pressure, potassium, bicarbonate, hemoglobin, calcium, phosphate and PTH. Check potassium and creatinine 2-4 weeks after starting or increasing RAS inhibitors. Adjust drug doses to eGFR, refer to nephrology for eGFR below 30, rapid decline or heavy albuminuria, and plan dialysis access and transplant evaluation early.', 'KDIGO 2024 CKD Guideline; StatPearls: Chronic Kidney Disease (2024); Harrison''s Principles of Internal Medicine, 21st ed.', 'Slowly progressive over months to years, often over decades in diabetes and hypertension. Symptoms usually appear only in stages G4-G5. Acute illness, dehydration, NSAIDs or contrast can cause sudden worsening (acute-on-chronic kidney injury).', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('chronic_kidney_disease', 0, 'Diabetic kidney disease (leading cause)'),
    ('chronic_kidney_disease', 1, 'Hypertensive nephrosclerosis'),
    ('chronic_kidney_disease', 2, 'Chronic glomerulonephritis (e.g., IgA nephropathy, lupus nephritis)'),
    ('chronic_kidney_disease', 3, 'Polycystic kidney disease and other inherited diseases'),
    ('chronic_kidney_disease', 4, 'Chronic obstruction (stones, prostatic enlargement) and recurrent pyelonephritis or reflux nephropathy'),
    ('chronic_kidney_disease', 5, 'Nephrotoxic medicines and chronic NSAID use')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'chronic_kidney_disease');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('chronic_kidney_disease', 0, 'Diabetes mellitus'),
    ('chronic_kidney_disease', 1, 'Hypertension'),
    ('chronic_kidney_disease', 2, 'Obesity and metabolic syndrome'),
    ('chronic_kidney_disease', 3, 'Age over 60'),
    ('chronic_kidney_disease', 4, 'Family history of kidney disease'),
    ('chronic_kidney_disease', 5, 'Smoking'),
    ('chronic_kidney_disease', 6, 'Cardiovascular disease'),
    ('chronic_kidney_disease', 7, 'History of acute kidney injury'),
    ('chronic_kidney_disease', 8, 'Recurrent urinary tract infections or kidney stones')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'chronic_kidney_disease');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('chronic_kidney_disease', 0, 'Serum creatinine with eGFR (CKD-EPI equation), repeated to confirm chronicity over more than 3 months'),
    ('chronic_kidney_disease', 1, 'Urine albumin-creatinine ratio (UACR) on an early-morning sample, and urinalysis for blood and casts'),
    ('chronic_kidney_disease', 2, 'Serum electrolytes (potassium, bicarbonate), calcium, phosphate, PTH and vitamin D'),
    ('chronic_kidney_disease', 3, 'CBC for anemia and iron studies'),
    ('chronic_kidney_disease', 4, 'Kidney ultrasound (size, cortical thinning, cysts, obstruction)'),
    ('chronic_kidney_disease', 5, 'Kidney biopsy when the cause is unclear, e.g., suspected glomerulonephritis')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'chronic_kidney_disease');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('chronic_kidney_disease', 0, 'Treat the cause and risk factors: glucose control in diabetes, blood pressure control (KDIGO suggests systolic below 120 mmHg when tolerated)'),
    ('chronic_kidney_disease', 1, 'ACE inhibitor or ARB at the maximum tolerated dose for albuminuric CKD, with potassium and creatinine monitoring'),
    ('chronic_kidney_disease', 2, 'SGLT2 inhibitor (e.g., dapagliflozin) for CKD with type 2 diabetes and eGFR 20 or above, and for CKD with significant albuminuria or heart failure (KDIGO 2024)'),
    ('chronic_kidney_disease', 3, 'Statin therapy for cardiovascular risk reduction in adults with CKD'),
    ('chronic_kidney_disease', 4, 'Dietary sodium below 2 g per day, protein intake guided by a dietitian, and avoidance of NSAIDs and other nephrotoxins'),
    ('chronic_kidney_disease', 5, 'Manage complications: loop diuretics for fluid overload, bicarbonate for metabolic acidosis, phosphate binders and vitamin D analogues for mineral bone disease, iron and erythropoiesis-stimulating agents for anemia'),
    ('chronic_kidney_disease', 6, 'Kidney replacement therapy (hemodialysis, peritoneal dialysis) or kidney transplantation for kidney failure; conservative care for those who decline dialysis')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'chronic_kidney_disease');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('chronic_kidney_disease', 0, 'Take blood pressure and diabetes medicines as prescribed and keep a home blood pressure log'),
    ('chronic_kidney_disease', 1, 'Limit salt, processed and canned foods; follow dietitian advice on protein, potassium and phosphate'),
    ('chronic_kidney_disease', 2, 'Avoid painkillers such as ibuprofen and mefenamic acid and unprescribed herbal products; ask before taking any new medicine'),
    ('chronic_kidney_disease', 3, 'Stay active, stop smoking and keep a healthy weight'),
    ('chronic_kidney_disease', 4, 'Weigh yourself regularly and report rapid weight gain or swelling')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'chronic_kidney_disease');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('chronic_kidney_disease', 0, 'Shortness of breath, especially when lying flat'),
    ('chronic_kidney_disease', 1, 'Chest pain (possible pericarditis or heart disease)'),
    ('chronic_kidney_disease', 2, 'Confusion, drowsiness or seizures'),
    ('chronic_kidney_disease', 3, 'Very little or no urine'),
    ('chronic_kidney_disease', 4, 'Muscle weakness or palpitations (possible high potassium)'),
    ('chronic_kidney_disease', 5, 'Persistent vomiting and inability to keep medicines down')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'chronic_kidney_disease');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('chronic_kidney_disease', 0, 'Control of diabetes, blood pressure and weight, not smoking, and avoiding unnecessary NSAIDs and nephrotoxic remedies.', 'primary'::public.prevention_tier),
    ('chronic_kidney_disease', 1, 'Screening people with diabetes, hypertension, cardiovascular disease or a family history with eGFR and urine albumin, so CKD is found and treated early.', 'secondary'::public.prevention_tier),
    ('chronic_kidney_disease', 2, 'RAS inhibitors, SGLT2 inhibitors, complication management and timely dialysis or transplant planning to slow progression and prevent cardiovascular events.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'chronic_kidney_disease');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('chronic_kidney_disease', 0, 'Acute kidney injury', 'Rise in creatinine over hours to days; normal-sized kidneys; usually a clear precipitant and potential recovery'),
    ('chronic_kidney_disease', 1, 'Nephrotic syndrome', 'Heavy proteinuria above 3.5 g/day, hypoalbuminemia, edema and hyperlipidemia'),
    ('chronic_kidney_disease', 2, 'Heart failure (cardiorenal syndrome)', 'Edema and breathlessness from cardiac dysfunction; raised natriuretic peptides; reduced ejection fraction on echo'),
    ('chronic_kidney_disease', 3, 'Obstructive uropathy', 'Hydronephrosis on ultrasound; prostatic enlargement or stones; may improve after relief of obstruction')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'chronic_kidney_disease');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('chronic_kidney_disease', 'kidney failure'),
    ('chronic_kidney_disease', 'eGFR'),
    ('chronic_kidney_disease', 'albuminuria'),
    ('chronic_kidney_disease', 'dialysis'),
    ('chronic_kidney_disease', 'diabetes complication')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'chronic_kidney_disease');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('chronic_kidney_disease', 'sym_edema', 6::smallint, true, 1.0::numeric),
    ('chronic_kidney_disease', 'sym_foamy_urine', 5::smallint, true, 1.2::numeric),
    ('chronic_kidney_disease', 'sym_fatigue', 6::smallint, false, 0.7::numeric),
    ('chronic_kidney_disease', 'sym_pruritus', 5::smallint, false, 1.0::numeric),
    ('chronic_kidney_disease', 'sym_nocturia', 4::smallint, false, 1.0::numeric),
    ('chronic_kidney_disease', 'sym_decreased_urine', 4::smallint, false, 1.0::numeric),
    ('chronic_kidney_disease', 'sym_nausea_vomiting', 5::smallint, false, 0.7::numeric),
    ('chronic_kidney_disease', 'sym_anorexia', 5::smallint, false, 0.6::numeric),
    ('chronic_kidney_disease', 'sym_muscle_cramps', 4::smallint, false, 0.8::numeric),
    ('chronic_kidney_disease', 'sym_dyspnea', 4::smallint, false, 0.6::numeric),
    ('chronic_kidney_disease', 'sym_pallor', 4::smallint, false, 0.6::numeric),
    ('chronic_kidney_disease', 'sym_confusion', 2::smallint, false, 0.5::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'chronic_kidney_disease');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('chronic_kidney_disease', 'med_losartan', 0, 'safe'::public.condition_safety, 'ARB to lower blood pressure and albuminuria; check potassium and creatinine 2-4 weeks after starting or dose changes.'),
    ('chronic_kidney_disease', 'med_enalapril', 1, 'safe'::public.condition_safety, 'ACE inhibitor alternative to an ARB; do not combine with an ARB. Teratogenic.'),
    ('chronic_kidney_disease', 'med_dapagliflozin', 2, 'safe'::public.condition_safety, 'SGLT2 inhibitor that slows CKD progression and reduces heart failure events (KDIGO 2024: start at eGFR 20 or above).'),
    ('chronic_kidney_disease', 'med_atorvastatin', 3, 'safe'::public.condition_safety, 'Statin for cardiovascular risk reduction in adults with CKD not on dialysis.'),
    ('chronic_kidney_disease', 'med_furosemide', 4, 'safe'::public.condition_safety, 'Loop diuretic for edema and fluid overload; remains effective at low eGFR.'),
    ('chronic_kidney_disease', 'med_amlodipine', 5, 'safe'::public.condition_safety, 'Calcium channel blocker often added to reach blood pressure targets; no dose change needed for kidney function.'),
    ('chronic_kidney_disease', 'med_metformin', 6, 'caution'::public.condition_safety, 'Review dose: reduce at eGFR 30-44 and stop below 30 because of lactic acidosis risk.'),
    ('chronic_kidney_disease', 'med_nitrofurantoin', 7, 'caution'::public.condition_safety, 'Less effective and more toxic with reduced kidney function; avoid when eGFR is below 30.'),
    ('chronic_kidney_disease', 'med_aluminium_magnesium_hydroxide', 8, 'avoid'::public.condition_safety, 'Aluminium and magnesium accumulate in advanced CKD; avoid regular use.'),
    ('chronic_kidney_disease', 'med_ibuprofen', 9, 'avoid'::public.condition_safety, 'NSAIDs reduce kidney blood flow, raise blood pressure and potassium, and can precipitate acute kidney injury.'),
    ('chronic_kidney_disease', 'med_mefenamic_acid', 10, 'avoid'::public.condition_safety, 'NSAID; nephrotoxic risk in CKD.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_chronic_kidney_disease_1', 'chronic_kidney_disease', 0, 'Harrison''s Principles of Internal Medicine', 'Loscalzo J, Fauci A, Kasper D, Hauser S, Longo D, Jameson JL, eds. Harrison''s Principles of Internal Medicine, 21st ed. New York: McGraw Hill; 2022.', null, 'Internal Medicine', true),
    ('ref_chronic_kidney_disease_2', 'chronic_kidney_disease', 1, 'KDIGO 2024 Clinical Practice Guideline - Chronic Kidney Disease', 'Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group. KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease. Kidney Int. 2024;105(4S):S117-S314.', null, 'Nephrology', false),
    ('ref_chronic_kidney_disease_3', 'chronic_kidney_disease', 2, 'StatPearls - Chronic Kidney Disease', 'Vaidya SR, Aeddula NR. Chronic Kidney Disease. [Updated 2024 Jul 31]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing.', 'https://www.ncbi.nlm.nih.gov/books/NBK535404/', 'Nephrology', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'chronic_kidney_disease');

-- ===================================================== Acute Rheumatic Fever and Rheumatic Heart Disease
insert into public.diseases (id, name, scientific_name, description, body_system_id, severity, urgency, urgency_criteria, contagious, pathophysiology, clinicopathologic_correlation, follow_up_monitoring, source_attribution, onset_progression, is_published)
values ('rheumatic_fever', 'Acute Rheumatic Fever and Rheumatic Heart Disease', 'Post-streptococcal (group A Streptococcus) inflammatory disease', 'Acute rheumatic fever (ARF) is an autoimmune inflammatory illness that follows untreated group A streptococcal throat infection, mainly in children aged 5-15 in low- and middle-income settings. It affects the heart, joints, brain and skin. Repeated or severe attacks permanently scar the heart valves, causing rheumatic heart disease (RHD), which WHO estimates affects about 55 million people and causes about 360,000 deaths a year. It is preventable with prompt treatment of strep throat and long-term penicillin prophylaxis.', 'sys_cardio', 'Severe', 'SEE_DOCTOR_SOON', 'A child or young person with fever and migrating joint pain or swelling, new chorea, or a new heart murmur weeks after a sore throat needs prompt medical assessment, including echocardiography. Breathlessness, chest pain, leg swelling or palpitations (possible carditis or heart failure) need urgent care. Sore throats in children should be assessed and streptococcal pharyngitis treated with antibiotics.', false, 'Group A Streptococcus (Streptococcus pyogenes) pharyngitis triggers antibodies and T cells against the M protein and other antigens that cross-react with host tissues such as cardiac myosin, valve glycoproteins, synovium and basal ganglia neurons (molecular mimicry). The result is a pancarditis, most importantly valvulitis of the mitral and aortic valves, a transient arthritis, and neuronal dysfunction causing chorea. Aschoff bodies are characteristic. Recurrent attacks and chronic inflammation lead to valve fibrosis, commissural fusion and calcification, producing regurgitation and later stenosis, classically mitral stenosis.', 'Symptoms begin about 2-4 weeks after the sore throat. Arthritis is typically a painful, migratory polyarthritis of large joints that responds dramatically to salicylates. Carditis presents with new murmurs of mitral or aortic regurgitation, tachycardia, pericarditis or heart failure, and subclinical valvulitis may only be seen on echocardiography. Sydenham chorea may appear months later. Erythema marginatum and painless subcutaneous nodules over bony prominences are rare but specific. Raised ESR and CRP, a prolonged PR interval and raised antistreptococcal antibodies support the diagnosis (revised Jones criteria, 2015).', 'Echocardiography at diagnosis and during follow-up to grade valve disease. Secondary prophylaxis with benzathine penicillin G every 3-4 weeks: typically for 5 years or until age 21 (whichever is longer) without carditis, 10 years or until 21 with carditis but no residual valve disease, and 10 years or until age 40 (sometimes lifelong) with residual valve disease. Regular cardiology review, dental care, and anticoagulation monitoring for atrial fibrillation or mechanical valves; pregnancy needs specialist care.', 'WHO Rheumatic heart disease fact sheet; AHA revision of the Jones criteria (2015); AHA statement on prevention of rheumatic fever (2009); Harrison''s Principles of Internal Medicine, 21st ed.', 'Acute onset about 2-4 weeks after streptococcal pharyngitis; chorea can appear 1-8 months after the infection. Arthritis and fever settle within weeks, but carditis can leave permanent valve damage. Each recurrence worsens valve injury, and symptoms of chronic RHD (breathlessness, palpitations, atrial fibrillation, heart failure) often develop years to decades later, frequently first noticed in pregnancy.', true)
on conflict (id) do nothing;
insert into public.disease_causes (disease_id, position, content)
select * from (values
    ('rheumatic_fever', 0, 'Autoimmune reaction to group A Streptococcus (Streptococcus pyogenes) pharyngitis'),
    ('rheumatic_fever', 1, 'Molecular mimicry between streptococcal M protein and heart, joint, brain and skin tissue'),
    ('rheumatic_fever', 2, 'Recurrent streptococcal infections causing recurrent attacks and progressive valve damage')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_causes where disease_id = 'rheumatic_fever');

insert into public.disease_risk_factors (disease_id, position, content)
select * from (values
    ('rheumatic_fever', 0, 'Age 5-15 years'),
    ('rheumatic_fever', 1, 'Untreated or incompletely treated strep throat'),
    ('rheumatic_fever', 2, 'Household overcrowding and poverty'),
    ('rheumatic_fever', 3, 'Limited access to health care and antibiotics'),
    ('rheumatic_fever', 4, 'Previous episode of rheumatic fever (high risk of recurrence)'),
    ('rheumatic_fever', 5, 'Genetic susceptibility and family history')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_risk_factors where disease_id = 'rheumatic_fever');

insert into public.disease_recommended_tests (disease_id, position, content)
select * from (values
    ('rheumatic_fever', 0, 'Evidence of preceding group A strep infection: raised or rising ASO or anti-DNase B titers, positive throat culture or rapid antigen test'),
    ('rheumatic_fever', 1, 'ESR and CRP (inflammatory markers; minor Jones criteria)'),
    ('rheumatic_fever', 2, 'ECG for a prolonged PR interval, heart block or arrhythmia'),
    ('rheumatic_fever', 3, 'Echocardiography with Doppler in all suspected cases, to detect clinical and subclinical carditis'),
    ('rheumatic_fever', 4, 'CBC, and chest X-ray if heart failure is suspected'),
    ('rheumatic_fever', 5, 'Diagnosis by the revised Jones criteria (2015): 2 major, or 1 major plus 2 minor criteria, with evidence of strep infection')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_recommended_tests where disease_id = 'rheumatic_fever');

insert into public.disease_treatments (disease_id, position, content)
select * from (values
    ('rheumatic_fever', 0, 'Eradicate streptococci: benzathine penicillin G as a single IM injection, or 10 days of oral penicillin or amoxicillin (erythromycin if allergic)'),
    ('rheumatic_fever', 1, 'Anti-inflammatory therapy for arthritis and mild carditis: high-dose aspirin (or naproxen) for 2-6 weeks, tapered as inflammation settles'),
    ('rheumatic_fever', 2, 'Corticosteroids (e.g., prednisone) are sometimes used for severe carditis with heart failure, although evidence of long-term benefit is limited'),
    ('rheumatic_fever', 3, 'Heart failure treatment: bed rest, diuretics, ACE inhibitors and fluid restriction; urgent valve surgery for severe acute valve dysfunction'),
    ('rheumatic_fever', 4, 'Sydenham chorea: a calm environment; medicines such as carbamazepine or valproate for severe chorea'),
    ('rheumatic_fever', 5, 'Begin secondary prophylaxis with benzathine penicillin G every 3-4 weeks immediately after diagnosis'),
    ('rheumatic_fever', 6, 'Chronic RHD: balloon mitral valvotomy, valve repair or replacement, and anticoagulation for atrial fibrillation or mechanical valves')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_treatments where disease_id = 'rheumatic_fever');

insert into public.disease_home_care (disease_id, position, content)
select * from (values
    ('rheumatic_fever', 0, 'Never miss a penicillin injection; keep a card with the schedule and next due date'),
    ('rheumatic_fever', 1, 'Rest during the acute illness and return to activity gradually as advised'),
    ('rheumatic_fever', 2, 'Have sore throats checked and treated promptly, for the patient and the household'),
    ('rheumatic_fever', 3, 'Keep teeth and gums healthy and see a dentist regularly'),
    ('rheumatic_fever', 4, 'Women with RHD should plan pregnancy with their doctor')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_home_care where disease_id = 'rheumatic_fever');

insert into public.disease_emergency_signs (disease_id, position, content)
select * from (values
    ('rheumatic_fever', 0, 'Shortness of breath at rest or when lying flat'),
    ('rheumatic_fever', 1, 'Chest pain or a racing, irregular heartbeat'),
    ('rheumatic_fever', 2, 'Swelling of the legs or abdomen'),
    ('rheumatic_fever', 3, 'Fainting'),
    ('rheumatic_fever', 4, 'Coughing up blood or pink frothy sputum'),
    ('rheumatic_fever', 5, 'Sudden weakness, slurred speech or facial droop (possible stroke from a heart clot)')
) v(disease_id, position, content)
where not exists (select 1 from public.disease_emergency_signs where disease_id = 'rheumatic_fever');

insert into public.disease_prevention (disease_id, position, content, tier)
select * from (values
    ('rheumatic_fever', 0, 'Prompt diagnosis and antibiotic treatment of group A streptococcal sore throat, ideally within 9 days of onset; better housing and less overcrowding reduce transmission.', 'primary'::public.prevention_tier),
    ('rheumatic_fever', 1, 'Long-term benzathine penicillin G every 3-4 weeks after a first attack to prevent recurrences that worsen valve damage; echocardiographic screening in high-risk communities.', 'secondary'::public.prevention_tier),
    ('rheumatic_fever', 2, 'Heart failure treatment, anticoagulation, valve repair or replacement, and specialist pregnancy care to limit disability and death from rheumatic heart disease.', 'tertiary'::public.prevention_tier)
) v(disease_id, position, content, tier)
where not exists (select 1 from public.disease_prevention where disease_id = 'rheumatic_fever');

insert into public.disease_differentials (disease_id, position, condition, distinguishing_feature)
select * from (values
    ('rheumatic_fever', 0, 'Septic arthritis', 'Usually one hot joint with high fever; organisms in joint fluid; does not migrate'),
    ('rheumatic_fever', 1, 'Juvenile idiopathic arthritis', 'Arthritis lasting more than 6 weeks, non-migratory, poor response to salicylates'),
    ('rheumatic_fever', 2, 'Reactive arthritis', 'Follows gastrointestinal or genitourinary infection; asymmetric lower-limb arthritis, urethritis, conjunctivitis'),
    ('rheumatic_fever', 3, 'Infective endocarditis', 'Fever with a murmur, positive blood cultures and embolic phenomena'),
    ('rheumatic_fever', 4, 'Systemic lupus erythematosus', 'Rash, cytopenias, kidney involvement and positive ANA'),
    ('rheumatic_fever', 5, 'Chikungunya', 'Severe symmetric polyarthralgia with fever and rash in an outbreak setting; no evidence of strep infection')
) v(disease_id, position, condition, distinguishing_feature)
where not exists (select 1 from public.disease_differentials where disease_id = 'rheumatic_fever');

insert into public.disease_tags (disease_id, tag)
select * from (values
    ('rheumatic_fever', 'group A Streptococcus'),
    ('rheumatic_fever', 'Jones criteria'),
    ('rheumatic_fever', 'valvular heart disease'),
    ('rheumatic_fever', 'penicillin prophylaxis'),
    ('rheumatic_fever', 'pediatrics')
) v(disease_id, tag)
where not exists (select 1 from public.disease_tags where disease_id = 'rheumatic_fever');

insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select * from (values
    ('rheumatic_fever', 'sym_fever', 7::smallint, true, 1.0::numeric),
    ('rheumatic_fever', 'sym_arthralgia', 7::smallint, true, 1.2::numeric),
    ('rheumatic_fever', 'sym_joint_swelling', 6::smallint, true, 1.3::numeric),
    ('rheumatic_fever', 'sym_sore_throat', 3::smallint, false, 0.8::numeric),
    ('rheumatic_fever', 'sym_dyspnea', 4::smallint, false, 0.8::numeric),
    ('rheumatic_fever', 'sym_palpitations', 3::smallint, false, 0.6::numeric),
    ('rheumatic_fever', 'sym_chest_pain', 3::smallint, false, 0.6::numeric),
    ('rheumatic_fever', 'sym_fatigue', 4::smallint, false, 0.5::numeric),
    ('rheumatic_fever', 'sym_edema', 2::smallint, false, 0.5::numeric),
    ('rheumatic_fever', 'sym_chorea', 2::smallint, false, 1.5::numeric),
    ('rheumatic_fever', 'sym_erythema_marginatum', 1::smallint, false, 1.5::numeric)
) v(disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
where not exists (select 1 from public.disease_symptoms where disease_id = 'rheumatic_fever');

insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select * from (values
    ('rheumatic_fever', 'med_benzathine_penicillin', 0, 'safe'::public.condition_safety, 'Single IM dose eradicates group A strep; repeated every 3-4 weeks as secondary prophylaxis (WHO, AHA). Never give IV.'),
    ('rheumatic_fever', 'med_amoxicillin', 1, 'safe'::public.condition_safety, '10-day oral course is an alternative for eradicating streptococcal pharyngitis.'),
    ('rheumatic_fever', 'med_aspirin', 2, 'caution'::public.condition_safety, 'High anti-inflammatory doses (not the low cardiac dose) relieve arthritis and mild carditis; monitor for toxicity and avoid during influenza or varicella (Reye syndrome).'),
    ('rheumatic_fever', 'med_prednisone', 3, 'caution'::public.condition_safety, 'Sometimes used for severe carditis with heart failure; evidence of long-term benefit on valve outcome is limited.'),
    ('rheumatic_fever', 'med_furosemide', 4, 'safe'::public.condition_safety, 'Loop diuretic for heart failure caused by carditis or chronic valve disease.'),
    ('rheumatic_fever', 'med_warfarin', 5, 'caution'::public.condition_safety, 'Used for atrial fibrillation with mitral stenosis and for mechanical valves; needs regular INR monitoring.'),
    ('rheumatic_fever', 'med_paracetamol', 6, 'safe'::public.condition_safety, 'Analgesia while the diagnosis is confirmed; does not mask the arthritis pattern the way salicylates can.')
) v(disease_id, medicine_id, position, safety, note)
where not exists (select 1 from public.disease_medicines where disease_id = 'rheumatic_fever');

insert into public.clinical_references (id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
select * from (values
    ('ref_rheumatic_fever_1', 'rheumatic_fever', 0, 'Harrison''s Principles of Internal Medicine', 'Loscalzo J, Fauci A, Kasper D, Hauser S, Longo D, Jameson JL, eds. Harrison''s Principles of Internal Medicine, 21st ed. New York: McGraw Hill; 2022.', null, 'Internal Medicine', true),
    ('ref_rheumatic_fever_2', 'rheumatic_fever', 1, 'AHA Scientific Statement - Revision of the Jones Criteria (2015)', 'Gewitz MH, Baltimore RS, Tani LY, et al. Revision of the Jones Criteria for the diagnosis of acute rheumatic fever in the era of Doppler echocardiography: a scientific statement from the American Heart Association. Circulation. 2015;131(20):1806-1818.', null, 'Cardiology / Pediatrics', false),
    ('ref_rheumatic_fever_3', 'rheumatic_fever', 2, 'AHA Scientific Statement - Prevention of Rheumatic Fever (2009)', 'Gerber MA, Baltimore RS, Eaton CB, et al. Prevention of rheumatic fever and diagnosis and treatment of acute streptococcal pharyngitis. Circulation. 2009;119(11):1541-1551.', null, 'Cardiology / Infectious Disease', false),
    ('ref_rheumatic_fever_4', 'rheumatic_fever', 3, 'WHO Fact Sheet - Rheumatic heart disease', 'World Health Organization. Rheumatic heart disease. Fact sheet. Geneva: WHO.', 'https://www.who.int/news-room/fact-sheets/detail/rheumatic-heart-disease', 'Public Health / Cardiology', false)
) v(id, disease_id, position, source_name, citation_text, url, specialty, is_mother_book)
where not exists (select 1 from public.clinical_references where disease_id = 'rheumatic_fever');

-- ===================================================== related diseases (after all exist)
insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('acute_appendicitis', 'acute_gastroenteritis'),
    ('acute_appendicitis', 'urinary_tract_infection'),
    ('acute_appendicitis', 'typhoid_fever'),
    ('acute_appendicitis', 'peptic_ulcer_disease')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'acute_appendicitis');

insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('gerd', 'peptic_ulcer_disease'),
    ('gerd', 'acute_coronary_syndrome'),
    ('gerd', 'asthma')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'gerd');

insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('iron_deficiency_anemia', 'peptic_ulcer_disease'),
    ('iron_deficiency_anemia', 'schistosomiasis'),
    ('iron_deficiency_anemia', 'chronic_kidney_disease'),
    ('iron_deficiency_anemia', 'malaria'),
    ('iron_deficiency_anemia', 'heart_failure')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'iron_deficiency_anemia');

insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('chronic_kidney_disease', 'type2_diabetes'),
    ('chronic_kidney_disease', 'hypertension'),
    ('chronic_kidney_disease', 'heart_failure'),
    ('chronic_kidney_disease', 'urinary_tract_infection'),
    ('chronic_kidney_disease', 'iron_deficiency_anemia')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'chronic_kidney_disease');

insert into public.disease_related (disease_id, related_disease_id)
select * from (values
    ('rheumatic_fever', 'heart_failure'),
    ('rheumatic_fever', 'chikungunya')
) v(disease_id, related_disease_id)
where not exists (select 1 from public.disease_related where disease_id = 'rheumatic_fever');

-- every running Akeso downloads the new entries on its next sync
update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
