-- 028_symptoms_review_08.sql  -  symptom review, session 08: 10 symptoms
-- Adds only: longer descriptions, extra causes, red flags, references and disease links.
-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).
-- A description is only extended if it is still the exported text (your own edits are kept).

begin;

-- ================================================ sym_ruq_pain  (Right upper abdominal pain (right upper quadrant))
update public.symptoms set description = 'Right upper quadrant pain is pain localized beneath the right costal margin, overlying the liver, gallbladder and biliary tree, with contributions from the duodenum, right kidney, hepatic flexure and right lung base. Biliary pain is often steady and may radiate to the right scapula, whereas hepatic pain from capsular stretch is usually a dull ache accompanying hepatitis or congestion. Acute cholecystitis feels like biliary colic but is more severe and lasts over 6 hours, with a positive Murphy sign and guarding; ultrasound is the best first test. In dengue, abdominal pain and an enlarging liver are warning signs of severe disease.', updated_at = now()
where id = 'sym_ruq_pain' and description = 'Right upper quadrant pain is pain localized beneath the right costal margin, overlying the liver, gallbladder and biliary tree, with contributions from the duodenum, right kidney, hepatic flexure and right lung base. Biliary pain is often steady and may radiate to the right scapula, whereas hepatic pain from capsular stretch is usually a dull ache accompanying hepatitis or congestion.';
update public.symptoms set tags = tags || array['Murphy sign']::text[]
where id = 'sym_ruq_pain' and not (tags @> array['Murphy sign']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Acute Cholecystitis; Merck Manual Professional - Acute Abdominal Pain'
where id = 'sym_ruq_pain' and position('Merck Manual Professional - Acute Cholecystitis' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_ruq_pain', 'Right kidney stone or kidney infection', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_ruq_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_ruq_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_ruq_pain' and content = 'Right kidney stone or kidney infection');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_ruq_pain', 'Dengue (enlarged, tender liver)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_ruq_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_ruq_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_ruq_pain' and content = 'Dengue (enlarged, tender liver)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_ruq_pain', 'Pain lasting more than 6 hours with fever (possible acute cholecystitis)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_ruq_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_ruq_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_ruq_pain' and content = 'Pain lasting more than 6 hours with fever (possible acute cholecystitis)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_ruq_pain', 'Merck Manual Professional - Acute Cholecystitis', 'Saiman Y. Acute Cholecystitis. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Oct 2025.', 'https://www.merckmanuals.com/professional/hepatic-and-biliary-disorders/gallbladder-and-bile-duct-disorders/acute-cholecystitis', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_ruq_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_ruq_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_ruq_pain' and url = 'https://www.merckmanuals.com/professional/hepatic-and-biliary-disorders/gallbladder-and-bile-duct-disorders/acute-cholecystitis');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_ruq_pain', 'Merck Manual Professional - Acute Abdominal Pain', 'Ansari P. Acute Abdominal Pain. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2024.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/acute-abdomen-and-surgical-gastroenterology/acute-abdominal-pain', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_ruq_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_ruq_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_ruq_pain' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/acute-abdomen-and-surgical-gastroenterology/acute-abdominal-pain');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'dengue', 'sym_ruq_pain', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'dengue')
  and exists (select 1 from public.symptoms where id = 'sym_ruq_pain')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'dengue' and symptom_id = 'sym_ruq_pain');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'heart_failure', 'sym_ruq_pain', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.symptoms where id = 'sym_ruq_pain')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'heart_failure' and symptom_id = 'sym_ruq_pain');

