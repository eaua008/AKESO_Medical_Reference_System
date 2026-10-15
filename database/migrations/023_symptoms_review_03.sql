-- 023_symptoms_review_03.sql  -  symptom review, session 03: 10 symptoms
-- Adds only: longer descriptions, extra causes, red flags, references and disease links.
-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).
-- A description is only extended if it is still the exported text (your own edits are kept).

begin;

-- ================================================ sym_hemoptysis  (Coughing up blood (hemoptysis))
update public.symptoms set description = 'Hemoptysis is the expectoration of blood or blood-tinged sputum originating from the lungs or tracheobronchial tree, distinguished from bleeding from the nose, mouth or upper gastrointestinal tract. Massive hemoptysis is a life-threatening emergency. In adults the commonest causes are bronchitis, bronchiectasis, necrotizing pneumonia, tuberculosis and COPD, with lung cancer important in heavy smokers; in children, lower respiratory infection and inhaled foreign bodies predominate. In up to half of patients no cause is found, and most of these settle within 6 months.', updated_at = now()
where id = 'sym_hemoptysis' and description = 'Hemoptysis is the expectoration of blood or blood-tinged sputum originating from the lungs or tracheobronchial tree, distinguished from bleeding from the nose, mouth or upper gastrointestinal tract. Massive hemoptysis is a life-threatening emergency.';
update public.symptoms set tags = tags || array['bronchiectasis']::text[]
where id = 'sym_hemoptysis' and not (tags @> array['bronchiectasis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Hemoptysis'
where id = 'sym_hemoptysis' and position('Merck Manual Professional - Hemoptysis' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hemoptysis', 'COPD flare', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hemoptysis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemoptysis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hemoptysis' and content = 'COPD flare');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hemoptysis', 'Necrotizing pneumonia or lung abscess', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hemoptysis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemoptysis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hemoptysis' and content = 'Necrotizing pneumonia or lung abscess');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hemoptysis', 'Inhaled foreign body (children)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hemoptysis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemoptysis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hemoptysis' and content = 'Inhaled foreign body (children)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hemoptysis', 'Mitral stenosis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hemoptysis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemoptysis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hemoptysis' and content = 'Mitral stenosis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_hemoptysis', 'Any hemoptysis in a heavy smoker', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_hemoptysis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemoptysis')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_hemoptysis' and content = 'Any hemoptysis in a heavy smoker');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_hemoptysis', 'Absent breath sounds on one side or breathlessness at rest', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_hemoptysis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemoptysis')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_hemoptysis' and content = 'Absent breath sounds on one side or breathlessness at rest');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_hemoptysis', 'Merck Manual Professional - Hemoptysis', 'Dezube R. Hemoptysis. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Nov 2025.', 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/hemoptysis', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_hemoptysis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemoptysis')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_hemoptysis' and url = 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/hemoptysis');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'community_acquired_pneumonia', 'sym_hemoptysis', 4::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'community_acquired_pneumonia')
  and exists (select 1 from public.symptoms where id = 'sym_hemoptysis')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'community_acquired_pneumonia' and symptom_id = 'sym_hemoptysis');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'copd', 'sym_hemoptysis', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'copd')
  and exists (select 1 from public.symptoms where id = 'sym_hemoptysis')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'copd' and symptom_id = 'sym_hemoptysis');

