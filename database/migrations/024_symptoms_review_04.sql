-- 024_symptoms_review_04.sql  -  symptom review, session 04: 10 symptoms
-- Adds only: longer descriptions, extra causes, red flags, references and disease links.
-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).
-- A description is only extended if it is still the exported text (your own edits are kept).

begin;

-- ================================================ sym_polyuria  (Excessive urination (polyuria))
update public.symptoms set description = 'Polyuria is production of abnormally large volumes of urine, generally more than 2.5 L per day in adults, distinct from frequent passage of small volumes. It results from osmotic diuresis (e.g., hyperglycemia), excess fluid intake, diuretics or impaired urine concentration. Some references use more than 3 L a day. Uncontrolled diabetes and diuretics are the commonest causes, followed by primary polydipsia and diabetes insipidus; a high blood sodium suggests diabetes insipidus, while a low sodium suggests drinking too much water.', updated_at = now()
where id = 'sym_polyuria' and description = 'Polyuria is production of abnormally large volumes of urine, generally more than 2.5 L per day in adults, distinct from frequent passage of small volumes. It results from osmotic diuresis (e.g., hyperglycemia), excess fluid intake, diuretics or impaired urine concentration.';
update public.symptoms set tags = tags || array['diabetes insipidus']::text[]
where id = 'sym_polyuria' and not (tags @> array['diabetes insipidus']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Polyuria'
where id = 'sym_polyuria' and position('Merck Manual Professional - Polyuria' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_polyuria', 'Primary polydipsia', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_polyuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_polyuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_polyuria' and content = 'Primary polydipsia');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_polyuria', 'Lithium and other drugs that block vasopressin', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_polyuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_polyuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_polyuria' and content = 'Lithium and other drugs that block vasopressin');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_polyuria', 'Onset in early childhood or a sudden, abrupt start', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_polyuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_polyuria')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_polyuria' and content = 'Onset in early childhood or a sudden, abrupt start');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_polyuria', 'Night sweats, cough or weight loss', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_polyuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_polyuria')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_polyuria' and content = 'Night sweats, cough or weight loss');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_polyuria', 'Merck Manual Professional - Polyuria', 'Maddukuri G. Polyuria. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Sep 2024.', 'https://www.merckmanuals.com/professional/genitourinary-disorders/symptoms-of-genitourinary-disorders/polyuria', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_polyuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_polyuria')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_polyuria' and url = 'https://www.merckmanuals.com/professional/genitourinary-disorders/symptoms-of-genitourinary-disorders/polyuria');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'chronic_kidney_disease', 'sym_polyuria', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.symptoms where id = 'sym_polyuria')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'chronic_kidney_disease' and symptom_id = 'sym_polyuria');

