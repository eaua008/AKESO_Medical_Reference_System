-- 026_symptoms_review_06.sql  -  symptom review, session 06: 10 symptoms
-- Adds only: longer descriptions, extra causes, red flags, references and disease links.
-- Nothing is deleted or replaced. Safe to run twice (every insert is guarded).
-- A description is only extended if it is still the exported text (your own edits are kept).

begin;

-- ================================================ sym_myalgia  (Muscle aches (myalgia))
update public.symptoms set description = 'Myalgia is diffuse or localized pain in skeletal muscles, which may also be felt in the associated tendons, ligaments and fascia. Generalized myalgia is a common feature of systemic viral and bacterial infections, while localized myalgia more often reflects overuse or injury. In adults over 50, aching and morning stiffness lasting over an hour in both shoulders and hips, with a markedly raised ESR and CRP but no true weakness, suggests polymyalgia rheumatica; 40 to 60% of patients with giant cell arteritis also have it.', updated_at = now()
where id = 'sym_myalgia' and description = 'Myalgia is diffuse or localized pain in skeletal muscles, which may also be felt in the associated tendons, ligaments and fascia. Generalized myalgia is a common feature of systemic viral and bacterial infections, while localized myalgia more often reflects overuse or injury.';
update public.symptoms set tags = tags || array['polymyalgia rheumatica']::text[]
where id = 'sym_myalgia' and not (tags @> array['polymyalgia rheumatica']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Polymyalgia Rheumatica'
where id = 'sym_myalgia' and position('Merck Manual Professional - Polymyalgia Rheumatica' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_myalgia', 'Polymyalgia rheumatica (adults over 50)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_myalgia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_myalgia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_myalgia' and content = 'Polymyalgia rheumatica (adults over 50)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_myalgia', 'Inflammatory myositis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_myalgia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_myalgia')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_myalgia' and content = 'Inflammatory myositis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_myalgia', 'Shoulder and hip stiffness with headache, jaw pain or vision changes in someone over 50', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_myalgia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_myalgia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_myalgia' and content = 'Shoulder and hip stiffness with headache, jaw pain or vision changes in someone over 50');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_myalgia', 'Merck Manual Professional - Polymyalgia Rheumatica', 'Villa-Forte A. Polymyalgia Rheumatica. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Dec 2024.', 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/vasculitis/polymyalgia-rheumatica', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_myalgia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_myalgia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_myalgia' and url = 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/vasculitis/polymyalgia-rheumatica');

-- ================================================ sym_muscle_cramps  (Muscle cramps)
update public.symptoms set description = 'Muscle cramps are sudden, involuntary and painful contractions of a muscle or muscle group, commonly the calves and feet. They occur with overuse and dehydration and with electrolyte disturbances such as hypokalemia, hyponatremia and hypocalcemia, as in the large fluid and electrolyte losses of cholera. Most cramps are benign night-time calf cramps or cramps during exercise, helped by tight calf muscles, dehydration, low potassium or magnesium and some medicines. Stretching and fluids are preferred; drugs for cramps have little proven benefit.', updated_at = now()
where id = 'sym_muscle_cramps' and description = 'Muscle cramps are sudden, involuntary and painful contractions of a muscle or muscle group, commonly the calves and feet. They occur with overuse and dehydration and with electrolyte disturbances such as hypokalemia, hyponatremia and hypocalcemia, as in the large fluid and electrolyte losses of cholera.';
update public.symptoms set tags = tags || array['nocturnal leg cramps']::text[]
where id = 'sym_muscle_cramps' and not (tags @> array['nocturnal leg cramps']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Muscle Cramps'
where id = 'sym_muscle_cramps' and position('Merck Manual Professional - Muscle Cramps' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_muscle_cramps', 'Benign night-time leg cramps', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_muscle_cramps'), 0)
where exists (select 1 from public.symptoms where id = 'sym_muscle_cramps')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_muscle_cramps' and content = 'Benign night-time leg cramps');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_muscle_cramps', 'Low magnesium', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_muscle_cramps'), 0)
where exists (select 1 from public.symptoms where id = 'sym_muscle_cramps')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_muscle_cramps' and content = 'Low magnesium');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_muscle_cramps', 'Cramps in the arms or trunk, or with muscle twitching, wasting or weakness', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_muscle_cramps'), 0)
where exists (select 1 from public.symptoms where id = 'sym_muscle_cramps')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_muscle_cramps' and content = 'Cramps in the arms or trunk, or with muscle twitching, wasting or weakness');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_muscle_cramps', 'Merck Manual Professional - Muscle Cramps', 'Freedman M. Muscle Cramps. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2025.', 'https://www.merckmanuals.com/professional/neurologic-disorders/symptoms-of-neurologic-disorders/muscle-cramps', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_muscle_cramps'), 0)
where exists (select 1 from public.symptoms where id = 'sym_muscle_cramps')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_muscle_cramps' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/symptoms-of-neurologic-disorders/muscle-cramps');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'acute_gastroenteritis', 'sym_muscle_cramps', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'acute_gastroenteritis')
  and exists (select 1 from public.symptoms where id = 'sym_muscle_cramps')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'acute_gastroenteritis' and symptom_id = 'sym_muscle_cramps');