-- ================================================ sym_pica  (Craving ice, soil or other non-food items (pica))
update public.symptoms set description = 'Persistent craving for and eating of non-food substances such as ice (pagophagia), clay or soil (geophagia), starch or chalk. Pica is a recognised feature of iron deficiency, with or without anemia, and is also seen in pregnancy, young children and some developmental conditions. It is diagnosed when the eating of non-food material lasts at least a month and is not normal for the person''s age or culture (it is not diagnosed under age 2). Clay can bind iron and zinc and worsen the deficiency, and pica often coexists with autism or intellectual disability.', updated_at = now()
where id = 'sym_pica' and description = 'Persistent craving for and eating of non-food substances such as ice (pagophagia), clay or soil (geophagia), starch or chalk. Pica is a recognised feature of iron deficiency, with or without anemia, and is also seen in pregnancy, young children and some developmental conditions.';
update public.symptoms set tags = tags || array['geophagia', 'pagophagia']::text[]
where id = 'sym_pica' and not (tags @> array['geophagia', 'pagophagia']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Pica'
where id = 'sym_pica' and position('Merck Manual Professional - Pica' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_pica', 'Intellectual disability', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_pica'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pica')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_pica' and content = 'Intellectual disability');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_pica', 'Swallowing hair, sharp objects or other hard items', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_pica'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pica')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_pica' and content = 'Swallowing hair, sharp objects or other hard items');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_pica', 'Merck Manual Professional - Pica', 'Attia E, Walsh BT. Pica. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2025.', 'https://www.merckmanuals.com/professional/psychiatric-disorders/feeding-and-eating-disorders/pica', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_pica'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pica')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_pica' and url = 'https://www.merckmanuals.com/professional/psychiatric-disorders/feeding-and-eating-disorders/pica');

-- ================================================ sym_dark_urine  (Dark urine)
update public.symptoms set description = 'Dark urine is urine that is dark yellow, tea- or cola-coloured. Dark brown clear urine may reflect bilirubinuria from liver disease, while dark urine can also result from severe dehydration, rhabdomyolysis, hemoglobinuria, blood in the urine or certain foods and medicines. Conjugated bilirubin can darken the urine before jaundice is visible, so dark urine is an early sign of hepatitis or bile duct blockage; unconjugated bilirubin (as in hemolysis) does not pass into urine. Several drugs, including rifampicin, phenazopyridine, levodopa, methyldopa and senna, change urine color.', updated_at = now()
where id = 'sym_dark_urine' and description = 'Dark urine is urine that is dark yellow, tea- or cola-coloured. Dark brown clear urine may reflect bilirubinuria from liver disease, while dark urine can also result from severe dehydration, rhabdomyolysis, hemoglobinuria, blood in the urine or certain foods and medicines.';
update public.symptoms set tags = tags || array['bilirubinuria']::text[]
where id = 'sym_dark_urine' and not (tags @> array['bilirubinuria']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Jaundice; Merck Manual Professional - Table: Causes of Urine Color Changes'
where id = 'sym_dark_urine' and position('Merck Manual Professional - Jaundice' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dark_urine', 'Bile duct blockage (gallstones, tumor)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dark_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dark_urine')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dark_urine' and content = 'Bile duct blockage (gallstones, tumor)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dark_urine', 'Leptospirosis (jaundice and kidney involvement)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dark_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dark_urine')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dark_urine' and content = 'Leptospirosis (jaundice and kidney involvement)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dark_urine', 'Specific drugs: rifampicin, phenazopyridine, levodopa, methyldopa, senna', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dark_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dark_urine')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dark_urine' and content = 'Specific drugs: rifampicin, phenazopyridine, levodopa, methyldopa, senna');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_dark_urine', 'Abdominal pain with fever and jaundice (possible cholangitis)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_dark_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dark_urine')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dark_urine' and content = 'Abdominal pain with fever and jaundice (possible cholangitis)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_dark_urine', 'Bruising, small red spots or bleeding', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_dark_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dark_urine')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dark_urine' and content = 'Bruising, small red spots or bleeding');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_dark_urine', 'Merck Manual Professional - Jaundice', 'Tholey D. Jaundice. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2025.', 'https://www.merckmanuals.com/professional/hepatic-and-biliary-disorders/approach-to-the-patient-with-liver-disease/jaundice', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_dark_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dark_urine')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_dark_urine' and url = 'https://www.merckmanuals.com/professional/hepatic-and-biliary-disorders/approach-to-the-patient-with-liver-disease/jaundice');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_dark_urine', 'Merck Manual Professional - Table: Causes of Urine Color Changes', 'Merck & Co. Table: Causes of Urine Color Changes. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; 2026.', 'https://www.merckmanuals.com/professional/multimedia/table/causes-of-urine-color-changes', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_dark_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dark_urine')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_dark_urine' and url = 'https://www.merckmanuals.com/professional/multimedia/table/causes-of-urine-color-changes');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'leptospirosis', 'sym_dark_urine', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'leptospirosis')
  and exists (select 1 from public.symptoms where id = 'sym_dark_urine')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'leptospirosis' and symptom_id = 'sym_dark_urine');

