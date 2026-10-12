-- 027_symptoms_review_07.sql  -  symptom review, session 07: 10 symptoms
-- Adds only: longer descriptions, extra causes, red flags, references and disease links.
-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).
-- A description is only extended if it is still the exported text (your own edits are kept).

begin;

-- ================================================ sym_palpitations  (Palpitations)
update public.symptoms set description = 'Palpitations are an awareness of the heartbeat as pounding, racing, fluttering or irregular, felt in the chest, throat or neck. They may be benign or reflect arrhythmia, structural heart disease, anemia, thyrotoxicosis or stimulant use. Most are caused by harmless extra beats (premature atrial or ventricular contractions); others include supraventricular tachycardia, atrial fibrillation or flutter, ventricular tachycardia and non-cardiac triggers such as thyrotoxicosis, anemia, caffeine and low potassium. An ECG recorded during symptoms is the key test.', updated_at = now()
where id = 'sym_palpitations' and description = 'Palpitations are an awareness of the heartbeat as pounding, racing, fluttering or irregular, felt in the chest, throat or neck. They may be benign or reflect arrhythmia, structural heart disease, anemia, thyrotoxicosis or stimulant use.';
update public.symptoms set tags = tags || array['ECG']::text[]
where id = 'sym_palpitations' and not (tags @> array['ECG']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Palpitations'
where id = 'sym_palpitations' and position('Merck Manual Professional - Palpitations' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_palpitations', 'Harmless extra beats (premature contractions)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_palpitations'), 0)
where exists (select 1 from public.symptoms where id = 'sym_palpitations')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_palpitations' and content = 'Harmless extra beats (premature contractions)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_palpitations', 'Supraventricular tachycardia', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_palpitations'), 0)
where exists (select 1 from public.symptoms where id = 'sym_palpitations')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_palpitations' and content = 'Supraventricular tachycardia');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_palpitations', 'Ventricular tachycardia', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_palpitations'), 0)
where exists (select 1 from public.symptoms where id = 'sym_palpitations')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_palpitations' and content = 'Ventricular tachycardia');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_palpitations', 'Low potassium', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_palpitations'), 0)
where exists (select 1 from public.symptoms where id = 'sym_palpitations')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_palpitations' and content = 'Low potassium');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_palpitations', 'Heart rate over 120 or under 45 at rest', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_palpitations'), 0)
where exists (select 1 from public.symptoms where id = 'sym_palpitations')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_palpitations' and content = 'Heart rate over 120 or under 45 at rest');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_palpitations', 'Palpitations during exercise, or a family history of sudden death', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_palpitations'), 0)
where exists (select 1 from public.symptoms where id = 'sym_palpitations')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_palpitations' and content = 'Palpitations during exercise, or a family history of sudden death');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_palpitations', 'Merck Manual Professional - Palpitations', 'Thompson AD, Shea MJ. Palpitations. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2024.', 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/palpitations', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_palpitations'), 0)
where exists (select 1 from public.symptoms where id = 'sym_palpitations')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_palpitations' and url = 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/palpitations');

