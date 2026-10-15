-- 022_symptoms_review_02.sql  -  symptom review, session 02: 10 symptoms
-- Adds only: longer descriptions, extra causes, red flags, references and disease links.
-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).
-- A description is only extended if it is still the exported text (your own edits are kept).

begin;

-- ================================================ sym_proptosis  (Bulging or staring eyes (proptosis))
update public.symptoms set description = 'Forward displacement of one or both eyeballs, often with eyelid retraction, a staring look, gritty or watery eyes and sometimes double vision. Graves orbitopathy is the most common cause in adults; one-sided or rapidly progressive proptosis needs urgent assessment for orbital infection or tumor. Graves disease is the commonest cause in adults and orbital cellulitis in children. Sudden one-sided bulging suggests bleeding or inflammation in the orbit, while slow progression suggests a tumor; it is confirmed with an exophthalmometer, and CT or MRI of the orbits shows the cause.', updated_at = now()
where id = 'sym_proptosis' and description = 'Forward displacement of one or both eyeballs, often with eyelid retraction, a staring look, gritty or watery eyes and sometimes double vision. Graves orbitopathy is the most common cause in adults; one-sided or rapidly progressive proptosis needs urgent assessment for orbital infection or tumor.';
update public.symptoms set tags = tags || array['orbit']::text[]
where id = 'sym_proptosis' and not (tags @> array['orbit']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Proptosis (Exophthalmos)'
where id = 'sym_proptosis' and position('Merck Manual Professional - Proptosis (Exophthalmos)' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_proptosis', 'Bleeding inside the orbit after injury', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_proptosis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_proptosis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_proptosis' and content = 'Bleeding inside the orbit after injury');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_proptosis', 'Sinus infection spreading into the orbit', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_proptosis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_proptosis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_proptosis' and content = 'Sinus infection spreading into the orbit');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_proptosis', 'Pulsating eye or a whooshing sound in the head (possible carotid-cavernous fistula)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_proptosis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_proptosis')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_proptosis' and content = 'Pulsating eye or a whooshing sound in the head (possible carotid-cavernous fistula)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_proptosis', 'Sudden bulging of one eye', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_proptosis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_proptosis')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_proptosis' and content = 'Sudden bulging of one eye');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_proptosis', 'Merck Manual Professional - Proptosis (Exophthalmos)', 'Brady CJ. Proptosis (Exophthalmos). Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Oct 2025.', 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmologic-disorders/proptosis', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_proptosis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_proptosis')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_proptosis' and url = 'https://www.merckmanuals.com/professional/eye-disorders/symptoms-of-ophthalmologic-disorders/proptosis');

-- ================================================ sym_calf_pain  (Calf muscle pain / tenderness)
update public.symptoms set description = 'Calf pain is pain or tenderness localized to the posterior lower leg muscles. In an acute febrile illness, myalgia characteristically involving the calves and lower back is a recognized feature of leptospirosis; outside that context, calf pain is often musculoskeletal or vascular. Deep vein thrombosis is among the commonest causes of non-injury leg pain, and the swelling, warmth and redness can be slight, so ultrasound is often needed. Calf pain that comes on reliably with walking and settles with rest is claudication from peripheral arterial disease.', updated_at = now()
where id = 'sym_calf_pain' and description = 'Calf pain is pain or tenderness localized to the posterior lower leg muscles. In an acute febrile illness, myalgia characteristically involving the calves and lower back is a recognized feature of leptospirosis; outside that context, calf pain is often musculoskeletal or vascular.';
update public.symptoms set tags = tags || array['DVT', 'claudication']::text[]
where id = 'sym_calf_pain' and not (tags @> array['DVT', 'claudication']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Limb Pain'
where id = 'sym_calf_pain' and position('Merck Manual Professional - Limb Pain' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_calf_pain', 'Sudden blockage of a leg artery (acute arterial occlusion)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_calf_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_calf_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_calf_pain' and content = 'Sudden blockage of a leg artery (acute arterial occlusion)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_calf_pain', 'Deep soft-tissue infection (cellulitis, necrotizing fasciitis)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_calf_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_calf_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_calf_pain' and content = 'Deep soft-tissue infection (cellulitis, necrotizing fasciitis)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_calf_pain', 'Benign acute myositis in children after influenza', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_calf_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_calf_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_calf_pain' and content = 'Benign acute myositis in children after influenza');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_calf_pain', 'Crackling under the skin, blisters or rapidly spreading tense swelling (possible deep tissue infection)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_calf_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_calf_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_calf_pain' and content = 'Crackling under the skin, blisters or rapidly spreading tense swelling (possible deep tissue infection)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_calf_pain', 'Sudden severe pain with a pulseless leg', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_calf_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_calf_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_calf_pain' and content = 'Sudden severe pain with a pulseless leg');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_calf_pain', 'Merck Manual Professional - Limb Pain', 'Thompson AD, Shea MJ. Limb Pain. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2024.', 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/limb-pain', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_calf_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_calf_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_calf_pain' and url = 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/limb-pain');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'influenza', 'sym_calf_pain', 2::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'influenza')
  and exists (select 1 from public.symptoms where id = 'sym_calf_pain')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'influenza' and symptom_id = 'sym_calf_pain');