-- ================================================ sym_nausea_vomiting  (Nausea & vomiting)
update public.symptoms set description = 'Nausea is an unpleasant sensation of the urge to vomit, and vomiting (emesis) is forceful expulsion of gastric contents through the mouth. Both are common and arise from gastrointestinal, central nervous system, metabolic, drug-related and pregnancy-related causes. The commonest causes are gastroenteritis, medicines or drugs and toxins. Repeated cycles of vomiting in an adult who uses cannabis heavily, eased by hot showers, suggest cannabinoid hyperemesis, which settles when cannabis is stopped; a pregnancy test is advised in women who could be pregnant.', updated_at = now()
where id = 'sym_nausea_vomiting' and description = 'Nausea is an unpleasant sensation of the urge to vomit, and vomiting (emesis) is forceful expulsion of gastric contents through the mouth. Both are common and arise from gastrointestinal, central nervous system, metabolic, drug-related and pregnancy-related causes.';
update public.symptoms set tags = tags || array['cyclic vomiting']::text[]
where id = 'sym_nausea_vomiting' and not (tags @> array['cyclic vomiting']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Nausea and Vomiting'
where id = 'sym_nausea_vomiting' and position('Merck Manual Professional - Nausea and Vomiting' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_nausea_vomiting', 'Cannabinoid hyperemesis syndrome', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_nausea_vomiting'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nausea_vomiting')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_nausea_vomiting' and content = 'Cannabinoid hyperemesis syndrome');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_nausea_vomiting', 'Toxins and poisoning', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_nausea_vomiting'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nausea_vomiting')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_nausea_vomiting' and content = 'Toxins and poisoning');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_nausea_vomiting', 'Bowel obstruction', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_nausea_vomiting'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nausea_vomiting')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_nausea_vomiting' and content = 'Bowel obstruction');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_nausea_vomiting', 'Diabetic ketoacidosis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_nausea_vomiting'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nausea_vomiting')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_nausea_vomiting' and content = 'Diabetic ketoacidosis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_nausea_vomiting', 'Swollen, drum-like abdomen (possible bowel obstruction)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_nausea_vomiting'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nausea_vomiting')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_nausea_vomiting' and content = 'Swollen, drum-like abdomen (possible bowel obstruction)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_nausea_vomiting', 'Vomiting with confusion or drowsiness', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_nausea_vomiting'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nausea_vomiting')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_nausea_vomiting' and content = 'Vomiting with confusion or drowsiness');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_nausea_vomiting', 'Merck Manual Professional - Nausea and Vomiting', 'Gotfried J. Nausea and Vomiting. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Apr 2026 (updated Jun 2026).', 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/symptoms-of-gastrointestinal-disorders/nausea-and-vomiting', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_nausea_vomiting'), 0)
where exists (select 1 from public.symptoms where id = 'sym_nausea_vomiting')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_nausea_vomiting' and url = 'https://www.merckmanuals.com/professional/gastrointestinal-disorders/symptoms-of-gastrointestinal-disorders/nausea-and-vomiting');