-- ================================================ sym_erythema_marginatum  (Pink ring-shaped rash on the trunk (erythema marginatum))
update public.symptoms set description = 'A faint pink, non-itchy rash of rings or arcs with pale centres and sharp, raised edges, appearing mainly on the trunk and upper limbs and sparing the face. It comes and goes, may be brought out by heat, and is a rare but specific sign of acute rheumatic fever. The rash is flat or slightly raised, painless and leaves no scar, sometimes lasting less than a day, and is seen in fewer than 6% of children with acute rheumatic fever. It is one of the five major Jones criteria: diagnosis needs two major, or one major and two minor criteria, plus evidence of recent group A streptococcal infection.', updated_at = now()
where id = 'sym_erythema_marginatum' and description = 'A faint pink, non-itchy rash of rings or arcs with pale centres and sharp, raised edges, appearing mainly on the trunk and upper limbs and sparing the face. It comes and goes, may be brought out by heat, and is a rare but specific sign of acute rheumatic fever.';
update public.symptoms set tags = tags || array['Jones criteria']::text[]
where id = 'sym_erythema_marginatum' and not (tags @> array['Jones criteria']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Rheumatic Fever'
where id = 'sym_erythema_marginatum' and position('Merck Manual Professional - Rheumatic Fever' in source_attribution) = 0;
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_erythema_marginatum', 'Merck Manual Professional - Rheumatic Fever', 'Weinberg GA. Rheumatic Fever. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2024.', 'https://www.merckmanuals.com/professional/pediatrics/miscellaneous-bacterial-infections-in-infants-and-children/rheumatic-fever', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_erythema_marginatum'), 0)
where exists (select 1 from public.symptoms where id = 'sym_erythema_marginatum')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_erythema_marginatum' and url = 'https://www.merckmanuals.com/professional/pediatrics/miscellaneous-bacterial-infections-in-infants-and-children/rheumatic-fever');

-- ================================================ sym_pleuritic_chest_pain  (Pleuritic chest pain)
update public.symptoms set description = 'Pleuritic chest pain is sharp, localized pain in the chest, neck or shoulder that worsens with breathing, coughing or sneezing. It results from irritation or inflammation of the parietal pleura; pulmonary embolism is the most frequent serious cause. Pulmonary embolism comes with breathlessness, fast heart rate and sometimes coughing blood; pneumothorax with reduced breath sounds on one side; pericarditis with pain worse lying flat and better leaning forward and a friction rub. Pain that worsens with breathing or pressing on the chest does not by itself prove a chest-wall cause.', updated_at = now()
where id = 'sym_pleuritic_chest_pain' and description = 'Pleuritic chest pain is sharp, localized pain in the chest, neck or shoulder that worsens with breathing, coughing or sneezing. It results from irritation or inflammation of the parietal pleura; pulmonary embolism is the most frequent serious cause.';
update public.symptoms set tags = tags || array['pleurisy']::text[]
where id = 'sym_pleuritic_chest_pain' and not (tags @> array['pleurisy']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Chest Pain'
where id = 'sym_pleuritic_chest_pain' and position('Merck Manual Professional - Chest Pain' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_pleuritic_chest_pain', 'Pain worse lying flat and better leaning forward (possible pericarditis)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_pleuritic_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pleuritic_chest_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_pleuritic_chest_pain' and content = 'Pain worse lying flat and better leaning forward (possible pericarditis)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_pleuritic_chest_pain', 'Merck Manual Professional - Chest Pain', 'Thompson AD, Shea MJ. Chest Pain. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2024.', 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/chest-pain', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_pleuritic_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pleuritic_chest_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_pleuritic_chest_pain' and url = 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/chest-pain');

-- ================================================ sym_productive_cough  (Productive cough (sputum))
update public.symptoms set description = 'A productive cough brings up sputum from the lower respiratory tract. Purulent sputum (yellow, green, opaque) suggests bacterial infection, rust-coloured sputum is associated with pneumococcal pneumonia, and pink frothy sputum suggests pulmonary edema. Chronic bronchitis is defined as a productive cough for 3 months a year for 2 years in a row, usually in smokers. The color or thickness of sputum does not reliably tell bacterial from viral infection.', updated_at = now()
where id = 'sym_productive_cough' and description = 'A productive cough brings up sputum from the lower respiratory tract. Purulent sputum (yellow, green, opaque) suggests bacterial infection, rust-coloured sputum is associated with pneumococcal pneumonia, and pink frothy sputum suggests pulmonary edema.';
update public.symptoms set tags = tags || array['chronic bronchitis']::text[]
where id = 'sym_productive_cough' and not (tags @> array['chronic bronchitis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Cough in Adults'
where id = 'sym_productive_cough' and position('Merck Manual Professional - Cough in Adults' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_productive_cough', 'Heart failure (pink frothy sputum)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_productive_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_productive_cough')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_productive_cough' and content = 'Heart failure (pink frothy sputum)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_productive_cough', 'Known HIV infection or contact with someone with TB', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_productive_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_productive_cough')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_productive_cough' and content = 'Known HIV infection or contact with someone with TB');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_productive_cough', 'Merck Manual Professional - Cough in Adults', 'Dezube R. Cough in Adults. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Nov 2025.', 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/cough-in-adults', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_productive_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_productive_cough')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_productive_cough' and url = 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/cough-in-adults');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'heart_failure', 'sym_productive_cough', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.symptoms where id = 'sym_productive_cough')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'heart_failure' and symptom_id = 'sym_productive_cough');

-- ================================================ sym_watery_diarrhea  (Profuse watery ("rice-water") diarrhea)
update public.symptoms set description = 'Profuse watery diarrhea consists of large-volume, liquid stools; in cholera it is classically pale, flecked with mucus and described as "rice-water". Toxin-mediated intestinal secretion can cause losses of up to about a liter per hour in adults, producing severe dehydration and hypovolemic shock within hours if fluid is not replaced. Cholera diarrhea starts suddenly and is painless, often with vomiting, and the white stool contains no fecal material. Without treatment it causes low blood potassium, acidosis and circulatory collapse with a death rate above 50%, falling to about 1% with prompt rehydration.', updated_at = now()
where id = 'sym_watery_diarrhea' and description = 'Profuse watery diarrhea consists of large-volume, liquid stools; in cholera it is classically pale, flecked with mucus and described as "rice-water". Toxin-mediated intestinal secretion can cause losses of up to about a liter per hour in adults, producing severe dehydration and hypovolemic shock within hours if fluid is not replaced.';
update public.symptoms set tags = tags || array['oral rehydration']::text[]
where id = 'sym_watery_diarrhea' and not (tags @> array['oral rehydration']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Cholera'
where id = 'sym_watery_diarrhea' and position('Merck Manual Professional - Cholera' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_watery_diarrhea', 'Several cases in a household or community, especially after flooding or water contamination', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_watery_diarrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_watery_diarrhea')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_watery_diarrhea' and content = 'Several cases in a household or community, especially after flooding or water contamination');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_watery_diarrhea', 'Merck Manual Professional - Cholera', 'Bush LM, Vazquez-Pertejo MT. Cholera. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2024.', 'https://www.merckmanuals.com/professional/infectious-diseases/gram-negative-bacilli/cholera', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_watery_diarrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_watery_diarrhea')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_watery_diarrhea' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/gram-negative-bacilli/cholera');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'acute_gastroenteritis', 'sym_watery_diarrhea', 5::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.symptoms where id = 'sym_watery_diarrhea')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'acute_gastroenteritis' and symptom_id = 'sym_watery_diarrhea');

-- ================================================ sym_periorbital_edema  (Puffy eyelids and face (periorbital edema))
update public.symptoms set description = 'Swelling around the eyes and face, usually most obvious on waking and improving during the day. In children it is often the first sign of kidney disease such as post-streptococcal glomerulonephritis or nephrotic syndrome; allergy and insect bites cause similar but usually itchy swelling. Post-infectious glomerulonephritis typically begins 6 to 21 days after a throat or skin infection, with edema, blood and protein in the urine, reduced urine output and high blood pressure; complement C3 is low and usually returns to normal within 6 to 8 weeks. Angioedema causes sudden, uneven facial or lip swelling that can involve the airway.', updated_at = now()
where id = 'sym_periorbital_edema' and description = 'Swelling around the eyes and face, usually most obvious on waking and improving during the day. In children it is often the first sign of kidney disease such as post-streptococcal glomerulonephritis or nephrotic syndrome; allergy and insect bites cause similar but usually itchy swelling.';
update public.symptoms set tags = tags || array['nephritic']::text[]
where id = 'sym_periorbital_edema' and not (tags @> array['nephritic']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Edema; Merck Manual Professional - Postinfectious Glomerulonephritis (PIGN)'
where id = 'sym_periorbital_edema' and position('Merck Manual Professional - Edema' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_periorbital_edema', 'Swelling 1 to 3 weeks after a sore throat or skin infection, with dark urine', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_periorbital_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_periorbital_edema')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_periorbital_edema' and content = 'Swelling 1 to 3 weeks after a sore throat or skin infection, with dark urine');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_periorbital_edema', 'Merck Manual Professional - Edema', 'Thompson AD, Shea MJ. Edema. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2024.', 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/edema', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_periorbital_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_periorbital_edema')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_periorbital_edema' and url = 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/edema');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_periorbital_edema', 'Merck Manual Professional - Postinfectious Glomerulonephritis (PIGN)', 'O''Brien F. Postinfectious Glomerulonephritis (PIGN). Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Apr 2025.', 'https://www.merckmanuals.com/professional/genitourinary-disorders/glomerular-disorders/postinfectious-glomerulonephritis-pign', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_periorbital_edema'), 0)
where exists (select 1 from public.symptoms where id = 'sym_periorbital_edema')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_periorbital_edema' and url = 'https://www.merckmanuals.com/professional/genitourinary-disorders/glomerular-disorders/postinfectious-glomerulonephritis-pign');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'chronic_kidney_disease', 'sym_periorbital_edema', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.symptoms where id = 'sym_periorbital_edema')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'chronic_kidney_disease' and symptom_id = 'sym_periorbital_edema');

-- ================================================ sym_nonblanching_rash  (Purple rash that does not fade when pressed (non-blanching rash))
update public.symptoms set description = 'Small red-purple spots (petechiae) or larger bruise-like patches (purpura) that stay visible when a clear glass is pressed against them, because blood has leaked into the skin. With fever it can signal meningococcal septicemia, which can progress within hours; it also occurs with low platelets, dengue and vasculitis. In meningococcal disease the rash appears soon after onset, mainly on the trunk and legs; in fulminant cases the spots merge into bruises and dark patches of dead skin, with shock and DIC. Antibiotics (a third-generation cephalosporin) are started immediately, before tests come back.', updated_at = now()
where id = 'sym_nonblanching_rash' and description = 'Small red-purple spots (petechiae) or larger bruise-like patches (purpura) that stay visible when a clear glass is pressed against them, because blood has leaked into the skin. With fever it can signal meningococcal septicemia, which can progress within hours; it also occurs with low platelets, dengue and vasculitis.';
update public.symptoms set tags = tags || array['purpura']::text[]
where id = 'sym_nonblanching_rash' and not (tags @> array['purpura']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Meningococcal Diseases'
where id = 'sym_nonblanching_rash' and position('Merck Manual Professional - Meningococcal Diseases' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_nonblanching_rash', 'Spots merging into large bruises or dark patches', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_nonblanching_rash'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nonblanching_rash')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_nonblanching_rash' and content = 'Spots merging into large bruises or dark patches');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_nonblanching_rash', 'Merck Manual Professional - Meningococcal Diseases', 'Bush LM, Vazquez-Pertejo MT. Meningococcal Diseases. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2024.', 'https://www.merckmanuals.com/professional/infectious-diseases/gram-negative-cocci-and-coccobacilli/meningococcal-diseases', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_nonblanching_rash'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nonblanching_rash')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_nonblanching_rash' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/gram-negative-cocci-and-coccobacilli/meningococcal-diseases');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'dengue', 'sym_nonblanching_rash', 4::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'dengue')
  and exists (select 1 from public.symptoms where id = 'sym_nonblanching_rash')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'dengue' and symptom_id = 'sym_nonblanching_rash');

-- ================================================ sym_conjunctivitis  (Red eyes (conjunctivitis / conjunctival suffusion))
update public.symptoms set description = 'Red eye results from dilated or swollen blood vessels on the surface of the eye. Conjunctivitis involves inflammation with discharge, whereas conjunctival suffusion is redness without purulent discharge that is characteristic of leptospirosis; conjunctivitis is also part of the measles prodrome. Most red eyes are infectious or allergic conjunctivitis, which causes no real pain, no light sensitivity and no corneal staining; viral and bacterial conjunctivitis cannot be told apart reliably on clinical grounds.', updated_at = now()
where id = 'sym_conjunctivitis' and description = 'Red eye results from dilated or swollen blood vessels on the surface of the eye. Conjunctivitis involves inflammation with discharge, whereas conjunctival suffusion is redness without purulent discharge that is characteristic of leptospirosis; conjunctivitis is also part of the measles prodrome.';
update public.symptoms set tags = tags || array['red eye']::text[]
where id = 'sym_conjunctivitis' and not (tags @> array['red eye']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Red Eye'
where id = 'sym_conjunctivitis' and position('Merck Manual Professional - Red Eye' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_conjunctivitis', 'Shingles rash on the forehead or nose tip with a red eye', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_conjunctivitis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_conjunctivitis')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_conjunctivitis' and content = 'Shingles rash on the forehead or nose tip with a red eye');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_conjunctivitis', 'Merck Manual Professional - Red Eye', 'Brady CJ. Red Eye. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Oct 2025.', 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmologic-disorders/red-eye', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_conjunctivitis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_conjunctivitis')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_conjunctivitis' and url = 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmologic-disorders/red-eye');

-- ================================================ sym_retroorbital_pain  (Retro-orbital pain (pain behind the eyes))
update public.symptoms set description = 'Retro-orbital pain is aching or pressure felt behind the eyeball, often worsened by eye movement. In febrile illness it is a characteristic feature of dengue, accompanying severe headache, myalgia and arthralgia; it also occurs with migraine, sinusitis and orbital disease. In dengue it starts abruptly with fever, headache, lower back pain and prostration after a 3 to 15 day incubation; warning signs appear around days 4 to 7. Deep aching or throbbing eye pain in someone without fever suggests serious eye disease such as glaucoma, uveitis, scleritis or orbital cellulitis.', updated_at = now()
where id = 'sym_retroorbital_pain' and description = 'Retro-orbital pain is aching or pressure felt behind the eyeball, often worsened by eye movement. In febrile illness it is a characteristic feature of dengue, accompanying severe headache, myalgia and arthralgia; it also occurs with migraine, sinusitis and orbital disease.';
update public.symptoms set tags = tags || array['dengue warning signs']::text[]
where id = 'sym_retroorbital_pain' and not (tags @> array['dengue warning signs']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Dengue; Merck Manual Professional - Eye Pain'
where id = 'sym_retroorbital_pain' and position('Merck Manual Professional - Dengue' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_retroorbital_pain', 'Glaucoma', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_retroorbital_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_retroorbital_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_retroorbital_pain' and content = 'Glaucoma');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_retroorbital_pain', 'Scleritis or uveitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_retroorbital_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_retroorbital_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_retroorbital_pain' and content = 'Scleritis or uveitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_retroorbital_pain', 'Chikungunya', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_retroorbital_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_retroorbital_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_retroorbital_pain' and content = 'Chikungunya');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_retroorbital_pain', 'Halos around lights with vomiting (possible acute glaucoma)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_retroorbital_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_retroorbital_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_retroorbital_pain' and content = 'Halos around lights with vomiting (possible acute glaucoma)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_retroorbital_pain', 'Merck Manual Professional - Dengue', 'Carmona S. Dengue. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2025.', 'https://www.merckmanuals.com/professional/infectious-diseases/arboviruses-arenaviridae-and-filoviridae/dengue', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_retroorbital_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_retroorbital_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_retroorbital_pain' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/arboviruses-arenaviridae-and-filoviridae/dengue');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_retroorbital_pain', 'Merck Manual Professional - Eye Pain', 'Brady CJ. Eye Pain. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Oct 2025.', 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmologic-disorders/eye-pain', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_retroorbital_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_retroorbital_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_retroorbital_pain' and url = 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmologic-disorders/eye-pain');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'migraine', 'sym_retroorbital_pain', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'migraine')
  and exists (select 1 from public.symptoms where id = 'sym_retroorbital_pain')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'migraine' and symptom_id = 'sym_retroorbital_pain');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'chikungunya', 'sym_retroorbital_pain', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'chikungunya')
  and exists (select 1 from public.symptoms where id = 'sym_retroorbital_pain')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'chikungunya' and symptom_id = 'sym_retroorbital_pain');