-- ================================================ sym_decreased_urine  (Decreased urine output (oliguria))
update public.symptoms set description = 'Oliguria is reduced urine output, commonly defined in adults as less than 400 mL per day (or below about 0.5 mL/kg/h). Causes are classified as prerenal (reduced kidney perfusion, e.g., dehydration or shock), intrinsic renal and postrenal (urinary obstruction). Some references use under 500 mL in 24 hours for adults, and under 1 mL/kg/h in newborns. A palpable bladder suggests outlet obstruction, a sudden drop in a catheterised patient with normal blood pressure suggests a blocked catheter, and dark brown urine suggests myoglobin from muscle breakdown.', updated_at = now()
where id = 'sym_decreased_urine' and description = 'Oliguria is reduced urine output, commonly defined in adults as less than 400 mL per day (or below about 0.5 mL/kg/h). Causes are classified as prerenal (reduced kidney perfusion, e.g., dehydration or shock), intrinsic renal and postrenal (urinary obstruction).';
update public.symptoms set tags = tags || array['oliguria']::text[]
where id = 'sym_decreased_urine' and not (tags @> array['oliguria']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Oliguria'
where id = 'sym_decreased_urine' and position('Merck Manual Professional - Oliguria' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_decreased_urine', 'Kidney stones or enlarged prostate', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_decreased_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_decreased_urine')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_decreased_urine' and content = 'Kidney stones or enlarged prostate');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_decreased_urine', 'Muscle breakdown (rhabdomyolysis)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_decreased_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_decreased_urine')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_decreased_urine' and content = 'Muscle breakdown (rhabdomyolysis)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_decreased_urine', 'Severe dengue with plasma leakage', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_decreased_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_decreased_urine')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_decreased_urine' and content = 'Severe dengue with plasma leakage');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_decreased_urine', 'Full, palpable bladder with inability to pass urine', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_decreased_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_decreased_urine')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_decreased_urine' and content = 'Full, palpable bladder with inability to pass urine');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_decreased_urine', 'Dark brown urine with muscle pain (possible rhabdomyolysis)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_decreased_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_decreased_urine')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_decreased_urine' and content = 'Dark brown urine with muscle pain (possible rhabdomyolysis)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_decreased_urine', 'Merck Manual Professional - Oliguria', 'Berry C. Oliguria. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Oct 2025.', 'https://www.merckmanuals.com/professional/critical-care-medicine/approach-to-the-critically-ill-patient/oliguria', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_decreased_urine'), 0)
where exists (select 1 from public.symptoms where id = 'sym_decreased_urine')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_decreased_urine' and url = 'https://www.merckmanuals.com/professional/critical-care-medicine/approach-to-the-critically-ill-patient/oliguria');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'dengue', 'sym_decreased_urine', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'dengue')
  and exists (select 1 from public.symptoms where id = 'sym_decreased_urine')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'dengue' and symptom_id = 'sym_decreased_urine');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'heart_failure', 'sym_decreased_urine', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.symptoms where id = 'sym_decreased_urine')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'heart_failure' and symptom_id = 'sym_decreased_urine');