-- ================================================ sym_rhinorrhea  (Runny nose (coryza))
update public.symptoms set description = 'Rhinorrhea is discharge of fluid from the nose, often with nasal congestion, caused by inflamed nasal mucosa and blood vessels. Coryza (runny nose with sneezing and congestion) is typical of viral upper respiratory infections and is part of the measles prodrome. Rhinoviruses cause about half of colds; symptoms start 1 to 3 days after exposure and usually clear within about 10 days. Thick, colored mucus does not by itself mean a bacterial infection.', updated_at = now()
where id = 'sym_rhinorrhea' and description = 'Rhinorrhea is discharge of fluid from the nose, often with nasal congestion, caused by inflamed nasal mucosa and blood vessels. Coryza (runny nose with sneezing and congestion) is typical of viral upper respiratory infections and is part of the measles prodrome.';
update public.symptoms set tags = tags || array['common cold']::text[]
where id = 'sym_rhinorrhea' and not (tags @> array['common cold']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Common Cold'
where id = 'sym_rhinorrhea' and position('Merck Manual Professional - Common Cold' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_rhinorrhea', 'Symptoms lasting more than 10 days, or worsening after first improving (possible bacterial sinusitis)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_rhinorrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_rhinorrhea')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_rhinorrhea' and content = 'Symptoms lasting more than 10 days, or worsening after first improving (possible bacterial sinusitis)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_rhinorrhea', 'Merck Manual Professional - Common Cold', 'Katz S. Common Cold. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2026.', 'https://www.merckmanuals.com/professional/infectious-diseases/respiratory-viruses/common-cold', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_rhinorrhea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_rhinorrhea')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_rhinorrhea' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/respiratory-viruses/common-cold');

-- ================================================ sym_seizures  (Seizures (fits or convulsions))
update public.symptoms set description = 'Episodes of abnormal electrical activity in the brain causing jerking movements, stiffening, staring or loss of awareness. A first seizure, a seizure with fever in an adult, or one lasting more than 5 minutes needs urgent medical assessment. Status epilepticus is a convulsion lasting more than 5 minutes or repeated seizures without recovery in between, and needs an IV benzodiazepine promptly. Tongue biting, incontinence and prolonged confusion afterwards favour a seizure over a faint.', updated_at = now()
where id = 'sym_seizures' and description = 'Episodes of abnormal electrical activity in the brain causing jerking movements, stiffening, staring or loss of awareness. A first seizure, a seizure with fever in an adult, or one lasting more than 5 minutes needs urgent medical assessment.';
update public.symptoms set tags = tags || array['status epilepticus']::text[]
where id = 'sym_seizures' and not (tags @> array['status epilepticus']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Seizure Disorders'
where id = 'sym_seizures' and position('Merck Manual Professional - Seizure Disorders' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_seizures', 'Brain tumor', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_seizures'), 0)
where exists (select 1 from public.symptoms where id = 'sym_seizures')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_seizures' and content = 'Brain tumor');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_seizures', 'Drug toxicity', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_seizures'), 0)
where exists (select 1 from public.symptoms where id = 'sym_seizures')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_seizures' and content = 'Drug toxicity');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_seizures', 'Cerebral malaria', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_seizures'), 0)
where exists (select 1 from public.symptoms where id = 'sym_seizures')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_seizures' and content = 'Cerebral malaria');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_seizures', 'Seizure in someone with cancer or a weakened immune system', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_seizures'), 0)
where exists (select 1 from public.symptoms where id = 'sym_seizures')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_seizures' and content = 'Seizure in someone with cancer or a weakened immune system');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_seizures', 'Merck Manual Professional - Seizure Disorders', 'Adamolekun B. Seizure Disorders. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2026.', 'https://www.merckmanuals.com/professional/neurologic-disorders/seizure-disorders/seizure-disorders', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_seizures'), 0)
where exists (select 1 from public.symptoms where id = 'sym_seizures')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_seizures' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/seizure-disorders/seizure-disorders');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'malaria', 'sym_seizures', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'malaria')
  and exists (select 1 from public.symptoms where id = 'sym_seizures')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'malaria' and symptom_id = 'sym_seizures');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'rabies', 'sym_seizures', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'rabies')
  and exists (select 1 from public.symptoms where id = 'sym_seizures')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'rabies' and symptom_id = 'sym_seizures');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'ischemic_stroke', 'sym_seizures', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'ischemic_stroke')
  and exists (select 1 from public.symptoms where id = 'sym_seizures')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'ischemic_stroke' and symptom_id = 'sym_seizures');