-- ================================================ sym_rlq_pain  (Right lower abdominal pain (right lower quadrant))
update public.symptoms set description = 'Pain felt in the right lower part of the abdomen, below the navel and toward the hip bone. In acute appendicitis it typically begins as vague pain around the navel and moves to the right lower quadrant (McBurney point) over 12-24 hours as the inflamed appendix irritates the overlying peritoneum. Ovarian, tubal, urinary tract and bowel conditions can cause pain in the same area. Classic signs include tenderness at McBurney point with rebound, and the Rovsing, psoas and obturator signs, but more than half of patients present atypically, especially older adults and pregnant women. Classic cases are diagnosed clinically, while CT or ultrasound helps when the picture is unclear.', updated_at = now()
where id = 'sym_rlq_pain' and description = 'Pain felt in the right lower part of the abdomen, below the navel and toward the hip bone. In acute appendicitis it typically begins as vague pain around the navel and moves to the right lower quadrant (McBurney point) over 12-24 hours as the inflamed appendix irritates the overlying peritoneum. Ovarian, tubal, urinary tract and bowel conditions can cause pain in the same area.';
update public.symptoms set tags = tags || array['McBurney point']::text[]
where id = 'sym_rlq_pain' and not (tags @> array['McBurney point']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Appendicitis; Merck Manual Professional - Acute Abdominal Pain'
where id = 'sym_rlq_pain' and position('Merck Manual Professional - Appendicitis' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_rlq_pain', 'Typhoid fever (inflamed or perforated ileum)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_rlq_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_rlq_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_rlq_pain' and content = 'Typhoid fever (inflamed or perforated ileum)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_rlq_pain', 'Abdominal pain in a pregnant woman or older adult (appendicitis is often atypical)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_rlq_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_rlq_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_rlq_pain' and content = 'Abdominal pain in a pregnant woman or older adult (appendicitis is often atypical)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_rlq_pain', 'Merck Manual Professional - Appendicitis', 'Ansari P. Appendicitis. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2024.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/acute-abdomen-and-surgical-gastroenterology/appendicitis', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_rlq_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_rlq_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_rlq_pain' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/acute-abdomen-and-surgical-gastroenterology/appendicitis');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_rlq_pain', 'Merck Manual Professional - Acute Abdominal Pain', 'Ansari P. Acute Abdominal Pain. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2024.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/acute-abdomen-and-surgical-gastroenterology/acute-abdominal-pain', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_rlq_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_rlq_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_rlq_pain' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/acute-abdomen-and-surgical-gastroenterology/acute-abdominal-pain');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'typhoid_fever', 'sym_rlq_pain', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'typhoid_fever')
  and exists (select 1 from public.symptoms where id = 'sym_rlq_pain')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'typhoid_fever' and symptom_id = 'sym_rlq_pain');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