-- ================================================ sym_diarrhea  (Diarrhea)
update public.symptoms set description = 'Diarrhea is the passage of loose or watery stools, typically three or more times a day. Acute diarrhea is most often infectious, while chronic diarrhea suggests malabsorptive, inflammatory or functional disease. It arises from too much osmotic load, increased secretion or reduced absorption, or fast transit, and infection is the commonest cause of acute secretory diarrhea. Diarrhea that wakes the patient at night, comes with weight loss or lasts weeks points to an organic cause rather than irritable bowel syndrome.', updated_at = now()
where id = 'sym_diarrhea' and description = 'Diarrhea is the passage of loose or watery stools, typically three or more times a day. Acute diarrhea is most often infectious, while chronic diarrhea suggests malabsorptive, inflammatory or functional disease.';
update public.symptoms set tags = tags || array['malabsorption']::text[]
where id = 'sym_diarrhea' and not (tags @> array['malabsorption']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Diarrhea'
where id = 'sym_diarrhea' and position('Merck Manual Professional - Diarrhea' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_diarrhea', 'Celiac disease and lactose intolerance', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_diarrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diarrhea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_diarrhea' and content = 'Celiac disease and lactose intolerance');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_diarrhea', 'Overactive thyroid', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_diarrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diarrhea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_diarrhea' and content = 'Overactive thyroid');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_diarrhea', 'Laxative misuse', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_diarrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diarrhea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_diarrhea' and content = 'Laxative misuse');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_diarrhea', 'Clostridioides difficile after antibiotics', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_diarrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diarrhea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_diarrhea' and content = 'Clostridioides difficile after antibiotics');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_diarrhea', 'Diarrhea that wakes the patient at night, or with weight loss', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_diarrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diarrhea')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_diarrhea' and content = 'Diarrhea that wakes the patient at night, or with weight loss');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_diarrhea', 'Recent antibiotics or hospital stay (possible C. difficile)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_diarrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diarrhea')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_diarrhea' and content = 'Recent antibiotics or hospital stay (possible C. difficile)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_diarrhea', 'Merck Manual Professional - Diarrhea', 'Gotfried J. Diarrhea. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Apr 2026.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/symptoms-of-gastrointestinal-disorders/diarrhea', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_diarrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_diarrhea')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_diarrhea' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/symptoms-of-gastrointestinal-disorders/diarrhea');

-- ================================================ sym_dysphagia  (Difficulty swallowing (dysphagia))
update public.symptoms set description = 'A sensation that food or liquid sticks or passes slowly on the way from the mouth to the stomach. Oropharyngeal dysphagia (trouble starting a swallow, coughing or choking) usually has a neurologic or muscular cause, while esophageal dysphagia (food sticking behind the breastbone) suggests a stricture, ring, motility disorder or tumor. In GERD it is an alarm feature. Oropharyngeal dysphagia usually comes from nerve or muscle disease such as stroke, Parkinson disease or myasthenia gravis; esophageal dysphagia comes from motility disorders or mechanical narrowing. Upper endoscopy is the usual first test, with biopsies for eosinophilic esophagitis if no structural cause is seen.', updated_at = now()
where id = 'sym_dysphagia' and description = 'A sensation that food or liquid sticks or passes slowly on the way from the mouth to the stomach. Oropharyngeal dysphagia (trouble starting a swallow, coughing or choking) usually has a neurologic or muscular cause, while esophageal dysphagia (food sticking behind the breastbone) suggests a stricture, ring, motility disorder or tumor. In GERD it is an alarm feature.';
update public.symptoms set tags = tags || array['oropharyngeal']::text[]
where id = 'sym_dysphagia' and not (tags @> array['oropharyngeal']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Dysphagia'
where id = 'sym_dysphagia' and position('Merck Manual Professional - Dysphagia' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dysphagia', 'Parkinson disease or myasthenia gravis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dysphagia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dysphagia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dysphagia' and content = 'Parkinson disease or myasthenia gravis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dysphagia', 'Rabies (painful throat spasms)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dysphagia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dysphagia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dysphagia' and content = 'Rabies (painful throat spasms)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_dysphagia', 'Repeated chest infections from aspiration', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_dysphagia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dysphagia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dysphagia' and content = 'Repeated chest infections from aspiration');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_dysphagia', 'Merck Manual Professional - Dysphagia', 'Lynch KL. Dysphagia. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2026.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/esophageal-and-swallowing-disorders/dysphagia', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_dysphagia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dysphagia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_dysphagia' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/esophageal-and-swallowing-disorders/dysphagia');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'ischemic_stroke', 'sym_dysphagia', 4::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'ischemic_stroke')
  and exists (select 1 from public.symptoms where id = 'sym_dysphagia')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'ischemic_stroke' and symptom_id = 'sym_dysphagia');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'rabies', 'sym_dysphagia', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'rabies')
  and exists (select 1 from public.symptoms where id = 'sym_dysphagia')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'rabies' and symptom_id = 'sym_dysphagia');