-- ================================================ sym_facial_droop  (Facial droop)
update public.symptoms set description = 'Facial droop is weakness of the facial muscles causing asymmetry of the face, such as a drooping mouth corner. Stroke typically causes lower facial weakness with forehead sparing, whereas Bell''s palsy affects the whole side of the face including the forehead. Peripheral facial palsy has many causes besides Bell''s palsy (usually herpes simplex): herpes zoster of the ear, Lyme disease, sarcoidosis, diabetes, skull fractures and tumors near the ear. MRI is needed when there are other neurological signs or the weakness comes on gradually.', updated_at = now()
where id = 'sym_facial_droop' and description = 'Facial droop is weakness of the facial muscles causing asymmetry of the face, such as a drooping mouth corner. Stroke typically causes lower facial weakness with forehead sparing, whereas Bell''s palsy affects the whole side of the face including the forehead.';
update public.symptoms set tags = tags || array['Bell palsy']::text[]
where id = 'sym_facial_droop' and not (tags @> array['Bell palsy']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Facial Nerve Palsy'
where id = 'sym_facial_droop' and position('Merck Manual Professional - Facial Nerve Palsy' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_facial_droop', 'Herpes zoster of the ear (Ramsay Hunt syndrome)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_facial_droop'), 0)
where exists (select 1 from public.symptoms where id = 'sym_facial_droop')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_facial_droop' and content = 'Herpes zoster of the ear (Ramsay Hunt syndrome)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_facial_droop', 'Diabetes', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_facial_droop'), 0)
where exists (select 1 from public.symptoms where id = 'sym_facial_droop')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_facial_droop' and content = 'Diabetes');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_facial_droop', 'Sarcoidosis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_facial_droop'), 0)
where exists (select 1 from public.symptoms where id = 'sym_facial_droop')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_facial_droop' and content = 'Sarcoidosis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_facial_droop', 'Skull base fracture', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_facial_droop'), 0)
where exists (select 1 from public.symptoms where id = 'sym_facial_droop')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_facial_droop' and content = 'Skull base fracture');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_facial_droop', 'Weakness on both sides of the face', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_facial_droop'), 0)
where exists (select 1 from public.symptoms where id = 'sym_facial_droop')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_facial_droop' and content = 'Weakness on both sides of the face');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_facial_droop', 'Weakness that develops slowly over weeks (possible tumor)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_facial_droop'), 0)
where exists (select 1 from public.symptoms where id = 'sym_facial_droop')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_facial_droop' and content = 'Weakness that develops slowly over weeks (possible tumor)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_facial_droop', 'Merck Manual Professional - Facial Nerve Palsy', 'Rubin M. Facial Nerve Palsy. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2025.', 'https://www.merckmanuals.com/professional/neurologic-disorders/neuro-ophthalmologic-and-cranial-nerve-disorders/facial-nerve-palsy', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_facial_droop'), 0)
where exists (select 1 from public.symptoms where id = 'sym_facial_droop')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_facial_droop' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/neuro-ophthalmologic-and-cranial-nerve-disorders/facial-nerve-palsy');

-- ================================================ sym_fatigue  (Fatigue & malaise)
update public.symptoms set description = 'Fatigue is a feeling of weariness, tiredness or lack of energy that is not relieved by usual rest, and malaise is a general sense of being unwell. Both accompany a very broad range of infectious, metabolic, hematologic, psychiatric and lifestyle-related conditions. The likely causes change with duration: under a month, mostly medicines, anemia, stress or depression; one to six months, diabetes, hypothyroidism, sleep apnea or cancer; beyond six months, chronic fatigue syndrome, post-viral or psychiatric causes. Fatigue that worsens with activity and improves with rest suggests a physical cause.', updated_at = now()
where id = 'sym_fatigue' and description = 'Fatigue is a feeling of weariness, tiredness or lack of energy that is not relieved by usual rest, and malaise is a general sense of being unwell. Both accompany a very broad range of infectious, metabolic, hematologic, psychiatric and lifestyle-related conditions.';
update public.symptoms set tags = tags || array['chronic fatigue']::text[]
where id = 'sym_fatigue' and not (tags @> array['chronic fatigue']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Fatigue'
where id = 'sym_fatigue' and position('Merck Manual Professional - Fatigue' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_fatigue', 'Medicines', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_fatigue'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fatigue')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_fatigue' and content = 'Medicines');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_fatigue', 'Obstructive sleep apnea', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_fatigue'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fatigue')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_fatigue' and content = 'Obstructive sleep apnea');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_fatigue', 'Cancer', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_fatigue'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fatigue')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_fatigue' and content = 'Cancer');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_fatigue', 'Chronic fatigue syndrome (ME/CFS) and post-viral fatigue', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_fatigue'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fatigue')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_fatigue' and content = 'Chronic fatigue syndrome (ME/CFS) and post-viral fatigue');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_fatigue', 'Swollen lymph nodes in several areas, or fever with night sweats', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_fatigue'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fatigue')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_fatigue' and content = 'Swollen lymph nodes in several areas, or fever with night sweats');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_fatigue', 'New headache or vision problems in an older adult (possible giant cell arteritis)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_fatigue'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fatigue')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_fatigue' and content = 'New headache or vision problems in an older adult (possible giant cell arteritis)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_fatigue', 'Merck Manual Professional - Fatigue', 'Wasserman MR. Fatigue. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2025 (updated Jan 2026).', 'https://www.merckmanuals.com/professional/special-subjects/nonspecific-symptoms/fatigue', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_fatigue'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fatigue')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_fatigue' and url = 'https://www.merckmanuals.com/professional/special-subjects/nonspecific-symptoms/fatigue');