-- ================================================ sym_night_sweats  (Night sweats)
update public.symptoms set description = 'Night sweats are episodes of sweating during sleep severe enough to soak nightclothes or bedding, resulting from exaggeration of the normal circadian temperature rhythm. They may accompany any febrile illness and are classically associated with tuberculosis and lymphoma. In active TB they come with fever, weight loss, poor appetite and fatigue, plus a cough of 3 weeks or more in pulmonary TB. In lymphoma, fever, drenching night sweats and weight loss of more than 10% in 6 months are the ''B symptoms'' that affect staging and prognosis.', updated_at = now()
where id = 'sym_night_sweats' and description = 'Night sweats are episodes of sweating during sleep severe enough to soak nightclothes or bedding, resulting from exaggeration of the normal circadian temperature rhythm. They may accompany any febrile illness and are classically associated with tuberculosis and lymphoma.';
update public.symptoms set tags = tags || array['lymphoma']::text[]
where id = 'sym_night_sweats' and not (tags @> array['lymphoma']::text[]);
update public.symptoms set source_attribution = source_attribution || '; CDC - Signs and Symptoms of Tuberculosis; Merck Manual Professional - Hodgkin Lymphoma'
where id = 'sym_night_sweats' and position('CDC - Signs and Symptoms of Tuberculosis' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_night_sweats', 'HIV infection', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_night_sweats'), 0)
where exists (select 1 from public.symptoms where id = 'sym_night_sweats')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_night_sweats' and content = 'HIV infection');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_night_sweats', 'Weight loss of more than 10% in 6 months', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_night_sweats'), 0)
where exists (select 1 from public.symptoms where id = 'sym_night_sweats')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_night_sweats' and content = 'Weight loss of more than 10% in 6 months');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_night_sweats', 'Cough lasting 3 weeks or more', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_night_sweats'), 0)
where exists (select 1 from public.symptoms where id = 'sym_night_sweats')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_night_sweats' and content = 'Cough lasting 3 weeks or more');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_night_sweats', 'CDC - Signs and Symptoms of Tuberculosis', 'Centers for Disease Control and Prevention. Signs and Symptoms of Tuberculosis. Atlanta (GA): CDC; reviewed Mar 2024.', 'https://www.cdc.gov/tb/signs-symptoms/index.html', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_night_sweats'), 0)
where exists (select 1 from public.symptoms where id = 'sym_night_sweats')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_night_sweats' and url = 'https://www.cdc.gov/tb/signs-symptoms/index.html');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_night_sweats', 'Merck Manual Professional - Hodgkin Lymphoma', 'Martin P, Leonard JP. Hodgkin Lymphoma. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2024 (updated Apr 2026).', 'https://www.merckmanuals.com/professional/oncology/lymphomas/hodgkin-lymphoma', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_night_sweats'), 0)
where exists (select 1 from public.symptoms where id = 'sym_night_sweats')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_night_sweats' and url = 'https://www.merckmanuals.com/professional/oncology/lymphomas/hodgkin-lymphoma');