-- ================================================ sym_dizziness  (Dizziness / lightheadedness)
update public.symptoms set description = 'Dizziness is a term used for two main symptoms: lightheadedness (a feeling of faintness) and vertigo (a false sense of spinning or movement). Lightheadedness often reflects reduced blood flow to the brain, while vertigo usually reflects inner ear or brainstem disease. Common inner-ear causes are benign positional vertigo, Meniere disease and vestibular neuritis or labyrinthitis; the commonest central cause is vestibular migraine, followed by drug effects, especially blood pressure medicines. Ringing, fullness or hearing loss in the ear suggests an inner-ear cause, whereas nystagmus that is not suppressed by fixing the gaze suggests a central cause.', updated_at = now()
where id = 'sym_dizziness' and description = 'Dizziness is a term used for two main symptoms: lightheadedness (a feeling of faintness) and vertigo (a false sense of spinning or movement). Lightheadedness often reflects reduced blood flow to the brain, while vertigo usually reflects inner ear or brainstem disease.';
update public.symptoms set tags = tags || array['vertigo']::text[]
where id = 'sym_dizziness' and not (tags @> array['vertigo']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Dizziness and Vertigo'
where id = 'sym_dizziness' and position('Merck Manual Professional - Dizziness and Vertigo' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dizziness', 'Meniere disease', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dizziness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dizziness')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dizziness' and content = 'Meniere disease');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dizziness', 'Vestibular migraine', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dizziness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dizziness')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dizziness' and content = 'Vestibular migraine');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dizziness', 'Labyrinthitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dizziness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dizziness')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dizziness' and content = 'Labyrinthitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dizziness', 'Severe dengue with low blood pressure', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dizziness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dizziness')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dizziness' and content = 'Severe dengue with low blood pressure');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_dizziness', 'Unsteady walking or inability to stand', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_dizziness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dizziness')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dizziness' and content = 'Unsteady walking or inability to stand');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_dizziness', 'Constant severe vertigo lasting more than an hour', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_dizziness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dizziness')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dizziness' and content = 'Constant severe vertigo lasting more than an hour');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_dizziness', 'Merck Manual Professional - Dizziness and Vertigo', 'Formeister EJ. Dizziness and Vertigo. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jan 2025.', 'https://www.merckmanuals.com/professional/ear-nose-and-throat-disorders/approach-to-the-patient-with-ear-problems/dizziness-and-vertigo', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_dizziness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dizziness')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_dizziness' and url = 'https://www.merckmanuals.com/professional/ear-nose-and-throat-disorders/approach-to-the-patient-with-ear-problems/dizziness-and-vertigo');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'dengue', 'sym_dizziness', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'dengue')
  and exists (select 1 from public.symptoms where id = 'sym_dizziness')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'dengue' and symptom_id = 'sym_dizziness');