-- ================================================ sym_hydrophobia  (Fear of water / throat spasms on swallowing (hydrophobia))
update public.symptoms set description = 'Hydrophobia is a terrifying, involuntary spasm of the pharyngeal, laryngeal and inspiratory muscles provoked by attempts to drink, and in time by the sight, sound or even thought of water. It is the hallmark of furious (encephalitic) rabies and is often accompanied by aerophobia, spasms triggered by a draft of air on the face. About 80% of rabies cases are furious, with agitation, hallucinations and insomnia; the remaining 20% are paralytic, with ascending paralysis and no hydrophobia. The incubation period averages 1 to 2 months but can exceed a year, death usually follows within days of symptom onset, and prompt post-exposure prophylaxis almost always prevents the disease.', updated_at = now()
where id = 'sym_hydrophobia' and description = 'Hydrophobia is a terrifying, involuntary spasm of the pharyngeal, laryngeal and inspiratory muscles provoked by attempts to drink, and in time by the sight, sound or even thought of water. It is the hallmark of furious (encephalitic) rabies and is often accompanied by aerophobia, spasms triggered by a draft of air on the face.';
update public.symptoms set tags = tags || array['post-exposure prophylaxis']::text[]
where id = 'sym_hydrophobia' and not (tags @> array['post-exposure prophylaxis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Rabies; CDC - Clinical Features of Rabies'
where id = 'sym_hydrophobia' and position('Merck Manual Professional - Rabies' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_hydrophobia', 'Pain, itching or tingling at the site of an old bite', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_hydrophobia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hydrophobia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_hydrophobia' and content = 'Pain, itching or tingling at the site of an old bite');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_hydrophobia', 'Merck Manual Professional - Rabies', 'Klein RS. Rabies. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2026 (updated Sep 2026).', 'https://www.merckmanuals.com/professional/neurologic-disorders/brain-infections/rabies', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_hydrophobia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hydrophobia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_hydrophobia' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/brain-infections/rabies');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_hydrophobia', 'CDC - Clinical Features of Rabies', 'Centers for Disease Control and Prevention. Clinical Features of Rabies. Atlanta (GA): CDC; reviewed Jul 2025 (updated Mar 2026).', 'https://www.cdc.gov/rabies/hcp/clinical-signs/index.html', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_hydrophobia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hydrophobia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_hydrophobia' and url = 'https://www.cdc.gov/rabies/hcp/clinical-signs/index.html');

-- ================================================ sym_fever  (Fever)
update public.symptoms set description = 'Fever is a regulated elevation of body temperature above the individual''s normal range, produced when pyrogens reset the hypothalamic thermoregulatory set point. It is most often a response to infection but also accompanies inflammatory, malignant, drug-related and other conditions. An oral temperature of 37.8 °C or more after early morning, or 37.2 °C or more in the early morning, is raised; fever differs from hyperthermia (such as heat stroke), where the set point is normal. Older adults may have little or no fever despite a serious infection.', updated_at = now()
where id = 'sym_fever' and description = 'Fever is a regulated elevation of body temperature above the individual''s normal range, produced when pyrogens reset the hypothalamic thermoregulatory set point. It is most often a response to infection but also accompanies inflammatory, malignant, drug-related and other conditions.';
update public.symptoms set tags = tags || array['hyperthermia']::text[]
where id = 'sym_fever' and not (tags @> array['hyperthermia']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Fever'
where id = 'sym_fever' and position('Merck Manual Professional - Fever' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_fever', 'Abscess or other hidden infection', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_fever'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fever')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_fever' and content = 'Abscess or other hidden infection');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_fever', 'Heat stroke (hyperthermia, not a true fever)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_fever'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fever')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_fever' and content = 'Heat stroke (hyperthermia, not a true fever)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_fever', 'Temperature above 40 °C or below 35 °C', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_fever'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fever')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_fever' and content = 'Temperature above 40 °C or below 35 °C');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_fever', 'Recent travel or a weakened immune system', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_fever'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fever')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_fever' and content = 'Recent travel or a weakened immune system');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_fever', 'Merck Manual Professional - Fever', 'Bush LM, Vazquez-Pertejo MT. Fever. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2024 (updated Apr 2026).', 'https://www.merckmanuals.com/professional/infectious-diseases/biology-of-infectious-disease/fever', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_fever'), 0)
where exists (select 1 from public.symptoms where id = 'sym_fever')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_fever' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/biology-of-infectious-disease/fever');