-- ================================================ sym_hemiparesis  (One-sided weakness or numbness)
update public.symptoms set description = 'Hemiparesis is weakness of one side of the body, often with numbness (hemisensory loss). Sudden onset is a hallmark of stroke; middle cerebral artery infarction typically causes contralateral weakness and sensory loss affecting the face and arm more than the leg. Arm and leg weakness on one side with spasticity, brisk reflexes and an upgoing plantar response points to a lesion in the opposite brain hemisphere. Weakness that becomes severe within minutes is usually stroke or injury.', updated_at = now()
where id = 'sym_hemiparesis' and description = 'Hemiparesis is weakness of one side of the body, often with numbness (hemisensory loss). Sudden onset is a hallmark of stroke; middle cerebral artery infarction typically causes contralateral weakness and sensory loss affecting the face and arm more than the leg.';
update public.symptoms set tags = tags || array['upper motor neuron']::text[]
where id = 'sym_hemiparesis' and not (tags @> array['upper motor neuron']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Weakness'
where id = 'sym_hemiparesis' and position('Merck Manual Professional - Weakness' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_hemiparesis', 'Weakness after a seizure (Todd paralysis)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_hemiparesis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemiparesis')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_hemiparesis' and content = 'Weakness after a seizure (Todd paralysis)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_hemiparesis', 'Weakness reaching its worst within minutes', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_hemiparesis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemiparesis')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_hemiparesis' and content = 'Weakness reaching its worst within minutes');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_hemiparesis', 'Merck Manual Professional - Weakness', 'Freedman M. Weakness. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2025.', 'https://www.merckmanuals.com/professional/neurologic-disorders/symptoms-of-neurologic-disorders/weakness', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_hemiparesis'), 0)
where exists (select 1 from public.symptoms where id = 'sym_hemiparesis')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_hemiparesis' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/symptoms-of-neurologic-disorders/weakness');