-- ================================================ sym_tophi  (Chalky lumps under the skin near joints or ears (tophi))
update public.symptoms set description = 'Firm, painless, whitish or yellowish lumps formed by deposits of urate crystals, typically over the toes, fingers, elbows, Achilles tendon or ear rims. They appear after years of high uric acid and can discharge chalky material or damage joints. They are found on the fingers, hands and feet, around the elbow (olecranon) and Achilles tendon, and in the skin of the ear, and they mark chronic gouty arthritis. Material aspirated from a tophus shows needle-shaped, strongly negatively birefringent urate crystals under polarised light.', updated_at = now()
where id = 'sym_tophi' and description = 'Firm, painless, whitish or yellowish lumps formed by deposits of urate crystals, typically over the toes, fingers, elbows, Achilles tendon or ear rims. They appear after years of high uric acid and can discharge chalky material or damage joints.';
update public.symptoms set tags = tags || array['urate']::text[]
where id = 'sym_tophi' and not (tags @> array['urate']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Gout'
where id = 'sym_tophi' and position('Merck Manual Professional - Gout' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_tophi', 'Long-standing high uric acid, made worse by kidney disease or diuretics', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_tophi'), 0)
where exists (select 1 from public.symptoms where id = 'sym_tophi')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_tophi' and content = 'Long-standing high uric acid, made worse by kidney disease or diuretics');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_tophi', 'Tophus over a joint with loss of movement or deformity', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_tophi'), 0)
where exists (select 1 from public.symptoms where id = 'sym_tophi')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_tophi' and content = 'Tophus over a joint with loss of movement or deformity');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_tophi', 'Merck Manual Professional - Gout', 'Keller SF. Gout. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2025.', 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_tophi'), 0)
where exists (select 1 from public.symptoms where id = 'sym_tophi')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_tophi' and url = 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout');

-- ================================================ sym_chest_pain  (Chest pain or pressure (angina-like))
update public.symptoms set description = 'Anginal chest pain is typically a dull, heavy, pressing or crushing substernal discomfort that may radiate to the arm, neck or jaw, is precipitated by exertion or stress and relieved by rest. Chest pain has a broad differential that includes several immediately life-threatening causes. The immediately life-threatening causes to exclude first are acute coronary syndrome, aortic dissection, tension pneumothorax, esophageal rupture and pulmonary embolism; most other chest pain comes from the chest wall, pleura or digestive tract. Pain that has been present for weeks to months is rarely immediately dangerous.', updated_at = now()
where id = 'sym_chest_pain' and description = 'Anginal chest pain is typically a dull, heavy, pressing or crushing substernal discomfort that may radiate to the arm, neck or jaw, is precipitated by exertion or stress and relieved by rest. Chest pain has a broad differential that includes several immediately life-threatening causes.';
update public.symptoms set tags = tags || array['differential']::text[]
where id = 'sym_chest_pain' and not (tags @> array['differential']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Chest Pain'
where id = 'sym_chest_pain' and position('Merck Manual Professional - Chest Pain' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chest_pain', 'Tension pneumothorax', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chest_pain' and content = 'Tension pneumothorax');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chest_pain', 'Esophageal rupture or spasm', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chest_pain' and content = 'Esophageal rupture or spasm');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chest_pain', 'Peptic ulcer or gallstones', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chest_pain' and content = 'Peptic ulcer or gallstones');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chest_pain', 'Pericarditis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chest_pain' and content = 'Pericarditis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chest_pain', 'Pneumonia or pleurisy', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_pain')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chest_pain' and content = 'Pneumonia or pleurisy');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_chest_pain', 'Unequal pulses or blood pressure between the arms, or a new heart murmur', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_chest_pain' and content = 'Unequal pulses or blood pressure between the arms, or a new heart murmur');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_chest_pain', 'Sudden sharp pain with breathlessness (possible pneumothorax or pulmonary embolism)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_pain')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_chest_pain' and content = 'Sudden sharp pain with breathlessness (possible pneumothorax or pulmonary embolism)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_chest_pain', 'Merck Manual Professional - Chest Pain', 'Thompson AD, Shea MJ. Chest Pain. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2024.', 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/chest-pain', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_chest_pain'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_pain')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_chest_pain' and url = 'https://www.merckmanuals.com/professional/cardiovascular-disorders/symptoms-of-cardiovascular-disorders/chest-pain');