-- ================================================ sym_photophobia  (Sensitivity to light (photophobia))
update public.symptoms set description = 'Photophobia is discomfort or pain in the eyes in response to bright light. It is a common feature of migraine and also occurs with meningitis, subarachnoid hemorrhage and inflammatory eye disease. In true photophobia from eye disease, light shone into the healthy eye causes pain in the affected eye, as with corneal injury or uveitis. In migraine it comes with nausea and sensitivity to sound and smells, and patients prefer a dark, quiet room.', updated_at = now()
where id = 'sym_photophobia' and description = 'Photophobia is discomfort or pain in the eyes in response to bright light. It is a common feature of migraine and also occurs with meningitis, subarachnoid hemorrhage and inflammatory eye disease.';
update public.symptoms set tags = tags || array['uveitis']::text[]
where id = 'sym_photophobia' and not (tags @> array['uveitis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Eye Pain; Merck Manual Professional - Migraine'
where id = 'sym_photophobia' and position('Merck Manual Professional - Eye Pain' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_photophobia', 'Halos around lights or vomiting with eye pain (possible acute glaucoma)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_photophobia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_photophobia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_photophobia' and content = 'Halos around lights or vomiting with eye pain (possible acute glaucoma)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_photophobia', 'Merck Manual Professional - Eye Pain', 'Brady CJ. Eye Pain. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Oct 2025.', 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmologic-disorders/eye-pain', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_photophobia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_photophobia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_photophobia' and url = 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmologic-disorders/eye-pain');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_photophobia', 'Merck Manual Professional - Migraine', 'Silberstein SD. Migraine. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2025.', 'https://www.merckmanuals.com/professional/neurologic-disorders/headache/migraine', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_photophobia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_photophobia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_photophobia' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/headache/migraine');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'measles', 'sym_photophobia', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'measles')
  and exists (select 1 from public.symptoms where id = 'sym_photophobia')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'measles' and symptom_id = 'sym_photophobia');

-- ================================================ sym_tremor  (Shaky hands (tremor))
update public.symptoms set description = 'Rhythmic, involuntary shaking, most often of the hands. A fine, fast tremor seen with arms outstretched is typical of hyperthyroidism, anxiety and stimulants; a slower tremor at rest suggests Parkinson disease. A tremor while reaching for a target (intention tremor) suggests cerebellar disease. Hyperthyroidism and drugs such as lithium, SSRIs, valproate and theophylline cause or worsen tremor.', updated_at = now()
where id = 'sym_tremor' and description = 'Rhythmic, involuntary shaking, most often of the hands. A fine, fast tremor seen with arms outstretched is typical of hyperthyroidism, anxiety and stimulants; a slower tremor at rest suggests Parkinson disease.';
update public.symptoms set tags = tags || array['essential tremor']::text[]
where id = 'sym_tremor' and not (tags @> array['essential tremor']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Tremor'
where id = 'sym_tremor' and position('Merck Manual Professional - Tremor' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_tremor', 'Cerebellar disease (tremor on reaching for a target)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_tremor'), 0)
where exists (select 1 from public.symptoms where id = 'sym_tremor')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_tremor' and content = 'Cerebellar disease (tremor on reaching for a target)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_tremor', 'SSRIs and theophylline', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_tremor'), 0)
where exists (select 1 from public.symptoms where id = 'sym_tremor')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_tremor' and content = 'SSRIs and theophylline');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_tremor', 'Tremor starting before age 50 with no family history', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_tremor'), 0)
where exists (select 1 from public.symptoms where id = 'sym_tremor')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_tremor' and content = 'Tremor starting before age 50 with no family history');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_tremor', 'Merck Manual Professional - Tremor', 'Rajput A, Noyes E. Tremor. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2026.', 'https://www.merckmanuals.com/professional/neurologic-disorders/movement-and-cerebellar-disorders/tremor', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_tremor'), 0)
where exists (select 1 from public.symptoms where id = 'sym_tremor')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_tremor' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/movement-and-cerebellar-disorders/tremor');