-- ================================================ sym_flank_pain  (Flank pain)
update public.symptoms set description = 'Flank pain is pain in one side of the body between the upper abdomen and the back. It commonly arises from the kidney or ureter, as in pyelonephritis or kidney stones, and costovertebral angle tenderness may be present. Kidney stone colic is excruciating, comes in waves of 20 to 60 minutes with nausea, and makes the patient writhe or pace, unlike peritonitis where the patient lies still. Pain spreading across the abdomen suggests a stone high in the ureter, and pain spreading to the groin or genitals suggests one lower down.', updated_at = now()
where id = 'sym_flank_pain' and description = 'Flank pain is pain in one side of the body between the upper abdomen and the back. It commonly arises from the kidney or ureter, as in pyelonephritis or kidney stones, and costovertebral angle tenderness may be present.';
update public.symptoms set tags = tags || array['renal colic']::text[]
where id = 'sym_flank_pain' and not (tags @> array['renal colic']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Urinary Calculi'
where id = 'sym_flank_pain' and position('Merck Manual Professional - Urinary Calculi' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_flank_pain', 'Aortic dissection or aneurysm (older patients)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_flank_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_flank_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_flank_pain' and content = 'Aortic dissection or aneurysm (older patients)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_flank_pain', 'Fever or cloudy urine with a blocked kidney (needs urgent drainage)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_flank_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_flank_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_flank_pain' and content = 'Fever or cloudy urine with a blocked kidney (needs urgent drainage)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_flank_pain', 'Merck Manual Professional - Urinary Calculi', 'Preminger GM. Urinary Calculi. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jan 2025 (updated Apr 2025).', 'https://www.merckmanuals.com/professional/genitourinary-disorders/urinary-calculi/urinary-calculi', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_flank_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_flank_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_flank_pain' and url = 'https://www.merckmanuals.com/professional/genitourinary-disorders/urinary-calculi/urinary-calculi');

-- ================================================ sym_foamy_urine  (Foamy or bubbly urine)
update public.symptoms set description = 'Urine that repeatedly forms a frothy layer that does not settle. Occasional foam is normal (forceful stream, concentrated urine), but persistent foaminess can reflect large amounts of protein in the urine (proteinuria), a marker of glomerular kidney damage in diabetes, hypertension and glomerulonephritis. Glomerular disease is the commonest cause of heavy proteinuria, including diabetic nephropathy, membranous nephropathy and focal segmental glomerulosclerosis; nephrotic-range proteinuria is more than 3.5 g a day. Persistent proteinuria on a dipstick should be measured (urine protein-to-creatinine ratio) and investigated.', updated_at = now()
where id = 'sym_foamy_urine' and description = 'Urine that repeatedly forms a frothy layer that does not settle. Occasional foam is normal (forceful stream, concentrated urine), but persistent foaminess can reflect large amounts of protein in the urine (proteinuria), a marker of glomerular kidney damage in diabetes, hypertension and glomerulonephritis.';
update public.symptoms set tags = tags || array['nephrotic syndrome']::text[]
where id = 'sym_foamy_urine' and not (tags @> array['nephrotic syndrome']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Proteinuria'
where id = 'sym_foamy_urine' and position('Merck Manual Professional - Proteinuria' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_foamy_urine', 'Membranous nephropathy and focal segmental glomerulosclerosis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_foamy_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_foamy_urine')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_foamy_urine' and content = 'Membranous nephropathy and focal segmental glomerulosclerosis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_foamy_urine', 'Persistent foamy urine in someone with diabetes or high blood pressure', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_foamy_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_foamy_urine')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_foamy_urine' and content = 'Persistent foamy urine in someone with diabetes or high blood pressure');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_foamy_urine', 'Merck Manual Professional - Proteinuria', 'Maddukuri G. Proteinuria. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Sep 2024 (updated Feb 2026).', 'https://www.merckmanuals.com/professional/genitourinary-disorders/symptoms-of-genitourinary-disorders/proteinuria', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_foamy_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_foamy_urine')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_foamy_urine' and url = 'https://www.merckmanuals.com/professional/genitourinary-disorders/symptoms-of-genitourinary-disorders/proteinuria');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'type2_diabetes', 'sym_foamy_urine', 2::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.symptoms where id = 'sym_foamy_urine')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'type2_diabetes' and symptom_id = 'sym_foamy_urine');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'hypertension', 'sym_foamy_urine', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'hypertension')
  and exists (select 1 from public.symptoms where id = 'sym_foamy_urine')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'hypertension' and symptom_id = 'sym_foamy_urine');

-- ================================================ sym_headache  (Headache)
update public.symptoms set description = 'Headache is pain in any region of the head, arising from pain-sensitive intracranial or extracranial structures. Most headaches are primary (migraine, tension-type, cluster), but headache also accompanies systemic infection and can signal serious intracranial disease. A new headache after age 50 is treated as secondary until proven otherwise. A sudden thunderclap headache needs urgent brain imaging and, if imaging is normal, a lumbar puncture to look for bleeding.', updated_at = now()
where id = 'sym_headache' and description = 'Headache is pain in any region of the head, arising from pain-sensitive intracranial or extracranial structures. Most headaches are primary (migraine, tension-type, cluster), but headache also accompanies systemic infection and can signal serious intracranial disease.';
update public.symptoms set tags = tags || array['thunderclap']::text[]
where id = 'sym_headache' and not (tags @> array['thunderclap']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Approach to the Patient With Headache'
where id = 'sym_headache' and position('Merck Manual Professional - Approach to the Patient With Headache' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_headache', 'Cluster headache', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_headache'), 0)
where exists (select 1 from public.symptoms where id = 'sym_headache')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_headache' and content = 'Cluster headache');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_headache', 'Giant cell arteritis (older adults)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_headache'), 0)
where exists (select 1 from public.symptoms where id = 'sym_headache')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_headache' and content = 'Giant cell arteritis (older adults)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_headache', 'Medication-overuse headache', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_headache'), 0)
where exists (select 1 from public.symptoms where id = 'sym_headache')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_headache' and content = 'Medication-overuse headache');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_headache', 'Carbon monoxide poisoning', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_headache'), 0)
where exists (select 1 from public.symptoms where id = 'sym_headache')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_headache' and content = 'Carbon monoxide poisoning');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_headache', 'Jaw pain on chewing, scalp tenderness or vision changes in someone over 50', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_headache'), 0)
where exists (select 1 from public.symptoms where id = 'sym_headache')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_headache' and content = 'Jaw pain on chewing, scalp tenderness or vision changes in someone over 50');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_headache', 'Headache in a person with cancer or a weakened immune system', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_headache'), 0)
where exists (select 1 from public.symptoms where id = 'sym_headache')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_headache' and content = 'Headache in a person with cancer or a weakened immune system');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_headache', 'Merck Manual Professional - Approach to the Patient With Headache', 'Silberstein SD. Approach to the Patient With Headache. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2025.', 'https://www.merckmanuals.com/professional/neurologic-disorders/headache/approach-to-the-patient-with-headache', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_headache'), 0)
where exists (select 1 from public.symptoms where id = 'sym_headache')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_headache' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/headache/approach-to-the-patient-with-headache');