-- ================================================ sym_chest_tightness  (Chest tightness)
update public.symptoms set description = 'Chest tightness is a sensation of constriction or inability to fully expand the chest. It is one of the cardinal symptoms of asthma, often reported more frequently than wheeze, but a sensation of tightness or pressure may also represent myocardial ischemia. Tightness that comes in episodes with wheeze, cough and typical triggers (exercise, cold air, allergens) points to asthma, whereas pressure behind the breastbone spreading to the arm or jaw needs an ECG and cardiac enzymes to exclude ischemia. A normal oxygen saturation does not rule out pulmonary embolism.', updated_at = now()
where id = 'sym_chest_tightness' and description = 'Chest tightness is a sensation of constriction or inability to fully expand the chest. It is one of the cardinal symptoms of asthma, often reported more frequently than wheeze, but a sensation of tightness or pressure may also represent myocardial ischemia.';
update public.symptoms set tags = tags || array['bronchospasm']::text[]
where id = 'sym_chest_tightness' and not (tags @> array['bronchospasm']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Dyspnea'
where id = 'sym_chest_tightness' and position('Merck Manual Professional - Dyspnea' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chest_tightness', 'Pulmonary embolism or pneumothorax', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chest_tightness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_tightness')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chest_tightness' and content = 'Pulmonary embolism or pneumothorax');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chest_tightness', 'Heart failure', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chest_tightness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_tightness')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chest_tightness' and content = 'Heart failure');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_chest_tightness', 'Sudden sharp chest pain with rapid breathing', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_chest_tightness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_tightness')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_chest_tightness' and content = 'Sudden sharp chest pain with rapid breathing');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_chest_tightness', 'Merck Manual Professional - Dyspnea', 'Dezube R. Dyspnea. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Nov 2025.', 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/dyspnea', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_chest_tightness'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chest_tightness')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_chest_tightness' and url = 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/dyspnea');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'acute_coronary_syndrome', 'sym_chest_tightness', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.symptoms where id = 'sym_chest_tightness')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'acute_coronary_syndrome' and symptom_id = 'sym_chest_tightness');

-- ================================================ sym_chills  (Chills / rigors)
update public.symptoms set description = 'Chills are a sensation of coldness, often with shivering and pallor, that occur as body temperature rises toward a newly elevated set point. Rigors are intense, uncontrollable shaking chills (''teeth-chattering, bed-shaking'') that are associated with rapid temperature rise and suggest bacteremia or other acute infection. Rigors suggest an infectious cause but are not specific to any one infection. In adults, an acute fever of 4 days or less with chills is very likely infectious, usually from the respiratory, digestive or urinary tract or the skin.', updated_at = now()
where id = 'sym_chills' and description = 'Chills are a sensation of coldness, often with shivering and pallor, that occur as body temperature rises toward a newly elevated set point. Rigors are intense, uncontrollable shaking chills (''teeth-chattering, bed-shaking'') that are associated with rapid temperature rise and suggest bacteremia or other acute infection.';
update public.symptoms set tags = tags || array['rigors']::text[]
where id = 'sym_chills' and not (tags @> array['rigors']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Fever'
where id = 'sym_chills' and position('Merck Manual Professional - Fever' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chills', 'Abscess or other deep infection', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chills'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chills')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chills' and content = 'Abscess or other deep infection');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chills', 'Cholangitis (bile duct infection)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chills'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chills')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chills' and content = 'Cholangitis (bile duct infection)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_chills', 'Dengue', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_chills'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chills')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_chills' and content = 'Dengue');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_chills', 'Temperature above 40 °C or below 35 °C', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_chills'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chills')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_chills' and content = 'Temperature above 40 °C or below 35 °C');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_chills', 'Rash of small purple spots that do not fade when pressed (possible meningococcal infection)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_chills'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chills')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_chills' and content = 'Rash of small purple spots that do not fade when pressed (possible meningococcal infection)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_chills', 'Merck Manual Professional - Fever', 'Bush LM, Vazquez-Pertejo MT. Fever. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2024.', 'https://www.merckmanuals.com/professional/infectious-diseases/biology-of-infectious-disease/fever', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_chills'), 0)
where exists (select 1 from public.symptoms where id = 'sym_chills')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_chills' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/biology-of-infectious-disease/fever');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'dengue', 'sym_chills', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'dengue')
  and exists (select 1 from public.symptoms where id = 'sym_chills')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'dengue' and symptom_id = 'sym_chills');