-- ================================================ sym_dyspnea  (Shortness of breath (dyspnea))
update public.symptoms set description = 'Dyspnea is a subjective sensation of uncomfortable or difficult breathing, or of not getting enough air. It arises from respiratory, cardiac, metabolic, hematologic and psychological causes, and severe or sudden dyspnea can indicate a life-threatening condition. Wheeze points to asthma or COPD, stridor to upper airway obstruction, and crackles to heart failure, pneumonia or interstitial lung disease. A normal oxygen saturation does not exclude pulmonary embolism.', updated_at = now()
where id = 'sym_dyspnea' and description = 'Dyspnea is a subjective sensation of uncomfortable or difficult breathing, or of not getting enough air. It arises from respiratory, cardiac, metabolic, hematologic and psychological causes, and severe or sudden dyspnea can indicate a life-threatening condition.';
update public.symptoms set tags = tags || array['wheeze']::text[]
where id = 'sym_dyspnea' and not (tags @> array['wheeze']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Dyspnea'
where id = 'sym_dyspnea' and position('Merck Manual Professional - Dyspnea' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dyspnea', 'Pneumothorax', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dyspnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dyspnea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dyspnea' and content = 'Pneumothorax');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dyspnea', 'Interstitial lung disease', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dyspnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dyspnea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dyspnea' and content = 'Interstitial lung disease');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dyspnea', 'Physical deconditioning', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dyspnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dyspnea')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dyspnea' and content = 'Physical deconditioning');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_dyspnea', 'Using the neck and shoulder muscles to breathe', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_dyspnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dyspnea')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dyspnea' and content = 'Using the neck and shoulder muscles to breathe');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_dyspnea', 'Merck Manual Professional - Dyspnea', 'Dezube R. Dyspnea. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Nov 2025.', 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/dyspnea', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_dyspnea'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dyspnea')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_dyspnea' and url = 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/dyspnea');

-- ================================================ sym_dehydration  (Signs of dehydration (sunken eyes, dry mouth, intense thirst))
update public.symptoms set description = 'Dehydration is a deficit of body water and electrolytes from fluid losses exceeding intake, most often from diarrhea, vomiting, fever, sweating or osmotic diuresis. Clinical signs progress from thirst, dry mucous membranes and reduced dark urine to sunken eyes, reduced skin turgor, tachycardia, confusion and hypovolemic shock. Mild volume loss (under 5%) gives thirst and reduced urine; moderate loss (5 to 10%) adds dizziness on standing; severe loss (over 10%) leads to shock with low blood pressure, confusion and slow capillary refill. Skin turgor and a dry mouth are unreliable signs in older adults.', updated_at = now()
where id = 'sym_dehydration' and description = 'Dehydration is a deficit of body water and electrolytes from fluid losses exceeding intake, most often from diarrhea, vomiting, fever, sweating or osmotic diuresis. Clinical signs progress from thirst, dry mucous membranes and reduced dark urine to sunken eyes, reduced skin turgor, tachycardia, confusion and hypovolemic shock.';
update public.symptoms set tags = tags || array['volume depletion']::text[]
where id = 'sym_dehydration' and not (tags @> array['volume depletion']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Volume Depletion'
where id = 'sym_dehydration' and position('Merck Manual Professional - Volume Depletion' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dehydration', 'Burns or bleeding', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dehydration'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dehydration')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dehydration' and content = 'Burns or bleeding');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_dehydration', 'Infant or older adult with ongoing diarrhea or vomiting', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_dehydration'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dehydration')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dehydration' and content = 'Infant or older adult with ongoing diarrhea or vomiting');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_dehydration', 'Merck Manual Professional - Volume Depletion', 'Lewis JL III. Volume Depletion. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jun 2026.', 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/fluid-metabolism/volume-depletion', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_dehydration'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dehydration')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_dehydration' and url = 'https://www.merckmanuals.com/professional/endocrine-and-metabolic-disorders/fluid-metabolism/volume-depletion');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'acute_gastroenteritis', 'sym_dehydration', 5::smallint, false, 0.6::numeric
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.symptoms where id = 'sym_dehydration')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'acute_gastroenteritis' and symptom_id = 'sym_dehydration');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'type2_diabetes', 'sym_dehydration', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'type2_diabetes')
  and exists (select 1 from public.symptoms where id = 'sym_dehydration')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'type2_diabetes' and symptom_id = 'sym_dehydration');