-- ================================================ sym_bite_site_paresthesia  (Pain or tingling at an animal-bite site)
update public.symptoms set description = 'Pain, itching, tingling or burning at a healed or healing animal-bite or scratch wound can mark the prodrome of rabies as the virus reaches the dorsal root ganglia. It typically appears with nonspecific fever, malaise and headache weeks to months after the exposure and precedes the neurologic phase. The incubation period averages 1 to 2 months but can exceed a year, and brain symptoms usually follow within about 2 weeks of the first symptoms. Immediate wound washing and post-exposure prophylaxis (vaccine plus rabies immune globulin) after a bite prevent the disease; any contact with a bat is an indication.', updated_at = now()
where id = 'sym_bite_site_paresthesia' and description = 'Pain, itching, tingling or burning at a healed or healing animal-bite or scratch wound can mark the prodrome of rabies as the virus reaches the dorsal root ganglia. It typically appears with nonspecific fever, malaise and headache weeks to months after the exposure and precedes the neurologic phase.';
update public.symptoms set tags = tags || array['post-exposure prophylaxis']::text[]
where id = 'sym_bite_site_paresthesia' and not (tags @> array['post-exposure prophylaxis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Rabies; CDC - Clinical Features of Rabies'
where id = 'sym_bite_site_paresthesia' and position('Merck Manual Professional - Rabies' in source_attribution) = 0;
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_bite_site_paresthesia', 'Any contact with a bat', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_bite_site_paresthesia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bite_site_paresthesia')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_bite_site_paresthesia' and content = 'Any contact with a bat');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_bite_site_paresthesia', 'Merck Manual Professional - Rabies', 'Klein RS. Rabies. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Jul 2026.', 'https://www.merckmanuals.com/professional/neurologic-disorders/brain-infections/rabies', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_bite_site_paresthesia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bite_site_paresthesia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_bite_site_paresthesia' and url = 'https://www.merckmanuals.com/professional/neurologic-disorders/brain-infections/rabies');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_bite_site_paresthesia', 'CDC - Clinical Features of Rabies', 'Centers for Disease Control and Prevention. Clinical Features of Rabies. Atlanta (GA): CDC, National Center for Emerging and Zoonotic Infectious Diseases; reviewed Jul 2025.', 'https://www.cdc.gov/rabies/hcp/clinical-signs/index.html', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_bite_site_paresthesia'), 0)
where exists (select 1 from public.symptoms where id = 'sym_bite_site_paresthesia')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_bite_site_paresthesia' and url = 'https://www.cdc.gov/rabies/hcp/clinical-signs/index.html');

-- ================================================ sym_mouth_sores  (Painful mouth sores or ulcers)
update public.symptoms set description = 'Mouth sores are painful breaks or vesicles in the oral mucosa that often cause difficulty eating, drinking and swallowing. Most are aphthous, traumatic or viral (herpes simplex, enteroviruses in hand, foot and mouth disease), but persistent ulcers may reflect systemic, autoimmune, immunodeficient or malignant disease. The commonest causes are recurrent aphthous ulcers, herpes viruses, Candida, injury and irritants, and chemotherapy or radiation. Mouth sores alone without fever or other signs are usually viral or aphthous; blistering skin that peels with light rubbing (Nikolsky sign) suggests Stevens-Johnson syndrome or pemphigus.', updated_at = now()
where id = 'sym_mouth_sores' and description = 'Mouth sores are painful breaks or vesicles in the oral mucosa that often cause difficulty eating, drinking and swallowing. Most are aphthous, traumatic or viral (herpes simplex, enteroviruses in hand, foot and mouth disease), but persistent ulcers may reflect systemic, autoimmune, immunodeficient or malignant disease.';
update public.symptoms set tags = tags || array['stomatitis']::text[]
where id = 'sym_mouth_sores' and not (tags @> array['stomatitis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Stomatitis'
where id = 'sym_mouth_sores' and position('Merck Manual Professional - Stomatitis' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_mouth_sores', 'Oral thrush (Candida)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_mouth_sores'), 0)
where exists (select 1 from public.symptoms where id = 'sym_mouth_sores')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_mouth_sores' and content = 'Oral thrush (Candida)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_mouth_sores', 'Chemotherapy or radiation', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_mouth_sores'), 0)
where exists (select 1 from public.symptoms where id = 'sym_mouth_sores')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_mouth_sores' and content = 'Chemotherapy or radiation');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_mouth_sores', 'Stevens-Johnson syndrome or pemphigus', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_mouth_sores'), 0)
where exists (select 1 from public.symptoms where id = 'sym_mouth_sores')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_mouth_sores' and content = 'Stevens-Johnson syndrome or pemphigus');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_mouth_sores', 'Fever with skin blisters or red, painful eyes', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_mouth_sores'), 0)
where exists (select 1 from public.symptoms where id = 'sym_mouth_sores')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_mouth_sores' and content = 'Fever with skin blisters or red, painful eyes');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_mouth_sores', 'Merck Manual Professional - Stomatitis', 'Hennessy BJ. Stomatitis. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Mar 2026.', 'https://www.merckmanuals.com/professional/dental-disorders/symptoms-of-dental-and-oral-disorders/stomatitis', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_mouth_sores'), 0)
where exists (select 1 from public.symptoms where id = 'sym_mouth_sores')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_mouth_sores' and url = 'https://www.merckmanuals.com/professional/dental-disorders/symptoms-of-dental-and-oral-disorders/stomatitis');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'varicella', 'sym_mouth_sores', 3::smallint, false, 0.4::numeric
where exists (select 1 from public.diseases where id = 'varicella')
  and exists (select 1 from public.symptoms where id = 'sym_mouth_sores')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'varicella' and symptom_id = 'sym_mouth_sores');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'hiv_infection', 'sym_mouth_sores', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.symptoms where id = 'sym_mouth_sores')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'hiv_infection' and symptom_id = 'sym_mouth_sores');