-- ================================================ sym_confusion  (Confusion / altered mental status)
update public.symptoms set description = 'Confusion is the inability to think as clearly or quickly as usual, with disorientation and difficulty with attention, memory and decisions. Acute confusion (delirium) is a medical emergency commonly caused by infection, metabolic derangement, hypoxia, drugs or brain disease. The commonest triggers are medicines (especially anticholinergic drugs and opioids), dehydration and infection. Delirium is marked by poor attention and a level of alertness that fluctuates and is often worse at night; unlike dementia it starts quickly and is often reversible.', updated_at = now()
where id = 'sym_confusion' and description = 'Confusion is the inability to think as clearly or quickly as usual, with disorientation and difficulty with attention, memory and decisions. Acute confusion (delirium) is a medical emergency commonly caused by infection, metabolic derangement, hypoxia, drugs or brain disease.';
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Delirium'
where id = 'sym_confusion' and position('Merck Manual Professional - Delirium' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_confusion', 'Dehydration', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_confusion'), 0)
where exists (select 1 from public.symptoms where id = 'sym_confusion')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_confusion' and content = 'Dehydration');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_confusion', 'Liver or kidney failure', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_confusion'), 0)
where exists (select 1 from public.symptoms where id = 'sym_confusion')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_confusion' and content = 'Liver or kidney failure');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_confusion', 'Head injury', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_confusion'), 0)
where exists (select 1 from public.symptoms where id = 'sym_confusion')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_confusion' and content = 'Head injury');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_confusion', 'An older adult who becomes suddenly quiet or drowsy (hypoactive delirium)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_confusion'), 0)
where exists (select 1 from public.symptoms where id = 'sym_confusion')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_confusion' and content = 'An older adult who becomes suddenly quiet or drowsy (hypoactive delirium)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_confusion', 'Merck Manual Professional - Delirium', 'Huang J. Delirium. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Feb 2025.', 'https://www.merckmanuals.com/professional/neurologic-disorders/delirium-and-dementia/delirium', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_confusion'), 0)
where exists (select 1 from public.symptoms where id = 'sym_confusion')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_confusion' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/delirium-and-dementia/delirium');

-- ================================================ sym_constipation  (Constipation)
update public.symptoms set description = 'Constipation is infrequent bowel movements (commonly fewer than three per week) or hard, dry stools that are difficult or painful to pass. It is most often functional or dietary, but may reflect medicines, metabolic disease or bowel obstruction. New, acute constipation suggests an organic cause, and bowel obstruction must be considered when it is sudden and severe. When fibre and laxatives fail, anorectal tests can show dyssynergic defecation, where the pelvic floor muscles do not relax during straining.', updated_at = now()
where id = 'sym_constipation' and description = 'Constipation is infrequent bowel movements (commonly fewer than three per week) or hard, dry stools that are difficult or painful to pass. It is most often functional or dietary, but may reflect medicines, metabolic disease or bowel obstruction.';
update public.symptoms set tags = tags || array['bowel obstruction']::text[]
where id = 'sym_constipation' and not (tags @> array['bowel obstruction']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Constipation'
where id = 'sym_constipation' and position('Merck Manual Professional - Constipation' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_constipation', 'Neurological disease (Parkinson''s disease, spinal cord injury)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_constipation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_constipation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_constipation' and content = 'Neurological disease (Parkinson''s disease, spinal cord injury)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_constipation', 'Pelvic floor dysfunction (dyssynergic defecation)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_constipation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_constipation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_constipation' and content = 'Pelvic floor dysfunction (dyssynergic defecation)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_constipation', 'High calcium and diabetes', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_constipation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_constipation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_constipation' and content = 'High calcium and diabetes');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_constipation', 'Anticholinergic drugs', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_constipation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_constipation')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_constipation' and content = 'Anticholinergic drugs');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_constipation', 'Family history of colorectal cancer or iron-deficiency anemia', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_constipation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_constipation')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_constipation' and content = 'Family history of colorectal cancer or iron-deficiency anemia');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_constipation', 'Merck Manual Professional - Constipation', 'Gotfried J. Constipation. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Apr 2026.', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/symptoms-of-gastrointestinal-disorders/constipation', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_constipation'), 0)
where exists (select 1 from public.symptoms where id = 'sym_constipation')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_constipation' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/symptoms-of-gastrointestinal-disorders/constipation');