-- ================================================ sym_rash  (Skin rash)
update public.symptoms set description = 'A rash is a change in the colour, texture or feel of the skin, which may be macular, papular, vesicular, petechial or urticarial. In febrile illness, a generalized exanthem accompanies many viral infections (e.g., measles, dengue) and some bacterial and drug-related conditions. Lesions are described by their size (under or over 10 mm) and type, and their arrangement gives clues: target lesions suggest erythema multiforme, grouped vesicles herpes simplex, and a band on one side zoster. Redness can be subtle on darker skin.', updated_at = now()
where id = 'sym_rash' and description = 'A rash is a change in the colour, texture or feel of the skin, which may be macular, papular, vesicular, petechial or urticarial. In febrile illness, a generalized exanthem accompanies many viral infections (e.g., measles, dengue) and some bacterial and drug-related conditions.';
update public.symptoms set tags = tags || array['morphology']::text[]
where id = 'sym_rash' and not (tags @> array['morphology']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Description of Skin Lesions'
where id = 'sym_rash' and position('Merck Manual Professional - Description of Skin Lesions' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_rash', 'Erythema multiforme', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_rash'), 0)
where exists (select 1 from public.symptoms where id = 'sym_rash')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_rash' and content = 'Erythema multiforme');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_rash', 'A black, scab-like sore (eschar)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_rash'), 0)
where exists (select 1 from public.symptoms where id = 'sym_rash')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_rash' and content = 'A black, scab-like sore (eschar)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_rash', 'Merck Manual Professional - Description of Skin Lesions', 'Benedetti J. Description of Skin Lesions. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2026.', 'https://www.merckmanuals.com/professional/dermatologic-disorders/approach-to-the-dermatologic-patient/description-of-skin-lesions', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_rash'), 0)
where exists (select 1 from public.symptoms where id = 'sym_rash')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_rash' and url = 'https://www.merckmanuals.com/professional/dermatologic-disorders/approach-to-the-dermatologic-patient/description-of-skin-lesions');