-- ================================================ sym_dysuria  (Painful urination (dysuria))
update public.symptoms set description = 'Dysuria is pain, burning, stinging or itching of the urethra or urethral meatus during urination. Acute cystitis is the most common cause, but urethritis, sexually transmitted infections, vaginitis and prostatitis also cause it. Cystitis and sexually transmitted urethritis are the commonest causes. Pus from the urethra suggests gonorrhea, a tender prostate suggests prostatitis, and red cells without white cells with a sterile culture may point to a stone or cancer.', updated_at = now()
where id = 'sym_dysuria' and description = 'Dysuria is pain, burning, stinging or itching of the urethra or urethral meatus during urination. Acute cystitis is the most common cause, but urethritis, sexually transmitted infections, vaginitis and prostatitis also cause it.';
update public.symptoms set tags = tags || array['urethritis']::text[]
where id = 'sym_dysuria' and not (tags @> array['urethritis']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Dysuria'
where id = 'sym_dysuria' and position('Merck Manual Professional - Dysuria' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_dysuria', 'Bladder cancer (blood without infection)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_dysuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dysuria')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_dysuria' and content = 'Bladder cancer (blood without infection)');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_dysuria', 'Recent catheter or urinary procedure', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_dysuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dysuria')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dysuria' and content = 'Recent catheter or urinary procedure');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_dysuria', 'Weakened immune system or known urinary tract abnormality', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_dysuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dysuria')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_dysuria' and content = 'Weakened immune system or known urinary tract abnormality');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_dysuria', 'Merck Manual Professional - Dysuria', 'Maddukuri G. Dysuria. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Sep 2024.', 'https://www.merckmanuals.com/professional/genitourinary-disorders/symptoms-of-genitourinary-disorders/dysuria', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_dysuria'), 0)
where exists (select 1 from public.symptoms where id = 'sym_dysuria')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_dysuria' and url = 'https://www.merckmanuals.com/professional/genitourinary-disorders/symptoms-of-genitourinary-disorders/dysuria');