-- ================================================ sym_cough  (Cough)
update public.symptoms set description = 'Cough is a protective reflex that expels air forcefully to clear the airways of secretions and irritants. It is classified as acute (under 3 weeks), subacute (3-8 weeks) or chronic (over 8 weeks) and may be dry or productive. Acute cough is mostly from upper respiratory infection, sinusitis, pneumonia, COPD flares, pertussis or heart failure; subacute cough is usually post-infectious airway hyperresponsiveness; chronic cough is mainly from upper airway cough syndrome (postnasal drip), reflux, asthma, chronic bronchitis or ACE inhibitors.', updated_at = now()
where id = 'sym_cough' and description = 'Cough is a protective reflex that expels air forcefully to clear the airways of secretions and irritants. It is classified as acute (under 3 weeks), subacute (3-8 weeks) or chronic (over 8 weeks) and may be dry or productive.';
update public.symptoms set tags = tags || array['chronic cough']::text[]
where id = 'sym_cough' and not (tags @> array['chronic cough']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Cough in Adults'
where id = 'sym_cough' and position('Merck Manual Professional - Cough in Adults' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_cough', 'Postnasal drip (upper airway cough syndrome)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_cough')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_cough' and content = 'Postnasal drip (upper airway cough syndrome)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_cough', 'Post-infectious cough', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_cough')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_cough' and content = 'Post-infectious cough');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_cough', 'Pertussis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_cough')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_cough' and content = 'Pertussis');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_cough', 'Heart failure', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_cough')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_cough' and content = 'Heart failure');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_cough', 'Known HIV infection or contact with someone with TB', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_cough')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_cough' and content = 'Known HIV infection or contact with someone with TB');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_cough', 'Merck Manual Professional - Cough in Adults', 'Dezube R. Cough in Adults. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Nov 2025.', 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/cough-in-adults', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_cough')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_cough' and url = 'https://www.merckmanuals.com/professional/pulmonary-disorders/symptoms-of-pulmonary-disorders/cough-in-adults');

-- ================================================ sym_paroxysmal_cough  (Coughing fits with a "whoop" (paroxysmal cough))
update public.symptoms set description = 'Paroxysmal cough consists of bursts of rapid, uncontrollable coughs on a single expiration, followed by a forced inspiration against a partially closed glottis that produces the characteristic high-pitched whoop. It is the defining feature of the paroxysmal stage of pertussis, although the whoop is often absent in young infants and in adolescents and adults. Pertussis runs through a catarrhal stage (runny nose, low fever, mild cough), a paroxysmal stage and a slow convalescent stage. Coughing fits are worse at night, may number around 15 in 24 hours and are often followed by vomiting; in young infants apnea may be the only sign.', updated_at = now()
where id = 'sym_paroxysmal_cough' and description = 'Paroxysmal cough consists of bursts of rapid, uncontrollable coughs on a single expiration, followed by a forced inspiration against a partially closed glottis that produces the characteristic high-pitched whoop. It is the defining feature of the paroxysmal stage of pertussis, although the whoop is often absent in young infants and in adolescents and adults.';
update public.symptoms set tags = tags || array['whooping cough']::text[]
where id = 'sym_paroxysmal_cough' and not (tags @> array['whooping cough']::text[]);
update public.symptoms set source_attribution = source_attribution || '; CDC - Clinical Features of Pertussis'
where id = 'sym_paroxysmal_cough' and position('CDC - Clinical Features of Pertussis' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_paroxysmal_cough', 'Coughing fits followed by vomiting or exhaustion', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_paroxysmal_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_paroxysmal_cough')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_paroxysmal_cough' and content = 'Coughing fits followed by vomiting or exhaustion');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_paroxysmal_cough', 'CDC - Clinical Features of Pertussis', 'Centers for Disease Control and Prevention. Clinical Features of Pertussis. Atlanta (GA): CDC; last reviewed Dec 2025.', 'https://www.cdc.gov/pertussis/hcp/clinical-signs/index.html', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_paroxysmal_cough'), 0)
where exists (select 1 from public.symptoms where id = 'sym_paroxysmal_cough')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_paroxysmal_cough' and url = 'https://www.cdc.gov/pertussis/hcp/clinical-signs/index.html');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