-- ================================================ sym_epigastric_pain  (Epigastric pain)
update public.symptoms set description = 'Epigastric pain is pain or burning located in the upper central abdomen below the xiphoid process. It is characteristic of peptic ulcer disease, gastritis and functional dyspepsia, but cardiac, biliary and pancreatic disease may also present here. Medicines such as NSAIDs, opioids and iron, delayed stomach emptying and celiac disease can also cause it, and when all tests are normal the diagnosis is functional dyspepsia. If ischemia is possible, cardiac causes are checked first; endoscopy is advised for new symptoms after about age 60.', updated_at = now()
where id = 'sym_epigastric_pain' and description = 'Epigastric pain is pain or burning located in the upper central abdomen below the xiphoid process. It is characteristic of peptic ulcer disease, gastritis and functional dyspepsia, but cardiac, biliary and pancreatic disease may also present here.';
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Dyspepsia'
where id = 'sym_epigastric_pain' and position('Merck Manual Professional - Dyspepsia' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_epigastric_pain', 'Medicines (NSAIDs, opioids, iron)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_epigastric_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_epigastric_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_epigastric_pain' and content = 'Medicines (NSAIDs, opioids, iron)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_epigastric_pain', 'Stomach or esophageal cancer', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_epigastric_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_epigastric_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_epigastric_pain' and content = 'Stomach or esophageal cancer');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_epigastric_pain', 'Myocardial ischemia', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_epigastric_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_epigastric_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_epigastric_pain' and content = 'Myocardial ischemia');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_epigastric_pain', 'Early appendicitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_epigastric_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_epigastric_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_epigastric_pain' and content = 'Early appendicitis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_epigastric_pain', 'New symptoms after age 60', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_epigastric_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_epigastric_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_epigastric_pain' and content = 'New symptoms after age 60');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_epigastric_pain', 'Symptoms not improving on acid-suppressing medicine', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_epigastric_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_epigastric_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_epigastric_pain' and content = 'Symptoms not improving on acid-suppressing medicine');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_epigastric_pain', 'Merck Manual Professional - Dyspepsia', 'Gotfried J. Dyspepsia. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Apr 2026.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/symptoms-of-gastrointestinal-disorders/dyspepsia', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_epigastric_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_epigastric_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_epigastric_pain' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/symptoms-of-gastrointestinal-disorders/dyspepsia');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'acute_appendicitis', 'sym_epigastric_pain', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'acute_appendicitis')
  and exists (select 1 from public.symptoms where id = 'sym_epigastric_pain')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'acute_appendicitis' and symptom_id = 'sym_epigastric_pain');