-- ================================================ sym_heartburn  (Heartburn)
update public.symptoms set description = 'Heartburn is a painful burning feeling just below or behind the breastbone, usually caused by reflux of gastric acid into the esophagus. It is often worse after meals, when lying down or bending over. Heartburn, with or without regurgitation, is the main symptom of GERD in adolescents and adults. Long-standing reflux can lead to esophagitis, stricture, Barrett esophagus and adenocarcinoma, and reflux into the airway can cause chronic cough, hoarseness or wheeze.', updated_at = now()
where id = 'sym_heartburn' and description = 'Heartburn is a painful burning feeling just below or behind the breastbone, usually caused by reflux of gastric acid into the esophagus. It is often worse after meals, when lying down or bending over.';
update public.symptoms set tags = tags || array['Barrett esophagus']::text[]
where id = 'sym_heartburn' and not (tags @> array['Barrett esophagus']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Gastroesophageal Reflux Disease (GERD)'
where id = 'sym_heartburn' and position('Merck Manual Professional - Gastroesophageal Reflux Disease (GERD)' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_heartburn', 'Eosinophilic esophagitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_heartburn'), 0)
where exists (select 1 from public.symptoms where id = 'sym_heartburn')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_heartburn' and content = 'Eosinophilic esophagitis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_heartburn', 'No improvement after a course of acid-suppressing medicine', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_heartburn'), 0)
where exists (select 1 from public.symptoms where id = 'sym_heartburn')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_heartburn' and content = 'No improvement after a course of acid-suppressing medicine');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_heartburn', 'Hoarseness, chronic cough or wheeze', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_heartburn'), 0)
where exists (select 1 from public.symptoms where id = 'sym_heartburn')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_heartburn' and content = 'Hoarseness, chronic cough or wheeze');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_heartburn', 'Merck Manual Professional - Gastroesophageal Reflux Disease (GERD)', 'Lynch KL. Gastroesophageal Reflux Disease (GERD). Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2026.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/esophageal-and-swallowing-disorders/gastroesophageal-reflux-disease-gerd', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_heartburn'), 0)
where exists (select 1 from public.symptoms where id = 'sym_heartburn')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_heartburn' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/esophageal-and-swallowing-disorders/gastroesophageal-reflux-disease-gerd');