-- ================================================ sym_speech_difficulty  (Slurred or difficult speech)
update public.symptoms set description = 'Speech difficulty includes dysarthria (slurred, poorly articulated speech from weakness or incoordination of speech muscles) and aphasia (impaired production or comprehension of language from injury to the dominant hemisphere). Sudden onset is a classic warning sign of stroke. In Broca (expressive) aphasia speech is halting but understanding is preserved; in Wernicke (receptive) aphasia speech flows but makes little sense and understanding is poor. Assessment covers spontaneous speech, naming, repetition and comprehension, followed by brain imaging.', updated_at = now()
where id = 'sym_speech_difficulty' and description = 'Speech difficulty includes dysarthria (slurred, poorly articulated speech from weakness or incoordination of speech muscles) and aphasia (impaired production or comprehension of language from injury to the dominant hemisphere). Sudden onset is a classic warning sign of stroke.';
update public.symptoms set tags = tags || array['aphasia', 'dysarthria']::text[]
where id = 'sym_speech_difficulty' and not (tags @> array['aphasia', 'dysarthria']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Aphasia'
where id = 'sym_speech_difficulty' and position('Merck Manual Professional - Aphasia' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_speech_difficulty', 'Encephalitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_speech_difficulty'), 0)
where exists (select 1 from public.symptoms where id = 'sym_speech_difficulty')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_speech_difficulty' and content = 'Encephalitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_speech_difficulty', 'Brain tumor or dementia (gradual onset)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_speech_difficulty'), 0)
where exists (select 1 from public.symptoms where id = 'sym_speech_difficulty')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_speech_difficulty' and content = 'Brain tumor or dementia (gradual onset)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_speech_difficulty', 'Speech that gets steadily worse over weeks', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_speech_difficulty'), 0)
where exists (select 1 from public.symptoms where id = 'sym_speech_difficulty')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_speech_difficulty' and content = 'Speech that gets steadily worse over weeks');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_speech_difficulty', 'Merck Manual Professional - Aphasia', 'Huang J. Aphasia. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Sep 2025.', 'https://www.merckmanuals.com/professional/neurologic-disorders/function-and-dysfunction-of-the-cerebral-lobes/aphasia', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_speech_difficulty'), 0)
where exists (select 1 from public.symptoms where id = 'sym_speech_difficulty')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_speech_difficulty' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/function-and-dysfunction-of-the-cerebral-lobes/aphasia');

-- ================================================ sym_sore_throat  (Sore throat)
update public.symptoms set description = 'Sore throat is discomfort, pain or scratchiness in the throat that often makes swallowing painful. Most cases are due to viral upper respiratory infection; group A streptococcus is the main bacterial cause. Group A streptococcus causes about 10 to 25% of cases in adults. Testing is reasonable when two or more Centor criteria are present (tonsil exudate, tender neck nodes, fever, no cough), and severe pain with a normal-looking throat suggests epiglottitis.', updated_at = now()
where id = 'sym_sore_throat' and description = 'Sore throat is discomfort, pain or scratchiness in the throat that often makes swallowing painful. Most cases are due to viral upper respiratory infection; group A streptococcus is the main bacterial cause.';
update public.symptoms set tags = tags || array['Centor criteria']::text[]
where id = 'sym_sore_throat' and not (tags @> array['Centor criteria']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Sore Throat'
where id = 'sym_sore_throat' and position('Merck Manual Professional - Sore Throat' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_sore_throat', 'Epiglottitis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_sore_throat'), 0)
where exists (select 1 from public.symptoms where id = 'sym_sore_throat')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_sore_throat' and content = 'Epiglottitis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_sore_throat', 'Peritonsillar abscess', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_sore_throat'), 0)
where exists (select 1 from public.symptoms where id = 'sym_sore_throat')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_sore_throat' and content = 'Peritonsillar abscess');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_sore_throat', 'Severe pain but the throat looks normal (possible epiglottitis)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_sore_throat'), 0)
where exists (select 1 from public.symptoms where id = 'sym_sore_throat')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_sore_throat' and content = 'Severe pain but the throat looks normal (possible epiglottitis)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_sore_throat', 'Merck Manual Professional - Sore Throat', 'Fried MP. Sore Throat. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2025.', 'https://www.merckmanuals.com/professional/ear-nose-and-throat-disorders/approach-to-the-patient-with-nasal-and-pharyngeal-symptoms/sore-throat', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_sore_throat'), 0)
where exists (select 1 from public.symptoms where id = 'sym_sore_throat')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_sore_throat' and url = 'https://www.merckmanuals.com/professional/ear-nose-and-throat-disorders/approach-to-the-patient-with-nasal-and-pharyngeal-symptoms/sore-throat');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