-- ================================================ sym_hypersalivation  (Excessive salivation / drooling)
update public.symptoms set description = 'Hypersalivation and drooling result from excess saliva production or, more often, from an inability to retain or swallow normal saliva. Causes range from oral and pharyngeal infections to neurologic disorders that impair swallowing, and in rabies drooling reflects both autonomic stimulation and painful pharyngeal spasms. In children, drooling without a barking cough strongly suggests epiglottitis rather than croup, and drooling with stridor means the airway may need urgent securing; the child should not be upset or examined in the throat until then. Excess saliva with tears, sweating, small pupils and muscle twitching suggests organophosphate poisoning.', updated_at = now()
where id = 'sym_hypersalivation' and description = 'Hypersalivation and drooling result from excess saliva production or, more often, from an inability to retain or swallow normal saliva. Causes range from oral and pharyngeal infections to neurologic disorders that impair swallowing, and in rabies drooling reflects both autonomic stimulation and painful pharyngeal spasms.';
update public.symptoms set tags = tags || array['epiglottitis', 'poisoning']::text[]
where id = 'sym_hypersalivation' and not (tags @> array['epiglottitis', 'poisoning']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Organophosphate Poisoning and Carbamate Poisoning; Merck Manual Professional - Epiglottitis'
where id = 'sym_hypersalivation' and position('Merck Manual Professional - Organophosphate Poisoning and Carbamate Poisoning' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hypersalivation', 'Epiglottitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hypersalivation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hypersalivation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hypersalivation' and content = 'Epiglottitis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_hypersalivation', 'Small pupils, sweating, vomiting and muscle twitching (possible organophosphate poisoning)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_hypersalivation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hypersalivation')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_hypersalivation' and content = 'Small pupils, sweating, vomiting and muscle twitching (possible organophosphate poisoning)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_hypersalivation', 'Merck Manual Professional - Organophosphate Poisoning and Carbamate Poisoning', 'O''Malley GF, O''Malley R. Organophosphate Poisoning and Carbamate Poisoning. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Apr 2025.', 'https://www.merckmanuals.com/professional/injuries-poisoning/poisoning/organophosphate-poisoning-and-carbamate-poisoning', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_hypersalivation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hypersalivation')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_hypersalivation' and url = 'https://www.merckmanuals.com/professional/injuries-poisoning/poisoning/organophosphate-poisoning-and-carbamate-poisoning');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_hypersalivation', 'Merck Manual Professional - Epiglottitis', 'Cheng AG. Epiglottitis. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2026.', 'https://www.merckmanuals.com/professional/ear-nose-and-throat-disorders/oral-and-pharyngeal-disorders/epiglottitis', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_hypersalivation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hypersalivation')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_hypersalivation' and url = 'https://www.merckmanuals.com/professional/ear-nose-and-throat-disorders/oral-and-pharyngeal-disorders/epiglottitis');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'hfmd', 'sym_hypersalivation', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'hfmd')
  and exists (select 1 from public.symptoms where id = 'sym_hypersalivation')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'hfmd' and symptom_id = 'sym_hypersalivation');

-- ================================================ sym_polydipsia  (Excessive thirst (polydipsia))
update public.symptoms set description = 'Polydipsia is an abnormal, persistent feeling of needing to drink fluids. It usually accompanies polyuria and dehydration, and is a classic symptom of uncontrolled diabetes mellitus. Diabetes mellitus is the commonest cause of thirst with heavy urination; others are diuretics, diabetes insipidus and primary polydipsia. People with primary polydipsia may drink up to 6 L a day and usually do not wake at night to pass urine; drinking that much can cause dangerously low sodium.', updated_at = now()
where id = 'sym_polydipsia' and description = 'Polydipsia is an abnormal, persistent feeling of needing to drink fluids. It usually accompanies polyuria and dehydration, and is a classic symptom of uncontrolled diabetes mellitus.';
update public.symptoms set tags = tags || array['diabetes insipidus']::text[]
where id = 'sym_polydipsia' and not (tags @> array['diabetes insipidus']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Arginine Vasopressin Deficiency (Central Diabetes Insipidus)'
where id = 'sym_polydipsia' and position('Merck Manual Professional - Arginine Vasopressin Deficiency (Central Diabetes Insipidus)' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_polydipsia', 'Nephrogenic diabetes insipidus (vasopressin resistance)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_polydipsia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_polydipsia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_polydipsia' and content = 'Nephrogenic diabetes insipidus (vasopressin resistance)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_polydipsia', 'Headache, vomiting or confusion after drinking very large amounts (possible low sodium)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_polydipsia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_polydipsia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_polydipsia' and content = 'Headache, vomiting or confusion after drinking very large amounts (possible low sodium)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_polydipsia', 'Merck Manual Professional - Arginine Vasopressin Deficiency (Central Diabetes Insipidus)', 'Carmichael JD. Arginine Vasopressin Deficiency (Central Diabetes Insipidus). Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2025.', 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/pituitary-disorders/arginine-vasopressin-deficiency-central-diabetes-insipidus', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_polydipsia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_polydipsia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_polydipsia' and url = 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/pituitary-disorders/arginine-vasopressin-deficiency-central-diabetes-insipidus');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