-- ================================================ sym_heat_intolerance  (Heat intolerance and excessive sweating)
update public.symptoms set description = 'Feeling unusually hot, sweaty or uncomfortable in warm surroundings that others tolerate. It reflects increased heat production from a raised metabolic rate and is a classic symptom of hyperthyroidism, together with weight loss, tremor and palpitations. It reflects increased sensitivity to adrenaline and comes with warm moist skin, tremor and a fast heart rate. Eye changes (bulging eyes) and shin skin thickening point specifically to Graves disease; older adults may have apathetic hyperthyroidism with low mood, weight loss and atrial fibrillation rather than heat intolerance.', updated_at = now()
where id = 'sym_heat_intolerance' and description = 'Feeling unusually hot, sweaty or uncomfortable in warm surroundings that others tolerate. It reflects increased heat production from a raised metabolic rate and is a classic symptom of hyperthyroidism, together with weight loss, tremor and palpitations.';
update public.symptoms set tags = tags || array['hyperthyroidism']::text[]
where id = 'sym_heat_intolerance' and not (tags @> array['hyperthyroidism']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Hyperthyroidism'
where id = 'sym_heat_intolerance' and position('Merck Manual Professional - Hyperthyroidism' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_heat_intolerance', 'Taking too much thyroid hormone medicine', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_heat_intolerance'), 0)
where exists (select 1 from public.symptoms where id = 'sym_heat_intolerance')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_heat_intolerance' and content = 'Taking too much thyroid hormone medicine');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_heat_intolerance', 'Irregular heartbeat (possible atrial fibrillation)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_heat_intolerance'), 0)
where exists (select 1 from public.symptoms where id = 'sym_heat_intolerance')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_heat_intolerance' and content = 'Irregular heartbeat (possible atrial fibrillation)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_heat_intolerance', 'Merck Manual Professional - Hyperthyroidism', 'Boucai L. Hyperthyroidism. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jan 2026.', 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/hyperthyroidism', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_heat_intolerance'), 0)
where exists (select 1 from public.symptoms where id = 'sym_heat_intolerance')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_heat_intolerance' and url = 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/thyroid-disorders/hyperthyroidism');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