-- ================================================ sym_pale_stool  (Pale or clay-colored stools)
update public.symptoms set description = 'Pale, clay-colored (acholic) stools result from reduced delivery of bile pigments to the intestine, so that stercobilin no longer gives stool its normal brown color. The finding indicates cholestasis, either intrahepatic (hepatitis, cirrhosis) or extrahepatic (bile duct obstruction), and usually accompanies jaundice and dark urine. Cholestasis shows alkaline phosphatase and GGT more than three times normal with aminotransferases usually under 200 U/L, and dark urine may appear before jaundice is visible. Ultrasound is the first imaging test to look for a blocked bile duct.', updated_at = now()
where id = 'sym_pale_stool' and description = 'Pale, clay-colored (acholic) stools result from reduced delivery of bile pigments to the intestine, so that stercobilin no longer gives stool its normal brown color. The finding indicates cholestasis, either intrahepatic (hepatitis, cirrhosis) or extrahepatic (bile duct obstruction), and usually accompanies jaundice and dark urine.';
update public.symptoms set tags = tags || array['acholic']::text[]
where id = 'sym_pale_stool' and not (tags @> array['acholic']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Jaundice'
where id = 'sym_pale_stool' and position('Merck Manual Professional - Jaundice' in source_attribution) = 0;
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_pale_stool', 'Merck Manual Professional - Jaundice', 'Tholey D. Jaundice. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed Aug 2025.', 'https://www.merckmanuals.com/professional/hepatic-and-biliary-disorders/approach-to-the-patient-with-liver-disease/jaundice', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_pale_stool'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pale_stool')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_pale_stool' and url = 'https://www.merckmanuals.com/professional/hepatic-and-biliary-disorders/approach-to-the-patient-with-liver-disease/jaundice');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'hepatitis_b', 'sym_pale_stool', 3::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.symptoms where id = 'sym_pale_stool')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'hepatitis_b' and symptom_id = 'sym_pale_stool');

-- ================================================ sym_pallor  (Pale skin, lips or inner eyelids (pallor))
update public.symptoms set description = 'Unusual paleness of the skin and mucous membranes, best seen in the inner lower eyelids (conjunctivae), palms, nail beds and lips. It most often reflects a reduced hemoglobin concentration (anemia) but can also occur with shock or reduced skin blood flow. Pallor is usually obvious only with severe anemia (hemoglobin under about 7 g/dL), so its absence does not rule anemia out. A reticulocyte count separates low production from blood loss or hemolysis.', updated_at = now()
where id = 'sym_pallor' and description = 'Unusual paleness of the skin and mucous membranes, best seen in the inner lower eyelids (conjunctivae), palms, nail beds and lips. It most often reflects a reduced hemoglobin concentration (anemia) but can also occur with shock or reduced skin blood flow.';
update public.symptoms set tags = tags || array['reticulocytes']::text[]
where id = 'sym_pallor' and not (tags @> array['reticulocytes']::text[]);
update public.symptoms set source_attribution = source_attribution || '; Merck Manual Professional - Evaluation of Anemia'
where id = 'sym_pallor' and position('Merck Manual Professional - Evaluation of Anemia' in source_attribution) = 0;
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_pallor', 'Hemolysis (e.g., malaria)', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_pallor'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pallor')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_pallor' and content = 'Hemolysis (e.g., malaria)');
insert into public.symptom_causes (symptom_id, content, position)
select 'sym_pallor', 'Intestinal worms and schistosomiasis', coalesce((select max(position) + 1 from public.symptom_causes where symptom_id = 'sym_pallor'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pallor')
  and not exists (select 1 from public.symptom_causes where symptom_id = 'sym_pallor' and content = 'Intestinal worms and schistosomiasis');
insert into public.symptom_red_flags (symptom_id, content, position)
select 'sym_pallor', 'Pallor with jaundice and dark urine (possible hemolysis)', coalesce((select max(position) + 1 from public.symptom_red_flags where symptom_id = 'sym_pallor'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pallor')
  and not exists (select 1 from public.symptom_red_flags where symptom_id = 'sym_pallor' and content = 'Pallor with jaundice and dark urine (possible hemolysis)');
insert into public.symptom_references (symptom_id, source_name, citation_text, url, is_mother_book, position)
select 'sym_pallor', 'Merck Manual Professional - Evaluation of Anemia', 'Gerber GF. Evaluation of Anemia. Merck Manual Professional Version. Rahway (NJ): Merck & Co.; reviewed May 2024.', 'https://www.merckmanuals.com/professional/hematology-and-oncology/approach-to-the-patient-with-anemia/evaluation-of-anemia', false, coalesce((select max(position) + 1 from public.symptom_references where symptom_id = 'sym_pallor'), 0)
where exists (select 1 from public.symptoms where id = 'sym_pallor')
  and not exists (select 1 from public.symptom_references where symptom_id = 'sym_pallor' and url = 'https://www.merckmanuals.com/professional/hematology-and-oncology/approach-to-the-patient-with-anemia/evaluation-of-anemia');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'malaria', 'sym_pallor', 4::smallint, false, 0.5::numeric
where exists (select 1 from public.diseases where id = 'malaria')
  and exists (select 1 from public.symptoms where id = 'sym_pallor')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'malaria' and symptom_id = 'sym_pallor');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'schistosomiasis', 'sym_pallor', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'schistosomiasis')
  and exists (select 1 from public.symptoms where id = 'sym_pallor')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'schistosomiasis' and symptom_id = 'sym_pallor');
insert into public.disease_symptoms (disease_id, symptom_id, typical_intensity, is_primary, weight_multiplier)
select 'peptic_ulcer_disease', 'sym_pallor', 2::smallint, false, 0.3::numeric
where exists (select 1 from public.diseases where id = 'peptic_ulcer_disease')
  and exists (select 1 from public.symptoms where id = 'sym_pallor')
  and not exists (select 1 from public.disease_symptoms where disease_id = 'peptic_ulcer_disease' and symptom_id = 'sym_pallor');

update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
